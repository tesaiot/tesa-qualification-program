---
id: fw-sdk.m06.l02
lang: en
title:
  th: 'แล็บ: Wi-Fi, MQTT connect, publish และ subscribe'
  en: 'Lab: Wi-Fi, MQTT Connect, Publish, and Subscribe'
summary:
  th: join Wi-Fi เชื่อม MQTT publish ข้อความหรือ telemetry แล้ว subscribe รับคำสั่งกลับ พร้อมบันทึกคอนฟิกโดยไม่เปิดเผยความลับ
  en: Join Wi-Fi, connect MQTT, publish a message or telemetry, subscribe to commands and record the configuration without exposing secrets.
level: L3
time_min:
  lab: 210
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m06.l01
objectives:
- th: เชื่อม Wi-Fi จนสถานะ CONNECTED แล้วเชื่อม MQTT กับ broker ที่เลือก
  en: Join Wi-Fi until CONNECTED, then connect MQTT to the chosen broker.
- th: publish ข้อความหรือ telemetry แล้วเห็นบน subscriber ของโฮสต์
  en: Publish a message or telemetry and see it on a host subscriber.
- th: รับคำสั่งกลับที่อุปกรณ์ผ่าน subscribe และบันทึกคอนฟิกที่ใช้โดยไม่มีความลับในรายงาน
  en: Receive a command on the device via subscribe and record the configuration with no secrets in the report.
develops:
- skill: proto.mqtt
  to: 2
- skill: proto.wifi
  to: 2
- skill: sec.tls
  to: 1
assesses:
- skill: proto.mqtt
  level: 2
  evidence: README.md#submit-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: a551df47f0c589ac436d0223a2272b2cbfc9a966641611c007ac85ab7d4beb32
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — Wi‑Fi, MQTT Connect, Publish, and Subscribe

**Course 1 · Module 6**
**Type:** Hands-on lab (network + broker + device)
**Suggested time:** 2.5–3.5 hours

Read first: [Lesson](../l01-mqtt-and-mqtts/README.md) · [Cheatsheet](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [MQTT and MQTTs on an Edge Device](../l01-mqtt-and-mqtts/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [Lesson](../l01-mqtt-and-mqtts/README.md) | `cm55_trigger_mqtt_*`, CONFIG, topics |
| [Hackathon MQTT pages](https://github.com/drsanti/TESAIoT_Hackathon) | `web-app/ex09`–`ex15` |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Starting the broker / MQTT tools |
| [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) | Reviewing QoS / retain |

---

## Lab Goals

- Join Wi‑Fi until the status is **CONNECTED**
- **Connect MQTT** to the broker you choose
- **Publish** a message or telemetry at least once
- **Subscribe** (from the host or the device) and see the message
- Explain the difference between MQTT vs MQTTs, and record the config values used
- (Recommended) watch JSON telemetry from a sensor (continuing from M05)

---

## Prerequisites

- [ ] Have passed M05, at least able to read a sensor (for telemetry)
- [ ] The room's Wi‑Fi SSID / password (do not record it in Git)
- [ ] The broker host/port you will use
- [ ] A subscribe tool on the PC (MQTTX, mosquitto_sub, or the Hackathon web-app)

> **Do not** publish a real password or certificate into a public report

---

## Lab A — Wi‑Fi link (required)

1. Call `cm55_trigger_connect` or `example_wifi_ui_connect`, per the project
2. Read `cm55_get_wifi_status` until `IPC_WIFI_LINK_CONNECTED`
3. Record the SSID (no need to record the password)

**Pass when:** the Wi‑Fi link is ready before touching MQTT

---

## Lab B — MQTT connect + status (required)

1. Set the policy so MQTT can be used (such as the factory default)
2. `cm55_trigger_mqtt_connect`
3. Read `cm55_get_mqtt_status` until `state == CONNECTED (2)`
4. Note the `broker_host`, `port`, `tls`, and `effective_client_id`

```c
(void)cm55_trigger_mqtt_connect();
/* poll cm55_get_mqtt_status until connected or timeout */
```

**Pass when:** the status is CONNECTED and you have a client id to note

---

## Lab C — Publish and observe (required)

Choose at least one path:

### C1 Telemetry path

- Turn on the sensor + the `TELEMETRY_PUBLISH` policy
- Subscribe on the host to the topic `bitstream/<MAC12>/sensors` (or whatever topic you set)
- Confirm JSON is coming in

### C2 Explicit publish

- Use either path (`cm33_mqtt_stack_publish`, or the Studio panel) to send `{"hello":1}`
- See the message on a subscriber

**Pass when:** you see a payload on a host tool at least once

---

## Lab D — Subscribe / command path (required)

1. Subscribe on the device side to the actuators topic (or use the existing topic-table config)
2. From the host, publish a test command to that topic
3. Record how the device received it (a log / an LED / an event, per what the firmware supports)

**Pass when:** there is evidence a message from the cloud/host reached the device (or reached the stack's log)

---

## Lab E — Choose one (recommended)

### E1 MQTT vs MQTTs table

Fill in a comparison table from your experiment, or from the documentation of the kit used: port, `tls`, CA

### E2 Hackathon web MQTT

Run `ex09`–`ex14` per the [Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) (a broker in the Studio if needed)

### E3 Payload design

Design a JSON for an event from M05 (a temperature threshold/feature), then try publishing it once

**Pass when:** you submit a table/screenshot/short design file

---

## Short report (10–15 lines)

1. The Wi‑Fi SSID (no password)
2. The broker host:port and tls 0/1
3. The client id / MAC topic used
4. Evidence of publish + subscribe
5. Limitations you observed (such as telemetry's QoS, needing Wi‑Fi first)

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| An MQTT error / it won't connect | Wi‑Fi isn't up yet · `MQTT_ENABLED` is off · the wrong host/port |
| Connects but no telemetry | The sensor isn't publishing · `TELEMETRY_PUBLISH` is off · the wrong topic |
| TLS fails | The port isn't 8883 · the CA doesn't match the broker · the device's clock is wrong (if certificate checking depends on it) |
| Subscribe sees nothing | A different MAC / a different topic prefix · a different broker |
| Auth fails | The username/password is empty or wrong |

---

## Submit checklist

- [ ] Labs A–D passed
- [ ] At least 1 item from Lab E
- [ ] [mqtt-cloud.md](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md) filled in
- [ ] The short report has no secrets

[Lesson](../l01-mqtt-and-mqtts/README.md) · [Cheatsheet](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md) · [Table of Contents](../../README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)
