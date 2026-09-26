---
id: twin.m01.l01
lang: en
title:
  th: Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง
  en: Virtual Devices, Digital Twins and Real Firmware
summary:
  th: ความหมายของ Virtual Device และ Digital Twin สถาปัตยกรรมเป็นชั้น เส้นทาง live สองเส้น (Bitstream กับ Simulator) และเกณฑ์ตัดสินใจว่าเมื่อไรต้องใช้บอร์ดจริง
  en: What a Virtual Device and a Digital Twin are, the layered architecture, the two live paths (Bitstream and Simulator) and when the real board is required.
level: L3
time_min:
  concept: 45
  practise: 15
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites: []
objectives:
- th: แยกความหมายของ Physical Device, Virtual Device, Digital Twin Platform และ Host ด้วยคำพูดของตัวเอง
  en: Distinguish Physical Device, Virtual Device, Digital Twin Platform and Host in your own words.
- th: อธิบายว่า Bitstream (UART/บอร์ด) กับ Simulator เป็นเส้นทาง live ที่ใช้ทีละเส้น และบอกเหตุผลที่ไม่ผสมกัน
  en: Explain that Bitstream (UART/board) and Simulator are live paths used one at a time, and why they are not mixed.
- th: ตัดสินใจว่าสถานการณ์ทดสอบหนึ่งใช้ Twin/Simulator ได้พอ หรือต้องยืนยันบนบอร์ดจริง พร้อมเหตุผล
  en: Decide whether a test scenario can use the Twin/Simulator or needs the real board, with a reason.
develops:
- skill: iot.digital-twin
  to: 2
- skill: sys.simulation
  to: 1
- skill: test.sil-hil
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 2c4cba261cb2d1799d7d931e7a97c1ff5e3a4125007c4740e38e9281367b98b4
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — Digital Twin Architecture

**Course 2 · Module 1**
**Suggested time:** about 2 hours (concepts + a diagram + opening the host to see the data pipeline)
**Format:** a conceptual lesson — building a full Virtual Device is not yet required (hands-on work starts in [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) / [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md))

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the **Virtual Device** and **Digital Twin** concepts in IoT / Firmware work
2. Explain the **TESA Digital Twin Platform** architecture as layers you can put into practice in the lab
3. Explain simulating signals, sensors, device behaviour, and the **Data Pipeline**
4. Identify the relationship between **real Firmware** and the **Twin Environment** — when to use a board / when to use the Simulator / when you must confirm on hardware

This module is the **mental map** for Course 2. Once you understand the Twin's architecture, installing the VS Code host ([M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md)) and building a Virtual Device ([M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md)) will have a clear frame.

