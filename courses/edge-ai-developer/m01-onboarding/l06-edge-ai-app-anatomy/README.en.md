---
id: edgeai-dev.m01.l06
lang: en
title: {th: 'แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action', en: 'Taking an edge AI app apart: the registry, the verdict and the action'}
summary: {th: แกะแอป Edge AI ที่โฟกัสโมเดลเดียวเป็นสามจังหวะ select → result → action เลือกโมเดลจากชื่อแทนเลข เข้าใจที่มาของ conf จาก softmax และ argmax แล้วเพิ่ม action ที่ยิงครั้งเดียวเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ, en: 'Take a single-model edge AI app apart into select → result → action, pick the model by name instead of number, see where conf comes from (softmax and argmax), and add an action that fires once when a confident target class appears.'}
level: L3
time_min: {concept: 40, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l05]
objectives:
  - {th: เขียน find_model() ที่ค้นโมเดลจากคำในชื่อผ่าน edge_ai.models() แล้วส่ง index ของ dict ที่ได้ไปให้ select() และอธิบายว่าทำไมทนกว่าการ select ด้วยเลขตายตัว, en: 'Write find_model() to look a model up by a word in its name via edge_ai.models(), pass the returned dict''s index to select(), and explain why this is sturdier than selecting a fixed number.'}
  - {th: คำนวณ softmax ของคะแนนดิบชุดเล็ก ๆ และบอกได้ว่า label มาจาก argmax ส่วน conf มาจาก max ของ scores ชุดเดียวกัน, en: Compute the softmax of a small set of raw scores and state that label comes from the argmax and conf from the max of the same scores.}
  - {th: เขียนเงื่อนไข action ที่ต้องผ่านทั้ง label ตรงเป้าหมายและ conf ≥ CONF_FLOOR พร้อมธง fired ที่ทำให้ action ยิงครั้งเดียวต่อการเจอ (edge-trigger), en: 'Write an action condition that needs both the target label and conf ≥ CONF_FLOOR, with a fired flag so the action fires once per detection (edge-triggered).'}
  - {th: เปรียบเทียบการ poll ด้วย result() กับ on_result(cb) ได้ว่าใครเป็นผู้ขับ ต้องเช็ก seq หรือไม่ และเหมาะกับงานแบบไหน, en: 'Compare polling with result() against on_result(cb) by who drives, whether seq must be checked, and what each suits.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: prog.state-machines, to: 1}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 5a32862350afc74752e72d8b54a79016bd3dd9856b77ccb0aa08455ee3b22d43
---

# Lesson 1.6 — Taking an edge AI app apart: the registry, the verdict and the action

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Take a single-model edge AI app apart into three beats — select → result → action — pick a model by name instead of number, see where conf comes from (softmax and argmax), and add an action that fires once when a confident target class appears.

## Objectives

By the end of this lesson, you will:

1. Write find_model() to look a model up by a word in its name via edge_ai.models(), pass the returned dict's index to select(), and explain why this is sturdier than selecting a fixed number.
2. Compute the softmax of a small set of raw scores, and state that label comes from the argmax and conf from the max of the same scores.
3. Write an action condition that needs both the target label and conf ≥ CONF_FLOOR, with a fired flag so the action fires once per detection (edge-triggered).
4. Compare polling with result() against on_result(cb) — who drives it, whether seq must be checked, and what each suits.

## Before you start

You've been through lessons 1.1–1.5, and remember the four calls models, select, result, stop and the four-beat skeleton. Open `13_edge_ai_motion.py` in BENTO IDE, and if you can, open `12_edge_ai_menu.py` to compare.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the emulator has no Push Detection, and model scores are simulated.
- **Prior lesson:** [lesson 1.5 — Hands-on: remix it into your own Tilt Monitor](../l05-sensor-remix-lab/README.md)

## See it work first

Run `13_edge_ai_motion.py` before touching any code, then shake the board, draw circles, or hold it still — the winning class, the score bars, and the latency all update live. This app is the single-model twin of the `12_edge_ai_menu.py` menu — try running them side by side, and notice how "one model" differs from "a menu."

## Concepts

A single-model edge AI app reads as **three beats**: (1) **select** — pick a model from the registry; (2) **result** — read the verdict and draw the screen; (3) **action** — act when the verdict matches a condition. Lessons 1.1–1.3 stopped at beat 2; this lesson adds beat 3, which is what makes edge AI "actually useful." Most real work never lets the user choose a model themselves — a fall-detection clock runs one model continuously and acts the moment it finds something.

The registry from `edge_ai.models()` is the app's source of truth. Instead of `select(0)` with a number that might shift when the firmware changes, we write `find_model(keyword)`, which searches by name and returns the whole dict — giving both the `index` to pass to select, and `labels` to set the target class. Change one keyword, and you've remixed the app for a different model.

`scores` comes from **softmax**, which squeezes raw scores (logits) $z_i$ into probabilities that add up to 1: $\text{softmax}(z)_i = e^{z_i} / \sum_j e^{z_j}$. From there, `label` is the **argmax** (the position of the highest score), and `conf` is the **max** (the highest score's value). For example, scores = [0.03, 0.05, 0.92] gives label = shaking and conf = 0.92. `CONF_FLOOR` has meaning precisely because the scores have already been normalized.

An action must fire when it's **both the target class and confident enough** (`r['conf'] >= edge_ai.CONF_FLOOR`), and fire **once per detection** with a `fired` flag (edge-triggered) — not every frame while the class keeps matching (level-triggered). Keeping "the decision" (the `hit` condition) separate from "the act" (`fire_action()`, which beeps with `ui.tone` and shows a banner) lets you remix the action without touching the detection logic. The other approach is `edge_ai.on_result(cb)`, which has the firmware call our function whenever there's a verdict (immediately on a class change, and repeating the same class roughly once a second), so you don't have to check `seq` yourself — though on the BENTO Emulator, the callback only fires when the program itself calls `edge_ai.result()` or `edge_ai.active()`.

## Worked example

`11_edge_ai_motion.py` does the same job as `13`, but uses the older module (deepcraft), which only gives the winning class. `13` uses `edge_ai`, so it also gets every class's score and the latency. Open both files side by side to see what the model registry adds.

| File | What this file teaches |
|---|---|
| [examples/11_edge_ai_motion.py](examples/11_edge_ai_motion.py) | Edge AI: an AI model classifying motion (runs on the board, no network needed) |
| [examples/13_edge_ai_motion.py](examples/13_edge_ai_motion.py) | Edge AI: Motion (IMU) with the new edge_ai API — seeing every class's score plus latency |

This lesson's slides also reference files in other lessons:

- [m01-onboarding/l02-edge-ai-module/examples/12_edge_ai_menu.py](../l02-edge-ai-module/examples/12_edge_ai_menu.py) — Edge AI Menu: select and run any AI model in one firmware image (no network needed)
- [m01-onboarding/l03-first-inference-lab/solution/s01_first_inference.py](../l03-first-inference-lab/solution/s01_first_inference.py) — running our first edge AI model
- [m01-onboarding/l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py](../l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py) — watching for a class with on_result, then acting (full version)
- [m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py](../l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) — taking an edge AI app apart, then remixing it: swap the model, act on a class (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Why is find_model("Motion") better than edge_ai.select(0) in an app meant to work across several boards? *(single choice · objective 1)*
   - a) Because select() can't accept a number
   - b) Because model order can differ by firmware or board — searching by name always gets the model you want, and also hands you its labels to use
   - c) Because find_model() runs faster on the NPU
   - d) Because model names never change, but the index changes on every boot

   <details><summary>Solution</summary>

   **b** — on the Dev Kit, Cough sits at 3, but on the emulator it's at 2, since there's no Push. Querying the registry by name makes the code resilient to this difference.

   </details>

