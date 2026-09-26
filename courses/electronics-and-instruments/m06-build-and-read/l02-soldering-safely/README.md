---
id: elec.m06.l02
lang: th
title: {th: บัดกรีอย่างปลอดภัย, en: Soldering safely}
summary: {th: บัดกรีจุดต่อที่ดี ตรวจงานด้วยตาและมัลติมิเตอร์ และทำงานอย่างปลอดภัยต่อตัวเองและบอร์ด, en: 'Make good joints, inspect by eye and multimeter, and work safely for yourself and the board.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l01]
objectives:
- {th: บัดกรีหัวต่อหนึ่งแถวที่ไม่มีจุดเย็นหรือสะพานตะกั่ว และตรวจด้วยมัลติมิเตอร์, en: Solder a header row with no cold joints or bridges and verify with a multimeter.}
- {th: ระบุข้อปฏิบัติด้านความปลอดภัยของงานบัดกรีได้อย่างน้อยสี่ข้อ เช่น การระบายควันและการป้องกันไฟฟ้าสถิต, en: 'Name at least four soldering safety practices, such as fume extraction and ESD protection.'}
develops:
- {skill: hwdev.soldering, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. บัดกรีหัวต่อหนึ่งแถวที่ไม่มีจุดเย็นหรือสะพานตะกั่ว และตรวจด้วยมัลติมิเตอร์
2. ระบุข้อปฏิบัติด้านความปลอดภัยของงานบัดกรีได้อย่างน้อยสี่ข้อ เช่น การระบายควันและการป้องกันไฟฟ้าสถิต

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- อุณหภูมิและหัวแร้ง
- จุดต่อที่ดีกับจุดเย็น
- การถอดและแก้งาน
- ความปลอดภัยและไฟฟ้าสถิต

## แหล่งอ้างอิง

- [Soldering (Wikipedia)](https://en.wikipedia.org/wiki/Soldering)
