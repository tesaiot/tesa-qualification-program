---
id: c-found.m02.l01
lang: th
title: {th: ชุดเครื่องมือและการ build ครั้งแรก, en: The toolchain and a first build}
summary: {th: ติดตั้ง ModusToolbox ตรวจความพร้อม ดึง dependency แล้ว build และแฟลชแม่แบบเฟิร์มแวร์ของ SDK, en: 'Install ModusToolbox, check readiness, fetch dependencies, then build and flash the SDK firmware template.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l03]
objectives:
- {th: รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ, en: 'Run the readiness check, fetch every project''s dependencies, build and flash the firmware template.'}
- {th: 'อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้', en: 'Explain what CM33_S, CM33_NS and CM55 each run in this template.'}
- {th: บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้, en: Record the tool versions and SDK commit used so others can reproduce the build.}
develops:
- {skill: build.vendor-sdk, to: 3}
- {skill: build.compilers, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ
2. อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้
3. บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- `./bento.sh doctor`
- `make getlibs` แยกทีละโปรเจกต์
- `./bento.sh build` และ `./bento.sh flash`
- ทำไมต้องปิดเปิดไฟบอร์ดหลังแฟลช

## แหล่งอ้างอิง

- [SDK: แม่แบบ mtb-only README (First run, CLI, สามคอร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [A0 — What you can build, and where each piece lives (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html)
- [A1 — From the zip to your first program (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)
- [Infineon ModusToolbox software (GitHub)](https://github.com/Infineon/modustoolbox-software)
- [Infineon mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0)
