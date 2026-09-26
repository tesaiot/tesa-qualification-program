---
id: fw-sdk.m08.l02
lang: th
title:
  th: 'แล็บ Capstone: มินิโปรเจกต์'
  en: 'Lab: Capstone Mini Project'
summary:
  th: สร้างมินิโปรเจกต์บนบอร์ดจริงที่รวม sensor, RTOS และ MQTT หรือ BLE สาธิตสามสถานการณ์ และส่งมอบ README ที่ทำซ้ำได้
  en: Build a mini project on the real board that combines sensing, RTOS and MQTT or BLE, demo three scenarios and hand over a reproducible README.
level: L3
time_min:
  lab: 240
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m08.l01
objectives:
- th: ส่งมอบมินิโปรเจกต์บนบอร์ดจริงที่ผ่านเกณฑ์ขั้นต่ำทั้งห้าข้อ
  en: Deliver a mini project on the real board that meets all five minimum criteria.
- th: สาธิตครบสามสถานการณ์ (Normal, Stimulus, Command) พร้อมหลักฐาน
  en: Demonstrate all three scenarios (Normal, Stimulus, Command) with evidence.
- th: เขียน README ที่ผู้อื่น build/flash ซ้ำได้โดยไม่เปิดเผยรหัสผ่าน
  en: Write a README that lets others build and flash the project without exposing passwords.
develops:
- skill: rtos.freertos
  to: 3
- skill: iot.fundamentals
  to: 2
- skill: soft.communication
  to: 2
assesses:
- skill: rtos.freertos
  level: 3
  evidence: README.md#minimum-pass-criteria
- skill: iot.fundamentals
  level: 2
  evidence: README.md#deliverables-checklist
- skill: soft.communication
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M08/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M08 — Capstone Mini Project

**Course 1 · Module 8**  
**Type:** Capstone (integrate M02–M07 on real hardware)  
**Suggested time:** 2–4 hours (+ optional extra time)  

