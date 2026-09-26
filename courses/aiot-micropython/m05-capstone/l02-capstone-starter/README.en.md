---
id: aiot-mpy.m05.l02
lang: en
title: {th: 'โครงตั้งต้น: Sense Decide Show Send', en: 'The starter: Sense, Decide, Show, Send'}
summary: {th: แกะโครง s12_capstone_starter.py ทีละท่า ทั้ง Sense Decide Show Send และการกันเน็ตหลุด ฝึกสามไฟล์ตัวอย่างที่ทำให้ demo ไม่ล้ม แล้วรันโครงบนบอร์ดให้ผ่านก่อนแก้อะไร, en: 'Take the s12_capstone_starter.py skeleton apart move by move (Sense, Decide, Show, Send and surviving a dropped network), practise the three examples that keep a demo standing, and run the skeleton on the board before changing anything.'}
level: L2
time_min: {concept: 15, practise: 30, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m05.l01]
objectives:
  - {th: ชี้ในโครงตั้งต้นได้ว่าห้าท่าอยู่ตรงไหน อธิบายว่า read_value() คืนค่าเดียวพร้อมธง stale อย่างไร และบอกได้ว่าส่วนไหนของวงจรต้องทำงานต่อได้แม้ไม่มีเน็ต, en: 'Locate the five moves in the starter, explain how read_value() returns a single value together with a stale flag, and name which part of the loop must keep working without the network.'}
  - {th: แยกค่าที่วัดได้ออกจากสถานะด้วยฟังก์ชันตัดสินที่ไล่จากเกณฑ์เข้มที่สุดลงมา และบอกราคาของการยืนยัน N รอบเป็นวินาทีได้ (N คูณคาบลูป) จาก 01_state_machine.py และ 02_confirm_n.py, en: 'Separate the measured value from the decided state with a decision function that checks the strictest threshold first, and state the cost of confirming N rounds in seconds (N times the loop period), using 01_state_machine.py and 02_confirm_n.py.'}
  - {th: ตรวจหน้าจอของโครงด้วยเกณฑ์สี่ข้อ (ค่ามาพร้อมพิสัย · สถานะเป็นไฟ · ปุ่มเปิดกับปิดแยกกัน · คำสั่งที่ทำให้ของจริงขยับมีกล่องยืนยันที่บอกสิ่งที่จะเกิด) และหลบกับดักของ ui.MsgBox ได้ทั้งสองข้อ, en: 'Check the starter''s screen against the four rules (value with its range, state as lamps, separate on and off buttons, a confirmation box that says what will happen before anything real moves) and avoid both ui.MsgBox traps.'}
  - {th: รันโครงบนบอร์ดโดยยังไม่แก้ตรรกะ เห็นข้อความ kind event ใน MQTT Explorer เมื่อเอียงบอร์ดเกิน 15 องศา เห็นจอขึ้น offline แต่ยังวาดต่อเมื่อปิด WiFi และอธิบายได้ว่าทำไมการต่อใหม่ต้องนัดเวลา ไม่ต่อรัวทุกรอบลูป, en: 'Run the unmodified starter on the board, see a kind event message in MQTT Explorer when the board tilts past 15 degrees, see the screen show offline yet keep drawing when WiFi is off, and explain why reconnecting must be scheduled rather than retried every loop.'}
