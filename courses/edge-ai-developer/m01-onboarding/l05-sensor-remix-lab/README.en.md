---
id: edgeai-dev.m01.l05
lang: en
title: {th: 'ลงมือทำ: remix เป็น Tilt Monitor ของเรา', en: 'Hands-on: remix it into your own Tilt Monitor'}
summary: {th: remix สามแอปเซนเซอร์เป็น Tilt Monitor ของเราเอง ด้วยการเติมสี่ช่องที่เป็นหัวใจของโครงร่วม แล้วลองสลับเซนเซอร์ เปลี่ยนการแสดงผล และจงใจทำให้พังแล้วซ่อม จนอธิบายได้ทุกบรรทัดว่าอยู่จังหวะไหน, en: 'Remix the three sensor apps into your own Tilt Monitor by filling the four blanks at the heart of the skeleton, then swap the sensor, change the display and break-and-fix until you can place every line in its beat.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l04]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) จนเอียงบอร์ดแล้วเกจสองแกนขยับ มุมเด่นขึ้น Seg7 ป้ายเปลี่ยนเป็น TILTED เมื่อเอียงถึง 20 องศา และกดปุ่มออกแล้วโปรแกรมจบ', en: 'Fill the four blanks in practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) until tilting moves both gauges, the dominant angle shows on the Seg7, the panel turns TILTED at 20 degrees, and the back button ends the program.'}
  - {th: วินิจฉัยอาการเข็มไม่ขยับ มุมเป็นศูนย์ตลอด ตัวเลขใหญ่ไม่เปลี่ยน และกดออกแล้วไม่ออก ว่าเกิดจากช่องใดที่ยังไม่ได้เติม, en: 'Diagnose a still needle, an angle stuck at zero, a big number that never changes and a back button that does nothing, each to the blank that is still empty.'}
  - {th: ทำ remix ที่ต่างจากต้นฉบับอย่างน้อยหนึ่งอย่าง (สลับเป็น sensors.radar() หรือเปลี่ยนการแสดงผล) แล้วชี้ได้ว่าบรรทัดใดอยู่จังหวะใดและแต่ละคำสั่ง sensors.* กับ dsp.tilt ทำอะไร, en: Make at least one remix that differs from the originals (switch to sensors.radar() or change the display) and point out which line belongs to which beat and what each sensors.* and dsp.tilt call does.}
develops: [{skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: gui.embedded, to: 2}, {skill: soft.problem-solving, to: 2}]
assesses: [{skill: lang.micropython, level: 2, evidence: practice/s02_anatomy_sensor.py}, {skill: sys.sensors-actuators, level: 2, evidence: practice/s02_anatomy_sensor.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: c7b45795a006f6ac9f048a31b708b1e120473ce2f9e06c1ddb4e61ef9bdae588
---

# Lesson 1.5 — Hands-on: remix it into your own Tilt Monitor

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Remix the three sensor apps into your own Tilt Monitor by filling the four blanks at the heart of the skeleton, then swap the sensor, change the display, and deliberately break and fix it, until you can place every line in its beat.

## Objectives

By the end of this lesson, you will:

1. Fill the four blanks in practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) until tilting the board moves both gauges, the dominant angle shows on the Seg7, the panel turns TILTED at 20 degrees, and the back button ends the program.
2. Diagnose a still needle, an angle stuck at zero, a big number that never changes, and a back button that does nothing — each to the blank that's still empty.
3. Make at least one remix that differs from the originals (switching to sensors.radar(), or changing the display), and point out which line belongs to which beat, and what each sensors.* and dsp.tilt call does.

## Before you start

You've been through lesson 1.4, and remember the three-app comparison table: what "read, compute, draw" means for each app. Open the practice file in BENTO IDE, and keep your learning log ready to note what you changed in your remix, and why.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 1.4 — Taking a sensor app apart: the four-beat skeleton of every program](../l04-sensor-app-anatomy/README.md)

## Concepts

Our task is a **Tilt Monitor**: take the "read" slot from `01` (`bmi270.motion()`), the "compute" slot from `02` (`dsp.tilt`), and the "only redraw on change" trick from `04`, and blend them into a new app. A pair of arc gauges shows pitch and roll, a Seg7 shows the largest tilt angle, and a LEVEL/TILTED label changes colour past `TILT_LIMIT` = 20 degrees. The constants `DEAD` and `TILT_LIMIT` at the top of the file are the easiest knobs to remix.

The practice file already gives you beats 1–2 (import and creating widgets) in full — the four blanks sit exactly in beats 3–4: read the IMU, convert it into an angle, put the dominant angle on the Seg7, and `raise KeyboardInterrupt` when the back button is pressed. Notice the event-driven drawing nested two levels deep: the outer check is whether the angle changed, the inner check is whether the tilted/flat status changed — both exist to avoid touching the screen more than necessary.

Remixing is the heart of PRIMM's Modify step: **swap the sensor** (read `sensors.radar()` and show presence or energy instead of an angle — the skeleton doesn't need touching), **change the display** (Seg7 to a Bar, change `TILT_LIMIT` to 10), and **break and fix** (move `ui.Arc(...)` into the loop, watch the screen flicker, then move it back). A remix that runs but that its own author can't explain doesn't count yet — the goal is "being able to read it," not just "copying it until it runs."

