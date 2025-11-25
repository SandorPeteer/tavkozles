#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import serial
import serial.tools.list_ports
import struct
import datetime

import threading
import queue
import csv
import os

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

BAUD = 115200        # szükség esetén módosítható
RETRY_DELAY = 2.0    # másodperc – újrapróbálkozás között


# Globális változók az utolsó TEL-ből rekonstruált értékekhez
last_tel_T = None
last_tel_RH = None
last_tel_P = None

# GUI-hoz használt globális struktúrák
sample_queue = queue.Queue()
csv_file = None
csv_writer = None


def find_serial_port():
    """
    Automatikus portkeresés ESP / MCU eszközökhöz (CH340, CP210x, FTDI, stb.).
    Visszatér: port neve (pl. 'COM3', '/dev/ttyUSB0', '/dev/cu.usbserial-110') vagy None.
    """
    patterns = [
        "ch340",
        "cp210",
        "ftdi",
        "usb-serial",
        "usb serial",
        "wchusb",
        "silicon labs",
        "usb uart",
        "usb2.0-serial",
        "ttyusb",
        "ttyacm",
        "usbserial",
        "slab_usb"
    ]

    ports = list(serial.tools.list_ports.comports())

    # Első kör: ismert USB–soros átalakítók
    for p in ports:
        text = f"{p.device} {p.description} {p.hwid}".lower()
        if any(pat in text for pat in patterns):
            print(f"[OK] ESP/MCU eszköz detektálva: {p.device}  ({p.description})")
            return p.device

    # Második kör: ha csak egy nem-Bluetooth soros eszköz van, azt választjuk
    candidates = []
    for p in ports:
        desc = (p.description or "").lower()
        if "bluetooth" in desc:
            continue
        candidates.append(p.device)

    if len(candidates) == 1:
        print(f"[OK] Egyetlen soros eszköz elérhető, ezt használom: {candidates[0]}")
        return candidates[0]

    # Nincs egyértelmű jelölt
    if not ports:
        print("[ERR] Egyetlen soros eszköz sem látható a rendszerben.")
    else:
        print("[ERR] Több lehetséges soros eszköz van, és egyiket sem tudtam egyértelműen azonosítani:")
        for p in ports:
            print(f"      - {p.device}: {p.description}")

    return None


def open_serial_with_retry(baud=BAUD, retry_delay=RETRY_DELAY):
    """
    Addig próbálkozik, amíg sikerül egy automatikusan detektált portra csatlakozni.
    """
    while True:
        port = find_serial_port()
        if port is None:
            print(f"[INFO] Várakozás... csatlakoztasd / reseteld az ESP-t, újrapróbálkozás {retry_delay} s múlva.")
            time.sleep(retry_delay)
            continue

        try:
            print(f"[INFO] Soros port megnyitása: {port} @ {baud} baud")
            ser = serial.Serial(port, baudrate=baud, timeout=0)
            print("[OK] Soros kapcsolat létrejött.")
            return ser
        except serial.SerialException as e:
            print(f"[ERR] Nem sikerült megnyitni a portot: {e}")
            print(f"[INFO] Újrapróbálkozás {retry_delay} s múlva...")
            time.sleep(retry_delay)


