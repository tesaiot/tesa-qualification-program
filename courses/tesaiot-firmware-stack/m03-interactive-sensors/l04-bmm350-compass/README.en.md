---
id: fw-stack.m03.l04
lang: en
title:
  th: "เข็มทิศดิจิทัลจาก BMM350 บน I3C พร้อม calibration"
  en: "Digital compass from the BMM350 over I3C with calibration"
summary:
  th: "สร้างเข็มทิศดิจิทัลจากเซนเซอร์สนามแม่เหล็ก Bosch BMM350 บน I3C พร้อมฟีเจอร์ปรับแต่ง (hard-iron calibration)"
  en: "Digital compass from the BMM350 over I3C with calibration"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l03]
objectives:
  - th: "อ่านสนามแม่เหล็กจาก BMM350 บน I3C แล้วคำนวณทิศเป็นองศา"
    en: "Read the magnetic field from the BMM350 over I3C and compute a heading in degrees"
  - th: "ทำ hard-iron calibration และแสดงว่าทิศแม่นขึ้นหลังปรับ"
    en: "Run hard-iron calibration and show that the heading improves afterwards"
  - th: "อธิบายว่าโลหะและกระแสไฟรอบบอร์ดรบกวนเข็มทิศอย่างไร"
    en: "Explain how metal and currents near the board disturb the compass"
develops:
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: sys.dsp, to: 1}
  - {skill: proto.i2c, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep04_bmm350_compass"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: cad5bd11852857dfe82c92c42ddc2e7a49139777330fc33d1b754aa3d1269f31
---

# Digital compass from the BMM350 over I3C with calibration

## Objectives

1. Read the magnetic field from the BMM350 over I3C and compute a heading in degrees
2. Run hard-iron calibration and show that the heading improves afterwards
3. Explain how metal and currents near the board disturb the compass

## Concepts

Building a digital compass from the Bosch BMM350 magnetometer over I3C, with a hard-iron calibration feature

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/main_example.c)
- [`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_config.h)
- [`app_sensor/bmm350/bmm350_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.c)
- [`app_sensor/bmm350/bmm350_driver.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.h)
- [`app_sensor/bmm350/bmm350_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_reader.c)
- and 6 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass) and flash the ready-made firmware.

## See it work first

![Screen of EP04 — BMM350 Compass on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/int_ep04_bmm350_compass.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What is hard-iron error, and how do you correct it?
- Why must you rotate the board through every direction while calibrating?
- How does I3C differ from I2C from a user's point of view?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
