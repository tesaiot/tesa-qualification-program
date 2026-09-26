---
id: elec.m06.l04
lang: th
title: {th: พื้นฐาน PCB และ EMC, en: PCB and EMC basics}
summary: {th: เข้าใจหลักการวางชิ้นส่วน กราวด์ และเส้นทางสัญญาณที่ลดปัญหาสัญญาณรบกวนและการแผ่คลื่น, en: 'Understand placement, grounding and routing principles that reduce noise and emissions.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l03]
objectives:
- {th: อธิบายหน้าที่ของระนาบกราวด์และตัวเก็บประจุ decoupling ที่วางชิดขาไฟของชิป, en: Explain the ground plane and decoupling capacitors placed close to chip power pins.}
- {th: ระบุปัจจัยที่ทำให้บอร์ดแผ่คลื่นรบกวนหรือไวต่อสัญญาณรบกวนได้อย่างน้อยสามข้อ, en: Name at least three factors that make a board emit or pick up interference.}
- {th: อธิบายว่าทำไมผลิตภัณฑ์ที่มีวิทยุหรือไฟฟ้าต้องผ่านการทดสอบมาตรฐานก่อนวางขาย, en: Explain why products with radios or electronics must pass standards testing before sale.}
develops:
- {skill: hwdev.pcb-emc, to: 2}
- {skill: test.standards, to: 1}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายหน้าที่ของระนาบกราวด์และตัวเก็บประจุ decoupling ที่วางชิดขาไฟของชิป
2. ระบุปัจจัยที่ทำให้บอร์ดแผ่คลื่นรบกวนหรือไวต่อสัญญาณรบกวนได้อย่างน้อยสามข้อ
3. อธิบายว่าทำไมผลิตภัณฑ์ที่มีวิทยุหรือไฟฟ้าต้องผ่านการทดสอบมาตรฐานก่อนวางขาย

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ชั้นของแผ่นวงจรและระนาบกราวด์
- decoupling
- loop area และขอบสัญญาณ
- การทดสอบ EMC ก่อนวางขาย

## แหล่งอ้างอิง

- [Printed circuit board (Wikipedia)](https://en.wikipedia.org/wiki/Printed_circuit_board)
- [Electromagnetic compatibility (Wikipedia)](https://en.wikipedia.org/wiki/Electromagnetic_compatibility)
