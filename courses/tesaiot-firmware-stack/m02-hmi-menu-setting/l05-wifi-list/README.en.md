---
id: fw-stack.m02.l05
lang: en
title:
  th: "สแกน Wi-Fi และแสดงรายการเครือข่าย"
  en: "Wi-Fi scan and a network list"
summary:
  th: "สแกน WiFi ผ่าน WHD/cy_wcm แล้วแสดงผลเป็น list พร้อม RSSI + security type — เพิ่มหน้า WiFi Scan เข้าไปใน shell ของ EP04"
  en: "Wi-Fi scan and a network list"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l04]
objectives:
  - th: "สแกน Wi-Fi ผ่าน WHD/cy_wcm แล้วแสดงรายการพร้อม RSSI และชนิด security"
    en: "Scan Wi-Fi through WHD/cy_wcm and list networks with RSSI and security type"
  - th: "แยก scan service ออกจากหน้า UI และส่งผลสแกนเข้าหน้าอย่างปลอดภัย"
    en: "Keep the scan service apart from the UI page and hand results to the page safely"
  - th: "อ่านค่า RSSI และบอกได้ว่าเครือข่ายใดสัญญาณดีพอจะเชื่อมต่อ"
    en: "Read RSSI values and judge which network is strong enough to join"
develops:
  - {skill: proto.wifi, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: rtos.basics, to: 1}
  - {skill: iot.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep05_wifi_list"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: f70e1eabf2a6b8caebabf0d373271a386f7edf3feee3b157bcdb5d3bb6995dd3
---

# Wi-Fi scan and a network list

## Objectives

1. Scan Wi-Fi through WHD/cy_wcm and list networks with RSSI and security type
2. Keep the scan service apart from the UI page and hand results to the page safely
3. Read RSSI values and judge which network is strong enough to join

## Concepts

### Scanning Wi-Fi goes through a three-layer stack

Scanning on the PSoC Edge passes through `whd` (the WiFi Host Driver, talking SDIO to the radio module) →
`cy_wcm` (the Connection Manager, wrapping `whd` in a higher-level scan/connect API) → the application's own
callback, which `cy_wcm` calls every time it discovers a new AP. This episode wraps all three layers in a
**service layer** (`wifi_scan_service.c`) so the UI page (`ui_wifi_list_page.c`) only ever calls
`wifi_scan_service_start()` / `wifi_scan_service_process()`, without needing to know `cy_wcm` at all.

### Pre-init: warm up the radio at boot, not on the button press

`example_main()` calls `wifi_scan_service_preinit()` before the UI is even created. This function does the SDIO
bring-up (setting up the SDIO and host-wake interrupt handlers, registering the SDHC controller's deep-sleep
callback) and `cy_wcm_init()`, all at boot time. If that were done on the first "Scan" tap instead, the user would
see the UI freeze for 1–3 seconds while the radio bring-up runs. This pre-init pattern makes the first tap just as
fast as every later one. If pre-init fails, the code merely logs it and lets the UI open anyway (only Scan itself
will then fail when tried).

### The WHD callback never touches LVGL at all — unlike what the upstream README describes

The episode's README on the Developer Hub says it uses `lv_async_call()` to hand work from the WHD callback back
to the LVGL thread. The actual code at commit `9a8e3ed` uses a different pattern instead: **a critical section
plus a poll timer**. `wifi_scan_callback()` (called from the WCM's own internal task, not the LVGL task) only
copies each AP's result into an array inside FreeRTOS's `taskENTER_CRITICAL()` / `taskEXIT_CRITICAL()`, then sets
the `scan_done_pending`/`scan_error_pending` flags — it never calls a single LVGL widget API. This is just as safe
from races as `lv_async_call()`, just a different mechanism.

### The LVGL side polls the flag instead of being woken up

`ui_wifi_list_page_create()` creates `lv_timer_create(ui_wifi_poll_timer_cb, UI_WIFI_POLL_MS, NULL)` with
`UI_WIFI_POLL_MS = 150`. Every 150 milliseconds, `ui_wifi_poll_timer_cb()` — which already runs on the LVGL thread
and so may safely call widget APIs — calls `wifi_scan_service_process()`, which reads and clears the
`scan_done_pending`/`scan_error_pending` flags inside the same critical section. If the flag says the scan is
done, it then reads the result list and re-renders. In short: **data crosses threads through a critical section,
notification crosses threads through periodic polling**, rather than being pushed into LVGL immediately the way
`lv_async_call()` would. Both approaches are equally correct and safe; they are simply different mechanisms — this
lesson follows the actual code.

### Preventing overlapping scans lives in the service, not just at the button

`wifi_scan_service_start()` checks `service->scanning` first and returns `false` right away if a scan is already
running. The UI side also sets `LV_STATE_DISABLED` on the Scan button while waiting for results. This two-layer
guard (the service layer inside, the UI button outside) keeps the system safe even if the UI side ever forgets to
disable the button itself.

### RSSI, invisible SSIDs, and sorting the results

Scan results are sorted strongest-to-weakest signal (`wifi_scan_sort_by_rssi_desc`) before being displayed. An AP
whose SSID is not printable text (a hidden network) is shown as the literal text `<hidden>`
(`WIFI_SCAN_HIDDEN_SSID_TEXT`) instead. The `wifi_scan_ap_t` struct holds only `ssid`, `rssi` (an `int16_t` in
dBm) and `security` (a string already converted from the `cy_wcm_security_t` enum) — it has no `bssid` field, as
the upstream README mentions — and holds at most `WIFI_SCAN_MAX_APS = 12` networks per scan.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the real thread-safety mechanism differs from what the upstream
README describes.

[`wifi_list/wifi_scan_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/wifi_scan_service.c) — the WHD callback only writes data and flags inside a critical section, never touching LVGL:

```c
if(status == CY_WCM_SCAN_COMPLETE) {
    taskENTER_CRITICAL();
    wifi_scan_sort_by_rssi_desc(service);
    service->scan_done_pending = true;
    taskEXIT_CRITICAL();
}
```

`wifi_scan_service_process()`, called by the poll timer every 150 ms — reads and clears the flag atomically:

```c
bool wifi_scan_service_process(wifi_scan_service_t *service)
{
    bool done;
    bool error;

    taskENTER_CRITICAL();
    done = service->scan_done_pending;
    error = service->scan_error_pending;
    service->scan_done_pending = false;
    service->scan_error_pending = false;
    taskEXIT_CRITICAL();

    if(done) {
        service->scanning = false;
        service->scan_sequence++;
        return true;
    }
    /* ... error handling ... */
    return false;
}
```

[`wifi_list/ui_wifi_list_page.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/ui_wifi_list_page.c) — the LVGL-side poll timer that calls `process()` and re-renders:

```c
static void ui_wifi_poll_timer_cb(lv_timer_t *timer)
{
    uint16_t count = 0U;
    LV_UNUSED(timer);

    if(wifi_scan_service_process(&s_ctx.service)) {
        lv_obj_clear_state(s_ctx.scan_btn, LV_STATE_DISABLED);
        (void)wifi_scan_service_get_list(&s_ctx.service, &count);
        ui_wifi_update_status_labels();
        ui_wifi_render_ap_list();
    }
}
/* ... */
s_ctx.poll_timer = lv_timer_create(ui_wifi_poll_timer_cb, UI_WIFI_POLL_MS, NULL);
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/main_example.c) calls `wifi_scan_service_preinit()` then forwards into the UI, exactly as the upstream README describes
- [`wifi_list/wifi_scan_types.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/wifi_scan_types.h) — the real `wifi_scan_ap_t` struct (no `bssid`)
- See the full folder at [`hmi_ep05_wifi_list/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) — EP04's shell (`nav/`) is reused, with the Home page replaced by the WiFi List page

## Common mistakes

- **Assuming this episode uses `lv_async_call()`** — the upstream README says so, but the real code uses a
  critical section plus an `lv_timer` polling every 150 ms. Trust the real code when explaining the
  thread-safety mechanism.
- **Calling LVGL widget APIs directly from the `cy_wcm`/`whd` callback** — the callback runs on the WCM's internal
  task, not the LVGL task. Calling `lv_label_set_text()` right there would race with `lv_timer_handler()`, which
  may be drawing at the same time. It must go through a critical section plus polling (or `lv_async_call()`).
- **Forgetting to guard against overlapping scans** — without checking `service->scanning` before
  `cy_wcm_start_scan()`, mashing the Scan button repeatedly would fire multiple overlapping scans.
- **Mixing up the struct's field names** — the upstream README mentions `bssid`, but the real `wifi_scan_ap_t`
  only has `ssid`, `rssi` and `security`.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list) and flash the ready-made firmware.

## See it work first

![Screen of EP05 — WiFi List on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/hmi_ep05_wifi_list.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Which is better, an RSSI of -45 dBm or -85 dBm?
- Why should you not scan for Wi-Fi directly inside a button's callback?
- What does the security type in the list tell the user?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
