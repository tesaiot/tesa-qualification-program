---
id: edgeai-dev.m01.l01
lang: en
title: {th: 'Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้', en: 'What edge AI is: the five-stage data lifecycle and where a model can run'}
summary: {th: รู้ว่า Edge AI ต่างจาก AI บนคลาวด์ตรงไหน เห็นวงจรชีวิตของข้อมูลห้าขั้นที่เป็นโครงของทั้งหลักสูตร และรู้ว่าโมเดลตัวเดียวไปรันได้ที่ไหนบ้าง บนบอร์ดที่มีคอร์ควบคุมกับคอร์ AI แยกกัน, en: 'Learn how edge AI differs from cloud AI, see the five-stage data lifecycle that structures the whole course, and where one model can run, on a board with separate control and AI cores.'}
level: L3
time_min: {concept: 45, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: []
objectives:
  - {th: 'อธิบายความต่างระหว่าง Cloud AI กับ Edge AI จากจุดที่การอนุมานเกิดขึ้น และยกเหตุผลที่ควรรันบนอุปกรณ์ได้อย่างน้อยสามข้อจากสี่ข้อ (latency, privacy, cost, offline)', en: 'Explain how cloud AI and edge AI differ by where inference happens, and give at least three of the four reasons to run on the device (latency, privacy, cost, offline).'}
  - {th: เรียงห้าขั้นของวงจรชีวิตข้อมูล DAQ → Processing → Analysis → Training → Apps ได้ถูกลำดับ และบอกได้ว่าแต่ละขั้นตรงกับโมดูลใดของหลักสูตร, en: Put the five lifecycle stages DAQ → Processing → Analysis → Training → Apps in order and name the module of this course that covers each.}
  - {th: 'จับคู่เป้าหมาย MCU, Web, Cortex-A และ PC กับสิ่งที่ต้องทำกับไฟล์ .tflite แบบ int8 และ runtime ที่ใช้ แล้วอธิบายว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela', en: 'Match the MCU, web, Cortex-A and PC targets to what each does with the int8 .tflite file and the runtime it uses, and explain why only the MCU needs Vela.'}
  - {th: บอกได้ว่าโค้ด MicroPython รันบน Cortex-M33 ส่วนโมเดลรันบน Cortex-M55 กับ Ethos-U55 และเลือกโมเดลจากตารางหกโมเดลให้ตรงกับเซนเซอร์ที่ต้องใช้, en: 'State that MicroPython runs on the Cortex-M33 while models run on the Cortex-M55 with the Ethos-U55, and pick the model from the six-model table that matches a given sensor.'}
develops: [{skill: ai.edge, to: 1}, {skill: ai.model-deploy, to: 1}, {skill: hw.architecture, to: 1}, {skill: biz.product-decision, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 10cc2a2f3298660f01db08f880dc0eb8d11e3b411a9d1bf06cd3b451b3b06ee9
---

# Lesson 1.1 — What edge AI is: the five-stage data lifecycle and where a model can run

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Learn how edge AI differs from cloud AI, see the five-stage data lifecycle that structures the whole course, and where one model can run, on a board with separate control and AI cores.

## Objectives

By the end of this lesson, you will:

1. Explain how cloud AI and edge AI differ by where inference happens, and give at least three of the four reasons to run on the device (latency, privacy, cost, offline).
2. Put the five lifecycle stages DAQ → Processing → Analysis → Training → Apps in order, and name the module of this course that covers each.
3. Match the MCU, web, Cortex-A and PC targets to what each does with the int8 .tflite file and the runtime it uses, and explain why only the MCU needs Vela.
4. State that MicroPython code runs on the Cortex-M33 while models run on the Cortex-M55 with the Ethos-U55, and pick the model from the six-model table that matches a given sensor.

## Before you start

Nothing much to prepare for this first lesson — it's pure concepts. Actually running a model comes in lessons 1.2 and 1.3. If you have time, open [BENTO IDE](https://ide.tesaiot.dev/) in another tab to get a look at the tool you'll use throughout the course.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/).

## See it work first

This course teaches **backwards**: start from something that already works, then take it apart to see how it works inside (the PRIMM approach: Predict → Run → Investigate → Modify → Make). Lessons 1.1–1.3 lead you to running a six-model menu on the board, which is stage 5 of the cycle, before stepping back to build things yourself from stage 1 in later modules.

## Concepts

**Edge AI** means running a model (inference) on the device where the data is generated, without sending raw data off to a server to think for it. Both cloud AI and edge AI can use the exact same model — they differ only in where inference happens. There are four reasons it's worth moving inference onto the device: low latency, data that never leaves the device (privacy), no per-call server cost, and it keeps working even offline. The price you pay is that the model has to be small and fast enough to fit on a tiny chip, which is exactly what this course teaches directly.

The course follows the **five-stage data lifecycle** engineers actually use: DAQ (collecting raw data, module 2) → Processing (maths and physics, module 3) → Analysis (DSP, FFT, features, module 4) → Training (training a model in Docker, module 5) → Apps (inference and taking action, module 6). Most edge AI courses only teach the last stage, but we'll also understand what a model "sees," and why it has to be squeezed so small.

A model trained once can run across the whole spectrum: on the **MCU + NPU** (a BENTO board, needing an extra Vela compile step so the Ethos-U55 can read it), on the **web** (LiteRT.js in a browser), on **Cortex-A** (Raspberry Pi, Jetson, a mini PC, using ai-edge-litert), and on a **PC** inside Docker. The int8 `.tflite` file is the single source of truth, because int8 is the common denominator: the MCU requires it, and everything else can accept it. You can learn from three different surfaces with the same one set of MicroPython code: the BENTO Emulator in your browser, a real board, and Python with Docker for training models.

The board has "two brains": the **Cortex-M55 (400 MHz) with the Ethos-U55 NPU** is where models run, while the **Cortex-M33 (200 MHz)** is the control core, and where our MicroPython code runs. When you call `edge_ai.result()`, code on the M33 pulls the result from the M55 across an on-chip communication channel (IPC). The firmware on the TESAIoT Dev Kit ships with six ready-to-use DEEPCRAFT models (Motion, Baby Cry, Push, Cough, Alarm, Siren), each tied to one sensor — the IMU, a microphone, or radar. These models are the work of Imagimob AB, an Infineon group company, built with DEEPCRAFT Studio. The BENTO Emulator has five of them (no Push Detection), so the order doesn't match the board — always find a model by its name.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which of these are reasons to run a model on the device instead of sending it to the cloud? (select every correct answer) *(multiple choice · objective 1)*
   - a) It can decide within a fraction of a second, with no round trip to a server
   - b) Raw audio and gestures never have to leave the device
   - c) A model on the device is always bigger and more accurate than one on the cloud
   - d) The device can still decide even if the network drops

   <details><summary>Solution</summary>

   **a, b, d** — the four reasons in the slides are latency, privacy, cost and offline. Size, on the other hand, is the trade-off of going to the edge: the model has to be small enough to run on a tiny chip, not bigger than a cloud one.

   </details>

