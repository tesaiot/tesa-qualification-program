---
id: fw-stack.m02.l01
lang: en
title:
  th: "หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย"
  en: "First LVGL screen: logo, title and subtitle"
summary:
  th: "หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen"
  en: "First LVGL screen: logo, title and subtitle"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง"
    en: "Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot"
  - th: "อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง"
    en: "Explain when the master template calls example_main(parent) and why we do not write main ourselves"
  - th: "สร้าง object tree screen → image → label และจัดวางด้วย align ได้"
    en: "Build a screen → image → label object tree and place it with align"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: lang.c, to: 2}
  - {skill: build.vendor-sdk, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep01_basic_label"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: e9907425445968901bad1ae83869302af5f0cfe6bb01ff49105a7f488831045b
---

# First LVGL screen: logo, title and subtitle

## Objectives

1. Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot
2. Explain when the master template calls example_main(parent) and why we do not write main ourselves
3. Build a screen → image → label object tree and place it with align

## Concepts

### Every LVGL widget is an `lv_obj_t *`

LVGL (Light and Versatile Graphics Library) represents every kind of widget — screen, image, label, button, menu —
with the same struct, `lv_obj_t`. So we create, style and place every kind of widget with the same API regardless
of what it is. `lv_screen_active()` (formerly `lv_scr_act()`) returns the `lv_obj_t *` of the screen currently
shown, and we use it as the parent when creating an episode's first widget.

### The object tree: screen → image → label

EP01 creates three widgets in a tree rooted at the screen: `screen` (the background) → `logo` (an image, a child
of screen) → `title` and `subtitle` (two labels). Placement uses two functions with different meanings —
`lv_obj_align(obj, align, x, y)` places `obj` relative to its own **parent**, while `lv_obj_align_to(obj, target,
align, x, y)` places `obj` relative to **another widget** (`target`) as the anchor. For example, title is placed
below the logo with `LV_ALIGN_OUT_BOTTOM_MID`, not below the screen directly — if the logo's size changes, title
moves with it automatically, because the anchor is a widget, not a fixed coordinate. The offsets used are 24 px
(logo from the top edge), 48 px (title below the logo) and 24 px (subtitle below title).

### Color and fonts: the units the code actually uses

Every color is set with `lv_color_hex(0xRRGGBB)`, which converts a hex literal into an `lv_color_t` — the
background uses `0x0F172A` (slate-900 from the Tailwind palette) together with `lv_obj_set_style_bg_opa(screen,
LV_OPA_COVER, LV_PART_MAIN)` so the fill is fully opaque (`LV_OPA_COVER` is the maximum opacity value).
`LV_PART_MAIN` means the main part of the widget that this style targets. Fonts must already be enabled in the
master's `lv_conf.h` (this episode uses 30 px for the title and 20 px for the subtitle) — picking a size that is
not enabled will either fail to build or silently fall back to a different font.

### Why the logo is embedded as a C array instead of loaded from a file

This board has no filesystem or SD card for LVGL to open an image file from at runtime. The logo image is
converted ahead of time into `lv_image_dsc_t APP_LOGO` — a struct holding both the header (size, color format) and
the raw pixel data — compiled straight into the same flash image as the program. `lv_image_set_src(logo,
&APP_LOGO)` therefore takes a pointer directly into flash: no file read, no I/O latency, and no dependency on any
filesystem.

### The episode's entry/exit contract

The master template (see lesson 1.1) calls `example_main(lv_scr_act())` exactly once, after FreeRTOS, the display
driver, the VGLite GPU and LVGL are all ready. This episode's `main_example.c` provides a strong definition of
`example_main()` and immediately forwards to `ui_ep01_basic_label_create()`, without using the `parent` value it
receives directly (marked with `(void)parent;`), because the UI-creation function calls `lv_screen_active()`
itself internally — designed this way so other episodes can copy the UI-creation code without changing its
signature. `main_example.c` also calls `tesaiot_add_thai_support_badge()` before building the episode's screen —
a master helper function that confirms Noto Sans Thai font files were bundled; it is not part of the UI tree EP01
teaches. After `example_main()` returns, the master loops `lv_timer_handler()` forever to redraw — EP01 has no
event or timer of its own, so it draws once and holds that image.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How**
first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md).
The excerpts below are copied from tesaiot/developer-hub (Apache-2.0) at the same commit.

[`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/main_example.c) — where the master hands control to the episode:

```c
void example_main(lv_obj_t *parent)
{
    /* Master template bundles Noto Sans Thai fonts — this badge
     * confirms to the developer that Thai rendering is available. */
    tesaiot_add_thai_support_badge();

    (void)parent;   /* The episode manages its own screen composition via lv_screen_active(). */

    ui_ep01_basic_label_create();
}
```

[`ui_ep01_basic_label.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c) — builds the episode's whole object tree:

```c
lv_obj_t *screen = lv_screen_active();
lv_obj_set_style_bg_color(screen, lv_color_hex(0x0F172A), LV_PART_MAIN);
lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, LV_PART_MAIN);

lv_obj_t *logo = lv_image_create(screen);
lv_image_set_src(logo, &APP_LOGO);
lv_obj_align(logo, LV_ALIGN_TOP_MID, 0, 24);

lv_obj_t *title = lv_label_create(screen);
lv_label_set_text(title, "EP01 - Basic Label");
lv_obj_set_style_text_color(title, lv_color_hex(0xF8FAFC), LV_PART_MAIN);
lv_obj_set_style_text_font(title, &lv_font_montserrat_30, LV_PART_MAIN);
lv_obj_align_to(title, logo, LV_ALIGN_OUT_BOTTOM_MID, 0, 48);
```

Notice the key API calls — `lv_image_create(parent)` creates an image widget with `screen` as its parent,
`lv_image_set_src()` takes a pointer to an `lv_image_dsc_t` embedded in flash (not a file path), `lv_obj_align()`
places relative to the parent, while `lv_obj_align_to()` places relative to another widget as anchor. The full
file also has a `subtitle` label placed the same way — see the [full file on the Developer Hub](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c).

- [`ui_ep01_basic_label.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.h) — declares the single `ui_ep01_basic_label_create(void)`

## Common mistakes

- **Using `lv_obj_align()` instead of `lv_obj_align_to()`** — to place title relative to the logo (which may
  change size), you must use `lv_obj_align_to(title, logo, ...)`, not `lv_obj_align(title, ...)`, which would
  place it relative to `screen` instead.
- **Forgetting to enable the font size in `lv_conf.h`** — `lv_font_montserrat_30`/`_20` must already be enabled in
  the master project. Picking a size that is not enabled either fails to build or silently substitutes a
  different font with no clear error.
- **Assuming you must use the `parent` you were handed directly** — `main_example.c` has `(void)parent;` because
  the UI-creation function calls `lv_screen_active()` itself internally; both values are the same active screen,
  but not using `parent` directly lets the episode be dropped into another project without changing the
  UI-creation function's signature.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label) and flash the ready-made firmware.

## See it work first

![Screen of EP01 — Basic Label on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/hmi_ep01_basic_label.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What has the master template already done for us before it calls example_main()?
- Why is the logo embedded as a C array (APP_LOGO) instead of being loaded from a file?
- If you wanted to move the title down by 20 px, which value in the code would you change?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
