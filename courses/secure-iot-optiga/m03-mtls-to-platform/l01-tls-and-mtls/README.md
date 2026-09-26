---
id: sec-iot.m03.l01
lang: th
title: {th: TLS และ mTLS, en: TLS and mTLS}
summary: {th: เข้าใจ handshake ของ TLS 1.3 และสิ่งที่เพิ่มขึ้นเมื่ออุปกรณ์ต้องยืนยันตัวตนด้วยใบรับรองของตัวเอง, en: Understand the TLS 1.3 handshake and what changes when the device authenticates with its own certificate.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l02]
objectives:
- {th: วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน, en: Draw the TLS 1.3 handshake and mark where server and device prove their identity.}
- {th: อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา, en: Explain that with a secure element the handshake signature happens inside the chip and the private key never leaves.}
- {th: วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ, en: Diagnose at least three common causes of TLS connection failure.}
develops:
- {skill: sec.tls, to: 3}
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน
2. อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา
3. วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- handshake ของ TLS 1.3
- ใบรับรองของเซิร์ฟเวอร์และของอุปกรณ์
- ตัวตนจาก OPTIGA ใน TLS
- เวลาของอุปกรณ์กับอายุใบรับรอง

## แหล่งอ้างอิง

- [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) — Unified, beginner-friendly C example that can send telemetry over either:
- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) — Unified, intermediate-level C example that can send telemetry over either:
