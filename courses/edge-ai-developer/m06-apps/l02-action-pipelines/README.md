---
id: edgeai-dev.m06.l02
lang: th
title: {th: ท่อการกระทำ (action pipeline), en: Action pipelines}
summary: {th: เปลี่ยนผลของโมเดลเป็นการกระทำ เช่น ไฟ เสียง หรือบันทึก โดยกันผลที่แกว่งและการเตือนผิด, en: 'Turn model results into actions such as light, sound or logging, guarding against flapping and false alarms.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m06.l01]
objectives:
- {th: ออกแบบเงื่อนไขยืนยันผลหลายครั้งก่อนลงมือ และวัดว่าลดการเตือนผิดได้เท่าไร, en: Design an N-confirmation rule before acting and measure how much it cuts false alarms.}
- {th: อธิบายการแลกเปลี่ยนระหว่างความเร็วในการตอบสนองกับการเตือนผิด, en: Explain the trade-off between response speed and false alarms.}
develops:
- {skill: ai.edge, to: 3}
- {skill: prog.state-machines, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ออกแบบเงื่อนไขยืนยันผลหลายครั้งก่อนลงมือ และวัดว่าลดการเตือนผิดได้เท่าไร
2. อธิบายการแลกเปลี่ยนระหว่างความเร็วในการตอบสนองกับการเตือนผิด

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/08_deepcraft_link.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c)
