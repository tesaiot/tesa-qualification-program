---
id: edgeai-dev.m04.l03
lang: th
title: {th: Feature และการแบ่งหน้าต่าง, en: Features and windowing}
summary: {th: แบ่งสัญญาณเป็นหน้าต่าง สร้าง feature และเข้าใจว่าโมเดลเห็นข้อมูลแบบไหน, en: 'Window signals, build features and understand what the model actually sees.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m04.l02]
objectives:
- {th: เลือกขนาดหน้าต่างและระยะเลื่อนให้เหมาะกับเหตุการณ์ที่ต้องการจับ, en: Choose window size and hop to fit the event to detect.}
- {th: สร้าง feature vector จากข้อมูลดิบให้ได้ผลเหมือนเดิมทุกครั้ง และอธิบายว่าทำไมขั้นตอนเตรียมข้อมูลต้องเหมือนกันตอนฝึกและตอนใช้งาน, en: Build a reproducible feature vector from raw data and explain why preprocessing must match between training and inference.}
develops:
- {skill: sys.dsp, to: 3}
- {skill: ai.data-collection, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เลือกขนาดหน้าต่างและระยะเลื่อนให้เหมาะกับเหตุการณ์ที่ต้องการจับ
2. สร้าง feature vector จากข้อมูลดิบให้ได้ผลเหมือนเดิมทุกครั้ง และอธิบายว่าทำไมขั้นตอนเตรียมข้อมูลต้องเหมือนกันตอนฝึกและตอนใช้งาน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s08/07_mic_window_stats.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s08/07_mic_window_stats.py)
- [LiteRT (เดิมชื่อ TensorFlow Lite) documentation](https://ai.google.dev/edge/litert)
