# --- Byte counter globals for packet stats ---
bytes_last = 0
bytes_total = 0

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

# --- Serial port selector override ---
SELECTED_PORT_OVERRIDE = None

# --- Global handle for the serial object ---
serial_handle = None

 # --- Serial thread started flag ---
serial_thread_started = False

# --- Serial connection active flag ---
serial_connection_active = False

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

    # Filter out WLAN/network devices
    ports = [p for p in ports if "wlan" not in p.description.lower()
                             and "wifi" not in p.description.lower()
                             and "network" not in p.description.lower()]

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
    global SELECTED_PORT_OVERRIDE
    global serial_handle
    if SELECTED_PORT_OVERRIDE:
        try:
            print(f"[INFO] Kiválasztott port megnyitása: {SELECTED_PORT_OVERRIDE}")
            ser = serial.Serial(SELECTED_PORT_OVERRIDE, baudrate=baud, timeout=0)
            serial_handle = ser
            print("[OK] Soros kapcsolat létrejött a kijelölt portról.")
            return ser
        except Exception as e:
            print(f"[ERR] A kijelölt port nem nyitható meg: {e}")
            # fallback to auto-search
    while True:
        port = find_serial_port()
        if port is None:
            print(f"[INFO] Várakozás... csatlakoztasd / reseteld az ESP-t, újrapróbálkozás {retry_delay} s múlva.")
            time.sleep(retry_delay)
            continue

        try:
            print(f"[INFO] Soros port megnyitása: {port} @ {baud} baud")
            ser = serial.Serial(port, baudrate=baud, timeout=0)
            serial_handle = ser
            print("[OK] Soros kapcsolat létrejött.")
            return ser
        except serial.SerialException as e:
            print(f"[ERR] Nem sikerült megnyitni a portot: {e}")
            print(f"[INFO] Újrapróbálkozás {retry_delay} s múlva...")
            time.sleep(retry_delay)


def serial_worker():
    global serial_handle, rx_led
    ser = open_serial_with_retry(baud=BAUD, retry_delay=RETRY_DELAY)

    try:
        buffer = bytearray()

        global serial_connection_active
        while serial_connection_active:
            try:
                data = ser.read_all()
                # --- Byte counter logic ---
                global bytes_last, bytes_total
                bytes_last = len(data)
                bytes_total += len(data)
                # Schedule GUI label updates
                try:
                    if bytes_total_label is not None:
                        bytes_total_label.after(0, lambda: bytes_total_label.config(text=f"Total: {bytes_total} B"))
                except Exception:
                    pass
                # MCU boot ASCII filter
                if data and (b"OLED" in data or b"START" in data or b"READY" in data):
                    # ignore boot/status ASCII
                    data = b""

                # RX LED: if data received, flash sandybrown briefly
                if data and rx_led is not None:
                    def set_rx_yellow():
                        rx_led.config(bg="sandybrown")
                        rx_led.after(150, lambda: rx_led.config(bg="black"))
                    rx_led.after(0, set_rx_yellow)

                if not data:
                    time.sleep(0.001)   # CPU kímélés, de nem blokkol
                    continue

                buffer.extend(data)

                # --- RAW LoRa packet forwarding: variable-length only, no fixed 11-byte frames ---
                # (keep TEL variable-length decoder below)

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

                                # Alap érvényességi ellenőrzés: ha nagyon elszállt érték jön, tekintsük hibás dekódolásnak
                                if -50.0 <= T <= 80.0 and 0.0 <= RH <= 100.0 and 800.0 <= P <= 1100.0:
                                    last_tel_T  = T
                                    last_tel_RH = RH
                                    last_tel_P  = P
                                else:
                                    print(f"[WARN] Érvénytelen decode: "
                                          f"T_code={T_code} RH_code={RH_code} P_int={P_int_code} P_frac={P_frac_code} -> "
                                          f"T={T:.2f} RH={RH:.1f} P={P:.1f}")
                                    # Ne frissítsük a last_tel_* értékeket, így a legutóbbi jó érték marad meg
                                    continue

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
    print("[INFO] Serial thread stopped.")



