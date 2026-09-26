---
id: fw-stack.m04.l02
lang: en
title:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
summary:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์"
    en: "Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent"
  - th: "แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC"
    en: "Plot them as a scrolling scope and explain ADC resolution"
develops:
  - {skill: mcu.adc-dac, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_pot_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 027558dbe151cbd838c89e242f86213e911c8fa118e14f58c7e7ee3d58a7d061
---

# Analog voltages with the 12-bit SAR ADC

## Objectives

1. Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent
2. Plot them as a scrolling scope and explain ADC resolution

## Concepts

### What the QWA309 base board gives you to practise with

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board. Both exercises in this lesson read the same four potentiometers (VR1–VR4 on P15.4–P15.7), but present them differently: the first as a numeric-plus-bar dashboard, the second as a scrolling oscilloscope-style chart.

### What a 12-bit SAR ADC is, and what its numbers mean

The AUTANALOG SAR ADC is the PSoC Edge's built-in successive-approximation analog-to-digital converter. It returns a 12-bit integer, 0–4095 (`POT_ADC_FULL_SCALE = 4095`), measured against a reference voltage (`POT_ADC_VREF_MV = 1800`) — that is **1.8 V, not 3.3 V**. The resolution is therefore 1800 mV ÷ 4095 steps ≈ 0.44 mV per step, finer than the resolution at 3.3 V (≈ 0.81 mV) because the voltage range being divided is narrower. But finer resolution does not mean a steady reading — just a few millivolts of supply or reference noise already exceed 0.44 mV per step, so the raw value can be seen drifting by 1–3 counts even when the pot is untouched.

### Initialising the ADC in the UI module's own code, not the framework

Unlike the I2C bus, which the master template already opens (see lesson 1.1), reading the potentiometers requires initialising the SAR ADC entirely from scratch. `pot_adc_init()` first sets all four pins (P15.4–P15.7) to `CY_GPIO_DM_ANALOG` mode with `Cy_GPIO_Pin_FastInit()`, then calls `Cy_AutAnalog_Init(&autonomous_analog_init)` using the `autonomous_analog_init` config the BSP generates, followed by `Cy_AutAnalog_Enable()` and `Cy_AutAnalog_StartAutonomousControl()` to make the ADC convert continuously in the background. If `Cy_AutAnalog_Init()` fails (its return value does not equal `CY_AUTANALOG_SUCCESS`), neither exercise creates its polling timer, and the screen shows "ADC init failed" instead.

### Converting the raw value to voltage and percentage with integer math

Pot Monitor's `update_channel()` reads the result with `Cy_AutAnalog_SAR_ReadResult(POT_ADC_INDEX, CY_AUTANALOG_SAR_INPUT_GPIO, channel->adc_channel)`, masks it with `0x0FFFU` in case any stray bits arrive, then converts it with plain integer arithmetic (no float): `millivolts = raw * 1800 / 4095` and `percent_tenths = raw * 1000 / 4095` (in tenths of a percent, so one decimal digit can be printed without float). Example: raw = 2048 → 2048×1800/4095 = 900 mV (0.900 V) and 2048×1000/4095 = 500 (50.0 %). Integer division always truncates the remainder; it never rounds up.

### What "Live" and "ADC settling" tell you — and what they do not

`pot_timer_cb()` checks `Cy_AutAnalog_SAR_GetHSchanResultStatus(POT_ADC_INDEX)` against `POT_ADC_READY_MASK` (the combined mask of all four GPIO0–GPIO3 channels). If all four channels' bits are ready it shows "Live" in mint green; otherwise "ADC settling" in yellow. Notice that this function already called `update_channel()` to read and display all four channels in the loop above, without waiting for this status first. The "Live/settling" label is only a flag for whether the hardware conversion cycle has completed — not a gate on whether the on-screen numbers get updated.

### A scrolling oscilloscope: point count × sample period = the time window shown

ADC Scope converts the raw value to percent more simply than Pot Monitor: `pct = raw * 100 / SCOPE_FULL_SCALE` (a plain integer 0–100, no decimal), then feeds it into the chart with `lv_chart_set_next_value()` on an `lv_chart` configured with `lv_chart_set_update_mode(s_chart, LV_CHART_UPDATE_MODE_SHIFT)` — this mode shifts old points off the left as new points arrive on the right. The chart holds `SCOPE_POINTS = 100` points, sampled every `SCOPE_PERIOD_MS = 60` ms, so the time window visible on the chart equals the point count times the sample period: 100 × 60 ms = 6 seconds. Halving the period to 30 ms with the same point count would only cover 3 seconds — more time detail, but a shorter visible history.

### The VR1–VR4 names are not tied to the same index in both exercises

Pot Monitor's `pot_channels[]` maps VR1 to result index 1 (P15.5) and VR2 to result index 0 (P15.4) — swapped from the order one would naturally expect. ADC Scope, on the other hand, defines `s_ch[] = {0, 1, 2, 3}` with names `s_name[] = {"VR1","VR2","VR3","VR4"}` in plain index order. The result: turning the very same pot on pin P15.4 moves the **VR2** card in Pot Monitor but the **VR1** trace in ADC Scope, even though both are reading SAR channel index 0. The name shown on screen, the physical pin on the board, and the result index in the code are three separate things that always need to be checked against each other — never trust one example's on-screen name to match another's directly.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Potentiometer Monitor** — reads four potentiometers (P15.4–P15.7) through the AUTANALOG 12-bit SAR ADC (Vref 1.8 V), showing each as a bar plus voltage and percentage in real time — the first exercise to use a real ADC on the TESAIoT Dev Kit
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor)
- **QWA309 — 4-Channel ADC Scope** — plots all four potentiometers (P15.4–7, 12-bit SAR) as scrolling traces on a 0–100% LVGL chart — an analogue oscilloscope
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope)

