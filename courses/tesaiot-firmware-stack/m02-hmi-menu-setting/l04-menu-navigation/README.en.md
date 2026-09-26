---
id: fw-stack.m02.l04
lang: en
title:
  th: "โครง navigation: แถบเมนู หน้า และการสลับหน้า"
  en: "Navigation shell: menu bar, pages and page routing"
summary:
  th: "โครง navigation หลัก — top nav bar พร้อมปุ่มสลับหน้า + icon action buttons + หน้าต่าง ๆ ที่ lv_menu สร้างไว้ครั้งเดียวแล้วสลับตามเมนูที่เลือก (README ของ episode เล่าแบบ stage container แต่โค้ดใช้ lv_menu ให้ยึดตามโค้ด)"
  en: "Navigation shell: menu bar, pages and page routing"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l03]
objectives:
  - th: "สร้างเมนูนำทางด้วย lv_menu ที่สร้างทุกหน้าไว้ครั้งเดียว แล้วสลับหน้าที่แสดงตามเมนูที่เลือก"
    en: "Build navigation with lv_menu that creates every page once and switches the visible page from the menu"
  - th: "แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode"
    en: "Keep layout, navigation logic and pages apart, following the episode file structure"
  - th: "เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่"
    en: "Add one page to the menu without changing the existing pages"
