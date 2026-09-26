---
id: edgeai-dev.m04.l03
lang: en
title: {th: 'FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window', en: 'The FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window'}
summary: {th: มองสัญญาณในโดเมนความถี่ เข้าใจว่า FFT แยกสัญญาณเป็นไซน์หลายความถี่อย่างไร แปลง bin เป็น Hz ด้วย f = k·FS/N รู้จัก bin width และ Nyquist เลือก N อย่างมีเหตุผล และจัดการศัตรูของสเปกตรัมด้วยการตัด DC Hann window และ magnitude, en: 'See signals in the frequency domain - how the FFT splits a signal into sines, converting a bin to Hz with f = k·FS/N, bin width and Nyquist, choosing N sensibly, and handling the spectrum''s enemies with DC removal, a Hann window and the magnitude.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l02]
objectives:
  - {th: อธิบายความต่างของโดเมนเวลากับโดเมนความถี่ และเหตุผลที่โมเดลเสียงดูสเปกตรัมแทนคลื่นดิบได้อย่างน้อยสองข้อ, en: Explain the difference between the time and frequency domains and give at least two reasons audio models look at the spectrum rather than the raw wave.}
  - {th: คำนวณความถี่ของ bin ด้วย f = k·FS/N bin width = FS/N และ Nyquist = FS/2 ได้ และเลือก N ให้เหมาะกับงานโดยบอกข้อแลกเปลี่ยนระหว่างความละเอียดกับความไว, en: 'Compute a bin''s frequency with f = k·FS/N, the bin width FS/N and Nyquist FS/2, and choose N for a task by stating the resolution-versus-responsiveness trade-off.'}
  - {th: อธิบายว่าทำไมต้องลบค่าเฉลี่ย (ตัด DC) คูณ Hann window และหา magnitude √(re² + im²) เฉพาะครึ่งแรกของ bin ก่อนอ่านสเปกตรัม, en: 'Explain why you subtract the mean (remove DC), multiply by a Hann window and take the magnitude √(re² + im²) over the first half of the bins before reading the spectrum.'}
  - {th: ตรวจความถูกต้องของ FFT ด้วยไซน์ที่รู้ความถี่ล่วงหน้า และทำนายได้ว่า peak ควรอยู่ที่ bin ใด, en: Check an FFT with a sine of known frequency and predict which bin the peak should land in.}
develops: [{skill: sys.dsp, to: 3}, {skill: hw.math, to: 2}, {skill: test.unit-tdd, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 48ea0f8629cc958b8f150769a5ebffcf9480255d1a53a19c47b4265bdc4de3a9
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.3 — The FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

See a signal in the frequency domain. Understand how the FFT splits a signal into sines of several frequencies, convert a bin to Hz with f = k·FS/N, know bin width and Nyquist, choose N sensibly, and handle the spectrum's enemies with DC removal, a Hann window and the magnitude.

## Objectives

By the end of this lesson, you will:

1. Explain the difference between the time and frequency domains, and give at least two reasons audio models look at the spectrum instead of the raw wave.
2. Compute a bin's frequency with f = k·FS/N, the bin width FS/N and Nyquist FS/2, and choose N for a task by stating the resolution-versus-responsiveness trade-off.
3. Explain why you subtract the mean (removing DC), multiply by a Hann window, and take the magnitude √(re² + im²) over only the first half of the bins before reading the spectrum.
4. Check an FFT's correctness with a sine of known frequency, and predict which bin the peak should land in.

## Before you start

You've been through lessons 4.1–4.2, and understand time-domain filters, and remember the Nyquist rule from lesson 2.1. If you have time, download [`math_lab.html`](../../shared/interactive/math_lab.html) and open it in a browser (needs internet to load GeoGebra) to try sliding the frequency of a mixed wave.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 4.2 — Hands-on: cleaning a live signal with a filter](../l02-filters-lab/README.md)

## See it work first

Run `s09_fft_spectrum_full.py` (in lesson 4.4) and shake the board up and down slowly, then quickly. The spectrum bars move, and the dominant frequency shifts with the rhythm. See "energy moving between frequencies" first, then ask how it knows.

## Concepts

The same signal can be viewed two ways. The **time domain** says when it's high and when it's low; the **frequency domain** says which frequency is strong. Audio models choose the latter, because the same sound played twice never matches in the time domain, but the way energy spreads across frequencies stays similar. The spectrum also compresses 16,000 points per second down to a few dozen values, and frequency carries physical meaning. Fourier's core idea is that any signal can be written as a sum of sines at several frequencies. The FFT asks back: "which sine frequencies are present, and how strong is each?"

The **FFT** is a fast way to compute the DFT, $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N}$, taking N points (a power of two) and returning N complex values, in $N\log N$ time instead of $N^2$. Bin k has frequency $f_k = k F_S / N$; the bin width $F_S/N$ is the resolution, and Nyquist $F_S/2$ is the ceiling. At $F_S = 50$ Hz and $N = 32$, one bin is 1.5625 Hz wide, bin 4 is 6.25 Hz, and you can read up to 25 Hz. Choosing N is a trade-off: a larger N tells nearby frequencies apart but needs a longer capture (N = 64 takes about 1.28 seconds); a smaller N updates faster but merges nearby frequencies into one bin.

A spectrum has enemies that must be handled before reading it: (1) **DC** — an accelerometer lying still has constant gravity, which piles up at bin 0 and drowns out everything else. Fixed by subtracting the window's mean. (2) **Spectral leakage** — the edges of a signal chunk don't line up exactly with the signal's period, so energy leaks into neighbouring bins. Fixed with a Hann window, $w[i] = 0.5 - 0.5\cos(2\pi i/(N-1))$, which pushes the edges to zero, at the cost of a slightly fatter peak. (3) The result is complex numbers — we only care about the magnitude, $|X[k]| = \sqrt{re^2 + im^2}$, and only use the first half (`HALF = N//2`), since the second half is a mirror image. Then find the dominant bin, skipping bin 0, and convert it to Hz. Before trusting an FFT against real data, always check it with a sine whose answer you already know — for example, a 6.25 Hz sine must give a peak at bin 4.

## Worked example

This lesson's slides also reference a file under `shared/`:

- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which of these are reasons audio models look at the spectrum instead of the raw wave? (select every correct answer) *(multiple choice · objective 1)*
   - a) The same sound played twice has a different waveform, but a similar energy distribution across frequencies
   - b) The spectrum compresses the data shorter, so the model is smaller and faster
   - c) Frequency carries physical meaning that can be read
   - d) The FFT makes the sound louder

   <details><summary>Solution</summary>

   **a, b, c** — the first three are the reasons in the slides. The FFT doesn't change loudness — it only changes the viewpoint from time to frequency.

   </details>

