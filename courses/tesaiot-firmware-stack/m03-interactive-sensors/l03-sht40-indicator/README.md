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
translation: pending
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

วัดความชื้นสัมพัทธ์และอุณหภูมิด้วยเซนเซอร์ Sensirion SHT4x บน I2C แล้วแสดงผลเป็นตัวบ่งชี้บนจอ LVGL

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/main_example.c)
- [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_config.h)
- [`app_sensor/sht4x/sht4x_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.c)
- [`app_sensor/sht4x/sht4x_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.h)
- [`app_sensor/sht4x/sht4x_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_reader.c)
- และอีก 6 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
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
