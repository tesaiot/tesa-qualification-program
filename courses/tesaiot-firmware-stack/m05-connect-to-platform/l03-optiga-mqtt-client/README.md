---
id: fw-stack.m05.l03
lang: th
title:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
summary:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [eva-kit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M"
    en: "Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M"
  - th: "เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง"
    en: "Connect MQTT over TLS with the certificate stored in OPTIGA, following the example"
develops:
  - {skill: sec.secure-element, to: 2}
  - {skill: sec.tls, to: 3}
  - {skill: sec.fundamentals, to: 2}
context: {platform: psoc-edge-e84, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/security/pse84_tesaiot_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป

## เป้าหมาย

1. อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M
2. เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง

## แนวคิด

อุปกรณ์ที่ส่งข้อมูลขึ้นแพลตฟอร์มต้องพิสูจน์ได้ว่าคุยกับเซิร์ฟเวอร์ตัวจริง และแพลตฟอร์มต้องรู้ว่าอุปกรณ์เป็นตัวจริง บทเรียนนี้ใช้ตัวอย่างอ้างอิงของ Developer Hub ที่เชื่อมกับ TESAIoT Platform จริง

## ตัวอย่างสมบูรณ์

รันบนบอร์ด PSoC Edge E84 พร้อม OPTIGA™ Trust M (โปรเจกต์นี้มี BSP ของ Eva Kit: APP_KIT_PSE84_EVAL_EPC2)

- [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client) · commit `d2ed42c`
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม private key ที่อยู่ใน secure element ปลอดภัยกว่าใน flash
- Protected Update ใช้ทำอะไรกับ certificate

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client)
- โค้ดชุดนี้อยู่ภายใต้ Cypress (Infineon) EULA จึงอ้างอิงด้วยลิงก์เท่านั้น

