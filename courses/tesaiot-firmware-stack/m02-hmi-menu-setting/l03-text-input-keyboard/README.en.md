---
id: fw-stack.m02.l03
lang: en
title:
  th: "รับข้อความด้วย textarea และ keyboard"
  en: "Text input with a textarea and keyboard"
summary:
  th: "lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number"
  en: "Text input with a textarea and keyboard"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l02]
objectives:
  - th: "เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK"
    en: "Connect lv_textarea to lv_keyboard and take input both in real time and on OK"
  - th: "สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown"
    en: "Switch the keyboard between normal and number modes from a dropdown"
  - th: "อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน"
    en: "Explain when a value should update immediately and when it should wait for confirmation"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep03_text_input_keyboard"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 2e138807a1daa6a7153fe96e095e49d10a9ded18af441007b0801c6e4a351e21
---

# Text input with a textarea and keyboard

## Objectives

1. Connect lv_textarea to lv_keyboard and take input both in real time and on OK
2. Switch the keyboard between normal and number modes from a dropdown
3. Explain when a value should update immediately and when it should wait for confirmation

## Concepts

### Why an on-screen keyboard at all

This board has no hardware keyboard. Every time the user must type something (a Wi-Fi name, a password, a
setpoint value), the code shows `lv_keyboard`, LVGL's ready-made keyboard widget. It does not work independently
of a textarea — it must be bound to one with `lv_keyboard_set_textarea(kb, ta)` so the keyboard knows which
textarea it is currently typing into.

### Two input modes: real-time versus commit-on-OK

EP03 places two textareas side by side to compare behavior. **Input A (Realtime)** binds the
`LV_EVENT_VALUE_CHANGED` event straight to its display label, so the label changes on every keypress on the
keyboard (good for a search box or a live preview). **Input B (Confirmed on OK)** does not sync its label while
typing at all — the value updates only when `LV_EVENT_READY` fires (the user pressed OK on the keyboard), which
suits a form that needs validation before it is applied, such as the Wi-Fi password in a later module. Which mode
to pick depends on whether an in-progress, possibly-incomplete value would cause a problem immediately — if not,
real time is fine; if it would, wait for commit.

### One callback, several events: branch on event code and target

`text_input_logic_textarea_event_cb` is bound to **both** textareas and receives **three** events
(`LV_EVENT_CLICKED`, `LV_EVENT_FOCUSED`, `LV_EVENT_VALUE_CHANGED`) inside a single function. The callback branches
using `lv_event_get_code(e)` and `lv_event_get_target(e)` — on CLICKED or FOCUSED it opens the keyboard and sets
`state->active_textarea = target` regardless of which textarea fired it, but on VALUE_CHANGED it updates the label
**only when `target == state->realtime_textarea`**. Input B subscribes to VALUE_CHANGED too, but the callback
simply does nothing with it. That is the entire reason A's value changes on every keystroke while B's does not
change until OK is pressed, even though the exact same events fire for both.

### On OK: which label updates depends on which textarea was active

`text_input_logic_keyboard_event_cb` is bound to the keyboard widget itself (not to a textarea) and receives
`LV_EVENT_READY` and `LV_EVENT_CANCEL`. When READY fires, the code checks whether `state->active_textarea` was the
confirmed or the realtime textarea at that moment and updates that side's label — in other words, **one keyboard
serves both textareas** by knowing which one it is currently typing for from the state the textarea callback set
on FOCUSED, not from a separate callback bound per textarea.

### The dropdown changes more than the keyboard's face

`text_input_apply_mode_for_target()` runs both when the dropdown changes and when a textarea gains focus. Picking
"Number" calls `lv_keyboard_set_mode(kb, LV_KEYBOARD_MODE_NUMBER)` **and**
`lv_textarea_set_accepted_chars(target, "0123456789")` together — so Number mode does not just relabel the keys,
it also **blocks every other character from being typed into the textarea at all**, even from a physical
keyboard. `text_input_apply_mode_for_all()` applies this to both textareas every time the dropdown changes, even
if neither one is currently focused.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How**
first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md).
The excerpts below are copied from tesaiot/developer-hub (Apache-2.0) at the same commit — the callback names here
follow the actual source code, which names things slightly differently from the How section of the upstream
README.

