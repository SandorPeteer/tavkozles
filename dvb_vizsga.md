# Távközlési technikus vizsgafeladat

## **B tétel:** Földfelszíni digitális TV vételi rendszer telepítése, konfigurálása és mérése

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése a megadott eszközökkel, egy elérhető adótorony (Miskolc, Avasi adótorony) adatbázisból történő kiválasztása.

> A megfelelő frekvenciák beállítása, valamint a jelszint és egyéb paraméterek mérése és dokumentálása.

> A beállított jelet a villamos 3 laborba kell bevinni, ahol azt egy jelosztón keresztül a set-top boxra és spektrum analizátorra csatlakoztat.   

**Időkeret:** 120 perc  

---

![dvb](https://github.com/user-attachments/assets/3c122ca7-9e70-4e0a-92ad-e9ea1788b259)

## **1. Szükséges eszközök**
- **Antenna:** Beltéri vagy kültéri antenna (a vizsgázó választása alapján)
- **Set-top box:** Amiko HD8265+ vagy Nytro Box
- **Mérőműszer:** METEK HDD digitális TV jelmérő
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** jelosztó a mérési pontok kialakításához
- **Szerelési eszközök:** iránytű, maps.google.com

---

## **2. Feladatok és időbeosztás**

### **1. Előkészületek (10 perc)**
- Ellenőrizze az összes szükséges eszközt.
- Biztosítsa a megfelelő munkakörnyezetet.
- **Internetes adatbázisból keressen egy elérhető multiplexet a Miskolc, Avasi adótoronyból.** (Frekvencia, teljesítmény, polarizáció, adás típusa)
- Az adótorony adatbázisa elérhető itt: [fmdx.hu](https://www.fmdx.hu/transmitters-hng-avas.htm)

### **2. Antenna felszerelése és beállítása (30 perc)**
- **Válassza ki a megfelelő antennát** (beltéri vagy kültéri), figyelembe véve az adótorony távolságát és a vételi környezetet.
- **Kültéri antenna esetén:** rögzítse stabil módon a tripod-ra.
- **Beltéri antenna esetén:** helyezze el optimálisan a v3 labor egyik jó vételi pontján, akadálymentesen.
- **Az antenna pontos beállítása:**
  - Használja az **iránytűt** és a google maps-t az adótorony felé történő pontos irányba állításhoz.
  - METEK HDD mérőműszer segítségével végezze el a **finomhangolást**.

### **3. Kábelezés, mérési pontok kialakítása és eszközök csatlakoztatása (20 perc)**
- **Antenna és set-top box összekötése:** Csatlakoztassa a megfelelő koaxiális kábelt.
- **Set-top box és TV / monitor csatlakoztatása:** Használja a megfelelő HDMI vagy AV kábelt.
- **Jelosztó beépítése:** Helyezzen be egy jelosztót a mérési pont kialakításához.
- **Külső antenna esetén a jelet a villamos 3 laborba kell bevinni, hogy az csatlakoztatható legyen.**

### **4. Set-top box beállítása és csatornakeresés (15 perc)**
- **Az ingyenes DVB-T multiplexek kiválasztása a miskolci Avasi adótorony adatbázisából.**
- **A multiplexhez tartozó paraméterek beállítása:**
  - Frekvencia (MHz)
  - Moduláció típusa és egyéb jellemzők
- **Automatikus vagy kézi csatornakeresés indítása**
- Ellenőrizze az elérhető DVB-T **FTA csatorna** megfelelő működését.

### **5. Jelszintmérés és dokumentáció (15 perc)**
- Másoljon magának mentés máskénttel ebből a táblázatból, majd töltse ki a DVB-t vétel minőségi paramétereinek dokumentálásához: [TÁBLÁZAT](https://docs.google.com/spreadsheets/d/1NkTK1tls5gR6LeJ_V9S_o9S0uxuxc8ZEIHaER2DFV2k/edit?gid=0#gid=0)
- **Mérések és dokumentáció az antennánál:**
  - Spektrum analizátor képe
  - Jelszintek és jelminőség
  - Multiplex adatok (frekvencia, szimbólumráta, FEC)
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

### **6. Mérési eredmények** rögzítése a jegyzőkönyvben:
  - **Jelerősség (dBμV)**
  - **Jel-zaj viszony (SNR - dB)**
  - **Bit Error Rate (BER)**
  - **Modulation Error Ratio (MER - dB)**
  - **Csillapítás (dB)**
  - **Lock állapot:** [ ] Igen [ ] Nem
  - **Hőmérséklet és időjárási körülmények**
  - **Multiplex adatok és frekvenciák**
- **Jegyzőkönyv elkészítése és aláírása.**

--- 

### **7. Szituációs feladat:**

#### Ha a való életben egy családi házra vagy társasházra kellene felszerelnie a műholdas antennát, hova helyezné el azt, és miért?

- **Melyik tető- vagy homlokzati részt választaná az antenna felszereléséhez, és milyen szempontokat venne figyelembe a döntés során?**  
- **Hogyan biztosítaná, hogy az antenna megfelelő rálátást kapjon az adott műholdra, és milyen módszerekkel határozná meg a pontos irányt és dőlésszöget?**  
- **Milyen rögzítési megoldásokat alkalmazna a stabil és biztonságos telepítés érdekében?**  
- **Hogyan kezelné az időjárási viszontagságokat (pl. erős szél, jég, hó) az antenna rögzítése és védelme szempontjából?**  
- **Ha hosszú koaxiális kábeleket kellene használnia a beltéri egységhez, milyen módon csökkentené a jelveszteséget?**  

📌 **A jegyzőkönyvbe írja le részletesen a választását, és indokolja meg a döntéseit a műholdas vétel minősége és a hosszú távú megbízhatóság szempontjából!**

---

## **3. Értékelési szempontok**

| Feladat | Pontszám |
|---------|----------|
| Eszközök beüzemelése | 5 pont |
| Antenna finomhangolása | 10 pont |
| Multiplexek kiválasztása internetes adatbázisból | 10 pont |
| Kábelezés, jelosztó használata és csatlakoztatás | 5 pont |
| Vételi paramétertek vizsgálata a METEK HDD-vel | 25 pont |
| Set-top box megfelelő beállítása | 5 pont |
| FTA csatorna megtalálása és beállítása | 10 pont |
| Részletes dokumentálás  | 20 pont |
| Szituációs feladat  | 10 pont |
| **Összesen:** | **100 pont** |

**Sikeres vizsgához minimum 40 pont szükséges.**   

---

**Megjegyzés:** A feladat során ügyelni kell a pontos dokumentálásra és a mérési eredmények rögzítésére.

---

**Vizsgázó neve:** ........................................  
**Vizsgázó aláírása:** .....................................

**Vizsgáztató aláírása:** .....................................

**Dátum:** ....................................
