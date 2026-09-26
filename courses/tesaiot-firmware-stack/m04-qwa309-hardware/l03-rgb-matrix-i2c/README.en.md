---
id: fw-stack.m04.l03
lang: en
title:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
summary:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V"
    en: "Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus"
  - th: "ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว"
    en: "Combine potentiometer input with matrix and screen output in one program"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_rgb_matrix"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 628dbe7d75d68b80990c582a13832dc3afb1610244eb0416c23e3dbfd4a8b7b0
---

# Driving an RGB dot matrix over I2C

## Objectives

1. Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus
2. Combine potentiometer input with matrix and screen output in one program

## Concepts

### What the QWA309 base board gives you to practise with

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board. All three exercises in this lesson drive the same RGB dot-matrix display (a DFRobot DFR0522) through a shared low-level I2C driver in `rgb_panel.c`, but differ in how they trigger it: direct button commands, an automatic animation, and colour mixing from potentiometers.

### What the DFR0522 is, and what commands it accepts

The DFR0522 is a 16×8-pixel RGB dot-matrix display (`RGB_PANEL_WIDTH = 16`, `RGB_PANEL_HEIGHT = 8`), driven over I2C at address `0x10` (`RGB_PANEL_I2C_ADDRESS`), supporting 8 colours (`RGB_PANEL_COLOR_OFF` through `RGB_PANEL_COLOR_WHITE`, values 0–7). Every command is assembled into one frame: the first byte is a fixed command register `0x02`, followed by a function byte that says whether to clear (`0x01`), fill the whole panel (`0x09`) or light a single pixel (`0x08`), then the colour value and the x/y coordinates. The whole frame is padded to a fixed `RGB_PANEL_TX_SIZE = 51` bytes (a 50-byte payload plus the 1-byte command register), so every command sends the same length regardless of what it does.

### Writing a byte-level I2C driver by hand, with no ready-made wrapper

`rgb_panel_write()` in `rgb_panel.c` drives I2C with three of the lowest-level PDL calls: `Cy_SCB_I2C_MasterSendStart()` sends the address with a write transfer, a loop of `Cy_SCB_I2C_MasterWriteByte()` then sends each byte until all `RGB_PANEL_TX_SIZE` bytes are out, and `Cy_SCB_I2C_MasterSendStop()` always closes the transaction, whether or not the byte writes succeeded (so the bus returns to a clean state instead of hanging). Every byte has a `RGB_PANEL_BYTE_TIMEOUT_MS = 5` ms timeout. All three exercises call this same driver through three public functions: `rgb_panel_clear()`, `rgb_panel_fill()` and `rgb_panel_pixel()`.

### Sharing the display/touch I2C bus, not the master's sensor I2C

All three exercises drive the DFR0522 through `DISPLAY_I2C_CONTROLLER_HW` and the `disp_touch_i2c_controller_context` context — the same SCB I2C instance used for the display and touchscreen, not the sensor I2C the master template opens (see lesson 3.1). The reason is that the sensor I2C sits on the 1.8 V domain, while the DFR0522 shares the 3.3 V bus with the display/touch. Wiring a device to the wrong voltage domain can fail to communicate, or damage the pins. It also matters that the framework already initialises this bus before `example_main()` ever runs, so the code can reuse the existing context immediately without re-initialising it (re-initialising it could break the touchscreen).

### Checking a device is really there before trusting the result

The "Check 0x10" button in DFR0522 RGB Dot Matrix calls `check_panel_device()`, which sends only a START with the address, then an immediate STOP — no data at all — to test whether any device ACKs that address. The result is a `cy_en_scb_i2c_status_t` value, translated into readable text by `i2c_status_to_text()`: for example "ADDRESS NACK" (nothing answered at all), "DATA NACK" (a device answered the address but rejected the data), "TIMEOUT", or "ARBITRATION LOST". This distinction matters: "ADDRESS NACK" points to a wiring, power or wrong-address problem, whereas an error that appears after the address is acknowledged points to a command-level or timing problem instead.

### Mixing R/G/B from potentiometers by packing bits (Pot → RGB Mixer)

Pot → RGB Mixer reads the first three potentiometers (channel indices 0–2 on P15.4–P15.6) every `MIX_REFRESH_MS = 120` ms. Each channel turns its own bit on if the raw value is ≥ `MIX_THRESHOLD = 2048` (about 50%): `bits |= (1U << i)`, with `i = 0` for R, `i = 1` for G, `i = 2` for B. The three bits together cast directly to `rgb_panel_color_t`, because the DFR0522's colour enum packs its bits in the same order (for example R and B both on gives bits 0b101 = 5 = `RGB_PANEL_COLOR_PURPLE`). The code only rewrites the panel when the colour changes from the previous tick (`if (color != s_last_color)`), so it does not resend a 51-byte frame every 120 ms on a bus shared with the touchscreen when nothing needs to change. `s_last_color` starts at `RGB_PANEL_COLOR_WHITE` to force the very first write.

### Animating with a frame-counting state machine (RGB Matrix FX)

