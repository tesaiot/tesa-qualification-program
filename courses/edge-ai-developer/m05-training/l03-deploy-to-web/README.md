---
id: edgeai-dev.m05.l03
lang: th
title: {th: นำโมเดลขึ้นเว็บ และเรื่องของคอมพิวเตอร์ Linux ขนาดเล็ก, en: 'Deploying to the web, and the small-Linux-computer story'}
summary: {th: รันโมเดลเดียวกันในเบราว์เซอร์ เทียบผลกับบน PC และรู้ว่าบนคอมพิวเตอร์ Linux ขนาดเล็กต่างกันอย่างไร, en: 'Run the same model in a browser, compare with PC results, and see what changes on a small Linux computer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [none]
prerequisites: [edgeai-dev.m05.l02]
objectives:
- {th: รันโมเดลที่แปลงแล้วในเบราว์เซอร์และเทียบผลกับบน PC ภายในค่าคลาดเคลื่อนที่กำหนด, en: Run the converted model in a browser and match PC results within a given tolerance.}
- {th: อธิบายว่าทำไมขั้นเตรียมข้อมูลต้องถูกเขียนซ้ำอย่างถูกต้องในทุกเป้าหมาย, en: Explain why preprocessing must be reimplemented faithfully on every target.}
develops:
- {skill: ai.model-deploy, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. รันโมเดลที่แปลงแล้วในเบราว์เซอร์และเทียบผลกับบน PC ภายในค่าคลาดเคลื่อนที่กำหนด
2. อธิบายว่าทำไมขั้นเตรียมข้อมูลต้องถูกเขียนซ้ำอย่างถูกต้องในทุกเป้าหมาย

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [LiteRT (เดิมชื่อ TensorFlow Lite) documentation](https://ai.google.dev/edge/litert)
