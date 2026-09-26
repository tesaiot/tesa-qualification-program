---
id: edgeai-dev.m06.l03
lang: en
title: {th: 'ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result', en: 'The action pipeline: CONF_FLOOR, debounce, cooldown and on_result'}
summary: {th: 'เปลี่ยนการนับเป็นการสั่งการจริงอย่างมีวินัยด้วยท่อสี่ด่าน คือกรองด้วย CONF_FLOOR, debounce ที่ต้องจับต่อเนื่อง, cooldown ที่เว้นช่วงกันยิงรัว และ action ผ่านไฟ RGB เสียงและ log เสริมด้วย EMA smoothing คณิตของการยิงตอนขอบขึ้น และการเลือกระหว่าง poll กับ on_result', en: 'Turn counting into disciplined action with a four-stage pipeline - a CONF_FLOOR filter, a debounce that needs a streak, a cooldown against rapid re-firing, and the action itself through an RGB light, sound and a log - plus EMA smoothing, the maths of firing on the rising edge, and choosing between polling and on_result.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l02]
objectives:
  - {th: อธิบายท่อสี่ด่าน (กรอง → debounce → cooldown → action) และบอกได้ว่าแต่ละด่านกัน false positive แบบใด, en: Describe the four-stage pipeline (filter → debounce → cooldown → action) and say which kind of false positive each stage stops.}
  - {th: 'คำนวณ EMA หนึ่งก้าวด้วยมือจาก y_t = αx_t + (1 − α)y_{t−1} และอธิบายว่าทำไมมันกดยอดแหลมเดี่ยวได้โดยเก็บสถานะแค่ค่าเดียว', en: 'Compute one EMA step by hand from y_t = αx_t + (1 − α)y_{t−1}, and explain why it flattens single spikes while keeping only one state value.'}
  - {th: 'ใช้เงื่อนไขยิง fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] กับลำดับเฟรมที่กำหนด และอธิบายว่าทำไมต้องวัดเวลาด้วย ticks_diff', en: 'Apply the firing rule fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] to a given frame sequence, and explain why time must be measured with ticks_diff.'}
  - {th: เลือกระหว่าง poll ด้วย result() กับ callback ด้วย on_result() ให้งานที่กำหนด โดยรู้ว่า callback มาเมื่อคลาสเปลี่ยนและทวนคลาสเดิมราววินาทีละครั้ง, en: 'Choose between polling result() and an on_result() callback for a given task, knowing the callback arrives on a class change and repeats the same class about once a second.'}
develops: [{skill: ai.edge, to: 3}, {skill: sys.dsp, to: 2}, {skill: prog.state-machines, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: fc9064ce622270b2f6f4fe8ce593e4a6ff9d74925e6b958d32df1bfc87076fa5
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.3 — The action pipeline: CONF_FLOOR, debounce, cooldown and on_result

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Turn counting into disciplined, real action with a four-stage pipeline: a CONF_FLOOR filter, a debounce needing a streak, a cooldown against rapid re-firing, and the action itself through an RGB light, sound and a log — plus EMA smoothing, the maths of firing on the rising edge, and choosing between polling and on_result.

## Objectives

By the end of this lesson, you will:

1. Describe the four-stage pipeline (filter → debounce → cooldown → action), and say which kind of false positive each stage stops.
2. Compute one EMA step by hand from y_t = αx_t + (1 − α)y_{t−1}, and explain why it flattens a single spike while keeping only one value of state.
3. Apply the firing rule fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] to a given frame sequence, and explain why time must be measured with ticks_diff.
4. Choose between polling with result() and a callback with on_result() for a given task, knowing the callback arrives on a class change and repeats the same class about once a second.

## Before you start

You've been through lessons 6.1–6.2, and have a counting app using CONF_FLOOR and rising-edge counting, and remember `dsp.EMA` from lesson 4.1. Open the `20_confirmed_alert.py` example in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, use the Motion model with the Shake button to practise the whole pipeline (the audio models on the emulator are simulated values where the event class never wins), and the on_result callback fires when the program calls result() or active().
- **Prior lesson:** [lesson 6.2 — Hands-on: your own focused app](../l02-focused-app-lab/README.md)

## See it work first

Run `s16_action_pipeline_full.py` (in lesson 6.4), select the Cough model, and try coughing. The light on screen moves from blue (watching) to yellow (detected, but not sure yet) to red (firing). Notice that a single brief cough doesn't fire right away, then ask: how does it know which one is real?

## Concepts

A raw verdict can't be trusted whole — a model can always flicker past the threshold for a moment. If you fired on every frame where `label == "cough"`, you'd get so many false alerts that people would stop paying attention — the same problem as switch bounce on a button. So we build a **four-stage pipeline**: (1) **filter**: `hit = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR`, cutting out unsure answers (2) **debounce**: `streak += 1` on a hit, `streak = 0` the instant it drops — it must reach `NEED_HITS` to be ready, so a single spike can't get through because it doesn't hold (3) **cooldown**: `time.ticks_diff(now, last_fire) >= COOLDOWN_MS`, guarding against rapid re-firing while an event stays active a long time — always use `ticks_diff`, since the ms counter can wrap around (4) **action**, inside a separate `fire_action()`: a coloured card on screen standing in for an RGB light (blue, yellow, red), `ui.tone(note, wave, velocity, dur_ms)` or `ui.sfx(...)` wrapped in `hasattr`, and a log through `lcd.console` with the time and confidence.

An extra layer of protection is **EMA**, $y_t = \alpha x_t + (1-\alpha) y_{t-1}$, at $\alpha = 0.35$. If $y_{t-1} = 0.20$ and a spike $x_t = 0.90$ appears, you get $y_t = 0.445$ — still short of 0.50. It takes several genuinely high frames in a row to climb over the line, keeping just one value of state. Debounce counts frames, while smoothing flattens the value's size — used together, they're even tighter. This can be written as maths: $c_t = c_{t-1} + 1$ on a hit, $c_t = 0$ on a miss, then fire when $[c_t \ge H] \wedge [c_{t-1} < H] \wedge [t - t_{last} \ge T_{cool}]$ — firing the moment readiness is first reached, once per event, exactly like an edge-triggered interrupt.

There are two ways to receive results. **Polling** means calling `result()` yourself every round, getting every frame, so you can count a streak. **`edge_ai.on_result(cb)`** has the firmware call us the instant the winning class changes, and repeats the same class about once a second — suiting logging a class change (remember the last class and skip the repeated rounds), but not suiting debounce. A job that needs to count frames or time uses polling; a job that just reacts to an event uses the callback, always removed with `edge_ai.on_result(None)` at the end.

## Worked example

`19_motion_verdict_action.py` checks the label, confidence, and inference time together before triggering a sound (threshold `CONF = 0.70`). `20_confirmed_alert.py` confirms `CONFIRM_N = 4` consecutive rounds before trusting a result, then waits `ALERT_GAP_MS = 8000` before alerting again — the same pipeline, with a different set of numbers (both files were carried over from the author's AIoT course).

| File | What this file teaches |
|---|---|
| [examples/19_motion_verdict_action.py](examples/19_motion_verdict_action.py) | Gesture-triggered actions, and the cost of each decision |
| [examples/20_confirmed_alert.py](examples/20_confirmed_alert.py) | Treating a model as a source of values, then confirming before alerting |

This lesson's slides also reference files in another lesson:

- [m06-apps/l04-action-pipeline-lab/examples/s16_action_pipeline_full.py](../l04-action-pipeline-lab/examples/s16_action_pipeline_full.py) — a full action pipeline: filter + smooth + debounce + action (full version)
- [m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py](../l04-action-pipeline-lab/practice/s16_action_pipeline.py) — from a verdict to a real action: RGB + sound + a log (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. The cough class jumps above CONF_FLOOR for a single frame, then drops. Which stage stops it from firing? *(single choice · objective 1)*
   - a) The filter stage
   - b) The debounce stage, because streak never reaches NEED_HITS and resets to 0
   - c) The cooldown stage
   - d) The action stage

   <details><summary>Solution</summary>

   **b** — a spike high enough can pass the filter stage, but it doesn't hold continuously, so streak never completes. Cooldown, on the other hand, exists to stop rapid re-firing while a real event stays active a long time.

   </details>

