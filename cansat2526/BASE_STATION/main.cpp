#include "heltec.h"
#include <Arduino.h>

#include <SPI.h>
#include <Preferences.h>
#include "esp_task_wdt.h"
#include <stdio.h>

// -----------------------------------------------------------------------------
//  HARDVER PIN DEFINÍCIÓK (EZEKET A SAJÁT BEKÖTÉSEDHEZ IGAZÍTSD!)
// -----------------------------------------------------------------------------

// I2C BME280 – ESP32-CAM-on általában:

// SX1278 LoRa (példa bekötés – ezt a saját modulodhoz igazítsd)
#define LORA_SCK   5
#define LORA_MISO  19
#define LORA_MOSI  27
#define LORA_SS    18
#define LORA_RST   14
#define LORA_DIO0  26
#define LORA_DIO1  35
#define LORA_DIO2  34
#define VEXT_PIN 21


#define HELTEC_LED_PIN 25
#define HELTEC_BUTTON_PIN 0

#define CAM_LED_PIN 4

// -----------------------------------------------------------------------------
//  LoRa frekvencia beállítások (globális)
// ---------------------------------------------------------------------------
static uint32_t LORA_FREQ_HZ = 433200000; // alap vivőfrekvencia (Hz)
static int32_t LORA_OFFSET_HZ = 0;     // kézi offset (Hz)

static uint32_t led_on_until = 0;

struct TeleSample
{
  float tempC;
  float rh;
  float press_hPa;
};

// Regiszter címek
#define REG_FIFO 0x00
#define REG_OP_MODE 0x01
#define REG_FRF_MSB 0x06
#define REG_FRF_MID 0x07
#define REG_FRF_LSB 0x08
#define REG_PA_CONFIG 0x09
#define REG_OCP 0x0B
#define REG_LNA 0x0C
#define REG_FIFO_ADDR_PTR 0x0D
#define REG_FIFO_TX_BASE 0x0E
#define REG_FIFO_RX_BASE 0x0F
#define REG_FIFO_RX_CURRENT_ADDR 0x10
#define REG_IRQ_FLAGS 0x12
#define REG_RX_NB_BYTES 0x13
#define REG_MODEM_CONFIG1 0x1D
#define REG_MODEM_CONFIG2 0x1E
#define REG_SYMB_TIMEOUT_LSB 0x1F
#define REG_PREAMBLE_MSB 0x20
#define REG_PREAMBLE_LSB 0x21
#define REG_PAYLOAD_LENGTH 0x22
#define REG_MODEM_CONFIG3 0x26
#define REG_DIO_MAPPING1 0x40
#define REG_VERSION 0x42
#define REG_PA_DAC 0x4D

// -----------------------------------------------------------------------------
//  SX1278 – ALAP SPI/REG KEZELÉS
// -----------------------------------------------------------------------------

static uint8_t lora_read_reg(uint8_t addr)
{
  digitalWrite(LORA_SS, LOW);
  SPI.transfer(addr & 0x7F);
  uint8_t val = SPI.transfer(0x00);
  digitalWrite(LORA_SS, HIGH);
  return val;
}

static void lora_write_reg(uint8_t addr, uint8_t val)
{
  digitalWrite(LORA_SS, LOW);
  SPI.transfer(addr | 0x80);
  SPI.transfer(val);
  digitalWrite(LORA_SS, HIGH);
}

// FIFO-ba több byte írása
static void lora_write_fifo(const uint8_t *data, uint8_t len)
{
  digitalWrite(LORA_SS, LOW);
  SPI.transfer(REG_FIFO | 0x80);
  for (uint8_t i = 0; i < len; ++i)
  {
    SPI.transfer(data[i]);
  }
  digitalWrite(LORA_SS, HIGH);
}

