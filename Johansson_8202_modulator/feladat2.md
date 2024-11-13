# Mérési Feladat:   
> A különböző bitsebesség milyen hatással van a jelminőségre.

Ez a mérési feladat a Johansson 8202 DVB-T modulátor többcsatornás képességeit, illetve a bitsebesség és jelminőség kapcsolatát vizsgálja.

## Cél
A hallgatók megismerjék a Johansson 8202 DVB-T modulátor további képességeit, különös tekintettel a többcsatornás jel generálásra. A mérés során a résztvevők két programot állítanak be és mérik a jel minőségét különböző bitsebességek mellett.

## Eszközök
- 2db Johansson 8202 DVB-T modulátor
- DVB-T vevő (pl. TV vagy mérőműszer)
- RF kábelek
- METEK HD spektrum/jelszint analizátor
- Laptop a jegyzőkönyv készítéséhez

## Feladat

### 1. Johansson 8202 modulátor konfiguráció  
   - Kábelezzék össze a modulátorokat egymásba fűzve, majd a kör végén található modulátor RF kimenetét kössék a Spektrumanalizátorra.
   - Gyári beállításokra állítsa vissza a modulátorokat (Factory Reset).
   - A hardver vezérlőfelületén keresztül állítsák be a modulátort. Válasszanak két külön testre szabott RF frekvenciát (pl. 674 MHz, 682 MHz).
   - Állítsák be a többcsatornás jelkimenetet: két különálló programot (pl. TV1 és TV2 néven átnevezve a modulátor beállításában).
   - Moduláció: 64-QAM.
   - Sávszélesség: 8 MHz.
   - Válasszanak eltérő bitsebességet a két program számára, például:
     - TV1: 15 Mbps
     - TV2: 10 Mbps

### 2. DVB-T jel mérés és stream ellenőrzés
   - Az RF kábelen keresztül csatlakoztassák a DVB-T vevőt a modulátorhoz, és ellenőrizzék, hogy mindkét program helyesen vehető-e a METEK HD spektrum/jelszint analizátorral.
   - Mérjék meg a következő paramétereket:
     - Jelszint (dBm)
     - Modulation Error Ratio (MER)
     - A két program bitsebessége

### 3. Bitsebesség és jelminőség összefüggése
   - A következő lépésben újra változtassák meg a bitsebességet az egyik programnál (pl. TV2), és figyeljék meg, hogyan változik a jelminőség (MER).
   - Mérések: növeljék a TV2 bitsebességét 10 Mbps-ról MAXIMUM Mbps-ra, majd ismét mérjék meg a jelszintet, a MER-t és a vevő reakcióját.

### 4. Jegyzőkönyv készítése
   - A laptopon készítsenek jegyzőkönyvet a mért paraméterekről:
     - RF frekvencia (MHz)
     - Moduláció típusa
     - Sávszélesség (MHz)
     - Jelszint (dBm)
     - Bitsebesség (Mbps) mindkét programhoz
     - MER érték (dB)
   - A jegyzőkönyv tartalmazzon megjegyzéseket a bitsebesség változásának hatásáról a jelminőségre és a vevő működésére.

### 5. Összegzés és kiértékelés
   - Hasonlítsák össze a mérések eredményeit a különböző bitsebességek mellett. Melyik beállítás biztosította a legjobb jelminőséget mindkét program számára?
   - Beszéljék meg a csoportban, hogyan lehet optimalizálni a többcsatornás jelek sugárzását.

## Jegyzőkönyv sablon

| Mérési paraméter   | RF frekvencia (MHz) | Program neve | Bitsebesség (Mbps) | Jelszint (dBm) | MER érték (dB) |
|--------------------|---------------------|--------------|--------------------|----------------|----------------|
| **Mérési eredmény 1** | 674              | TV1          | 15                 | 70             | 38             |
| **Mérési eredmény 2** | 682              | TV2          | 10                 | 70             | 40             |
| **Mérési eredmény 3** | 682              | TV2          | 21.5 (max)         | 68             | 35             |

## Időtartam
- A modulátor beállítása: 30 perc
- Mérések különböző bitsebességekkel: 60 perc
- Jegyzőkönyvezés és megbeszélés: 30 perc
