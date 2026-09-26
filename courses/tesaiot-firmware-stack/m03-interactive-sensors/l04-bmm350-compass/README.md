---
id: fw-stack.m03.l04
lang: th
title:
  th: "เข็มทิศดิจิทัลจาก BMM350 บน I3C พร้อม calibration"
  en: "Digital compass from the BMM350 over I3C with calibration"
summary:
  th: "สร้างเข็มทิศดิจิทัลจากเซนเซอร์สนามแม่เหล็ก Bosch BMM350 บน I3C พร้อมฟีเจอร์ปรับแต่ง (hard-iron calibration)"
  en: "Digital compass from the BMM350 over I3C with calibration"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l03]
objectives:
  - th: "อ่านสนามแม่เหล็กจาก BMM350 บน I3C แล้วคำนวณทิศเป็นองศา"
    en: "Read the magnetic field from the BMM350 over I3C and compute a heading in degrees"
  - th: "ทำ hard-iron calibration และแสดงว่าทิศแม่นขึ้นหลังปรับ"
    en: "Run hard-iron calibration and show that the heading improves afterwards"
  - th: "อธิบายว่าโลหะและกระแสไฟรอบบอร์ดรบกวนเข็มทิศอย่างไร"
    en: "Explain how metal and currents near the board disturb the compass"
