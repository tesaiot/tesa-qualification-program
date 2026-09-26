---
id: c-found.m01.l02
lang: th
title: {th: แผนที่หน่วยความจำ stack และ heap, en: 'Memory map, stack and heap'}
summary: {th: รู้ว่าข้อมูลแต่ละก้อนอยู่ที่ใด และป้องกัน stack ล้นกับการจองหน่วยความจำในที่ที่ไม่ควร, en: Know where each piece of data lives and prevent stack overflow and allocation in the wrong place.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l01]
objectives:
- {th: 'จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static', en: 'Classify the variables of an example program as stack, heap or static.'}
- {th: อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่, en: Read a task's remaining stack from the counters the SDK exposes and judge whether it is near overflow.}
- {th: อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง, en: Explain why dynamic allocation does not belong in an ISR or a real-time loop.}
develops:
- {skill: prog.memory, to: 3}
- {skill: lang.c, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static
2. อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่
3. อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ส่วน .text .data .bss stack heap
- stack ต่อ task ใน RTOS
- fragmentation และการจองล่วงหน้า
- ตัวนับสุขภาพของงานใน SDK

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/07_engine_health.c (ai_engine_stack_words และ ai_engine_stack_free_words)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: cm33/storage/10_littlefs_basics.c (บัฟเฟอร์และสัญญาของ API หน่วยเก็บ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
