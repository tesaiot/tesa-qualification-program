---
id: aiot-mpy.m04.l09
lang: en
title: {th: 'ลงมือทำ: ส่งค่าจริงผ่านช่องทางเข้ารหัส', en: 'Hands-on: real readings over an encrypted channel'}
summary: {th: เติมช่องว่างห้าจุดใน s11_secure_telemetry.py ทีละท่าจนค่าเซนเซอร์จริงขึ้นกราฟบน dashboard ของแพลตฟอร์มผ่าน TLS แล้วตอบได้ด้วยคำของตัวเองว่า serverTLS ปกป้องอะไรและไม่ปกป้องอะไร, en: 'Fill the five blanks in s11_secure_telemetry.py one move at a time until real sensor values reach the platform dashboard graph over TLS, then say in your own words what serverTLS protects and what it does not.'}
level: L2
time_min: {concept: 10, practise: 35, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l08]
objectives:
  - {th: 'เติมช่องว่างห้าจุดใน `s11_secure_telemetry.py` โดยรันหลังเติมเสร็จแต่ละท่า จนจอบอร์ดแสดง `device_id` โหมด `tls_mode` และตัวนับที่เดินขึ้นต่อเนื่อง และกราฟของ `device_id` ทีมบน dashboard ขยับตามเมื่อเอียงบอร์ด', en: 'Fill the five blanks in s11_secure_telemetry.py, running after each move, until the board screen shows the device_id, the tls_mode and a counter that keeps rising, and the team''s device_id graph on the dashboard moves when the board is tilted.'}
  - {th: ใช้ตารางกับดักสองหน้าหาสาเหตุของอาการที่ไม่มี error ชี้สาเหตุได้อย่างน้อยสามอาการ เช่น ต่อไม่ติดเงียบ ๆ ข้อมูลขึ้นแต่ไม่มีเส้นกราฟ และหลายบอร์ดหลุดสลับกัน, en: 'Use the two pages of pitfall tables to find the cause of at least three symptoms whose error does not point at the cause, such as a silent failure to connect, data without a graph line, and several boards dropping in turns.'}
  - {th: 'กรอกตารางเทียบ 1883 กับ 8884 ในบันทึกการเรียนจากสิ่งที่เห็นเอง และตอบได้โดยไม่เปิดสไลด์ว่า serverTLS ปกป้องอะไร ไม่ปกป้องอะไร และพอร์ต 8884 มาจาก `tls_mode` ไม่ใช่คีย์ `port`', en: 'Fill the 1883-versus-8884 table in the learning log from what you saw yourself, and answer without the slides what serverTLS protects, what it does not, and that port 8884 comes from tls_mode rather than the port key.'}
  - {th: อธิบายขีดจำกัดสองข้อของงานนี้ได้ คือการเข้ารหัสไม่ได้ทำให้ค่าที่วัดถูกต้องขึ้น และ `mqtt_pass` เป็นความลับที่คัดลอกได้ ต่างจากกุญแจส่วนตัวในชิป OPTIGA ที่ออกจากชิปไม่ได้, en: 'Explain the two limits of this work, that encryption does not make a measured value more correct, and that mqtt_pass is a copyable secret, unlike the private key in the OPTIGA chip that can never leave it.'}
