---
id: fw-sdk.m05.l01
lang: th
title:
  th: สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI
  en: AI-ready Sensor Streams
summary:
  th: 'จากขาเซ็นเซอร์สู่สตรีมที่พร้อมเข้าโมเดล: คาบเวลาคงที่ ตัวกรอง normalize หน้าต่างข้อมูล และการส่งต่อไปโฮสต์'
  en: 'From sensor pins to model-ready streams: fixed sampling periods, filtering, normalisation, windows and forwarding to a host.'
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m04.l02
objectives:
- th: อ่านเซ็นเซอร์ด้วยคาบเวลาคงที่ เลือก `vTaskDelayUntil` เมื่อต้องการคาบที่แม่นยำ และกำหนดคาบให้เหมาะกับชนิดเซ็นเซอร์
  en: Sample sensors at a fixed period, use `vTaskDelayUntil` when the period must be accurate, and choose a period that suits each sensor.
- th: คำนวณและเขียนตัวกรอง EMA และฟังก์ชัน normalize ให้ค่าอยู่ในช่วงที่คาดไว้
  en: Compute and implement an EMA filter and a normalise function that maps values into the expected range.
- th: จัดข้อมูลเป็น ring window ขนาด N ตัวอย่าง และบอกได้ว่าหน้าต่างเต็มเมื่อใด
  en: Arrange samples in an N-sample ring window and state when the window is full.
develops:
- skill: sys.sensors-actuators
  to: 2
- skill: ai.data-collection
  to: 2
- skill: sys.dsp
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Sensor Data and Edge AI Preparation

**Course 1 · Module 5**  
**Suggested time:** ประมาณ 3.5–4 ชั่วโมง (อ่าน + lab เซ็นเซอร์ / หน้าต่างข้อมูล)  
**Format:** บทเรียนเชิงปฏิบัติ — อ่านเซ็นเซอร์ให้เสถียร จัดโครงสร้างข้อมูล และเตรียมทางไป Edge AI / Digital Twin / cloud

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sensor-ai-prep.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-rtos/l01-freertos-programming/README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `sensor_bmi270_*`, `sensor_sht40_*`, `sensor_dps368_read`, `sensor_bmm350_read`, `cm55_imu_fusion_bridge_*`, `bitstream_bs_cfg_*` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/sensors/02_read_imu.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c) — BMI270 accelerometer / gyroscope (`bmi270_read_accel`, `bmi270_read_gyro`)
> - [`proj_cm33_ns/examples/sensors/03_read_magnetometer.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/03_read_magnetometer.c) — BMM350 และการ calibrate เข็มทิศ (`bmm350_*`)
> - [`proj_cm33_ns/examples/sensors/04_read_environment.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/04_read_environment.c) — SHT40 และ DPS368 (`sht40_read_both`, `dps368_read_both`)
> - [`proj_cm33_ns/examples/sensors/05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c) — task อ่านเซ็นเซอร์เบื้องหลัง ปรับอัตราด้วย `sensor_auto_set_rate` (20–5000 ms; ต่ำกว่า 50 ms อ่านเฉพาะ accelerometer)
> - [`proj_cm55/examples/sensors/01_feed_sensor_hub.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/01_feed_sensor_hub.c) — ส่งค่าที่อ่านบน CM55 เข้า sensor hub ให้ผู้ใช้ปลายทางทุกตัวเห็น
>
> ยังไม่พบตัวเทียบใน SDK สาธารณะ: IMU fusion (`cm55_imu_fusion_bridge_*`) และ SENSOR_CFG ของ Bitstream (`bitstream_bs_cfg_*`)

---

## เป้าหมาย (Learning Outcomes)

### Sensor data handling

1. อ่านข้อมูลเซ็นเซอร์ให้เสถียรขึ้นด้วยเทคนิคเช่น **filtering** และ **normalization** (ในแล็บ)  
2. จัดการ **sampling rate**, จังหวะเวลา และลด noise พื้นฐาน  
3. จัดโครงสร้างข้อมูล (sample / window) เพื่อใช้กับ AI / inference ในขั้นถัดไป  
4. เรียก **Sensor Driver API** ของ TESA Firmware SDK ได้จริง  

### Edge AI applications

