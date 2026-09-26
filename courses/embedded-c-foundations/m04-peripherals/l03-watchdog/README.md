---
id: c-found.m04.l03
lang: th
title: {th: Watchdog, en: The watchdog}
summary: {th: ใช้ watchdog ให้ระบบฟื้นตัวเองเมื่อค้าง โดยป้อนในจุดที่พิสูจน์ว่าระบบยังทำงานจริง, en: 'Use a watchdog so the system recovers when it hangs, feeding it only where progress is proven.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l02]
objectives:
- {th: อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด, en: Explain what a watchdog does and what happens when it is not fed in time.}
- {th: ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก, en: Identify the correct feeding point in a multi-task program and explain why feeding from a timer ISR is a trap.}
- {th: ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด, en: Design reset-cause logging so you know when the watchdog fired.}
develops:
- {skill: mcu.watchdog, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด
2. ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก
3. ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- watchdog ของฮาร์ดแวร์และของงาน
- ป้อนเมื่อพิสูจน์ความก้าวหน้าเท่านั้น
- สาเหตุการรีเซ็ต
- ตัวอย่างการป้อน watchdog ของ task ใน SDK

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/08_deepcraft_link.c (deepcraft_task_watchdog)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer)
