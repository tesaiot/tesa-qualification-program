---
id: aiot-mpy.m04.l04
lang: en
title: {th: 'MQTT: pub/sub topic QoS และงบข้อมูล', en: 'MQTT: pub/sub, topics, QoS and the data budget'}
summary: {th: 'เข้าใจว่าทำไม IoT เลือก publish/subscribe ผ่าน broker แล้วออกแบบ topic, payload, QoS และงบข้อมูลต่อรอบของทีม โดยรู้เพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดก่อนเขียนโค้ดบรรทัดแรก', en: 'Understand why IoT chooses publish/subscribe through a broker, then design the team''s topics, payload, QoS and per-cycle data budget, knowing the four silent limits of the board''s mqtt module before writing the first line.'}
level: L2
time_min: {concept: 35, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l03]
objectives:
  - {th: อธิบายความต่างของ client–server กับ publish/subscribe ได้ และบอกผลที่ตามมาสามข้อที่ทำให้ IoT เลือกแบบหลัง (บอร์ดไม่ต้องมี IP ที่คนอื่นเข้าถึงได้ · เพิ่มผู้รับได้โดยไม่แตะโค้ดบนบอร์ด · ผู้รับล่มไม่ทำให้ผู้ส่งล่ม), en: 'Explain how client–server differs from publish/subscribe and give the three consequences that make IoT choose the latter (the board needs no reachable IP, receivers can be added without touching board code, a receiver crash does not bring down the sender).'}
  - {th: ออกแบบ topic ของทีมได้ทั้งสองแบบ (`bento/<รหัสของคุณ>/telemetry` บน broker สาธารณะ และ `device/<device_id>/telemetry` บน TESAIoT CE ที่ช่องที่สองต้องเท่ากับ device_id) ตามกติกาตั้งชื่อสี่ข้อ และบอกได้ว่า subscription ที่มี `+` หรือ `#` รับ topic ใดบ้าง, en: 'Design the team''s topics in both patterns (`bento/<team>/telemetry` on a public broker and `device/<device_id>/telemetry` on TESAIoT CE, where the second level must equal the device_id) following the four naming rules, and state which topics a subscription with `+` or `#` receives.'}
  - {th: เลือก QoS ของแต่ละ topic ด้วยคำถาม "ถ้าข้อความนี้หายไปหนึ่งใบ ใครเดือดร้อน" และคำนวณงบข้อมูลต่อรอบได้ เช่น payload 80 ไบต์ทุก 5 วินาทีคือ 16 B/s พร้อมเขียน JSON ที่ทุกค่าที่ต้องขึ้นกราฟเป็นตัวเลข, en: 'Choose each topic''s QoS with the question "if one of these messages is lost, who suffers?", compute the data budget per cycle, e.g. an 80-byte payload every 5 seconds is 16 B/s, and write JSON in which every value meant for a graph is a number.'}
  - {th: บอกเพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดได้ครบ (ช่องรับ 1 ข้อความ · payload ขาเข้า 255 ไบต์ · topic 127 ไบต์ · client_id / username / password 31 ตัวอักษร) พร้อมอาการเมื่อเกิน และอธิบายว่าทำไมลูปต้องฟังคำสั่งทุก 100 ms ไม่ใช่ทุก 5 วินาที, en: 'State all four silent limits of the board''s mqtt module (a 1-message receive slot, 255-byte incoming payload, 127-byte topic, 31-character client_id / username / password) with the symptom when each is exceeded, and explain why the loop must listen for commands every 100 ms, not every 5 seconds.'}
