---
id: edgeai-dev.m04.l01
lang: en
title: {th: 'ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile', en: 'DSP filters: EMA, Median, Kalman and the radar range profile'}
summary: {th: 'เปิดเสาที่ 3 (Analysis) ด้วยฟิลเตอร์ตามเวลา รู้ว่าสัญญาณรบกวนมีหลายหน้า เลือก EMA, Median หรือ Kalman1D ให้ตรงกับหน้าของ noise ใช้ API ร่วม update/value/reset และเห็น radar range profile ที่ฝั่ง C ทำให้แล้ว', en: 'Open pillar 3 (Analysis) with temporal filters - recognise the kinds of noise, choose EMA, Median or Kalman1D to match, use the shared update/value/reset API, and see the radar range profile the C side already computes.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l04]
objectives:
  - {th: 'แยกชนิดของสัญญาณรบกวน (white noise, spike, drift) และเลือกฟิลเตอร์ที่เหมาะกับแต่ละชนิดได้ พร้อมเหตุผล', en: 'Tell apart kinds of noise (white noise, spikes, drift) and choose the filter that suits each, with a reason.'}
  - {th: คำนวณ EMA หนึ่งก้าวด้วย y = αx + (1−α)y_prev และค่ากลางของหน้าต่าง Median ด้วยมือ แล้วอธิบายข้อแลกเปลี่ยนระหว่างความเรียบกับการตอบสนองเมื่อปรับ α, en: 'Compute one EMA step with y = αx + (1−α)y_prev and the median of a window by hand, and explain the smoothness-versus-response trade-off when α changes.'}
  - {th: อธิบาย Kalman gain K = P/(P+R) ว่าคือน้ำหนักที่ให้กับการวัด และบอกผลของการเพิ่ม r หรือ q, en: 'Explain the Kalman gain K = P/(P+R) as the weight given to the measurement, and state the effect of raising r or q.'}
  - {th: สร้างฟิลเตอร์ของ dsp ด้วย keyword argument ครั้งเดียวนอกลูป แล้วป้อนทีละค่าด้วย update() และอธิบายได้ว่าทำไมสร้างในลูปแล้วไม่เรียบ, en: 'Create a dsp filter with keyword arguments once outside the loop, feed it one sample at a time with update(), and explain why creating it inside the loop never smooths.'}
develops: [{skill: sys.dsp, to: 2}, {skill: hw.math, to: 2}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 5ba2a40cc3b489aaf2a07ab7d354999dc528677dec756cf4f46d2600011e4b33
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.1 — DSP filters: EMA, Median, Kalman and the radar range profile

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Open pillar 3 (Analysis) with temporal filters. Recognise that noise wears many faces, choose EMA, Median or Kalman1D to match, use the shared update/value/reset API, and see the radar range profile the C side already computes.

## Objectives

By the end of this lesson, you will:

1. Tell apart kinds of noise (white noise, spikes, drift), and choose the filter that suits each, with a reason.
2. Compute one EMA step with y = αx + (1−α)y_prev and the median of a window by hand, and explain the smoothness-versus-response trade-off as α changes.
3. Explain the Kalman gain K = P/(P+R) as the weight given to the measurement, and state the effect of raising r or q.
4. Create a dsp filter with keyword arguments once outside the loop, feed it one sample at a time with update(), and explain why creating it inside the loop never smooths anything.

## Before you start

You've been through module 3, and saw a gauge jitter even while the board lay still, in lesson 3.2. This lesson is the answer to that symptom. Open `s08_filters_full.py` (in lesson 4.2) and try it before taking it apart.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — real radar exists on the TESAIoT Dev Kit; on the emulator, radar distance is simulated with a knob.
- **Prior lesson:** [lesson 3.4 — Hands-on: a rule-based comfort classifier](../../m03-processing/l04-rule-classifier-lab/README.md)

## See it work first

Run `s08_filters_full.py` before reading any code. The top graph is the raw signal (three-axis acceleration magnitude); the bottom graph is the same value after filtering. Shake the board gently and switch filters in the dropdown, watching how the bottom line's behaviour changes, and how the noise-down % bar reports how much jitter was reduced.

## Concepts

No sensor gives a smooth value. Noise wears several faces: **white noise**, small spikes scattered by heat or the ADC (suits EMA/SMA); **spikes/outliers**, values that jump occasionally from multipath or signal collisions (suits Median); **drift**, a value slowly sliding (suits an HPF); and mixed noise (suits Kalman). There's no single perfect filter — you have to look at the enemy before picking up a tool. Analysis always comes before Training, because if you feed in a dirty signal, the model learns the "spikes" along with everything else.

A temporal filter is **memory** — it weighs a new value against the past. The filters in `dsp` run as a stream on the CM33, and every one shares the same API: create it once outside the loop → `y = f.update(x)` every round → `f.value()` reads the latest value → `f.reset()` clears the state. Every parameter is a **keyword argument** (`alpha=`, `window=`, `q=`, `r=`) — passing one positionally, such as `dsp.EMA(0.15)`, throws a `TypeError`. If you accidentally create the filter inside the loop, its memory gets wiped every round, and the line will never smooth out.

**EMA:** $y[n] = \alpha x[n] + (1-\alpha) y[n-1]$. A small α is smooth but slow to follow; a large α is quick but spikes still show through. `EMA_ALPHA = 0.15` means trusting a new value 15%. **Median** sorts the latest N values and takes the middle one, so an outlier never has a chance to win (for example, 98, 101, 240, 99, 100 gives 100, while the average gives 127.6). The firmware requires the window to be an odd number no greater than 15. **Kalman1D** keeps both an estimate and its uncertainty P. Every step it computes $K = P/(P+R)$, then $x \leftarrow x + K(z - x)$. A high `r` (distrusting the sensor) shrinks K, giving smoothness; a high `q` lets the true value move quickly. You can think of Kalman as an EMA that adjusts its own α.

A real-world example is the **radar range profile**: `sensors.radar_range()` returns `distance_m`, `peak_db`, `resolution_m`, `target`, `seq`. The C side does HPF → FFT → dB → peak-finding, all of it. Resolution is roughly 0.33 metres per bin, and the range loves to jump due to multipath — genuine spikes. The suitable filter is therefore Median, and in real work we often chain filters — Median to guard against spikes first, then EMA to smooth what's left.

## Worked example

`05_radar_distance.py` is a radar tape measure that uses Median to guard against jumping readings. **Predict** before running it: if you walk in and out in front of the board, will the number stay steady or jump around? Then run it on the board and compare.

| File | What this file teaches |
|---|---|
| [examples/05_radar_distance.py](examples/05_radar_distance.py) | Radar Range: a tape measure on screen (Bar + Seg7 + graph) |

This lesson's slides also reference files in another lesson:

- [m04-analysis/l02-filters-lab/examples/s08_filters_full.py](../l02-filters-lab/examples/s08_filters_full.py) — cleaning a signal with DSP filters (full version)
- [m04-analysis/l02-filters-lab/practice/s08_filters.py](../l02-filters-lab/practice/s08_filters.py) — cleaning a signal with DSP filters (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Radar distance occasionally jumps due to multipath reflections. Which filter should be chosen first? *(single choice · objective 1)*
   - a) EMA
   - b) Median
   - c) HPF
   - d) No filtering needed

   <details><summary>Solution</summary>

   **b** — a jump is a genuine spike. Median votes for the middle value, so it can drop the spike entirely, while EMA would just smooth it into a bump that's still visible.

   </details>

