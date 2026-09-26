---
id: elec.m01.l02
lang: th
title: {th: วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก, en: Voltage dividers and analog sensors}
summary: {th: เข้าใจลูกบิดบนบอร์ดในฐานะวงจรแบ่งแรงดัน และแปลงค่าที่ ADC อ่านได้เป็นโวลต์, en: Understand the board's knob as a voltage divider and convert ADC counts to volts.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l01]
objectives:
- {th: คำนวณแรงดันขาออกของวงจรแบ่งแรงดันจากค่าตัวต้านทานสองตัว, en: Compute the output of a voltage divider from two resistor values.}
- {th: แปลงค่าที่ ADC อ่านได้เป็นแรงดันจากความละเอียดและแรงดันอ้างอิง แล้วเทียบกับมัลติมิเตอร์, en: 'Convert ADC counts to volts from resolution and reference, and compare with a multimeter.'}
- {th: อธิบายผลของความต้านทานขาเข้าของ ADC ต่อความแม่นยำของวงจรแบ่งแรงดัน, en: Explain how ADC input impedance affects divider accuracy.}
develops:
- {skill: hw.circuits, to: 2}
- {skill: mcu.adc-dac, to: 2}
- {skill: sys.sensors-actuators, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. คำนวณแรงดันขาออกของวงจรแบ่งแรงดันจากค่าตัวต้านทานสองตัว
2. แปลงค่าที่ ADC อ่านได้เป็นแรงดันจากความละเอียดและแรงดันอ้างอิง แล้วเทียบกับมัลติมิเตอร์
3. อธิบายผลของความต้านทานขาเข้าของ ADC ต่อความแม่นยำของวงจรแบ่งแรงดัน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- วงจรแบ่งแรงดัน
- ลูกบิดเป็นวงจรแบ่งแรงดันที่ปรับได้
- ADC: ความละเอียดและแรงดันอ้างอิง
- เทียบกับมัลติมิเตอร์

## แหล่งอ้างอิง

- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)
- [AIoT in Action: examples/s05/03_pot_setpoint_deadband.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/03_pot_setpoint_deadband.py)
- [SDK: cm33/io/03_read_potentiometers.c (raw, percent และ volts)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/03_read_potentiometers.c)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
