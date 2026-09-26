---
id: fw-sdk.m05.l01
lang: en
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
slides: slides.md
source_sha256: dc51d1759435dfa1622efafb012f226d58e9038fb743f688ae7bb07362da43b7
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Sensor Data and Edge AI Preparation

**Course 1 · Module 5**
**Suggested time:** about 3.5–4 hours (reading + a sensor / data-window lab)
**Format:** a hands-on lesson — reading sensors reliably, structuring data, and preparing the path to Edge AI / Digital Twin / cloud

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sensor-ai-prep.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-rtos/l01-freertos-programming/README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `sensor_bmi270_*`, `sensor_sht40_*`, `sensor_dps368_read`, `sensor_bmm350_read`, `cm55_imu_fusion_bridge_*` and `bitstream_bs_cfg_*` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. Examples already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/sensors/02_read_imu.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c) — the BMI270 accelerometer / gyroscope (`bmi270_read_accel`, `bmi270_read_gyro`)
> - [`proj_cm33_ns/examples/sensors/03_read_magnetometer.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/03_read_magnetometer.c) — the BMM350 and compass calibration (`bmm350_*`)
> - [`proj_cm33_ns/examples/sensors/04_read_environment.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/04_read_environment.c) — the SHT40 and DPS368 (`sht40_read_both`, `dps368_read_both`)
> - [`proj_cm33_ns/examples/sensors/05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c) — a background sensor-reading task, with the rate adjusted through `sensor_auto_set_rate` (20–5000 ms; below 50 ms it reads only the accelerometer)
> - [`proj_cm55/examples/sensors/01_feed_sensor_hub.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/01_feed_sensor_hub.c) — sending values read on the CM55 into a sensor hub, visible to every downstream consumer
>
> No equivalent found yet in the public SDK: IMU fusion (`cm55_imu_fusion_bridge_*`) and Bitstream's SENSOR_CFG (`bitstream_bs_cfg_*`)

---

## Objectives (Learning Outcomes)

### Sensor data handling

1. Read sensor data more reliably using techniques such as **filtering** and **normalization** (in the lab)
2. Manage the **sampling rate**, timing, and basic noise reduction
3. Structure data (sample / window) for use with AI / inference in the next step
4. Genuinely call the TESA Firmware SDK's **Sensor Driver API**

### Edge AI applications

1. Explain applying the SDK to Edge AI work (gesture / activity / event) at the **data-pipeline** level
2. Prepare data to pass on to a **Digital Twin**, an inference engine, or the cloud
3. Test on real hardware, and watch the result on a host when telemetry exists