develops:
  - {skill: sys.sensors-actuators, to: 3}
  - {skill: sys.dsp, to: 1}
  - {skill: proto.i2c, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep04_bmm350_compass"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# เข็มทิศดิจิทัลจาก BMM350 บน I3C พร้อม calibration

## เป้าหมาย

1. อ่านสนามแม่เหล็กจาก BMM350 บน I3C แล้วคำนวณทิศเป็นองศา
2. ทำ hard-iron calibration และแสดงว่าทิศแม่นขึ้นหลังปรับ
3. อธิบายว่าโลหะและกระแสไฟรอบบอร์ดรบกวนเข็มทิศอย่างไร

## แนวคิด

### BMM350 คืออะไร และทำไมต้องใช้ I3C

BMM350 เป็น magnetometer 3 แกนรุ่นล่าสุดของ Bosch (2023) noise ต่ำ (1.4 µT RMS) วัดได้ถึง ±2000 µT (ครอบคลุม
สนามแม่เหล็กโลกที่ ~25–65 µT สบาย ๆ) และเป็นตัวแรกในซีรีส์ที่ต่อผ่าน **I3C** แทน I2C — I3C เป็นบัสที่พัฒนาต่อจาก
I2C ให้เร็วกว่า มี dynamic addressing และ in-band interrupt (IBI) แต่ pin ทางไฟฟ้ายังคล้าย I2C มาก master
template เตรียม `i3c_controller_init()` ให้เหมือนที่เตรียม I2C bus ให้กับ DPS368/BMI270/SHT4x — episode นี้จึง
รับ `CYBSP_I3C_CONTROLLER_HW` และ `&CYBSP_I3C_CONTROLLER_context` มาใช้ตรง ๆ โดยไม่ต้อง init เอง

### บั๊กของ vendor library ที่ทำให้จอค้าง — ต้อง patch ก่อน build

นี่คือจุดสำคัญที่สุดของ episode นี้: ไลบรารี `BMM350_SensorAPI` ของ Bosch (v1.10.0 ที่ vendored มาใน master
template) มีบั๊กที่รู้จักแล้วเมื่อใช้งานผ่าน I3C — ใน `bmm350_init()` มีการส่ง soft-reset ไปที่เซนเซอร์ ซึ่งทำให้
BMM350 รีเซ็ตกลับไปโหมด I2C (ค่า default จากโรงงาน) driver จึงพยายามคุยต่อผ่าน I3C กับเซนเซอร์ที่ตอนนี้ไม่ฟัง I3C
แล้ว ทำให้ `bmm350_init()` บล็อกรอ response ไม่มีวันจบ ผลคือ `bmm350_presenter_start()` ไม่ return, LVGL event loop
ไม่เคยเริ่ม และ**จอดำค้างตั้งแต่ boot** อาการนี้สังเกตได้จาก serial log ที่หยุดอยู่แค่ `[MASTER] I3C init OK` โดย
ไม่มีบรรทัด `[BMM350] INIT_OK` ตามมาเลย ต้องรัน patch script (`bmm350_fix.bash`) หรือ comment บรรทัด soft-reset
ด้วย `sed` หนึ่งครั้งหลัง `make getlibs` ก่อน build — master template จงใจไม่ทำ patch อัตโนมัติผ่าน `PREBUILD=`
เพราะ Windows ไม่มี bash มาให้ในตัว และ prebuild แบบนี้ทำให้ build ไม่ deterministic (ถ้ามีคนสั่ง `make getlibs`
ใหม่หลัง patch แล้ว ไฟล์ patch จะถูกเขียนทับกลับไปเป็น pristine โดยไม่รู้ตัว)

### calibration ต้องผ่านสองเงื่อนไข ไม่ใช่แค่รอเวลา

`bmm350_config.h` กำหนด `BMM350_CALIBRATION_SAMPLES = 140` ที่คาบ poll 120 ms (`BMM350_SAMPLE_PERIOD_MS`) รวม
เป็นเวลาประมาณ 16.8 วินาที (คอมเมนต์ในซอร์สระบุตัวเลขนี้ตรง ๆ ไม่ใช่ "15 วินาที" แบบกลม ๆ) แต่การนับตัวอย่างครบยัง
ไม่พอ — โค้ดยังเช็ค `BMM350_CALIBRATION_MIN_SPAN_UT = 20.0f` คือช่วง max−min ของ**ทั้ง X และ Y** ต้องกว้างอย่าง
น้อย 20 µT ด้วย ถ้าวางบอร์ดนิ่งไม่หมุนเลยตลอด 140 ตัวอย่าง ช่วงจะแคบกว่านี้มาก และ calibration จะ**ค้างไม่จบ**
ทั้งที่ครบจำนวนตัวอย่างแล้ว — เหตุผลคือถ้า span แคบ ค่ากึ่งกลางที่คำนวณได้ไม่มีความหมายในฐานะ hard-iron offset

### โค้ดจริงทำ soft-iron scale อย่างง่ายด้วย ไม่ใช่แค่ hard-iron offset ตามที่ README ต้นทางบอก

README ต้นทางบอกว่า "Soft-iron calibration จะไม่ทำในตอนนี้ — ต้อง fit ellipsoid ซึ่งซับซ้อน" แต่คอมเมนต์ใน
`bmm350_config.h` เขียนไว้ตรง ๆ ว่า "Runtime heading calibration (hard-iron + simple soft-iron scale)" — โค้ด
จริงคำนวณทั้ง offset (จุดกึ่งกลาง) **และ** scale ต่อแกนจาก span เฉลี่ยของ X/Y เพื่อดึงวงรีให้กลมขึ้นแบบง่าย ๆ
(ไม่ใช่การ fit ellipsoid เต็มรูปแบบที่ซับซ้อนตามที่ README ต้นทางอ้างถึง แต่ก็ไม่ใช่ "ไม่ทำอะไรเลย" กับความบิดเบี้ยว
ของสเกลเช่นกัน)

### ค่า calibration อยู่ใน RAM เท่านั้น หายเมื่อรีเซ็ตบอร์ด

state ของ calibration เป็นตัวแปร `static` เก็บใน RAM ไม่ได้เขียนลง NVM เหมือน WiFi profile (บทเรียน 2.6) —
`bmm350_reader_init()` เคลียร์ค่า calibration ทุกครั้งที่ถูกเรียก (คือทุกครั้งที่บอร์ด boot ใหม่) ผู้ใช้ต้องกด
Calibrate ใหม่ทุกครั้งหลัง reset ถ้าต้องการให้จำข้ามการ reboot ต้องเพิ่ม store แบบเดียวกับ WiFi profile เอง

### heading คำนวณจาก X/Y เท่านั้น ไม่ชดเชยความเอียง

`atan2f(y, x)` ของค่าที่ผ่าน hard-iron offset และ soft-iron scale แล้วให้มุม heading ตรง ๆ โดยไม่ใช้แกน Z หรือ
ข้อมูลความเอียงจาก accelerometer เลย — สนามแม่เหล็กโลกมีองค์ประกอบแนวดิ่งด้วย การเอียงบอร์ดจึงเปลี่ยนสัดส่วนที่
วัดได้บนแกน X/Y และทำให้ทิศคลาด แม้จะ calibrate ดีแล้วก็ตาม ต้องวางบอร์ดให้ราบขณะอ่านทิศ (การชดเชยความเอียง
tilt-compensated heading ต้องรวมข้อมูลจาก BMI270 บทเรียน 3.2 เข้ามาด้วย ซึ่งเป็นหัวข้อ "ลองแก้" ของ episode นี้)

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why และหัวข้อ BMM350 Vendor Code Fix ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md) ให้ครบก่อน build จริง แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน)

