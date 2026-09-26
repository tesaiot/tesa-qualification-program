# Edge AI Developer: From Sensor to On-Device Model

> Adapted from Edge AI Developer, © 2026 Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU) · BENTO & TESAIoT (CC BY 4.0 / MIT)

Thai version: [README.md](README.md). The lessons, slides and code comments are in Thai (technical terms and code in English).

Learn **edge AI** end to end on a real PSoC Edge board (**TESAIoT Dev Kit**: Cortex-M33 + Cortex-M55 + Ethos-U55 NPU) in **MicroPython**. You start by running the models that ship on the board, so you see where the course ends, then follow the five pillars of the data lifecycle:

**data acquisition (DAQ) → processing → signal analysis → training → edge AI apps**

Along the way you train your own model on a PC and take the same file to the MCU, the browser and a Cortex-A board, open the stack from MicroPython down to the NPU, and finish with a capstone you can ship. Every lesson follows PRIMM: see a working thing first, then take it apart, modify it and make your own.

## Who it is for

- Developers and learners who already write MicroPython and Python (for example after AIoT in Action) and want edge AI on a real device
- Engineers who want the whole path from raw data to a model on an NPU, not just an API call
- Educators who want lessons with slides, code, practice files and solutions

No machine-learning background is needed. The maths (trigonometry, basic statistics, the FFT, softmax) is explained step by step in the slides.

## Outcomes

1. Explain the five-stage edge AI data lifecycle, and use the edge_ai module to pick a model from the registry, read its verdict and wire it to an action on the board.
2. Log labelled sensor data to CSV at a steady sample rate, and prepare a balanced dataset with a stratified train/val/test split and no data leakage.
3. Turn raw signals into physical quantities and features with filters, the FFT and sliding windows, and measure the effect of each step with numbers.
4. Train a Conv1D model in Docker, quantise it to int8, and measure its accuracy and latency on the PC, the web and the MCU through Vela, proving parity within a tolerance.
5. Build edge AI apps that resist false positives with CONF_FLOOR, debounce and cooldown, fuse the verdict with a raw sensor, and publish events over MQTT.
6. Explain the stack from MicroPython down to the NPU, add a model to the firmware, and deliver a capstone that crosses at least three pillars with design reasons backed by measurements.

## What you need

