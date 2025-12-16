# -------------------------------------------------------------------------
# Color constants for HTML frame rendering
# -------------------------------------------------------------------------
COLOR_FULL  = "#2ecc71"   # green
COLOR_DELTA = "#3498db"   # blue
COLOR_NOISE = "#e74c3c"   # red
COLOR_META  = "#aaaaaa"   # gray

# Bump this when debugging so you can see you're running the right file.
APP_VERSION = "2025-12-15a"
# Fast telemetry plotter using pyqtgraph
# Usage: python plot_telemetry.py raw_xxx.bin

from pathlib import Path
import sys
import time
import binascii
import os
import re
from datetime import datetime
import math

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

# Qt model/view imports (stay on the same binding that pyqtgraph picked)
Qt = QtCore.Qt

# Qt6 enum compat: expose Qt.AlignCenter-style names when running on Qt6 bindings.
def _install_qt_enum_compat():
    def _set(name, value):
        if not hasattr(Qt, name):
            setattr(Qt, name, value)

    qt = QtCore.Qt
    if hasattr(qt, "AlignmentFlag"):
        _set("AlignCenter", qt.AlignmentFlag.AlignCenter)
        _set("AlignVCenter", qt.AlignmentFlag.AlignVCenter)
        _set("AlignLeft", qt.AlignmentFlag.AlignLeft)
    if hasattr(qt, "Orientation"):
        _set("Horizontal", qt.Orientation.Horizontal)
        _set("Vertical", qt.Orientation.Vertical)
    if hasattr(qt, "PenStyle"):
        _set("DashLine", qt.PenStyle.DashLine)
    if hasattr(qt, "TextElideMode"):
        _set("ElideRight", qt.TextElideMode.ElideRight)
        _set("ElideMiddle", qt.TextElideMode.ElideMiddle)
    if hasattr(qt, "BrushStyle"):
        _set("NoBrush", qt.BrushStyle.NoBrush)
    if hasattr(qt, "ItemFlag"):
        _set("NoItemFlags", qt.ItemFlag.NoItemFlags)
    if hasattr(qt, "ScrollBarPolicy"):
        _set("ScrollBarAlwaysOff", qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    if hasattr(qt, "FocusPolicy"):
        _set("StrongFocus", qt.FocusPolicy.StrongFocus)
    if hasattr(qt, "TextInteractionFlag"):
        _set("TextSelectableByMouse", qt.TextInteractionFlag.TextSelectableByMouse)
    if hasattr(qt, "ItemDataRole"):
        _set("UserRole", qt.ItemDataRole.UserRole)
    if hasattr(qt, "GlobalColor"):
        _set("red", qt.GlobalColor.red)
        _set("white", qt.GlobalColor.white)


_install_qt_enum_compat()

# Convenience aliases so the rest of the file can use the short class names.
QTableWidget = QtWidgets.QTableWidget
QTableWidgetItem = QtWidgets.QTableWidgetItem
QSplitter = QtWidgets.QSplitter
QPlainTextEdit = QtWidgets.QPlainTextEdit
QHBoxLayout = QtWidgets.QHBoxLayout
QVBoxLayout = QtWidgets.QVBoxLayout
QGridLayout = QtWidgets.QGridLayout
QComboBox = QtWidgets.QComboBox
QLabel = QtWidgets.QLabel
QPushButton = QtWidgets.QPushButton
QTabWidget = QtWidgets.QTabWidget
QButtonGroup = QtWidgets.QButtonGroup
QGroupBox = QtWidgets.QGroupBox
QSlider = QtWidgets.QSlider
QFormLayout = QtWidgets.QFormLayout
QListWidget = QtWidgets.QListWidget
QHeaderView = QtWidgets.QHeaderView
QFrame = QtWidgets.QFrame

QFRAME_PANEL = getattr(QFrame, "Panel", QFrame.Shape.Panel)
QFRAME_SUNKEN = getattr(QFrame, "Sunken", QFrame.Shadow.Sunken)

QFONT_BOLD = getattr(QtGui.QFont, "Bold", QtGui.QFont.Weight.Bold)
QFONT_MONOSPACE = getattr(QtGui.QFont, "Monospace", QtGui.QFont.StyleHint.Monospace)

QFONTDB_FIXED = getattr(
    QtGui.QFontDatabase,
    "FixedFont",
    getattr(getattr(QtGui.QFontDatabase, "SystemFont", object()), "FixedFont", None),
)

QTEXTEDIT_NOWRAP = getattr(
    QtWidgets.QTextEdit,
    "NoWrap",
    getattr(getattr(QtWidgets.QTextEdit, "LineWrapMode", object()), "NoWrap", None),
)

QPAINTER_ANTIALIASING = getattr(
    QtGui.QPainter,
    "Antialiasing",
    getattr(getattr(QtGui.QPainter, "RenderHint", object()), "Antialiasing", None),
)

QTEXTCURSOR_START = getattr(
    QtGui.QTextCursor,
    "Start",
    getattr(getattr(QtGui.QTextCursor, "MoveOperation", object()), "Start", None),
)
QTEXTCURSOR_BLOCKUNDERCURSOR = getattr(
    QtGui.QTextCursor,
    "BlockUnderCursor",
    getattr(getattr(QtGui.QTextCursor, "SelectionType", object()), "BlockUnderCursor", None),
)

QMSGBOX_YES = getattr(
    QtWidgets.QMessageBox,
    "Yes",
    getattr(getattr(QtWidgets.QMessageBox, "StandardButton", object()), "Yes", None),
)
QMSGBOX_NO = getattr(
    QtWidgets.QMessageBox,
    "No",
    getattr(getattr(QtWidgets.QMessageBox, "StandardButton", object()), "No", None),
)

QSIZEPOLICY_FIXED = getattr(
    QtWidgets.QSizePolicy,
    "Fixed",
    getattr(getattr(QtWidgets.QSizePolicy, "Policy", object()), "Fixed", None),
)
QSIZEPOLICY_PREFERRED = getattr(
    QtWidgets.QSizePolicy,
    "Preferred",
    getattr(getattr(QtWidgets.QSizePolicy, "Policy", object()), "Preferred", None),
)
QSIZEPOLICY_EXPANDING = getattr(
    QtWidgets.QSizePolicy,
    "Expanding",
    getattr(getattr(QtWidgets.QSizePolicy, "Policy", object()), "Expanding", None),
)

QSTYLE_STATE_SELECTED = getattr(
    QtWidgets.QStyle,
    "State_Selected",
    getattr(getattr(QtWidgets.QStyle, "StateFlag", object()), "State_Selected", None),
)
QSTYLE_CE_ITEMVIEWITEM = getattr(
    QtWidgets.QStyle,
    "CE_ItemViewItem",
    getattr(getattr(QtWidgets.QStyle, "ControlElement", object()), "CE_ItemViewItem", None),
)

QABSTRACTITEMVIEW_SINGLE = getattr(
    QtWidgets.QAbstractItemView,
    "SingleSelection",
    getattr(getattr(QtWidgets.QAbstractItemView, "SelectionMode", object()), "SingleSelection", None),
)
QABSTRACTITEMVIEW_POSITIONATBOTTOM = getattr(
    QtWidgets.QAbstractItemView,
    "PositionAtBottom",
    getattr(getattr(QtWidgets.QAbstractItemView, "ScrollHint", object()), "PositionAtBottom", None),
)

QABSTRACTITEMVIEW_SELECTROWS = getattr(
    QtWidgets.QAbstractItemView,
    "SelectRows",
    getattr(getattr(QtWidgets.QAbstractItemView, "SelectionBehavior", object()), "SelectRows", None),
)

QPAL_WINDOW = getattr(QtGui.QPalette, "Window", QtGui.QPalette.ColorRole.Window)
QPAL_WINDOWTEXT = getattr(QtGui.QPalette, "WindowText", QtGui.QPalette.ColorRole.WindowText)
QPAL_BASE = getattr(QtGui.QPalette, "Base", QtGui.QPalette.ColorRole.Base)
QPAL_ALTERNATEBASE = getattr(QtGui.QPalette, "AlternateBase", QtGui.QPalette.ColorRole.AlternateBase)
QPAL_TOOLTIPBASE = getattr(QtGui.QPalette, "ToolTipBase", QtGui.QPalette.ColorRole.ToolTipBase)
QPAL_TOOLTIPTEXT = getattr(QtGui.QPalette, "ToolTipText", QtGui.QPalette.ColorRole.ToolTipText)
QPAL_TEXT = getattr(QtGui.QPalette, "Text", QtGui.QPalette.ColorRole.Text)
QPAL_BUTTON = getattr(QtGui.QPalette, "Button", QtGui.QPalette.ColorRole.Button)
QPAL_BUTTONTEXT = getattr(QtGui.QPalette, "ButtonText", QtGui.QPalette.ColorRole.ButtonText)
QPAL_BRIGHTTEXT = getattr(QtGui.QPalette, "BrightText", QtGui.QPalette.ColorRole.BrightText)
QPAL_HIGHLIGHT = getattr(QtGui.QPalette, "Highlight", QtGui.QPalette.ColorRole.Highlight)
QPAL_HIGHLIGHTEDTEXT = getattr(
    QtGui.QPalette, "HighlightedText", QtGui.QPalette.ColorRole.HighlightedText
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
SYNC_META1 = 0xD3   # RF meta frame (post-payload)
SYNC_META2 = 0xD4

# Frame lengths (must match firmware)
FULL_FRAME_LEN  = 38
DELTA_FRAME_LEN = 23
META_FRAME_LEN  = 28

def crc8_xor(data: bytes) -> int:
    c = 0
    for b in data:
        c ^= b
    return c & 0xFF

def _i8(b: int) -> int:
    return b - 256 if b & 0x80 else b

def _i16le(lo: int, hi: int) -> int:
    v = lo | (hi << 8)
    return v - 65536 if v & 0x8000 else v

def parse_rf_meta_frame(frame: bytes):
    """
    Firmware RF META v1 (28 bytes), SYNC 0xD3 0xD4.
    Returns dict or None if invalid.
    """
    if len(frame) != META_FRAME_LEN:
        return None
    if frame[0] != SYNC_META1 or frame[1] != SYNC_META2:
        return None
    ver = frame[2]
    if ver != 1:
        return None
    total_len = frame[3]
    if total_len != META_FRAME_LEN:
        return None
    crc_ok = (frame[27] == crc8_xor(frame[2:27]))
    if not crc_ok:
        return None

    flags = frame[5]
    phy_ok = bool(flags & (1 << 0))
    app_ok = bool(flags & (1 << 1))
    is_full = bool(flags & (1 << 2))
    is_delta = bool(flags & (1 << 3))

    fei_hz = _i16le(frame[9], frame[10])
    offset_hz = _i16le(frame[11], frame[12])

    return {
        "ver": ver,
        "payload_len": frame[4],
        "phy_ok": phy_ok,
        "app_ok": app_ok,
        "is_full": is_full,
        "is_delta": is_delta,
        "rssi_pkt_dbm": _i8(frame[6]),
        "rssi_inst_dbm": _i8(frame[7]),
        "snr_db": _i8(frame[8]) / 4.0,
        "snr_qdb": _i8(frame[8]),
        "fei_hz": fei_hz,
        "offset_hz": offset_hz,
        "bw_bits": frame[13],
        "sf": frame[14],
        "cr": frame[15],
        "rx_nb_bytes": frame[16],
        "modem_stat": frame[17],
        "irq_flags": frame[18],
        "rx_header_cnt": frame[19] | (frame[20] << 8),
        "rx_packet_cnt": frame[21] | (frame[22] << 8),
        "link_score": frame[23],
        "seq": frame[24],
        "met": frame[25] | (frame[26] << 8),
    }

def link_score_pc(meta: dict) -> int:
    """
    PC-side Link Quality Score (0..100) from META fields.
    Uses RSSI/SNR/FEI plus basic validity penalties.
    """
    rssi = int(meta.get("rssi_pkt_dbm", -150))
    snr = float(meta.get("snr_db", -32.0))
    fei_abs = abs(int(meta.get("fei_hz", 0)))

    # RSSI: -120..-60 => 0..100
    rssi_score = int(round((rssi + 120) * 100 / 60))
    rssi_score = max(0, min(100, rssi_score))

    # SNR: -20..+10 => 0..100
    snr_score = int(round((snr + 20.0) * (100.0 / 30.0)))
    snr_score = max(0, min(100, snr_score))

    # FEI stability: 0..5000Hz => 100..0
    fei_score = 100 - int((fei_abs * 100) / 5000) if fei_abs <= 5000 else 0
    fei_score = max(0, min(100, fei_score))

    # Penalties: if the receiver itself marks bad, degrade hard
    penalty = 0
    if not meta.get("phy_ok", True):
        penalty += 40
    if not meta.get("app_ok", True):
        penalty += 20

    score = int(round(0.45 * snr_score + 0.35 * rssi_score + 0.20 * fei_score))
    score -= penalty
    return max(0, min(100, score))

def lora_bw_khz_from_bits(bw_bits: int) -> float:
    m = {
        0: 7.8, 1: 10.4, 2: 15.6, 3: 20.8, 4: 31.25, 5: 41.7,
        6: 62.5, 7: 125.0, 8: 250.0, 9: 500.0
    }
    return float(m.get(int(bw_bits), 125.0))

def lora_required_snr_db(sf: int) -> float:
    # Typical LoRa demodulation limits (datasheet-ish), used for UI thresholds.
    req = {7: -7.5, 8: -10.0, 9: -12.5, 10: -15.0, 11: -17.5, 12: -20.0}
    return float(req.get(int(sf), -10.0))

def lora_sensitivity_dbm(sf: int, bw_khz: float) -> float:
    # Rough sensitivity model: BW=125k reference + 10*log10(BW/125k)
    base_125 = {7: -123.0, 8: -126.0, 9: -129.0, 10: -132.0, 11: -134.5, 12: -137.0}
    s = float(base_125.get(int(sf), -126.0))
    bw = float(bw_khz) if bw_khz > 0 else 125.0
    s += 10.0 * math.log10(bw / 125.0)
    return s

def lora_noise_floor_dbm(bw_khz: float, noise_figure_db: float = 6.0) -> float:
    """
    Rough channel noise floor estimate for coloring "instant RSSI" as channel energy.
    N ≈ -174 dBm/Hz + 10*log10(BW_Hz) + NF
    """
    bw_hz = max(1.0, float(bw_khz) * 1000.0)
    return -174.0 + 10.0 * math.log10(bw_hz) + float(noise_figure_db)

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
    # Keep LED indicators compact and non-stretchy.
    try:
        lbl.setSizePolicy(QSIZEPOLICY_FIXED, QSIZEPOLICY_FIXED)
        lbl.setFixedSize(36, 22)
        lbl.setAlignment(Qt.AlignCenter)
    except Exception:
        pass
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
    app.setStyle("Fusion")

    # Windows often runs with UI scaling; keep the interface compact and consistent.
    try:
        if sys.platform.startswith("win"):
            f = app.font()
            if f.pointSize() <= 0:
                f.setPointSize(9)
            else:
                f.setPointSize(min(f.pointSize(), 9))
            f.setFamily("Segoe UI")
            app.setFont(f)
    except Exception:
        pass

    BTN_H = 24
    BTN_ICON_W = 28

    # Selection should never paint a filled block. We enforce this with a custom delegate
    # that clears the Selected state and draws only a thin outline.
    selection_outline = QtGui.QColor(255, 107, 96)

    class OutlineSelectionDelegate(QtWidgets.QStyledItemDelegate):
        def __init__(self, color: QtGui.QColor, parent=None):
            super().__init__(parent)
            self._color = QtGui.QColor(color)

        def setColor(self, color: QtGui.QColor):
            self._color = QtGui.QColor(color)

        def paint(self, painter, option, index):
            opt = QtWidgets.QStyleOptionViewItem(option)
            self.initStyleOption(opt, index)

            selected = bool(opt.state & QSTYLE_STATE_SELECTED)
            if selected:
                opt.state &= ~QSTYLE_STATE_SELECTED

            style = opt.widget.style() if opt.widget is not None else QtWidgets.QApplication.style()
            style.drawControl(QSTYLE_CE_ITEMVIEWITEM, opt, painter, opt.widget)

            if selected:
                painter.save()
                painter.setClipRect(opt.rect)
                pen = QtGui.QPen(self._color)
                pen.setWidth(1)
                painter.setPen(pen)
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawRect(opt.rect.adjusted(0, 0, -1, -1))
                painter.restore()

    table_sel_delegate = None
    list_sel_delegate = None

    class LinearBar(QtWidgets.QWidget):
        def __init__(self, vmin: float, vmax: float, title: str = "", unit: str = "", good_high: bool = True):
            super().__init__()
            self.vmin = float(vmin)
            self.vmax = float(vmax)
            self.title = str(title)
            self.unit = str(unit)
            self.good_high = bool(good_high)
            self.value = float(vmin)
            self.peak = float(vmin)
            self._have_peak = False
            # Thresholds for coloring (ESA-style): green/yellow/red
            self._thr_green = None  # type: float|None
            self._thr_yellow = None  # type: float|None
            self.setMinimumHeight(18)

        def setThresholds(self, green: float, yellow: float):
            self._thr_green = float(green)
            self._thr_yellow = float(yellow)
            self.update()

        def setValue(self, v: float):
            self.value = float(v)
            if not self._have_peak:
                self.peak = self.value
                self._have_peak = True
            else:
                if self.value > self.peak:
                    self.peak = self.value
            self.update()

        def setPeak(self, v: float):
            self.peak = float(v)
            self._have_peak = True
            self.update()

        def resetPeak(self):
            self._have_peak = False
            self.update()

        def paintEvent(self, ev):
            p = QtGui.QPainter(self)
            p.setRenderHint(QPAINTER_ANTIALIASING, False)
            r = self.rect().adjusted(0, 0, -1, -1)
            p.setPen(QtGui.QColor(120, 120, 120))
            p.drawRect(r)

            inner = r.adjusted(1, 1, -1, -1)
            if inner.width() <= 0 or inner.height() <= 0:
                return

            v = max(self.vmin, min(self.vmax, self.value))
            frac = 0.0 if self.vmax == self.vmin else (v - self.vmin) / (self.vmax - self.vmin)
            fill_w = int(inner.width() * frac)

            # Solid, semi-transparent fill with green/yellow/red zones (human-friendly)
            if self._thr_green is not None and self._thr_yellow is not None:
                if self.good_high:
                    good = v >= self._thr_green
                    warn = v >= self._thr_yellow
                else:
                    good = v <= self._thr_green
                    warn = v <= self._thr_yellow
                if good:
                    col = QtGui.QColor(0, 200, 100, 140)
                elif warn:
                    col = QtGui.QColor(255, 200, 0, 140)
                else:
                    col = QtGui.QColor(255, 80, 80, 140)
            else:
                # fallback
                goodness = frac if self.good_high else (1.0 - frac)
                if goodness >= 0.66:
                    col = QtGui.QColor(0, 200, 100, 140)
                elif goodness >= 0.33:
                    col = QtGui.QColor(255, 200, 0, 140)
                else:
                    col = QtGui.QColor(255, 80, 80, 140)
            if fill_w > 0:
                p.fillRect(QtCore.QRect(inner.left(), inner.top(), fill_w, inner.height() + 1), col)

            # peak marker line
            if self._have_peak:
                pk = max(self.vmin, min(self.vmax, self.peak))
                pk_frac = 0.0 if self.vmax == self.vmin else (pk - self.vmin) / (self.vmax - self.vmin)
                px = inner.left() + int(inner.width() * pk_frac)
                p.setPen(QtGui.QColor(255, 255, 255))
                p.drawLine(px, inner.top(), px, inner.bottom())

            # label
            p.setPen(QtGui.QColor(220, 220, 220))
            txt = f"{self.title}: {self.value:.1f}{self.unit}" if self.unit else f"{self.title}: {self.value:.1f}"
            p.drawText(r.adjusted(4, 0, -4, 0), Qt.AlignVCenter | Qt.AlignLeft, txt)

    class CenteredBar(QtWidgets.QWidget):
        def __init__(self, abs_range: float, title: str = "", unit: str = ""):
            super().__init__()
            self.abs_range = float(abs_range)
            self.title = str(title)
            self.unit = str(unit)
            self.value = 0.0
            self.peak = 0.0
            self._have_peak = False
            self._thr_green = None  # abs(value) <= green
            self._thr_yellow = None  # abs(value) <= yellow
            self.setMinimumHeight(18)

        def setAbsThresholds(self, green: float, yellow: float):
            self._thr_green = float(green)
            self._thr_yellow = float(yellow)
            self.update()

        def setValue(self, v: float):
            self.value = float(v)
            if not self._have_peak:
                self.peak = self.value
                self._have_peak = True
            else:
                if abs(self.value) > abs(self.peak):
                    self.peak = self.value
            self.update()

        def setPeak(self, v: float):
            self.peak = float(v)
            self._have_peak = True
            self.update()

        def resetPeak(self):
            self._have_peak = False
            self.update()

        def paintEvent(self, ev):
            p = QtGui.QPainter(self)
            p.setRenderHint(QPAINTER_ANTIALIASING, False)
            r = self.rect().adjusted(0, 0, -1, -1)
            p.setPen(QtGui.QColor(120, 120, 120))
            p.drawRect(r)
            inner = r.adjusted(1, 1, -1, -1)
            if inner.width() <= 0 or inner.height() <= 0:
                return
            cx = inner.left() + inner.width() // 2
            p.setPen(QtGui.QColor(160, 160, 160))
            p.drawLine(cx, inner.top(), cx, inner.bottom())

            rng = max(1.0, self.abs_range)
            v = max(-rng, min(rng, self.value))
            mag = int((abs(v) / rng) * (inner.width() // 2))
            # Color by "how close to center" (0 = bad/red, 1 = good/green)
            av = abs(v)
            if self._thr_green is not None and self._thr_yellow is not None:
                if av <= self._thr_green:
                    col = QtGui.QColor(0, 200, 100, 140)
                elif av <= self._thr_yellow:
                    col = QtGui.QColor(255, 200, 0, 140)
                else:
                    col = QtGui.QColor(255, 80, 80, 140)
            else:
                goodness = 1.0 - (av / rng)
                if goodness >= 0.66:
                    col = QtGui.QColor(0, 200, 100, 140)
                elif goodness >= 0.33:
                    col = QtGui.QColor(255, 200, 0, 140)
                else:
                    col = QtGui.QColor(255, 80, 80, 140)

            if mag > 0:
                x0 = cx if v >= 0 else (cx - mag)
                p.fillRect(QtCore.QRect(x0, inner.top(), mag, inner.height() + 1), col)

            if self._have_peak:
                pk = max(-rng, min(rng, self.peak))
                pmag = int((abs(pk) / rng) * (inner.width() // 2))
                px = (cx + pmag) if pk >= 0 else (cx - pmag)
                p.setPen(QtGui.QColor(255, 255, 255))
                p.drawLine(px, inner.top(), px, inner.bottom())

            p.setPen(QtGui.QColor(220, 220, 220))
            txt = f"{self.title}: {self.value:.0f}{self.unit}" if self.unit else f"{self.title}: {self.value:.0f}"
            p.drawText(r.adjusted(4, 0, -4, 0), Qt.AlignVCenter | Qt.AlignLeft, txt)

    def apply_theme(dark: bool):
        # Minimal, readable "mission control" theme. Keep it deterministic across platforms.
        if dark:
            pg.setConfigOptions(background=(12, 12, 14), foreground=(230, 230, 235))
            try:
                plots.setBackground((12, 12, 14))
            except Exception:
                pass
            pal = QtGui.QPalette()
            pal.setColor(QPAL_WINDOW, QtGui.QColor(32, 32, 34))
            pal.setColor(QPAL_WINDOWTEXT, Qt.white)
            pal.setColor(QPAL_BASE, QtGui.QColor(22, 22, 24))
            pal.setColor(QPAL_ALTERNATEBASE, QtGui.QColor(36, 36, 40))
            pal.setColor(QPAL_TOOLTIPBASE, QtGui.QColor(18, 18, 20))
            pal.setColor(QPAL_TOOLTIPTEXT, QtGui.QColor(235, 235, 240))
            pal.setColor(QPAL_TEXT, Qt.white)
            pal.setColor(QPAL_BUTTON, QtGui.QColor(45, 45, 48))
            pal.setColor(QPAL_BUTTONTEXT, Qt.white)
            pal.setColor(QPAL_BRIGHTTEXT, Qt.red)
            # Selection highlight should NOT paint a block; use only a red outline via stylesheet.
            pal.setColor(QPAL_HIGHLIGHT, QtGui.QColor(0, 0, 0, 0))
            pal.setColor(QPAL_HIGHLIGHTEDTEXT, Qt.white)
            app.setPalette(pal)
            app.setStyleSheet(
                """
                QGroupBox { border: 1px solid #3a3a3f; border-radius: 10px; margin-top: 10px; padding-top: 6px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; color: #cfcfd6; }
                QPushButton {
                    border: 1px solid #4a4a4a;
                    border-radius: 10px;
                    padding: 3px 10px;
                    min-height: 22px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3a3a3f, stop:1 #2a2a2e);
                }
                QPushButton:hover { border-color: #6a6a6f; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #44444a, stop:1 #2e2e33); }
                QPushButton:pressed { border-color: #2c6fb8; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b3f5b, stop:1 #223246); }
                QPushButton:checked { background: #2c6fb8; border-color: #2c6fb8; color: #ffffff; }
                QPushButton:disabled { color: #7a7a80; border-color: #3a3a3f; background: #2a2a2e; }
                QComboBox {
                    padding: 2px 8px;
                    min-height: 22px;
                    border: 1px solid #4a4a4a;
                    border-radius: 10px;
                    background: #2a2a2e;
                }
                QComboBox:hover { border-color: #6a6a6f; }
                QComboBox:disabled { color: #7a7a80; border: 1px solid #3a3a3f; background: #2a2a2e; }
                QLabel:disabled { color: #7a7a80; }
                QTabWidget::pane { border: 1px solid #3a3a3f; top: -1px; }
                QTabBar::tab { padding: 7px 12px; border: 1px solid #3a3a3f; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; background: #2a2a2e; margin-right: 2px; }
                QTabBar::tab:selected { background: #323236; border-color: #4a4a4a; }
                QTabBar::tab:hover { border-color: #2c6fb8; }
                QSplitter::handle { background: #2a2a2e; }
                QSplitter::handle:horizontal { width: 6px; }
                QSplitter::handle:vertical { height: 6px; }
                QToolTip { background-color: #121214; color: #ebebf0; border: 1px solid #4a4a4a; padding: 4px 6px; }
                QSlider::groove:horizontal { height: 8px; border-radius: 4px; background: #3a3a3f; }
                QSlider::sub-page:horizontal { background: #2c6fb8; border-radius: 4px; }
                QSlider::add-page:horizontal { background: #2a2a2e; border-radius: 4px; }
                QSlider::handle:horizontal { width: 14px; height: 14px; margin: -4px 0; border-radius: 7px; background: #d7d7dd; border: 1px solid #6a6a6f; }
                QSlider::handle:horizontal:hover { background: #ffffff; border-color: #2c6fb8; }
                """
            )
        else:
            pg.setConfigOptions(background=(248, 248, 250), foreground=(25, 25, 28))
            try:
                plots.setBackground((248, 248, 250))
            except Exception:
                pass
            app.setPalette(app.style().standardPalette())
            app.setStyleSheet(
                """
                QGroupBox { border: 1px solid #d4d4da; border-radius: 10px; margin-top: 10px; padding-top: 6px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; color: #303036; }
                QPushButton {
                    border: 1px solid #c3c3cc;
                    border-radius: 10px;
                    padding: 3px 10px;
                    min-height: 22px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #ececf1);
                }
                QPushButton:hover { border-color: #2c6fb8; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e3efff); }
                QPushButton:pressed { border-color: #2c6fb8; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dbe9ff, stop:1 #cfe0ff); }
                QPushButton:checked { background: #2c6fb8; border-color: #2c6fb8; color: white; }
                QComboBox {
                    padding: 2px 8px;
                    min-height: 22px;
                    border: 1px solid #c3c3cc;
                    border-radius: 10px;
                    background: #ffffff;
                }
                QComboBox:hover { border-color: #2c6fb8; }
                QTabWidget::pane { border: 1px solid #cfcfd6; top: -1px; }
                QTabBar::tab { padding: 7px 12px; border: 1px solid #cfcfd6; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; background: #f0f0f4; margin-right: 2px; }
                QTabBar::tab:selected { background: #ffffff; border-color: #c3c3cc; }
                QTabBar::tab:hover { border-color: #2c6fb8; }
                QSplitter::handle { background: #e6e6eb; }
                QSplitter::handle:horizontal { width: 6px; }
                QSplitter::handle:vertical { height: 6px; }
                QToolTip { background-color: #fffffb; color: #111118; border: 1px solid #cfcfd6; padding: 4px 6px; }
                QSlider::groove:horizontal { height: 8px; border-radius: 4px; background: #d9d9df; }
                QSlider::sub-page:horizontal { background: #2c6fb8; border-radius: 4px; }
                QSlider::add-page:horizontal { background: #f0f0f4; border-radius: 4px; }
                QSlider::handle:horizontal { width: 14px; height: 14px; margin: -4px 0; border-radius: 7px; background: #33333a; border: 1px solid #8e8ea0; }
                QSlider::handle:horizontal:hover { background: #111118; border-color: #2c6fb8; }
                """
            )

        # Ensure existing plot axes also switch colors (pyqtgraph config is not always retroactive).
        fg = QtGui.QColor(230, 230, 235) if dark else QtGui.QColor(25, 25, 28)
        axis_pen = pg.mkPen(fg, width=1)
        for plot in (p_temp, p_hum, p_pres):
            if plot is None:
                continue
            for ax_name in ("left", "bottom"):
                try:
                    ax = plot.getAxis(ax_name)
                    ax.setPen(axis_pen)
                    ax.setTextPen(axis_pen)
                    ax.setTickPen(axis_pen)
                except Exception:
                    pass

        # Keep selection outline visible on both themes.
        try:
            if table_sel_delegate is not None:
                table_sel_delegate.setColor(selection_outline)
            if list_sel_delegate is not None:
                list_sel_delegate.setColor(selection_outline)
        except Exception:
            pass

    # Main window
    win = QtWidgets.QWidget()
    win.setWindowTitle(f"AstroLink – Telemetry Ground Station ({APP_VERSION})")
    win.setMinimumSize(1280, 720)
    win.resize(1500, 900)

    layout = QVBoxLayout(win)
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(6)

    # -------------------------------------------------------------------------
    # Top control bar (single compact row)
    # -------------------------------------------------------------------------
    top = QHBoxLayout()
    top.setContentsMargins(0, 0, 0, 0)
    top.setSpacing(6)
    layout.addLayout(top)

    mode_cb = QComboBox()
    mode_cb.addItems(["OFFLINE", "ONLINE"])
    top.addWidget(QLabel("Mode:"))
    top.addWidget(mode_cb)

    port_cb = QComboBox()
    port_cb.setMinimumWidth(220)
    # Avoid the combo box growing the whole window based on long descriptions (Qt/Windows).
    try:
        port_cb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        port_cb.setMinimumContentsLength(18)
    except Exception:
        pass
    top.addWidget(QLabel("Port:"))
    top.addWidget(port_cb, 1)

    btn_refresh_ports = QPushButton("Refresh")
    top.addWidget(btn_refresh_ports)

    btn_connect = QPushButton("Connect")
    btn_disconnect = QPushButton("Disconnect")
    btn_connect.setCheckable(True)
    btn_disconnect.setCheckable(True)
    conn_btn_group = QButtonGroup(win)
    conn_btn_group.setExclusive(True)
    conn_btn_group.addButton(btn_connect)
    conn_btn_group.addButton(btn_disconnect)
    btn_disconnect.setChecked(True)  # default state: disconnected
    top.addWidget(btn_connect)
    top.addWidget(btn_disconnect)

    btn_sidebar = QPushButton("Sidebar")
    btn_sidebar.setCheckable(True)
    btn_sidebar.setChecked(True)
    btn_sidebar.setToolTip("Show/hide sidebar (graphs focus)")
    top.addWidget(btn_sidebar)

    top.addWidget(QLabel("RX:"))
    led_rx = QLabel("")
    led_rx.setText("RX")
    led_rx.setAlignment(Qt.AlignCenter)
    top.addWidget(led_rx)
    top.addWidget(QLabel("LINK:"))
    led_conn = QLabel("")
    led_conn.setText("OK")
    led_conn.setAlignment(Qt.AlignCenter)
    top.addWidget(led_conn)

    lbl_bytes = QLabel("Bytes: 0")
    lbl_bytes.setMinimumWidth(110)
    lbl_bytes.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    lbl_bytes.setAlignment(Qt.AlignCenter)
    top.addWidget(lbl_bytes)

    lbl_status = QLabel("Status: idle")
    lbl_status.setMinimumWidth(0)
    lbl_status.setSizePolicy(QSIZEPOLICY_EXPANDING, QSIZEPOLICY_PREFERRED)
    lbl_status.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    lbl_status.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    top.addWidget(lbl_status, 2)

    btn_log = QPushButton("LOG")
    btn_log.setCheckable(True)
    btn_log.setEnabled(False)
    top.addWidget(btn_log)

    btn_fullscreen = QPushButton("Full screen")
    btn_fullscreen.setToolTip("Toggle fullscreen (F11)")
    top.addWidget(btn_fullscreen)

    top.addWidget(QLabel("Theme:"))
    theme_cb = QComboBox()
    theme_cb.addItems(["Dark", "Light"])
    theme_cb.setFixedWidth(110)
    top.addWidget(theme_cb)

    # Make the top bar uniformly compact.
    try:
        for w in (
            mode_cb,
            port_cb,
            btn_refresh_ports,
            btn_connect,
            btn_disconnect,
            btn_sidebar,
            led_rx,
            led_conn,
            lbl_bytes,
            lbl_status,
            btn_log,
            btn_fullscreen,
            theme_cb,
        ):
            w.setFixedHeight(24)
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Main content area (sidebar + plots)
    # -------------------------------------------------------------------------
    main_hsplit = QSplitter(Qt.Horizontal)
    main_hsplit.setChildrenCollapsible(False)
    layout.addWidget(main_hsplit, 1)

    # Offline file list chooser (OFFLINE mode)
    file_box = QtWidgets.QWidget()
    file_box_layout = QVBoxLayout(file_box)
    file_box_layout.setContentsMargins(0, 0, 0, 0)
    file_box_layout.setSpacing(10)

    file_list = QListWidget()
    file_list.setMinimumHeight(180)
    file_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    file_list.setTextElideMode(Qt.ElideRight)
    file_list.setMinimumWidth(340)
    file_list.setMaximumWidth(900)
    file_sel_delegate = OutlineSelectionDelegate(selection_outline, file_list)
    file_list.setItemDelegate(file_sel_delegate)
    # Reserve some space on the right so per-row buttons don't sit under the scrollbar.
    try:
        file_list.setViewportMargins(0, 0, 30, 0)
    except Exception:
        pass
    file_box_layout.addWidget(file_list, 1)

    # Sidebar controls (stacked): FILES + SIM + PLAYBACK + VIEW
    right_panel = QtWidgets.QWidget()
    rp = QVBoxLayout(right_panel)
    rp.setContentsMargins(0, 0, 0, 0)
    rp.setSpacing(10)

    gb_files = QGroupBox("FILES")
    gb_files.setMinimumWidth(220)
    gb_files_l = QVBoxLayout(gb_files)
    gb_files_l.setContentsMargins(10, 12, 10, 10)
    gb_files_l.setSpacing(8)

    btn_delete = QPushButton("Delete selected…")
    btn_delete.setToolTip("Delete selected BIN file (OFFLINE)")
    btn_delete.setMinimumHeight(BTN_H)
    btn_delete.setEnabled(False)
    gb_files_l.addWidget(btn_delete, 0)

    btn_refresh_files = QPushButton("Reload list")
    btn_refresh_files.setToolTip("Refresh BIN file list (OFFLINE)")
    btn_refresh_files.setMinimumHeight(BTN_H)
    gb_files_l.addWidget(btn_refresh_files, 0)

    lbl_file_info = QLabel("No file selected")
    lbl_file_info.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    lbl_file_info.setMinimumHeight(44)
    lbl_file_info.setWordWrap(True)
    gb_files_l.addWidget(lbl_file_info, 0)
    gb_files_l.addStretch(1)
    rp.addWidget(gb_files, 0)

    gb_sim = QGroupBox("SIM")
    gb_sim.setMinimumWidth(170)
    gb_sim_l = QVBoxLayout(gb_sim)
    gb_sim_l.setContentsMargins(10, 12, 10, 10)
    gb_sim_l.setSpacing(8)

    btn_sim = QPushButton("Sim Flight")
    btn_sim.setToolTip("Generate simulated flight (OFFLINE)")
    btn_sim.setMinimumHeight(BTN_H)
    gb_sim_l.addWidget(btn_sim, 0)

    btn_export = QPushButton("Export plots…")
    btn_export.setToolTip("Export visible plots as PNG images")
    btn_export.setMinimumHeight(BTN_H)
    gb_sim_l.addWidget(btn_export, 0)

    gb_sim_l.addStretch(1)
    rp.addWidget(gb_sim, 0)

    gb_play = QGroupBox("PLAYBACK")
    gb_play_l = QVBoxLayout(gb_play)
    gb_play_l.setContentsMargins(10, 12, 10, 10)
    gb_play_l.setSpacing(8)

    gb_play_btn_row = QHBoxLayout()
    gb_play_btn_row.setContentsMargins(0, 0, 0, 0)
    gb_play_btn_row.setSpacing(8)

    btn_rw = QPushButton("⏪")
    btn_rw.setToolTip("Visszatekerés (RW): -20 minta")
    btn_play = QPushButton("▶")
    btn_play.setToolTip("Play: Lejátszás indítása")
    btn_pause = QPushButton("⏸")
    btn_pause.setToolTip("Pause: Lejátszás szünet")
    btn_stop = QPushButton("⏹")
    btn_stop.setToolTip("Stop: Lejátszás leállítása")
    btn_ff = QPushButton("⏩")
    btn_ff.setToolTip("Előretekerés (FF): +20 minta")

    # Show playback state visually
    pb_group = QButtonGroup(win)
    pb_group.setExclusive(True)
    for b in (btn_play, btn_pause, btn_stop):
        b.setCheckable(True)
        pb_group.addButton(b)
    btn_stop.setChecked(True)

    for b in (btn_rw, btn_play, btn_pause, btn_stop, btn_ff):
        b.setMinimumSize(BTN_ICON_W, BTN_H)
        gb_play_btn_row.addWidget(b, 0)

    gb_play_btn_row.addSpacing(10)

    # Speed buttons (inline, no label)
    speed_group = QButtonGroup(win)
    speed_group.setExclusive(True)
    btn_sp1 = QPushButton("1×")
    btn_sp2 = QPushButton("2×")
    btn_sp4 = QPushButton("4×")
    btn_sp8 = QPushButton("8×")
    for b in (btn_sp1, btn_sp2, btn_sp4, btn_sp8):
        b.setCheckable(True)
        b.setMinimumSize(34, BTN_H)
        speed_group.addButton(b)
        gb_play_btn_row.addWidget(b, 0)
    btn_sp1.setChecked(True)

    gb_play_btn_row.addStretch(1)
    gb_play_l.addLayout(gb_play_btn_row)

    # Playback time displays (2 Hz)
    lbl_met = QLabel("MET: 00:00:00.0  |  sample 0")
    lbl_met.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    lbl_met.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    lbl_met.setMinimumHeight(24)
    gb_play_l.addWidget(lbl_met, 0)

    seek_slider = QSlider(Qt.Horizontal)
    seek_slider.setRange(0, 0)
    seek_slider.setSingleStep(1)
    seek_slider.setPageStep(10)
    seek_slider.setTracking(True)
    seek_slider.setMinimumHeight(18)
    seek_slider.setToolTip("Seek (click/drag): jump to sample index")
    gb_play_l.addWidget(seek_slider, 0)

    lbl_clock = QLabel("Local: --:--:--")
    lbl_clock.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    lbl_clock.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    lbl_clock.setMinimumHeight(24)
    gb_play_l.addWidget(lbl_clock, 0)
    rp.addWidget(gb_play, 0)

    gb_view = QGroupBox("VIEW")
    gb_view.setFixedWidth(230)
    gb_view_l = QVBoxLayout(gb_view)
    gb_view_l.setContentsMargins(10, 12, 10, 10)
    gb_view_l.setSpacing(8)

    view_row = QHBoxLayout()
    view_row.setContentsMargins(0, 0, 0, 0)
    view_row.setSpacing(6)

    btn_view_t = QPushButton("T")
    btn_view_h = QPushButton("H")
    btn_view_p = QPushButton("P")
    view_group = QButtonGroup(win)
    view_group.setExclusive(True)
    for b in (btn_view_t, btn_view_h, btn_view_p):
        b.setCheckable(True)
        b.setMinimumSize(28, BTN_H)
        view_group.addButton(b)
        view_row.addWidget(b, 1)
    btn_view_p.setChecked(True)  # default: Pressure
    gb_view_l.addLayout(view_row)

    layout_row = QHBoxLayout()
    layout_row.setContentsMargins(0, 0, 0, 0)
    layout_row.setSpacing(6)

    btn_single = QPushButton("Single")
    btn_single.setCheckable(True)
    btn_single.setToolTip("Vertical layout: show only one plot (select T/H/P above)")
    btn_single.setMinimumHeight(BTN_H)
    layout_row.addWidget(btn_single, 1)

    plot_toggle = QPushButton("H")
    plot_toggle.setCheckable(True)
    plot_toggle.setChecked(True)  # startup: Horizontal
    plot_toggle.setMinimumSize(28, BTN_H)
    plot_toggle.setToolTip("Grafikon elrendezés váltása\nH = Horizontal, V = Vertical")
    plot_toggle.setFont(QtGui.QFont("Menlo", 10, QFONT_BOLD))
    layout_row.addWidget(plot_toggle, 0)
    gb_view_l.addLayout(layout_row)

    rp.addWidget(gb_view, 0)
    file_box_layout.addWidget(right_panel, 0)

    # Right side: plots (top) + tabs (bottom)
    right_vsplit = QSplitter(Qt.Vertical)
    right_vsplit.setChildrenCollapsible(False)
    right_vsplit.setStretchFactor(0, 5)
    right_vsplit.setStretchFactor(1, 2)

    main_hsplit.addWidget(file_box)
    main_hsplit.addWidget(right_vsplit)
    main_hsplit.setStretchFactor(0, 0)
    main_hsplit.setStretchFactor(1, 1)
    try:
        main_hsplit.setSizes([420, 1500])
    except Exception:
        pass

    def _set_sidebar_visible(visible: bool):
        file_box.setVisible(bool(visible))
        try:
            if visible:
                main_hsplit.setSizes([420, 1500])
            else:
                main_hsplit.setSizes([0, 1])
        except Exception:
            pass

    def on_sim_flight():
        if mode_cb.currentText() != "OFFLINE":
            return
        _generate_simulated_flight()
        update_from_raw()

    btn_sim.clicked.connect(on_sim_flight)

    def export_plots():
        """
        Export current plots to PNG files.
        Uses pyqtgraph ImageExporter for each PlotItem.
        """
        # Pick output directory
        out_dir = QtWidgets.QFileDialog.getExistingDirectory(win, "Export plots to folder", "")
        if not out_dir:
            return

        try:
            from pyqtgraph.exporters import ImageExporter
        except Exception as e:
            _warn(win, "Export", f"pyqtgraph ImageExporter not available: {e}")
            return

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Prefer current offline file name if available, otherwise generic.
        try:
            base = _selected_filename() or f"AstoLink_{ts}"
        except Exception:
            base = f"AstroLink_{ts}"
        base = os.path.splitext(os.path.basename(base))[0]

        exported = []

        def _export_plot(plot_item, suffix: str):
            if plot_item is None:
                return
            try:
                exp = ImageExporter(plot_item)
                # Make it readable in reports/logbooks
                try:
                    exp.parameters()["width"] = 1400
                except Exception:
                    pass
                path = os.path.join(out_dir, f"{base}_{suffix}_{ts}.png")
                exp.export(path)
                exported.append(path)
            except Exception as e:
                append_raw_debug(f"[ERR] export {suffix} failed: {e}")

        # Telemetry plots
        _export_plot(p_temp, "tele_T")
        _export_plot(p_hum, "tele_RH")
        _export_plot(p_pres, "tele_P")

        # RF Trends plots
        _export_plot(rftr_p_rssi, "rf_rssi")
        _export_plot(rftr_p_snr, "rf_snr")
        _export_plot(rftr_p_fei, "rf_fei")
        _export_plot(rftr_p_score, "rf_score")

        if exported:
            append_raw_debug(f"[INFO] Exported {len(exported)} plot(s) to: {out_dir}")
        else:
            _warn(win, "Export", "No plots available to export.")

    btn_export.clicked.connect(export_plots)

    def refresh_file_list():
        file_list.clear()
        files = [f for f in sorted(os.listdir(os.getcwd())) if f.lower().endswith(".bin")]
        max_w = 0
        fm = QtGui.QFontMetrics(file_list.font())
        for fname in files:
            it = QtWidgets.QListWidgetItem(fname)
            it.setData(Qt.UserRole, fname)
            it.setToolTip(fname)
            file_list.addItem(it)
            try:
                max_w = max(max_w, fm.horizontalAdvance(fname))
            except Exception:
                pass

        # Tight file list width: enough to show names, without wasting plot space.
        if max_w > 0:
            target = max(280, min(700, max_w + 40))
            file_list.setFixedWidth(int(target))
        _update_file_actions()
        _update_file_info()

    def _selected_filename():
        it = file_list.currentItem()
        if it is None:
            return None
        return it.data(Qt.UserRole) or it.text()

    def _format_size(n: int) -> str:
        try:
            n = int(n)
        except Exception:
            return "?"
        if n < 1024:
            return f"{n} B"
        size = float(n)
        for unit in ("KB", "MB", "GB", "TB"):
            size /= 1024.0
            if size < 1024.0 or unit == "TB":
                return f"{size:.1f} {unit}"
        return f"{size:.1f} TB"

    def _update_file_info():
        fn = _selected_filename()
        if not fn:
            lbl_file_info.setText("No file selected")
            lbl_file_info.setToolTip("")
            return
        path = os.path.join(os.getcwd(), fn)
        try:
            size = os.path.getsize(path)
            size_s = _format_size(size)
        except Exception:
            size_s = "?"
        # Elide filename to fit the small info panel, but keep full name in tooltip.
        try:
            avail = max(80, lbl_file_info.width() - 16)
            fm = QtGui.QFontMetrics(lbl_file_info.font())
            fn_disp = fm.elidedText(fn, Qt.ElideMiddle, avail)
        except Exception:
            fn_disp = fn
        lbl_file_info.setToolTip(f"{fn}\n{path}")
        lbl_file_info.setText(f"{fn_disp}\nSize: {size_s}  ({size} B)")

    def _update_file_actions():
        offline = (mode_cb.currentText() == "OFFLINE")
        btn_delete.setEnabled(offline and _selected_filename() is not None)
        btn_refresh_files.setEnabled(offline)

    def _delete_selected():
        fn = _selected_filename()
        if not fn:
            return
        ret = QtWidgets.QMessageBox.question(
            win,
            "Delete file",
            f"Delete file?\n\n{fn}",
            QMSGBOX_YES | QMSGBOX_NO,
            QMSGBOX_NO
        )
        if ret != QMSGBOX_YES:
            return
        try:
            os.remove(os.path.join(os.getcwd(), fn))
        except Exception as e:
            _warn(win, "Delete failed", str(e))
            return
        refresh_file_list()
        _update_file_actions()
        _update_file_info()
        lbl_status.setText(f"Status: deleted {fn}")

    btn_delete.clicked.connect(_delete_selected)
    btn_refresh_files.clicked.connect(refresh_file_list)
    file_list.currentItemChanged.connect(lambda *_: (_update_file_actions(), _update_file_info()))

    tabs = QTabWidget()
    right_vsplit.addWidget(tabs)

    # Table view for decoded samples (Decoded tab)
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Index", "Temp (°C)", "Hum (%)", "Press (hPa)"])
    table.horizontalHeader().setStretchLastSection(True)
    table_sel_delegate = OutlineSelectionDelegate(selection_outline, table)
    table.setItemDelegate(table_sel_delegate)
    tabs.addTab(table, "Decoded samples")

    # Raw view tab (shows incoming/raw bytes + frame summaries)
    fixed_font = QtGui.QFontDatabase.systemFont(QFONTDB_FIXED)
    fixed_font.setFamily("Menlo")
    fixed_font.setStyleHint(QFONT_MONOSPACE)
    raw_splitter = QSplitter(Qt.Horizontal)

    raw_human_view = QtWidgets.QTextEdit()
    raw_human_view.setFont(fixed_font)
    raw_human_view.setReadOnly(True)
    raw_human_view.setLineWrapMode(QTEXTEDIT_NOWRAP)
    raw_human_view.setAcceptRichText(True)

    raw_hex_view = QtWidgets.QTextEdit()
    raw_hex_view.setFont(fixed_font)
    raw_hex_view.setReadOnly(True)
    raw_hex_view.setLineWrapMode(QTEXTEDIT_NOWRAP)
    raw_hex_view.setAcceptRichText(True)

    raw_splitter.addWidget(raw_human_view)
    raw_splitter.addWidget(raw_hex_view)
    raw_splitter.setSizes([600, 600])

    tabs.addTab(raw_splitter, "Raw stream")

    # Frame Inspector tab (QTableWidget)
    frame_table = QTableWidget()
    frame_table.setColumnCount(7)
    frame_table.setHorizontalHeaderLabels(["#", "Type", "SEQ", "REF", "CRC", "Status", "Reason"])
    frame_table.setSelectionBehavior(QABSTRACTITEMVIEW_SELECTROWS)
    frame_table.setSelectionMode(QABSTRACTITEMVIEW_SINGLE)
    frame_table.setFocusPolicy(Qt.StrongFocus)
    frame_table.setItemDelegate(table_sel_delegate)
    frame_table.setAlternatingRowColors(True)
    try:
        frame_table.verticalHeader().setVisible(False)  # avoid double numbering (# + row header)
    except Exception:
        pass
    try:
        hh = frame_table.horizontalHeader()
        hh.setMinimumSectionSize(24)
        # Fixed/compact columns + stretch last column.
        for c in range(7):
            hh.setSectionResizeMode(c, QHeaderView.Interactive)
        frame_table.setColumnWidth(0, 34)   # #
        frame_table.setColumnWidth(1, 62)   # Type
        frame_table.setColumnWidth(2, 58)   # SEQ
        frame_table.setColumnWidth(3, 58)   # REF
        frame_table.setColumnWidth(4, 54)   # CRC
        frame_table.setColumnWidth(5, 140)  # Status
        hh.setSectionResizeMode(6, QHeaderView.Stretch)  # Reason
        hh.setStretchLastSection(True)
    except Exception:
        pass

    # Separate META table (RF diagnostics frames)
    meta_table = QTableWidget()
    meta_table.setColumnCount(10)
    meta_table.setHorizontalHeaderLabels([
        "#", "SEQ", "Sample", "LEN", "PHY", "APP", "PktStr", "Noise", "SNR", "FEI"
    ])
    meta_table.setSelectionBehavior(QABSTRACTITEMVIEW_SELECTROWS)
    meta_table.setSelectionMode(QABSTRACTITEMVIEW_SINGLE)
    meta_table.setFocusPolicy(Qt.StrongFocus)
    meta_table.setItemDelegate(table_sel_delegate)
    meta_table.setAlternatingRowColors(True)
    try:
        meta_table.verticalHeader().setVisible(False)
        hh = meta_table.horizontalHeader()
        hh.setMinimumSectionSize(24)
        for c in range(meta_table.columnCount()):
            hh.setSectionResizeMode(c, QHeaderView.Interactive)
        meta_table.setColumnWidth(0, 34)   # #
        meta_table.setColumnWidth(1, 58)   # SEQ
        meta_table.setColumnWidth(2, 68)   # Sample
        meta_table.setColumnWidth(3, 50)   # LEN
        meta_table.setColumnWidth(4, 48)   # PHY
        meta_table.setColumnWidth(5, 48)   # APP
        meta_table.setColumnWidth(6, 70)   # PktStr
        meta_table.setColumnWidth(7, 78)   # Noise
        meta_table.setColumnWidth(8, 64)   # SNR
        hh.setSectionResizeMode(9, QHeaderView.Stretch)  # FEI
        hh.setStretchLastSection(True)
    except Exception:
        pass

    frame_container = QtWidgets.QWidget()
    frame_layout = QVBoxLayout(frame_container)
    frame_layout.setContentsMargins(4, 4, 4, 4)
    # Two-column inspector:
    # Left: Frames table + its own explanation (vertical split)
    # Right: META table + its own explanation (vertical split)
    frame_split = QSplitter(Qt.Horizontal)

    # Left explain
    frame_explain_left = QLabel("Select a FULL/DELTA row to see explanation.")
    frame_explain_left.setWordWrap(True)
    frame_explain_left.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    frame_explain_left.setMinimumHeight(44)
    try:
        frame_explain_left.setTextInteractionFlags(Qt.TextSelectableByMouse)
    except Exception:
        pass

    frames_box = QtWidgets.QWidget()
    frames_box_l = QVBoxLayout(frames_box)
    frames_box_l.setContentsMargins(0, 0, 0, 0)
    frames_box_l.setSpacing(4)
    frames_lbl = QLabel("Frames (FULL/DELTA)")
    frames_lbl.setStyleSheet("QLabel { color: #cfcfd6; padding-left: 2px; }")
    frames_box_l.addWidget(frames_lbl, 0)
    frames_box_l.addWidget(frame_table, 1)

    frames_col = QSplitter(Qt.Vertical)
    frames_col.addWidget(frames_box)
    frames_col.addWidget(frame_explain_left)
    try:
        frames_col.setSizes([420, 90])
    except Exception:
        pass

    # Right explain
    meta_explain_right = QLabel("Select a META row to see RF explanation.")
    meta_explain_right.setWordWrap(True)
    meta_explain_right.setFrameStyle(QFRAME_PANEL | QFRAME_SUNKEN)
    meta_explain_right.setMinimumHeight(44)
    try:
        meta_explain_right.setTextInteractionFlags(Qt.TextSelectableByMouse)
    except Exception:
        pass

    meta_box = QtWidgets.QWidget()
    meta_box_l = QVBoxLayout(meta_box)
    meta_box_l.setContentsMargins(0, 0, 0, 0)
    meta_box_l.setSpacing(4)
    meta_lbl = QLabel("RF META")
    meta_lbl.setStyleSheet("QLabel { color: #cfcfd6; padding-left: 2px; }")
    meta_box_l.addWidget(meta_lbl, 0)
    meta_box_l.addWidget(meta_table, 1)

    meta_col = QSplitter(Qt.Vertical)
    meta_col.addWidget(meta_box)
    meta_col.addWidget(meta_explain_right)
    try:
        meta_col.setSizes([420, 90])
    except Exception:
        pass

    frame_split.addWidget(frames_col)
    frame_split.addWidget(meta_col)
    try:
        frame_split.setSizes([760, 520])
    except Exception:
        pass

    frame_layout.addWidget(frame_split)

    tabs.addTab(frame_container, "Frame Inspector")
    # ---------------------------------------------------------------------
    # Mission Timeline tab (OBOE MODE v1)
    # ---------------------------------------------------------------------
    timeline_widget = QtWidgets.QWidget()
    timeline_layout = QVBoxLayout(timeline_widget)
    timeline_layout.setContentsMargins(6, 6, 6, 6)

    timeline_events = QtWidgets.QListWidget()
    timeline_events.setMinimumHeight(180)
    timeline_events.setSelectionMode(QABSTRACTITEMVIEW_SINGLE)
    timeline_events.setToolTip("Mission events derived from telemetry stream")
    list_sel_delegate = OutlineSelectionDelegate(selection_outline, timeline_events)
    timeline_events.setItemDelegate(list_sel_delegate)
    timeline_layout.addWidget(timeline_events, 2)

    tabs.addTab(timeline_widget, "Mission Timeline")
    # Reference holder for timeline updates
    timeline_events_ref = timeline_events
    # Reference holder for latest decoded keyframes (Timeline sync)
    keyframes_ref = []

    # ---------------------------------------------------------------------
    # RF Metrics tab (META frames from receiver)
    # ---------------------------------------------------------------------
    rf_widget = QtWidgets.QWidget()
    rf_layout = QVBoxLayout(rf_widget)
    rf_layout.setContentsMargins(6, 6, 6, 6)

    rf_top = QHBoxLayout()
    rf_layout.addLayout(rf_top)

    rf_led_phy = QLabel("PHY")
    rf_led_app = QLabel("APP")
    rf_led_full = QLabel("FULL")
    rf_led_delta = QLabel("DELTA")
    for led, col in ((rf_led_phy, "#00cc66"), (rf_led_app, "#00ccff"), (rf_led_full, "#2ecc71"), (rf_led_delta, "#3498db")):
        _set_led(led, False, col)
        rf_top.addWidget(led)

    rf_lbl = QLabel("RF META: —")
    rf_lbl.setStyleSheet("QLabel { color: #ccc; padding-left: 8px; }")
    rf_top.addWidget(rf_lbl, 1)

    rf_grid = QGridLayout()
    rf_layout.addLayout(rf_grid)

    rf_score_fw = LinearBar(0, 100, "LINK FW", "")
    rf_score_pc = LinearBar(0, 100, "LINK PC", "")
    rf_rssi_pkt = LinearBar(-150, 0, "PktStr", " dBm", good_high=True)
    # Instant RSSI is better interpreted as channel energy/noise floor: lower (more negative) is better.
    rf_rssi_inst = LinearBar(-150, 0, "Noise (inst)", " dBm", good_high=False)
    rf_snr = LinearBar(-32, 31.75, "SNR", " dB")
    rf_fei = CenteredBar(60000, "FEI", " Hz")
    rf_ofs = CenteredBar(60000, "OFFSET", " Hz")

    rf_grid.addWidget(rf_score_fw, 0, 0, 1, 2)
    rf_grid.addWidget(rf_score_pc, 1, 0, 1, 2)
    rf_grid.addWidget(rf_rssi_pkt, 2, 0, 1, 2)
    rf_grid.addWidget(rf_rssi_inst, 3, 0, 1, 2)
    rf_grid.addWidget(rf_snr, 4, 0, 1, 2)
    rf_grid.addWidget(rf_fei, 5, 0, 1, 2)
    rf_grid.addWidget(rf_ofs, 6, 0, 1, 2)

    rf_info_box = QGroupBox("Registers / Counters")
    rf_info_layout = QFormLayout(rf_info_box)
    rf_layout.addWidget(rf_info_box)

    rf_lbl_len = QLabel("—")
    rf_lbl_modem = QLabel("—")
    rf_lbl_irq = QLabel("—")
    rf_lbl_bw = QLabel("—")
    rf_lbl_cnt = QLabel("—")
    rf_lbl_seqmet = QLabel("—")

    for lab in (rf_lbl_len, rf_lbl_modem, rf_lbl_irq, rf_lbl_bw, rf_lbl_cnt, rf_lbl_seqmet):
        lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lab.setStyleSheet("QLabel { color: #ddd; }")

    rf_info_layout.addRow("Payload len:", rf_lbl_len)
    rf_info_layout.addRow("ModemStat:", rf_lbl_modem)
    rf_info_layout.addRow("IrqFlags:", rf_lbl_irq)
    rf_info_layout.addRow("BW/SF/CR:", rf_lbl_bw)
    rf_info_layout.addRow("Hdr/Pkt cnt:", rf_lbl_cnt)
    rf_info_layout.addRow("SEQ / MET:", rf_lbl_seqmet)

    tabs.addTab(rf_widget, "RF Metrics")

    # ---------------------------------------------------------------------
    # RF Trends tab (time-series from META frames)
    # ---------------------------------------------------------------------
    rftr_widget = QtWidgets.QWidget()
    rftr_layout = QVBoxLayout(rftr_widget)
    rftr_layout.setContentsMargins(6, 6, 6, 6)

    rftr_plots = pg.GraphicsLayoutWidget()
    rftr_layout.addWidget(rftr_plots, 1)

    # 2x2 layout:
    # (0,0) RSSI pkt + noise
    # (0,1) SNR
    # (1,0) FEI + OFFSET
    # (1,1) Link score (FW + PC)
    rftr_p_rssi = rftr_plots.addPlot(title="RSSI / Noise (dBm)")
    rftr_plots.nextColumn()
    rftr_p_snr = rftr_plots.addPlot(title="SNR (dB)")
    rftr_plots.nextRow()
    rftr_p_fei = rftr_plots.addPlot(title="FEI / OFFSET (Hz)")
    rftr_plots.nextColumn()
    rftr_p_score = rftr_plots.addPlot(title="Link Score (0–100)")

    for p in (rftr_p_rssi, rftr_p_snr, rftr_p_fei, rftr_p_score):
        try:
            p.showGrid(x=True, y=True, alpha=0.25)
            p.setLabel("bottom", "Sample")
        except Exception:
            pass

    # Curves
    rftr_rssi_pkt_curve = rftr_p_rssi.plot([], pen=pg.mkPen("#00ccff", width=2), name="PktStr")
    rftr_rssi_inst_curve = rftr_p_rssi.plot([], pen=pg.mkPen("#aaaaaa", width=1), name="Noise(inst)")
    try:
        rftr_p_rssi.addLegend(offset=(10, 10))
    except Exception:
        pass

    rftr_snr_curve = rftr_p_snr.plot([], pen=pg.mkPen("#ffcc66", width=2), name="SNR")

    rftr_fei_curve = rftr_p_fei.plot([], pen=pg.mkPen("#66ff99", width=2), name="FEI")
    rftr_ofs_curve = rftr_p_fei.plot([], pen=pg.mkPen("#ff9966", width=2), name="OFFSET")
    try:
        rftr_p_fei.addLegend(offset=(10, 10))
    except Exception:
        pass

    rftr_score_fw_curve = rftr_p_score.plot([], pen=pg.mkPen("#2ecc71", width=2), name="FW")
    rftr_score_pc_curve = rftr_p_score.plot([], pen=pg.mkPen("#dddddd", width=2), name="PC")
    try:
        rftr_p_score.addLegend(offset=(10, 10))
    except Exception:
        pass

    # Cursor marker (sync to selected sample)
    rftr_marker_pen = pg.mkPen(color=(255, 255, 0, 160), width=2, style=QtCore.Qt.DashLine)
    rftr_rssi_marker = pg.InfiniteLine(angle=90, movable=False, pen=rftr_marker_pen)
    rftr_snr_marker = pg.InfiniteLine(angle=90, movable=False, pen=rftr_marker_pen)
    rftr_fei_marker = pg.InfiniteLine(angle=90, movable=False, pen=rftr_marker_pen)
    rftr_score_marker = pg.InfiniteLine(angle=90, movable=False, pen=rftr_marker_pen)
    rftr_p_rssi.addItem(rftr_rssi_marker)
    rftr_p_snr.addItem(rftr_snr_marker)
    rftr_p_fei.addItem(rftr_fei_marker)
    rftr_p_score.addItem(rftr_score_marker)

    tabs.addTab(rftr_widget, "RF Trends")
    # Frame diagnostic record:
    # {
    #   type: "FULL" | "DELTA",
    #   seq: int,
    #   ref_seq: Optional[int],
    #   crc_ok: bool,
    #   status: "ACCEPTED" | "DROPPED_NO_REF" | "DROPPED_CRC" | "DROPPED_REF_MISMATCH"
    # }

    def decode_frames_verbose(raw: bytes, allow_crc_fail: bool = False):
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

        def _consume_meta_at(pos: int) -> int:
            """
            Consume an RF META frame only at a known frame boundary.
            This prevents accidentally matching SYNC_META1/SYNC_META2 inside
            FULL/DELTA payload bytes (which are essentially random).
            Returns number of bytes consumed (0 if no META found).
            """
            if pos < 0:
                return 0
            if (pos + META_FRAME_LEN) > n:
                return 0
            if raw[pos] != SYNC_META1 or raw[pos + 1] != SYNC_META2:
                return 0
            frame = raw[pos:pos + META_FRAME_LEN]
            meta = parse_rf_meta_frame(frame)
            if not meta:
                frames_diag.append({
                    "type": "META",
                    "seq": None,
                    "ref_seq": None,
                    "crc_ok": False,
                    "status": "DROPPED_CRC",
                    "reason": "META CRC8/len/version mismatch."
                })
                return 1  # resync: step one byte
            # Attach this META to the last decoded sample index (packet-level meta follows
            # a FULL/DELTA that carries 8 samples). For mid-stream META (no samples yet),
            # this stays None.
            meta["_sample_idx"] = (sample_index - 1) if sample_index > 0 else None
            frames_diag.append({
                "type": "META",
                "seq": meta.get("seq"),
                "ref_seq": None,
                "crc_ok": True,
                "status": "ACCEPTED",
                "reason": f"RF SCORE={meta['link_score']} RSSI={meta['rssi_pkt_dbm']} SNR={meta['snr_db']:.1f} FEI={meta['fei_hz']}Hz",
                "meta": meta,
                "sample_idx": meta.get("_sample_idx"),
            })
            return META_FRAME_LEN

        frame_num = 0
        while i < n:
            sync = raw[i]

            # META can appear when logging starts mid-stream; handle it, but avoid
            # scanning META inside full/delta payload bytes by consuming it only at
            # a top-level sync boundary.
            if sync == SYNC_META1:
                consumed = _consume_meta_at(i)
                i += max(1, consumed)
                frame_num += 1
                continue

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
                frames_diag.append({
                    "type": ftype,
                    "seq": None,
                    "ref_seq": None,
                    "crc_ok": False,
                    "status": "DROPPED_TRUNC",
                    "reason": "Frame header found, but buffer ended before full frame length."
                })
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
                if not allow_crc_fail:
                    frames_diag.append({
                        "type": ftype,
                        "seq": frame[4] if flen > 4 else None,
                        "ref_seq": frame[5] if (ftype == "DELTA" and flen > 5) else None,
                        "crc_ok": False,
                        "status": "DROPPED_CRC",
                        "reason": "CRC16 mismatch."
                    })
                    i += 1
                    frame_num += 1
                    continue

                # OFFLINE recovery mode: accept frames with CRC mismatch only if the
                # header is self-consistent (prevents most false positives).
                if sync == SYNC_FULL:
                    flags = frame[3]
                    validity = frame[5]
                    full_state_ok = (flags & 0x01) != 0
                    delta_state_ok = (flags & 0x02) == 0
                    validity_ok = (validity & 0xF8) == 0  # only bits0..2 are used
                    if not (full_state_ok and delta_state_ok and validity_ok):
                        frames_diag.append({
                            "type": "FULL",
                            "seq": frame[4],
                            "ref_seq": None,
                            "crc_ok": False,
                            "status": "DROPPED_CRC",
                            "reason": "CRC16 mismatch (lenient mode: header check failed)."
                        })
                        i += 1
                        frame_num += 1
                        continue
                else:
                    # DELTA: require delta-state bit set and full-state bit clear
                    flags = frame[3]
                    full_state_ok = (flags & 0x01) == 0
                    delta_state_ok = (flags & 0x02) != 0
                    if not (full_state_ok and delta_state_ok):
                        frames_diag.append({
                            "type": "DELTA",
                            "seq": frame[4],
                            "ref_seq": frame[5],
                            "crc_ok": False,
                            "status": "DROPPED_CRC",
                            "reason": "CRC16 mismatch (lenient mode: header check failed)."
                        })
                        i += 1
                        frame_num += 1
                        continue

            if sync == SYNC_FULL:
                frame_sample_start = sample_index
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

                frames_diag.append({
                    "type": "FULL",
                    "seq": frame[4],
                    "ref_seq": None,
                    "crc_ok": bool(crc_ok),
                    "status": "ACCEPTED" if crc_ok else "ACCEPTED_NO_CRC",
                    "reason": "FULL keyframe accepted." if crc_ok else "FULL accepted (CRC mismatch; OFFLINE lenient mode).",
                    "sample_start": frame_sample_start,
                    "sample_end": sample_index - 1
                })
                i += flen
                i += _consume_meta_at(i)
                frame_num += 1
                continue

            # DELTA frame
            seq = frame[4]
            ref_key_seq = frame[5]

            # If receiver starts mid-stream, we must wait for a keyframe.
            # Also drop deltas that reference a different keyframe than our last one.
            if not have_ref:
                frames_diag.append({
                    "type": "DELTA",
                    "seq": seq,
                    "ref_seq": ref_key_seq,
                    "crc_ok": bool(crc_ok),
                    "status": "DROPPED_NO_REF",
                    "reason": "DELTA received before any keyframe.",
                    "sample_start": None,
                    "sample_end": None
                })
                i += flen
                i += _consume_meta_at(i)
                frame_num += 1
                continue

            if last_key_seq is not None and ref_key_seq != last_key_seq:
                frames_diag.append({
                    "type": "DELTA",
                    "seq": seq,
                    "ref_seq": ref_key_seq,
                    "crc_ok": bool(crc_ok),
                    "status": "DROPPED_REF_MISMATCH",
                    "reason": "DELTA references a different keyframe than the last accepted FULL.",
                    "sample_start": None,
                    "sample_end": None
                })
                i += flen
                i += _consume_meta_at(i)
                frame_num += 1
                continue

            frame_sample_start = sample_index
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

            frames_diag.append({
                "type": "DELTA",
                "seq": seq,
                "ref_seq": ref_key_seq,
                "crc_ok": bool(crc_ok),
                "status": "ACCEPTED" if crc_ok else "ACCEPTED_NO_CRC",
                "reason": "DELTA frame accepted and applied." if crc_ok else "DELTA accepted (CRC mismatch; OFFLINE lenient mode).",
                "sample_start": frame_sample_start,
                "sample_end": sample_index - 1
            })
            i += flen
            i += _consume_meta_at(i)
            frame_num += 1

        return Ts, Hs, Ps, keyframe_idx, frames_diag

    # ---------------------------------------------------------------------
    # Decode cache (single decode per buffer version)
    # ---------------------------------------------------------------------
    class DecodeCache:
        def __init__(self):
            self._sig = None
            self._result = None

        @staticmethod
        def _signature(b: bytes, allow_crc_fail: bool):
            tail = b[-64:] if len(b) > 64 else b
            return (bool(allow_crc_fail), len(b), tail)

        def decode(self, b: bytes, allow_crc_fail: bool = False):
            sig = self._signature(b, allow_crc_fail)
            if self._sig == sig and self._result is not None:
                return self._result
            self._result = decode_frames_verbose(b, allow_crc_fail=bool(allow_crc_fail))
            self._sig = sig
            return self._result

        def invalidate(self):
            self._sig = None
            self._result = None

    decode_cache = DecodeCache()

    # ---------------------------------------------------------------------
    # Mission Timeline logic (extracted)
    # ---------------------------------------------------------------------
    class TimelineEngine:
        """Derive mission events and timeline items from decoded sample arrays."""

        def __init__(self, sample_period_s: float = 0.5):
            self.sample_period_s = float(sample_period_s)

        @staticmethod
        def _avg(seq):
            return (sum(seq) / len(seq)) if seq else 0.0

        @staticmethod
        def _stable(win, tol):
            return (max(win) - min(win)) < tol if win else False

        def derive(self, Ts, Hs, Ps, keyframes):
            """
            Pressure-driven fázisdetektálás (liftoff→apogee→descent→landed).
            Visszaad:
              {
                "mission_events": [(name, idx)],
                "adaptive_kf": [idx],
                "timeline_items": [(text, idx_or_None, (bg,fg)_or_None)]
              }
            """
            mission_events = []
            timeline_items = []

            if not Ts or not Hs or not Ps or len(Ps) < 8:
                return {"mission_events": mission_events, "adaptive_kf": [], "timeline_items": timeline_items}

            # Paraméterek (adaptive: ground zajhoz viszonyított küszöbök)
            WIN_STABLE = 24          # ~12 s ablak stabilitáshoz
            WIN_SLOPE = 12           # derivált simítás (~6 s)
            GROUND_RANGE = 3.5       # hPa belső tartomány stabilnak
            GROUND_SLOPE = 0.4       # hPa/step maximum stabil talajon
            # Liftoff / descent küszöbök később, ground zaj alapján (sigma alapú)
            LIFTOFF_ABS_DROP = 8.0   # hPa abszolút esés ground szinthez képest
            LAND_RANGE = 6.0         # hPa ground közelség landoláshoz
            LAND_STABLE = 3.0        # hPa tartomány landoláskor

            def movavg_series(seq, w):
                if w <= 1:
                    return list(seq)
                out = []
                acc = 0.0
                for i, v in enumerate(seq):
                    acc += v
                    if i >= w:
                        acc -= seq[i - w]
                    if i + 1 >= w:
                        out.append(acc / w)
                    else:
                        out.append(acc / (i + 1))
                return out

            def moving_avg(seq, w):
                out = []
                acc = 0.0
                for i, v in enumerate(seq):
                    acc += v
                    if i >= w:
                        acc -= seq[i - w]
                    if i + 1 >= w:
                        out.append(acc / w)
                return out

            # Kis simítás a zaj ellen (fázisdetektálásra, nem a plotra)
            P_f = movavg_series(Ps, 5)

            # 1) Ground szint és stabil ablak keresése:
            # CanSat-nál a GROUND tipikusan a legmagasabb nyomású stabil szakasz.
            ground_p = None
            ground_idx = 0
            ground_window = None
            candidates = []
            for i in range(WIN_STABLE, len(P_f)):
                pwin = P_f[i - WIN_STABLE:i]
                if (max(pwin) - min(pwin)) < GROUND_RANGE:
                    slopes = [pwin[j] - pwin[j - 1] for j in range(1, len(pwin))]
                    if max(abs(s) for s in slopes) < GROUND_SLOPE:
                        candidates.append((self._avg(pwin), i, list(pwin)))

            if candidates:
                # CanSat esetben a log tipikusan a földön indul, ezért az első stabil, "magas nyomású"
                # szegmenst tekintjük induló GROUND-nak. Ha a felvétel nem a földön indul (mid-flight),
                # akkor az első stabil szegmens nyomása tipikusan jelentősen alacsonyabb lesz, ezért
                # visszaesünk a legmagasabb átlagnyomású stabil szegmensre.
                best_high = max(m for (m, _, _) in candidates)
                tol = max(4.0, 8.0 * (0.2))  # lazább tolerancia (hPa), később a zajhoz igazítjuk
                # a zajt csak később számoljuk, ezért itt fix de óvatos toleranciát használunk

                candidates_sorted = sorted(candidates, key=lambda x: x[1])
                early = None
                for m, i, w in candidates_sorted:
                    if m >= (best_high - tol):
                        early = (m, i, w)
                        break

                if early is None:
                    # fallback: legmagasabb átlagnyomású stabil ablak
                    candidates_sorted = sorted(candidates, key=lambda x: (-x[0], x[1]))
                    ground_p, ground_idx, ground_window = candidates_sorted[0]
                else:
                    ground_p, ground_idx, ground_window = early

                # GROUND eseményt a stabil ablak elejére tesszük (misszió indulás jelölése)
                ground_start_idx = max(0, int(ground_idx) - WIN_STABLE)
                mission_events.append(("GROUND", ground_start_idx))

            if ground_p is None:
                # Nem talált stabil ground-ot: legalább keyframe lista legyen
                timeline_items.append(("Nincs stabil GROUND detektálva (állíts küszöböket).", None, None))
                timeline_items.append(("────────── KEYFRAMES ──────────", None, None))
                for kf_idx in keyframes or []:
                    met_sec = kf_idx * self.sample_period_s
                    timeline_items.append((f"KEYFRAME  |  sample {kf_idx}  |  MET ≈ {met_sec:.1f} s", int(kf_idx), None))
                return {"mission_events": mission_events, "adaptive_kf": [], "timeline_items": timeline_items}

            # 2) Robosztus zajbecslés a ground ablakból (median abs(dP))
            try:
                gd = [ground_window[i] - ground_window[i - 1] for i in range(1, len(ground_window or []))]
                abs_gd = sorted(abs(x) for x in gd) or [0.1]
                noise = float(abs_gd[len(abs_gd) // 2])
                noise = max(0.05, noise)
            except Exception:
                noise = 0.2

            # 3) Liftoff/ASCENT: nem csak derivált, hanem tartós abs esés is (hysteresis)
            drop_abs = max(LIFTOFF_ABS_DROP, 12.0 * noise)
            consec = max(3, int(round(2.0 / max(self.sample_period_s, 0.1))))  # ~2 s

            ascent_start = None
            start_idx = max(ground_idx, WIN_STABLE)
            for i in range(start_idx, len(P_f) - consec):
                if (ground_p - P_f[i]) < drop_abs:
                    continue
                # tartósan lent marad-e?
                ok = True
                for j in range(i, i + consec):
                    if (ground_p - P_f[j]) < (0.7 * drop_abs):
                        ok = False
                        break
                if ok:
                    ascent_start = i
                    mission_events.append(("ASCENT", i))
                    break

            if ascent_start is None:
                # Ne legyen üres: GROUND-ot már látjuk, csak a liftoff hiányzik.
                timeline_items.append(("ASCENT nem detektálható (tartós nyomásesés nincs a GROUND-hoz képest).", None, None))
                # Timeline összeállítás később (events + keyframes)
                adaptive_kf = []
                # 8) Timeline elemek
                style_map = {
                    "GROUND":  (QtGui.QColor(220, 220, 220), QtGui.QColor(20, 20, 20)),
                    "ASCENT":  (QtGui.QColor(60, 120, 200),  QtGui.QColor(255, 255, 255)),
                    "APOGEE":  (QtGui.QColor(255, 200, 60),  QtGui.QColor(20, 20, 20)),
                    "DESCENT": (QtGui.QColor(60, 200, 200),  QtGui.QColor(20, 20, 20)),
                    "LANDED":  (QtGui.QColor(80, 200, 120),  QtGui.QColor(20, 20, 20)),
                }
                for name, idx in mission_events:
                    met_sec = idx * self.sample_period_s
                    timeline_items.append((f"{name}  |  sample {idx}  |  MET ≈ {met_sec:.1f} s", int(idx), style_map.get(name)))
                timeline_items.append(("────────── KEYFRAMES ──────────", None, None))
                for kf_idx in keyframes or []:
                    met_sec = kf_idx * self.sample_period_s
                    timeline_items.append((f"KEYFRAME  |  sample {kf_idx}  |  MET ≈ {met_sec:.1f} s", int(kf_idx), None))
                return {"mission_events": mission_events, "adaptive_kf": adaptive_kf, "timeline_items": timeline_items}

            # 4) Apogee: minimum nyomás + (gyakran) plató/szaturáció detektálás
            min_p = min(P_f[ascent_start:])
            eps = max(1.0, 4.0 * noise)
            plateau_min_len = max(8, int(round(4.0 / max(self.sample_period_s, 0.1))))  # ~4 s

            plateau_start = None
            plateau_end = None
            run = 0
            run_start = None
            for i in range(ascent_start, len(P_f)):
                if P_f[i] <= (min_p + eps):
                    if run == 0:
                        run_start = i
                    run += 1
                else:
                    if run >= plateau_min_len:
                        plateau_start = run_start
                        plateau_end = i - 1
                        break
                    run = 0
                    run_start = None
            if plateau_start is None and run >= plateau_min_len:
                plateau_start = run_start
                plateau_end = len(P_f) - 1

            if plateau_start is not None:
                apogee_idx = int((plateau_start + plateau_end) // 2)
            else:
                apogee_idx = ascent_start + P_f[ascent_start:].index(min_p)
            mission_events.append(("APOGEE", apogee_idx))

            # 5) DESCENT: nyomás tartós emelkedése a minimum/plató után
            rise_abs = max(8.0, 12.0 * noise)
            descent_idx = None
            scan_from = (plateau_end + 1) if plateau_end is not None else (apogee_idx + 1)
            scan_from = max(scan_from, apogee_idx + 1)
            for i in range(scan_from, len(P_f) - consec):
                if (P_f[i] - min_p) < rise_abs:
                    continue
                ok = True
                for j in range(i, i + consec):
                    if (P_f[j] - min_p) < (0.7 * rise_abs):
                        ok = False
                        break
                if ok:
                    descent_idx = i
                    mission_events.append(("DESCENT", i))
                    break

            # 6) LANDED: vissza ground közelébe és stabil
            land_idx = None
            if descent_idx is not None:
                for i in range(descent_idx + WIN_STABLE, len(P_f)):
                    pwin = P_f[i - WIN_STABLE:i]
                    if abs(self._avg(pwin) - ground_p) < LAND_RANGE and (max(pwin) - min(pwin)) < LAND_STABLE:
                        land_idx = i
                        mission_events.append(("LANDED", i))
                        break

            # 7) Adaptive keyframe javaslat (ritka események)
            adaptive_kf = []
            cooldown = 10
            last_kf = -cooldown
            for i in range(3, len(Ps)):
                dP1 = Ps[i] - Ps[i - 1]
                dP2 = Ps[i - 1] - Ps[i - 2]
                d2P = dP1 - dP2
                if abs(d2P) > 3.0:
                    if i - last_kf >= cooldown:
                        adaptive_kf.append(i)
                        last_kf = i
            adaptive_kf = sorted(set(adaptive_kf))

            # 8) Timeline elemek
            style_map = {
                "GROUND":  (QtGui.QColor(220, 220, 220), QtGui.QColor(20, 20, 20)),
                "ASCENT":  (QtGui.QColor(60, 120, 200),  QtGui.QColor(255, 255, 255)),
                "APOGEE":  (QtGui.QColor(255, 200, 60),  QtGui.QColor(20, 20, 20)),
                "DESCENT": (QtGui.QColor(60, 200, 200),  QtGui.QColor(20, 20, 20)),
                "LANDED":  (QtGui.QColor(80, 200, 120),  QtGui.QColor(20, 20, 20)),
            }

            if mission_events:
                for name, idx in mission_events:
                    met_sec = idx * self.sample_period_s
                    timeline_items.append((f"{name}  |  sample {idx}  |  MET ≈ {met_sec:.1f} s", int(idx), style_map.get(name)))
            else:
                timeline_items.append(("Nincs mission esemény detektálva.", None, None))

            timeline_items.append(("────────── KEYFRAMES ──────────", None, None))

            for kf_idx in keyframes or []:
                met_sec = kf_idx * self.sample_period_s
                timeline_items.append((
                    f"KEYFRAME  |  sample {kf_idx}  |  MET ≈ {met_sec:.1f} s",
                    int(kf_idx),
                    None
                ))

            for akf in adaptive_kf:
                met_sec = akf * self.sample_period_s
                timeline_items.append((
                    f"ADAPTIVE KF  |  sample {akf}  |  MET ≈ {met_sec:.1f} s",
                    int(akf),
                    None
                ))

            return {"mission_events": mission_events, "adaptive_kf": adaptive_kf, "timeline_items": timeline_items}

    timeline_engine = TimelineEngine(sample_period_s=0.5)

    # Plot area container with toggle for orientation
    plot_container = QtWidgets.QWidget()
    plot_layout = QtWidgets.QVBoxLayout(plot_container)
    plot_layout.setContentsMargins(0, 0, 0, 0)
    right_vsplit.insertWidget(0, plot_container)

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
    # Playback "future" shading regions (from playhead -> end)
    t_future = None
    h_future = None
    p_future = None

    # PlotItem refs (needed for Mission Timeline markers)
    p_temp = None
    p_hum = None
    p_pres = None

    # Mission event markers (InfiniteLine/TextItem) – updated from telemetry
    mission_events_ref = []     # list of (name:str, sample_idx:int)
    # NOTE: Do NOT reuse a single GraphicsItem across plots. Keep per-plot items.
    event_lines = []            # list of (ln_temp, ln_hum, ln_pres)
    event_labels = []           # list of pg.TextItem (kept empty when only dots)
    # State bands (background colored time ranges)
    state_regions = []          # list of (reg_temp, reg_hum, reg_pres)
    # Mission scatter markers per plot
    event_scatters = []         # list of (scat_t, scat_h, scat_p)

    marker_pen = pg.mkPen(color=(255, 255, 0), width=2)
    kf_scatter_pen = pg.mkPen(None)
    kf_scatter_brush = pg.mkBrush(255, 255, 0, 120)

    # Single-plot mode (only in Vertical layout)
    single_mode = False
    single_channel = "P"  # "T" | "H" | "P"

    # --- Playback FSM ---
    PLAY_STOPPED = 0
    PLAY_RUNNING = 1
    PLAY_PAUSED  = 2

    play_state = PLAY_STOPPED
    play_idx = None
    play_base_idx = 0
    play_wall0 = None
    play_speed = 1.0
    live_mode = False
    online_started = False
    last_stop_wall = None

    playback_timer = QtCore.QTimer()
    playback_timer.setInterval(50)

    def _format_met(seconds: float) -> str:
        if seconds < 0:
            seconds = 0.0
        sec_int = int(seconds)
        frac = seconds - sec_int
        h = sec_int // 3600
        m = (sec_int % 3600) // 60
        s = sec_int % 60
        # 0.5 s resolution -> show 1 decimal
        return f"{h:02d}:{m:02d}:{s:02d}.{int(round(frac * 10))%10}"

    def _cursor_sample_idx() -> int:
        # If user selected a row, follow that. Otherwise follow "latest" sample.
        if table.currentRow() >= 0:
            idx = int(table.currentRow())
        else:
            idx = max(0, table.rowCount() - 1)
        if table.rowCount() > 0:
            return max(0, min(idx, table.rowCount() - 1))
        return 0

    def _playhead_sample_idx() -> int:
        # Prefer playback head when playing/paused; otherwise follow cursor/latest.
        if play_idx is not None:
            idx = int(play_idx) - 1
            if table.rowCount() > 0:
                return max(0, min(idx, table.rowCount() - 1))
            return max(0, idx)
        return _cursor_sample_idx()

    def _set_live_mode(on: bool):
        nonlocal live_mode, play_state, play_idx, play_base_idx, play_wall0, play_speed
        live_mode = bool(on)
        if not live_mode:
            return
        # Snap to the newest available sample and run at 1x.
        play_speed = 1.0
        if table.rowCount() > 0:
            newest = table.rowCount() - 1
            play_base_idx = newest
            play_wall0 = time.monotonic()
            play_idx = newest + 1
            table.selectRow(newest)
        play_state = PLAY_RUNNING
        btn_play.setChecked(True)
        update_time_displays()
        update_view_only()

    def _set_play_speed(speed: float):
        nonlocal play_speed, play_wall0, play_base_idx
        try:
            speed = float(speed)
        except Exception:
            speed = 1.0
        if speed <= 0:
            speed = 1.0
        # Preserve continuity: re-base clock from current playhead.
        cur = _playhead_sample_idx()
        play_speed = speed
        play_base_idx = cur
        play_wall0 = time.monotonic()

    def _update_playhead_from_clock():
        nonlocal play_idx, play_state, play_wall0, play_base_idx
        if play_state != PLAY_RUNNING:
            return
        if play_wall0 is None:
            play_wall0 = time.monotonic()
        # target sample index based on wall clock (0.5s/sample)
        elapsed = max(0.0, time.monotonic() - play_wall0)
        target = play_base_idx + int(elapsed * float(play_speed) / 0.5)
        max_idx = max(0, table.rowCount() - 1)
        target = max(0, min(target, max_idx))
        # play_idx is "end" (exclusive)
        play_idx = target + 1

    time_timer = QtCore.QTimer()
    time_timer.setInterval(500)  # 2 Hz

    def update_time_displays():
        try:
            # While scrubbing, preview the slider position.
            if seek_slider.isSliderDown():
                idx = int(seek_slider.value())
            else:
                idx = _playhead_sample_idx()
            met_s = idx * 0.5
            lbl_met.setText(f"MET: {_format_met(met_s)}  |  sample {idx}")
        except Exception:
            pass
        try:
            lbl_clock.setText(f"Local: {datetime.now().strftime('%H:%M:%S')}")
        except Exception:
            pass

        # Keep seek slider synced to data (but don't fight the user's drag).
        try:
            max_idx = max(0, table.rowCount() - 1)
            if seek_slider.maximum() != max_idx:
                seek_slider.setRange(0, max_idx)
            if not seek_slider.isSliderDown():
                seek_slider.setValue(int(_playhead_sample_idx()))
        except Exception:
            pass

    time_timer.timeout.connect(update_time_displays)

    def on_playback_tick():
        nonlocal play_idx, play_state

        if play_state != PLAY_RUNNING:
            playback_timer.stop()
            return

        _update_playhead_from_clock()

        update_time_displays()
        update_view_only()
    def on_play():
        nonlocal play_idx, play_state, play_wall0, play_base_idx, live_mode
        if decode_cache._result is None:
            update_from_raw()
        live_mode = False
        play_state = PLAY_RUNNING
        btn_play.setChecked(True)
        start_idx = _playhead_sample_idx() if play_idx is not None else _cursor_sample_idx()
        play_base_idx = int(start_idx)
        play_wall0 = time.monotonic()
        play_idx = int(start_idx) + 1
        update_time_displays()
        playback_timer.start()

    def on_pause():
        nonlocal play_state, live_mode
        live_mode = False
        play_state = PLAY_PAUSED
        btn_pause.setChecked(True)
        update_time_displays()
        playback_timer.stop()

    def on_stop():
        nonlocal play_idx, play_state, live_mode, play_wall0, play_base_idx, last_stop_wall
        live_mode = False
        now = time.monotonic()
        double = (play_state == PLAY_STOPPED) and (last_stop_wall is not None) and ((now - last_stop_wall) < 0.9)
        last_stop_wall = now

        btn_stop.setChecked(True)
        play_state = PLAY_STOPPED
        play_wall0 = None

        if double:
            play_base_idx = 0
            play_idx = None
            if table.rowCount() > 0:
                table.selectRow(0)
        else:
            # Stop keeps the current position (show full data, keep cursor).
            idx = _playhead_sample_idx()
            play_base_idx = idx
            play_idx = None
            if table.rowCount() > 0:
                table.selectRow(idx)
        update_time_displays()
        playback_timer.stop()
        update_view_only()

    def on_ff():
        nonlocal play_idx, live_mode, play_state, play_wall0, play_base_idx
        Ts, _, _, _, _ = decode_cache._result or ([], [], [], [], [])
        if play_idx is not None:
            live_mode = False
            play_idx = min(play_idx + 20, len(Ts))
            # Snap to live if we're at the end
            if play_idx >= len(Ts):
                _set_live_mode(True)
                return
            play_base_idx = max(0, int(play_idx) - 1)
            play_wall0 = time.monotonic()
            update_view_only()

    def on_rw():
        nonlocal play_idx, live_mode, play_state, play_wall0, play_base_idx
        if play_idx is not None:
            live_mode = False
            play_idx = max(0, play_idx - 20)
            play_base_idx = max(0, int(play_idx) - 1)
            play_wall0 = time.monotonic()
            update_view_only()

    playback_timer.timeout.connect(on_playback_tick)
    btn_play.clicked.connect(on_play)
    btn_pause.clicked.connect(on_pause)
    btn_stop.clicked.connect(on_stop)
    btn_ff.clicked.connect(on_ff)
    btn_rw.clicked.connect(on_rw)

    # Guard against recursive UI updates (table selection <-> seek <-> update_from_raw)
    ui_sync_busy = False

    def _seek_to(idx: int):
        nonlocal play_idx, live_mode, play_state, play_base_idx, play_wall0, ui_sync_busy
        idx = int(idx)
        if table.rowCount() > 0:
            idx = max(0, min(idx, table.rowCount() - 1))
        # Seeking puts us into time-shift mode but does NOT pause automatically.
        live_mode = False
        if play_state == PLAY_RUNNING or play_state == PLAY_PAUSED:
            play_base_idx = idx
            play_wall0 = time.monotonic()
            play_idx = idx + 1
        else:
            play_base_idx = idx
            play_wall0 = None
            play_idx = None
        # Update UI elements without triggering recursive callbacks.
        if ui_sync_busy:
            return
        ui_sync_busy = True
        try:
            try:
                seek_slider.blockSignals(True)
                seek_slider.setValue(int(idx))
            except Exception:
                pass
            finally:
                try:
                    seek_slider.blockSignals(False)
                except Exception:
                    pass

            if 0 <= idx < table.rowCount():
                try:
                    table.blockSignals(True)
                    table.selectRow(idx)
                except Exception:
                    pass
                finally:
                    try:
                        table.blockSignals(False)
                    except Exception:
                        pass
        finally:
            ui_sync_busy = False
        update_time_displays()
        update_view_only()

    seek_slider.sliderReleased.connect(lambda: _seek_to(seek_slider.value()))
    seek_slider.sliderMoved.connect(lambda v: update_time_displays())

    def _on_speed_button():
        # Keep speed change seamless.
        if btn_sp1.isChecked():
            _set_play_speed(1.0)
        elif btn_sp2.isChecked():
            _set_play_speed(2.0)
        elif btn_sp4.isChecked():
            _set_play_speed(4.0)
        elif btn_sp8.isChecked():
            _set_play_speed(8.0)
        update_time_displays()

    btn_sp1.clicked.connect(_on_speed_button)
    btn_sp2.clicked.connect(_on_speed_button)
    btn_sp4.clicked.connect(_on_speed_button)
    btn_sp8.clicked.connect(_on_speed_button)

    def _curve_data(curve):
        """Safe getter for PlotDataItem data; returns (xs, ys) as lists."""
        if curve is None:
            return [], []
        try:
            xdata, ydata = curve.getData()
        except Exception:
            return [], []
        if xdata is None or ydata is None:
            return [], []
        return list(xdata), list(ydata)

    def _auto_range_plots():
        """Keep plot ranges tied to data, not to overlaid labels/regions."""
        for curve, plot in ((t_curve, p_temp), (h_curve, p_hum), (p_curve, p_pres)):
            if curve is None or plot is None:
                continue
            xs, ys = _curve_data(curve)
            if not xs or not ys:
                continue
            x_min = min(xs)
            x_max = max(xs)
            if x_max == x_min:
                x_min -= 1.0
                x_max += 1.0
            y_min = min(ys)
            y_max = max(ys)
            if y_max == y_min:
                pad = abs(y_max) * 0.05 + 1.0
                y_min -= pad
                y_max += pad
            plot.setXRange(x_min, x_max, padding=0.02)
            plot.setYRange(y_min, y_max, padding=0.1)

    def rebuild_plots(horizontal: bool):
        nonlocal t_curve, h_curve, p_curve
        nonlocal t_marker, h_marker, p_marker
        nonlocal t_kf, h_kf, p_kf
        nonlocal p_temp, p_hum, p_pres
        nonlocal t_future, h_future, p_future

        # Preserve current data before rebuild (robust to empty curves)
        t_x_cur, t_y_cur = _curve_data(t_curve)
        h_x_cur, h_y_cur = _curve_data(h_curve)
        p_x_cur, p_y_cur = _curve_data(p_curve)

        # Preserve marker positions
        t_marker_pos = t_marker.value() if t_marker is not None else None
        h_marker_pos = h_marker.value() if h_marker is not None else None
        p_marker_pos = p_marker.value() if p_marker is not None else None
        # Preserve keyframe scatter data
        t_kf_x, t_kf_y = t_kf.getData() if t_kf is not None else ([], [])
        h_kf_x, h_kf_y = h_kf.getData() if h_kf is not None else ([], [])
        p_kf_x, p_kf_y = p_kf.getData() if p_kf is not None else ([], [])
        plots.clear()
        # Reset refs (important when switching into single-plot mode)
        p_temp = p_hum = p_pres = None
        t_curve = h_curve = p_curve = None

        if horizontal:
            p_temp = plots.addPlot(title="Temperature (°C)")
            p_hum = plots.addPlot(title="Humidity (%)")
            p_pres = plots.addPlot(title="Pressure (hPa)")
            t_curve = p_temp.plot([], pen="r")
            h_curve = p_hum.plot([], pen="g")
            p_curve = p_pres.plot([], pen="b")
        else:
            if single_mode:
                if single_channel == "T":
                    p_temp = plots.addPlot(title="Temperature (°C)")
                    t_curve = p_temp.plot([], pen="r")
                elif single_channel == "H":
                    p_hum = plots.addPlot(title="Humidity (%)")
                    h_curve = p_hum.plot([], pen="g")
                else:
                    p_pres = plots.addPlot(title="Pressure (hPa)")
                    p_curve = p_pres.plot([], pen="b")
            else:
                p_temp = plots.addPlot(title="Temperature (°C)")
                t_curve = p_temp.plot([], pen="r")
                plots.nextRow()
                p_hum = plots.addPlot(title="Humidity (%)")
                h_curve = p_hum.plot([], pen="g")
                plots.nextRow()
                p_pres = plots.addPlot(title="Pressure (hPa)")
                p_curve = p_pres.plot([], pen="b")

        # Markers (only for existing plots)
        t_marker = h_marker = p_marker = None
        if p_temp is not None:
            t_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
            p_temp.addItem(t_marker)
        if p_hum is not None:
            h_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
            p_hum.addItem(h_marker)
        if p_pres is not None:
            p_marker = pg.InfiniteLine(angle=90, movable=False, pen=marker_pen)
            p_pres.addItem(p_marker)

        # "Future" shading (from playhead to end) to emulate progressive playback without re-plotting data
        fut_brush = pg.mkBrush(180, 180, 180, 55)
        fut_pen = pg.mkPen(None)
        t_future = h_future = p_future = None
        if p_temp is not None:
            t_future = pg.LinearRegionItem(values=(0, 0), movable=False, brush=fut_brush, pen=fut_pen)
            t_future.setZValue(-10)
            p_temp.addItem(t_future)
        if p_hum is not None:
            h_future = pg.LinearRegionItem(values=(0, 0), movable=False, brush=fut_brush, pen=fut_pen)
            h_future.setZValue(-10)
            p_hum.addItem(h_future)
        if p_pres is not None:
            p_future = pg.LinearRegionItem(values=(0, 0), movable=False, brush=fut_brush, pen=fut_pen)
            p_future.setZValue(-10)
            p_pres.addItem(p_future)

        # Keyframe scatters (only for existing plots)
        t_kf = h_kf = p_kf = None
        if p_temp is not None:
            t_kf = pg.ScatterPlotItem(size=6, pen=None, brush=pg.mkBrush(255, 200, 0, 180))
            p_temp.addItem(t_kf)
        if p_hum is not None:
            h_kf = pg.ScatterPlotItem(size=6, pen=None, brush=pg.mkBrush(255, 200, 0, 180))
            p_hum.addItem(h_kf)
        if p_pres is not None:
            p_kf = pg.ScatterPlotItem(size=6, pen=None, brush=pg.mkBrush(255, 200, 0, 180))
            p_pres.addItem(p_kf)
        # Restore data after rebuild
        if t_curve is not None and t_y_cur:
            t_curve.setData(t_x_cur, t_y_cur)
        if h_curve is not None and h_y_cur:
            h_curve.setData(h_x_cur, h_y_cur)
        if p_curve is not None and p_y_cur:
            p_curve.setData(p_x_cur, p_y_cur)
        # Restore keyframe scatter data
        if t_kf is not None and t_kf_x is not None and len(t_kf_x) > 0:
            t_kf.setData(t_kf_x, t_kf_y)
        if h_kf is not None and h_kf_x is not None and len(h_kf_x) > 0:
            h_kf.setData(h_kf_x, h_kf_y)
        if p_kf is not None and p_kf_x is not None and len(p_kf_x) > 0:
            p_kf.setData(p_kf_x, p_kf_y)

        # Restore marker positions
        if t_marker is not None and t_marker_pos is not None:
            t_marker.setPos(t_marker_pos)
        if h_marker is not None and h_marker_pos is not None:
            h_marker.setPos(h_marker_pos)
        if p_marker is not None and p_marker_pos is not None:
            p_marker.setPos(p_marker_pos)

        # If plots got rebuilt, existing mission markers need to be re-rendered.
        try:
            _render_event_markers()
        except Exception:
            pass

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

    def _clear_event_markers():
        nonlocal event_lines, event_labels, event_scatters
        # remove old markers from plots (per-plot items)
        for triple in event_lines:
            try:
                ln_t, ln_h, ln_p = triple
            except Exception:
                ln_t = ln_h = ln_p = None
            for plot, item in ((p_temp, ln_t), (p_hum, ln_h), (p_pres, ln_p)):
                try:
                    if plot is not None and item is not None:
                        plot.removeItem(item)
                except Exception:
                    pass

        for tx in event_labels:
            try:
                if p_temp is not None and tx is not None:
                    p_temp.removeItem(tx)
            except Exception:
                pass

        event_lines = []
        event_labels = []
        # remove scatter markers
        for triple in event_scatters:
            try:
                sc_t, sc_h, sc_p = triple
            except Exception:
                sc_t = sc_h = sc_p = None
            for plot, item in ((p_temp, sc_t), (p_hum, sc_h), (p_pres, sc_p)):
                try:
                    if plot is not None and item is not None:
                        plot.removeItem(item)
                except Exception:
                    pass
        event_scatters = []

    def _clear_state_bands():
        nonlocal state_regions
        for triple in state_regions:
            try:
                r_t, r_h, r_p = triple
            except Exception:
                r_t = r_h = r_p = None
            for plot, item in ((p_temp, r_t), (p_hum, r_h), (p_pres, r_p)):
                try:
                    if plot is not None and item is not None:
                        plot.removeItem(item)
                except Exception:
                    pass
        state_regions = []

    def _render_event_markers():
        nonlocal event_lines, event_labels, state_regions

        # Mission label colors (match Mission Timeline)
        label_style = {
            "GROUND":  (QtGui.QColor(220, 220, 220), QtGui.QColor(20, 20, 20)),
            "ASCENT":  (QtGui.QColor(60, 120, 200),  QtGui.QColor(255, 255, 255)),
            "APOGEE":  (QtGui.QColor(255, 200, 60),  QtGui.QColor(20, 20, 20)),
            "DESCENT": (QtGui.QColor(60, 200, 200),  QtGui.QColor(20, 20, 20)),
            "LANDED":  (QtGui.QColor(80, 200, 120),  QtGui.QColor(20, 20, 20)),
        }

        # Remove old stuff
        _clear_event_markers()
        _clear_state_bands()

        if p_temp is None or p_hum is None or p_pres is None:
            return

        # -----------------------
        # 1) Event markers (scatter only, all plots)
        # -----------------------
        if mission_events_ref:
            # Current data for y lookup
            _, t_ys = _curve_data(t_curve)
            _, h_ys = _curve_data(h_curve)
            _, p_ys = _curve_data(p_curve)

            for name, idx in mission_events_ref:
                try:
                    color = label_style.get(name, (QtGui.QColor(255, 255, 0), QtGui.QColor(0, 0, 0)))[0]
                    brush = pg.mkBrush(color)
                    pen = pg.mkPen(color, width=2)

                    def _make_scatter(plot, ys):
                        if plot is None or not ys or idx >= len(ys):
                            return None
                        sc = pg.ScatterPlotItem([float(idx)], [float(ys[idx])], size=10, brush=brush, pen=pen)
                        plot.addItem(sc)
                        return sc

                    sc_t = _make_scatter(p_temp, t_ys)
                    sc_h = _make_scatter(p_hum, h_ys)
                    sc_p = _make_scatter(p_pres, p_ys)
                    event_scatters.append((sc_t, sc_h, sc_p))
                except Exception:
                    pass

        # ------------------------------------------
        # 2) State bands (background colored ranges)
        # ------------------------------------------
        # Build segments from mission_events_ref. Expect: GROUND, ASCENT, APOGEE, DESCENT, LANDED
        if not mission_events_ref:
            return

        # Ensure sorted by sample index
        ev = sorted([(n, int(i)) for (n, i) in mission_events_ref], key=lambda x: x[1])

        # If first event is not GROUND, assume GROUND from 0
        if ev[0][0] != "GROUND":
            ev = [("GROUND", 0)] + ev

        # End index is last sample
        try:
            end_idx = max(0, table.rowCount() - 1)
        except Exception:
            end_idx = ev[-1][1]

        color_map = {
            "GROUND":  (220, 220, 220, 60),
            "ASCENT":  (60, 120, 200, 60),
            "APOGEE":  (255, 200, 60, 70),
            "DESCENT": (60, 200, 200, 60),
            "LANDED":  (80, 200, 120, 70),
        }

        for k in range(len(ev)):
            name, start = ev[k]
            stop = ev[k + 1][1] if k + 1 < len(ev) else end_idx
            if stop <= start:
                continue
            rgba = color_map.get(name, (180, 180, 180, 50))
            try:
                r_t = pg.LinearRegionItem(values=(float(start), float(stop)), movable=False,
                                          brush=pg.mkBrush(*rgba), pen=None)
                r_h = pg.LinearRegionItem(values=(float(start), float(stop)), movable=False,
                                          brush=pg.mkBrush(*rgba), pen=None)
                r_p = pg.LinearRegionItem(values=(float(start), float(stop)), movable=False,
                                          brush=pg.mkBrush(*rgba), pen=None)
                # Put behind curves
                for rr in (r_t, r_h, r_p):
                    try:
                        rr.setZValue(-50)
                    except Exception:
                        pass
                p_temp.addItem(r_t)
                p_hum.addItem(r_h)
                p_pres.addItem(r_p)
                state_regions.append((r_t, r_h, r_p))
            except Exception:
                pass
    def _generate_simulated_flight():
        nonlocal raw_buffer, raw_rx_buffer, have_new_bytes

        import random

        # ------------------------------------------------------------------
        # Simulated flight profile (realistic atmospheric model)
        # ------------------------------------------------------------------
        samples = []

        def add_sample(T, H, P):
            import random
            samples.append((
                T + random.uniform(-0.4, 0.4),
                H + random.uniform(-2.5, 2.5),
                P + random.uniform(-0.6, 0.6)
            ))

        # GROUND (stable)
        for _ in range(90):
            add_sample(25.0, 40.0, 1013.0)

        # EJECTION / KICK (oscillation + fast initial drop)
        for i in range(16):
            add_sample(
                25.0 + ((-1) ** i) * 5.0,
                40.0 + ((-1) ** i) * 12.0,
                1013.0 - i * 18.0
            )

        # ASCENT (pressure ↓, temp ↓, humidity ↑)
        for i in range(240):
            f = i / 240.0
            add_sample(
                25.0 - 50.0 * f,
                40.0 + 35.0 * f,
                1013.0 - 680.0 * f
            )

        # APOGEE (short plateau)
        for _ in range(55):
            add_sample(-25.0, 75.0, 330.0)

        # DESCENT (return)
        for i in range(240):
            f = i / 240.0
            add_sample(
                -25.0 + 50.0 * f,
                75.0 - 35.0 * f,
                330.0 + 680.0 * f
            )

        # LANDED (stable again)
        for _ in range(110):
            add_sample(25.0, 40.0, 1013.0)

        # ------------------------------------------------------------------
        # Encode into MIXED FULL + DELTA frames (realistic telemetry stream)
        # FULL every 5 frames, DELTA in between
        # ------------------------------------------------------------------

        raw_buffer.clear()
        raw_rx_buffer.clear()

        seq = 0
        last_v30 = None
        last_key_seq = None

        for i in range(0, len(samples), 8):
            make_full = (seq % 5 == 0) or (last_v30 is None)

            if make_full:
                frame = bytearray(FULL_FRAME_LEN)
                frame[0] = SYNC_FULL

                met = i // 8
                frame[1] = met & 0xFF
                frame[2] = (met >> 8) & 0xFF
                frame[4] = seq & 0xFF
                frame[5] = 0  # validity/meta

                bitpos = 6 * 8
                for j in range(8):
                    if i + j < len(samples):
                        T, H, P = samples[i + j]

                        T_code = max(0, min(2047, int((T + 40.0) * 10)))
                        H_code = max(0, min(127, int(H)))
                        P_code = int((P - 822.0) * 10)
                        P_code = max(0, min(2550, P_code))

                        v30 = (
                            (T_code & 0x7FF)
                            | ((H_code & 0x7F) << 11)
                            | (((P_code // 10) & 0xFF) << 18)
                            | ((P_code % 10) << 26)
                        )
                    else:
                        v30 = 0

                    last_v30 = v30
                    last_key_seq = seq & 0xFF

                    for b in range(30):
                        if v30 & (1 << b):
                            bi = (bitpos + b) >> 3
                            bj = (bitpos + b) & 7
                            frame[bi] |= (1 << bj)
                    bitpos += 30

                crc = crc16_ccitt(frame[:36])
                frame[36] = crc & 0xFF
                frame[37] = (crc >> 8) & 0xFF

                raw_buffer.extend(frame)
                raw_rx_buffer.extend(frame)
                seq += 1
                continue

            # ---------------- DELTA FRAME ----------------
            frame = bytearray(DELTA_FRAME_LEN)
            frame[0] = SYNC_DELTA

            met = i // 8
            frame[1] = met & 0xFF
            frame[2] = (met >> 8) & 0xFF
            frame[4] = seq & 0xFF
            frame[5] = last_key_seq

            bitpos = 6 * 8
            prev = last_v30

            for j in range(8):
                if i + j < len(samples):
                    T, H, P = samples[i + j]

                    T_code = max(0, min(2047, int((T + 40.0) * 10)))
                    H_code = max(0, min(127, int(H)))
                    P_code = int((P - 822.0) * 10)
                    P_code = max(0, min(2550, P_code))

                    v30 = (
                        (T_code & 0x7FF)
                        | ((H_code & 0x7F) << 11)
                        | (((P_code // 10) & 0xFF) << 18)
                        | ((P_code % 10) << 26)
                    )
                else:
                    v30 = prev

                # compute deltas
                dT = ((v30 & 0x7FF) - (prev & 0x7FF))
                dRH = (((v30 >> 11) & 0x7F) - ((prev >> 11) & 0x7F))
                P_prev = ((prev >> 18) & 0xFF) * 10 + ((prev >> 26) & 0x0F)
                P_now = ((v30 >> 18) & 0xFF) * 10 + ((v30 >> 26) & 0x0F)
                dP = P_now - P_prev

                # clamp deltas to bit widths
                dT = max(-16, min(15, dT))
                dRH = max(-8, min(7, dRH))
                dP = max(-32, min(31, dP))

                def _pack(val, bits):
                    if val < 0:
                        val = (1 << bits) + val
                    return val & ((1 << bits) - 1)

                dT_p = _pack(dT, 5)
                dRH_p = _pack(dRH, 4)
                dP_p = _pack(dP, 6)

                # write bits
                for b in range(5):
                    if dT_p & (1 << b):
                        bi = (bitpos + b) >> 3
                        bj = (bitpos + b) & 7
                        frame[bi] |= (1 << bj)
                bitpos += 5

                for b in range(4):
                    if dRH_p & (1 << b):
                        bi = (bitpos + b) >> 3
                        bj = (bitpos + b) & 7
                        frame[bi] |= (1 << bj)
                bitpos += 4

                for b in range(6):
                    if dP_p & (1 << b):
                        bi = (bitpos + b) >> 3
                        bj = (bitpos + b) & 7
                        frame[bi] |= (1 << bj)
                bitpos += 6

                prev = v30
                last_v30 = v30

            crc = crc16_ccitt(frame[:21])
            frame[21] = crc & 0xFF
            frame[22] = (crc >> 8) & 0xFF

            raw_buffer.extend(frame)
            raw_rx_buffer.extend(frame)
            seq += 1

        have_new_bytes = True

    # Connect toggle and initialize layout
    def _on_plot_toggle(checked):
        nonlocal single_mode
        # checked == True  -> Horizontal
        # checked == False -> Vertical
        plot_toggle.setText("H" if checked else "V")
        # Single-plot mode is only meaningful in Vertical layout.
        if checked and btn_single.isChecked():
            btn_single.setChecked(False)
            single_mode = False
        rebuild_plots(checked)
        update_from_raw()
        _update_view_buttons()

    def _update_view_buttons():
        vertical = not plot_toggle.isChecked()
        enable = vertical and btn_single.isChecked()
        for b in (btn_view_t, btn_view_h, btn_view_p):
            b.setEnabled(enable)

    def _on_single_toggle(checked):
        nonlocal single_mode
        single_mode = bool(checked)
        if checked and plot_toggle.isChecked():
            # Force vertical layout
            plot_toggle.setChecked(False)
            return
        rebuild_plots(plot_toggle.isChecked())
        update_from_raw()
        _update_view_buttons()

    def _on_view_select(which: str):
        nonlocal single_channel
        single_channel = which
        # If user presses T/H/P in vertical mode, go to single view automatically.
        if not plot_toggle.isChecked() and (not btn_single.isChecked()):
            btn_single.setChecked(True)
            return
        if (not plot_toggle.isChecked()) and btn_single.isChecked():
            rebuild_plots(False)
            update_from_raw()
        _update_view_buttons()

    plot_toggle.toggled.connect(_on_plot_toggle)
    btn_single.toggled.connect(_on_single_toggle)
    btn_view_t.clicked.connect(lambda: _on_view_select("T"))
    btn_view_h.clicked.connect(lambda: _on_view_select("H"))
    btn_view_p.clicked.connect(lambda: _on_view_select("P"))

    rebuild_plots(True)  # Startup: Horizontal layout
    _update_view_buttons()

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
        # Keep plots the focus in ONLINE mode: hide OFFLINE-only sidebar elements.
        file_list.setVisible(offline)
        gb_files.setVisible(offline)
        gb_sim.setVisible(offline)
        file_list.setEnabled(offline)
        btn_sim.setEnabled(offline)
        _update_file_actions()
        _update_file_info()
        gb_files.setEnabled(offline)
        gb_sim.setEnabled(offline)
        port_cb.setEnabled(not offline)
        btn_refresh_ports.setEnabled(not offline)
        btn_connect.setEnabled(not offline)
        btn_disconnect.setEnabled(not offline)
        btn_log.setEnabled(not offline and ser is not None)
        btn_sidebar.setChecked(offline)
        _set_sidebar_visible(btn_sidebar.isChecked())
        # Visual state: show connection status on the buttons themselves.
        if ser is None:
            btn_disconnect.setChecked(True)
        else:
            btn_connect.setChecked(True)
        tabs.setCurrentIndex(0)

    def append_raw_debug(text: str):
        # keep raw view lightweight: append and trim to last ~2000 lines
        # Dedup spammy lines (e.g. periodic status lines), keep last message stable.
        if not hasattr(append_raw_debug, "_last"):
            append_raw_debug._last = None
            append_raw_debug._last_t = 0.0
            append_raw_debug._last_n = 0

        now = time.monotonic()
        if text == append_raw_debug._last and (now - append_raw_debug._last_t) < 2.0:
            append_raw_debug._last_n += 1
            return

        append_raw_debug._last = text
        append_raw_debug._last_t = now
        append_raw_debug._last_n = 0

        raw_human_view.append(text)
        doc = raw_human_view.document()
        if doc.blockCount() > 2000:
            cursor = QtGui.QTextCursor(doc)
            cursor.movePosition(QTEXTCURSOR_START)
            cursor.select(QTEXTCURSOR_BLOCKUNDERCURSOR)
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
                if i + META_FRAME_LEN <= n and buf[i] == SYNC_META1 and buf[i + 1] == SYNC_META2:
                    m = buf[i:i + META_FRAME_LEN]
                    meta = parse_rf_meta_frame(m)
                    if meta:
                        lines.append(f"[META ] @0x{i:04X}  SCORE={meta['link_score']}  RSSI={meta['rssi_pkt_dbm']}  SNR={meta['snr_db']:.1f}")
                    else:
                        lines.append(f"[META ] @0x{i:04X}  (invalid)")
                    lines.append(render_hex_dump(m))
                    i += META_FRAME_LEN
                continue
            if b == SYNC_DELTA and i + DELTA_FRAME_LEN <= n:
                frame = buf[i:i + DELTA_FRAME_LEN]
                seq = frame[4]
                ref = frame[5]
                lines.append(f"[DELTA] @0x{i:04X}  SEQ={seq}  REF={ref}")
                lines.append(render_hex_dump(frame))
                i += DELTA_FRAME_LEN
                if i + META_FRAME_LEN <= n and buf[i] == SYNC_META1 and buf[i + 1] == SYNC_META2:
                    m = buf[i:i + META_FRAME_LEN]
                    meta = parse_rf_meta_frame(m)
                    if meta:
                        lines.append(f"[META ] @0x{i:04X}  SCORE={meta['link_score']}  RSSI={meta['rssi_pkt_dbm']}  SNR={meta['snr_db']:.1f}")
                    else:
                        lines.append(f"[META ] @0x{i:04X}  (invalid)")
                    lines.append(render_hex_dump(m))
                    i += META_FRAME_LEN
                continue
            if b == SYNC_META1 and i + META_FRAME_LEN <= n and buf[i + 1] == SYNC_META2:
                m = buf[i:i + META_FRAME_LEN]
                meta = parse_rf_meta_frame(m)
                if meta:
                    lines.append(f"[META ] @0x{i:04X}  SCORE={meta['link_score']}  RSSI={meta['rssi_pkt_dbm']}  SNR={meta['snr_db']:.1f}")
                else:
                    lines.append(f"[META ] @0x{i:04X}  (invalid)")
                lines.append(render_hex_dump(m))
                i += META_FRAME_LEN
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
                if i + META_FRAME_LEN <= n and buf[i] == SYNC_META1 and buf[i + 1] == SYNC_META2:
                    m = buf[i:i + META_FRAME_LEN]
                    meta = parse_rf_meta_frame(m)
                    tag = "[META ]"
                    if meta:
                        tag = f"[META ] SCORE={meta['link_score']:3d} RSSI={meta['rssi_pkt_dbm']:4d} SNR={meta['snr_db']:4.1f}"
                    lines.append(html_line(
                        f"{tag} @0x{i:04X} | {render_hex_one_line(m)}",
                        COLOR_META
                    ))
                    i += META_FRAME_LEN
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
                if i + META_FRAME_LEN <= n and buf[i] == SYNC_META1 and buf[i + 1] == SYNC_META2:
                    m = buf[i:i + META_FRAME_LEN]
                    meta = parse_rf_meta_frame(m)
                    tag = "[META ]"
                    if meta:
                        tag = f"[META ] SCORE={meta['link_score']:3d} RSSI={meta['rssi_pkt_dbm']:4d} SNR={meta['snr_db']:4.1f}"
                    lines.append(html_line(
                        f"{tag} @0x{i:04X} | {render_hex_one_line(m)}",
                        COLOR_META
                    ))
                    i += META_FRAME_LEN
                continue
            if b == SYNC_META1 and i + META_FRAME_LEN <= n and buf[i + 1] == SYNC_META2:
                m = buf[i:i + META_FRAME_LEN]
                meta = parse_rf_meta_frame(m)
                tag = "[META ]"
                if meta:
                    tag = f"[META ] SCORE={meta['link_score']:3d} RSSI={meta['rssi_pkt_dbm']:4d} SNR={meta['snr_db']:4.1f}"
                lines.append(html_line(
                    f"{tag} @0x{i:04X} | {render_hex_one_line(m)}",
                    COLOR_META
                ))
                i += META_FRAME_LEN
                continue

            # Collect consecutive NOISE bytes into one row (up to 32 bytes)
            start = i
            chunk = [b]
            i += 1
            while i < n and buf[i] not in (SYNC_FULL, SYNC_DELTA, SYNC_META1) and len(chunk) < 32:
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
                out.append(f"SAMPLES   : 8 (fixed per FULL frame)")
                out.append(f"VALIDITY  : 0x{frame[5]:02X}")
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
            # ---------------- META FRAME ----------------
            if b == SYNC_META1 and i < n and buf[i] == SYNC_META2 and (start + META_FRAME_LEN) <= n:
                frame = buf[start:start + META_FRAME_LEN]
                meta = parse_rf_meta_frame(frame)
                out.append("────────────────────────────────────────")
                out.append("META FRAME  (RF)")
                out.append("────────────────────────────────────────")
                if meta:
                    out.append(f"LEN       : {meta['payload_len']} B")
                    out.append(f"FLAGS     : PHY={'OK' if meta['phy_ok'] else 'BAD'} APP={'OK' if meta['app_ok'] else 'BAD'} FULL={int(meta['is_full'])} DELTA={int(meta['is_delta'])}")
                    out.append(f"RSSI pkt  : {meta['rssi_pkt_dbm']} dBm  inst: {meta['rssi_inst_dbm']} dBm")
                    out.append(f"SNR       : {meta['snr_db']:.2f} dB   FEI: {meta['fei_hz']} Hz")
                    out.append(f"OFFSET    : {meta['offset_hz']} Hz   SCORE: {meta['link_score']}/100")
                    out.append(f"BWbits={meta['bw_bits']} SF={meta['sf']} CR={meta['cr']}  RxNb={meta['rx_nb_bytes']}")
                    out.append(f"ModemStat : 0x{meta['modem_stat']:02X}  IRQ: 0x{meta['irq_flags']:02X}")
                    out.append(f"RxHdrCnt  : {meta['rx_header_cnt']}  RxPktCnt: {meta['rx_packet_cnt']}")
                    out.append(f"SEQ/MET   : {meta['seq']} / {meta['met']}")
                else:
                    out.append("INVALID META (CRC/len/version)")
                out.append("HEX:")
                out.append(render_hex_one_line(frame))
                i = start + META_FRAME_LEN
                continue

            while i < n and buf[i] not in (SYNC_FULL, SYNC_DELTA, SYNC_META1) and len(chunk) < 32:
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
    # Stream mode for ONLINE serial ingest.
    # IMPORTANT: once we have seen any SYNC byte, we MUST treat all subsequent bytes as binary
    # (frames can span serial.read() chunk boundaries). Never drop bytes in this mode.
    stream_mode = "unknown"  # "unknown" | "binary" | "asciihex"

    def _contains_sync(data: bytes) -> bool:
        if not data:
            return False
        return (SYNC_FULL in data) or (SYNC_DELTA in data) or (SYNC_META1 in data)

    def _likely_ascii_hex(data: bytes) -> bool:
        """
        Detect a *real* ASCII HEX dump (e.g. 'A5 01 02 ...'), not arbitrary boot text.
        We keep this strict to avoid corrupting binary logs by accidentally converting
        normal ASCII strings (e.g. 'ets Jun 8 2016...') into random bytes.
        """
        if not data:
            return False
        if _contains_sync(data):
            return False

        # If most bytes are printable/whitespace, it may be text
        printable = sum((32 <= b <= 126) or b in (9, 10, 13) for b in data)
        if (printable / max(1, len(data))) <= 0.90:
            return False

        try:
            txt = data.decode("ascii", errors="ignore")
        except Exception:
            return False

        # Count tokens that look exactly like hex bytes
        toks = txt.replace(",", " ").replace(":", " ").split()
        hex_toks = [t for t in toks if len(t) == 2 and all(c in "0123456789abcdefABCDEF" for c in t)]

        # Require a decent chunk to avoid triggering on incidental numbers in boot logs.
        return len(hex_toks) >= 16

    def _extract_hex_bytes_from_text(txt: str):
        """
        Returns (bin_bytes, leftover_txt)
        Extract contiguous hex pairs from txt, convert them to bytes.
        Keeps any trailing incomplete hex pair text as leftover.
        """
        # Only accept whitespace-separated tokens that are EXACTLY 2 hex chars.
        # This prevents converting normal boot text into random bytes.
        toks = txt.replace(",", " ").replace(":", " ").split()
        hex_toks = [t for t in toks if len(t) == 2 and all(c in "0123456789abcdefABCDEF" for c in t)]
        if len(hex_toks) < 16:
            # Not a real hex dump: treat as noise/text and keep buffer bounded.
            return b"", txt[-4096:]

        try:
            out = bytes(int(t, 16) for t in hex_toks)
        except Exception:
            out = b""

        # Keep a small tail for incomplete next chunk
        return out, txt[-256:]

    def normalize_to_binary_stream(raw: bytes) -> bytes:
        """
        If raw looks like ASCII hex dump, convert it to the real binary stream.
        Otherwise return raw unchanged.
        """
        # If any sync byte exists anywhere, treat it as a binary stream that may contain ASCII noise.
        # We never want to globally "hex-decode" a mixed stream (it would destroy framing/CRC).
        if _contains_sync(raw):
            return raw
        if _likely_ascii_hex(raw):
            try:
                txt = raw.decode("ascii", errors="ignore")
            except Exception:
                return raw
            out, _ = _extract_hex_bytes_from_text(txt)
            return out if out else raw
        return raw

    def _update_markers_and_future(idx: int, n_samples: int):
        """Fast UI path for playhead movement (no decode, no table rebuild)."""
        if n_samples <= 0:
            return
        idx = max(0, min(int(idx), int(n_samples) - 1))
        try:
            if t_marker is not None:
                t_marker.setPos(idx)
            if h_marker is not None:
                h_marker.setPos(idx)
            if p_marker is not None:
                p_marker.setPos(idx)
        except Exception:
            pass

        # Future shading: (idx .. last sample)
        try:
            lo = float(idx)
            hi = float(max(0, n_samples - 1))
            if t_future is not None:
                t_future.setRegion((lo, hi))
            if h_future is not None:
                h_future.setRegion((lo, hi))
            if p_future is not None:
                p_future.setRegion((lo, hi))
        except Exception:
            pass

        # RF trend cursor
        try:
            rftr_rssi_marker.setPos(idx)
            rftr_snr_marker.setPos(idx)
            rftr_fei_marker.setPos(idx)
            rftr_score_marker.setPos(idx)
        except Exception:
            pass

    def _latest_meta_for_end(frames_diag, end_exclusive: int):
        if end_exclusive is None:
            end_exclusive = 0
        end_exclusive = int(end_exclusive)
        if end_exclusive < 0:
            end_exclusive = 0

        # ONLINE startup assist: show the first META as soon as it exists.
        if mode_cb.currentText() == "ONLINE" and ser is not None:
            try:
                first_meta_sidx = min(
                    int(d["meta"].get("_sample_idx"))
                    for d in frames_diag
                    if d.get("type") == "META" and d.get("status") == "ACCEPTED" and d.get("meta")
                    and d["meta"].get("_sample_idx") is not None
                )
                end_exclusive = max(end_exclusive, first_meta_sidx + 1)
            except Exception:
                pass

        for d in reversed(frames_diag):
            if d.get("type") != "META" or d.get("status") != "ACCEPTED" or not d.get("meta"):
                continue
            meta = d["meta"]
            sidx = meta.get("_sample_idx")
            if sidx is None:
                continue
            try:
                sidx = int(sidx)
            except Exception:
                continue
            if sidx < end_exclusive:
                return meta
        return None

    def update_view_only():
        """Update cursor markers + RF panel based on current playhead, without decoding."""
        if decode_cache._result is None:
            return
        Ts, _, _, _, frames_diag = decode_cache._result
        n = len(Ts)
        if n <= 0:
            return

        try:
            idx = int(seek_slider.value()) if seek_slider.isSliderDown() else int(_playhead_sample_idx())
        except Exception:
            idx = 0
        idx = max(0, min(idx, n - 1))

        # Avoid doing heavy widget updates at timer rate if playhead didn't move.
        last = getattr(update_view_only, "_last_state", None)
        cur = (idx, n, bool(seek_slider.isSliderDown()))
        if last == cur:
            return
        update_view_only._last_state = cur

        _update_markers_and_future(idx, n)

        # RF metrics: pick META closest to playhead
        latest_meta = _latest_meta_for_end(frames_diag, idx + 1)
        if not latest_meta:
            rf_lbl.setText("RF META: — (no meta frames yet)")
            return

        _set_led(rf_led_phy, bool(latest_meta.get("phy_ok")), "#00cc66")
        _set_led(rf_led_app, bool(latest_meta.get("app_ok")), "#00ccff")
        _set_led(rf_led_full, bool(latest_meta.get("is_full")), "#2ecc71")
        _set_led(rf_led_delta, bool(latest_meta.get("is_delta")), "#3498db")

        rf_lbl.setText(f"RF META v{latest_meta.get('ver')}  (FW vs PC)")

        fw_score = int(latest_meta.get("link_score", 0))
        rf_score_fw.setValue(float(fw_score))

        pc_raw = link_score_pc(latest_meta)
        if not hasattr(update_from_raw, "_pc_score_ema"):
            update_from_raw._pc_score_ema = float(pc_raw)
        ema = update_from_raw._pc_score_ema
        alpha = 0.25
        ema = (1.0 - alpha) * ema + alpha * float(pc_raw)
        update_from_raw._pc_score_ema = ema
        rf_score_pc.setValue(float(ema))

        rf_rssi_pkt.setValue(float(latest_meta.get("rssi_pkt_dbm", -150)))
        rf_rssi_inst.setValue(float(latest_meta.get("rssi_inst_dbm", -150)))
        rf_snr.setValue(float(latest_meta.get("snr_db", 0.0)))
        rf_fei.setValue(float(latest_meta.get("fei_hz", 0)))
        rf_ofs.setValue(float(latest_meta.get("offset_hz", 0)))

        sf = int(latest_meta.get("sf", 12))
        bw_khz = lora_bw_khz_from_bits(int(latest_meta.get("bw_bits", 7)))
        sens = lora_sensitivity_dbm(sf, bw_khz)
        req_snr = lora_required_snr_db(sf)

        rf_rssi_pkt.setThresholds(green=sens + 20.0, yellow=sens + 10.0)
        nf = lora_noise_floor_dbm(bw_khz, noise_figure_db=6.0)
        rf_rssi_inst.setThresholds(green=nf + 3.0, yellow=nf + 10.0)
        rf_snr.setThresholds(green=req_snr + 6.0, yellow=req_snr + 2.0)
        rf_fei.setAbsThresholds(green=500.0, yellow=2000.0)
        rf_ofs.setAbsThresholds(green=5000.0, yellow=20000.0)

        rf_lbl_len.setText(str(latest_meta.get("payload_len")))
        rf_lbl_modem.setText(f"0x{latest_meta.get('modem_stat', 0):02X}")
        rf_lbl_irq.setText(f"0x{latest_meta.get('irq_flags', 0):02X}")
        rf_lbl_bw.setText(f"BWbits={latest_meta.get('bw_bits')}  SF={latest_meta.get('sf')}  CR={latest_meta.get('cr')}")
        rf_lbl_cnt.setText(f"Hdr={latest_meta.get('rx_header_cnt')}  Pkt={latest_meta.get('rx_packet_cnt')}")
        rf_lbl_seqmet.setText(f"SEQ={latest_meta.get('seq')}  MET={latest_meta.get('met')}")

    def update_from_raw():
        # Decode whatever we have; this is used by BOTH offline load and online stream
        nonlocal have_new_bytes, online_started, play_state, play_idx, play_wall0, play_base_idx, play_speed, live_mode
        if not raw_buffer:
            return
        # Decode whatever we have (strict CRC by default).
        Ts, Hs, Ps, keyframes, frames_diag = decode_cache.decode(bytes(raw_buffer), allow_crc_fail=False)
        # --- playback window ---
        nonlocal play_idx
        end = play_idx if play_idx is not None else len(Ts)
        # Store latest keyframes for Timeline/Table sync
        keyframes_ref.clear()
        keyframes_ref.extend(keyframes)
        # -----------------------------------------------------------------
        # Mission Timeline – derived events + keyframes (TimelineEngine)
        # -----------------------------------------------------------------
        timeline_events_ref.clear()

        tl = timeline_engine.derive(Ts, Hs, Ps, keyframes)

        # Update mission events for plot markers
        mission_events_ref.clear()
        mission_events_ref.extend(tl.get("mission_events", []) or [])

        # Fill timeline list widget
        for text, sample_idx, style in tl.get("timeline_items", []) or []:
            it = QtWidgets.QListWidgetItem(text)
            if sample_idx is None:
                it.setFlags(Qt.NoItemFlags)
            else:
                it.setData(Qt.UserRole, int(sample_idx))

            if style is not None and sample_idx is not None:
                bg, fg = style
                it.setBackground(bg)
                it.setForeground(fg)

            # Special tint for adaptive keyframes
            if text.startswith("ADAPTIVE KF") and sample_idx is not None:
                it.setForeground(QtGui.QColor(255, 180, 0))

            timeline_events_ref.addItem(it)

        # Update plot markers for mission events
        _render_event_markers()

        # Fill decoded-samples table (incremental append for performance).
        try:
            prev_n = int(getattr(update_from_raw, "_table_len", table.rowCount()))
        except Exception:
            prev_n = table.rowCount()

        cur_n = len(Ts)
        if cur_n < prev_n:
            table.setRowCount(0)
            prev_n = 0
        if table.rowCount() != cur_n:
            table.setRowCount(cur_n)

        keyset = set(keyframes)
        for i in range(prev_n, cur_n):
            table.setItem(i, 0, QTableWidgetItem(str(i)))
            table.setItem(i, 1, QTableWidgetItem(f"{Ts[i]:.2f}"))
            table.setItem(i, 2, QTableWidgetItem(f"{Hs[i]:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{Ps[i]:.2f}"))
            if i in keyset:
                for c in range(4):
                    it = table.item(i, c)
                    if it is not None:
                        it.setBackground(QtGui.QColor(50, 50, 0, 140))

        update_from_raw._table_len = cur_n

        # ONLINE: auto-follow latest sample
        if mode_cb.currentText() == "ONLINE" and ser is not None and table.rowCount() > 0:
            try:
                last = table.rowCount() - 1
                # don't steal focus if user is time-shifting (scrubbing or not in live mode)
                if (not seek_slider.isSliderDown()) and (live_mode or online_started):
                    table.scrollToItem(table.item(last, 0), QABSTRACTITEMVIEW_POSITIONATBOTTOM)
            except Exception:
                pass

        # Update plots (full-series). Playback "reveal" is done via marker + future shading.
        xs_full = getattr(update_from_raw, "_xs_full", None)
        if xs_full is None or len(xs_full) != len(Ts):
            xs_full = list(range(len(Ts)))
            update_from_raw._xs_full = xs_full
        try:
            if t_curve is not None:
                t_curve.setData(xs_full, Ts)
            if h_curve is not None:
                h_curve.setData(xs_full, Hs)
            if p_curve is not None:
                p_curve.setData(xs_full, Ps)
        except Exception:
            pass

        # Re-apply autorange so overlays (labels/regions) don't drift the view
        _auto_range_plots()

        # Keyframes (full-series)
        try:
            if t_kf is not None:
                t_kf.setData(keyframes, [Ts[i] for i in keyframes])
            if h_kf is not None:
                h_kf.setData(keyframes, [Hs[i] for i in keyframes])
            if p_kf is not None:
                p_kf.setData(keyframes, [Ps[i] for i in keyframes])
        except Exception:
            pass

        lbl_status.setText(
            f"Status: decoded_samples={len(Ts)}  keyframes={len(keyframes)}  bin_bytes={len(raw_buffer)}"
        )

        # Raw stream info: only when Raw tab is visible (avoid spamming the human view)
        if tabs.currentIndex() == 1:
            append_raw_debug(f"[INFO] bin_bytes={len(raw_buffer)}  decoded_samples={len(Ts)}  keyframes={len(keyframes)}")

        # Populate frame inspector tables.
        # IMPORTANT: update_from_raw() is called frequently (online decode tick + playhead seeks).
        # Rebuilding large QTableWidgets on every call can freeze the UI.
        #
        # We rebuild the inspector tables only when frames_diag actually changed
        # (i.e., new bytes arrived / decode output changed), not when only the playhead moved.
        main_rows = [d for d in frames_diag if d.get("type") in ("FULL", "DELTA")]
        meta_rows = [d for d in frames_diag if d.get("type") == "META"]

        def _sig(rows):
            tail = rows[-6:] if len(rows) > 6 else rows
            return (len(rows), tuple((r.get("type"), r.get("seq"), r.get("status"), r.get("crc_ok")) for r in tail))

        inspector_sig = (_sig(main_rows), _sig(meta_rows))
        if not hasattr(update_from_raw, "_inspector_sig"):
            update_from_raw._inspector_sig = None

        if update_from_raw._inspector_sig != inspector_sig:
            update_from_raw._inspector_sig = inspector_sig

            # Avoid recursive selection-change handlers while rebuilding tables.
            nonlocal ui_sync_busy
            ui_sync_busy = True
            try:
                try:
                    frame_table.blockSignals(True)
                    meta_table.blockSignals(True)
                except Exception:
                    pass

                frame_table.setRowCount(len(main_rows))
                for idx, diag in enumerate(main_rows):
                    # Columns: ["#", "Type", "SEQ", "REF", "CRC", "Status", "Reason"]
                    it0 = QTableWidgetItem(str(idx + 1))
                    it0.setData(Qt.UserRole, diag)
                    frame_table.setItem(idx, 0, it0)
                    frame_table.setItem(idx, 1, QTableWidgetItem(str(diag.get("type", ""))))
                    frame_table.setItem(idx, 2, QTableWidgetItem(str(diag.get("seq", ""))))
                    ref_val = str(diag.get("ref_seq", "")) if diag.get("type") == "DELTA" else ""
                    frame_table.setItem(idx, 3, QTableWidgetItem(ref_val))
                    crc_val = "OK" if diag.get("crc_ok", False) else "FAIL"
                    frame_table.setItem(idx, 4, QTableWidgetItem(crc_val))
                    frame_table.setItem(idx, 5, QTableWidgetItem(str(diag.get("status", ""))))
                    frame_table.setItem(idx, 6, QTableWidgetItem(str(diag.get("reason", ""))))
                    if diag.get("status") != "ACCEPTED":
                        for c in range(7):
                            item = frame_table.item(idx, c)
                            if item is not None:
                                item.setBackground(QtGui.QColor(255, 128, 128, 120))

                meta_table.setRowCount(len(meta_rows))
                for idx, diag in enumerate(meta_rows):
                    meta = diag.get("meta") if isinstance(diag, dict) else None
                    sidx = meta.get("_sample_idx") if isinstance(meta, dict) else None
                    it0 = QTableWidgetItem(str(idx + 1))
                    it0.setData(Qt.UserRole, diag)
                    meta_table.setItem(idx, 0, it0)
                    meta_table.setItem(idx, 1, QTableWidgetItem(str(diag.get("seq", ""))))
                    meta_table.setItem(idx, 2, QTableWidgetItem("" if sidx is None else str(sidx)))
                    meta_table.setItem(idx, 3, QTableWidgetItem(str(meta.get("payload_len", "")) if isinstance(meta, dict) else ""))
                    meta_table.setItem(idx, 4, QTableWidgetItem("OK" if (isinstance(meta, dict) and meta.get("phy_ok")) else "BAD"))
                    meta_table.setItem(idx, 5, QTableWidgetItem("OK" if (isinstance(meta, dict) and meta.get("app_ok")) else "BAD"))
                    meta_table.setItem(idx, 6, QTableWidgetItem(str(meta.get("rssi_pkt_dbm", "")) if isinstance(meta, dict) else ""))
                    meta_table.setItem(idx, 7, QTableWidgetItem(str(meta.get("rssi_inst_dbm", "")) if isinstance(meta, dict) else ""))
                    if isinstance(meta, dict) and meta.get("snr_db") is not None:
                        try:
                            meta_table.setItem(idx, 8, QTableWidgetItem(f"{float(meta.get('snr_db')):.2f}"))
                        except Exception:
                            meta_table.setItem(idx, 8, QTableWidgetItem(str(meta.get("snr_db"))))
                    else:
                        meta_table.setItem(idx, 8, QTableWidgetItem(""))
                    meta_table.setItem(idx, 9, QTableWidgetItem(str(meta.get("fei_hz", "")) if isinstance(meta, dict) else ""))

                # Column sizing is fixed/compact; avoid expensive resizeColumnsToContents()
            finally:
                try:
                    frame_table.blockSignals(False)
                    meta_table.blockSignals(False)
                except Exception:
                    pass
                ui_sync_busy = False

        # RF Metrics tab update (latest META)
        latest_meta = None
        # Pick META that belongs to the current playback window (playhead-follow).
        # Note: in ONLINE mode the playhead can lag behind the newest packet by a few samples,
        # so we allow a small startup assist: once the first META exists, include it even if
        # the playhead hasn't reached it yet. This prevents an empty RF panel while frames arrive.
        target_end = int(end) if end is not None else len(Ts)
        if target_end < 0:
            target_end = 0

        if mode_cb.currentText() == "ONLINE" and ser is not None:
            try:
                first_meta_sidx = min(
                    int(d["meta"].get("_sample_idx"))
                    for d in frames_diag
                    if d.get("type") == "META" and d.get("status") == "ACCEPTED" and d.get("meta")
                    and d["meta"].get("_sample_idx") is not None
                )
                target_end = max(target_end, first_meta_sidx + 1)
            except Exception:
                pass
        for d in reversed(frames_diag):
            if d.get("type") != "META" or d.get("status") != "ACCEPTED" or not d.get("meta"):
                continue
            meta = d["meta"]
            sidx = meta.get("_sample_idx")
            if sidx is None:
                continue
            try:
                sidx = int(sidx)
            except Exception:
                continue
            if sidx < target_end:
                latest_meta = meta
                break

        if latest_meta:
            _set_led(rf_led_phy, bool(latest_meta.get("phy_ok")), "#00cc66")
            _set_led(rf_led_app, bool(latest_meta.get("app_ok")), "#00ccff")
            _set_led(rf_led_full, bool(latest_meta.get("is_full")), "#2ecc71")
            _set_led(rf_led_delta, bool(latest_meta.get("is_delta")), "#3498db")

            rf_lbl.setText(
                f"RF META v{latest_meta.get('ver')}  (FW vs PC)"
            )

            fw_score = int(latest_meta.get("link_score", 0))
            rf_score_fw.setValue(float(fw_score))

            # PC score: compute + smooth with EMA to be more human-readable
            pc_raw = link_score_pc(latest_meta)
            if not hasattr(update_from_raw, "_pc_score_ema"):
                update_from_raw._pc_score_ema = float(pc_raw)
            ema = update_from_raw._pc_score_ema
            alpha = 0.25  # 0..1, higher = faster response
            ema = (1.0 - alpha) * ema + alpha * float(pc_raw)
            update_from_raw._pc_score_ema = ema
            rf_score_pc.setValue(float(ema))

            rf_rssi_pkt.setValue(float(latest_meta.get("rssi_pkt_dbm", -150)))
            rf_rssi_inst.setValue(float(latest_meta.get("rssi_inst_dbm", -150)))
            rf_snr.setValue(float(latest_meta.get("snr_db", 0.0)))
            rf_fei.setValue(float(latest_meta.get("fei_hz", 0)))
            rf_ofs.setValue(float(latest_meta.get("offset_hz", 0)))

            # ESA-style coloring thresholds (LoRa-mode aware)
            sf = int(latest_meta.get("sf", 12))
            bw_khz = lora_bw_khz_from_bits(int(latest_meta.get("bw_bits", 7)))
            sens = lora_sensitivity_dbm(sf, bw_khz)
            req_snr = lora_required_snr_db(sf)

            # RSSI pkt: green if strong margin above sensitivity, yellow moderate, red near sensitivity
            rf_rssi_pkt.setThresholds(green=sens + 20.0, yellow=sens + 10.0)

            # Noise floor (inst RSSI): lower is better (more negative)
            # Treat as "channel energy / noise": green near noise floor, yellow moderately above, red if very high.
            nf = lora_noise_floor_dbm(bw_khz, noise_figure_db=6.0)
            rf_rssi_inst.setThresholds(green=nf + 3.0, yellow=nf + 10.0)

            # SNR: compare to SF-required SNR (+ margin)
            rf_snr.setThresholds(green=req_snr + 6.0, yellow=req_snr + 2.0)

            # FEI: AFC threshold is 500 Hz; use it as green band, yellow up to 2 kHz
            rf_fei.setAbsThresholds(green=500.0, yellow=2000.0)

            # OFFSET: engineering “ok” bands
            rf_ofs.setAbsThresholds(green=5000.0, yellow=20000.0)

            rf_lbl_len.setText(str(latest_meta.get("payload_len")))
            rf_lbl_modem.setText(f"0x{latest_meta.get('modem_stat', 0):02X}")
            rf_lbl_irq.setText(f"0x{latest_meta.get('irq_flags', 0):02X}")
            rf_lbl_bw.setText(f"BWbits={latest_meta.get('bw_bits')}  SF={latest_meta.get('sf')}  CR={latest_meta.get('cr')}")
            rf_lbl_cnt.setText(f"Hdr={latest_meta.get('rx_header_cnt')}  Pkt={latest_meta.get('rx_packet_cnt')}")
            rf_lbl_seqmet.setText(f"SEQ={latest_meta.get('seq')}  MET={latest_meta.get('met')}")
        else:
            rf_lbl.setText("RF META: — (no meta frames yet)")

        # -----------------------------------------------------------------
        # RF Trends (META time-series up to playback window)
        # -----------------------------------------------------------------
        rf_x = []
        rf_rssi_pkt_y = []
        rf_rssi_inst_y = []
        rf_snr_y = []
        rf_fei_y = []
        rf_ofs_y = []
        rf_score_fw_y = []
        rf_score_pc_y = []

        # Same window rule as above: follow the playhead (with the same ONLINE startup assist).
        trend_end = end if end is not None else len(Ts)
        if trend_end < 0:
            trend_end = 0
        if mode_cb.currentText() == "ONLINE" and ser is not None:
            try:
                first_meta_sidx = min(
                    int(d["meta"].get("_sample_idx"))
                    for d in frames_diag
                    if d.get("type") == "META" and d.get("status") == "ACCEPTED" and d.get("meta")
                    and d["meta"].get("_sample_idx") is not None
                )
                trend_end = max(int(trend_end), first_meta_sidx + 1)
            except Exception:
                pass

        for d in frames_diag:
            if d.get("type") != "META" or d.get("status") != "ACCEPTED" or not d.get("meta"):
                continue
            m = d["meta"]
            sidx = m.get("_sample_idx")
            if sidx is None:
                continue
            try:
                sidx = int(sidx)
            except Exception:
                continue
            if sidx < 0 or sidx >= trend_end:
                continue

            rf_x.append(float(sidx))
            rf_rssi_pkt_y.append(float(m.get("rssi_pkt_dbm", -150)))
            rf_rssi_inst_y.append(float(m.get("rssi_inst_dbm", -150)))
            rf_snr_y.append(float(m.get("snr_db", 0.0)))
            rf_fei_y.append(float(m.get("fei_hz", 0)))
            rf_ofs_y.append(float(m.get("offset_hz", 0)))
            rf_score_fw_y.append(float(m.get("link_score", 0)))
            try:
                rf_score_pc_y.append(float(link_score_pc(m)))
            except Exception:
                rf_score_pc_y.append(0.0)

        try:
            rftr_rssi_pkt_curve.setData(rf_x, rf_rssi_pkt_y)
            rftr_rssi_inst_curve.setData(rf_x, rf_rssi_inst_y)
            rftr_snr_curve.setData(rf_x, rf_snr_y)
            rftr_fei_curve.setData(rf_x, rf_fei_y)
            rftr_ofs_curve.setData(rf_x, rf_ofs_y)
            rftr_score_fw_curve.setData(rf_x, rf_score_fw_y)
            rftr_score_pc_curve.setData(rf_x, rf_score_pc_y)
        except Exception:
            pass

        # Keep markers/future shading and RF panel synced even if playhead didn't move.
        try:
            update_view_only()
        except Exception:
            pass

        have_new_bytes = False
        update_time_displays()

        # ONLINE auto-play: start as soon as first samples arrive, at 1x (0.5s/sample) paced by wall clock.
        if mode_cb.currentText() == "ONLINE" and ser is not None and (not online_started) and len(Ts) > 0:
            online_started = True
            live_mode = True
            play_speed = 1.0
            play_state = PLAY_RUNNING
            btn_play.setChecked(True)
            play_base_idx = 0
            play_wall0 = time.monotonic()
            play_idx = 1  # start from first sample
            playback_timer.start()

    # Timers: serial poll + decode throttle
    serial_timer = QtCore.QTimer()
    serial_timer.setInterval(20)

    decode_timer = QtCore.QTimer()
    decode_timer.setInterval(200)  # 5 Hz update; stable

    def serial_poll():
        nonlocal have_new_bytes, total_bytes, raw_rx_buffer, raw_buffer, ascii_hex_buf, stream_mode
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

        # Decide stream mode:
        # - If we see SYNC anywhere, lock to binary and never drop bytes.
        # - Only if we have not seen SYNC yet, allow legacy ASCII-HEX decode.
        if stream_mode != "binary" and _contains_sync(chunk):
            stream_mode = "binary"
        elif stream_mode == "unknown" and _likely_ascii_hex(chunk):
            stream_mode = "asciihex"

        if stream_mode == "asciihex":
            ascii_hex_buf += chunk.decode("ascii", errors="ignore")
            bin_chunk, ascii_hex_buf = _extract_hex_bytes_from_text(ascii_hex_buf)
        else:
            # "binary" or "unknown": keep bytes as-is (unknown just means boot/noise before first SYNC).
            bin_chunk = chunk

        # Append to binary decode buffer
        if bin_chunk:
            raw_buffer.extend(bin_chunk)
            have_new_bytes = True

            # Logging: save the ORIGINAL serial stream bytes (exactly what arrived).
            if log_fp is not None:
                try:
                    log_fp.write(chunk)
                    log_fp.flush()
                except Exception as e:
                    append_raw_debug(f"[ERR] log write failed: {e}")

        total_bytes += len(chunk)
        lbl_bytes.setText(f"Bytes: {total_bytes}")
        lbl_status.setText(f"Status: online rx (raw_bytes={total_bytes}  bin_bytes={len(raw_buffer)})")

        # RX LED flash
        _set_led(led_rx, True, "#00ccff")
        QtCore.QTimer.singleShot(80, lambda: _set_led(led_rx, False, "#00ccff"))

    # Raw view render throttle
    last_raw_render_sig = None

    def decode_tick():
        nonlocal last_raw_render_sig

        if have_new_bytes:
            update_from_raw()

        # RAW tab index = 1 (HEX / HUMAN)
        if tabs.currentIndex() == 1:
            sig = (
                len(raw_buffer),
                bytes(raw_buffer[-64:]) if len(raw_buffer) > 64 else bytes(raw_buffer)
            )

            if sig != last_raw_render_sig:
                last_raw_render_sig = sig

                TAIL = 8192  # bytes
                tail_buf = bytes(raw_buffer[-TAIL:]) if len(raw_buffer) > TAIL else bytes(raw_buffer)

                # Human-readable view
                raw_human_view.clear()
                raw_human_view.append(
                    f"[RAW FRAME VIEW — tail {len(tail_buf)} bytes / total {len(raw_buffer)} bytes]"
                )
                raw_human_view.append(render_human_frames(tail_buf))

                # Hex view
                raw_hex_view.clear()
                raw_hex_view.append(render_hex_frames_colored(tail_buf))

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
        # Render only tail in the Raw tab for responsiveness (files can be large, META increases size).
        TAIL = 16384
        tail_buf = bytes(raw_buffer[-TAIL:]) if len(raw_buffer) > TAIL else bytes(raw_buffer)
        raw_human_view.append(f"[RAW FRAME VIEW — tail {len(tail_buf)} bytes / total {len(raw_buffer)} bytes]")
        raw_human_view.append(render_human_frames(tail_buf))
        raw_hex_view.append(render_hex_frames_colored(tail_buf))
        lbl_status.setText("Status: offline file loaded")
        update_from_raw()

        # On new file load: jump to the first sample (but keep full data visible).
        try:
            if table.rowCount() > 0:
                table.selectRow(0)
        except Exception:
            pass
        update_time_displays()

    def on_table_select():
        nonlocal ui_sync_busy
        row = table.currentRow()
        if row < 0:
            return
        if ui_sync_busy:
            # Selection was triggered programmatically by _seek_to / inspector jump.
            return
        if t_marker is not None:
            t_marker.setPos(row)
        if h_marker is not None:
            h_marker.setPos(row)
        if p_marker is not None:
            p_marker.setPos(row)
        # RF Trends markers
        try:
            rftr_rssi_marker.setPos(row)
            rftr_snr_marker.setPos(row)
            rftr_fei_marker.setPos(row)
            rftr_score_marker.setPos(row)
        except Exception:
            pass
        # Click-to-seek behavior (single source of truth)
        _seek_to(row)

    def on_frame_select(row_override=None):
        if row_override is not None:
            row = row_override
        else:
            row = frame_table.currentRow()
        if row < 0:
            return

        diag = None
        try:
            diag = frame_table.item(row, 0).data(Qt.UserRole)
        except Exception:
            diag = None

        ftype = (frame_table.item(row, 1).text() if frame_table.item(row, 1) is not None else "")
        seq = (frame_table.item(row, 2).text() if frame_table.item(row, 2) is not None else "")
        ref = (frame_table.item(row, 3).text() if frame_table.item(row, 3) is not None else "")
        status = (frame_table.item(row, 5).text() if frame_table.item(row, 5) is not None else "")

        # Compact, width-optimized single/dual line explain text (avoid tall panels).
        if ftype == "FULL":
            txt = f"FULL | SEQ={seq} | MET={frame_table.item(row, 3).text() if frame_table.item(row, 3) else ''}".strip()
        elif ftype == "DELTA":
            txt = f"DELTA | SEQ={seq} | REF={ref}".strip()
        elif ftype == "META":
            meta = (diag or {}).get("meta") if isinstance(diag, dict) else None
            if isinstance(meta, dict):
                sidx = meta.get("_sample_idx")
                txt = (
                    f"META | SEQ={seq} | sample={sidx if sidx is not None else '—'} | len={meta.get('payload_len')}B"
                    f" | PHY={'OK' if meta.get('phy_ok') else 'BAD'} APP={'OK' if meta.get('app_ok') else 'BAD'}"
                    f" | FULL={int(bool(meta.get('is_full')))} DELTA={int(bool(meta.get('is_delta')))}"
                    f"\nPktStr={meta.get('rssi_pkt_dbm')}dBm Noise={meta.get('rssi_inst_dbm')}dBm"
                    f" SNR={float(meta.get('snr_db', 0.0)):.2f}dB FEI={meta.get('fei_hz')}Hz OFS={meta.get('offset_hz')}Hz"
                    f" BWbits={meta.get('bw_bits')} SF={meta.get('sf')} CR={meta.get('cr')} RxNb={meta.get('rx_nb_bytes')}"
                    f" Modem=0x{meta.get('modem_stat',0):02X} IRQ=0x{meta.get('irq_flags',0):02X}"
                    f" Hdr={meta.get('rx_header_cnt')} Pkt={meta.get('rx_packet_cnt')} LQ(FW)={meta.get('link_score')}/100"
                )
            else:
                txt = f"META | SEQ={seq}"
        else:
            txt = f"{ftype} | SEQ={seq}"

        reason_item = frame_table.item(row, 6)
        reason = reason_item.text() if reason_item is not None else ""
        txt += f"\n\nStatus: {status}"
        if reason:
            txt += f"\nReason: {reason}"
        frame_explain_left.setText(txt)

    def on_frame_click(row_override=None):
        """User-initiated click: update explain + jump to decoded sample range."""
        nonlocal ui_sync_busy
        if ui_sync_busy:
            return
        if row_override is not None:
            row = row_override
        else:
            row = frame_table.currentRow()
        if row < 0:
            return
        # Update the explain panel first
        on_frame_select(row)
        # Then jump
        try:
            diag = frame_table.item(row, 0).data(Qt.UserRole)
            if isinstance(diag, dict) and diag.get("sample_start") is not None:
                sidx = int(diag.get("sample_start"))
                if 0 <= sidx < table.rowCount():
                    _seek_to(sidx)
        except Exception:
            pass

    def on_meta_select(row_override=None):
        if row_override is not None:
            row = row_override
        else:
            row = meta_table.currentRow()
        if row < 0:
            return
        diag = None
        try:
            diag = meta_table.item(row, 0).data(Qt.UserRole)
        except Exception:
            diag = None
        meta = (diag or {}).get("meta") if isinstance(diag, dict) else None
        seq = meta_table.item(row, 1).text() if meta_table.item(row, 1) is not None else ""
        status = (diag or {}).get("status", "") if isinstance(diag, dict) else ""
        reason = (diag or {}).get("reason", "") if isinstance(diag, dict) else ""
        sidx = None
        if isinstance(meta, dict):
            sidx = meta.get("_sample_idx")

        if isinstance(meta, dict):
            txt = (
                f"META | SEQ={seq} | sample={sidx if sidx is not None else '—'} | len={meta.get('payload_len')}B"
                f" | PHY={'OK' if meta.get('phy_ok') else 'BAD'} APP={'OK' if meta.get('app_ok') else 'BAD'}"
                f" | FULL={int(bool(meta.get('is_full')))} DELTA={int(bool(meta.get('is_delta')))}"
                f"\nPktStr={meta.get('rssi_pkt_dbm')}dBm Noise={meta.get('rssi_inst_dbm')}dBm"
                f" SNR={float(meta.get('snr_db', 0.0)):.2f}dB FEI={meta.get('fei_hz')}Hz OFS={meta.get('offset_hz')}Hz"
                f" BWbits={meta.get('bw_bits')} SF={meta.get('sf')} CR={meta.get('cr')} RxNb={meta.get('rx_nb_bytes')}"
                f" Modem=0x{meta.get('modem_stat',0):02X} IRQ=0x{meta.get('irq_flags',0):02X}"
                f" Hdr={meta.get('rx_header_cnt')} Pkt={meta.get('rx_packet_cnt')} LQ(FW)={meta.get('link_score')}/100"
            )
        else:
            txt = f"META | SEQ={seq}"

        txt += f"\nStatus: {status}"
        if reason:
            txt += f" | Reason: {reason}"
        meta_explain_right.setText(txt)

    def on_meta_click(row_override=None):
        """User-initiated click: update explain + jump to attached sample index."""
        nonlocal ui_sync_busy
        if ui_sync_busy:
            return
        if row_override is not None:
            row = row_override
        else:
            row = meta_table.currentRow()
        if row < 0:
            return
        on_meta_select(row)
        try:
            diag = meta_table.item(row, 0).data(Qt.UserRole)
            meta = (diag or {}).get("meta") if isinstance(diag, dict) else None
            sidx = meta.get("_sample_idx") if isinstance(meta, dict) else None
            if sidx is not None and table.rowCount() > 0:
                sidx = int(sidx)
                if 0 <= sidx < table.rowCount():
                    _seek_to(sidx)
        except Exception:
            pass

    def connect_serial():
        nonlocal ser, raw_rx_buffer, raw_buffer, total_bytes, have_new_bytes
        nonlocal ascii_hex_buf
        nonlocal online_started, live_mode, play_state, play_idx, play_wall0, play_base_idx, play_speed
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
        online_started = False
        live_mode = False
        play_state = PLAY_STOPPED
        play_idx = None
        play_wall0 = None
        play_base_idx = 0
        play_speed = 1.0

        raw_human_view.clear()
        raw_hex_view.clear()
        append_raw_debug(f"[INFO] ONLINE connected: {dev}")

        _set_led(led_conn, True, "#00cc00")
        btn_connect.setChecked(True)
        btn_disconnect.setChecked(False)
        btn_log.setEnabled(True)

        serial_timer.start()
        decode_timer.start()

        # Auto-start LOG in ONLINE mode
        _start_auto_log()

        set_mode_ui()

    def disconnect_serial():
        nonlocal ser, log_fp, log_path
        nonlocal online_started, live_mode, play_state, play_idx, play_wall0, play_base_idx
        if ser is None:
            return

        serial_timer.stop()
        decode_timer.stop()

        try:
            ser.close()
        except Exception:
            pass
        ser = None
        online_started = False
        live_mode = False
        play_state = PLAY_STOPPED
        play_idx = None
        play_wall0 = None
        play_base_idx = 0

        _set_led(led_conn, False, "#00cc00")
        btn_disconnect.setChecked(True)
        btn_connect.setChecked(False)
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
    table.itemSelectionChanged.connect(lambda: table.viewport().update())
    frame_table.itemSelectionChanged.connect(lambda: frame_table.viewport().update())
    file_list.currentItemChanged.connect(lambda *_: file_list.viewport().update())
    timeline_events_ref.itemSelectionChanged.connect(lambda: timeline_events_ref.viewport().update())
    def on_timeline_select():
        item = timeline_events_ref.currentItem()
        if item is None:
            return
        sample_idx = item.data(Qt.UserRole)
        if sample_idx is None:
            return
        try:
            sample_idx = int(sample_idx)
        except Exception:
            return
        if 0 <= sample_idx < table.rowCount():
            table.selectRow(sample_idx)

    timeline_events_ref.itemSelectionChanged.connect(on_timeline_select)
    frame_table.itemClicked.connect(lambda item: on_frame_click(item.row()))
    frame_table.cellClicked.connect(lambda r, c: on_frame_click(r))
    frame_table.itemSelectionChanged.connect(lambda: on_frame_select(frame_table.currentRow()))
    meta_table.itemClicked.connect(lambda item: on_meta_click(item.row()))
    meta_table.cellClicked.connect(lambda r, c: on_meta_click(r))
    meta_table.itemSelectionChanged.connect(lambda: on_meta_select(meta_table.currentRow()))

    btn_refresh_ports.clicked.connect(refresh_ports)
    btn_connect.clicked.connect(connect_serial)
    btn_disconnect.clicked.connect(disconnect_serial)
    btn_log.toggled.connect(toggle_log)
    mode_cb.currentIndexChanged.connect(on_mode_changed)
    theme_cb.currentIndexChanged.connect(lambda _=None: apply_theme(theme_cb.currentText() == "Dark"))

    apply_theme(True)
    refresh_ports()
    refresh_file_list()
    set_mode_ui()
    lbl_status.setText("Status: ready")

    time_timer.start()
    update_time_displays()

    serial_timer.stop()
    decode_timer.stop()

    def _apply_default_layout():
        try:
            w = max(1200, win.width())
            h = max(800, win.height())

            # Sidebar vs main
            main_hsplit.setStretchFactor(0, 0)
            main_hsplit.setStretchFactor(1, 1)
            if file_box.isVisible():
                main_hsplit.setSizes([min(460, int(w * 0.30)), w])
            else:
                main_hsplit.setSizes([0, 1])

            # Plots vs tabs
            right_vsplit.setStretchFactor(0, 5)
            right_vsplit.setStretchFactor(1, 2)
            right_vsplit.setSizes([int(h * 0.62), int(h * 0.38)])

            try:
                raw_splitter.setSizes([w // 2, w - (w // 2)])
            except Exception:
                pass
            try:
                frame_split.setSizes([int(w * 0.62), int(w * 0.38)])
            except Exception:
                pass
            try:
                frames_col.setSizes([int(h * 0.78), int(h * 0.22)])
            except Exception:
                pass
            try:
                meta_col.setSizes([int(h * 0.78), int(h * 0.22)])
            except Exception:
                pass
        except Exception:
            pass

    def _toggle_fullscreen():
        if win.isFullScreen():
            win.showNormal()
            win.showMaximized()
        else:
            win.showFullScreen()

    try:
        act_fs = QtGui.QAction("Toggle Fullscreen", win)
        act_fs.setShortcut(QtGui.QKeySequence("F11"))
        act_fs.triggered.connect(_toggle_fullscreen)
        win.addAction(act_fs)
    except Exception:
        pass

    try:
        btn_fullscreen.clicked.connect(_toggle_fullscreen)
    except Exception:
        pass

    try:
        btn_sidebar.toggled.connect(_set_sidebar_visible)
    except Exception:
        pass

    win.show()
    QtCore.QTimer.singleShot(0, _apply_default_layout)
    if hasattr(app, "exec"):
        app.exec()
    else:
        app.exec_()

if __name__ == "__main__":
    main()
