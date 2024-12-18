# Gyakorlati feladat: Johansson 6700 Profiler programozható antennaerősítő-szűrő használata

## Cél
A gyakorlat célja, hogy a diákok elsajátítsák a Johansson 6700 Profiler antennaerősítő-szűrő beállításainak gyakorlati használatát különböző antennák jeleinek kezelésére. A feladat során a diákok beállítják a csatornákat, optimalizálják a jelszinteket és vizsgálják a bejövő és kimenő jeleket spektrum analizátor segítségével.

## Szükséges eszközök
- Johansson 6700 Profiler programozható antennaerősítő-szűrő
- FM antenna (87-108 MHz)
- DVB-T szoba antenna, pl.: SMART HD550 (UHF: 470-862 MHz)
- Spektrum analizátor
- Koaxiális kábelek
- Laptop a beállítások elvégzéséhez és jegyzőkönyv készítéséhez

## Feladat leírása

### 1. Eszközök bekapcsolása és bekötése (30 perc)
1. Kössétek rá az antennát a spektrumanalizátorra, mentsétek el 45 - 1000 MHz közötti ablakban milyen jelek érkeznek be! 
2. Csatlakoztassátok át az antennát a Johansson 6700 Profiler egyik illeszkedő bemenetére és a spektrumanalizátorra is RF kábeleket és jelosztót felhasználva.
3. Kössetek be egy FM antennát az FM bemenetre, egy DVB-T antennát a VHF/UHF bemenetre, (és egy koax kábelt egy másik VHF/UHF bemenetre például a Johansson 8202 modulátort).
4. Csatlakoztassátok a spektrum analizátort a Johansson 6700 Profiler kimenetére a kimenő jelek méréséhez.

### 2. Csatornaáthelyezés és jelszint-optimalizálás (45 perc)
1. Használjátok a Johansson 6700 csatornaáthelyezési funkcióját (frekvenciakonverter), hogy az FM és DVB-T jeleket különböző frekvenciákra helyezzétek át.
   - Példa: A DVB-T jeleeket helyezzétek át növekső sorrendbe a 41-es csatornától kezdve. 
   - Csatorna információk: [Avasi adótoronyról érkező jelek](https://www.fmdx.hu/transmitters-hng-avas.htm)
   - Jegyezzétek fel az összes bejövő frekvenciát és az áthelyezett csatornák új frekvenciáit a jegyzőkönyvbe.
   
2. Aktiváljátok az automatikus csatornánkénti szintszabályzást (AGC) az eszköz menüjében amennyiben lehetséges, valamint ha szükséges kapcsoljátok be az antenna erősítő fokozatot is.
   - Ellenőrizzétek, hogy a kimenő jelszintek egységesek legyenek, állítsd be 100dBu -ra, függetlenül a bejövő jelek eltérő szintjétől.
   - Rögzítsétek a bemeneti és kimeneti jelszinteket a spektrum analizátor segítségével, és jegyezzétek fel azokat.

### 3. Szűrő beállítások és interferencia vizsgálat (15 perc)
1. Ellenőrizzétek le az LTE szűrőt az eszközben, hogy megszűri-e a 790 MHz feletti zavaró jeleket.
   - Vizsgáljátok meg a spektrum analizátorral, hogyan változnak a jelek a kimeneten, a szűrő funkcionál vagy sem.
   
2. Készítsetek jegyzőkönyvet a bemeneti és kimeneti spektrum különbségeiről, és jegyezzétek fel, hogy a szűrők hogyan hatnak a jelminőségre és jelszintre.

### 4. Jegyzőkönyv készítése (30 perc)
- Készítsetek részletes jegyzőkönyvet a gyakorlatról, amely tartalmazza:
   - Az antennák beállításait és bemeneti jelszinteket.
   - A csatornaáthelyezési beállításokat és azok hatását a kimenő jelszintekre.
   - Az AGC (Automatic Gain Control) működésének hatását a jelszintek kiegyenlítésére.
   - A szűrés mérési eredményeit.
 
#### Javasolt táblázat a jegyzőkönyvhöz

| Antenna típusa           | Eredeti csatorna  | Áthelyezett csatorna | Eredeti frekvencia | Áthelyezett frekvencia | Bemeneti jelszint (dB) | Kimeneti jelszint (dB) | Spektrum analizátor kép neve    |
|--------------------------|-------------------|----------------------|--------------------|------------------------|------------------------|------------------------|---------------------------------|
| FM antenna               | 101,7 MHz         | 183,7 MHz            | 100 MHz            | 180 MHz                | -30 dB                 | -20 dB                 | FM_before_after.png             |
| DVB-T antenna (VHF)      | 5. csatorna       | 10. csatorna         | 220 MHz            | 230 MHz                | -40 dB                 | -30 dB                 | VHF_signal_comparison.png       |
| DVB-T antenna (UHF)      | 28. csatorna      | 33. csatorna         | 500 MHz            | 600 MHz                | -35 dB                 | -25 dB                 | UHF_signal_shift.png            |
| Koax Kábel (RF-modulátor)| KábelTV (CH22)    | KábelTV (CH23)       | 600 MHz            | 700 MHz                | -45 dB                 | -30 dB                 | Coax_signal_modification.png    |


---

A jegyzőkönyvben a tanulóknak részletesen dokumentálniuk kell az eredeti és áthelyezett frekvenciákat, a bemeneti és kimeneti jelszinteket, valamint a szűrők alkalmazásának hatását. A javasolt táblázat segít abban, hogy a mérési eredmények könnyen átláthatók legyenek.   


---

## Időkeret
A teljes feladat időtartama: 2 óra
- Eszközök bekötése: 30 perc
- Csatornaáthelyezés és jelszint-optimalizálás: 45 perc
- Szűrő beállítások ellenőrzése: 15 perc
- Jegyzőkönyv készítése: 30 perc

## Értékelés
A feladat értékelése a jegyzőkönyv részletessége és pontossága, valamint a helyes beállítások és mérések alapján történik.   

---

Ez a feladat biztosítja, hogy a diákok valós környezetben gyakorolják a Johansson 6700 Profiler képességeit az antennarendszerek kezelésében és optimalizálásában.
