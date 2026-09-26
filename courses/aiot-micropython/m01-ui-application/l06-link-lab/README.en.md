---
id: aiot-mpy.m01.l06
lang: en
title: {th: 'ลงมือทำ: พาค่าจริงออกจากบอร์ด และสรุปโมดูล 1', en: 'Hands-on: a real value leaves the board, module 1 wrap-up'}
summary: {th: ปิดชุดบทเรียน 1.4–1.6 ด้วยแล็บของทีม ผ่าน MVP checkpoint จากไฟล์ตัวอย่างทั้งชุด เติมสมุดบันทึกผลการทดลอง s02_ai_observer.py ด้วยค่าที่ทีมวัดเอง แล้วสรุปว่าโมดูล 1 วางรากอะไรไว้ให้โมดูลถัดไป, en: 'Close lessons 1.4–1.6 with a team lab - pass the MVP checkpoint across the whole example set, fill the s02_ai_observer.py lab notebook with trials your team measured itself, and sum up what module 1 lays down for the modules ahead.'}
level: L2
time_min: {concept: 10, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m01.l05]
objectives:
  - {th: ผ่าน MVP checkpoint ของชุดบทเรียน คือบอร์ดของทีมขึ้นเลข IP ที่ไม่ใช่ 0.0.0.0 ด้วย wifi.connect() และติ๊กครบทุกข้อในรายการตรวจ (01 04 02 05 06 03) พร้อมรูปหน้าจอบอร์ดในบันทึกการเรียน, en: 'Pass the MVP checkpoint - the team''s board shows an IP other than 0.0.0.0 via wifi.connect(), and every item on the checklist (01, 04, 02, 05, 06, 03) is ticked, with a photo of the board screen in your learning log.'}
  - {th: เติมช่องว่างหกจุดใน s02_ai_observer.py ด้วยผลการทดลองสามแถวที่ทีมวัดเองบนบอร์ด จนลิ้นชัก Console ขึ้นครบทุกแถว มาตรวัดเวลาต่อเฉลี่ยขยับจากศูนย์ และแผงขวาติดดวง "ต่ออยู่" พร้อมเลข IP, en: 'Fill the six blanks in s02_ai_observer.py with three trials your team measured on the board, until the Console drawer lists every row, the average-connect-time gauge moves off zero, and the right panel lights "connected" with an IP.'}
  - {th: ระบุสาเหตุที่แท้จริงและวิธีแก้จากอาการในตารางกับดักที่เจอบ่อยได้ และแยกได้ว่าอาการไหนไม่มี error ให้จับเลย, en: 'Name the real cause and the fix for symptoms in the common-traps table, and tell which symptoms raise no error at all.'}
  - {th: อธิบายหลักออกแบบสี่ข้อที่ชุดบทเรียนนี้ใช้ (บอกได้ว่าล้มที่ขั้นไหน · ไม่เชื่อข้อมูลที่คนอื่นส่งมา · รอหลักฐานหลายรอบก่อนรายงาน · ใช้ข้อมูลที่บันทึกไว้เป็นชุดทดสอบ) พร้อมชี้ไฟล์ที่ใช้แต่ละข้อ, en: 'Explain the four design principles this set of lessons uses (say which step failed, never trust data others send, wait for several rounds of evidence before reporting, use recorded data as a test set) and point to the file that uses each one.'}
