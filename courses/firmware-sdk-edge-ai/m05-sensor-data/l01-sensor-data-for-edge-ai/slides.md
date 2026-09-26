---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
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

# บทเรียน 5.1 — สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI

## จากขาเซ็นเซอร์สู่สตรีมที่พร้อมเข้าโมเดล: คาบเวลาคงที่ ตัวกรอง normalize หน้าต่างข้อมูล และการส่งต่อไปโฮสต์

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 5 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่านเซ็นเซอร์ด้วยคาบเวลาคงที่ เลือก `vTaskDelayUntil` เมื่อต้องการคาบที่แม่นยำ และกำหนดคาบให้เหมาะกับชนิดเซ็นเซอร์
2. คำนวณและเขียนตัวกรอง EMA และฟังก์ชัน normalize ให้ค่าอยู่ในช่วงที่คาดไว้
3. จัดข้อมูลเป็น ring window ขนาด N ตัวอย่าง และบอกได้ว่าหน้าต่างเต็มเมื่อใด

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 4.2 — แล็บ M04](../../m04-rtos/l02-lab/README.md) มาแล้ว
- ใช้บอร์ดจริง: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL)
- บทเรียนเชิงปฏิบัติ — อ่านเซ็นเซอร์ให้เสถียร จัดโครงสร้างข้อมูล และเตรียมทางไป Edge AI / Digital Twin / cloud

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส ฟังก์ชันอย่าง `sensor_bmi270_*`, `sensor_sht40_*`, `sensor_dps368_read`, `sensor_bmm350_read`, `cm55_imu_fusion_bridge_*`, `bitstream_bs_cfg_*` จึงยังไม่มี header ให้เปิดดูหรือ build เอง — อ่านเป็นแนวคิดและลำดับการเรียกใช้

---

## ดูของจริงก่อน — จากขาเซ็นเซอร์สู่สตรีมพร้อม AI

```text
Sensor HW  →  sensor_* Driver  →  sample structs
                 │
                 ├─ (lab) filter / normalize / window
                 ├─ (optional) IMU fusion → quat / euler
                 └─ Bitstream / host / MQTT (โมดูล 6) / Digital Twin
```

> **ขอบเขตที่ซื่อสัตย์กับ SDK ปัจจุบัน**: ไดรเวอร์เซ็นเซอร์และ Bitstream telemetry / IMU fusion มีใน TESA Firmware SDK — **ยังไม่มี** API ระดับแอปสำหรับ Ethos-U / NNLite / DEEPCRAFT inference ในหลักสูตรนี้ บทเรียนนี้สอน *การเตรียมข้อมูลและการไหลของสัญญาณ* ไม่ใช่การเทรนโมเดลบน NPU

> **Key phrase**: Edge AI เริ่มจาก *ข้อมูลสะอาดและจังหวะคงที่* — ไม่ใช่จากโมเดลอย่างเดียว

---

## แนวคิด — รูปแบบร่วมของไดรเวอร์เซ็นเซอร์

```c
cy_rslt_t sensor_<name>_startup(void);
bool      sensor_<name>_read(<name>_sample_t *out_sample);
bool      sensor_<name>_is_ready(void);
```

| เซ็นเซอร์ | ค่าที่อ่านได้ (หน่วย) | บัส |
|---|---|---|
| BMI270 (IMU) | ความเร่ง 3 แกน (m/s²), มุมเชิงมุม 3 แกน (rad/s), อุณหภูมิ (°C) | I²C |
| BMM350 (magnetometer) | สนามแม่เหล็ก 3 แกน (µT), อุณหภูมิ | **I3C** (ไม่ผ่าน `cm55_i2c_manager`) |
| DPS368 | ความดัน (Pa), อุณหภูมิ | I²C |
| SHT40 | อุณหภูมิ (°C), ความชื้น (%RH) | I²C |

BMI270 / SHT40 / DPS368 ใช้บัส I²C ร่วม → ไดรเวอร์ `sensor_*_read` จัดการล็อกภายในแล้ว — อย่าล็อกซ้อนโดยไม่จำเป็น

---

## ตัวอย่างสมบูรณ์ — อ่าน SHT40 และ BMI270

```c
#include "sensor_sht40.h"

sht40_sample_t s;
if (sensor_sht40_startup() == CY_RSLT_SUCCESS && sensor_sht40_is_ready()) {
    if (sensor_sht40_read(&s)) {
        printf("T=%.2f C  RH=%.2f %%\r\n", (double)s.temperature, (double)s.humidity);
    }
}
```

```c
#include "sensor_bmi270.h"

bmi270_sample_t imu;
if (sensor_bmi270_is_ready() && sensor_bmi270_read(&imu)) {
    printf("acc=%.3f %.3f %.3f\r\n", (double)imu.acc_x, (double)imu.acc_y, (double)imu.acc_z);
}
```

จาก [README.md](README.md) หัวข้อ 2.2–2.3 — ทางเลือก non-blocking: `sensor_bmi270_try_read(&imu)`

---

## ตัวอย่างสมบูรณ์ — อ่านด้วยคาบเวลาคงที่ (task pattern)

SDK **ไม่มี** `sensor_*_set_rate_hz` — จังหวะอ่านในแล็บมาจากคาบของ FreeRTOS task (จากโมดูล 4)

```c
void sensor_lab_task(void *arg)
{
    TickType_t last = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(40); /* ~25 Hz */
    bmi270_sample_t s;
    (void)arg;

    for (;;) {
        if (sensor_bmi270_read(&s)) {
            /* filter / window / queue — learner code */
        }
        vTaskDelayUntil(&last, period);
    }
}
```

