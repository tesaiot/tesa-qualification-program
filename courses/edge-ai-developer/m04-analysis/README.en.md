# Module 4 — Signal analysis

> Signal analysis · [Course page](../README.md)

Clean a signal with DSP filters, look in the frequency domain with FFT, then squeeze a sliding window into the feature vector a model actually sees.

## Module goal

Understand that a model never sees a raw signal — it sees the features a front-end prepares for it, and that front-end must match everywhere.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [4.1](l01-dsp-filters/README.md) | DSP filters: EMA, Median, Kalman and the radar range profile | 65 | [slides.md](l01-dsp-filters/slides.md) |
| [4.2](l02-filters-lab/README.md) | Hands-on: filters cleaning a signal live | 75 | [slides.md](l02-filters-lab/slides.md) |
| [4.3](l03-fft-frequency-domain/README.md) | FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window | 65 | [slides.md](l03-fft-frequency-domain/slides.md) |
| [4.4](l04-fft-spectrum-lab/README.md) | Hands-on: a live spectrum from the IMU | 75 | [slides.md](l04-fft-spectrum-lab/slides.md) |
| [4.5](l05-features-and-windowing/README.md) | Features and windows: what a model actually sees | 65 | [slides.md](l05-features-and-windowing/slides.md) |
| [4.6](l06-windowing-lab/README.md) | Hands-on: a feature vector from a sliding window | 75 | [slides.md](l06-windowing-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] A filter visibly improves a noisy sensor signal — the Filtered line is clearly smoother than Raw, confirmed with a noise-down % figure (lesson 4.2).
- [ ] Run `s09_fft_spectrum.py` and read a live spectrum — the frequency bars and the peak (Hz) genuinely change with faster or slower shaking (lesson 4.4).
- [ ] Build a feature vector from a raw signal by hand: slice a window (window + hop), then squeeze it into mean, std and band values that change with motion (lesson 4.6).
