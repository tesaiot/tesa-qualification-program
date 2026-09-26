---
id: aiot-mpy.m05.l01
lang: en
title: {th: 'จากโจทย์จริงสู่แบบ: canvas schema และการออกแบบตอนพัง', en: 'From a real problem to a design: canvas, schema and designing for failure'}
summary: {th: เริ่มงานจบจากความเจ็บปวดจริงในงาน แล้วออกแบบบนกระดาษให้ครบก่อนแตะโค้ด ทั้ง canvas ห้าช่อง schema ที่อยู่ได้นาน การส่งเป็นเหตุการณ์ และพฤติกรรมของระบบตอนพัง, en: 'Start the capstone from a real pain point and finish the design on paper before touching code, covering the five-box canvas, a schema that lasts, event-based sending and how the system behaves when things break.'}
level: L2
time_min: {concept: 25, lab: 30, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l09]
objectives:
  - {th: เขียนโจทย์ของทีมจากสามคำถาม (ใครเสียอะไรอยู่ทุกวัน · ตอนนี้เขารู้ได้อย่างไรว่ามีปัญหา · ถ้ารู้เร็วขึ้นสามสิบนาทีจะเปลี่ยนอะไรได้) แล้วกรอก canvas ห้าช่อง Sense → Decide → Show → Send → Act ให้ครบ โดยช่อง Act ระบุว่าใครทำอะไรภายในกี่นาที, en: 'Write the team''s problem from three questions (who loses what every day, how they find out today, what changes if they knew thirty minutes sooner) and fill all five canvas boxes Sense → Decide → Show → Send → Act, with Act stating who does what within how many minutes.'}
  - {th: ออกแบบ payload JSON ของทีมที่เล็ก คงที่ มีหน่วยและ device id ไม่เกิน 1000 ไบต์ อธิบายเหตุผลของทุกฟิลด์ได้ และตั้งชื่อฟิลด์ของค่าตัวแทน (proxy) ให้ประกาศตัวว่าเป็นตัวแทน, en: 'Design a small, stable JSON payload under 1000 bytes with a unit and a device id, justify every field, and name any proxy field so that it declares itself a proxy.'}
  - {th: คำนวณจำนวนข้อความต่อวันของการส่งทุกค่าเทียบกับการส่งเหตุการณ์บวก heartbeat และอธิบายได้ว่าทำไมยังต้องมี heartbeat, en: 'Calculate messages per day for sending every reading versus sending events plus a heartbeat, and explain why the heartbeat is still needed.'}
  - {th: กำหนดพฤติกรรมของระบบในห้าสถานการณ์ตอนพัง (WiFi หลุด · broker ไม่ตอบ · เน็ตกลับมา · ค่ากระโดดวูบเดียว · เตือนแล้วไม่มีใครอยู่หน้าจอ) และตัดสินว่าจะทิ้งหรือเก็บข้อมูลตอนออฟไลน์ พร้อมเหตุผลที่ผูกกับโจทย์ของทีม, en: 'Specify how the system behaves in five failure situations (WiFi drops, broker silent, network returns, a one-off spike, an alert nobody sees) and decide whether to drop or keep data while offline, with a reason tied to the team''s problem.'}
