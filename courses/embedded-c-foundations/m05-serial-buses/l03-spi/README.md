---
id: c-found.m05.l03
lang: th
title: {th: SPI, en: SPI}
summary: {th: เข้าใจโหมดของ SPI และสาย chip select แล้วยืนยันสัญญาณด้วย logic analyzer, en: 'Understand SPI modes and chip select, and verify signals with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l02]
objectives:
- {th: อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้, en: Explain the four SPI modes from CPOL and CPHA and match a device datasheet.}
- {th: 'ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS', en: 'Decode an SPI trace with SCLK, MOSI, MISO and CS.'}
- {th: เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว, en: 'Compare SPI and I2C on wire count, speed and multi-device wiring.'}
develops:
- {skill: proto.spi, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้
2. ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS
3. เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- CPOL และ CPHA
- chip select หลายตัว
- SDK ที่ commit นี้ยังไม่มีตัวอย่าง SPI โดยตรง บทนี้อ้าง PDL
- ถอดรหัสด้วย logic analyzer

## แหล่งอ้างอิง

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Serial Peripheral Interface (Wikipedia)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
