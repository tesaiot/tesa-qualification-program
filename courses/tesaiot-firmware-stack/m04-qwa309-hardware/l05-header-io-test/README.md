---
id: fw-stack.m04.l05
lang: th
title:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
summary:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ"
    en: "Exercise every I/O type on the header with the diagnostic program and read the on-screen console"
  - th: "ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป"
    en: "Confirm at least one signal with a logic analyzer or oscilloscope"
develops:
  - {skill: proto.uart, to: 2}
  - {skill: proto.spi, to: 1}
  - {skill: proto.i2c, to: 2}
  - {skill: mcu.pwm, to: 1}
  - {skill: meas.logic-analyzer, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_header_hw_test"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC

## เป้าหมาย

1. ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ
2. ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป

## แนวคิด

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Header I/O Test** — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)

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

- SPI แบบ bit-bang ต่างจาก SPI ด้วยฮาร์ดแวร์อย่างไร
- ถ้าโปรแกรมรายงานว่า UART ผ่าน แต่ logic analyzer ไม่เห็นสัญญาณ เชื่ออะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
