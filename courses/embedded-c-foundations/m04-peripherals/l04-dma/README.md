---
id: c-found.m04.l04
lang: th
title: {th: DMA, en: DMA}
summary: {th: ย้ายข้อมูลโดยไม่ใช้ CPU และรู้ข้อควรระวังเรื่องบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน, en: Move data without the CPU and know the pitfalls of buffers shared by DMA and the CPU.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l03]
objectives:
- {th: อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม, en: Explain how DMA offloads data movement from the CPU and when it is not worth it.}
- {th: ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ, en: 'Identify the risks of buffers shared by DMA and the CPU, such as caches and reading before the transfer completes.'}
develops:
- {skill: mcu.dma, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม
2. ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- descriptor และการย้ายข้อมูลแบบต่อเนื่อง
- double buffering
- cache coherence
- SDK ที่ commit นี้ยังไม่มีตัวอย่าง DMA โดยตรง บทนี้อ้าง PDL

## แหล่งอ้างอิง

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Direct memory access (Wikipedia)](https://en.wikipedia.org/wiki/Direct_memory_access)
