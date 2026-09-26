---
id: elec.m05.l01
lang: th
title: {th: ออสซิลโลสโคปเบื้องต้น, en: Oscilloscope basics}
summary: {th: 'ตั้ง timebase, volts/div และ trigger และต่อสายกราวด์ของโพรบให้ถูก', en: 'Set timebase, volts/div and trigger, and connect the probe ground properly.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m04.l02]
objectives:
- {th: 'ตั้ง timebase, volts/div และ trigger ให้เห็นสัญญาณนิ่งบนจอ', en: 'Set timebase, volts/div and trigger to get a stable trace.'}
- {th: อธิบายว่าทำไมสายกราวด์ของโพรบต้องต่อกับกราวด์ของวงจรและสั้นที่สุด, en: Explain why the probe ground must go to circuit ground and be as short as possible.}
- {th: อธิบายว่าออสซิลโลสโคปให้ข้อมูลอะไรที่ logic analyzer ให้ไม่ได้, en: Explain what an oscilloscope shows that a logic analyzer cannot.}
develops:
- {skill: meas.oscilloscope, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ตั้ง timebase, volts/div และ trigger ให้เห็นสัญญาณนิ่งบนจอ
2. อธิบายว่าทำไมสายกราวด์ของโพรบต้องต่อกับกราวด์ของวงจรและสั้นที่สุด
3. อธิบายว่าออสซิลโลสโคปให้ข้อมูลอะไรที่ logic analyzer ให้ไม่ได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- timebase และ volts/div
- trigger
- โพรบและกราวด์
- ขอบสัญญาณและ overshoot

## แหล่งอ้างอิง

- [Oscilloscope (Wikipedia)](https://en.wikipedia.org/wiki/Oscilloscope)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
