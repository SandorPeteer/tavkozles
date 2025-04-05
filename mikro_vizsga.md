# Távközlési Technikus Vizsgafeladat

## C tétel: Komplex Távközlési Hálózat Tervezése, Telepítése és Mérése

### **Feladat leírása:**    
> A vizsgázó feladata egy nagytávolságú mikrohullámú vezeték nélküli rendszer kiépítése.  

> A internetre csatlakozáshoz nagy nyereségű mobilantenna használata.  

> A hálózati eszközök forgalomirányítása SOHO router segítségével.  

**Időkeret:** 120 perc  

---   

**Eszközök:**  

- **Mikrotik LHG18 LTE antenna** (alapértelmezett IP: `192.168.188.1`)   

<img src="https://github.com/user-attachments/assets/bd348bcc-664c-4348-ab69-c8d4478b8b71" alt="lhg18" style="width:150px;"/>   

- **Mikrotik nRay 60GHz mikrohullámú antenna szett** (eszközök IP-címei: `192.168.88.2` és `192.168.88.3`)   

<img src="https://github.com/user-attachments/assets/2ccd65b7-5b63-4b0b-a1e5-d55c70593576" alt="nray60" style="width:250px;"/>  

- **TP-LINK vagy ASUS SOHO router** (AP módban)

<img src="https://github.com/user-attachments/assets/70ec1eea-8cd0-4c06-9fdf-2e12e8bef59c" alt="asus" style="width:250px;"/>  

- **Laptop vagy PC** a konfigurációkhoz és mérésekhez
- **iperf szoftver** a sávszélesség mérésekhez

**Laptop bejelentkezési adatok:**  
- Felhasználónév: `V3-XX\admin` (XX - az aktuális laptop száma)  
- Jelszó: `mzKvsd`  

---

## 1. Előkészítés és tervezés

### 1.1. Eszközök gyári beállításainak visszaállítása (Factory Reset)

   - Minden eszköz a vizsga előtt gyári alaphelyzetbe állítva.

---

### 1.2. Hálózati topológia

1. **A hálózati diagram**, amely tartalmazza az összes eszközt és azok kapcsolatait.  

