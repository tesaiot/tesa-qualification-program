---
id: edgeai-dev.m08.l02
lang: en
title: {th: 'ลงมือทำ: สร้างและส่งมอบแอป Edge AI', en: 'Hands-on: build and ship an edge AI app'}
summary: {th: 'เติมห้าบรรทัดสันหลังของ s20_capstone.py คือ select, อ่านความเร่งดิบ, result, กรองความมั่นใจด้วย EMA และ fire_alert แล้วออกแบบ จูน และเดโม Guardian ของเราเอง พิสูจน์ด้วยหลักฐานว่าเหตุการณ์จริงทำให้เตือนครั้งเดียว ส่วนเคสหลอกไม่ทำให้เตือน และเล่าเหตุผลของค่าออกแบบที่เลือก', en: 'Fill the five backbone lines of s20_capstone.py (select, raw acceleration, result, EMA-filtered confidence and fire_alert), then design, tune and demo your own Guardian - proving with evidence that a real event alerts once while decoys do not, and explaining the design values you chose.'}
level: L3
time_min: {concept: 15, practise: 45, lab: 90, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m08.l01]
objectives:
  - {th: เติมห้าจุดใน practice/s20_capstone.py จน Guardian แสดงบริบท motion กับ verdict ที่กรองแล้ว และเตือน (เสียง แบนเนอร์ ตัวนับ) ครั้งเดียวเมื่อคลาสเป้าหมายต่อเนื่องครบ HITS_NEEDED ผล, en: 'Fill the five points in practice/s20_capstone.py until the Guardian shows the motion context and a filtered verdict, and alerts once (sound, banner, counter) when the target class lasts HITS_NEEDED results.'}
  - {th: 'ออกแบบ Guardian ของคุณ (โมเดล action และค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA) และบันทึกเหตุผลพร้อมหลักฐานที่วัดได้ คือจำนวนการเตือนจากเหตุการณ์จริงกับจากเคสหลอกอย่างละอย่างน้อยห้าครั้ง', en: 'Design your Guardian (model, action, CONF_FLOOR, HITS_NEEDED, EMA_ALPHA) and record the reasons with measured evidence - the alerts from real events and from decoys, at least five trials each.'}
  - {th: เดโมสองนาทีที่แสดงการเตือนจริง เคสหลอกที่ไม่เตือน และการแลกเปลี่ยนที่เลือก พร้อมเสนอทิศต่อยอดหนึ่งทิศ, en: 'Give a two-minute demo showing a real alert, a decoy that does not alert and the trade-off you chose, and propose one extension direction.'}
