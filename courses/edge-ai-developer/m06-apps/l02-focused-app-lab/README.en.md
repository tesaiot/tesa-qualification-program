---
id: edgeai-dev.m06.l02
lang: en
title: {th: 'ลงมือทำ: แอปโฟกัสของเราเอง', en: 'Hands-on: your own focused app'}
summary: {th: เติมสี่จุดใน s15_apps.py ให้เป็นแอปโฟกัสที่นับเสียงไอ ได้แก่ select โมเดลเป้าหมายก่อนลูป อ่าน result โชว์คลาสที่ชนะ และเงื่อนไขตรวจเจอที่ผ่าน CONF_FLOOR แล้วรีทาร์เก็ตเป็น Alarm หรือ Siren ด้วยการแก้แค่สองบรรทัดบนหัวไฟล์ จนได้ตระกูลแอปต่อโมเดลของเราเอง, en: 'Fill four points in s15_apps.py to make a focused cough-counting app - select the target model before the loop, read the result, show the winning class, and a detection condition gated by CONF_FLOOR - then retarget it to Alarm or Siren by editing just two lines at the top, giving you your own family of per-model apps.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l01]
objectives:
  - {th: เติมสี่จุดใน practice/s15_apps.py จนแอปขึ้นคลาสที่ชนะ แถบทุกคลาส latency และตัวนับที่เพิ่มหนึ่งครั้งต่อเหตุการณ์เป้าหมายหนึ่งครั้ง, en: 'Fill the four points in practice/s15_apps.py until the app shows the winning class, a bar per class, the latency, and a counter that rises once per target event.'}
  - {th: รีทาร์เก็ตแอปเป็นโมเดลอื่นอย่างน้อยหนึ่งตัวโดยแก้แค่ TARGET_KEYWORDS กับ TARGET_CLASS และตรวจชื่อคลาสจาก edge_ai.models() ก่อน (เช่น Siren ใช้คลาส sirens), en: 'Retarget the app to at least one other model by editing only TARGET_KEYWORDS and TARGET_CLASS, checking the class name in edge_ai.models() first (Siren''s class is sirens).'}
  - {th: ทดลองตัดเงื่อนไข conf ≥ CONF_FLOOR ออกชั่วคราว แล้วอธิบายจากผลที่เห็นว่าทำไมตัวนับจึงเก็บ false positive, en: Temporarily remove the conf ≥ CONF_FLOOR condition and use what you see to explain why the counter then collects false positives.}
develops: [{skill: ai.edge, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}]
assesses: [{skill: ai.edge, level: 2, evidence: practice/s15_apps.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 84cc10a2c5075babd1dd07f6671964e3b80f00c3ed2ece328a7c3c6a04177dfc
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.2 — Hands-on: your own focused app

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill four points in s15_apps.py to make a focused cough-counting app: select the target model before the loop, read the result, show the winning class, and a detection condition gated by CONF_FLOOR. Then retarget it to Alarm or Siren by editing just two lines at the top of the file, giving you your own family of per-model apps.

## Objectives

By the end of this lesson, you will:

1. Fill the four points in practice/s15_apps.py until the app shows the winning class, a bar for every class, the latency, and a counter that rises once per target event.
2. Retarget the app to at least one other model by editing only TARGET_KEYWORDS and TARGET_CLASS, checking the class name in edge_ai.models() first (Siren's class is sirens).
3. Temporarily remove the conf ≥ CONF_FLOOR condition, and use what you see to explain why the counter then collects false positives.

## Before you start

You've been through lesson 6.1, and understand find_model, CONF_FLOOR, and counting on the rising edge. Prepare a coughing clip, an alarm sound, or a siren to play near the board.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, the audio models are simulated values where the event class never beats unlabelled, so the counter never moves. You can still test the counting logic on the emulator using the Motion model with the Shake button; counting real coughs needs the board.
- **Prior lesson:** [lesson 6.1 — Six models and the edge_ai API: an app focused on one model](../l01-focused-apps/README.md)

## Concepts

The whole file reads as one sentence: target the cough model → create the card → start it running → loop reading results, showing the class on screen, counting on detection → stop on exit. The settings panel at the top of the file is `TARGET_KEYWORDS = ("cough",)`, `TARGET_CLASS = "cough"`, and `TARGET_SENSOR = edge_ai.SENSOR_MIC`, keeping the model's name separate from the class's name, since they aren't always the same. The four points we fill in are: (1) `edge_ai.select(model['index'])` before the loop, inside a `try`, since `select()` can throw `OSError` if the switch isn't confirmed (2) `r = edge_ai.result()` (3) `verdict.text(r['label'] or '-')` when `seq` changes, and (4) `is_target = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR`, which is the genuinely new part of this lesson.

The counter rises when `is_target and not was_target` — one per cough. If you see the number jump several times for one sound, the rising-edge condition is missing. If the result freezes and `seq` never moves, that's the evaluation Ready Model's ceiling, not broken code. Retargeting takes less than a minute: `("alarm",)` with `"alarm"`, or `("siren",)` with `"sirens"` (note the s), then save as a new file. The rest of the file's skeleton doesn't need touching, because `find_model()` finds the model for you, and the bars adjust to whichever `labels` it returns. Success is being able to say when your action trusts the verdict, and how it guards against overcounting.

## Worked example

`s15_apps_full.py` adds colour based on `CONF_FLOOR`, light debouncing (counting only after two consecutive detections), a label showing the time of the last detection, and a Reset button that clears the counter.

| File | What this file teaches |
|---|---|
| [examples/s15_apps_full.py](examples/s15_apps_full.py) | An edge AI app "focused on one model" (full version) |

This lesson's slides also reference a file in another lesson:

- [m06-apps/l01-focused-apps/examples/16_edge_ai_sound_events.py](../l01-focused-apps/examples/16_edge_ai_sound_events.py) — Edge AI: Sound Events (Cough / Alarm / Siren) — 3 mic models in one dropdown

## Practice

The `# TODO:` comments are at lines 87 (`select`), 96 (`result`), 101 (`verdict.text`), and 112 (`is_target`). If the card fully shows but never any results, check point 87 first. If the bars move but the large text never changes, check point 101.

| Practice file | Topic |
|---|---|
| [practice/s15_apps.py](practice/s15_apps.py) | An edge AI app "focused on one model" (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s15_apps.py](solution/s15_apps.py) | [practice/s15_apps.py](practice/s15_apps.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. The app's card fully shows, but there's never any result at all, and the counter never moves. Which point is most likely still empty? *(single choice · objective 1)*
   - a) Point 1, edge_ai.select(model['index'])
   - b) Point 3, verdict.text(...)
   - c) Point 4, is_target
   - d) Nothing is wrong

   <details><summary>Solution</summary>

   **a** — without selecting the target model, no model runs, so there's nothing for result() to return.

   </details>

2. One cough, but the counter rises three to four times. Which part of the condition is missing? *(single choice · objective 1)*
   - a) r["conf"] >= edge_ai.CONF_FLOOR
   - b) not was_target (counting on the rising edge only)
   - c) r["label"] == TARGET_CLASS
   - d) edge_ai.stop()

   <details><summary>Solution</summary>

   **b** — one cough spans several inference results. Without remembering the previous round's state, every matching result gets counted.

   </details>

