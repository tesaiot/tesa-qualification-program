---
id: sec-iot.m04.l01
lang: th
title: {th: Secure boot และ chain of trust, en: Secure boot and the chain of trust}
summary: {th: ตามลำดับการบูตของบอร์ดและดูว่าแต่ละขั้นตรวจขั้นถัดไปอย่างไร, en: Follow the board's boot order and how each stage checks the next.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l02]
objectives:
- {th: อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์, en: Explain the role of the CM33_S core in the template's secure boot.}
- {th: วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด, en: Draw the chain of trust from ROM to application and mark where signatures are checked.}
- {th: อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์, en: Explain the difference between secure boot and firmware encryption.}
develops:
- {skill: sec.secure-boot, to: 3}
- {skill: mcu.bootloader, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์
2. วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด
3. อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ลำดับการบูตสามคอร์
- root of trust
- การตรวจลายเซ็นทีละขั้น
- สิ่งที่ secure boot ไม่ได้ป้องกัน

## แหล่งอ้างอิง

- [SDK: แม่แบบ mtb-only README (CM33_S secure boot)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [B1 — CM33_NS boot walk-through (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [PSA Certified](https://www.psacertified.org/)
