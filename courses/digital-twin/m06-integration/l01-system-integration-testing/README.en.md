---
id: twin.m06.l01
lang: en
title:
  th: ทดสอบ end-to-end บน Digital Twin
  en: End-to-end Testing on the Digital Twin
summary:
  th: เกณฑ์ผ่านขั้นต่ำของ Capstone การวิเคราะห์ log ทีละชั้น โจทย์จากโดเมนจริง และกรณีศึกษา Smart Environmental Monitor
  en: The capstone's minimum rubric, layer-by-layer log analysis, domain stories and the Smart Environmental Monitor case study.
level: L3
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m05.l02
objectives:
- th: ตรวจระบบ Twin แบบ end-to-end ตามเกณฑ์ผ่านขั้นต่ำ (virtual device + script, co-sim, visualization, MQTT, README, ตารางเทส ≥ 3 เคส)
  en: Check a Twin system end to end against the minimum rubric (virtual device + script, co-sim, visualisation, MQTT, README, at least three test cases).
- th: วิเคราะห์ log ทีละชั้น โดยเก็บ log ฝั่งเฟิร์มแวร์และฝั่งโฮสต์ในรอบเดียวกัน
  en: Analyse logs layer by layer, capturing firmware-side and host-side logs in the same run.
- th: แปลงโจทย์จากโดเมนจริง (IoT ทั่วไป บ้าน โรงงาน สุขภาพ) ลงท่อ Twin ชุดเดียวกัน
  en: Map a real-domain story (general IoT, home, factory, health) onto the same Twin pipeline.
develops:
- skill: test.sil-hil
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: soft.communication
  to: 2
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 8d0edeae2b10f1cbc97ded33949cfcfccf93412f4f92255d6609b9195337a025
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — System Integration and Testing

**Course 2 · Module 6**
**Suggested time:** about 2 hours + extra time to make the mini-project complete
**Format:** Capstone — combining M01–M05 into a repeatably demonstrable system, with an E2E test table and evidence

