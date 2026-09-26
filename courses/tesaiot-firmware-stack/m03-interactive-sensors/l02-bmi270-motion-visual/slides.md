---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — ภาพการเคลื่อนไหว 6 แกนจาก BMI270"
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

# บทเรียน 3.2 — ภาพการเคลื่อนไหว 6 แกนจาก BMI270

## แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์
2. แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง
3. ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m03.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP02 — BMI270 Motion Visual บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/int_ep02_bmi270_motion_visual.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — BMI270 คืออะไร

IMU 6 แกนของ Bosch — accel 3 แกน (±2g ถึง ±16g, 16-bit) + gyro 3 แกน (±125 ถึง ±2000 °/s)

episode นี้ใช้ค่า default ของไลบรารี: **±2g และ ±2000 dps** (กว้างสุด ไม่ clip ตอนเขย่าแรง)

---

# แนวคิด — poll 200 ms ด้วย `lv_timer` เดียว

เหมือนบทเรียน 3.1 — ไม่ใช่ 100 Hz ผ่าน FreeRTOS task ตามที่บางครั้งอาจเข้าใจผิด

คอมเมนต์ในซอร์ส: "Poll slower to reduce redraw pressure on small HMI panel"

---

# แนวคิด — อ่านทุกรอบ วาดจอแค่บางรอบ

`BMI270_UI_UPDATE_DIV = 2` — อ่าน + ตัดสิน ALERT ทุก 200 ms แต่วาด widget แค่ทุก 2 ตัวอย่าง (400 ms)

การอ่านเซนเซอร์กับการวาดจอไม่ต้องคาบเดียวกัน — วาดแค่ถี่พอสายตาเห็นก็พอ

---

# แนวคิด — motion alert ใช้ hysteresis สองเกณฑ์

ฟีเจอร์ที่ README ต้นทางไม่พูดถึง: **MOTION ALERT**

- เปิดเมื่อ acc ≥ 1.45g หรือ gyro ≥ 280°/s
- ปิดเมื่อ acc < 1.25g **และ** gyro < 220°/s

เกณฑ์เปิด/ปิดต่างกัน → ไม่กระพริบเมื่อค่าแกว่งอยู่รอบเกณฑ์เดียว

---

# แนวคิด — จอแสดง "ขนาดรวม" ไม่ใช่ 6 แกนแยก

`bmi270_view.c` สร้างแค่ **2 บาร์** (accel/gyro magnitude) + **chart เส้นเดียว 2 series**

ไม่ใช่ 6 บาร์แยก x/y/z ตามที่บางครั้งอาจเข้าใจผิด — ค่าที่แสดงคือ √(x²+y²+z²)

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sys.sensors-actuators` (ระดับ 2)
- `proto.i2c` (ระดับ 2)
- `gui.hmi` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — ค่าคงที่ตัวจริง

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_config.h)

```c
/* Poll slower to reduce redraw pressure on small HMI panel. */
#define BMI270_SAMPLE_PERIOD_MS           (200U)

/* Update LVGL widgets every N samples to reduce flicker. */
#define BMI270_UI_UPDATE_DIV              (2U)

/* Motion thresholds with hysteresis. */
#define BMI270_ALERT_ACC_ON_G             (1.45f)
#define BMI270_ALERT_ACC_OFF_G            (1.25f)
#define BMI270_ALERT_GYR_ON_DPS           (280.0f)
#define BMI270_ALERT_GYR_OFF_DPS          (220.0f)
```

---

# ตัวอย่างสมบูรณ์ — hysteresis สำหรับ alert

[`bmi270_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_ui/bmi270/bmi270_presenter.c)

```c
static bool bmi270_should_alert(const bmi270_sample_t *sample,
                                bool is_alert_active)
{
    if (is_alert_active)
    {
        bool below_acc = (sample->acc_mag_g < BMI270_ALERT_ACC_OFF_G);
        bool below_gyr = (sample->gyr_mag_dps < BMI270_ALERT_GYR_OFF_DPS);
        return !(below_acc && below_gyr);
    }

    return ((sample->acc_mag_g >= BMI270_ALERT_ACC_ON_G) ||
            (sample->gyr_mag_dps >= BMI270_ALERT_GYR_ON_DPS));
}
```

---

# จุดที่มักพลาด

- จำ poll rate ผิดเป็น 100 Hz ผ่าน FreeRTOS task — จริงคือ 200 ms ด้วย `lv_timer` เดียว
- คิดว่าอ่านเซนเซอร์กับวาดจอต้องคาบเดียวกัน — จริงแยกกันด้วย `UI_UPDATE_DIV`
- ใช้ threshold เดียวสำหรับ alert — ไม่มี hysteresis จะกระพริบเมื่อค่าแกว่งรอบเกณฑ์
- คิดว่าจอแสดงค่าต่อแกน x/y/z — จริงแสดงแค่ขนาดรวม 2 บาร์

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- บอร์ดวางนิ่งบนโต๊ะ แกนใดควรอ่านได้ประมาณ 1 g
- gyroscope อ่านอะไรเมื่อบอร์ดไม่หมุน
- ทำไมไม่ควรวาดจอทุกครั้งที่อ่านเซนเซอร์ได้

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep02_bmi270_motion_visual) ที่ commit `9a8e3ed`