develops: [{skill: proto.mqtt, to: 2}, {skill: iot.fundamentals, to: 2}, {skill: iot.cloud-platform, to: 1}, {skill: hw.architecture, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-10.html (slides 1–15), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: e58478cc5ff5945c962d8c4242524b4d912c0f0a294fdbbb7fde6c1ad7a5087b
---

# Lesson 4.4 — MQTT: pub/sub, topics, QoS and the data budget

> Module 4 — IoT Platform Connectivity · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Understand why IoT chooses publish/subscribe through a broker, then design the team's topics, payload, QoS and per-cycle data budget, knowing the four silent limits of the board's mqtt module before writing the first line.

## Objectives

By the end of this lesson you will be able to:

1. Explain how client–server differs from publish/subscribe and give the three consequences that make IoT choose the latter (the board needs no reachable IP, receivers can be added without touching board code, a receiver crash does not bring down the sender)
2. Design the team's topics in both patterns (`bento/<team>/telemetry` on a public broker and `device/<device_id>/telemetry` on TESAIoT CE, where the second level must equal the device_id) following the four naming rules, and state which topics a subscription with `+` or `#` receives
3. Choose each topic's QoS with the question "if one of these messages is lost, who suffers?", compute the data budget per cycle, e.g. an 80-byte payload every 5 seconds is 16 B/s, and write JSON in which every value meant for a graph is a number
4. State all four silent limits of the board's mqtt module (a 1-message receive slot, 255-byte incoming payload, 127-byte topic, 31-character client_id / username / password) with the symptom when each is exceeded, and explain why the loop must listen for commands every 100 ms, not every 5 seconds

## Before you start

Review two things from lessons 4.1–4.3: `wifi.connect()` can block for about 85 seconds on a wrong password, so get WiFi working before starting on MQTT,
and `wifi.ping()` only accepts an IP number, which we use to check the machine running the broker can really be reached. If `wifi.is_connected()` is False,
do not go looking for the cause in MQTT yet. This lesson has no code to write yet — have your learning log ready to design your team's topics and payload.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/) (this lesson has no code to run yet; the screenshots in the slides come from running lesson 4.5's `03_connect_and_publish.py` on the Emulator, which can only say the board "commanded a send" — the real result must be seen on the receiving machine)
- **Before this:** [Lesson 4.3 — Hands-on: your team's network status page](../l03-network-status-lab/README.md)

## See it work first

Look at the slides' first picture: the board reads a sensor and publishes JSON every 5 seconds to a broker on port 1883, which is a single middleman —
it does not store, does not decide, only forwards. MQTT Explorer on a computer sees every message, and typing a toggle-LED command sends it back to the board,
with neither machine ever knowing the other's address. The next Emulator screenshot shows the three-step ladder before it can send (WiFi has an IP,
broker connected, publish sending). If the screen says it sent but the receiving side sees nothing, it is not finished yet — this set of lessons needs both screens watched at once.

## Concepts

**A ping only proves the cable is good — it proves nothing about anyone at the destination.** And something that can only send is not yet a system; it must also take commands back.
In the client–server style we know, the asker must know the answerer's name and ask first to get an answer — the two sides are tied directly together. In publish/subscribe,
the sender throws data at a topic, and the receiver asks to receive by topic — both sides only know the same topic name. Pub/sub therefore separates sender from receiver both in space
and in time. The result: the board runs out to find the broker itself, so it can sit behind NAT; receivers can be added without touching board code; and a receiver crashing
does not crash the sender. The broker is not a database — it is a post office that receives and forwards immediately. The only commands we use are `CONNECT`, `SUBSCRIBE`, `PUBLISH`, `DISCONNECT`.

**A topic is a tree, not a flat name.** `+` stands for exactly one level; `#` stands for everything below, any number of levels, and must always be last.
In the slides' picture, a laptop subscribed to `/plug1/#` gets every value for plug one; a phone subscribed to `/+/current` gets the current of every plug.
A topic needs no advance declaration — publishing to any name makes it exist. This means discipline is needed on our own: order broad to narrow, never start with `/`,
never include spaces or Thai characters, and never put a fast-changing value into the topic name itself. On the public broker, we guard against collisions with a unique code, for example
`bento/team03/telemetry` and `bento/team03/cmd/led` (in real use, use your own code instead of `team03`,
such as a lowercase English nickname followed by a random 4-digit number like `nok4821`, because other learners share the same broker). On TESAIoT CE, the platform locks the pattern to `device/team03/telemetry`
and `device/team03/commands`, with the second level required to exactly equal the device_id, or the ACL rejects it. Payload only carries the data, because the bridge adds
the device_id and timestamp itself. A nested value like `{"accel":{"x":1}}` is flattened to `accel_x`, and only numeric values become chart lines;
`{"status":"ok"}` is stored but never charted — it must be converted to `{"ok": 1}`. The topic name and the payload's shape are a contract with everyone who consumes this data downstream.

**On the board, WiFi and MQTT both live on CM33_NS, the same core as the Python code**, while CM55, which draws the screen and reads sensors, never touches the network at all.
This picture is true on both the Eva Kit and the Dev Kit. The `mqtt` module always sends TLS credentials as empty, so it can only connect to the plain-text port 1883 —
TLS is in lessons 4.7–4.9. The one rule to remember firmly is that networking work can drop an incoming message into the receive slot "at any moment", not waiting for us to call
`get_message()`, and there is only one slot — two messages arriving back to back before we call it means the second silently overwrites the first, with no error, no flag.
Three more silent limits: an incoming payload over 255 bytes gets truncated until JSON parsing fails · an incoming topic over 127 bytes gets truncated ·
`client_id`, `username`, `password` over 31 characters get truncated, so the platform cannot find the device and rejects the connection. The practical fix is to
poll more often than a human types a command — `sleep_ms(100)` in the loop, not `sleep(5)`, which suits a command paced by a finger, not a constantly flowing stream.

**QoS is the price of the word "sure".** QoS 0 sends once; a dropped network loses it — the cheapest. QoS 1 sends at least once with a PUBACK; a lost ack means resending,
so the receiver may get a duplicate. QoS 2 is exactly once through four round trips, the slowest and most memory-hungry. `mqtt.publish(topic, payload, qos)`
and `mqtt.subscribe(topic, qos)` take qos as a positional argument. Telemetry every 5 seconds uses QoS 0, because the next value is already on its way;
commands should use QoS 1, because a lost command is a press that made nothing happen.

**The data budget per cycle:** $\frac{80\ \text{B}}{5\ \text{s}} = 16\ \text{B/s}$. An outgoing payload of about 80 bytes is well under the safe ceiling of 1000 bytes.
An incoming command of about 26 bytes must never exceed the hard ceiling of 255 bytes. MQTT's fixed header is only 2 bytes, while HTTP's headers run to hundreds of bytes of text
per request — that is the power and network cost of a device sending every five seconds for a year (MQTT 3.1.1 became an OASIS standard on 2014-10-29, and 5.0
on 2019-03-07; most embedded devices still use 3.1.1). The send period is chosen by how fast a measured value actually changes — room temperature is plenty at every 5 seconds,
while motor vibration should have the board summarise it first (a peak RMS value, or a count of threshold crossings). "Send as often as possible" is always a poor design choice.

## Worked example

The slides for this lesson also refer to a file that lives in another lesson:

- [m04-iot-connectivity/l05-mqtt-platform/examples/03_connect_and_publish.py](../l05-mqtt-platform/examples/03_connect_and_publish.py) — connect to the broker and send one set of values up

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. Which of these are reasons IoT chooses publish/subscribe over client–server? Choose every correct one. *(choose all that apply · objective 1)*
   - A) The board needs no IP reachable by others, because it runs out to find the broker itself, letting it sit behind NAT
   - B) A new receiver can be added by subscribing, without touching board code
   - C) The broker keeps every message as a database you can always search back through
   - D) A receiver crashing does not bring down the sender, because neither side waits on the other

   <details><summary>Solution</summary>

   **A, B, D** — pub/sub separates sender from receiver in both space and time. The broker is not a database — it is a post office that receives and forwards immediately, storing nothing unless explicitly told to.

   </details>

