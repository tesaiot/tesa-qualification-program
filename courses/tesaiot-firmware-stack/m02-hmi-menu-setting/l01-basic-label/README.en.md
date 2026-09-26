---
id: fw-stack.m02.l01
lang: en
title:
  th: "หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย"
  en: "First LVGL screen: logo, title and subtitle"
summary:
  th: "หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen"
  en: "First LVGL screen: logo, title and subtitle"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง"
    en: "Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot"
  - th: "อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง"
    en: "Explain when the master template calls example_main(parent) and why we do not write main ourselves"
  - th: "สร้าง object tree screen → image → label และจัดวางด้วย align ได้"
    en: "Build a screen → image → label object tree and place it with align"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: lang.c, to: 2}
  - {skill: build.vendor-sdk, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep01_basic_label"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: dc5f9fbe61cb8bed0d5ff6d0a8536440db063935390200d8c26fa28b90531aa7
---

# First LVGL screen: logo, title and subtitle

## Objectives

1. Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot
2. Explain when the master template calls example_main(parent) and why we do not write main ourselves
3. Build a screen → image → label object tree and place it with align

## Concepts

The first LVGL screen — drawing a logo, title and subtitle as static objects on the active screen

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/main_example.c)
- [`ui_ep01_basic_label.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c)
- [`ui_ep01_basic_label.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.h)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label) and flash the ready-made firmware.

## See it work first

![Screen of EP01 — Basic Label on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/hmi_ep01_basic_label.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What has the master template already done for us before it calls example_main()?
- Why is the logo embedded as a C array (APP_LOGO) instead of being loaded from a file?
- If you wanted to move the title down by 20 px, which value in the code would you change?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
