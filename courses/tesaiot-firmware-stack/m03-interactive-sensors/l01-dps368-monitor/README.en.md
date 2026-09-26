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
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep01_dps368_monitor"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 0e4129e109217b0e63b39b7f4b5ad9811757d930ddfe488cdec272d26dd794ba
---

# Pressure and temperature from the DPS368 over I2C

## Objectives

1. Read pressure and temperature from the DPS368 over I2C and show them on screen
2. Explain the driver → reader → presenter → view layering of the episode
3. Check the reading against a local reference pressure and explain the difference

## Concepts

### What the DPS368 is, and what its spec numbers mean

The DPS368 is a capacitive-MEMS barometric pressure sensor from Infineon. It measures pressure across 300–1200
hPa with a precision around ±0.002 hPa (roughly a 2 cm change in altitude), and it also measures temperature in
the same package, because the pressure reading has to be compensated using the sensor's own internal temperature
(this math is already done inside Infineon's library, so we never write that formula ourselves).

### Four code layers: driver → reader → presenter → view

The code splits the work across four layers matching the folder names. Under `app_sensor/dps368/` there is
`dps368_driver` (talks to the sensor through Infineon's own `xensiv_dps3xx` library directly) and `dps368_reader`
(wraps the driver into one function, `dps368_reader_poll()`, that returns a `bool` for whether a new sample
arrived). Under `app_ui/dps368/` there is `dps368_presenter` (owns the timer and decides when to update the
screen) and `dps368_view` (creates and updates plain labels only — no gauge or arc widget, despite what one might
assume). Each layer only knows about its immediate neighbor — `dps368_view` knows nothing about I2C at all, and
`dps368_driver` knows nothing about LVGL at all.

### Reaching the sensor over a bus the master already set up, with an I2C address fallback

`main_example.c` passes `&sensor_i2c_controller_hal_obj` (the HAL handle the master template already opened
before `example_main()` was ever called — see lesson 1.1) straight into `dps368_presenter_start()`, with no
repeated `cyhal_i2c_init()`. Inside, `app_dps368_service_init()` first tries the default address
(`XENSIV_DPS3XX_I2C_ADDR_DEFAULT` = 0x77); if that does not respond, it tries the alternate address
(`XENSIV_DPS3XX_I2C_ADDR_ALT` = 0x76, set by the sensor's SDO pin). The code therefore works on boards that strap
the SDO pin either way, with no code change needed.

### The real polling mechanism: one `lv_timer` on the LVGL thread, not a separate FreeRTOS task

`dps368_presenter_start()` calls `lv_timer_create(dps368_poll_sensor_cb, DPS368_SAMPLE_PERIOD_MS, NULL)`, where
`DPS368_SAMPLE_PERIOD_MS = 1000` (once per second). `dps368_poll_sensor_cb()` runs on the **same LVGL thread** as
the code that draws the screen — it is not a separate FreeRTOS task pushing data through a queue and back into
LVGL with `lv_async_call()`, as one might otherwise assume. The I2C read
(`dps368_driver_read_hpa_c()`) is therefore a **direct, blocking call inside the timer's callback**, because one
I2C transaction is fast enough not to stutter the screen. At once per second, this episode chooses simplicity
over splitting threads, because a single sensor does not justify the complexity of a task-plus-queue design.

### Telling "no new sample yet" apart from a real error

`dps368_reader_poll()` checks for one special driver return code, `XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY`. On
that code it returns `false` but **does not treat it as an error** — it simply means the sensor's next conversion
cycle has not finished yet. Any other error code is a real problem, which the presenter shows on the status label
as `"Sensor: read error (0x........)"`. Separating these two cases matters: if "not ready yet" were treated as an
error every time, the screen would flash an error message every second the sensor simply had not finished its
next reading.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the real polling mechanism differs from what the upstream README
describes (no separate FreeRTOS task or queue).

[`app_ui/dps368/dps368_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_ui/dps368/dps368_presenter.c) — a single `lv_timer` that polls and updates the screen:

```c
static void dps368_poll_sensor_cb(lv_timer_t *timer)
{
    (void)timer;

    dps368_sample_t sample;
    bool has_new_sample = dps368_reader_poll(&sample);

    if (has_new_sample)
    {
        dps368_view_update_sample(&sample);
        /* ... */
        return;
    }

    cy_rslt_t rslt = dps368_reader_get_last_error();
    if (CY_RSLT_SUCCESS == rslt)
    {
        return;   /* not-ready is not an error */
    }
    /* ... real error -> update status label ... */
}
```

[`app_sensor/dps368/dps368_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_reader.c) — separating "not ready yet" from a real error:

```c
if (CY_RSLT_SUCCESS == rslt)
{
    s_last_sample.pressure_hpa = pressure_hpa;
    s_last_sample.temperature_c = temperature_c;
    s_last_sample.sample_count++;
    if (NULL != out_sample) { *out_sample = s_last_sample; }
    return true;
}

/* At low sample rate, polling can happen before conversion is ready. */
if (rslt == XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY)
{
    s_last_error = CY_RSLT_SUCCESS;
    return false;
}

s_last_error = rslt;
return false;
```

[`app_sensor/app_dps368_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.c) — trying the primary I2C address first, then falling back:

```c
rslt = mtb_xensiv_dps3xx_init_i2c(&s_dps368, i2c_bus, XENSIV_DPS3XX_I2C_ADDR_DEFAULT);
if (CY_RSLT_SUCCESS != rslt)
{
    rslt = mtb_xensiv_dps3xx_init_i2c(&s_dps368, i2c_bus, XENSIV_DPS3XX_I2C_ADDR_ALT);
    /* ... */
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/main_example.c) hands the master's I2C handle to `dps368_presenter_start()`, exactly as the upstream README describes
- The `basic_label_legacy.*` and `dps368_monitor_legacy.*` files are the pre-refactor version kept for comparison — they are not part of the episode's real running code
- See the full folder at [`int_ep01_dps368_monitor/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor)

## Common mistakes

- **Assuming a separate FreeRTOS task polls the sensor every 100 ms** — the real code uses a single `lv_timer`
  on the LVGL thread at 1000 ms, reading I2C as a direct blocking call inside it, with no queue or
  `lv_async_call()`. This works because there is only one sensor and the I2C transaction is short — if more,
  slower sensors are added later, that is when splitting off a real task becomes worth considering (see EP07 —
  SensorHub Final).
- **Treating `XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY` as an error** — it must always be separated from other error
  codes, because it only signals that the next conversion cycle has not finished, not a failure. Treating it as
  an error every time produces a misleading log/status.
- **Forgetting the sensor has two possible I2C addresses** — hard-coding only `0x77` breaks on boards that strap
  the SDO pin the other way. Always try the fallback the way `app_dps368_service_init()` does.

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
