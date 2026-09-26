---
id: edgeai-dev.m07.l01
lang: th
title: {th: สแตก Edge AI ใต้ฝากระโปรง, en: The edge AI stack under the hood}
summary: {th: ตามเส้นทางข้อมูลผ่านหลายคอร์ เอนจินของโมเดล และ NPU ในโค้ดและเอกสารจริง, en: 'Trace the data path across cores, the model engine and the NPU in real code and docs.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [none]
prerequisites: [edgeai-dev.m06.l03]
objectives:
- {th: อธิบายว่าคอร์ใดทำอะไรในเส้นทางจากเซนเซอร์ถึงผลของโมเดล, en: Explain which core does what on the path from sensor to model result.}
- {th: ชี้ไฟล์และฟังก์ชันจริงในเอกสารของ SDK ที่รับผิดชอบแต่ละขั้น, en: Point to the real files and functions in the SDK docs responsible for each step.}
develops:
- {skill: ai.model-deploy, to: 3}
- {skill: rtos.multicore-ipc, to: 3}
- {skill: hw.architecture, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายว่าคอร์ใดทำอะไรในเส้นทางจากเซนเซอร์ถึงผลของโมเดล
2. ชี้ไฟล์และฟังก์ชันจริงในเอกสารของ SDK ที่รับผิดชอบแต่ละขั้น

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
- [B3 — The IPC backbone: setup, deferred binding, snapshots (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b3__ipc__backbone.html)
- [SDK: lib/edge_ai/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/lib/edge_ai/README.md)
