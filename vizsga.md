A Távközlési Technikus 2023.11.21. KKK dokumentum szerint az **I. Távközlési alapmérések** során a vizsgázónak **tételhúzással** kell kiválasztania egy feladatot az alábbi három kategóriából:

1. Elektronikai alapfeladat:   
	•	Alapelemekből épít egy egyszerű áramkört.   
	•	Mérések elvégzése (feszültség, áramerősség, ellenállás mérése).   
	•	Az elektronika alapvető törvényeinek igazolása (pl. Ohm-törvény).

3. Elektronikai összetett kapcsolások:   
	•	Komplexebb áramkörök beüzemelése (pl. erősítők, műveleti erősítők, digitális kombinációs hálózatok).  
	•	A kapcsolás helyes működésének igazolása mérésekkel.  

4. Távközlési alapfeladat:  
	•	Távközlési berendezések beüzemelése.  
	•	Modulációs és multiplexált jelek mérése.  

Vizsgáztatás módja:  
	•	Tételhúzás: A tanuló egy feladatot húz a három közül, és csak azt kell teljesítenie.  
	•	Eszközigény: Minden tanulónak külön mérőállomás szükséges, mivel mindenki saját tételt old meg.  
	•	Mérési eredmények rögzítése: A mérési eredményeket a vizsgázónak elektronikus jegyzőkönyvben kell rögzítenie.  
 
# Elektronikai alapfeladatok Tételei:

Az alábbi tételek az elektronikai alapméréseket, az alapelemekből épített áramkörök méréstechnikai vizsgálatát tartalmazzák. A feladatokat minden tanulónak egyéni eszközkészlettel kell végrehajtania, az eredményeket mérési jegyzőkönyvben kell dokumentálni.

---

## **Elektro 1A: T-ellenállás hálózat építése és mérése**
**Feladat:**
- Építsen meg egy **T ellenállás hálózatot** breadboardon.  
- Használja az **NI MyDAQ mérőadatgyűjtő modult** a mérésekhez.  
- Mérje meg a **csillapítást** terheletlen állapotban.  
- Határozza meg a **bemeneti és kimeneti impedanciát**.  
- Ismételje meg a méréseket **illesztett terheléssel**, és hasonlítsa össze az eredményeket.  

**Elvárások:**
- Az áramkör szakszerű megépítése breadboardon.  
- Pontos mérések végrehajtása.  
- Mérési jegyzőkönyv készítése:  
   - Kapcsolási rajz.  
   - Mérési adatok rögzítése.  
   - Bemeneti és kimeneti impedancia számítása.  

**Időkeret:** 60 perc  

---

## **Elektro 1B: RC aluláteresztő szűrő építése és mérése**
**Feladat:**
- Építsen meg egy **RC aluláteresztő szűrőt** breadboardon.  
- Használja az **NI MyDAQ adatgyűjtőt** a vizsgálatokhoz.  
- Változtassa a bemeneti frekvenciát, és mérje meg a **kimeneti feszültséget** különböző frekvenciákon.  
- Határozza meg a **-3 dB-es vágási frekvenciát**.  
- Ábrázolja a **frekvenciamenetet (Bode-diagram)** a mért adatok alapján.  

**Elvárások:**
- Szakszerű áramkörszerelés.  
- Az RC szűrő helyes működésének igazolása mérésekkel.  
- Jegyzőkönyv készítése, amely tartalmazza:  
   - Kapcsolási rajz.  
   - Mérési eredmények.  
   - Frekvenciamenet kiértékelése.  

**Időkeret:** 60 perc  

---

## **Elektro 1C: Párhuzamos RLC rezgőkör rezonanciafrekvenciájának meghatározása**
**Feladat:**
- Építsen meg egy **párhuzamos RLC rezgőkört** breadboardon.  
- Használjon **100 nF kapacitású kondenzátort**.  
- Számítsa ki a rezonanciafrekvenciát (**L = 100 mH**).  
- Határozza meg a **rezonanciafrekvenciát** a mért adatok alapján.  
- Ábrázolja a **frekvenciamenetet (Bode-diagram)** a mért adatok alapján.  

