---
id: edgeai-dev.m05.l02
lang: th
title: {th: ฝึกโมเดลด้วย TensorFlow, en: Training with TensorFlow}
summary: {th: ฝึกตัวจำแนกขนาดเล็กบนเครื่อง PC ในสภาพแวดล้อมที่ทำซ้ำได้ และประเมินกับชุดทดสอบ, en: Train a small classifier on a PC in a reproducible environment and evaluate it on the test set.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [none]
prerequisites: [edgeai-dev.m05.l01]
objectives:
- {th: ฝึกโมเดลขนาดเล็กให้ได้ความแม่นบนชุดทดสอบตามเกณฑ์ที่กำหนด และรายงาน confusion matrix, en: Train a small model to a given test accuracy and report the confusion matrix.}
- {th: บันทึกเวอร์ชันของเครื่องมือและข้อมูลเพื่อให้การฝึกทำซ้ำได้, en: Record tool and data versions so training is reproducible.}
develops:
- {skill: ai.model-training, to: 3}
- {skill: lang.python, to: 3}
- {skill: build.docker, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ฝึกโมเดลขนาดเล็กให้ได้ความแม่นบนชุดทดสอบตามเกณฑ์ที่กำหนด และรายงาน confusion matrix
2. บันทึกเวอร์ชันของเครื่องมือและข้อมูลเพื่อให้การฝึกทำซ้ำได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [TensorFlow](https://www.tensorflow.org/)
- [LiteRT (เดิมชื่อ TensorFlow Lite) documentation](https://ai.google.dev/edge/litert)
