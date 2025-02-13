# Távközlési Technikus Vizsgafeladat

## Komplex Távközlési Hálózat Tervezése, Telepítése és Mérése

**Időtartam:** 2 óra

**Eszközök:**  


- **Mikrotik LHG18 LTE antenna** (alapértelmezett IP: `192.168.188.1`)   

<img src="https://github.com/user-attachments/assets/bd348bcc-664c-4348-ab69-c8d4478b8b71" alt="lhg18" style="width:150px;"/>   

- **Mikrotik nRay 60GHz mikrohullámú antenna szett** (eszközök IP-címei: `192.168.88.2` és `192.168.88.3`)   

<img src="https://github.com/user-attachments/assets/2ccd65b7-5b63-4b0b-a1e5-d55c70593576" alt="nray60" style="width:250px;"/>  

- **D-LINK vagy TP-LINK vagy ASUS SOHO router** (AP módban)

<img src="https://github.com/user-attachments/assets/70ec1eea-8cd0-4c06-9fdf-2e12e8bef59c" alt="asus" style="width:250px;"/>  

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
4. **Tartsa lenyomva a gombot, amíg a status LED villogni nem kezd** (kb. 5 másodperc).
5. Engedje el a gombot. Az eszköz ekkor visszaáll a gyári beállításokra.

#### **Mikrotik nRay 60GHz antennák resetelése:**
1. Ismételje meg a fent leírt folyamatot mindkét antennán (`192.168.88.2` és `192.168.88.3`).

#### **SOHO router (D-LINK vagy TP-LINK vagy ASUS) resetelése:**
1. Keresse meg a reset gombot (Asus router esetében WPS nyomógomb) az eszközön
2. Áramtalanítás!
3. Egy kis várakozási idő után nyomja be a reset gombot,
4. Kapcsolja vissza az eszközt és tartsa lenyomva kb. **10 másodpercig**, amíg a gyári visszaállítás folyamata lezajlik.

---

### 1.2. Hálózati topológia tervezése

