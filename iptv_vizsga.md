# Távközlési technikus vizsgafeladat

## DVB-T jel fejállomásba küldése és IPTV rendszeren való kiadása

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése, a megfelelő adótorony (Miskolc, Avasi adótorony) kiválasztása, a jel mérésének és elosztásának elvégzése, valamint az IPTV rendszer konfigurálása.  

> Az ingyenesen fogható multiplexek jelerősségének ellenőrzése, és a DVB-T jel **LEMCO SCL-824CT fejállomásba** történő bevezetése. A fejállomásból a digitális tartalom **IPTV streamként kerül kiadásra**.  

> A Multicast IP tartomány megválasztása és az IPTV Set-top-box konfigurálása a megfelelő vételhez.  

**Időkeret:** 120 perc  

---

![lemco-scl-824ct-8-dvb-s-s2-t-t2-c-to-4-dvb-t-c-ip-fta-fejallomas](https://github.com/user-attachments/assets/869b782c-e77b-4485-81ab-3d00005527cc)

## **1. Szükséges eszközök**
- **Antenna:** kültéri antenna (IKUSI FLASH HD)
- **Fejállomás:** LEMCO SCL-824CT 4 × DVB-T & IP (FTA)
- **Set-top box:** MAG IPTV
- **Mérőműszer:** digitális TV jelmérő, IPC TESTER HDMI bemenete használata monitorként
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** jelosztó a fejállomás bemeneteire érkező jelek kialakításához
- **UTP kábelek az IPTV jel továbbításához**
- **Szerelési eszközök:** iránytű

---

## **2. Feladatok és időbeosztás**

### **1. Előkészületek (10 perc)**
- Ellenőrizze az összes szükséges eszközt.
- Biztosítsa a megfelelő munkakörnyezetet.
- **Internetes adatbázisból keressen elérhető multiplexeket a Miskolc, Avasi adótoronyból.** (Frekvencia, teljesítmény, adás típusa)
- Az adótorony adatbázisa elérhető itt: [fmdx.hu](https://www.fmdx.hu/transmitters-hng-avas.htm)

### **2. Antenna felszerelése és beállítása (30 perc)**
- **Válassza ki a megfelelő antennát** kültéri, figyelembe véve az adótorony távolságát és a vételi környezetet.
- **Kültéri antenna esetén:** rögzítse stabil módon a tripod-ra.
- **Az antenna pontos beállítása:**
  - Használja az **iránytűt** az adótorony felé történő pontos irányba állításhoz.
  - Jelszint mérő műszer segítségével végezze el a **finomhangolást**.

### **3. Kábelezés, mérési pontok kialakítása és jel bevezetése a fejállomásba (25 perc)**
- **Antenna és fejállomás összekötése:** Csatlakoztassa a megfelelő koaxiális kábelt és osztót.
- **A Jelosztó beépítése:** Helyezzen be egy célnak megfelelő jelosztót a rendszer és a mérési pont kialakításához.
- **A fejállomás megfelelő bemeneteire ossza el a jelet**, hogy minden ingyenesen fogható multiplex bekerüljön a rendszerbe.
- **A jelet a villamos 3 laborba kell bevinni, hogy az IPTV hálózaton keresztül továbbítható legyen.**

### **4. Fejállomás beállítása és IPTV stream konfigurálása (25 perc)**
- **A fejállomás beállítása:**
  - Minden bemenetre megfelelő multiplex hozzárendelése.
  - A szabadon fogható (FTA) DVB-T jel feldolgozása és IP streamre konvertálása.
- **Multicast IP tartomány megválasztása és konfigurálása** a streamelt IPTV csatornákhoz. (pl: 239.1.1.1)

- **IPTV Set-top-box (MAG 522 IPTV) csatlakoztatása és konfigurálása:**
  - Hálózati kapcsolat létrehozása az eszközök között.
  - Multicast IP címek hozzáadása a csatornalistához.
  - Csatornakeresés indítása és ellenőrzés.

### **5. Jelszintmérés és dokumentáció (30 perc)**
- **Mérések és dokumentáció az antennánál:**
  - Jelszintek és jelminőség
  - Antenna pozíciók és szögek.
  - Multiplex adatok (frekvencia, szimbólumráta, Moduláció)
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

- **Mérések és dokumentáció a fejállomás után (IPTV stream vizsgálata):**
  - Multicast IP címek ellenőrzése
  - IPTV stream stabilitásának vizsgálata
  - Hálózati késleltetés és csomagvesztés vizsgálata
  - Stream adatok rögzítése
  - az eredmények dokumentálása
    
- **A teljes jegyzőkönyv elkészítése és aláírása.**

---

## **3. Értékelési szempontok**

| Feladat | Pontszám |
|---------|----------|
| Eszközök előkészítése | 5 pont |
| Antenna kiválasztása és telepítése | 10 pont |
| Multiplexek kiválasztása internetes adatbázisból | 10 pont |
| Antenna pontos beállítása és jelszintmérés a LEMCO-val | 20 pont |
| Fejállomás konfigurálása, jelosztás beállítása | 15 pont |
| IPTV multicast konfigurálása és stream beállítása | 15 pont |
| Részletes jelszintmérés és dokumentálás | 25 pont |
| **Összesen:** | **100 pont** |

**Sikeres vizsgához minimum 40 pont szükséges.**

