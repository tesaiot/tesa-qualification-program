# Edge AI Developer: From Sensor to On-Device Model

Level **L3** · status **pre-alpha (outline, being written)** · 7 modules, 20 lessons · about 40 hours

**The full course will be published once the author releases it.** The source Edge AI Developer course already has slides and code
and is under the author's review. This page therefore publishes only the outline: module and lesson titles, objectives written
for this repository, the skills developed and verified public references. No slides or code from the source course are in this folder.

The course follows the real data lifecycle in five pillars: **DAQ → processing → signal analysis → training → edge AI apps**.
It is MicroPython-first on the TESAIoT Dev Kit, uses the BENTO Emulator where real hardware is not needed, and trains models on a PC.
It starts by taking working apps apart (in the spirit of PRIMM) before learners build their own.

The lesson pages are Thai-first; English lesson pages are pending (`translation: pending`).

## Who it is for

- Developers and students who finished AIoT in Action or already write MicroPython and Python
- No prior machine learning needed
- A TESAIoT Dev Kit is needed for the microphone, radar and NPU lessons, and a PC for training

## Outcomes

1. Explain the five-stage edge AI data lifecycle and decide whether a problem needs an on-device model or a plain rule.
2. Capture multi-sensor data on one timeline and prepare a correctly labelled and split dataset.
3. Process and analyse signals with filters, FFT and windowing to build the features a model uses.
4. Train a small model, convert it for several targets, and compare results on PC, web and board.
5. Build an edge AI app that acts reliably on model results and sends events to an IoT platform.

## Modules and lessons

**Module 1 — Getting started and taking working apps apart** ([m01-onboarding](m01-onboarding/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m01.l01 | Edge AI and the data lifecycle | 70 min |
| edgeai-dev.m01.l02 | Taking a sensor app apart | 70 min |
| edgeai-dev.m01.l03 | Taking an edge AI app apart | 70 min |

**Module 2 — Data acquisition (DAQ)** ([m02-daq](m02-daq/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m02.l01 | Sampling and logging | 70 min |
| edgeai-dev.m02.l02 | Audio and multi-sensor capture on one timeline | 70 min |

**Module 3 — Processing with maths and physics** ([m03-processing](m03-processing/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m03.l01 | Maths, physics and visualisation | 70 min |
| edgeai-dev.m03.l02 | Derived metrics and rule-based classification | 70 min |

**Module 4 — Signal analysis** ([m04-analysis](m04-analysis/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m04.l01 | DSP filtering | 70 min |
| edgeai-dev.m04.l02 | FFT and the frequency domain | 70 min |
| edgeai-dev.m04.l03 | Features and windowing | 70 min |

**Module 5 — Training and deploying to several targets** ([m05-training](m05-training/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m05.l01 | Dataset engineering | 70 min |
| edgeai-dev.m05.l02 | Training with TensorFlow | 70 min |
| edgeai-dev.m05.l03 | Deploying to the web, and the small-Linux-computer story | 70 min |
| edgeai-dev.m05.l04 | Quantising and running on the NPU | 70 min |

**Module 6 — Edge AI apps** ([m06-apps](m06-apps/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m06.l01 | The shipped models and the edge_ai API | 70 min |
| edgeai-dev.m06.l02 | Action pipelines | 70 min |
| edgeai-dev.m06.l03 | Sensor fusion and IoT | 70 min |

**Module 7 — Under the hood, extending, and the capstone** ([m07-under-the-hood](m07-under-the-hood/README.md))

| Lesson | Topic | Time |
|---|---|---|
| edgeai-dev.m07.l01 | The edge AI stack under the hood | 70 min |
| edgeai-dev.m07.l02 | Extending with your own model | 70 min |
| edgeai-dev.m07.l03 | Capstone: a complete edge AI application | 75 min |

## Status

Pre-alpha, outline only: every lesson has objectives, skills and public references, but no content, practice or checks.
Full content, slides and code will be added when the author releases the source course.
C-side references link to the SDK at commit `ef72c1b`; MicroPython DSP examples link to AIoT in Action (MIT) at a pinned commit.

## Main references

- [SDK: แคตตาล็อกตัวอย่าง (หมวด edge_ai)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
- [TESAIoT PSE84 Dev Kit SDK README (ฮาร์ดแวร์โดยย่อ: Cortex-M55, Ethos-U55 NPU, เซนเซอร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [TensorFlow](https://www.tensorflow.org/)
- [LiteRT (เดิมชื่อ TensorFlow Lite) documentation](https://ai.google.dev/edge/litert)
- [TensorFlow Lite for Microcontrollers (tflite-micro)](https://github.com/tensorflow/tflite-micro)
- [Arm Ethos-U Vela compiler (PyPI: ethos-u-vela)](https://pypi.org/project/ethos-u-vela/)

## Licence

- Content (this outline): CC BY 4.0
- New code added to this course: Apache-2.0
- No code or slides from the source course are in this folder yet

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Edge AI Developer: From Sensor to On-Device Model" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
