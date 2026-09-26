---
id: sec-iot.m03.l02
lang: th
title: {th: MQTTs ขึ้น TESAIoT Platform, en: MQTTs to the TESAIoT Platform}
summary: {th: ตามเส้นทางตั้งแต่ไฟล์ตั้งค่า งาน MQTT จนถึง broker และส่งข้อมูลขึ้นแพลตฟอร์มผ่านการเชื่อมต่อที่เข้ารหัส, en: 'Follow the path from config file to MQTT task to broker, and publish to the platform over an encrypted link.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l01]
objectives:
- {th: อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น, en: Explain the data path from config file through the MQTT task to the TESAIoT broker.}
- {th: เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด, en: Join WiFi with credentials from a store rather than hard-coded in source.}
- {th: เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน, en: Compare MQTTs and HTTPS for a device and choose for the job.}
develops:
- {skill: sec.tls, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: proto.mqtt, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น
2. เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด
3. เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ไฟล์ตั้งค่าและตัวตนของอุปกรณ์
- งาน MQTT และการเชื่อมต่อใหม่
- WiFi จากที่เก็บข้อมูลรับรอง
- HTTPS เมื่อใดเหมาะกว่า

## แหล่งอ้างอิง

- [C3 — TESAIoT cloud: config file → MQTT task → broker (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- [SDK: โมดูล tesaiot_mqtt](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/README.md)
- [SDK: cm33/connectivity/10_wifi_join.c (ข้อมูลรับรองจากที่เก็บ ไม่ใช่ #define)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c)
- [SDK: cm33/connectivity/03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c)
- [TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) — Unified, intermediate-level C example that can send telemetry over either:
- [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) — **Firmware Version:** v3.0.0 Production