[`app_sensor/bmm350/bmm350_config.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_config.h) — ค่าคงที่ calibration ตัวจริง:

```c
/* Runtime heading calibration (hard-iron + simple soft-iron scale)
 * At default 120 ms sample period and 140 samples = ~16.8 seconds.
 */
#define BMM350_CALIBRATION_SAMPLES             (140U)
#define BMM350_CALIBRATION_MIN_SPAN_UT         (20.0f)

/* Heading axis mapping for board orientation tuning.
 * Signs should be +1 or -1.
 */
#define BMM350_HEADING_SWAP_XY                 (0U)
#define BMM350_HEADING_X_SIGN                  (1)
#define BMM350_HEADING_Y_SIGN                  (1)
#define BMM350_HEADING_OFFSET_DEG              (0.0f)
```

[`app_ui/bmm350/bmm350_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_ui/bmm350/bmm350_presenter.c) — poll ด้วย `lv_timer` เดียวแบบเดียวกับ episode อื่นในโมดูลนี้ พร้อม overlay กันแตะจอระหว่าง calibrate:

```c
void bmm350_presenter_start(I3C_CORE_Type *i3c_hw, cy_stc_i3c_context_t *i3c_context)
{
    bmm350_view_create();
    bmm350_view_set_calibrate_handler(bmm350_calibrate_requested_cb, NULL);

    cy_rslt_t init_rslt = bmm350_reader_init(i3c_hw, i3c_context);
    if (CY_RSLT_SUCCESS != init_rslt)
    {
        bmm350_view_set_init_failed();
        return;
    }

    bmm350_view_set_ready();
    bmm350_update_calibration_ui();

    /* Periodic sensor polling runs in LVGL task context. */
    (void)lv_timer_create(bmm350_poll_sensor_cb, BMM350_SAMPLE_PERIOD_MS, NULL);
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/main_example.c) ส่ง I3C handle เข้า `bmm350_presenter_start()` ตรงตามที่ README ต้นทางอธิบาย
- [`app_sensor/bmm350/bmm350_driver.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/app_sensor/bmm350/bmm350_driver.c) ห่อ Bosch SensorAPI พร้อม inject I3C read/write callback ตรงตามที่ README ต้นทางอธิบาย — นี่คือไฟล์ vendor ที่ต้อง patch ก่อน build (ดูหัวข้อด้านบน)
- ดูโฟลเดอร์เต็มที่ [`int_ep04_bmm350_compass/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass)

## จุดที่มักพลาด

- **build/flash แล้วจอดำค้างตั้งแต่ boot** — สาเหตุเกือบทุกครั้งคือลืม patch บั๊ก I3C soft-reset ของ
  `BMM350_SensorAPI` ให้เช็ค serial log ว่ามีบรรทัด `[BMM350] INIT_OK` ตามหลัง `[MASTER] I3C init OK` หรือไม่
  ถ้าไม่มีแปลว่า `bmm350_init()` ยังบล็อกอยู่ ต้องรัน patch script ก่อน
- **คิดว่า calibrate เสร็จเมื่อครบเวลา/จำนวนตัวอย่าง** — ถ้าไม่หมุนบอร์ดให้ span ของ X และ Y กว้างพอ (≥20 µT)
  calibration จะไม่จบแม้ครบ 140 ตัวอย่างแล้ว ต้องหมุนบอร์ดครบทุกทิศจริง ๆ (figure-8)
- **คิดว่า calibration ยังอยู่หลัง reset บอร์ด** — ค่าอยู่ใน RAM เท่านั้น `bmm350_reader_init()` เคลียร์ทุกครั้งที่
  boot ต้อง calibrate ใหม่เสมอ
- **ลืมว่า heading ไม่ชดเชยความเอียง** — ถ้าบอร์ดไม่ราบ ทิศที่อ่านได้จะคลาดแม้ calibrate ดีแล้ว

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP04 — BMM350 Compass บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/int_ep04_bmm350_compass.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- hard-iron error คืออะไร และแก้ด้วยวิธีใด
- ทำไมต้องหมุนบอร์ดให้ครบทุกทิศตอน calibrate
- I3C ต่างจาก I2C อย่างไรในมุมผู้ใช้งาน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep04_bmm350_compass) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
