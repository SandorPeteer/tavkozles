# Távközlési Technikus Vizsgafeladat

## Komplex Távközlési Hálózat Tervezése, Telepítése és Mérése

**Időtartam:** 2 óra

**Eszközök:**  
- **Mikrotik LHG18 LTE antenna** (alapértelmezett IP: `192.168.188.1`)
- **Mikrotik nRay 60GHz mikrohullámú antenna szett** (eszközök IP-címei: `192.168.88.2` és `192.168.88.3`)
- **D-LINK vagy TP-LINK vagy ASUS SOHO router** (AP módban)
- **HP switch** (opcionálisan felhasználható)
- **Laptop vagy PC** a konfigurációkhoz és mérésekhez
- **iperf szoftver** a sávszélesség mérésekhez

**Laptop bejelentkezési adatok:**  
- Felhasználónév: `V3-XX\admin` (XX - az aktuális laptop száma)  
- Jelszó: `mzKvsd`  

---

## 1. Előkészítés és tervezés

### 1.1. Eszközök gyári beállításainak visszaállítása (Factory Reset)

Minden eszköz gyári alaphelyzetbe állítása szükséges a vizsga kezdetén:

#### **Mikrotik LHG18 LTE antenna resetelése:**
1. Húzza ki az eszközt a tápellátásból.
2. Nyomja meg és tartsa lenyomva a **reset** gombot.
3. Csatlakoztassa vissza a tápellátást, miközben továbbra is nyomva tartja a reset gombot.
4. Tartsa lenyomva a gombot, **amíg a status LED villogni nem kezd** (kb. 5 másodperc).
5. Engedje el a gombot. Az eszköz ekkor visszaáll a gyári beállításokra.

#### **Mikrotik nRay 60GHz antennák resetelése:**
1. Ismételje meg a fent leírt folyamatot mindkét antennán (`192.168.88.2` és `192.168.88.3`).

#### **SOHO router (D-LINK vagy TP-LINK vagy ASUS) resetelése:**
1. Keresse meg a reset gombot az eszközön.
2. Nyomja meg és tartsa lenyomva a gombot kb. **10 másodpercig**, amíg az eszköz újra nem indul.

---

### 1.2. Hálózati topológia tervezése

1. **Rajzoljon egy hálózati diagramot**, amely tartalmazza az összes eszközt és azok kapcsolatait.  
2. **IP-cím kiosztás:**  
   - Mikrotik LHG18 LTE: `192.168.88.1`
   - Mikrotik nRay 60GHz Master: `192.168.88.2`
   - Mikrotik nRay 60GHz Slave: `192.168.88.3`
   - Router (AP mód): `192.168.88.4`
   - Switch (ha szükséges): `192.168.88.254`
   - Kliens laptop: `192.168.88.100-250` (DHCP-ből)

3. **Ügyeljen az IP-ütközések elkerülésére és az alhálózati maszk helyes beállítására (`255.255.255.0`).**  

