---
id: elec.m03.l02
lang: th
title: {th: วัดกระแสอย่างปลอดภัย, en: Measuring current safely}
summary: {th: ต่อมัลติมิเตอร์อนุกรมเพื่อวัดกระแส ย้ายสายวัดให้ถูกช่อง และเข้าใจว่าทำไมการวัดกระแสผิดวิธีทำให้ฟิวส์ขาด, en: 'Insert the meter in series to measure current, move the leads to the right jack, and see why doing it wrong blows fuses.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m03.l01]
objectives:
- {th: วัดกระแสของหลอด LED หนึ่งดวงโดยต่อมัลติมิเตอร์อนุกรมและใช้ช่องเสียบที่ถูกต้อง, en: Measure one LED's current with the meter in series using the correct jack.}
- {th: อธิบายว่าทำไมการต่อมัลติมิเตอร์ในโหมดวัดกระแสคร่อมแหล่งจ่ายจึงอันตราย, en: Explain why connecting a meter in current mode across a supply is dangerous.}
- {th: เทียบกระแสที่วัดได้กับค่าที่คำนวณจากกฎของโอห์ม และอธิบายความต่าง, en: Compare measured current with the Ohm's-law calculation and explain the difference.}
develops:
- {skill: meas.multimeter, to: 2}
- {skill: hw.circuits, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. วัดกระแสของหลอด LED หนึ่งดวงโดยต่อมัลติมิเตอร์อนุกรมและใช้ช่องเสียบที่ถูกต้อง
2. อธิบายว่าทำไมการต่อมัลติมิเตอร์ในโหมดวัดกระแสคร่อมแหล่งจ่ายจึงอันตราย
3. เทียบกระแสที่วัดได้กับค่าที่คำนวณจากกฎของโอห์ม และอธิบายความต่าง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- วัดอนุกรม
- ช่องเสียบและฟิวส์
- ความต้านทานของตัววัดเอง
- เทียบกับการคำนวณ

## แหล่งอ้างอิง

- [Multimeter (Wikipedia)](https://en.wikipedia.org/wiki/Multimeter)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