1. **Rajzoljon egy hálózati diagramot**, amely tartalmazza az összes eszközt és azok kapcsolatait.  
   - [Draw.io használata a rajzhoz](https://draw.io)
2. **IP-cím kiosztás:**  
   - Mikrotik LHG18 LTE: `192.168.88.1`
   - Mikrotik nRay 60GHz Master: `192.168.88.2`
   - Mikrotik nRay 60GHz Slave: `192.168.88.3`
   - Router (AP mód): `192.168.88.4`
   - Switch (ha szükséges): `192.168.88.254`
   - Kliens laptop: `192.168.88.100-250` (DHCP-ből)

3. **Ügyeljen az IP-ütközések elkerülésére és az alhálózati maszk helyes beállítására (`255.255.255.0`).**

![Hálózati Diagram – Távközlési Vizsgafeladat](https://github.com/user-attachments/assets/65ea3fec-c9b5-4812-82ef-f7cc8e3778fb)

---

## 2. Eszközök telepítése és konfigurálása

### 2.1. Mikrotik LHG18 LTE antenna beállítása
1. **Csatlakoztassa a laptopot a Mikrotik LHG18 LTE-hez** Ethernet kábellel.
2. **Állítsa be a laptop IP-címét az antenna konfigurációját figyelembe véve:**  
   - IP: `192.168.188.2`  
   - Alhálózati maszk: `255.255.255.0`  
   - Átjáró (gateway): `192.168.188.1`
3. **Nyisson meg egy böngészőt, vagy a WinBox alkalmazást és lépjen be az LTE antenna konfig felületére:**  
   - Cím: `http://192.168.188.1`  
   - Felhasználónév: `admin`, jelszó: `A1234567`. (Első bejelentkezésnél az antenna hátulján olvasható a default jelszó)
4. **Konfigurálja az LTE kapcsolatot** a szolgáltató által megadott APN beállításokkal.
5. **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**
6. **Állítsa be az eszközt**, hogy egy tartományba essen a hálózat többi elemével: pl: `192.168.88.1`  
   - Az antenna legyen a DHCP szerver: `192.168.88.100-250`
   - A NAT és egyéb szükséges opciók legyenek beállítva, alhálózati maszk: `255.255.255.0`
7. **Mentse a beállításokat**
   - Figyeljen a `laptop IP` címének `automatikusra` visszaállítására
8. **Ellenőrizze a kapcsolat állapotát** és rögzítse a jelerősség paramétereit (**RSRP, RSRQ, SINR, RSSI**).
   - Végezzen **ping tesztet** egy külső szerverhez (`8.8.8.8`), és mérje meg a késleltetést.   
   - Dokumentálja a kapott **nyilvános IP címet** és a hálózati beállításokat.      

---

### 2.2. Mikrotik nRay 60GHz antennapár beállítása

#### **Master antenna (`192.168.88.2`) konfigurálása:**
1. Csatlakozzon az eszközhöz Ethernet kábellel.
2. Nyisson meg egy böngészőt vagy a WinBox alkalmazást és írja be: `http://192.168.88.2`
3. Bejelentkezés (konfiguráláshoz az antenna hátulján olvasható a jelszó):  
   - Felhasználónév: `admin`, jelszó `A1234567`.  
4. **Állítsa be az eszközt "Master" módban**. 
   - Ellenőrizze az IP címet és a beállításokat, hogy a Slave antenna képes legyen csatlakozni. 
   - **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**

#### **Slave antenna (`192.168.88.3`) konfigurálása:**  
1. Ismételje meg a fenti lépéseket a `192.168.88.3` IP-n.  
2. **Állítsa be az eszközt "Slave" módban**, és csatlakozzon a Master antennához.   
   - **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**
   - Ellenőrizze a kapcsolat minőségét és rögzítse a jelminőségi paramétereket, `WIRELESS 60G STATUS`.
   - Készítsen képernyőképet a kapcsolat aktuális értékeiről.   

---

### 2.3. SOHO router beállítása AP módban   

1. Csatlakoztassa a routert a laptophoz Etherneten keresztül.
2. Nyisson egy parancssort (cmd vagy Terminal).
3. Keresse meg a router IP címét: 
   ```sh
    arp -a 
   ```
4. Nyisson meg egy böngészőt, és érje el a megfelelő IP-címen.  
5. **WiFI és router adminisztrációjához a beállítás** SSID/felhasználó: `GazdaXX` jelszó: `G1234567`. (XX - egy azonosító szám, pl: Gazda01, Gazda02)   
6. **Kapcsolja AP módba az eszközt** és konfigurálja át manuálisan a `192.168.88.xxx` tartományba, hogy ne ütközzön másik eszközzel.    
7. **Figyeljen az átjáróra, és a többi opcionális beállításra.**   

---

## 3. Hálózati tesztelés és hibakeresés

### 3.1. Ping teszt végrehajtása

1. Nyisson egy parancssort (cmd vagy Terminal).
2. Pingelje meg a hálózaton lévő eszközöket:

   ```sh
   ping 192.168.88.1
   ping 192.168.88.2
   ping 192.168.88.3
   ping 192.168.88.4
   stb...
   ```
   Ha hálózati kapcsolat problémák lépnek fel:

   ```sh
   ipconfig
   ipconfig /all
   ipconfig /release
   ipconfig /renew
   ```
3. **Jegyezze fel a válaszidőket és a sikeres csomagokat.**
4. **Ha probléma van a DHCP szerverrel, érdemes megújítani az IP-ket.**


### 3.2. Sávszélesség mérése (iperf használata)

1. **Telepítse az iperf szoftvert** a laptopokra.   

   ```sh
   winget install iperf3
   ```
   az [iperf3 letöltése](https://iperf.fr/iperf-download.php) és telepítése után a terminál bezárása, majd ujraindítása szükséges lehet.   

2. Az egyik laptopon futtassa szerverként:

   ```sh
   iperf3 -s
   ```
3. A másik végponti eszközön futtassa kliensként:

   ```sh
   iperf3 -c 192.168.88.xxx (xxx - tesztelő eszköz IP címe)
   ```
   Ha a teszt nem indulna el, a `Windows hálózati felderítést be kell kapcsolni`:

   ```sh
   netsh advfirewall firewall set rule group="Network Discovery" new enable=Yes
   ```
   A tűzfalon engedélyezni kell az alkalmazást!  

4. **Rögzítse az eredményeket (Mbps értékek), tesztelje az internet elérést és futtasson speedtest-et.**

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