![Hálózati Diagram – Távközlési Vizsgafeladat](https://github.com/user-attachments/assets/85dce293-ca3b-4569-bed8-d9afd6a08380)   

---

## 2. Eszközök telepítése és konfigurálása

### 2.1. Mikrotik LHG18 LTE antenna beállítása
1. **Csatlakoztassa a laptopot a Mikrotik LHG18 LTE-hez** Ethernet kábellel.
2. **Állítsa be a laptop IP-címét:**  
   - IP: `192.168.188.2`  
   - Alhálózati maszk: `255.255.255.0`  
   - Átjáró (gateway): `192.168.188.1`
3. **Nyisson meg egy böngészőt, vagy a WinBox alkalmazást és lépjen be az LTE antenna konfig felületére:**  
   - Cím: `http://192.168.188.1`  
   - Felhasználónév: `admin`, jelszó: `antennán`.
4. **Konfigurálja az LTE kapcsolatot** a szolgáltató által megadott APN beállításokkal.
5. **Alláítsa be az eszközt**, hogy egy tartományba essen a hálózat többi elemével: pl: `192.168.88.1`  
   - Az antenna legyen a DHCP szerver: `192.168.88.100-250`
   - A NAT és egyéb szükséges opciók legyenek beállítva, alhálózati maszk: `255.255.255.0`
6. **Mentse a beállításokat**
7. **Ellenőrizze a kapcsolat állapotát** és rögzítse a jelerősség paramétereit (RSRP, RSRQ, SINR, RSSI).
   - Végezzen **ping tesztet** egy külső szerverhez (`8.8.8.8`), és mérje meg a késleltetést.   
   - Dokumentálja a kapott **nyilvános IP címet** és a hálózati beállításokat.      

---

### 2.2. Mikrotik nRay 60GHz antennapár beállítása

#### **Master antenna (`192.168.88.2`) konfigurálása:**
1. Csatlakozzon az eszközhöz Ethernet kábellel.
2. Nyisson meg egy böngészőt vagy a WinBox alkalmazást és írja be: `http://192.168.88.2`
3. Bejelentkezés:  
   - Felhasználónév: `admin`, jelszó `antennán`.  
4. **Állítsa be az eszközt "Master" módban**.  
   - Állítsa be a pont-pont kapcsolatot a két eszköz között.
   - Ellenőrizze a kapcsolat minőségét és rögzítse a jelminőségi paramétereket.

#### **Slave antenna (`192.168.88.3`) konfigurálása:**  
1. Ismételje meg a fenti lépéseket a `192.168.88.3` IP-n.  
2. **Állítsa be az eszközt "Slave" módban**, és csatlakozzon a Master antennához.   
   - Ellenőrizze a kapcsolat minőségét és rögzítse a jelminőségi paramétereket.
   - Készítsen képernyőképet a kapcsolat **Throughput (Mbps)** értékéről.   

---

### 2.3. SOHO router beállítása AP módban   

1. Csatlakoztassa a routert a laptophoz Etherneten keresztül.  
2. Nyisson meg egy böngészőt, és érje el a megfelelő IP-címen.  
3. **WiFI beállítása** SSID: `GazdaXX` jelszó: `G1234567`. (XX - egy azonosító szám, pl: Gazda01, Gazda02)   
4. **Kapcsolja AP módba az eszközt** és konfigurálja át a `192.168.88.xxx` tartományba, hogy ne ütközzön másik eszközzel.    
5. **Engedélyezze a DHCP szervert**, tartomány: `192.168.88.100-150`.   

---

## 3. Hálózati tesztelés és hibakeresés

### 3.1. Ping teszt végrehajtása

1. Nyisson egy parancssort (cmd vagy Terminal).
2. Pingelje meg a hálózaton lévő eszközöket:
   ```sh
   ping 192.168.88.1
   ping 192.168.88.2
   ping 192.168.88.3
   stb...
   ```
3. **Jegyezze fel a válaszidőket és a sikeres csomagokat.**

### 3.2. Sávszélesség mérése (iperf használata)

1. **Telepítse az iperf szoftvert** a kliens laptopra.   
   iperf3[Download](https://iperf.fr/iperf-download.php)
2. Az egyik eszközön futtassa szerverként:
   ```sh
   iperf3 -s
   ```
3. A másik eszközön futtassa kliensként:
   ```sh
   iperf3 -c 192.168.88.xxx (xxx - tesztelő eszköz IP címe)
   ```
4. **Rögzítse az eredményeket (Mbps értékek).**

---

## 4. Dokumentáció és értékelés

**Hálózati forgalom monitorozása és hibakeresés:**
   - Használja az **iperf** szoftvert a sávszélesség mérésére a hálózat különböző pontjai között, és rögzítse az eredményeket.
   - Végezzen ping és traceroute teszteket a hálózati kapcsolatok ellenőrzésére.
   - Azonosítson és hárítson el esetleges hálózati hibákat.

**Dokumentáció és prezentáció:**
   - Készítsen részletes dokumentációt, amely tartalmazza:
     - A hálózati topológiát és az eszközök IP-címeit.
     - Az eszközök konfigurációs lépéseit és beállításait.
     - A mérési eredményeket és azok elemzését.
     - A hálózati biztonsági beállításokat.
     - Az esetleges hibák és azok elhárításának leírását.
   - Prezentálja a projektet, kiemelve a megvalósítás lépéseit és a tapasztalatokat.


| Részfeladat                         | Pontszám |
|-------------------------------------|----------|
| Eszközök resetelése és előkészítése | 10       |
| Eszközök konfigurálása              | 40       |
| Ping és iperf tesztek               | 20       |
| Dokumentáció (képernyőképekkel)      | 20       |
| Összegzés és hibakeresés             | 10       |
| **Összesen:**                       | **100**  |

---

Kérem, hogy a feladat végrehajtása során minden lépést pontosan jegyzőkönyvezzenek!

