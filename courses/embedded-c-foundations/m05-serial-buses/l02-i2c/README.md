---
id: c-found.m05.l02
lang: th
title: {th: I2C, en: I2C}
summary: {th: สแกนบัส อ่านเขียนรีจิสเตอร์ของอุปกรณ์ และใช้ lock ของบัสร่วมกับงานอื่นอย่างถูกต้อง, en: 'Scan the bus, read and write device registers, and share the bus lock correctly with other tasks.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l01]
objectives:
- {th: สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้, en: Scan the I2C bus and identify devices by address.}
- {th: อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง, en: Read and write device registers while holding the bus lock for one whole transaction and always releasing it.}
- {th: 'ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop', en: 'Decode an I2C trace: start, address, read/write, ACK/NACK and stop.'}
develops:
- {skill: proto.i2c, to: 3}
- {skill: meas.logic-analyzer, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้
2. อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง
3. ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- address และ ACK
- lock ของบัสและเจ้าของหลายราย
- อ่าน chip ID ก่อนเชื่อ driver
- ถอดรหัสด้วย logic analyzer

## แหล่งอ้างอิง

- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [SDK: cm33/sensors/06_raw_register_access.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/sensors/02_read_imu.c (พิสูจน์สายก่อนเชื่อ driver)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c)
- [J1 — The sensor bus and its lock (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — DFR0522 RGB Dot Matrix](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix) — ควบคุม DFRobot DFR0522 RGB matrix 8x16 (I2C 0x10) บน bus 3.3V ร่วมกับ display แสดง clear/fill/pixel/pattern ผ่าน LVGL UI
- [EP01 — DPS368 Monitor](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) — อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL
