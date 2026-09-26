---
id: edgeai-dev.m05.l08
lang: en
title: {th: 'quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55', en: 'Quantize and Vela: putting our model on the Ethos-U55'}
summary: {th: 'เป้าหมายสุดท้ายและยากที่สุดของ "train once, run everywhere" คือ MCU กับ Ethos-U55 เข้าใจว่าทำไม NPU ต้องมีขั้นคอมไพล์ Vela เพิ่ม ไฟล์ .tflite สามหน้าตาไปเป้าหมายใด สัญญาสี่ฟังก์ชัน AIM_* ที่ทำให้ edge_ai เรียกโมเดลได้ สองทางในการห่อโมเดล และเหตุผลที่ NPU เร็วและประหยัดกว่า', en: 'The last and hardest target of "train once, run everywhere" is the MCU with its Ethos-U55. Learn why the NPU needs an extra Vela compile, which of three .tflite packages goes where, the four-function AIM_* contract that lets edge_ai call a model, the two ways to wrap a model, and why the NPU is faster and cheaper per inference.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l07]
objectives:
  - {th: 'อธิบายได้ว่าทำไมมีแค่ MCU ที่ต้องคอมไพล์ด้วย Vela และจับคู่ไฟล์ model_int8, model_int8_vela และ model_web กับเป้าหมายที่ถูกต้อง', en: 'Explain why only the MCU needs a Vela compile, and match model_int8, model_int8_vela and model_web to the right targets.'}
  - {th: รัน quantize_vela.sh ใน Docker image เดิมจนได้ output/model_int8_vela.tflite และอธิบายตัวเลือก --accelerator-config ethos-u55-128 กับ --optimise Performance, en: 'Run quantize_vela.sh in the same Docker image to get output/model_int8_vela.tflite, and explain --accelerator-config ethos-u55-128 and --optimise Performance.'}
  - {th: 'อธิบายสัญญา AIM_* สี่ฟังก์ชัน (init, enqueue, dequeue, finalize) กับรหัสคืนค่า และบอกได้ว่ากับดักหลักของการห่อโมเดลคือ feature parity ไม่ใช่ตัวกราฟ', en: 'Describe the four-function AIM_* contract (init, enqueue, dequeue, finalize) and its return codes, and name feature parity, not the graph, as the main trap when wrapping a model.'}
  - {th: อธิบายว่าทำไม NPU จึงเร็วกว่าและใช้พลังงานต่อการอนุมานน้อยกว่า CPU และอ่านตารางเทียบโดยดู worst-case latency กับความผิดพลาดรายคลาสได้, en: 'Explain why the NPU is faster and uses less energy per inference than the CPU, and read a comparison table looking at worst-case latency and per-class errors.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: hw.architecture, to: 2}, {skill: build.vendor-sdk, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: a4cbb2a5ed660f38900f5ca723498103ce84bca14788db11b4a7491fa64f46c0
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.8 — Quantize and Vela: putting our model on the Ethos-U55

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

The last and hardest target of "train once, run everywhere" is the MCU with its Ethos-U55. Understand why the NPU needs an extra Vela compile, which of three .tflite files goes where, the four-function AIM_* contract that lets edge_ai call a model, the two ways to wrap a model, and why the NPU is faster and cheaper.

## Objectives

By the end of this lesson, you will:

1. Explain why only the MCU needs a Vela compile, and match model_int8, model_int8_vela and model_web to the right targets.
2. Run quantize_vela.sh in the same Docker image to get output/model_int8_vela.tflite, and explain the options --accelerator-config ethos-u55-128 and --optimise Performance.
3. Describe the four-function AIM_* contract (init, enqueue, dequeue, finalize) and its return codes, and name feature parity, not the graph, as the main trap when wrapping a model.
4. Explain why the NPU is faster and uses less energy per inference than the CPU, and read a comparison table looking at worst-case latency and per-class errors.

## Before you start

You've been through lessons 5.3–5.7, and have `model_int8.tflite` that passed `eval_pc.py`, and understand quantize and dequantize. Open [`quantize_vela.sh`](../../shared/training/quantize_vela.sh) to read alongside the slides.

- **Hardware:** your computer, no board needed — a PC with the same Docker image. The part that needs a board is in lesson 5.9.
- **Prior lesson:** [lesson 5.7 — Hands-on: a web verdict that matches the PC, and the Cortex-A story](../l07-web-parity-lab/README.md)

## See it work first

In the same Docker image, run `./quantize_vela.sh model_int8.tflite`, and look at the new file in `output/`. This `_vela.tflite` file can no longer be opened by a browser or a PC. Ask yourself: what does Vela change inside the file, and why shouldn't accuracy change after it?

## Concepts

Web, Cortex-A and PC can all run an ordinary TFLite graph directly, on CPU or GPU. But **an NPU is not a CPU** — it's a specialized int8 matrix-multiply circuit. **Vela** (Arm's `ethos-u-vela`) therefore takes a full-integer int8 `.tflite`, and replaces the subgraph the NPU can run with a single custom op named `ethos-u`. Whatever the NPU can't do is left for the Cortex-M55. `quantize_vela.sh` wraps the command `vela --accelerator-config ethos-u55-128 --optimise Performance` (a U55 at 128 MAC per cycle, tuned for speed), producing `output/model_int8_vela.tflite`, usable only on the MCU. At this point, there is **one set of weights, three packages**: `model_int8.tflite` (PC, Cortex-A, and Vela's source), `_vela.tflite` (MCU), and `model_web.tflite` (browser). Loading the wrong file in the wrong place fails to load immediately.

