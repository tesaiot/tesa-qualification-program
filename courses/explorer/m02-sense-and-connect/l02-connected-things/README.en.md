---
id: explore.m02.l02
lang: en
title:
  th: "ของที่คุยกันได้: MQTT และแดชบอร์ด"
  en: "Connected things: MQTT and a dashboard"
summary:
  th: เข้าใจว่า MQTT ส่งข้อความผ่าน broker อย่างไร แล้วส่งค่าเซนเซอร์ขึ้น broker สาธารณะให้ไปโผล่บนหน้าเว็บอ่านค่า
  en: Understand how MQTT moves messages through a broker, then publish sensor values to a public broker and watch them on a web page.
level: L1
time_min: {concept: 12, practise: 13, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [explore.m02.l01]
objectives:
  - th: อธิบายบทบาทของ broker, topic, publish และ subscribe ได้ด้วยแผนภาพหรือคำพูดของตัวเอง
    en: Explain the roles of broker, topic, publish and subscribe with a diagram or in your own words.
  - th: แก้ค่า TEAM ในตัวอย่าง รันให้ค่าเซนเซอร์ขึ้นหน้าเว็บอ่านค่า หรืออธิบายได้ว่าติดที่ขั้นไหนจากป้ายบนจอ
    en: Edit TEAM in the example and run it until sensor values reach the reader page, or explain from the on-screen steps where it stopped.
  - th: ระบุความเสี่ยงของการส่งข้อมูลผ่าน broker สาธารณะที่พอร์ต 1883 ได้อย่างน้อย 2 ข้อ
    en: Name at least two risks of sending data through a public broker on port 1883.
develops:
  - {skill: iot.fundamentals, to: 1}
  - {skill: proto.mqtt, to: 1}
  - {skill: sec.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, emulator: bento-emulator, broker: broker.hivemq.com}
status: alpha
translation: done
source_sha256: f5aeedf4952e6b697042087f88dddad1e13975f4ca26306a36fff14eb69c571a
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s02/05_value_leaves_the_board.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## Objectives

1. Explain the roles of broker, topic, publish and subscribe
2. Run the example so sensor values reach the reader web page, or say where it stopped
3. Name at least two risks of an unencrypted public broker

## Before you start

- In the previous lesson, which key of `sensors.snapshot()` held the knob value?
- If you want a friend in another province to see the knob value on our board, what does the data need to travel through?

## See it work first

This lesson is a guided example. Follow it step by step.

1. Open [examples/01_send_to_dashboard.py](examples/01_send_to_dashboard.py) in BENTO IDE
2. Change the line `TEAM = "teamXX"` to a two-digit number of your own choosing, for example `"team37"` (do not use `team00`)
3. **If you are using a real board**, change `WIFI_SSID` and `WIFI_PASS` to a WiFi network the board can connect to (WiFi that needs a web login usually does not work with a board; use a phone hotspot instead).
   **If you are using the BENTO Emulator**, you do not need to change these two lines; WiFi in the emulator is simulated.
4. Open a new browser tab, go to the AIoT in Action course's reader page, and add the same team number at the end, for example
   `https://advance-innovation-centre-aic.github.io/embedded-systems-for-aiot-developer/examples/web/my_first_reader.html?team=team37`
5. Come back and run the program. Watch the three-step label on screen turn green, then check the web page: the `knob` and `az` number boxes should appear and change every 2 seconds
6. Turn the knob or tilt the board (use the **HW** panel in the emulator) and watch the numbers on the web page move along

**Something you should know if you use the emulator** The emulator tries to connect to the real public broker through the browser. If it cannot connect within a few seconds,
it reports this in the Console drawer and falls back to a simulated broker in the browser instead. In that case the message never leaves your machine, and the web page will not show anything.
If this happens, it is not the code's fault; try again later, or try from a different network.

## Concepts

### 1. A central post office called broker

**MQTT** is a very popular way to send short messages between devices in IoT work. Its heart is the **broker**, which you can think of as a central post office.

- A device with data will **publish** (send) a message to the broker, along with a **topic**, for example `bento-aiot/team37/telemetry`
- Anyone who wants to know about that subject will **subscribe** to that topic with the broker
- The broker forwards the message to everyone who subscribed to that topic. The sender and the receiver never need to know each other

```
  board ──publish──►  broker  ──forwards──►  web page that subscribed
          bento-aiot/team37/telemetry
```

In this example, the board (or the emulator) is the publisher, and the reader web page is the subscriber to the topic `bento-aiot/team37/#`.
The `#` symbol means "every sub-topic underneath this one".

### 2. Three steps you cannot skip or reorder

For data to leave the board, it must pass through three steps in order. **WiFi must first get an IP address**, only then can it **introduce itself to the broker**, and only then can it **publish**.
The example draws a three-step label on screen: a step that passes turns green, a step that fails turns red along with a reason. A good program can always say which step it stopped at.

### 3. What the message looks like

The value sent is packaged as a **JSON** message with `json.dumps()`, for example

```json
{"id": "team37", "n": 5, "knob": 42, "az": 9.79}
```

The reader web page draws one box per key, so we do not need to edit the web page when we add a new key.

### 4. A public broker is not a place to send secrets

`broker.hivemq.com` on port 1883 is open for anyone to use for free, and it is **unencrypted**. Anyone can subscribe to our topic, and anyone can publish fake data into the same topic.
If someone else picks the same team number as you, you might see their values mixed in with yours. This is fine for learning only.
Real work uses **MQTTs** (MQTT over encrypted TLS) with a broker that requires authentication, which is a topic for the next-level course.

## Worked example

[examples/01_send_to_dashboard.py](examples/01_send_to_dashboard.py) is a shortened version of
[`examples/s02/05_value_leaves_the_board.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s02/05_value_leaves_the_board.py)
from the AIoT in Action course. The reader web page is
[`examples/web/my_first_reader.html`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/web/my_first_reader.html)
from the same course.

- **Move 1: check TEAM** If it is still `teamXX`, the program refuses to run, because a name shared with someone else would make the broker kick the other side off
- **Move 2: WiFi** `wifi.connect(ssid, password)` returns `True` or `False`, then asks `wifi.ip()` whether it actually has an IP address (`"0.0.0.0"` means not yet)
- **Move 3: broker** `mqtt.connect(BROKER, port=1883, client_id=..., keepalive=60)` returns `True` when connected successfully
- **Move 4: publish** Read the sensors, build the JSON, then `mqtt.publish(TOPIC, body)` every 2 seconds, catching both `False` and `OSError`
- **Move 5: summarise** `mqtt.is_connected()` answers whether it is still connected "right now"

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/01_send_to_dashboard.webp" alt="examples/01_send_to_dashboard.py running in the BENTO Emulator" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_send_to_dashboard.py"><code>01_send_to_dashboard.py</code></a></figcaption></figure>
</div>

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Lab

Draw your own diagram on paper showing the path of one message, from the knob all the way to the number on the web page, including the words broker, topic, publish and subscribe.
Photograph the diagram together with a screenshot of the web page showing your value (or a screenshot of the on-screen label showing which step it reached), and keep it in your portfolio.

## Going further

- The [AIoT in Action](../../../aiot-micropython/README.md) course builds on this, all the way to receiving commands back from the web page and sending encrypted data up to the TESAIoT Platform
- Read more about MQTT at https://mqtt.org/

## Reflect

If you were to use a system like this to watch a shop's refrigerator, what data would you be willing to let others see, and what data must never be allowed to leak out?
