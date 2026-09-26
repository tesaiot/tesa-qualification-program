---
id: edgeai-dev.m04.l04
lang: en
title: {th: 'ลงมือทำ: สเปกตรัมสดจาก IMU', en: 'Hands-on: a live spectrum from the IMU'}
summary: {th: เติม pipeline สี่ขั้นใน s09_fft_spectrum.py คือตัด DC คูณ Hann window หา magnitude และหา peak แล้วเขย่าบอร์ดดูแท่งสเปกตรัมกับความถี่เด่นเลื่อนตามจังหวะ พร้อมทดลองปิดทีละขั้นเพื่อเห็นว่าแต่ละขั้นแก้อะไร, en: 'Fill the four-step pipeline in s09_fft_spectrum.py (remove DC, apply a Hann window, compute the magnitude, find the peak), then shake the board to watch the bars and the dominant frequency follow your rhythm, and switch steps off one at a time to see what each fixes.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l03]
objectives:
  - {th: เติมสี่ขั้นใน practice/s09_fft_spectrum.py จนแท่งสเปกตรัมขยับตามการเขย่า และความถี่เด่นที่แสดงอยู่ใกล้จำนวนครั้งที่เขย่าต่อวินาที (เช่นเขย่า 3 ครั้งต่อวินาทีได้ราว 3 Hz), en: Fill the four steps in practice/s09_fft_spectrum.py until the spectrum bars follow your shaking and the displayed peak is close to your shakes per second (about 3 Hz for three shakes a second).}
  - {th: ทดลองรันแบบไม่ตัด DC และแบบไม่คูณ window แล้วอธิบายได้ว่าสเปกตรัมเปลี่ยนไปอย่างไรและเพราะอะไร, en: 'Run once without removing DC and once without the window, and explain how the spectrum changes and why.'}
  - {th: อธิบายได้ว่าการเก็บ N จุดด้วยการหน่วง 1000/FS ms สม่ำเสมอ และการ normalize แท่งด้วยยอดสูงสุด ส่งผลต่อการอ่านสเปกตรัมอย่างไร, en: Explain how collecting N points with an even 1000/FS ms delay and normalising the bars by the highest peak affect reading the spectrum.}
develops: [{skill: sys.dsp, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 1}]
assesses: [{skill: sys.dsp, level: 2, evidence: practice/s09_fft_spectrum.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 102d18c9a06b6db5908105b90d800dc25e042e6935162b919af253a8ab1a5e24
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.4 — Hands-on: a live spectrum from the IMU

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill a four-step pipeline in s09_fft_spectrum.py — remove DC, apply a Hann window, compute the magnitude, find the peak — then shake the board and watch the spectrum bars and the dominant frequency follow your rhythm, and switch off each step in turn to see what it fixes.

## Objectives

By the end of this lesson, you will:

1. Fill the four steps in practice/s09_fft_spectrum.py until the spectrum bars follow your shaking, and the displayed peak is close to your shakes per second (for example, three shakes per second gives about 3 Hz).
2. Run once without removing DC and once without the window, and explain how the spectrum changes and why.
3. Explain how collecting N points with an even 1000/FS ms delay, and normalising the bars by the highest peak, affect reading the spectrum.

## Before you start

You've been through lesson 4.3, and know how a bin converts to Hz and why DC must be removed and the window applied. Prepare three shaking rhythms (slow, medium, fast), and count the shakes per second for each to compare against.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 4.3 — The FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window](../l03-fft-frequency-domain/README.md)

## Concepts

The whole file reads as one sentence: collect N points → remove DC → apply the window → FFT → find the magnitude → find the peak → draw the bars. What's already given is collecting `az` from `sensors.bmi270.motion()`, 32 points, with an even `1000/FS` ms delay (an FFT only reads frequency correctly when the spacing is equal), a `fft()` function using radix-2 Cooley-Tukey, written in Python so you can read it as just organized addition and multiplication, and the bar drawing, created once before the loop.

The four steps we fill in are: (1) `mean = sum(buf) / N` (2) `re = [(buf[i] - mean) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1))) for i in range(N)]`, which removes DC and applies the window's shape in one line (3) `mag = [math.sqrt(re[k] * re[k] + im[k] * im[k]) for k in range(HALF)]`, and (4) `kmax = max(range(1, HALF), key=lambda k: mag[k])`, starting at 1 to skip bin 0, where leftover DC might linger. The dominant frequency is shown as `kmax * FS / N`. The bars are normalized by the highest peak, so they always fill the screen whether you shake hard or gently.

If you forget any step, the symptom tells you: skip removing DC and bin 0 towers over everything; skip the window and the peak's neighbouring bars leak higher than they should; skip the magnitude and the bars stay flat; skip finding the peak and the dominant frequency stays stuck at bin 1. Success isn't just watching the bars move — you should be able to say what a peak of 3 Hz actually means, and why shaking faster shifts the peak toward higher frequency.

## Worked example

`s09_fft_spectrum.py` in the examples folder is the reference version, using N = 64. `s09_fft_spectrum_full.py` adds EMA-averaging the spectrum to keep the bars steady, shows the dominant frequency large on a Seg7, holds the highest peak (peak-hold), and measures total energy (RMS).

| File | What this file teaches |
|---|---|
| [examples/s09_fft_spectrum.py](examples/s09_fft_spectrum.py) | From the time domain to the frequency domain (FFT) |
| [examples/s09_fft_spectrum_full.py](examples/s09_fft_spectrum_full.py) | A live FFT spectrum from the IMU (full version) |

## Practice

The 4 `# TODO:` comments are at lines 95 (remove DC), 100 (Hann window), 110 (magnitude), and 115 (peak). Replace the starting values with the calls the hints describe, then shake the board's Z axis, alternating fast and slow. If the bars never move, check your indentation and variable names first.

| Practice file | Topic |
|---|---|
| [practice/s09_fft_spectrum.py](practice/s09_fft_spectrum.py) | From the time domain to the frequency domain (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s09_fft_spectrum.py](solution/s09_fft_spectrum.py) | [practice/s09_fft_spectrum.py](practice/s09_fft_spectrum.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put the steps of s09_fft_spectrum.py's pipeline in order *(ordering · objective 1)*
   - a) fft(re, im)
   - b) mean = sum(buf) / N (remove DC)
   - c) kmax = max(range(1, HALF), key=...) (find the peak)
   - d) apply the Hann window
   - e) mag = sqrt(re² + im²) over the first half

   <details><summary>Solution</summary>

   **b → d → a → e → c** — remove DC → window → FFT → magnitude → peak. The FFT step is already given; the other four are the blanks we fill in.

   </details>