[`text_input_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.c) — the textarea callback separates CLICKED/FOCUSED from VALUE_CHANGED:

```c
void text_input_logic_textarea_event_cb(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    text_input_state_t *state = (text_input_state_t *)lv_event_get_user_data(e);
    lv_obj_t *target = (lv_obj_t *)lv_event_get_target(e);

    if(state == NULL || target == NULL) {
        return;
    }

    /* Keyboard opens only from input widgets (not from dropdown). */
    if(code == LV_EVENT_CLICKED || code == LV_EVENT_FOCUSED) {
        state->active_textarea = target;
        lv_keyboard_set_textarea(state->keyboard, target);
        text_input_apply_mode_for_target(state, target);
        text_input_show_keyboard(state);
        return;
    }

    /* Realtime output is bound only to Input A. */
    if(code == LV_EVENT_VALUE_CHANGED && target == state->realtime_textarea) {
        text_input_update_realtime_label(state);
    }
}
```

The keyboard's own callback separates READY (commit) from CANCEL:

```c
if(code == LV_EVENT_READY) {
    /* Confirm behavior depends on which input currently owns keyboard focus. */
    if(state->active_textarea == state->confirmed_textarea) {
        text_input_update_confirmed_label(state);
    } else if(state->active_textarea == state->realtime_textarea) {
        text_input_update_realtime_label(state);
    }
    text_input_hide_keyboard(state);
    return;
}

if(code == LV_EVENT_CANCEL) {
    text_input_hide_keyboard(state);
}
```

[`ui_text_input_keyboard.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.c) — binding all three of Input A's events to one callback:

```c
/* Input A: open keyboard + realtime update while typing. */
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_CLICKED, &s_text_input_state);
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_FOCUSED, &s_text_input_state);
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_VALUE_CHANGED, &s_text_input_state);
```

Input B registers the exact same three events (see the full file) — the callback simply chooses to do nothing
with its VALUE_CHANGED.

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/main_example.c), [`text_input_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.h), [`ui_text_input_keyboard.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.h) and [`ui_text_input_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_layout.h) (all the layout constants, to avoid magic numbers)

## Common mistakes

- **Assuming Cancel restores the textarea's original value** — the actual `LV_EVENT_CANCEL` handler only hides
  the keyboard; it calls no API to revert already-typed characters, because the textarea's text is edited for
  real as you type, not held in a temporary buffer. If you want "cancel reverts to the original value," you must
  back up the text yourself on FOCUSED and restore it yourself in the callback.
- **Forgetting Number mode also blocks characters at the textarea, not just the key labels** —
  `lv_textarea_set_accepted_chars()` is always called alongside `lv_keyboard_set_mode()`. To allow other
  characters again, you must call `lv_textarea_set_accepted_chars(ta, NULL)` to clear the filter.
- **Binding Input A's callback to Input B without checking `target`** — because one callback serves both
  textareas, forgetting to check `target == state->realtime_textarea` before updating a label will update the
  wrong input's label.
- **Mixing up callback names between the upstream How section and the real code** — the upstream README describes
  separate callbacks such as `text_input_logic_focus_cb` and `text_input_logic_realtime_change_cb`, but the actual
  code at commit `9a8e3ed` combines every textarea event into the single function
  `text_input_logic_textarea_event_cb`. When reading the code, trust the code.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard) and flash the ready-made firmware.

## See it work first

![Screen of EP03 — Text Input Keyboard on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/hmi_ep03_text_input_keyboard.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Which event tells you the user pressed OK on the keyboard?
- Should the Wi-Fi password field use real-time or commit-on-OK input, and why?
- What kind of mistake does number mode prevent?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