> **A scope that is honest about the current SDK**
> Sensor drivers and Bitstream telemetry / IMU fusion exist in the TESA Firmware SDK.
> There is **not yet** an app-level API for Ethos-U / NNLite / DEEPCRAFT inference in this course — M05 teaches *data preparation and the signal flow*, not training a model on the NPU.
> The snippets below reference function names from the TESA Firmware SDK — use them together with an example project, or an example on the Developer Hub.

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | The **Sensors** / Embedded domain examples |
| [M03 — Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | The I²C lock, UART logging |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | A fixed-period task for sampling |
| [M01 — Architecture](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) | The M55+Ethos / M33+NNLite domains (the chip map) |
| [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) | Infineon's ML workflow (overview) |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Watching telemetry / a twin on the host |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX + `web-app/` demos (SHT40, BMI270, …) |
| [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) | Ethos-U55 / NNLite at the chip level |

---

## 1. From Raw Pins to AI-Ready Streams

```text
Sensor HW  →  sensor_* Driver  →  sample structs
                 │
                 ├─ (lab) filter / normalize / window
                 ├─ (optional) IMU fusion → quat / euler
                 └─ Bitstream / host / MQTT (M06) / Digital Twin
```

| Layer | Role in M05 |
|---|---|
| **Driver** | `sensor_*_startup` / `read` / `is_ready` |
| **Timing** | A FreeRTOS task + `vTaskDelayUntil`, or a SENSOR_CFG interval |
| **Conditioning** | Filtering / normalising in lab code (the SDK has no ready-made filter module yet) |
| **Features / window** | An N-sample window buffer — ready to feed into a model |
| **Host / twin** | Bitstream Studio · the Hackathon web-app |
| **NPU / DEEPCRAFT** | An architecture map + Infineon documentation — this lab does not call an inference API |

> **Key phrase**
> Edge AI starts from *clean data at a steady rhythm* — not from the model alone.

---

## 2. Sensor Drivers in TESA Firmware SDK

The common pattern of the main drivers:

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

### 2.3 BMI270 (IMU — important for motion / orientation)

```c
#include "sensor_bmi270.h"

bmi270_sample_t imu;
if (sensor_bmi270_is_ready() && sensor_bmi270_read(&imu)) {
    printf("acc=%.3f %.3f %.3f\r\n",
           (double)imu.acc_x, (double)imu.acc_y, (double)imu.acc_z);
}
```

A non-blocking alternative when the bus is busy: `sensor_bmi270_try_read(&imu)`

### 2.4 DPS368 and BMM350

```c
#include "sensor_dps368.h"
#include "sensor_bmm350.h"

dps368_sample_t baro;
bmm350_sample_t mag;
(void)sensor_dps368_read(&baro);  /* pressure Pa */
(void)sensor_bmm350_read(&mag);   /* mag_x/y/z */
```

> The **BMM350** uses the **I3C** path — it does not go through `cm55_i2c_manager`
> **BMI270 / SHT40 / DPS368** share the I²C bus → lock it with `cm55_i2c_manager_i2c_lock` / `unlock` when writing your own transaction

```c
cm55_i2c_manager_i2c_lock();
/* custom transfer if needed */
cm55_i2c_manager_i2c_unlock();
```

The `sensor_*_read` drivers generally already handle locking internally — don't lock on top of that unnecessarily.

---

## 3. Sampling Rate, Timing, and Noise

### 3.1 Fixed-rate task (lab pattern)

The SDK's current drivers have **no** `sensor_*_set_rate_hz`.
The read rhythm in the lab = the period of a FreeRTOS task (from M04):

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

| Goal | Approach |
|---|---|
| A fixed rate | `vTaskDelayUntil` is better than `vTaskDelay` when the period needs to be more accurate |
| A slow sensor (SHT40) | A longer period (e.g. 500–1000 ms) |
| An IMU | A shorter period (e.g. 20–40 ms), depending on the task |

### 3.2 Filtering and normalization (lab-local)

There is no ready-made filter module in the SDK yet — this is taught as lab code:

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

Other common techniques: a median over a short window, cutting outliers, subtracting the accelerometer's offset when lying still

### 3.3 Time synchronization (practical)

| Approach | Use when |
|---|---|
| `elapsed_ms` in `bmi270_sample_t` | Referencing an IMU sample's relative time |
| The FreeRTOS tick | Timestamping inside a lab task |
| Bitstream's publish period | Giving the host a steady stream |

M05 does not go into NTP/PTP detail yet — the focus is making the example have a **clear rhythm and clear units**.

---

## 4. Structuring Data for AI / Inference

An edge model usually needs a **time window** of feature vectors, not a single value.

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

Once the window is full → ready to send to (future) inference, or to send a summary up to the host

### 4.2 Feature ideas (conceptual)

| Task | Example features from the window |
|---|---|
| Activity / motion intensity | Mean \|a\|, variance |
| Orientation change | The delta of pitch/roll from fusion |
| Environment event | A temperature/humidity threshold after filtering |
| Gesture (concept) | The acceleration-axis pattern in a short window |

Real gesture classification with the NPU = the next step, outside the current API's scope — M05 makes *the input ready*.

---

## 5. On-Device Intelligence Today: IMU Fusion

The closest thing to "smart on device" in the current SDK is **BMI270 → CM33 BSXLite fusion → quaternion / euler**

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

Connecting to the M01 map: heavy processing/fusion may sit in a different domain from always-on work — learners focus on the API on the CM55 that pushes/gets the result.

---

## 6. Preparing Streams for Host, Twin, and Cloud

### 6.1 Bitstream SENSOR_CFG (firmware view)

Streaming to the host is controlled by a per-sensor config (interval / mode / mask):

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

Reading the current value (when the project has Bitstream enabled):

```c
#include "bitstream_bs_cfg.h"
#include "bitstream_bs_wire.h"

const bitstream_bs_sensor_cfg_t *cfg =
    bitstream_bs_cfg_get_by_source(BITSTREAM_SENSOR_SOURCE_ID_SHT40);
/* cfg->enabled, sampling_interval_ms, publish_interval_ms, publish_mode, mask */
```

| Sensor ID (concept) | Used with |
|---|---|
| BMI270 | The IMU (+ a mask for ACC/GYR/TMP/EULER/QUAT, depending on the firmware) |
| BMM350 | The magnetometer |
| SHT40 | Temperature/humidity |
| DPS368 | Pressure |

On the host: configure it through **Bitstream Studio** (Sensor Telemetry), or see the HTML examples in [TESAIoT_Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon)

### 6.2 Digital Twin and dashboards

| Goal | Tool |
|---|---|
| Live gauges / a deck | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| HTML demos | Hackathon `ex01` SHT40 … `ex04` BMI270 … |
| Publishing to the cloud | Prepare the payload in M05 → actually send it in **M06 (MQTT)** |

### 6.3 Edge AI silicon vs course labs

| Piece (from M01) | In M05 |
|---|---|
| Ethos-U55 / NNLite | Know it exists on the chip — there is no inference wrapper in the lab SDK yet |
| DEEPCRAFT™ | Infineon's model workflow — read the overview at [DEEPCRAFT AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) |
| Your lab work | sample → filter → window → (fusion / telemetry) |

---

## 7. Application Patterns (Gesture / Activity / Events)

| Product pattern | What you can do in M05 with the current SDK |
|---|---|
| **Event / condition** | A threshold on a filtered value (such as temperature over a limit) → LED / UART / a queue |
| **Activity monitoring (concept)** | The variance of acceleration in a window |
| **Orientation / pose** | `ipc_fusion_result_t` |
| **Gesture classifier** | Preparing a feature window — the NPU model is the next step |

A simple event example:

```c
if (ema > 30.0f) {
    led_controller_set(LED_RED, true);
    printf("TEMP_EVENT high\r\n");
}
```

---

## 8. Module Summary

1. Get **`sensor_*_startup` / `read`** calls working first, then tune the rhythm with a task
2. Filter / normalize / window = the **lab code** essential for AI preparation
3. **Fusion** gives orientation, ready to use on the device
4. **SENSOR_CFG / Bitstream Studio** connects the stream to the host and the Digital Twin
5. NPU / DEEPCRAFT = the platform's direction — M05 gets the data ready
6. Next, **M06** sends a summary up over MQTT / to the cloud

### Next Steps

1. Do the exercise: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [Cheatsheet](resources/sensor-ai-prep.md)
3. When ready, continue to **M06 — MQTT and MQTTs for Cloud Communication** ([M06 lesson](../../m06-mqtt/l01-mqtt-and-mqtts/README.md))

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — the Sensors domain
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

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: a sensor stream and a data window ready for AI](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sensor-ai-prep.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-rtos/l01-freertos-programming/README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- [EP01 — DPS368 Monitor](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) — reads atmospheric pressure and temperature from an Infineon DPS368 sensor over I2C and displays it on an LVGL screen
- [EP02 — BMI270 Motion Visual](https://dev.tesaiot.dev/?example=developer-hub--int_ep02_bmi270_motion_visual&q=int_ep02_bmi270_motion_visual) — shows 6-axis motion values from a Bosch BMI270 sensor (accelerometer + gyroscope) on an LVGL screen in real time
- [EP03 — SHT40 Indicator](https://dev.tesaiot.dev/?example=developer-hub--int_ep03_sht40_indicator&q=int_ep03_sht40_indicator) — measures relative humidity and temperature with a Sensirion SHT4x sensor over I2C and shows it as an indicator on an LVGL screen
- [EP04 — BMM350 Compass](https://dev.tesaiot.dev/?example=developer-hub--int_ep04_bmm350_compass&q=int_ep04_bmm350_compass) — builds a digital compass from a Bosch BMM350 magnetic-field sensor over I3C, with a hard-iron calibration feature
- [EP06 — Digital Mic Probe](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) — captures audio from the board's stereo PDM microphone, computes the left/right loudness level and shows it as a level meter on an LVGL screen