2. y_prev = 10, x = 20, and α = 0.25. What is this round's EMA value? *(single choice · objective 2)*
   - a) 12.5
   - b) 15
   - c) 17.5
   - d) 20

   <details><summary>Solution</summary>

   **a** — y = 0.25 × 20 + 0.75 × 10 = 5 + 7.5 = 12.5. The new value only gets a quarter of the weight, so the line follows slowly but stays smooth.

   </details>

3. A five-value Median window is 98, 101, 240, 99, 100. What's the result? *(single choice · objective 2)*
   - a) 127.6
   - b) 100
   - c) 240
   - d) 98

   <details><summary>Solution</summary>

   **b** — sorted: 98, 99, 100, 101, 240. The middle value is 100 — the spike 240 gets pushed to the edge, while the average, 127.6, gets dragged along by it.

   </details>

4. In Kalman1D, if r increases (trusting the sensor less) while q stays the same, what happens? *(single choice · objective 3)*
   - a) K grows, and the value jumps to follow the measurement
   - b) K shrinks, the value moves in smaller steps — smoother but slower to follow
   - c) No effect, since K is constant
   - d) The filter stops working

   <details><summary>Solution</summary>

   **b** — K = P/(P+R). As R grows, K shrinks, so x += K(z − x) moves less. You gain smoothness at the cost of response, the same trade-off as a small α in EMA.

   </details>

5. This code creates f = dsp.EMA(alpha=0.15) inside the loop every round, then calls f.update(x). What shows on the graph? *(single choice · objective 4)*
   - a) A very smooth line, because α is small
   - b) The filtered line looks just like the raw line, because a freshly created filter returns the first value fed to it directly, and its memory is wiped every round
   - c) The program throws TypeError
   - d) The line stays at zero forever

   <details><summary>Solution</summary>

   **b** — state lives inside the object. Recreating it every round means starting fresh every time, so the filter never has a past to weigh against. It must be created once, outside the loop.

   </details>

## Lab

- [ ] Compute EMA by hand for three steps from x = 10, 10, 20, starting at y = 10, at α = 0.5 and α = 0.1, and compare which one keeps up better.
- [ ] Find the median of the window [5, 7, 90, 6, 5], compare it against the average, and note in your learning log why they differ.
- [ ] In the REPL, try calling `dsp.EMA(0.15)`, look at the error message, then fix it to `dsp.EMA(alpha=0.15)`.

## Going further

In lesson 4.2, we'll fill in the `s08_filters.py` file so it creates a filter from its name, filters a real signal, and measures the result as a noise-down %.

Next lesson: [lesson 4.2 — Hands-on: filters cleaning a signal live](../l02-filters-lab/README.md)

## Reflect

- Which kind of noise does the work you care about run into most, and how much lag are you willing to accept in exchange for smoothness?
- Why does measuring smoothness by jitter between frames work on a real sensor, even with no "answer key" for what the true value actually is?
