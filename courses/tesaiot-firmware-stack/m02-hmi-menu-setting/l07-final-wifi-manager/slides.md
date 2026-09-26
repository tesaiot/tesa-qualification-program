---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.7 — Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 2.7 — Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ

## รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile ที่เก็บไว้

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้
2. ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ
3. ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l06`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP07 — Final WiFi Manager บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/hmi_ep07_final_wifi_manager.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — service ถือ state, UI แค่ observe

`wifi_connection_service` รันเป็น background task ถือ state machine + ข้อมูลทั้งหมดไว้เอง

หน้า UI **ไม่เก็บ state เอง** — แค่ `lv_timer` เรียก `get_snapshot()` เป็นระยะมาคัดลอกแสดง

เหตุผล: หน้า UI ถูก `lv_menu_set_page()` สลับออกได้ (บทเรียน 2.4) แต่ service อยู่ยงไม่ว่า UI จะสลับไปไหน

`get_snapshot()` ล็อก semaphore ก่อน `memcpy` — ปลอดภัยเพราะ background task ก็ lock ตัวเดียวกันก่อนแก้ state

---

# แนวคิด — retry ladder ตัวจริง 1-2-5-10s

README ต้นทางบอก 1s → 5s → 15s → 60s

**โค้ดจริง**: `{ 1000, 2000, 5000, 10000 }` ms — คอมเมนต์ในซอร์สยืนยันตรง ๆ

`retry_stage` เป็น index เข้าตาราง ถ้าเกินขนาดจะ clamp ไว้ที่ตัวสุดท้าย (เพดาน 10s ไม่ใช่ 60s)

---

# แนวคิด — ping watchdog ไม่ได้สั่งต่อใหม่

`cy_wcm_ping()` ไปที่ **gateway** (จาก DHCP) ทุก 20 วินาที — ไม่ใช่ IP สาธารณะตายตัว

ping fail ครบ 3 ครั้ง → แค่ตั้ง `internet_ok = false` ให้ UI แสดง **ไม่แตะ state machine เลย**

สิ่งที่สั่ง `RECONNECT_WAIT` จริงคือ WCM disconnect event หรือ `cy_wcm_is_connected_to_ap() == 0`

ping watchdog = เกจวัดให้ผู้ใช้ดู ไม่ใช่ตัวขับ retry

---

# แนวคิด — command queue เดียว + auto-connect ตอน boot

ปุ่ม Connect/Disconnect/Retry ไม่แก้ state ตรง ๆ — ส่งคำสั่งเข้าคิวที่ background task เดียวประมวลผลทีละคำสั่ง

กันสองคำสั่งชนกัน เช่นกด Disconnect พร้อมกับ retry ladder กำลังจะ connect เอง

`wifi_connection_service_init()` โหลด profile จาก NVM (บทเรียน 2.6) ถ้า valid → connect ทันทีโดยไม่ต้องกดอะไร

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `prog.state-machines` (ระดับ 3)
- `proto.wifi` (ระดับ 3)
- `proto.tcp-ip` (ระดับ 1)
- `rtos.basics` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — retry ladder ตัวจริง

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`wifi_connection_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/wifi_conn/wifi_connection_service.c)

```c
static const uint32_t s_reconnect_backoff_ms[] =
    { 1000U, 2000U, 5000U, 10000U };

/* Reconnect backoff: 1s -> 2s -> 5s -> 10s (cap at max stage). */
static bool wifi_conn_schedule_retry_locked(void)
{
    uint8_t idx = s_ctx.retry_stage;
    if(idx >= 4U) { idx = 3U; }

    s_ctx.retry_wait_ms = s_reconnect_backoff_ms[idx];
    if(s_ctx.retry_stage < 3U) { s_ctx.retry_stage++; }

    wifi_conn_set_state_locked(WIFI_CONN_STATE_RECONNECT_WAIT);
    return true;
}
```

---

# ตัวอย่างสมบูรณ์ — ping ไม่แตะ state machine

```c
if(0 == wifi_conn_ping_ok) {
    if(s_ctx.ping_fail_streak < 0xFFU) {
        s_ctx.ping_fail_streak++;
    }

    if(s_ctx.ping_fail_streak >= WIFI_CONN_PING_FAIL_THRESHOLD) {
        s_ctx.internet_ok = false;   /* display only —
                                       * no state transition here */
    }
}
```

snapshot getter ล็อกก่อน copy:

```c
if(pdTRUE != xSemaphoreTake(s_ctx.lock, portMAX_DELAY)) {
    return false;
}
out_snapshot->state = s_ctx.state;
/* ... copy every field ... */
(void)xSemaphoreGive(s_ctx.lock);
```

---

# จุดที่มักพลาด

- จำ retry ladder ผิดเป็น 1s/5s/15s/60s — ค่าจริงคือ 1s/2s/5s/10s
- คิดว่า ping fail สั่ง retry ทันที — จริง ๆ แค่ตั้งธงแสดงผล ไม่แตะ state
- ให้ UI แก้ state ของ service ตรง ๆ — ต้องผ่าน command queue เท่านั้น
- อ่าน state โดยไม่ล็อก semaphore — ต้องผ่าน `get_snapshot()` เท่านั้น

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

- หลักฐานที่ประเมิน (`prog.state-machines` ระดับ 2): วิดีโอหรือ log ที่บอร์ดต่อ Wi-Fi อัตโนมัติหลังรีเซ็ต และกลับมาเองหลังปิด AP

---

# เช็กความเข้าใจ

- ทำไม "ต่อ AP ได้" ยังไม่พอจะบอกว่าอินเทอร์เน็ตใช้ได้
- state ใดบ้างที่จำเป็นใน state machine ของการเชื่อมต่อ
- ถ้าลองใหม่ถี่เกินไปจะเกิดปัญหาอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (hmi_ep07_final_wifi_manager) ที่ commit `9a8e3ed`
