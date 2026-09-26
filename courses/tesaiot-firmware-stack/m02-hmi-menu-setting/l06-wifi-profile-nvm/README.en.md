---
id: fw-stack.m02.l06
lang: en
title:
  th: "เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร"
  en: "Store the Wi-Fi profile in non-volatile memory"
summary:
  th: "เก็บ SSID + password ลง non-volatile memory — form กรอก profile ผ่าน lv_textarea (password mode) และ save/load ผ่าน profile store"
  en: "Store the Wi-Fi profile in non-volatile memory"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l05]
objectives:
  - th: "สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode"
    en: "Build an SSID and password form with the password field in password mode"
  - th: "บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด"
    en: "Save, load and clear the profile through the NVM profile store, and keep it across a board reset"
  - th: "อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง"
    en: "Explain the risk of keeping a password in flash and ways to reduce it"
develops:
  - {skill: sys.memory-fs, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: sec.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep06_wifi_profile_nvm"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 8736e55a331b87cb853ae97553812419a1e9be7bf2ad826c4be7d1b71ff789b9
---

# Store the Wi-Fi profile in non-volatile memory

## Objectives

1. Build an SSID and password form with the password field in password mode
2. Save, load and clear the profile through the NVM profile store, and keep it across a board reset
3. Explain the risk of keeping a password in flash and ways to reduce it

## Concepts

Storing SSID + password in non-volatile memory — a form that fills in the profile through lv_textarea (password mode), and save/load through a profile store

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/nav/ui_menu_navigation.c)
- and 11 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm) and flash the ready-made firmware.

## See it work first

![Screen of EP06 — WiFi Profile NVM on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/hmi_ep06_wifi_profile_nvm.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does data in NVM differ from a variable in RAM when the board resets?
- Why must the password field hide its characters?
- If you need to erase every profile, which profile-store function must you call?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
