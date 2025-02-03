# Távközlési technikus vizsgafeladat

## **Téma:** Műholdas vételi rendszer telepítése, konfigurálása és mérése

**Vizsgázó neve:** ........................................  
**Időkeret:** 120 perc  
**Feladat leírása:** A vizsgázó feladata egy műholdas vételi rendszer kiépítése a megadott eszközökkel, egy szabadon fogható (FTA) csatorna beállítása, valamint a jelszint mérése és dokumentálása. A vizsgázónak **internet alapú adatbázisból** ki kell választania egy **aktuálisan vehető műholdat és egy FTA csatornát**, amelyre a rendszert beállítja. A műhold pontos azonosítását és finomhangolását **METEK HDD műszerrel** kell elvégeznie. A beállított jelet **a villamos 3 laborba kell bevinni, ahol az már közvetlenül a set-top boxra csatlakoztatható.**

---

## **1. Szükséges eszközök**
- **Parabolaantenna:** D80 Mesh hálós acél parabola antenna (tripodra szerelve)
- **Műholdvevő fej (LNB):** **A vizsgázó maga választja ki az elérhető Inverto ULTRA vagy Ekselans SATCR LNB-k közül**
- **Set-top box:** Amiko HD 8265+ vagy Amiko Viper Combo 4K-V40
- **Mérőműszer:** METEK HDD műholdas jelmérő
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** 2-es műholdas jelosztó a mérési pontok kialakításához
- **Szerelési eszközök:** csavarhúzó, villáskulcs, iránytű, dőlésszögmérő

---

## **2. Feladatok és időbeosztás**

### **1. Előkészületek (10 perc)**
- Ellenőrizze az összes szükséges eszközt.
- Biztosítsa a megfelelő munkakörnyezetet.
- **Válasszon ki egy LNB-t** az elérhető Inverto ULTRA vagy Ekselans SATCR műholdfejek közül.
- **Internetes műholdas adatbázisból** keressen egy **aktuálisan vehető műholdat és FTA csatornát**. Ajánlott források:
  - [LyngSat](https://www.lyngsat.com/)
  - [KingOfSat](https://en.kingofsat.net/)
  - [SatBeams](https://www.satbeams.com/)

### **2. Antenna és LNB felszerelése (30 perc)**
- Szerelje össze és rögzítse a **D80 Mesh parabolaantennát** a tripod állványra.
- Helyezze fel a **kiválasztott LNB-t** az antennára.
- Ellenőrizze az LNB rögzítését és a megfelelő polarizációs szög beállítását.
- **Jelosztó beépítése:** Helyezzen be egy 2-es műholdas jelosztót a mérési pont kialakításához.


### **3. Antenna beállítása és műhold azonosítása (30 perc)**
- Vigye ki szabadtérre az antennát a megfelelő vételi környezet kialakítása miatt. 
- Használja az **iránytűt és a dőlésszögmérőt** az antenna azimut és eleváció beállításához az **interneten választott műhold** adatai alapján.
- **METEK HDD műszer segítségével azonosítsa a műholdat.**
- Végezze el a **finomhangolást** a maximális jelerősség eléréséhez.
- **Mérések és dokumentáció az antennánál:**
  - Spektrum analizátor képe
  - Jelszintek és jelminőség
  - Antenna pozíciók és szögek (azimut, eleváció)
  - Kimenő feszültség és áramerősség az LNB-re
  - Polarizáció
  - Transzponder adatok (frekvencia, szimbólumráta, FEC)
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

### **4. Kábelezés, mérési pontok kialakítása és eszközök csatlakoztatása (20 perc)**
- **LNB és set-top box összekötése:** Csatlakoztassa a megfelelő koaxiális kábelt.
- **Set-top box és TV csatlakoztatása:** Használja a megfelelő HDMI vagy AV kábelt.
- **A jelet a villamos 3 laborba kell bevinni, hogy az közvetlenül a set-top boxra csatlakoztatható legyen.**

### **5. Set-top box beállítása és csatornakeresés (15 perc)**
- **Szerelje össze a beltéri rendszert** és csatlakoztassa a TV / monitorra. 
- **Nyelv és régió beállítása:** Magyar nyelv, megfelelő régió kiválasztása.
- **Műhold és transzponder beállítása:**
  - A **korábban interneten kiválasztott műhold és FTA csatorna adatai alapján**.
  - **Automatikus csatornakeresés indítása**
  - Ellenőrizze a kijelölt **FTA csatorna** megfelelő működését.
- **Mérések és dokumentáció bent, a set-top boxnál:**
  - Spektrum analizátor képe (jelosztó után)
  - Jelszintek és jelminőség
  - Transzponder adatok ellenőrzése
  - Kimenő feszültség az LNB-re
  - Polarizáció
  - Hőmérséklet, időjárás feljegyzése

### **6. Jelszintmérés és dokumentáció (15 perc)**
- Mérési eredmények rögzítése a jegyzőkönyvben:
  - **Jelerősség (dBμV)**
  - **Jel-zaj viszony (SNR - dB)**
  - **Bit Error Rate (BER)**
  - **Modulation Error Ratio (MER - dB)**
  - **Csillapítás (dB)**
  - **Lock állapot:** [ ] Igen [ ] Nem
  - **Hőmérséklet és időjárási körülmények**
  - **Transzponder adatok és frekvenciák**
- **Jegyzőkönyv elkészítése és aláírása.**

--- 

### **.7 Szituációs feladat:**

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
| Eszközök előkészítése | 5 pont |
| LNB kiválasztása és felszerelése | 10 pont |
| Műhold kiválasztása internetes adatbázisból | 10 pont |
| Antenna pontos beállítása és műhold azonosítása METEK HDD-vel | 25 pont |
| Kábelezés, jelosztó használata és csatlakoztatás | 5 pont |
| Set-top box megfelelő beállítása | 5 pont |
| FTA csatorna megtalálása és beállítása | 10 pont |
| Részletes jelszintmérés és dokumentálás  | 20 pont |
| Szituációs feladat  | 10 pont |
| **Összesen:** | **100 pont** |

**Sikeres vizsgához minimum 40 pont szükséges.**

---

**Megjegyzés:** A feladat során ügyelni kell a pontos dokumentálásra és a mérési eredmények rögzítésére.

---

**Vizsgázó aláírása:** .....................................

**Vizsgáztató aláírása:** .....................................

**Dátum:** ....................................

