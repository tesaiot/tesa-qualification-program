---
id: edgeai-dev.m08.l01
lang: en
title: {th: 'ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว', en: 'Designing the capstone: Guardian, three pillars in one file'}
summary: {th: ออกแบบ capstone ที่ต่างจากเดโมหนึ่งชิ้น Guardian ร้อยสามเสาของวงจรข้อมูลไว้ในลูปเดียว ได้แก่ DAQ (ความเร่งดิบเป็นบริบท) Processing (EMA กรองความมั่นใจ) และ Apps (verdict ผ่านชั้นตัดสินใจแล้วสั่งการ) พร้อมคณิตของขนาดเวกเตอร์ EMA และเงื่อนไขยิงสามด่าน และการเลือกค่าออกแบบอย่างมีเหตุผล, en: 'Design a capstone that is more than one more demo. The Guardian threads three pillars of the data lifecycle through one loop - DAQ (raw acceleration as context), Processing (EMA-filtered confidence) and Apps (a verdict through a decision layer to an action) - with the maths of vector magnitude, EMA and the three-gate firing rule, and reasoned choices of design values.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l04]
objectives:
  - {th: 'แยก capstone หรือผลิตภัณฑ์ออกจากเดโม และชี้ได้ว่า Guardian ข้ามสามเสาใด (DAQ, Processing, Apps) และต่อยอดด้วยเสา Training หรือ Analysis ได้อย่างไร', en: 'Tell a capstone or product from a demo, and show which three pillars the Guardian crosses (DAQ, Processing, Apps) and how Training or Analysis could extend it.'}
  - {th: คำนวณขนาดเวกเตอร์ความเร่งและ EMA ของความมั่นใจหนึ่งก้าว และอธิบายว่าทำไมต้องสร้างตัวกรองนอกลูปและล้างเมื่อกด Load, en: 'Compute the acceleration vector magnitude and one EMA step of the confidence, and explain why the filter is created outside the loop and reset on Load.'}
  - {th: เขียนเงื่อนไขยิง (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) พร้อม edge-trigger และบอกว่าพีคหลอกแบบใดถูกด่านใดกันไว้, en: 'Write the firing rule (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) with an edge trigger, and say which gate stops which kind of fake peak.'}
  - {th: 'เลือกค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA และจังหวะลูปให้ผลิตภัณฑ์ที่กำหนด พร้อมเหตุผลเรื่องการพลาดของจริงเทียบกับการเตือนผิด ความไว ความนิ่ง และพลังงาน', en: 'Choose CONF_FLOOR, HITS_NEEDED, EMA_ALPHA and the loop period for a given product, with reasons about misses versus false alarms, responsiveness, stability and energy.'}
develops: [{skill: ai.edge, to: 3}, {skill: biz.product-decision, to: 2}, {skill: sys.dsp, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 60a4553243738452f69067980b1350fd26cbd7a81e0f60d9eaf6faa83cab63d8
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 8.1 — Designing the capstone: Guardian, three pillars in one file

> Module 8 — Capstone: your own Edge AI app · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Design a capstone that's more than one more demo. The Guardian threads three pillars of the data lifecycle through one loop: DAQ (raw acceleration as context), Processing (EMA-filtered confidence), and Apps (a verdict through a decision layer to an action), with the maths of vector magnitude, EMA, and the three-gate firing rule, and reasoned choices of design values.

## Objectives

By the end of this lesson, you will:

1. Tell a capstone or product apart from a demo, and show which three pillars the Guardian crosses (DAQ, Processing, Apps), and how Training or Analysis could extend it.
2. Compute the acceleration vector magnitude and one EMA step of the confidence, and explain why the filter is created outside the loop and reset on Load.
3. Write the firing rule (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) with an edge trigger, and say which gate stops which kind of fake peak.
4. Choose CONF_FLOOR, HITS_NEEDED, EMA_ALPHA, and the loop period for a given product, with reasons about misses versus false alarms, responsiveness, stability, and energy.

## Before you start

You've been through modules 1 through 7, and have a logger, a filter, a self-trained model, and an action pipeline in hand. Open `s20_capstone_full.py` (in lesson 8.2) in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — Guardian uses the IMU and edge_ai, both of which the emulator supports (the Motion model with the Shake button). A real-world event such as sound or radar needs the board.
- **Prior lesson:** [lesson 7.4 — Hands-on: make a new model appear in edge_ai.models()](../../m07-under-the-hood/l04-extend-model-lab/README.md)

## See it work first

Run `s20_capstone_full.py`, select Motion, press Load, then hold a shake until the `! ALERT !` banner pops up with a sound and a counter. Then try a single brief shake, and notice it doesn't alert. Ask yourself which modules' work Guardian draws on to be able to do this.

## Concepts

A **demo** answers "can it be done" under ideal conditions. A **capstone** answers "is it usable in practice" — it must handle noise, false positives, and cleanup, and its design must be explainable. The requirement is to cross at least three pillars of the data lifecycle. The Guardian threads three pillars through a single `while` loop: **DAQ** reads `ax, ay, az = sensors.bmi270.acceleration()`, then computes $mag = \sqrt{a_x^2 + a_y^2 + a_z^2}$ (about 9.8 m/s² at rest, spiking upward on a shake) as context. **Processing** filters the confidence with $s_n = \alpha c_n + (1-\alpha) s_{n-1}$ via `conf_ema = dsp.EMA(alpha=EMA_ALPHA)`, created outside the loop because it must remember the past, and `reset()` when Load is pressed to start a fresh watch cycle. **Apps** uses the same core — `models` / `select` / `result` / `stop` with `CONF_FLOOR` — then adds a decision layer, extendable with a self-trained model (Training) or FFT-derived features (Analysis).

The decision layer stacks three gates: the right class (`top == alert_idx`, by design convention the last class is the event, such as shaking), confident enough from the filtered value (`conf_s >= CONF_FLOOR`), and held long enough (`streak >= HITS_NEEDED`) — that is, $\text{fire} \iff (top = alert\_idx) \wedge (s_n \ge \text{CONF\_FLOOR}) \wedge (streak \ge \text{HITS\_NEEDED})$, then a `fired` flag fires once per event. Fail any gate, and `streak` resets to zero. Most false positives only pass one or two gates — requiring all three is exactly why a single brief peak doesn't trigger an alert.

Every design value has a two-sided cost. A high `CONF_FLOOR` misses real events; a low one gives false alarms. A high `HITS_NEEDED` responds slowly; a low one gets fooled by peaks. A high `EMA_ALPHA` is responsive but jittery; a low one is stable but laggy. And the loop's `time.sleep_ms` trades energy against responsiveness. There's no single correct value — only a value suited to the cost of missing in that job. Detecting a fall for an elderly person, for instance, would rather have a false alarm than a miss, while a hand-waving advertising sign would rather miss than bother passersby. A capstone starts with **Design** (what to watch, what action, what threshold and why), then **Build**, then **Ship**.

## Worked example

This lesson's slides also reference files in another lesson or in `shared/`:

- [m08-capstone/l02-capstone-build-lab/examples/s20_capstone_full.py](../l02-capstone-build-lab/examples/s20_capstone_full.py) — Capstone: Edge AI Guardian (full version)
- [m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py](../l02-capstone-build-lab/practice/s20_capstone.py) — Capstone: Edge AI Guardian (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which pillars does Guardian touch directly? *(single choice · objective 1)*
   - a) DAQ, Processing, and Apps
   - b) Training only
   - c) Analysis and Training
   - d) Apps only

   <details><summary>Solution</summary>

   **a** — it reads raw acceleration (DAQ), filters confidence with EMA (Processing), and takes the verdict to an action (Apps). Training and Analysis are ways to extend it.

   </details>

