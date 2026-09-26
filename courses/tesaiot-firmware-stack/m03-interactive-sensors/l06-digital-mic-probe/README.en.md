---
id: fw-stack.m03.l06
lang: en
title:
  th: "ไมโครโฟน PDM สเตอริโอและ level meter"
  en: "Stereo PDM microphone and a level meter"
summary:
  th: "เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL"
  en: "Stereo PDM microphone and a level meter"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l05]
objectives:
  - th: "เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา"
    en: "Capture the stereo PDM microphone and compute left/right sound levels"
  - th: "แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS"
    en: "Show the levels as a meter and explain whether it uses peak or RMS"
  - th: "ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน"
    en: "Test with sound from each side and confirm the channels are not swapped"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep06_digital_mic_probe"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: c494db7358e4f880179dc109f72b0a74ac2e9cd8c5dd95eceabe5cd96e57d8f2
---

# Stereo PDM microphone and a level meter

## Objectives

1. Capture the stereo PDM microphone and compute left/right sound levels
2. Show the levels as a meter and explain whether it uses peak or RMS
3. Test with sound from each side and confirm the channels are not swapped

## Concepts

### PDM versus PCM: why a MEMS mic sends PDM

PDM (Pulse Density Modulation) is a high-speed (1–3 MHz) 1-bit stream where **pulse density** represents the
signal amplitude, unlike PCM, where each sample is a multi-bit number (16/24-bit) at a much lower rate (8–48
kHz). Small MEMS microphones output PDM directly because their internal circuitry is simpler. The PSoC Edge's
PDM/PCM converter turns PDM into PCM in hardware (lowpass + decimate) before it reaches a FIFO the CPU reads.
This episode configures 16 kHz with 160 samples per channel per frame
(`PDM_MIC_FRAME_SAMPLES_PER_CHANNEL = 160`), which is exactly 10 ms per frame at 16 kHz.

### The real capture path is interrupt-driven FIFO reads plus a software double buffer, not DMA as the upstream README describes

The upstream README says "DMA-driven — the CPU stays out of it, hardware writes to a circular buffer" and "bind
the DMA channel to an IRQ handler." The real code at commit `9a8e3ed` **uses no DMA at all** — each channel (left
= channel 2, right = channel 3) has its own interrupt that fires when the FIFO reaches its trigger level
(`PDM_RX_FIFO_TRIG_LEVEL`, half the FIFO size), and `process_channel_irq()` reads samples out of the FIFO one at a
time with `Cy_PDM_PCM_Channel_ReadFifo()` into whichever buffer is currently being written
(`buffer0`/`buffer1`, ping-ponged **entirely in software**, not through a DMA descriptor). Once both channels
reach 160 samples (`PDM_READY_BOTH`), a semaphore wakes the waiting task to compute levels. The CPU really is
"busy" with every sample, through interrupts, rather than simply waiting for a DMA transfer to finish.

### The "average" computed is mean(|x|), not RMS, even though it plays a similar role

`compute_level()` computes `peak_abs` (the maximum |sample|) and `avg_abs` — the sum of |sample| divided by the
sample count. That is a mean of **absolute values**, with no squaring or square root anywhere, so it is **not
RMS** (root-mean-square). It rises and falls with loudness similarly to RMS and is cheaper to compute (no
multiplication), but it always reads lower than RMS for the same signal (for a pure sine wave, mean|x| ≈ 0.9 ×
RMS).

### The on-screen percentage is not peak/32767 directly — it is mapped through a floor/ceiling tuned for classroom speech

`to_ui_pct()` does not divide `avg_abs` by `INT16_MAX` (32767) directly, as the upstream README's formula
suggests (and that formula there actually uses peak, not average, anyway). The real code linearly clamps
`avg_abs` between `PDM_UI_FLOOR_ABS = 80` (giving 0%) and `PDM_UI_CEIL_ABS = 8000` (giving 100%). The source
comment states the reason directly: "Tuned for classroom speech level so UI% doesn't saturate too early." Normal
classroom speech is far quieter than int16 full scale — dividing by 32767 directly would barely move the bar, so
the usable range has to be "compressed" to fill it.

### The balance meter is already implemented, not just a suggested extension as the upstream README implies

The upstream README's Experiment Ideas section suggests "Balance meter — show (L-R)/(L+R) as a needle in the
center of the screen" as if it were not yet built. The real code already computes
`balance_lr = (L_avg - R_avg) * 100 / (L_avg + R_avg)` in `pdm_probe_logger.c`, and the view already shows an "L"
when balance > 3 or an "R" when balance < -3. This feature is ready from the very first build — nothing more to
write.

