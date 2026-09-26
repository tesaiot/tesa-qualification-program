---
id: fw-stack.m03.l05
lang: th
title:
  th: "Motion radar: วาดทิศการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
summary:
  th: "นำข้อมูล accelerometer/gyroscope จาก BMI270 มาวาดเป็น motion radar บนจอ LVGL เพื่อให้เห็นทิศทางการเคลื่อนไหวแบบ polar"
  en: "Motion radar: movement direction in polar form"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l04]
objectives:
  - th: "แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar"
    en: "Turn accelerometer and gyroscope readings into angle and magnitude and draw them in polar form"
  - th: "ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms"
    en: "Use a baseline and a dead-band to drop small jitter before drawing, and work out how much lag a moving average would add at the 50 ms read period"
  - th: "ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที"
    en: "Design a view that lets a user read the direction within a second"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: gui.hmi, to: 3}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep05_bmi270_radar_view"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# Motion radar: วาดทิศการเคลื่อนไหวแบบ polar

## เป้าหมาย

1. แปลงค่า accelerometer และ gyroscope เป็นมุมและขนาด แล้ววาดเป็นกราฟ polar
2. ใช้ baseline และ dead-band ตัดการสั่นเล็ก ๆ ก่อนวาด และคำนวณว่าถ้าใช้ moving average แทน จะเพิ่มความหน่วงเท่าไรที่คาบเวลาอ่าน 50 ms
3. ออกแบบการแสดงผลที่ผู้ใช้อ่านทิศทางได้ในหนึ่งวินาที

## แนวคิด

### baseline คือ "ท่านิ่ง" ที่จับตอน boot ครั้งเดียว ไม่ใช่ high-pass filter แบบต่อเนื่อง

`radar_update_baseline()` เฉลี่ย accel X/Y และ gyro Z ของ **30 ตัวอย่างแรก** (ที่คาบอ่าน `BMI270_SAMPLE_PERIOD_MS
= 50` ก็คือประมาณ 1.5 วินาทีแรกหลัง boot) เก็บไว้เป็น `s_baseline_acc_x/y`, `s_baseline_gyr_z` แล้ว**ไม่คำนวณใหม่
อีกเลย**ตลอด session นี่คือวิธีลบ gravity/offset คงที่แบบง่ายที่สุด (baseline subtraction) ไม่ใช่ moving-average
หรือ low-pass filter ที่คำนวณต่อเนื่อง — ข้อดีคือไม่เพิ่มความหน่วง (latency) เลย ข้อเสียคือถ้าท่าทางตอนบูตไม่ใช่ท่า
ที่จะใช้งานจริง baseline จะผิดไปตลอด

### มุมและขนาดบน radar คำนวณจาก**ส่วนต่างจาก baseline** ไม่ใช่ค่าดิบสามแกน

จุดที่ต่างจากสูตร Cartesian→Polar ทั่วไปคือ code คำนวณ `acc_dx = sample.acc_g_x - s_baseline_acc_x` และ `acc_dy`
แบบเดียวกัน แล้ว `acc_xy_delta_g = sqrt(acc_dx² + acc_dy²)` — ใช้แค่แกน X/Y ของ**ส่วนต่าง**เท่านั้น ไม่รวมแกน Z และ
ไม่ใช่ magnitude ของเวกเตอร์ดิบ (ที่จะรวม gravity ~1g ติดมาตลอดเวลาแม้บอร์ดไม่ขยับ) มุมทิศคือ `atan2f(acc_dy,
acc_dx)` ของเวกเตอร์ส่วนต่างนี้ — พูดอีกแบบคือ radar ชี้ไปทาง "ทิศที่ความเร่งเพิ่งเปลี่ยนไปจากตอน boot" ไม่ใช่
"ทิศที่ความเร่งรวมชี้อยู่ ณ ขณะนี้"

### dead-band สองเกณฑ์ก่อนยอมให้เข็มขยับเลย