[Lab](../l02-lab/README.md) · [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Test a system **End-to-End** (Firmware + Twin + Cloud/Dashboard)
2. Analyse **Logs** and fix problems with evidence
3. Do a case study / mini-project (such as a **Smart Environmental Monitor**) and map it onto a **real domain** — general IoT · in the home · a factory · health
4. Use the **Developer Guide / project examples** and the course's online documentation pack
5. Deliver the full lab: building a Twin model, testing code through the Twin, simulating sensors/signals

> **Key phrase**
> The Course 2 Capstone = *choosing and connecting pieces you've already built* into a pass/fail table — not writing a whole new Twin from scratch.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M01](../../m01-twin-architecture/l01-twin-architecture/README.md)–[M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | The pieces that need combining |
| [Course 1 M08 Capstone](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) | The delivery form / rubric on the firmware side |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The Twin host · broker · visualization |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX · VSIX · **`web-app/`** (ex06 · ex15) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware examples / API |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | A GLB for a 3D demo (if used) |
| [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) | The deliverable forms |

---

## 1. Course 2 Lab Index (What You Already Have)

| Module | Lab focus | Used in M06 |
|---|---|---|
| [M01](../../m01-twin-architecture/l02-lab/README.md) | The Twin map / the backend XOR rule | Explaining the demo's architecture |
| [M02](../../m02-vscode-twin/l02-lab/README.md) | The Studio workspace / Link | A repeatable bring-up |
| [M03](../../m03-virtual-device/l02-lab/README.md) | A virtual device + event script (+ GLB) | The sensor trigger source |
| [M04](../../m04-cosimulation/l02-lab/README.md) | Co-sim I/O · optional `ex05` | Proving firmware ↔ Twin |
| [M05](../../m05-telemetry-cloud/l02-lab/README.md) | Telemetry · MQTT · `ex08`/`ex09` | The pipe out to a dashboard / cloud |
| **[M06](../l02-lab/README.md)** | **The E2E mini-project** | Combining it + a test table + a README |

If any piece hasn't met its minimum bar yet, fix it before expanding features in the Capstone.

---

## 2. End-to-End Path on Twin

The minimum path that must have pass/fail evidence:

```text
[1 Stimulus]
  M03 event script / scene / switch / tilt
        │
        ▼
[2 Firmware]
  read → decide → act (LED / flag / publish)
        │
        ▼
[3 Twin / Studio visualization]
  telemetry panel · 3D · status
        │
        ├──► [4a Live Data dashboard]  e.g. web-app ex06
        │
        └──► [4b MQTT]  broker + pub and/or sub  e.g. ex09 / ex15
```

| Step | Acceptable evidence |
|---|---|
| 1 Stimulus | A script/time note + before–after screenshots |
| 2 Firmware | UART/a log, or behaviour observable on the host as coming from the logic |
| 3 Studio | A matching graph / status / 3D |
| 4a or 4b | An outer consumer on **at least one pipe** (Live Data and/or MQTT) |

Don't use the feeling of "seems to work" as your only criterion — use the table in [e2e-case-brief.md](resources/e2e-case-brief.md)

### 2.1 Minimum pass rubric

| Criterion | Required |
|---|---|
| A virtual device + an event script (or an equivalent timeline) | Yes |
| Firmware co-sim works (Simulator and/or Board) | Yes |
| Visualization in Studio shows a value/status | Yes |
| MQTT publish **or** subscribe on at least one path | Yes |
| A README on how to rerun it (bring-up → demo → teardown) | Yes |
| An E2E test table passing at least **3 cases** | Yes |
| No secrets (Wi‑Fi / broker password) embedded in submitted files | Yes |

Extension work (optional): both Live Data **and** MQTT on the same demo · a fault/reconnect case · a GLB from M03 · comparing Path A vs B

---

## 3. Log Analysis — Layer by Layer

When the demo breaks, ask in this order (expanded from M04/M05):

```text
1. Firmware still alive?           → heartbeat / UART / LED
2. Twin / Studio session up?     → Link · backend XOR
3. Stimulus actually applied?    → M03 script / scene
4. Value reached firmware?       → log read path
5. Firmware decided / wrote?     → log / LED / publish
6. Studio shows change?          → correct panel
7. Live Data consumer OK?        → ex06 / ex08 connected · not stale
8. Broker up + topic match?      → Start broker · ex09/ex15
9. Payload schema OK?            → fields / units (M05 drill)
```

| Symptom | Suspect first at layer |
|---|---|
| No stream at all | 2 — the host / Link |
| A stream exists, but it's silent after triggering | 3–4 — the script / config |
| The log is correct, the UI doesn't move | 6–7 — the panel / the consumer |
| Live Data is fine, MQTT is empty | 8 — a different pipe / the broker / the topic |
| MQTT has messages, but the values are off | 9 — the schema |

> **Key phrase**
> Fix one layer at a time — capture logs from both the firmware side and the host side in the same run.

Keep important lines in the case brief's "issues found and fixed" section.

---

## 4. Domain Stories — Same E2E Pipe, Different Worlds

The E2E structure in §2 is **the same across every domain** — what differs is *the story*, the imagined sensor names, the alert threshold, and what the audience understands as "why does this need a Twin?"

Pick one domain in the Capstone and map it onto the lab's tools (SHT40 / DPS368 / BMI270 / a switch / MQTT) — **no domain-specific hardware needed**.

> **Key phrase**
> The domain = *the user's language* · the Twin pipe = *the firmware engineer's language* — the Capstone must speak both.

### 4.0 How to pick a domain (quick)

| If the team is interested in… | Choose domain | The demo's highlight |
|---|---|---|
| General cloud-connected devices | §4.1 IoT | A fleet / gateway / dashboard |
| Everyday life at home | §4.2 Home | Comfort · home safety |
| A production line / machinery | §4.3 Industrial | A threshold · an operator command · downtime |
| Healthcare / wellness (simulated) | §4.4 Health | Orientation · simulated vital signs · privacy |

Then use §5 as the lab template (the Smart Environmental Monitor), or rename the project to match your chosen domain — **the pass criteria are still the same set**.

### 4.1 Internet of Things (general)

**What the audience sees:** an edge sensor node sending values to a gateway / Twin, then up to a simulated cloud dashboard — "the device can talk to the back-end system."

| E2E piece | Example in this domain | Mapped to the lab |
|---|---|---|
| Stimulus | The environment changes · or a test mode opened from a control centre | The Quiet → Active scene · an event script |
| Sense | Temperature · humidity · pressure · IMU | SHT40 / DPS368 / BMI270 |
| Decide | Over a threshold → an `alert` event · change `mode` | Firmware threshold + state |
| Act / publish | Periodic telemetry + occasional events | MQTT `…/telemetry` · `…/event/alert` |
| Observe | A multi-channel dashboard · a clear route/origin | Studio + **ex06** + **ex09/ex15** |

**Three demo scenes**

1. **Normal** — the node is online, sending telemetry steadily (`origin` matching the Simulator or Board)
2. **Stimulus** — a simulated temperature spike → a `threshold_exceeded` event reaches the subscriber
3. **Command / fault** — command `mode=maintenance` from MQTT, **or** briefly cut the broker then reconnect

**Example topics (adjustable)**

```text
device/<id>/iot/telemetry
device/<id>/iot/state
device/<id>/iot/event/alert
device/<id>/iot/cmd                 ← subscribe for a command back
```

### 4.2 Inside the home (smart home)

**What the audience sees:** sensors in a living room / bedroom helping with comfort and safety — not just a number graph, but "a home that responds."

| Home scenario | How the Twin simulates it | What's demonstrated on the host |
|---|---|---|
| The room is too hot | The script drives `temperatureC` high | LED/state = `cool_request` · an MQTT event |
| A window / door opens | A simulated switch or GPIO | State `window=open` · retain on the state topic |
| Someone walks around at night | An IMU / a motion scene | A brief `motion_detected` event |
| The owner commands from an app | An MQTT command | `mode=away` / `mode=home` |

**Three demo scenes**

1. **Normal** — temperature/humidity are steady and comfortable, on ex06
2. **Stimulus** — "bright sun in the room" (a Warm scene) → an alert + a mode change
3. **Command** — send `away` from the host → the device enters a saving/watch mode (shown on Studio)

**A good storytelling point:** use a room or device GLB from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) as a backdrop — remind the audience the 3D image **does not replace** the real sensor value.