2. A team publishes to bento/team03/telemetry and bento/team03/cmd/led. Which subscription receives both topics? *(choose one · objective 2)*
   - A) bento/+/telemetry
   - B) bento/team03/#
   - C) bento/team03/+
   - D) #/team03

   <details><summary>Solution</summary>

   **B** — # stands for every level below, any number deep, so it covers both telemetry and cmd/led. + stands for exactly one level, so bento/team03/+ never reaches cmd/led, which is two levels deep, and # must always be last.

   </details>

3. A device is registered on TESAIoT CE with device_id team03. Which topic does the platform allow it to publish telemetry to? *(choose one · objective 2)*
   - A) /device/team03/telemetry
   - B) telemetry/team03/device
   - C) device/team03/telemetry
   - D) device/ทีม03/telemetry

   <details><summary>Solution</summary>

   **C** — CE locks the pattern to device/<device_id>/telemetry, and the second level must exactly equal the device_id, or the ACL rejects it. Starting with / or including Thai characters both break the naming rules.

   </details>

4. A team sends telemetry every 5 seconds and takes on/off LED commands from a user. What QoS should be chosen? *(choose one · objective 3)*
   - A) QoS 2 for both, for maximum certainty
   - B) QoS 0 for telemetry and QoS 1 for commands
   - C) QoS 1 for telemetry and QoS 0 for commands
   - D) QoS 0 for both, because it's cheapest

   <details><summary>Solution</summary>

   **B** — Losing one telemetry message costs nothing, because the next value arrives within 5 seconds anyway, but a lost command is a press that made nothing happen. QoS 2 is the slowest and most memory-hungry, so it is a poor default.

   </details>

