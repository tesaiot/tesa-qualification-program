---
id: fw-stack.m03.l04
lang: th
title:
  th: "เข็มทิศดิจิทัลจาก BMM350 บน I3C พร้อม calibration"
  en: "Digital compass from the BMM350 over I3C with calibration"
summary:
  th: "สร้างเข็มทิศดิจิทัลจากเซนเซอร์สนามแม่เหล็ก Bosch BMM350 บน I3C พร้อมฟีเจอร์ปรับแต่ง (hard-iron calibration)"
  en: "Digital compass from the BMM350 over I3C with calibration"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l03]
objectives:
  - th: "อ่านสนามแม่เหล็กจาก BMM350 บน I3C แล้วคำนวณทิศเป็นองศา"
    en: "Read the magnetic field from the BMM350 over I3C and compute a heading in degrees"
  - th: "ทำ hard-iron calibration และแสดงว่าทิศแม่นขึ้นหลังปรับ"
    en: "Run hard-iron calibration and show that the heading improves afterwards"
  - th: "อธิบายว่าโลหะและกระแสไฟรอบบอร์ดรบกวนเข็มทิศอย่างไร"
    en: "Explain how metal and currents near the board disturb the compass"
develops:
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: sys.dsp, to: 1}
  - {skill: proto.i2c, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep04_bmm350_compass"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# เข็มทิศดิจิทัลจาก BMM350 บน I3C พร้อม calibration

## เป้าหมาย

1. อ่านสนามแม่เหล็กจาก BMM350 บน I3C แล้วคำนวณทิศเป็นองศา
2. ทำ hard-iron calibration และแสดงว่าทิศแม่นขึ้นหลังปรับ
3. อธิบายว่าโลหะและกระแสไฟรอบบอร์ดรบกวนเข็มทิศอย่างไร

## แนวคิด

สร้างเข็มทิศดิจิทัลจากเซนเซอร์สนามแม่เหล็ก Bosch BMM350 บน I3C พร้อมฟีเจอร์ปรับแต่ง (hard-iron calibration)

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/main_example.c)
- [`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_config.h)
- [`app_sensor/bmm350/bmm350_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.c)
- [`app_sensor/bmm350/bmm350_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.h)
- [`app_sensor/bmm350/bmm350_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_reader.c)
- และอีก 6 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP04 — BMM350 Compass บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/int_ep04_bmm350_compass.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- hard-iron error คืออะไร และแก้ด้วยวิธีใด
- ทำไมต้องหมุนบอร์ดให้ครบทุกทิศตอน calibrate
- I3C ต่างจาก I2C อย่างไรในมุมผู้ใช้งาน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
