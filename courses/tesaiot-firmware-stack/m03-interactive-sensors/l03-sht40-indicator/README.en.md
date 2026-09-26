---
id: fw-stack.m03.l03
lang: en
title:
  th: "ตัวบ่งชี้ความชื้นและอุณหภูมิจาก SHT4x"
  en: "Humidity and temperature indicator from the SHT4x"
summary:
  th: "วัดความชื้นสัมพัทธ์และอุณหภูมิด้วยเซนเซอร์ Sensirion SHT4x บน I2C แล้วแสดงผลเป็นตัวบ่งชี้บนจอ LVGL"
  en: "Humidity and temperature indicator from the SHT4x"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l02]
objectives:
  - th: "อ่านความชื้นสัมพัทธ์และอุณหภูมิจาก SHT4x ผ่าน I2C แล้วแสดงเป็นตัวบ่งชี้"
    en: "Read relative humidity and temperature from the SHT4x over I2C and show them as indicators"
  - th: "ตั้งเกณฑ์สีของตัวบ่งชี้จากช่วงความชื้นที่สบาย และอธิบายที่มาของเกณฑ์"
    en: "Set the indicator colour thresholds from a comfort humidity range and justify them"
  - th: "เปรียบเทียบอุณหภูมิจาก SHT4x กับ DPS368 และอธิบายว่าทำไมอาจไม่เท่ากัน"
    en: "Compare the SHT4x and DPS368 temperatures and explain why they may differ"
develops:
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: proto.i2c, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep03_sht40_indicator"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: b7815133bba2cfe5195133ca9e03a77bc2064d5a3301d6d4c89045b27c7ad73d
---

# Humidity and temperature indicator from the SHT4x

## Objectives

1. Read relative humidity and temperature from the SHT4x over I2C and show them as indicators
2. Set the indicator colour thresholds from a comfort humidity range and justify them
3. Compare the SHT4x and DPS368 temperatures and explain why they may differ

## Concepts

Measuring relative humidity and temperature with the Sensirion SHT4x sensor over I2C, then showing the results as indicators on the LVGL screen

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/main_example.c)
- [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_config.h)
- [`app_sensor/sht4x/sht4x_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.c)
- [`app_sensor/sht4x/sht4x_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.h)
- [`app_sensor/sht4x/sht4x_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_reader.c)
- and 6 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator) and flash the ready-made firmware.

## See it work first

![Screen of EP03 — SHT40 Indicator on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/int_ep03_sht40_indicator.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does relative humidity depend on temperature?
- Why do two sensors on the same board read different temperatures?
- What humidity range does your colour threshold use, and what did you base it on?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
