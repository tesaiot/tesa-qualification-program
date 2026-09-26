---
id: edgeai-dev.m04.l02
lang: en
title: {th: 'ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ', en: 'Hands-on: cleaning a live signal with a filter'}
summary: {th: เติมห้าจุดใน s08_filters.py ให้สร้างฟิลเตอร์จากชื่อด้วย keyword argument อ่านขนาดความเร่ง ป้อนเข้า filt.update และวาดกราฟดิบเทียบกรอง แล้ววัดผลด้วย noise down % และเทียบสามฟิลเตอร์กับสัญญาณเดียวกัน, en: 'Fill five points in s08_filters.py to build a filter by name with keyword arguments, read the acceleration magnitude, feed filt.update and plot raw against filtered, then measure the result as noise down % and compare three filters on the same signal.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l01]
objectives:
  - {th: 'เติมห้าจุดใน practice/s08_filters.py จนสองกราฟต่างกันชัด (เส้นล่างเรียบกว่าเส้นบน) และเลือก EMA, Median, Kalman1D ใน dropdown ได้ครบโดยไม่เกิด error', en: 'Fill the five points in practice/s08_filters.py until the two charts clearly differ (the lower line is smoother) and EMA, Median and Kalman1D can all be selected without an error.'}
  - {th: จดค่า noise down % ของสามฟิลเตอร์กับสัญญาณเดียวกัน และสร้างสถานการณ์ที่ Median ชนะ EMA ชัดเจนพร้อมอธิบายเหตุผล, en: 'Record noise down % for the three filters on the same signal, and create a situation where Median clearly beats EMA, explaining why.'}
  - {th: อธิบายได้ว่าทำไมบรรทัด y = filt.update(x) บรรทัดเดียวใช้ได้กับทุกฟิลเตอร์ และทำไม noise down % วัดจากการกระตุกระหว่างเฟรม, en: 'Explain why the single line y = filt.update(x) works for every filter, and why noise down % is measured from frame-to-frame jitter.'}
develops: [{skill: sys.dsp, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}]
assesses: [{skill: sys.dsp, level: 2, evidence: practice/s08_filters.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 60379838aca8d2e0b13aac247e538d926e57274c0c024516ef46eb7250da37c5
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.2 — Hands-on: cleaning a live signal with a filter

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s08_filters.py to build a filter by name with keyword arguments, read the acceleration magnitude, feed it into filt.update, and plot raw against filtered, then measure the result as noise down %, comparing three filters on the same signal.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s08_filters.py until the two charts clearly differ (the lower line is smoother than the upper one), and EMA, Median and Kalman1D can all be selected in the dropdown without an error.
2. Record the noise down % of three filters on the same signal, and create a situation where Median clearly beats EMA, explaining why.
3. Explain why the single line y = filt.update(x) works for every filter, and why noise down % is measured from frame-to-frame jitter.

## Before you start

You've been through lesson 4.1, and know the personalities of EMA, Median and Kalman1D. Keep your learning log ready to note the noise-down % for each filter.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — IMU mode works fully on the emulator; Radar range mode on the emulator is a simulated distance from a knob, with no real multipath.
- **Prior lesson:** [lesson 4.1 — DSP filters: EMA, Median, Kalman and the radar range profile](../l01-dsp-filters/README.md)

## Concepts

The whole file reads as one sentence: read a raw value → feed it into a filter → plot raw against filtered → measure how many percent noise was reduced, looping every 60 ms. The filter is created in a "create once" step, through `make_filter(name)`, which turns a name into an object. EMA is already given as an example — we fill in `return dsp.Median(window=MED_WINDOW)` and `return dsp.Kalman1D(q=KAL_Q, r=KAL_R)`, which must always be keyword arguments. If you forget these two, the app still runs with EMA, but selecting Median or Kalman makes the function return `None`, which crashes when `update` is called.

`read_raw()` reads `sensors.bmi270.acceleration()` and collapses it into a magnitude, `mag = (ax*ax + ay*ay + az*az) ** 0.5` (at rest, about 9.8), multiplied by 10 to show clearly on a 0..250 graph, since this lesson's filters are one-dimensional, so the vector must be turned into a scalar first. Radar range mode reads `sensors.radar_range()` in centimetres, wrapped in `try/except OSError`. The heart of this lesson is the single line `y = filt.update(x)`, which never needs to know what kind of filter `filt` is, because every one shares the same API. If you forget to fill it in (`y = x`), the two graphs will match exactly — a simple test of whether you've filled it in correctly.

We measure smoothness from **frame-to-frame jitter**: the sum of |x − x_prev| for the raw line versus the filtered line, then `red = (1 − filt_jit / raw_jit) × 100`. With a real sensor, we have no answer key for what the true value is, so a reduction in jitter is a straightforward indicator. Success isn't "the line looks nice" — you should be able to say why Median beats EMA when a spike hits, and why a smaller α gets smoother but slower to follow.

## Worked example

`s08_filters_full.py` adds sliders to tune parameters live, depending on the filter type (α for EMA, window for Median, r for Kalman), a noise-down bar that changes colour by threshold, and a Freeze button to pause the picture and compare the spike against the smooth line.

| File | What this file teaches |
|---|---|
| [examples/s08_filters_full.py](examples/s08_filters_full.py) | Cleaning a signal with DSP filters (full version) |

## Practice

The 5 `# TODO:` comments are at lines 46 (Median), 49 (Kalman1D), 99 (acceleration magnitude), 144 (`filt.update`), and 148 (plotting the two graphs). Fill in one at a time, then move the board and switch through all three filters. If the two graphs never differ, check point 144 first.

| Practice file | Topic |
|---|---|
| [practice/s08_filters.py](practice/s08_filters.py) | Cleaning a signal with DSP filters (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s08_filters.py](solution/s08_filters.py) | [practice/s08_filters.py](practice/s08_filters.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You've filled in the file, but the Filtered line matches the Raw line exactly, no matter which filter you choose. Which point is still empty? *(single choice · objective 1)*
   - a) return dsp.Median(window=MED_WINDOW)
   - b) mag = (ax*ax + ay*ay + az*az) ** 0.5
   - c) y = filt.update(x)
   - d) raw_chart.value(clamp(x))

   <details><summary>Solution</summary>

   **c** — the placeholder y = x means the value drawn on the lower line is the raw value. The two graphs only differ once the value genuinely passes through filt.update.

   </details>