Vela doesn't touch the model's maths — $q = \mathrm{round}(x/s) + z$ and $x = (q - z)\cdot s$ still use the $s, z$ that PTQ embedded into every tensor, so accuracy on the NPU should match int8 on the PC (differing only at the level of kernel rounding). If the board diverges dramatically, suspect the front-end first — a Vela file still isn't a model the board recognizes. It must be **wrapped** with a four-function contract: `<SLOT>_init`, `<SLOT>_enqueue(const float *in)`, `<SLOT>_dequeue(float *out)`, and `<SLOT>_finalize` — Imagimob's IPWIN streaming ABI, which DEEPCRAFT Studio generates. `dequeue` returning −1 (NODATA) while the window isn't full yet is normal. There are two ways to wrap it: DEEPCRAFT's own converter, which generates C along with the front-end, or wrapping TFLite-Micro yourself and writing a front-end that matches training exactly. The number-one trap is mismatched features, not the graph. The BENTO firmware source this course uses isn't public yet — in the [public SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk), the engine ships as a prebuilt library, so a new model registers with `ai_engine_register()`, or replaces an existing slot, following the [Filling a model slot guide](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/proj_cm55/modules/ai_models/README.md).

The NPU isn't smarter than the CPU — it does one job, multiplying int8 matrices, with 128 parallel MAC circuits per cycle, so the same work finishes in far fewer cycles. Finishing quickly means waking the circuit briefly then going back to sleep, so energy per inference is correspondingly low. When reading a comparison table, watch for three things: overall accuracy can hide a missed class (check the confusion matrix), average latency hides the worst case, and the web can differ slightly because its activations are float.

## Worked example

This lesson's slides also reference files under `shared/`:

- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which file should be sent to a web page? *(single choice · objective 1)*
   - a) model_int8_vela.tflite
   - b) model_web.tflite, whose I/O is float and has no NPU custom op
   - c) model.keras
   - d) Any file works

   <details><summary>Solution</summary>

   **b** — the Vela file has the ethos-u op, which only runs on the NPU. model_web.tflite is built for the browser, and model_int8.tflite is used with the PC and Cortex-A.

   </details>

2. After running ./quantize_vela.sh model_int8.tflite, where is the MCU's file? *(single choice · objective 2)*
   - a) ./model_int8.tflite, overwriting the original
   - b) ./output/model_int8_vela.tflite
   - c) ./vela/model.bin
   - d) Directly on the board

   <details><summary>Solution</summary>

   **b** — Vela writes its result into the output folder, appending _vela to the name. The original int8 file remains, used for the PC and Cortex-A.

   </details>

3. AIM_GESTURE_dequeue returns −1 right after start. What does that mean? *(single choice · objective 3)*
   - a) The model is broken and needs reflashing
   - b) NODATA: the window hasn't finished collecting data yet — normal
   - c) The NPU is overheating
   - d) The winning class is −1

   <details><summary>Solution</summary>

   **b** — per the IPWIN ABI, −1 means no result yet. Keep enqueueing until the window is full, and dequeue then returns 0 with a score.

   </details>

4. int8 is 0.95 accurate on the PC, but the board gets nearly everything wrong. What should you suspect first? *(single choice · objective 3)*
   - a) Vela computed something wrong
   - b) The board's front-end (normalize, quantize, or the feature) doesn't match training
   - c) The NPU is too slow
   - d) It needs retraining with more epochs

   <details><summary>Solution</summary>

   **b** — Vela never touches the maths. A gap this large usually comes from data fed into the model on the board being at a different scale or a different feature than during training.

   </details>

5. Why does the Ethos-U55 use less energy per inference than the Cortex-M55 doing it itself? *(single choice · objective 4)*
   - a) Because it uses float32
   - b) Because it multiplies int8 matrices with 128 parallel MACs per cycle, finishing the work in fewer cycles, so the board can go back to sleep sooner
   - c) Because it skips normalize
   - d) Because it uses no power at all

   <details><summary>Solution</summary>

   **b** — speed and energy come from the same reason: a specialized circuit doing one job in parallel uses far fewer clock cycles.

   </details>

## Lab

- [ ] Run `./quantize_vela.sh model_int8.tflite` in the same Docker image, and note the `_vela.tflite` file's size against `model_int8.tflite` in your learning log.
- [ ] Read the report Vela prints, and find whether any op fell back to running on the CPU.
- [ ] Draw a "one set of weights, three packages" map, writing which script each file comes from and which target it goes to.

## Going further

In lesson 5.9, we'll fill in `s14_tflite_board.py` to benchmark int8 on the PC, run Vela, and fill in a three-target comparison table, including reading real latency from the board.

Next lesson: [lesson 5.9 — Hands-on: comparing three targets — MCU, web and PC](../l09-three-targets-lab/README.md)

## Reflect

- If your model had several ops the Ethos-U55 can't run, what would that do to latency, and where would you fix it?
- What kind of work would you accept an extra compile step for, in exchange for a longer battery life?
