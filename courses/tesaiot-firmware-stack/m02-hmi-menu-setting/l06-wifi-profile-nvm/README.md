---
id: fw-stack.m02.l06
lang: th
title:
  th: "เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร"
  en: "Store the Wi-Fi profile in non-volatile memory"
summary:
  th: "เก็บ SSID + password ลง non-volatile memory — form กรอก profile ผ่าน lv_textarea (password mode) และ save/load ผ่าน profile store"
  en: "Store the Wi-Fi profile in non-volatile memory"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l05]
objectives:
  - th: "สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode"
    en: "Build an SSID and password form with the password field in password mode"
  - th: "บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด"
    en: "Save, load and clear the profile through the NVM profile store, and keep it across a board reset"
  - th: "อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง"
    en: "Explain the risk of keeping a password in flash and ways to reduce it"
develops:
  - {skill: sys.memory-fs, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: sec.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep06_wifi_profile_nvm"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร

## เป้าหมาย

1. สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode
2. บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด
3. อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง

## แนวคิด

เก็บ SSID + password ลง non-volatile memory — form กรอก profile ผ่าน lv_textarea (password mode) และ save/load ผ่าน profile store

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/ui_menu_navigation.c)
- และอีก 11 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP06 — WiFi Profile NVM บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/hmi_ep06_wifi_profile_nvm.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ข้อมูลใน NVM ต่างจากตัวแปรใน RAM อย่างไรเมื่อบอร์ดรีเซ็ต
- ทำไมช่องรหัสผ่านต้องซ่อนตัวอักษร
- ถ้าต้องการลบโปรไฟล์ทั้งหมด ต้องเรียกฟังก์ชันใดของ profile store

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
