---
id: fw-sdk.m08.l02
lang: en
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
translation: done
slides: slides.md
source_sha256: fca456b305037aa3e125a6b9444f4e29cfb9d1aed35d8a4d37a9628edc6aa2fe
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

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [Plan the Capstone and Use the Resource Map](../l01-capstone-and-resources/README.md)

> **The `ble-flet` host is not yet published** — the [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) states that `python-app/`, `ble-react/` and `ble-flet/` belong to the maintainers and are not in the public repo. Use the backup path the lesson already suggests: a general GATT explorer such as nRF Connect, LightBlue, or AIROC™ Bluetooth® Connect

### Useful references during the lab

| Document | Use when |
|---|---|
| [M05 lab](../../m05-sensor-data/l02-lab/README.md) | sensor / window |
| [M06 lab](../../m06-mqtt/l02-lab/README.md) | Wi‑Fi / MQTT |
| [M07 lab](../../m07-ble/l02-lab/README.md) | A BLE peripheral / host |
| [M04 lab](../../m04-rtos/l02-lab/README.md) | Tasks / queue |
| [Hackathon web-app / ble-flet](https://github.com/drsanti/TESAIoT_Hackathon) | Live dashboard evidence |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Host / broker tools |

---

## Lab Goals

Deliver a mini-project running on real hardware, covering:

- A sensor path + indication
- ≥ 2 FreeRTOS tasks
- Connectivity: **MQTT and/or BLE** (at least one path, with a command received or a link confirmed)
- A README others can reproduce
- Demo evidence (a photo / clip / dashboard)

---

## Prerequisites

- [ ] The main labs M02–M07 meet their minimum bar (at least the path you'll use in the Capstone)
- [ ] The combined project builds on your machine
- [ ] A broker + Wi‑Fi **or** a BLE host of your choice
- [ ] [capstone-brief.md](../l01-capstone-and-resources/resources/capstone-brief.md) open, ready to fill in

---

## Recommended build order

1. **Architecture (30–45 minutes)** — fill in the Task / Topic / BLE table in the capstone brief
2. **Sensor + indication** — a fixed-period read + LED/UART
3. **RTOS wiring** — split into tasks, add a queue if there's a producer/consumer
4. **Connectivity** — choose MQTT and/or BLE and get the link and commands working
5. **Hardening** — don't hardcode secrets; test triggering the sensor / sending a command / briefly disconnecting the cable
6. **Evidence** — a README + screenshots/a clip + (recommended) the Hackathon `web-app` / `ble-flet`, or Bitstream Studio

---

## Minimum pass criteria

| Criterion | Required |
|---|---|
| Builds + flashes from your README | Yes |
| ≥ 2 tasks genuinely running | Yes |
| A sensor path + status on LED/UART | Yes |
| MQTT **or** BLE works + a command received/a link confirmed | Yes |
| No password embedded in files submitted publicly | Yes |

### Stretch goals (optional)

- Use both MQTT and BLE
- A threshold → an `alert` publish / notify
- A correct mutex on a shared bus
- A separate `to_twin` queue or topic
- Demonstrate on [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) or [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)

---

## Demo scenarios (test all three)

1. **Normal** — sensor values flow, LED/UART behave normally, telemetry reaches the host (an MQTT subscriber and/or a BLE dashboard)
2. **Stimulus** — change the temperature/move the board/turn the POT → see the value or an event change
3. **Command** — from a PC/phone, send a command (an MQTT topic or a BLE write) → the device responds

---

## Deliverables checklist

- [ ] The project folder/link
- [ ] A README: how to build, flash, the Wi‑Fi/broker or BLE host without exposing a password, and the topic/UUID used
- [ ] [capstone-brief.md](../l01-capstone-and-resources/resources/capstone-brief.md) filled in completely
- [ ] A diagram or table of Tasks
- [ ] Demo evidence for all 3 scenarios
- [ ] Confirmation there are no secrets in public files

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| Combining code breaks the build | Combine one layer at a time from a stable M02 project |
| MQTT never comes up | Check Wi‑Fi first (M06 Lab A) |
| BLE not seen in a scan | Is the BLE profile on? · reboot · an ADV timeout (M07) |
| Tasks collide on the bus | Add `cm55_i2c_manager_i2c_lock` / a mutex |
| The host demo shows no value | The HEX/VSIX version, the MAC topic, the Studio Link, or the `ble-flet` connection |

[Lesson](../l01-capstone-and-resources/README.md) · [Capstone brief](../l01-capstone-and-resources/resources/capstone-brief.md) · [Table of Contents](../../README.md)
