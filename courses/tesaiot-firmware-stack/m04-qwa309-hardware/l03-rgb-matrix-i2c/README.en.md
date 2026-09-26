---
id: fw-stack.m04.l03
lang: en
title:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
summary:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V"
    en: "Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus"
  - th: "ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว"
    en: "Combine potentiometer input with matrix and screen output in one program"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_rgb_matrix"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 7effe7b945774d6d50e1ce21736330bdf849eb7e307968a2743c7f9d01afeb63
---

# Driving an RGB dot matrix over I2C

## Objectives

1. Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus
2. Combine potentiometer input with matrix and screen output in one program

## Concepts

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — DFR0522 RGB Dot Matrix** — drives a DFRobot DFR0522 8x16 RGB matrix (I2C address 0x10) on the 3.3 V bus alongside the display, showing clear/fill/pixel/pattern actions through the LVGL UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix)
- **QWA309 — RGB Matrix FX** — animated effects on the DFR0522 8x16 matrix (colour cycle / pixel sweep / row wipe), auto-cycling with status shown on the LCD
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix_fx&q=prac_qwa309_rgb_matrix_fx)
- **QWA309 — Pot → RGB Mixer** — three potentiometers act as the R/G/B channels (over 50% turns that colour on), mixed into one of the DFR0522 matrix's 8 colours and shown on the LCD — combining the SAR pots with RGB over I2C
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_rgb_mixer&q=prac_qwa309_pot_rgb_mixer)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What tells two devices on the same I2C bus apart?
- If the matrix does not respond, what should you check first (cable, power, address)?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
