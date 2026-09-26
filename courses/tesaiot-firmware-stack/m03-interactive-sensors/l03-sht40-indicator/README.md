---
id: fw-stack.m03.l03
lang: th
title:
  th: "ตัวบ่งชี้ความชื้นและอุณหภูมิจาก SHT4x"
  en: "Humidity and temperature indicator from the SHT4x"
summary:
  th: "วัดความชื้นสัมพัทธ์และอุณหภูมิด้วยเซนเซอร์ Sensirion SHT4x บน I2C แล้วแสดงผลเป็นตัวบ่งชี้บนจอ LVGL"
  en: "Humidity and temperature indicator from the SHT4x"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l02]
objectives:
  - th: "อ่านความชื้นสัมพัทธ์และอุณหภูมิจาก SHT4x ผ่าน I2C แล้วแสดงเป็นตัวบ่งชี้"
    en: "Read relative humidity and temperature from the SHT4x over I2C and show them as indicators"
  - th: "ตั้งเกณฑ์สีของตัวบ่งชี้จากช่วงความชื้นที่สบาย และอธิบายที่มาของเกณฑ์"
    en: "Set the indicator colour thresholds from a comfort humidity range and justify them"
  - th: "เปรียบเทียบอุณหภูมิจาก SHT4x กับ DPS368 และอธิบายว่าทำไมอาจไม่เท่ากัน"
    en: "Compare the SHT4x and DPS368 temperatures and explain why they may differ"
develops:
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: proto.i2c, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep03_sht40_indicator"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# ตัวบ่งชี้ความชื้นและอุณหภูมิจาก SHT4x

## เป้าหมาย

1. อ่านความชื้นสัมพัทธ์และอุณหภูมิจาก SHT4x ผ่าน I2C แล้วแสดงเป็นตัวบ่งชี้
2. ตั้งเกณฑ์สีของตัวบ่งชี้จากช่วงความชื้นที่สบาย และอธิบายที่มาของเกณฑ์
3. เปรียบเทียบอุณหภูมิจาก SHT4x กับ DPS368 และอธิบายว่าทำไมอาจไม่เท่ากัน

## แนวคิด

### SHT4x คืออะไร และตัวเลขในสเปกหมายถึงอะไร

SHT4x (SHT40/41/45) เป็นเซนเซอร์วัดความชื้นสัมพัทธ์ (RH%) และอุณหภูมิของ Sensirion รุ่น SHT40 แม่นยำ ±1.8 %RH และ
±0.2 °C วัด RH ได้ 0–100% และอุณหภูมิ -40 ถึง +125 °C กินไฟเฉลี่ยต่ำกว่า 0.4 µA ที่อัตราวัด 1 ครั้ง/วินาที
ต่างจาก DPS368/BMI270 ตรงที่ SHT4x ไม่มี register map ให้อ่าน-เขียนทีละ address แต่คุยกันด้วย **command-based
protocol**: ส่ง 1 byte สั่งวัด แล้วรอ conversion delay (สูงสุดราว 8.2 ms ที่ high precision) ก่อนอ่านผลกลับ 6
byte พร้อม CRC-8 ตรวจสอบความถูกต้อง (polynomial `0x31` ตามมาตรฐานของ Sensirion) — โปรโตคอลระดับนี้เป็นความรู้จริง
ของเซนเซอร์ตระกูลนี้ แต่ **ไม่ได้ถูกเขียนเองในไฟล์ของ episode นี้เลย**

### ทำไมต้องรู้ว่าโค้ดชั้นไหนทำอะไรจริง

`sht4x_driver.c` ของ episode นี้ไม่ได้ส่ง command byte, รอ delay, หรือคำนวณ CRC-8/สูตรแปลงหน่วยเอง — มันเรียก
`mtb_sht4x_measure_high_precision(i2c_bus, &temp_milli_c, &hum_milli_rh)` ของมิดเดิลแวร์ Infineon ตัวเดียว ซึ่ง
ทำทุกขั้นตอน (ส่ง command `0xFD`, รอ delay, อ่าน 6 byte, ตรวจ CRC, แปลงหน่วยตามสูตร Sensirion) ไว้ให้เสร็จแล้ว คืน
ค่ากลับมาเป็น**หน่วย milli** (milli-°C, milli-%RH) — โค้ดของ episode แค่หาร 1000 เพื่อแปลงเป็นหน่วยปกติ
(`temperature_c`, `humidity_rh`) โปรโตคอลระดับ byte ที่ README ต้นทางอธิบายไว้ละเอียดจึงเป็นสิ่งที่**เกิดขึ้นจริง
บนสาย I2C** แต่ซ่อนอยู่ในมิดเดิลแวร์ ไม่ใช่โค้ดที่ episode นี้ให้นักเรียนอ่าน — เหมือนกับที่ DPS368 (บทเรียน 3.1)
ใช้ `xensiv_dps3xx_read()` และ BMI270 (บทเรียน 3.2) ใช้ config file ของ Bosch: รูปแบบซ้ำของซีรีส์นี้คือห่อโปรโตคอล
ระดับ byte ไว้ในไลบรารีของผู้ผลิตเซนเซอร์เสมอ

### เกณฑ์สีจริงมีแค่ 3 โซน ไม่ใช่ 4 โซนตามที่ README ต้นทางอธิบาย

