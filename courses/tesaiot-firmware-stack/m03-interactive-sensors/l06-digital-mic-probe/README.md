---
id: fw-stack.m03.l06
lang: th
title:
  th: "ไมโครโฟน PDM สเตอริโอและ level meter"
  en: "Stereo PDM microphone and a level meter"
summary:
  th: "เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL"
  en: "Stereo PDM microphone and a level meter"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l05]
objectives:
  - th: "เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา"
    en: "Capture the stereo PDM microphone and compute left/right sound levels"
  - th: "แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS"
    en: "Show the levels as a meter and explain whether it uses peak or RMS"
  - th: "ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน"
    en: "Test with sound from each side and confirm the channels are not swapped"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep06_digital_mic_probe"
  ref: e48fbd2a8d786730e30aed96eb129150e2bcf66d
---

# ไมโครโฟน PDM สเตอริโอและ level meter

## เป้าหมาย

1. เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา
2. แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS
3. ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน

## แนวคิด

เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `e48fbd2`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/main_example.c)
- [`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.c)
- [`app_audio/pdm/pdm_mic.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.h)
- [`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.c)
- [`app_audio/pdm/pdm_probe_logger.h`](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.h)
- และอีก 4 ไฟล์ใน [โฟลเดอร์ของ episode](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP06 — Digital Mic Probe บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/int_ep06_digital_mic_probe.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- PDM ต่างจาก PCM อย่างไร
- RMS กับ peak ให้ภาพระดับเสียงต่างกันอย่างไร
- ทดสอบอย่างไรว่าช่องซ้ายและขวาไม่สลับกัน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/e48fbd2a8d786730e30aed96eb129150e2bcf66d/int_ep06_digital_mic_probe) · commit `e48fbd2`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
