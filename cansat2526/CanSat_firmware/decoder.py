#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import serial
import serial.tools.list_ports
import struct
import datetime

BAUD = 115200        # szükség esetén módosítható
RETRY_DELAY = 2.0    # másodperc – újrapróbálkozás között


# Globális változók az utolsó TEL-ből rekonstruált értékekhez
last_tel_T = None
last_tel_RH = None
last_tel_P = None


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


def main():
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

                # SYNC-to-SYNC continuous extraction (no 48-byte limit)
                while True:
                    if len(buffer) < 2:
                        break

                    # Ensure first byte is SYNC
                    if buffer[0] not in (0xA5, 0xA6):
                        try:
                            next_sync_pos = min(
                                buffer.index(0xA5) if 0xA5 in buffer else len(buffer),
                                buffer.index(0xA6) if 0xA6 in buffer else len(buffer)
                            )
                            del buffer[:next_sync_pos]
                        except ValueError:
                            buffer.clear()
                        continue

                    # Look for next SYNC after byte 0
                    next_sync = None
                    for i in range(1, len(buffer)):
                        if buffer[i] in (0xA5, 0xA6):
                            next_sync = i
                            break

                    # If no next SYNC yet → need more data
                    if next_sync is None:
                        break

                    # Extract packet: SYNC → before next SYNC
                    packet = buffer[:next_sync]
                    del buffer[:next_sync]

                    sync = packet[0]
                    data = packet[1:]

                    # TELE – teljes, bitre pontos visszafejtés 0,5 s-es mintákra
                    if sync == 0xA5:
                        if len(data) >= 4:
                            base_MET = data[0] | (data[1] << 8)
                            N        = data[2]
                            bitmask  = data[3]

                            # A pack-ek a 4. bájttól indulnak
                            pack_idx = 4

                            # Végigmegyünk az összes mintán (0..N-1),
                            # és minden 0,5 s-es mintát rekonstruálunk.
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

                                    pack_bytes = data[pack_idx:pack_idx+4]
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
                                    # Ha még soha nem volt TEL-érték, akkor nem tudunk érvényes sort írni.
                                    if last_tel_T is None:
                                        continue

                                # Minden 0,5 s-es mintát külön sorba írunk ki
                                print(f"{datetime.datetime.now().strftime('[%H:%M:%S]')} [TEL] MET={MET_i}  T={last_tel_T:.2f}C  RH={last_tel_RH:.1f}%  P={last_tel_P:.1f}hPa")

                        else:
                            print(f"[TEL] RAW {data.hex().upper()}")

                    else:
                        print(f"[UNK] {packet.hex().upper()}")

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


if __name__ == "__main__":
    # Ellenőrzés: telepítve van-e a pyserial
    try:
        # már importáltuk fent, ez csak emlékeztető hiba esetére
        pass
    except ImportError:
        print("Hiányzik a pyserial csomag. Telepítés:\n\n    pip install pyserial\n")
        sys.exit(1)

    main()