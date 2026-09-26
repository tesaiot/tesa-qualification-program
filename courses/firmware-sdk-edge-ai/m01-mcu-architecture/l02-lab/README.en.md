---
id: fw-sdk.m01.l02
lang: en
title:
  th: 'แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK'
  en: 'Lab: Map MCU Domains to SDK Layers'
summary:
  th: 'แล็บเชิงแนวคิด (ไม่ต้อง flash บอร์ด): กรอกตารางจับคู่โดเมนกับงาน ติดป้ายชั้นซอฟต์แวร์ และตอบโจทย์รวมสองสถานการณ์'
  en: 'A conceptual lab (no flashing): fill in the domain-to-workload table, label the software layers and answer two integrated scenarios.'
level: L3
time_min:
  lab: 45
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- fw-sdk.m01.l01
objectives:
- th: กรอกตารางจับคู่โดเมนกับงาน (ส่วนที่ 1) และตารางชั้นซอฟต์แวร์ (ส่วนที่ 2) ครบทุกแถวพร้อมเหตุผล
  en: Complete the domain-to-workload table (Part 1) and the software-layer table (Part 2) with a reason for every row.
- th: ทำ checklist จริง/เท็จ (ส่วนที่ 4) ถูกอย่างน้อย 8 จาก 10 ข้อ
  en: Score at least 8 of 10 on the true/false checklist (Part 4).
develops:
- skill: hw.architecture
  to: 2
- skill: build.vendor-sdk
  to: 1
assesses:
- skill: hw.architecture
  level: 2
  evidence: README.md#submission-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: ea74094d7e08a7e652c93e8b299658af475b070e8670374e17c859ff662191b1
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Map MCU Domains to TESA Firmware SDK Layers

**Course 1 · Module 1**
**Type:** Conceptual lab (no board flash required)
**Suggested time:** 30–45 minutes