## Worked example

`s02_anatomy_sensor_full.py` is a polished version that adds an |a| bar, remembers the peak angle ever seen, and a Reset button. Open it once your own practice file is working, to compare how it builds on the same skeleton.

| File | What this file teaches |
|---|---|
| [examples/s02_anatomy_sensor_full.py](examples/s02_anatomy_sensor_full.py) | A Tilt Monitor remix (full version) |

## Practice

The file has 4 blanks (lines 62, 67, 76 and 96), each marked with a `# TODO:` comment. 1) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` 2) `roll, pitch = dsp.tilt(ax, ay, az)` 3) `seg.text("%d" % ang)` 4) `raise KeyboardInterrupt`. Tilt the board slowly and check whether the needle, the number and the label all respond.

| Practice file | Topic |
|---|---|
| [practice/s02_anatomy_sensor.py](practice/s02_anatomy_sensor.py) | Taking apart a sensor app's structure, then remixing it yourself (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s02_anatomy_sensor.py](solution/s02_anatomy_sensor.py) | [practice/s02_anatomy_sensor.py](practice/s02_anatomy_sensor.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. What's the Tilt Monitor's second blank? *(single choice · objective 1)*
   - a) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
   - b) roll, pitch = dsp.tilt(ax, ay, az)
   - c) seg.text("%d" % ang)
   - d) raise KeyboardInterrupt

   <details><summary>Solution</summary>

   **b** — blank 1 reads, blank 2 computes the angle with dsp.tilt, blank 3 draws the dominant angle, and blank 4 exits the loop when the back button is pressed, matching the read-compute-draw-listen skeleton.

   </details>

2. You run it and the needle never moves, and the angle stays at 0 no matter how you tilt the board. What's the most likely cause? *(single choice · objective 2)*
   - a) Blank 1 hasn't been filled in yet, so ax, ay, az are stuck at 0, so dsp.tilt always gets an angle of 0
   - b) Forgot to fill in raise KeyboardInterrupt
   - c) TILT_LIMIT is set too high
   - d) The screen is broken

   <details><summary>Solution</summary>

   **a** — the placeholder line `ax = ay = az = ... = 0` lets the program run, but with zero values — a clue while debugging that the sensor-reading blank is still empty.

   </details>

3. Pressing "< back" doesn't end the program; it keeps looping forever. Which blank is still empty? *(single choice · objective 2)*
   - a) Blank 1
   - b) Blank 2
   - c) Blank 3
   - d) Blank 4, raise KeyboardInterrupt inside ui.poll

   <details><summary>Solution</summary>

   **d** — without raising inside the ui.poll loop, the program sees the button's event but does nothing about it, so it just keeps looping.

   </details>

4. You want the same app to show whether someone is in front of the board instead of the tilt angle. What's the main thing to change? *(single choice · objective 3)*
   - a) Rewrite the whole file's skeleton
   - b) Change the read slot to sensors.radar() and the compute slot to bool(r["presence"]); leave poll and the back button as they are
   - c) Only change TILT_LIMIT
   - d) Remove ui.poll entirely

   <details><summary>Solution</summary>

   **b** — the three-app comparison table is the remix map: swapping the read and compute slots gives you a whole new app; the rest of the skeleton doesn't need touching.

   </details>

## Lab

**The MVP for lessons 1.4–1.5:** a remix that genuinely differs from the originals, with every part explained by which beat it belongs to.

- [ ] All four blanks in the practice file are filled in, running on the emulator or the board with the needle, the dominant angle, and the status label all working.
- [ ] Make at least one remix that differs from `01`/`02`/`04`, and note in your learning log what you changed and why.
- [ ] Try break-and-fix: move a widget's creation into the loop, observe the symptom, then move it back.
- [ ] Be able to point out which line in your file belongs to import, create-once, loop, or poll.

## Going further

In the next pair of lessons (1.6–1.7), we'll take the edge AI app apart the same way, then remix it to switch models and trigger an action on a matching class.

Next lesson: [lesson 1.6 — Taking apart the edge AI app: the model registry, verdicts and actions](../l06-edge-ai-app-anatomy/README.md)

## Reflect

- Which slots of the four-beat skeleton did your remix actually change? What does the part you never touched tell you about this program's design?
- When you moved the widget into the loop, what symptom did you see, and what do you think would happen if you left it that way for a long time?