ก่อนจะคำนวณมุมด้วยซ้ำ โค้ดเช็คก่อนว่า `acc_xy_delta_g >= 0.06g` **หรือ** `gyr_z_delta_abs_dps >= 12°/s` ถ้าไม่ถึง
ทั้งคู่จะถือว่า `motion_active = false` แล้วบังคับมุมเป็น 0 และไม่วาดเข็มเลย เหตุผลคือ `atan2()` ของเวกเตอร์ที่
เกือบเป็นศูนย์ (สัญญาณรบกวนระดับ mg) จะให้มุมสุ่มไปทุกทิศ ถ้าไม่มี dead-band เข็มจะส่ายไปมาทั้งที่บอร์ดนิ่งสนิท
เทคนิคนี้ต่างจาก low-pass filter ตรงที่ **ไม่เพิ่มความหน่วง** เลย (ไม่มีการเฉลี่ยข้ามเวลา) แค่ตัดสินใจแสดง/ไม่แสดง
ต่อตัวอย่างเดียว ๆ

### สามระดับความแรง คำนวณจาก score ที่ normalize แล้วเทียบสองแกน

`radar_calc_motion_level()` แปลง `acc_xy_delta_g` และ `gyr_z_delta_abs_dps` เป็น score โดยหารด้วยค่าคงที่คนละตัว
(`0.45g` และ `140°/s`) แล้วเลือก score ที่**มากกว่า**ระหว่างสองค่านั้นมาตัดสินระดับ — `< 0.35` = LOW (เขียว
`0x22C55E`), `0.35–0.80` = MEDIUM (เหลืองอำพัน `0xF59E0B`), `≥ 0.80` = HIGH (แดง `0xEF4444`) ระบบนี้ไม่ได้อยู่ใน
README ต้นทางเลย แต่เป็นสิ่งที่ทำให้ผู้ใช้อ่านทั้ง "แรงแค่ไหน" (จากสี) และ "ไปทางไหน" (จากมุมเข็ม) ได้พร้อมกันใน
แวบเดียว

### หน้าจอจริงใช้ widget `lv_scale` + เข็มเดียว ไม่ใช่ canvas วาด ring และ trace history

README ต้นทางอธิบายว่าใช้ `lv_canvas` วาดวงแหวนซ้อน 4 วง เส้นทิศหลัก N/E/S/W และเก็บ trace 64 จุดล่าสุดมาต่อเป็น
เส้นแบบจางลงตามอายุ — แต่โค้ดจริงใช้ **`lv_scale`** ซึ่งเป็น widget สำเร็จรูปของ LVGL 9 (หน้าปัดวงกลม 0–360°
พร้อม tick 41 อัน) แล้ววาด**เข็มเดียว**ด้วย `lv_scale_set_line_needle_value(scale, needle, needle_len, angle_i)`
โดยความยาวเข็มสื่อขนาดของการเคลื่อนไหว มุมสื่อทิศทาง และเข็มถูกซ่อน (`LV_OBJ_FLAG_HIDDEN`) เมื่อ `motion_active`
เป็น false ไม่มี trace history หรือ ring grid หลายวงเลย ส่วน gyro แสดงผ่าน dual-ring arc gauge อีกตัว
(`intensity_gyr_arc`) ที่ map ค่า delta เป็น 0–100 ไม่ใช่ arc มุมตามแกน Z ตามที่ README ต้นทางอธิบาย

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะการคำนวณและ widget บนจอต่างจากที่ README ต้นทางอธิบายมาก

