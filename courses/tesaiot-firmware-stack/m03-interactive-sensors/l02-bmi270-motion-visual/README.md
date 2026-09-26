---
id: fw-stack.m03.l02
lang: th
title:
  th: "ภาพการเคลื่อนไหว 6 แกนจาก BMI270"
  en: "Six-axis motion from the BMI270"
summary:
  th: "แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์"
  en: "Six-axis motion from the BMI270"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l01]
objectives:
  - th: "อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์"
    en: "Read the BMI270 accelerometer and gyroscope and display them in real time"
  - th: "แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง"
    en: "Tell acceleration (g) from angular rate (°/s) and predict the values of a board at rest"
  - th: "ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์"
    en: "Match the screen refresh rate to the sensor read rate"
develops:
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: proto.i2c, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep02_bmi270_motion_visual"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# ภาพการเคลื่อนไหว 6 แกนจาก BMI270

## เป้าหมาย

1. อ่าน accelerometer และ gyroscope จาก BMI270 แล้วแสดงแบบเรียลไทม์
2. แยกความหมายของค่าเร่ง (g) กับค่าหมุน (°/s) และทายค่าที่ควรเห็นเมื่อวางบอร์ดนิ่ง
3. ปรับอัตราการรีเฟรชหน้าจอให้เหมาะกับอัตราการอ่านเซนเซอร์

## แนวคิด

### BMI270 คืออะไร และตัวเลขในสเปกหมายถึงอะไร

BMI270 เป็น IMU (Inertial Measurement Unit) 6 แกนของ Bosch มี accelerometer วัดความเร่งได้ 3 แกน (เลือกช่วงได้
±2g/±4g/±8g/±16g ความละเอียด 16-bit) และ gyroscope วัดอัตราการหมุนได้ 3 แกน (±125 ถึง ±2000 องศา/วินาที) episode
นี้ตั้งค่าเริ่มต้นของไลบรารี `mtb_bmi270_config_default()` ไว้ตามที่มากับไลบรารีคือ **±2g และ ±2000 dps** (ค่ากว้าง
ที่สุดของแต่ละเซนเซอร์ ไม่ใช่ ±4g/±500dps ตามที่ระบุใน README ต้นทาง) เหมาะกับการสอนเพราะรับค่าการเขย่าแรง ๆ ได้
โดยไม่ clip แต่แลกกับความละเอียดต่อบิตที่หยาบกว่าถ้าเลือกช่วงแคบกว่า

### poll ทุก 200 ms ด้วย `lv_timer` เดียว เหมือน DPS368 — ไม่ใช่ 100 Hz ผ่าน FreeRTOS task

เหมือนบทเรียน 3.1 (DPS368) episode นี้ก็ใช้ `lv_timer_create(bmi270_poll_sensor_cb, BMI270_SAMPLE_PERIOD_MS, NULL)`
บน LVGL thread เดียว โดย `BMI270_SAMPLE_PERIOD_MS = 200` (5 ครั้ง/วินาที) — ไม่ใช่ทุก 10 ms (100 Hz) ผ่าน FreeRTOS
task + queue + `lv_async_call()` ตามที่ README ต้นทางอธิบาย คอมเมนต์ในซอร์สบอกเหตุผลตรง ๆ ว่า "Poll slower to
reduce redraw pressure on small HMI panel" — จอเล็กวาดถี่เกินไปจะกระตุกและกินทรัพยากรโดยไม่จำเป็น

### อ่านทุกรอบ แต่วาดจอแค่บางรอบ: การ throttle ที่แยกจากการอ่าน

`bmi270_config.h` มีค่าคงที่อีกตัวคือ `BMI270_UI_UPDATE_DIV = 2` — sensor callback อ่านค่าทุก 200 ms เหมือนเดิม
(และเอาไปตัดสิน ALERT ทุกรอบ) แต่จะเรียก `bmi270_view_update_sample()` วาด widget ใหม่แค่ **ทุก 2 ตัวอย่าง**
เท่ากับวาดจอทุก 400 ms เท่านั้น เหตุผลคือ "Update LVGL widgets every N samples to reduce visible flicker" — การอ่าน
เซนเซอร์กับการวาดจอไม่จำเป็นต้องคาบเดียวกันเสมอไป ถ้าอ่านถี่กว่าที่ตาคนแยกความต่างได้ ให้อ่านไปเก็บไว้ (เพื่อ log
หรือ trigger logic อื่น) แต่วาดจอให้ถี่พอสายตาเห็นแค่นั้นพอ

### motion alert ใช้ hysteresis สองเกณฑ์ ไม่ใช่เกณฑ์เดียว

โค้ดมีฟีเจอร์ที่ README ต้นทางไม่ได้พูดถึงเลยคือ **MOTION ALERT** — ถ้า magnitude ของ accel หรือ gyro เกิน threshold
จะเปิด alert label บนจอ แต่ threshold เปิด (`BMI270_ALERT_ACC_ON_G = 1.45g`, `BMI270_ALERT_GYR_ON_DPS = 280`) กับ
threshold ปิด (`BMI270_ALERT_ACC_OFF_G = 1.25g`, `BMI270_ALERT_GYR_OFF_DPS = 220`) เป็นคนละค่ากัน — เรียกว่า
**hysteresis** ถ้าใช้เกณฑ์เดียวและค่าที่อ่านได้แกว่งอยู่รอบ ๆ เกณฑ์นั้นพอดี (เช่น สั่นเบา ๆ รอบ 1.4g) alert จะ
กระพริบ ON/OFF ถี่ยิบ การมีสองเกณฑ์ทำให้ต้องลดลงมาต่ำกว่าเกณฑ์ปิดจริง ๆ ก่อน alert ถึงจะดับ