![Hálózati Diagram – Távközlési Vizsgafeladat](https://github.com/user-attachments/assets/65ea3fec-c9b5-4812-82ef-f7cc8e3778fb)   

2. **IP-cím kiosztás:**  
   - Mikrotik LHG18 LTE: `192.168.88.1` Mobilinternet + DHCP szerver (`192.168.88.100-250`)
   - Mikrotik nRay 60GHz Master: `192.168.88.2`
   - Mikrotik nRay 60GHz Slave: `192.168.88.3`
   - Router (AP üzemmód)
   - Szerver laptop: `192.168.88.100-250` (DHCP-ből)
   - Kliens laptop: `192.168.88.100-250` (DHCP-ből)

3. **Ügyeljen az IP-ütközések elkerülésére és az alhálózati maszk helyes beállítására /24 (`255.255.255.0`).**

---

## 2. Eszközök telepítése és konfigurálása

### 2.1. Mikrotik LHG18 LTE antenna beállítása
1. **Csatlakoztassa a laptopot a Mikrotik LHG18 LTE-hez** POE Ethernet kábellel + a hozzá való tápegységet!
2. **Állítsa be a laptop IP-címét az antenna konfigurációját figyelembe véve:**  
   - IP: `192.168.188.2`  
   - Alhálózati maszk: `255.255.255.0`  
   - Átjáró (gateway): `192.168.188.1`
3. **Nyisson meg egy böngészőt, vagy a WinBox alkalmazást és lépjen be az LTE antenna konfig felületére:**  
   - Cím: `http://192.168.188.1`  
   - Felhasználónevet és jelszavat állítsa át: `admin`, jelszó: `A1234567`. (Első bejelentkezésnél az antenna hátulján olvasható az alapértelmezett jelszó)
4. **Konfigurálja az LTE kapcsolatot** a szolgáltató által megadott APN beállításokkal + a SIM kártyához tartozó PIN kóddal.
5. **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**
6. **Állítsa be az eszközt**, hogy egy tartományba essen a hálózat többi elemével: pl: `192.168.88.1`  
   - Az LTE antenna legyen DHCP szerver: `192.168.88.100-250`
   - Az UPnP és egyéb szükséges opciók legyenek beállítva, alhálózati maszk: `255.255.255.0`
7. **Mentse a beállításokat**
   - Figyeljen a `laptop IP` címének `automatikusra` visszaállítására
8. **Ellenőrizze a kapcsolat állapotát** és rögzítse a jelerősség paramétereit (**RSRP, RSRQ, SINR, RSSI**).
   - Végezzen **ping tesztet** egy külső szerverhez (`8.8.8.8`), és mérje meg a késleltetést.   
   - Dokumentálja a kapott **nyilvános IP címet** és a hálózati beállításokat.      

---

### 2.2. SOHO router konfigurálása AP módra   

1. Csatlakoztassa a routert a Szerver laptophoz Etherneten keresztül.
2. Nyisson egy parancssort (cmd vagy Terminal).
3. Keresse meg a router IP címét: 
   ```sh
    arp -a 
   ```
4. Nyisson meg egy böngészőt, és érje el a megfelelő IP-címen.  
5. **WiFI és router adminisztrációjához a beállítás legyen:** SSID/felhasználó: `GazdaXX` jelszó: `G1234567`. (XX - egy azonosító szám, pl: Gazda01, Gazda02)   
6. **Kapcsolja AP módba az eszközt** - konfigurálja át.
7. **Csatlakoztassa az LTE antennát a router WAN portjára.**
8. Ha minden sikeres, akkor a Szerver laptop kap DHCP-n keresztül IP címet automatiksan, és internet hozzáférést is az átjárón keresztül.
   
---

### 2.3. Mikrotik nRay 60GHz antennapár beállítása

#### **Master antenna (`192.168.88.2`) konfigurálása:**
1. Csatlakoztassa a Master antennát Ethernet kábellel a router egyik szabad portjára.
2. Nyisson meg egy böngészőt vagy a WinBox alkalmazást és lépjen be az antenna konfig felületére: `http://192.168.88.2`
3. Bejelentkezés (konfiguráláshoz az antenna hátulján olvasható a jelszó):  
   - Először állítsa át az alapértelmezett jelszót: legyen az új jelszó `A1234567`.  
4. **Ellenőrizze az eszközt, hogy "Master" üzemmódban van**. 
   - Ellenőrizze az IP címet és a beállításokat, hogy a Slave antenna képes legyen csatlakozni. 
   - **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**

#### **Slave antenna (`192.168.88.3`) konfigurálása:**  
1. Csatlakoztassa a Slave antennát Ethernet kábellel a Kliens laptop Ethernet portjára.
2. Nyisson meg egy böngészőt vagy a WinBox alkalmazást és lépjen be az antenna konfig felületére: `http://192.168.88.3`
3. **Állítsa be a "Slave" antennát, hogy rálásson a "Master" antennára**   
   - **Figyeljen az aktuális DÁTUM / IDŐ beállítására a konfiguráláskor**
   - Ellenőrizze a kapcsolat minőségét és rögzítse a jelminőségi paramétereket, `WIRELESS 60G STATUS`.
   - Készítsen képernyőképet a kapcsolat aktuális értékeiről.   

---

## 3. Hálózati tesztelés és hibakeresés

### 3.1. Ping teszt végrehajtása

1. Nyisson egy parancssort a Kliens laptopon (cmd vagy Terminal).
2. Pingelje meg a hálózaton lévő eszközöket:

   ```sh
   ping 192.168.88.1
   ping 192.168.88.2
   ping 192.168.88.3
   ping 192.168.88.xxx - DHCP által kiosztott címeket is, amit a Szerver laptop kapott
   stb...
   ```
   Ha hálózati kapcsolat problémák lépnek fel, az alábbiak segíthetnek:

   ```sh
   ipconfig
   ipconfig /all
   ipconfig /release
   ipconfig /renew
   ```
3. **Jegyezze fel a válaszidőket és a sikeres csomagokat.**
4. **Ha probléma van a DHCP szerverrel, érdemes megújítani az IP-ket.**


### 3.2. Sávszélesség mérése (iperf használatával) a mikrohullámú antennák között

1. **Telepítse az iperf szoftvert** a laptopokra.   

   ```sh
   winget install iperf3
   ```
   az [iperf3 letöltése](https://iperf.fr/iperf-download.php) és telepítése után a terminál bezárása, majd ujraindítása szükséges lehet.   

2. A Szerver laptopon futtassa szerverként:

   ```sh
   iperf3 -s
   ```
3. A Kliens végponti eszközön futtassa kliensként:

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
| Eszközök előkészítése               | 10       |
| Eszközök konfigurálása              | 40       |
| Ping és iperf tesztek               | 20       |
| Dokumentáció (képernyőképekkel)     | 20       |
| Összegzés és hibakeresés            | 10       |
| **Összesen:**                       | **100**  |

---

Kérem, hogy a feladat végrehajtása során minden lépést pontosan jegyzőkönyvezzenek!

