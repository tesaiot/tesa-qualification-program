---
id: elec.m02.l01
lang: th
title: {th: ระดับลอจิกและเกตพื้นฐาน, en: Logic levels and basic gates}
summary: {th: รู้ว่าแรงดันเท่าไรนับเป็น 0 หรือ 1 และทำไมการต่ออุปกรณ์ต่างระดับแรงดันจึงอันตราย, en: 'Know which voltages count as 0 or 1, and why mixing voltage levels is dangerous.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l03]
objectives:
- {th: อ่านค่าระดับลอจิกขาเข้าและขาออกจากเอกสารข้อมูลของชิป แล้วบอกได้ว่าสองอุปกรณ์ต่อกันตรงได้หรือไม่, en: Read input and output logic thresholds from datasheets and decide whether two devices can connect directly.}
- {th: 'เขียนตารางความจริงของเกต AND, OR, NOT, XOR และใช้แก้โจทย์เงื่อนไขง่าย ๆ ได้', en: 'Write truth tables for AND, OR, NOT and XOR and use them on simple conditions.'}
develops:
- {skill: hw.digital, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อ่านค่าระดับลอจิกขาเข้าและขาออกจากเอกสารข้อมูลของชิป แล้วบอกได้ว่าสองอุปกรณ์ต่อกันตรงได้หรือไม่
2. เขียนตารางความจริงของเกต AND, OR, NOT, XOR และใช้แก้โจทย์เงื่อนไขง่าย ๆ ได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ระดับลอจิก 3.3 V
- ขาลอยและสัญญาณรบกวน
- ตารางความจริง
- การแปลงระดับแรงดัน

## แหล่งอ้างอิง

- [Logic gate (Wikipedia)](https://en.wikipedia.org/wiki/Logic_gate)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