static void oled_show_lora_config()
{
  if (!Heltec.display) return;

  // Read back current LoRa frequency from FRF registers
  uint8_t frfMsb = lora_read_reg(REG_FRF_MSB);
  uint8_t frfMid = lora_read_reg(REG_FRF_MID);
  uint8_t frfLsb = lora_read_reg(REG_FRF_LSB);
  uint32_t frf = ((uint32_t)frfMsb << 16) | ((uint32_t)frfMid << 8) | frfLsb;
  double fstep = 32000000.0 / 524288.0; // Fxtal / 2^19
  double freq_hz = frf * fstep;
  double freq_mhz = freq_hz / 1e6;

  uint8_t mc1 = lora_read_reg(REG_MODEM_CONFIG1);
  uint8_t mc2 = lora_read_reg(REG_MODEM_CONFIG2);

  uint8_t bw = (mc1 >> 4) & 0x0F;
  uint8_t cr = (mc1 >> 1) & 0x07;
  uint8_t sf = (mc2 >> 4) & 0x0F;

  const char *bwStr = "BW?";
  switch (bw)
  {
    case 0: bwStr = "BW7.8k"; break;
    case 1: bwStr = "BW10.4k"; break;
    case 2: bwStr = "BW15.6k"; break;
    case 3: bwStr = "BW20.8k"; break;
    case 4: bwStr = "BW31.25k"; break;
    case 5: bwStr = "BW41.7k"; break;
    case 6: bwStr = "BW62.5k"; break;
    case 7: bwStr = "BW125k"; break;
    case 8: bwStr = "BW250k"; break;
    case 9: bwStr = "BW500k"; break;
  }

  const char *crStr = "CR?";
  switch (cr)
  {
    case 1: crStr = "CR4/5"; break;
    case 2: crStr = "CR4/6"; break;
    case 3: crStr = "CR4/7"; break;
    case 4: crStr = "CR4/8"; break;
  }

  char line1[32];
  char line2[32];
  char line3[32];
  char line4[32];

  snprintf(line1, sizeof(line1), "LoRa RX READY");
  snprintf(line2, sizeof(line2), "F=%.3fMHz", freq_mhz);
  snprintf(line3, sizeof(line3), "Offset=%ldHz", (long)LORA_OFFSET_HZ);
  snprintf(line4, sizeof(line4), "SF%u %s %s", (unsigned)sf, bwStr, crStr);

  Heltec.display->clear();
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 0, line1);
  Heltec.display->drawString(0, 12, line2);
  Heltec.display->drawString(0, 24, line3);
  Heltec.display->drawString(0, 36, line4);
  Heltec.display->display();
}

// LoRa op-mode bitek
#define LONG_RANGE_MODE 0x80
#define MODE_SLEEP 0x00
#define MODE_STDBY 0x01
#define MODE_TX 0x03
#define MODE_RXCONTINUOUS 0x05
#define IRQ_RX_DONE 0x40

// Csomagméret
static const uint8_t LORA_MAX_PAYLOAD = 48;

// -----------------------------------------------------------------------------
//  VÁLTOZÁSDETEKTÁLÁS – PACK SZINTEN
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//  SX1278 – ALAP SPI/REG KEZELÉS
// -----------------------------------------------------------------------------

static void lora_read_fifo(uint8_t *data, uint8_t len)
{
  digitalWrite(LORA_SS, LOW);
  // Read from FIFO register (address 0x00, MSB=0 for read)
  SPI.transfer(REG_FIFO & 0x7F);
  for (uint8_t i = 0; i < len; ++i)
  {
    data[i] = SPI.transfer(0x00);
  }
  digitalWrite(LORA_SS, HIGH);
}

static void lora_set_lora_opmode(uint8_t mode)
{
  uint8_t op = LONG_RANGE_MODE | (mode & 0x07);
  lora_write_reg(REG_OP_MODE, op);
}

static void lora_set_opmode(uint8_t mode)
{
  uint8_t op = lora_read_reg(REG_OP_MODE);
  op = (op & 0xF8) | (mode & 0x07);
  lora_write_reg(REG_OP_MODE, op);
}

// -----------------------------------------------------------------------------
//  SX1278 – INIT (433 MHz, LoRa, SF12, BW125, CR4/8, +20 dBm, preamble 8)
// -----------------------------------------------------------------------------

