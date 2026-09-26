---
id: fw-stack.m03.l07
lang: th
title:
  th: "SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)"
  en: "SensorHub: one dashboard for every sensor (series project)"
summary:
  th: "โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว"
  en: "SensorHub: one dashboard for every sensor (series project)"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l06]
objectives:
  - th: "รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว"
    en: "Combine the DPS368, SHT4x, BMI270, BMM350 and PDM microphone on one dashboard"
  - th: "จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก"
    en: "Schedule each sensor read so the screen does not stutter"
  - th: "นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร"
    en: "Present the dashboard and explain how each value is shown"
develops:
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: rtos.basics, to: 2}
  - {skill: soft.problem-solving, to: 2}
  - {skill: soft.communication, to: 2}
assesses:
  - {skill: gui.hmi, level: 3, evidence: "วิดีโอแดชบอร์ดบนบอร์ดจริง 1 นาที พร้อมคำอธิบายการออกแบบ"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep07_sensorhub_final"
  ref: e48fbd2a8d786730e30aed96eb129150e2bcf66d
---

# SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)

## เป้าหมาย

1. รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว
2. จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก
3. นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร

## แนวคิด

โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `e48fbd2`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/main_example.c)
- [`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/app_audio/pdm/pdm_mic.c)
- [`app_audio/pdm/pdm_mic.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/app_audio/pdm/pdm_mic.h)
- [`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/app_audio/pdm/pdm_probe_logger.c)
- [`app_audio/pdm/pdm_probe_logger.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/app_audio/pdm/pdm_probe_logger.h)
- และอีก 32 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?q=int_ep07_sensorhub_final) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP07 — SensorHub Final บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/int_ep07_sensorhub_final.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- เซนเซอร์ตัวใดควรอ่านถี่ที่สุด และตัวใดอ่านช้าได้
- อะไรทำให้จอกระตุกเมื่อรวมเซนเซอร์หลายตัว
- ถ้าจะส่งข้อมูลชุดนี้ขึ้น TESAIoT Platform ควรเลือกค่าใดบ้าง

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep07_sensorhub_final) · commit `e48fbd2`
- [ค้นหาตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?q=int_ep07_sensorhub_final)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
