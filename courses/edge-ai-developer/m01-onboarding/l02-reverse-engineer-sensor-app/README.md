---
id: edgeai-dev.m01.l02
lang: th
title: {th: แกะแอปเซนเซอร์ทีละส่วน, en: Taking a sensor app apart}
summary: {th: รันแอปเซนเซอร์ที่เสร็จแล้ว แยกโครงสร้างของมัน แล้วดัดแปลงเป็นของตัวเอง, en: 'Run a finished sensor app, separate its structure, then remix it.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m01.l01]
objectives:
- {th: ระบุโครงสร้างร่วมของแอป MicroPython บนบอร์ด คือ import สร้างของครั้งเดียว วนลูป และ ui.poll, en: 'Identify the shared structure of a board MicroPython app: imports, create-once, loop and ui.poll.'}
- {th: ดัดแปลงแอปเซนเซอร์หนึ่งแอปให้ใช้เซนเซอร์หรือการแสดงผลต่างจากเดิม และอธิบายส่วนที่แก้, en: 'Remix a sensor app to use a different sensor or display, explaining each change.'}
develops:
- {skill: sys.sensors-actuators, to: 2}
- {skill: lang.micropython, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ระบุโครงสร้างร่วมของแอป MicroPython บนบอร์ด คือ import สร้างของครั้งเดียว วนลูป และ ui.poll
2. ดัดแปลงแอปเซนเซอร์หนึ่งแอปให้ใช้เซนเซอร์หรือการแสดงผลต่างจากเดิม และอธิบายส่วนที่แก้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s01/12_every_sense_at_once.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/12_every_sense_at_once.py)
- [AIoT in Action: examples/s06/03_tilt_from_gravity.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s06/03_tilt_from_gravity.py)