void IRAM_ATTR onRxDone();
static volatile bool g_rx_done = false;
static bool lora_begin()
{
  pinMode(LORA_SS, OUTPUT);
  pinMode(LORA_RST, OUTPUT);
  pinMode(LORA_DIO0, INPUT);
  attachInterrupt(digitalPinToInterrupt(LORA_DIO0), onRxDone, RISING);

  pinMode(CAM_LED_PIN, OUTPUT);
  digitalWrite(CAM_LED_PIN, LOW);

  digitalWrite(LORA_SS, HIGH);

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  SPI.setDataMode(SPI_MODE0);
  SPI.setBitOrder(MSBFIRST);
  SPI.setFrequency(8000000);

  // Reset
  digitalWrite(LORA_RST, LOW);
  delay(10);
  digitalWrite(LORA_RST, HIGH);
  delay(10);

  // LoRa mód, sleep → standby
  lora_write_reg(REG_OP_MODE, LONG_RANGE_MODE | MODE_SLEEP);
  delay(10);
  lora_set_lora_opmode(MODE_STDBY);
  delay(10);

  // Verzió ellenőrzés
  uint8_t ver = lora_read_reg(REG_VERSION);
  if (ver == 0x00 || ver == 0xFF)
  {
    return false; // nincs modul / hibás
  }

  // Frekvencia: beállítás LORA_FREQ_HZ és LORA_OFFSET_HZ alapján
  // FRF = Freq / Fstep, Fstep = 32MHz / 2^19 ≈ 61.035 Hz
  uint64_t targetFreq = (uint64_t)LORA_FREQ_HZ + (int64_t)LORA_OFFSET_HZ;
  double fstep = 32000000.0 / 524288.0; // datasheet: Fxtal/2^19
  uint32_t frf = (uint32_t)(targetFreq / fstep);

  lora_write_reg(REG_FRF_MSB, (uint8_t)((frf >> 16) & 0xFF));
  lora_write_reg(REG_FRF_MID, (uint8_t)((frf >> 8) & 0xFF));
  lora_write_reg(REG_FRF_LSB, (uint8_t)(frf & 0xFF));

  // PA konfiguráció: PA_BOOST, ~+20 dBm
  // 17–20 dBm környéke: PaConfig ≈ 0x8F, PaDac ≈ 0x87 (20 dBm mód)
  lora_write_reg(REG_PA_CONFIG, 0x8F); // PA_BOOST, max power
  lora_write_reg(REG_PA_DAC, 0x87);    // +20 dBm mód

  // OCP limit módosítása (0x0F ≠ teljes kikapcsolás, hanem magas áramhatár)
  lora_write_reg(REG_OCP, 0x0F); // OCP OFF – teljes áram a PA-nak

  // LNA boost on
  lora_write_reg(REG_LNA, 0x23);

  // ModemConfig1: BW=125 kHz, CR=4/8, explicit header
  // BW=125k → 0b0111, CR=4/8 → 0b100, explicit header=0
  // 0b0111 1000 = 0x78
  lora_write_reg(REG_MODEM_CONFIG1, 0x78);

  // ModemConfig2: SF12, CRC ON, SymbTimeoutMSB=0
  // SF12 → 0b1100, CRC ON → bit2=1
  // 0b1100 0100 = 0xC4
  lora_write_reg(REG_MODEM_CONFIG2, 0xC4);

  // Symbol timeout (LSB) – nagy érték, hogy ne timeout-oljon RX-ben
  lora_write_reg(REG_SYMB_TIMEOUT_LSB, 0x64);

  // ModemConfig3: LowDataRateOptimize ON (SF11/12 + BW125), AGC Auto ON
  lora_write_reg(REG_MODEM_CONFIG3, 0x0C);

  // Preamble = 8
  lora_write_reg(REG_PREAMBLE_MSB, 0x00);
  lora_write_reg(REG_PREAMBLE_LSB, 8);

  // FIFO base address
  lora_write_reg(REG_FIFO_TX_BASE, 0x00);
  lora_write_reg(REG_FIFO_RX_BASE, 0x00);

  // DIO0 → RxDone
  lora_write_reg(REG_DIO_MAPPING1, 0x00);

  // Standby
  lora_set_lora_opmode(MODE_STDBY);
  // Continuous RX mode
  lora_set_lora_opmode(0x05); // MODE_RXCONTINUOUS
  return true;
}

