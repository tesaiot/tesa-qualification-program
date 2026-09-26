---
id: fw-stack.m01.l01
lang: th
title:
  th: "เครื่องมือ บอร์ด และ master template"
  en: "Toolchain, board and the master template"
summary:
  th: "ติดตั้ง ModusToolbox เตรียม master template ของ TESAIoT Firmware Stack แล้ว build และ flash ครั้งแรก"
  en: "Install ModusToolbox, set up the TESAIoT Firmware Stack master template, then build and flash for the first time"
level: L2
time_min: {concept: 15, lab: 45}
hardware: {emulator: false, boards: [devkit]}
prerequisites: []
objectives:
  - th: "ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error"
    en: "Install ModusToolbox, clone the master template and build it without errors"
  - th: "วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้"
    en: "Drop an episode into proj_cm55/apps/ and flash it through KitProg3"
  - th: "อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์"
    en: "Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip"
develops:
  - {skill: build.vendor-sdk, to: 2}
  - {skill: build.make-cmake, to: 2}
  - {skill: build.compilers, to: 1}
  - {skill: vcs.git, to: 1}
  - {skill: hw.architecture, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "README.md"
  ref: 082fd3e76595b62cfdb213499a093c233dbb4b53
---

# เครื่องมือ บอร์ด และ master template

## เป้าหมาย

1. ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error
2. วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้
3. อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์

## สิ่งที่ต้องมี

- **TESAIoT Dev Kit** (PSoC Edge AI Kit SoM บนบอร์ดฐาน QWA309) และสาย USB-C สำหรับ KitProg3
- **ModusToolbox** ของ Infineon รุ่น 3.6 ขึ้นไปตาม README ของ master template (README ของชุด episode แนะนำ 3.8)
- **git** และเครื่องที่ build ภาษา C ได้ (Windows, macOS หรือ Linux)

## แนวคิด

TESAIoT Firmware Stack แบ่งงานเป็นสามโปรเจกต์ตามคอร์ของ PSoC Edge E84 คือ `proj_cm33_s` (secure)
`proj_cm33_ns` (non-secure: Wi-Fi และการเชื่อมต่อ) และ `proj_cm55` (จอ LVGL, GPU VGLite และแอปของเรา)
master template เตรียมทุกอย่างให้พร้อมตั้งแต่ boot เราเขียนเฉพาะไฟล์ใน `proj_cm55/apps/` และเขียนฟังก์ชัน
`example_main(parent)` ที่ master เรียกให้

## แล็บ: build และ flash ครั้งแรก

1. clone master template จาก branch `tesaiot_dev_kit_master` ของ Developer Hub

   ```sh
   git clone -b tesaiot_dev_kit_master https://github.com/tesaiot/developer-hub.git tesaiot_dev_kit_master
   cd tesaiot_dev_kit_master
   make getlibs
   ```


2. build และ flash ตามขั้นตอนใน [README ของ master template](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md)

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

3. ถ้ายังไม่พร้อม build เอง ให้เปิดตัวอย่างบน [Developer Hub](https://dev.tesaiot.dev/) แล้ว flash เฟิร์มแวร์สำเร็จรูป
   จากหน้าตัวอย่าง (episode ในโมดูล 2–3 และแบบฝึก QWA309 ในโมดูล 4 มีเฟิร์มแวร์พร้อมใช้ทุกตัว)

## เช็กความเข้าใจ

- ไฟล์ของ episode ต้องวางไว้ที่ไหน และห้ามลบไฟล์ใดในโฟลเดอร์นั้น
- งานจอและงาน Wi-Fi อยู่คนละคอร์เพราะอะไร
- `make build` ผ่านแต่ `make program` ไม่เจอบอร์ด ควรตรวจอะไรก่อน

## แหล่งอ้างอิง

- [README ของ master template (ภาษาไทย)](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md) · commit `082fd3e`
- [TESAIoT Developer Hub](https://dev.tesaiot.dev/) · [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
- [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)
