---
id: fw-stack.m02.l02
lang: th
title:
  th: "ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
summary:
  th: "ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l01]
objectives:
  - th: "ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT"
    en: "Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT"
  - th: "แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น"
    en: "Separate UI logic from counter logic into different files and explain why that makes testing easier"
  - th: "เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้"
    en: "Add one new button that reuses the same logic"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: prog.design-patterns, to: 1}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep02_button_event"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET

## เป้าหมาย

1. ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT
2. แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น
3. เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้

## แนวคิด

ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`counter_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.c)
- [`counter_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.h)
- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/main_example.c)
- [`ui_button_counter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.c)
- [`ui_button_counter.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.h)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP02 — Button Event บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/hmi_ep02_button_event.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- LV_EVENT_PRESSED กับ LV_EVENT_LONG_PRESSED_REPEAT ต่างกันอย่างไรเมื่อกดค้าง
- counter_logic.c รู้จัก LVGL หรือไม่ และทำไมจึงออกแบบแบบนั้น
- ถ้าตัวนับต้องไม่ติดลบ ควรแก้ที่ไฟล์ใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