`sht4x_view.c` มีฟังก์ชัน `hum_level_color()` และ `set_comfort_chip()` ที่ใช้เกณฑ์เดียวกันคือ **RH < 40% = Dry
(สีเหลืองอำพัน), 40–60% = Comfort (สีเขียว), RH > 60% = Humid (สีน้ำเงิน)** — มีแค่สองจุดตัด (40 กับ 60) ไม่ใช่
สามจุดตัด (30/60/80) และไม่มีโซน "อันตราย" สีแดงแยกต่างหากตามที่ README ต้นทางอธิบาย ช่วง comfort 40–60% ตรงกับ
คำแนะนำทั่วไปของ HVAC/ASHRAE สำหรับความชื้นในอาคารที่สบายและลดการเติบโตของเชื้อรา/ไรฝุ่น

### เกณฑ์สีถูกกำหนดซ้ำสองที่ ต้องแก้พร้อมกันเสมอ

`hum_level_color()` (กำหนดสีของ chip) และ `set_comfort_chip()` (กำหนดข้อความ "Dry"/"Comfort"/"Humid") เป็นสอง
ฟังก์ชัน**แยกกัน** แต่ต่างก็ hard-code ค่า 40.0f และ 60.0f ของตัวเอง ไม่ได้แชร์ constant เดียวกัน — ถ้าแก้เกณฑ์ใน
ฟังก์ชันเดียวโดยลืมอีกฟังก์ชัน จะได้ข้อความกับสีที่ไม่ตรงกัน (เช่น ข้อความขึ้น "Humid" แต่สียังเป็นสีเขียวของ
"Comfort")

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md) เพื่อเข้าใจความรู้เรื่องโปรโตคอลของ SHT4x แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะโปรโตคอลระดับ byte อยู่ในมิดเดิลแวร์ ไม่ใช่ในไฟล์ของ episode และเกณฑ์สีจริงต่างจากที่ README ต้นทางอธิบาย

[`app_sensor/sht4x/sht4x_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.c) — เรียกมิดเดิลแวร์ตัวเดียว ไม่มี command byte/CRC ในไฟล์นี้:

```c
cy_rslt_t sht4x_driver_read_sample(sht4x_sample_t *sample)
{
    int32_t temp_milli_c = 0;
    int32_t hum_milli_rh = 0;

    cy_rslt_t rslt = mtb_sht4x_measure_high_precision(s_i2c_bus, &temp_milli_c, &hum_milli_rh);
    if (CY_RSLT_SUCCESS != rslt)
    {
        return rslt;
    }

    /* Middleware returns milli-units; convert once here for UI/presenter layers. */
    sample->temperature_c = ((float)temp_milli_c) / 1000.0f;
    sample->humidity_rh = ((float)hum_milli_rh) / 1000.0f;
    return CY_RSLT_SUCCESS;
}
```

[`app_ui/sht4x/sht4x_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_ui/sht4x/sht4x_view.c) — เกณฑ์สีตัวจริง สามโซน สองจุดตัด:

```c
static lv_color_t hum_level_color(float humidity_rh)
{
    if (humidity_rh < 40.0f)
    {
        return lv_color_hex(0xD97706);   /* Dry */
    }

    if (humidity_rh <= 60.0f)
    {
        return lv_color_hex(0x16A34A);   /* Comfort */
    }

    return lv_color_hex(0x2563EB);       /* Humid */
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/main_example.c) ส่ง I2C handle เข้า `sht4x_presenter_start()` ตรงตามที่ README ต้นทางอธิบาย
- [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_config.h) — `SHT4X_SAMPLE_PERIOD_MS = 1000` (poll ด้วย `lv_timer` เดียวบน LVGL thread แบบเดียวกับบทเรียน 3.1–3.2) และที่อยู่ I2C หลัก/สำรอง
- ดูโฟลเดอร์เต็มที่ [`int_ep03_sht40_indicator/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator)

## จุดที่มักพลาด

- **คิดว่าต้องเขียน command byte/CRC-8 เองในโค้ดของ episode นี้** — โปรโตคอลระดับ byte ถูกทำใน
  `mtb_sht4x_measure_high_precision()` ของมิดเดิลแวร์แล้ว ไฟล์ `sht4x_driver.c` ของ episode แค่เรียกมันแล้วแปลง
  หน่วยจาก milli เป็นหน่วยปกติ
- **จำเกณฑ์สีผิดเป็น 4 โซน (30/60/80%)** — เกณฑ์จริงมีแค่ 3 โซนที่จุดตัด 40% และ 60% ไม่มีโซนสีแดง "อันตราย"
  แยกต่างหาก
- **แก้เกณฑ์สีแค่ฟังก์ชันเดียว** — `hum_level_color()` และ `set_comfort_chip()` มีค่า 40.0f/60.0f แยกกันคนละที่
  ต้องแก้พร้อมกันเสมอ ไม่งั้นข้อความกับสีจะไม่ตรงกัน

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP03 — SHT40 Indicator บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/int_ep03_sht40_indicator.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ความชื้นสัมพัทธ์ขึ้นกับอุณหภูมิอย่างไร
- ทำไมเซนเซอร์สองตัวบนบอร์ดเดียวกันอ่านอุณหภูมิไม่เท่ากัน
- เกณฑ์สีของคุณใช้ช่วงความชื้นเท่าไร และอ้างอิงจากอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