develops: [{skill: ai.edge, to: 3}, {skill: biz.product-decision, to: 2}, {skill: soft.communication, to: 2}]
assesses: [{skill: ai.edge, level: 3, evidence: practice/s20_capstone.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 3f5e9d18d4fb65daff735f37cac1cc5ae657e93357efbd926c59ab979e9f3db0
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 8.2 — Hands-on: build and ship an Edge AI app

> Module 8 — Capstone: your own Edge AI app · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the five backbone lines of s20_capstone.py — select, reading raw acceleration, result, EMA-filtered confidence, and fire_alert — then design, tune, and demo your own Guardian, proving with evidence that a real event alerts once while a decoy doesn't, and explaining the reasoning behind the design values you chose.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s20_capstone.py until the Guardian shows the motion context and a filtered verdict, and alerts once (sound, banner, counter) when the target class holds for HITS_NEEDED results.
2. Design your own Guardian (model, action, and the values CONF_FLOOR, HITS_NEEDED, EMA_ALPHA), and record your reasoning with measured evidence — the number of alerts from real events versus from decoys, at least five trials each.
3. Give a two-minute demo showing a real alert, a decoy that doesn't alert, and the trade-off you chose, and propose one extension direction.

## Before you start

You've been through lesson 8.1, and have a draft of your Guardian and starting values with reasons. Prepare a decoy in advance, such as a single brief shake or a borderline sound, to prove the decision layer works.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — you can complete the whole capstone on the emulator with the Motion model and the Shake button. Watching for sound or radar needs the board.
- **Prior lesson:** [lesson 8.1 — Designing the capstone: Guardian, three pillars in one file](../l01-capstone-design/README.md)

## Concepts

The whole file reads as one sentence: select a model → read context and the verdict → filter it steady → once the threshold is met, act → clean up on exit. The design knobs sit at the top of the file (`MODEL_KEYWORD`, `HITS_NEEDED = 3`, `EMA_ALPHA = 0.4`, `ACTION_NOTE = 72`). The five points to fill in are: (1) `edge_ai.select(model['index'])` when Load is pressed, inside a `try`, showing RUNNING only after select succeeds (2) `ax, ay, az = sensors.bmi270.acceleration()` — forget this, and motion stays stuck at 0.0 (3) `r = edge_ai.result()` — forget this, and the card never moves (4) `conf_s = conf_ema.update(r['conf'])` — forget this, and the status colour flickers with every peak, and (5) `fire_alert(r['label'], conf_s)` when `streak >= HITS_NEEDED and not fired` — forget this, and the threshold is met, but Guardian stays silent.

Filling it in isn't the capstone yet. The fifth step the solution doesn't hand you is your own design: choose a model and an action, set the design values, then measure real results — run the real event and the decoy several times each, count how many alerts each produces, then tune and record how the values change the result, so your design's explanation stands on numbers, not on a feeling. Deliver it with a short demo showing both a real alert and a non-alert. There are four extension directions: plugging in a self-trained model from module 5, adding FFT-derived features from module 4, fusing with a raw sensor or radar as in lesson 6.5, and sending events to MQTT as in lesson 6.6.

## Worked example

`s20_capstone_full.py` is the polished version of Guardian — selects a model live from a dropdown, shows latency, resets the filter when starting a fresh watch cycle, and counts the number of alerts.

| File | What this file teaches |
|---|---|
| [examples/s20_capstone_full.py](examples/s20_capstone_full.py) | Capstone: Edge AI Guardian (full version) |

This lesson's slides also reference a file in another lesson or in `shared/`:

- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.

## Practice

The `# TODO:` comments are at lines 127 (`select`), 152 (raw acceleration), 159 (`result`), 166 (`conf_ema.update`), and 194 (`fire_alert`). If it shows RUNNING but the card never moves, check points 127 and 159. If the status colour flickers every frame, check point 166.

| Practice file | Topic |
|---|---|
| [practice/s20_capstone.py](practice/s20_capstone.py) | Capstone: Edge AI Guardian (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s20_capstone.py](solution/s20_capstone.py) | [practice/s20_capstone.py](practice/s20_capstone.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Guardian shows RUNNING, but the result card never moves at all, while motion moves with the shaking. Which point is still empty? *(single choice · objective 1)*
   - a) Point 2, reading acceleration
   - b) Point 3, r = edge_ai.result() (or point 1, select)
   - c) Point 4, EMA
   - d) Point 5, fire_alert

   <details><summary>Solution</summary>

   **b** — motion moving means the DAQ pillar is working. The result card needs both the model correctly selected and result read in the loop.

   </details>

2. You hold a shake past the threshold, and the banner shows up waiting to trigger the whole time, but there's no sound or counter increase. Which point is still empty? *(single choice · objective 1)*
   - a) Point 5, fire_alert(r["label"], conf_s)
   - b) Point 2
   - c) Point 1
   - d) Nothing is wrong

   <details><summary>Solution</summary>

   **a** — all three gates have passed, but the fire_alert action is never called. That's the end of the pipeline that makes the sound, the banner, and the count.

   </details>

3. What's the best evidence for explaining why you chose HITS_NEEDED = 4? *(single choice · objective 2)*
   - a) "It felt about right"
   - b) A results table: at 4, real events alert 5/5 with decoys alerting 0/5, while at 2, decoys alert 3/5
   - c) The same value your friend used
   - d) The largest value you can enter

   <details><summary>Solution</summary>

   **b** — engineering decisions must stand on measurement. The count of alerts from real events versus decoys is the evidence for the trade-off.

   </details>

4. What should a good capstone demo show, besides an alert that works? *(single choice · objective 3)*
   - a) The whole file's code on screen
   - b) A decoy that Guardian doesn't alert on, and the reasoning behind the trade-off chosen
   - c) The number of lines of code
   - d) Nothing more is needed

   <details><summary>Solution</summary>

   **b** — the hard, valuable part is rejecting a fake signal, and explaining why these values were chosen. That's the difference between a product and a demo.

   </details>

## Lab

**The MVP for lessons 8.1–8.2:** deliver a Guardian with at least three working pillars (DAQ, Processing, Apps), watching for a target event, passing through a decision layer (a filtered conf with debounce), with an action that genuinely fires — and be able to explain the design.

- [ ] All five points in the practice file are filled in. Run it on the emulator or the board until you see a real alert.
- [ ] Design your own Guardian, set the design values, then test the real event and the decoy at least five times each, and note the results in your learning log.
- [ ] Try at least two sets of design values, and choose the one you'll use with reasons from the numbers.
- [ ] Record or perform a two-minute demo: a real alert, a decoy that doesn't alert, and the trade-off chosen, closing with one research question or extension direction.

## Going further

The course is now complete. Extend it in any of the four directions in this lesson, or go back to module 5 to train your own model and plug it into Guardian.

This is the course's last lesson. Return to the [course page](../../README.md) to see where to go next.

## Reflect

- How far did the design values you chose end up from the starting values, and which number changed your mind?
- If you had to ship this Guardian for a customer to actually use, what would still be missing the most?
