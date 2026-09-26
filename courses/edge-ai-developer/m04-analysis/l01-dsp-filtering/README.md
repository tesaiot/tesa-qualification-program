---
id: edgeai-dev.m04.l01
lang: th
title: {th: ฟิลเตอร์ DSP, en: DSP filtering}
summary: {th: ลดสัญญาณรบกวนด้วยฟิลเตอร์หลายแบบ และเลือกฟิลเตอร์จากผลที่วัดได้, en: Reduce noise with several filters and choose one from measured results.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m03.l02]
objectives:
- {th: เปรียบเทียบฟิลเตอร์อย่างน้อยสามแบบกับสัญญาณเดียวกัน ในด้านความเรียบและความหน่วง, en: Compare at least three filters on one signal for smoothness and lag.}
- {th: เลือกค่าพารามิเตอร์ของฟิลเตอร์จากความหน่วงที่ยอมรับได้ของงาน, en: Choose filter parameters from the lag the task can tolerate.}
develops:
- {skill: sys.dsp, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เปรียบเทียบฟิลเตอร์อย่างน้อยสามแบบกับสัญญาณเดียวกัน ในด้านความเรียบและความหน่วง
2. เลือกค่าพารามิเตอร์ของฟิลเตอร์จากความหน่วงที่ยอมรับได้ของงาน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s05/06_ema_time_constant.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/06_ema_time_constant.py)
- [AIoT in Action: examples/s05/08_six_filters_one_signal.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/08_six_filters_one_signal.py)