develops:
  - {skill: gui.hmi, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: prog.state-machines, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep04_menu_navigation"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: e48374cc1f19628460781a009231509f7dcb65e1cad513ecfd0bb69aaf2db79b
---

# Navigation shell: menu bar, pages and page routing

## Objectives

1. Build navigation with lv_menu that creates every page once and switches the visible page from the menu
2. Keep layout, navigation logic and pages apart, following the episode file structure
3. Add one page to the menu without changing the existing pages

## Concepts

### The real code uses the `lv_menu` widget, not four nested containers as the upstream README describes

The episode's README on the Developer Hub says, in its How section, that the code creates four empty containers
(header/nav/stage/footer) and calls `lv_obj_clean()` plus rebuilds content every time the page switches. The
actual code at commit `9a8e3ed` instead uses **`lv_menu`**, LVGL's ready-made widget built specifically for
multi-page navigation — every page is created up front with `lv_menu_page_create(menu, title)`, and switching is
done purely with `lv_menu_set_page(menu, target_page)`, with no widget ever deleted or recreated. This lesson
follows the actual code, not the upstream README's How narrative.

### The screen layout: a fixed header, a fixed top nav, `lv_menu` in the middle, and a footer

`ui_menu_navigation_create()` lays the screen out as a vertical column (`LV_FLEX_FLOW_COLUMN`): a header (a
settings icon plus a title), a top nav row (Home/WiFi/Display/Info/Back buttons that are "always visible for
simple navigation in class", per the source's own comment), a content area holding the `lv_menu`, and a footer
status strip. `lv_menu` itself is configured with `lv_menu_set_mode_header(menu, LV_MENU_HEADER_TOP_FIXED)` and
`lv_menu_set_mode_root_back_button(menu, LV_MENU_ROOT_BACK_BUTTON_DISABLED)`, and both of its own internal headers
(`lv_menu_get_main_header()`, `lv_menu_get_sidebar_header()`) are hidden with `LV_OBJ_FLAG_HIDDEN`, because the
header and top nav we drew ourselves already do that job — forget to hide them and you get two headers stacked on
top of each other.

### Two entry points into the same destination: top nav and sidebar

Besides the always-visible top nav, the code also builds a hidden **sidebar page** ("Navigate") that opens and
closes via the settings icon in the header's corner. The sidebar links to the same three destinations as the top
nav (WiFi/Display/Device) — each entry point calls a different callback (for example, the top nav's WiFi button
and the sidebar's WiFi link both call `menu_nav_logic_wifi_btn_event_cb`), but both ultimately call the exact
same `menu_nav_set_page()`. Same destination, two doors in.

### Active-state highlighting must stay in sync in two places at once

Because there are two entry points (top nav and sidebar), every page change must have
`menu_nav_apply_active_state()` update the style of **both the top nav button and the sidebar link at once**,
comparing against `state->current_page`. Update only one side and a user who switches pages from the sidebar will
see the top nav button still highlighting the previous page (or vice versa).

### Why the page switch is deferred with `lv_async_call`

The most subtle part of this episode is `menu_nav_queue_page_switch()`, which does not call
`lv_menu_set_page()` immediately inside the callback. It stores `pending_page` first, then calls
`lv_async_call(menu_nav_async_apply_pending_page, state)`. The source comment states the reason directly: "Always
defer actual page switching to avoid lv_menu state race after sidebar transitions." `lv_async_call()` hands a
function to LVGL to run on the next tick instead of running it right there — every top nav button calls
`menu_nav_set_page(state, page_id, true)`, which may collapse the sidebar (`collapse_sidebar = true`) before
switching pages. Switching the page synchronously inside the very function that just told the sidebar to collapse
would collide with `lv_menu`'s own internal layout state, which has not finished adjusting yet. Deferring by one
tick lets the sidebar transition finish first, then switches the page.

### The footer status label is `printf`-style through `lv_label_set_text_fmt`

`menu_nav_update_status()` calls `lv_label_set_text_fmt(state->status_label, "Page: %s | Sidebar: %s", ...)` every
time after a page switch or a sidebar toggle, so the footer is the single place that reports both pieces of state
together.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md)
to understand the episode's purpose, but **the excerpts below are copied from the actual files** so they match
what really builds (Apache-2.0, tesaiot/developer-hub, same commit).

[`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.c) — deferring the page switch with `lv_async_call`:

```c
static void menu_nav_async_apply_pending_page(void *user_data)
{
    menu_nav_state_t *state = (menu_nav_state_t *)user_data;

    if(state == NULL || !state->page_switch_pending) {
        return;
    }

    state->page_switch_pending = false;
    menu_nav_apply_page_now(state, state->pending_page);
}

static void menu_nav_queue_page_switch(menu_nav_state_t *state, menu_nav_page_id_t page_id)
{
    if(state == NULL || state->menu == NULL) {
        return;
    }

    state->pending_page = page_id;

    if(!state->page_switch_pending) {
        state->page_switch_pending = true;
        lv_async_call(menu_nav_async_apply_pending_page, state);
    }
}
```

Hiding `lv_menu`'s own two internal headers, because the hand-drawn header/top nav already do that job:

```c
lv_obj_t *main_header = lv_menu_get_main_header(state->menu);
if(main_header != NULL) {
    lv_obj_add_flag(main_header, LV_OBJ_FLAG_HIDDEN);
}

lv_obj_t *sidebar_header = lv_menu_get_sidebar_header(state->menu);
if(sidebar_header != NULL) {
    lv_obj_add_flag(sidebar_header, LV_OBJ_FLAG_HIDDEN);
}
```

[`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_navigation.c) — creating `lv_menu` and all four pages up front:

```c
lv_obj_t *menu = lv_menu_create(content);
lv_menu_set_mode_header(menu, LV_MENU_HEADER_TOP_FIXED);
lv_menu_set_mode_root_back_button(menu, LV_MENU_ROOT_BACK_BUTTON_DISABLED);

lv_obj_t *home_page = create_full_content_page(menu, "Home", "Home", ...);
lv_obj_t *page_wifi = create_full_content_page(menu, "WiFi Manager", "WiFi Manager", ...);
lv_obj_t *page_display = create_full_content_page(menu, "Display Setting", "Display Setting", ...);
lv_obj_t *page_device = create_full_content_page(menu, "Device Info", "Device Info", ...);

lv_menu_set_page(menu, home_page);
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/main_example.c), [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.h) and [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_layout.h) (every component's layout constants) — see the full folder at [`hmi_ep04_menu_navigation/nav/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav)

## Common mistakes

- **Trusting the upstream README's How section completely** — it says the code uses header/nav/stage/footer
  containers with `lv_obj_clean()` plus rebuild on every page switch, but the real code uses `lv_menu`, which
  creates every page up front and only ever calls `lv_menu_set_page()` — no clean/rebuild at all. When the code
  and the prose disagree, trust the code.
- **Forgetting to hide `lv_menu`'s own internal headers** — without
  `lv_obj_add_flag(main_header, LV_OBJ_FLAG_HIDDEN)` (and the sidebar one), you get two headers stacked on top of
  each other, because `lv_menu` ships its own.
- **Calling `lv_menu_set_page()` right after toggling the sidebar without going through `lv_async_call`** — this
  collides with `lv_menu`'s own internal layout state, which has not finished adjusting after the sidebar
  transition, producing unpredictable behavior.
- **Updating the active-state style on only one side (top nav or sidebar)** — both must be updated together every
  time, because there are two entry points into the same destination.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation) and flash the ready-made firmware.

## See it work first

![Screen of EP04 — Menu Navigation on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/hmi_ep04_menu_navigation.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does lv_menu keep all the pages, and what are the pros and cons of building every page just once?
- If you add a new page, which files must you change?
- If you instead created a new page every time the menu switched, without deleting the old one, what would happen to memory?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
