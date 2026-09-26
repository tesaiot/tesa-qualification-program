---
id: edgeai-dev.m02.l01
lang: th
title: {th: อัตราสุ่มตัวอย่างและการบันทึกข้อมูล, en: Sampling and logging}
summary: {th: เลือกอัตราสุ่มตัวอย่าง อ่านเซนเซอร์ และบันทึกลงไฟล์ CSV บนหน่วยเก็บของบอร์ด, en: 'Choose a sample rate, read sensors and log to CSV on the board''s storage.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m01.l03]
objectives:
- {th: เลือกอัตราสุ่มตัวอย่างที่เหมาะกับสัญญาณที่ต้องการเก็บ และอธิบายเหตุผลจากความถี่ของสัญญาณ, en: Choose a sample rate for the signal and justify it from the signal's frequency.}
- {th: บันทึกตัวอย่างที่ติดป้ายตามจำนวนที่กำหนดลงไฟล์ CSV และตรวจว่าไม่มีตัวอย่างหาย, en: Log a given number of labelled samples to CSV and check none are missing.}
develops:
- {skill: ai.data-collection, to: 3}
- {skill: sys.memory-fs, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เลือกอัตราสุ่มตัวอย่างที่เหมาะกับสัญญาณที่ต้องการเก็บ และอธิบายเหตุผลจากความถี่ของสัญญาณ
2. บันทึกตัวอย่างที่ติดป้ายตามจำนวนที่กำหนดลงไฟล์ CSV และตรวจว่าไม่มีตัวอย่างหาย

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s07/03_aliasing_nyquist.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s07/03_aliasing_nyquist.py)
- [Edge AI: Sensor cadence (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__sensor__rate.html)
