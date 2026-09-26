---
id: edgeai-dev.m05.l04
lang: th
title: {th: Quantize และรันบน NPU, en: Quantising and running on the NPU}
summary: {th: แปลงโมเดลเป็น int8 คอมไพล์สำหรับ NPU แล้วเทียบความแม่น ความเร็ว และขนาดระหว่างเป้าหมาย, en: 'Quantise to int8, compile for the NPU, and compare accuracy, speed and size across targets.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [edgeai-dev.m05.l03]
objectives:
- {th: quantize โมเดลเป็น int8 และวัดผลต่อความแม่นเทียบกับโมเดล float, en: Quantise a model to int8 and measure the accuracy change against float.}
- {th: คอมไพล์โมเดลสำหรับ Ethos-U NPU และเทียบเวลาในการรันกับบน CPU, en: Compile the model for the Ethos-U NPU and compare latency with CPU.}
- {th: อธิบายว่าทำไมโมเดลที่คอมไพล์สำหรับ NPU แล้วจึงนำไปรันบนเป้าหมายอื่นตรง ๆ ไม่ได้, en: Explain why an NPU-compiled model cannot run as-is on other targets.}
develops:
- {skill: ai.model-deploy, to: 3}
- {skill: ai.model-training, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. quantize โมเดลเป็น int8 และวัดผลต่อความแม่นเทียบกับโมเดล float
2. คอมไพล์โมเดลสำหรับ Ethos-U NPU และเทียบเวลาในการรันกับบน CPU
3. อธิบายว่าทำไมโมเดลที่คอมไพล์สำหรับ NPU แล้วจึงนำไปรันบนเป้าหมายอื่นตรง ๆ ไม่ได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [Arm Ethos-U Vela compiler (PyPI: ethos-u-vela)](https://pypi.org/project/ethos-u-vela/)
- [TensorFlow Lite for Microcontrollers (tflite-micro)](https://github.com/tensorflow/tflite-micro)
- [SDK: cm55/edge_ai/05_register_model.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/05_register_model.c)
- [SDK: lib/edge_ai/MODEL_SLOTS.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/lib/edge_ai/MODEL_SLOTS.md)
