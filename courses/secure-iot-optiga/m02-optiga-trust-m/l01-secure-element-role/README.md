---
id: sec-iot.m02.l01
lang: th
title: {th: ชิปความปลอดภัยทำอะไรให้เรา, en: What a secure element does for us}
summary: {th: รู้ว่า OPTIGA™ Trust M เก็บและทำอะไร และอ่านสถานะของ HSM จาก SDK โดยไม่เริ่มธุรกรรม, en: 'Learn what OPTIGA™ Trust M stores and does, and read HSM state from the SDK without starting a transaction.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l02]
objectives:
- {th: ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข, en: 'Name at least three secure-element functions, such as key storage, signing and random numbers.'}
- {th: อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK, en: 'Read HSM state with calls that need no chip transaction, following the SDK reference example.'}
- {th: อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น, en: Explain which chip operations are irreversible and why the lessons will not touch them.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: sec.crypto, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข
2. อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK
3. อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- OPTIGA™ Trust M ในระบบ
- object และ metadata
- สถานะที่เปลี่ยนทางเดียว
- อ่านสถานะโดยไม่เริ่มธุรกรรม

## แหล่งอ้างอิง

- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3)
- [SDK: เอกสาร tesaiot_hsm](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/README.md)
- [SDK: cm33/security/ref_hsm.c (อ่านสถานะโดยไม่เริ่มธุรกรรม)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c)
- [SDK: ตัวอย่างฝั่ง CM33 (ข้อควรทราบเรื่องสถานะ LcsO)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) — **Firmware Version:** v3.0.0 Production
