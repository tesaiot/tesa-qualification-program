---
id: c-found.m01.l01
lang: th
title: {th: ภาษา C บนไมโครคอนโทรลเลอร์, en: C on a microcontroller}
summary: {th: ใช้ชนิดข้อมูลขนาดแน่นอน ตัวดำเนินการระดับบิต และ volatile กับรีจิสเตอร์ของอุปกรณ์, en: 'Use fixed-width types, bit operators and volatile with device registers.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: []
objectives:
- {th: เลือกชนิดข้อมูลขนาดแน่นอนจาก stdint.h ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้, en: Choose fixed-width stdint.h types for given values and explain overflow.}
- {th: เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง, en: 'Write correct read-modify-write set, clear and toggle operations with bit operators.'}
- {th: อธิบายว่าเมื่อใดต้องใช้ volatile กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt, en: Explain when volatile is required for variables shared with hardware or interrupts.}
develops:
- {skill: lang.c, to: 3}
- {skill: hw.architecture, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เลือกชนิดข้อมูลขนาดแน่นอนจาก stdint.h ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้
2. เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง
3. อธิบายว่าเมื่อใดต้องใช้ volatile กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ชนิดข้อมูล `uint8_t` `int32_t` และ overflow
- ตัวดำเนินการระดับบิตและ mask
- `volatile` และรีจิสเตอร์ที่แมปกับหน่วยความจำ
- การเรียก PDL แทนการแตะรีจิสเตอร์ตรง

## แหล่งอ้างอิง

- [SDK: cm33/sensors/06_raw_register_access.c (read-modify-write บนอุปกรณ์ I2C)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/io/04_gpio_led_button.c (คำสั่ง PDL เบื้องหลัง gpio.led()/gpio.button())](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [Peripherals at a glance (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__peripherals__quickref.html)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
