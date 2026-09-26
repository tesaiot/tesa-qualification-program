---
id: fw-stack.m05.l04
lang: th
title:
  th: "อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client"
  en: "Remote firmware update with the OTA client"
summary:
  th: "อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client"
  en: "Remote firmware update with the OTA client"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบายขั้นตอน OTA: ถามงาน อ่าน job document ดาวน์โหลด ตรวจ integrity และรายงานผล"
    en: "Explain the OTA steps: poll, read the job document, download, verify integrity and report"
  - th: "อ่านโค้ด OTA client และระบุว่าขั้นตอนใด (รายงานสถานะ ดาวน์โหลด ตรวจ integrity) ยังเป็น TODO ในตัวอย่างอ้างอิง"
    en: "Read the OTA client code and name which steps (status report, download, integrity check) are still TODO in the reference example"
develops:
  - {skill: iot.ota, to: 2}
  - {skill: mcu.bootloader, to: 1}
  - {skill: sec.fundamentals, to: 1}
context: {platform: host-pc, lang: c}
status: alpha
translation: pending
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/advanced/c_ota_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client

## เป้าหมาย

1. อธิบายขั้นตอน OTA: ถามงาน อ่าน job document ดาวน์โหลด ตรวจ integrity และรายงานผล
2. อ่านโค้ด OTA client และระบุว่าขั้นตอนใด (รายงานสถานะ ดาวน์โหลด ตรวจ integrity) ยังเป็น TODO ในตัวอย่างอ้างอิง

## แนวคิด

อุปกรณ์ที่ส่งข้อมูลขึ้นแพลตฟอร์มต้องพิสูจน์ได้ว่าคุยกับเซิร์ฟเวอร์ตัวจริง และแพลตฟอร์มต้องรู้ว่าอุปกรณ์เป็นตัวจริง บทเรียนนี้ใช้ตัวอย่างอ้างอิงของ Developer Hub ที่เชื่อมกับ TESAIoT Platform จริง

## ตัวอย่างสมบูรณ์

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด

- [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client) · commit `d2ed42c`
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

> **ระวัง:** ถ้าไม่ใส่ `--ca-cert` ตัวอย่าง `ota_client.c` ที่ commit นี้จะปิดการตรวจ certificate ของเซิร์ฟเวอร์ และตัวอย่างคำสั่งใน README ของตัวอย่างก็ไม่ได้ใส่ flag นี้ ให้ใส่ `--ca-cert` ทุกครั้ง อุปกรณ์จริงต้องไม่ปิดการตรวจ certificate

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไมต้องตรวจ integrity ของเฟิร์มแวร์ก่อนติดตั้ง
- ถ้าไฟดับระหว่างอัปเดต ระบบที่ดีควรทำอย่างไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client)
- ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

