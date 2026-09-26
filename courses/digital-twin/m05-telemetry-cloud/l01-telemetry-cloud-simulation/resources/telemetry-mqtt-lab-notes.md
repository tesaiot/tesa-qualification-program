# Telemetry / MQTT lab notes — Course 2 M05

**Course 2 · Module 5**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

---

## Setup

| Item | Your value |
|---|---|
| Path (Simulator / Board / Both) | |
| Bitstream Studio version | |
| Broker (Studio local / LAN / other) | |
| Device id / default topic | |
| Dashboard / subscriber used | ex08 · ex09 · other: |

---

## A — Classify (topics + samples)

| Kind | Topic | Sample payload (short) | Rate / when |
|---|---|---|---|
| Telemetry | | | |
| State | | | |
| Event | | | |

---

## B — Live Data (`ex08`)

| Check | OK? | Notes / evidence |
|---|---|---|
| `connected` | | |
| Connection route | | |
| COM open | | |
| Last sample origin (`uart` / `sim`) | | |
| Forced stale → fresh | | |

---

## C — MQTT (`ex09`)

| Check | OK? | Notes / evidence |
|---|---|---|
| Start broker | | |
| Subscriber `connected` | | |
| Topic subscribed | | |
| Message count ≥ 1 | | |
| Payload fields / units match | | |
| Publisher tool used | | |

---

## D — Schema / QoS drill (optional)

| What you changed | What broke | What still worked |
|---|---|---|
| | | |

QoS / retain notes (ex14):  

---

## E — Lossy / error injection

| Trial | What you injected | What you observed | Drop / retry / reconnect / stale? |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Suspected weak point before M06:  

---

## Quick recall

```text
Classify → prove Live Data (ex08) → Start broker → prove MQTT (ex09)
         → break one thing (schema or link) → write what recovered
```

| Pipe | Default check |
|---|---|
| Live Data | `TelemetryClient` + route / origin / stale |
| MQTT | `ws://127.0.0.1:8883/mqtt` after **Start broker** |

| Backend | Use alone |
|---|---|
| Simulator | COM closed · expect `origin: sim` |
| Bitstream | COM open · expect `origin: uart` |

---

## Portals

- [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
- [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) — `web-app/ex08` … `ex15`  
- [Developer Hub](https://dev.tesaiot.dev/)  
- [Course 1 M06 MQTT](../../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M06](../../../m06-integration/l01-system-integration-testing/README.md)
