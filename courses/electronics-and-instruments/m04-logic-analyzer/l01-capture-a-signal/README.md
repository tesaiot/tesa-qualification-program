---
id: elec.m04.l01
lang: th
title: {th: จับสัญญาณดิจิทัลครั้งแรก, en: Capturing a first digital signal}
summary: {th: ต่อ logic analyzer เลือกอัตราสุ่มตัวอย่างและ trigger แล้ววัดเวลาของสัญญาณ, en: 'Connect a logic analyzer, choose sample rate and trigger, and time the signal.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m03.l02]
objectives:
- {th: ต่อสายกราวด์และสายสัญญาณของ logic analyzer กับบอร์ดได้ถูกต้อง, en: Connect the logic analyzer's ground and signal leads to the board correctly.}
- {th: เลือกอัตราสุ่มตัวอย่างที่เร็วพอสำหรับสัญญาณที่ต้องการวัด และอธิบายผลเมื่อช้าเกินไป, en: Choose a sample rate fast enough for the signal and explain what happens when it is too slow.}
- {th: วัดความกว้างพัลส์และความถี่ของสัญญาณไฟกะพริบจากภาพที่จับได้, en: Measure pulse width and frequency of a blink signal from a capture.}
develops:
- {skill: meas.logic-analyzer, to: 2}
- {skill: sys.dsp, to: 1}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ต่อสายกราวด์และสายสัญญาณของ logic analyzer กับบอร์ดได้ถูกต้อง
2. เลือกอัตราสุ่มตัวอย่างที่เร็วพอสำหรับสัญญาณที่ต้องการวัด และอธิบายผลเมื่อช้าเกินไป
3. วัดความกว้างพัลส์และความถี่ของสัญญาณไฟกะพริบจากภาพที่จับได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- กราวด์ร่วม
- อัตราสุ่มตัวอย่างและ aliasing
- trigger
- วัดเวลา

## แหล่งอ้างอิง

- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [Logic analyzer (Wikipedia)](https://en.wikipedia.org/wiki/Logic_analyzer)
- [AIoT in Action: examples/s03/02_led_blink.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/02_led_blink.py)
