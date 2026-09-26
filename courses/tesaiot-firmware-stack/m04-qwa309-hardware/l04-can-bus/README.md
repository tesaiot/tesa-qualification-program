---
id: fw-stack.m04.l04
lang: th
title:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
summary:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งเฟรม heartbeat 1 Hz ผ่าน CANFD0 แบบ Classic CAN 2.0A ที่ 500 kbps"
    en: "Send a 1 Hz heartbeat on CANFD0 as Classic CAN 2.0A at 500 kbps"
  - th: "อ่านเฟรมที่เข้ามาและแสดงเป็นตาราง ID ข้อมูล และจำนวนครั้ง"
    en: "Receive frames and list their ID, data and count"
develops:
  - {skill: proto.can, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_can_monitor"
  ref: 372d0d849578a6a49b634d3ecaab8b5958166921
---

# CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม

## เป้าหมาย

1. ส่งเฟรม heartbeat 1 Hz ผ่าน CANFD0 แบบ Classic CAN 2.0A ที่ 500 kbps
2. อ่านเฟรมที่เข้ามาและแสดงเป็นตาราง ID ข้อมูล และจำนวนครั้ง

## แนวคิด

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `372d0d8`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — CAN Bus Monitor** — CANFD0 Classic CAN 2.0A @ 500 kbps (P16.2 RX / P16.3 TX, SN65HVD230) บน CM55 แบบ polled — TX heartbeat 1Hz + RX frame table บน LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_can_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_can_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_can_monitor&q=prac_qwa309_can_monitor)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม CAN bus ต้องมี termination ที่ปลายสาย
- ID ของเฟรม CAN บอกอะไรนอกจากชื่อข้อความ

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/372d0d849578a6a49b634d3ecaab8b5958166921) · commit `372d0d8`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
