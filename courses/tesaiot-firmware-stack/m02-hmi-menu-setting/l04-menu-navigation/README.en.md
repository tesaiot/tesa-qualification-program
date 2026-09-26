---
id: fw-stack.m02.l04
lang: en
title:
  th: "โครง navigation: แถบเมนู หน้า และการสลับหน้า"
  en: "Navigation shell: menu bar, pages and page routing"
summary:
  th: "โครง navigation หลัก — top nav bar พร้อมปุ่มสลับหน้า + icon action buttons + หน้าต่าง ๆ ที่ lv_menu สร้างไว้ครั้งเดียวแล้วสลับตามเมนูที่เลือก (README ของ episode เล่าแบบ stage container แต่โค้ดใช้ lv_menu ให้ยึดตามโค้ด)"
  en: "Navigation shell: menu bar, pages and page routing"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l03]
objectives:
  - th: "สร้างเมนูนำทางด้วย lv_menu ที่สร้างทุกหน้าไว้ครั้งเดียว แล้วสลับหน้าที่แสดงตามเมนูที่เลือก"
    en: "Build navigation with lv_menu that creates every page once and switches the visible page from the menu"
  - th: "แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode"
    en: "Keep layout, navigation logic and pages apart, following the episode file structure"
  - th: "เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่"
    en: "Add one page to the menu without changing the existing pages"
develops:
  - {skill: gui.hmi, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: prog.state-machines, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep04_menu_navigation"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: a8a9a6a48364bbf2f6d526914476e02b948f20f453e70a86374f37b0933263bb
---

# Navigation shell: menu bar, pages and page routing

## Objectives

1. Build navigation with lv_menu that creates every page once and switches the visible page from the menu
2. Keep layout, navigation logic and pages apart, following the episode file structure
3. Add one page to the menu without changing the existing pages

## Concepts

The main navigation shell — a top nav bar with page-switching buttons plus icon action buttons, and pages that lv_menu creates once and then switches between based on the selected menu item (the episode's README describes it as a stage container, but the code uses lv_menu — follow the code).

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_navigation.c)
- and 1 more file in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation) and flash the ready-made firmware.

## See it work first

![Screen of EP04 — Menu Navigation on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/hmi_ep04_menu_navigation.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does lv_menu keep all the pages, and what are the pros and cons of building every page just once?
- If you add a new page, which files must you change?
- If you instead created a new page every time the menu switched, without deleting the old one, what would happen to memory?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
