---
id: fw-stack.m02.l07
lang: th
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
---

# Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ

## เป้าหมาย

1. รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้
2. ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ
3. ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่

## แนวคิด

### service ถือ state ทั้งหมด UI เป็นแค่ observer ที่ copy snapshot ออกมาดู

หัวใจของ ep07 คือ `wifi_connection_service` ที่รันเป็น background task ของตัวเอง ถือ state machine
(`wifi_conn_state_t`: `IDLE`, `CONNECTING`, `CONNECTED`, `DISCONNECTING`, `RECONNECT_WAIT`, `ERROR`) และข้อมูล
ทั้งหมด (SSID, RSSI, IP, retry stage ฯลฯ) ไว้ในตัวเอง หน้า UI (`ui_wifi_status_page.c`) **ไม่เก็บ state ของ
connection เอง** — มันแค่สร้าง `lv_timer` ที่เรียก `wifi_connection_service_get_snapshot()` เป็นระยะเพื่อคัดลอกค่า
ออกมาแสดง เหตุผลที่ต้องออกแบบแบบนี้: หน้า UI อาจถูก `lv_menu_set_page()` สลับออกจากจอ (ดูบทเรียน 2.4) ถ้า state
อยู่ใน UI widget เอง ข้อมูลจะหายเมื่อสลับหน้า แต่ service อยู่ยงคงกระพันไม่ว่า UI จะสลับไปไหน

`wifi_connection_service_get_snapshot()` ใช้ FreeRTOS semaphore (`xSemaphoreTake`/`xSemaphoreGive`) ล็อกก่อน
`memcpy` ค่าจาก state ภายในออกมาใส่ struct `wifi_connection_snapshot_t` ที่ผู้เรียกส่งมา แล้วปลดล็อก — ปลอดภัยจาก
race เพราะ background task ก็ต้อง lock semaphore ตัวเดียวกันนี้ทุกครั้งก่อนแก้ state

### retry ladder ตัวจริงคือ 1s → 2s → 5s → 10s ไม่ใช่ 1s → 5s → 15s → 60s ตามที่ README ต้นทางบอก

โค้ดจริงประกาศ `static const uint32_t s_reconnect_backoff_ms[] = { 1000U, 2000U, 5000U, 10000U };` พร้อมคอมเมนต์
กำกับตรง ๆ ว่า "Reconnect backoff: 1s -> 2s -> 5s -> 10s (cap at max stage)" — `wifi_conn_schedule_retry_locked()`
ใช้ `retry_stage` เป็น index เข้าตาราง ถ้า index เกินขนาด array จะ clamp ไว้ที่ตัวสุดท้าย (10s) ไม่ปล่อยให้โตไม่
สิ้นสุด นี่คือ exponential-ish backoff ที่มี **เพดาน** ชัดเจน ป้องกันการยิง `cy_wcm_connect_ap()` รัวเกินไปเมื่อ AP
หายไปนาน แต่ก็ไม่รอนานเกินไปเมื่อ AP กลับมาเร็ว

### ping watchdog เช็ค gateway อยู่แล้ว และ**ไม่ได้สั่งให้ต่อใหม่**

`wifi_conn_probe_internet_once()` เรียก `cy_wcm_ping()` ไปที่ **gateway address** (ที่ได้จาก DHCP ตอนต่อ AP)
ทุก `WIFI_CONN_PING_INTERVAL_MS = 20000` (20 วินาที) โดย default อยู่แล้ว ไม่ใช่ IP สาธารณะตายตัวอย่าง 8.8.8.8
ตามที่ README ต้นทางแนะนำให้ "ลองเปลี่ยน" ที่สำคัญกว่านั้นคือ**ผลของ ping ไม่ได้ทำให้ state machine เปลี่ยน**
เลย — ถ้า ping fail ครบ `WIFI_CONN_PING_FAIL_THRESHOLD = 3` ครั้งติดกัน โค้ดแค่ตั้ง `internet_ok = false` ให้ UI
แสดงผล ("ping fail 3") เท่านั้น ไม่เรียก `wifi_conn_schedule_retry_locked()` หรือเปลี่ยน `state` แต่อย่างใด สิ่งที่
ทำให้ state เปลี่ยนไป `RECONNECT_WAIT` จริง ๆ คือเหตุการณ์ตัดการเชื่อมต่อจาก WCM เอง
(`wifi_conn_handle_disconnect_event`) หรือตรวจพบว่า `cy_wcm_is_connected_to_ap() == 0` ตอน refresh ข้อมูล — พูด
อีกแบบคือ ping watchdog เป็นแค่ **เกจวัด** อินเทอร์เน็ตให้ผู้ใช้ดู ไม่ใช่ตัวขับ retry

