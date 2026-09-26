---
id: fw-stack.m02.l01
lang: th
title:
  th: "หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย"
  en: "First LVGL screen: logo, title and subtitle"
summary:
  th: "หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen"
  en: "First LVGL screen: logo, title and subtitle"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง"
    en: "Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot"
  - th: "อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง"
    en: "Explain when the master template calls example_main(parent) and why we do not write main ourselves"
  - th: "สร้าง object tree screen → image → label และจัดวางด้วย align ได้"
    en: "Build a screen → image → label object tree and place it with align"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: lang.c, to: 2}
  - {skill: build.vendor-sdk, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep01_basic_label"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย

## เป้าหมาย

1. build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง
2. อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง
3. สร้าง object tree screen → image → label และจัดวางด้วย align ได้

## แนวคิด

หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/main_example.c)
- [`ui_ep01_basic_label.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c)
- [`ui_ep01_basic_label.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.h)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP01 — Basic Label บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/hmi_ep01_basic_label.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- master template ทำอะไรให้เราแล้วบ้างก่อนเรียก example_main()
- ทำไมโลโก้ถูกฝังเป็น C array (APP_LOGO) แทนการโหลดจากไฟล์
- ถ้าอยากย้าย title ลงอีก 20 px ต้องแก้ค่าใดในโค้ด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