develops: [{skill: proto.wifi, to: 2}, {skill: proto.mqtt, to: 2}, {skill: soft.teamwork, to: 1}]
assesses: [{skill: proto.wifi, level: 2, evidence: practice/s02_ai_observer.py}, {skill: lang.micropython, level: 2, evidence: practice/s02_ai_observer.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-02.html (slides 27–38), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: a3afbfafe9b2d623ab58f7ec3bcb90eb448dfd2acfcbd8c8ddadbac86913d2ee
---

# Lesson 1.6 — Hands-on: a real value leaves the board, module 1 wrap-up

> Module 1 — Existing UI-based Application · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Close lessons 1.4–1.6 with a team lab: pass the MVP checkpoint across the whole example set, fill the s02_ai_observer.py lab notebook with trials your team measured itself, and sum up what module 1 lays down for the modules ahead.

## Objectives

By the end of this lesson you will be able to:

1. Pass the MVP checkpoint for this set of lessons: the team's board shows an IP other than 0.0.0.0 via wifi.connect(), and every item on the checklist (01, 04, 02, 05, 06, 03) is ticked, with a photo of the board screen in your learning log
2. Fill the six blanks in s02_ai_observer.py with three trials your team measured on the board, until the Console drawer lists every row, the average-connect-time gauge moves off zero, and the right panel lights "connected" with an IP
3. Name the real cause and the fix for symptoms in the common-traps table, and tell which symptoms raise no error at all
4. Explain the four design principles this set of lessons uses (say which step failed, never trust data others send, wait for several rounds of evidence before reporting, use recorded data as a test set) and point to the file that uses each one

## Before you start

Open your learning log with results from lessons 1.4 and 1.5: the board's IP address, the time `connect()` took for both a correct and a wrong password, the dBm figures from `04`, and the outcome of `03`.
The board can already join your team's phone hotspot, your team's `my_first_reader.html` page is open, and on the board's screen the **BENTO Playground** card is open before you send any code.
One board per team, taking turns at the keyboard; whoever is not typing takes on timing and recording the numbers.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 1.5 — Values out, commands back: MQTT on a public broker](../l05-values-out-commands-back/README.md)

## Concepts

This lesson has no new commands. **The team's job is the example files from lessons 1.4–1.5 themselves.** Work through four steps in order: get onto the network (`01`, `04`) · watch the link and actually force it to drop (`02`)
· send a value out and take a command back (`05`, `06`) · define for yourself what counts as a usable link until the two numbers match (`03`). Edit one file at a time, run it, then move on — never edit several files and run them all at once.
The practice file `s02_ai_observer.py` is a lab notebook: it puts results your team wrote down by hand on screen as a table, then takes the board online and reports its IP address back.
The two together are the shape of almost every front-line instrument: measure, record, then report out. And because the table holds values written down by hand, not values measured live, the screen labels it as such —
a value that does not say where it came from is a value you cannot trust.

Half of the common-traps table has **no error to catch at all**. The program runs through quietly and reports something untrue: `if wifi.ip():` passes even when it got `"0.0.0.0"` ·
the signal-strength chart is a flat zero line because it picked up `wifi.status()["rssi"]` · three commands are sent but the board only counts one, because the inbox has room for only one message · two boards keep kicking each other off because `client_id` collides ·
the web page stays empty because `TEAM` does not match in the two places, or the page was opened after the board finished sending (the firmware cannot publish with retain) · setting the `port` key of `tesaiot` has no effect at all.
The traps that do raise a visible error are `TypeError` from `user=` (the real name is `username=`) and `OSError` from `publish()` when the link drops. The silent kind is the most expensive bug in networking work.

What we touched today has three sides. The network side: joining a network happens in stages, getting an address is a separate step from joining, a broker lets the sender and receiver be strangers to each other,
and failure takes longer than success because there are hidden retries. The Python side: `dict` and JSON · `bytes` versus `str` and `.decode()` · `try/except` with a failure you already expected ·
comparing strings directly instead of relying on truthiness · timing across a command you cannot control. The systems-design side: a program that fails must be able to say which step it failed at (`05`)
· data from someone else must always be checked before use (`06`) · wait for several rounds of evidence before reporting (`NEED` in `03`) · use recorded data as a test set instead of relying on real-world conditions you cannot control (the tape in `03`).

Lessons 1.1–1.6 have been about seeing the whole set of what the library offers — from the screen, sensors and sound, to sending data to someone in another place — not so you memorise every bit of it,
but so you know what the destination looks like. Starting from lesson 2.1 we go back and build it piece by piece with our own hands: driving hardware directly in module 2, reading sensors and drawing dashboards in module 3,
then sending it up to a platform and building something real in modules 4–5. The "read → decide → report" loop is still the same shape.

## Worked example

This lesson has no example files of its own; it uses the files from lessons 1.4 and 1.5, in the four steps: `01` → `04` → `02` → `05` → `06` → `03`,
completing the **your turn** block at the end of every file. If you get stuck on any step, open the traps table in the slides before asking anyone else. `07_button_to_broker.py` in the list below belongs to lesson 2.3.

The slides for this lesson also refer to files that live in other lessons:

- [m01-ui-application/l02-first-lines-on-screen/examples/06_safe_print.py](../l02-first-lines-on-screen/examples/06_safe_print.py) — a print helper that is never cut off silently
- [m01-ui-application/l04-wifi-first-connect/examples/01_wifi_first_connect.py](../l04-wifi-first-connect/examples/01_wifi_first_connect.py) — take the board online for the first time, then read its own address
- [m01-ui-application/l04-wifi-first-connect/examples/02_link_uptime.py](../l04-wifi-first-connect/examples/02_link_uptime.py) — "connected" and "still connected" are not the same question
- [m01-ui-application/l04-wifi-first-connect/examples/04_scan_the_room.py](../l04-wifi-first-connect/examples/04_scan_the_room.py) — have the board listen to the whole room, and say who is where
- [m01-ui-application/l05-values-out-commands-back/examples/03_your_link_rule.py](../l05-values-out-commands-back/examples/03_your_link_rule.py) — this file runs, but it cannot see the second kind of problem
- [m01-ui-application/l05-values-out-commands-back/examples/05_value_leaves_the_board.py](../l05-values-out-commands-back/examples/05_value_leaves_the_board.py) — a value measured on this desk shows up on someone else's machine
- [m01-ui-application/l05-values-out-commands-back/examples/06_command_comes_back.py](../l05-values-out-commands-back/examples/06_command_comes_back.py) — someone else types a command from far away, and a light on our desk turns on
- [m02-ui-to-hardware/l03-led-button-lab/examples/07_button_to_broker.py](../../m02-ui-to-hardware/l03-led-button-lab/examples/07_button_to_broker.py) — a button and a light on our desk end up on the broker, for a web page to read
- [shared/web/my_first_reader.html](../../shared/web/my_first_reader.html) — reads values from the board

## Practice

Open `practice/s02_ai_observer.py` and work in three steps: **one**, run trials on the real board with `01_wifi_first_connect.py` to get three rows of results (for example, standing next to the hotspot, walking to the far end of the room, a wrong password),
and overwrite all three rows in `TRIALS` — the rows already filled in are just an example of the shape from an earlier round, not results to copy. **Two**, edit `TEAM_NAME`, `WIFI_SSID`, `WIFI_PASS` at the top.
**Three**, fill the six blanks following the `# เติม:` (fill in) hints **one at a time**, sending to the board each time: clearing the drawer and the `h2` heading · printing each row to the drawer · calculating `avg_ms` · `wifi.connect()` · the line reporting the IP.
The screen has already been written for you in full — the gaps are in the logic, not the drawing. How to know you passed: the drawer has a heading and one line per row, the time gauge does not sit still at zero (if it does, `avg_ms` has not been filled in yet),
and the right panel lights "connected" with an IP address — check by eye that the number is not `0.0.0.0`, per the MVP item — and always record the minimum and maximum alongside the average in your learning log,
because an average of three trials does not yet count as a measurement.

| Practice file | Topic |
|---|---|
| [practice/s02_ai_observer.py](practice/s02_ai_observer.py) | A lab notebook, then taking the board online (fill-in version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.md#วิธีใช้เฉลย) first.

| Solution | Goes with |
|---|---|
| [solution/s02_ai_observer.py](solution/s02_ai_observer.py) | [practice/s02_ai_observer.py](practice/s02_ai_observer.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. The organisation's network blocks a port across the whole room. The team runs file 05 and step 2 turns red. How can MVP item 05 still count as passed? *(choose one · objective 1)*
   - A) The team can point from the screen to which step the link broke at and why
   - B) They must wait until the network is opened up; there is no other way to pass
   - C) Edit the code so step 2 skips straight to step 3
   - D) Change TEAM to a nearby team's, since theirs already got through

   <details><summary>Solution</summary>

   **A** — Item 05 passes when you see your own team's value on the web page, or, if the room's network blocks the port, the team can read from the screen which step the link broke at and why. A program that fails and can say where it failed is itself a usable outcome.

   </details>

