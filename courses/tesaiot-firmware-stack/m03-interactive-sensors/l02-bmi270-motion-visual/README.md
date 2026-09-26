---
id: fw-stack.m03.l02
lang: th
title:
  th: "ภาพการเคลื่อนไหว 6 แกนจาก BMI270"
  en: "Six-axis motion from the BMI270"
summary:
  th: "แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์"
  en: "Six-axis motion from the BMI270"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l01]
objectives:
  - th: "อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์"
    en: "Read the BMI270 accelerometer and gyroscope and display them in real time"
  - th: "แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง"
    en: "Tell acceleration (g) from angular rate (°/s) and predict the values of a board at rest"
  - th: "ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์"
    en: "Match the screen refresh rate to the sensor read rate"
develops:
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: proto.i2c, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep02_bmi270_motion_visual"
  ref: e48fbd2a8d786730e30aed96eb129150e2bcf66d
---

# ภาพการเคลื่อนไหว 6 แกนจาก BMI270

## เป้าหมาย

1. อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์
2. แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง
3. ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์

## แนวคิด

แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `e48fbd2`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/main_example.c)
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_config.h)
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.c)
- [`app_sensor/bmi270/bmi270_driver.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.h)
- [`app_sensor/bmi270/bmi270_reader.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_reader.c)
- และอีก 6 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?q=int_ep02_bmi270_motion_visual) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP02 — BMI270 Motion Visual บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/int_ep02_bmi270_motion_visual.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- บอร์ดวางนิ่งบนโต๊ะ แกนใดควรอ่านได้ประมาณ 1 g
- gyroscope อ่านอะไรเมื่อบอร์ดไม่หมุน
- ทำไมไม่ควรวาดจอทุกครั้งที่อ่านเซนเซอร์ได้

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep02_bmi270_motion_visual) · commit `e48fbd2`
- [ค้นหาตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?q=int_ep02_bmi270_motion_visual)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
