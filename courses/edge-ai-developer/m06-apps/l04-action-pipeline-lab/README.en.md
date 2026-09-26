---
id: edgeai-dev.m06.l04
lang: en
title: {th: 'ลงมือทำ: action pipeline ที่กัน false positive', en: 'Hands-on: an action pipeline that resists false positives'}
summary: {th: เติมสี่ด่านของท่อใน s16_action_pipeline.py คือ อ่านผล กรอง debounce+cooldown และยิง action จนไฟบนจอไล่ฟ้า เหลือง แดง พร้อมเสียงและ log เมื่อคลาสเป้าหมายค้างนานพอ แล้วจูน NEED_HITS กับ COOLDOWN_MS และพิสูจน์ว่าท่อปฏิเสธสัญญาณปลอมได้จริง, en: 'Fill the four pipeline stages in s16_action_pipeline.py (read, filter, debounce plus cooldown, fire) until the on-screen light goes cyan, amber, red with a sound and a log line when the target class lasts long enough, then tune NEED_HITS and COOLDOWN_MS and prove the pipeline really rejects fake signals.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l03]
objectives:
  - {th: เติมสี่จุดใน practice/s16_action_pipeline.py จนการเจอคลาสเป้าหมายต่อเนื่องครบ NEED_HITS ยิงไฟแดง เสียง และ log หนึ่งบรรทัด ส่วนสัญญาณเฟรมเดียวไม่ยิง, en: 'Fill the four points in practice/s16_action_pipeline.py so that the target class held for NEED_HITS frames fires the red light, a sound and one log line, while a one-frame signal does not.'}
  - {th: 'จูน NEED_HITS อย่างน้อยสามค่า (เช่น 1, 3, 6) บันทึกจำนวน false positive และ false negative ของแต่ละค่า แล้วเลือกค่าให้งานที่กำหนดพร้อมเหตุผล', en: 'Tune NEED_HITS to at least three values (for example 1, 3, 6), record the false positives and false negatives of each, and pick a value for a given job with reasons.'}
  - {th: ชี้ได้ว่าสัญญาณปลอมที่คุณสร้างถูกด่านใดกันไว้ และอธิบายว่าถ้าลืม last_fire = now จะเกิดอะไร, en: 'Point to the stage that blocked the fake signal you made, and explain what happens if last_fire = now is forgotten.'}
develops: [{skill: ai.edge, to: 3}, {skill: prog.state-machines, to: 2}, {skill: lang.micropython, to: 2}]
assesses: [{skill: ai.edge, level: 3, evidence: practice/s16_action_pipeline.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: c220d96407988627da9248035c939f7f014d7a9ad5d60947babc8997bd44a130
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.4 — Hands-on: an action pipeline that resists false positives

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the four pipeline stages in s16_action_pipeline.py — read the result, filter, debounce plus cooldown, and fire the action — until the light on screen goes blue, yellow, red, with a sound and a log line, once the target class has held long enough. Then tune NEED_HITS and COOLDOWN_MS, and prove the pipeline genuinely rejects fake signals.

## Objectives

By the end of this lesson, you will:

1. Fill the four points in practice/s16_action_pipeline.py so that the target class held continuously for NEED_HITS fires the red light, a sound, and one log line, while a single-frame signal doesn't fire.
2. Tune NEED_HITS to at least three values (for example, 1, 3, 6), record the false positives and false negatives of each, and choose a value for a given job with reasons.
3. Point to which stage blocked a fake signal you created, and explain what happens if last_fire = now is forgotten.

## Before you start

You've been through lesson 6.3, and understand the four-stage pipeline, EMA, and firing on the rising edge. Keep your learning log ready to record a NEED_HITS tuning table.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, set MODEL_KEYWORD = "Motion" and TARGET_CLASS = "shaking", then hold the Shake button to practise the pipeline. Real coughing needs the board.
- **Prior lesson:** [lesson 6.3 — The action pipeline: CONF_FLOOR, debounce, cooldown and on_result](../l03-action-pipeline/README.md)

## Concepts

The whole file reads as one sentence: select a model → loop reading results → does this frame hit the target? → has debounce and cooldown both been satisfied? → fire the action. The practice file already prepares the light-card widget, `fire_action()` and `set_light()`. Four points remain, following the flow: (1) `r = edge_ai.result()` — leave it empty, and the screen never shows a class, and the pipeline never runs (2) `hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)` — leave it empty, and streak never moves (3) `should_fire = ready and cooled`, where `ready = streak >= NEED_HITS` and `cooled` comes from the already-prepared `ticks_diff`, and (4) `fire_action(r['conf']); last_fire = now; streak = 0` — triggering the action, resetting the cooldown clock, and clearing the counter. Forget `last_fire = now`, and cooldown never restarts, so the pipeline fires repeatedly while the event holds.

The engineering heart of this is tuning — there's no single correct value. A high `NEED_HITS` gives fewer false alerts but misses brief events. A high `CONF_FLOOR` only trusts very confident results. A long `COOLDOWN_MS` avoids repeated disturbance, but two real events back to back get seen as one. Measure the result by counting false positives (firing when there's no event) against false negatives (an event happens but nothing fires), then ask which kind of mistake is more costly for this job. Success isn't just a light turning on — you must show that the pipeline **rejects** a fake signal.

## Worked example

`s16_action_pipeline_full.py` adds `dsp.EMA` smoothing at `EMA_ALPHA = 0.35`, a four-state light, `on_result` that logs only on a class change, and a `blocked` counter that counts how many times cooldown stopped a repeated firing. Try coughing or shaking for a long time and watch `blocked` increase.

| File | What this file teaches |
|---|---|
| [examples/s16_action_pipeline_full.py](examples/s16_action_pipeline_full.py) | A full action pipeline: filter + smooth + debounce + action (full version) |

## Practice

The `# TODO:` comments are at lines 120 (reading the result), 134 (filter), 152 (debounce + cooldown), and 157 (firing the action). If a single brief cough fires it, stage 2 or 3 isn't working yet. If holding a shake fires repeatedly, check `last_fire = now` at point 157.

| Practice file | Topic |
|---|---|
| [practice/s16_action_pipeline.py](practice/s16_action_pipeline.py) | From a verdict to a real action: RGB + sound + a log (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s16_action_pipeline.py](solution/s16_action_pipeline.py) | [practice/s16_action_pipeline.py](practice/s16_action_pipeline.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. The light stays blue forever, even while shaking is held a long time, and streak never moves at all. Which point is still empty? *(single choice · objective 1)*
   - a) Point 2, hit is still False
   - b) Point 4
   - c) Point 3
   - d) Nothing is wrong

   <details><summary>Solution</summary>

   **a** — streak only increases when hit is true. If hit is still stuck at its starting value False, the pipeline resets every frame.

   </details>