| เป้าหมาย | แนวทาง |
|---|---|
| อัตราคงที่แม่นยำขึ้น | `vTaskDelayUntil` ดีกว่า `vTaskDelay` |
| เซ็นเซอร์ช้า (SHT40) | คาบยาวกว่า (เช่น 500–1000 ms) |
| IMU | คาบสั้นกว่า (เช่น 20–40 ms) ตามงาน |

---

## ตัวอย่างสมบูรณ์ — ตัวกรอง EMA และ normalize (โค้ดแล็บ)

ยังไม่มีโมดูล filter สำเร็จรูปใน SDK — สอนเป็นโค้ดแล็บ:

```c
/* Exponential moving average — lab-local, not a TESA SDK API */
float ema = 0.0f;
const float alpha = 0.2f;

void on_temp_sample(float t_c)
{
    ema = alpha * t_c + (1.0f - alpha) * ema;
}

/* Simple normalize to roughly [-1, 1] using expected range */
float normalize(float x, float x_min, float x_max)
{
    if (x_max <= x_min) { return 0.0f; }
    float y = (x - x_min) / (x_max - x_min);
    return (2.0f * y) - 1.0f;
}
```

---

## ตัวอย่างสมบูรณ์ — ring window ขนาด N ตัวอย่าง

```c
#define WIN_N 32

typedef struct {
    float ax[WIN_N]; float ay[WIN_N]; float az[WIN_N];
    uint16_t count; uint16_t head;
} imu_window_t;

void imu_window_push(imu_window_t *w, const bmi270_sample_t *s)
{
    w->ax[w->head] = s->acc_x; w->ay[w->head] = s->acc_y; w->az[w->head] = s->acc_z;
    w->head = (uint16_t)((w->head + 1U) % WIN_N);
    if (w->count < WIN_N) { w->count++; }
}

bool imu_window_full(const imu_window_t *w) { return w->count >= WIN_N; }
```

จาก [README.md](README.md) หัวข้อ 4.1 — เมื่อหน้าต่างเต็ม พร้อมส่งเข้า (อนาคต) inference หรือส่งสรุปขึ้นโฮสต์

---

## แนวคิด — บนอุปกรณ์วันนี้: IMU fusion

ใกล้เคียง "smart on device" มากที่สุดใน SDK ปัจจุบันคือ **BMI270 → CM33 BSXLite fusion → quaternion / euler**

```c
if (sensor_bmi270_read(&s)) {
    (void)cm55_imu_fusion_bridge_push_raw_components(
        s.acc_x, s.acc_y, s.acc_z, s.gyr_x, s.gyr_y, s.gyr_z, s.elapsed_ms);
}
if (cm55_imu_fusion_bridge_get_latest_result(&f)) {
    /* f.qw..qz, f.heading, f.pitch, f.roll (radians), f.orientation */
    printf("pitch=%.2f roll=%.2f\r\n", (double)f.pitch, (double)f.roll);
}
```

---

## แนวคิด — ส่งสตรีมไปโฮสต์ / Digital Twin / cloud

| เป้าหมาย | เครื่องมือ |
|---|---|
| Live gauges / deck | Bitstream Studio (Sensor Telemetry) |
| HTML demos | TESAIoT_Hackathon `web-app/` (ex01 SHT40 … ex04 BMI270 …) |
| Cloud publish | เตรียม payload ไว้ในโมดูล 5 → ส่งจริงใน **โมดูล 6 (MQTT)** |

สตรีมไปโฮสต์ถูกควบคุมด้วยคอนฟิกระดับเซ็นเซอร์ (`bitstream_bs_sensor_cfg_t`: `enabled`, `publish_mode`, `sampling_interval_ms`, `publish_interval_ms`) ที่ตั้งค่าผ่าน Bitstream Studio

---

## ฝึกเติม/แล็บ

[แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI](../l02-lab/README.md)

- อ่านเซ็นเซอร์อย่างน้อยหนึ่งตัวด้วยคาบเวลาคงที่บน task ของตัวเอง
- เขียนตัวกรอง EMA และฟังก์ชัน normalize
- จัดข้อมูลเป็น ring window และตรวจว่าหน้าต่างเต็มเมื่อใด
- (ถ้าเวลาเหลือ) ต่อยอดด้วย IMU fusion หรือดู telemetry บน Bitstream Studio

---

## เช็กความเข้าใจ

1. ถ้าต้องการอัตราอ่านคงที่ที่แม่นยำขึ้น บทเรียนแนะนำฟังก์ชันใด
2. โค้ด EMA คือ `ema = alpha * t + (1 - alpha) * ema` ถ้า ema = 20.0, alpha = 0.2 และค่าใหม่ t = 30.0 ค่า ema ใหม่เท่าใด
3. ใน ring window ที่ `WIN_N = 32` ฟังก์ชัน `imu_window_full()` คืนค่า true เมื่อใด

---

## ไปต่อ

- เรียก `sensor_*_startup` / `read` ให้ได้ก่อน แล้วค่อยปรับจังหวะด้วย task
- Filter / normalize / window = **โค้ดแล็บ** ที่ขาดไม่ได้สำหรับ AI prep
- **Fusion** ให้ orientation พร้อมใช้บนอุปกรณ์ · **SENSOR_CFG / Bitstream Studio** เชื่อมสตรีมไปโฮสต์และ Digital Twin
- NPU / DEEPCRAFT = ทิศทางแพลตฟอร์ม — บทเรียนนี้ทำให้ข้อมูลพร้อม ต่อไป **โมดูล 6** ส่งสรุปขึ้น MQTT / cloud

[บทเรียนโมดูล 6 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

---

## แหล่งที่มา

"บทเรียน 5.1 — สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