> **The approach: "state the concept, then point at the real tool"**
> The course documentation talks about the Twin platform's *engines* at the architecture level.
> In the lab, the main host is **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** + the **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** pack — this lesson pairs the concept with what you actually open in the lab.

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The VS Code host — telemetry, Sensor Studio, the Simulator, MQTT, a 3D preview |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware / API examples that will flow into the Twin |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX, VSIX, the Flasher, `web-app/` dashboards |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | 3D models (GLB), textures, cubemaps, images for the Twin / Sensor Studio |
| [Course 1 TOC](../../../firmware-sdk-edge-ai/README.md) | The SDK / sensors / MQTT / BLE fundamentals |
| [Course 1 M05 — Sensor prep](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | The data source that will feed the pipeline |
| [Course 1 M06 — MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | The cloud layer the Twin will simulate/test |
| [Bluetooth / local path (C1 M07)](../../../firmware-sdk-edge-ai/m07-ble/l01-ble-connectivity/README.md) | The local option when not using Wi‑Fi |
| [Digital Twin — Wikipedia overview](https://en.wikipedia.org/wiki/Digital_twin) | A general definition outside the course (further reading) |

---

## 1. Why Digital Twin for Firmware Development

IoT / Edge AI firmware development today is no longer just "blink an LED" — a system usually has:

- Several sensors + filtering/data windows
- Several RTOS tasks
- Connectivity (Wi‑Fi / MQTT / BLE)
- A host watching values in real time, and sometimes the cloud

If you test every case on real hardware alone, you run into high cost, slow turnaround, and risk to the hardware.

**Digital Twin** in this course means building a **digital stand-in for the device** in a virtual environment, so you can develop, test, analyse and demonstrate it without relying on a real board the whole time.

### 1.1 What Twin Helps You Do

| Benefit | Meaning in the lab |
|---|---|
| Simulating hardware | Reading sensor values/status without wiring up every real pin |
| Repeatable logic testing | A script can shake the IMU / press a switch / cut the network, repeatably |
| Reducing board risk | Test edge cases on the Twin before flashing the real thing |
| Seeing results immediately | A graph / panel / 3D view / host dashboard |
| Preparing before the cloud | Checking the telemetry format / topic before going to a real broker |

> **Key phrase**
> The Twin does not replace the board 100% — it is a **bridge** between firmware theory and repeatable testing.

### 1.2 Prerequisites from Course 1

Course 2 assumes you already know (or can review):

| From Course 1 | How it's used in Course 2 |
|---|---|
| The SDK layers / chip domains | Knowing where the app code lives |
| Sensors + windows | The data that will feed the Twin / dashboard |
| MQTT / BLE | The channels the Twin and the cloud will test |
| Capstone patterns | The task structure + indication + connectivity |

---

## 2. Virtual Device vs Digital Twin

| Term | Meaning in this course |
|---|---|
| **Physical Device** | The real board + sensors (such as a PSoC Edge kit) |
| **Virtual Device** | A software model of *one device* — pins, sensors, state, response behaviour |
| **Digital Twin (Platform)** | An environment combining the Virtual Device + communication + visualization + event scripts + (often) a simulated MQTT/cloud |
| **Firmware Logic** | The product's logic code, which should run against both the Twin and hardware, once the I/O layer is properly separated |
| **Host / Twin UI** | The VS Code extension and host app you use to see the result — in this course, mainly **Bitstream Studio** |

```text
Physical Device  ≈  "the real thing on the desk"
Virtual Device   ≈  "a model of one device, in software"
Digital Twin     ≈  "a whole simulated factory" (model + comms + screen + scripts + cloud sim)
```

A good code-design goal:

- Separate **application logic** from the raw hardware detail enough
- Be able to switch targets (Simulator / board / MQTT host) without rewriting the whole app

---

## 3. TESA Digital Twin Platform Architecture

The course explains the platform as a set of **engines** working around a central core — learners don't need to memorise every sub-product's name, but should be able to point out *where each role* sits during the lab.

### 3.1 Conceptual engines (curriculum map)

```text
                    ┌─────────────────────────────┐
                    │   Development Host (VS Code) │
                    │   Bitstream Studio / tools   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
┌──────────────┐     ┌─────────────────────────┐     ┌────────────────┐
│ Firmware     │────►│  Digital Twin Engine     │────►│ Visualization  │
│ Logic        │     │  (state · time · events) │     │ Graphics / UI  │
└──────────────┘     └────────────┬────────────┘     └────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
      Communication         Scripting /           AI Connectivity
      (UART·MQTT·BLE)       Event / Behavior      (optional path)
              │
              ▼
         Cloud / Broker sim · external dashboards
```

| Layer (concept) | Role | What is usually opened in this lab |
|---|---|---|
| **Digital Twin Engine** | Manages the Virtual Device's state, simulated time, coordinates events | The sensor/mode state in Studio · the Simulator stream |
| **Communication Engine** | The data channel between firmware ↔ host ↔ cloud | The UART/bridge, the MQTT broker in Studio, the BLE host as needed |
| **Graphics / Visualization** | Graphs, panels, 3D, orientation | Sensor Telemetry · Sensor Studio · a 3D rotation preview |
| **User Interaction** | Input from the learner (buttons, scripts, toolbar modes) | Switching the Bitstream/Simulator backend · driving the scene · publishing commands |
| **Scripting & Events** | Repeatable event simulation | An event script / behaviour (detail in M03) · fault injection (M05) |
| **AI Connectivity (extra)** | Sending data off for analysis / receiving a result back | The path prepared in Course 1 M05 — not required in M01 |
| **Physics (extra)** | Simulating motion/force when a model needs it | Used when the project has a mechanism — not every lab |

> **Honest mapping**
> Each extension version's UI may differ — **remember the layer's role**, not every screen's exact button position.

### 3.2 Concrete lab stack (what you install)

| Piece | Role in Course 2 |
|---|---|
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The main VS Code host — Twin / telemetry / MQTT / 3D |
| **Bitstream Simulator** (a companion when using Simulator mode) | A virtual MCU that injects telemetry with no COM port needed |
| **A board + HEX** from [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | The physical path — confirming against the real thing |
| **The Hackathon `web-app/`** | An external dashboard watching the telemetry / MQTT pipe |
| **The [Developer Hub](https://dev.tesaiot.dev/)** | The upstream firmware examples |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB / textures / images for 3D visualization |

### 3.3 Two telemetry backends (critical mental model)

An important concept in Bitstream Studio: **Bitstream (UART/board)** and **Simulator** are live paths that are **used one at a time** — never mixed in the UI.

```text
Toolbar source = Bitstream  →  COM open  →  samples origin: uart
Toolbar source = Simulator →  COM closed →  samples origin: sim
```

| Question | Short answer |
|---|---|
| Does the Twin need a board? | Not always — the Simulator is a board-free path |
| Is a board still necessary? | Yes — for RF, analogue, power, and real pins |
| Why must they never mix? | To prevent uart/sim data from mixing into the same graph |

The lifecycle detail is practised in M02/M04 — in M01, just remember that **the Twin Environment has at least two ways into the host**.

---

## 4. Signals, Sensors, Behavior, and Data Pipeline

The Twin can simulate at several *levels of detail* — choose the one that fits the question you want answered.

### 4.1 Simulation levels

| Level | Example | Answers what question |
|---|---|---|
| **I/O / pin logic** | A virtual switch, a virtual LED | Basic control logic |
| **Sensor values** | IMU, temperature, pressure | Reading a value → filtering → deciding |
| **Behavior** | A mode change when a button is pressed | Responding to an event |
| **Connectivity** | MQTT pub/sub, a lossy link | The message format + robustness |
| **Presentation** | A graph / 3D view / dashboard | Does the user see the correct result? |

### 4.2 Data pipeline (one page)

```text
[Source]
  board sensors  or  virtual/sim sensors
        │
        ▼
[Firmware Logic]  — filter · window · decide · encode
        │
        ▼
[Communication]   — UART / MQTT / BLE
        │
        ▼
[Twin Host]       — decode · state · route
        │
        ├─► Visualization (Telemetry / Studio / 3D)
        ├─► External dashboard (Hackathon web-app)
        └─► Cloud / broker (M05)
```

Data types worth telling apart mentally (detail in M05):

| Type | Meaning |
|---|---|
| **Telemetry** | Periodic measured values (temperature, accel, …) |
| **State** | System state (connected, mode, streaming) |
| **Event** | A single-point occurrence (a threshold crossed, a button, an alert) |

What must be clear when designing a test:

1. Whether the input comes from **a script / the Simulator / a Twin user**, or from **the real world**
2. The firmware still "thinks" it is reading hardware through the layer it was designed with
3. The result must be observable in **the console + visualization**, in at least one form

---

## 5. Firmware Reality vs Twin Environment

| On a real board | On the Twin / Simulator |
|---|---|
| A driver ↔ real silicon / a real radio | A simulated port ↔ the Virtual Device / a sim injection |
| Timing from a crystal + a real RTOS | Simulated timing — the host's latency has an effect |
| Debugging with a probe / UART | Debugging through VS Code + the host's logs / panels |
| RF / analogue / power can be measured | Usually **cannot be fully simulated** — must be confirmed on the board |

### 5.1 Decision guide (preview of lab table)

| Scenario | Is the Twin/Sim enough? | Does it need a real board? |
|---|---|---|
| Mode-switching logic from a button | Usually enough | Not necessary at first |
| A JSON format / an MQTT topic | Enough (very good for this) | Confirm in a final round if using real Wi‑Fi |
| Reading the IMU and computing in code | Enough for the logic | Confirm real noise/bias on the board |
| Wi‑Fi range / BLE in a real room | Cannot substitute for this | **Required** |
| Checking a pin map / a soldering mistake | Cannot substitute for this | **Required** |

### 5.2 Recommended workflow

1. Develop and test edge cases on the **Twin / Simulator**
2. Reuse as much of the same test set (topics, payloads, scenarios) as possible
3. Confirm in a final round on **real hardware**, especially analogue, RF, and power
4. Keep evidence from both worlds when submitting the Capstone (M06)

---

## 6. Course 2 Map — Where M01 Fits

| Module | What you will do next, from this map |
|---|---|
| **M01 (now)** | Point out the Twin's layers + decide which tests fit |
| [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | Install Bitstream Studio, bind the workspace, Run/Debug and see the result |
| [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) | Build a Virtual Device + behaviour + an event script |
| [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | Co-simulate firmware ↔ Twin, measuring timing |
| [M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | The telemetry pipeline + MQTT + a lossy network |
| [M06](../../m06-integration/l01-system-integration-testing/README.md) | An E2E mini-project + delivery documentation |

---

## Next Steps

1. Do the mapping lab: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [twin-architecture-map.md](resources/twin-architecture-map.md)
3. When ready, continue to **M02 — VS Code for Twin Development**

---

## References and Further Reading

1. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
2. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**
4. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets)
5. [Course 2 TOC](../../README.md) · [Course 1 TOC](../../../firmware-sdk-edge-ai/README.md)
6. [Digital twin (overview)](https://en.wikipedia.org/wiki/Digital_twin)
7. [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) — reviewing the cloud layer touched in M05
8. [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) — the reference physical device

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: mapping the Twin architecture](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)
