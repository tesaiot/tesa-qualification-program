---
id: fw-stack.m02.l05
lang: th
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
---

# สแกน Wi-Fi และแสดงรายการเครือข่าย

## เป้าหมาย

1. สแกน Wi-Fi ผ่าน WHD/cy_wcm แล้วแสดงรายการพร้อม RSSI และชนิด security
2. แยก scan service ออกจากหน้า UI และส่งผลสแกนเข้าหน้าอย่างปลอดภัย
3. อ่านค่า RSSI และบอกได้ว่าเครือข่ายใดสัญญาณดีพอจะเชื่อมต่อ

## แนวคิด

### สแกน Wi-Fi ต้องผ่าน stack สามชั้น

การสแกนบน PSoC Edge ไล่ผ่าน `whd` (WiFi Host Driver คุย SDIO กับโมดูลวิทยุ) → `cy_wcm` (Connection Manager ห่อ
`whd` เป็น API scan/connect ระดับสูง) → callback ของแอปที่ `cy_wcm` เรียกทุกครั้งที่เจอ AP ใหม่ episode นี้ห่อทั้ง
สามชั้นไว้ใน **service layer** (`wifi_scan_service.c`) เพื่อให้หน้า UI (`ui_wifi_list_page.c`) เรียกแค่
`wifi_scan_service_start()` / `wifi_scan_service_process()` โดยไม่ต้องรู้จัก `cy_wcm` เลย

### pre-init: warm up radio ตั้งแต่ boot ไม่ใช่ตอนกดปุ่ม

`example_main()` เรียก `wifi_scan_service_preinit()` ก่อนสร้าง UI เสียอีก ฟังก์ชันนี้ทำ SDIO bring-up (ตั้ง
interrupt handler ของ SDIO และ host-wake, ลงทะเบียน deep-sleep callback ของ SDHC controller) และ `cy_wcm_init()`
ให้เสร็จตั้งแต่ boot ถ้าไปเรียกตอนกดปุ่ม "Scan" ครั้งแรกโดยตรง ผู้ใช้จะเห็น UI ค้าง 1-3 วินาทีระหว่างที่ radio
กำลัง bring-up — pre-init pattern นี้ทำให้การกดปุ่มครั้งแรกเร็วเท่ากับครั้งถัดไป ถ้า pre-init ล้มเหลว โค้ดแค่ log
แล้วปล่อยให้ UI เปิดต่อได้ (แค่ปุ่ม Scan จะ fail เมื่อลอง)

### callback จาก WHD ไม่แตะ LVGL เลยแม้แต่บรรทัดเดียว — ต่างจากที่ README ต้นทางอธิบาย

README ของ episode บน Developer Hub อธิบายว่าใช้ `lv_async_call()` ส่งงานจาก callback ของ WHD กลับเข้า LVGL thread
แต่โค้ดจริงที่ commit `9a8e3ed` ใช้อีก pattern หนึ่งคือ **critical section + poll timer**: `wifi_scan_callback()`
(เรียกจาก WCM internal task ไม่ใช่ LVGL task) แค่คัดลอกผล AP แต่ละตัวเข้า array ภายใน `taskENTER_CRITICAL()` /
`taskEXIT_CRITICAL()` ของ FreeRTOS แล้วตั้งธง `scan_done_pending`/`scan_error_pending` เท่านั้น ไม่เรียก widget API
ของ LVGL แม้แต่ตัวเดียว — วิธีนี้ก็ปลอดภัยจาก race เหมือนกับ `lv_async_call()` เพียงแค่เป็นคนละกลไก

### ฝั่ง LVGL ใช้ `lv_timer` มา "poll" ธงแทนที่จะรอถูกปลุก

`ui_wifi_list_page_create()` สร้าง `lv_timer_create(ui_wifi_poll_timer_cb, UI_WIFI_POLL_MS, NULL)` ที่ `UI_WIFI_POLL_MS
= 150` — ทุก 150 มิลลิวินาที `ui_wifi_poll_timer_cb()` ซึ่งรันอยู่บน LVGL thread อยู่แล้ว (ปลอดภัยที่จะเรียก
widget API) จะเรียก `wifi_scan_service_process()` ซึ่งอ่านและเคลียร์ธง `scan_done_pending`/`scan_error_pending`
ภายใน critical section เดียวกัน ถ้าธงบอกว่าสแกนเสร็จ ก็ค่อยอ่าน list ผลลัพธ์แล้ว render ใหม่ — สรุปคือ **ข้อมูล
ข้าม thread ด้วย critical section, การแจ้งเตือนข้าม thread ด้วยการ poll เป็นจังหวะ** แทนที่จะ push เข้า LVGL
ทันทีแบบ `lv_async_call()` ทั้งสองวิธีถูกต้องและปลอดภัยเท่ากัน แต่เป็นคนละกลไก — บทเรียนนี้อธิบายตามโค้ดจริง

