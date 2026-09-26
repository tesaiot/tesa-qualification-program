---
id: fw-stack.m04.l01
lang: en
title:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
summary:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
level: L2
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง"
    en: "Read active-low pull-up buttons and count presses correctly"
  - th: "นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk"
    en: "Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style"
develops:
  - {skill: mcu.gpio, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_button_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 8a16b4afef640e06ea42a14d8d6e49955125f7de690ec59539c75e20df680d4c
---

# Base-board buttons and a menu without touch

## Objectives

1. Read active-low pull-up buttons and count presses correctly
2. Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style

## Concepts

### What the QWA309 base board gives you to practise with

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board. The first two exercises both use the same two base-board buttons as input, but read them with two different pieces of logic: the first one reads the "current state" (level) at all times, while the second one catches only "the moment the state just changed" (an edge).

### Active-low buttons with an internal pull-up

Both exercises set up the button pins with `Cy_GPIO_Pin_FastInit(port, pin, CY_GPIO_DM_PULLUP, 1UL, HSIOM_SEL_GPIO)`. The `CY_GPIO_DM_PULLUP` parameter tells the chip to enable its internal pull-up resistor, holding the pin HIGH whenever nothing is touching it, while `HSIOM_SEL_GPIO` selects plain digital I/O for the pin, with no peripheral attached. The button ties the pin to ground when pressed, pulling the level down to LOW, and `Cy_GPIO_Read()` returns 0 when pressed — so the code writes the "pressed" condition as `0U == Cy_GPIO_Read(...)` in both Push Button Monitor and Hardware Button Menu. Using the internal pull-up this way means no external resistor is needed, and the released state is always well-defined (never floating).

### Filtering bounce by counting ticks before trusting a new value (Push Button Monitor)

`button_monitor_ui.c` polls the buttons with `lv_timer_create(button_timer_cb, BUTTON_REFRESH_PERIOD_MS, NULL)`, where `BUTTON_REFRESH_PERIOD_MS = 25` (once every 25 ms). On each tick, `update_button()` compares the freshly sampled value (`sampled_pressed`) against the previous one. If the value changed, `debounce_count` resets to 0 and starts counting again; if it stayed the same, `debounce_count` increments by one, until it reaches `BUTTON_DEBOUNCE_TICKS = 2`, at which point the code accepts that the state has really changed (`stable_pressed`). That means the same level has to be read three times in a row, which at a 25 ms poll tick is roughly 50 ms before the state actually flips. This window filters out contact bounce shorter than that. `press_count` only increases when the "stable" state flips from released to pressed (not on every tick that reads LOW), while `hold_time_ms` resets to 0 on release and accumulates by `BUTTON_REFRESH_PERIOD_MS` on every tick where `stable_pressed` is true — so this value has a resolution of 25 ms steps, not a continuous clock.

### Catching the "falling edge" instead of a held level (Hardware Button Menu)

`hw_button_menu_ui.c` takes a different approach: `btn_pressed_edge()` has the same kind of debounce (`MENU_DEBOUNCE = 2`, counted on a `MENU_POLL_MS = 30` ms poll tick), but it returns `true` only for "the one tick where the stable state just flipped from released to pressed" — not `true` on every tick the button happens to still be held. This is the key difference from Push Button Monitor's `update_button()`, whose caller reads `stable_pressed` as a level on every tick. The effect: if you hold the MOVE button down for a long time, `menu_timer_cb()` advances the highlight forward exactly once per press. The menu has `MENU_ITEMS = 4` entries and wraps around with the modulo arithmetic `(s_sel + 1U) % MENU_ITEMS`. Buttons SW6 (MOVE) and SW5 (SELECT) each have their own `btn_t` struct and their own debounce state (`s_move`, `s_selb`), so pressing both at once does not interfere between them. Pressing SELECT only changes the status text; it never moves the highlight.

### Mismatched button names between the description and the code: SW9/SW10 vs SW5/SW6

Push Button Monitor's `metadata.json` and the top-of-file comment in `main_example.c` describe the buttons as "SW9 (P17.5) and SW10 (P17.7)". But the real code in `button_monitor_ui.c` names the buttons in the `buttons[]` array `"SW5"` (pin P17.7) and `"SW6"` (pin P17.5) — the same text that actually shows on screen. Hardware Button Menu, which drives the same two pins, calls them SW6 (P17.5, MOVE) and SW5 (P17.7, SELECT), matching Push Button Monitor's code naming exactly. In short, the SW9/SW10 names are a mismatched summary within the Developer Hub itself — trust the code that actually runs and the board's silkscreen labels.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Push Button Monitor** — reads buttons SW9 (P17.5) and SW10 (P17.7) as active-low pull-up inputs, showing pressed/released state plus a press counter on LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor)
- **QWA309 — Hardware Button Menu** — navigates an LVGL menu with physical buttons, SW6 = Move and SW5 = Select (no touch) — a headless/kiosk UX pattern
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu)