3. You retarget to siren with TARGET_KEYWORDS = ("siren",) and TARGET_CLASS = "siren", but the counter never moves. Why? *(single choice · objective 2)*
   - a) The Siren model isn't on the board
   - b) The real class name is sirens (with an s), so label == TARGET_CLASS is never true
   - c) CONF_FLOOR is too high
   - d) find_model can't find it

   <details><summary>Solution</summary>

   **b** — a model's name and its class's name aren't always the same. Check `labels` from edge_ai.models() in the REPL before retargeting.

   </details>

4. You remove the conf condition, and the counter rises even with no one coughing. Why? *(single choice · objective 3)*
   - a) The microphone is broken
   - b) argmax always gives a winner, even when cough wins narrowly, 0.51 to 0.49 — that still gets counted, becoming a false positive
   - c) seq never changes
   - d) The model switched to Motion

   <details><summary>Solution</summary>

   **b** — CONF_FLOOR is the gate that says to trust a result only once it's confident enough. Without that gate, every narrow win turns into an action.

   </details>

## Lab

**The MVP for lessons 6.1–6.2:** a single-model focused app with a clean UI, targeting a model with `find_model()`, showing the verdict, every class's bar, and latency, with a counter that genuinely fires when the target class crosses `CONF_FLOOR`, retargetable to at least two models.

- [ ] All four points in the practice file are filled in. Practise on the emulator, then count real coughs on the board.
- [ ] Retarget to Alarm or Siren, save as a new file, and confirm the counter works.
- [ ] Temporarily remove `and r['conf'] >= edge_ai.CONF_FLOOR`, play other sounds, and note in your learning log how the counter differs from before. Then put it back.
- [ ] Be able to explain why `CONF_FLOOR` must be checked before counting, and why counting must happen only on the rising edge.

## Going further

In the next pair of lessons (6.3–6.4), we'll turn counting into a stronger action, such as an RGB light, sound, and a log, with full debounce and cooldown.

Next lesson: [lesson 6.3 — An action pipeline: CONF_FLOOR, debounce, cooldown and on_result](../l03-action-pipeline/README.md)

## Reflect

- If a cough-counting app overcounts in a room where people are talking, would you adjust CONF_FLOOR or debounce first?
- How does separating TARGET_KEYWORDS from TARGET_CLASS help whoever maintains your code after you?
