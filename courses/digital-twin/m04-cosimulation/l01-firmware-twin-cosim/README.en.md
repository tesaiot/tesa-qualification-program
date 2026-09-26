---
id: twin.m04.l01
lang: en
title:
  th: 'Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา'
  en: 'Co-simulation: Prove I/O, Measure Latency, Isolate Faults'
summary:
  th: bring-up ให้เสถียรก่อน พิสูจน์เส้นทาง input/output ใช้ web-app ภายนอกเป็นหลักฐานชั้นที่สอง วัด latency และไล่ปัญหาทีละชั้น
  en: Stable bring-up first, prove the input and output paths, use an external web-app as second-layer evidence, measure latency and debug layer by layer.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m03.l02
objectives:
- th: พิสูจน์เส้นทาง input (Twin → เฟิร์มแวร์) และ output (เฟิร์มแวร์ → Twin) ด้วยหลักฐานที่ตรวจตามรอยได้
  en: Prove the input path (Twin to firmware) and the output path (firmware to Twin) with traceable evidence.
- th: วัด latency คร่าว ๆ ซ้ำสามครั้ง และระบุแหล่งหน่วงที่น่าจะเป็น
  en: Measure rough latency three times and name the likely source of delay.
- th: ไล่แยกปัญหาฝั่งเฟิร์มแวร์กับฝั่งโฮสต์ทีละชั้น โดยเปลี่ยนตัวแปรครั้งละอย่าง
  en: Isolate firmware-side and host-side faults layer by layer, changing one variable at a time.
develops:
- skill: test.sil-hil
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: soft.problem-solving
  to: 2
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 65e3c5b3364f8d410529ecb198d98c23f4acab9b2ee20cc3a5b4ec3a587b42fd
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — Firmware–Twin Co-simulation

**Course 2 · Module 4**
**Suggested time:** about 3 hours (bring-up + I/O both ways + latency notes + optional web-app evidence)
**Format:** a hands-on lesson — running firmware alongside the Twin/Simulator and proving the input–output path with evidence

