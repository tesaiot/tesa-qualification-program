---
id: c-found.m05.l01
lang: th
title: {th: UART, en: UART}
summary: {th: เข้าใจเฟรมของ UART และกติกาเจ้าของพอร์ตเดียว แล้วยืนยันด้วย logic analyzer, en: 'Understand UART framing and the single-owner rule, and verify it with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l04]
objectives:
- {th: 'ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit', en: 'Decode one UART frame from a trace: start bit, data, parity and stop bit.'}
- {th: อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์, en: Explain why one UART port should have a single owner task that hands data on through a buffer.}
- {th: ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้, en: Set up a logic analyzer to decode UART at a given baud rate.}
develops:
- {skill: proto.uart, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit
2. อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์
3. ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- baud rate และเฟรม
- เจ้าของพอร์ตเดียว
- ring buffer กับการรับข้อมูล
- ถอดรหัสด้วย PulseView

## แหล่งอ้างอิง

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (UART มีเจ้าของเดียว)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [Universal asynchronous receiver-transmitter (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
