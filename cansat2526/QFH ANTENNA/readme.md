# QFH Antenna – 434 MHz (2.2 mm csupasz réz, 32 mm PVC)
**Végleges, reprodukálható méretezés**

<img width="270" alt="434MHz_QFH_SP" src="https://github.com/user-attachments/assets/7cff62a1-229a-473c-84df-f088b39bd899" />

Ez a szerkezet bármelyik villanyszerelési boltban kapható 2.2 mm csupasz rézből, 32 mm PVC csőre épített, 434 MHz-re optimalizált QFH antenna végleges méreteit tartalmazza.  
A modell alapja valós mérésekkel kalibrált geometria, LoRa 433–434 MHz-es sávra optimalizálva.

---

## 📡 Áttekintés

- **Célfrekvencia:** 434 MHz  
- **Vezető:** 2.2 mm csupasz réz  
- **Tartócső:** 32 mm PVC (külső átmérő)  
- **Kialakítás:** félfordulatos (0.5 turn) Quadrifilar Helix  
- **Építési metódus:** derékszögű hajlítások a dróton, PVC furatokba illesztett egyenes szárakkal  
- **Méréssel igazolt CF:** 433–435 MHz tartományban, S11 ≈ –10…–12 dB

---

# 1. Méretek összefoglaló táblázatban

## 1.1 Large loop – 2.2 mm csupasz réz

| Paraméter | Érték (mm) |
|----------|------------|
| **Teljes dróthossz** | **736.8** |
| **Középpont a dróton** | 368.4 |
| **Belső átmérő (Di1)** | 93.9 |
| **Sugár (Di1/2)** | **47.0** *(PVC-be illeszkedő egyenes szakasz)* |

### Hajlítási pontok (az egyik végétől mérve)

| Hajlítás sorszáma | Hely (mm) |
|-------------------|-----------|
| 1. | **47.0** |
| 2. | **321.4** |
| 3. | **415.4** |
| 4. | **689.8** |

---

## 1.2 Small loop – 2.2 mm csupasz réz

| Paraméter | Érték (mm) |
|----------|------------|
| **Teljes dróthossz** | **701.8** |
| **Középpont a dróton** | 350.9 |
| **Belső átmérő (Di2)** | 89.3 |
| **Sugár (Di2/2)** | **44.6** |

### Hajlítási pontok (az egyik végétől mérve)

| Hajlítás sorszáma | Hely (mm) |
|-------------------|-----------|
| 1. | **44.6** |
| 2. | **306.3** |
| 3. | **395.6** |
| 4. | **657.2** |

---

# 2. PVC cső – furatok pozíciói

A felső furatsor fixen maradhat.  
Az alsó furatokat ennyire kell lejjebb fúrni a felsőkhöz képest:

| Hurok | Felső–alsó furatsor távolság (H) |
|-------|----------------------------------|
| **Large loop** | **222.5 mm** |
| **Small loop** | **211.9 mm** |

A furatok egymással **90°-ban eltolva** helyezkedjenek el.   
---

# 3. Építés menete (röviden)

1. **Drót levágása**  
   - Large: 736.8 mm  
   - Small: 701.8 mm  

2. **Hajlítási pontok bejelölése**  
   - a táblázatok alapján  
   - minden jelölt ponton 90°-os törés

3. **PVC furatok elkészítése**  
   - Large: 222.5 mm  
   - Small: 211.9 mm  
   (a felső lyukaktól mérve lefelé)

4. **Drótok befűzése**  
   - a 44–47 mm-es egyenes szárak mennek a PVC-be  
   - a drót a cső körül félfordulatot tesz (0.5 twist)

5. **Koax csatlakoztatása**  
   - közvetlen forrasztás  
   - javasolt: ferrit gyűrű vagy 5–6 menet koax fojtó

---

# 4. Validáció (NanoVNA)

- **433.5–437.5 MHz** közötti fő rezonanciavölgy  
- S11 ≈ –10…–12 dB  
- Impedancia ≈ 45–55 Ω  
- Stabilabb frekvencia fojtóval

---

# 5. Reprodukciós megjegyzések

- A méretek valós mérések alapján kerültek kalibrálásra.  
- A 2.2 mm csupasz réz elsőre a 434 MHz-es sávba hangol.  
- A környezet (asztal, kéz, koax) 1–3 MHz eltolást okozhat.

---

# 🔧 Licenc
Szabadon felhasználható LoRa, SDR és műholdas projektekhez.
