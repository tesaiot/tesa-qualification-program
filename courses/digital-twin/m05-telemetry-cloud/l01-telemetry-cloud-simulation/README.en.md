---
id: twin.m05.l01
lang: en
title:
  th: ท่อ telemetry, MQTT บน Twin และ fault injection
  en: Telemetry Pipelines, MQTT on the Twin and Fault Injection
summary:
  th: แยก Telemetry/State/Event แยกท่อ Live Data กับ MQTT ใช้ web-app ex08/ex09 ตรวจสตรีม และออกแบบการทดลองเครือข่ายเสีย
  en: Separate Telemetry, State and Event, tell the Live Data pipe from the MQTT pipe, check streams with web-app ex08/ex09 and design network-fault experiments.
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
- twin.m04.l02
objectives:
- th: จำแนกข้อมูลอุปกรณ์เป็น Telemetry, State และ Event และเลือก topic กับ retain ให้เหมาะแต่ละชนิด
  en: Classify device data as Telemetry, State or Event and choose a topic and retain setting for each.
- th: แยกท่อ Live Data กับ MQTT และใช้อาการที่เห็นระบุว่าท่อไหนมีปัญหา
  en: Tell the Live Data pipe from the MQTT pipe and use symptoms to say which one is failing.
- th: ออกแบบการทดลอง fault injection ที่เปลี่ยนตัวแปรครั้งละหนึ่งตัว และบันทึกผลทั้งสองฝั่ง
  en: Design a fault-injection experiment that changes one variable at a time and logs both sides.
develops:
- skill: proto.mqtt
  to: 2
- skill: iot.cloud-platform
  to: 2
- skill: test.sil-hil
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: b46a7aa7576571b1e274d11df08f72bc7035ef6e2666a28d3fcb0833f81ceda1
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Telemetry and Cloud Simulation

**Course 2 · Module 5**
**Suggested time:** about 4 hours (classifying data · a pipeline · an MQTT broker · a dashboard · fault injection)
**Format:** a hands-on lesson — shaping data from the Twin/firmware, then passing it on to a broker / dashboard under controlled conditions

