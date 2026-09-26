---
id: fw-stack.m03.l01
lang: th
title:
  th: "อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C"
  en: "Pressure and temperature from the DPS368 over I2C"
summary:
  th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL"
  en: "Pressure and temperature from the DPS368 over I2C"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ"
    en: "Read pressure and temperature from the DPS368 over I2C and show them on screen"
  - th: "อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode"
    en: "Explain the driver → reader → presenter → view layering of the episode"
  - th: "ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง"
    en: "Check the reading against a local reference pressure and explain the difference"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep01_dps368_monitor"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# อ่านความดันและอุณหภูมิจาก DPS368 ผ่าน I2C

## เป้าหมาย

1. อ่านค่าความดันบรรยากาศและอุณหภูมิจาก DPS368 ผ่าน I2C แล้วแสดงบนจอ
2. อธิบายการแบ่งชั้น driver → reader → presenter → view ของ episode
3. ตรวจค่าที่อ่านได้กับค่าความดันอ้างอิงของพื้นที่ และอธิบายส่วนต่าง

## แนวคิด

### DPS368 คืออะไร และตัวเลขในสเปกหมายถึงอะไร

DPS368 เป็นเซนเซอร์ความดันบรรยากาศ (barometer) แบบ capacitive MEMS ของ Infineon วัดความดันได้ในช่วง 300–1200 hPa
ด้วยความละเอียดระดับ ±0.002 hPa (ประมาณการเปลี่ยนระดับความสูง 2 ซม.) และวัดอุณหภูมิร่วมด้วยในตัวเดียวกัน เพราะค่า
ความดันต้องชดเชยด้วยอุณหภูมิภายในเซนเซอร์เอง (การคำนวณนี้ทำอยู่ในไลบรารีของ Infineon ให้แล้ว ไม่ต้องเขียนสูตรเอง)

### สี่ชั้นของโค้ด: driver → reader → presenter → view

โค้ดแบ่งงานเป็นสี่ชั้นตามชื่อโฟลเดอร์ `app_sensor/dps368/` มี `dps368_driver` (คุยกับเซนเซอร์ผ่านไลบรารี
`xensiv_dps3xx` ของ Infineon โดยตรง) และ `dps368_reader` (ห่อ driver ให้เป็น `dps368_reader_poll()` ฟังก์ชันเดียว
คืน `bool` บอกว่ามี sample ใหม่หรือไม่) ส่วน `app_ui/dps368/` มี `dps368_presenter` (ผูก timer + ตัดสินใจว่าจะ
อัปเดตจอเมื่อไร) และ `dps368_view` (สร้างและอัปเดต label ล้วน ๆ ไม่มี gauge หรือ arc ตามที่บางครั้งอาจถูกเข้าใจผิด)
แต่ละชั้นรู้จักแค่ชั้นที่อยู่ติดกัน — `dps368_view` ไม่รู้จัก I2C เลย และ `dps368_driver` ไม่รู้จัก LVGL เลย

### สัญญาณเข้าเซนเซอร์ผ่าน bus ที่ master เตรียมไว้แล้ว พร้อม fallback ที่อยู่ I2C

`main_example.c` ส่ง `&sensor_i2c_controller_hal_obj` (HAL handle ที่ master template เปิดไว้แล้วตั้งแต่ก่อน
`example_main()` ถูกเรียก — ดูบทเรียน 1.1) เข้าไปให้ `dps368_presenter_start()` โดยตรง ไม่ต้อง `cyhal_i2c_init()`
ซ้ำ ภายใน `app_dps368_service_init()` ลองต่อที่ address เริ่มต้น (`XENSIV_DPS3XX_I2C_ADDR_DEFAULT` = 0x77) ก่อน
ถ้าไม่ตอบจะลองที่อยู่สำรอง (`XENSIV_DPS3XX_I2C_ADDR_ALT` = 0x76 ซึ่งกำหนดโดยขา SDO ของเซนเซอร์) — โค้ดจึงใช้งานได้
กับบอร์ดที่ strap ขา SDO ไว้คนละแบบโดยไม่ต้องแก้โค้ด

### วิธี poll จริง: `lv_timer` เดียวบน LVGL thread ไม่ใช่ FreeRTOS task แยก

`dps368_presenter_start()` เรียก `lv_timer_create(dps368_poll_sensor_cb, DPS368_SAMPLE_PERIOD_MS, NULL)` โดย
`DPS368_SAMPLE_PERIOD_MS = 1000` (วินาทีละครั้ง) — `dps368_poll_sensor_cb()` รันอยู่บน **LVGL thread เดียวกัน**
กับส่วนที่วาดจอ ไม่ใช่ FreeRTOS task แยกต่างหากที่ส่งข้อมูลผ่านคิวแล้วกลับเข้า LVGL ด้วย `lv_async_call()`
ตามที่บางครั้งอาจเข้าใจผิด การอ่าน I2C (`dps368_driver_read_hpa_c()`) จึงเป็น**การเรียกแบบ blocking ตรง ๆ ภายใน
callback ของ timer** เพราะ transaction I2C หนึ่งครั้งเร็วพอที่จะไม่ทำให้จอกระตุก ที่ 1 ครั้ง/วินาที episode นี้จึง
เลือกความเรียบง่ายเหนือการแยก thread เพราะเซนเซอร์ตัวเดียวไม่คุ้มความซับซ้อนของ task+queue