### หน้าจอแสดง "ขนาดรวม" ของแต่ละเซนเซอร์ ไม่ใช่ 6 บาร์แยกแกน

`bmi270_view.c` สร้าง **บาร์แค่ 2 อัน** (accel กับ gyro) ช่วง 0–350 บวก **chart เส้นเดียวที่มี 2 series** (accel
สีเขียว, gyro สีส้ม) ไม่ใช่ 6 บาร์แยกแกน x/y/z ตามที่ README ต้นทางอธิบาย — ค่าที่แสดงคือขนาดรวม
(`acc_mag_g`, `gyr_mag_dps`) ซึ่งคำนวณจาก √(x²+y²+z²) ของทั้งสามแกน ไม่ใช่ค่าดิบต่อแกน (ค่าต่อแกนยังถูก log ผ่าน
serial แต่ไม่ได้เอาขึ้นจอ)

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะอัตรา poll, ช่วงวัด และ widget บนจอต่างจากที่ README ต้นทางอธิบาย

[`app_sensor/bmi270/bmi270_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_config.h) — ค่าคงที่ตัวจริง:

```c
/* Poll slower to reduce redraw pressure on small HMI panel. */
#define BMI270_SAMPLE_PERIOD_MS           (200U)

/* Update LVGL widgets every N samples to reduce visible flicker. */
#define BMI270_UI_UPDATE_DIV              (2U)

/* mtb_bmi270_config_default() uses ACC=+-2g and GYR=+-2000dps by default. */
#define BMI270_ACC_RANGE_G                (2.0f)
#define BMI270_GYR_RANGE_DPS              (2000.0f)

/* Motion thresholds with hysteresis to avoid ON/OFF toggling noise. */
#define BMI270_ALERT_ACC_ON_G             (1.45f)
#define BMI270_ALERT_ACC_OFF_G            (1.25f)
#define BMI270_ALERT_GYR_ON_DPS           (280.0f)
#define BMI270_ALERT_GYR_OFF_DPS          (220.0f)
```

[`app_ui/bmi270/bmi270_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_ui/bmi270/bmi270_presenter.c) — hysteresis สองเกณฑ์สำหรับ alert:

```c
static bool bmi270_should_alert(const bmi270_sample_t *sample, bool is_alert_active)
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

การอ่านทุกรอบแต่วาดจอแค่บางรอบ:

```c
s_ui_update_div_counter++;
if ((s_ui_update_div_counter >= BMI270_UI_UPDATE_DIV) ||
    (sample.sample_count <= 1U))
{
    bmi270_view_update_sample(&sample);
    s_ui_update_div_counter = 0U;
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/main_example.c) ส่ง I2C handle เข้า `bmi270_presenter_start()` ตรงตามที่ README ต้นทางอธิบาย
- [`app_sensor/bmi270/bmi270_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/app_sensor/bmi270/bmi270_driver.c) — ลำดับ bootstrap (CHIP_ID, soft-reset, อัปโหลด config ~8 KB) ตรงตามที่ README ต้นทางอธิบาย เฉพาะ BMI270 เท่านั้นที่ต้องทำขั้นนี้ (BMI160/BMI088 ไม่ต้อง)
- ดูโฟลเดอร์เต็มที่ [`int_ep02_bmi270_motion_visual/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual)

## จุดที่มักพลาด

- **จำอัตรา poll ผิดเป็น 100 Hz ผ่าน FreeRTOS task** — โค้ดจริง poll ทุก 200 ms ด้วย `lv_timer` เดียวบน LVGL
  thread เท่านั้น
- **คิดว่าการอ่านเซนเซอร์กับการวาดจอต้องคาบเดียวกัน** — โค้ดแยกสองอย่างออกจากกันด้วย `BMI270_UI_UPDATE_DIV`
  อ่านทุกรอบ (เพื่อ log และ alert) แต่วาดจอห่างกว่า
- **ใช้ threshold เดียวสำหรับ alert** — ถ้าไม่มี hysteresis (เกณฑ์เปิด/ปิดต่างกัน) alert จะกระพริบเมื่อค่าที่วัด
  ได้แกว่งอยู่รอบเกณฑ์พอดี
- **คิดว่าจอแสดงค่าต่อแกน x/y/z** — จอแสดงแค่ขนาดรวม (magnitude) ของ accel และ gyro สองบาร์ ไม่ใช่ 6 บาร์แยกแกน

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP02 — BMI270 Motion Visual บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/int_ep02_bmi270_motion_visual.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- บอร์ดวางนิ่งบนโต๊ะ แกนใดควรอ่านได้ประมาณ 1 g
- gyroscope อ่านอะไรเมื่อบอร์ดไม่หมุน
- ทำไมไม่ควรวาดจอทุกครั้งที่อ่านเซนเซอร์ได้

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep02_bmi270_motion_visual) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
