---
id: fw-stack.m04.l01
lang: en
title:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
summary:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
level: L2
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง"
    en: "Read active-low pull-up buttons and count presses correctly"
  - th: "นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk"
    en: "Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style"
develops:
  - {skill: mcu.gpio, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_button_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: dcaa5dcc29475f32d58ac4e466634e6088373bc069f1697920f8c6b8fce521e7
---

# Base-board buttons and a menu without touch

## Objectives

1. Read active-low pull-up buttons and count presses correctly
2. Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style

## Concepts

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Push Button Monitor** — reads buttons SW9 (P17.5) and SW10 (P17.7) as active-low pull-up inputs, showing pressed/released state plus a press counter on LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor)
- **QWA309 — Hardware Button Menu** — navigates an LVGL menu with physical buttons, SW6 = Move and SW5 = Select (no touch) — a headless/kiosk UX pattern
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

> The button names in the Developer Hub's description (SW9/SW10) do not match the exercise's code (SW5/SW6); follow the code and the board's silkscreen labels

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why does an active-low button read 0 when pressed?
- One press but the counter jumps by two — what causes this, and how do you fix it?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