def start_gui():
    """Tkinter alapú GUI 2 Hz-es visszajátszással.

    Bal oldali táblázat + grafikonok: 2 Hz-es, MET szerint egyenletesen kirajzolt minták.
    Jobb oldali táblázat: valós időben beérkező, dekódolt TEL minták.
    """
    global csv_file, csv_writer

    root = tk.Tk()
    global led_status, rx_led, tx_led
    global bytes_total_label
    # --- Serial port selector embedded in main GUI ---
    selector_frame = ttk.Frame(root)
    selector_frame.pack(pady=5)
    rx_led = None
    tx_led = None
    root.title("CanSat telemetria dekóder")

    # RX/TX LED indicators (as colored squares)
    rx_led = tk.Label(selector_frame, text="RX", width=3, bg="black", fg="white", font=("Arial", 10))
    rx_led.pack(side=tk.LEFT, padx=2)
    tx_led = tk.Label(selector_frame, text="TX", width=3, bg="black", fg="white", font=("Arial", 10))
    tx_led.pack(side=tk.LEFT, padx=2)

    # --- Byte counters directly under RX/TX LEDs ---
    global bytes_total_label

    byte_counter_frame = tk.Frame(selector_frame, bg="black")
    byte_counter_frame.pack(side=tk.LEFT, padx=10)

    bytes_total_label = tk.Label(byte_counter_frame, text="Total: 0 B",
                                 fg="white", bg="black", font=("Arial", 10))
    bytes_total_label.pack(anchor="w")

    tk.Label(selector_frame, text="Válaszd ki a soros portot:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    ports = list(serial.tools.list_ports.comports())
    # Rebuild port list: USB devices first, others later
    filtered_ports = []
    usb_ports = []
    other_ports = []

    for p in ports:
        desc = (p.description or "").lower()

        # skip WLAN, Bluetooth, audio and n/a junk
        if ("wlan" in desc or
            "wifi" in desc or
            "network" in desc or
            "bluetooth" in desc or
            "(n/a)" in desc or
            "bose" in desc or
            "galaxybuds" in desc):
            continue

        # classify USB-based serial adapters
        if ("usb" in desc or "cp210" in desc or "ch340" in desc or "ftdi" in desc):
            usb_ports.append(p)
        else:
            other_ports.append(p)

    ports = usb_ports + other_ports
    port_choices = [f"{p.device} ({p.description})" for p in ports]

    selected_port = tk.StringVar(value=port_choices[0] if port_choices else "")
    combo = ttk.Combobox(selector_frame, textvariable=selected_port, values=port_choices, width=40, state="readonly")
    combo.pack(side=tk.LEFT, padx=5)
    led_status = tk.Label(selector_frame, text="LINK", width=4, bg="darkgreen", fg="white", font=("Arial", 10, "bold"), relief="solid", bd=1)
    led_status.pack(side=tk.LEFT, padx=10)

    # --- AUTO-CONNECT TO FIRST AVAILABLE DEVICE ---
    if port_choices:
        device = port_choices[0].split(" ")[0]
        global SELECTED_PORT_OVERRIDE
        SELECTED_PORT_OVERRIDE = device
        global serial_thread_started, serial_connection_active
        if not serial_thread_started:
            serial_thread_started = True
            serial_connection_active = True
            threading.Thread(target=serial_worker, daemon=True).start()
            led_status.config(bg="lime", fg="black")

    def apply_port_choice():
        sel = selected_port.get()
        if sel:
            device = sel.split(" ")[0]
            global SELECTED_PORT_OVERRIDE
            SELECTED_PORT_OVERRIDE = device
            global serial_thread_started
            global serial_connection_active
            if not serial_thread_started:
                serial_thread_started = True
                threading.Thread(target=serial_worker, daemon=True).start()
                serial_connection_active = True
                led_status.config(bg="lime", fg="black")

    connect_button = tk.Button(selector_frame, text="Csatlakozás", command=apply_port_choice)
    connect_button.pack(side=tk.LEFT, padx=5)

    # Disconnect button
    def disconnect_serial():
        global SELECTED_PORT_OVERRIDE, serial_thread_started, serial_connection_active, serial_handle
        SELECTED_PORT_OVERRIDE = None
        serial_thread_started = False
        serial_connection_active = False
        print("[INFO] Disconnect requested.")
        led_status.config(bg="red", fg="black")
        # Close serial port if open
        if serial_handle is not None:
            try:
                serial_handle.close()
            except Exception:
                pass
            serial_handle = None

    disconnect_button = tk.Button(selector_frame, text="Leválasztás", command=disconnect_serial)
    disconnect_button.pack(side=tk.LEFT, padx=5)

    # --- Repülési idő számláló ---
    flight_start_MET = tk.IntVar(value=-1)
    flight_elapsed_label = tk.Label(root, text="Eltelt idő: 0 s", font=("Arial", 12))
    flight_elapsed_label.pack(pady=5)

    # Start/Stop buttons in one line
    control_frame = ttk.Frame(root)
    control_frame.pack(pady=5)
    # (Byte counter labels moved to selector_frame, no longer in control_frame)

    def start_flight_timer():
        # jelzés, hogy a következő kirajzolt mintánál állítsuk be a start MET-et
        flight_start_MET.set(-2)
        flight_elapsed_label.config(text="Eltelt idő: 0 s")
        xs.clear()
        Ts.clear()
        RHs.clear()
        Ps.clear()

    def stop_flight_timer():
        flight_start_MET.set(-1)  # stop mode
        flight_elapsed_label.config(text="Eltelt idő: STOP")

    start_button = tk.Button(control_frame, text="Start", command=start_flight_timer)
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(control_frame, text="Stop", command=stop_flight_timer)
    stop_button.pack(side=tk.LEFT, padx=5)

    # A grafikonokhoz használt idősorok
    xs = []   # MET értékek (kirajzolt)
    Ts = []
    RHs = []
    Ps = []
    max_len = 300

    # ------- Felső rész: két táblázat (bal: 2 Hz-es playback, jobb: nyers RX) -------
    table_frame = ttk.Frame(root)
    table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    left_frame = ttk.Frame(table_frame)
    right_frame = ttk.Frame(table_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Bal oldali táblázat – 2 Hz-es visszajátszott minták
    columns_left = ("time", "met", "t", "rh", "p")
    tree_left = ttk.Treeview(left_frame, columns=columns_left, show="headings", height=10)

    tree_left.heading("time", text="Idő (2Hz)")
    tree_left.heading("met",  text="MET")
    tree_left.heading("t",    text="T [°C]")
    tree_left.heading("rh",   text="RH [%]")
    tree_left.heading("p",    text="P [hPa]")

    tree_left.column("time", anchor=tk.CENTER, width=90, stretch=False)
    tree_left.column("met",  anchor=tk.CENTER, width=80, stretch=False)
    tree_left.column("t",    anchor=tk.CENTER, width=80, stretch=False)
    tree_left.column("rh",   anchor=tk.CENTER, width=80, stretch=False)
    tree_left.column("p",    anchor=tk.CENTER, width=100, stretch=False)

    vsb_left = ttk.Scrollbar(left_frame, orient="vertical", command=tree_left.yview)
    tree_left.configure(yscrollcommand=vsb_left.set)

    tree_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb_left.pack(side=tk.RIGHT, fill=tk.Y)

    # Jobb oldali táblázat – nyers, beérkező minták
    columns_right = ("time", "met", "t", "rh", "p")
    tree_right = ttk.Treeview(right_frame, columns=columns_right, show="headings", height=10)

    tree_right.heading("time", text="Idő (RX)")
    tree_right.heading("met",  text="MET_in")
    tree_right.heading("t",    text="T_in [°C]")
    tree_right.heading("rh",   text="RH_in [%]")
    tree_right.heading("p",    text="P_in [hPa]")

    tree_right.column("time", anchor=tk.CENTER, width=90, stretch=False)
    tree_right.column("met",  anchor=tk.CENTER, width=80, stretch=False)
    tree_right.column("t",    anchor=tk.CENTER, width=80, stretch=False)
    tree_right.column("rh",   anchor=tk.CENTER, width=80, stretch=False)
    tree_right.column("p",    anchor=tk.CENTER, width=100, stretch=False)

    vsb_right = ttk.Scrollbar(right_frame, orient="vertical", command=tree_right.yview)
    tree_right.configure(yscrollcommand=vsb_right.set)

    tree_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb_right.pack(side=tk.RIGHT, fill=tk.Y)

    # ------- Alsó rész: Matplotlib ábra 3 tengellyel -------
    fig = Figure(figsize=(8, 5), dpi=100)
    axT = fig.add_subplot(311)
    axRH = fig.add_subplot(312)
    axP = fig.add_subplot(313)

    axT.set_ylabel("T [°C]")
    axRH.set_ylabel("RH [%]")
    axP.set_ylabel("P [hPa]")
    axP.set_xlabel("Idő (2Hz) [s]")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # ------- CSV log fájl -------
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

    # 2 Hz-es visszajátszás állapota
    pending_samples = []   # itt várakoznak a dekódolt minták, amiket 2 Hz-cel játszunk vissza
    prefill_target = 4     # ennyi mintát pufferelünk indulás előtt a simább rajzoláshoz (kb. 2 s)
    tick_started = False   # külön flag a 2 Hz-es tick indulásához
    last_tick_time = 0.0   # az utolsó 500 ms tick időpontja (time.time() szerint)
    playback_seconds = 0.0 # playback idő akkumulátor (2Hz tick)

    def smooth(data, window=5):
        """Egyszerű mozgóátlag a grafikon kisimításához."""
        if len(data) < window:
            return data
        out = []
        for i in range(len(data)):
            start = max(0, i - window + 1)
            out.append(sum(data[start:i+1]) / (i - start + 1))
        return out

    def process_queue():
        """Queue-ból minták átvétele, nyers táblázat frissítése és 2 Hz-es playback."""
        nonlocal tick_started, last_tick_time, pending_samples

        # 1) Minden beérkező mintát azonnal tegyünk át a pending listába és a jobb oldali táblázatba
        while True:
            try:
                MET_i, T, RH, P = sample_queue.get_nowait()
            except queue.Empty:
                break

            pending_samples.append((MET_i, T, RH, P))

            now_str_rx = datetime.datetime.now().strftime("%H:%M:%S")
            tree_right.insert("", "end", values=(now_str_rx, MET_i, f"{T:.2f}", f"{RH:.1f}", f"{P:.1f}"))
            tree_right.yview_moveto(1.0)

        now = time.time()

        # 2) Precíz 500 ms tick – csak akkor indul, ha már van elég minta a pufferben
        if pending_samples:
            # Ha még nem indult a 2 Hz-es tick, várjuk meg a prefill_target mintát
            if not tick_started:
                if len(pending_samples) >= prefill_target:
                    tick_started = True
                    last_tick_time = now
            # Ha már fut a tick, csak akkor dolgozunk, ha letelt a 0,5 s
            if tick_started and (now - last_tick_time) >= 0.5:
                last_tick_time += 0.5

                # Ha időközben kiürült a puffer, ne próbáljunk pop-olni
                if not pending_samples:
                    # semmit nem rajzolunk, de a GUI megy tovább
                    pass
                else:
                    # --- PREVENT advancing MET beyond last received ---
                    latest_rx_met = pending_samples[-1][0]
                    oldest_rx_met = pending_samples[0][0]
                    if xs and xs[-1] >= latest_rx_met:
                        # GUI MET already reached newest RX MET → do NOT tick further
                        return

                    # Safe to advance: pop next chronological sample
                    MET_i, T, RH, P = pending_samples.pop(0)

                    # Biztosítsuk, hogy a bal oldali idősor MET-je szigorúan növekvő legyen.
                    # Ha valamiért régebbi MET érkezne, azt kihagyjuk a kirajzolásból.
                    if not xs or MET_i > xs[-1]:
                        # Repülési idő frissítése a bal oldali (kirajzolt) MET alapján
                        if flight_start_MET.get() == -2:
                            flight_start_MET.set(MET_i)
                        start_met = flight_start_MET.get()
                        if start_met >= 0:
                            elapsed = (MET_i - start_met) * 0.5
                            if elapsed < 0:
                                elapsed = 0
                            flight_elapsed_label.config(text=f"Eltelt idő: {elapsed} s")

                        # 2Hz playback idő akkumulátor frissítése
                        nonlocal playback_seconds
                        playback_seconds += 0.5
                        now_str = f"{playback_seconds:6.1f}s"
                        # Bal oldali táblázat bővítése
                        tree_left.insert("", "end", values=(now_str, MET_i, f"{T:.2f}", f"{RH:.1f}", f"{P:.1f}"))
                        tree_left.yview_moveto(1.0)

                        # Idősorok frissítése a grafikonhoz
                        xs.append(MET_i)
                        Ts.append(T)
                        RHs.append(RH)
                        Ps.append(P)

                        if len(xs) > max_len:
                            xs[:] = xs[-max_len:]
                            Ts[:] = Ts[-max_len:]
                            RHs[:] = RHs[-max_len:]
                            Ps[:] = Ps[-max_len:]

                        # CSV log – a 2 Hz-es, kirajzolt streamről
                        if csv_writer is not None:
                            try:
                                csv_writer.writerow([now_str, MET_i, f"{T:.2f}", f"{RH:.1f}", f"{P:.1f}"])
                                csv_file.flush()
                            except Exception as e:
                                print(f"[WARN] CSV írási hiba: {e}")

                        # Grafikonok frissítése
                        if xs:
                            axT.clear()
                            axRH.clear()
                            axP.clear()

                            # X tengely: eltelt idő másodpercben (2Hz → 0.5s lépés)
                            xs_plot = [i * 0.5 for i in range(len(xs))]

                            axT.plot(xs_plot, smooth(Ts, 3))
                            axRH.plot(xs_plot, smooth(RHs, 3))
                            axP.plot(xs_plot, smooth(Ps, 7))

                            axT.set_ylabel("T [°C]")
                            axRH.set_ylabel("RH [%]")
                            axP.set_ylabel("P [hPa]")
                            axP.set_xlabel("Time [s]")

                            # 120 s-es csúszó ablak
                            if start_met >= 0 and xs_plot:
                                x_max = xs_plot[-1]
                                x_min = max(0, x_max - 120)
                                axT.set_xlim([x_min, x_max])
                                axRH.set_xlim([x_min, x_max])
                                axP.set_xlim([x_min, x_max])

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

    # Indítjuk a periodikus queue feldolgozást
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
    # t = threading.Thread(target=serial_worker, daemon=True)
    # t.start()

    # Grafikus felület indítása (blokkoló hívás)
    start_gui()