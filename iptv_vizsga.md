# Távközlési technikus vizsgafeladat

## **B tétel:** DVB-T jel fejállomásba küldése és IPTV rendszeren való kiadása

### **Feladat leírása:**    
> A vizsgázó feladata egy földfelszíni digitális TV vételi rendszer kiépítése, a megfelelő adótorony (Miskolc, Avasi adótorony) kiválasztása, a jel mérésének és elosztásának elvégzése, valamint az IPTV rendszer konfigurálása.  

> A fogható multiplexek jelerősségének ellenőrzése, és a DVB-T jel **LEMCO SCL-824CT fejállomásba** történő bevezetése. A fejállomásból a digitális tartalom **IPTV streamként kerül kiadásra**.  

> A Multicast IP tartomány megválasztása és az IPTV Set-top-box konfigurálása a megfelelő vételhez.  

**Időkeret:** 120 perc  

---

## **1. Szükséges eszközök**
- **Antenna:** Beltéri vagy kültéri antenna (a vizsgázó választása alapján)
- **Fejállomás:** LEMCO SCL-824CT 8 × DVB-S/S2/T/T2/C to 4 × DVB-T/C & IP (FTA)
- **Set-top box:** MAG IPTV
- **Hálózati elosztó:** pl: hp switch, vagy router
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
- **IPTV Set-top-box (MAG IPTV) csatlakoztatása és konfigurálása:**
  - Hálózati kapcsolat beállítása.
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

- Mérési eredmények rögzítése a jegyzőkönyvben:
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

# **IPTV Multicast Mérések és Hibakeresés – Parancssoros Segédlet**

Ez a dokumentum segít az IPTV multicast stream mérések és hibakeresés parancssoros elvégzésében.

---

## **1. Multicast IP címek ellenőrzése**

📌 **VLC használata a stream tesztelésére**  
```sh
vlc -vvv udp://@239.1.1.1:1234 --sout="#display"
```
- **`-vvv`** → Részletes logolás engedélyezése  
- **`udp://@239.1.1.1:1234`** → IPTV multicast IP és port megadása  
- **`--sout="#display"`** → A stream megjelenítése  

📌 **Csak információk kiírása (videó nélkül)**
```sh
vlc -vvv udp://@239.1.1.1:1234 --intf dummy
```

📌 **Logfájlba mentés**
```sh
vlc -vvv udp://@239.1.1.1:1234 --sout="#display" > vlc_log.txt 2>&1
```

---

## **2. IPTV stream stabilitásának mérése**

📌 **FFmpeg segítségével IPTV stream vizsgálata**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -f null -
```
- Kiírja a stream formátumát, bitrátáját, késleltetést és csomagvesztést.  

📌 **IPTV stream mentése fájlba**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -c copy output.ts
```
- A streamet veszteségmentesen menti el `output.ts` fájlba.

📌 **IPTV stream csomagvesztés elemzés**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -loglevel debug -f null -
```
- Részletes hibajelentést ír ki a hálózati problémákról, csomagvesztésről.

---

## **3. Hálózati késleltetés és csomagvesztés vizsgálata**

📌 **Ping teszt IPTV szerverre**  
```sh
ping 239.1.1.1
```
- Ha magas a válaszidő (ms) vagy csomagvesztés tapasztalható, az hálózati problémára utalhat.

📌 **Traceroute vizsgálat (útvonal ellenőrzése)**  
**Windows**  
```sh
tracert 239.1.1.1
```
**Linux/macOS**  
```sh
traceroute 239.1.1.1
```
- Figyelje, hogy a csomagok merre haladnak, és hol van esetleges késleltetés.

📌 **Wireshark CLI verzió (TShark)**
```sh
tshark -i eth0 -Y "ip.dst == 239.1.1.1"
```
- Csak az IPTV multicast csomagokat mutatja meg.

---

## **4. Stream adatok rögzítése és hálózati forgalom figyelése**

📌 **Wireshark csomagrögzítés**
```sh
tshark -i eth0 -w iptv_stream.pcap
```
- Az `iptv_stream.pcap` fájlba menti az IPTV forgalmat.

📌 **FFmpeg segítségével IPTV stream rögzítése**  
```sh
ffmpeg -i "udp://@239.1.1.1:1234" -c copy output.ts
```
- Az `output.ts` fájlba menti a streamet.

---

## **5. IPTV stream tesztelése és csomagvesztés mérése (iPerf)**

📌 **Multicast forgalom vizsgálata**
```sh
iperf -c 239.1.1.1 -u -p 1234 -b 10M
```
- Elküld **10 Mbps adatot** a multicast címre, és méri a csomagvesztést.

📌 **iPerf szerver mód multicast vizsgálatra**
```sh
iperf -s -u
```
- Indít egy UDP szervert, amely figyeli a multicast adatokat.

---

A winget csomagkezelővel egyszerűen telepíthető a VLC, iperf3 és Wireshark (TShark) Windows rendszeren.

VLC és TShark telepítése winget segítségével

📌 VLC telepítése

winget install -e --id VideoLAN.VLC

	•	-e → Exact match (pontos egyezés az alkalmazás ID-jával)
	•	--id VideoLAN.VLC → A VLC hivatalos ID-je wingetben

📌 Wireshark (TShark) telepítése

winget install -e --id WiresharkFoundation.Wireshark

	•	A telepítés után a tshark parancs parancssorból közvetlenül elérhető lesz.

📌 Ellenőrzés, hogy telepítve vannak-e

winget list | findstr "VLC Wireshark"

Ha a listában megjelenik a VLC és a Wireshark, akkor sikeresen telepítve vannak.

Alternatív módszer: winget keresés

📌 Keresés a winget csomagok között

winget search VLC
winget search Wireshark

Ez megmutatja a pontos ID-t és verziót, amit telepíteni lehet.

🚀 Ezzel egyszerűen telepítheted VLC-t és TShark-ot Windows rendszeren winget segítségével!

---

## **Összegzés**

| Mérési feladat | Parancssoros eszköz |
|---------------|---------------------|
| **Multicast IP címek ellenőrzése** | VLC, tcpdump, tshark |
| **IPTV stream stabilitásának mérése** | FFmpeg, VLC |
| **Hálózati késleltetés és csomagvesztés vizsgálata** | iPerf, tshark |
| **Stream adatok rögzítése** | FFmpeg, Wireshark |

🚀 **Ezekkel a parancsokkal a vizsgázók teljes IPTV mérést és hibakeresést végezhetnek parancssorból!**   

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

