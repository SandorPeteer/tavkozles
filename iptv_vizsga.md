# Távközlési technikus vizsgafeladat

## **B tétel:** DVB-T jel fejállomásba küldése és IPTV rendszeren való kiadása

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése, a megfelelő adótorony (Miskolc, Avasi adótorony) kiválasztása, a jel mérésének és elosztásának elvégzése, valamint az IPTV rendszer konfigurálása.  

> A fogható multiplexek jelerősségének ellenőrzése, és a DVB-T jel **LEMCO SCL-824CT fejállomásba** történő bevezetése. A fejállomásból a digitális tartalom **IPTV streamként kerül kiadásra**.  

> A Multicast IP tartomány megválasztása és az IPTV Set-top-box konfigurálása a megfelelő vételhez.  

**Időkeret:** 120 perc  

---

![lemco-scl-824ct-8-dvb-s-s2-t-t2-c-to-4-dvb-t-c-ip-fta-fejallomas](https://github.com/user-attachments/assets/869b782c-e77b-4485-81ab-3d00005527cc)

## **1. Szükséges eszközök**
- **Antenna:** Beltéri vagy kültéri antenna (a vizsgázó választása alapján)
- **Fejállomás:** LEMCO SCL-824CT 8 × DVB-S/S2/T/T2/C to 4 × DVB-T/C & IP (FTA)
- **Set-top box:** MAG IPTV
- **Hálózati eszköz:** IGMP protokollt támogató és DHCP képes router internet kapcsolattal
- **Mérőműszer:** METEK HDD digitális TV jelmérő
- **Koaxiális kábelek és csatlakozók (már előkészítve egy másik vizsgafeladat során)**
- **Jelosztó:** jelosztó a fejállomás bemeneteire érkező jelek kialakításához
- **UTP kábelek az IPTV jel továbbításához**
- **Szerelési eszközök:** csavarhúzó, villáskulcs, kábelvágó, iránytű, dőlésszögmérő

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
  - Használja az **iránytűt és dőlésszögmérőt** az adótorony felé történő pontos irányba állításhoz.
  - METEK HDD mérőműszer segítségével végezze el a **finomhangolást**.

### **3. Kábelezés, mérési pontok kialakítása és jel bevezetése a fejállomásba (25 perc)**
- **Antenna és fejállomás összekötése:** Csatlakoztassa a megfelelő koaxiális kábelt és osztót.
- **A Jelosztó beépítése:** Helyezzen be egy célnak megfelelő jelosztót a rendszer és a mérési pont kialakításához.
- **A fejállomás megfelelő bemeneteire ossza el a jelet**, hogy minden fogható multiplex bekerüljön a rendszerbe.
- **A jelet a villamos 3 laborba kell bevinni, hogy az IPTV hálózaton keresztül továbbítható legyen.**

### **4. Fejállomás beállítása és IPTV stream konfigurálása (25 perc)**
- **A fejállomás beállítása:**
  - Minden bemenetre megfelelő multiplex hozzárendelése.
  - A szabadon fogható (FTA) DVB-T jel feldolgozása és IP streamre konvertálása.
- **Multicast IP tartomány megválasztása és konfigurálása** a streamelt IPTV csatornákhoz.
- **IPTV Set-top-box (MAG IPTV) csatlakoztatása és router konfigurálása:**
  - DHCP szerver, internet, IGMP konfigurálása a routeren 
  - Hálózati kapcsolat létrehozása az eszközök között.
  - Multicast IP címek hozzáadása a csatornalistához.
  - Csatornakeresés indítása és ellenőrzés.

### **5. Jelszintmérés és dokumentáció (30 perc)**
- **Mérések és dokumentáció az antennánál:**
  - Spektrum analizátor képe
  - Jelszintek és jelminőség
  - Antenna pozíciók és szögek.
  - Polarizáció
  - Multiplex adatok (frekvencia, szimbólumráta, FEC)
  - Időjárási körülmények (hőmérséklet, szélsebesség, egyéb megjegyzések)

- **Mérések és dokumentáció a fejállomás után (IPTV stream vizsgálata):**
  - Multicast IP címek ellenőrzése
  - IPTV stream stabilitásának mérése
  - Hálózati késleltetés és csomagvesztés vizsgálata
  - Stream adatok rögzítése
  - az eredmények dokumentálása

- DVB-T/T2 Mérési eredmények rögzítése a jegyzőkönyvben:
  - **Jelerősség (dBμV)**
  - **Jel-zaj viszony (SNR - dB)**
  - **Bit Error Rate (BER)**
  - **Modulation Error Ratio (MER - dB)**
  - **Csillapítás (dB) az osztó után / előtte**
  - **Lock állapot:** [ ] Igen [ ] Nem
  - **Hőmérséklet és időjárási körülmények**
  - **Multiplex adatok és frekvenciák**
    
- **A teljes jegyzőkönyv elkészítése és aláírása.**

---

# **Winget csomagkezelő használata IPTV vizsgálati eszközök telepítésére**

Ez a dokumentum segít a szükséges IPTV vizsgálati eszközök **Windows rendszerre való telepítésében** a **winget** csomagkezelő segítségével.

---

## **1. VLC és WireShark telepítése**

📌 **VLC telepítése**  
```sh
winget install -e --id VideoLAN.VLC
```
- **`-e`** → Exact match (pontos egyezés az alkalmazás ID-jával)  
- **`--id VideoLAN.VLC`** → A VLC hivatalos ID-je wingetben  

📌 **Wireshark telepítése**  
```sh
winget install -e --id WiresharkFoundation.Wireshark
```
- A telepítés után a `Wireshark` a programok között feltelepítve megtalálható.

---

## **2. FFmpeg telepítése IPTV stream elemzéshez**

📌 **FFmpeg telepítése**  
```sh
winget install -e --id Gyan.FFmpeg
```
- Ez a **legfrissebb FFmpeg verziót** telepíti.
- A telepítések után a parancssort újra kell nyitni! 

📌 **Ellenőrzés, hogy az FFmpeg elérhető-e**  
```sh
ffmpeg -version
```
Ha az FFmpeg verziószáma megjelenik, akkor sikeresen települt.

---

## **3. Multicast forgalom és hálózati késleltetés vizsgálata**

📌 **Wireshark UDP stream vizsgálatához**
  - Az NCAP telepítése még szükséges
  - A programban az `UDP stream` opció mutatja az összes IPTV forgalmat.

---

## **4. IPTV stream elemzése**

📌 **FFmpeg segítségével IPTV stream elemzése**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -f null -
```
- Kiírja a stream formátumát, bitrátáját, késleltetést és csomagvesztést.

📌 **FFmpeg segítségével IPTV stream csomagvesztés vizsgálata**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -loglevel debug -f null -
```
- Részletes hibajelentést ír ki a hálózati problémákról, csomagvesztésről.

---

## **5. Ellenőrzés, hogy az összes szükséges IPTV műsor elérhető**  

📌 **FFplay segítségével az IPTV egyik csatornájának vizsgálata**  
```sh
ffplay -i udp://@239.1.1.1:1234 -sn
```

📌 **VLC segítségével is nézhető az IPTV stream és az adatfolyam vizsgálható**  
```sh
vlc udp://@239.1.1.1:10001
```


---

## **Összegzés**

| Telepítendő eszköz | Winget ID | Felhasználási cél |
|----------------|----------------------------|---------------------------------|
| **VLC** | `VideoLAN.VLC` | IPTV stream lejátszása és tesztelése |
| **Wireshark (TShark)** | `WiresharkFoundation.Wireshark` | Multicast csomagok figyelése |
| **FFmpeg** | `Gyan.FFmpeg` | IPTV stream elemzése és rögzítése |

🚀 **Ezekkel a parancsokkal a vizsgázók minden szükséges IPTV mérést és hibakeresést el tudnak végezni.**


---   

## **3. Értékelési szempontok**

| Feladat | Pontszám |
|---------|----------|
| Eszközök előkészítése | 5 pont |
| Antenna kiválasztása és telepítése | 10 pont |
| Multiplexek kiválasztása internetes adatbázisból | 10 pont |
| Antenna pontos beállítása és jelszintmérés METEK HDD-vel | 20 pont |
| Fejállomás konfigurálása, jelosztás beállítása | 15 pont |
| IPTV multicast konfigurálása és stream beállítása | 15 pont |
| Részletes jelszintmérés és dokumentálás | 25 pont |
| **Összesen:** | **100 pont** |

**Sikeres vizsgához minimum 40 pont szükséges.**

