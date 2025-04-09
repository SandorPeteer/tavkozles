# Távközlési technikus vizsgafeladat

## D tétel: DVB-T antenna jelének szétosztása majd a fejállomásba küldése és IPTV rendszeren való továbbítása

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése, a szabadon fogható csatornák kiválasztása (Miskolc, Avasi adótorony), a jel elosztásának elvégzése, valamint az IPTV rendszer konfigurálása.  

> Az ingyenesen fogható multiplexek jelerősségének ellenőrzése a **LEMCO SCL-824CT fejállomással**. A fejállomásból a digitális tartalom **IPTV streamként kerül kiadásra**.  

> A Multicast IP tartomány megválasztása és az IPTV Set-top-box konfigurálása a megfelelő vételhez.  

**Időkeret:** 120 perc  

---

![lemco-scl-824ct-8-dvb-s-s2-t-t2-c-to-4-dvb-t-c-ip-fta-fejallomas](https://github.com/user-attachments/assets/869b782c-e77b-4485-81ab-3d00005527cc)

## **1. Szükséges eszközök**
- **Antenna:** kültéri antenna IKUSI FlasHD C48
- **Fejállomás:** LEMCO SCL-824CT
- **Set-top box:** MAG 522
- **Mérőműszer:** IPC TESTER HDMI bemenete használata monitorként
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** legalább 4-es jelosztó a fejállomás bemeneteire érkező jelek kialakításához
- **UTP kábelek:** 2db a konfiguráláshoz és az IPTV jel továbbításához**

---

## **2. Feladatok és időbeosztás**

### **1. Előkészületek (10 perc)**
- Ellenőrizze az összes szükséges eszközt.
- Biztosítsa a megfelelő munkakörnyezetet.
- **Internetes adatbázisból keressen elérhető multiplexeket a Miskolc, Avasi adótoronyból.** (Frekvencia, teljesítmény, adás típusa)
- Az adótorony adatbázisa elérhető itt: [fmdx.hu](https://www.fmdx.hu/transmitters-hng-avas.htm)

### **2. Antenna felszerelése és beállítása (30 perc)**
- **Szerelje fel az antennát** figyelembe véve az adótorony távolságát és a vételi környezetet.
- **Kültéri antenna esetén:** rögzítse azt stabil módon az időjárási viszonyoknak megfelelően.
- **Az antenna irányba állítása:**
  - Használja a [Google](maps.google.com) térképet az adótorony felé történő pontos irányba állításhoz.
  - Jelszint mérő műszer segítségével végezze el a **finomhangolást**.

### **3. Kábelezés, mérési pontok kialakítása és jel bevezetése a fejállomásba (25 perc)**
- **Antenna és fejállomás összekötése:** Csatlakozzon a v3 laborba bemenő megfelelő koax kábelre.
- **A Jelosztó beépítése:** Helyezzen be egy célnak megfelelő jelosztót.
- **A fejállomás megfelelő bemeneteire ossza el a jelet**, hogy minden ingyenesen fogható multiplex bekerüljön a rendszerbe.
- **A TV adások az IPTV hálózaton keresztül továbbítható legyen a set-top-box felé.**

### **4. Fejállomás beállítása és IPTV stream konfigurálása (25 perc)**
- **A fejállomás beállítása:**
  - Minden bemenetre megfelelő multiplex hozzárendelése, és a [LOCK] állapot elérése.
  - A szabadon fogható (FTA) DVB-T csatornák egyenletes elosztása a TS kimeneteken, azokat nem túlterhelve!
- **Multicast IP tartomány megválasztása és konfigurálása** a streamelt IPTV csatornákhoz. (pl: IP: 239.1.1.1 PORT: 1234 UDP)

- **IPTV Set-top-box (MAG 522 IPTV) csatlakoztatása és konfigurálása:**
  - Hálózati kapcsolat létrehozása az eszközök között.
  - Állítsa be manuálisan a set-top-box IP címét úgy, hogy a fejállomás címeivel ne ütközzön.
  - Multicast IP címek hozzáadása a csatornalistához a fejállomással generált M3U lejátszási lista segítségével.
  - Csatornák mentése, indítás és ellenőrzés.

### **5. Jelszintmérés és dokumentáció (30 perc)**
- **Mérések és dokumentáció:**
  - Jelszintek és jelminőség a LEMCO interfészen képernyőképpel dokumentálva,
  - Multiplex adatok (frekvencia, csatorna, sávszélesség, jelerősség, jelminőség)
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

- **Mérések és dokumentáció a fejállomás után (IPTV stream vizsgálata):**
  - A kiosztott multicast IP címek ellenőrzése
  - IPTV stream stabilitásának vizsgálata
  - Hálózati késleltetés és csomagvesztés vizsgálata
  - Stream adatok rögzítése
  - az eredmények dokumentálása
    
- **A teljes jegyzőkönyv elkészítése és aláírása.**

---

## **3. Értékelési szempontok**

| Feladat | Pontszám |
|---------|----------|
| Eszközök előkészítése, ellenőrzése | 5 pont |
| Antenna telepítése | 10 pont |
| Multiplexek kiválasztása internetes adatbázisból | 10 pont |
| Antenna bekötése, jel szétosztása és behangolás a LEMCO fejállomással | 20 pont |
| Fejállomás konfigurálása, TS stream megfelelő kiosztása | 15 pont |
| IPTV multicast konfigurálása és stream beállítása | 15 pont |
| Részletes dokumentáció a beállításokról és a csatorna kiosztásról, valamint a stream vételi ponton történő ellenőrzéséről | 25 pont |
| **Összesen:** | **100 pont** |

**Sikeres vizsgához minimum 40 pont szükséges.**

