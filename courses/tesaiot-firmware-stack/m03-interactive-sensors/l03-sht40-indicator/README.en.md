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
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep03_sht40_indicator"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 5c5155ebfe2ca722fb54a3235a9b45229e99df97dccf40519523451960e13fc8
---

# Humidity and temperature indicator from the SHT4x

## Objectives

1. Read relative humidity and temperature from the SHT4x over I2C and show them as indicators
2. Set the indicator colour thresholds from a comfort humidity range and justify them
3. Compare the SHT4x and DPS368 temperatures and explain why they may differ

## Concepts

### What the SHT4x is, and what its spec numbers mean

The SHT4x (SHT40/41/45) is Sensirion's relative-humidity (RH%) and temperature sensor. The SHT40 variant is
accurate to ±1.8 %RH and ±0.2 °C, measures RH across 0–100% and temperature from -40 to +125 °C, and averages
under 0.4 µA at a 1-reading-per-second rate. Unlike the DPS368/BMI270, the SHT4x has no register map to read or
write addresses on — it talks over a **command-based protocol**: send a 1-byte command to start a measurement,
wait out the conversion delay (up to about 8.2 ms at high precision), then read back 6 bytes with a CRC-8 check
(polynomial `0x31`, Sensirion's standard). That protocol is real knowledge about this sensor family, but **none of
it is written in this episode's own files**.

### Why it matters to know which code layer actually does what

This episode's `sht4x_driver.c` does not send a command byte, wait out a delay, or compute the CRC-8/conversion
formula itself — it calls a single Infineon middleware function,
`mtb_sht4x_measure_high_precision(i2c_bus, &temp_milli_c, &hum_milli_rh)`, which already does every step (sending
command `0xFD`, waiting, reading 6 bytes, checking the CRC, converting using Sensirion's formulas) and returns the
result in **milli-units** (milli-°C, milli-%RH). The episode's own code just divides by 1000 to get normal units
(`temperature_c`, `humidity_rh`). The byte-level protocol the upstream README describes in detail really does
happen on the I2C wire — it is just hidden inside the middleware, not in the code this episode shows the student.
This is the same pattern as the DPS368 (lesson 3.1) using `xensiv_dps3xx_read()` and the BMI270 (lesson 3.2)
uploading Bosch's config file: this series consistently wraps byte-level sensor protocol inside the vendor's own
library.

### The real color thresholds have three zones, not the four the upstream README describes

`sht4x_view.c` has `hum_level_color()` and `set_comfort_chip()`, which both use the same thresholds: **RH < 40% =
Dry (amber), 40–60% = Comfort (green), RH > 60% = Humid (blue)** — only two cut points (40 and 60), not three
(30/60/80), and there is no separate red "danger" zone as the upstream README describes. The 40–60% comfort range
matches common HVAC/ASHRAE guidance for indoor humidity that feels comfortable while limiting mold and dust-mite
growth.

### The threshold is defined twice, and both copies must be edited together

`hum_level_color()` (sets the chip's color) and `set_comfort_chip()` (sets the "Dry"/"Comfort"/"Humid" text) are
two **separate** functions, each hard-coding its own 40.0f and 60.0f — they do not share one constant. Edit the
threshold in one function and forget the other, and the text and the color will disagree (for example, the text
reads "Humid" while the chip is still colored "Comfort" green).

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md)
to learn the SHT4x's protocol, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the byte-level protocol lives in the middleware, not in the
episode's own files, and the real color thresholds differ from what the upstream README describes.

[`app_sensor/sht4x/sht4x_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.c) — a single middleware call, no command byte or CRC in this file:

```c
cy_rslt_t sht4x_driver_read_sample(sht4x_sample_t *sample)
{
    int32_t temp_milli_c = 0;
    int32_t hum_milli_rh = 0;

    cy_rslt_t rslt = mtb_sht4x_measure_high_precision(s_i2c_bus, &temp_milli_c, &hum_milli_rh);
    if (CY_RSLT_SUCCESS != rslt)
    {
        return rslt;
    }

    /* Middleware returns milli-units; convert once here for UI/presenter layers. */
    sample->temperature_c = ((float)temp_milli_c) / 1000.0f;
    sample->humidity_rh = ((float)hum_milli_rh) / 1000.0f;
    return CY_RSLT_SUCCESS;
}
```

[`app_ui/sht4x/sht4x_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_ui/sht4x/sht4x_view.c) — the real thresholds, three zones, two cut points:

```c
static lv_color_t hum_level_color(float humidity_rh)
{
    if (humidity_rh < 40.0f)
    {
        return lv_color_hex(0xD97706);   /* Dry */
    }

    if (humidity_rh <= 60.0f)
    {
        return lv_color_hex(0x16A34A);   /* Comfort */
    }

    return lv_color_hex(0x2563EB);       /* Humid */
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/main_example.c) hands the I2C handle to `sht4x_presenter_start()`, exactly as the upstream README describes
- [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_config.h) — `SHT4X_SAMPLE_PERIOD_MS = 1000` (polled by a single `lv_timer` on the LVGL thread, the same pattern as lessons 3.1–3.2) plus the primary/alternate I2C addresses
- See the full folder at [`int_ep03_sht40_indicator/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator)

## Common mistakes

- **Assuming you must write the command byte/CRC-8 yourself in this episode's code** — the byte-level protocol
  is already done inside `mtb_sht4x_measure_high_precision()`; `sht4x_driver.c` only calls it and converts
  milli-units to normal ones.
- **Misremembering the color thresholds as four zones (30/60/80%)** — the real thresholds have only three zones
  at the 40% and 60% cut points, with no separate red "danger" zone.
- **Editing the threshold in only one function** — `hum_level_color()` and `set_comfort_chip()` each hard-code
  40.0f/60.0f separately; both must be changed together or the text and the color will disagree.

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
