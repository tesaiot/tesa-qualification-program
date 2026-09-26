---
id: c-found.m06.l01
lang: th
title: {th: Unit test บนเครื่องโฮสต์, en: Unit tests on the host}
summary: {th: แยกตรรกะออกจากฮาร์ดแวร์เพื่อทดสอบบนเครื่องโฮสต์ด้วย Unity, en: Separate logic from hardware to test it on the host with Unity.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l03]
objectives:
- {th: แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้, en: Split logic such as a filter or state machine from hardware-touching code so it compiles on the host.}
- {th: เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด, en: 'Write Unity tests covering normal, edge and error cases.'}
- {th: พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน, en: Prove a test can fail by planting a bug before trusting a pass.}
develops:
- {skill: test.unit-tdd, to: 3}
- {skill: prog.state-machines, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้
2. เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด
3. พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ตะเข็บระหว่างตรรกะกับฮาร์ดแวร์
- Unity: assertion และ test runner
- test ที่ล้มเหลวไม่เป็นคือ test ที่ไม่ได้ทดสอบอะไร
- TDD แบบย่อ

## แหล่งอ้างอิง

- [ThrowTheSwitch Unity @ v2.7.0](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0)
- [Unity test framework](https://www.throwtheswitch.org/unity)
