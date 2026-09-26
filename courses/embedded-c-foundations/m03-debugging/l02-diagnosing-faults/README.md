---
id: c-found.m03.l02
lang: th
title: {th: วินิจฉัยความผิดพลาดจากหลักฐาน, en: Diagnosing faults from evidence}
summary: {th: แยกสาเหตุของความผิดพลาดด้วยตัวนับและผลลัพธ์ที่ตรงไปตรงมา แทนการเดาจาก log ที่ดูน่าเชื่อ, en: Separate fault causes with honest counters and result codes instead of guessing from reassuring logs.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l01]
objectives:
- {th: ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ 'ไม่มีผลลัพธ์' และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน, en: Form at least three hypotheses for a 'no result' symptom and pick evidence that separates them.}
- {th: อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด, en: Read the SDK's diagnostic counters and locate the failing stage.}
- {th: อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ, en: Explain why functions should return honest results such as unavailable or no data instead of pretending success.}
develops:
- {skill: debug.gdb, to: 3}
- {skill: soft.problem-solving, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ 'ไม่มีผลลัพธ์' และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน
2. อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด
3. อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ตัวนับสะสมกับการอ่านค่าส่วนต่าง
- result code ที่ไม่โกหก
- อาการที่ดูเหมือนกันแต่สาเหตุต่างกัน
- ลำดับการบูตกับความผิดพลาดตอนเริ่มระบบ

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/10_model_load_diagnosis.c (สี่สาเหตุของอาการไม่มีผลลัพธ์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c)
- [SDK: แคตตาล็อกตัวอย่าง (Rules every example follows, result codes)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [B1 — CM33_NS boot walk-through (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
