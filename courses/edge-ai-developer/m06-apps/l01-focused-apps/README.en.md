---
id: edgeai-dev.m06.l01
lang: en
title: {th: 'หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว', en: 'Six models and the edge_ai API: an app focused on one model'}
summary: {th: เปิดโมดูลแอป จากเมนูที่ให้เลือกทุกโมเดลไปสู่แอปที่โฟกัสโมเดลเดียว เล็งโมเดลด้วย find_model() แทนเลข index อ่าน scores ทุกคลาสกับ latency_ms ให้เป็น และต่อ verdict เข้ากับ action แรกคือการนับเมื่อคลาสเป้าหมายมั่นใจถึง CONF_FLOOR เฉพาะจังหวะขอบขาขึ้น, en: 'Open the apps module - from a menu that offers every model to an app focused on one. Target the model with find_model() instead of an index, read every class score and latency_ms, and wire the verdict to a first action - counting when the target class reaches CONF_FLOOR, on the rising edge only.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l09]
objectives:
  - {th: เปรียบเทียบแอปเมนูกับแอปโฟกัสโมเดลเดียว และบอกได้ว่างานแบบใดควรใช้แบบใด, en: 'Compare a menu app with a single-model focused app, and say which kind of job suits each.'}
  - {th: อธิบาย find_model() ที่ถอยสามชั้น (ชื่อ → เซนเซอร์ → ตัวแรก) และเหตุผลที่ไม่ควร hard-code เลข index ของโมเดล, en: Explain find_model() with its three fallbacks (name → sensor → first) and why a model index should never be hard-coded.}
  - {th: 'อ่าน dict ของ edge_ai.result() ได้ครบ ทั้ง top ที่มาจาก argmax, conf ที่เป็นคะแนนสูงสุด, scores ทุกคลาส, latency_ms และ seq ที่ใช้วาดจอเฉพาะผลใหม่', en: 'Read an edge_ai.result() dict fully - top from argmax, conf as the highest score, every class score, latency_ms, and seq for redrawing only on new results.'}
  - {th: เขียนเงื่อนไขนับ label == TARGET_CLASS และ conf ≥ CONF_FLOOR (0.50) ที่นับเฉพาะขอบขาขึ้น และอธิบายขีดจำกัดของโมเดล Ready-Model แบบประเมินผล, en: 'Write the counting condition label == TARGET_CLASS and conf ≥ CONF_FLOOR (0.50) that counts on the rising edge only, and explain the limits of the evaluation Ready Models.'}
develops: [{skill: ai.edge, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 99e6b836e6e2b4e6945f03a2ad0981bb9378e2e08de5b10e25ebb278eab48152
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.1 — Six models and the edge_ai API: an app focused on one model

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Open the apps module. Go from a menu offering every model to an app focused on one. Target a model with find_model() instead of an index, learn to read every class's score and latency_ms, and wire a verdict to a first action — counting when the target class reaches CONF_FLOOR, on the rising edge only.

## Objectives

By the end of this lesson, you will:

1. Compare a menu app with a single-model focused app, and say which kind of job suits each.
2. Explain find_model() and its three fallbacks (name → sensor → first), and why a model's index should never be hard-coded.
3. Fully read an edge_ai.result() dict — top from argmax, conf as the highest score, every class's score, latency_ms, and seq, used to redraw only on a new result.
4. Write the counting condition label == TARGET_CLASS and conf ≥ CONF_FLOOR (0.50), counting on the rising edge only, and explain the limits of the evaluation Ready Models.

## Before you start

You've been through module 1, already used `edge_ai.models()`, `select()`, `result()` and `stop()`, and remember the verdict-to-action skeleton from lesson 1.6. Open the `16_edge_ai_sound_events.py` example in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, model scores are simulated: the audio models move with the POTEN knob, but the event class never wins over unlabelled, and there's no Push model. Real sound and radar need the board.
- **Prior lesson:** [lesson 5.9 — Hands-on: comparing three targets, MCU, web and PC](../../m05-training/l09-three-targets-lab/README.md)

## See it work first

Run `16_edge_ai_sound_events.py` on the board, and switch between Cough, Alarm and Siren in one single dropdown. Watch the two-class bars move when there's sound. Ask yourself: if this device had to count coughs in a patient's room all night long, should the user have to pick the model themselves?

## Concepts

A model-selection menu suits exploration and demos, but nearly every real product is a **focused app**: target a single model when the app opens, design a UI for exactly that job, and wire the verdict to an action. Examples 13 through 16 share the same shape: `find_model()` → `select()` → a `result()` loop → drawing the verdict and its bars → `finally: stop()`. The board has six models (Motion, Baby Cry, Push, Cough, Alarm, Siren), while the emulator has five, so the order differs. `find_model()` first searches by keyword in the name; failing that, it uses the first model matching a `sensor` (such as `edge_ai.SENSOR_MIC = 2`); and finally falls back to the first model, to keep the app from crashing. A fixed `select(3)` breaks the instant the registry changes.

The `result()` dict gives more than just the winning class: `top` is $\hat{y} = \arg\max_i s_i$, `conf` is $s_{\hat{y}}$, `scores` draws a bar for every class, showing whether the model is unsure or confident, `latency_ms` reports the NPU's inference time, which differs by model, and `seq` is used to redraw only when there's a new result. argmax always picks a winner, even at 0.51 versus 0.49, so we set a gate on the action: count when `r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR` (0.50), and count only on the **rising edge** (`is_target and not was_target`), because a single cough spans several inference results. Setting the threshold high gives certainty but misses quiet sounds; setting it low catches quickly but produces many false positives.

Cough, Alarm and Siren are DEEPCRAFT Ready Models from Imagimob AB (an Infineon group company), evaluation versions meant for experimentation only, with a limited number of inferences. If a result stays frozen and `seq` never moves, that's the model hitting its ceiling, not broken code — the author recommends rebooting the board. Once you can train your own model, as in module 5, this limitation disappears.

## Worked example

`14_edge_ai_babycry.py`: a result card with a confidence bar for the mic model. `15_edge_ai_radar_push.py`: the Push radar model (stand about 60 cm away; needs a board with radar). `16_edge_ai_sound_events.py`: a sub-menu of three audio models. `17_latency_min_max_avg.py`: collects latency over 20 rounds and reports the minimum, maximum, and average. And `18_switch_cost.py`: times how long switching models with `select()` takes, showing that switching frequently has a cost (the last two files were carried over from the author's AIoT course).

| File | What this file teaches |
|---|---|
| [examples/14_edge_ai_babycry.py](examples/14_edge_ai_babycry.py) | Edge AI: Baby Cry (microphone) — detecting a crying baby on the board (no network needed) |
| [examples/15_edge_ai_radar_push.py](examples/15_edge_ai_radar_push.py) | Edge AI: Radar Push (60 GHz radar) — classifying hand gestures with radar on the board |
| [examples/16_edge_ai_sound_events.py](examples/16_edge_ai_sound_events.py) | Edge AI: Sound Events (Cough / Alarm / Siren) — 3 mic models in one dropdown |
| [examples/17_latency_min_max_avg.py](examples/17_latency_min_max_avg.py) | Measuring how long a model takes to think |
| [examples/18_switch_cost.py](examples/18_switch_cost.py) | Switching models while the program is running |

This lesson's slides also reference files in another lesson:

- [m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py](../../m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) — Edge AI: Motion (IMU) with the new edge_ai API — seeing every class's score plus latency
- [m06-apps/l02-focused-app-lab/practice/s15_apps.py](../l02-focused-app-lab/practice/s15_apps.py) — an edge AI app that's "focused on one model" (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. A device counting coughs at a patient's bedside should be what kind of app? *(single choice · objective 1)*
   - a) A menu letting the user choose a model every time
   - b) A focused app that targets the Cough model from the start, wiring the verdict to a counter
   - c) An app that switches every model every second
   - d) No app needed — just use the REPL

   <details><summary>Solution</summary>

   **b** — an end user shouldn't need to know what models exist. Menus suit exploration and demos; focused apps suit real work.

   </details>

