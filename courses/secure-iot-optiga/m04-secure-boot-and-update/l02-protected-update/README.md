---
id: sec-iot.m04.l02
lang: th
title: {th: Protected Update, en: Protected Update}
summary: {th: ขออัปเดตแบบป้องกันจากแพลตฟอร์ม เข้าใจตัวนับกันย้อนรุ่น และการเปลี่ยนแปลงบนชิปที่ย้อนกลับไม่ได้, en: 'Request a protected update from the platform, and understand the anti-rollback counter and irreversible chip changes.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m04.l01]
objectives:
- {th: อธิบายขั้นตอนของ Protected Update ตั้งแต่คำขอจนถึงการตรวจ manifest, en: Explain Protected Update from request to manifest verification.}
- {th: อธิบายหน้าที่ของตัวนับกันย้อนรุ่น และผลของ manifest lock, en: Explain the anti-rollback counter and the effect of a manifest lock.}
- {th: ระบุการเปลี่ยนแปลงบนชิปที่รีแฟลชแล้วก็กู้คืนไม่ได้ ตามที่ตัวอย่างของ SDK เตือนไว้, en: 'Identify the chip change that no reflash can undo, as the SDK example warns.'}
develops:
- {skill: sec.secure-boot, to: 3}
- {skill: iot.ota, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายขั้นตอนของ Protected Update ตั้งแต่คำขอจนถึงการตรวจ manifest
2. อธิบายหน้าที่ของตัวนับกันย้อนรุ่น และผลของ manifest lock
3. ระบุการเปลี่ยนแปลงบนชิปที่รีแฟลชแล้วก็กู้คืนไม่ได้ ตามที่ตัวอย่างของ SDK เตือนไว้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- manifest และลายเซ็น
- ตัวนับกันย้อนรุ่น
- manifest lock
- การตรวจลายเซ็นของโมเดลที่ถูก stage

## แหล่งอ้างอิง

- [SDK: cm33/security/06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c)
- [SDK: PROTECTED_UPDATE_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/PROTECTED_UPDATE_CONTRACT.md)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [SDK: cm33/security/02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c)
- [Firmware update (BLE NUS) (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__ble__nus__fw__update.html)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [TESAIoT OTA HTTPS Client (C Version)](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) — A C implementation of the TESAIoT OTA (Over-The-Air) update client for embedded devices.
- [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) — **Firmware Version:** v3.0.0 Production
