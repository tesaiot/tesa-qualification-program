---
id: fw-stack.m02.l03
lang: en
title:
  th: "รับข้อความด้วย textarea และ keyboard"
  en: "Text input with a textarea and keyboard"
summary:
  th: "lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number"
  en: "Text input with a textarea and keyboard"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l02]
objectives:
  - th: "เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK"
    en: "Connect lv_textarea to lv_keyboard and take input both in real time and on OK"
  - th: "สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown"
    en: "Switch the keyboard between normal and number modes from a dropdown"
  - th: "อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน"
    en: "Explain when a value should update immediately and when it should wait for confirmation"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep03_text_input_keyboard"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: bef08c61b7ea14e68fd81d43c4ebe79a91bc3b9f28250f9e0865391bba220583
---

# Text input with a textarea and keyboard

## Objectives

1. Connect lv_textarea to lv_keyboard and take input both in real time and on OK
2. Switch the keyboard between normal and number modes from a dropdown
3. Explain when a value should update immediately and when it should wait for confirmation

## Concepts

lv_textarea + lv_keyboard — taking input in real time and commit-on-OK style, with a dropdown to pick normal / number mode

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/main_example.c)
- [`text_input_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.c)
- [`text_input_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.h)
- [`ui_text_input_keyboard.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.c)
- [`ui_text_input_keyboard.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.h)
- [`ui_text_input_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_layout.h)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard) and flash the ready-made firmware.

## See it work first

![Screen of EP03 — Text Input Keyboard on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/hmi_ep03_text_input_keyboard.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Which event tells you the user pressed OK on the keyboard?
- Should the Wi-Fi password field use real-time or commit-on-OK input, and why?
- What kind of mistake does number mode prevent?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