Read first: [Lesson](../l01-capstone-and-resources/README.md) · [Capstone brief](../l01-capstone-and-resources/resources/capstone-brief.md) · [Course package](../l01-capstone-and-resources/resources/course-package.md) · [← Table of Contents](../../README.md) · [← M07](../../m07-ble/l01-ble-connectivity/README.md)

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [วางแผน Capstone และใช้แผนที่เอกสาร](../l01-capstone-and-resources/README.md)

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่** — [README ของ TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) ระบุว่า `python-app/`, `ble-react/` และ `ble-flet/` เป็นของผู้ดูแลและไม่อยู่ใน repo สาธารณะ ให้ใช้เส้นทางสำรองที่บทเรียนเสนอไว้แล้ว คือ GATT explorer ทั่วไป เช่น nRF Connect, LightBlue หรือ AIROC™ Bluetooth® Connect

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M05 lab](../../m05-sensor-data/l02-lab/README.md) | sensor / window |
| [M06 lab](../../m06-mqtt/l02-lab/README.md) | Wi‑Fi / MQTT |
| [M07 lab](../../m07-ble/l02-lab/README.md) | BLE peripheral / host |
| [M04 lab](../../m04-rtos/l02-lab/README.md) | tasks / queue |
| [Hackathon web-app / ble-flet](https://github.com/drsanti/TESAIoT_Hackathon) | live dashboard evidence |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | host / broker tools |

---

## Lab Goals

ส่งมอบมินิโปรเจกต์ที่รันบนบอร์ดจริง ครอบคลุม:

- Sensor path + indication  
- ≥ 2 FreeRTOS tasks  
- Connectivity: **MQTT และ/หรือ BLE** (อย่างน้อยหนึ่งเส้น พร้อมรับคำสั่งหรือยืนยันลิงก์)  
- README ที่ผู้อื่นทำซ้ำได้  
- หลักฐานสาธิต (รูป / คลิป / dashboard)  

---

## Prerequisites

- [ ] Lab หลัก M02–M07 ผ่านเกณฑ์ขั้นต่ำ (อย่างน้อย path ที่จะใช้ใน Capstone)  
- [ ] โปรเจกต์รวมโค้ดได้บนเครื่องคุณ  
- [ ] Broker + Wi‑Fi **หรือ** โฮสต์ BLE ที่เลือกใช้  
- [ ] เปิด [capstone-brief.md](../l01-capstone-and-resources/resources/capstone-brief.md) สำหรับกรอก  

---

## Recommended build order

1. **Architecture (30–45 นาที)** — กรอกตาราง Task / Topic / BLE ใน capstone brief  
2. **Sensor + indication** — อ่านคาบคงที่ + LED/UART  
3. **RTOS wiring** — แยก task, ใส่คิวถ้ามี producer/consumer  
4. **Connectivity** — เลือก MQTT และ/หรือ BLE แล้วทำให้ลิงก์และคำสั่งทำงาน  
5. **Hardening** — ไม่ hardcode secret; ทดสอบกระตุ้นเซ็นเซอร์ / ส่งคำสั่ง / ถอดสายสั้น ๆ  
6. **Evidence** — README + สกรีนช็อต/คลิป + (แนะนำ) Hackathon `web-app` / `ble-flet` หรือ Bitstream Studio  

---

## Minimum pass criteria

| เกณฑ์ | ต้องมี |
|---|---|
| Build + flash ได้จาก README ของคุณ | ใช่ |
| ≥ 2 Task ทำงานจริง | ใช่ |
| Sensor path + สถานะบน LED/UART | ใช่ |
| MQTT **หรือ** BLE ใช้งานได้ + รับคำสั่ง/ยืนยันลิงก์ | ใช่ |
| ไม่ฝังรหัสผ่านในไฟล์ส่งสาธารณะ | ใช่ |

### Stretch goals (optional)

- ใช้ทั้ง MQTT และ BLE  
- Threshold → `alert` publish / notify  
- Mutex ถูกต้องบนบัสร่วม  
- `to_twin` queue หรือ topic แยก  
- สาธิตบน [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) หรือ [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  

---

## Demo scenarios (test all three)

1. **Normal** — ค่าเซ็นเซอร์ไหล, LED/UART ปกติ, telemetry เข้าโฮสต์ (MQTT subscriber และ/หรือ BLE dashboard)  
2. **Stimulus** — เปลี่ยนอุณหภูมิ/ขยับบอร์ด/หมุน POT → เห็นค่าหรือ event เปลี่ยน  
3. **Command** — จาก PC/phone ส่งคำสั่ง (MQTT topic หรือ BLE write) → อุปกรณ์ตอบสนอง  

---

## Deliverables checklist

- [ ] โฟลเดอร์/ลิงก์โปรเจกต์  
- [ ] README: วิธี build, flash, Wi‑Fi/broker หรือ BLE host แบบไม่เปิดเผยรหัส, topic/UUID ที่ใช้  
- [ ] [capstone-brief.md](../l01-capstone-and-resources/resources/capstone-brief.md) กรอกครบ  
- [ ] แผนภาพหรือตาราง Task  
- [ ] หลักฐานสาธิต 3 สถานการณ์  
- [ ] ยืนยันไม่มี secret ในไฟล์สาธารณะ  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| รวมโค้ดแล้ว build พัง | รวมทีละชั้นจากโปรเจกต์ M02 ที่นิ่ง |
| MQTT ไม่ขึ้น | ตรวจ Wi‑Fi ก่อน (M06 Lab A) |
| BLE ไม่เห็นในสแกน | profile BLE เปิดหรือยัง · reboot · ADV timeout (M07) |
| Task ชนบัส | ใส่ `cm55_i2c_manager_i2c_lock` / mutex |
| สาธิตโฮสต์ไม่มีค่า | HEX/VSIX เวอร์ชัน, topic MAC, Studio Link, หรือ `ble-flet` connect |

[Lesson](../l01-capstone-and-resources/README.md) · [Capstone brief](../l01-capstone-and-resources/resources/capstone-brief.md) · [Table of Contents](../../README.md)
