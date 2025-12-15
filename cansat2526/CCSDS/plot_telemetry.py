# -------------------------------------------------------------------------
# Color constants for HTML frame rendering
# -------------------------------------------------------------------------
COLOR_FULL  = "#2ecc71"   # green
COLOR_DELTA = "#3498db"   # blue
COLOR_NOISE = "#e74c3c"   # red
COLOR_META  = "#aaaaaa"   # gray
# Fast telemetry plotter using pyqtgraph
# Usage: python plot_telemetry.py raw_xxx.bin

from pathlib import Path
import sys
import time
import binascii
import os
import re
from datetime import datetime

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

# Qt model/view imports
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSplitter,
    QPlainTextEdit, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton, QTabWidget
)

# Serial (pyserial)
try:
    import serial
    import serial.tools.list_ports
except Exception:
    serial = None

# Frame sync bytes (must match firmware)
SYNC_FULL  = 0xA5   # keyframe / FULL
SYNC_DELTA = 0xA4   # DELTA frame

# Frame lengths (must match firmware)
FULL_FRAME_LEN  = 38
DELTA_FRAME_LEN = 23

def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

def extract_bits_le(buf: bytes, bitpos: int, bits: int) -> int:
    v = 0
    for i in range(bits):
        bi = (bitpos + i) >> 3
        bj = (bitpos + i) & 7
        if buf[bi] & (1 << bj):
            v |= (1 << i)
    return v

def decode_sample(v30: int):
    T_code = (v30 >> 0)  & ((1 << 11) - 1)
    H_code = (v30 >> 11) & ((1 << 7)  - 1)
    P_int  = (v30 >> 18) & 0xFF
    P_frac = (v30 >> 26) & 0x0F

    T = -40.0 + T_code * 0.1
    H = float(H_code)
    P = 822.0 + (P_int * 10 + P_frac) * 0.1
    return T, H, P

def decode_frames(raw: bytes):
    """
    Decode a mixed stream of FULL (38B) and DELTA (23B) frames.

    FULL:
      [0]=0xA5, [1..2]=base_MET(LE), [3]=FLAGS, [4]=SEQ, [5]=VALIDITY,
      [6..35]=bitstream 8×30-bit samples (LSB-first), [36..37]=CRC16(LE) over 0..35.

    DELTA:
      [0]=0xA4, [1..2]=base_MET(LE), [3]=FLAGS, [4]=SEQ, [5]=REF_KEY_SEQ,
      [6..20]=bitstream 8×(dT5 + dRH4 + dP6)=120 bits (LSB-first), [21..22]=CRC16(LE) over 0..20.

    Delta decoding needs the last absolute 30-bit sample from the last decoded frame,
    and a matching last keyframe sequence.
    """
    Ts, Hs, Ps = [], [], []
    keyframe_idx = []
    sample_index = 0

    have_ref = False
    last_abs30 = 0
    last_key_seq = None

    def _twos_comp(val: int, bits: int) -> int:
        sign = 1 << (bits - 1)
        return val - (1 << bits) if (val & sign) else val

    i = 0
    n = len(raw)

    while i < n:
        sync = raw[i]

        if sync == SYNC_FULL:
            flen = FULL_FRAME_LEN
        elif sync == SYNC_DELTA:
            flen = DELTA_FRAME_LEN
        else:
            i += 1
            continue

        if i + flen > n:
            break

        frame = raw[i:i + flen]

        # ------------------------------------------------------------------
        # CRC check
        # ------------------------------------------------------------------
        if sync == SYNC_FULL:
            calc = crc16_ccitt(frame[:36])
            got = frame[36] | (frame[37] << 8)
            if calc != got:
                i += 1
                continue
        else:
            calc = crc16_ccitt(frame[:21])
            got = frame[21] | (frame[22] << 8)
            if calc != got:
                i += 1
                continue

        # ------------------------------------------------------------------
        # Decode
        # ------------------------------------------------------------------
        if sync == SYNC_FULL:
            # FULL keyframe: 8×30-bit absolute samples
            last_key_seq = frame[4]

            bitpos = 6 * 8
            for _ in range(8):
                v30 = extract_bits_le(frame, bitpos, 30)
                bitpos += 30

                last_abs30 = v30
                have_ref = True

                T, H, P = decode_sample(v30)
                Ts.append(T)
                Hs.append(H)
                Ps.append(P)

                keyframe_idx.append(sample_index)
                sample_index += 1

            i += flen
            continue

        # DELTA frame
        seq = frame[4]
        ref_key_seq = frame[5]

        # If receiver starts mid-stream, we must wait for a keyframe.
        # Also drop deltas that reference a different keyframe than our last one.
        if (not have_ref) or (last_key_seq is not None and ref_key_seq != last_key_seq):
            i += flen
            continue

        bitpos = 6 * 8
        prev = last_abs30

        for _ in range(8):
            dT = _twos_comp(extract_bits_le(frame, bitpos, 5), 5)
            bitpos += 5
            dRH = _twos_comp(extract_bits_le(frame, bitpos, 4), 4)
            bitpos += 4
            dP = _twos_comp(extract_bits_le(frame, bitpos, 6), 6)
            bitpos += 6

            # Unpack previous absolute codes
            T_code = (prev & 0x7FF) + dT
            RH_code = ((prev >> 11) & 0x7F) + dRH
            P_int = (prev >> 18) & 0xFF
            P_frac = (prev >> 26) & 0x0F
            if P_frac > 9:
                P_frac = 9
            P_code12 = (P_int * 10 + P_frac) + dP

            # Clamp to valid ranges (prevents runaway on a single corrupted delta)
            if T_code < 0:
                T_code = 0
            elif T_code > 0x7FF:
                T_code = 0x7FF

            if RH_code < 0:
                RH_code = 0
            elif RH_code > 0x7F:
                RH_code = 0x7F

            if P_code12 < 0:
                P_code12 = 0
            elif P_code12 > 2550:
                P_code12 = 2550

            P_int = P_code12 // 10
            P_frac = P_code12 % 10

            v30 = (T_code & 0x7FF) | ((RH_code & 0x7F) << 11) | ((P_int & 0xFF) << 18) | ((P_frac & 0x0F) << 26)

            prev = v30
            last_abs30 = v30
            have_ref = True

            T, H, P = decode_sample(v30)
            Ts.append(T)
            Hs.append(H)
            Ps.append(P)
            sample_index += 1

        i += flen

    return Ts, Hs, Ps, keyframe_idx