2. EMA_ALPHA = 0.4, the previously filtered value is 0.30, and the new raw conf is 0.90. What's the new value? *(single choice · objective 2)*
   - a) 0.90
   - b) 0.60
   - c) 0.54
   - d) 0.36

   <details><summary>Solution</summary>

   **c** — 0.4 × 0.90 + 0.6 × 0.30 = 0.36 + 0.18 = 0.54, already past the 0.50 threshold, but it still needs to pass the streak gate too.

   </details>

3. What happens if you create a new dsp.EMA every time through the loop? *(single choice · objective 2)*
   - a) It filters better
   - b) The filter loses its memory every frame, and the output equals the raw value — so nothing gets filtered at all
   - c) The program stops
   - d) The value becomes zero

   <details><summary>Solution</summary>

   **b** — the first call of an EMA returns exactly the input value. Creating a new one every round is the same as having no filter at all, so it must be created once, before the loop.

   </details>

4. top = alert_idx, conf_s = 0.62, and streak = 2, while HITS_NEEDED = 3. Does Guardian fire? *(single choice · objective 3)*
   - a) Yes, because the class is right and it's confident enough
   - b) Not yet, because the streak gate isn't satisfied yet
   - c) It fires twice
   - d) It doesn't fire, because conf is too low

   <details><summary>Solution</summary>

   **b** — all three gates must pass at once. If the next result is still the right class and confident enough, streak reaches 3, and it fires once.

   </details>

5. Guardian is detecting falls for elderly people. Which direction should the values be tuned? *(single choice · objective 4)*
   - a) A high CONF_FLOOR and a large HITS_NEEDED, so it never gives a false alarm
   - b) Accept some false alarms in exchange for not missing real events — for example, lower CONF_FLOOR and lower HITS_NEEDED
   - c) No decision layer is needed
   - d) EMA_ALPHA = 0

   <details><summary>Solution</summary>

   **b** — the cost of missing a fall is far higher than the cost of a false alarm. Tuning should therefore lean toward responsiveness, with that reasoning written into the design.

   </details>

## Lab

- [ ] Write out Guardian's three-pillar diagram in your learning log, with the main command of each pillar named.
- [ ] Spend 15 minutes designing your own Guardian: which model to watch, what the event is, what the action is, and how far apart the costs of a miss and a false alarm are.
- [ ] Choose starting values for `CONF_FLOOR`, `HITS_NEEDED`, and `EMA_ALPHA`, with one line of reasoning per value.

## Going further

In lesson 8.2, we'll fill in the five backbone lines of `s20_capstone.py`, then build, tune, and demo our own Guardian.

Next lesson: [lesson 8.2 — Hands-on: building and delivering an Edge AI app](../l02-capstone-build-lab/README.md)

## Reflect

- Which jobs around you have a real miss that costs more than a false alarm, and which have it the other way around?
- If you could add a fourth pillar to Guardian, would you choose Training or Analysis, and what would it add?
