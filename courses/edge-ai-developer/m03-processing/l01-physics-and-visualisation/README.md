---
id: edgeai-dev.m03.l01
lang: th
title: {th: คณิตศาสตร์ ฟิสิกส์ และการแสดงผล, en: 'Maths, physics and visualisation'}
summary: {th: คำนวณมุมเอียง ความสูง พลังงาน และระดับเสียงจากค่าดิบ แล้วแสดงเป็นมาตรวัดบนจอ, en: 'Derive tilt, altitude, energy and sound level from raw values and show them as gauges.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m02.l02]
objectives:
- {th: คำนวณมุมเอียงจากค่าความเร่งสามแกนและตรวจกับการเอียงจริง, en: Compute tilt from three-axis acceleration and check it against real tilt.}
- {th: แสดงปริมาณที่คำนวณได้บนจอด้วย widget ที่เหมาะกับชนิดข้อมูล, en: Display a derived quantity with a widget suited to the data.}
develops:
- {skill: sys.sensors-actuators, to: 3}
- {skill: hw.math, to: 2}
- {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. คำนวณมุมเอียงจากค่าความเร่งสามแกนและตรวจกับการเอียงจริง
2. แสดงปริมาณที่คำนวณได้บนจอด้วย widget ที่เหมาะกับชนิดข้อมูล

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s06/03_tilt_from_gravity.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s06/03_tilt_from_gravity.py)
- [SDK: cm55/display/04_live_chart.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/display/04_live_chart.c)
