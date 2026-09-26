---
id: edgeai-dev.m07.l02
lang: th
title: {th: ต่อเติมด้วยโมเดลของตัวเอง, en: Extending with your own model}
summary: {th: เพิ่มโมเดลที่ฝึกเองเข้าเฟิร์มแวร์ ให้ปรากฏในทะเบียนและรันบนบอร์ด, en: Add your own trained model to the firmware so it appears in the registry and runs on the board.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [edgeai-dev.m07.l01]
objectives:
- {th: ลงทะเบียนโมเดลของตัวเองให้ปรากฏในรายการโมเดลและรันบนบอร์ดได้, en: Register your own model so it appears in the model list and runs on the board.}
- {th: วินิจฉัยได้ว่าเมื่อโมเดลไม่ให้ผล สาเหตุอยู่ที่ขั้นใดจากตัวนับของเอนจิน, en: Diagnose from engine counters at which step a silent model fails.}
develops:
- {skill: ai.model-deploy, to: 3}
- {skill: lang.c, to: 3}
- {skill: build.vendor-sdk, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ลงทะเบียนโมเดลของตัวเองให้ปรากฏในรายการโมเดลและรันบนบอร์ดได้
2. วินิจฉัยได้ว่าเมื่อโมเดลไม่ให้ผล สาเหตุอยู่ที่ขั้นใดจากตัวนับของเอนจิน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/05_register_model.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/05_register_model.c)
- [SDK: cm55/edge_ai/06_staged_load.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/06_staged_load.c)
- [SDK: cm55/edge_ai/10_model_load_diagnosis.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c)
- [SDK: proj_cm55/modules/ai_models/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/modules/ai_models/README.md)
