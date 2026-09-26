---
id: fw-stack.m03.l05
lang: th
title:
  th: "Motion radar: วาดทิศการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
summary:
  th: "นำข้อมูล accelerometer/gyroscope จาก BMI270 มาวาดเป็น motion radar บนจอ LVGL เพื่อให้เห็นทิศทางการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l04]
objectives:
  - th: "แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar"
    en: "Turn accelerometer and gyroscope readings into angle and magnitude and draw them in polar form"
  - th: "ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms"
    en: "Use a baseline and a dead-band to drop small jitter before drawing, and work out how much lag a moving average would add at the 50 ms read period"
  - th: "ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที"
    en: "Design a view that lets a user read the direction within a second"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep05_bmi270_radar_view"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# Motion radar: วาดทิศการเคลื่อนไหวแบบ polar

## เป้าหมาย

1. แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar
2. ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms
3. ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที

## แนวคิด

นำข้อมูล accelerometer/gyroscope จาก BMI270 มาวาดเป็น motion radar บนจอ LVGL เพื่อให้เห็นทิศทางการเคลื่อนไหวแบบ polar

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/main_example.c)
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_config.h)
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_driver.c)
- [`app_sensor/bmi270/bmi270_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_driver.h)
- [`app_sensor/bmi270/bmi270_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_reader.c)
- และอีก 6 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP05 — BMI270 Radar View บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/int_ep05_bmi270_radar_view.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- atan2 ใช้ทำอะไรในการหาทิศ
- dead-band ต่างจาก moving average อย่างไรในแง่ความหน่วงของจุดบน radar
- สีหรือขนาดของจุดควรสื่อข้อมูลอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