1. อธิบายการประยุกต์ SDK กับงาน Edge AI (gesture / activity / event) ในระดับ **pipeline ข้อมูล**  
2. เตรียมข้อมูลเพื่อส่งต่อไปยัง **Digital Twin**, inference engine หรือ cloud  
3. ทดสอบบนอุปกรณ์จริง และดูผลบนโฮสต์เมื่อมี telemetry  

> **ขอบเขตที่ซื่อสัตย์กับ SDK ปัจจุบัน**  
> ไดรเวอร์เซ็นเซอร์และ Bitstream telemetry / IMU fusion มีใน TESA Firmware SDK  
> **ยังไม่มี** API ระดับแอปสำหรับ Ethos-U / NNLite / DEEPCRAFT inference ในหลักสูตรนี้ — M05 สอน *การเตรียมข้อมูลและการไหลของสัญญาณ* ไม่ใช่การเทรนโมเดลบน NPU  
> Snippet ด้านล่างอ้างชื่อฟังก์ชันจาก TESA Firmware SDK — ใช้ร่วมกับโปรเจกต์ตัวอย่างหรือตัวอย่างบน Developer Hub

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่าง Domain **Sensors** / Embedded |
| [M03 — Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | I²C lock, UART log |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | task คาบคงที่สำหรับ sampling |
| [M01 — Architecture](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) | โดเมน M55+Ethos / M33+NNLite (แผนที่ชิป) |
| [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) | เวิร์กโฟลว์ ML ของ Infineon (ภาพรวม) |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | ดู telemetry / twin บนโฮสต์ |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX + `web-app/` demos (SHT40, BMI270, …) |
| [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) | Ethos-U55 / NNLite ในระดับชิป |

---

## 1. From Raw Pins to AI-Ready Streams

```text
Sensor HW  →  sensor_* Driver  →  sample structs
                 │
                 ├─ (lab) filter / normalize / window
                 ├─ (optional) IMU fusion → quat / euler
                 └─ Bitstream / host / MQTT (M06) / Digital Twin
```

| ชั้น | บทบาทใน M05 |
|---|---|
| **Driver** | `sensor_*_startup` / `read` / `is_ready` |
| **Timing** | FreeRTOS task + `vTaskDelayUntil` หรือ SENSOR_CFG interval |
| **Conditioning** | filter / normalize ในโค้ดแล็บ (ยังไม่มีโมดูล filter สำเร็จรูปใน SDK) |
| **Features / window** | บัฟเฟอร์หน้าต่าง N ตัวอย่าง — เตรียมเข้าโมเดล |
| **Host / twin** | Bitstream Studio · Hackathon web-app |
| **NPU / DEEPCRAFT** | แผนที่สถาปัตยกรรม + เอกสาร Infineon — ไม่เรียก inference API ในแล็บนี้ |

> **Key phrase**  
> Edge AI เริ่มจาก *ข้อมูลสะอาดและจังหวะคงที่* — ไม่ใช่จากโมเดลอย่างเดียว

---

## 2. Sensor Drivers in TESA Firmware SDK

รูปแบบร่วมของไดรเวอร์หลัก:

```c
cy_rslt_t sensor_<name>_startup(void);
bool      sensor_<name>_read(<name>_sample_t *out_sample);
bool      sensor_<name>_is_ready(void);
```

### 2.1 Sample structures (units)

```c
typedef struct {
    float acc_x, acc_y, acc_z;   /* m/s^2 */
    float gyr_x, gyr_y, gyr_z;   /* rad/s */
    float temperature;           /* °C */
    int32_t elapsed_ms;
} bmi270_sample_t;

typedef struct {
    float mag_x, mag_y, mag_z;   /* µT */
    float temperature;
} bmm350_sample_t;

typedef struct {
    float pressure;              /* Pa */
    float temperature;
} dps368_sample_t;

typedef struct {
    float temperature;           /* °C */
    float humidity;              /* %RH */
} sht40_sample_t;
```

### 2.2 SHT40 (temperature / humidity)

```c
#include "sensor_sht40.h"

sht40_sample_t s;
if (sensor_sht40_startup() == CY_RSLT_SUCCESS && sensor_sht40_is_ready()) {
    if (sensor_sht40_read(&s)) {
        printf("T=%.2f C  RH=%.2f %%\r\n",
               (double)s.temperature, (double)s.humidity);
    }
}
```

### 2.3 BMI270 (IMU — สำคัญต่อ motion / orientation)

```c
#include "sensor_bmi270.h"

bmi270_sample_t imu;
if (sensor_bmi270_is_ready() && sensor_bmi270_read(&imu)) {
    printf("acc=%.3f %.3f %.3f\r\n",
           (double)imu.acc_x, (double)imu.acc_y, (double)imu.acc_z);
}
```

ทางเลือก non-blocking เมื่อบัสไม่ว่าง: `sensor_bmi270_try_read(&imu)`

### 2.4 DPS368 and BMM350

```c
#include "sensor_dps368.h"
#include "sensor_bmm350.h"

dps368_sample_t baro;
bmm350_sample_t mag;
(void)sensor_dps368_read(&baro);  /* pressure Pa */
(void)sensor_bmm350_read(&mag);   /* mag_x/y/z */
```

> **BMM350** ใช้เส้นทาง **I3C** — ไม่ผ่าน `cm55_i2c_manager`  
> **BMI270 / SHT40 / DPS368** ใช้บัส I²C ร่วม → ล็อกด้วย `cm55_i2c_manager_i2c_lock` / `unlock` เมื่อเขียนธุรกรรมเอง

```c
cm55_i2c_manager_i2c_lock();
/* custom transfer if needed */
cm55_i2c_manager_i2c_unlock();
```

ไดรเวอร์ `sensor_*_read` โดยทั่วไปจัดการล็อกภายในแล้ว — อย่าล็อกซ้อนโดยไม่จำเป็น

---

## 3. Sampling Rate, Timing, and Noise

### 3.1 Fixed-rate task (lab pattern)

SDK **ไม่มี** `sensor_*_set_rate_hz` ในไดรเวอร์ปัจจุบัน  
จังหวะอ่านในแล็บ = คาบของ FreeRTOS task (จาก M04):

```c
#include "FreeRTOS.h"
#include "task.h"
#include "sensor_bmi270.h"

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
| อัตราคงที่ | `vTaskDelayUntil` ดีกว่า `vTaskDelay` เมื่อต้องการคาบแม่นยำขึ้น |
| เซ็นเซอร์ช้า (SHT40) | คาบยาวกว่า (เช่น 500–1000 ms) |
| IMU | คาบสั้นกว่า (เช่น 20–40 ms) ตามงาน |

### 3.2 Filtering and normalization (lab-local)

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
    if (x_max <= x_min) {
        return 0.0f;
    }
    float y = (x - x_min) / (x_max - x_min);
    return (2.0f * y) - 1.0f;
}
```

เทคนิคอื่นที่พบบ่อย: median ของหน้าต่างสั้น, ตัด outlier, ลบค่า offset ของ accelerometer เมื่อวางนิ่ง

### 3.3 Time synchronization (practical)

| แนวทาง | ใช้เมื่อ |
|---|---|
| `elapsed_ms` ใน `bmi270_sample_t` | อ้างอิงเวลาสัมพัทธ์ของตัวอย่าง IMU |
| tick ของ FreeRTOS | ประทับเวลาใน task แล็บ |
| คาบ publish ของ Bitstream | ให้โฮสต์เห็นสตรีมสม่ำเสมอ |

ยังไม่ลงรายละเอียด NTP/PTP ใน M05 — โฟกัสให้ตัวอย่างมี **จังหวะและหน่วยชัด**

---

## 4. Structuring Data for AI / Inference

โมเดล Edge มักต้องการ **หน้าต่างเวลา** ของเวกเตอร์ฟีเจอร์ ไม่ใช่ค่าเดี่ยว

### 4.1 Ring window (lab pattern)

```c
#define WIN_N 32

typedef struct {
    float ax[WIN_N];
    float ay[WIN_N];
    float az[WIN_N];
    uint16_t count;
    uint16_t head;
} imu_window_t;

void imu_window_push(imu_window_t *w, const bmi270_sample_t *s)
{
    w->ax[w->head] = s->acc_x;
    w->ay[w->head] = s->acc_y;
    w->az[w->head] = s->acc_z;
    w->head = (uint16_t)((w->head + 1U) % WIN_N);
    if (w->count < WIN_N) {
        w->count++;
    }
}

bool imu_window_full(const imu_window_t *w)
{
    return w->count >= WIN_N;
}
```

เมื่อหน้าต่างเต็ม → พร้อมส่งเข้า (อนาคต) inference / หรือส่งสรุปขึ้นโฮสต์

### 4.2 Feature ideas (conceptual)

| งาน | ตัวอย่างฟีเจอร์จากหน้าต่าง |
|---|---|
| Activity / motion intensity | ค่าเฉลี่ย \|a\|, variance |
| Orientation change | delta ของ pitch/roll จาก fusion |
| Environment event | เกณฑ์อุณหภูมิ/ความชื้นหลัง filter |
| Gesture (แนวคิด) | รูปแบบแกน accel ในหน้าต่างสั้น |

การจำแนก gesture จริงด้วย NPU = ขั้นถัดไปนอกขอบเขต API ปัจจุบัน — M05 ทำให้ *อินพุตพร้อม*

---

## 5. On-Device Intelligence Today: IMU Fusion

ใกล้เคียง “smart on device” มากที่สุดใน SDK ปัจจุบันคือ **BMI270 → CM33 BSXLite fusion → quaternion / euler**

```c
#include "cm55_imu_fusion_bridge.h"
#include "sensor_bmi270.h"

bmi270_sample_t s;
ipc_fusion_result_t f;

if (sensor_bmi270_read(&s)) {
    (void)cm55_imu_fusion_bridge_push_raw_components(
        s.acc_x, s.acc_y, s.acc_z,
        s.gyr_x, s.gyr_y, s.gyr_z,
        s.elapsed_ms);
}

if (cm55_imu_fusion_bridge_get_latest_result(&f)) {
    /* f.qw..qz, f.heading, f.pitch, f.roll (radians), f.orientation */
    printf("pitch=%.2f roll=%.2f\r\n",
           (double)f.pitch, (double)f.roll);
}
```

```c
typedef struct {
    float qw, qx, qy, qz;
    float heading, pitch, roll; /* radians */
    uint8_t orientation;        /* discrete pose; 0 = unknown */
    uint8_t reserved[3];
} ipc_fusion_result_t;
```

เชื่อมกับแผนที่ M01: การประมวลผลหนัก/ฟิวชันอาจอยู่คนละโดเมนกับ always-on — ผู้เรียนโฟกัส API บน CM55 ที่ push/get ผล

---

## 6. Preparing Streams for Host, Twin, and Cloud

### 6.1 Bitstream SENSOR_CFG (firmware view)

สตรีมไปโฮสต์ถูกควบคุมด้วยคอนฟิกระดับเซ็นเซอร์ (interval / mode / mask):

```c
typedef struct {
    uint8_t  enabled;
    uint8_t  publish_mode;           /* 0=periodic, 1=on_change, 2=hybrid */
    uint8_t  mask;
    uint16_t sampling_interval_ms;
    uint16_t delta_x100;
    uint16_t min_publish_interval_ms;
    uint16_t publish_interval_ms;
} bitstream_bs_sensor_cfg_t;
```

อ่านค่าปัจจุบัน (เมื่อโปรเจกต์เปิด Bitstream):

```c
#include "bitstream_bs_cfg.h"
#include "bitstream_bs_wire.h"

const bitstream_bs_sensor_cfg_t *cfg =
    bitstream_bs_cfg_get_by_source(BITSTREAM_SENSOR_SOURCE_ID_SHT40);
/* cfg->enabled, sampling_interval_ms, publish_interval_ms, publish_mode, mask */
```

| Sensor ID (แนวคิด) | ใช้กับ |
|---|---|
| BMI270 | IMU (+ mask สำหรับ ACC/GYR/TMP/EULER/QUAT ตามเฟิร์มแวร์) |
| BMM350 | แมกนีโตมิเตอร์ |
| SHT40 | อุณหภูมิ/ความชื้น |
| DPS368 | ความดัน |

บนโฮสต์: ตั้งค่าผ่าน **Bitstream Studio** (Sensor Telemetry) หรือดูตัวอย่าง HTML ใน [TESAIoT_Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon)

### 6.2 Digital Twin and dashboards

| เป้าหมาย | เครื่องมือ |
|---|---|
| Live gauges / deck | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| HTML demos | Hackathon `ex01` SHT40 … `ex04` BMI270 … |
| Cloud publish | เตรียม payload ไว้ใน M05 → ส่งจริงใน **M06 (MQTT)** |

### 6.3 Edge AI silicon vs course labs

| ชิ้นส่วน (จาก M01) | ใน M05 |
|---|---|
| Ethos-U55 / NNLite | รู้ว่ามีบนชิป — ยังไม่มี wrapper inference ใน SDK แล็บ |
| DEEPCRAFT™ | เวิร์กโฟลว์โมเดลของ Infineon — อ่านภาพรวมได้จาก [DEEPCRAFT AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) |
| งานแล็บของคุณ | sample → filter → window → (fusion / telemetry) |

---

## 7. Application Patterns (Gesture / Activity / Events)

| รูปแบบผลิตภัณฑ์ | สิ่งที่ทำได้ใน M05 ด้วย SDK ปัจจุบัน |
|---|---|
| **Event / condition** | เกณฑ์บนค่า filter แล้ว (เช่น อุณหภูมิเกิน) → LED / UART / คิว |
| **Activity monitoring (แนวคิด)** | variance ของ accel ในหน้าต่าง |
| **Orientation / pose** | `ipc_fusion_result_t` |
| **Gesture classifier** | เตรียมหน้าต่างฟีเจอร์ — โมเดล NPU เป็นขั้นถัดไป |

ตัวอย่าง event ง่าย ๆ:

```c
if (ema > 30.0f) {
    led_controller_set(LED_RED, true);
    printf("TEMP_EVENT high\r\n");
}
```

---

## 8. Module Summary

1. เรียก **`sensor_*_startup` / `read`** ให้ได้ก่อน แล้วค่อยปรับจังหวะด้วย task  
2. Filter / normalize / window = **โค้ดแล็บ** ที่ขาดไม่ได้สำหรับ AI prep  
3. **Fusion** ให้ orientation พร้อมใช้บนอุปกรณ์  
4. **SENSOR_CFG / Bitstream Studio** เชื่อมสตรีมไปโฮสต์และ Digital Twin  
5. NPU / DEEPCRAFT = ทิศทางแพลตฟอร์ม — M05 ทำให้ข้อมูลพร้อม  
6. ต่อไป **M06** ส่งสรุปขึ้น MQTT / cloud  

### Next Steps

1. ทำแบบฝึก: [Lab](../l02-lab/README.md)  
2. เก็บแผ่นสรุป: [Cheatsheet](resources/sensor-ai-prep.md)  
3. เมื่อพร้อม ไปต่อ **M06 — MQTT and MQTTs for Cloud Communication** ([บทเรียน M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md))

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — Domain Sensors  
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `web-app/` sensor demos  

### Platform / ML overview

4. [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)  
5. [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)  
6. [Arm Ethos-U55](https://developer.arm.com/Processors/Ethos-U55)  

### Prior modules

7. [M03 — GPIO and Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)  
8. [M04 — RTOS Programming](../../m04-rtos/l01-freertos-programming/README.md)  
9. [M01 — MCU Architecture](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md)  

### FreeRTOS timing

10. [vTaskDelayUntil](https://www.freertos.org/vtaskdelayuntil.html)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sensor-ai-prep.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-rtos/l01-freertos-programming/README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [EP01 — DPS368 Monitor](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) — อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL
- [EP02 — BMI270 Motion Visual](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual) — แสดงค่าการเคลื่อนไหว 6 แกนจากเซนเซอร์ Bosch BMI270 (accelerometer + gyroscope) บนจอ LVGL แบบเรียลไทม์
- [EP03 — SHT40 Indicator](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator) — วัดความชื้นสัมพัทธ์และอุณหภูมิด้วยเซนเซอร์ Sensirion SHT4x บน I2C แล้วแสดงผลเป็นตัวบ่งชี้บนจอ LVGL
- [EP04 — BMM350 Compass](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass) — สร้างเข็มทิศดิจิทัลจากเซนเซอร์สนามแม่เหล็ก Bosch BMM350 บน I3C พร้อมฟีเจอร์ปรับแต่ง (hard-iron calibration)
- [EP06 — Digital Mic Probe](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) — เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL
