---
id: fw-stack.m03.l07
lang: th
title:
  th: "SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)"
  en: "SensorHub: one dashboard for every sensor (series project)"
summary:
  th: "โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว"
  en: "SensorHub: one dashboard for every sensor (series project)"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l06]
objectives:
  - th: "รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว"
    en: "Combine the DPS368, SHT4x, BMI270, BMM350 and PDM microphone on one dashboard"
  - th: "จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก"
    en: "Schedule each sensor read so the screen does not stutter"
  - th: "นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร"
    en: "Present the dashboard and explain how each value is shown"
develops:
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: rtos.basics, to: 2}
  - {skill: soft.problem-solving, to: 2}
  - {skill: soft.communication, to: 2}
assesses:
  - {skill: gui.hmi, level: 3, evidence: "วิดีโอแดชบอร์ดบนบอร์ดจริง 1 นาที พร้อมคำอธิบายการออกแบบ"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep07_sensorhub_final"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# SensorHub: แดชบอร์ดรวมเซนเซอร์ทุกตัว (งานปิดชุด)

## เป้าหมาย

1. รวม DPS368, SHT4x, BMI270, BMM350 และไมโครโฟน PDM ไว้บนแดชบอร์ดเดียว
2. จัดจังหวะการอ่านเซนเซอร์แต่ละตัวให้จอไม่กระตุก
3. นำเสนอแดชบอร์ดพร้อมอธิบายว่าเลือกแสดงข้อมูลแต่ละตัวอย่างไร

## แนวคิด

### ประสานสี่เซนเซอร์ด้วย `lv_timer` เดียว ไม่ใช่สี่ FreeRTOS task ตามที่ README ต้นทางอธิบาย

README ต้นทางอธิบายว่า episode นี้สร้าง "4 reader task (ละ 2 KB stack) priority เท่ากัน" ที่ push ข้อมูลผ่าน
single message queue แบบ tagged union แล้ว consumer dispatch ผ่าน `lv_async_call()` — แต่โค้ดจริงที่ commit
`9a8e3ed` **ไม่มี** `xTaskCreate`, `xQueueCreate`, หรือ `lv_async_call` แม้แต่ตัวเดียวใน
`sensorhub_presenter.c` ทั้งไฟล์ สถาปัตยกรรมจริงคือ `lv_timer` **หนึ่งตัว** ที่ `HUB_UI_POLL_MS = 100` ทำหน้าที่
เป็น cooperative scheduler เอง — ทุก 100 ms มันเช็คว่าถึงเวลาของเซนเซอร์ตัวไหนบ้าง แล้วอ่านเฉพาะตัวที่ถึงรอบ
เท่านั้น ทั้งหมดยังรันบน LVGL thread เดียว ไม่มี thread อื่นเข้ามายุ่งกับ sensor reading เลย

### รูปแบบ "next due time" ต่อเซนเซอร์ ภายใน timer เดียว

แต่ละเซนเซอร์มีตัวแปร `next_..._ms` ของตัวเอง (`next_dps_ms`, `next_sht_ms`, `next_bmi_ms`, `next_bmm_ms`) ทุกครั้ง
ที่ timer ทำงาน (ทุก 100 ms) จะเช็คแบบ `(int32_t)(now_ms - next_xxx_ms) < 0` ถ้ายังไม่ถึงจะข้าม ถ้าถึงแล้วจะอ่าน
เซนเซอร์ตัวนั้นแล้วตั้งเวลาถัดไปเป็น `now_ms + <คาบของเซนเซอร์นั้น>` — คาบของแต่ละเซนเซอร์คือค่าเดิมจากบทเรียนของ
มันเองไม่มีการเปลี่ยน (`DPS368_SAMPLE_PERIOD_MS = 1000`, `SHT4X_SAMPLE_PERIOD_MS = 1000`,
`BMI270_SAMPLE_PERIOD_MS = 200`, `BMM350_SAMPLE_PERIOD_MS = 120`) — **ไม่ใช่ตาราง 200/500/20/50 ms** ตามที่
README ต้นทางอ้างไว้เลยสักตัว

### ผลข้างเคียงของ tick 100 ms: คาบที่ไม่ใช่ผลคูณของ 100 จะถูกปัดขึ้น

เพราะ timer หลักเดินทุก 100 ms พอดี เซนเซอร์ที่มีคาบไม่ใช่ผลคูณของ 100 (เช่น BMM350 ที่ 120 ms) จะไม่มีวันถูกอ่าน
ตรงตามคาบของมันเอง — ที่ t=100 ms ยังไม่ถึง 120 จึงข้าม ที่ t=200 ms ถึงแล้วจึงอ่านแล้วตั้ง next เป็น 320 ซึ่งจะถูก
ข้ามที่ t=300 อีก จนอ่านจริงที่ t=400 — คาบจริงที่ใช้งานจึงกลายเป็น 200 ms ไม่ใช่ 120 ms ผลต่อเนื่องที่วัดได้ชัดคือ
**auto-calibration ของ BMM350 ที่ต้องเก็บ 140 ตัวอย่าง (บทเรียน 3.4) ใช้เวลาประมาณ 28 วินาทีใน episode นี้ ไม่ใช่
16.8 วินาทีเหมือนตอนรันเดี่ยว ๆ ใน EP04** เพราะแต่ละตัวอย่างมาช้าลงเป็นสองเท่าจากการปัดเวลา

### calibration ของ BMM350 เริ่มอัตโนมัติตั้งแต่ boot ไม่ต้องกดปุ่มเหมือนบทเรียน 3.4

`sensorhub_presenter_start()` เรียก `bmm350_reader_start_calibration()` เองทันทีตอนเริ่ม ต่างจากบทเรียน 3.4 ที่
ผู้ใช้ต้องกดปุ่ม Calibrate เอง — เพราะ dashboard นี้ต้องการให้เข็มทิศพร้อมใช้โดยเร็วที่สุดโดยผู้ใช้ไม่ต้องรู้ขั้นตอน
เพิ่ม (ผู้ใช้แค่ต้องหมุนบอร์ดตามคำแนะนำระหว่างที่หน้าจออื่นกำลังทำงานอยู่)

### หน้าจอจริงเป็นแท็บ 5 หน้า ไม่ใช่ grid 2×2 + บาร์ล่างตามที่ README ต้นทางวาดไว้

README ต้นทางวาดผังหน้าจอเป็น grid 2×2 (DPS368/SHT4x แถวบน, BMI270/BMM350 แถวล่าง) บวกแถบ mic ด้านล่างที่แสดง
พร้อมกันทั้งหมด — แต่โค้ดจริงมี `sensorhub_page_t` ห้าค่า (`SENSORHUB_PAGE_HOME`, `_ENV`, `_MOTION`, `_COMPASS`,
`_AUDIO`) และ `sensorhub_view_set_active_page()` ซ่อนหน้าที่ไม่ได้เลือกไว้ — เป็น**แท็บที่แสดงทีละหน้า**เหมือนโครง
navigation shell จากโมดูล 2 (บทเรียน 2.4 เป็นต้นไป) ไม่ใช่ tile ทั้งหมดโชว์พร้อมกันในจอเดียว หน้า Audio เองก็แสดง
**ระดับเสียงที่คำนวณแล้ว** (peak/avg ตามบทเรียน 3.6) ไม่ใช่รูปคลื่นดิบ

### patch ของ BMM350 ยังจำเป็นเหมือนเดิม

บั๊ก I3C soft-reset ของ `BMM350_SensorAPI` (อธิบายละเอียดในบทเรียน 3.4) ยังอยู่ในไลบรารีตัวเดียวกันที่ episode
นี้ใช้ — ต้อง patch ก่อน build เหมือนเดิม การแก้เป็น idempotent ถ้าทำใน EP04 แล้วไม่ต้องทำซ้ำสำหรับ workspace เดียวกัน

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md) เพื่อเข้าใจโจทย์ของบทปิดคอร์ส แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะสถาปัตยกรรมจริงต่างจากที่ README ต้นทางอธิบายมาก

