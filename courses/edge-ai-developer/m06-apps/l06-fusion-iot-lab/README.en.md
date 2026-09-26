---
id: edgeai-dev.m06.l06
lang: en
title: {th: 'ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT', en: 'Hands-on: send the fused event over MQTT'}
summary: {th: 'เติมห้าจุดใน s17_fusion_iot.py ให้เลือกโมเดล อ่าน verdict อ่าน gyro ดิบ รวมสองสัญญาณด้วย AND แล้ว publish เหตุการณ์ที่ผ่านการยืนยันเป็น JSON ขึ้น MQTT broker ผ่าน WiFi ครั้งเดียวต่อเหตุการณ์ พร้อมเขียนโค้ดชุดเดียวที่ถอยเป็นโหมด [SIM] เองเมื่อไม่มีเน็ต', en: 'Fill five points in s17_fusion_iot.py to select the model, read the verdict, read the raw gyro, AND the two signals and publish each confirmed event once as JSON to an MQTT broker over WiFi, with one codebase that falls back to a [SIM] mode by itself when there is no network.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l05]
objectives:
  - {th: เติมห้าจุดใน practice/s17_fusion_iot.py จนเหตุการณ์ fused ถูก publish ขึ้น topic ครั้งเดียวต่อการเขย่าหนึ่งครั้ง และตรวจเห็นข้อความได้จากฝั่งผู้รับ (เช่น mosquitto_sub หรือเว็บ MQTT client), en: 'Fill the five points in practice/s17_fusion_iot.py until each shake publishes one fused event to the topic, and confirm the message on the receiving side (for example mosquitto_sub or a web MQTT client).'}
  - {th: หาท่าที่โมเดลตอบคลาสเป้าหมายแต่ประตูดิบไม่ผ่าน (หรือกลับกัน) แล้วยืนยันว่าไม่มีเหตุการณ์ถูกส่ง, en: Find a motion where the model reports the target class but the raw gate fails (or the reverse) and confirm no event is sent.}
  - {th: อธิบายการ degrade อย่างสง่างามด้วย try/except ImportError และ is_connected() และบอกได้ว่าทำไมควรส่งเฉพาะเหตุการณ์ที่สรุปแล้วพร้อมหลักฐานดิบใน payload, en: 'Explain graceful degradation with try/except ImportError and is_connected(), and why only the summarised event with its raw evidence should go in the payload.'}
develops: [{skill: proto.mqtt, to: 2}, {skill: proto.wifi, to: 2}, {skill: ai.edge, to: 3}]
assesses: [{skill: proto.mqtt, level: 2, evidence: practice/s17_fusion_iot.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: cf265d24dda833184b0ec1a3f3679172572aa7155afcaec7f72fb5c8a776310d
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.6 — Hands-on: send the fused event over MQTT

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s17_fusion_iot.py to select the model, read the verdict, read the raw gyro, AND the two signals together, and publish each confirmed event as JSON to an MQTT broker over WiFi, once per event, with one codebase that falls back to a [SIM] mode by itself when there's no network.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s17_fusion_iot.py until each fused event is published to the topic once per shake, and confirm the message on the receiving side (for example mosquitto_sub or a web MQTT client).
2. Find a motion where the model reports the target class but the raw gate fails (or the reverse), and confirm no event is sent.
3. Explain graceful degradation with try/except ImportError and is_connected(), and why only the summarised event with its raw evidence should go in the payload.

## Before you start

You've been through lesson 6.5, and understand the fused condition and the edge trigger. Prepare an MQTT-receiving program, such as `mosquitto_sub -h test.mosquitto.org -t "tesaiot/edge-ai/s17/#" -v`, or a web MQTT client that can connect to the same broker.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the emulator simulates WiFi connecting successfully, and sends MQTT to a real public broker over WebSocket (falling back to a simulated broker if it can't connect), but the gyro on the emulator stays near zero, so practising on the emulator needs the gate temporarily switched to the accelerometer. On the board, you need to enter your own WiFi name and password.
- **Prior lesson:** [lesson 6.5 — Sensor fusion: a model's verdict with a raw sensor](../l05-sensor-fusion/README.md)

## Concepts

The whole file reads as one sentence: connect to the network → find a model and start it running → loop reading the verdict and the raw gyro → once the two signals agree, publish → stop on exit. The networking part is already provided: `import wifi, mqtt` sits inside `try/except ImportError` (set `HAVE_NET = False` if the modules are missing); `wifi.connect(WIFI_SSID, WIFI_PASS)` returns True/False and blocks until connected or timed out; `wifi.ip()` reports the IP; `mqtt.connect(BROKER, PORT, client_id=CLIENT_ID)`, then check `mqtt.is_connected()` — failing to connect enters `[SIM]` mode, which prints the payload to the console instead. The five points to fill in are: (1) `edge_ai.select(model['index'])` (2) `r = edge_ai.result()` (3) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (4) `fused = model_hit and raw_ok`, and (5) `mqtt.publish(TOPIC, payload)` inside `publish_event()`, which wraps `try/except OSError`, since publish throws `OSError` when the connection drops.

MQTT is publish/subscribe through a broker — the sender doesn't need to know who's listening. Our payload is a short piece of JSON, `{"event": ..., "conf": ..., "gyro": ..., "ts": ...}`, carrying both the verdict and the raw evidence, so the receiving end can audit the decision afterward. It sends only the summarised event, not a raw stream, saving bandwidth and protecting privacy. The `fired` flag makes one event equal one message, so it doesn't spam the public broker. Public brokers are heavily shared, so change `CLIENT_ID` and `TOPIC` to have your own name appended — if a client_id collides with someone else's, the broker will kick the old connection out — and never send private data to a public broker. On the emulator, temporarily switch the gate to `gmag = abs(ax) + abs(ay) + abs(az - 9.81)` with `MOTION_FLOOR = 5.0`, since the HW panel only moves the accelerometer; pressing Shake on a real board still uses the gyro gate as before.

## Worked example

`s17_fusion_iot_full.py` lets you pick between two gates with `GATE_MODE`: `"imu"` (the raw gyro, corroboration-style) or `"radar"` (is someone present — multi-modal, a different sensor from the model; on the emulator, the Shake button makes presence true). It counts events, automatically reconnects to the broker when it drops, and shows RSSI from `wifi.status()["rssi"]`.

| File | What this file teaches |
|---|---|
| [examples/s17_fusion_iot_full.py](examples/s17_fusion_iot_full.py) | Fusion + IoT, polished version |

## Practice

The `# TODO:` comments are at lines 127 (`select`), 142 (`result`), 151 (reading `motion()`), 162 (`fused`), and 115 (`mqtt.publish` inside `publish_event`). If the gyro stays stuck at 0 on the board, point 151 is still empty. If you see a `MQTT TX` line but the receiving side sees nothing, check point 115 and the topic name on both sides.

| Practice file | Topic |
|---|---|
| [practice/s17_fusion_iot.py](practice/s17_fusion_iot.py) | Combining a model's verdict with a raw sensor, then streaming it to the cloud (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s17_fusion_iot.py](solution/s17_fusion_iot.py) | [practice/s17_fusion_iot.py](practice/s17_fusion_iot.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. One hard shake, but the receiving side sees more than ten messages. Which part of the code is missing? *(single choice · objective 1)*
   - a) try/except OSError
   - b) The fired flag that fires only on the rising edge of fused
   - c) wifi.ip()
   - d) The gyro gate

   <details><summary>Solution</summary>

   **b** — fused stays true across several consecutive frames during a shake. Without fired, every frame gets published.

   </details>

