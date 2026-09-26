---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.5 — Motion radar: วาดทิศการเคลื่อนไหวแบบ polar"
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

# บทเรียน 3.5 — Motion radar: วาดทิศการเคลื่อนไหวแบบ polar

## นำข้อมูล accelerometer/gyroscope จาก BMI270 มาวาดเป็น motion radar บนจอ LVGL เพื่อให้เห็นทิศทางการเคลื่อนไหวแบบ polar

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar
2. ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms
3. ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m03.l04`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP05 — BMI270 Radar View บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/int_ep05_bmi270_radar_view.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — baseline จับครั้งเดียวตอน boot

เฉลี่ย accel X/Y + gyro Z ของ **30 ตัวอย่างแรก** (~1.5 วิที่ 50 ms/ตัวอย่าง) แล้วไม่คำนวณใหม่อีกเลย

ไม่ใช่ moving-average/low-pass ต่อเนื่อง — ไม่เพิ่ม latency แต่ถ้าท่าตอน boot ไม่ใช่ท่าใช้งานจริง จะผิดไปตลอด

---

# แนวคิด — มุม/ขนาดจากส่วนต่างจาก baseline

`acc_dx = acc_g_x - baseline_x`, `acc_dy` แบบเดียวกัน → ใช้แค่ X/Y ของ**ส่วนต่าง** ไม่รวม Z ไม่ใช่ raw magnitude

`atan2f(acc_dy, acc_dx)` — radar ชี้ทาง "ที่ความเร่งเพิ่งเปลี่ยนจากตอน boot" ไม่ใช่ทิศรวมปัจจุบัน

---

# แนวคิด — dead-band สองเกณฑ์ก่อนขยับเข็ม

`motion_active` จริงเมื่อ `acc_xy_delta ≥ 0.06g` **หรือ** `gyr_z_delta ≥ 12°/s` เท่านั้น

ไม่ถึง → บังคับมุม = 0 ไม่วาดเข็มเลย — กัน `atan2()` ของเวกเตอร์เกือบศูนย์ให้มุมสุ่ม

ต่างจาก low-pass: **ไม่เพิ่ม latency** เลย เป็นการตัดสินใจต่อตัวอย่างเดียว

---

# แนวคิด — 3 ระดับความแรงจาก score ที่ normalize

`acc_score = delta/0.45g`, `gyr_score = delta/140°/s` → ใช้ค่าที่**มากกว่า**

`< 0.35` LOW (เขียว) · `0.35–0.80` MEDIUM (เหลืองอำพัน) · `≥ 0.80` HIGH (แดง)

ไม่มีใน README ต้นทางเลย — ทำให้อ่านทั้ง "แรงแค่ไหน" (สี) และ "ทางไหน" (มุม) พร้อมกัน

---

# แนวคิด — จอจริงใช้ `lv_scale` เข็มเดียว ไม่ใช่ canvas+trace

README ต้นทาง: `lv_canvas` วาด 4 ring + trace 64 จุด

**โค้ดจริง**: `lv_scale` widget สำเร็จรูป (dial 0-360°) + เข็มเดียวด้วย `lv_scale_set_line_needle_value()`

เข็มซ่อนเมื่อนิ่ง ไม่มี trace history เลย — gyro แสดงผ่าน dual-ring arc gauge แยกต่างหาก

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sys.dsp` (ระดับ 2)
- `gui.hmi` (ระดับ 3)
- `sys.sensors-actuators` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — มุมและ dead-band

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`radar_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_presenter.c)

```c
acc_dx = sample.acc_g_x - s_baseline_acc_x;
acc_dy = sample.acc_g_y - s_baseline_acc_y;
acc_xy_delta_g = sqrtf((acc_dx*acc_dx)+(acc_dy*acc_dy));

motion_active = s_baseline_ready &&
    ((acc_xy_delta_g >= RADAR_STILL_ACC_DELTA_G) ||
     (gyr_z_delta_abs_dps >= RADAR_STILL_GYR_DELTA_DPS));

angle_deg = motion_active ?
    (atan2f(acc_dy, acc_dx) * RADAR_DEG_PER_RAD) : 0.0f;
```

---

# ตัวอย่างสมบูรณ์ — เข็มเดียวบน `lv_scale`

[`radar_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_view.c)

```c
s_view.radar_scale = lv_scale_create(radar_card);
lv_scale_set_mode(s_view.radar_scale, LV_SCALE_MODE_ROUND_INNER);
lv_scale_set_range(s_view.radar_scale, 0, 360);

s_view.radar_needle = lv_line_create(s_view.radar_scale);
lv_scale_set_line_needle_value(s_view.radar_scale,
    s_view.radar_needle, 18, 0);
/* Hide needle in STILL state. */
lv_obj_add_flag(s_view.radar_needle, LV_OBJ_FLAG_HIDDEN);
```

---

# จุดที่มักพลาด

- บอร์ดไม่ราบตอน boot → เข็มค้างชี้ทิศเดียวแม้วางนิ่ง — baseline จับครั้งเดียว
- คิดว่า magnitude มาจากทั้งสามแกน — จริงใช้แค่ X/Y ส่วนต่างจาก baseline
- เอา dead-band ออกเพื่อให้ "ไวขึ้น" — เข็มจะส่ายสุ่มตอนบอร์ดนิ่งสนิท
- คิดว่ามี canvas+ring 4 วง+trace — จริงคือ `lv_scale` เข็มเดียว ไม่มีประวัติเก็บไว้

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- atan2 ใช้ทำอะไรในการหาทิศ
- dead-band ต่างจาก moving average อย่างไรในแง่ความหน่วงของจุดบน radar
- สีหรือขนาดของจุดควรสื่อข้อมูลอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep05_bmi270_radar_view) ที่ commit `9a8e3ed`
