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
source_sha256: f7975781f04170918116132ea442c751d698b18a83b41314eac50974a79c5be1
---

# Motion radar: movement direction in polar form

## Objectives

1. Turn accelerometer and gyroscope readings into angle and magnitude and draw them in polar form
2. Use a baseline and a dead-band to drop small jitter before drawing, and work out how much lag a moving average would add at the 50 ms read period
3. Design a view that lets a user read the direction within a second

## Concepts

### The baseline is a "resting pose" captured once at boot, not a running high-pass filter

`radar_update_baseline()` averages accel X/Y and gyro Z over the **first 30 samples** (at the
`BMI270_SAMPLE_PERIOD_MS = 50` read period, that is roughly the first 1.5 seconds after boot), stores them as
`s_baseline_acc_x/y` and `s_baseline_gyr_z`, and **never recomputes them again** for the rest of the session. This
is the simplest way to remove a constant gravity/offset (baseline subtraction), not a continuously running
moving-average or low-pass filter — the upside is zero added latency; the downside is that if the pose at boot is
not the pose you actually use, the baseline stays wrong for the whole session.

### The radar's angle and magnitude come from the *difference* from baseline, not the raw three axes

Unlike a textbook Cartesian-to-polar formula, the code computes `acc_dx = sample.acc_g_x - s_baseline_acc_x` and
`acc_dy` the same way, then `acc_xy_delta_g = sqrt(acc_dx² + acc_dy²)` — using only the X/Y axes of the
**difference**, never the Z axis, and never the raw vector's magnitude (which would always include roughly 1g of
gravity even when the board is not moving). The direction is `atan2f(acc_dy, acc_dx)` of this difference vector —
in other words, the radar points toward "the direction acceleration just changed from what it was at boot," not
"the direction the total acceleration vector currently points."

### Two dead-band thresholds gate whether the needle moves at all

Before even computing an angle, the code checks whether `acc_xy_delta_g >= 0.06g` **or**
`gyr_z_delta_abs_dps >= 12°/s`. If neither holds, `motion_active = false`, the angle is forced to 0, and no
needle is drawn at all. The reason: `atan2()` of a near-zero vector (mg-level noise) returns a nearly random
angle, so without this dead-band the needle would wander even while the board sits perfectly still. Unlike a
low-pass filter, this technique adds **no latency** — there is no averaging across time, just a per-sample
decision on whether to show or hide.

### Three intensity levels come from a normalized score comparing both axes

`radar_calc_motion_level()` converts `acc_xy_delta_g` and `gyr_z_delta_abs_dps` into a score by dividing each by
its own constant (`0.45g` and `140°/s`), then picks whichever score is **larger** to decide the level —
`< 0.35` is LOW (green `0x22C55E`), `0.35–0.80` is MEDIUM (amber `0xF59E0B`), `≥ 0.80` is HIGH (red `0xEF4444`).
This system does not appear in the upstream README at all, but it is what lets a user read both "how hard" (from
color) and "which way" (from the needle's angle) in a single glance.

### The real screen uses an `lv_scale` widget with one needle, not a canvas with rings and trace history

The upstream README describes an `lv_canvas` drawing four concentric rings, N/E/S/W cardinal lines, and a
64-point trace history connected into a fading line. The real code instead uses **`lv_scale`**, LVGL 9's
ready-made widget (a round 0–360° dial with 41 ticks), and draws **one needle** with
`lv_scale_set_line_needle_value(scale, needle, needle_len, angle_i)`, where the needle's length encodes movement
magnitude, its angle encodes direction, and it is hidden (`LV_OBJ_FLAG_HIDDEN`) whenever `motion_active` is
false. There is no trace history or multi-ring grid at all. The gyro reading is shown through a separate dual-ring
arc gauge (`intensity_gyr_arc`) that maps the delta to 0–100, not an arc drawn at the Z-axis angle as the upstream
README describes.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the math and the on-screen widget differ substantially from what the
upstream README describes.

[`app_ui/radar/radar_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_presenter.c) — angle and dead-band from the baseline delta:

```c
acc_dx = sample.acc_g_x - s_baseline_acc_x;
acc_dy = sample.acc_g_y - s_baseline_acc_y;
acc_xy_delta_g = sqrtf((acc_dx * acc_dx) + (acc_dy * acc_dy));
gyr_z_delta_abs_dps = fabsf(sample.gyr_dps_z - s_baseline_gyr_z);

/* Treat signal as STILL until delta crosses threshold from baseline. */
motion_active = s_baseline_ready &&
                ((acc_xy_delta_g >= RADAR_STILL_ACC_DELTA_G) ||
                 (gyr_z_delta_abs_dps >= RADAR_STILL_GYR_DELTA_DPS));

angle_deg = motion_active ? (atan2f(acc_dy, acc_dx) * RADAR_DEG_PER_RAD) : 0.0f;
level = motion_active ? radar_calc_motion_level(acc_xy_delta_g, gyr_z_delta_abs_dps) : RADAR_LEVEL_LOW;
```

The three intensity levels from a normalized score:

```c
static radar_motion_level_t radar_calc_motion_level(float acc_xy_delta_g, float gyr_z_delta_abs_dps)
{
    float acc_score = acc_xy_delta_g / 0.45f;
    float gyr_score = gyr_z_delta_abs_dps / 140.0f;
    float score = (acc_score > gyr_score) ? acc_score : gyr_score;

    if (score < 0.35f) { return RADAR_LEVEL_LOW; }
    if (score < 0.80f) { return RADAR_LEVEL_MEDIUM; }
    return RADAR_LEVEL_HIGH;
}
```

[`app_ui/radar/radar_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_view.c) — one needle on an `lv_scale`, hidden while still:

```c
s_view.radar_scale = lv_scale_create(radar_card);
lv_scale_set_mode(s_view.radar_scale, LV_SCALE_MODE_ROUND_INNER);
lv_scale_set_range(s_view.radar_scale, 0, 360);
lv_scale_set_total_tick_count(s_view.radar_scale, 41);

s_view.radar_needle = lv_line_create(s_view.radar_scale);
lv_scale_set_line_needle_value(s_view.radar_scale, s_view.radar_needle, 18, 0);
/* Hide needle in STILL state; presenter shows it only when motion is active. */
lv_obj_add_flag(s_view.radar_needle, LV_OBJ_FLAG_HIDDEN);
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/main_example.c) hands the I2C handle to `radar_presenter_start()`, exactly as the upstream README describes
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_config.h) — `BMI270_SAMPLE_PERIOD_MS = 50` (faster than lesson 3.2's 200 ms, since a radar needs higher responsiveness)
- See the full folder at [`int_ep05_bmi270_radar_view/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view)

## Common mistakes

- **The board is not level at boot, so the needle sticks pointing one way even when still** — the baseline is
  captured once from the first 30 samples; if the board was tilted at boot, a later level pose will differ from
  the baseline enough to look like continuous motion. Hold the board still in its intended pose when powering on.
- **Assuming magnitude comes from all three axes (x, y, z)** — the real code only uses the X/Y difference from
  baseline, never Z, and never the raw value.
- **Removing or shrinking the dead-band to make it "more responsive"** — this makes the needle wander randomly
  while the board sits perfectly still, because `atan2()` of a near-zero vector is meaningless.
- **Assuming there is a canvas with 4 rings and a 64-point trace** — the real screen uses a ready-made `lv_scale`
  widget with a single needle; no movement history is kept at all.

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
