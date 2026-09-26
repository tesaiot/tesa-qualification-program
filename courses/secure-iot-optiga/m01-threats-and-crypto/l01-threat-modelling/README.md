---
id: sec-iot.m01.l01
lang: th
title: {th: Threat model ของอุปกรณ์ IoT, en: Threat modelling an IoT device}
summary: {th: ระบุทรัพย์สิน ผู้โจมตี และช่องทางโจมตีของอุปกรณ์หนึ่งชิ้น แล้วเลือกมาตรการที่ตรวจได้, en: 'Name the assets, attackers and attack paths of one device and pick verifiable mitigations.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: []
objectives:
- {th: ระบุทรัพย์สินที่ต้องปกป้องของอุปกรณ์ IoT หนึ่งชิ้นได้อย่างน้อยสี่รายการ, en: Name at least four assets to protect on one IoT device.}
- {th: จัดภัยคุกคามตามหมวด STRIDE และจับคู่แต่ละภัยกับมาตรการป้องกันที่ตรวจได้, en: Classify threats with STRIDE and pair each with a verifiable mitigation.}
- {th: เทียบ threat model ของตัวเองกับข้อกำหนดพื้นฐานของ ETSI EN 303 645 และระบุข้อที่ยังขาด, en: Compare your threat model with the ETSI EN 303 645 baseline and list what is missing.}
develops:
- {skill: sec.fundamentals, to: 3}
- {skill: soft.problem-solving, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. ระบุทรัพย์สินที่ต้องปกป้องของอุปกรณ์ IoT หนึ่งชิ้นได้อย่างน้อยสี่รายการ
2. จัดภัยคุกคามตามหมวด STRIDE และจับคู่แต่ละภัยกับมาตรการป้องกันที่ตรวจได้
3. เทียบ threat model ของตัวเองกับข้อกำหนดพื้นฐานของ ETSI EN 303 645 และระบุข้อที่ยังขาด

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- ทรัพย์สิน ผู้โจมตี และขอบเขตความเชื่อใจ
- STRIDE
- ข้อกำหนดพื้นฐานสำหรับ IoT ผู้บริโภค
- มาตรการที่ตรวจได้

## แหล่งอ้างอิง

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OWASP Internet of Things Project](https://owasp.org/www-project-internet-of-things/)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [NIST IR 8259 Foundational Cybersecurity Activities for IoT Device Manufacturers](https://csrc.nist.gov/pubs/ir/8259/final)
