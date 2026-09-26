---
id: fw-stack.m03.l06
lang: en
title:
  th: "ไมโครโฟน PDM สเตอริโอและ level meter"
  en: "Stereo PDM microphone and a level meter"
summary:
  th: "เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL"
  en: "Stereo PDM microphone and a level meter"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l05]
objectives:
  - th: "เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา"
    en: "Capture the stereo PDM microphone and compute left/right sound levels"
  - th: "แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS"
    en: "Show the levels as a meter and explain whether it uses peak or RMS"
  - th: "ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน"
    en: "Test with sound from each side and confirm the channels are not swapped"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep06_digital_mic_probe"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 52c287ac90cbe6ed752401e302c318282db78cc0a5fe7f2c4a90b4cb15a365bd
---

# Stereo PDM microphone and a level meter

## Objectives

1. Capture the stereo PDM microphone and compute left/right sound levels
2. Show the levels as a meter and explain whether it uses peak or RMS
3. Test with sound from each side and confirm the channels are not swapped

## Concepts

Capturing audio from the board's stereo PDM microphone, computing the left/right loudness levels, and showing them as a level meter on the LVGL screen

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/main_example.c)
- [`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.c)
- [`app_audio/pdm/pdm_mic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.h)
- [`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.c)
- [`app_audio/pdm/pdm_probe_logger.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.h)
- and 4 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) and flash the ready-made firmware.

## See it work first

![Screen of EP06 — Digital Mic Probe on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/int_ep06_digital_mic_probe.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does PDM differ from PCM?
- How do RMS and peak give different pictures of the sound level?
- How do you test that the left and right channels are not swapped?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
