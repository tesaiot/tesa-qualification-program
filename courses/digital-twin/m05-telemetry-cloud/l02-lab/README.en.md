---
id: twin.m05.l02
lang: en
title:
  th: 'แล็บ: ท่อ telemetry และ MQTT บน Twin'
  en: 'Lab: Telemetry Pipeline and MQTT on Twin'
summary:
  th: ออกแบบ topic ตรวจคุณภาพ Live Data ด้วย ex08 ตั้ง broker แล้ว subscribe ด้วย ex09 และทดลอง lossy/reconnect
  en: Design topics, check Live Data quality with ex08, start a broker and subscribe with ex09, then try lossy/reconnect cases.
level: L3
time_min:
  lab: 240
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m05.l01
objectives:
- th: ออกแบบ topic สำหรับ Telemetry/State/Event และตรวจฟิลด์กับหน่วยบน dashboard
  en: Design topics for Telemetry/State/Event and check fields and units on a dashboard.
- th: ตั้ง broker ใน Studio แล้วทำ pub/sub ได้อย่างน้อยหนึ่งคู่
  en: Start the broker in Studio and complete at least one pub/sub pair.
- th: ทดลอง lossy / disconnect / schema break อย่างน้อยหนึ่งเคสและบันทึกผล
  en: Run at least one lossy, disconnect or schema-break case and record the result.
develops:
- skill: proto.mqtt
  to: 2
- skill: iot.cloud-platform
  to: 2
assesses:
- skill: proto.mqtt
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
slides: slides.md
source_sha256: 57ddafc8b0f94fb39eed27d86d332c72fb86fd8ba6de717a43b81bb6eded91d6
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M05/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M05 — Telemetry Pipeline and MQTT on Twin

**Course 2 · Module 5**
**Type:** Hands-on (classify · Live Data quality · MQTT pub/sub · fault injection)
**Suggested time:** ~3.5–4 hours

Read first: [Lesson](../l01-telemetry-cloud-simulation/README.md) · [Lab notes](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [M04 lab](../../m04-cosimulation/l02-lab/README.md) · [the ex05 walkthrough](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | The basic Live Data consumer |
| [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | MQTT on the firmware / QoS |
| [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) | **ex08**, **ex09**–ex15 |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Start broker · Twin publish |

---

## Lab Goals

- Separate and send at least one instance each of the **Telemetry / State / Event** concepts
- Check on a dashboard or a subscriber that the fields/units are correct
- Start an **MQTT broker** in Studio and complete at least one pub/sub pair
- Try at least one **lossy / disconnect / schema-break** case
- Fill in [telemetry-mqtt-lab-notes.md](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md)

---

## Prerequisites

- [ ] M04's bring-up passed (a stable Link · know Simulator XOR Bitstream)
- [ ] The Hackathon folder has `web-app/`
- [ ] Know how to **Serve Web App Folder over HTTP** (M04)
- [ ] A `lab-notes/` folder for evidence

---

## Lab A — Classify & design topics (required)

Design (on paper, or in the lab notes):

1. **Telemetry** — a topic + one example JSON block + an approximate rate
2. **State** — a topic + when it will be sent (a mode change / LED / Link)
3. **Event** — a topic or event name + a short condition

You may use the example structure from the lesson, such as:

```text
device/<id>/devkit-twin/telemetry
device/<id>/state
device/<id>/event/<name>
```

**Pass when:** a teammate reads the topic and correctly guesses the data type, without having to guess from the payload alone

---

## Lab B — Live Data quality with `ex08` (required)

1. Link Studio (a single mode)
2. Serve `web-app/` → open **`ex08_stale_and_route.html`**
3. Note the `route`, `COM open`, `last origin`
4. Make at least one sensor go **stale**, then return to **fresh**
5. Take a screenshot of the event log + pills

**Pass when:** you can explain that stale is a host-side **Event** when telemetry has a gap — and the `origin` matches Studio's mode

---

## Lab C — MQTT broker + `ex09` subscriber (required)

1. In Bitstream Studio: **Start broker**
2. Open **`ex09_mqtt_subscriber.html`** — wait for `connected`
3. Publish to the topic the web page subscribes to (default `device/devkit-twin-01/devkit-twin/telemetry`, or per `?device=` / `?topic=`)
   - Publish source: the DevKit Twin MQTT tab / Sensor Studio connectivity / another tool you have
4. Confirm **Last payload**'s fields and units match
5. Take a paired screenshot: the publish source + the ex09 page

**Pass when:** the message count is ≥ 1, and the JSON can be explained as Telemetry (or the intended type)

---

## Lab D — Pipeline / schema drill (recommended)

Choose at least one:

- Remove a field from the payload and see exactly where the subscriber/dashboard breaks
- Deliberately send the wrong unit, and note that the UI "still looks fine but means the wrong thing"
- Open **ex14** and try QoS + retain on `lab/qos-demo`, then have a friend open a subscriber (such as ex11) after you've retained a message

**Pass when:** there is at least one line of "what broke / what didn't" in the lab notes

---

## Lab E — Lossy / reconnect (recommended — part of the complete deliverable)

Choose at least one case, and fill in the table in the lab notes:

| Case | Example way to do it |
|---|---|
| Stop / Start the broker briefly | Watch ex09 go `reconnecting` → `connected` |
| Briefly stop the publisher | Watch for a gap · or ex08's stale |
| Close the ex09 tab and reopen it | If a state topic has retain — do you get the latest value or not? |

**Pass when:** you can name the behaviour seen (drop / retry / reconnect / stale) without guessing

---

## Lab F — Optional ladder

If time remains, choose more:

- **ex10** publishing from the browser
- **ex12** gauges
- **ex15** a combined dashboard
- Publishing from real firmware after Wi‑Fi ([C1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)) into the lab's broker

---

## Deliverables checklist

- [ ] Labs A–C passed
- [ ] Lab E (or at least Lab D, if time is short)
- [ ] [telemetry-mqtt-lab-notes.md](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) filled in completely
- [ ] Screenshot evidence: ex08 + ex09 (+ schema/lossy, per what you did)

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| ex08 is disconnected | Studio/the bridge · serve the correct `web-app/` folder |
| ex09 is stuck connecting | **Start broker** · check `ws://127.0.0.1:8883/mqtt` |
| connected, but Waiting for messages | No publisher exists yet · the topic doesn't match · check `?device=` / `?topic=` |
| Live Data is fine, MQTT is empty | Different pipes — don't fix the firmware before checking the broker/topic |
| The origin is confusing | Don't mix Simulator + Bitstream · clear it and Link fresh |
| Retain makes a value "stuck" | Check you're experimenting on the lab topic, not a dense telemetry one |

[Lesson](../l01-telemetry-cloud-simulation/README.md) · [Lab notes](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) · [Table of Contents](../../README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)