### The UI polls a "latest sample wins" snapshot every 50 ms, not `lv_async_call` at "50 Hz"

Same pattern seen in lesson 2.5 (WiFi scan): `mic_presenter.c` does not use `lv_async_call()` as the upstream
README describes ("lv_async_call at a 50 Hz cadence"). It creates an `lv_timer` at a 50 ms period (that is 20
times a second, not 50) that reads the latest sample written under `taskENTER_CRITICAL()`/`EXIT`. The producer
(the logger task) publishes a new sample every 10 ms, but the policy is "latest sample wins" (it overwrites the
old one) — a short click that appears and disappears within a single 10 ms frame may never be seen by the UI at
all, if the 50 ms timer reads after that frame has already been overwritten.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md)
to learn PDM/PCM, but **the excerpts below are copied from the actual files** (Apache-2.0, tesaiot/developer-hub,
same commit), because the capture mechanism and the level formulas differ from what the upstream README
describes.

[`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.c) — mean-abs, not RMS, and the floor/ceiling-clamped percentage:

```c
/* Tuned for classroom speech level so UI% doesn't saturate too early. */
#define PDM_UI_FLOOR_ABS              (80U)
#define PDM_UI_CEIL_ABS               (8000U)

static uint32_t to_ui_pct(uint32_t avg_abs)
{
    if (avg_abs <= PDM_UI_FLOOR_ABS) { return 0U; }
    if (avg_abs >= PDM_UI_CEIL_ABS)  { return 100U; }
    return ((avg_abs - PDM_UI_FLOOR_ABS) * 100U) / (PDM_UI_CEIL_ABS - PDM_UI_FLOOR_ABS);
}
```

[`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.c) — capture by interrupt-driven FIFO reads, not DMA:

```c
static void process_channel_irq(pdm_channel_state_t *state, uint8_t channel_index, uint8_t ready_bit)
{
    /* ... */
    for (uint32_t index = 0U; index < PDM_RX_FIFO_TRIG_LEVEL; index++)
    {
        int16_t sample = (int16_t)Cy_PDM_PCM_Channel_ReadFifo(CYBSP_PDM_HW, channel_index);
        /* write into state->active[out_idx++] until the frame is full, then swap active/full */
    }
    Cy_PDM_PCM_Channel_ClearInterrupt(CYBSP_PDM_HW, channel_index, CY_PDM_PCM_INTR_RX_TRIGGER);
}
```

[`app_ui/mic/mic_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_ui/mic/mic_presenter.c) — polling every 50 ms, latest-sample-wins:

```c
static void mic_presenter_ui_timer_cb(lv_timer_t *timer)
{
    mic_presenter_sample_t local = {0};
    bool has_sample = false;

    taskENTER_CRITICAL();
    has_sample = s_has_sample;
    if (has_sample) { local = s_latest_sample; }
    taskEXIT_CRITICAL();

    if (has_sample && s_view_ready) { mic_view_apply(&local); }
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/main_example.c) calls `mic_presenter_start()` before `pdm_probe_logger_start()`, exactly as the upstream README describes (build the consumer before the producer)
- See the full folder at [`int_ep06_digital_mic_probe/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe)

## Common mistakes

- **Assuming DMA is used, as the upstream README describes** — the real code uses interrupt-driven FIFO reads,
  one sample at a time, with a software-managed double buffer. Trust the real code when explaining the capture
  mechanism.
- **Assuming the computed average is RMS** — it is just the mean of absolute values (mean|x|), with no squaring
  at all, and always reads lower than RMS for the same signal.
- **Assuming the UI percentage is `avg*100/32767` directly** — it is actually clamped through the 80–8000 range
  tuned for quiet classroom speech. Anything quieter than 80 always shows 0%, and anything louder than 8000
  always shows 100%.
- **Assuming the UI catches every short click** — the "latest sample wins" policy at the 50 ms UI timer can miss
  a 10 ms frame containing a click entirely if the next frame overwrites it before the UI reads.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) and flash the ready-made firmware.

## See it work first

![Screen of EP06 — Digital Mic Probe on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/int_ep06_digital_mic_probe.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does PDM differ from PCM?
- How do RMS and peak give different pictures of the sound level?
- How do you test that the left and right channels are not swapped?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