develops: [{skill: iot.fundamentals, to: 2}, {skill: biz.product-decision, to: 2}, {skill: soft.problem-solving, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-12.html (slides 1–21), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 083a7ef369d6a2e6cab1beca6004e5578de7bd5511622604646900cf8ab213d1
---

# Lesson 5.1 — From a real problem to a design: canvas, schema and designing for failure

> Module 5 — Capstone: AIoT Mini-Product · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Start the capstone from a real pain point and finish the design on paper before touching code, covering the five-box canvas, a schema that lasts, event-based sending and how the system behaves when things break.

## Objectives

By the end of this lesson you will be able to:

1. Write the team's problem from three questions (who loses what every day, how they find out today, what changes if they knew thirty minutes sooner) and fill all five canvas boxes Sense → Decide → Show → Send → Act, with Act stating who does what within how many minutes
2. Design a small, stable JSON payload under 1000 bytes with a unit and a device id, justify every field, and name any proxy field so that it declares itself a proxy
3. Calculate messages per day for sending every reading versus sending events plus a heartbeat, and explain why the heartbeat is still needed
4. Specify how the system behaves in five failure situations (WiFi drops, broker silent, network returns, a one-off spike, an alert nobody sees) and decide whether to drop or keep data while offline, with a reason tied to the team's problem

## Before you start

This lesson writes no code yet. Open a fresh page in your **learning log** for the capstone — the five-box canvas, the schema table,
and your team's failure-behaviour table will all live there, and will be used again in lessons 5.2 and 5.3.
Review two things your team already has: the dashboard from lessons 3.7–3.9, and the telemetry sent to a broker
in lessons 4.4–4.6 and 4.7–4.9. This set of lessons introduces not a single new API — only things your team has already run yourselves.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 4.9 — Hands-on: real readings over an encrypted channel](../../m04-iot-connectivity/l09-secure-telemetry-lab/README.md)

## See it work first

Open two things at once: your team's dashboard on the board, and the telemetry flowing into the broker.
While both are running, have a teammate quietly turn off WiFi, and watch what the board's screen does — does it hang, does an error appear in the middle of the screen,
or does it keep working and report its state? Both of these already work, but neither is yet a product. What you see when the network vanishes is the distance
from demo to product that this set of lessons will walk you through.

## Concepts

**A demo and a product differ in decisions made, not in the API used.** A product must be able to answer why this thing needs to exist at all
(someone is losing money or time to this problem right now). The value on screen is a quantity with a unit that someone can actually decide from.
Only what the destination truly uses gets sent up. The screen keeps working when the network drops. And there is a device id to check against.
None of these five needs an API we have not learned yet. What is in our hands is nine modules (`lcd`, `gpio`, `ui`, `sensors`, `dsp`,
`mic`, `wifi`, `mqtt`, `tesaiot`) — check today whether your team's problem needs a name that is not on this list.

**Start from the problem, not from a list of sensors.** Ask in order: who loses what every day · how do they find out today that there is a problem ·
what would change if they knew thirty minutes sooner (unable to answer question three means the problem is not yet worth doing). Only then ask what the board can measure
that speaks to that. If the board cannot measure what you want to know, use a **proxy**, and declare clearly that it is a stand-in, both in the slides and in the field name.
For example, the Eva Kit has no room-temperature sensor, so a cold-room problem instead measures how long the door has been left open, and names the field `door_open_s`, not `temp_c`
(the Dev Kit can read room temperature directly from `sensors.sht40`, but neither board has a gas or current sensor).

**Fill all five canvas boxes before touching the keyboard.** Sense (what to measure, how often, how filtered) · Decide (what threshold, how many rounds to confirm,
decided on the board) · Show (what appears on screen, is it understood within two seconds, does it have a network status and an acknowledge button) · Send (what to send, where, what schema)
· Act (who does what next, within how many minutes). You may fill it right to left, starting from Act, and this often gives a smaller, more focused system.
If nobody does anything in the Act box, that data never needed to be sent in the first place. The example in the slides is a third-floor scaffold that tilts and nobody knows until morning —
this is the problem lesson 5.3's solution carries all the way through.

**A schema that lasts, and event-based sending.** The starter's payload has six fields:
`{"id": "team01", "v": 17.4, "unit": "deg", "state": "ALERT", "kind": "event", "t": 812340}`
— the board's identity, the decided value, its unit, the board's own verdict, the message's type, and the board's own time for ordering.
The rule is: field names stay constant for the whole project; new fields can be added but the meaning of an existing field must never change, and the payload always stays under 1000 bytes.
Reading every 200 ms and sending every value gives 432,000 messages a day per board (about 39 MB), but sending only on a state change
plus a heartbeat every 30 seconds leaves about 2,883. The heartbeat is still needed because silence alone
cannot tell the destination "everything is fine" apart from "the board died yesterday". MQTT itself was born for exactly this kind of poor signal
(designed in 1999, for oil pipelines connected by satellite).

**Design for failure from the very start.** A dropped network is the normal condition of a device installed in the real world; a product must keep drawing the screen and show the word offline,
schedule a retry every 10 seconds, count failed sends and show them on screen, reconnect on its own once the network returns and tell the receiving side,
require a value past the threshold for several rounds in a row before changing state, and hold an alert state until someone presses acknowledge. Another thing that must be decided clearly is
whether to **drop** or **keep for later** while offline. The starter drops and counts, because a tilt reading from ten minutes ago
is no use to someone standing under the scaffold. Either answer can be correct — the wrong thing is never deciding at all.

## Worked example

The slides for this lesson also refer to files that live in another lesson:

- [m05-capstone/l03-build-and-present/practice/s12_capstone_starter.py](../l03-build-and-present/practice/s12_capstone_starter.py) — a mini-product starter structure: Sense -> Decide -> Show -> Send
- [m05-capstone/l03-build-and-present/solution/s12_capstone_starter.py](../l03-build-and-present/solution/s12_capstone_starter.py) — one finished example: a Tilt Alarm for a scaffold or shelf

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. In the slides' tilting-scaffold problem, which is the correctly written Act box for the canvas? *(choose one · objective 1)*
   - A) Send the tilt value to the cloud every 200 ms
   - B) The site supervisor gets an alert and walks over to check within 15 minutes
   - C) Show the word ALERT in large text on screen
   - D) Store the data for a historical chart

   <details><summary>Solution</summary>

   **B** — The Act box is written as "who does what, within how many minutes", not "send to the cloud". If nobody at the destination does anything, that data never needed to be sent in the first place. Showing ALERT on screen is the Show box's job.

   </details>

