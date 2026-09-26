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
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep07_sensorhub_final"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: f6e5c076b8fe00395c053ad5210d9c97e3b1f3ebeb5e12795fb53bffe26eb84e
---

# SensorHub: one dashboard for every sensor (series project)

## Objectives

1. Combine the DPS368, SHT4x, BMI270, BMM350 and PDM microphone on one dashboard
2. Schedule each sensor read so the screen does not stutter
3. Present the dashboard and explain how each value is shown

## Concepts

### One `lv_timer` orchestrates four sensors, not four FreeRTOS tasks as the upstream README describes

The upstream README describes this episode creating "4 reader tasks (2 KB stack each) at equal priority" that
push data through a single tagged-union message queue, dispatched by a consumer through `lv_async_call()`. The
real code at commit `9a8e3ed` has **no** `xTaskCreate`, `xQueueCreate`, or `lv_async_call` anywhere in
`sensorhub_presenter.c`. The real architecture is **one** `lv_timer` at `HUB_UI_POLL_MS = 100`, acting as its own
cooperative scheduler — every 100 ms it checks which sensors are due and reads only those. Everything still runs
on the single LVGL thread; no other thread ever touches sensor reading.

### A "next due time" per sensor, all inside one timer

Each sensor has its own `next_..._ms` variable (`next_dps_ms`, `next_sht_ms`, `next_bmi_ms`, `next_bmm_ms`).
Every time the timer runs (every 100 ms), it checks `(int32_t)(now_ms - next_xxx_ms) < 0`; if not due yet, it
skips that sensor, and if due, it reads that sensor and sets the next due time to
`now_ms + <that sensor's own period>`. Each period is exactly the value from that sensor's own lesson, unchanged
(`DPS368_SAMPLE_PERIOD_MS = 1000`, `SHT4X_SAMPLE_PERIOD_MS = 1000`, `BMI270_SAMPLE_PERIOD_MS = 200`,
`BMM350_SAMPLE_PERIOD_MS = 120`) — **not** the 200/500/20/50 ms table the upstream README states.

### A side effect of the 100 ms tick: periods that are not multiples of 100 get rounded up

Because the main timer ticks exactly every 100 ms, a sensor whose own period is not a multiple of 100 (such as
BMM350 at 120 ms) can never actually be read on its own exact period. At t=100 ms, 120 has not been reached yet,
so it is skipped; at t=200 ms it has, so it reads and sets next to 320, which then gets skipped again at t=300,
reading for real only at t=400. The effective period in practice becomes 200 ms, not 120 ms. A measurable
consequence: **BMM350's auto-calibration, which needs 140 samples (lesson 3.4), takes about 28 seconds in this
episode, not the 16.8 seconds it takes running alone in EP04**, because every sample now arrives roughly twice as
slowly due to this rounding.

### BMM350 calibration starts automatically at boot, unlike lesson 3.4's button press

`sensorhub_presenter_start()` calls `bmm350_reader_start_calibration()` itself immediately at startup, unlike
lesson 3.4, where the user had to press a Calibrate button. This dashboard wants the compass ready as soon as
possible without the user needing to know an extra step (they just need to rotate the board as instructed while
the other pages keep working).

### The real screen is five tabs, not a 2×2 grid plus a bottom bar as the upstream README draws it

The upstream README draws the layout as a 2×2 grid (DPS368/SHT4x on top, BMI270/BMM350 below) plus a mic bar at
the bottom, all shown at once. The real code has a `sensorhub_page_t` enum with five values
(`SENSORHUB_PAGE_HOME`, `_ENV`, `_MOTION`, `_COMPASS`, `_AUDIO`), and `sensorhub_view_set_active_page()` hides
whichever page is not selected — this is a **tabbed, one-page-at-a-time** view, following the same navigation
shell pattern from module 2 (lesson 2.4 onward), not all tiles shown together on one screen. The Audio page itself
shows the **already-computed** sound level (peak/average, from lesson 3.6), not a raw waveform.

### The BMM350 patch is still required

The BMM350 SensorAPI's I3C soft-reset bug (explained in detail in lesson 3.4) lives in the exact same library this
episode uses — it must be patched before building here too. The fix is idempotent, so if it was already applied
for EP04 in the same workspace, it does not need to be redone.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md)
to understand the capstone's brief, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the real architecture differs substantially from what the upstream
README describes.

[`app_ui/sensorhub/sensorhub_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_ui/sensorhub/sensorhub_presenter.c) — one `lv_timer` calling every sensor's poll each tick:

```c
static void sensorhub_poll_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    uint32_t now_ms = lv_tick_get();

    sensorhub_poll_dps(now_ms);
    sensorhub_poll_sht(now_ms);
    sensorhub_poll_bmi(now_ms);
    sensorhub_poll_bmm(now_ms);
    sensorhub_poll_bmm_calibration();
    sensorhub_poll_mic();
    /* ... */
}
/* ... */
s_ctx.poll_timer = lv_timer_create(sensorhub_poll_timer_cb, HUB_UI_POLL_MS, NULL);
```

The "next due time" pattern for one sensor (DPS368 shown; the same shape repeats for SHT4x/BMI270/BMM350):

```c
/* Poll DPS368 on its own sampling period and push value to Env page. */
static void sensorhub_poll_dps(uint32_t now_ms)
{
    if ((!s_ctx.dps_ready) || ((int32_t)(now_ms - s_ctx.next_dps_ms) < 0))
    {
        return;
    }

    s_ctx.next_dps_ms = now_ms + DPS368_SAMPLE_PERIOD_MS;

    dps368_sample_t sample;
    if (dps368_reader_poll(&sample))
    {
        s_ctx.dps_sample = sample;
        sensorhub_view_update_env(&s_ctx.dps_sample, s_ctx.has_sht ? &s_ctx.sht_sample : NULL);
        /* ... */
    }
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/main_example.c) calls `sensorhub_presenter_start()` then `pdm_probe_logger_start()`, exactly as the upstream README describes
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/bmi270/bmi270_config.h), [`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/bmm350/bmm350_config.h), [`app_sensor/dps368/dps368_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/dps368/dps368_config.h), [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/sht4x/sht4x_config.h) — each sensor's real period, unchanged from its own lesson
- See the full folder at [`int_ep07_sensorhub_final/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final) — each sensor's own driver/reader files are identical to lessons 3.1–3.4; only the UI layer that combines them is new

## Common mistakes

- **Assuming there are 4 FreeRTOS tasks plus a queue, as the upstream README describes** — the real code uses one
  `lv_timer` as a cooperative scheduler. Trust the real code when explaining the architecture.
- **Misremembering the read periods as 200/500/20/50 ms** — the real values are 1000/1000/200/120 ms, taken
  directly from each sensor's own unmodified config.h.
- **Forgetting the 100 ms main tick rounds up periods that are not multiples of 100** — BMM350 (120 ms) is
  actually read every 200 ms in practice, making auto-calibration take nearly twice as long as it does running
  alone in EP04.
- **Assuming the screen shows every tile at once in a 2×2 grid** — it is really five tabs
  (Home/Env/Motion/Compass/Audio), showing one page at a time.
- **Forgetting to patch the BMM350 bug** — the same bug from lesson 3.4 is still present; it must be patched
  before building here too.

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