2. You run s02_ai_observer.py and the table fills in with all three rows, but the average-connect-time gauge sits still at zero. What does that mean? *(choose one · objective 2)*
   - A) The board failed to connect to WiFi
   - B) The line avg_ms = total_ms // len(TRIALS) has not been filled in yet, so the value is still the 0 it was preset to
   - C) ui.Bar cannot take a value over 1000
   - D) The TRIALS table must have at least five rows

   <details><summary>Solution</summary>

   **B** — The file presets avg_ms = 0 so it can run even before you fill it in. The gauge moves only once after the calculation runs; if it stays at zero, that is the answer telling you the blank is not yet filled.

   </details>

3. Which symptoms in the traps table have **no error to catch**, with the program simply continuing quietly? Choose every correct one. *(choose all that apply · objective 3)*
   - A) The signal-strength chart is a flat zero line forever, because it picked up wifi.status()["rssi"]
   - B) The code says it has an IP but cannot send anything, because it was written as if wifi.ip()
   - C) mqtt.connect() was given user= instead of username=
   - D) Three commands are sent but the board only counts one

   <details><summary>Solution</summary>

   **A, B, D** — status() returns a fixed rssi value, "0.0.0.0" is a string Python treats as true, and the inbox has room for only one message so a new one overwrites the old. None of these three raise any error at all. user= raises a TypeError immediately.

   </details>

