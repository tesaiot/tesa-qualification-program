---
id: edgeai-dev.m03.l03
lang: en
title: {th: 'ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ', en: 'Derived metrics and rule-based classification: dew point, heat index and the rule ladder'}
summary: {th: เขียน classifier ตัวแรกของหลักสูตรโดยยังไม่ใช้ ML แปลงอุณหภูมิกับความชื้นเป็นค่าอนุพัทธ์ dew point และ heat index แล้วตัดสินเป็นคลาสด้วยเส้นแบ่งและบันไดกฎที่ลำดับชั้นถูกต้อง, en: 'Build the course''s first classifier without ML - turn temperature and humidity into the derived metrics dew point and heat index, then decide a class with thresholds and a correctly ordered rule ladder.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l02]
objectives:
  - {th: อธิบายได้ว่า classifier คือกล่องที่รับตัวเลขแล้วคืนคลาส และเปรียบเทียบการหาเส้นแบ่งด้วยกฎมือกับด้วย ML ได้อย่างน้อยสองมิติ (ข้อมูลฝึก ความอธิบายได้ หรือความซับซ้อนของ pattern), en: 'Explain a classifier as a box that takes numbers and returns a class, and compare hand-set rules with ML on at least two dimensions (training data, explainability or pattern complexity).'}
  - {th: เรียก dsp.dew_point และ dsp.heat_index แล้วอธิบายได้ว่าทำไมค่าอนุพัทธ์ช่วยให้กฎตัดสินได้ดีกว่าค่าดิบ เช่น 32°C ที่ความชื้น 40% กับ 80% ให้ heat index ต่างกันราว 12 องศา, en: Call dsp.dew_point and dsp.heat_index and explain why derived metrics help rules decide better than raw values (for example 32°C at 40% and 80% humidity differ by about 12 degrees of heat index).}
  - {th: เรียงบันไดกฎหลายชั้นให้เงื่อนไขที่เฉพาะหรือรุนแรงกว่าอยู่บน และหา dead branch ในบันไดที่เรียงผิดได้, en: 'Order a multi-step rule ladder with the more specific or severe conditions on top, and spot the dead branch in a wrongly ordered ladder.'}
develops: [{skill: ai.edge, to: 1}, {skill: sys.dsp, to: 2}, {skill: prog.algo-ds, to: 2}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: afb1863d43b6f029429e8cc873778af926b70935b60de947af689f912e6aaf2f
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 3.3 — Derived metrics and rule-based classification: dew point, heat index and the rule ladder

> Module 3 — Processing with maths and physics · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Build the course's first classifier without ML. Turn temperature and humidity into the derived metrics dew point and heat index, then decide a class with thresholds and a correctly ordered rule ladder.

## Objectives

By the end of this lesson, you will:

1. Explain a classifier as a box that takes numbers and returns a class, and compare hand-set rules with ML on at least two dimensions (training data, explainability, or pattern complexity).
2. Call dsp.dew_point and dsp.heat_index, and explain why derived metrics help rules decide better than raw values — for example, 32°C at 40% and 80% humidity give heat index values about 12 degrees apart.
3. Order a multi-step rule ladder with the more specific or severe conditions on top, and spot the dead branch in a wrongly ordered ladder.

## Before you start

You've been through lessons 3.1–3.2, and understand the raw → derived → viz pattern. Keep the REPL open to try `dsp.dew_point`, `dsp.heat_index` and `dsp.comfort_zone` with values of your own choosing.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — uses the DPS368 and SHT40 found on the TESAIoT Dev Kit (the Eva Kit doesn't have them); the emulator simulates temperature and humidity values.
- **Prior lesson:** [lesson 3.2 — Hands-on: four physics gauges on screen](../l02-physics-gauges-lab/README.md)

## See it work first

Run the ready-made rule `dsp.comfort_zone(t, rh)` that the firmware provides first — it answers `comfortable`, `hot`, `humid`, and so on, right away. Then ask "how does it know it's hot right now?" The answer is a handful of `if` lines in C — not a shred of AI.

## Concepts

A **classifier** is a function that takes numbers and returns one "class" label from a fixed set. The Motion model in module 1 is a classifier too, except inside it's a neural network. Today, what's inside is **rules we set ourselves**. The shape in and out is identical — what differs is how the boundary is found: hand-set rules need no training data, run immediately, and every decision can be explained — but they balloon out of control once there are many conditions, and struggle with complex patterns. ML learns a boundary from data and can capture patterns across many dimensions, but needs data, needs training, and is harder to explain "why" for. In plenty of real work, a simple threshold rule beats ML.

Raw values are sometimes hard to judge on their own — 32°C feels very different dry versus humid. A **derived metric** combines several raw values into a single one that's easier to judge — in the world of ML, this is called feature engineering. `dsp.dew_point(t, rh)` uses the Magnus–Tetens formula to return the dew point (the closer it gets to air temperature, the more saturated the air is). `dsp.heat_index(t, rh)` uses the Rothfusz regression to return "how hot it feels" — for example, 32°C at 40% gives about 32°C, but at 80% gives about 44°C. Both are computed on the CM33, not the NPU. `dsp.comfort_zone` is a ready-made classifier that decides from the raw `t` and `rh` values with an `if` ladder.

The smallest unit of a rule is a **single threshold**, splitting the world into two classes. Where that threshold sits (such as heat index 32) is a hyperparameter — a value we choose ourselves from knowledge or a standard. Once you need several classes, you stack `if`s into a **rule ladder**, checked top to bottom — the first one that's true wins and returns immediately. The iron rule is: **more specific or more severe conditions must sit on top.** If `hi >= 32` sits above `hi >= 41`, a value of 43 gets `hot`, and the `danger` step can never be reached — a dead branch the compiler never warns about. It has to be caught by testing.

## Worked example

`08_environment_dashboard.py` is a three-card dashboard (temperature, humidity, pressure) reading the same sensors as this lesson. Run it to see the raw values first, then think about which derived metric you'd need to add to have a card say "comfortable or not."

| File | What this file teaches |
|---|---|
| [examples/08_environment_dashboard.py](examples/08_environment_dashboard.py) | Environment Dashboard: 3 cards (temperature / humidity / pressure) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which of these are strengths of hand-set rules compared with ML? (select every correct answer) *(multiple choice · objective 1)*
   - a) No training data needed, runs immediately
   - b) Every decision can be explained by which condition triggered it
   - c) Captures complex patterns across dozens of dimensions well
   - d) Adjusts its own threshold as new data arrives

   <details><summary>Solution</summary>

   **a, b** — the last two are ML's strengths, since it learns a boundary from data. Hand-set rules are lightweight, explainable, and need no training data.

   </details>

