---
id: fw-stack.m02.l02
lang: en
title:
  th: "ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
summary:
  th: "ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l01]
objectives:
  - th: "ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT"
    en: "Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT"
  - th: "แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น"
    en: "Separate UI logic from counter logic into different files and explain why that makes testing easier"
  - th: "เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้"
    en: "Add one new button that reuses the same logic"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: prog.design-patterns, to: 1}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep02_button_event"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 7584b38d3649ed29dcb9d5b49118a17eeef8859bc8dd90d5061d415672b1e4a1
---

# Buttons and event callbacks: an UP / DOWN / RESET counter

## Objectives

1. Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT
2. Separate UI logic from counter logic into different files and explain why that makes testing easier
3. Add one new button that reuses the same logic

## Concepts

### Event-driven programming in LVGL

After EP01, which drew a purely static screen, EP02 adds something every embedded GUI needs: an **event
callback** — a function LVGL calls itself when an event matching a registered filter occurs. It is attached with
`lv_obj_add_event_cb(obj, callback, filter, user_data)`, where `filter` picks which event type to receive
(`LV_EVENT_PRESSED`, `LV_EVENT_LONG_PRESSED_REPEAT`, `LV_EVENT_CLICKED`, etc.) and `user_data` is a pointer we
supply ourselves so the callback can read it back with `lv_event_get_user_data(e)`. This technique replaces global
variables, because each button can send its own `user_data` while the same callback serves several buttons at
once.

### Tap and hold are simply different events

`LV_EVENT_PRESSED` fires the instant a finger touches the widget, with no need to wait for release.
`LV_EVENT_LONG_PRESSED_REPEAT` fires repeatedly every N milliseconds for as long as the press is held (N is set in
`lv_conf.h` via `LV_INDEV_DEF_LONG_PRESS_REP_TIME`). EP02 attaches the same callback to both events on the same
button (two separate `lv_obj_add_event_cb()` calls), and the callback checks `lv_event_get_code(e)` to pick a
different delta — a plain tap moves 1 unit, while a held press moves 5 units on every repeat.

### Separating UI from logic: why it matters

`ui_button_counter.c` knows LVGL fully (creates widgets, sets colors, places them), but `counter_logic.c` **does
not call LVGL widget APIs directly** — it only knows the `lv_obj_t *` of the label it must update text on, and
keeps its own state in a `struct` (`counter_state_t`) separate from the UI. This design lets the UP and DOWN
buttons **share the exact same callback** (`counter_logic_button_event_cb`); they differ only in the payload
passed through `user_data` (`tap_delta`/`hold_repeat_delta` being positive or negative). Adding a new button that
reuses the same logic therefore needs no new callback at all — just a new `counter_button_action_t` bound to the
existing callback.

### Where state lives, and why it must be `static`

`s_counter_state`, `s_up_action` and `s_down_action` in `ui_button_counter.c` are file-scope **`static`**
variables, not local variables inside `ui_button_counter_create()`. The reason: `lv_obj_add_event_cb()` stores the
`user_data` **pointer** to call later (every time the user presses the button, long after the UI-creation function
has already returned). If `s_up_action` were a local variable on the stack, it would be destroyed the moment
`ui_button_counter_create()` returns, leaving the callback reading a dangling pointer. `counter_logic_init()`
likewise only stores the label's pointer in the state rather than copying data, so it must be updated through
`state->value_label` for the same reason.

### Laying out buttons in a row with flex layout

The three-button row uses `lv_obj_set_layout(btn_row, LV_LAYOUT_FLEX)` together with
`lv_obj_set_flex_flow(btn_row, LV_FLEX_FLOW_ROW)` so LVGL arranges children left to right automatically, CSS
flexbox style, with no need to compute each button's `x` by hand. `lv_obj_set_flex_align(...,
LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER)` centers both along the main axis and the cross
axis, and `lv_obj_set_style_pad_column(btn_row, 20, LV_PART_MAIN)` leaves 20 px of gap between buttons. Each
button still uses the label-on-button pattern: create `lv_label_create(btn)` as the button's child, then
`lv_obj_align(lbl, LV_ALIGN_CENTER, 0, 0)` to center the text inside the button.

### Scaling the logo with `lv_image_set_scale`

`lv_image_set_scale(logo, 128)` shrinks the logo to half size, because LVGL uses **256 to mean 1.0x** (a
fixed-point scale), so 128 equals 0.5x — unlike EP01, which used the logo at full size with no scaling at all.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How**
first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md).
The excerpts below are copied from tesaiot/developer-hub (Apache-2.0) at the same commit.

[`counter_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.c) — one callback handles both tap and hold, branching on the event code:

```c
void counter_logic_button_event_cb(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    counter_button_action_t *action = (counter_button_action_t *)lv_event_get_user_data(e);

    if(action == NULL || action->state == NULL) {
        return;
    }

    if(code == LV_EVENT_PRESSED) {
        counter_logic_apply_delta(action->state, action->tap_delta);
        counter_logic_log_action("TAP", action->tap_delta, action->state->value);
        return;
    }

    if(code == LV_EVENT_LONG_PRESSED_REPEAT) {
        counter_logic_apply_delta(action->state, action->hold_repeat_delta);
        counter_logic_log_action("HOLD_REPEAT", action->hold_repeat_delta, action->state->value);
    }
}
```

[`ui_button_counter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.c) — the UP button binds the same callback twice, once per event:

```c
/* Event payload: tap +1, hold-repeat +5. */
s_up_action.state = &s_counter_state;
s_up_action.tap_delta = 1;
s_up_action.hold_repeat_delta = 5;
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb, LV_EVENT_PRESSED, &s_up_action);
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb, LV_EVENT_LONG_PRESSED_REPEAT, &s_up_action);
```

Notice `s_up_action` is a file-scope `static` variable (see why in Concepts above), and the DOWN button calls the
**exact same** `counter_logic_button_event_cb`, just passing `s_down_action` with `tap_delta = -1` instead — no
new callback to write.

[`counter_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.h) and [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/main_example.c) share the same shape as EP01: forward to `ui_button_counter_create()`.

## Common mistakes

- **Passing `user_data` as a local (stack) variable** — it must be `static` or global, because
  `lv_obj_add_event_cb()` stores the pointer to call later. A stack variable dies as soon as the UI-creation
  function returns, leaving the callback reading a dangling pointer.
- **Forgetting that RESET checks both `LV_EVENT_PRESSED` and `LV_EVENT_CLICKED`** — unlike UP/DOWN, which check
  only `LV_EVENT_PRESSED`. If you copy the UP/DOWN callback for a new button that needs RESET-like behavior, check
  which event codes actually match the behavior you want.
- **Assuming one `lv_obj_add_event_cb()` call can catch both tap and hold** — you must register **twice**, once
  per `filter` (`LV_EVENT_PRESSED` and `LV_EVENT_LONG_PRESSED_REPEAT`), because each call's `filter` takes a
  single event code.
- **Forgetting `lv_image_set_scale` is base-256, not base-100** — 256 means 1.0x, not a percentage; 128 is 0.5x,
  not "128%".

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event) and flash the ready-made firmware.

## See it work first

![Screen of EP02 — Button Event on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/hmi_ep02_button_event.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How do LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT differ when a button is held down?
- Does counter_logic.c know about LVGL at all, and why was it designed that way?
- If the counter must never go negative, which file should you change?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