### กันสแกนซ้อนสแกนที่ตัว service ไม่ใช่แค่ที่ปุ่ม

`wifi_scan_service_start()` เช็ค `service->scanning` เป็นด่านแรกและคืน `false` ทันทีถ้ากำลังสแกนอยู่ ฝั่ง UI เอง
ก็ใส่ `LV_STATE_DISABLED` ให้ปุ่ม Scan ระหว่างรอผลเช่นกัน — การกันซ้อนสองชั้นนี้ (service ชั้นใน + ปุ่ม UI ชั้นนอก)
ทำให้ระบบยังปลอดภัยแม้ฝั่ง UI จะลืม disable ปุ่มเอง

### RSSI, SSID ที่มองไม่เห็น และการเรียงผล

ผลสแกนถูกเรียงจากสัญญาณแรงไปอ่อน (`wifi_scan_sort_by_rssi_desc`) ก่อนแสดง AP ที่ SSID ไม่ใช่ตัวอักษรที่พิมพ์ได้
(hidden network) จะถูกแสดงเป็นข้อความ `<hidden>` แทน (`WIFI_SCAN_HIDDEN_SSID_TEXT`) โครง struct
`wifi_scan_ap_t` เก็บแค่ `ssid`, `rssi` (int16_t หน่วย dBm) และ `security` (string ที่แปลงจาก enum
`cy_wcm_security_t` แล้ว) ไม่มีฟิลด์ bssid ตามที่ README ต้นทางกล่าวถึง และรับได้สูงสุด `WIFI_SCAN_MAX_APS = 12`
เครือข่ายต่อการสแกนหนึ่งครั้ง

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะกลไก thread-safety ในโค้ดจริงต่างจากที่ README ต้นทางอธิบาย

[`wifi_list/wifi_scan_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/wifi_scan_service.c) — callback ของ WHD เขียนแค่ข้อมูล+ธงภายใน critical section ไม่แตะ LVGL:

```c
if(status == CY_WCM_SCAN_COMPLETE) {
    taskENTER_CRITICAL();
    wifi_scan_sort_by_rssi_desc(service);
    service->scan_done_pending = true;
    taskEXIT_CRITICAL();
}
```

`wifi_scan_service_process()` ที่ poll timer เรียกทุก 150 ms — อ่านและเคลียร์ธงในจังหวะเดียว:

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

[`wifi_list/ui_wifi_list_page.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/ui_wifi_list_page.c) — poll timer ฝั่ง LVGL ที่เรียก `process()` แล้ว render ใหม่:

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

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/main_example.c) เรียก `wifi_scan_service_preinit()` แล้ว forward เข้า UI ตรงตามที่ README ต้นทางอธิบาย
- [`wifi_list/wifi_scan_types.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/wifi_list/wifi_scan_types.h) — struct `wifi_scan_ap_t` จริง (ไม่มี bssid)
- ดูโฟลเดอร์เต็มที่ [`hmi_ep05_wifi_list/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) — shell จาก EP04 (`nav/`) ถูกใช้ซ้ำโดยแทน Home ด้วยหน้า WiFi List

## จุดที่มักพลาด

- **คิดว่า episode นี้ใช้ `lv_async_call()`** — README ต้นทางบอกอย่างนั้น แต่โค้ดจริงใช้ critical section + lv_timer
  poll ทุก 150 ms ให้ยึดโค้ดจริงเมื่ออธิบายกลไก thread-safety
- **เรียก LVGL widget API จาก callback ของ `cy_wcm`/`whd` โดยตรง** — callback รันบน WCM internal task ไม่ใช่ LVGL
  task การเรียก `lv_label_set_text()` ตรงนั้นจะชนกับ `lv_timer_handler()` ที่กำลังวาดอยู่ ต้องผ่าน critical
  section + poll (หรือ `lv_async_call()`) เท่านั้น
- **ลืมกันสแกนซ้อน** — ถ้าไม่เช็ค `service->scanning` ก่อน `cy_wcm_start_scan()` การกดปุ่ม Scan รัว ๆ จะยิง scan
  ซ้อนหลายครั้ง
- **สับสนชื่อฟิลด์ struct** — README ต้นทางพูดถึง `bssid` แต่ `wifi_scan_ap_t` จริงมีแค่ `ssid`, `rssi`, `security`

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP05 — WiFi List บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/hmi_ep05_wifi_list.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- RSSI -45 dBm กับ -85 dBm อันไหนดีกว่า
- ทำไมไม่ควรสแกน Wi-Fi ใน callback ของปุ่มโดยตรง
- ชนิด security ในรายการบอกอะไรกับผู้ใช้

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep05_wifi_list) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep05_wifi_list&q=hmi_ep05_wifi_list)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
