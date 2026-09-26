---
id: sec-iot.m02.l02
lang: th
title: {th: กติกาการเข้าถึงชิป, en: The chip-access discipline}
summary: {th: ใช้ประตูเข้าชิป lock และการกันหน้าจอสัมผัสออกจากบัสขณะชิปทำงาน ตามลำดับที่ SDK กำหนด, en: 'Use the chip gate, lock and touch-hold in the order the SDK requires.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l01]
objectives:
- {th: 'เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release', en: 'Order init, acquire, use and release correctly, and explain what happens if release is forgotten.'}
- {th: อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ, en: 'Explain why touch-hold must wrap the whole transaction, not just its setup.'}
- {th: ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที, en: Identify work that must leave the display task because chip transactions take seconds.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release
2. อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ
3. ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ประตูเข้าชิปแบบ re-entrant
- lock และ touch-hold
- ธุรกรรมที่ใช้เวลานาน
- หน้าจอที่ถามสถานะแทนการรอ

## แหล่งอ้างอิง

- [SDK: cm33/security/03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c)
- [SDK: cm33/security/04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c)
- [D1 — The chip-access discipline: gate, lock, touch-hold (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html)
- [Chip gate & manager (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tesaiot__hsm__chip__manager.html)
