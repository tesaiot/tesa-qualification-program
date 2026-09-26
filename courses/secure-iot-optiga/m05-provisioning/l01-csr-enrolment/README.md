---
id: sec-iot.m05.l01
lang: th
title: {th: ลงทะเบียนด้วย CSR, en: Enrolment with a CSR}
summary: {th: สร้างคำขอใบรับรองจากกุญแจในชิป ส่งให้แพลตฟอร์ม และติดตามคำขอจนได้ใบรับรอง, en: 'Create a certificate request from the on-chip key, send it to the platform and track it to a certificate.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m04.l02]
objectives:
- {th: อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป, en: Explain what a CSR contains and why the private key never leaves the chip.}
- {th: ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK, en: Track a request by correlation id and target OIDs as the SDK example does.}
- {th: ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก, en: State the buffer contract the CSR publishing function imposes on its caller.}
develops:
- {skill: sec.crypto, to: 3}
- {skill: sec.secure-element, to: 3}
- {skill: iot.cloud-platform, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป
2. ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK
3. ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- PKCS #10 และ CSR
- correlation id และ OID
- สัญญาของการส่ง CSR
- เมื่อคำขอล้มเหลว

## แหล่งอ้างอิง

- [SDK: cm33/security/05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c)
- [SDK: CSR_SUBMISSION_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- [RFC 2986: PKCS #10 Certification Request Syntax](https://www.rfc-editor.org/rfc/rfc2986)