```text
home/<roomId>/climate/telemetry
home/<roomId>/security/state
home/<roomId>/cmd
```

### 4.3 Industrial plant / factory floor

**What the audience sees:** a machine on the production line has a "digital twin" for rehearsing alerts and commands from the control room — reducing how many trials happen directly on the real machine.

| Factory scenario | How the Twin simulates it | What's demonstrated on the host |
|---|---|---|
| Bearing / control cabinet temperature is high | Temperature + a threshold | An `overtemp` event · stopping the simulated run mode |
| Abnormal vibration / tilt | BMI270 accel, or orientation (`ex05`) | A `vibration_high` event / a tilt alarm |
| Pressure in a pneumatic/hydraulic system | DPS368 as a proxy | A graph + MQTT telemetry |
| A technician commands from a simulated SCADA | An MQTT command | `run` / `stop` / `ack_alarm` |
| A signal gap on the line | Stopping publish / stopping the broker | Stale (ex08) · reconnect |

**Three demo scenes**

1. **Normal** — the line is "green," values are in range · the operator dashboard (ex06) updates
2. **Stimulus** — inject overtemp/vibration → an alarm state + an event topic
3. **Command / fault** — command `stop` from MQTT, **or** briefly lose the link then recover (important for a downtime narrative)

**A good storytelling point:** emphasise that the Twin is used to **rehearse the runbook** (who does what when the alarm fires) before touching the real machine.