2. You've filled everything in. The bars move with the shaking, but the peak label stays stuck at 1.6 Hz (bin 1) forever. Which step is still unfilled? *(single choice · objective 1)*
   - a) Remove DC
   - b) Hann window
   - c) Magnitude
   - d) Find the peak (kmax is still its starting value, 1)

   <details><summary>Solution</summary>

   **d** — the placeholder kmax = 1 always points the dominant frequency at bin 1. It must be replaced with max(range(1, HALF), key=lambda k: mag[k]).

   </details>

3. If you don't apply the Hann window, how does the spectrum change? *(single choice · objective 2)*
   - a) Bin 0 towers over everything
   - b) The peak stays where it was, but the neighbouring bars leak higher than they should — the spectrum gets messy
   - c) All bars go flat
   - d) The dominant frequency disappears

   <details><summary>Solution</summary>

   **b** — a window edge that doesn't line up with the signal's period leaks energy (spectral leakage). Hann pushes the edges to zero, reducing the leak. Bin 0 towering is instead the symptom of not removing DC.

   </details>

4. If you remove `time.sleep_ms(int(1000 / FS))` from the loop that collects N points, what happens? *(single choice · objective 3)*
   - a) No effect, since the FFT doesn't care about timing
   - b) The real sampling rate is no longer FS, so converting kmax · FS / N to Hz becomes wrong
   - c) The spectrum always gets finer
   - d) The board restarts

   <details><summary>Solution</summary>

   **b** — the formula f = k·FS/N assumes points are equally spaced 1/FS seconds apart. If the real rate differs, the Hz value shown no longer matches reality.

   </details>

## Lab

**The MVP for lessons 4.3–4.4:** run `s09_fft_spectrum.py` and read a live spectrum — the frequency bars and the peak (Hz) genuinely change with faster or slower shaking.

- [ ] All four steps in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Shake at three rhythms (slow, medium, fast), note the peak in Hz for each in your learning log, and compare against the shakes-per-second you counted.
- [ ] Run once without removing DC (leave `mean = 0.0`) and once without the window, and explain how the spectrum changes.
- [ ] Be able to explain where the DC-removal, window, magnitude and peak steps sit in the pipeline, and what each does.

## Going further

In the next pair of lessons (4.5–4.6), we'll move on from the spectrum to a sliding window and a feature vector — what a model actually sees.

Next lesson: [lesson 4.5 — Features and windows: what a model actually sees](../l05-features-and-windowing/README.md)

## Reflect

- How closely did the peak you measured match the rhythm you counted yourself? If it was off, do you think that came from the bin resolution, or from your own hand?
- If you needed to inspect a motor spinning at 1,500 RPM, what's the minimum FS you'd need to set?