[Lab](../l02-lab/README.md) · [Checklist](resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Run / test firmware together with the **Virtual Device** or the **Simulator** (and/or a real board through the host), reliably
2. Connect **Input/Output** between the Firmware and the Digital Twin so it is traceable
3. Check **Timing / Latency** and real-time data with evidence
4. Systematically isolate a firmware-side problem from a host/Twin-side one
5. Use an **outer consumer** (the Hackathon live web-app) as evidence that the data pipe isn't stuck at just one panel in Studio

This module builds on [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md), where you already have a Virtual Device + an event script — now bring **real firmware code** to run alongside the Twin, to prove the full loop before expanding into telemetry/cloud in [M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md).

> **Key phrase**
> Co-simulation = *the firmware thinks and responds* at the same time the Twin *triggers and displays the result* — not just opening a graph and watching a value.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M02 — VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | Linking Studio / the Simulator / a COM |
| [M03 — Virtual Device](../../m03-virtual-device/l01-virtual-device-modeling/README.md) | The sensor model + event script you'll trigger repeatedly |
| [Course 1 M04 — RTOS](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) | Tasks / delays that affect timing |
| [Course 1 M05 — Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | What the values flowing through co-sim mean |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The visualization host + Link |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | A HEX matched to the VSIX · the **`web-app/`** folder (live HTML examples) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware examples / API |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | 3D models for visualization (if used) |

---

## 1. What Co-simulation Means Here

In Course 2, **Firmware–Twin Co-simulation** means:

Letting the **firmware logic** run alongside the **Twin / Simulator / host** environment, at the same time, to prove that the code:

- Reads a simulated input (or from a board, through the host) correctly
- Decides per the behaviour designed in M03
- Drives an output observable on the Twin / UI / LED / **a web consumer page**

| It is not | It is |
|---|---|
| A substitute for all unit testing | A bridge before / alongside a real board |
| Just opening the Simulator and watching a sine wave | Triggering it → seeing the logic respond |
| Mixing UART + Simulator in one UI | Choosing **one** backend, per [M01](../../m01-twin-architecture/l01-twin-architecture/README.md) |
| Trusting just one panel in Studio | Confirming it again with another consumer (such as `web-app/ex05`) |

### 1.1 Two practical lab paths

| Path | Firmware runs on | Twin / host role |
|---|---|---|
| **A — Simulator** | A virtual MCU (the Bitstream Simulator) | Studio shows values as `origin: sim` |
| **B — Board + Host** | A real DevKit (a HEX / your own build) | Studio shows values as `origin: uart` |

Both paths count as co-sim with the Twin host — they differ only in the hardware input source.

```text
Path A:  [Simulator firmware] ──WS──► [Bridge] ──► [Bitstream Studio]
Path B:  [MCU firmware] ──UART──► [Bridge] ──► [Bitstream Studio]
                      ▲
                      └── same observe / command habits as Twin lab
```

### 1.2 Three places you may observe the same stream

| Observation layer | Example | Proves what |
|---|---|---|
| In Studio | Telemetry / BMI270 / a 3D rotation | The host decodes + the UI works |
| On the board / in a log | An LED, a UART print | The firmware genuinely decides |
| Outside Studio | The Hackathon **`web-app/`** HTML | The Live Data pipe reaches a general consumer (not tied to one panel) |

If all three layers (or at least Studio + the web-app) show a matching change after a trigger — you have stronger co-sim evidence than "a screenshot of one panel's graph."

---

## 2. Bring-up: Stable Session First

Before measuring I/O or latency, have **a heartbeat on both sides**.

### 2.1 Bring-up checklist

1. Open [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) from the workspace already bound in M02
2. Choose a backend: **Simulator** *or* **Bitstream** (never mixed)
3. Link / Connect until the status is normal
4. See a sensor stream or a log in at least one channel
5. (Path B) confirm the HEX/VSIX version is matched, from [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)

**Passes when:** the session is stable ≥ 30–60 seconds without the Link dropping on its own

### 2.2 What "firmware on Virtual Device" means in this course

The course documentation talks about running firmware on a Virtual Device — in the lab this usually means one of:

| Meaning | What you do |
|---|---|
| The Simulator stands in for the MCU | Start the Simulator + Link |
| Firmware on a board talks to the Twin host | Flash + a COM + Link |
| A profile/simulated port of your kit | Per your kit's guide, if it has a special abstraction layer |

Don't assume every hardware API has an automatic twin stub — if a driver only binds to real silicon, use the profile the lab pack provides, or test only the path that exists on the host (telemetry, command topics, an LED visible in the UI).

---

## 3. Connecting Inputs and Outputs

The path that must be clearly proven:

```text
[Stimulus]
  event script / UI / scene change / physical button / tilt board
        │
        ▼
[Sensor or pin value]     ← Virtual Device (M03) or real sensor
        │
        ▼
[Firmware read path]      ← task / driver / SENSOR_CFG
        │
        ▼
[Firmware decision]       ← behavior WHEN/THEN
        │
        ▼
[Firmware write path]     ← LED / flag / publish / log
        │
        ▼
[Twin / Studio / web-app observe]
```

### 3.1 Input path (Twin → Firmware)

| Step | Acceptable evidence |
|---|---|
| Triggered from the M03 script or the UI | A time note + a before screenshot |
| The value reaches the firmware | A UART log / a variable / a mode change |
| The value matches the sensor type | Compare units with [C1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) |

Common triggers used:

- Switching the scene **Lab Quiet → Motion** (the IMU path)
- Pressing a button on the board, or a host command
- Following the timeline in the M03 event script
- (A real board) tilting / rotating the board so the BMI270 fusion changes

### 3.2 Output path (Firmware → Twin)

| Step | Acceptable evidence |
|---|---|
| The firmware decides and drives an output | A command log line / an LED GPIO |
| The Twin or Studio reflects the state | A graph / a panel / 3D / a dashboard |
| An outer consumer reflects the state | The Hackathon `web-app/` (see §4) |
| The behaviour from M03 matches what's seen | WHEN/THEN in the checklist |

Basic success criteria:

1. A value triggered from the Twin/script **reaches** the firmware's behaviour
2. A command from the firmware **causes** the host's state to change as expected

### 3.3 Why an external web-app helps

A panel in Bitstream Studio might be "biased," because you are testing the same host that is already decoding the stream.
The HTML page in **`TESAIoT_Hackathon/web-app/`** is an **independent client** connected to Studio's Live Data provider — if it updates as you tilt the board or switch to the Motion scene, that shows:

- The bridge / provider is up
- The sensor id and fields are being published
- The data pipe isn't broken only within the extension's own UI

The next section walks through one example in detail: **`ex05_bmi270_orientation.html`**

---

## 4. Walkthrough — Hackathon web-app `ex05` (BMI270 orientation)

This example is an **artificial horizon + Euler angles** from the **BMI270** sensor — a good fit for M04 because:

- It shows the **output path** clearly (fusion → angles → a horizon picture)
- It forces the **publish mask** to be set correctly (Euler or Quaternion) — practising telling apart "there's a stream but the fields are wrong"
- It shows the **connection state** and **route** — helping confirm it's the same backend Studio uses

The file lives in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) repo, under the **`web-app/`** folder:

- `web-app/ex05_bmi270_orientation.html`
- Used together with `web-app/shared/ex-demo.js` (helpers: `TelemetryClient`, `resolveOrientation`, `drawHorizon`)

A map of other examples (for a rough look — MQTT detail is in M05):

| File | Role in brief |
|---|---|
| `ex04_bmi270_imu.html` | Raw accel/gyro — not orientation yet |
| **`ex05_bmi270_orientation.html`** | **M04 — fusion → horizon (this lesson's main example)** |
| `ex06_dashboard.html` | Several sensors on one screen |
| `ex08_stale_and_route.html` | Stale + route (preparing for M05) |

### 4.1 How to open it (lab flow)

1. Have Bitstream Studio **Linked** already, with a BMI270 stream (Path A or B — never mixed)
2. Clone or open the Hackathon folder that has **`web-app/`**
3. In VS Code / Studio: use a command roughly like **Serve Web App Folder over HTTP** (or another static server you're comfortable with), pointed at the `web-app/` folder
4. Open `index.html` → choose **ex05 — BMI270 Orientation**
5. Watch the top-corner badge: it should go to `connected`, with a message roughly like `route: …` once connected successfully

If you see a message like *provider not reachable* — the bridge / Studio services haven't started yet (go back to bring-up §2)

### 4.2 Prerequisites on the sensor mask

The ex05 page states clearly that **accel/gyro alone is not enough**.

You must turn on, in the sensor settings (the Virt MCU / Bitstream), at least one of these sets for the BMI270 to publish:

| Field set | Result on the web page |
|---|---|
| **Euler:** `headingRad`, `pitchRad`, `rollRad` | `resolveOrientation` uses it immediately · shows `source: euler` |
| **Quaternion:** `quatW` … `quatZ` | Converted to Euler in `ex-demo.js` · shows `source: quaternion` |

If the mask only has accel/gyro:

- Studio may still have an IMU graph
- But ex05's horizon will stay stuck at *waiting for orientation fields…*

This is a good example of **fault isolation**: the stream exists, but the consumer is silent because **the fields don't match the contract** — not because "the web-app is broken."

### 4.3 What you see on the page

| UI part | Meaning in co-sim |
|---|---|
| `#state` / `#route` | Whether the provider is connected · the route the client received (relates to the backend) |
| The artificial horizon (canvas) | A visualization of pitch + roll |
| Heading / Pitch / Roll (°) | The numeric value from the latest sample |
| `source: euler \| quaternion` | Which field set the data came from |
| `mask 0x…` | Confirms the publish mask matches what you set |
| **Stale** highlighting | No new sample within the catalog's `staleAfterMs` |

### 4.4 Data path (same stream, second screen)

```text
[Stimulus: tilt board / Motion scene / M03 script]
        │
        ▼
[BMI270 on MCU or Simulator]  →  fusion / publish per SENSOR_CFG mask
        │
        ▼
[Bridge]  →  Bitstream Studio (decode + optional 3D)
        │
        └──► Live Data provider
                    │
                    ▼
         [TelemetryClient in ex05]
                    │
                    ▼
         onSensor('bmi270') → resolveOrientation → drawHorizon + ° text
```

Compared with the §3 diagram: ex05 is the last layer, **[Twin / Studio / web-app observe]**, as an external consumer.

### 4.5 How the page code works (teaching view)

The important structure in `ex05_bmi270_orientation.html` (summarised — see the real file in Hackathon):

1. **Load the SDK** — `loadSdk()` gets `TelemetryClient` and the `bmi270` catalog entry
2. **Track staleness** — `createStaleTracker(imu.staleAfterMs, …)` changes the card's class when data is old
3. **The connection badge** — `wireConnectionBadge(client, stateEl, routeEl)`
4. **Subscribe to the sensor** — `client.onSensor('bmi270', (s) => { … })`
5. **Convert orientation** — `resolveOrientation(s.fields)`
   - Full Euler present → use it directly (`source: 'euler'`)
   - No Euler but a quat present → `quatToEuler` (`source: 'quaternion'`)
   - Neither present → `null` (nothing drawn)
6. **Draw + show the numbers** — `drawHorizon(ctx, canvas, pitch, roll)`, and convert radians → degrees
7. **connect** — `await connectTelemetry(client, routeEl)`

Concepts worth remembering:

```text
Studio Link  ≠  web-app connected
Has BMI270 raw data  ≠  has orientation fields
The horizon moves      =  the output path has reached an outer consumer
```

### 4.6 Map ex05 onto M04 I/O proofs

| M04 question | What to do with ex05 |
|---|---|
| Does **Input** reach the firmware? | Tilt the board / switch to the Motion scene, and watch whether the ° value changes (alongside a UART log, if any) |
| Does the host reflect **Output**? | The horizon + numbers move; capture it alongside the BMI270 panel in Studio |
| **Latency**? | Time it from when you start tilting until the number on ex05 changes (do 3 rounds) — usually a bit slower than the log, because of WS + the UI |
| Where is the **fault**? | See the table below |

| Symptom on ex05 | Suspect |
|---|---|
| `disconnected` / provider not reachable | The bridge / Studio services (§2) |
| `connected`, but waiting for orientation… | The mask has no Euler/Quat (§4.2) |
| The numbers are stuck + a stale card | The stream stopped / the firmware isn't publishing / the Link dropped |
| Studio has orientation, but ex05 doesn't move | The wrong folder was served · an old tab · the client didn't connect |
| The Simulator is normal, the board doesn't move | Path B: the HEX / COM / hardware |

### 4.7 Evidence to keep for the checklist

Record in `lab-notes/` (or the checklist):

1. A screenshot of Studio (Linked + BMI270) **alongside** the ex05 page, `connected`, with a horizon value
2. The `source: … · mask 0x…` line
3. A short note: how you triggered it → how the ° changed
4. (Recommended) a rough latency range over 3 rounds

> **Key phrase**
> ex05 does not replace unit testing the firmware — it is **a second mirror** showing whether the BMI270's publish reaches the world outside Studio.

---

## 5. Timing, Latency, and Real-time Observation

M04's goal is **not** the prettiest latency number, but **measuring and pointing at the source of delay** without guessing.

### 5.1 Simple measurements to record

| Measurement | Rough method | What to note |
|---|---|---|
| Stimulus → the firmware log | Time from the trigger until a log line appears | Approximate milliseconds |
| The firmware acts → the Studio UI | From the log until the graph/LED on Studio changes | Approximate milliseconds |
| The firmware acts → the web-app (ex05) | From the log / starting to tilt, until the ° on the web page changes | Approximate milliseconds |
| The sample period | Look at the scene rate / SENSOR_CFG | Hz or ms |

Repeat 3 times and note the value range (min–max) — enough for the lab.

The order usually seen: **the log is fastest → Studio close behind → the web-app slightly slower** (still within an acceptable range if consistent).

### 5.2 Where latency usually comes from

| Source | Signal |
|---|---|
| The RTOS task period / `vTaskDelay` | The value jumps per the period |
| The sensor publish interval | The Lab Quiet scene is slower than Motion |
| The bridge / WS / UI refresh | The UI / web-app is slower than the log |
| Human reaction when timing by eye | Values scatter a lot — use video or a log timestamp if possible |

Review RTOS: [Course 1 M04](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md)

### 5.3 Real-time observation habits

1. Open **Telemetry** (or the designated panel) alongside the **UART/Output log**
2. (Recommended) open **ex05** as a parallel consumer screen
3. Don't switch the backend in the middle of timing
4. Record screenshots with a clock or a round number
5. If using 3D / a GLB from M03 — confirm the animation/image doesn't mislead you into thinking it's sensor truth

A form: [cosim-checklist.md](resources/cosim-checklist.md)

---

## 6. Isolating Faults (Firmware vs Host)

When co-sim breaks, work through the layers in this order:

```text
1. Extension / backend up?          → M02
2. Correct source (sim XOR uart)? → M01/M02
3. Stream present at all?
4. Stimulus actually applied?       → M03 script / tilt / scene
5. Firmware log shows read?
6. Firmware log shows write/decision?
7. Studio UI shows change?
8. web-app (ex05) shows change?     → mask / provider / serve
```

| Symptom | Suspected side |
|---|---|
| No stream at all | The host / Link / Simulator / COM |
| A stream exists, but the firmware is silent after triggering | Input mapping / config / a task |
| The firmware log is correct, but the UI doesn't move | Visualization / the wrong panel / the consumer |
| Studio is correct, but ex05 is waiting… | The publish mask (Euler/Quat) |
| Only the board is broken, the Simulator is normal | Hardware / the HEX / a cable |
| The Simulator is broken, the board is normal | The Sim VSIX / the route |

> **Key phrase**
> Fix one layer at a time — don't change the firmware and Studio's mode at the same time in a single debug round.

---

## 7. How M04 Feeds M05 and M06

| After M04, you have | Used next in |
|---|---|
| A proven I/O loop | M05 — arranging telemetry / MQTT |
| Recorded latency / issues | M06 — E2E and the report |
| An M03 script that can run alongside firmware | Regression when you edit code |
| Familiarity with `web-app/` + the route badge | M05's stale/route examples and MQTT (ex08+) |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md) — includes an optional step to open **ex05**
2. Fill in [cosim-checklist.md](resources/cosim-checklist.md)
3. When ready, continue to [M05 — Telemetry and Cloud Simulation](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## References and Further Reading

1. [M02 VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M03 Virtual Device](../../m03-virtual-device/l01-virtual-device-modeling/README.md)
2. [Course 1 M04 RTOS](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) · [Course 1 M05 Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — especially `web-app/ex05_bmi270_orientation.html`
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**
7. [Course 2 TOC](../../README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: full-cycle I/O with co-simulation](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
