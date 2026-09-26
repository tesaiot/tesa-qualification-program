---
id: c-found.m02.l02
lang: th
title: {th: Make และตัวแปรของการ build, en: Make and build flags}
summary: {th: อ่าน Makefile เปิดปิดส่วนของเฟิร์มแวร์ด้วยตัวแปร และรันตัวอย่างของ SDK ทีละตัว, en: 'Read a Makefile, switch firmware parts with variables, and run SDK examples one at a time.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l01]
objectives:
- {th: เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย ENABLE_PAGE_EXAMPLES=1 และเลือกรันตัวอย่างฝั่ง CM33 ด้วย SDK_EXAMPLE_CM33 ได้, en: Enable the SDK example catalogue with ENABLE_PAGE_EXAMPLES=1 and select a CM33 example with SDK_EXAMPLE_CM33.}
- {th: 'อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ ?= กับ = และผลต่อการ build', en: 'Explain the difference between ?= and = assignments in Make and their effect on the build.'}
- {th: อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย, en: Explain why disabled examples add nothing to the firmware image.}
develops:
- {skill: build.make-cmake, to: 3}
- {skill: build.vendor-sdk, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย ENABLE_PAGE_EXAMPLES=1 และเลือกรันตัวอย่างฝั่ง CM33 ด้วย SDK_EXAMPLE_CM33 ได้
2. อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ ?= กับ = และผลต่อการ build
3. อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- โครงของ Makefile ในโปรเจกต์ ModusToolbox
- ตัวแปรเปิดปิดส่วนของเฟิร์มแวร์
- `CY_IGNORE` และผลต่อขนาดเฟิร์มแวร์
- อ่านข้อความผิดพลาดของ build

## แหล่งอ้างอิง

- [SDK: แคตตาล็อกตัวอย่าง (Turning them on, Which core)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [SDK: ตัวอย่างฝั่ง CM33 Non-secure (วิธีรัน)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [GNU Make](https://www.gnu.org/software/make/)
