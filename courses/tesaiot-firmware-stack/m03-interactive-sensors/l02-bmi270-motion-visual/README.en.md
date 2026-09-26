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
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep02_bmi270_motion_visual"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 997ad2eb3866882e60666e9427c025aa3fd932f7c569d02f35409e97900615dc
---

# Six-axis motion from the BMI270

## Objectives

1. Read the BMI270 accelerometer and gyroscope and display them in real time
2. Tell acceleration (g) from angular rate (°/s) and predict the values of a board at rest
3. Match the screen refresh rate to the sensor read rate

## Concepts

### What the BMI270 is, and what its spec numbers mean

The BMI270 is a six-axis IMU (Inertial Measurement Unit) from Bosch: a 3-axis accelerometer (selectable range
±2g/±4g/±8g/±16g, 16-bit resolution) and a 3-axis gyroscope (±125 to ±2000 degrees per second). This episode uses
the library's default configuration, `mtb_bmi270_config_default()`, which is **±2g and ±2000 dps** (the widest
range for each sensor, not ±4g/±500dps as the upstream README states). That is a good teaching choice because it
accepts hard shakes without clipping, at the cost of coarser per-bit resolution than a narrower range would give.

### Polling every 200 ms with one `lv_timer`, same as the DPS368 — not 100 Hz through a FreeRTOS task

Just like lesson 3.1 (DPS368), this episode uses `lv_timer_create(bmi270_poll_sensor_cb, BMI270_SAMPLE_PERIOD_MS,
NULL)` on a single LVGL thread, with `BMI270_SAMPLE_PERIOD_MS = 200` (5 times a second) — not every 10 ms (100 Hz)
through a FreeRTOS task, a queue and `lv_async_call()` as the upstream README describes. The source comment states
the reason directly: "Poll slower to reduce redraw pressure on small HMI panel" — redrawing a small screen too
often stutters and burns resources needlessly.

### Reading every cycle but drawing only some of them: throttling kept separate from sampling

`bmi270_config.h` has one more constant, `BMI270_UI_UPDATE_DIV = 2`. The sensor callback still reads every 200 ms
(and still uses every reading to decide the ALERT state), but it only calls `bmi270_view_update_sample()` to
redraw the widgets **every 2nd sample** — meaning the screen is only redrawn every 400 ms. The reason: "Update
LVGL widgets every N samples to reduce visible flicker." Reading the sensor and drawing the screen do not need to
share the same period — if reads happen faster than the eye can tell apart, keep reading (for logging or other
logic) but draw the screen only as often as the eye actually needs.

### The motion alert uses two hysteresis thresholds, not one

The code has a feature the upstream README never mentions at all: a **MOTION ALERT**. If the magnitude of the
accelerometer or gyroscope reading crosses a threshold, an alert label appears on screen — but the ON threshold
(`BMI270_ALERT_ACC_ON_G = 1.45g`, `BMI270_ALERT_GYR_ON_DPS = 280`) and the OFF threshold
(`BMI270_ALERT_ACC_OFF_G = 1.25g`, `BMI270_ALERT_GYR_OFF_DPS = 220`) are different values — this is called
**hysteresis**. With a single threshold, a reading that oscillates right around that value (say, light shaking
near 1.4g) would flicker the alert ON/OFF rapidly. Having two thresholds means the reading must drop well below
the OFF line before the alert actually turns off.

### The screen shows each sensor's "combined magnitude", not six per-axis bars

`bmi270_view.c` creates **only two bars** (accel and gyro), each ranged 0–350, plus **one chart with two series**
(accel in green, gyro in orange) — not six per-axis x/y/z bars as the upstream README describes. What is shown is
the combined magnitude (`acc_mag_g`, `gyr_mag_dps`), computed as √(x²+y²+z²) across all three axes, not the raw
per-axis values (those are still logged over serial, just not drawn on screen).

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the poll rate, the sensor ranges and the on-screen widgets differ
from what the upstream README describes.

[`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_config.h) — the real constants:

```c
/* Poll slower to reduce redraw pressure on small HMI panel. */
#define BMI270_SAMPLE_PERIOD_MS           (200U)

/* Update LVGL widgets every N samples to reduce visible flicker. */
#define BMI270_UI_UPDATE_DIV              (2U)

/* mtb_bmi270_config_default() uses ACC=+-2g and GYR=+-2000dps by default. */
#define BMI270_ACC_RANGE_G                (2.0f)
#define BMI270_GYR_RANGE_DPS              (2000.0f)

/* Motion thresholds with hysteresis to avoid ON/OFF toggling noise. */
#define BMI270_ALERT_ACC_ON_G             (1.45f)
#define BMI270_ALERT_ACC_OFF_G            (1.25f)
#define BMI270_ALERT_GYR_ON_DPS           (280.0f)
#define BMI270_ALERT_GYR_OFF_DPS          (220.0f)
```

[`app_ui/bmi270/bmi270_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_ui/bmi270/bmi270_presenter.c) — the two-threshold hysteresis for the alert:

```c
static bool bmi270_should_alert(const bmi270_sample_t *sample, bool is_alert_active)
{
    if (is_alert_active)
    {
        bool below_acc = (sample->acc_mag_g < BMI270_ALERT_ACC_OFF_G);
        bool below_gyr = (sample->gyr_mag_dps < BMI270_ALERT_GYR_OFF_DPS);
        return !(below_acc && below_gyr);
    }

    return ((sample->acc_mag_g >= BMI270_ALERT_ACC_ON_G) ||
            (sample->gyr_mag_dps >= BMI270_ALERT_GYR_ON_DPS));
}
```

Reading every cycle but redrawing only some of them:

```c
s_ui_update_div_counter++;
if ((s_ui_update_div_counter >= BMI270_UI_UPDATE_DIV) ||
    (sample.sample_count <= 1U))
{
    bmi270_view_update_sample(&sample);
    s_ui_update_div_counter = 0U;
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/main_example.c) hands the I2C handle to `bmi270_presenter_start()`, exactly as the upstream README describes
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.c) — the bootstrap sequence (CHIP_ID, soft-reset, the ~8 KB config upload) matches what the upstream README describes; only the BMI270 needs this step (BMI160/BMI088 do not)
- See the full folder at [`int_ep02_bmi270_motion_visual/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual)

## Common mistakes

- **Misremembering the poll rate as 100 Hz through a FreeRTOS task** — the real code polls every 200 ms with a
  single `lv_timer` on the LVGL thread.
- **Assuming sensor reads and screen draws must share the same period** — the code separates the two with
  `BMI270_UI_UPDATE_DIV`: it reads every cycle (for logging and alerts) but draws less often.
- **Using a single threshold for the alert** — without hysteresis (different ON/OFF thresholds), the alert
  flickers whenever the reading oscillates right around that one value.
- **Assuming the screen shows per-axis x/y/z values** — it shows only the combined magnitude of accel and gyro
  as two bars, not six per-axis bars.

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