The excerpts below are copied from the actual files at the same commit (Apache-2.0, tesaiot/developer-hub).

[`button_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/button_monitor_ui.c) — configures the button pins as pull-up inputs before reading them:

```c
static void button_inputs_init(void)
{
    Cy_GPIO_Pin_FastInit(P17_5_PORT,
                         P17_5_PIN,
                         CY_GPIO_DM_PULLUP,
                         1UL,
                         HSIOM_SEL_GPIO);
    Cy_GPIO_Pin_FastInit(P17_7_PORT,
                         P17_7_PIN,
                         CY_GPIO_DM_PULLUP,
                         1UL,
                         HSIOM_SEL_GPIO);
}
```

[`button_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/button_monitor_ui.c) — tick-counting debounce before accepting a real state change (level):

```c
static void update_button(button_channel_t *button)
{
    bool sampled_pressed = (0U == Cy_GPIO_Read(button->port, button->pin_num));

    if (sampled_pressed == button->last_sample_pressed)
    {
        if (button->debounce_count < BUTTON_DEBOUNCE_TICKS)
        {
            button->debounce_count++;
        }
    }
    else
    {
        button->last_sample_pressed = sampled_pressed;
        button->debounce_count = 0U;
    }

    if ((button->debounce_count >= BUTTON_DEBOUNCE_TICKS) &&
        (sampled_pressed != button->stable_pressed))
    {
        button->stable_pressed = sampled_pressed;
        /* ... press_count++ on press / hold_time_ms reset on release ... */
    }
    /* ... hold_time_ms accumulation, apply_button_visual(button) ... */
}
```

[`hw_button_menu_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/hw_button_menu_ui.c) — the same kind of debounce, but returns `true` only once per press (edge):

```c
static bool btn_pressed_edge(btn_t *b)
{
    bool raw = (0U == Cy_GPIO_Read(b->port, b->pin));   /* active low */
    bool edge = false;
    if (raw == b->last) {
        if (b->cnt < MENU_DEBOUNCE) { b->cnt++; }
        if ((b->cnt >= MENU_DEBOUNCE) && (raw != b->stable)) {
            b->stable = raw;
            if (raw) { edge = true; }   /* press edge */
        }
    } else {
        b->cnt = 0U;
    }
    b->last = raw;
    return edge;
}
```

[`hw_button_menu_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/hw_button_menu_ui.c) — uses the edge result to move the highlight exactly once per press:

```c
static void menu_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    if (btn_pressed_edge(&s_move)) {
        s_sel = (uint8_t)((s_sel + 1U) % MENU_ITEMS);
        highlight();
        lv_label_set_text_fmt(s_status, "MOVE -> %s", s_items[s_sel]);
    }
    if (btn_pressed_edge(&s_selb)) {
        lv_label_set_text_fmt(s_status, "SELECT: %s", s_items[s_sel]);
    }
}
```

## Common mistakes

- **Forgetting the pull-up and leaving the pin high-Z** — if the button pin is set up as a plain input with no pull-up while the button only ties it to ground, the pin floats when released. The reading then drifts with noise, and the counter can increment on its own with nobody pressing anything. Always set `CY_GPIO_DM_PULLUP`.
- **Assuming a held button repeats the menu move** — in Hardware Button Menu the highlight moves exactly once per press, because `btn_pressed_edge()` returns `true` only on the falling edge, not on the held level. If auto-repeat while held is wanted, that logic has to be written separately.
- **Mixing the two patterns together** — plugging the level-reading code (`stable_pressed` from Push Button Monitor) directly into the menu would move the highlight on every poll tick for as long as the button stays pressed (every 30 ms), not once per press. Pick the pattern (level or edge) that matches the behaviour you actually want.

> The button names in the Developer Hub's description (SW9/SW10) do not match the exercise's code (SW5/SW6); follow the code and the board's silkscreen labels

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

- Why does an active-low button read 0 when pressed?
- One press but the counter jumps by two — what causes this, and how do you fix it?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
