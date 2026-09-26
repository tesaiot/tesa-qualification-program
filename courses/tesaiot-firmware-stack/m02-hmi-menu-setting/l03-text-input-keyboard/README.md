---
id: fw-stack.m02.l03
lang: th
title:
  th: "รับข้อความด้วย textarea และ keyboard"
  en: "Text input with a textarea and keyboard"
summary:
  th: "lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number"
  en: "Text input with a textarea and keyboard"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l02]
objectives:
  - th: "เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK"
    en: "Connect lv_textarea to lv_keyboard and take input both in real time and on OK"
  - th: "สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown"
    en: "Switch the keyboard between normal and number modes from a dropdown"
  - th: "อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน"
    en: "Explain when a value should update immediately and when it should wait for confirmation"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep03_text_input_keyboard"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# รับข้อความด้วย textarea และ keyboard

## เป้าหมาย

1. เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK
2. สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown
3. อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน

## แนวคิด

lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) แล้วไล่โค้ดตามลำดับนี้

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/main_example.c)
- [`text_input_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.c)
- [`text_input_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.h)
- [`ui_text_input_keyboard.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.c)
- [`ui_text_input_keyboard.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.h)
- [`ui_text_input_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_layout.h)

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ episode เก่าใน proj_cm55/apps/ (เก็บ app_interface.h และ _default/ ไว้)
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP03 — Text Input Keyboard บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/hmi_ep03_text_input_keyboard.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- event ใดบอกว่าผู้ใช้กด OK บนแป้นพิมพ์
- ช่องกรอกรหัส Wi-Fi ควรใช้แบบ realtime หรือ commit-on-OK เพราะอะไร
- โหมด number ป้องกันความผิดพลาดแบบไหน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
