---
id: elec.m01.l03
lang: th
title: {th: 'ชิ้นส่วนพื้นฐาน: ตัวต้านทาน ตัวเก็บประจุ ไดโอด และทรานซิสเตอร์', en: 'Basic components: resistors, capacitors, diodes and transistors'}
summary: {th: รู้จักหน้าที่ของชิ้นส่วนพื้นฐาน และใช้ทรานซิสเตอร์เป็นสวิตช์ขับโหลดที่ขาไมโครคอนโทรลเลอร์ขับเองไม่ได้, en: 'Know what the basic components do, and use a transistor as a switch for loads a pin cannot drive.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l02]
objectives:
- {th: คำนวณตัวต้านทานจำกัดกระแสของหลอด LED จากแรงดันแหล่งจ่าย แรงดันตกคร่อม LED และกระแสที่ต้องการ, en: 'Compute an LED current-limiting resistor from supply voltage, LED forward voltage and target current.'}
- {th: อธิบายหน้าที่ของตัวเก็บประจุ decoupling และไดโอดกันไฟย้อนในวงจรขับโหลดแบบขดลวด, en: Explain decoupling capacitors and flyback diodes on inductive loads.}
- {th: เลือกใช้ทรานซิสเตอร์หรือ MOSFET เป็นสวิตช์เมื่อโหลดต้องการกระแสเกินขาของไมโครคอนโทรลเลอร์, en: Choose a transistor or MOSFET switch when a load needs more current than a pin supplies.}
develops:
- {skill: hw.electronics, to: 2}
- {skill: hwdev.design-basics, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. คำนวณตัวต้านทานจำกัดกระแสของหลอด LED จากแรงดันแหล่งจ่าย แรงดันตกคร่อม LED และกระแสที่ต้องการ
2. อธิบายหน้าที่ของตัวเก็บประจุ decoupling และไดโอดกันไฟย้อนในวงจรขับโหลดแบบขดลวด
3. เลือกใช้ทรานซิสเตอร์หรือ MOSFET เป็นสวิตช์เมื่อโหลดต้องการกระแสเกินขาของไมโครคอนโทรลเลอร์

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- LED และตัวต้านทานจำกัดกระแส
- ตัวเก็บประจุ decoupling
- ไดโอดกันไฟย้อน
- MOSFET เป็นสวิตช์

## แหล่งอ้างอิง

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [AIoT in Action: examples/s03/03_led_brightness.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py)
