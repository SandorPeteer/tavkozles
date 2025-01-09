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
- **Az NI MyDAQ adatgyűjtő és breadboard kötelező használata.**  
- **Minden mérési adat jegyzőkönyvben történő rögzítése.**  
- **Kapcsolási rajz és számítások mellékelése.**  
- **Az eredmények szakszerű dokumentálása.**  

---

## **Eszközigény termenként (9 tanulóhoz):**
- **9 db NI MyDAQ adatgyűjtő modul.**  
- **9 db breadboard.**  
- **Ellenállások, kondenzátorok, tekercsek, mérővezetékek.**  
- **NI Multisim vagy megfelelő szoftver.**  

**Ez a tételsor kiegyensúlyozott, minden tanuló egyenértékű feladatot kap, hasonló eszközhasználattal és időigénnyel.**
  
# Elektronikai összetett kapcsolások (60 perc)

Az alábbi három tétel komplexebb áramkörök beüzemelését, méréstechnikai vizsgálatát és dokumentálását tartalmazza, a rendelkezésre álló alkatrészekhez igazítva.

---

## **Elektro 2A: TL072 műveleti erősítős feszültségerősítő áramkör építése és mérése**
**Feladat:**
- Építsen meg egy **nem invertáló műveleti erősítős feszültségerősítő** áramkört a TL072 IC felhasználásával.  
- Alkalmazandó alkatrészek:  
   - Bemeneti ellenállás: \(R_1 = 10 k\Omega\)  
   - Visszacsatoló ellenállás: \(R_2 = 100 k\Omega\)  
- Határozza meg az erősítést:  
   \[
   A_v = 1 + \frac{R_2}{R_1}
   \]  
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
   \[
   Y = (A \cdot B) + (\neg C)
   \]  
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

---

**Ez a tételsor kiegyensúlyozott, minden tanuló egyenértékű feladatot kap, azonos technológiai szinten és komplexitással.**  



# Elektronikai összetett kapcsolások (60 perc)

A dokumentum MathJax támogatással készült, így a képletek webes környezetben helyesen jelennek meg.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
