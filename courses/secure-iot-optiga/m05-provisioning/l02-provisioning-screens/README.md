---
id: sec-iot.m05.l02
lang: th
title: {th: หน้าจอลงทะเบียนบนอุปกรณ์, en: Provisioning screens on the device}
summary: {th: ส่งงานที่ใช้เวลาหลายวินาทีให้หน้าจอที่คอยถามสถานะ และปิดหน้าจอเก่าก่อนเปิดใหม่เสมอ, en: Hand seconds-long secure-element work to a polling screen and always tear the previous overlay down first.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l01]
objectives:
- {th: อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป, en: Explain why the provisioning screen polls instead of waiting on the chip.}
- {th: เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง, en: Order the overlay teardown and the enrol screen opening as the SDK example does.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: gui.embedded, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป
2. เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- งานยาวกับงานวาดจอ
- หน้าจอลงทะเบียนและหน้าจอป้องกัน
- ปิดของเก่าก่อนเสมอ

## แหล่งอ้างอิง

- [SDK: cm55/security/01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c)
- [Security / HSM: Tutorials (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security__tut.html)
