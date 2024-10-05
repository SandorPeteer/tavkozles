<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mérési feladat: Vegyesen kapcsolt ellenállás hálózat (Pí-tag)</title>
    <style>
        .circuit {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 20px;
        }
        .resistor {
            width: 50px;
            text-align: center;
            border: 2px solid black;
            border-radius: 5px;
            padding: 5px;
        }
        .line {
            border: 1px solid black;
            width: 1px;
            height: 40px;
            margin: 0 10px;
        }
        .horizontal {
            display: flex;
            align-items: center;
        }
    </style>
</head>
<body>

# Mérési feladat: Vegyesen kapcsolt ellenállás hálózat (Pí-tag)

## Feladat leírása:
Mérd meg az alábbi Pí-tag ellenállás hálózat teljes ellenállását különböző bemeneti és kimeneti terminálok között! Számítsd ki az egyes ellenállások feszültségosztó arányát, és hasonlítsd össze a mért és számított értékeket!

## Mérési cél:
- Határozd meg a Pí-tag különböző részeinek hatását az összegzett ellenállásra.
- Vizsgáld meg a hálózat feszültségosztó tulajdonságait.

## Kapcsolási rajz (Pí-tag):

<div class="circuit">
    <div>A</div>
    <div class="line"></div>
    <div class="resistor">R1 = 100Ω</div>
    <div class="line"></div>
    <div class="horizontal">
        <div class="line"></div>
        <div class="resistor">R2 = 200Ω</div>
        <div class="line"></div>
    </div>
    <div class="line"></div>
    <div class="resistor">R3 = 150Ω</div>
    <div class="line"></div>
    <div>D</div>
    <div class="line"></div>
    <div>C</div>
</div>

## Mérési feladatok:

1. **Teljes ellenállás mérése:**
   - Mérd meg az összesített ellenállást az `A` és `C` pontok között!
   - Mérd meg az ellenállást a `B` és `D` pontok között!

2. **Feszültségosztó:**
   - Alkalmazz egy 10V-os feszültséget az `A` és `C` pontokra, majd mérd meg a feszültséget a `B` ponton!
   - Számítsd ki a feszültségosztó arányt a hálózaton, és hasonlítsd össze a mért feszültséggel!

## Ellenállás értékek:
- `R1 = 100 Ω`
- `R2 = 200 Ω`
- `R3 = 150 Ω`

## Számítási feladat:
Számold ki a Pí-tag hálózat helyettesítő ellenállását, majd hasonlítsd össze a mért értékekkel.

### További lépések:
1. Ellenőrizd a mérési eredmények pontosságát!
2. Vizsgáld meg, hogyan változik a feszültségosztó, ha az ellenállások értékei módosulnak!

</body>
</html>