2. Why does this lesson's rule ladder decide hot and danger from heat index instead of raw temperature? *(single choice · objective 2)*
   - a) Because heat index reads faster
   - b) Because the same temperature at different humidity levels feels very different to the body, and heat index already accounts for that
   - c) Because the temperature sensor isn't accurate
   - d) Because heat index is always a whole number

   <details><summary>Solution</summary>

   **b** — 32°C at 80% humidity feels like about 44°C. Deciding from raw temperature would miss a genuinely dangerous sweltering condition.

   </details>

3. What does it mean when the dew point gets very close to air temperature? *(single choice · objective 2)*
   - a) The air is very dry
   - b) The air is close to saturated, very humid — water vapour is close to condensing into droplets
   - c) The sensor is broken
   - d) Temperature is dropping fast

   <details><summary>Solution</summary>

   **b** — as RH approaches 100%, ln(RH/100) approaches 0, making the dew point approach the real temperature. The gap t − Td is therefore a good humidity signal.

   </details>

4. The ladder has `if hi >= 32: return "hot"` before `if hi >= 41: return "danger"`. With input hi = 43, what's the result? *(single choice · objective 3)*
   - a) danger
   - b) hot, and the danger step becomes a dead branch that can never be reached
   - c) An error, because the conditions overlap
   - d) comfortable

   <details><summary>Solution</summary>

   **b** — the ladder returns at the first true step. 43 ≥ 32, so it answers hot before ever reaching the danger step. More severe conditions must always sit on top.

   </details>

## Lab

- [ ] In the REPL, call `dsp.heat_index(32, 40)` and `dsp.heat_index(32, 80)`, and note the results in your learning log.
- [ ] Call `dsp.comfort_zone` with three sets of values that give different classes, and write down which ladder step each set falls into.
- [ ] Write a 6-step rule ladder on paper, then swap the top two steps to find an input that creates a dead branch.

## Going further

In lesson 3.4, we'll write our own `classify()` in the `s07_rule_classifier.py` file and compare it against the firmware's ready-made rule.

Next lesson: [lesson 3.4 — Hands-on: a rule-based comfort classifier](../l04-rule-classifier-lab/README.md)

## Reflect

- What job can you think of where rules should be used over ML, because the decision must be explainable, or because a legal standard already sets the threshold?
- If your sensor had 50 values, where would writing a rule ladder get harder?
