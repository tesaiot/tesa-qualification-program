---
id: edgeai-dev.m06.l05
lang: en
title: {th: 'sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ', en: 'Sensor fusion: the model''s verdict with the raw sensor'}
summary: {th: ทำให้การตัดสินใจเชื่อถือได้ขึ้นด้วย sensor fusion เอา verdict ของโมเดล (บอกว่าเป็นอะไร) มายืนยันกับเซนเซอร์ดิบ (บอกว่าแรงแค่ไหน) เข้าใจ corroboration แบบ AND กับ majority vote แบบ k จาก n ผ่านสูตรถ่วงน้ำหนักเดียวกัน และเห็นตัวอย่างระบบกันขโมยสามเซนเซอร์, en: 'Make decisions more trustworthy with sensor fusion - confirm the model''s verdict (what it is) with a raw sensor (how strong it is). Understand AND-style corroboration and k-of-n majority voting as one weighted formula, and study a three-sensor intruder alarm.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l04]
objectives:
  - {th: อธิบายได้ว่าทำไม verdict ของโมเดลเดี่ยวยังไม่พอ และโมเดลกับเซนเซอร์ดิบตอบคนละคำถามอย่างไร, en: 'Explain why a single model''s verdict is not enough, and how the model and a raw sensor answer different questions.'}
  - {th: คำนวณการตัดสินแบบโหวต k จาก n และแบบถ่วงน้ำหนัก S = Σ wᵢsᵢ ≥ θ ได้ และแสดงว่า AND คือกรณี k = n, en: 'Compute a k-of-n vote and a weighted decision S = Σ wᵢsᵢ ≥ θ, and show that AND is the case k = n.'}
  - {th: เขียนประตูยืนยันจากเซนเซอร์ดิบ gmag = |gx| + |gy| + |gz| > MOTION_FLOOR และเงื่อนไข fused = model_hit and raw_ok พร้อม edge-trigger, en: Write a raw-sensor gate gmag = |gx| + |gy| + |gz| > MOTION_FLOOR and the condition fused = model_hit and raw_ok with an edge trigger.}
develops: [{skill: ai.edge, to: 3}, {skill: sys.sensors-actuators, to: 3}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 72f461e44e2ca1531b04a00a7a9d74fb898a7254657882e564f583c74dd2ea24
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 6.5 — Sensor fusion: a model's verdict with a raw sensor

> Module 6 — Edge AI apps · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Make decisions more trustworthy with sensor fusion: confirm a model's verdict (what it is) with a raw sensor (how strong it is). Understand AND-style corroboration and k-of-n majority voting as one weighted formula, and study a three-sensor intruder alarm.

## Objectives

By the end of this lesson, you will:

1. Explain why a single model's verdict isn't enough, and how a model and a raw sensor answer different questions.
2. Compute a k-of-n vote and a weighted decision S = Σ wᵢsᵢ ≥ θ, and show that AND is the case k = n.
3. Write a raw-sensor gate gmag = |gx| + |gy| + |gz| > MOTION_FLOOR and the condition fused = model_hit and raw_ok, with an edge trigger.

## Before you start

You've been through lessons 6.3–6.4, have an action pipeline that resists false positives, and remember the rule classifier from lesson 3.3. Open the `10_motion_alarm.py` example in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, the HW panel only moves the accelerometer (drag to tilt, and the Shake button); the gyro stays near zero. Example 10, which opens the PDM microphone, doesn't yet run on the TESAIoT Dev Kit (it works on the emulator and the PSoC Edge AI Kit).
- **Prior lesson:** [lesson 6.4 — Hands-on: an action pipeline that resists false positives](../l04-action-pipeline-lab/README.md)

## See it work first

Run `10_motion_alarm.py`, press the Arm switch, then try shaking one sensor at a time, and several at once. Notice it doesn't alert every time a single sensor moves — it needs two of three votes before showing `!! INTRUDER !!` (on the emulator, the Shake button lets the radar vote, but this example's IMU reads the gyro, which the emulator keeps stuck near zero).

## Concepts

A model can guess wrong with fairly high confidence — for example, answering `shaking` at 62% when the board was just set down a bit hard. **Sensor fusion** combines several sources into one better decision. The model (`edge_ai`, running on the CM55 with the NPU) answers **"what is this?"** as a probability, while a raw sensor (`sensors`, read from Python on the CM33) answers **"how strong is it?"** in physical units. Each fails in its own way, so corroborating them together resists false positives better — the same way a car uses a camera, radar, and lidar together before braking.

Two flavours of fusion come up often. **Corroboration (AND)**: one primary signal plus one confirming gate, firing only when both pass — suited to "don't alert unless you're sure." And **majority vote** $\text{fire} = [\sum_{i=1}^{n} s_i \ge k]$, as in `10_motion_alarm.py`, which votes two of three among radar, IMU, and microphone, tolerating one sensor missing. Both are the same formula: $S = \sum w_i s_i$ and $\text{fire} = [S \ge \theta]$. When $w_i = 1$ and $\theta = n$, that's AND; lowering $\theta$ relaxes it into a vote. Raising the $w_i$ of a trusted sensor gives it a louder voice.

Our confirming gate is the rule classifier from lesson 3.3: `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (accel in m/s², gyro in deg/s), then `gmag = abs(gx) + abs(gy) + abs(gz)` with `raw_ok = gmag > MOTION_FLOOR` (default 40), combined as `fused = model_hit and raw_ok`, where `model_hit = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR`. The event then fires on the rising edge with a `fired` flag, so it isn't sent again every frame. Shake hard but the model answers `idle`, and it doesn't fire; the model answers `shaking` but the gyro is light, and it doesn't fire either.

## Worked example

`10_motion_alarm.py` is a three-sensor intruder alarm (radar via `sensors.radar()["presence"]`, IMU, and a sound level from PDM), with an on-screen Arm switch. It's a state machine, DISARMED → ARMED → TRIGGERED, voting two of three, and updating the screen only when the state changes. The header notes that on the TESAIoT Dev Kit, opening PDM still clashes with the audio system's clock, so it only works on the PSoC Edge AI Kit and the emulator.

| File | What this file teaches |
|---|---|
| [examples/10_motion_alarm.py](examples/10_motion_alarm.py) | A 3-sensor intruder alarm + an on-screen arm/disarm switch |

This lesson's slides also reference files in another lesson or in `shared/`:

- [m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py](../../m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py) — Taking apart an Edge AI app and remixing it: swapping models + acting on a detected class
- [m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py](../l06-fusion-iot-lab/practice/s17_fusion_iot.py) — Combining a model's verdict with a raw sensor, then streaming it to the cloud (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which statement correctly describes the roles of the model and the raw sensor in fusion? *(single choice · objective 1)*
   - a) The model says what this is (a probability); the raw sensor says how strong it is (physical units)
   - b) Both say the same thing, so they're interchangeable
   - c) The raw sensor is always more accurate than the model
   - d) The model reads physical values better than the raw sensor

   <details><summary>Solution</summary>

   **a** — the two sources answer different questions and fail in different ways. Corroborating them together resists false positives.

   </details>

2. A two-of-three voting system: radar sees it, IMU is quiet, the mic sees it. What's the result? *(single choice · objective 2)*
   - a) No alert, because the IMU is quiet
   - b) Alert, because the total 2 ≥ k = 2
   - c) Undetermined
   - d) Alert only if all three see it

   <details><summary>Solution</summary>

   **b** — Σsᵢ = 1 + 0 + 1 = 2, which meets the threshold k = 2. Voting tolerates one sensor missing; requiring all three would be k = n = AND.

   </details>

3. Two signals, equal weights wᵢ = 1. What θ makes this equal to AND? *(single choice · objective 2)*
   - a) θ = 0
   - b) θ = 1
   - c) θ = 2
   - d) θ = 0.5

   <details><summary>Solution</summary>

   **c** — θ equal to the sum of weights means every signal must pass. If θ = 1, it becomes an OR — passing just one fires it.

   </details>

4. The model answers shaking at conf 0.8, but gx, gy, gz = 5, 10, 8, and MOTION_FLOOR = 40. What is fused? *(single choice · objective 3)*
   - a) True, because the model is confident
   - b) False, because gmag = 23 doesn't exceed 40 — the raw gate fails
   - c) True, because gmag > 0
   - d) An error

   <details><summary>Solution</summary>

   **b** — fusion uses AND. One stage failing means it doesn't fire. This is exactly the model's false positive that fusion filters out.

   </details>

## Lab

- [ ] Run `10_motion_alarm.py` (on the PSoC Edge AI Kit or the emulator), and note which action makes which sensor vote, and which doesn't trigger an alert.
- [ ] Compute S and the firing result for three cases in your learning log, giving radar weight 2, IMU weight 1, mic weight 1, and θ = 3.
- [ ] Write the fused condition out by hand, and identify one move where the model would likely answer shaking but the gyro gate doesn't pass.

## Going further

In lesson 6.6, we'll fill in `s17_fusion_iot.py` to fuse a verdict with the raw gyro, then send the event to an MQTT broker over WiFi.

Next lesson: [lesson 6.6 — Hands-on: publishing a fused event to MQTT](../l06-fusion-iot-lab/README.md)

## Reflect

- Which systems around you should use AND, and which should use voting, based on which kind of mistake is more costly?
- If one sensor in a voting system fails permanently, how does the system's behaviour change?