def serial_worker():
    ser = open_serial_with_retry(baud=BAUD, retry_delay=RETRY_DELAY)

    try:
        buffer = bytearray()

        while True:
            try:
                data = ser.read_all()

                if not data:
                    time.sleep(0.001)   # CPU kímélés, de nem blokkol
                    continue

                buffer.extend(data)

                # TEL csomagok hossz-alapú kinyerése (csak 0xA5, nincs SYNC-to-SYNC heuristika)
                while True:
                    # Legalább a SYNC byte kell
                    if len(buffer) < 1:
                        break

                    # Igazítsuk a buffert a következő 0xA5 TEL SYNC-re
                    if buffer[0] != 0xA5:
                        try:
                            next_sync = buffer.index(0xA5)
                            del buffer[:next_sync]
                        except ValueError:
                            # Nincs több SYNC a bufferben
                            buffer.clear()
                            break

                    # Most buffer[0] == 0xA5, de kell a teljes fejléc: SYNC + MET_low + MET_high + N + MASK
                    if len(buffer) < 5:
                        # Várunk még bájtokat
                        break

                    sync     = buffer[0]
                    base_MET = buffer[1] | (buffer[2] << 8)
                    N        = buffer[3]
                    bitmask  = buffer[4]

                    # Érvénytelen N esetén dobjuk ezt a SYNC-et és keresünk újat
                    if N == 0 or N > 8:
                        del buffer[0]
                        continue

                    # Maszkon belüli használt bitek (0..N-1)
                    used_mask = bitmask & ((1 << N) - 1)

                    # Pack-ek száma = a használt bitek száma
                    m = used_mask
                    num_packs = 0
                    while m:
                        num_packs += (m & 1)
                        m >>= 1

                    # TEL csomag teljes hossza: 1 (SYNC) + 2 (MET) + 1 (N) + 1 (MASK) + 4 * num_packs
                    expected_len = 1 + 2 + 1 + 1 + num_packs * 4

                    # Ha még nincs meg az összes bájt, várunk
                    if len(buffer) < expected_len:
                        break

                    # Kivágjuk a teljes TEL packetet
                    packet = buffer[:expected_len]
                    del buffer[:expected_len]

                    data = packet[1:]  # SYNC utáni rész

                    # TELE – teljes, bitre pontos visszafejtés 0,5 s-es mintákra
                    if sync == 0xA5:
                        # base_MET, N, bitmask már kiolvasva a bufferből
                        # A pack-ek a data[4]-től indulnak
                        pack_idx = 4

                        global last_tel_T, last_tel_RH, last_tel_P

                        for i in range(N):
                            MET_i = base_MET + i
                            mask_bit_set = (bitmask & (1 << i)) != 0

                            if mask_bit_set:
                                # Kell legyen legalább 4 bájt a packhez
                                if pack_idx + 4 > len(data):
                                    # Hibás / csonka csomag – nyers HEX kiírása és megszakítjuk a feldolgozást
                                    print(f"[TEL] RAW {data.hex().upper()}")
                                    break

                                pack_bytes = data[pack_idx:pack_idx + 4]
                                pack_idx  += 4

                                # 4 bájtból 30 bit: 11 (T) + 7 (RH) + 8 (P_int) + 4 (P_frac)
                                acc = int.from_bytes(pack_bytes, byteorder='little', signed=False)

                                T_code      =  acc        & ((1 << 11) - 1)          # 0..2047
                                RH_code     = (acc >> 11) & ((1 << 7)  - 1)          # 0..127
                                P_int_code  = (acc >> 18) & 0xFF                     # 0..255
                                P_frac_code = (acc >> 26) & 0x0F                     # 0..15

                                # Invertáljuk az encode_dynamic_pack logikáját
                                T  = (T_code / 10.0) - 40.0
                                RH = float(RH_code)
                                P  = 822.0 + float(P_int_code) + (P_frac_code / 10.0)

                                last_tel_T  = T
                                last_tel_RH = RH
                                last_tel_P  = P

                            else:
                                # Nem változott: a legutóbbi TEL-ből ismert értéket használjuk.
                                if last_tel_T is None:
                                    continue

                            # Minden 0,5 s-es mintát külön sorba írunk ki
                            print(f"{datetime.datetime.now().strftime('[%H:%M:%S]')}"
                                  f" [TEL] MET={MET_i}  T={last_tel_T:.2f}C  RH={last_tel_RH:.1f}%  P={last_tel_P:.1f}hPa")

                            # A dekódolt mintát betesszük a GUI sorába is
                            try:
                                sample_queue.put_nowait((MET_i, float(last_tel_T), float(last_tel_RH), float(last_tel_P)))
                            except Exception:
                                # Ha valamiért nem sikerül, a terminálos kiírás akkor is megmarad
                                pass

            except UnicodeDecodeError as e:
                print(f"[WARN] Dekódolási hiba: {e}")
            except serial.SerialException as e:
                print(f"[ERR] Soros hiba: {e}")
                print("[INFO] Újracsatlakozás indul...")
                ser.close()
                ser = open_serial_with_retry(baud=BAUD, retry_delay=RETRY_DELAY)

    except KeyboardInterrupt:
        print("\n[INFO] Megszakítva (Ctrl+C).")
    finally:
        try:
            ser.close()
        except Exception:
            pass
        print("[INFO] Soros port lezárva.")