develops: [{skill: prog.state-machines, to: 2}, {skill: gui.hmi, to: 2}, {skill: proto.mqtt, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-12.html (slides 22–34), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: e68c370ce25ffecab00ea89ff16496731d1ee83c3cf97d14d88559dab6d4fba6
---

# Lesson 5.2 — The starter: Sense, Decide, Show, Send

> Module 5 — Capstone: AIoT Mini-Product · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Take the s12_capstone_starter.py skeleton apart move by move (Sense, Decide, Show, Send and surviving a dropped network), practise the three examples that keep a demo standing, and run the skeleton on the board before changing anything.

## Objectives

By the end of this lesson you will be able to:

1. Locate the five moves in the starter, explain how read_value() returns a single value together with a stale flag, and name which part of the loop must keep working without the network
2. Separate the measured value from the decided state with a decision function that checks the strictest threshold first, and state the cost of confirming N rounds in seconds (N times the loop period), using 01_state_machine.py and 02_confirm_n.py
3. Check the starter's screen against the four rules (value with its range, state as lamps, separate on and off buttons, a confirmation box that says what will happen before anything real moves) and avoid both ui.MsgBox traps
4. Run the unmodified starter on the board, see a kind event message in MQTT Explorer when the board tilts past 15 degrees, see the screen show offline yet keep drawing when WiFi is off, and explain why reconnecting must be scheduled rather than retried every loop

## Before you start

Bring the five-box canvas and schema table from lesson 5.1 with you in your learning log. If you still cannot answer what your team's problem's "single value" is,
the Sense box is not yet finished. Have MQTT Explorer ready on your computer (already used in lessons 4.4–4.6), the name and password of the WiFi
or hotspot the board will connect to, and a unique code for `DEVICE_ID` and the topic `bento/<code>/...`
(such as a lowercase English nickname followed by a random 4-digit number, `nok4821`, because the starter's broker is public). The starter file is in lesson 5.3's `practice/`.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 5.1 — From a real problem to a design: canvas, schema and designing for failure](../l01-problem-to-design/README.md)

## Concepts

**70 versus 30.** What is already given is firmware that reads sensors and draws the screen, the modules `sensors`, `dsp`, `ui`, `wifi`, `mqtt`,
and the structure `s12_capstone_starter.py`, which already runs a full loop even before anything is changed. The team's remaining 30% is decisions —
from what to measure, what threshold to set, how to design the screen, how to design the schema, all the way to what happens offline. The structure has five moves,
and every line that says "the team writes this" is exactly where the team's work goes.

- **Move 1, Sense** `read_value()` reads `sensors.bmi270.motion()`, feeds it into `dsp.tilt()` (which always returns roll before pitch),
  then filters with `dsp.EMA(alpha=0.2)` — six axes in, one value out. If the read fails (`OSError`), it returns the last value and raises a `stale` flag
  so the screen shows "value stale, cannot read" instead of showing the old number as if it were fresh. There is no need to call `sensors.init()` on the Eva
  (calling it raises `OSError`), and no need on the Dev Kit either. The field warning lamp is chosen **by name** from
  `gpio.board_info()["led_names"]`, because the index differs by board, and `RGB_RED` on the Eva is actually blue
- **Move 2, Decide** `decide()` checks the strictest threshold first, deciding on the board so it can still decide even if the network drops.
  `on_state_change()` is left for the team to write, for what happens when the state changes. The starter believes it the instant a value crosses once;
  the solution adds confirmation across 3 rounds in a row (`CONFIRM_N`)
- **Move 3, Show** the screen follows four rules: `ui.Bar` laid over `ui.Scale` (Scale does not accept `.value()`; it is a ruler) ·
  three `ui.Led`s that light one at a time (`.value(0)` dims, does not vanish) · separate on and off buttons · the off button must pass through a confirmation box.
  The bar and lamp move every round; the status label writes on a state change; the number is rewritten at most once a second, and `lbl_net` tells the truth about the network
- **Move 4, Send, and move 5, surviving a dropped network** `send()` checks `mqtt.is_connected()` before sending and returns `True` or `False`
  so the caller knows the result. Reconnecting is scheduled every `RETRY_MS` (10 seconds), so the loop runs every round regardless of the network's state.
  `client_id=DEVICE_ID` must never collide with another board, or two boards will keep kicking each other off the public broker in turns

The "sensor → decide → screen" path does not depend on the network; the "send to broker" path does. Design it so the important thing lives on the first path,
and if one path fails, the other must not fail with it.

**Two `ui.MsgBox` traps.** A button built into MsgBox itself does not send an event Python can see at all. The starter therefore uses two real `ui.Button`s,
created along with the screen and `.hide()`den. And MsgBox's text carries 95 bytes (about 31 Thai characters);
anything longer is silently truncated. A confirmation message must state what will happen, for example "the field lamp will turn off immediately",
never just ask "confirm?"

## Worked example

**Must be done.** Open these in order, about 28 minutes total. Before running each file, read the "look at the screen" section at the top and predict what you will see.

1. `01_state_machine.py` (10 minutes) — watch the status label change colour when the chart crosses the amber and red lines, then try swapping the order of `if`s in `level_of()`
   to check WARN before ALERT, and watch ALERT vanish, with no error at all
2. `02_confirm_n.py` (10 minutes) — the left label "believe instantly" turns red on a single spike; the right label "confirm 3 rounds" stays green.
   Try changing `CONFIRM_N` and read the "price paid" line in the Console
3. `03_reconnect_backoff.py` (8 minutes) — edit `WIFI_SSID`, `WIFI_PASS`, `BROKER` at the top of the file to match your own network first,
   then unplug the router, and watch the wait interval climb 2000, 4000, 8000 ms up to a ceiling, and reset the instant it reconnects

**Whatever you're stuck on, open this file.** Unplug the router and the whole screen hangs — open `05_hmi_survives_offline.py` (also needs WiFi
and broker edited at the top). Alerts fire so often people stop reading — open `04_heartbeat_and_alert.py`, which separates heartbeat
from alert onto different rhythms and counts held-back messages. Teams who want to use sound as a data source, or want to see that the loop has not hung,
find files from other lessons referenced by the slides below.

| File | What this file teaches |
|---|---|
| [examples/01_state_machine.py](examples/01_state_machine.py) | Three states, and the dividing line decided in advance |
| [examples/02_confirm_n.py](examples/02_confirm_n.py) | How many rounds in a row before it can be believed |
| [examples/03_reconnect_backoff.py](examples/03_reconnect_backoff.py) | Reconnect with growing backoff, never in a rapid burst |
| [examples/04_heartbeat_and_alert.py](examples/04_heartbeat_and_alert.py) | Two kinds of message, two rhythms, two separate jobs |
| [examples/05_hmi_survives_offline.py](examples/05_hmi_survives_offline.py) | The screen must keep working when the network drops |

The slides for this lesson also refer to files that live in other lessons:

- [m03-sensor-hmi/l06-accel-chart-lab/examples/01_imu_vibration_monitor.py](../../m03-sensor-hmi/l06-accel-chart-lab/examples/01_imu_vibration_monitor.py) — watching a machine's vibration
- [m03-sensor-hmi/l08-dashboard-build/examples/02_mic_sound_level_meter.py](../../m03-sensor-hmi/l08-dashboard-build/examples/02_mic_sound_level_meter.py) — a room sound-level meter
- [m05-capstone/l03-build-and-present/practice/s12_capstone_starter.py](../l03-build-and-present/practice/s12_capstone_starter.py) — a mini-product starter structure: Sense -> Decide -> Show -> Send
- [shared/usecase/02_heartbeat_liveness.py](../../shared/usecase/02_heartbeat_liveness.py) — a heartbeat lamp, telling you the loop has not died

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/01_state_machine.webp" alt="examples/01_state_machine.py running in the BENTO Emulator: Three states, and the dividing line decided in advance" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_state_machine.py"><code>01_state_machine.py</code></a> Three states, and the dividing line decided in advance</figcaption></figure>
<figure><img src="img/screens/02_confirm_n.webp" alt="examples/02_confirm_n.py running in the BENTO Emulator: How many rounds in a row before it can be believed" width="800" height="480" loading="lazy"><figcaption><a href="examples/02_confirm_n.py"><code>02_confirm_n.py</code></a> How many rounds in a row before it can be believed</figcaption></figure>
<figure><img src="img/screens/03_reconnect_backoff.webp" alt="examples/03_reconnect_backoff.py running in the BENTO Emulator: Reconnect with growing backoff, never in a rapid burst" width="800" height="480" loading="lazy"><figcaption><a href="examples/03_reconnect_backoff.py"><code>03_reconnect_backoff.py</code></a> Reconnect with growing backoff, never in a rapid burst</figcaption></figure>
<figure><img src="img/screens/04_heartbeat_and_alert.webp" alt="examples/04_heartbeat_and_alert.py running in the BENTO Emulator: Two kinds of message, two rhythms, two separate jobs" width="800" height="480" loading="lazy"><figcaption><a href="examples/04_heartbeat_and_alert.py"><code>04_heartbeat_and_alert.py</code></a> Two kinds of message, two rhythms, two separate jobs</figcaption></figure>
<figure><img src="img/screens/05_hmi_survives_offline.webp" alt="examples/05_hmi_survives_offline.py running in the BENTO Emulator: The screen must keep working when the network drops" width="800" height="480" loading="lazy"><figcaption><a href="examples/05_hmi_survives_offline.py"><code>05_hmi_survives_offline.py</code></a> The screen must keep working when the network drops</figcaption></figure>
</div>

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. On one round, the board fails to read the IMU (sensors.bmi270.motion() raises OSError). What does read_value() do in the starter? *(choose one · objective 1)*
   - A) Stop the program, to keep a wrong value from being sent to the broker
   - B) Return the last value that could be read, and raise a stale flag so the screen shows "value stale, cannot read"
   - C) Return 0, which will send the state back to OK
   - D) Return the last value and display it as if it were just measured normally

   <details><summary>Solution</summary>

   **B** — A device that must run for months must tolerate one bad read round. A stale value is still useful, but must never be shown as if it were fresh. A device that fails to read a sensor and then shows the old number frozen is a device lying to the person in front of it.

   </details>

