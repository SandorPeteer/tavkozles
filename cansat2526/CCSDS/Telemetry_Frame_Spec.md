# Telemetry Frame Specification
## CCSDS-Inspired, State-Based Telemetry over LoRa PHY

---

## 1. Scope

This document defines a fixed-length, deterministic telemetry frame format
for space-grade telemetry transmission over LoRa PHY.
The protocol is state-based, delta-encoded, and self-synchronizing.

---

## 2. Design Rules

- Fixed frame length
- Deterministic decoding
- State-based interpretation
- Delta encoding with absolute resynchronization
- No variable-length fields
- No unused bytes
- Frame-level suppression only
- Explicit sequence counter
- CRC protected

---

## 3. Physical Layer Assumptions

| Parameter | Value |
|----------|-------|
| Modulation | LoRa (SX1278 class) |
| CRC (PHY) | Enabled |
| Endianness | Little-endian |
| Bit ordering | LSB-first inside fields |
| Packet length | Fixed |

---

## 4. Frame Types

| Type | Description |
|------|-------------|
| FULL_STATE | Absolute state frame (key frame) |
| DELTA_STATE | Delta update frame |

Frame type is indicated by FLAGS.bit0.

---

## 5. Telemetry Frame Layout

```
BYTE
────────────────────────────────────────────
0      SYNC                0xA5

1–2    MET / SEQ           uint16

3      FLAGS
       bit0 = FULL_STATE
       bit1 = RESET_EVENT
       bit2 = MODE_CHANGE
       bit3..7 = RESERVED

4      VALIDITY MAP
       bit0 = Temperature
       bit1 = Humidity
       bit2 = Pressure
       bit3..7 = RESERVED

5–34   DATA BLOCK          30 bytes

35–36  CRC16-CCITT
────────────────────────────────────────────
```

Total frame length: **37 bytes**

---

## 6. FULL_STATE Data Encoding

Per-sample field layout:

| Field | Bits | Resolution | Range |
|-------|------|------------|-------|
| Temperature | 11 | 0.1 °C | −40.0 … +87.9 |
| Humidity | 7 | 1 % | 0 … 100 |
| Pressure | 12 | 0.1 hPa | 822.0 … 1077.0 |

Bits per sample: **30**

Samples per frame: **8**

Total payload: `8 × 30 bit = 240 bit = 30 byte`

---

## 7. DELTA_STATE Data Encoding

Delta limits are symmetric around zero.

| Field | Bits | Resolution | Range |
|-------|------|------------|-------|
| ΔTemperature | 6 | 0.1 °C | −3.2 … +3.1 |
| ΔHumidity | 4 | 1 % | −8 … +7 |
| ΔPressure | 7 | 0.1 hPa | −6.4 … +6.3 |

Bits per sample: **17**

Unused bits are zero-filled.

---

## 8. Validity Map Semantics

| Bit | Meaning |
|-----|--------|
| 0 | Temperature updated |
| 1 | Humidity updated |
| 2 | Pressure updated |

VALIDITY = 0 indicates no state change.

---

## 9. Frame Suppression Rules

A frame MUST NOT be transmitted if:

- VALIDITY MAP == 0
- No event flags set
- Data identical to previous frame

Sequence counter continues.

---

## 10. FULL_STATE Transmission Requirements

FULL_STATE MUST be sent on:

- System startup
- Reset or watchdog event
- Sequence discontinuity
- Delta overflow
- Receiver desynchronization
- Periodic resynchronization

---

## 11. Receiver State Rules

RX_STATE_VALID = false

on FULL_STATE:
  RX_STATE = absolute values
  RX_STATE_VALID = true

on DELTA_STATE:
  if RX_STATE_VALID:
    RX_STATE += delta
  else:
    discard frame

on SEQ discontinuity:
  RX_STATE_VALID = false

---

## 12. Error Protection

| Layer | Mechanism |
|-------|-----------|
| PHY | LoRa FEC |
| Frame | CRC16-CCITT |
| Logic | Sequence counter |
| Data | Delta overflow → FULL_STATE |

---

## 13. Specification Status

This specification is FINAL and FROZEN.
Any change requires protocol version increment.
