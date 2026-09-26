---
id: edgeai-dev.m01.l07
lang: en
title: {th: 'ลงมือทำ: จาก verdict สู่ action บนบอร์ด', en: 'Hands-on: from verdict to action on the board'}
summary: {th: เติมสี่ช่องในไฟล์ s03_anatomy_edgeai.py จนแอปเฝ้าโมเดลเดียวบี๊บและขึ้นแบนเนอร์เองเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ แล้ว remix ให้สลับโมเดล เปลี่ยนคลาสเป้าหมาย และเปลี่ยน action โดยไม่แตะ logic ตรวจจับ, en: 'Fill the four blanks in s03_anatomy_edgeai.py until the single-model watcher beeps and shows a banner on its own when a confident target class appears, then remix the model, the target class and the action without touching the detection logic.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l06]
objectives:
  - {th: 'เติม practice/s03_anatomy_edgeai.py ครบสี่ช่อง (select, result, verdict.text, fire_action) จนทำท่าหรือส่งเสียงตรงคลาสเป้าหมายแล้วได้ยินบี๊บหนึ่งครั้งและเห็นแบนเนอร์ และเมื่อออกจากคลาสนั้นแบนเนอร์กลับเป็น "รอจับ ..."', en: 'Fill the four blanks of practice/s03_anatomy_edgeai.py (select, result, verdict.text, fire_action) so that performing the target class gives one beep and a banner, and leaving it turns the banner back to "waiting".'}
  - {th: remix แอปด้วยการเปลี่ยน MODEL_KEYWORD และ TARGET_CLASS เป็นโมเดลอื่นที่ใช้เซนเซอร์ต่างกัน โดยตั้งคลาสเป้าหมายจาก labels ที่อ่านได้จริง แล้วยืนยันว่า action ยิงตามคลาสใหม่, en: 'Remix the app by changing MODEL_KEYWORD and TARGET_CLASS to another model with a different sensor, setting the target from the labels actually reported, and confirm the action fires on the new class.'}
  - {th: หากรณีที่คลาสเป้าหมายชนะแต่ conf ต่ำกว่า CONF_FLOOR แล้วอธิบายได้ว่าทำไม action จึงไม่ยิง และธง fired ป้องกันอะไร, en: 'Find a case where the target class wins but conf is below CONF_FLOOR, and explain why the action does not fire and what the fired flag prevents.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: prog.state-machines, to: 2}]
assesses: [{skill: ai.edge, level: 2, evidence: practice/s03_anatomy_edgeai.py}, {skill: prog.state-machines, level: 2, evidence: practice/s03_anatomy_edgeai.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 72f2b2f4c19cc7026691b1353ed326c7bbfeefe9457a0dffb041d21b870ed3d7
---

# Lesson 1.7 — Hands-on: from verdict to action on the board

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the four blanks in the s03_anatomy_edgeai.py file until the single-model watcher beeps and shows a banner on its own when a confident target class appears, then remix the model, the target class and the action without touching the detection logic.

## Objectives

By the end of this lesson, you will:

1. Fill in all four blanks of practice/s03_anatomy_edgeai.py (select, result, verdict.text, fire_action) so that performing the target class or making the target sound gives one beep and a banner, and leaving that class turns the banner back to "waiting…".
2. Remix the app by changing MODEL_KEYWORD and TARGET_CLASS to another model using a different sensor, setting the target class from the labels actually reported, and confirm the action fires on the new class.
3. Find a case where the target class wins but conf is below CONF_FLOOR, and explain why the action doesn't fire, and what the fired flag prevents.

## Before you start

You've been through lesson 1.6, and understand the hit condition (a matching label and conf ≥ CONF_FLOOR) and the fired flag. If you don't remember the four calls from lesson 1.3 well, open the `s01_first_inference.py` solution to review first, since blanks 1–3 here are the same ones.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the full version uses on_result, and on the emulator the callback only fires when the program itself calls edge_ai.result() or edge_ai.active(), so it's best to try the full version on a board.
- **Prior lesson:** [lesson 1.6 — Taking an edge AI app apart: the registry, the verdict and the action](../l06-edge-ai-app-anatomy/README.md)

## Concepts

The whole file reads as one sentence: find the model by name → tell it to run → loop reading results onto the screen roughly every 180 ms → once a confident target class appears, act → stop on exit. Blanks 1–3 repeat what you already did in lesson 1.3 (`select(model['index'])` inside a `try`, `r = edge_ai.result()`, `verdict.text(...)`). Blank 4 is new: `fire_action(r['conf'])`, inside the condition `if hit and not fired:`. The left half of the loop (sensor → model) happens automatically on the CM55; the right half (result → screen → action) is entirely our own Python code on the CM33.

There are two layers to remix. The first sits in two lines at the top of the file: `MODEL_KEYWORD` swaps both the model and the sensor (IMU → MIC → RADAR), while `TARGET_CLASS` must spell exactly the same as a name in that model's `labels` (readable from the console line or from `edge_ai.models()`) — for instance, `"Cough"` pairs with `"cough"`. The second layer is `fire_action()`, editable in one place: change `ui.tone`'s note, use `ui.sfx(ui.SFX_UI_SELECT)`, beep at two levels depending on confidence, or count occurrences — none of which affects what the app detects.

At the end, the `finally` block always stops the engine. If you use `on_result` (as in the full version), you must remove the callback with `edge_ai.on_result(None)` before calling `stop()`. Success in this lesson isn't just seeing the banner — you should be able to say how this app differs from lesson 1.3, and what your remix changed.

## Worked example

`s03_anatomy_edgeai_full.py` moves to `on_result`, colours things using `CONF_FLOOR`, counts actions, and shows latency. Read it once your practice file is working, and notice the main loop now only handles buttons, because reading results has moved into the callback.

| File | What this file teaches |
|---|---|
| [examples/s03_anatomy_edgeai_full.py](examples/s03_anatomy_edgeai_full.py) | Watching for a class with on_result, then acting (full version) |

## Practice

Fill it in this order: 1) `edge_ai.select(model['index'])` after `find_model` 2) `r = edge_ai.result()` 3) `verdict.text(r['label'] or '-')` 4) `fire_action(r['conf'])` inside the hit condition. Choose `MODEL_KEYWORD`/`TARGET_CLASS` to try first (starting with Motion and shaking works well). If the screen stays stuck at `---`, blank 1 is still empty. If the class shows correctly but there's no sound or banner, blank 4 is still empty.