[`app_ui/sensorhub/sensorhub_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_ui/sensorhub/sensorhub_presenter.c) — `lv_timer` เดียวเรียก poll ของทุกเซนเซอร์ทุกรอบ:

```c
static void sensorhub_poll_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    uint32_t now_ms = lv_tick_get();

    sensorhub_poll_dps(now_ms);
    sensorhub_poll_sht(now_ms);
    sensorhub_poll_bmi(now_ms);
    sensorhub_poll_bmm(now_ms);
    sensorhub_poll_bmm_calibration();
    sensorhub_poll_mic();
    /* ... */
}
/* ... */
s_ctx.poll_timer = lv_timer_create(sensorhub_poll_timer_cb, HUB_UI_POLL_MS, NULL);
```

รูปแบบ "next due time" ต่อเซนเซอร์หนึ่งตัว (DPS368 เป็นตัวอย่าง โครงเดียวกันซ้ำสำหรับ SHT4x/BMI270/BMM350):

```c
/* Poll DPS368 on its own sampling period and push value to Env page. */
static void sensorhub_poll_dps(uint32_t now_ms)
{
    if ((!s_ctx.dps_ready) || ((int32_t)(now_ms - s_ctx.next_dps_ms) < 0))
    {
        return;
    }

    s_ctx.next_dps_ms = now_ms + DPS368_SAMPLE_PERIOD_MS;

    dps368_sample_t sample;
    if (dps368_reader_poll(&sample))
    {
        s_ctx.dps_sample = sample;
        sensorhub_view_update_env(&s_ctx.dps_sample, s_ctx.has_sht ? &s_ctx.sht_sample : NULL);
        /* ... */
    }
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/main_example.c) เรียก `sensorhub_presenter_start()` แล้ว `pdm_probe_logger_start()` ตรงตามที่ README ต้นทางอธิบาย
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/bmi270/bmi270_config.h), [`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/bmm350/bmm350_config.h), [`app_sensor/dps368/dps368_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/dps368/dps368_config.h), [`app_sensor/sht4x/sht4x_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/app_sensor/sht4x/sht4x_config.h) — คาบจริงของแต่ละเซนเซอร์ ค่าเดิมจากบทเรียนของมันเองไม่เปลี่ยน
- ดูโฟลเดอร์เต็มที่ [`int_ep07_sensorhub_final/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final) — ไฟล์ของแต่ละเซนเซอร์ (driver/reader) เหมือนกับบทเรียน 3.1–3.4 ทุกประการ ต่างแค่ชั้น UI ที่มารวมกันใหม่

