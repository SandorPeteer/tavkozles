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