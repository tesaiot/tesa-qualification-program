---
id: edgeai-dev.m02.l02
lang: th
title: {th: เก็บเสียงและหลายเซนเซอร์บนเส้นเวลาเดียว, en: Audio and multi-sensor capture on one timeline}
summary: {th: เก็บเสียงจากไมโครโฟนบนบอร์ด และจัดข้อมูลจากหลายเซนเซอร์ให้อยู่บนเส้นเวลาเดียวกันเป็นฐานของชุดข้อมูล, en: Capture audio from the board microphone and align several sensors on one timeline as a dataset base.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [edgeai-dev.m02.l01]
objectives:
- {th: เก็บเสียงจากไมโครโฟนบนบอร์ดและบันทึกค่าระดับเสียงเป็นช่วงเวลา, en: Capture microphone audio and log sound levels over time.}
- {th: จัดข้อมูลจากเซนเซอร์อย่างน้อยสองตัวให้อยู่บนเส้นเวลาเดียวกัน และอธิบายวิธีจัดการเมื่ออัตราต่างกัน, en: Align at least two sensors on one timeline and explain how to handle different rates.}
develops:
- {skill: ai.data-collection, to: 3}
- {skill: sys.sensors-actuators, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เก็บเสียงจากไมโครโฟนบนบอร์ดและบันทึกค่าระดับเสียงเป็นช่วงเวลา
2. จัดข้อมูลจากเซนเซอร์อย่างน้อยสองตัวให้อยู่บนเส้นเวลาเดียวกัน และอธิบายวิธีจัดการเมื่ออัตราต่างกัน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s08/02_mic_sound_level_meter.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s08/02_mic_sound_level_meter.py)
- [SDK: cm55/sensors/01_feed_sensor_hub.c (ใครเป็นเจ้าของเลขลำดับ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/01_feed_sensor_hub.c)