develops: [{skill: sec.tls, to: 2}, {skill: iot.cloud-platform, to: 2}, {skill: soft.problem-solving, to: 2}, {skill: sec.secure-element, to: 1}]
assesses: [{skill: sec.tls, level: 2, evidence: practice/s11_secure_telemetry.py}, {skill: iot.cloud-platform, level: 2, evidence: practice/s11_secure_telemetry.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-11.html (slides 28–45), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 6d8948c0f299e7a6991de9277e8d912c67dd7fa96e1774e67003e61db721444d
---

# Lesson 4.9 — Hands-on: real readings over an encrypted channel

> Module 4 — IoT Platform Connectivity · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the five blanks in s11_secure_telemetry.py one move at a time until real sensor values reach the platform dashboard graph over TLS, then say in your own words what serverTLS protects and what it does not.

## Objectives

By the end of this lesson you will be able to:

1. Fill the five blanks in `s11_secure_telemetry.py`, running after each move, until the board screen shows the device_id, the tls_mode and a counter that keeps rising, and the team's device_id graph on the dashboard moves when the board is tilted
2. Use the two pages of pitfall tables to find the cause of at least three symptoms whose error does not point at the cause, such as a silent failure to connect, data without a graph line, and several boards dropping in turns
3. Fill the 1883-versus-8884 table in the learning log from what you saw yourself, and answer without the slides what serverTLS protects, what it does not, and that port 8884 comes from tls_mode rather than the port key
4. Explain the two limits of this work, that encryption does not make a measured value more correct, and that mqtt_pass is a copyable secret, unlike the private key in the OPTIGA chip that can never leave it

## Before you start

This lesson is a lab following on from lessons 4.7–4.8. Before touching code, have the device's four identity values in your learning log (`device_id` · `api_key` · `mqtt_pass` · the broker's hostname),
from the device management page in your TESAIoT Platform account (see lesson 4.7 — if learning in a group, your organiser may have prepared it for you).
The board is already connected to WiFi, and the platform's dashboard is open with your device selected and waiting. Review two things from lesson 4.8: `connect()` returns before the connection finishes;
the one that can really answer is `is_connected()`, and `tesaiot.publish(payload)` puts payload first, with no topic needed.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/) (filling in the blanks and watching the screen can be rehearsed on the Emulator, because the tesaiot module is simulated, but there is no real TLS handshake and the graph never reaches the dashboard — passing the MVP needs a real board with a `device_id` already from your TESAIoT Platform account, and the OPTIGA chip bonus needs a real board too)
- **Before this:** [Lesson 4.8 — The tesaiot module: MQTTs to the platform](../l08-tesaiot-module/README.md)

## Concepts

This set of lessons' MVP has two halves: your device's telemetry reaches the dashboard over TLS **and** you can say how it differs from lessons 4.4–4.6.
The heart of it is being able to say what serverTLS protects and what it does not. If you cannot answer that, it means we have installed security
without yet knowing what we bought or at what price.

The practice file has already drawn the screen in full; all five blanks are pure logic, and `tesaiot.connect()` **is already given, not a blank** — what we write is the loop that waits for it.
The order of filling in runs from easy to check to hard to check: identity first, because it can be checked without any network at all
(`print(tesaiot.config())` and the table on screen); the wait loop is its own separate move, because "the connection is finished" happens after the command, not as a result of it;
real data is sent once the first two moves are confirmed — if the graph is still empty, you know for certain the problem is the shape of the JSON; and the last move is evidence on screen
letting someone else check the work without opening the code. Ordered this way, a failure always tells you its own location. The screen writes `mqtt_pass` as "set, but cannot read back" instead of leaving it blank,
because a blank field makes a viewer conclude it was never set. The disconnect button has a confirmation box that states what will happen; the reconnect button does not.
**The level of confirmation comes from the price of a mistake**, not from how important the button looks.

The two pages of pitfall tables have thirteen rows; ten of them are not a bug in the code at all, but a misunderstanding of the API's boundaries, and almost none of them give an error that points to the cause,
so you must read it before hitting the problem. Common rows: `sni_hostname` not matching `broker` fails to connect silently · publishing before `is_connected()` is True
raises no error but leaves no data · a wait loop with no timeout hangs forever · several boards using the same default `device_id` drop and reconnect in turns ·
sending a value as a string means data shows up but leaves no graph line · wrapping the payload yourself with `{"data": ...}` gives measurement names starting with `data_` · swapping to
`tesaiot.publish(topic, payload)` sends data to the wrong topic. The row about `protected_update()` on the Dev Kit is the one row where "no error"
means damage has already been done — never call it on either board.

Two limits must be stated clearly. First, **encryption does not make data more correct** — it only stops someone in the middle from reading it. If the measured value was wrong from the start,
it travels wrong, but safely, all the way to the destination. The system's trustworthiness starts at the sensor, not at the certificate. Second, today's `mqtt_pass` is a secret
that **can be copied**, while the private key in the OPTIGA Trust M chip **can never leave the chip at all** — the chip only agrees to sign with it. The chip also holds a factory certificate,
which is the piece mTLS needs. A device identity that cannot be copied must come from hardware, not from a string in a Python file.

## Worked example

