---
id: fw-stack.m02.l02
lang: en
title:
  th: "ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
summary:
  th: "ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l01]
objectives:
  - th: "ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT"
    en: "Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT"
  - th: "แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น"
    en: "Separate UI logic from counter logic into different files and explain why that makes testing easier"
  - th: "เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้"
    en: "Add one new button that reuses the same logic"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: prog.design-patterns, to: 1}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep02_button_event"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 58b2875f13d254da460643959d7e92f4d93a7baf085bfb54eed692028ff9b05f
---

# Buttons and event callbacks: an UP / DOWN / RESET counter

## Objectives

1. Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT
2. Separate UI logic from counter logic into different files and explain why that makes testing easier
3. Add one new button that reuses the same logic

## Concepts

UP / DOWN / RESET buttons that respond to LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT — separating UI logic from counter logic

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md), then work through the code in this order:

- [`counter_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.c)
- [`counter_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.h)
- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/main_example.c)
- [`ui_button_counter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.c)
- [`ui_button_counter.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.h)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event) and flash the ready-made firmware.

## See it work first

![Screen of EP02 — Button Event on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/hmi_ep02_button_event.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How do LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT differ when a button is held down?
- Does counter_logic.c know about LVGL at all, and why was it designed that way?
- If the counter must never go negative, which file should you change?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