// -----------------------------------------------------------------------------
//  SX1278 – KÜLDÉS (NEM BLOKKOLÓ, TXDONE-t loop-ban kezeljük)
// -----------------------------------------------------------------------------

void IRAM_ATTR onRxDone() {
  g_rx_done = true;
}

static void decode_dynamic_pack(const uint8_t *in, TeleSample &s)
{
  uint32_t acc = 0;
  acc |= (uint32_t)in[0];
  acc |= (uint32_t)in[1] << 8;
  acc |= (uint32_t)in[2] << 16;
  acc |= (uint32_t)in[3] << 24;

  uint32_t T_code      =  acc        & ((1u << 11) - 1u);
  uint32_t RH_code     = (acc >> 11) & ((1u << 7)  - 1u);
  uint32_t P_int_code  = (acc >> 18) & ((1u << 8)  - 1u);
  uint32_t P_frac_code = (acc >> 26) & ((1u << 4)  - 1u);

  float T_c = ((float)T_code / 10.0f) - 40.0f;
  if (T_c < -40.0f) T_c = -40.0f;
  if (T_c > 87.9f)  T_c = 87.9f;

  float H = (float)RH_code;
  if (H < 0.0f)  H = 0.0f;
  if (H > 100.0f) H = 100.0f;

  uint32_t P_int = P_int_code + 822u;
  if (P_int < 822u)  P_int = 822u;
  if (P_int > 1077u) P_int = 1077u;

  if (P_frac_code > 9u) P_frac_code = 9u;
  float P = (float)P_int + ((float)P_frac_code / 10.0f);

  s.tempC = T_c;
  s.rh = H;
  s.press_hPa = P;
}

