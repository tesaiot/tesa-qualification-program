---
id: fw-stack.m04.l03
lang: th
title:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
summary:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V"
    en: "Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus"
  - th: "ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว"
    en: "Combine potentiometer input with matrix and screen output in one program"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_rgb_matrix"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ควบคุม RGB dot matrix ผ่าน I2C

## เป้าหมาย

1. ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V
2. ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว

## แนวคิด

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — DFR0522 RGB Dot Matrix** — ควบคุม DFRobot DFR0522 RGB matrix 8x16 (I2C 0x10) บน bus 3.3V ร่วมกับ display แสดง clear/fill/pixel/pattern ผ่าน LVGL UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix)
- **QWA309 — RGB Matrix FX** — เอฟเฟกต์แอนิเมชันบน DFR0522 8x16 (color cycle / pixel sweep / row wipe) auto-cycle + สถานะบน LCD
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix_fx&q=prac_qwa309_rgb_matrix_fx)
- **QWA309 — Pot → RGB Mixer** — 3 potentiometers เป็น R/G/B channel (>50% = เปิดสีนั้น) ผสมเป็น 1 ใน 8 สีของ DFR0522 matrix + แสดงบน LCD — รวม SAR pots + RGB I2C
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_rgb_mixer&q=prac_qwa309_pot_rgb_mixer)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- อุปกรณ์สองตัวบน I2C bus เดียวกันแยกกันด้วยอะไร
- ถ้า matrix ไม่ตอบ ต้องตรวจอะไรก่อน (สาย ไฟ address)

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
