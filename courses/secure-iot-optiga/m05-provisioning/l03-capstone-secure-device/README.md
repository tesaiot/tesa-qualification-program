---
id: sec-iot.m05.l03
lang: th
title: {th: 'งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น', en: 'Capstone: one secure device'}
summary: {th: รวม threat model การลงทะเบียน mTLS และการอัปเดตแบบป้องกัน เป็นอุปกรณ์หนึ่งชิ้นพร้อมหลักฐาน, en: 'Combine the threat model, enrolment, mTLS and protected update into one device with evidence.'}
level: L3
time_min: {concept: 5, practise: 10, lab: 55, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l02]
objectives:
- {th: ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน, en: 'Deliver an enrolled device that connects over mTLS and publishes to the platform, with logs as evidence.'}
- {th: ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ, en: Update the module-one threat model to reflect implemented mitigations and remaining risks.}
develops:
- {skill: sec.fundamentals, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: soft.communication, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน
2. ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- รายการตรวจก่อนส่ง
- หลักฐานที่ต้องเก็บ
- ความเสี่ยงที่เหลือและแผนต่อไป

## แหล่งอ้างอิง

- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