- **A board**: TESAIoT Dev Kit (PSoC Edge E84) with the BENTO MicroPython firmware — **or start without a board** in the BENTO Emulator (it simulates sensors and model results; some lessons need the real board, see each lesson's hardware line)
- **BENTO IDE** — <https://ide.tesaiot.dev/> write code and press **Program to Device** from the browser; the BENTO Emulator is built in
- **A PC** with Python 3 and numpy (module 5) and Docker for training, or Google Colab instead of Docker
- **WiFi** for lesson 6.6 (MQTT to a public broker)
- **ModusToolbox** and the [TESAIoT PSE84 DevKit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) if you do the add-a-model firmware part of module 7
- A notebook or file for your own **learning log**; the slides and labs say what to record

## Course map

Eight modules, 42 lessons: about 60 hours as in the source course (20 sets of about three hours); the lesson estimates here add up to about 50 hours, and the rest is data collection, training and capstone time that varies by learner. Concept lessons are followed by a **hands-on** lesson.

| Module | Lessons | Hours (approx.) | Topic |
|---|---|---|---|
| [Module 1 — Getting started: run the real thing, then take it apart](m01-onboarding/README.md) | 7 | 7.8 | Run a real edge AI model first, then take a sensor app and an edge AI app apart to see the shared four-beat skeleton, the model registry and the path from verdict to action. |
| [Module 2 — Data acquisition (DAQ)](m02-daq/README.md) | 4 | 4.5 | Acquire sensor data the way a model needs it: sample rate, Nyquist, windows, a CSV schema, and IMU plus sound on one timeline. |
| [Module 3 — Processing with maths and physics](m03-processing/README.md) | 4 | 4.6 | Turn raw numbers into physical quantities (tilt, energy, altitude, dBFS), derived metrics such as dew point and heat index, and classify with rules before reaching for ML. |
| [Module 4 — Signal analysis](m04-analysis/README.md) | 6 | 7.0 | Clean signals with DSP filters, look at them in the frequency domain with the FFT, and squeeze sliding windows into the feature vectors a model actually sees. |
| [Module 5 — Training and deploying to several targets](m05-training/README.md) | 9 | 10.7 | Prepare a balanced dataset, train your own model in Docker, quantise it to int8, and take the one file to the web, Cortex-A and the MCU through Vela while measuring parity. |
| [Module 6 — Edge AI apps](m06-apps/README.md) | 6 | 7.2 | Build apps focused on one model, wire verdicts to actions through a pipeline that resists false positives, fuse them with a raw sensor, and publish events over MQTT. |
| [Module 7 — Under the hood and extending the firmware](m07-under-the-hood/README.md) | 4 | 4.8 | Take the stack apart from MicroPython across IPC to ai_engine and the NPU, then use that map to make your own model appear in edge_ai.models(). |
| [Module 8 — Capstone: your own edge AI app](m08-capstone/README.md) | 2 | 3.8 | Design, build and ship the Guardian, an edge AI app that threads three pillars through one loop, with design reasons backed by measurements. |

<details><summary>All lessons</summary>

**Module 1 — Getting started: run the real thing, then take it apart**

- [Lesson 1.1 — What edge AI is: the five-stage data lifecycle and where a model can run](m01-onboarding/l01-edge-ai-lifecycle/README.md)
- [Lesson 1.2 — The edge_ai module: list the models, select one, read its answer](m01-onboarding/l02-edge-ai-module/README.md)
- [Lesson 1.3 — Hands-on: your first model menu](m01-onboarding/l03-first-inference-lab/README.md)
- [Lesson 1.4 — Taking a sensor app apart: the four-beat skeleton of every program](m01-onboarding/l04-sensor-app-anatomy/README.md)
- [Lesson 1.5 — Hands-on: remix it into your own Tilt Monitor](m01-onboarding/l05-sensor-remix-lab/README.md)
- [Lesson 1.6 — Taking an edge AI app apart: the registry, the verdict and the action](m01-onboarding/l06-edge-ai-app-anatomy/README.md)
- [Lesson 1.7 — Hands-on: from verdict to action on the board](m01-onboarding/l07-verdict-action-lab/README.md)

**Module 2 — Data acquisition (DAQ)**

- [Lesson 2.1 — Sampling to match the model: rate, Nyquist, windows and the CSV schema](m02-daq/l01-sampling-and-schema/README.md)
- [Lesson 2.2 — Hands-on: a DAQ logger that writes a CSV dataset](m02-daq/l02-daq-logger-lab/README.md)
- [Lesson 2.3 — Audio and several sensors on one timeline: 16 kHz PDM, timestamps and jitter](m02-daq/l03-audio-and-timeline/README.md)
- [Lesson 2.4 — Hands-on: IMU and sound in one file](m02-daq/l04-multicapture-lab/README.md)

**Module 3 — Processing with maths and physics**

- [Lesson 3.1 — From raw numbers to physical quantities: tilt, energy, altitude and dBFS](m03-processing/l01-physics-quantities/README.md)
- [Lesson 3.2 — Hands-on: four physics gauges on screen](m03-processing/l02-physics-gauges-lab/README.md)
- [Lesson 3.3 — Derived metrics and rule-based classification: dew point, heat index and the rule ladder](m03-processing/l03-rules-before-ml/README.md)
- [Lesson 3.4 — Hands-on: a rule-based comfort classifier](m03-processing/l04-rule-classifier-lab/README.md)

**Module 4 — Signal analysis**

- [Lesson 4.1 — DSP filters: EMA, Median, Kalman and the radar range profile](m04-analysis/l01-dsp-filters/README.md)
- [Lesson 4.2 — Hands-on: cleaning a live signal with a filter](m04-analysis/l02-filters-lab/README.md)
- [Lesson 4.3 — The FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window](m04-analysis/l03-fft-frequency-domain/README.md)
- [Lesson 4.4 — Hands-on: a live spectrum from the IMU](m04-analysis/l04-fft-spectrum-lab/README.md)
- [Lesson 4.5 — Features and windowing: what the model actually sees](m04-analysis/l05-features-and-windowing/README.md)
- [Lesson 4.6 — Hands-on: a feature vector from a sliding window](m04-analysis/l06-windowing-lab/README.md)

**Module 5 — Training and deploying to several targets**

- [Lesson 5.1 — Dataset engineering: class balance, windows and the train/val/test split](m05-training/l01-dataset-engineering/README.md)
- [Lesson 5.2 — Hands-on: capture a balanced dataset on the board, split it on the PC](m05-training/l02-dataset-lab/README.md)
- [Lesson 5.3 — Training in Docker: one artifact, four targets](m05-training/l03-training-pipeline/README.md)
- [Lesson 5.4 — Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix](m05-training/l04-inside-training/README.md)
- [Lesson 5.5 — Hands-on: complete the training script and run it in Docker](m05-training/l05-train-lab/README.md)
- [Lesson 5.6 — Running the model on the web: LiteRT.js, int8 I/O and parity](m05-training/l06-web-runtime/README.md)
- [Lesson 5.7 — Hands-on: a web verdict that matches the PC, and the Cortex-A story](m05-training/l07-web-parity-lab/README.md)
- [Lesson 5.8 — Quantize and Vela: putting our model on the Ethos-U55](m05-training/l08-quantize-and-vela/README.md)
- [Lesson 5.9 — Hands-on: comparing three targets, MCU, web and PC](m05-training/l09-three-targets-lab/README.md)

**Module 6 — Edge AI apps**

- [Lesson 6.1 — Six models and the edge_ai API: an app focused on one model](m06-apps/l01-focused-apps/README.md)
- [Lesson 6.2 — Hands-on: your own focused app](m06-apps/l02-focused-app-lab/README.md)
- [Lesson 6.3 — The action pipeline: CONF_FLOOR, debounce, cooldown and on_result](m06-apps/l03-action-pipeline/README.md)
- [Lesson 6.4 — Hands-on: an action pipeline that resists false positives](m06-apps/l04-action-pipeline-lab/README.md)
- [Lesson 6.5 — Sensor fusion: the model's verdict with the raw sensor](m06-apps/l05-sensor-fusion/README.md)
- [Lesson 6.6 — Hands-on: send the fused event over MQTT](m06-apps/l06-fusion-iot-lab/README.md)

**Module 7 — Under the hood and extending the firmware**

- [Lesson 7.1 — The edge AI stack: tri-core, ai_engine, the IPC model link and TFLite-Micro](m07-under-the-hood/l01-edge-ai-stack/README.md)
- [Lesson 7.2 — Hands-on: tracing the stack from MicroPython](m07-under-the-hood/l02-trace-the-stack-lab/README.md)
- [Lesson 7.3 — Adding your own model: three edits, a four-function contract and Vela](m07-under-the-hood/l03-add-your-own-model/README.md)
- [Lesson 7.4 — Hands-on: make a new model appear in edge_ai.models()](m07-under-the-hood/l04-extend-model-lab/README.md)

**Module 8 — Capstone: your own edge AI app**

- [Lesson 8.1 — Designing the capstone: Guardian, three pillars in one file](m08-capstone/l01-capstone-design/README.md)
- [Lesson 8.2 — Hands-on: build and ship an edge AI app](m08-capstone/l02-capstone-build-lab/README.md)

</details>

## What is in each lesson

| File | What it is |
|---|---|
| `README.md` | Objectives, preparation, the concept in brief, the code files, the lab and a quiz |
| `slides.md` | The lesson's slides (Marp) |
| `examples/` | Examples and full versions that run as they are |
| `practice/` | Practice files with `# เติม` (fill in) gaps (hands-on lessons) |
| `solution/` | Solutions, with the same file names as the practice files |
| `quiz.yaml` | Check-for-understanding questions tied to the objectives |

Running MicroPython code: open the file in BENTO IDE and press **Program to Device** (board) or **Run** (BENTO Emulator). Code files keep the source numbering, for example `s11_dataset.py`.

The PC tools of module 5 are in [`shared/training/`](shared/training/README.md) (`dataset_tools.py`, `train.py`, `eval_pc.py`, `convert_web.py`, `quantize_vela.sh`, the `Dockerfile` and a Colab notebook). The interactive maths page [`shared/interactive/math_lab.html`](shared/interactive/math_lab.html) must be downloaded and opened in a browser (it loads GeoGebra from the internet).

## Limits to know

- The **BENTO Emulator** simulates sensors and model results (except the Motion model with its REAL switch on, which runs through ONNX Runtime Web). It has no Push model, its HW panel moves only the accelerometer, and its sound models never beat the unlabelled class. Real latency and real sound need the board.
- The Cough, Alarm and Siren models are DEEPCRAFT Ready Models by Imagimob AB, an Infineon Technologies company, licensed for evaluation only and metered. Motion, Baby Cry and Push are DEEPCRAFT Studio exports, also Imagimob's. None of these model files is in this repository.
- On the TESAIoT Dev Kit, opening the PDM microphone from MicroPython still clashes with the audio clock; the examples that read raw sound (lessons 2.3–2.4 and example 10) were tested by the author on the PSoC Edge AI Kit. Sound models through `edge_ai` work.
- The BENTO firmware source and the internal architecture notes cited in module 7 are not published. What you can check is the headers and documentation in the [public SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk), which adds a model with `ai_engine_register()` instead of editing `ai_engine.c`.

## Changes from the original

This course adapts the 20 Edge AI Developer decks. Facts that did not match the public SDK, the BENTO Emulator or a re-run of
the tools are corrected in the lessons. The main ones:

- `motion()` returns m/s², so the energy formula divides by 9.81, and pitch is `atan2(−ax, …)`.
- `dataset_tools.py` gives 143 windows split 101/21/21 (the decks said 142 and 100/22/22), and the split formula matches `split()`.
- Forgetting `representative_dataset` in the int8 conversion raises ValueError; it does not quietly lose accuracy.
- The Emulator has 5 models (no Push). Its results are simulated except the Motion model, which really runs through ONNX
  Runtime Web, and it cannot load a learner's model, so the web parity lab runs in the learner's own page.
- The firmware `wifi` module has no `rssi()`, so the examples read `status()["rssi"]`; `ui.tone` takes (note, wave, velocity, ms).
- References to internal documents that are not public now point to the headers and docs of the public SDK.
- `train.py` gains the `--save-keras` option that `convert_web.py` needs.

Accuracy and latency figures in the lessons are the author's and have not been re-measured on a board.

## Licences

- **Content** (slides, READMEs, own diagrams and screenshots) — CC BY 4.0
- **Code** (`examples/`, `practice/`, `solution/`, `shared/`) and the reference model `shared/training/model_int8.tflite` — MIT, Copyright (c) 2026 Wiroon Sriborrirux (full licence text in the repository's `LICENSES/MIT.txt`)
- **Third-party images** keep their own licences; authors, sources and licences are listed in [credits.yaml](credits.yaml)
- **The DEEPCRAFT models** the board uses belong to Imagimob AB (an Infineon Technologies company); this repository's licences do not cover them

## Source

Adapted from the **Edge AI Developer** course by Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU) (2026-09 edition). The 20 decks were split into 42 lessons in eight modules, the facts were checked against the BENTO firmware, the BENTO Emulator and the public SDK, and the wording was adapted for a general audience. BENTO & TESAIoT.

## How to cite TESA

When you use, adapt or redistribute this course or part of it, credit it as follows (add "(adapted)" after the title if you changed it, and keep the original author's credit):

> "Edge AI Developer: From Sensor to On-Device Model" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0 · Adapted from Edge AI Developer, © 2026 Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU) · BENTO & TESAIoT (CC BY 4.0 / MIT)

Attribution does not mean that TESA or Infineon endorse or certify your course or work. "TESA", "TQP" and "Certified by TESA and Infineon" are marks of the programme.