def _set_led(lbl: QLabel, on: bool, color_on: str):
    if on:
        lbl.setStyleSheet(
            "QLabel { background-color: %s; color: black; border: 1px solid #666;"
            " border-radius: 4px; padding: 2px 6px; font-weight: bold; }"
            % color_on
        )
    else:
        lbl.setStyleSheet(
            "QLabel { background-color: #333; color: #aaa; border: 1px solid #666;"
            " border-radius: 4px; padding: 2px 6px; }"
        )

def _msg(parent, title: str, text: str):
    QtWidgets.QMessageBox.information(parent, title, text)

def _warn(parent, title: str, text: str):
    QtWidgets.QMessageBox.warning(parent, title, text)

def main():
    app = QtWidgets.QApplication([])

    # Main window
    win = QtWidgets.QWidget()
    win.setWindowTitle("AstroLink – Telemetry Ground Station")
    win.resize(1200, 900)

    layout = QVBoxLayout(win)

    # -------------------------------------------------------------------------
    # Top control bar: OFFLINE/ONLINE + serial + logging
    # -------------------------------------------------------------------------
    top = QHBoxLayout()
    layout.addLayout(top)

    mode_cb = QComboBox()
    mode_cb.addItems(["OFFLINE", "ONLINE"])
    top.addWidget(QLabel("Mode:"))
    top.addWidget(mode_cb)

    port_cb = QComboBox()
    port_cb.setMinimumWidth(260)
    top.addWidget(QLabel("Port:"))
    top.addWidget(port_cb)

    btn_refresh_ports = QPushButton("Refresh")
    top.addWidget(btn_refresh_ports)

    btn_connect = QPushButton("Connect")
    btn_disconnect = QPushButton("Disconnect")
    btn_disconnect.setEnabled(False)
    top.addWidget(btn_connect)
    top.addWidget(btn_disconnect)

    top.addWidget(QLabel("RX:"))
    led_rx = QLabel("")
    led_rx.setText("RX")
    led_rx.setAlignment(Qt.AlignCenter)
    top.addWidget(led_rx)
    top.addWidget(QLabel("CONNECTED:"))
    led_conn = QLabel("")
    led_conn.setText("OK")
    led_conn.setAlignment(Qt.AlignCenter)
    top.addWidget(led_conn)

    lbl_bytes = QLabel("Bytes: 0")
    lbl_bytes.setFixedWidth(120)
    lbl_bytes.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
    lbl_bytes.setAlignment(Qt.AlignCenter)
    top.addWidget(lbl_bytes)

    lbl_status = QLabel("Status: idle")
    lbl_status.setFixedWidth(420)
    lbl_status.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
    lbl_status.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    top.addWidget(lbl_status)

    btn_log = QPushButton("LOG")
    btn_log.setCheckable(True)
    btn_log.setEnabled(False)
    top.addWidget(btn_log)

    top.addStretch(1)

    # -------------------------------------------------------------------------
    # Main content area
    # -------------------------------------------------------------------------
    splitter = QSplitter(Qt.Vertical)
    layout.addWidget(splitter, 1)

    # Offline file list chooser (OFFLINE mode)
    from PyQt5.QtWidgets import QListWidget

    file_box = QtWidgets.QWidget()
    file_box_layout = QHBoxLayout(file_box)
    file_box_layout.setContentsMargins(0, 0, 0, 0)

    file_list = QListWidget()
    file_list.setMaximumHeight(120)
    file_box_layout.addWidget(file_list, 1)


    plot_toggle = QPushButton("H")
    plot_toggle.setCheckable(True)
    plot_toggle.setChecked(True)  # startup: Horizontal
    plot_toggle.setMinimumSize(32, 28)
    plot_toggle.setToolTip("Grafikon elrendezés váltása\nH = Horizontal, V = Vertical")
    plot_toggle.setFont(QtGui.QFont("Menlo", 10, QtGui.QFont.Bold))
    toggle_box = QtWidgets.QWidget()
    toggle_layout = QVBoxLayout(toggle_box)
    toggle_layout.setContentsMargins(0, 0, 0, 0)
    toggle_layout.setSpacing(2)

    toggle_label = QLabel("Graph layout")
    toggle_label.setAlignment(Qt.AlignCenter)
    toggle_label.setStyleSheet("font-size: 9px; color: #888;")

    toggle_layout.addWidget(plot_toggle, 0, Qt.AlignCenter)
    toggle_layout.addWidget(toggle_label, 0, Qt.AlignCenter)

    file_box_layout.addWidget(toggle_box, 0, Qt.AlignBottom)

    layout.addWidget(file_box)

    def refresh_file_list():
        file_list.clear()
        files = [f for f in sorted(os.listdir(os.getcwd())) if f.lower().endswith(".bin")]
        for fname in files:
            item = QtWidgets.QListWidgetItem()
            item.setData(Qt.UserRole, fname)
            item.setSizeHint(QtCore.QSize(200, 26))
            file_list.addItem(item)

            row_widget = QtWidgets.QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(6, 0, 6, 0)
            row_layout.setSpacing(6)

            lbl = QLabel(fname)
            lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

            btn_del = QPushButton("✕")
            btn_del.setFixedSize(22, 22)
            btn_del.setToolTip("Delete this BIN file")
            btn_del.setStyleSheet(
                "QPushButton { color: #b00020; font-weight: bold; }"
                "QPushButton:hover { background-color: #ffdddd; }"
            )
            btn_del.hide()

            def _make_delete_cb(fn=fname):
                def _cb():
                    ret = QtWidgets.QMessageBox.question(
                        win,
                        "Delete file",
                        f"Delete file?\n\n{fn}",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )
                    if ret != QtWidgets.QMessageBox.Yes:
                        return
                    try:
                        os.remove(os.path.join(os.getcwd(), fn))
                    except Exception as e:
                        _warn(win, "Delete failed", str(e))
                        return
                    refresh_file_list()
                    lbl_status.setText(f"Status: deleted {fn}")
                return _cb

            btn_del.clicked.connect(_make_delete_cb())

            row_layout.addWidget(lbl, 1)
            row_layout.addWidget(btn_del, 0, Qt.AlignRight)

            file_list.setItemWidget(item, row_widget)

            def _enter_event(_e, b=btn_del):
                b.show()

            def _leave_event(_e, b=btn_del):
                b.hide()

            row_widget.enterEvent = _enter_event
            row_widget.leaveEvent = _leave_event

    tabs = QTabWidget()
    splitter.addWidget(tabs)

    # Table view for decoded samples (Decoded tab)
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Index", "Temp (°C)", "Hum (%)", "Press (hPa)"])
    table.horizontalHeader().setStretchLastSection(True)
    tabs.addTab(table, "Decoded samples")

    # Raw view tab (shows incoming/raw bytes + frame summaries)
    fixed_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
    fixed_font.setFamily("Menlo")
    fixed_font.setStyleHint(QtGui.QFont.Monospace)
    raw_splitter = QSplitter(Qt.Horizontal)

    raw_human_view = QtWidgets.QTextEdit()
    raw_human_view.setFont(fixed_font)
    raw_human_view.setReadOnly(True)
    raw_human_view.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
    raw_human_view.setAcceptRichText(True)

    raw_hex_view = QtWidgets.QTextEdit()
    raw_hex_view.setFont(fixed_font)
    raw_hex_view.setReadOnly(True)
    raw_hex_view.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
    raw_hex_view.setAcceptRichText(True)

    raw_splitter.addWidget(raw_human_view)
    raw_splitter.addWidget(raw_hex_view)
    raw_splitter.setSizes([600, 600])

    tabs.addTab(raw_splitter, "Raw stream")

    # Frame Inspector tab (QTableWidget)
    frame_table = QTableWidget()
    frame_table.setColumnCount(6)
    frame_table.setHorizontalHeaderLabels(["#", "Type", "SEQ", "REF", "CRC", "Status"])
    frame_table.horizontalHeader().setStretchLastSection(True)
    frame_table.setSelectionBehavior(QTableWidget.SelectRows)
    frame_table.setSelectionMode(QTableWidget.SingleSelection)
    frame_table.setFocusPolicy(Qt.StrongFocus)

    # Add explanation panel under frame_table
    frame_explain = QLabel("Select a frame to see explanation.")
    frame_explain.setWordWrap(True)
    frame_explain.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
    frame_explain.setMinimumHeight(80)

    frame_container = QtWidgets.QWidget()
    frame_layout = QVBoxLayout(frame_container)
    frame_layout.setContentsMargins(4, 4, 4, 4)
    frame_layout.addWidget(frame_table)
    frame_layout.addWidget(frame_explain)

    tabs.addTab(frame_container, "Frame Inspector")
    # Frame diagnostic record:
    # {
    #   type: "FULL" | "DELTA",
    #   seq: int,
    #   ref_seq: Optional[int],
    #   crc_ok: bool,
    #   status: "ACCEPTED" | "DROPPED_NO_REF" | "DROPPED_CRC" | "DROPPED_REF_MISMATCH"
    # }

    def decode_frames_verbose(raw: bytes):
        """
        Like decode_frames, but returns frame-level diagnostics.
        Returns: Ts, Hs, Ps, keyframe_idx, frames_diag
        """
        Ts, Hs, Ps = [], [], []
        keyframe_idx = []
        sample_index = 0
        frames_diag = []

        have_ref = False
        last_abs30 = 0
        last_key_seq = None

        def _twos_comp(val: int, bits: int) -> int:
            sign = 1 << (bits - 1)
            return val - (1 << bits) if (val & sign) else val

        i = 0
        n = len(raw)
        frame_num = 0
        while i < n:
            sync = raw[i]
            if sync == SYNC_FULL:
                flen = FULL_FRAME_LEN
                ftype = "FULL"
            elif sync == SYNC_DELTA:
                flen = DELTA_FRAME_LEN
                ftype = "DELTA"
            else:
                i += 1
                continue

            if i + flen > n:
                break

            frame = raw[i:i + flen]

            # CRC check
            if sync == SYNC_FULL:
                calc = crc16_ccitt(frame[:36])
                got = frame[36] | (frame[37] << 8)
                crc_ok = (calc == got)
            else:
                calc = crc16_ccitt(frame[:21])
                got = frame[21] | (frame[22] << 8)
                crc_ok = (calc == got)

            if not crc_ok:
                diag = {
                    "type": ftype,
                    "seq": frame[4] if flen > 4 else None,
                    "ref_seq": frame[5] if (ftype == "DELTA" and flen > 5) else None,
                    "crc_ok": False,
                    "status": "DROPPED_CRC"
                }
                frames_diag.append(diag)
                i += 1
                frame_num += 1
                continue

            if sync == SYNC_FULL:
                last_key_seq = frame[4]
                bitpos = 6 * 8
                for _ in range(8):
                    v30 = extract_bits_le(frame, bitpos, 30)
                    bitpos += 30
                    last_abs30 = v30
                    have_ref = True
                    T, H, P = decode_sample(v30)
                    Ts.append(T)
                    Hs.append(H)
                    Ps.append(P)
                    keyframe_idx.append(sample_index)
                    sample_index += 1
                diag = {
                    "type": "FULL",
                    "seq": frame[4],
                    "ref_seq": None,
                    "crc_ok": True,
                    "status": "ACCEPTED"
                }
                frames_diag.append(diag)
                i += flen
                frame_num += 1
                continue

            # DELTA frame
            seq = frame[4]
            ref_key_seq = frame[5]
            # If receiver starts mid-stream, we must wait for a keyframe.
            # Also drop deltas that reference a different keyframe than our last one.
            if not have_ref:
                diag = {
                    "type": "DELTA",
                    "seq": seq,
                    "ref_seq": ref_key_seq,
                    "crc_ok": True,
                    "status": "DROPPED_NO_REF"
                }
                frames_diag.append(diag)
                i += flen
                frame_num += 1
                continue
            if last_key_seq is not None and ref_key_seq != last_key_seq:
                diag = {
                    "type": "DELTA",
                    "seq": seq,
                    "ref_seq": ref_key_seq,
                    "crc_ok": True,
                    "status": "DROPPED_REF_MISMATCH"
                }
                frames_diag.append(diag)
                i += flen
                frame_num += 1
                continue

            bitpos = 6 * 8
            prev = last_abs30
            for _ in range(8):
                dT = _twos_comp(extract_bits_le(frame, bitpos, 5), 5)
                bitpos += 5
                dRH = _twos_comp(extract_bits_le(frame, bitpos, 4), 4)
                bitpos += 4
                dP = _twos_comp(extract_bits_le(frame, bitpos, 6), 6)
                bitpos += 6
                T_code = (prev & 0x7FF) + dT
                RH_code = ((prev >> 11) & 0x7F) + dRH
                P_int = (prev >> 18) & 0xFF
                P_frac = (prev >> 26) & 0x0F
                if P_frac > 9:
                    P_frac = 9
                P_code12 = (P_int * 10 + P_frac) + dP
                # Clamp ranges
                if T_code < 0:
                    T_code = 0
                elif T_code > 0x7FF:
                    T_code = 0x7FF
                if RH_code < 0:
                    RH_code = 0
                elif RH_code > 0x7F:
                    RH_code = 0x7F
                if P_code12 < 0:
                    P_code12 = 0
                elif P_code12 > 2550:
                    P_code12 = 2550
                P_int = P_code12 // 10
                P_frac = P_code12 % 10
                v30 = (T_code & 0x7FF) | ((RH_code & 0x7F) << 11) | ((P_int & 0xFF) << 18) | ((P_frac & 0x0F) << 26)
                prev = v30
                last_abs30 = v30
                have_ref = True
                T, H, P = decode_sample(v30)
                Ts.append(T)
                Hs.append(H)
                Ps.append(P)
                sample_index += 1
            diag = {
                "type": "DELTA",
                "seq": seq,
                "ref_seq": ref_key_seq,
                "crc_ok": True,
                "status": "ACCEPTED"
            }
            frames_diag.append(diag)
            i += flen
            frame_num += 1
        return Ts, Hs, Ps, keyframe_idx, frames_diag

    # Plot area container with toggle for orientation
    plot_container = QtWidgets.QWidget()
    plot_layout = QtWidgets.QVBoxLayout(plot_container)
    plot_layout.setContentsMargins(0, 0, 0, 0)
    splitter.addWidget(plot_container)

    plots = pg.GraphicsLayoutWidget()
    plot_layout.addWidget(plots, 1)

    # Init LEDs
    _set_led(led_rx, False, "#00ccff")
    _set_led(led_conn, False, "#00cc00")

    # Placeholders for curves and markers (will be assigned in rebuild_plots)
    t_curve = None
    h_curve = None
    p_curve = None
    t_marker = None
    h_marker = None
    p_marker = None
    t_kf = None
    h_kf = None
    p_kf = None

    marker_pen = pg.mkPen(color=(255, 255, 0), width=2)
    kf_scatter_pen = pg.mkPen(None)
    kf_scatter_brush = pg.mkBrush(255, 255, 0, 120)

    def rebuild_plots(horizontal: bool):
        nonlocal t_curve, h_curve, p_curve
        nonlocal t_marker, h_marker, p_marker
        nonlocal t_kf, h_kf, p_kf
        # Preserve current data before rebuild
        Ts_cur = t_curve.yData if t_curve is not None else []
        Hs_cur = h_curve.yData if h_curve is not None else []
        Ps_cur = p_curve.yData if p_curve is not None else []
        # Preserve marker positions
        t_marker_pos = t_marker.value() if t_marker is not None else None
        h_marker_pos = h_marker.value() if h_marker is not None else None
        p_marker_pos = p_marker.value() if p_marker is not None else None
        # Preserve keyframe scatter data
        t_kf_x, t_kf_y = t_kf.getData() if t_kf is not None else ([], [])
        h_kf_x, h_kf_y = h_kf.getData() if h_kf is not None else ([], [])
        p_kf_x, p_kf_y = p_kf.getData() if p_kf is not None else ([], [])
        plots.clear()
        if not horizontal:
            p1 = plots.addPlot(title="Temperature (°C)")
            t_curve = p1.plot([], pen='r')
            plots.nextRow()
            p2 = plots.addPlot(title="Humidity (%)")
            h_curve = p2.plot([], pen='g')
            plots.nextRow()
            p3 = plots.addPlot(title="Pressure (hPa)")
            p_curve = p3.plot([], pen='b')
        else:
            p1 = plots.addPlot(title="Temperature (°C)")
            p2 = plots.addPlot(title="Humidity (%)")
            p3 = plots.addPlot(title="Pressure (hPa)")
            t_curve = p1.plot([], pen='r')
            h_curve = p2.plot([], pen='g')
            p_curve = p3.plot([], pen='b')

        t_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
        h_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
        p_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
        p1.addItem(t_marker)
        p2.addItem(h_marker)
        p3.addItem(p_marker)

        t_kf = pg.ScatterPlotItem(size=8, pen=kf_scatter_pen, brush=kf_scatter_brush)
        h_kf = pg.ScatterPlotItem(size=8, pen=kf_scatter_pen, brush=kf_scatter_brush)
        p_kf = pg.ScatterPlotItem(size=8, pen=kf_scatter_pen, brush=kf_scatter_brush)
        p1.addItem(t_kf)
        p2.addItem(h_kf)
        p3.addItem(p_kf)
        # Restore data after rebuild
        if Ts_cur is not None and len(Ts_cur) > 0:
            t_curve.setData(Ts_cur)
        if Hs_cur is not None and len(Hs_cur) > 0:
            h_curve.setData(Hs_cur)
        if Ps_cur is not None and len(Ps_cur) > 0:
            p_curve.setData(Ps_cur)
        # Restore keyframe scatter data
        if t_kf_x is not None and len(t_kf_x) > 0:
            t_kf.setData(t_kf_x, t_kf_y)
        if h_kf_x is not None and len(h_kf_x) > 0:
            h_kf.setData(h_kf_x, h_kf_y)
        if p_kf_x is not None and len(p_kf_x) > 0:
            p_kf.setData(p_kf_x, p_kf_y)

        # Restore marker positions
        if t_marker_pos is not None:
            t_marker.setPos(t_marker_pos)
        if h_marker_pos is not None:
            h_marker.setPos(h_marker_pos)
        if p_marker_pos is not None:
            p_marker.setPos(p_marker_pos)

    def plot_clicked(evt):
        # `evt.currentItem` can be a PlotItem, ViewBox, or other graphics item depending on where you click.
        item = getattr(evt, "currentItem", None)
        if item is None:
            return

        # Prefer a ViewBox for coordinate mapping
        if hasattr(item, "mapSceneToView"):
            vb = item
        elif hasattr(item, "vb"):
            vb = item.vb
        else:
            return

        try:
            mousePoint = vb.mapSceneToView(evt.scenePos())
        except Exception:
            return

        idx = int(round(mousePoint.x()))
        if 0 <= idx < table.rowCount():
            table.selectRow(idx)

    plots.scene().sigMouseClicked.connect(plot_clicked)

    # Connect toggle and initialize layout
    def _on_plot_toggle(checked):
        # checked == True  -> Horizontal
        # checked == False -> Vertical
        plot_toggle.setText("H" if checked else "V")
        rebuild_plots(checked)

    plot_toggle.toggled.connect(_on_plot_toggle)

    rebuild_plots(True)  # Startup: Horizontal layout

    # -------------------------------------------------------------------------
    # ONLINE/OFFLINE state
    # -------------------------------------------------------------------------
    ser = None
    # raw_rx_buffer: stores whatever we received (for raw tab display)
    raw_rx_buffer = bytearray()

    # raw_buffer: BINARY stream used for decode_frames()
    raw_buffer = bytearray()

    have_new_bytes = False
    total_bytes = 0

    log_fp = None
    log_path = None

    def refresh_ports():
        port_cb.clear()
        if serial is None:
            port_cb.addItem("pyserial not installed")
            return
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            port_cb.addItem("(no ports)")
            return
        for p in ports:
            # Show both device and description
            port_cb.addItem(f"{p.device} — {p.description}", p.device)
        # Auto-select likely ESP32 port if present
        dev = _auto_pick_port()
        if dev is not None:
            for idx in range(port_cb.count()):
                if port_cb.itemData(idx) == dev:
                    port_cb.setCurrentIndex(idx)
                    break

    def set_mode_ui():
        m = mode_cb.currentText()
        offline = (m == "OFFLINE")
        file_list.setEnabled(offline)
        port_cb.setEnabled(not offline)
        btn_refresh_ports.setEnabled(not offline)
        btn_connect.setEnabled(not offline and ser is None)
        btn_disconnect.setEnabled(not offline and ser is not None)
        btn_log.setEnabled(not offline and ser is not None)
        tabs.setCurrentIndex(0)

    def append_raw_debug(text: str):
        # keep raw view lightweight: append and trim to last ~2000 lines
        raw_human_view.append(text)
        doc = raw_human_view.document()
        if doc.blockCount() > 2000:
            cursor = QtWidgets.QTextCursor(doc)
            cursor.movePosition(QtWidgets.QTextCursor.Start)
            cursor.select(QtWidgets.QTextCursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    def render_raw_tail(buf: bytes, tail: int = 256) -> str:
        t = buf[-tail:] if len(buf) > tail else buf
        return binascii.hexlify(t).decode("ascii")

    def render_hex_dump(buf: bytes, bytes_per_row: int = 16) -> str:
        """
        Render buffer as a classic HEX dump:
        0000: A5 01 02 ...
        """
        lines = []
        for i in range(0, len(buf), bytes_per_row):
            chunk = buf[i:i + bytes_per_row]
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            lines.append(f"{i:04X}: {hex_part}")
        return "\n".join(lines)

    def render_hex_one_line(buf: bytes) -> str:
        """
        Render a buffer as ONE LINE hex stream, space-separated.
        Example: A5 D6 3A 1D 00 07 ...
        """
        return " ".join(f"{b:02X}" for b in buf)

    # -------------------------------------------------------------------------
    # HTML-safe helpers for colored frame rendering
    # -------------------------------------------------------------------------
    def html_line(text: str, color: str) -> str:
        return f'<span style="color:{color}; font-family: Menlo, Consolas, DejaVu Sans Mono;">{text}</span>'

    def render_hex_frames(buf: bytes) -> str:
        """
        Human-readable frame-oriented HEX view.
        Groups bytes by FULL / DELTA frames and annotates headers.
        """
        lines = []
        i = 0
        n = len(buf)
        while i < n:
            b = buf[i]
            if b == SYNC_FULL and i + FULL_FRAME_LEN <= n:
                frame = buf[i:i + FULL_FRAME_LEN]
                seq = frame[4]
                lines.append(f"[FULL ] @0x{i:04X}  SEQ={seq}")
                lines.append(render_hex_dump(frame))
                i += FULL_FRAME_LEN
                continue
            if b == SYNC_DELTA and i + DELTA_FRAME_LEN <= n:
                frame = buf[i:i + DELTA_FRAME_LEN]
                seq = frame[4]
                ref = frame[5]
                lines.append(f"[DELTA] @0x{i:04X}  SEQ={seq}  REF={ref}")
                lines.append(render_hex_dump(frame))
                i += DELTA_FRAME_LEN
                continue
            # Unknown / noise byte
            lines.append(f"[NOISE] @0x{i:04X}: {b:02X}")
            i += 1
        return "\n".join(lines)

    def render_hex_frames_colored(buf: bytes) -> str:
        """
        HTML-colored frame-oriented HEX view.
        Groups bytes by FULL / DELTA frames and annotates headers, using color.
        """
        lines = []
        i = 0
        n = len(buf)
        while i < n:
            b = buf[i]
            if b == SYNC_FULL and i + FULL_FRAME_LEN <= n:
                frame = buf[i:i + FULL_FRAME_LEN]
                seq = frame[4]
                lines.append(html_line(
                    f"[FULL ] @0x{i:04X}  SEQ={seq} | {render_hex_one_line(frame)}",
                    COLOR_FULL
                ))
                i += FULL_FRAME_LEN
                continue
            if b == SYNC_DELTA and i + DELTA_FRAME_LEN <= n:
                frame = buf[i:i + DELTA_FRAME_LEN]
                seq = frame[4]
                ref = frame[5]
                lines.append(html_line(
                    f"[DELTA] @0x{i:04X}  SEQ={seq} REF={ref} | {render_hex_one_line(frame)}",
                    COLOR_DELTA
                ))
                i += DELTA_FRAME_LEN
                continue
            # Collect consecutive NOISE bytes into one row (up to 32 bytes)
            start = i
            chunk = [b]
            i += 1
            while i < n and buf[i] not in (SYNC_FULL, SYNC_DELTA) and len(chunk) < 32:
                chunk.append(buf[i])
                i += 1

            hexline = " ".join(f"{x:02X}" for x in chunk)
            lines.append(html_line(
                f"[NOISE] @0x{start:04X}  {hexline}",
                COLOR_NOISE
            ))
        return "<br>".join(lines)

    def render_human_frames(buf: bytes) -> str:
        out = []
        i = 0
        n = len(buf)

        while i < n:
            b = buf[i]

            # ---------------- FULL FRAME ----------------
            if b == SYNC_FULL and i + FULL_FRAME_LEN <= n:
                frame = buf[i:i + FULL_FRAME_LEN]
                seq = frame[4]
                met = frame[1] | (frame[2] << 8)

                out.append("────────────────────────────────────────")
                out.append(f"FULL FRAME   #{seq}")
                out.append("────────────────────────────────────────")
                out.append("ID        : FULL (0xA5)")
                out.append(f"SEQ       : {seq}")
                out.append(f"MET       : {met} ticks (0.5 s / tick)")
                out.append(f"MET (sec) : {met * 0.5:.1f} s")
                out.append(f"FLAGS     : 0x{frame[3]:02X}")
                out.append(f"VALID     : {frame[5]} samples")
                out.append("DATA:")

                bitpos = 6 * 8
                for s in range(8):
                    v30 = extract_bits_le(frame, bitpos, 30)
                    bitpos += 30
                    T, H, P = decode_sample(v30)
                    out.append(f"  [{s}]  T={T:5.2f} °C   RH={H:4.1f} %   P={P:7.2f} hPa")

                out.append("HEX:")
                out.append(render_hex_one_line(frame))
                i += FULL_FRAME_LEN
                continue

            # ---------------- DELTA FRAME ----------------
            if b == SYNC_DELTA and i + DELTA_FRAME_LEN <= n:
                frame = buf[i:i + DELTA_FRAME_LEN]
                seq = frame[4]
                ref = frame[5]

                out.append("────────────────────────────────────────")
                out.append(f"DELTA FRAME  #{seq}")
                out.append("────────────────────────────────────────")
                out.append("ID        : DELTA (0xA4)")
                out.append(f"SEQ       : {seq}")
                out.append(f"REF KEY   : {ref}")
                out.append("HEX:")
                out.append(render_hex_one_line(frame))
                i += DELTA_FRAME_LEN
                continue

            # ---------------- NOISE ----------------
            start = i
            chunk = [b]
            i += 1
            while i < n and buf[i] not in (SYNC_FULL, SYNC_DELTA) and len(chunk) < 32:
                chunk.append(buf[i])
                i += 1

            out.append("────────────────────────────────────────")
            out.append("NOISE BLOCK")
            out.append(f"Offset    : 0x{start:04X}")
            out.append(f"Bytes     : {' '.join(f'{x:02X}' for x in chunk)}")

        return "\n".join(out)

    # -------------------------------------------------------------------------
    # ASCII-HEX stream support (some firmwares print payload as hex text)
    # -------------------------------------------------------------------------
    _hex_re = re.compile(r"[0-9A-Fa-f]{2}")

    ascii_hex_buf = ""

    def _likely_ascii_hex(data: bytes) -> bool:
        if not data:
            return False
        # If most bytes are printable/whitespace, assume it may be text
        printable = sum((32 <= b <= 126) or b in (9, 10, 13) for b in data)
        return (printable / max(1, len(data))) > 0.85

    def _extract_hex_bytes_from_text(txt: str):
        """
        Returns (bin_bytes, leftover_txt)
        Extract contiguous hex pairs from txt, convert them to bytes.
        Keeps any trailing incomplete hex pair text as leftover.
        """
        pairs = _hex_re.findall(txt)
        if not pairs:
            # keep buffer bounded
            return b"", txt[-4096:]

        # Convert all pairs we found
        hex_str = "".join(pairs)
        try:
            out = bytes.fromhex(hex_str)
        except Exception:
            out = b""

        # Best-effort leftover: keep last 256 chars (for incomplete next chunk)
        return out, txt[-256:]

    def normalize_to_binary_stream(raw: bytes) -> bytes:
        """
        If raw looks like ASCII hex dump, convert it to the real binary stream.
        Otherwise return raw unchanged.
        """
        # Fast-path: already looks like a pure binary frame stream
        if raw and raw[0] in (SYNC_FULL, SYNC_DELTA):
            if (len(raw) % FULL_FRAME_LEN == 0) or (len(raw) % DELTA_FRAME_LEN == 0):
                return raw
        if _likely_ascii_hex(raw):
            try:
                txt = raw.decode("ascii", errors="ignore")
            except Exception:
                return raw
            out, _ = _extract_hex_bytes_from_text(txt)
            return out if out else raw
        return raw

    def update_from_raw():
        # Decode whatever we have; this is used by BOTH offline load and online stream
        nonlocal have_new_bytes
        if not raw_buffer:
            return
        Ts, Hs, Ps, keyframes, frames_diag = decode_frames_verbose(bytes(raw_buffer))

        # Fill table
        table.setRowCount(len(Ts))
        keyset = set(keyframes)
        for i in range(len(Ts)):
            table.setItem(i, 0, QTableWidgetItem(str(i)))
            table.setItem(i, 1, QTableWidgetItem(f"{Ts[i]:.2f}"))
            table.setItem(i, 2, QTableWidgetItem(f"{Hs[i]:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{Ps[i]:.2f}"))
            if i in keyset:
                for c in range(4):
                    table.item(i, c).setBackground(QtGui.QColor(50, 50, 0, 140))

        # Update plots
        if t_curve is not None:
            t_curve.setData(Ts)
        if h_curve is not None:
            h_curve.setData(Hs)
        if p_curve is not None:
            p_curve.setData(Ps)

        if t_kf is not None:
            t_kf.setData(keyframes, [Ts[i] for i in keyframes])
        if h_kf is not None:
            h_kf.setData(keyframes, [Hs[i] for i in keyframes])
        if p_kf is not None:
            p_kf.setData(keyframes, [Ps[i] for i in keyframes])

        lbl_status.setText(
            f"Status: decoded_samples={len(Ts)}  keyframes={len(keyframes)}  bin_bytes={len(raw_buffer)}"
        )

        # Raw stream info (only when Raw tab is visible or ONLINE mode)
        if mode_cb.currentText() == "ONLINE" or tabs.currentIndex() == 1:
            append_raw_debug(f"[INFO] bin_bytes={len(raw_buffer)}  decoded_samples={len(Ts)}  keyframes={len(keyframes)}")

        # Populate frame inspector table
        frame_table.setRowCount(len(frames_diag))
        for idx, diag in enumerate(frames_diag):
            # Columns: ["#", "Type", "SEQ", "REF", "CRC", "Status"]
            frame_table.setItem(idx, 0, QTableWidgetItem(str(idx)))
            frame_table.setItem(idx, 1, QTableWidgetItem(str(diag.get("type", ""))))
            frame_table.setItem(idx, 2, QTableWidgetItem(str(diag.get("seq", ""))))
            ref_val = str(diag.get("ref_seq", "")) if diag.get("type") == "DELTA" else ""
            frame_table.setItem(idx, 3, QTableWidgetItem(ref_val))
            crc_val = "OK" if diag.get("crc_ok", False) else "FAIL"
            frame_table.setItem(idx, 4, QTableWidgetItem(crc_val))
            frame_table.setItem(idx, 5, QTableWidgetItem(str(diag.get("status", ""))))
            # Tint dropped rows red
            if diag.get("status") != "ACCEPTED":
                for c in range(6):
                    item = frame_table.item(idx, c)
                    if item is not None:
                        item.setBackground(QtGui.QColor(255, 128, 128, 120))

        have_new_bytes = False

    # Timers: serial poll + decode throttle
    serial_timer = QtCore.QTimer()
    serial_timer.setInterval(20)

    decode_timer = QtCore.QTimer()
    decode_timer.setInterval(200)  # 5 Hz update; stable

    def serial_poll():
        nonlocal have_new_bytes, total_bytes, raw_rx_buffer, raw_buffer, ascii_hex_buf
        if ser is None:
            return
        try:
            waiting = ser.in_waiting
        except Exception:
            waiting = 0
        if waiting <= 0:
            return

        try:
            chunk = ser.read(min(4096, waiting))
        except Exception as e:
            append_raw_debug(f"[ERR] serial read failed: {e}")
            return

        if not chunk:
            return

        # Keep original RX stream for inspection
        raw_rx_buffer.extend(chunk)

        # Convert to binary stream for decoder if this looks like ASCII hex text
        bin_chunk = b""
        if _likely_ascii_hex(chunk):
            ascii_hex_buf += chunk.decode("ascii", errors="ignore")
            bin_chunk, ascii_hex_buf = _extract_hex_bytes_from_text(ascii_hex_buf)
        else:
            bin_chunk = chunk

        # Append to binary decode buffer
        if bin_chunk:
            # Guard: ignore boot noise until first SYNC byte
            if SYNC_FULL not in bin_chunk and SYNC_DELTA not in bin_chunk and not raw_buffer:
                return
            raw_buffer.extend(bin_chunk)
            have_new_bytes = True

            # Logging: save the binary stream (not the ASCII text)
            if log_fp is not None:
                try:
                    log_fp.write(bin_chunk)
                    log_fp.flush()
                except Exception as e:
                    append_raw_debug(f"[ERR] log write failed: {e}")

        total_bytes += len(chunk)
        lbl_bytes.setText(f"Bytes: {total_bytes}")
        lbl_status.setText(f"Status: online rx (raw_bytes={total_bytes}  bin_bytes={len(raw_buffer)})")

        # RX LED flash
        _set_led(led_rx, True, "#00ccff")
        QtCore.QTimer.singleShot(80, lambda: _set_led(led_rx, False, "#00ccff"))

    def decode_tick():
        if have_new_bytes:
            update_from_raw()
        # Show human-readable frame view in ONLINE mode, Raw stream tab
        if tabs.currentIndex() == 1:  # Raw stream tab
            raw_human_view.clear()
            raw_human_view.append("[FRAME VIEW – ONLINE STREAM]")
            raw_human_view.append(render_human_frames(bytes(raw_buffer)))

            raw_hex_view.clear()
            raw_hex_view.append(render_hex_frames_colored(bytes(raw_buffer)))

    serial_timer.timeout.connect(serial_poll)
    decode_timer.timeout.connect(decode_tick)

    def load_file():
        nonlocal raw_rx_buffer, raw_buffer, total_bytes, have_new_bytes
        item = file_list.currentItem()
        if item is None:
            return

        fname = item.data(Qt.UserRole)
        if not fname:
            return

        path = os.path.join(os.getcwd(), fname)

        raw = Path(path).read_bytes()
        raw_bin = normalize_to_binary_stream(raw)
        raw_rx_buffer = bytearray(raw)  # keep original for inspection
        raw_buffer = bytearray(raw_bin)
        total_bytes = len(raw_rx_buffer)
        lbl_bytes.setText(f"Bytes: {total_bytes}")
        have_new_bytes = True

        # Safety check: ensure full file is kept for decode
        if len(raw_buffer) < len(raw_rx_buffer):
            append_raw_debug("[WARN] Binary stream shorter than original (possible ASCII-HEX normalization)")

        raw_human_view.clear()
        raw_hex_view.clear()
        append_raw_debug(f"[INFO] OFFLINE file loaded: {path}")
        append_raw_debug(f"[INFO] Raw bytes loaded (original): {len(raw_rx_buffer)}")
        append_raw_debug(f"[INFO] Binary bytes for decode: {len(raw_buffer)}")
        append_raw_debug("[FRAME VIEW – OFFLINE FILE]")
        raw_human_view.append(render_human_frames(raw_buffer))
        raw_hex_view.append(render_hex_frames_colored(raw_buffer))
        lbl_status.setText("Status: offline file loaded")
        update_from_raw()

    def on_table_select():
        row = table.currentRow()
        if row < 0:
            return
        if t_marker is not None:
            t_marker.setPos(row)
        if h_marker is not None:
            h_marker.setPos(row)
        if p_marker is not None:
            p_marker.setPos(row)

    def on_frame_select(row_override=None):
        if row_override is not None:
            row = row_override
        else:
            row = frame_table.currentRow()
        if row < 0:
            return

        ftype = frame_table.item(row, 1).text()
        seq = frame_table.item(row, 2).text()
        ref = frame_table.item(row, 3).text()
        status = frame_table.item(row, 5).text()

        if ftype == "FULL":
            txt = (
                f"FULL FRAME #{seq}\n"
                "This is a keyframe containing full absolute sensor data.\n"
                "All subsequent DELTA frames reference this frame."
            )
        else:
            txt = (
                f"DELTA FRAME #{seq}\n"
                f"References keyframe SEQ={ref}.\n"
                "Contains only differences from the last absolute sample."
            )

        txt += f"\n\nStatus: {status}"
        frame_explain.setText(txt)

    def connect_serial():
        nonlocal ser, raw_rx_buffer, raw_buffer, total_bytes, have_new_bytes
        nonlocal ascii_hex_buf
        if serial is None:
            _warn(win, "Serial", "pyserial is not installed. Install: pip install pyserial")
            return
        if ser is not None:
            return
        dev = port_cb.currentData()
        if not dev:
            _warn(win, "Serial", "No serial port selected.")
            return
        try:
            # 115200 is a safe default for log streaming; change here if your device differs
            ser = serial.Serial(dev, 115200, timeout=0)
        except Exception as e:
            _warn(win, "Serial", f"Failed to open port: {e}")
            ser = None
            return

        raw_rx_buffer = bytearray()
        raw_buffer = bytearray()
        ascii_hex_buf = ""
        total_bytes = 0
        lbl_bytes.setText("Bytes: 0")
        lbl_status.setText("Status: connected")
        have_new_bytes = False

        raw_human_view.clear()
        raw_hex_view.clear()
        append_raw_debug(f"[INFO] ONLINE connected: {dev}")

        _set_led(led_conn, True, "#00cc00")
        btn_connect.setEnabled(False)
        btn_disconnect.setEnabled(True)
        btn_log.setEnabled(True)

        serial_timer.start()
        decode_timer.start()

        # Auto-start LOG in ONLINE mode
        _start_auto_log()

        set_mode_ui()

    def disconnect_serial():
        nonlocal ser, log_fp, log_path
        if ser is None:
            return

        serial_timer.stop()
        decode_timer.stop()

        try:
            ser.close()
        except Exception:
            pass
        ser = None

        _set_led(led_conn, False, "#00cc00")
        btn_connect.setEnabled(True)
        btn_disconnect.setEnabled(False)
        btn_log.setEnabled(False)

        if log_fp is not None:
            try:
                log_fp.close()
            except Exception:
                pass
            log_fp = None
            log_path = None
            btn_log.setChecked(False)
            btn_log.setText("LOG")

        append_raw_debug("[INFO] ONLINE disconnected")
        set_mode_ui()

    def toggle_log(checked: bool):
        nonlocal log_fp, log_path
        if ser is None:
            btn_log.setChecked(False)
            return

        if checked:
            if log_fp is not None:
                btn_log.setText("STOP")
                return
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                win,
                "Save RAW log as",
                "",
                "Raw binary (*.bin);;All files (*)"
            )
            if not path:
                btn_log.setChecked(False)
                return
            try:
                log_fp = open(path, "ab")
                log_path = path
            except Exception as e:
                _warn(win, "LOG", f"Failed to open log file: {e}")
                btn_log.setChecked(False)
                log_fp = None
                log_path = None
                return

            btn_log.setText("STOP")
            append_raw_debug(f"[INFO] LOG started: {path}")
        else:
            if log_fp is not None:
                try:
                    log_fp.close()
                except Exception:
                    pass
            log_fp = None
            log_path = None
            btn_log.setText("LOG")
            append_raw_debug("[INFO] LOG stopped")

    def _auto_pick_port():
        """
        Try to find an ESP32 serial device by description.
        Returns device string or None.
        """
        if serial is None:
            return None
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            return None
        # Prefer common ESP32 bridges/descriptions
        prefer = ("CP210", "CH340", "CH910", "USB Serial", "Silicon Labs", "Espressif", "UART")
        scored = []
        for p in ports:
            desc = (p.description or "") + " " + (getattr(p, "manufacturer", "") or "")
            score = 0
            for k in prefer:
                if k.lower() in desc.lower():
                    score += 1
            # Some macOS devices: /dev/cu.*
            if "cu." in (p.device or ""):
                score += 1
            scored.append((score, p.device, p.description))
        scored.sort(reverse=True)
        best = scored[0]
        return best[1] if best[0] > 0 else ports[0].device

    def _start_auto_log():
        nonlocal log_fp, log_path
        if log_fp is not None:
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"AstroLink_raw_{ts}.bin"
        path = os.path.join(os.getcwd(), fname)
        try:
            log_fp = open(path, "ab")
            log_path = path
        except Exception as e:
            append_raw_debug(f"[ERR] auto-log open failed: {e}")
            log_fp = None
            log_path = None
            return
        btn_log.blockSignals(True)
        btn_log.setChecked(True)
        btn_log.blockSignals(False)
        btn_log.setText("STOP")
        append_raw_debug(f"[INFO] LOG started (auto): {path}")

    def on_mode_changed():
        if mode_cb.currentText() == "OFFLINE":
            # Switching to OFFLINE will disconnect serial to keep deterministic behavior
            if ser is not None:
                disconnect_serial()
            set_mode_ui()
            return

        # ONLINE selected:
        refresh_ports()
        set_mode_ui()

        # Auto-pick and connect if possible
        if ser is None:
            dev = _auto_pick_port()
            if dev is not None:
                # select in combo box if present
                for idx in range(port_cb.count()):
                    if port_cb.itemData(idx) == dev:
                        port_cb.setCurrentIndex(idx)
                        break
                connect_serial()

    def _on_file_select():
        load_file()

    file_list.itemClicked.connect(lambda _: _on_file_select())
    table.itemSelectionChanged.connect(on_table_select)
    frame_table.itemClicked.connect(lambda item: on_frame_select(item.row()))
    frame_table.cellClicked.connect(lambda r, c: on_frame_select(r))
    frame_table.itemSelectionChanged.connect(lambda: on_frame_select(frame_table.currentRow()))

    btn_refresh_ports.clicked.connect(refresh_ports)
    btn_connect.clicked.connect(connect_serial)
    btn_disconnect.clicked.connect(disconnect_serial)
    btn_log.toggled.connect(toggle_log)
    mode_cb.currentIndexChanged.connect(on_mode_changed)

    refresh_ports()
    refresh_file_list()
    set_mode_ui()
    lbl_status.setText("Status: ready")

    serial_timer.stop()
    decode_timer.stop()

    win.show()
    app.exec_()

if __name__ == "__main__":
    main()
