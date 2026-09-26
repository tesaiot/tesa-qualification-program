---
id: elec.m05.l02
lang: th
title: {th: วัด PWM, en: Measuring PWM}
summary: {th: 'วัด period, ความถี่ และ duty cycle ของสัญญาณ PWM ที่หรี่หลอด LED และเทียบกับค่าที่โปรแกรมสั่ง', en: 'Measure period, frequency and duty cycle of the PWM dimming an LED and compare with the commanded value.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m05.l01]
objectives:
- {th: วัด period ความถี่ และ duty cycle ของ PWM จากรูปคลื่นได้, en: 'Measure PWM period, frequency and duty cycle from the waveform.'}
- {th: เทียบ duty cycle ที่วัดได้กับค่าที่โปรแกรมสั่ง และอธิบายเมื่อไม่ตรงกัน, en: Compare measured duty cycle with the commanded value and explain any mismatch.}
develops:
- {skill: meas.oscilloscope, to: 2}
- {skill: mcu.pwm, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. วัด period ความถี่ และ duty cycle ของ PWM จากรูปคลื่นได้
2. เทียบ duty cycle ที่วัดได้กับค่าที่โปรแกรมสั่ง และอธิบายเมื่อไม่ตรงกัน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- period และความถี่
- duty cycle
- PWM ของฮาร์ดแวร์กับพัลส์จากซอฟต์แวร์
- สิ่งที่ตาเห็นกับสิ่งที่วัดได้

## แหล่งอ้างอิง

- [AIoT in Action: examples/s03/03_led_brightness.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py)
- [Oscilloscope (Wikipedia)](https://en.wikipedia.org/wiki/Oscilloscope)