static void decode_telemetry_packet(const uint8_t *buf, uint8_t len)
{
  if (len < 5) return;
  if (buf[0] != 0xA5) return;

  uint16_t base_MET = (uint16_t)buf[1] | ((uint16_t)buf[2] << 8);
  uint8_t N        = buf[3];
  uint8_t bitmask  = buf[4];

  if (N == 0 || N > 8) return;

  uint8_t used_mask = bitmask & ((1 << N) - 1);

  uint8_t m = used_mask;
  uint8_t num_packs = 0;
  while (m) { num_packs += (m & 1); m >>= 1; }

  uint8_t expected_len = 1 + 2 + 1 + 1 + num_packs * 4;
  if (len < expected_len) return;

  uint8_t pack_idx = 5;

  static bool have_last = false;
  static float last_tel_T = 0;
  static float last_tel_RH = 0;
  static float last_tel_P = 0;
  static double last_freq_hz = 0.0;

  char lines[8][40];
  uint8_t lineCount = 0;

  // Read RSSI before filling lines[lineCount]
  uint8_t rssi_reg = lora_read_reg(0x1A); // REG_PKT_RSSI_VALUE
  int rssi_dbm = (int)rssi_reg - 164;

  // --- LoRa-mode FEI (Frequency Error Indicator) according to DS_SX1276-7-8-9, section 4.1.5 ---
  // FEI is a signed 20-bit value spread across RegFeiMsb/Mid/Lsb (0x28..0x2A) in LoRa mode.
  uint8_t fe_msb = lora_read_reg(0x28);
  uint8_t fe_mid = lora_read_reg(0x29);
  uint8_t fe_lsb = lora_read_reg(0x2A);

  int32_t fei_raw = (int32_t)(
      ((uint32_t)(fe_msb & 0x0F) << 16) |
      ((uint32_t)fe_mid << 8) |
      (uint32_t)fe_lsb);

  // Sign-extend 20-bit two's complement to 32-bit
  if (fei_raw & 0x80000)
  {
    fei_raw |= 0xFFF00000;
  }

  // Determine LoRa bandwidth in kHz from RegModemConfig1[7:4]
  uint8_t mc1 = lora_read_reg(REG_MODEM_CONFIG1);
  uint8_t bw_bits = (mc1 >> 4) & 0x0F;
  double bw_khz = 0.0;

  switch (bw_bits)
  {
    case 0: bw_khz = 7.8;   break;
    case 1: bw_khz = 10.4;  break;
    case 2: bw_khz = 15.6;  break;
    case 3: bw_khz = 20.8;  break;
    case 4: bw_khz = 31.25; break;
    case 5: bw_khz = 41.7;  break;
    case 6: bw_khz = 62.5;  break;
    case 7: bw_khz = 125.0; break;
    case 8: bw_khz = 250.0; break;
    case 9: bw_khz = 500.0; break;
    default: bw_khz = 125.0; break; // fallback, de nálunk BW=125k
  }

  // Datasheet formula (LoRa mode):
  // F_err_Hz = LoRaFeiValue * 2^24 / (32e6) * (BW_kHz / 500)
  const double fei_scale = (double)(1UL << 24) / 32000000.0;
  double freqErrHz = (double)fei_raw * fei_scale * (bw_khz / 500.0);

  // --- Automatikus frekvencia finomhangolás (AFC) ---
  // Csak akkor korrigálunk, ha az eltérés érdemi (500 Hz < |err| < 40 kHz),
  // így a kvantálási zajra és nagyon kis ingadozásokra nem reagálunk.
  double errAbs = (freqErrHz < 0.0) ? -freqErrHz : freqErrHz;
  if (errAbs > 500.0 && errAbs < 40000.0)
  {
    // Egy lépésben kompenzáljuk az eltérést: a vevő középfrekvenciáját
    // eltoljuk az ellenkező irányba.
    int32_t stepHz;
    if (freqErrHz >= 0.0)
      stepHz = (int32_t)(freqErrHz + 0.5);
    else
      stepHz = (int32_t)(freqErrHz - 0.5);

    LORA_OFFSET_HZ -= stepHz;

    // Új FRF beállítása: F_target = LORA_FREQ_HZ + LORA_OFFSET_HZ
    uint64_t targetFreq = (uint64_t)LORA_FREQ_HZ + (int64_t)LORA_OFFSET_HZ;
    double fstep = 32000000.0 / 524288.0; // Fxtal / 2^19
    uint32_t frf = (uint32_t)(targetFreq / fstep);

    // Átmenetileg STDBY módba lépünk a PLL állításához, majd vissza RX-be
    lora_set_lora_opmode(MODE_STDBY);
    lora_write_reg(REG_FRF_MSB, (uint8_t)((frf >> 16) & 0xFF));
    lora_write_reg(REG_FRF_MID, (uint8_t)((frf >> 8) & 0xFF));
    lora_write_reg(REG_FRF_LSB, (uint8_t)(frf & 0xFF));
    lora_set_lora_opmode(MODE_RXCONTINUOUS);
  }

  // Corrected actual RX centre frequency (információs célra)
  last_freq_hz = (double)LORA_FREQ_HZ + (double)LORA_OFFSET_HZ;

  // Első sor: RSSI + frekvencia-eltérés (Hz pontossággal, pillanatnyi FEI)
  snprintf(lines[0], sizeof(lines[0]), "%ddB %+.0fHz", rssi_dbm, freqErrHz);
  lineCount = 1;

  for (uint8_t i = 0; i < N; i++)
  {
    uint16_t MET_i = base_MET + i;
    bool changed = (bitmask & (1 << i)) != 0;

    if (changed)
    {
      if (pack_idx + 4 > len) break;

      uint32_t acc = 0;
      acc |= (uint32_t)buf[pack_idx + 0];
      acc |= (uint32_t)buf[pack_idx + 1] << 8;
      acc |= (uint32_t)buf[pack_idx + 2] << 16;
      acc |= (uint32_t)buf[pack_idx + 3] << 24;
      pack_idx += 4;

      uint32_t T_code      =  acc        & ((1u << 11) - 1u);
      uint32_t RH_code     = (acc >> 11) & ((1u << 7)  - 1u);
      uint32_t P_int_code  = (acc >> 18) & 0xFF;
      uint32_t P_frac_code = (acc >> 26) & 0x0F;

      float T = (T_code / 10.0f) - 40.0f;
      float RH = (float)RH_code;
      float P = 822.0f + (float)P_int_code + (float)P_frac_code / 10.0f;

      last_tel_T = T;
      last_tel_RH = RH;
      last_tel_P = P;
      have_last = true;
    }
    else
    {
      if (!have_last) continue;
    }

    if (lineCount < 6)
    {
      snprintf(lines[lineCount], sizeof(lines[0]),
               "%u %.1fC %.0f%% %.1fhPa",
               MET_i, last_tel_T, last_tel_RH, last_tel_P);
      lineCount++;
    }
  }

  if (lineCount > 0 && Heltec.display)
  {
    Heltec.display->clear();
    Heltec.display->setFont(ArialMT_Plain_10);
    for (uint8_t i = 0; i < lineCount; i++)
    {
      Heltec.display->drawString(0, i * 10, lines[i]);
    }
    Heltec.display->display();
  }
}

