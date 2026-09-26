---
id: elec.m01.l01
lang: th
title: {th: แรงดัน กระแส และความต้านทาน, en: 'Voltage, current and resistance'}
summary: {th: ใช้กฎของโอห์มและกฎกำลังไฟฟ้าคำนวณวงจรพื้นฐาน, en: Use Ohm's law and the power law to work out basic circuits.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: []
objectives:
- {th: คำนวณแรงดัน กระแส หรือความต้านทานที่ไม่ทราบค่าในวงจรอนุกรมและขนานด้วยกฎของโอห์ม, en: 'Compute an unknown voltage, current or resistance in series and parallel circuits with Ohm''s law.'}
- {th: คำนวณกำลังไฟฟ้าที่ตัวต้านทานรับ และเลือกพิกัดกำลังที่เหมาะสม, en: Compute the power a resistor dissipates and choose a suitable power rating.}
develops:
- {skill: hw.circuits, to: 2}
- {skill: hw.math, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. คำนวณแรงดัน กระแส หรือความต้านทานที่ไม่ทราบค่าในวงจรอนุกรมและขนานด้วยกฎของโอห์ม
2. คำนวณกำลังไฟฟ้าที่ตัวต้านทานรับ และเลือกพิกัดกำลังที่เหมาะสม

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- แรงดัน กระแส ความต้านทาน
- อนุกรมและขนาน
- กำลังไฟฟ้าและพิกัด
- ไฟ 3.3 V บนบอร์ด

## แหล่งอ้างอิง

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (บทวงจรไฟฟ้ากระแสตรง)](https://openstax.org/details/books/university-physics-volume-2)
- [Ohm's law (Wikipedia)](https://en.wikipedia.org/wiki/Ohm%27s_law)