**Elvárások:**
- Az NI MyDAQ adatgyűjtő szakszerű alkalmazása.  
- Mérési eredmények rögzítése:  
   - Frekvenciamenet.  
   - Maximális erősítés frekvenciájának azonosítása.  
   - Rezonanciafrekvencia számítása.  

**Időkeret:** 60 perc  

---

## **Közös követelmények mindhárom tételnél:**
- Az NI MyDAQ adatgyűjtő és breadboard kötelező használata.  
- Minden mérési adat jegyzőkönyvben történő rögzítése.  
- Kapcsolási rajz és számítások mellékelése.  
- Az eredmények szakszerű dokumentálása.  

---


  
# Elektronikai összetett kapcsolások (60 perc)

Az alábbi három tétel komplexebb áramkörök beüzemelését, méréstechnikai vizsgálatát és dokumentálását tartalmazza, a rendelkezésre álló alkatrészekhez igazítva.

---

## **Elektro 2A: TL072 műveleti erősítős feszültségerősítő áramkör építése és mérése**
**Feladat:**
- Építsen meg egy **nem invertáló műveleti erősítős feszültségerősítő** áramkört a TL072 IC felhasználásával.  
- Alkalmazandó alkatrészek:  
   - Bemeneti ellenállás: $$(R_1 = 10 k\Omega)$$  
   - Visszacsatoló ellenállás: $$(R_2 = 100 k\Omega)$$  
- Határozza meg az erősítést:  
   $$[A_v = 1 + \frac{R_2}{R_1}]$$  
- Mérje meg a kimeneti feszültséget különböző bemeneti amplitúdók és frekvenciák mellett.

**Mérési feladatok:**
- Feszültségerősítés mérése különböző bemeneti amplitúdóknál.  
- Frekvenciamenet mérése 10 Hz – 10 kHz között.  
- Fáziseltolódás vizsgálata oszcilloszkóppal.  

**Elvárások:**
- Az áramkör szakszerű felépítése.  
- Mérési eredmények helyes dokumentálása.  

**Időkeret:** 60 perc  

---

## **Elektro 2B: Digitális kombinációs hálózat építése logikai kapukból**
**Feladat:**
- Építsen meg egy **három bemenetű kombinációs logikai hálózatot** a rendelkezésre álló logikai kapukból.  
- Alkalmazandó logikai kapuk: **AND, OR, NOT**.  
- A logikai függvény:  
   $$[Y = (A \cdot B) + (\neg C)]$$  
- Mérje meg a logikai kimenetet minden bemeneti kombinációra.  

**Mérési feladatok:**
- Igazságtábla felállítása és kitöltése.  
- Logikai szintek mérése (LOW/HIGH).  
- Kapu késleltetés mérése (ha a mérőeszköz lehetővé teszi).  

**Elvárások:**
- Az áramkör helyes működésének igazolása igazságtábla alapján.  
- Mérési jegyzőkönyv készítése.  

**Időkeret:** 60 perc  

---

## **Elektro 2C: NE555 alapú PWM vezérlő LED fényerőszabályzáshoz**
**Feladat:**
- Építsen meg egy **PWM alapú fényerőszabályzó áramkört** az **NE555 időzítő IC** felhasználásával.  
- Az áramkör astabil multivibrátorként működjön, amely szabályozza a LED fényerejét.  
- **Alkalmazandó alkatrészek:**  
   - **R1:** 4.7 kΩ  
   - **R2:** 10 kΩ potméter (a kitöltési tényező szabályzásához)  
   - **C:** 10 µF  
- Mérje meg a kimeneti PWM jel frekvenciáját és kitöltési tényezőjét.

**Mérési feladatok:**
- Kimeneti feszültséghullámforma mérése oszcilloszkóppal.  
- Frekvencia és kitöltési tényező mérése.  
- LED fényerő változásának megfigyelése.  

**Elvárások:**
- Az áramkör helyes működésének igazolása.  
- Mérési jegyzőkönyv készítése.  

**Időkeret:** 60 perc  

---

## **Közös követelmények mindhárom tételnél:**
- **Mérési eszközök:**  
   - NI MyDAQ adatgyűjtő.  
   - Multiméter, oszcilloszkóp.  
