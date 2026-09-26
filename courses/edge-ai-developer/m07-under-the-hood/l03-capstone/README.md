---
id: edgeai-dev.m07.l03
lang: th
title: {th: 'งานปลายทาง: แอป Edge AI ครบวงจร', en: 'Capstone: a complete edge AI application'}
summary: {th: ออกแบบ สร้าง และนำเสนอแอป Edge AI ที่ครอบคลุมอย่างน้อยสามเสาหลัก พร้อมเหตุผลเชิงวิศวกรรม, en: 'Design, build and present an edge AI application covering at least three pillars, with engineering reasoning.'}
level: L3
time_min: {concept: 5, practise: 10, lab: 55, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [edgeai-dev.m07.l02]
objectives:
- {th: ส่งแอป Edge AI ที่ทำงานได้และครอบคลุมอย่างน้อยสามเสาหลัก พร้อมหลักฐานการทดสอบ, en: 'Deliver a working edge AI app covering at least three pillars, with test evidence.'}
- {th: นำเสนอการตัดสินใจเชิงวิศวกรรมอย่างน้อยสามเรื่อง เช่น เป้าหมายที่รัน ความแม่น และการเตือนผิด พร้อมเหตุผล, en: 'Present at least three engineering decisions, such as target, accuracy and false alarms, with reasons.'}
develops:
- {skill: ai.edge, to: 3}
- {skill: soft.problem-solving, to: 3}
- {skill: soft.communication, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ส่งแอป Edge AI ที่ทำงานได้และครอบคลุมอย่างน้อยสามเสาหลัก พร้อมหลักฐานการทดสอบ
2. นำเสนอการตัดสินใจเชิงวิศวกรรมอย่างน้อยสามเรื่อง เช่น เป้าหมายที่รัน ความแม่น และการเตือนผิด พร้อมเหตุผล

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
- [TensorFlow Lite for Microcontrollers (tflite-micro)](https://github.com/tensorflow/tflite-micro)
