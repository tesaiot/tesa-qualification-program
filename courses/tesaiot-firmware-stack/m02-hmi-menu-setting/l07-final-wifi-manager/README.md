---
id: fw-stack.m02.l07
lang: th
title:
  th: "Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
summary:
  th: "รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile ที่เก็บไว้"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l06]
objectives:
  - th: "รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้"
    en: "Combine scan, profile and connect into a Wi-Fi manager that auto-connects from the stored profile"
  - th: "ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ"
    en: "Design a connection state machine (connect, drop, retry) and show its state on screen"
  - th: "ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่"
    en: "Ping the gateway to check that the network really answers, and explain that in this example the ping result does not trigger a reconnect"
develops:
  - {skill: prog.state-machines, to: 3}
  - {skill: proto.wifi, to: 3}
  - {skill: proto.tcp-ip, to: 1}
  - {skill: rtos.basics, to: 2}
assesses:
  - {skill: prog.state-machines, level: 2, evidence: "วิดีโอหรือ log ที่บอร์ดต่อ Wi-Fi อัตโนมัติหลังรีเซ็ต และกลับมาเองหลังปิด AP"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep07_final_wifi_manager"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ

## เป้าหมาย

1. รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้
2. ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ
3. ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่

## แนวคิด

รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile ที่เก็บไว้

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/ui_menu_navigation.c)
- และอีก 15 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP07 — Final WiFi Manager บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/hmi_ep07_final_wifi_manager.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม "ต่อ AP ได้" ยังไม่พอจะบอกว่าอินเทอร์เน็ตใช้ได้
- state ใดบ้างที่จำเป็นใน state machine ของการเชื่อมต่อ
- ถ้าลองใหม่ถี่เกินไปจะเกิดปัญหาอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