2. Why is find_model(("cough",), edge_ai.SENSOR_MIC) better than edge_ai.select(3)? *(single choice · objective 2)*
   - a) It's faster
   - b) It finds the model by name, so it's still correct even if the registry order changes, such as on the emulator, where the lack of Push puts Cough at index 2
   - c) It uses less memory
   - d) select(3) doesn't work on the board

   <details><summary>Solution</summary>

   **b** — on the board, Cough is at index 3, but on the emulator, it's at index 2. Querying the registry by name lets one set of code work in both places.

   </details>

3. r['scores'] = [0.12, 0.88] for a model with ['unlabelled', 'cough']. What are r['top'] and r['conf']? *(single choice · objective 3)*
   - a) top = 0, conf = 0.12
   - b) top = 1, conf = 0.88
   - c) top = 0.88, conf = 1
   - d) top = 1, conf = 0.12

   <details><summary>Solution</summary>

   **b** — top is the index of the highest score (argmax), and conf is that score's value. The winning class is therefore cough, with 0.88 confidence.

   </details>

4. One cough spans three inference results, giving cough's conf as 0.8, 0.9, 0.85, then dropping. How many times does a rising-edge counter increase? *(single choice · objective 4)*
   - a) 0
   - b) 1
   - c) 3
   - d) 2

   <details><summary>Solution</summary>

   **b** — it counts only the moment it changes from not-target to target. As long as it stays above the threshold, it isn't counted again, so one cough gives 1.

   </details>

5. The Cough app has been working well for a while, then the result freezes and seq stops moving. What's the most likely cause? *(single choice · objective 4)*
   - a) A memory leak in the code
   - b) The evaluation Ready Model hit its inference count ceiling
   - c) CONF_FLOOR is set wrong
   - d) The microphone is broken

   <details><summary>Solution</summary>

   **b** — an evaluation model limits the number of inferences. This is a property of the license, not a bug in the code. A model you trained yourself has no such limit.

   </details>

## Lab

- [ ] Run `17_latency_min_max_avg.py` with `TARGET = "motion"`, then change it to `"cough"`. Note the minimum, maximum, and average for both in your learning log.
- [ ] Write out `find_model()` by hand in your learning log, and explain why, on the emulator with no Push, `select(3)` gets a different model than on the board.
- [ ] Sketch a rough graph of cough's conf over time, and mark the points that should count under the rising-edge rule.

## Going further

In lesson 6.2, we'll fill in `s15_apps.py` to make a cough-counting app, then retarget it to Alarm or Siren by changing just two lines at the top of the file.

Next lesson: [lesson 6.2 — Hands-on: our own focused app](../l02-focused-app-lab/README.md)

## Reflect

- Which device around you is a single-model focused app, and what action does it take on a verdict?
- If you had to choose CONF_FLOOR for a car's siren-detection alert, would you set it high or low, and why?
