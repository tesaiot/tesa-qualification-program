---
id: edgeai-dev.m01.l03
lang: th
title: {th: แกะแอป Edge AI, en: Taking an edge AI app apart}
summary: {th: ตามเส้นทางตั้งแต่ทะเบียนโมเดล การเลือกโมเดล ผลการจำแนก จนถึงสิ่งที่ขึ้นบนจอ, en: Follow the path from model registry and selection to the result and what appears on screen.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m01.l02]
objectives:
- {th: อธิบายเส้นทางจากการเลือกโมเดลจนถึงผลการจำแนกที่ขึ้นบนจอได้ครบทุกขั้น, en: Explain the full path from choosing a model to the result on screen.}
- {th: ดัดแปลงแอป Edge AI ให้เปลี่ยนโมเดลและเพิ่มการกระทำหนึ่งอย่างเมื่อได้ผลที่กำหนด, en: Remix an edge AI app to switch model and add one action on a given result.}
develops:
- {skill: ai.edge, to: 2}
- {skill: ai.model-deploy, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายเส้นทางจากการเลือกโมเดลจนถึงผลการจำแนกที่ขึ้นบนจอได้ครบทุกขั้น
2. ดัดแปลงแอป Edge AI ให้เปลี่ยนโมเดลและเพิ่มการกระทำหนึ่งอย่างเมื่อได้ผลที่กำหนด

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/02_model_registry.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/02_model_registry.c)
- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