- **Alkatrészek:**  
   - TL072 műveleti erősítő.  
   - NE555 időzítő IC.  
   - Logikai kapuk (AND, OR, NOT).  
   - Ellenállások, kondenzátorok, LED-ek, potenciométerek.  
- **Dokumentáció:**  
   - Kapcsolási rajz.  
   - Mérési adatok táblázatban.  
   - Grafikonok a mérésekhez.  

## **Eszközigény termenként (9 tanulóhoz):**
- 6 db NI MyDAQ adatgyűjtő modul.  
- 6 db breadboard.  
- Ellenállások, kondenzátorok, tekercsek, IC-k, mérővezetékek.  
- NI Multisim vagy megfelelő szoftver.  

---


# Távközlési alapfeladatok (60 perc)

Az alábbi tételsor a rendelkezésre álló **Johansson DVB-C modulátor**, **Metek HDD spektrumanalizátor**, **GRF-1300A RF és kommunikációs tréner** és **SDRplay spektrumanalizátor** alapján készült. A feladatok célja, hogy a vizsgázók önállóan végezzenek méréseket a különböző távközlési berendezéseken.

---

## **Távközlés 3A: DVB-C modulátor spektrális vizsgálata és jelszintmérés**

**Feladat:**
- Állítson be egy **Johansson DVB-C modulátort** egy adott frekvenciára (pl. 482 MHz).  
- Csatlakoztassa a modulátor HDMI bemenetére egy videóforrást (pl. médialejátszó).  
- A modulátor RF kimenetét csatlakoztassa a **Metek HDD spektrumanalizátorhoz**.  
- Vizsgálja meg a modulált jel spektrumát, mérje meg a jelszintet és a sávszélességet.  

**Mérési feladatok:**
- Jelszint mérése spektrumanalizátorral.  
- Spektrumkép mentése és kiértékelése.  
- Az RF jel sávszélességének meghatározása.  

**Eszközök:**  
- Johansson DVB-C modulátor  
- Metek HDD spektrumanalizátor  
- HDMI forrás (pl. médialejátszó)  

**Időkeret:** 60 perc  

---

## **Távközlés 3B: Amplitúdómoduláció vizsgálata a GRF-1300A trénerrel**

**Feladat:**
- Használja a **GRF-1300A RF és kommunikációs trénert** az amplitúdómoduláció (AM) előállítására.  
- Állítson be egy megfelelő RF vivőfrekvenciát (pl. 900 MHz) és egy moduláló jelet (pl. 1 kHz szinuszjel).  
- Csatlakoztassa a tréner RF kimenetét a hozzá tartozó spektrumanalizátorhoz.  
- Vizsgálja meg az AM jel spektrumát, mérje meg a jelszintet, a sávszélességet és a modulációs mélységet.  

**Mérési feladatok:**
- Jelszint mérése spektrumanalizátorral.  
- Spektrumkép mentése és kiértékelése.  
- Modulációs mélység és sávszélesség meghatározása.  

**Eszközök:**  
- GRF-1300A RF és kommunikációs tréner  
- Spektrumanalizátor (a tréner része)  
- Jelgenerátor a moduláló jel előállításához  

**Időkeret:** 60 perc  

---

## **Távközlés 3C: FM rádióadó vizsgálata J-FET áramkörrel és SDRplay spektrumanalizátorral**

**Feladat:**
- Forrasszon egy megfelelő antennát a **J-FET alapú FM rádióadó áramkörre**.  
- Hangolja be az FM adót egy szabad, **Miskolcon elérhető sávra**.  
- Csatlakoztassa az **SDRplay spektrumanalizátort** egy antennával.  
- Csatlakoztassa a laborban található **GAG-810 audiojel-generátort** az FM adó bemenetére, és állítson be egy megfelelő modulációs jelet.  
- Végezzen spektrumanalízist a sugárzott FM jel frekvenciájának és spektrális jellemzőinek vizsgálatára.  

**Mérési feladatok:**
- Vivőfrekvencia pontos mérése.  
- Jelszint meghatározása.  
- Modulációs mélység és sávszélesség mérése.  

**Eszközök:**  
- J-FET alapú FM rádióadó áramkör  
- SDRplay spektrumanalizátor  
- GAG-810 audiojel-generátor  
- Antennák (FM adóra és SDRplay-re külön-külön)  
- Multiméter, forrasztópáka  

