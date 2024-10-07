   # Mérési Feladat:
> A különböző típusú antennák teljesítménye és a vételi jelminőség összehasonlítása.  

Ez a mérési feladat lehetővé teszi a hallgatók számára, hogy megismerjék és összehasonlítsák három különböző antenna teljesítményét ugyanazon jel sugárzásával. Valamint a feladat lehetőséget biztosít arra, hogy a tanulók gyakorlati méréseken keresztül tapasztalják meg, hogyan befolyásolja az antenna típusa a jelminőséget és a nyereséget különböző környezetekben. A jegyzőkönyv segítségével dokumentálhatják az eredményeket és levonhatják a következtetéseket.


## Cél
A hallgatók ismerjék meg a különböző antennák jellemzőit, és mérjék a sugárzott DVB-T jel minőségét a Johansson 8202 DVB-T modulátorral. Az ISKRA P2845, ISKRA P20 LOGPER és IKUSI FLASHD C48 antennákat használva a jelminőség és jelszint értékek változását vizsgálják különböző körülmények között.

## Eszközök
- Johansson 8202 DVB-T modulátor   
- ISKRA P20 LOGPER antenna   
- ISKRA P2845 antenna   
- IKUSI FLASHD C48 antenna   
- Szobaantenna [Philips SDV5228/12] (aktív vagy passziv a vételhez)   
- RF kábelek  
- DVB-T vevő (pl. TV vagy mérőműszer)  
- METEK HD spektrum/jelszint analizátor   
- Laptop a jegyzőkönyv készítéséhez   

## Feladat

### 1. Johansson 8202 DVB-T modulátor beállítása
   - Állítsák be a modulátort a következő paraméterekkel:
     - **RF frekvencia:** Szabad sáv, amibe nem zavar bele az adás.
     - **Moduláció:** 16-QAM
     - **Sávszélesség:** 8 MHz
     - **Jelszint:** 65 dBm
   - A modulátor beállításai állandóak maradnak az egész mérés során, csak az antenna típusát változtatják.
   - A vételi oldalon egy szobaantenna segítségével vizsgálják a jelátvitelt.

### 2. Jelátvitel és mérés az ISKRA P20 LOGPER antennával
   - Csatlakoztassák az ISKRA P20 LOGPER antennát a DVB-T modulátorhoz.
   - Sugározzák a jelet az antennán keresztül, és a METEK HD spektrum/jelszint analizátor segítségével mérjék meg a következő paramétereket:
     - Jelszint (dBm)
     - Modulation Error Ratio (MER)
     - Bitsebesség (Mbps)
   - Rögzítsék az eredményeket.

### 3. Jelátvitel és mérés az ISKRA P2845 antennával
   - Csatlakoztassák az ISKRA P2845 antennát a DVB-T modulátorhoz.
   - Sugározzák a jelet az antennán keresztül, és ismét mérjék meg a jelszintet, a MER-t és a bitsebességet.
   - Rögzítsék az eredményeket.

### 4. Jelátvitel és mérés az IKUSI FLASHD C48 antennával
   - Csatlakoztassák az IKUSI FLASHD C48 antennát a DVB-T modulátorhoz.
   - Sugározzák a jelet ezen az antennán keresztül is, és mérjék meg a jelszintet, a MER-t és a bitsebességet.
   - Rögzítsék az eredményeket.   

### 5. Mérés ismétlése egy másik szabad frekvencián   
   - Ismételje meg a méréseket mindegyik antennatípussal egy másik szabad csatornán.
   - Az adóoldali csatorna térjen el legalább 80-100MHz frekvenciával az előző mérésekhez képest.


### 6. Jegyzőkönyv készítése
   - Készítsenek jegyzőkönyvet a mérési eredmények alapján, amely tartalmazza a következő paramétereket minden antennára vonatkozóan:
     - Antenna típusa
     - RF frekvencia (MHz)
     - Jelszint (dBm)
     - MER érték (dB)
     - Bitsebesség (Mbps)
   - A jegyzőkönyv végén hasonlítsák össze a három antenna teljesítményét, és értékeljék a jelminőséget.

### 7. Kiértékelés
   - Elemezzék, melyik antenna biztosította a legjobb jelminőséget és jelszintet az adott frekvencián.
   - Beszéljék meg, milyen tényezők befolyásolhatják a különböző antennák teljesítményét (pl. antenna típus, nyereség, iránykarakterisztika).

## Jegyzőkönyv sablon

| Antenna típusa      | RF frekvencia (MHz) | Jelszint (dBm) | Bitsebesség (Mbps) | MER érték (dB) |
|---------------------|---------------------|----------------|--------------------|----------------|
| **SMART HD 550**     | 522                 |                |                    |                |
| **ISKRA P20 LOGPER** | 522                 |                |                    |                |
| **IKUSI FLASHD C48** | 522                 |                |                    |                |
| **SMART HD 550**     | 610                 |                |                    |                |
| **ISKRA P20 LOGPER** | 610                 |                |                    |                |
| **IKUSI FLASHD C48** | 610                 |                |                    |                |

## Időtartam
- Modulátor beállítása, antennák felszerelése: 30 perc
- Mérések a három antennával: 60 perc
- Jegyzőkönyv készítése és kiértékelés: 30 perc
