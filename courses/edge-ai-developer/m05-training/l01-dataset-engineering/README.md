---
id: edgeai-dev.m05.l01
lang: th
title: {th: วิศวกรรมชุดข้อมูล, en: Dataset engineering}
summary: {th: เก็บ ติดป้าย และแบ่งชุดข้อมูลให้สมดุลและไม่รั่วระหว่างชุดฝึกกับชุดทดสอบ, en: 'Capture, label and split a balanced dataset with no leakage between training and test.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m04.l03]
objectives:
- {th: 'แบ่งชุดข้อมูลเป็น train, validation และ test โดยไม่ให้ข้อมูลจากการเก็บครั้งเดียวกันรั่วข้ามชุด', en: 'Split data into train, validation and test without leaking one capture session across sets.'}
- {th: ตรวจความสมดุลของคลาสและเสนอวิธีแก้เมื่อไม่สมดุล, en: Check class balance and propose fixes when it is skewed.}
develops:
- {skill: ai.data-collection, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. แบ่งชุดข้อมูลเป็น train, validation และ test โดยไม่ให้ข้อมูลจากการเก็บครั้งเดียวกันรั่วข้ามชุด
2. ตรวจความสมดุลของคลาสและเสนอวิธีแก้เมื่อไม่สมดุล

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [TensorFlow](https://www.tensorflow.org/)
