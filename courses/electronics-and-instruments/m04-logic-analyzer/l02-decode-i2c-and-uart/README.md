---
id: elec.m04.l02
lang: th
title: {th: ถอดรหัส I2C และ UART, en: Decoding I2C and UART}
summary: {th: ใช้ protocol decoder ของ sigrok อ่านธุรกรรม I2C และเฟรม UART จากบอร์ดจริง, en: Use sigrok protocol decoders to read I2C transactions and UART frames from a real board.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m04.l01]
objectives:
- {th: 'ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้', en: 'Set up the I2C decoder and read address, read/write and ACK from a bus scan.'}
- {th: ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด, en: Set up the UART decoder at the right baud rate and describe the symptoms of a wrong setting.}
develops:
- {skill: meas.logic-analyzer, to: 2}
- {skill: proto.i2c, to: 2}
- {skill: proto.uart, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้
2. ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- decoder ของ I2C
- decoder ของ UART
- เทียบภาพสัญญาณกับโค้ด
- หาความผิดพลาดจากภาพสัญญาณ

## แหล่งอ้างอิง

- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)
- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
