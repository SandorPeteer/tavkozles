# Mérési Jegyzőkönyv – Johansson 8202 DVB-T modulátor

**Mérés helye:** Laboratórium A2  
**Dátum:** 2024. október 5.  
**Hallgatók neve:** Kiss Péter, Kovács Anna  
**Csoport:** Távközlési technikus, 12B  
**Mérés tárgya:** DVB-T jel generálása és mérése Johansson 8202 DVB-T modulátorral és METEK HD spektrum/jelszint analizátorral.

---

## 1. Johansson 8202 modulátor beállítása

A mérés során a következő beállításokat alkalmaztuk a Johansson 8202 DVB-T modulátoron:

- **RF frekvencia:** 474 MHz
- **Moduláció típusa:** 64-QAM
- **Sávszélesség:** 8 MHz
- **Jelszint:** 70 dBm

A DVB-T jel generálása után csatlakoztattuk az RF kábelt a METEK HD spektrum/jelszint analizátorhoz, majd megkezdtük a mérési adatgyűjtést különböző modulációs típusokkal.

---

## 2. Mérési Eredmények

Az alábbi táblázatban összefoglaljuk a mérések eredményeit különböző beállításokkal.

| Mérési paraméter   | RF frekvencia (MHz) | Moduláció típusa | Sávszélesség (MHz) | Jelszint (dBm) | Bitsebesség (Mbps) | MER érték (dB) |
|--------------------|---------------------|------------------|--------------------|----------------|--------------------|----------------|
| **Mérési eredmény 1** | 474                 | 64-QAM           | 8                  | 70             | 24.1               | 36             |
| **Mérési eredmény 2** | 474                 | 16-QAM           | 8                  | 70             | 18.2               | 39             |
| **Mérési eredmény 3** | 474                 | QPSK             | 8                  | 70             | 12.1               | 42             |

---

## 3. Eredmények kiértékelése

- **MER (Modulation Error Ratio) értékek:**
  A mérési eredményekből látható, hogy a MER értékek modulációtól függően változnak. A 64-QAM modulációval a MER érték 36 dB, ami alacsonyabb, mint a 16-QAM és QPSK modulációk esetében. Ez összhangban van az elvárásokkal, mivel a magasabb modulációs rendnél (64-QAM) a jelkódolás érzékenyebb a zajokra és hibákra.

- **Bitsebesség:**
  A bitsebesség szintén a modulációs rend függvénye. 64-QAM moduláció esetén 24.1 Mbps, míg QPSK esetén 12.1 Mbps volt. Ez is megfelel az elvárásoknak, hiszen a nagyobb modulációs rend több információt képes továbbítani egy időegység alatt.

- **Jelminőség:**
  Az 474 MHz-es frekvencián végzett mérések stabil eredményeket mutattak minden modulációs típussal. A jelszint mindhárom mérésnél állandóan 70 dBm volt, így biztosítottuk, hogy a változó faktorok a modulációs típusok és nem a jelerősségből fakadtak.

---

## 4. Következtetések

A mérési eredmények alapján megállapítható, hogy a **64-QAM** moduláció biztosítja a legnagyobb adatsebességet, de a jelkódolás minősége (MER) alacsonyabb, mint a kisebb modulációs rendeknél (16-QAM és QPSK). A **QPSK** moduláció kiváló MER értéket nyújtott, de a bitsebesség lényegesen alacsonyabb volt.

**Ajánlás:** A DVB-T rendszerek esetében a modulációs típus megválasztása kompromisszumot igényel az adatsebesség és a jelminőség között. Amennyiben stabil környezeti feltételek mellett használják, a 64-QAM moduláció nagy adatsebességet biztosít. Zajosabb vagy interferenciás környezetben a QPSK moduláció megbízhatóbb jelátvitelt eredményez.

---

**Hallgatók aláírása:**  
Kiss Péter: ___________________  
Kovács Anna: ___________________

**Oktató aláírása:**  
Dr. Nagy László: ___________________
