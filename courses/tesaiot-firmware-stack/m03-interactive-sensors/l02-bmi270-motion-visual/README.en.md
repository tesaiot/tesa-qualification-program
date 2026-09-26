---
id: fw-stack.m03.l02
lang: en
title:
  th: "ภาพการเคลื่อนไหว 6 แกนจาก BMI270"
  en: "Six-axis motion from the BMI270"
summary:
  th: "แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์"
  en: "Six-axis motion from the BMI270"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l01]
objectives:
  - th: "อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์"
    en: "Read the BMI270 accelerometer and gyroscope and display them in real time"
  - th: "แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง"
    en: "Tell acceleration (g) from angular rate (°/s) and predict the values of a board at rest"
  - th: "ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์"
    en: "Match the screen refresh rate to the sensor read rate"
develops:
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: proto.i2c, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep02_bmi270_motion_visual"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 066b53ed4ae425be091d6fcdafe73482f265c6d73c78815d9041465bd3758d09
---

# Six-axis motion from the BMI270

## Objectives

1. Read the BMI270 accelerometer and gyroscope and display them in real time
2. Tell acceleration (g) from angular rate (°/s) and predict the values of a board at rest
3. Match the screen refresh rate to the sensor read rate

## Concepts

Showing six-axis motion from the Bosch BMI270 sensor (accelerometer + gyroscope) on the LVGL screen in real time

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/main_example.c)
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_config.h)
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.c)
- [`app_sensor/bmi270/bmi270_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.h)
- [`app_sensor/bmi270/bmi270_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_reader.c)
- and 6 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual) and flash the ready-made firmware.

## See it work first

![Screen of EP02 — BMI270 Motion Visual on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/int_ep02_bmi270_motion_visual.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- With the board resting still on a table, which axis should read about 1 g?
- What does the gyroscope read when the board is not rotating?
- Why should the screen not be redrawn every time a sensor reading comes in?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
