---
id: fw-stack.m02.l05
lang: en
title:
  th: "สแกน Wi-Fi และแสดงรายการเครือข่าย"
  en: "Wi-Fi scan and a network list"
summary:
  th: "สแกน WiFi ผ่าน WHD/cy_wcm แล้วแสดงผลเป็น list พร้อม RSSI + security type — เพิ่มหน้า WiFi Scan เข้าไปใน shell ของ EP04"
  en: "Wi-Fi scan and a network list"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l04]
objectives:
  - th: "สแกน Wi-Fi ผ่าน WHD/cy_wcm แล้วแสดงรายการพร้อม RSSI และชนิด security"
    en: "Scan Wi-Fi through WHD/cy_wcm and list networks with RSSI and security type"
  - th: "แยก scan service ออกจากหน้า UI และส่งผลสแกนเข้าหน้าอย่างปลอดภัย"
    en: "Keep the scan service apart from the UI page and hand results to the page safely"
  - th: "อ่านค่า RSSI และบอกได้ว่าเครือข่ายใดสัญญาณดีพอจะเชื่อมต่อ"
    en: "Read RSSI values and judge which network is strong enough to join"
develops:
  - {skill: proto.wifi, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: rtos.basics, to: 1}
  - {skill: iot.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep05_wifi_list"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: a2ac1a04d5efade4be081740eba5b308d339acf25565f42ac09425a77fc46d5b
---

# Wi-Fi scan and a network list

## Objectives

1. Scan Wi-Fi through WHD/cy_wcm and list networks with RSSI and security type
2. Keep the scan service apart from the UI page and hand results to the page safely
3. Read RSSI values and judge which network is strong enough to join

## Concepts

Scanning Wi-Fi through WHD/cy_wcm and displaying the results as a list with RSSI and security type — adding a Wi-Fi Scan page into EP04's shell

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/nav/ui_menu_navigation.c)
- and 6 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list) and flash the ready-made firmware.

## See it work first

![Screen of EP05 — WiFi List on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/hmi_ep05_wifi_list.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Which is better, an RSSI of -45 dBm or -85 dBm?
- Why should you not scan for Wi-Fi directly inside a button's callback?
- What does the security type in the list tell the user?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