2. The light turns yellow at 1/3 and 2/3 as you shake, but never red, with no sound or log. Which point is still empty? *(single choice · objective 1)*
   - a) Point 1
   - b) Point 2
   - c) Point 3 or 4 (should_fire is still False, or fire_action is never called)
   - d) COOLDOWN_MS is zero

   <details><summary>Solution</summary>

   **c** — streak moving means stages 1 and 2 are working. The end of the pipeline that never fires is the should_fire condition, or the fire_action call.

   </details>

3. NEED_HITS = 1. What would the test results likely look like? *(single choice · objective 2)*
   - a) It never fires
   - b) The fastest to respond, but with the most false positives, since even a single frame passing the filter stage fires it
   - c) It misses real events the most often
   - d) Same as NEED_HITS = 6

   <details><summary>Solution</summary>

   **b** — debouncing at 1 frame is the same as having no debounce at all. A high value like 6, on the other hand, misses real brief events more often.

   </details>

4. You forget last_fire = now at point 4, then hold a shake for a long time. What happens? *(single choice · objective 3)*
   - a) It fires once, normally
   - b) Cooldown never restarts, and the pipeline fires again every time streak completes
   - c) It never fires at all
   - d) The program errors out

   <details><summary>Solution</summary>

   **b** — cooled stays true forever, since last_fire never changes, so the cooldown stage has no effect.

   </details>

## Lab

**The MVP for lessons 6.3–6.4:** a debounced action pipeline where the target class held continuously triggers a real action, while a brief flicker of the signal is guarded against.

- [ ] All four points in the practice file are filled in. Practise on the emulator with Motion and the Shake button, then try it with real coughing on the board.
- [ ] Tune `NEED_HITS` = 1, 3, 6. Run the same test ten times per value, and record a table of false positives and false negatives in your learning log.
- [ ] Create a signal that should be blocked (a brief tap of Shake, or a single cough), confirm it doesn't fire, and say which stage blocked it.
- [ ] Choose a value for two jobs (a fire alert versus a burglar alert), with reasons.

## Going further

In the next pair of lessons (6.5–6.6), we'll combine a verdict with a raw sensor (sensor fusion), then send an event out over the network with WiFi and MQTT.

Next lesson: [lesson 6.5 — Sensor fusion: a model's verdict with a raw sensor](../l05-sensor-fusion/README.md)

## Reflect

- How do the values you'd choose for a burglar alert differ from a fire alert, and how would you explain that to a customer?
- If your log only ever showed ALERT, with no record of blocked firings, how would you know the guard is actually working?