**Időkeret:** 60 perc  

---

## **Közös követelmények mindhárom tételnél:**
- **Eszközök:**  
   - Johansson DVB-C modulátor  
   - Metek HDD spektrumanalizátor  
   - GRF-1300A RF és kommunikációs tréner  
   - SDRplay spektrumanalizátor  
   - GAG-810 audiojel-generátor  
   - Számítógép megfelelő szoftverrel (pl. SDRUno)  

- **Mérési dokumentáció:**  
   - Kapcsolási rajzok és beállítások dokumentálása.  
   - Mérési adatok táblázatos formában.  
   - Spektrumképek mentése és elemzése.  

---

**Megjegyzés:** Minden tételhez külön modulátort és spektrumanalizátort rendelünk, az eszközök egyszerre párhuzamosan használhatók a vizsgázók között.

*Ez a tételsor kiegyensúlyozott, minden tanuló egyenértékű feladatot kap, azonos technológiai szinten és komplexitással.*


# A KKK dokumentum szerint a II. vizsgarész a következőket tartalmazza:

Infokommunikációs hálózatokban alkalmazott passzív hálózati eszközök szerelése és mérése:
	•	Kommunikációs kábelek szerelése és mérése (pl. CAT5, CAT6 LAN kábelek krimpelése, mérőeszközzel ellenőrzése).
	•	Koaxiális tápvonalak szerelése és mérése.
	•	Rádiófrekvenciás passzív eszközök szerelése és mérése.

Elvárt tevékenységek:
	•	A vizsgázó a szerelési feladatokat önállóan végzi.
	•	Az elkészült szerelések megfelelő minőségét méréssel kell igazolni.
	•	Az eredményeket elektronikus jegyzőkönyvben kell dokumentálni.
	•	A feladat befejezése után a vizsgázónak rövid szóbeli összegzést kell adnia az elvégzett tevékenységekről ￼.

Tételsor javaslatok:

## CAT6 UTP kábel szerelése és tesztelése
	•	CAT6 UTP kábel levágása, krimpelése RJ45 csatlakozóval.
	•	Mérőműszerrel (pl. LAN-tester) az elkészült kábel tesztelése.
	•	Hibás kötés esetén a hiba feltárása és javítása.

## Koaxiális kábel szerelése és mérés
	•	RG6 koaxiális kábel levágása és F csatlakozó szerelése.
	•	A kábel jelszintének mérése spektrumanalizátorral (Metek HDD).
	•	A kábelcsillapítás ellenőrzése.

## Rádiófrekvenciás passzív eszközök szerelése és mérése
	•	Rádiófrekvenciás osztó vagy csillapító csatlakoztatása a tápvonalra.
	•	A jelszint mérése a csillapítás mértékének ellenőrzése céljából.
	•	A spektrumanalizátor segítségével a jel spektrális vizsgálata.

Minden tétel esetén:
	•	Mérési eredmények dokumentálása (elektronikus jegyzőkönyv).
	•	Rövid szóbeli összefoglaló a vizsgáztató számára.

# Kábel Szerelési Vizsgafeladat (60 perc)

**A vizsgázó feladata, hogy a 60 perces vizsgafeladat során a következő három feladatot elvégezze:**
- **CAT5 kommunikációs kábel szerelése és mérése**  
- **Koaxiális tápvonal szerelése és csillapításának mérése**  
- **Rádiófrekvenciás passzív eszközök szerelése és mérése**  

A mérési eredményeket **elektronikus jegyzőkönyvben** kell rögzíteni, a feladat végén pedig szóbeli összegzést kell adni a végzett munkáról.

---

## **Feladat 1: CAT5 UTP kábel szerelése és tesztelése**
**Cél:** Egy CAT5 UTP kábel szakszerű szerelése és minőségi ellenőrzése.

### **Lépések:**
1. **Kábel előkészítése:**
   - A kábel megfelelő hosszúságú levágása.  
   - Burkolat eltávolítása, érpárok szétválasztása.  

2. **Csatlakozók szerelése:**
   - RJ45 csatlakozók krimpelése mindkét végére (TIA/EIA-568B szabvány szerint).  

