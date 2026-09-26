---
id: elec.m02.l02
lang: th
title: {th: 'Pull-up, pull-down และปุ่มกด', en: 'Pull-ups, pull-downs and buttons'}
summary: {th: ต่อปุ่มแบบ active-low ด้วย pull-up และเห็นการเด้งของหน้าสัมผัสจริงบน logic analyzer, en: Wire an active-low button with a pull-up and see real contact bounce on a logic analyzer.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m02.l01]
objectives:
- {th: อธิบายว่าทำไมขาเข้าที่ไม่มี pull-up หรือ pull-down จึงอ่านค่าไม่แน่นอน, en: Explain why an input without a pull-up or pull-down reads unpredictably.}
- {th: ต่อปุ่มแบบ active-low และอธิบายว่าทำไมกดแล้วอ่านได้ 0, en: Wire an active-low button and explain why pressing reads 0.}
- {th: วัดระยะเวลาการเด้งของปุ่มด้วย logic analyzer แล้วเลือกเวลากันเด้งจากข้อมูลที่วัดได้, en: Measure bounce duration with a logic analyzer and choose a debounce time from the data.}
develops:
- {skill: hw.digital, to: 2}
- {skill: mcu.gpio, to: 2}
- {skill: meas.logic-analyzer, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายว่าทำไมขาเข้าที่ไม่มี pull-up หรือ pull-down จึงอ่านค่าไม่แน่นอน
2. ต่อปุ่มแบบ active-low และอธิบายว่าทำไมกดแล้วอ่านได้ 0
3. วัดระยะเวลาการเด้งของปุ่มด้วย logic analyzer แล้วเลือกเวลากันเด้งจากข้อมูลที่วัดได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ขาลอย
- pull-up ภายในและภายนอก
- active-low
- การเด้งของหน้าสัมผัส

## แหล่งอ้างอิง

- [AIoT in Action: examples/s03/04_button_active_low.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/04_button_active_low.py)
- [AIoT in Action: examples/s03/05_debounce_count.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/05_debounce_count.py)
- [SDK: cm33/io/04_gpio_led_button.c (drive mode ของปุ่ม)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