2. On the board, the on-screen gyro stays stuck at 0 the whole time, and no event is ever sent. Which point is still empty? *(single choice · objective 1)*
   - a) Point 3, reading sensors.bmi270.motion()
   - b) Point 5, mqtt.publish
   - c) Point 1, select
   - d) Nothing is wrong

   <details><summary>Solution</summary>

   **a** — the default values gx = gy = gz = 0.0 make gmag equal 0, so the raw gate never opens, and fused is never true.

   </details>

3. You pick the board up quickly. The model answers shaking at 0.7, but gmag = 25 with MOTION_FLOOR = 40. What happens? *(single choice · objective 2)*
   - a) The event is sent, because the model is confident
   - b) Nothing is sent, because the raw gate fails — fusion filters this false positive out
   - c) The app crashes
   - d) It sends in [SIM] mode

   <details><summary>Solution</summary>

   **b** — AND requires both stages to pass. This is exactly the kind of false positive fusion exists to filter out.

   </details>

4. Why is import wifi, mqtt wrapped in try/except ImportError? *(single choice · objective 3)*
   - a) To make the import faster
   - b) So one codebase still runs even when the firmware has no networking module, falling back to offline mode instead of crashing right at the import line
   - c) To hide the WiFi password
   - d) It isn't necessary

   <details><summary>Solution</summary>

   **b** — graceful degradation means checking before using a part that requires the network. The rest of the app still works and still demonstrates the fusion mechanism.

   </details>

5. Which payload best fits this lesson's edge-to-cloud principle? *(single choice · objective 3)*
   - a) Streaming raw IMU data 50 times a second
   - b) {"event":"shaking","conf":0.92,"gyro":180,"ts":123456}, once per event
   - c) A raw audio file every second
   - d) A screenshot every frame

   <details><summary>Solution</summary>

   **b** — think at the edge, then send only the summary with the necessary raw evidence. It saves bandwidth and protects privacy.

   </details>

## Lab

**The MVP for lessons 6.5–6.6:** a fused decision (verdict AND a raw gate) is genuinely published to MQTT, once per event, while gentle motion is never sent.

- [ ] Set `CLIENT_ID` and `TOPIC` to include your name. Fill in all five points of the practice file, then run it on the board or the emulator (switching to the accelerometer gate on the emulator).
- [ ] Open a receiving program subscribed to your topic, shake until you see a message on the receiving side, and note a sample payload in your learning log.
- [ ] Find a motion where one stage fails, and confirm no message is sent.
- [ ] Disconnect the network (or enter the wrong WiFi name), and confirm the app falls back to `[SIM]` mode without crashing.

## Going further

In the next module (under the hood), we'll dig into the real Edge AI stack — the tri-core setup, `ai_engine`, the IPC model link, and TFLite-Micro on the NPU — to see how the verdicts we've used throughout the course actually happen.

Next lesson: [lesson 7.1 — The Edge AI stack: tri-core, ai_engine, the IPC model link, and TFLite-Micro](../../m07-under-the-hood/l01-edge-ai-stack/README.md)

## Reflect

- If a hundred boards sent events to the same topic, how would you design the topic name and payload so the receiving end can tell them apart?
- What kind of data should never go to a public broker, and where would you send it instead?
