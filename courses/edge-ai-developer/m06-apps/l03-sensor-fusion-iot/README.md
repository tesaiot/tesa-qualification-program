---
id: edgeai-dev.m06.l03
lang: th
title: {th: รวมหลายแหล่งข้อมูลและส่งขึ้น IoT, en: Sensor fusion and IoT}
summary: {th: รวมผลของโมเดลกับค่าเซนเซอร์ดิบเพื่อตัดสินใจ แล้วส่งเหตุการณ์ขึ้นแพลตฟอร์มผ่าน MQTT, en: 'Fuse model results with raw sensor values to decide, and publish events over MQTT.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m06.l02]
objectives:
- {th: ออกแบบการตัดสินใจที่ใช้ทั้งผลของโมเดลและค่าเซนเซอร์ดิบ และอธิบายว่าดีกว่าแหล่งเดียวอย่างไร, en: Design a decision that uses both model results and raw sensor values and explain why it beats a single source.}
- {th: ส่งเหตุการณ์ที่ตัดสินแล้วขึ้นแพลตฟอร์มผ่าน MQTT โดยส่งเฉพาะเหตุการณ์ ไม่ส่งข้อมูลดิบ, en: 'Publish decided events over MQTT, sending events rather than raw data.'}
develops:
- {skill: iot.cloud-platform, to: 3}
- {skill: proto.mqtt, to: 3}
- {skill: ai.edge, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ออกแบบการตัดสินใจที่ใช้ทั้งผลของโมเดลและค่าเซนเซอร์ดิบ และอธิบายว่าดีกว่าแหล่งเดียวอย่างไร
2. ส่งเหตุการณ์ที่ตัดสินแล้วขึ้นแพลตฟอร์มผ่าน MQTT โดยส่งเฉพาะเหตุการณ์ ไม่ส่งข้อมูลดิบ

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s10/08_real_sensor_leaves_the_board.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s10/08_real_sensor_leaves_the_board.py)
- [SDK: cm55/sensors/02_radar_presence.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c)