2. A team writes decide() checking `if value > WARN_LIMIT` first, then `if value > LIMIT` (the ALERT threshold). What happens? *(choose one · objective 2)*
   - A) Works the same, because the order of ifs has no effect
   - B) Raises a runtime error, because the conditions overlap
   - C) ALERT is never reached at all, because the looser condition always catches it first, with no error visible
   - D) Reaches ALERT sooner, because the lower threshold is checked first

   <details><summary>Solution</summary>

   **C** — A value over LIMIT is also over WARN_LIMIT, so it always gets caught as WARN first. Checks must always be ordered from strictest to loosest — exactly the trap 01_state_machine.py points to.

   </details>

3. If CONFIRM_N = 3 and the loop runs every 200 ms, how much slower does the system alert compared with believing instantly? *(choose one · objective 2)*
   - A) 0.2 seconds
   - B) 0.6 seconds
   - C) 3 seconds
   - D) No slower at all

   <details><summary>Solution</summary>

   **B** — The price of confirmation is N times the loop period: 3 × 200 ms is six-tenths of a second. The team must be able to state this number in seconds — not just set N large without knowing the cost, in trade for a single spike no longer triggering a false alert.

   </details>

4. A team uses the button built into ui.MsgBox as the confirm button for turning off the warning lamp, then waits for someone to press it. What happens? *(choose one · objective 3)*
   - A) Works normally, because MsgBox sends a clicked event like any other button
   - B) A dead button on screen, because a button built into MsgBox does not send an event back to Python; two real ui.Buttons must be used instead
   - C) The warning lamp turns off immediately with no need to wait for a press
   - D) The board resets, because there are not enough handles

   <details><summary>Solution</summary>

   **B** — The firmware only binds a callback to ui.Button; a button built into MsgBox does nothing when pressed, and whoever presses it will conclude the machine has hung. The starter creates "confirm" and "cancel" buttons along with the screen and hides them, showing them only when asked.

   </details>