| Practice file | Topic |
|---|---|
| [practice/s03_anatomy_edgeai.py](practice/s03_anatomy_edgeai.py) | Taking an edge AI app apart, then remixing it: swap the model, act on a class (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s03_anatomy_edgeai.py](solution/s03_anatomy_edgeai.py) | [practice/s03_anatomy_edgeai.py](practice/s03_anatomy_edgeai.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You've filled in the whole file. The screen correctly shows the shaking class, but there's no beep and no banner at all. Which blank is still empty? *(single choice · objective 1)*
   - a) Blank 1, edge_ai.select(model['index'])
   - b) Blank 2, r = edge_ai.result()
   - c) Blank 4, fire_action(r['conf'])
   - d) None — it's because the emulator has no speaker

   <details><summary>Solution</summary>

   **c** — the class showing on screen means blanks 1–3 are working. Blank 4 is where a verdict becomes an action. If it's empty, the app "reports" but never "acts."

   </details>

2. You want to change the app into a cough detector. How should you set the two lines at the top of the file? *(single choice · objective 2)*
   - a) MODEL_KEYWORD = "Cough", TARGET_CLASS = "cough"
   - b) MODEL_KEYWORD = "cough", TARGET_CLASS = "Cough Detection"
   - c) MODEL_KEYWORD = "Motion", TARGET_CLASS = "cough"
   - d) MODEL_KEYWORD = 3, TARGET_CLASS = 1

   <details><summary>Solution</summary>

   **a** — find_model searches for a word in the name, case-insensitively, but TARGET_CLASS must match the model's labels exactly — for Cough Detection, those are unlabelled and cough.

   </details>

3. The result is {'label': 'shaking', 'conf': 0.42} and TARGET_CLASS = 'shaking'. What does the action do? *(single choice · objective 3)*
   - a) Fires right away, since the class matches
   - b) Doesn't fire, because hit also needs conf ≥ CONF_FLOOR (0.50), and fired gets reset to False
   - c) Fires twice
   - d) The program throws OSError

   <details><summary>Solution</summary>

   **b** — hit is False because conf hasn't reached the threshold, so the code takes the elif not hit branch, which resets fired and shows the "waiting" banner. This is what guards against a false positive.

   </details>

4. Put the sequence of events in order when a user shakes the board twice (shake, stop, shake), with the target set to shaking *(ordering · objective 3)*
   - a) hit is False, so fired resets to False
   - b) hit is True and fired is False, so the action fires and sets fired = True
   - c) hit is True again, fired is False, so the action fires a second time
   - d) hit is still True but fired is True, so it doesn't fire again

   <details><summary>Solution</summary>

   **b → d → a → c** — edge-triggered: it fires the moment the class is entered, doesn't fire again while still shaking, resets once you leave the class, and is ready to fire again once you enter it a second time.

   </details>

## Lab

**The MVP for lessons 1.6–1.7:** genuinely remix `s03_anatomy_edgeai.py` — swap the model (change `MODEL_KEYWORD` and `TARGET_CLASS`), and trigger an action when a matching verdict occurs.

- [ ] All four blanks in the practice file are filled in; performing the motion or sound gives one beep and shows the banner.
- [ ] Remix it to at least one other model (for example, Motion → Cough), and confirm the action fires on the new class.
- [ ] Find a motion or sound where the target class wins but conf is below CONF_FLOOR, and note in your learning log why the action doesn't fire.
- [ ] Be able to explain why both label and conf must be checked, and why the fired flag is needed.

## Going further

In the next module, we open pillar 1 (DAQ), starting to collect our own sensor data into CSV files as raw material for training models in module 5.

Next lesson: [lesson 2.1 — Sampling to match the model: Nyquist rate, windows and CSV schema](../../m02-daq/l01-sampling-and-schema/README.md)

## Reflect

- Should the action you chose in your remix fire once per detection, or repeatedly at intervals? If repeatedly, how would you design the flag or timer for that?
- If you had to bring this app to a model whose target class isn't in the same position, what parts of your code would need to change?
