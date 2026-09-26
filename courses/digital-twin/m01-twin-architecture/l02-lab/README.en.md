---
id: twin.m01.l02
lang: en
title:
  th: 'แล็บ: แผนที่สถาปัตยกรรม Twin'
  en: 'Lab: Twin Architecture Map'
summary:
  th: นิยามคำด้วยภาษาตัวเอง วาด data flow และกรอกตารางตัดสินใจว่าเทสไหนใช้ Twin ได้ เทสไหนต้องบอร์ด
  en: Define the terms in your own words, draw the data flow and fill in the table of which tests the Twin can cover and which need a board.
level: L3
time_min:
  lab: 45
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- twin.m01.l01
objectives:
- th: วาดแผนภาพ data flow ของระบบตัวอย่างหนึ่งชุด ตั้งแต่เซ็นเซอร์ถึง dashboard
  en: Draw the data flow of one example system from sensor to dashboard.
- th: กรอกตารางตัดสินใจอย่างน้อย 4 แถว โดยมีทั้งแถวที่ “Twin พอ” และ “ต้องบอร์ด”
  en: Fill at least four rows of the decision table, including both a “Twin is enough” row and a “needs the board” row.
develops:
- skill: iot.digital-twin
  to: 2
- skill: test.sil-hil
  to: 1
assesses:
- skill: iot.digital-twin
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 94a0c100130ec3b3e8ecb01daf39b56e93ce7a27299c25ccd3ba961a305b46e9
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Twin Architecture Map

**Course 2 · Module 1**
**Type:** Conceptual + diagram (+ optional host peek)
**Suggested time:** 30–45 minutes

Read first: [Lesson](../l01-twin-architecture/README.md) · [Cheatsheet](../l01-twin-architecture/resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Pointing out Visualization / Communication on the real host |
| [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | `web-app/` = a dashboard outside the Studio screen |
| [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | Reviewing MQTT in the pipeline |

---

## Lab Goals

- Distinguish **Virtual Device / Twin Platform / Firmware Logic / Host** in your own words
- Draw the **data flow** of one example system
- Fill in a decision table: is the Twin enough / does it need a real board?
- (Recommended) briefly open a host or dashboard to connect the concept with the real thing

---

## Part A — Definitions (your words)

Write 2–3 sentences for each:

1. What is a **Virtual Device**?
2. What does **Digital Twin** in this course cover, *besides* the device itself?
3. Why must **Firmware Logic** be separated from hardware detail?

**Pass when:** someone else on the team reads it and understands, without opening the lesson

---

## Part B — Architecture diagram

Draw (on paper / in Mermaid / as text boxes) showing at least:

- VS Code / Bitstream Studio
- Firmware Logic
- The communication path (UART and/or MQTT)
- The Twin Engine / Virtual Device (or Simulator)
- Visualization or a Dashboard
- (If any) Cloud / a broker

An example blank skeleton:

```text
[VS Code + Bitstream Studio]
        │
[Firmware Logic] ──comm──► [Twin / Simulator state]
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              [Telemetry UI]          [web-app / MQTT]
```

**Pass when:** the data-direction arrows are clear, and you can point out which box the Virtual Device is in

---

## Part C — Test decision table

Fill in at least 4 rows (all rows recommended):

| Test scenario | Is the Twin / Sim enough? | Does it need a real board? | Short reason |
|---|---|---|---|
| Mode-switching logic from a button | | | |
| Reading the IMU and computing in code | | | |
| Checking the MQTT JSON format / topic | | | |
| Wi‑Fi or BLE range in a real room | | | |
| Checking a pin map / a wrong pin | | | |
| Measuring power / battery life | | | |

**Pass when:** at least one row answers "the Twin is enough" and one row answers "needs a board"

---

## Part D — Optional host peek (recommended)

Choose at least one:

1. Open **Bitstream Studio** and point out to a friend which panel is Visualization / where you switch Bitstream vs Simulator
2. Open a dashboard page in the [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) (per your kit's guide) and explain which layer of the Part B diagram it belongs to

**Pass when (optional):** you have a 3–5 line note on "what I see on screen = which layer of the architecture"

---

## Deliverables checklist

- [ ] Part A's all 3 items complete
- [ ] Part B's diagram
- [ ] Part C's table, ≥ 4 rows
- [ ] (Recommended) Part D's note

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| Confusing the Virtual Device with the Twin | The Device = a model of one machine; the Twin = the whole surrounding system |
| Not sure where to draw the Simulator | Put it alongside the Twin Engine / Virtual Device as a *simulated data source* |
| Thinking the Twin can replace the board for everything | Look at the RF / pin / power rows in table C |

[Lesson](../l01-twin-architecture/README.md) · [Cheatsheet](../l01-twin-architecture/resources/twin-architecture-map.md) · [Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)