```text
plant/<lineId>/machine/<id>/telemetry
plant/<lineId>/machine/<id>/alarm
plant/<lineId>/machine/<id>/cmd
```

### 4.4 Medical / health & wellness (lab simulation only)

**What the audience sees:** a simulated health-tracking device or a bedside module — practising the data pipe and link reliability, **not** a clinically certified medical device.

> **The lab's scope**
> Use only simulated values / development-board sensors on the DevKit · never claim it meets a medical standard · never use real patient data in the lab · emphasise privacy: don't put a name or a hospital number (HN) in a topic/payload that is passed on.

| Health scenario (simulated) | How the Twin simulates it | What's demonstrated on the host |
|---|---|---|
| Ambient temperature around the patient / room | SHT40 | Climate comfort on the dashboard |
| Posture / a fall (concept) | BMI270 orientation — [M04 ex05](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | The horizon tilts abnormally → an event |
| Activity / movement | The IMU's Motion scene | A higher telemetry rate |
| A nurse/app commands a monitoring mode | An MQTT command | `mode=active_monitor` |
| A signal gap = a risk | Stale / disconnect | ex08 + the reconnect drill (M05) |

**Three demo scenes**

1. **Normal** — the stream is steady · shows the link and schema are correct
2. **Stimulus** — a strong tilt/Motion → a `posture_alert` event (a simulated name) reaches the subscriber
3. **Fault** — briefly cut the stream → the UI shows stale/reconnect — explain why a health link needs a watchdog

**Example topics (avoid identifying information)**

```text
care/device/<id>/vitals_sim/telemetry    ← simulated values only
care/device/<id>/state
care/device/<id>/event/posture_alert
care/device/<id>/cmd
```

### 4.5 One mapping table (all domains → same lab kit)

| Domain | The "hero" of the story | Main sensor in the lab | Recommended consumer | Example event |
|---|---|---|---|---|
| General IoT | An edge node ↔ the cloud | SHT40 + state | ex06 + ex15 | `threshold_exceeded` |
| The home | A comfortable / safe room | SHT40 + a switch | ex06 + an MQTT cmd | `motion_detected` |
| A factory | A machine + an alarm | temp/pressure + BMI270 | ex06 + ex08 + ex15 | `overtemp` / `tilt` |
| Health (simulated) | A watch link | BMI270 + SHT40 | ex05 + ex08 + ex09 | `posture_alert` |

Write the domain you chose on the first page of [e2e-case-brief.md](resources/e2e-case-brief.md)

---

## 5. Case Study — Smart Environmental Monitor (Twin)

The course's suggested starting task (equivalent to the **IoT / environmental** domain) — simulate an environmental monitor on the Twin and prove it end to end.
If you chose a domain from §4.2–§4.4, use the same structure, just changing the scenario and event names per the table above.

### 5.1 Suggested story

| Piece | Example in the lab |
|---|---|
| Sensors | Temperature / humidity (SHT40) and/or pressure · a switch or mode |
| Behaviour | Over a threshold → a state / LED / event change |
| Twin | A virtual device + a script, Lab Quiet → Warm / Alert |
| Host view | Studio telemetry + optional 3D |
| Cloud sim | An MQTT telemetry topic + a command back for the mode (at least one direction) |
| External proof | **`ex06`** (multi-sensor Live Data) and/or **`ex15`** (WS vs MQTT) |

### 5.2 Architecture sketch for your README

```text
[Event script] ──stimulus──► [Virtual sensors]
                                  │
                                  ▼
                         [Firmware co-sim]
                          decide / act
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            [Bitstream Studio]          [MQTT broker]
                    │                           │
                    ▼                           ▼
              web-app ex06              ex09 / ex15 / gauges
```

### 5.3 Three demo scenarios (required)

| # | Name | What the audience must see |
|---|---|---|
| 1 | **Normal** | Environmental values update steadily on Studio + the consumer |
| 2 | **Stimulus / threshold** | A script or switch clearly changes the state/event |
| 3 | **Command or fault** | An MQTT command reaches the device/Twin, **or** the broker/stream is briefly cut, then recovered |

Detail to fill in [e2e-case-brief.md](resources/e2e-case-brief.md)

### 5.4 Host evidence — `ex06` and `ex15`

| Page | Pipe | Used as evidence |
|---|---|---|
| **`ex06_dashboard.html`** | Live Data | A multi-sensor card · the `route` · primary field values |
| **`ex15_ws_mqtt_dashboard.html`** | Switching between MQTT (`:8883`) / WebSocket (`:9998`) | Shows the cloud-sim pipe and the bus are different channels — pick the transport that matches your demo |

Short steps for evidence:

1. Serve the Hackathon `web-app/`
2. Open ex06 during Normal + Stimulus — take a screenshot alongside Studio
3. Start broker → open ex15 in MQTT mode (or ex09) during a publish — take a screenshot of the payload/graph
4. Attach the evidence files in your deliverables folder

> ex15 helps teach the audience that a **WS bus ≠ an MQTT broker** — don't switch transport mid-demo without saying so.

---

## 6. Deliverables and Documentation

### 6.1 What to submit

| Piece | Description |
|---|---|
| The project / a link | The firmware + twin assets used |
| **README** | Step-by-step how to rerun it (see §6.2) · state the domain you chose |
| [e2e-case-brief.md](resources/e2e-case-brief.md) | All 3 cases + the domain, filled in completely |
| Demo evidence | Screenshots/a clip of Studio + ex06 and/or ex15/ex09 |
| (If any) a script / a device model | A version-locked one from M03 |

The whole course's document map: [course-package.md](resources/course-package.md)

### 6.2 README outline (copy into your project)

```text
# <Project name> (Course 2 Capstone)
Domain: IoT | Home | Industrial | Health-sim | Other: …

## Hardware / path
Simulator | Board + HEX version | Studio version

## Bring-up
1. Open workspace …
2. Link backend (one only) …
3. Start broker (if MQTT) …
4. Serve web-app …

## Demo script
1. Normal — …
2. Stimulus — …
3. Command / fault — …

## Topics / payloads
(no passwords · no personal health identifiers)

## Known limits
…
```

### 6.3 Where to look when stuck

| Need | Go to |
|---|---|
| Firmware code examples / API | The [Developer Hub](https://dev.tesaiot.dev/) |
| Host / broker / twin UI | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| HEX / VSIX / web-app | [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |
| MQTT on a real board | [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) |
| A Capstone on the SDK side alone | [Course 1 M08](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) |

---

## 7. After Course 2

After finishing this module, you should have taken the project from "runs on the Twin" to a level with **a repeatable test suite**, and be able to explain which domain the same pipe can support.

Common next directions:

| Direction | What to do next |
|---|---|
| Confirm on full hardware | Go back to [Course 1](../../../firmware-sdk-edge-ai/README.md) — flashing · real Wi‑Fi · real MQTT/BLE |
| Expand visualization / 3D | [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) + the M03 Blender path |
| Expand to the cloud | The lab's broker → your organisation's cloud policy (don't commit secrets) |
| A specific domain (factory / health) | Study the organisation's real requirements — the course's Twin is a practice field, not a certification |

---

## Next Steps

1. Choose a domain from §4 and do the [Lab](../l02-lab/README.md) — the E2E Capstone
2. Fill in [e2e-case-brief.md](resources/e2e-case-brief.md)
3. Check the deliverables list with [course-package.md](resources/course-package.md)

---

## References and Further Reading

1. [M01](../../m01-twin-architecture/l01-twin-architecture/README.md)–[M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) · [Course 2 TOC](../../README.md)
2. [Course 1 M08 Capstone](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) · [Course 1 M06 MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `web-app/ex06` · `ex15`
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Capstone lab: an E2E mini-project on the Digital Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
