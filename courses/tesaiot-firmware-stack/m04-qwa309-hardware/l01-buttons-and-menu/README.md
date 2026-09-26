---
id: fw-stack.m04.l01
lang: th
title:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
summary:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
level: L2
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง"
    en: "Read active-low pull-up buttons and count presses correctly"
  - th: "นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk"
    en: "Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style"
develops:
  - {skill: mcu.gpio, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_button_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส

## เป้าหมาย

1. อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง
2. นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk

## แนวคิด

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Push Button Monitor** — อ่านปุ่มกด SW9 (P17.5) และ SW10 (P17.7) แบบ active-low pull-up แสดงสถานะกด/ปล่อย + นับจำนวนครั้งบน LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor)
- **QWA309 — Hardware Button Menu** — นำทางเมนู LVGL ด้วยปุ่มกายภาพ SW6=Move SW5=Select (ไม่ใช้ touch) — headless/kiosk UX pattern
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu)

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

- ทำไมปุ่ม active-low อ่านได้ 0 ตอนกด
- กดครั้งเดียวแต่ตัวนับขึ้นสองครั้ง สาเหตุคืออะไรและแก้อย่างไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