### คำสั่งจากผู้ใช้ทั้งหมดถูก serialize ผ่าน command queue เดียว

ปุ่ม Connect/Disconnect/Retry now ในหน้า UI ไม่ได้เรียกแก้ state ตรง ๆ แต่เรียก
`wifi_connection_service_connect_profile()` / `_disconnect()` / `_retry_now()` ซึ่งแต่ละตัวส่งคำสั่งเข้าคิวที่
background task เดียว (`wifi_conn_task`) เป็นผู้ประมวลผลทีละคำสั่ง (`wifi_conn_process_cmd`) การ serialize แบบนี้
กันไม่ให้เกิดสองคำสั่งชนกัน (เช่น user กด Disconnect พร้อมกับที่ retry ladder กำลังจะเรียก connect เอง)

### `wifi_connection_service_init()` ทำ auto-connect ตั้งแต่ boot ถ้ามี profile

`main_example.c` เรียก `wifi_connection_service_init()` ก่อนสร้าง UI ภายในจะ `cy_wcm_init()`, โหลด profile จาก
NVM (บทเรียน 2.6) ผ่าน `wifi_profile_store_load()`, ถ้าโหลดสำเร็จและ valid จะตั้ง `have_profile = true` แล้วส่ง
คำสั่ง connect เข้าคิวทันที —ผู้ใช้ไม่ต้องกดอะไรเลยถ้าเคย save profile ไว้ก่อนหน้า

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะค่า retry ladder และพฤติกรรมของ ping ต่างจากที่ README ต้นทางอธิบาย

[`wifi_conn/wifi_connection_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/wifi_conn/wifi_connection_service.c) — retry ladder ตัวจริงพร้อมเพดาน:

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

ping watchdog เปลี่ยนแค่ `internet_ok` ไม่แตะ state machine:

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

snapshot getter ล็อกด้วย semaphore ก่อน copy ออก:

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

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/main_example.c) เรียก `wifi_connection_service_init()` แล้ว forward เข้า UI ตรงตามที่ README ต้นทางอธิบาย
- [`wifi_conn/wifi_connection_service.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/wifi_conn/wifi_connection_service.h) — enum `wifi_conn_state_t` ตัวจริง (ตรงกับที่ README ต้นทางระบุ)
- ดูโฟลเดอร์เต็มที่ [`hmi_ep07_final_wifi_manager/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager)

## จุดที่มักพลาด

- **จำค่า retry ladder ผิดเป็น 1s/5s/15s/60s** — ค่าจริงในโค้ดคือ 1s/2s/5s/10s ตามคอมเมนต์ในซอร์สตรง ๆ
- **คิดว่า ping fail จะสั่งให้ retry ใหม่ทันที** — ในโค้ดชุดนี้ ping แค่ตั้งธง `internet_ok` ให้ UI แสดงผล ไม่ได้
  เปลี่ยน state หรือสั่ง reconnect เลย การ reconnect มาจาก WCM disconnect event หรือ `cy_wcm_is_connected_to_ap()`
  เท่านั้น
- **ให้ UI แก้ state ของ connection ตรง ๆ** — ปุ่มทุกปุ่มต้องเรียกผ่าน service API ที่ส่งเข้า command queue ไม่ใช่
  ไปแก้ struct ของ service เอง เพราะ background task เป็นเจ้าของ state ที่แท้จริง
- **อ่าน field ของ service state โดยไม่ล็อก semaphore** — ต้องผ่าน `wifi_connection_service_get_snapshot()`
  เท่านั้น การอ่านตรงจะชนกับ background task ที่กำลังแก้ค่าเดียวกันอยู่

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP07 — Final WiFi Manager บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/hmi_ep07_final_wifi_manager.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม "ต่อ AP ได้" ยังไม่พอจะบอกว่าอินเทอร์เน็ตใช้ได้
- state ใดบ้างที่จำเป็นใน state machine ของการเชื่อมต่อ
- ถ้าลองใหม่ถี่เกินไปจะเกิดปัญหาอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