2. FS = 50 Hz and N = 32. What frequency is bin 3? *(single choice · objective 2)*
   - a) 3 Hz
   - b) 4.69 Hz
   - c) 6.25 Hz
   - d) 25 Hz

   <details><summary>Solution</summary>

   **b** — f = k·FS/N = 3 × 50 / 32 ≈ 4.69 Hz. One bin is 1.5625 Hz wide.

   </details>

3. If you increase N from 32 to 128 at FS = 50 Hz, what's the result? *(single choice · objective 2)*
   - a) Bins get wider, updates get faster
   - b) Bins narrow to about 0.39 Hz, telling nearby frequencies apart, but capturing takes about 2.56 seconds, so the spectrum updates more slowly
   - c) Nyquist rises to 100 Hz
   - d) No effect, since the FFT works with any N

   <details><summary>Solution</summary>

   **b** — bin width = FS/N, while Nyquist depends only on FS. Frequency resolution and time responsiveness always trade off against each other.

   </details>

4. The board lies still, and you see bin 0's bar towering over everything else. Which step was skipped? *(single choice · objective 3)*
   - a) Removing DC by subtracting the window's mean
   - b) Multiplying by a Hann window
   - c) Taking the magnitude
   - d) Finding the peak

   <details><summary>Solution</summary>

   **a** — gravity is a constant value, which is 0 Hz in the frequency domain, so it piles up at bin 0. The mean must be subtracted before the FFT.

   </details>

5. You generate a 12.5 Hz sine at FS = 50 Hz, N = 32, and feed it into the FFT. Which bin should the peak land in? *(single choice · objective 4)*
   - a) bin 4
   - b) bin 8
   - c) bin 12
   - d) bin 16

   <details><summary>Solution</summary>

   **b** — k = f·N/FS = 12.5 × 32 / 50 = 8 exactly. If the FFT is correct, the peak must be at bin 8.

   </details>

## Lab

- [ ] Compute the frequency of bins 1, 3 and 8 at FS = 50 Hz, N = 32, and note them in your learning log.
- [ ] In the REPL, do the sanity check with a 6.25 Hz sine as in the slides, then try 5 Hz and see which bins the peak splits between.
- [ ] Choose N for a task that must tell a 3.0 Hz vibration apart from a 3.5 Hz one, at FS = 50 Hz, with your reasoning.

## Going further

In lesson 4.4, we'll fill in a four-step pipeline in `s09_fft_spectrum.py` and read a live spectrum from the IMU with our own eyes.

Next lesson: [lesson 4.4 — Hands-on: a live spectrum from the IMU](../l04-fft-spectrum-lab/README.md)

## Reflect

- What job around you would "frequency" tell you more about than "a value over time" — such as a motor starting to fail?
- If you needed a spectrum that updates fast and is finely resolved at the same time, how would you solve that?
