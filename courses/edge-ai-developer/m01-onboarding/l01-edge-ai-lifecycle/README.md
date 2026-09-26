---
id: edgeai-dev.m01.l01
lang: th
title: {th: Edge AI และวงจรชีวิตของข้อมูล, en: Edge AI and the data lifecycle}
summary: {th: รู้จักห้าเสาหลักของ Edge AI และรันโมเดลที่มีอยู่ครั้งแรก, en: Meet the five pillars of edge AI and run an existing model for the first time.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: []
objectives:
- {th: เรียงห้าเสาหลักของวงจรชีวิตข้อมูลและบอกผลลัพธ์ของแต่ละเสาได้, en: Order the five lifecycle pillars and name each one's output.}
- {th: รันโมเดลที่มีอยู่แล้วอ่านผลการจำแนกพร้อมค่าความมั่นใจได้, en: Run an existing model and read its classification and confidence.}
- {th: อธิบายข้อดีข้อเสียของการรันโมเดลบนไมโครคอนโทรลเลอร์ เว็บเบราว์เซอร์ และคอมพิวเตอร์ Linux ขนาดเล็ก, en: 'Explain the trade-offs of running a model on a microcontroller, in a browser and on a small Linux computer.'}
develops:
- {skill: ai.edge, to: 2}
- {skill: sys.simulation, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เรียงห้าเสาหลักของวงจรชีวิตข้อมูลและบอกผลลัพธ์ของแต่ละเสาได้
2. รันโมเดลที่มีอยู่แล้วอ่านผลการจำแนกพร้อมค่าความมั่นใจได้
3. อธิบายข้อดีข้อเสียของการรันโมเดลบนไมโครคอนโทรลเลอร์ เว็บเบราว์เซอร์ และคอมพิวเตอร์ Linux ขนาดเล็ก

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/01_first_inference.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/01_first_inference.c)
- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
- [SDK README (ฮาร์ดแวร์โดยย่อ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
