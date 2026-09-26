---
id: edgeai-dev.m06.l01
lang: th
title: {th: โมเดลที่มีอยู่และ API ของ edge_ai, en: The shipped models and the edge_ai API}
summary: {th: สร้างแอปเฉพาะโมเดลหนึ่งตัว อ่านคะแนนและเวลาในการรัน และตรวจว่าโมเดลทำงานจริง, en: 'Build a single-model app, read scores and latency, and check the model is really running.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m05.l04]
objectives:
- {th: สร้างแอปเฉพาะโมเดลหนึ่งตัวที่แสดงผล คะแนน และเวลาในการรัน, en: 'Build a single-model app that shows result, score and latency.'}
- {th: ตรวจว่าโมเดลกำลังรันจริงจากตัวนับที่เพิ่มขึ้น ไม่ใช่จากผลล่าสุดที่อาจค้าง, en: 'Verify the model is running from increasing counters, not a possibly stale last result.'}
develops:
- {skill: ai.edge, to: 3}
- {skill: ai.model-deploy, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. สร้างแอปเฉพาะโมเดลหนึ่งตัวที่แสดงผล คะแนน และเวลาในการรัน
2. ตรวจว่าโมเดลกำลังรันจริงจากตัวนับที่เพิ่มขึ้น ไม่ใช่จากผลล่าสุดที่อาจค้าง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: cm55/edge_ai/03_parallel_set_run.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/03_parallel_set_run.c)
- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
