---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.7 — SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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

# บทเรียน 3.7 — SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)

## โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว
2. จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก
3. นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m03.l06`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP07 — SensorHub Final บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/int_ep07_sensorhub_final.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — `lv_timer` เดียว ไม่ใช่สี่ task

README ต้นทาง: "4 reader task + single queue + `lv_async_call`"

**โค้ดจริง**: ไม่มี `xTaskCreate`/`xQueueCreate`/`lv_async_call` เลยสักตัว — `lv_timer` เดียวที่ 100 ms เป็น cooperative scheduler เอง ทุกอย่างรันบน LVGL thread เดียว

---

# แนวคิด — "next due time" ต่อเซนเซอร์

แต่ละเซนเซอร์มี `next_..._ms` ของตัวเอง เช็ค `(now_ms - next_xxx_ms) < 0` ทุก tick 100 ms

คาบจริง = ค่าเดิมจากบทเรียนของมันเอง **ไม่ใช่ 200/500/20/50 ms** ตาม README ต้นทาง

`DPS368=1000` · `SHT4x=1000` · `BMI270=200` · `BMM350=120` ms

---

# แนวคิด — tick 100 ms ปัดคาบที่ไม่ใช่ผลคูณของ 100

BMM350 คาบ 120 ms แต่ timer หลัก 100 ms → อ่านจริงทุก 200 ms (ปัดขึ้นเป็นผลคูณของ 100)

ผลคือ **auto-calibration 140 ตัวอย่างใช้เวลา ~28 วินาที ไม่ใช่ 16.8 วินาที** เหมือนตอนรันเดี่ยวใน EP04

calibration เริ่มอัตโนมัติตั้งแต่ boot ต่างจากบทเรียน 3.4 ที่ต้องกดปุ่ม

---

# แนวคิด — จอจริงเป็นแท็บ 5 หน้า ไม่ใช่ grid 2×2

README ต้นทาง: grid 2×2 + บาร์ mic ด้านล่าง แสดงพร้อมกันทั้งหมด

**โค้ดจริง**: `sensorhub_page_t` 5 ค่า (Home/Env/Motion/Compass/Audio) — แสดงทีละหน้าแบบแท็บ เหมือนโครง nav shell จากโมดูล 2

หน้า Audio แสดงระดับเสียงที่คำนวณแล้ว ไม่ใช่คลื่นดิบ · บั๊ก BMM350 (บทเรียน 3.4) ยังต้อง patch เหมือนเดิม

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `gui.hmi` (ระดับ 3)
- `sys.sensors-actuators` (ระดับ 3)
- `rtos.basics` (ระดับ 2)
- `soft.problem-solving` (ระดับ 2)
- `soft.communication` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — `lv_timer` เดียวเรียก poll ทุกตัว

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`sensorhub_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_ui/sensorhub/sensorhub_presenter.c)

```c
static void sensorhub_poll_timer_cb(lv_timer_t *timer)
{
    uint32_t now_ms = lv_tick_get();

    sensorhub_poll_dps(now_ms);
    sensorhub_poll_sht(now_ms);
    sensorhub_poll_bmi(now_ms);
    sensorhub_poll_bmm(now_ms);
    sensorhub_poll_bmm_calibration();
    sensorhub_poll_mic();
}
/* ... */
s_ctx.poll_timer = lv_timer_create(sensorhub_poll_timer_cb,
                                   HUB_UI_POLL_MS, NULL);
```

---

# ตัวอย่างสมบูรณ์ — รูปแบบ "next due" ต่อเซนเซอร์

```c
/* Poll DPS368 on its own sampling period. */
static void sensorhub_poll_dps(uint32_t now_ms)
{
    if ((!s_ctx.dps_ready) ||
        ((int32_t)(now_ms - s_ctx.next_dps_ms) < 0)) {
        return;
    }

    s_ctx.next_dps_ms = now_ms + DPS368_SAMPLE_PERIOD_MS;

    dps368_sample_t sample;
    if (dps368_reader_poll(&sample)) {
        s_ctx.dps_sample = sample;
        sensorhub_view_update_env(&s_ctx.dps_sample,
            s_ctx.has_sht ? &s_ctx.sht_sample : NULL);
    }
}
```

---

# จุดที่มักพลาด

- คิดว่ามี 4 FreeRTOS task + queue — จริงคือ `lv_timer` เดียวเป็น scheduler
- จำคาบผิดเป็น 200/500/20/50 ms — จริงคือ 1000/1000/200/120 ms
- ลืมว่า tick 100 ms ปัดคาบ BMM350 (120ms) ขึ้นเป็น 200ms — calibration ช้าลงเกือบสองเท่า
- คิดว่าจอแสดงทุก tile พร้อมกัน — จริงเป็นแท็บ 5 หน้าทีละหน้า
- ลืม patch บั๊ก BMM350 — บั๊กเดียวกับบทเรียน 3.4 ยังอยู่

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

- หลักฐานที่ประเมิน (`gui.hmi` ระดับ 3): วิดีโอแดชบอร์ดบนบอร์ดจริง 1 นาที พร้อมคำอธิบายการออกแบบ

---

# เช็กความเข้าใจ

- เซนเซอร์ตัวใดควรอ่านถี่ที่สุด และตัวใดอ่านช้าได้
- อะไรทำให้จอกระตุกเมื่อรวมเซนเซอร์หลายตัว
- ถ้าจะส่งข้อมูลชุดนี้ขึ้น TESAIoT Platform ควรเลือกค่าใดบ้าง

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep07_sensorhub_final) ที่ commit `9a8e3ed`
