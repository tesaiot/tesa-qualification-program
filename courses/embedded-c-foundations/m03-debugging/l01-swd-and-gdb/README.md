---
id: c-found.m03.l01
lang: th
title: {th: SWD และ GDB เบื้องต้น, en: SWD and GDB basics}
summary: {th: ต่อ debugger ผ่าน SWD ตั้ง breakpoint ดูค่า และเดินโปรแกรมทีละบรรทัด, en: 'Attach a debugger over SWD, set breakpoints, inspect values and step through code.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l03]
objectives:
- {th: เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้, en: Start a debug session over SWD and stop at a breakpoint in a given function.}
- {th: ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้, en: 'Use GDB to print variables, show a backtrace and step line by line.'}
- {th: อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์, en: Explain why halting at a breakpoint can change the behaviour of a timing-sensitive or multi-core system.}
develops:
- {skill: debug.jtag-swd, to: 3}
- {skill: debug.gdb, to: 3}
- {skill: debug.openocd, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้
2. ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้
3. อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- SWD และ debugger บนบอร์ด (KitProg)
- OpenOCD กับ GDB
- breakpoint, watchpoint, backtrace
- ดีบักระบบหลายคอร์

## แหล่งอ้างอิง

- [GDB documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)
- [OpenOCD User's Guide](https://openocd.org/doc/html/index.html)
- [SDK: แม่แบบ mtb-only README (แฟลชผ่าน KitProg)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
