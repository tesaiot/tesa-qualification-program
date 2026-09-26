---
id: elec.m06.l01
lang: th
title: {th: ต่อวงจรบนเบรดบอร์ด, en: Breadboarding}
summary: {th: รู้ว่ารูบนเบรดบอร์ดเชื่อมกันอย่างไร และต่อวงจรตามแผนผังให้ตรวจง่าย, en: Know how breadboard holes connect and build circuits from a schematic that are easy to check.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m05.l02]
objectives:
- {th: ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง, en: Identify which rows and rails are connected on a breadboard.}
- {th: ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ, en: Build from a schematic with conventional wire colours and check with a multimeter before powering.}
develops:
- {skill: hwdev.breadboard, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง
2. ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- โครงสร้างของเบรดบอร์ด
- สีสายและการจัดวาง
- ตรวจก่อนจ่ายไฟ
- ข้อจำกัดของเบรดบอร์ดกับสัญญาณเร็ว

## แหล่งอ้างอิง

- [Breadboard (Wikipedia)](https://en.wikipedia.org/wiki/Breadboard)
