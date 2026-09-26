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
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep04_bmm350_compass"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 9fb82d4365e62418cea3cced3da464f16a44ece5d60dd65f9f12aac0bacc7727
---

# Digital compass from the BMM350 over I3C with calibration

## Objectives

1. Read the magnetic field from the BMM350 over I3C and compute a heading in degrees
2. Run hard-iron calibration and show that the heading improves afterwards
3. Explain how metal and currents near the board disturb the compass

## Concepts

### What the BMM350 is, and why it needs I3C

The BMM350 is Bosch's latest (2023) 3-axis magnetometer: low noise (1.4 µT RMS), a range up to ±2000 µT
(comfortably covering Earth's field of roughly 25–65 µT), and the first sensor in this series wired over **I3C**
instead of I2C. I3C is a bus built on top of I2C's wiring, adding dynamic addressing and in-band interrupts (IBI)
while staying electrically similar. The master template sets up `i3c_controller_init()` the same way it sets up
the I2C bus for the DPS368/BMI270/SHT4x — this episode simply receives `CYBSP_I3C_CONTROLLER_HW` and
`&CYBSP_I3C_CONTROLLER_context` ready to use, with no init of its own.

### A vendor library bug that freezes the screen — patch it before you build

This is the single most important thing about this episode: Bosch's `BMM350_SensorAPI` library (v1.10.0, vendored
into the master template) has a known bug over I3C. Inside `bmm350_init()`, a soft-reset command is sent to the
sensor, which resets the BMM350 back to I2C mode (its factory default). The driver then keeps trying to talk over
I3C to a sensor that no longer listens on I3C, so `bmm350_init()` blocks waiting for a response that never comes.
The result: `bmm350_presenter_start()` never returns, the LVGL event loop never starts, and **the screen stays
black from boot**. You can spot this from the serial log stopping right after `[MASTER] I3C init OK`, with no
`[BMM350] INIT_OK` line following it. A patch script (`bmm350_fix.bash`) or a one-time `sed` that comments out the
soft-reset line must be run once after `make getlibs`, before building. The master template deliberately does not
apply this patch automatically through `PREBUILD=`, because Windows has no bash available by default, and a
prebuild step like that makes builds non-deterministic (running `make getlibs` again after patching would silently
overwrite the patched file back to pristine).

### Calibration must satisfy two conditions, not just elapsed time

`bmm350_config.h` sets `BMM350_CALIBRATION_SAMPLES = 140` at a 120 ms poll period
(`BMM350_SAMPLE_PERIOD_MS`), totaling about 16.8 seconds (the source comment states this number directly, not a
rounded "15 seconds"). But reaching the sample count is not enough on its own — the code also checks
`BMM350_CALIBRATION_MIN_SPAN_UT = 20.0f`, meaning the max−min span of **both X and Y** must be at least 20 µT. If
the board sits still without rotating through all 140 samples, the span stays far narrower than that, and
calibration **never finishes**, even though the sample count target was met. The reason: with a narrow span, the
computed midpoint is meaningless as a hard-iron offset.

### The real code also does a simple soft-iron scale, not just a hard-iron offset as the upstream README says

The upstream README says "Soft-iron calibration will not be done in this episode — it would need an ellipsoid
fit, which is complex." But the comment in `bmm350_config.h` states directly: "Runtime heading calibration
(hard-iron + simple soft-iron scale)." The real code computes both the offset (the midpoint) **and** a per-axis
scale from the average X/Y span, to pull the ellipse closer to a circle in a simple way (not the full, complex
ellipsoid fit the upstream README refers to, but not "doing nothing at all" about scale distortion either).

### Calibration lives only in RAM and is lost on a board reset

Calibration state is a `static` variable held in RAM — it is never written to NVM the way the Wi-Fi profile is
(lesson 2.6). `bmm350_reader_init()` clears the calibration every time it is called, which is every time the board
boots. The user must press Calibrate again after every reset; to remember it across reboots, you would need to add
a store similar to the Wi-Fi profile's.

### Heading is computed from X/Y only, with no tilt compensation

`atan2f(y, x)`, applied to values already corrected by the hard-iron offset and soft-iron scale, gives the heading
angle directly — it never uses the Z axis or any tilt information from the accelerometer. Earth's magnetic field
has a vertical component too, so tilting the board changes the proportion measured on the X/Y axes and throws off
the heading even after a good calibration. The board must be held flat while reading a heading (tilt-compensated
heading would need to combine data from the BMI270, lesson 3.2 — one of this episode's suggested extensions).

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section and the BMM350
Vendor Code Fix section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md)
in full before actually building, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit).

[`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_config.h) — the real calibration constants:

```c
/* Runtime heading calibration (hard-iron + simple soft-iron scale)
 * At default 120 ms sample period and 140 samples = ~16.8 seconds.
 */
#define BMM350_CALIBRATION_SAMPLES             (140U)
#define BMM350_CALIBRATION_MIN_SPAN_UT         (20.0f)

/* Heading axis mapping for board orientation tuning.
 * Signs should be +1 or -1.
 */
#define BMM350_HEADING_SWAP_XY                 (0U)
#define BMM350_HEADING_X_SIGN                  (1)
#define BMM350_HEADING_Y_SIGN                  (1)
#define BMM350_HEADING_OFFSET_DEG              (0.0f)
```

[`app_ui/bmm350/bmm350_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_ui/bmm350/bmm350_presenter.c) — one `lv_timer`, same pattern as the rest of this module, with a touch-blocking overlay during calibration:

```c
void bmm350_presenter_start(I3C_CORE_Type *i3c_hw, cy_stc_i3c_context_t *i3c_context)
{
    bmm350_view_create();
    bmm350_view_set_calibrate_handler(bmm350_calibrate_requested_cb, NULL);

    cy_rslt_t init_rslt = bmm350_reader_init(i3c_hw, i3c_context);
    if (CY_RSLT_SUCCESS != init_rslt)
    {
        bmm350_view_set_init_failed();
        return;
    }

    bmm350_view_set_ready();
    bmm350_update_calibration_ui();

    /* Periodic sensor polling runs in LVGL task context. */
    (void)lv_timer_create(bmm350_poll_sensor_cb, BMM350_SAMPLE_PERIOD_MS, NULL);
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/main_example.c) hands the I3C handle to `bmm350_presenter_start()`, exactly as the upstream README describes
- [`app_sensor/bmm350/bmm350_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.c) wraps Bosch's SensorAPI with injected I3C read/write callbacks, exactly as the upstream README describes — this is the vendor file that needs patching before it builds (see above)
- See the full folder at [`int_ep04_bmm350_compass/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass)

## Common mistakes

- **Build/flash succeeds but the screen stays black from boot** — almost always a forgotten patch for the I3C
  soft-reset bug in `BMM350_SensorAPI`. Check the serial log for a `[BMM350] INIT_OK` line after
  `[MASTER] I3C init OK`; if it is missing, `bmm350_init()` is still blocked and the patch must be applied.
- **Assuming calibration is done once the time/sample count is reached** — if the board never rotates far enough
  to give X and Y a span of at least 20 µT, calibration never finishes even after 140 samples. The board must
  actually be rotated through every direction (a figure-8 motion).
- **Assuming calibration survives a board reset** — the value lives only in RAM; `bmm350_reader_init()` clears it
  on every boot, so calibration must be redone every time.
- **Forgetting heading has no tilt compensation** — if the board is not level, the reported heading drifts even
  after a good calibration.

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
