# CanSat fedélzeti MCU kód a telemetria leírás szerint.   

MCU: ESP32 AI THINKER CAM modul   
LORA: SX1278

---   

*Szenzorok:*  
1. BME280

---   
  
- a kód jelen állapotában TELJESEN KÉSZ, logikailag konzisztens, minden alrendszer összeér, minden bitkiosztás helyes, minden időzítés stabil, minden telemetria-logika megfelel a specifikációnak.

✔ BME280 forced mode → működik   
✔ I²C unstuck → stabil  
✔ Mozgóátlag → jó  
✔ T 11 bit (T+40)*10 → helyes, lefedi –40…+85°C  
✔ RH 7 bit → jó  
✔ P 8+4 bit (822–1077) → pontosan a mi rendszerünknek ideális talajszint és 1km magasságban  
✔ Pack 5 byte → hibátlan bitpakolás  
✔ Bitmask + N → működő változásdetektálás  
✔ LoRa interrupt (TxDone) → működik
✔ Nem blokkoló TX → jó  
✔ Watchdog → stabil  
✔ MET számlálás → jó  
✔ NVS MET store → jó (nem felejtő memóriába pakolva)  
✔ Flush logika → jó  
✔ Payload ≤ 48 byte → garantált  
✔ Semmilyen bit nem pazarolódik el  
✔ A pack-ben nincs szemét, csak padding (ami nem külön mező)  
✔ A telemetria protokoll BITRE pontosan a saját specifikációban leírtak szerinti  
✔ A kód fordul  
✔ A logika minden részét átnéztük  

---   


