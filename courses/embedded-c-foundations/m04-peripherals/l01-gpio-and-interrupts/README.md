---
id: c-found.m04.l01
lang: th
title: {th: GPIO และ interrupt, en: GPIO and interrupts}
summary: {th: ขับหลอดไฟ อ่านปุ่ม และรับเหตุการณ์ด้วย interrupt ตามกติกาของบริบท ISR, en: 'Drive LEDs, read buttons and handle events with interrupts under ISR rules.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l02]
objectives:
- {th: ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง, en: Configure GPIO pins with PDL calls as outputs and inputs with the correct drive mode.}
- {th: เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR, en: 'Write a short, non-blocking ISR that hands work to a task instead of doing it inside.'}
- {th: กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก, en: Debounce a button without blocking waits.}
develops:
- {skill: mcu.gpio, to: 3}
- {skill: mcu.interrupts, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง
2. เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR
3. กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- drive mode ของ GPIO
- ISR และการส่งงานต่อให้ task
- ห้าม printf ใน callback ที่เป็นบริบท ISR
- การกันเด้งแบบไม่บล็อก

## แหล่งอ้างอิง

- [SDK: cm33/io/04_gpio_led_button.c (drive mode และการกันเด้งแบบไม่บล็อก)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [SDK: ตัวอย่างฝั่ง CM33 (ข้อควรทราบเรื่องบริบท ISR)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Interrupt (Wikipedia)](https://en.wikipedia.org/wiki/Interrupt)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) — อ่านปุ่มกด SW9 (P17.5) และ SW10 (P17.7) แบบ active-low pull-up แสดงสถานะกด/ปล่อย + นับจำนวนครั้งบน LVGL
- [QWA309 — Hardware Button Menu](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu) — นำทางเมนู LVGL ด้วยปุ่มกายภาพ SW6=Move SW5=Select (ไม่ใช้ touch) — headless/kiosk UX pattern