4. The board runs file 05 and sends every message, but your team's web page stays empty. What should you fix? *(choose one · objective 3)*
   - A) Change the broker to broker.mqttdashboard.com
   - B) Check that TEAM matches in the web page and in the file, then rerun file 05 while the web page is already open
   - C) Have the web page subscribe to every topic with the # wildcard, so nothing is missed
   - D) Wait a while — the broker will send the stored message on its own

   <details><summary>Solution</summary>

   **B** — The cause is TEAM not matching in the two places, or the web page being opened after the board finished sending. The firmware cannot publish with retain, so the broker keeps no last message for anyone.

   </details>

5. The 24-round tape of checks in 03_your_link_rule.py is an example of which design principle? *(choose one · objective 4)*
   - A) Use recorded data as a test set, instead of relying on real-world conditions you cannot control
   - B) Never trust data someone else sends
   - C) Be able to say which of the three steps of the ladder failed
   - D) Publish with retain so a web page opened late still sees the value

   <details><summary>Solution</summary>

   **A** — A tape recorded from a real board gives the same result no matter how many times you replay it. A rule you cannot test repeatably is a rule you do not yet know is right, and this is exactly the move software test teams around the world make every day.

   </details>

## Lab

**MVP checkpoint.** Lessons 1.4–1.6 are passed when the team connects the board to the network with `wifi.connect()` and successfully reports an IP address on screen. In concrete, checkable terms:

- [ ] Edit `WIFI_SSID` and `WIFI_PASS` to match your team's phone hotspot, on your own
- [ ] `01_wifi_first_connect.py` shows an IP address on screen that is **not** `0.0.0.0`
- [ ] Record the time `connect()` took for both a correct and a wrong password, and explain why they differ
- [ ] `04_scan_the_room.py` lists the networks in the room, and you can point out where the number from `status()` differs from the number from `scan()`
- [ ] `02_link_uptime.py` runs the full 30 seconds, you make the link actually drop once, and you can point to the exact second it dropped (the item most teams miss, because you have to actively force it to break)
- [ ] `05_value_leaves_the_board.py` — you see your own team's value on the web page, or, if the room's network blocks it, you can read from the screen which step the link broke at and why
- [ ] `06_command_comes_back.py` — you can say which topic the board is listening to, and what commands it understands
- [ ] `03_your_link_rule.py` reports exactly 2 times (the two numbers on screen match)
- [ ] Take a photo of the board's screen and attach it to your learning log

**Pass the message around the room** (if learning as a class): every board runs `06` with its own `TEAM`. The educator sends a secret word as `say` to `team01`. The team that sees the word on screen relays it to the next team via the control centre
using the shared `mqtt_dashboard.html` page, until the last team sends it back to `team00` on the educator's desk. Split into four roles: the person at the board · the control centre · the timekeeper · the fixer (if the word does not show up, check the Console drawer to see how far it got).
`06` listens for 15 minutes — if it has been running longer than that before the game starts, run it again first.

**Teams that finish early** can run `05` and `06` at the same time on two boards with a nearby team, so one board sends the knob value and the other board sends a command back to switch a light.

## Going further

Team homework: pick one of these four and record it in your learning log — a door screen from `02` readable from three metres away · add your team's own value to the `payload` in `05` ·
add a fourth command to `06` · record your own `TAPE` in `03` and set `WANT_REPORTS` to match. Lessons 2.1–2.3 start driving hardware directly for the first time —
every LED (`gpio.num_leds()`: Eva Kit 3, Dev Kit 5) and one real user button — and `07_button_to_broker.py` in lesson 2.3 will publish a button press to this same broker; keep your team's web page.

Next lesson: [Lesson 2.1 — The gpio module: LEDs, a button and a board that describes itself](../../m02-ui-to-hardware/l01-gpio-leds-buttons/README.md)

## Reflect

- If your team's board had to hang in a factory for six months, reporting a value every minute, how would you know it stopped reporting at three in the morning?
- Who should be allowed to send a command back to control the board, and what today actually stops a stranger from doing it?
- In your team's `TRIALS` table, which value do you trust the least, and does your screen already tell viewers where it came from?
