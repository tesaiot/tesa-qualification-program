---
id: c-found.m02.l03
lang: th
title: {th: Git สำหรับงานเฟิร์มแวร์, en: Git for firmware work}
summary: {th: 'เก็บประวัติของเฟิร์มแวร์ด้วย commit, branch และ tag โดยไม่เก็บไฟล์ build และข้อมูลลับ', en: 'Keep firmware history with commits, branches and tags, without build outputs or secrets.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l02]
objectives:
- {th: สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี .gitignore ตัดไฟล์ build และ dependency ที่ดึงมา, en: Create a firmware repository whose .gitignore excludes build outputs and fetched dependencies.}
- {th: ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล, en: 'Use branches for new work and tags for released firmware, with commit messages that explain why.'}
- {th: ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ, en: 'Check before pushing that no WiFi password, key or token is in history, and explain why deleting it later is not enough.'}
develops:
- {skill: vcs.git, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี .gitignore ตัดไฟล์ build และ dependency ที่ดึงมา
2. ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล
3. ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- commit ที่ดี
- branch และ tag ของรุ่นเฟิร์มแวร์
- .gitignore สำหรับ ModusToolbox
- ข้อมูลลับในประวัติ

## แหล่งอ้างอิง

- [Pro Git (หนังสือ Git ฉบับเปิด)](https://git-scm.com/book/en/v2)
- [SDK: แม่แบบ mtb-only README (สิ่งที่ getlibs ดึงมา และไฟล์ที่ต้องจัดหาเอง)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
