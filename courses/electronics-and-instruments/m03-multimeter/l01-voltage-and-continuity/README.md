---
id: elec.m03.l01
lang: th
title: {th: วัดแรงดันและความต่อเนื่อง, en: Measuring voltage and continuity}
summary: {th: เลือกโหมดและย่านวัด วัดแรงดันขนานกับจุดที่ต้องการ และตรวจสายขาดหรือลัดวงจรด้วยโหมดความต่อเนื่อง, en: 'Pick mode and range, measure voltage in parallel, and find breaks or shorts with continuity mode.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m02.l02]
objectives:
- {th: วัดแรงดันที่จุดทดสอบบนบอร์ดโดยเลือกโหมดและย่านวัดถูกต้อง, en: Measure voltage at board test points with the right mode and range.}
- {th: ตรวจความต่อเนื่องของสายและหาจุดลัดวงจรบนวงจรที่ปิดไฟแล้ว, en: Check continuity and find shorts on an unpowered circuit.}
develops:
- {skill: meas.multimeter, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. วัดแรงดันที่จุดทดสอบบนบอร์ดโดยเลือกโหมดและย่านวัดถูกต้อง
2. ตรวจความต่อเนื่องของสายและหาจุดลัดวงจรบนวงจรที่ปิดไฟแล้ว

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- โหมดและย่านวัด
- วัดแรงดันแบบขนาน
- โหมดความต่อเนื่อง
- ปิดไฟก่อนวัดความต้านทาน

## แหล่งอ้างอิง

- [Multimeter (Wikipedia)](https://en.wikipedia.org/wiki/Multimeter)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
