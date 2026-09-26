---
id: fw-stack.m03.l05
lang: en
title:
  th: "Motion radar: วาดทิศการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
summary:
  th: "นำข้อมูล accelerometer/gyroscope จาก BMI270 มาวาดเป็น motion radar บนจอ LVGL เพื่อให้เห็นทิศทางการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l04]
objectives:
  - th: "แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar"
    en: "Turn accelerometer and gyroscope readings into angle and magnitude and draw them in polar form"
  - th: "ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms"
    en: "Use a baseline and a dead-band to drop small jitter before drawing, and work out how much lag a moving average would add at the 50 ms read period"
  - th: "ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที"
    en: "Design a view that lets a user read the direction within a second"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep05_bmi270_radar_view"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 7c064203d1175cb1a75e664c48d63803d332275673fe41c0c708032269736691
---

# Motion radar: movement direction in polar form

## Objectives

1. Turn accelerometer and gyroscope readings into angle and magnitude and draw them in polar form
2. Use a baseline and a dead-band to drop small jitter before drawing, and work out how much lag a moving average would add at the 50 ms read period
3. Design a view that lets a user read the direction within a second

## Concepts

Taking accelerometer/gyroscope data from the BMI270 and drawing it as a motion radar on the LVGL screen, to show movement direction in polar form

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/main_example.c)
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_config.h)
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_driver.c)
- [`app_sensor/bmi270/bmi270_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_driver.h)
- [`app_sensor/bmi270/bmi270_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_reader.c)
- and 6 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view) and flash the ready-made firmware.

## See it work first

![Screen of EP05 — BMI270 Radar View on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/int_ep05_bmi270_radar_view.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What does atan2 do when finding the direction?
- How does a dead-band differ from a moving average in terms of the lag of the point on the radar?
- What should the point's colour or size communicate?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
