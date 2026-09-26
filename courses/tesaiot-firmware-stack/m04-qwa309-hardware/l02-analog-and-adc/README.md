---
id: fw-stack.m04.l02
lang: th
title:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
summary:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์"
    en: "Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent"
  - th: "แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC"
    en: "Plot them as a scrolling scope and explain ADC resolution"
develops:
  - {skill: mcu.adc-dac, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_pot_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต

## เป้าหมาย

1. อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์
2. แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC

## แนวคิด

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Potentiometer Monitor** — อ่าน 4 potentiometers (P15.4–P15.7) ผ่าน AUTANALOG SAR ADC 12-bit (Vref 1.8V) แสดงเป็น bar + แรงดัน + เปอร์เซ็นต์ real-time — practise แรกที่ใช้ ADC จริงบน TESAIoT Dev Kit
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor)
- **QWA309 — 4-Channel ADC Scope** — plot ค่า pot 4 ตัว (P15.4-7, SAR 12-bit) เป็นเส้น scrolling บน LVGL chart 0-100% — analog oscilloscope
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope)

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

- ADC 12 บิต ที่ Vref 1.8 V แยกแรงดันได้ละเอียดกี่มิลลิโวลต์ต่อขั้น
- ทำไมค่าที่อ่านได้กระโดดเล็กน้อยแม้ไม่ได้หมุน pot

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
