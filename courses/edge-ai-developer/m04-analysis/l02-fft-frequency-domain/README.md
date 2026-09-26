---
id: edgeai-dev.m04.l02
lang: th
title: {th: FFT และโดเมนความถี่, en: FFT and the frequency domain}
summary: {th: มองสัญญาณในโดเมนความถี่ด้วย FFT และอ่านสเปกตรัมของสัญญาณจริง, en: View signals in the frequency domain with an FFT and read a real spectrum.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: true
  boards: [none, devkit]
prerequisites: [edgeai-dev.m04.l01]
objectives:
- {th: อธิบายความสัมพันธ์ระหว่างอัตราสุ่มตัวอย่าง จำนวนจุด FFT และความละเอียดความถี่, en: 'Explain how sample rate, FFT size and frequency resolution relate.'}
- {th: ระบุความถี่เด่นของสัญญาณการสั่นหรือเสียงจากสเปกตรัมได้, en: Identify the dominant frequency of a vibration or sound from its spectrum.}
develops:
- {skill: sys.dsp, to: 3}
- {skill: hw.math, to: 3}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, npu: ethos-u55}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. อธิบายความสัมพันธ์ระหว่างอัตราสุ่มตัวอย่าง จำนวนจุด FFT และความละเอียดความถี่
2. ระบุความถี่เด่นของสัญญาณการสั่นหรือเสียงจากสเปกตรัมได้

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แหล่งอ้างอิง

- [AIoT in Action: examples/s07/02_fft64_two_tones.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s07/02_fft64_two_tones.py)
- [AIoT in Action: examples/s07/01_imu_vibration_monitor.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s07/01_imu_vibration_monitor.py)