2. Raw scores z = [0, 0, 0] for three classes, run through softmax. What do you get? *(single choice · objective 2)*
   - a) [0, 0, 0]
   - b) [1, 1, 1]
   - c) roughly [0.33, 0.33, 0.33], so conf is below CONF_FLOOR
   - d) [1, 0, 0]

   <details><summary>Solution</summary>

   **c** — e⁰ = 1 for every class, divided by a total of 3 gives about 0.33 for each, all equal. argmax still picks one winner, but a conf of 0.33 is below 0.50, so it shouldn't be trusted.

   </details>

3. scores = [0.10, 0.70, 0.20] for labels ['idle', 'circle', 'shaking']. What are top, label and conf? *(single choice · objective 2)*
   - a) top = 1, label = circle, conf = 0.70
   - b) top = 0.70, label = circle, conf = 1
   - c) top = 2, label = shaking, conf = 0.20
   - d) top = 1, label = idle, conf = 0.10

   <details><summary>Solution</summary>

   **a** — argmax gives position 1 (top), matching the name circle; max gives the value 0.70, which is conf.

   </details>

4. You shake the board continuously for three seconds and the model answers shaking every frame. With no fired flag, what happens? *(single choice · objective 3)*
   - a) The action still fires only once, same as before
   - b) The action fires every frame it's still detected, beeping repeatedly and annoyingly (level-triggered)
   - c) The action never fires at all
   - d) The model stops working

   <details><summary>Solution</summary>

   **b** — the fired flag makes it fire once on the rising edge, then resets once you leave the target class. This is the same kind of edge-trigger as one button press giving exactly one event.

   </details>

5. Which of these are true about on_result(cb) compared with polling using result()? (select every correct answer) *(multiple choice · objective 4)*
   - a) The firmware calls cb for us, so we never have to check seq ourselves
   - b) cb fires immediately when the class changes, and can also be called repeatedly with the same class roughly once a second, so you still need a fired flag
   - c) Polling sees every beat inside one single loop, which suits early learning
   - d) on_result means you never need to call edge_ai.stop() at the end

   <details><summary>Solution</summary>

   **a, b, c** — both approaches are valid; they differ in who's asking. At the end, you still need to remove the callback with on_result(None) and always call stop().

   </details>

## Lab

- [ ] Run `13_edge_ai_motion.py` and note in your learning log which class and roughly what conf each motion gives.
- [ ] In the REPL, try `find_model("Cough")` and print the `index` and `labels` you get, comparing against your board or emulator.
- [ ] Compute the softmax of z = [2.0, 3.1, 1.2] with a calculator, and state which class wins and with what conf.

## Going further

In lesson 1.7, we'll fill in the `s03_anatomy_edgeai.py` file until the app beeps and shows a banner by itself when it finds the target class, then remix it into our own.

Next lesson: [lesson 1.7 — Hands-on: from a verdict to an action on the board](../l07-verdict-action-lab/README.md)

## Reflect

- At home or at work, what job "knows what it found" but that isn't enough — it also needs to "act on it"? Should that action fire once, or repeatedly?
- If your action was calling in an emergency, would you set CONF_FLOOR high or low, and why?