static void handle_lora_rx()
{
  uint8_t irq = lora_read_reg(REG_IRQ_FLAGS);

  if (irq & IRQ_RX_DONE)
  {
    uint8_t len = lora_read_reg(REG_RX_NB_BYTES);
    uint8_t addr = lora_read_reg(REG_FIFO_RX_CURRENT_ADDR);
    lora_write_reg(REG_FIFO_ADDR_PTR, addr);

    uint8_t buf[64];
    if (len > sizeof(buf))
      len = sizeof(buf);

    for (uint8_t i = 0; i < len; ++i)
    {
      buf[i] = lora_read_reg(REG_FIFO);
    }

    decode_telemetry_packet(buf, len);
    // Forward raw LoRa payload as binary over serial
    Serial.write(buf, len);

    led_on_until = millis() + 80;
    digitalWrite(HELTEC_LED_PIN, HIGH);

    // Clear all IRQ flags and stay in continuous RX
    lora_write_reg(REG_IRQ_FLAGS, 0xFF);
    lora_set_lora_opmode(MODE_RXCONTINUOUS);
  }
  else
  {
    // Clear any spurious IRQ flags and keep listening
    lora_write_reg(REG_IRQ_FLAGS, 0xFF);
    lora_set_lora_opmode(MODE_RXCONTINUOUS);
  }
}

// -----------------------------------------------------------------------------
//  SETUP / LOOP
// -----------------------------------------------------------------------------

void setup()
{
  Heltec.begin(true, false, true, false); // Display ON, LoRa OFF (we use raw SX1278), Serial ON, PA boost OFF
  pinMode(VEXT_PIN, OUTPUT);
  digitalWrite(VEXT_PIN, LOW); // VEXT ON – 3V3 power for external devices

  Serial.begin(115200);
  delay(1000);

  // Serial.println("CanSat BME280 + LoRa telemetria indul...");

  // Watchdog inicializalas (3s timeout, reset engedelyezve)
  esp_task_wdt_init(3, true);
  esp_task_wdt_add(NULL); // jelenlegi task


  if (!lora_begin())
  {
    // LoRa modul nem található – opcionálisan ide jöhetne hiba kijelzés
  }
  else
  {
    oled_show_lora_config();
  }

  pinMode(HELTEC_LED_PIN, OUTPUT);
  digitalWrite(HELTEC_LED_PIN, LOW);
  pinMode(HELTEC_BUTTON_PIN, INPUT_PULLUP);
}

void loop()
{
  uint32_t now = millis();

  if (g_rx_done)
  {
    g_rx_done = false;
    handle_lora_rx();
  }

  // turn off LED when time expires
  if (millis() > led_on_until)
  {
    digitalWrite(HELTEC_LED_PIN, LOW);
  }

  // Button for deep sleep
  if (digitalRead(HELTEC_BUTTON_PIN) == LOW)
  {
    digitalWrite(VEXT_PIN, HIGH);
    Heltec.display->clear();
    Heltec.display->drawString(0, 0, "DEEP SLEEP");
    Heltec.display->display();
    delay(2000);
    esp_deep_sleep_start();
  }

  // Watchdog reset – ha a loop lefut rendesen, nem indul ujra az ESP32
  esp_task_wdt_reset();

}