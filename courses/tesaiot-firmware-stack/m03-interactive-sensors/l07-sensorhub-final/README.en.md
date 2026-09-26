---
id: fw-stack.m03.l07
lang: en
title:
  th: "SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)"
  en: "SensorHub: one dashboard for every sensor (series project)"
summary:
  th: "โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว"
  en: "SensorHub: one dashboard for every sensor (series project)"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l06]
objectives:
  - th: "รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว"
    en: "Combine the DPS368, SHT4x, BMI270, BMM350 and PDM microphone on one dashboard"
  - th: "จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก"
    en: "Schedule each sensor read so the screen does not stutter"
  - th: "นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร"
    en: "Present the dashboard and explain how each value is shown"
develops:
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: rtos.basics, to: 2}
  - {skill: soft.problem-solving, to: 2}
  - {skill: soft.communication, to: 2}
assesses:
  - {skill: gui.hmi, level: 3, evidence: "วิดีโอแดชบอร์ดบนบอร์ดจริง 1 นาที พร้อมคำอธิบายการออกแบบ"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep07_sensorhub_final"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: d07b6fe958aa8c40f0ade9ce1fe721d11180488225325e5e9ef87d363e574bbf
---

# SensorHub: one dashboard for every sensor (series project)

## Objectives

1. Combine the DPS368, SHT4x, BMI270, BMM350 and PDM microphone on one dashboard
2. Schedule each sensor read so the screen does not stutter
3. Present the dashboard and explain how each value is shown

## Concepts

Course capstone project: a dashboard combining all 4 sensors (DPS368, SHT4x, BMI270, BMM350) plus the stereo PDM microphone on one screen

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/main_example.c)
- [`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_audio/pdm/pdm_mic.c)
- [`app_audio/pdm/pdm_mic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_audio/pdm/pdm_mic.h)
- [`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_audio/pdm/pdm_probe_logger.c)
- [`app_audio/pdm/pdm_probe_logger.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_audio/pdm/pdm_probe_logger.h)
- and 32 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) and flash the ready-made firmware.

## See it work first

![Screen of EP07 — SensorHub Final on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/int_ep07_sensorhub_final.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Which sensor should be read most often, and which can be read more slowly?
- What causes the screen to stutter when combining several sensors?
- If you were to send this data set to the TESAIoT Platform, which values would you choose to send?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
