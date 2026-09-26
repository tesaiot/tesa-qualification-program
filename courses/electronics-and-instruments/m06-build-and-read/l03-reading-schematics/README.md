---
id: elec.m06.l03
lang: th
title: {th: อ่านแผนผังวงจร, en: Reading schematics}
summary: {th: อ่านสัญลักษณ์ ชื่อสัญญาณ และบล็อกของแผนผังวงจร แล้วตามสัญญาณจากขาชิปไปถึงชิ้นส่วน, en: 'Read symbols, net names and blocks, and trace a signal from a chip pin to a component.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l02]
objectives:
- {th: ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้, en: Identify basic component symbols and net names on a schematic.}
- {th: ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้, en: Trace one signal from a microcontroller pin to an LED or button on a board schematic.}
develops:
- {skill: hwdev.design-basics, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้
2. ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- สัญลักษณ์และชื่อสัญญาณ
- แผนผังหลายหน้าและ hierarchy
- เอกสารข้อมูลของชิ้นส่วน
- จากแผนผังถึงบอร์ดจริง

## แหล่งอ้างอิง

- [Circuit diagram (Wikipedia)](https://en.wikipedia.org/wiki/Circuit_diagram)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