2. You write return dsp.Median(5) at point 1, then select Median. What happens? *(single choice · objective 1)*
   - a) You get the 5-value window you wanted
   - b) It throws TypeError, because window is a keyword-only parameter
   - c) You get a 6-value window
   - d) The filter becomes EMA

   <details><summary>Solution</summary>

   **b** — dsp's filter parameters are keyword-only. You must write dsp.Median(window=5) — passing it positionally is rejected immediately.

   </details>

3. You tap the board hard once, creating a spike. What would you expect to see on the Filtered line for EMA versus Median? *(single choice · objective 2)*
   - a) Both remove it equally well
   - b) EMA smooths it into a soft bump that's still visible; Median votes the spike away until it's barely visible
   - c) EMA removes it entirely; Median smooths it into a bump
   - d) Both flatten the line to zero

   <details><summary>Solution</summary>

   **b** — EMA weighs the outlier into the result partially; Median picks the middle value, so it ignores a lone outlier entirely. This is the difference between "smoothing" and "voting it out".

   </details>

4. raw_jit = 400 and filt_jit = 100. What's the noise down %? *(single choice · objective 3)*
   - a) 25%
   - b) 75%
   - c) 100%
   - d) 400%

   <details><summary>Solution</summary>

   **b** — red = (1 − 100/400) × 100 = 75%. The filtered line's jitter is down to a quarter of the raw line's.

   </details>

## Lab

**The MVP for lessons 4.1–4.2:** a filter visibly improves a noisy sensor signal — the Filtered line is clearly smoother than Raw, confirmed with a noise-down % figure.

- [ ] All five points in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Switch through all three filters on the same signal, and note each one's noise-down % in your learning log.
- [ ] Create a spike (tap the board hard once, or use the board's radar), and explain why Median beats EMA.
- [ ] Be able to explain which filter you'd choose, why, and what the smoothness-versus-response trade-off is.

## Going further

In the next pair of lessons (4.3–4.4), we'll look at the same signal in the frequency domain with FFT.

Next lesson: [lesson 4.3 — FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window](../l03-fft-frequency-domain/README.md)

## Reflect

- If you chained Median followed by EMA, what result would you expect, and what would you be trading off?
- Is the highest noise-down % always the best outcome? Think of a job that needs a fast response.