The excerpts below are copied from the actual files at the same commit (Apache-2.0, tesaiot/developer-hub).

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — sets the pins to analog input, then starts the AUTANALOG SAR ADC:

```c
static bool pot_adc_init(void)
{
    uint32_t init_status;

    pot_adc_init_pin(P15_4_PORT, P15_4_PIN);
    pot_adc_init_pin(P15_5_PORT, P15_5_PIN);
    pot_adc_init_pin(P15_6_PORT, P15_6_PIN);
    pot_adc_init_pin(P15_7_PORT, P15_7_PIN);

    init_status = Cy_AutAnalog_Init(&autonomous_analog_init);
    if (CY_AUTANALOG_SUCCESS != init_status)
    {
        return false;
    }

    Cy_AutAnalog_Enable();
    Cy_AutAnalog_StartAutonomousControl();

    return true;
}
```

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — converts the raw value to voltage and percentage with integer math:

```c
raw = (uint16_t)Cy_AutAnalog_SAR_ReadResult(POT_ADC_INDEX,
                                            CY_AUTANALOG_SAR_INPUT_GPIO,
                                            channel->adc_channel);
raw &= 0x0FFFU;

millivolts = ((uint32_t)raw * POT_ADC_VREF_MV) / POT_ADC_FULL_SCALE;
percent_tenths = ((uint32_t)raw * 1000U) / POT_ADC_FULL_SCALE;
bar_value = ((uint32_t)raw * 1000U) / POT_ADC_FULL_SCALE;
```

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — VR1/VR2 swapped against the index order one would expect:

```c
static pot_channel_t pot_channels[POT_COUNT] =
{
    { "VR1", "P15.5  ADC5", 1U, 0x14B8A6, NULL, NULL, NULL, NULL },
    { "VR2", "P15.4  ADC4", 0U, 0x22C55E, NULL, NULL, NULL, NULL },
    { "VR3", "P15.6  ADC6", 2U, 0xF59E0B, NULL, NULL, NULL, NULL },
    { "VR4", "P15.7  ADC7", 3U, 0xF43F5E, NULL, NULL, NULL, NULL },
};
```

[`adc_scope_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/adc_scope_ui.c) — reads every channel and feeds it into the SHIFT-mode scrolling chart:

```c
static void scope_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    if (!s_adc_ok) { return; }
    for (uint8_t i = 0U; i < SCOPE_CH; i++) {
        uint16_t raw = (uint16_t)Cy_AutAnalog_SAR_ReadResult(SCOPE_ADC_INDEX,
                          CY_AUTANALOG_SAR_INPUT_GPIO, s_ch[i]) & 0x0FFFU;
        uint32_t pct = ((uint32_t)raw * 100U) / SCOPE_FULL_SCALE;
        lv_chart_set_next_value(s_chart, s_series[i], (int32_t)pct);
        lv_label_set_text_fmt(s_val[i], "%s %lu%%", s_name[i], (unsigned long)pct);
    }
}
```

## Common mistakes

- **Assuming the reference voltage is 3.3 V** — this SAR ADC uses `POT_ADC_VREF_MV = 1800` (1.8 V). Assuming 3.3 V instead breaks every voltage conversion from the raw value.
- **Treating a 1–3 count jitter as a broken ADC** — at a resolution of roughly 0.44 mV per step, just a few millivolts of noise is enough to make the reading drift; that is normal, and is reduced with a moving average, not a symptom of damage.
- **Comparing the VR1–VR4 names across exercises without checking the real index** — Pot Monitor and ADC Scope map the names to SAR indices differently (VR1/VR2 are swapped); always check `pot_channels[]`/`s_ch[]` in the code, or the board's schematic.
- **Waiting for the "Live" label before trusting the on-screen numbers** — the Live/ADC settling label only reports whether the hardware conversion cycle has completed; the code already updates the on-screen numbers every tick regardless of what the label says.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- With a 12-bit ADC at Vref 1.8 V, how many millivolts does each step resolve?
- Why does the reading jitter slightly even when the pot is not turned?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
