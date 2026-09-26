---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C"
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

# บทเรียน 3.1 — อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C

## อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ
2. อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode
3. ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l07`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP01 — DPS368 Monitor บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/int_ep01_dps368_monitor.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — DPS368 คืออะไร

Barometer แบบ capacitive MEMS ของ Infineon — วัดความดัน 300–1200 hPa ที่ความละเอียด ±0.002 hPa (≈ 2 ซม. ความสูง)

วัดอุณหภูมิร่วมด้วยเพื่อชดเชยค่าความดัน — สูตรชดเชยอยู่ในไลบรารี Infineon แล้ว

---

# แนวคิด — สี่ชั้นของโค้ด

`dps368_driver` (คุย `xensiv_dps3xx` โดยตรง) → `dps368_reader` (ห่อเป็น `poll()` เดียว) → `dps368_presenter` (ผูก timer) → `dps368_view` (label ล้วน ๆ ไม่มี gauge)

แต่ละชั้นรู้จักแค่ชั้นติดกัน — `view` ไม่รู้จัก I2C, `driver` ไม่รู้จัก LVGL

---

# แนวคิด — I2C bus พร้อมใช้ + address fallback

`main_example.c` ส่ง `&sensor_i2c_controller_hal_obj` ที่ master เปิดไว้แล้วตรงเข้า `dps368_presenter_start()`

ลองที่อยู่ default ก่อน (`0x77`) ไม่ตอบค่อยลอง alternate (`0x76` จากขา SDO) — ใช้ได้ทั้งสองแบบ strap

---

# แนวคิด — poll จริงคือ `lv_timer` เดียว ไม่ใช่ FreeRTOS task

`lv_timer_create(dps368_poll_sensor_cb, 1000, NULL)` — รันบน **LVGL thread เดียวกัน** กับที่วาดจอ

อ่าน I2C แบบ blocking ตรงในนั้นเลย ไม่มี queue หรือ `lv_async_call()` — เซนเซอร์เดียว ไม่คุ้มความซับซ้อนของ task แยก

---

# แนวคิด — แยก "ยังไม่พร้อม" จาก error จริง

`XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY` → `false` แต่ **ไม่ใช่ error** (แค่ยังไม่ถึงรอบ conversion)

error code อื่นถือเป็นปัญหาจริง แสดงบน status label — ถ้าไม่แยกจะกระพริบ error ทุกวินาทีที่ยังไม่ถึงรอบอ่าน

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `proto.i2c` (ระดับ 2)
- `sys.sensors-actuators` (ระดับ 2)
- `prog.design-patterns` (ระดับ 2)
- `lang.c` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — `lv_timer` เดียวที่ poll

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`dps368_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_ui/dps368/dps368_presenter.c)

```c
static void dps368_poll_sensor_cb(lv_timer_t *timer)
{
    (void)timer;

    dps368_sample_t sample;
    bool has_new_sample = dps368_reader_poll(&sample);

    if (has_new_sample)
    {
        dps368_view_update_sample(&sample);
        return;
    }

    cy_rslt_t rslt = dps368_reader_get_last_error();
    if (CY_RSLT_SUCCESS == rslt)
    {
        return;   /* not-ready is not an error */
    }
    /* ... real error -> update status label ... */
}
```

---

# ตัวอย่างสมบูรณ์ — แยก not-ready จาก error

[`dps368_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_reader.c)

```c
if (CY_RSLT_SUCCESS == rslt)
{
    s_last_sample.pressure_hpa = pressure_hpa;
    s_last_sample.sample_count++;
    if (NULL != out_sample) { *out_sample = s_last_sample; }
    return true;
}

/* At low sample rate, polling can happen before
 * conversion is ready. */
if (rslt == XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY)
{
    s_last_error = CY_RSLT_SUCCESS;
    return false;
}

s_last_error = rslt;
return false;
```

---

# จุดที่มักพลาด

- คิดว่ามี FreeRTOS task แยก poll ทุก 100 ms — จริงคือ `lv_timer` เดียวที่ 1000 ms อ่าน I2C แบบ blocking ตรง ๆ
- ถือว่า `DATA_NOT_READY` เป็น error — ต้องแยกออกเสมอ เป็นแค่สัญญาณว่ายังไม่ถึงรอบ conversion
- ลืมว่าเซนเซอร์มีสองที่อยู่ I2C (`0x77`/`0x76`) — hard-code ตัวเดียวจะใช้ไม่ได้กับบางบอร์ด

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- ชั้น presenter ทำอะไรที่ view ไม่ทำ
- ความดันควรเปลี่ยนอย่างไรเมื่อยกบอร์ดขึ้นสูงหนึ่งชั้นตึก
- ถ้าเซนเซอร์ตอบ I2C ไม่ได้ ข้อความผิดพลาดควรขึ้นที่ชั้นใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep01_dps368_monitor) ที่ commit `9a8e3ed`
