---
id: edgeai-dev.m03.l02
lang: th
title: {th: ตัวชี้วัดที่คำนวณได้และการจำแนกด้วยกฎ, en: Derived metrics and rule-based classification}
summary: {th: สร้างตัวจำแนกแบบกฎด้วยเกณฑ์ที่อธิบายได้ เป็นฐานเปรียบเทียบก่อนใช้ machine learning, en: Build an explainable threshold classifier as a baseline before machine learning.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m03.l01]
objectives:
- {th: ออกแบบตัวจำแนกแบบกฎที่มีสถานะชัดเจนและ hysteresis กันการสลับไปมา, en: Design a rule classifier with clear states and hysteresis against flapping.}
- {th: วัดความแม่นของตัวจำแนกแบบกฎกับข้อมูลที่ติดป้าย เพื่อใช้เทียบกับโมเดลในภายหลัง, en: Measure the rule classifier's accuracy on labelled data as a baseline for later models.}
develops:
- {skill: prog.state-machines, to: 2}
- {skill: sys.dsp, to: 2}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ออกแบบตัวจำแนกแบบกฎที่มีสถานะชัดเจนและ hysteresis กันการสลับไปมา
2. วัดความแม่นของตัวจำแนกแบบกฎกับข้อมูลที่ติดป้าย เพื่อใช้เทียบกับโมเดลในภายหลัง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s05/03_pot_setpoint_deadband.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/03_pot_setpoint_deadband.py)