Open `07_real_reading_over_tls.py` after the practice file can already send to the platform. This file closes the loop with a value really measured, instead of one made up: measuring every 200 ms
but sending every 5 seconds. The value sent is temperature from `read_temp()`; on the Dev Kit, it comes from the SHT40; the Eva Kit has no temperature sensor, so the knob plays that role instead
(0–100% = 15–45 °C), and the console says where the value came from. Before running, predict which source your team's board will get its value from,
then open the destination and compare whether the number you see matches the number on the board's screen. If using the Eva Kit, try turning the knob and ask yourself whether the destination
can tell this value is not really room temperature.

| File | What this file teaches |
|---|---|
| [examples/07_real_reading_over_tls.py](examples/07_real_reading_over_tls.py) | A value really measured, going out in a form nobody in the middle can read |

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/07_real_reading_over_tls.webp" alt="examples/07_real_reading_over_tls.py running in the BENTO Emulator: A value really measured, going out in a form nobody in the middle can read" width="800" height="480" loading="lazy"><figcaption><a href="examples/07_real_reading_over_tls.py"><code>07_real_reading_over_tls.py</code></a> A value really measured, going out in a form nobody in the middle can read</figcaption></figure>
</div>

## Practice

Open `practice/s11_secure_telemetry.py` and edit the five lines at the top of the file to your own (`TEAM_NAME`, `DEVICE_ID`, `API_KEY`, `MQTT_PASS`, `BROKER`),
then fill in one blank at a time — **never fill in all five and run only once**. On a path with TLS in the middle, there are more places that can break than before, and none of them make a sound.

1. Blanks 1–2: `config_set()` for `device_id`, `api_key`, `mqtt_pass`, then for `broker` and `sni_hostname` (the same name as `broker`).
   Run it and check that `print(tesaiot.config())` shows every value, correctly spelled, and that the left-hand table on screen has no empty box
2. Blank 3: the loop `while not tesaiot.is_connected():`, which after 30000 ms prints a warning and `break`s, otherwise `time.sleep_ms(500)`.
   Run it and time how many seconds until the "success" lamp lights; record it in your learning log
3. Blank 4: a flat dict of real numbers, `accel_x`, `heading`, `pot`, per the comment in the file — never wrap it under `{"data": ...}`
4. Blank 5: `lcd.print("sent count", sent, "| mode", cfg["tls_mode"], "-> 8884")`, then open the dashboard and watch the graph move together with the counter on screen

You know you are done when the "sent ... messages" counter climbs every 5 seconds, the console says mode `serverTLS`, and the team's device graph moves when the board is tilted.
If the left-hand table still shows blank values, blanks 1–2 are not yet complete.

| Practice file | Topic |
|---|---|
| [practice/s11_secure_telemetry.py](practice/s11_secure_telemetry.py) | Send telemetry to the platform over TLS (fill-in version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.md#วิธีใช้เฉลย) first.

| Solution | Goes with |
|---|---|
| [solution/s11_secure_telemetry.py](solution/s11_secure_telemetry.py) | [practice/s11_secure_telemetry.py](practice/s11_secure_telemetry.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. Order the steps of completing the practice file `s11_secure_telemetry.py` so a failure tells you its own location. *(order · objective 1)*
   - A) Fill in the `is_connected()` wait loop with a 30-second ceiling, then time the handshake
   - B) Edit the five lines at the top of the file to your own device's values
   - C) Fill in the payload and the on-screen evidence line, then open the dashboard to watch the graph
   - D) Fill in `config_set()` for identity, then run and check `print(tesaiot.config())`

   <details><summary>Solution</summary>

   **B → D → A → C** — The values at the top of the file must come first. Identity can be checked without any network. The wait loop is its own separate move, because "the connection is finished" happens after the command. Real data is sent once the first two moves are confirmed, so if the graph is still empty, you know for certain the problem is the shape of the JSON.

   </details>

2. Two boards both run correct code, but drop and reconnect in alternating turns. What is the real cause per the pitfalls table? *(choose one · objective 2)*
   - A) Several boards share the same default device_id, so the broker kicks the old one off every time the new one joins
   - B) Every board's sni_hostname does not match broker
   - C) WiFi is too slow for TLS
   - D) time.sleep_ms(5000) was forgotten in the send loop

   <details><summary>Solution</summary>

   **A** — Boards leave the factory with identical default values. Reusing one means the broker keeps kicking the old one off in a loop; the fix is one provisioned device_id per board. A wrong sni_hostname gives the symptom of never connecting at all, not alternating drops.

   </details>

