---
id: c-found.m01.l03
lang: th
title: {th: 'struct, pointer และบัฟเฟอร์วงแหวน', en: 'Structs, pointers and ring buffers'}
summary: {th: จัดข้อมูลด้วย struct ส่งต่อด้วย pointer และรับข้อมูลต่อเนื่องด้วยบัฟเฟอร์วงแหวน, en: 'Organise data with structs, pass it by pointer, and stream it through a ring buffer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l02]
objectives:
- {th: ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้, en: Design a struct for one sensor sample and pass it by const pointer when it is read-only.}
- {th: เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน, en: Write a fixed-size ring buffer that never overwrites unread data.}
- {th: อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน, en: 'Explain the risk when an ISR and a task share a buffer, and how to guard it.'}
develops:
- {skill: lang.c, to: 3}
- {skill: prog.algo-ds, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้
2. เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน
3. อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- struct และ padding
- pointer, const และ array
- บัฟเฟอร์วงแหวนแบบผู้ผลิตหนึ่ง ผู้บริโภคหนึ่ง
- ข้อมูลร่วมระหว่าง ISR กับ task

## แหล่งอ้างอิง

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (ring buffer และฟังก์ชัน _from_isr)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [B3 — The IPC backbone: setup, deferred binding, snapshots (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b3__ipc__backbone.html)
