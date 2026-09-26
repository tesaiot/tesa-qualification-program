---
id: fw-stack.m04.l02
lang: en
title:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
summary:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์"
    en: "Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent"
  - th: "แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC"
    en: "Plot them as a scrolling scope and explain ADC resolution"
develops:
  - {skill: mcu.adc-dac, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_pot_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: c9a33f86b8b33b3ae87fa47cfa29e2c9d129cf1208691b0457b7785f8692d540
---

# Analog voltages with the 12-bit SAR ADC

## Objectives

1. Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent
2. Plot them as a scrolling scope and explain ADC resolution

## Concepts

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Potentiometer Monitor** — reads four potentiometers (P15.4–P15.7) through the AUTANALOG 12-bit SAR ADC (Vref 1.8 V), showing each as a bar plus voltage and percentage in real time — the first exercise to use a real ADC on the TESAIoT Dev Kit
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor)
- **QWA309 — 4-Channel ADC Scope** — plots all four potentiometers (P15.4–7, 12-bit SAR) as scrolling traces on a 0–100% LVGL chart — an analogue oscilloscope
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope)

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

- With a 12-bit ADC at Vref 1.8 V, how many millivolts does each step resolve?
- Why does the reading jitter slightly even when the pot is not turned?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