3. Data reaches the platform, but there is no graph line, and some measurement names start with `data_`. What are the possible causes? Choose every correct one. *(choose all that apply · objective 2)*
   - A) A value was sent as a string, such as "25.5", instead of a real number
   - B) The payload was wrapped yourself with `{"data": ...}`, even though the bridge already wraps it
   - C) `sni_hostname` does not match the broker's name
   - D) There is no `is_connected()` wait loop

   <details><summary>Solution</summary>

   **A, B** — Data reaching the platform means the channel and the connection are already working, so the problem is in the data's shape. A string shows a value but cannot be charted, and wrapping it again makes measurement names start with data_, so the units table cannot find them. A wrong SNI or a missing wait loop would mean data never arrives at all.

   </details>

4. A team runs `tesaiot.config_set("port", "1883")`, hoping to compare against the plain-text port, then runs the practice file normally. Which port does the board actually connect to? *(choose one · objective 3)*
   - A) 8884, because the port comes from tls_mode, which is serverTLS; the port key only changes the displayed label
   - B) 1883, unencrypted, following the value set
   - C) 8883, because the board switches to mTLS on its own
   - D) It fails to connect, with an error saying the port is wrong

   <details><summary>Solution</summary>

   **A** — On the tesaiot path, the port is a result of tls_mode: server_tls gives 8884, mutual_tls gives 8883. Setting the port key does not error, but it does not change the real port connected to.

   </details>

5. Which statements about this set of lessons' limits are correct? Choose every correct one. *(choose all that apply · objective 4)*
   - A) If the measured value was wrong from the start, TLS will safely carry that wrong value all the way to the destination
   - B) mqtt_pass is a copyable secret; whoever gets it can impersonate our device
   - C) The private key in the OPTIGA chip can never leave the chip; the chip only agrees to sign with it
   - D) TLS also checks that the sensor value sent is correct

   <details><summary>Solution</summary>

   **A, B, C** — Encryption only stops someone in the middle from reading it; it does not make data more correct, so trustworthiness starts at the sensor. A copy-proof identity must come from a key in hardware, not a password that is a string in a Python file.

   </details>

## Lab

**MVP: telemetry over TLS.** Do this on a real board that already has an identity, and keep evidence in your learning log.

- [ ] The team's `device_id` graph moves on the real platform's dashboard, and moves when the board is tilted
- [ ] The board's screen shows `device_id`, the `tls_mode` mode, and a counter that keeps rising
- [ ] The identity-value box in your learning log has all four values, and `device_id` does not collide with another team's
- [ ] The 1883-versus-8884 comparison table in your learning log is filled in all seven rows from what you saw yourself, not copied from the slides
- [ ] You can answer, without opening the slides, what serverTLS protects and what it does not
- [ ] You can answer what port 8884 is chosen from, and why it is not from the `port` key
- [ ] Pick one item from the extensions: time three rounds of the handshake compared with `mqtt.connect()` · break it one value at a time (`device_id` / `mqtt_pass` / `sni_hostname`) and build your team's own symptom table · demonstrate `optiga.uid()`, `optiga.random(16)`, `optiga.sha256()` (never touch `tesaiot.protected_update()`) · design a schema for a real machine with its daily data volume

## Going further

Module 5 is the capstone: your team chooses your own industrial problem, then assembles sensor → screen → MQTT/MQTTs → platform into one complete system.
Tell a classmate your answer to the extension task when starting lesson 5.1. Anyone who wants to go deeper can watch the TLS clips from Computerphile and Practical Networking at the end of the slides.

Next lesson: [Lesson 5.1 — From a real problem to a design: canvas, schema and designing for failure](../../m05-capstone/l01-problem-to-design/README.md)

## Reflect

- If our device's `mqtt_pass` leaked out, how would we know, and what should be done first?
- Who should decide to revoke a device's access — the platform administrator or the firmware developer?
- If there were 10,000 devices that each needed a unique identity, what should the factory's provisioning process look like?
