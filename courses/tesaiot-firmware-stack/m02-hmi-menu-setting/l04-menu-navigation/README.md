---
id: fw-stack.m02.l04
lang: th
title:
  th: "โครง navigation: แถบเมนู หน้า และการสลับหน้า"
  en: "Navigation shell: menu bar, pages and page routing"
summary:
  th: "โครง navigation หลัก — top nav bar พร้อมปุ่มสลับหน้า + icon action buttons + stage container ที่โหลดหน้าใหม่เมื่อผู้ใช้เลือกเมนู"
  en: "Navigation shell: menu bar, pages and page routing"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l03]
objectives:
  - th: "สร้าง top nav bar ที่สลับหน้าใน stage container ตามเมนูที่เลือก"
    en: "Build a top nav bar that swaps pages in a stage container"
  - th: "แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode"
    en: "Keep layout, navigation logic and pages apart, following the episode file structure"
  - th: "เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่"
    en: "Add one page to the menu without changing the existing pages"
develops:
  - {skill: gui.hmi, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: prog.state-machines, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep04_menu_navigation"
  ref: e48fbd2a8d786730e30aed96eb129150e2bcf66d
---

# โครง navigation: แถบเมนู หน้า และการสลับหน้า

## เป้าหมาย

1. สร้าง top nav bar ที่สลับหน้าใน stage container ตามเมนูที่เลือก
2. แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode
3. เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่

## แนวคิด

โครง navigation หลัก — top nav bar พร้อมปุ่มสลับหน้า + icon action buttons + stage container ที่โหลดหน้าใหม่เมื่อผู้ใช้เลือกเมนู

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `e48fbd2`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/nav/ui_menu_navigation.c)
- และอีก 1 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP04 — Menu Navigation บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/hmi_ep04_menu_navigation.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- stage container ทำหน้าที่อะไร
- ถ้าเพิ่มหน้าใหม่ ต้องแก้ไฟล์ใดบ้าง
- ทำไมจึงควรลบ object ของหน้าเก่าก่อนสร้างหน้าใหม่

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/hmi_ep04_menu_navigation) · commit `e48fbd2`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
