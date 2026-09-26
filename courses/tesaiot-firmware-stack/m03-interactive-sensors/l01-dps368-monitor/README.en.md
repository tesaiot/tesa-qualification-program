---
id: fw-stack.m03.l01
lang: en
title:
  th: "อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C"
  en: "Pressure and temperature from the DPS368 over I2C"
summary:
  th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL"
  en: "Pressure and temperature from the DPS368 over I2C"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ"
    en: "Read pressure and temperature from the DPS368 over I2C and show them on screen"
  - th: "อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode"
    en: "Explain the driver → reader → presenter → view layering of the episode"
  - th: "ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง"
    en: "Check the reading against a local reference pressure and explain the difference"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep01_dps368_monitor"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 7b1991d0f05062938a0cac42a1208d384c3229c65c711a6c5bb66443c2966146
---

# Pressure and temperature from the DPS368 over I2C

## Objectives

1. Read pressure and temperature from the DPS368 over I2C and show them on screen
2. Explain the driver → reader → presenter → view layering of the episode
3. Check the reading against a local reference pressure and explain the difference

## Concepts

Reading atmospheric pressure and temperature from the Infineon DPS368 sensor over I2C and showing the results on the LVGL screen

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/main_example.c)
- [`app_sensor/app_dps368_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.c)
- [`app_sensor/app_dps368_service.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.h)
- [`app_sensor/dps368/dps368_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_config.h)
- [`app_sensor/dps368/dps368_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_driver.c)
- and 12 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) and flash the ready-made firmware.

## See it work first

![Screen of EP01 — DPS368 Monitor on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/int_ep01_dps368_monitor.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What does the presenter layer do that the view does not?
- How should the pressure change when you lift the board up by one floor of a building?
- If the sensor does not respond on I2C, at which layer should the error message appear?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