2. Put the data lifecycle stages in the order this course follows *(ordering · objective 2)*
   - a) Training: train a model, then export it as .tflite
   - b) DAQ: collect raw data from a sensor
   - c) Apps: run inference, then take action
   - d) Analysis: DSP, FFT and features
   - e) Processing: maths and physics

   <details><summary>Solution</summary>

   **b → e → d → a → c** — DAQ → Processing → Analysis → Training → Apps, matching modules 2 through 6. This first set of lessons deliberately starts at Apps, but the real cycle starts from data.

   </details>

3. One single model_int8.tflite file runs on several targets. Which target needs an extra compile step? *(single choice · objective 3)*
   - a) A browser using LiteRT.js
   - b) An MCU board with an Ethos-U55, which needs Vela first
   - c) A Raspberry Pi using ai-edge-litert
   - d) A PC inside Docker

   <details><summary>Solution</summary>

   **b** — Vela converts part of the graph so the Ethos-U55 NPU can read it. Every other target can use the same int8 file directly, which is why int8 is the common denominator across every target.

   </details>

4. When MicroPython code calls edge_ai.result(), what happens? *(single choice · objective 4)*
   - a) The Cortex-M33 runs the model itself and returns the answer
   - b) Code on the Cortex-M33 pulls the latest inference result, computed by the Cortex-M55 and the Ethos-U55, over the on-chip communication channel
   - c) The board sends data to the cloud and waits for an answer
   - d) The Ethos-U55 runs the Python code instead of the M33

   <details><summary>Solution</summary>

   **b** — the model infers on the M55 and the NPU, while MicroPython runs on the M33. Calling result() pulls the result across cores over the on-chip communication channel.

   </details>

5. You want to detect someone reaching toward the board without using a camera or sound. Which model on the TESAIoT Dev Kit should you pick? *(single choice · objective 4)*
   - a) Motion Detection (IMU)
   - b) Cough Detection (MIC)
   - c) Push Detection (RADAR)
   - d) Siren Detection (MIC)

   <details><summary>Solution</summary>

   **c** — Push Detection uses 60 GHz radar, so it can detect a reaching hand without a camera. This model only exists on boards with radar — you won't see it in the list on the BENTO Emulator.

   </details>

## Going further

In the next lesson, we'll meet the `edge_ai` module's four commands, which take us from the model registry all the way to an answer on screen.

Next lesson: [lesson 1.2 — The edge_ai module: query the model registry, select, then read the answer](../l02-edge-ai-module/README.md)

## Reflect

- Which jobs at home or at work "must answer instantly" or "should never let data leave the machine," to the point they should really be edge AI?
- If a model can run both on a cheap chip and on a Jetson, what criteria would you use to decide where it belongs?