5. Which statements about moves 4 and 5 of the starter are correct? Choose every correct one. *(choose all that apply · objective 4)*
   - A) send() returns False when not yet connected to the broker, so the caller knows the result and can count failed sends
   - B) Reconnecting is scheduled every RETRY_MS, so the loop and screen run every round even when the network drops
   - C) Two boards can share the same client_id, as long as they publish to different topics
   - D) If it fails to connect, go_online() should be called every loop round, to reconnect as fast as possible

   <details><summary>Solution</summary>

   **A, B** — send() never fails silently, and reconnecting is scheduled. Retrying rapidly every round would bog down the loop and make the screen stutter. A colliding client_id makes two boards kick each other off in a loop, regardless of which topic each publishes to.

   </details>

## Lab

**Run the starter successfully before changing anything** (about 15 minutes). Record what you see for every item in your learning log.

- [ ] On the board's screen, touch the BENTO Playground card and keep this page open
- [ ] Open `s12_capstone_starter.py` in BENTO IDE and edit the CONFIG block to your own: `DEVICE_ID`, `WIFI_SSID`, `WIFI_PASS`, `TOPIC` (use a unique code in both `DEVICE_ID` and the topic `bento/<code>/...`, such as `nok4821`, because the starter's broker is public)
- [ ] Press Program to Device without changing any logic yet — the screen must show three cards and run immediately (on the Eva, the first sensor read after a reset can wait about 16 seconds, and `wifi.connect()` can block for a while — do not press run again right away)
- [ ] Open MQTT Explorer and subscribe to `bento/<code>/#`
- [ ] Tilt the board past 15 degrees and hold it — the "abnormal" lamp lights, a "waiting for acknowledgement" label appears, and a message with `kind` of `event` reaches the broker
- [ ] Test failure: turn off the WiFi the board is connected to (or unplug the router) — the screen must keep drawing, and the network status line shows offline with a count of failed sends
- [ ] Write a list of the "the team writes this" points in the file, and match each one to the canvas box that answers it

## Going further

Lesson 5.3 begins replacing the "the team writes this" points one at a time until it becomes your team's own work, then prepares for the presentation. If there is time, watch the extra slides video
on MQTT's QoS, which is the protocol-level answer to the question of messages not arriving. The upgrade path is `tesaiot.connect()`
over TLS on port 8884, from lessons 4.7–4.9, but it needs each team's device identity provisioned first, which is why it is not in the starter.

Next lesson: [Lesson 5.3 — Build and present your AIoT mini-product](../l03-build-and-present/README.md)

## Reflect

- What is your team's problem's "single value", and how many axes of raw data does it come from?
- If this screen were mounted in front of a real machine, would someone walking past understand within two seconds whether it is normal or not?
- Which command on your team's screen would be irreversible if pressed by mistake, and what should its confirmation box say will happen?
