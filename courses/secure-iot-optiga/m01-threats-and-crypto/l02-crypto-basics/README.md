---
id: sec-iot.m01.l02
lang: th
title: {th: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว, en: Crypto basics for embedded systems}
summary: {th: 'แยกหน้าที่ของ hash, MAC, ลายเซ็นดิจิทัล การเข้ารหัสสองแบบ และใบรับรอง X.509', en: 'Tell apart hashes, MACs, digital signatures, the two kinds of encryption and X.509 certificates.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l01]
objectives:
- {th: เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย ความลับ ความถูกต้อง หรือการยืนยันตัวตน ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี, en: 'Pick the right primitive for confidentiality, integrity or authenticity in at least 4 of 5 cases.'}
- {th: 'อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้', en: 'Read an X.509 certificate and identify subject, issuer, validity and public key.'}
- {th: อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป, en: Explain why private keys belong in a secure element rather than general flash.}
develops:
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย ความลับ ความถูกต้อง หรือการยืนยันตัวตน ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี
2. อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้
3. อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- hash และ HMAC
- สมมาตรและอสมมาตร
- ลายเซ็นดิจิทัลและ chain of trust
- ใบรับรอง X.509

## แหล่งอ้างอิง

- [RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