[Lab](../l02-lab/README.md) · [Lab notes](resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the device data set: **Telemetry, State, Event**
2. Simulate a **Data Pipeline** to test data formatting
3. Send simulated data to a **Cloud / external system** and check it with a **Dashboard**
4. Set up an **MQTT Broker** in the Twin / Studio environment
5. **Publish / Subscribe** between the Twin (or the device) and cloud services
6. Simulate **Lossy Network / Error Injection** scenarios and test under controlled conditions

This module builds on [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md), where you already proved the firmware ↔ Twin has real I/O — now expand the layer of **"data going outside Studio"** (a Live Data consumer + MQTT), before integrating the system in [M06](../../m06-integration/l01-system-integration-testing/README.md).

> **Key phrase**
> The Twin is a practice field for the data pipe — practise topics, payloads, dashboards and reconnecting **before** spending a whole day on the real cloud.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M04 — Co-simulation](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | The already-proven I/O pipe · `ex05` as an outer consumer |
| [Course 1 M06 — MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | Broker / QoS / retain / the firmware's CM55→CM33 path |
| [Course 1 M05 — Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | What the values you'll put into telemetry mean |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Starting the broker · the telemetry route · the Twin's MQTT tools |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/` — **ex08** (route/stale) · **ex09–ex15** (MQTT) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Encode / publish examples on the firmware side |
| [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) | Further reading on topic / QoS concepts |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | 3D visualization alongside a dashboard (if used) |

---

## 1. Telemetry, State, and Event

Separating data types helps design the **topic**, **the send rate**, and **the dashboard** so a dense stream doesn't bury an important event.

| Type | Character | Example in a Twin lab |
|---|---|---|
| **Telemetry** | A continuous stream over time | Temperature every 1 s · a BMI270 sample · DevKit Twin channels |
| **State** | The system's current status | `mode=idle`, `led=on`, the Link `connected`, `route=uart\|sim` |
| **Event** | Occasional, when a condition becomes true | `threshold_exceeded`, `stale`, `reconnect`, `fault_injected` |

### 1.1 Design habits

| Habit | Reason |
|---|---|
| Telemetry uses a fixed topic/rate | A dashboard expects a rhythm |
| State is sent when it changes (or retains the latest) | Reduces spam · a new subscriber knows the status immediately |
| Events keep a timestamp + a short reason | Debugging / tracing back in the M06 E2E |
| Don't put everything into one undifferentiated topic | Testing and ACLs become hard |

An example topic structure in the lab (adjustable to your own kit):

```text
device/<deviceId>/devkit-twin/telemetry     ← telemetry stream
device/<deviceId>/state                      ← current mode / flags
device/<deviceId>/event/<name>               ← sparse events
lab/qos-demo                                 ← a QoS/retain test field (ex14)
```

A default the Hackathon `web-app` often uses:
`device/devkit-twin-01/devkit-twin/telemetry` (see §5)

> **Key phrase**
> Telemetry = *breathing* · State = *the current posture* · Event = *an occurrence worth recording*

---

## 2. Data Pipeline (Twin Lab View)

The general sequence:

```text
[Source]
  Firmware / Simulator / Twin virtual device
        │
        ▼
[Shape]
  JSON fields · units · mask · channels
        │
        ▼
[Transport]
  A) Live Data provider (WS) → Studio panels / web-app ex05–ex08
  B) MQTT broker             → web-app ex09–ex15 / cloud / external tools
        │
        ▼
[Observe]
  Dashboard · subscriber log · gauges
```

### 2.1 Two pipes you must not confuse

| Pipe | Use when | Example consumer |
|---|---|---|
| **Live Data** (the telemetry provider) | Watching a sample already decoded from the bridge · `route` / `origin` / `stale` | `ex05`, `ex06`, **`ex08`** |
| **MQTT** (broker pub/sub) | Simulating the cloud layer / an external system | **`ex09`**, `ex12`, `ex15` |

Both pipes may show "the same block of temperature," but **the protocol and the failure point differ**.

| Symptom | Suspected pipe |
|---|---|
| `TelemetryClient` disconnected | Live Data / the bridge / serving the web-app |
| MQTT `disconnected` at `ws://127.0.0.1:8883/mqtt` | **Start broker** hasn't been done in Studio yet |
| Live Data is fine, but MQTT is empty | No publisher exists yet on that topic |
| MQTT has messages, but Live Data is silent | Different pipes — it doesn't mean "the sensor is dead" |

### 2.2 Schema / format drills (pipeline test)

Useful ways to test the pipe before going to the cloud:

1. Send a payload with all fields → the dashboard goes green
2. **Remove a field**, or rename a key → see where the UI breaks
3. Send the wrong unit (such as °C entered as milli) → the number is off but still parses
4. Send broken JSON → does the subscriber show a clear error, or stay silent?

Record the results in [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)

---

## 3. Walkthrough — `ex08` Stale, Route, and Origin

Before opening a broker, get familiar with **the quality of the Live Data stream** — continuing from M04, which used `ex05` as an orientation consumer.

File: [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) → `web-app/ex08_stale_and_route.html`

### 3.1 What the page proves

| UI | Meaning |
|---|---|
| The connection **route** | The backend the provider uses (relates to Simulator vs Bitstream) |
| **COM open** | Whether a serial port is open |
| The last sample's **origin** | `uart` or `sim` — must match the mode chosen in Studio |
| Sensor **pills** + stale | Whether each sensor is quiet past `staleAfterMs`, or still fresh |
| The event **log** | Connection / sample / stale as traceable events over time |

### 3.2 Lab steps

1. Link Studio (Simulator *or* Bitstream — never mixed)
2. Serve the `web-app/` folder and open **ex08**
3. Confirm `connected` · note the `route` and the `origin` of the latest sample
4. Briefly stop the stream (stop the Simulator / briefly unplug the COM, as your round allows) → the pill should go **stale**, with an event in the log
5. Resume streaming → the pill goes **fresh** again

**Passes when:** you can explain that `stale` is a host-side **Event** when telemetry has a gap — not a sensor value

> Use ex08 as evidence of **lossy / disconnect at the Live Data layer**, before moving to the MQTT layer (§6)

---

## 4. MQTT Broker in the Twin Host

In Course 2, the main host is Bitstream Studio — it usually has a command roughly like:

**Toolbar / Server → Start broker**

Then the MQTT web page in Hackathon connects to this default:

```text
ws://127.0.0.1:8883/mqtt
```

(see `DEFAULT_MQTT_WS_PATH` in `web-app/shared/ex-mqtt.js`)

| Check | Expect |
|---|---|
| Start broker, then open the web page | The broker is ready to accept a client |
| Open `ex09` without starting the broker first | It stays connecting / errors |
| An overridden URL | `?mqtt=ws://…` if the port changed |

### 4.1 Twin / cloud roles (honest mapping)

| Role in the course documentation | What you actually do in the lab |
|---|---|
| MQTT in the Twin | Studio's **Start broker** + publish from the Twin / Sensor Studio / a host tool |
| Cloud / an external system | The `web-app` subscriber · or a public/LAN broker (review [C1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)) |
| A real device publishing | Firmware on a board, behind Wi‑Fi (C1) — in M05, focus on the host pipe first if time is short |

Don't assume "Start broker" = telemetry automatically exists — there still needs to be a **publisher** on the topic being subscribed to.

---

## 5. Walkthrough — `ex09` MQTT Subscriber (main cloud-sim example)

M05's main example for the MQTT layer: **`ex09_mqtt_subscriber.html`**

### 5.1 What it does

1. Loads mqtt.js through Serve Web App (`/@bitstream/mqtt-live-data.js`)
2. Connects to `ws://127.0.0.1:8883/mqtt` (or `?mqtt=`)
3. Subscribes to the default topic:

```text
device/devkit-twin-01/devkit-twin/telemetry
```

Built from `devkitTwinTopic(deviceId)` — change it with `?device=` or `?topic=`

4. Shows the **last payload** (JSON) · counts messages · counts `channels` if present

### 5.2 How to run (evidence path)

```text
[Bitstream Studio] Start broker
        │
        ▼
[Publisher]
  DevKit Twin MQTT tab
  or Sensor Studio connectivity nodes
  or another publish tool
        │  topic: device/<id>/devkit-twin/telemetry
        ▼
[Broker ws://127.0.0.1:8883/mqtt]
        │
        ▼
[ex09 browser page]  →  Last payload + message count
```

Short steps:

1. **Start broker** in Studio
2. Serve `web-app/` → open **ex09**
3. Wait for the badge `connected`
4. Publish from the Twin / a host to the topic the web page subscribes to
5. Take a screenshot of `Last payload`, alongside the publish source

**Passes when:** there is at least one JSON message whose fields match what you intended to send (the units and key names)

### 5.3 Teaching view of the page code

The main concept (see the real file in Hackathon):

```text
connectMqtt(mqtt, MQTT_URL)
  → onConnect → client.subscribe(TOPIC)
  → on("message") → JSON.parse → update payload + chips
```

`wireMqttState` manages `connected` / `reconnecting` / `error` / `disconnected` — use it as evidence of **reconnecting** in the lossy lab (§6)

### 5.4 Nearby examples (ladder)

| File | Use when |
|---|---|
| **ex09** | Subscribing to one topic — **the main example in §5** |
| ex10 | Publishing from the browser |
| ex11 | Wildcards (`+` / `#`) |
| ex12 | DevKit gauges |
| ex13 | A Live data client mixed with an MQTT approach |
| **ex14** | Manually experimenting with QoS + retain |
| ex15 | A combined WS + MQTT dashboard |

For M05, make sure of **ex08 + ex09**, then choose at least one from ex10–ex15, depending on time.

---

## 6. Publish / Subscribe Patterns

A short review from [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md), then apply it in the Twin:

| Pattern | Who publishes | Who subscribes | Used in the lab |
|---|---|---|---|
| Device → Cloud | The Twin / the firmware | ex09 / a dashboard | telemetry |
| Cloud → Device | A host tool / ex10 | The Twin, or the firmware | a command / setting state |
| A lab mirror | ex14 | ex11, on the same topic | QoS / retain |

### 6.1 QoS and retain (a quick lab with ex14)

| Concept | What to try |
|---|---|
| QoS 0 | Send and move on — suited to a dense telemetry stream |
| QoS 1 / 2 | More guaranteed — watch the behaviour on a lab topic |
| **Retain** | Publish with retain on → open a new subscriber (such as ex11); it should get the latest message immediately |

Don't turn on retain on a high-frequency telemetry topic without thinking — the broker will keep "the latest value," which could mislead a newcomer into thinking it's a live stream.

### 6.2 Mapping Telemetry / State / Event onto MQTT

| Type | Topic approach | Retain? |
|---|---|---|
| Telemetry | `…/telemetry` or `…/sensors/<name>` | Usually **not** |
| State | `…/state` | Usually **yes** (the latest value) |
| Event | `…/event/<name>` | Usually **not** (kept in a log/DB instead) |

---

## 7. Lossy Network and Error Injection

The goal is not to be the best at breaking a network, but to **control one variable** and record how the queue / UI / client handles it.

### 7.1 Experiments you can run in the lab

| Experiment | How, in the Twin lab | What to watch |
|---|---|---|
| A gap in messages | Briefly stop the publisher · or stop the Simulator | ex08's stale · a gap on the graph |
| A brief disconnect | Stop the broker and Start it again · or close the tab and reopen it | ex09's `reconnecting` → `connected` |
| High latency | Reduce the publish rate / the Quiet scene | The time between message counts |
| A malformed payload | Send JSON with a missing field | A dashboard error vs silence |
| Switching backends at the wrong moment | (Don't do this while capturing evidence) mixing sim+uart | Origin confusion — used to teach that it must be XOR |

### 7.2 What to write down

For each case:

1. What was injected / cut
2. What was seen on the subscriber / Studio (with a timestamp)
3. The behaviour: **drop** · **retry** · **reconnect** · **stale UI** · **backoff**
4. Acceptable for the project, or must be fixed before M06

A form: [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)

> **Key phrase**
> Good fault injection = *change only one thing per round*, and keep a log on both sides.

---

## 8. How M05 Feeds M06

| After M05, you have | Used next in M06 |
|---|---|
| Topics + example payloads | The E2E Smart Environmental Monitor |
| A reusable dashboard / ex09–ex15 | Evidence-based acceptance criteria |
| Notes on lossy / stale / reconnect | The risk-analysis section of the report |
| The ability to tell Live Data from MQTT | Not mixing up evidence from the wrong pipe during a demo |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Fill in [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)
3. When ready, continue to [M06 — System Integration and Testing](../../m06-integration/l01-system-integration-testing/README.md)

---

## References and Further Reading

1. [M04 Co-simulation](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 1 M06 MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** — Start broker / Twin MQTT
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `web-app/ex08` … `ex15`
4. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
5. [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) · [mqtt.org](https://mqtt.org/)
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**
7. [Course 2 TOC](../../README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: the telemetry pipe and MQTT on the Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Lab notes](resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)