RGB Matrix FX cycles through 3 effects automatically with an `lv_timer` at `FX_PERIOD_MS = 140` ms. The variable `s_frame` counts from 0 up to `FX_FRAMES_PER_EFFECT - 1` (24 frames) per effect, then `s_effect` advances to the next one modulo 3. `fx_step()` picks the behaviour by `s_effect`: effect 0 (Colour Cycle) calls `rgb_panel_fill()` on the whole panel, cycling through the `s_cycle[7]` colour array by `s_frame % 7`; effect 1 (Pixel Sweep) clears the panel then lights a single pixel at `x = (s_frame * 2) % FX_COLS`, `y = (s_frame / 2) % FX_ROWS`; effect 2 (Row Wipe) fills the whole panel with a colour that changes more slowly (`s_frame / 4`). Every effect calls the same `rgb_panel` driver as the other two exercises.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — DFR0522 RGB Dot Matrix** — drives a DFRobot DFR0522 8x16 RGB matrix (I2C address 0x10) on the 3.3 V bus alongside the display, showing clear/fill/pixel/pattern actions through the LVGL UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix)
- **QWA309 — RGB Matrix FX** — animated effects on the DFR0522 8x16 matrix (colour cycle / pixel sweep / row wipe), auto-cycling with status shown on the LCD
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix_fx&q=prac_qwa309_rgb_matrix_fx)
- **QWA309 — Pot → RGB Mixer** — three potentiometers act as the R/G/B channels (over 50% turns that colour on), mixed into one of the DFR0522 matrix's 8 colours and shown on the LCD — combining the SAR pots with RGB over I2C
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_rgb_mixer&q=prac_qwa309_pot_rgb_mixer)

The excerpts below are copied from the actual files at the same commit (Apache-2.0, tesaiot/developer-hub).

[`rgb_panel.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/rgb_panel.c) — the byte-level I2C driver all three exercises share:

```c
status = Cy_SCB_I2C_MasterSendStart(base,
                                    RGB_PANEL_I2C_ADDRESS,
                                    CY_SCB_I2C_WRITE_XFER,
                                    RGB_PANEL_BYTE_TIMEOUT_MS,
                                    context);

if (status == CY_SCB_I2C_SUCCESS)
{
    for (uint32_t i = 0U; i < RGB_PANEL_TX_SIZE; i++)
    {
        status = Cy_SCB_I2C_MasterWriteByte(base,
                                            tx_buffer[i],
                                            RGB_PANEL_BYTE_TIMEOUT_MS,
                                            context);
        if (status != CY_SCB_I2C_SUCCESS) { break; }
    }
}

stop_status = Cy_SCB_I2C_MasterSendStop(base,
                                        RGB_PANEL_BYTE_TIMEOUT_MS,
                                        context);
```

[`rgb_matrix_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/rgb_matrix_ui.c) — checks whether a device ACKs address 0x10 before any real command is sent:

```c
static cy_en_scb_i2c_status_t check_panel_device(void)
{
    cy_en_scb_i2c_status_t status;

    status = Cy_SCB_I2C_MasterSendStart(DISPLAY_I2C_CONTROLLER_HW,
                                        RGB_PANEL_I2C_ADDRESS,
                                        CY_SCB_I2C_WRITE_XFER,
                                        DEVICE_CHECK_TIMEOUT_MS,
                                        &disp_touch_i2c_controller_context);
    (void)Cy_SCB_I2C_MasterSendStop(DISPLAY_I2C_CONTROLLER_HW,
                                    DEVICE_CHECK_TIMEOUT_MS,
                                    &disp_touch_i2c_controller_context);
    return status;
}
```

[`pot_rgb_mixer_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/pot_rgb_mixer_ui.c) — packs R/G/B bits from the threshold and writes the panel only when the colour changes:

```c
uint8_t bits = 0U;
for (uint8_t i = 0U; i < 3U; i++) {
    uint16_t raw = mix_read(s_ch[i].ch);
    /* ... update bar/label ... */
    if (raw >= MIX_THRESHOLD) { bits |= (uint8_t)(1U << i); }
}

/* bits: b0=R b1=G b2=B  ->  DFR0522 colour enum is the same RGB packing. */
rgb_panel_color_t color = (rgb_panel_color_t)bits;
if (color != s_last_color) {
    s_last_color = color;
    (void)rgb_panel_fill(DISPLAY_I2C_CONTROLLER_HW,
                         &disp_touch_i2c_controller_context, color);
}
```

[`rgb_fx_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/rgb_fx_ui.c) — picks the effect by `s_effect` and draws one frame:

```c
switch (s_effect) {
case 0U:  /* colour cycle — one fill per frame */
    (void)rgb_panel_fill(FX_HW, FX_CTX, s_cycle[s_frame % 7U]);
    break;
case 1U: { /* pixel sweep — clear then light one pixel */
    (void)rgb_panel_clear(FX_HW, FX_CTX);
    uint8_t x = (uint8_t)((s_frame * 2U) % FX_COLS);
    uint8_t y = (uint8_t)((s_frame / 2U) % FX_ROWS);
    (void)rgb_panel_pixel(FX_HW, FX_CTX, x, y, s_cycle[s_frame % 7U]);
    break;
}
```

## Common mistakes

- **Wiring the DFR0522 to the master's sensor I2C instead of the display/touch 3.3 V bus** — the sensor I2C sits on the 1.8 V domain; wiring the wrong voltage domain can fail to communicate or damage the pins. Always use `DISPLAY_I2C_CONTROLLER_HW`.
- **Treating "ADDRESS NACK" and a later error as the same problem** — ADDRESS NACK means nothing answered at all (check the cable, power, address); an error after the address is acknowledged is a command-level or timing problem, a different cause entirely.
- **Rewriting the panel on every poll tick without checking whether the colour changed** — Pot → RGB Mixer only writes when the colour actually changes, to spare the bus it shares with the touchscreen. If the first computed colour happens to match the `s_last_color` starting value (WHITE), the panel stays unwritten until the colour genuinely changes.
- **Forgetting that `rgb_panel_fill()`/`rgb_panel_pixel()` always validate their parameters first and return `CY_SCB_I2C_BAD_PARAM`** — an out-of-range colour or coordinate is caught inside the driver itself, before anything wrong ever reaches the bus.

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

- What tells two devices on the same I2C bus apart?
- If the matrix does not respond, what should you check first (cable, power, address)?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
