---
id: fw-stack.m02.l05
lang: th
title:
  th: "สแกน Wi-Fi และแสดงรายการเครือข่าย"
  en: "Wi-Fi scan and a network list"
summary:
  th: "สแกน WiFi ผ่าน WHD/cy_wcm แล้วแสดงผลเป็น list พร้อม RSSI + security type — เพิ่มหน้า WiFi Scan เข้าไปใน shell ของ EP04"
  en: "Wi-Fi scan and a network list"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l04]
objectives:
  - th: "สแกน Wi-Fi ผ่าน WHD/cy_wcm แล้วแสดงรายการพร้อม RSSI และชนิด security"
    en: "Scan Wi-Fi through WHD/cy_wcm and list networks with RSSI and security type"
  - th: "แยก scan service ออกจากหน้า UI และส่งผลสแกนเข้าหน้าอย่างปลอดภัย"
    en: "Keep the scan service apart from the UI page and hand results to the page safely"
  - th: "อ่านค่า RSSI และบอกได้ว่าเครือข่ายใดสัญญาณดีพอจะเชื่อมต่อ"
    en: "Read RSSI values and judge which network is strong enough to join"
develops:
  - {skill: proto.wifi, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: rtos.basics, to: 1}
  - {skill: iot.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep05_wifi_list"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# สแกน Wi-Fi และแสดงรายการเครือข่าย

## เป้าหมาย

1. สแกน Wi-Fi ผ่าน WHD/cy_wcm แล้วแสดงรายการพร้อม RSSI และชนิด security
2. แยก scan service ออกจากหน้า UI และส่งผลสแกนเข้าหน้าอย่างปลอดภัย
3. อ่านค่า RSSI และบอกได้ว่าเครือข่ายใดสัญญาณดีพอจะเชื่อมต่อ

## แนวคิด

สแกน WiFi ผ่าน WHD/cy_wcm แล้วแสดงผลเป็น list พร้อม RSSI + security type — เพิ่มหน้า WiFi Scan เข้าไปใน shell ของ EP04

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/ui_menu_navigation.c)
- และอีก 6 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP05 — WiFi List บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/hmi_ep05_wifi_list.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- RSSI -45 dBm กับ -85 dBm อันไหนดีกว่า
- ทำไมไม่ควรสแกน Wi-Fi ใน callback ของปุ่มโดยตรง
- ชนิด security ในรายการบอกอะไรกับผู้ใช้

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
