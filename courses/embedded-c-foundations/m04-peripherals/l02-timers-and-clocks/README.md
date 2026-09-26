---
id: c-found.m04.l02
lang: th
title: {th: Timer และสัญญาณนาฬิกา, en: Timers and clocks}
summary: {th: ทำงานเป็นจังหวะด้วย timer ของฮาร์ดแวร์และของ RTOS และเข้าใจว่าสัญญาณนาฬิกากำหนดความแม่นยำอย่างไร, en: Run periodic work with hardware and RTOS timers and understand how clocks set accuracy.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l01]
objectives:
- {th: คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้, en: Compute timer settings from the clock frequency and the desired interval.}
- {th: เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล, en: 'Choose between a hardware timer and an RTOS software timer for a task, with reasons.'}
- {th: อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ, en: Explain how the rate of a background task affects system load.}
develops:
- {skill: mcu.timers, to: 3}
- {skill: mcu.clock, to: 2}
- {skill: rtos.freertos, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้
2. เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล
3. อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- prescaler และ period ของ timer
- tick ของ RTOS และ software timer
- clock tree และความคลาดเคลื่อน
- อัตราการทำงานกับภาระระบบ

## แหล่งอ้างอิง

- [SDK: cm33/sensors/05_auto_push_task.c (อัตราของ task เบื้องหลังและขีดจำกัด 50 ms)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
