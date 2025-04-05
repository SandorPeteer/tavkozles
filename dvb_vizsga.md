# Távközlési technikus vizsgafeladat

## **B tétel:** Földfelszíni digitális TV vételi rendszer telepítése, konfigurálása és mérése

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése a megadott eszközökkel, az összes ingyenesen elérhető multiplex (Miskolc, Avasi adótorony) adatbázisból történő kiválasztása.

> A megfelelő frekvenciák beállítása, valamint a jelszintek és egyéb paraméterek mérése, annak dokumentálása.

> A beállított antenna jelét a villamos 3 laborba egy 2-es jelosztón keresztül a rendelkezésre álló set-top boxra, valamint egy Metek HDD spektrum analizátorra kell csatlakoztatni.   

**Időkeret:** 120 perc  

---

![dvb](https://github.com/user-attachments/assets/3c122ca7-9e70-4e0a-92ad-e9ea1788b259)

## **1. Szükséges eszközök**
- **Antenna:** Beltéri vagy kültéri antenna (a vizsgázó tétel húzásának alapján)
- **Set-top box:** Amiko HD8265+ vagy Nytro Box
- **Mérőműszer:** METEK HDD digitális TV jelmérő
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** 2-es jelosztó a mérési pont kialakításához
- **Szerelési eszközök:** telefonos iránytű, maps.google.com

---

## **2. Feladatok és időbeosztás**

### **1. Előkészületek (10 perc)**
- Ellenőrizze az összes szükséges eszközt.
- Biztosítsa a megfelelő munkakörnyezetet.

### **2. Antenna felszerelése és beállítása (30 perc)**
- **Válassza ki a megfelelő antennát** (beltéri vagy kültéri), figyelembe véve az adótorony távolságát és a vételi környezetet.
- **Kültéri antenna esetén:** rögzítse stabil módon az udvaron.
- **Beltéri antenna esetén:** helyezze el optimálisan a v3 labor asztalán, akadálymentesen.
- **Az antenna pontos beállítása:**
  - Használja az **iránytűt** és a **maps.google.com** oldalt az adótorony felé történő irányba állításhoz.
  - A METEK HDD mérőműszert az antennára közvetlenül rácsatlakoztatva végezze el a **finomhangolást**.
  - Az **5. pontban található táblázat** első részét töltse ki az aktuálisan mérhető értékekkel. Saját meghajtóra mentett táblázattal, hogy egymásét ne írjuk felül! [TÁBLÁZAT](https://docs.google.com/spreadsheets/d/1NkTK1tls5gR6LeJ_V9S_o9S0uxuxc8ZEIHaER2DFV2k/edit?gid=0#gid=0)

### **3. Kábelezés, mérési pontok kialakítása és eszközök csatlakoztatása (20 perc)**
- **Az Antenna átcsatlakoztatása a 2 utas jelosztón keresztül a set-top-boxra és a spektrum analizátorra:** Csatlakoztassa a megfelelő koaxiális kábeleket.
- **A Set-top box és a TV / monitor csatlakoztatása:** Használja a megfelelő HDMI vagy AV kábelt.
- Az **5. pontban található táblázat** jelosztás utáni méréseinek kitöltése. [TÁBLÁZAT](https://docs.google.com/spreadsheets/d/1NkTK1tls5gR6LeJ_V9S_o9S0uxuxc8ZEIHaER2DFV2k/edit?gid=0#gid=0)

### **4. Set-top box beállítása és csatornakeresés (15 perc)**
- **Az ingyenes DVB-T multiplexek kiválasztása a miskolci Avasi adótorony adatbázisából:** ami itt elérhető el: [fmdx.hu](https://www.fmdx.hu/transmitters-hng-avas.htm)
- **Automatikus vagy kézi csatornakeresés indítása**
- Ellenőrizze az elérhető DVB-T **FTA csatorna** megfelelő működését.

### **5. Jelszintmérés és dokumentáció (15 perc)**
- Másoljon magának mentés máskénttel ebből a táblázatból, majd töltse ki a DVB-t vétel minőségi paramétereinek dokumentálásához: [TÁBLÁZAT](https://docs.google.com/spreadsheets/d/1NkTK1tls5gR6LeJ_V9S_o9S0uxuxc8ZEIHaER2DFV2k/edit?gid=0#gid=0)
- **Mérések és dokumentáció az antennánál:**
  - A teljes spektrum képernyő képének mentése az összes fogható multiplex frekvenciáival
  - A meter rész képernyő képei csatornánként: Jelszintek, jelminőség, moduláció, konstelláció
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

### **6. Mérési eredmények** rögzítése a jegyzőkönyvben táblázatos formában:
  - **Multiplex neve**
  - **Frekvencia** MHz
  - **ERP** az adótorony által kisugárzott teljesítmény
  - **Jelerősség (dBμV)**
  - **Zaj viszony**
  - **Modulation Error Ratio (MER - dB)**
  - **Csomag vesztés** Pacekt errors
  - **Moduláció**
  - **Csillapítás számítása az osztott és osztatlan jel között (dB)**
  - **Hőmérséklet és időjárási körülmények**

- **Jegyzőkönyv elkészítése a táblázattal és a begyűjtött képekkel igazolva.**

--- 

### **7. Szituációs feladat:**

#### Ha a való életben egy családi házra vagy társasházra kellene felszerelnie az antennát, hova helyezné el azt, és miért?!

- **Melyik tető- vagy homlokzati részt választaná az antenna felszereléséhez, és milyen szempontokat venne figyelembe a döntés során?**  
- **Hogyan biztosítaná, hogy az antenna megfelelő rálátást kapjon az adóra, és milyen módszerekkel határozná meg a pontos irányt és dőlésszöget?**  
- **Milyen rögzítési megoldásokat alkalmazna a stabil és biztonságos telepítés érdekében?**  
- **Hogyan kezelné az időjárási viszontagságokat (pl. erős szél, jég, hó) az antenna rögzítése és védelme szempontjából?**  
- **Ha hosszú koaxiális kábeleket kellene használnia a beltéri egységhez, milyen módon csökkentené a jelveszteséget?**  

📌 **A jegyzőkönyvbe írja le részletesen a választását, és indokolja meg a döntéseit a vétel minősége és a hosszú távú megbízhatóság szempontjából!**

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