5. A user presses on then off in quick succession, while the board's code is sleeping 5 seconds before calling get_message(). What happens? *(choose one · objective 4)*
   - A) The board gets both commands in order, because the broker queues them
   - B) The board only gets off; on vanishes silently, because the receive slot has only one place and the new message overwrites it
   - C) get_message() raises an error saying the receive slot is full
   - D) The board only gets on, because the first message already reserved the slot

   <details><summary>Solution</summary>

   **B** — Networking work can drop a message into the receive slot at any moment, and there is only one slot, always overwritten, with no error and no flag. The fix is to poll more often than a human types a command, such as sleep_ms(100) in the loop.

   </details>

## Lab

**Design your team's data contract** (about 15 minutes) on paper or in your learning log — no code to write yet.

- [ ] Draw the board · broker · MQTT Explorer picture, with arrows for the direction of outgoing telemetry and returning commands
- [ ] Write your team's topics in both patterns (a public broker guarded with a unique code, and TESAIoT CE where the second level is the device_id), then check against the four naming rules
- [ ] Write one subscription line that receives all of your team's topics, and another that receives every team's telemetry, using `#` or `+`
- [ ] Write a JSON payload with at least three sensor values as numbers, count the bytes, and compute B/s at a 5-second cycle, compared with sending every 100 ms
- [ ] Write a command payload no larger than 255 bytes, and set a client_id no longer than 31 characters
- [ ] Choose each topic's QoS, with an answer to "if one message is lost, who suffers?"

## Going further

Lesson 4.5 walks through all six names of the `mqtt` module, installs TESAIoT Community Edition with Docker, and sends real telemetry and takes real commands from the board.

Next lesson: [Lesson 4.5 — MQTT with a self-hosted platform: telemetry and commands](../l05-mqtt-platform/README.md)

## Reflect

- If a second dashboard wanted to see your team's data tomorrow, what would need to change on the board, and what does that answer tell you about pub/sub?
- How fast does the value your team plans to send actually change — was the send period chosen from that question, or from a feeling?
- Which of the four silent failures do you think you will meet first, and how would you know?