2. EMA at α = 0.35, an existing y = 0.20, meets a new value x = 0.90. What's the new y? *(single choice · objective 2)*
   - a) 0.90
   - b) 0.55
   - c) 0.445
   - d) 0.315

   <details><summary>Solution</summary>

   **c** — 0.35 × 0.90 + 0.65 × 0.20 = 0.315 + 0.130 = 0.445. The spike gets flattened enough that it still hasn't crossed the 0.50 threshold.

   </details>

3. NEED_HITS = 3, and the cooldown has already passed. The frame sequence hit, hit, hit, hit, hit — how many times does it fire? *(single choice · objective 3)*
   - a) 0
   - b) 1 time, at the third frame
   - c) 3 times
   - d) 5 times

   <details><summary>Solution</summary>

   **b** — it fires the first time c_t reaches 3 (c_{t−1} = 2 < 3). By the next frame, c_{t−1} already meets it, so it doesn't fire again — and cooldown starts counting fresh too.

   </details>

4. Why use time.ticks_diff(now, last_fire) instead of now − last_fire? *(single choice · objective 3)*
   - a) It's faster
   - b) The ticks_ms counter can wrap around; ticks_diff handles the wrap so the difference stays correct
   - c) It gives a result in seconds
   - d) There's no difference

   <details><summary>Solution</summary>

   **b** — once the counter fills up and wraps around, a plain subtraction gives a negative or wrong value. ticks_diff is designed exactly for this case.

   </details>

5. Which task best suits edge_ai.on_result(cb)? *(single choice · objective 4)*
   - a) Counting a per-frame streak for debounce
   - b) Logging when the winning class changes, remembering the last class to skip rounds where the firmware repeats it
   - c) Measuring latency every frame
   - d) EMA smoothing every frame

   <details><summary>Solution</summary>

   **b** — the callback arrives on a class change and repeats about once a second, not every frame. A job that needs to count frames should use polling instead.

   </details>

## Lab

- [ ] Run `20_confirmed_alert.py` on the emulator with the Motion model, pressing Shake briefly versus holding it, and note when the confirmed status label changes.
- [ ] Continue the EMA calculation from the example for three more frames, with x = 0.90 held steady, and see which frame crosses 0.50.
- [ ] Write a ten-frame hit/miss sequence with both a single spike and a real event, then mark the frame that fires when NEED_HITS = 3.

## Going further

In lesson 6.4, we'll fill in the four pipeline stages in `s16_action_pipeline.py`, then tune `NEED_HITS` and `COOLDOWN_MS` until it genuinely guards against false positives.

Next lesson: [lesson 6.4 — Hands-on: an action pipeline that guards against false positives](../l04-action-pipeline-lab/README.md)

## Reflect

- For what kind of work is missing a real event (a false negative) more costly than a false alert, and which way would you tune the pipeline?
- If you used on_result to do debounce instead of polling, what problem would that cause?