3. **Tesztelés:**
   - **LAN kábelteszterrel** a kábel folytonosságának ellenőrzése.  
   - Hibás kötés esetén javítás elvégzése.  

### **Dokumentáció:**
- Krimpelési sorrend dokumentálása.  
- Mérési eredmények rögzítése (szakadás, helyes bekötés).  

### **Eszközök:**
- CAT5 UTP kábel  
- RJ45 csatlakozók  
- Krimpelő fogó  
- LAN kábelteszter  

---

## **Feladat 2: Koaxiális tápvonal szerelése és csillapításának mérése Johansson modulátorral vagy Profilerrel**
**Cél:** Koaxiális kábel szerelése, valamint a csillapítás mérése stabil RF jelforrással.

### **Lépések:**
1. **Kábel előkészítése:**
   - RG6 koaxiális kábel levágása megfelelő hosszúságúra.  
   - F csatlakozók felszerelése mindkét végére.  

2. **Referencia mérés:**
   - **Johansson modulátor vagy Profiler** beállítása egy adott frekvenciára.  
   - A modulátor kimenetét közvetlenül a **Metek HDD spektrumanalizátorhoz** csatlakoztatni.  
   - A referencia jelszint rögzítése (pl. -10 dBm).  

3. **Kábel csillapítás mérése:**
   - A koaxiális kábel beiktatása a modulátor és a spektrumanalizátor közé.  
   - A kimeneti jelszint mérése a kábel túloldalán.  
   - **Csillapítás kiszámítása:**  

   $$[A = P_{\text{in}} - P_{\text{out}}]$$

### **Dokumentáció:**
- Szerelési lépések rögzítése.  
- Mérési eredmények dokumentálása.  
- Csillapítás kiszámítása.  

### **Eszközök:**
- RG6 koaxiális kábel  
- F csatlakozók  
- Krimpelő fogó  
- Johansson modulátor (stabil jelforrás)  
- Metek HDD spektrumanalizátor  

---

## **Feladat 3: Rádiófrekvenciás passzív eszközök szerelése és mérése**
**Cél:** Rádiófrekvenciás osztók és csillapítók szerelése, valamint azok hatásának mérése.

### **Lépések:**
1. **Rendszer felépítése:**
   - **Johansson modulátor** kimenetéhez csatlakoztasson egy 2-irányú elosztót.  
   - Csatlakoztassa a két kimenetet különböző csillapítókhoz (pl. 6 dB és 10 dB csillapító).  
   - Az elosztó kimeneteihez csatlakoztasson két koaxiális kábelt.  

2. **Mérés:**
   - Mérje meg a kimeneti jelszintet mindkét kimeneten a **Metek HDD spektrumanalizátorral**.  
   - Jegyezze fel a csillapított értékeket, hasonlítsa össze a csillapítók névleges értékeivel.  

3. **Csillapítás ellenőrzése:**
   - Ellenőrizze, hogy az egyes elosztók és csillapítók megfelelnek-e a specifikációnak.  

### **Dokumentáció:**
- Az eszközök kapcsolási rajza.  
- Mérési eredmények rögzítése.  
- Az osztók és csillapítók jellemzőinek összehasonlítása.  

### **Eszközök:**
- kábeltv koax elosztók  
- Állítható csillapítók  
- Johansson modulátor (stabil jelforrás)  
- Metek HDD spektrumanalizátor  
- Koaxiális kábelek és F csatlakozók  

---

## **Közös követelmények:**
- **Időkeret:** 60 perc az összes feladat elvégzésére.  
- **Dokumentáció:** Minden mérési eredményt elektronikus jegyzőkönyvben kell rögzíteni.  
- **Szóbeli összegzés:** A vizsgázónak a feladat végén röviden ismertetnie kell az elvégzett tevékenységeket és az eredményeket.  
- **Hibakezelés:** Hibás szerelés esetén javítás és az újbóli mérés kötelező.  

**A feladatok célja az alapvető szerelési készségek, a precíz mérési technikák és a mérési eredmények dokumentálásának bemutatása.**

---


A dokumentum MathJax támogatással készült, így a képletek webes környezetben helyesen jelennek meg.  

<script async src="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML"></script>
