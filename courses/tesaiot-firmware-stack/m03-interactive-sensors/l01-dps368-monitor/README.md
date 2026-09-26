---
id: fw-stack.m03.l01
lang: th
title:
  th: "อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C"
  en: "Pressure and temperature from the DPS368 over I2C"
summary:
  th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL"
  en: "Pressure and temperature from the DPS368 over I2C"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ"
    en: "Read pressure and temperature from the DPS368 over I2C and show them on screen"
  - th: "อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode"
    en: "Explain the driver → reader → presenter → view layering of the episode"
  - th: "ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง"
    en: "Check the reading against a local reference pressure and explain the difference"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep01_dps368_monitor"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C

## เป้าหมาย

1. อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ
2. อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode
3. ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง

## แนวคิด

อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/main_example.c)
- [`app_sensor/app_dps368_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.c)
- [`app_sensor/app_dps368_service.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.h)
- [`app_sensor/dps368/dps368_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_config.h)
- [`app_sensor/dps368/dps368_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_driver.c)
- และอีก 12 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP01 — DPS368 Monitor บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/int_ep01_dps368_monitor.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ชั้น presenter ทำอะไรที่ view ไม่ทำ
- ความดันควรเปลี่ยนอย่างไรเมื่อยกบอร์ดขึ้นสูงหนึ่งชั้นตึก
- ถ้าเซนเซอร์ตอบ I2C ไม่ได้ ข้อความผิดพลาดควรขึ้นที่ชั้นใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
