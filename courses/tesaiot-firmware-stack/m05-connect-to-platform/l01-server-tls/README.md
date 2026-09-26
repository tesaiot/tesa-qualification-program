---
id: fw-stack.m05.l01
lang: th
title:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
summary:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C"
    en: "Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example"
  - th: "อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์"
    en: "Explain what the CA certificate does when verifying the server"
develops:
  - {skill: sec.tls, to: 2}
  - {skill: proto.mqtt, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/entry/device-servertls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS

## เป้าหมาย

1. ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C
2. อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์

## แนวคิด

อุปกรณ์ที่ส่งข้อมูลขึ้นแพลตฟอร์มต้องพิสูจน์ได้ว่าคุยกับเซิร์ฟเวอร์ตัวจริง และแพลตฟอร์มต้องรู้ว่าอุปกรณ์เป็นตัวจริง บทเรียนนี้ใช้ตัวอย่างอ้างอิงของ Developer Hub ที่เชื่อมกับ TESAIoT Platform จริง

## ตัวอย่างสมบูรณ์

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด

- [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls) · commit `d2ed42c`
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- Server-TLS ยืนยันตัวตนของใคร และไม่ได้ยืนยันของใคร
- ถ้าเวลาในเครื่องผิด TLS อาจล้มเหลวเพราะอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?q=device-servertls)
- ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

