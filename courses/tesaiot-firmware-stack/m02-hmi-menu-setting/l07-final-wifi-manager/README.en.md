---
id: fw-stack.m02.l07
lang: en
title:
  th: "Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
summary:
  th: "รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile ที่เก็บไว้"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l06]
objectives:
  - th: "รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้"
    en: "Combine scan, profile and connect into a Wi-Fi manager that auto-connects from the stored profile"
  - th: "ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ"
    en: "Design a connection state machine (connect, drop, retry) and show its state on screen"
  - th: "ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่"
    en: "Ping the gateway to check that the network really answers, and explain that in this example the ping result does not trigger a reconnect"
develops:
  - {skill: prog.state-machines, to: 3}
  - {skill: proto.wifi, to: 3}
  - {skill: proto.tcp-ip, to: 1}
  - {skill: rtos.basics, to: 2}
assesses:
  - {skill: prog.state-machines, level: 2, evidence: "วิดีโอหรือ log ที่บอร์ดต่อ Wi-Fi อัตโนมัติหลังรีเซ็ต และกลับมาเองหลังปิด AP"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep07_final_wifi_manager"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 82e708ef1d3af6b5525f0c31032add21a3df7a3d88cd26c5a5017a804cf6fef2
---

# Complete Wi-Fi manager: connect, retry and auto-connect

## Objectives

1. Combine scan, profile and connect into a Wi-Fi manager that auto-connects from the stored profile
2. Design a connection state machine (connect, drop, retry) and show its state on screen
3. Ping the gateway to check that the network really answers, and explain that in this example the ping result does not trigger a reconnect

## Concepts

### The service owns all the state; the UI is just an observer copying a snapshot

The heart of EP07 is `wifi_connection_service`, which runs as its own background task, owns the state machine
(`wifi_conn_state_t`: `IDLE`, `CONNECTING`, `CONNECTED`, `DISCONNECTING`, `RECONNECT_WAIT`, `ERROR`), and holds all
the data (SSID, RSSI, IP, retry stage, and so on) itself. The UI page (`ui_wifi_status_page.c`) **does not keep
any connection state of its own** — it only creates an `lv_timer` that periodically calls
`wifi_connection_service_get_snapshot()` to copy values out for display. The reason for this design: the UI page
can be switched away by `lv_menu_set_page()` (see lesson 2.4). If the state lived in a UI widget, it would vanish
whenever the page switched, but the service survives no matter where the UI goes.

`wifi_connection_service_get_snapshot()` locks a FreeRTOS semaphore (`xSemaphoreTake`/`xSemaphoreGive`) before
`memcpy`-ing the internal state into the caller's `wifi_connection_snapshot_t` struct, then unlocks. This is safe
from races because the background task also locks that same semaphore every time before it changes the state.

### The real retry ladder is 1s → 2s → 5s → 10s, not 1s → 5s → 15s → 60s as the upstream README says

The real code declares `static const uint32_t s_reconnect_backoff_ms[] = { 1000U, 2000U, 5000U, 10000U };`, with a
comment stating it directly: "Reconnect backoff: 1s -> 2s -> 5s -> 10s (cap at max stage)."
`wifi_conn_schedule_retry_locked()` uses `retry_stage` as an index into this table; if the index would run past
the end of the array, it clamps to the last entry (10s) instead of growing without bound. This is a bounded,
exponential-ish backoff: it stops the code from hammering `cy_wcm_connect_ap()` when an AP has been gone a long
time, but it also does not wait too long when the AP comes back quickly.

### The ping watchdog already checks the gateway, and it does not trigger a reconnect

`wifi_conn_probe_internet_once()` calls `cy_wcm_ping()` against the **gateway address** (obtained from DHCP when
the AP connection was made) every `WIFI_CONN_PING_INTERVAL_MS = 20000` (20 seconds) by default — not a fixed
public IP such as 8.8.8.8, which is what the upstream README suggests trying as a change. More importantly,
**the ping result never changes the state machine at all**. If ping fails
`WIFI_CONN_PING_FAIL_THRESHOLD = 3` times in a row, the code only sets `internet_ok = false` for the UI to
display ("ping fail 3") — it never calls `wifi_conn_schedule_retry_locked()` or touches `state`. What actually
moves the state to `RECONNECT_WAIT` is a real disconnect event from WCM (`wifi_conn_handle_disconnect_event`) or
discovering `cy_wcm_is_connected_to_ap() == 0` while refreshing connection info. In other words, the ping watchdog
is only a **gauge** shown to the user, not the thing driving reconnection.

### Every user command is serialized through one command queue

The Connect/Disconnect/Retry now buttons in the UI never mutate the state directly. They call
`wifi_connection_service_connect_profile()` / `_disconnect()` / `_retry_now()`, each of which pushes a command
into a queue that the single background task (`wifi_conn_task`) processes one at a time
(`wifi_conn_process_cmd`). This serialization prevents two commands from colliding — for example, the user
pressing Disconnect at the exact moment the retry ladder is about to call connect on its own.

### `wifi_connection_service_init()` auto-connects at boot if a profile exists

`main_example.c` calls `wifi_connection_service_init()` before building the UI. Inside, it calls `cy_wcm_init()`,
loads the profile from NVM (lesson 2.6) through `wifi_profile_store_load()`, and if that succeeds and is valid,
sets `have_profile = true` and immediately queues a connect command — the user does not need to tap anything if a
profile was saved earlier.

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the retry ladder values and the ping behavior differ from what the
upstream README describes.

[`wifi_conn/wifi_connection_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/wifi_conn/wifi_connection_service.c) — the real retry ladder with its cap:

```c
static const uint32_t s_reconnect_backoff_ms[] = { 1000U, 2000U, 5000U, 10000U };

/* Reconnect backoff: 1s -> 2s -> 5s -> 10s (cap at max stage). */
static bool wifi_conn_schedule_retry_locked(void)
{
    uint8_t idx = s_ctx.retry_stage;
    if(idx >= (uint8_t)(sizeof(s_reconnect_backoff_ms) / sizeof(s_reconnect_backoff_ms[0]))) {
        idx = (uint8_t)(sizeof(s_reconnect_backoff_ms) / sizeof(s_reconnect_backoff_ms[0])) - 1U;
    }

    s_ctx.retry_wait_ms = s_reconnect_backoff_ms[idx];
    if(s_ctx.retry_stage < ((uint8_t)(sizeof(s_reconnect_backoff_ms) / sizeof(s_reconnect_backoff_ms[0])) - 1U)) {
        s_ctx.retry_stage++;
    }

    wifi_conn_set_state_locked(WIFI_CONN_STATE_RECONNECT_WAIT);
    return true;
}
```

The ping watchdog only changes `internet_ok`, never the state machine:

```c
if(0 == wifi_conn_ping_ok) {
    if(s_ctx.ping_fail_streak < 0xFFU) {
        s_ctx.ping_fail_streak++;
    }

    if(s_ctx.ping_fail_streak >= WIFI_CONN_PING_FAIL_THRESHOLD) {
        s_ctx.internet_ok = false;   /* display only — no state transition here */
    }
}
```

The snapshot getter locks a semaphore before copying out:

```c
bool wifi_connection_service_get_snapshot(wifi_connection_snapshot_t *out_snapshot)
{
    if((out_snapshot == NULL) || (!s_ctx.initialized) || (s_ctx.lock == NULL)) {
        return false;
    }

    if(pdTRUE != xSemaphoreTake(s_ctx.lock, portMAX_DELAY)) {
        return false;
    }

    (void)memset(out_snapshot, 0, sizeof(*out_snapshot));
    out_snapshot->state = s_ctx.state;
    /* ... copy every field ... */

    (void)xSemaphoreGive(s_ctx.lock);
    return true;
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/main_example.c) calls `wifi_connection_service_init()` then forwards into the UI, exactly as the upstream README describes
- [`wifi_conn/wifi_connection_service.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/wifi_conn/wifi_connection_service.h) — the real `wifi_conn_state_t` enum (matches what the upstream README states)
- See the full folder at [`hmi_ep07_final_wifi_manager/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager)

## Common mistakes

- **Misremembering the retry ladder as 1s/5s/15s/60s** — the real values in the code are 1s/2s/5s/10s, straight
  from the source's own comment.
- **Assuming a ping failure triggers an immediate retry** — in this code, ping only sets the `internet_ok` flag
  for the UI to display; it never changes the state or triggers a reconnect. Reconnection comes only from a WCM
  disconnect event or `cy_wcm_is_connected_to_ap()`.
- **Letting the UI mutate the connection state directly** — every button must go through the service API, which
  pushes a command into the queue, rather than editing the service's struct directly, because the background task
  is the true owner of that state.
- **Reading a service state field without locking the semaphore** — you must go through
  `wifi_connection_service_get_snapshot()` only; reading directly would race with the background task changing
  the same value.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) and flash the ready-made firmware.

## See it work first

![Screen of EP07 — Final WiFi Manager on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/hmi_ep07_final_wifi_manager.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why is "connected to the AP" not enough on its own to say the internet works?
- Which states does the connection state machine need?
- What goes wrong if retries happen too often?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