## จุดที่มักพลาด

- **คิดว่ามี 4 FreeRTOS task + queue ตามที่ README ต้นทางอธิบาย** — โค้ดจริงใช้ `lv_timer` เดียวเป็น cooperative
  scheduler ให้ยึดโค้ดจริงเมื่ออธิบายสถาปัตยกรรม
- **จำคาบการอ่านผิดเป็น 200/500/20/50 ms** — ค่าจริงคือ 1000/1000/200/120 ms ตรงจาก config.h ของแต่ละเซนเซอร์ที่
  ไม่ถูกแก้เลย
- **ลืมว่า tick หลัก 100 ms ปัดคาบที่ไม่ใช่ผลคูณของ 100 ขึ้น** — BMM350 (120 ms) ถูกอ่านจริงทุก 200 ms ทำให้
  auto-calibration ใช้เวลาเกือบสองเท่าของตอนรันเดี่ยวใน EP04
- **คิดว่าจอแสดงทุก tile พร้อมกันแบบ grid 2×2** — จริงเป็นแท็บ 5 หน้า (Home/Env/Motion/Compass/Audio) แสดงทีละ
  หน้าเท่านั้น
- **ลืม patch บั๊ก BMM350** — บั๊กเดียวกับบทเรียน 3.4 ยังอยู่ ต้อง patch ก่อน build เช่นเดิม

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP07 — SensorHub Final บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/int_ep07_sensorhub_final.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- เซนเซอร์ตัวใดควรอ่านถี่ที่สุด และตัวใดอ่านช้าได้
- อะไรทำให้จอกระตุกเมื่อรวมเซนเซอร์หลายตัว
- ถ้าจะส่งข้อมูลชุดนี้ขึ้น TESAIoT Platform ควรเลือกค่าใดบ้าง

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep07_sensorhub_final) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