Read first: [Lesson](../l01-architecture-and-sdk-layers/README.md) · [Cheatsheet](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

### Useful references while you map domains

| Document | Use when |
|---|---|
| [E84 Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) | Checking domain names / NPU / HMI |
| [AN241775 — HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | Matching the BSP / PDL / HAL terminology |
| [Arm Cortex-M55](https://developer.arm.com/Processors/Cortex-M55) · [Ethos-U55](https://developer.arm.com/Processors/Ethos-U55) | Reading deeper on the core / NPU |

---

## Lab Goals

Once complete, you will:

- Match hardware domains (Cortex-M55 / Cortex-M33 / Ethos-U55 NPU) to workload types with sound reasoning
- Identify which layer (HAL/BSP, Driver API, Utility or Application) each kind of code should sit in
- Check your understanding with a short checklist

---

## Prerequisites

- [ ] Have finished reading the [lesson](../l01-architecture-and-sdk-layers/README.md)
- [ ] Have the summary sheet [sdk-layer-cheatsheet.md](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) open
- [ ] Paper, notes, or an empty file to fill in answers

> **Where's Flash / Hello World?**
> Installing ModusToolbox, creating a project, and flashing the board are in **M02**.
> This lab is deliberately a mental map, before you get hands-on with the tools.

---

## Part 1 — Map Domains to Workloads

From the table below, choose the most suitable domain for each task.
You may answer with more than one domain if needed, but must write a short reason.

| # | Task | Options | Your answer | Short reason |
|---|---|---|---|---|
| 1 | Loop reading buttons and blinking an LED per the UI state | M55 / M33 / NPU | | |
| 2 | Listen for a wake word continuously, low-power | M55 / M33 / NPU | | |
| 3 | Run a gesture-recognition model on the device | M55 / M33 / NPU | | |
| 4 | Format JSON and publish MQTT | M55 / M33 / NPU | | |

### Self-Check Guidance (read after answering)

| # | Guidance |
|---|---|
| 1 | Main UI/control work usually sits on the **Cortex-M55** |
| 2 | Always-on / low-power work usually ties to the **Cortex-M33** |
| 3 | Heavy inference work usually relies on the **Ethos-U55 (NPU)** (an app on M55 still coordinates it) |
| 4 | Building the payload / MQTT is **Application work on the main core** — not directly the NPU's job |

You don't need to match this table word for word; if your reasoning agrees with the multi-domain principle, it counts as a pass.

---

## Part 2 — Label the SDK Layers

Assume a simplified firmware project folder structure (hypothetical names for learning — not the SDK's real paths):

```text
app/
  main.c                 # product logic, creates tasks
  gesture_policy.c       # decides once an inference result comes back
bsp/
  board_init.c           # clock, pin mux, bring-up
drivers/
  gpio_api.c
  i2c_api.c
  uart_api.c
utils/
  ring_buffer.c
  simple_filter.c
```

Fill in the table:

| File group | Layer (HAL/BSP, Driver, Utility, Application) | Short reason |
|---|---|---|
| `bsp/board_init.c` | | |
| `drivers/i2c_api.c` | | |
| `utils/ring_buffer.c` | | |
| `app/gesture_policy.c` | | |

### Self-Check Guidance

| File group | Expected layer |
|---|---|
| `bsp/board_init.c` | HAL / BSP |
| `drivers/i2c_api.c` | Driver API |
| `utils/ring_buffer.c` | Utility |
| `app/gesture_policy.c` | Application |

---

## Part 3 — Integrated Scenarios

### 3A — On-Device Gesture

The task:

> Read IMU values periodically over I²C → keep a short window of samples → feed it into a model on the Ethos-U55 → if it's a gesture of interest, turn on an LED and prepare a message for the cloud

Answer point by point (no code needed):

1. Which layer is responsible for talking I²C to the sensor chip?
2. Which layer suits the sample-window buffer?
3. Which domain/hardware block accelerates advanced inference?
4. Which layer decides "this gesture is important enough to turn on the LED"?
5. Why is publishing MQTT still not the NPU's job?

### Self-Check Guidance (3A)

1. Driver API
2. Utility (or a structure in the Application that calls the utility)
3. Ethos-U55 NPU
4. Application
5. The NPU accelerates model computation — formatting the message and the protocol is app/communication-stack work on the main core

### 3B — Always-On Then Wake

The task:

> The system waits to catch audio activity on the low-power domain all night; once an event occurs, it wakes the high-performance domain to run a heavy model and update the screen

Answer:

1. Which core/accelerator suits the "listening all night" phase?
2. Which core/accelerator suits the "heavy inference after being woken" phase?
3. Why should the Ethos-U55 not run at full power for 24 hours if the product runs on a battery?

### Self-Check Guidance (3B)

1. The Cortex-M33 and/or NNLite
2. The Cortex-M55 coordinating + the Ethos-U55
3. The high-performance domain and the NPU use more power — always-on work should sit in the low-power domain and only wake the other when needed

---

## Part 4 — Understanding Checklist (True / False)

Answer **True** or **False**

1. TESA Firmware SDK is the name of an IDE program that replaces ModusToolbox
2. HAL/BSP lets a developer avoid setting up the board's basic registers by hand every time
3. The Driver API is the main layer for controlling GPIO, UART, I2C, SPI, PWM, ADC, in this course's approach
4. Utility modules replace the Driver when you need to talk to hardware directly
5. The Cortex-M55 and the Ethos-U55 play the same role in every task
6. Edge AI always means sending all raw data up to the cloud
7. Choosing a processing domain affects power and latency
8. M01 requires learners to successfully flash Hello World firmware
9. Chip-level security (such as Secure Boot) is part of the architecture, not a topic separate from the MCU
10. The next lesson (M02) will get hands-on installing tools and building a real project

### Checklist Answers

1. False — SDK ≠ IDE
2. True
3. True
4. False — Utility does not replace the Driver
5. False — they play different roles
6. False — Edge AI aims to process at the edge
7. True
8. False — that belongs to M02
9. True
10. True

Suggested bar: at least 8/10 before moving to M02

---

## Common Misconceptions

| Misconception | How to fix it |
|---|---|
| Having an NPU means you don't need to write I/O-controlling firmware | The NPU accelerates inference — reading sensors/driving actuators still goes through the Driver and the app |
| Utility is just a shorthand driver | Utility helps with repeated work — talking to hardware still goes through HAL/Driver |
| You must memorise the whole datasheet before the first lab | M01 focuses on the architecture and SDK-layer map |

---

## Submission Checklist

- [ ] Part 1's table filled in completely, with reasons
- [ ] Part 2's table filled in completely
- [ ] Parts 3A and 3B fully answered
- [ ] Part 4's checklist scored at least 8/10
- [ ] Ready for M02, able to explain how the SDK differs from the IDE, and how multi-domain differs from a single core

---

[Lesson](../l01-architecture-and-sdk-layers/README.md) · [Cheatsheet](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) · [Table of Contents](../../README.md)