### แยก "ยังไม่มีข้อมูลใหม่" ออกจาก "error จริง"

`dps368_reader_poll()` เช็ค return code ของ driver พิเศษกรณีเดียวคือ `XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY` — ถ้า
เจอค่านี้จะคืน `false` แต่ **ไม่ถือเป็น error** (แค่ยังไม่ถึงรอบ conversion ถัดไปของเซนเซอร์) ส่วน error code อื่น
ถือเป็นปัญหาจริงที่ presenter จะเอาไปแสดงบน status label เป็นข้อความ `"Sensor: read error (0x........)"` การแยก
สองกรณีนี้ออกจากกันสำคัญ เพราะถ้าถือว่า "ยังไม่พร้อม" เป็น error ทุกครั้ง จอจะกระพริบข้อความ error ทุกวินาทีที่ยัง
ไม่ถึงรอบอ่านจริง

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะกลไก poll จริงต่างจากที่ README ต้นทางอธิบาย (ไม่มี FreeRTOS task/queue แยก)

[`app_ui/dps368/dps368_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_ui/dps368/dps368_presenter.c) — `lv_timer` เดียวที่ poll แล้วอัปเดตจอ:

```c
static void dps368_poll_sensor_cb(lv_timer_t *timer)
{
    (void)timer;

    dps368_sample_t sample;
    bool has_new_sample = dps368_reader_poll(&sample);

    if (has_new_sample)
    {
        dps368_view_update_sample(&sample);
        /* ... */
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

[`app_sensor/dps368/dps368_reader.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/dps368/dps368_reader.c) — แยก "ยังไม่พร้อม" ออกจาก error จริง:

```c
if (CY_RSLT_SUCCESS == rslt)
{
    s_last_sample.pressure_hpa = pressure_hpa;
    s_last_sample.temperature_c = temperature_c;
    s_last_sample.sample_count++;
    if (NULL != out_sample) { *out_sample = s_last_sample; }
    return true;
}

/* At low sample rate, polling can happen before conversion is ready. */
if (rslt == XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY)
{
    s_last_error = CY_RSLT_SUCCESS;
    return false;
}

s_last_error = rslt;
return false;
```

[`app_sensor/app_dps368_service.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/app_sensor/app_dps368_service.c) — ลองที่อยู่ I2C หลักก่อน แล้วค่อย fallback ไปที่อยู่สำรอง:

```c
rslt = mtb_xensiv_dps3xx_init_i2c(&s_dps368, i2c_bus, XENSIV_DPS3XX_I2C_ADDR_DEFAULT);
if (CY_RSLT_SUCCESS != rslt)
{
    rslt = mtb_xensiv_dps3xx_init_i2c(&s_dps368, i2c_bus, XENSIV_DPS3XX_I2C_ADDR_ALT);
    /* ... */
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/main_example.c) ส่ง handle I2C ที่ master เตรียมไว้เข้า `dps368_presenter_start()` ตรงตามที่ README ต้นทางอธิบาย
- ไฟล์ `basic_label_legacy.*` และ `dps368_monitor_legacy.*` เป็นโค้ดเวอร์ชันก่อน refactor ไว้เทียบ ไม่ใช่ส่วนที่ทำงานจริงของ episode
- ดูโฟลเดอร์เต็มที่ [`int_ep01_dps368_monitor/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor)

## จุดที่มักพลาด

- **คิดว่ามี FreeRTOS task แยกต่างหาก poll เซนเซอร์ทุก 100 ms** — โค้ดจริงใช้ `lv_timer` เดียวบน LVGL thread ที่
  1000 ms และอ่าน I2C แบบ blocking ตรง ๆ ในนั้นเลย ไม่มี queue หรือ `lv_async_call()`
  แนวคิดนี้ใช้ได้เพราะมีเซนเซอร์เดียวและ I2C transaction สั้น — ถ้าเพิ่มเซนเซอร์ที่อ่านช้าลงในอนาคต ค่อยพิจารณาแยก
  task จริง (ดู EP07 — SensorHub Final)
- **ถือว่า `XENSIV_DPS3XX_RSLT_ERR_DATA_NOT_READY` เป็น error** — ต้องแยกจาก error code อื่นเสมอ เพราะเป็นแค่
  สัญญาณว่ายังไม่ถึงรอบ conversion ถัดไป ไม่ใช่ความล้มเหลว
  ถ้าปฏิบัติเหมือน error ทุกครั้งจะได้ log/สถานะ error ที่ไม่ตรงความจริง
- **ลืมว่าเซนเซอร์มีสองที่อยู่ I2C ที่เป็นไปได้** — ถ้า hard-code แค่ `0x77` โค้ดจะใช้ไม่ได้กับบอร์ดที่ strap ขา
  SDO ต่างไป ต้องลอง fallback เสมอแบบที่ `app_dps368_service_init()` ทำ

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP01 — DPS368 Monitor บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/int_ep01_dps368_monitor.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ชั้น presenter ทำอะไรที่ view ไม่ทำ
- ความดันควรเปลี่ยนอย่างไรเมื่อยกบอร์ดขึ้นสูงหนึ่งชั้นตึก
- ถ้าเซนเซอร์ตอบ I2C ไม่ได้ ข้อความผิดพลาดควรขึ้นที่ชั้นใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep01_dps368_monitor) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
