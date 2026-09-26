# Module 2 — Collecting sensor data (DAQ)

> Data acquisition (DAQ) · [Course page](../README.md)

Collect sensor data that matches what the model needs: sampling rate, Nyquist, windows, the CSV schema, and recording the IMU and audio on one shared timeline.

## Module goal

Collect trustworthy raw data, because a clean upstream is the first condition for an accurate model.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [2.1](l01-sampling-and-schema/README.md) | Sampling to match the model: rate, Nyquist, windows and the CSV schema | 60 | [slides.md](l01-sampling-and-schema/slides.md) |
| [2.2](l02-daq-logger-lab/README.md) | Hands-on: a DAQ logger that saves a dataset to CSV | 75 | [slides.md](l02-daq-logger-lab/slides.md) |
| [2.3](l03-audio-and-timeline/README.md) | Audio and several sensors on one timeline: PDM at 16 kHz, timestamps and jitter | 60 | [slides.md](l03-audio-and-timeline/slides.md) |
| [2.4](l04-multicapture-lab/README.md) | Hands-on: recording the IMU and audio into one file | 75 | [slides.md](l04-multicapture-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] A logger that genuinely saves N labelled samples to CSV, letting you choose the label, sampling at a steady rate, writing to a file on the board, and verifiable for the correct number of lines (lesson 2.2).
- [ ] A dataset logging at least two sensors on one shared timeline: the `/multicapture.csv` file has columns `t_ms` + IMU + `db`, with real values changing with motion and sound (lesson 2.4).