2. A team using an Eva Kit builds a cold-room problem, but the Eva has no room-temperature sensor, so they measure how many seconds the door has been left open instead. How should this field be named in the schema? *(choose one · objective 2)*
   - A) temp_c, because the real problem is about temperature
   - B) door_open_s
   - C) imu_temp_c, reading from sensors.bmi270.temperature() instead
   - D) cold_room

   <details><summary>Solution</summary>

   **B** — A proxy must declare itself a stand-in, both on the presentation slides and in the field name — name it door_open_s, not temp_c. sensors.bmi270.temperature() on the Eva raises OSError every time, and even if it could be read, it is the IMU chip's own temperature, not the room's.

   </details>

3. Which rules make a schema last a long time? Choose every correct one. *(choose all that apply · objective 2)*
   - A) Field names stay constant for the whole project
   - B) New fields can be added, but the meaning of an existing field must never change
   - C) The outgoing payload always stays under 1000 bytes
   - D) Send raw values for every axis too, in case the destination wants to compute its own
   - E) Rename fields to be clearer as the team understands the problem better

   <details><summary>Solution</summary>

   **A, B, C** — The receiving side writes code to unpack the data once; if we rename a field later, they must fix the whole system. The v field is the value already decided, not a raw one — the destination should not need to recompute it and get an answer that disagrees with the board's.

   </details>

4. A board reads a value every 200 ms. Sending every value gives 432,000 messages a day; changing to send only on a state change plus a heartbeat every 30 seconds leaves about 2,883 messages. Why is the heartbeat still needed? *(choose one · objective 3)*
   - A) So the destination can tell "everything is normal" apart from "the board has died"
   - B) So the destination's chart is as smooth as when every value was sent
   - C) So the filtered-out raw values are all still sent in full
   - D) So the number of messages per day stays the same as before

   <details><summary>Solution</summary>

   **A** — Silence alone cannot tell the destination "everything is fine" apart from "the board died yesterday". A heartbeat every 30 seconds is 2,880 messages a day, plus a handful of real events — still over a hundred times fewer than sending every value.

   </details>

5. A team builds a machine that counts parts produced. When the network drops, which approach makes the most sense? *(choose one · objective 4)*
   - A) Drop every value, because the starter chose to drop
   - B) Keep it to send later, because completeness matters more than freshness here, and record this decision in the learning log
   - C) No decision needed — just let the program do whatever it already does
   - D) Stop counting until the network returns

   <details><summary>Solution</summary>

   **B** — The starter drops and counts, because a tilt reading from ten minutes ago is no use to someone under the scaffold, but a parts counter's answer may be the opposite, because completeness matters more than freshness. Either answer can be correct — the wrong thing is never deciding at all, and letting behaviour happen by accident.

   </details>

## Lab

**Design the capstone on paper** (about 30 minutes, done as a team). Record every item in your learning log.

- [ ] Answer the problem's three questions, then tell another team your problem in under 30 seconds. If they ask "so what", go back and fix question three
- [ ] Pick your own team's problem, or one of the six field problems in the slides, and check the nine-module list to make sure every name you need really exists on your team's board
- [ ] If a proxy is needed, write down what it can and cannot tell you, and name the field so it declares itself a stand-in
- [ ] Fill all five canvas boxes. Write the Act box as "who does what, within how many minutes"
- [ ] Write a two-column schema table (field · why it must exist). Every field has a reason, a unit, and a device id
- [ ] Work out your team's messages per day two ways: sending every value versus sending events plus a heartbeat
- [ ] Write a five-row failure table (WiFi drops, broker silent, network returns, a one-off spike, an alert nobody sees) and decide "drop or keep for later" for each, with one sentence of reasoning
- [ ] Be able to answer: if your team's machine hangs, how would someone walking past know?

## Going further

Lesson 5.2 walks through the starter structure `s12_capstone_starter.py` move by move — bring your filled-in canvas with you, because every "the team writes this" point in the structure
asks for an answer from it. If there is time, watch the extra slides videos on topic design and MQTT's Last Will and Testament.

Next lesson: [Lesson 5.2 — The starter: Sense, Decide, Show, Send](../l02-capstone-starter/README.md)

## Reflect

- If your team's problem cannot answer "what changes if they knew thirty minutes sooner", would the team change the problem, or change who benefits?
- Which field in your team's schema does nobody at the destination actually use yet — what would be lost by cutting it?
- If your team's board went silent all night, could the receiving side tell whether that was normal or dead?