def start_gui():
    """
    Egyszerű Tkinter alapú GUI:
    - felső rész: görgethető táblázat az aktuális adatokkal
    - alsó rész: 3 külön grafikon (T, RH, P)
    - minden minta CSV-be is mentésre kerül
    """
    global csv_file, csv_writer

    root = tk.Tk()
    # --- Repülési idő számláló ---
    flight_start_MET = tk.IntVar(value=-1)
    flight_elapsed_label = tk.Label(root, text="Eltelt idő: 0 s", font=("Arial", 12))
    flight_elapsed_label.pack(pady=5)

    def start_flight_timer():
        flight_start_MET.set(-2)  # jelzés, hogy várjuk az első mintát
        flight_elapsed_label.config(text="Eltelt idő: 0 s")
        xs.clear()
        Ts.clear()
        RHs.clear()
        Ps.clear()

    start_button = tk.Button(root, text="Start (MET=0)", command=start_flight_timer)
    start_button.pack(pady=5)

    def stop_flight_timer():
        flight_start_MET.set(-1)  # stop mode
        flight_elapsed_label.config(text="Eltelt idő: STOP")

    stop_button = tk.Button(root, text="Stop", command=stop_flight_timer)
    stop_button.pack(pady=5)

    root.title("CanSat telemetria dekóder")

    # ------- Táblázat keret + görgetősáv -------
    table_frame = ttk.Frame(root)
    table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    columns = ("time", "met", "t", "rh", "p")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    tree.heading("time", text="Idő")
    tree.heading("met", text="MET")
    tree.heading("t",   text="T [°C]")
    tree.heading("rh",  text="RH [%]")
    tree.heading("p",   text="P [hPa]")

    tree.column("time", anchor=tk.CENTER, width=90, stretch=False)
    tree.column("met",  anchor=tk.CENTER, width=80, stretch=False)
    tree.column("t",    anchor=tk.CENTER, width=80, stretch=False)
    tree.column("rh",   anchor=tk.CENTER, width=80, stretch=False)
    tree.column("p",    anchor=tk.CENTER, width=100, stretch=False)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # ------- Matplotlib ábra: 3 külön tengely T / RH / P -------
    fig = Figure(figsize=(8, 5), dpi=100)
    axT = fig.add_subplot(311)
    axRH = fig.add_subplot(312)
    axP = fig.add_subplot(313)

    axT.set_ylabel("T [°C]")
    axRH.set_ylabel("RH [%]")
    axP.set_ylabel("P [hPa]")
    axP.set_xlabel("MET")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Idősor tárolók (csak az utolsó N pontot tartjuk meg)
    xs = []
    Ts = []
    RHs = []
    Ps = []
    max_len = 300

    # ------- CSV fájl megnyitása -------
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"telemetry_{timestamp_str}.csv"
    try:
        csv_file = open(filename, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["time", "MET", "T_C", "RH_pct", "P_hPa"])
        csv_file.flush()
        print(f"[INFO] CSV log fájl: {filename}")
    except Exception as e:
        print(f"[WARN] Nem sikerült megnyitni a CSV fájlt: {e}")
        csv_file = None
        csv_writer = None

    def process_queue():
        """Soronként beolvassa a dekóder által küldött mintákat és frissíti a GUI elemeket."""
        updated = False

        while True:
            try:
                MET_i, T, RH, P = sample_queue.get_nowait()
            except queue.Empty:
                break

            # Repülési idő frissítése
            if flight_start_MET.get() == -2:
                flight_start_MET.set(MET_i)
            start_met = flight_start_MET.get()
            if start_met >= 0:
                elapsed = MET_i - start_met
                if elapsed < 0:
                    elapsed = 0
                flight_elapsed_label.config(text=f"Eltelt idő: {elapsed} s")

            now_str = datetime.datetime.now().strftime("%H:%M:%S")

            # Táblázat bővítése + automatikus görgetés a végére
            tree.insert("", "end", values=(now_str, MET_i, f"{T:.2f}", f"{RH:.1f}", f"{P:.1f}"))
            tree.yview_moveto(1.0)

            # Idősorok frissítése
            xs.append(MET_i)
            Ts.append(T)
            RHs.append(RH)
            Ps.append(P)

            if len(xs) > max_len:
                xs[:] = xs[-max_len:]
                Ts[:] = Ts[-max_len:]
                RHs[:] = RHs[-max_len:]
                Ps[:] = Ps[-max_len:]

            # CSV log
            if csv_writer is not None:
                try:
                    csv_writer.writerow([now_str, MET_i, f"{T:.2f}", f"{RH:.1f}", f"{P:.1f}"])
                    csv_file.flush()
                except Exception as e:
                    print(f"[WARN] CSV írási hiba: {e}")

            updated = True

        # --- Smoothing helper ---
        def smooth(data, window=5):
            if len(data) < window:
                return data
            out = []
            for i in range(len(data)):
                start = max(0, i - window + 1)
                out.append(sum(data[start:i+1]) / (i - start + 1))
            return out

        # Ha frissült adat, rajzoljuk újra a grafikonokat
        if updated and xs:
            axT.clear()
            axRH.clear()
            axP.clear()

            # --- X tengely: eltelt idő másodpercben ---
            start_met = flight_start_MET.get()
            if start_met >= 0:
                xs_plot = [x - start_met for x in xs]
            else:
                xs_plot = xs[:]  # Start előtt és Stop után is az abszolút MET időt használjuk

            axT.plot(xs_plot, smooth(Ts, 3))
            axRH.plot(xs_plot, smooth(RHs, 3))
            axP.plot(xs_plot, smooth(Ps, 7))

            axT.set_ylabel("T [°C]")
            axRH.set_ylabel("RH [%]")
            axP.set_ylabel("P [hPa]")
            axP.set_xlabel("Eltelt idő [s]")

            # --- X tengely határok ---
            if start_met >= 0:
                # sliding 120-second window
                x_min = max(0, xs_plot[-1] - 120)
                x_max = xs_plot[-1]
                axT.set_xlim([x_min, x_max])
                axRH.set_xlim([x_min, x_max])
                axP.set_xlim([x_min, x_max])
            else:
                if xs_plot:
                    xmin = xs_plot[0]
                    xmax = xs_plot[-1]
                    axT.set_xlim([xmin, xmax])
                    axRH.set_xlim([xmin, xmax])
                    axP.set_xlim([xmin, xmax])

            fig.tight_layout()
            canvas.draw()

        # 200 ms múlva újra ellenőrzünk
        root.after(200, process_queue)

    def on_close():
        """Ablak bezárása esetén CSV lezárása is."""
        try:
            if csv_file is not None:
                csv_file.close()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Indítjuk a periodikus queue-feldolgozást
    root.after(200, process_queue)

    # Fő eseményciklus
    root.mainloop()


if __name__ == "__main__":
    # Ellenőrzés: telepítve van-e a pyserial
    try:
        # már importáltuk fent, ez csak emlékeztető hiba esetére
        pass
    except ImportError:
        print("Hiányzik a pyserial csomag. Telepítés:\n\n    pip install pyserial\n")
        sys.exit(1)

    # Soros olvasó szál indítása (a terminálos dekódolás továbbra is él)
    t = threading.Thread(target=serial_worker, daemon=True)
    t.start()

    # Grafikus felület indítása (blokkoló hívás)
    start_gui()