[`app_ui/radar/radar_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_presenter.c) — มุมและ dead-band จาก baseline delta:

```c
acc_dx = sample.acc_g_x - s_baseline_acc_x;
acc_dy = sample.acc_g_y - s_baseline_acc_y;
acc_xy_delta_g = sqrtf((acc_dx * acc_dx) + (acc_dy * acc_dy));
gyr_z_delta_abs_dps = fabsf(sample.gyr_dps_z - s_baseline_gyr_z);

/* Treat signal as STILL until delta crosses threshold from baseline. */
motion_active = s_baseline_ready &&
                ((acc_xy_delta_g >= RADAR_STILL_ACC_DELTA_G) ||
                 (gyr_z_delta_abs_dps >= RADAR_STILL_GYR_DELTA_DPS));

angle_deg = motion_active ? (atan2f(acc_dy, acc_dx) * RADAR_DEG_PER_RAD) : 0.0f;
level = motion_active ? radar_calc_motion_level(acc_xy_delta_g, gyr_z_delta_abs_dps) : RADAR_LEVEL_LOW;
```

สามระดับความแรงจาก score ที่ normalize แล้ว:

```c
static radar_motion_level_t radar_calc_motion_level(float acc_xy_delta_g, float gyr_z_delta_abs_dps)
{
    float acc_score = acc_xy_delta_g / 0.45f;
    float gyr_score = gyr_z_delta_abs_dps / 140.0f;
    float score = (acc_score > gyr_score) ? acc_score : gyr_score;

    if (score < 0.35f) { return RADAR_LEVEL_LOW; }
    if (score < 0.80f) { return RADAR_LEVEL_MEDIUM; }
    return RADAR_LEVEL_HIGH;
}
```

[`app_ui/radar/radar_view.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_ui/radar/radar_view.c) — เข็มเดียวบน `lv_scale`, ซ่อนเมื่อนิ่ง:

```c
s_view.radar_scale = lv_scale_create(radar_card);
lv_scale_set_mode(s_view.radar_scale, LV_SCALE_MODE_ROUND_INNER);
lv_scale_set_range(s_view.radar_scale, 0, 360);
lv_scale_set_total_tick_count(s_view.radar_scale, 41);

s_view.radar_needle = lv_line_create(s_view.radar_scale);
lv_scale_set_line_needle_value(s_view.radar_scale, s_view.radar_needle, 18, 0);
/* Hide needle in STILL state; presenter shows it only when motion is active. */
lv_obj_add_flag(s_view.radar_needle, LV_OBJ_FLAG_HIDDEN);
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/main_example.c) ส่ง I2C handle เข้า `radar_presenter_start()` ตรงตามที่ README ต้นทางอธิบาย
- [`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/app_sensor/bmi270/bmi270_config.h) — `BMI270_SAMPLE_PERIOD_MS = 50` (เร็วกว่าบทเรียน 3.2 ที่ 200 ms เพราะ radar ต้องการความไวสูงกว่า)
- ดูโฟลเดอร์เต็มที่ [`int_ep05_bmi270_radar_view/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view)

## จุดที่มักพลาด

- **บอร์ดไม่ราบตอน boot ทำให้เข็มค้างชี้ทิศเดียวแม้วางนิ่ง** — baseline จับจาก 30 ตัวอย่างแรกครั้งเดียว ถ้าตอน
  boot บอร์ดเอียงอยู่ ท่าราบทีหลังจะต่างจาก baseline เกินเกณฑ์ STILL ทำให้ดูเหมือนเคลื่อนไหวตลอด ต้องวางบอร์ดนิ่ง
  ในท่าที่จะใช้งานจริงตอนเปิดเครื่อง
- **คิดว่า magnitude มาจากทั้งสามแกน (x,y,z)** — โค้ดจริงใช้แค่ส่วนต่างของ X/Y จาก baseline ไม่รวม Z และไม่ใช่ค่า
  ดิบ
- **ลดหรือเอา dead-band ออกเพื่อให้ "ไวขึ้น"** — จะทำให้เข็มส่ายแบบสุ่มตอนบอร์ดนิ่งสนิท เพราะ `atan2()` ของ
  เวกเตอร์เกือบศูนย์ไม่มีความหมาย
- **คิดว่ามี canvas วาด ring 4 วงกับ trace 64 จุด** — หน้าจอจริงใช้ `lv_scale` widget สำเร็จรูปกับเข็มเดียว ไม่มี
  ประวัติการเคลื่อนไหวเก็บไว้เลย

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP05 — BMI270 Radar View บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/int_ep05_bmi270_radar_view.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- atan2 ใช้ทำอะไรในการหาทิศ
- dead-band ต่างจาก moving average อย่างไรในแง่ความหน่วงของจุดบน radar
- สีหรือขนาดของจุดควรสื่อข้อมูลอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep05_bmi270_radar_view) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep05_bmi270_radar_view&q=int_ep05_bmi270_radar_view)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
