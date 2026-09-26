---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.3 — ตัวบ่งชี้ความชื้นและอุณหภูมิจาก SHT4x"
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

# บทเรียน 3.3 — ตัวบ่งชี้ความชื้นและอุณหภูมิจาก SHT4x

## วัดความชื้นสัมพัทธ์และอุณหภูมิด้วยเซนเซอร์ Sensirion SHT4x บน I2C แล้วแสดงผลเป็นตัวบ่งชี้บนจอ LVGL

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่านความชื้นสัมพัทธ์และอุณหภูมิจาก SHT4x ผ่าน I2C แล้วแสดงเป็นตัวบ่งชี้
2. ตั้งเกณฑ์สีของตัวบ่งชี้จากช่วงความชื้นที่สบาย และอธิบายที่มาของเกณฑ์
3. เปรียบเทียบอุณหภูมิจาก SHT4x กับ DPS368 และอธิบายว่าทำไมอาจไม่เท่ากัน

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m03.l02`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP03 — SHT40 Indicator บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/int_ep03_sht40_indicator.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — SHT4x คืออะไร

Sensirion — RH ±1.8%, T ±0.2°C, RH 0-100%, T -40..125°C, < 0.4 µA ที่ 1 Hz

ไม่มี register map — คุยด้วย **command-based protocol**: ส่ง command byte → รอ delay → อ่าน 6 byte + CRC-8

---

# แนวคิด — โปรโตคอลอยู่ในมิดเดิลแวร์ ไม่ใช่โค้ดของ episode

`sht4x_driver.c` **ไม่มี** command byte/CRC เอง — เรียก `mtb_sht4x_measure_high_precision()` ตัวเดียว

มิดเดิลแวร์ทำครบ (ส่ง `0xFD`, รอ, อ่าน, ตรวจ CRC, แปลงหน่วย) คืนเป็น milli-units — โค้ด episode แค่หาร 1000

รูปแบบเดียวกับ DPS368/BMI270: ห่อโปรโตคอล byte ไว้ในไลบรารีผู้ผลิตเสมอ

---

# แนวคิด — เกณฑ์สีจริงมีแค่ 3 โซน

README ต้นทาง: 30/60/80% (4 โซน มีแดง "อันตราย")

**โค้ดจริง**: < 40% Dry (เหลืองอำพัน) · 40-60% Comfort (เขียว) · > 60% Humid (น้ำเงิน) — ไม่มีโซนแดง

40-60% ตรงกับคำแนะนำ HVAC/ASHRAE ทั่วไป

---

# แนวคิด — เกณฑ์ถูกกำหนดซ้ำสองที่

`hum_level_color()` (สี) และ `set_comfort_chip()` (ข้อความ) hard-code 40.0f/60.0f **แยกกันคนละฟังก์ชัน**

แก้ที่เดียวลืมอีกที่ → ข้อความกับสีไม่ตรงกัน (เช่น "Humid" แต่สียังเขียว)

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sys.sensors-actuators` (ระดับ 2)
- `proto.i2c` (ระดับ 2)
- `gui.hmi` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — driver เรียกมิดเดิลแวร์ตัวเดียว

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`sht4x_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_sensor/sht4x/sht4x_driver.c)

```c
cy_rslt_t sht4x_driver_read_sample(sht4x_sample_t *sample)
{
    int32_t temp_milli_c = 0;
    int32_t hum_milli_rh = 0;

    cy_rslt_t rslt = mtb_sht4x_measure_high_precision(
        s_i2c_bus, &temp_milli_c, &hum_milli_rh);
    if (CY_RSLT_SUCCESS != rslt) { return rslt; }

    /* Middleware returns milli-units; convert once here. */
    sample->temperature_c = ((float)temp_milli_c) / 1000.0f;
    sample->humidity_rh = ((float)hum_milli_rh) / 1000.0f;
    return CY_RSLT_SUCCESS;
}
```

---

# ตัวอย่างสมบูรณ์ — เกณฑ์สีตัวจริง

[`sht4x_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/app_ui/sht4x/sht4x_view.c)

```c
static lv_color_t hum_level_color(float humidity_rh)
{
    if (humidity_rh < 40.0f)
    {
        return lv_color_hex(0xD97706);   /* Dry */
    }
    if (humidity_rh <= 60.0f)
    {
        return lv_color_hex(0x16A34A);   /* Comfort */
    }
    return lv_color_hex(0x2563EB);       /* Humid */
}
```

---

# จุดที่มักพลาด

- คิดว่าต้องเขียน command byte/CRC-8 เอง — จริงอยู่ในมิดเดิลแวร์แล้ว
- จำเกณฑ์สีผิดเป็น 4 โซน (30/60/80%) — จริงมีแค่ 3 โซน (40/60)
- แก้เกณฑ์สีแค่ฟังก์ชันเดียว — ต้องแก้ `hum_level_color()` กับ `set_comfort_chip()` พร้อมกัน

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- ความชื้นสัมพัทธ์ขึ้นกับอุณหภูมิอย่างไร
- ทำไมเซนเซอร์สองตัวบนบอร์ดเดียวกันอ่านอุณหภูมิไม่เท่ากัน
- เกณฑ์สีของคุณใช้ช่วงความชื้นเท่าไร และอ้างอิงจากอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep03_sht40_indicator) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep03_sht40_indicator) ที่ commit `9a8e3ed`
