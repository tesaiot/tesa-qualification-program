# Cheatsheet — Sensor Data & AI Prep (M05)

**Course 1 · Module 5**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Driver calls

```c
sensor_sht40_startup();   sensor_sht40_read(&s);
sensor_bmi270_read(&imu); /* or sensor_bmi270_try_read */
sensor_dps368_read(&baro);
sensor_bmm350_read(&mag);
sensor_*_is_ready();
```

| Sample | Fields |
|---|---|
| `sht40_sample_t` | `temperature`, `humidity` |
| `bmi270_sample_t` | `acc_*`, `gyr_*`, `temperature`, `elapsed_ms` |
| `dps368_sample_t` | `pressure`, `temperature` |
| `bmm350_sample_t` | `mag_*`, `temperature` |

I²C shared bus: `cm55_i2c_manager_i2c_lock` / `unlock`  
BMM350: **I3C** (not I2C manager)

---

## Sampling task

```c
vTaskDelayUntil(&last, pdMS_TO_TICKS(period_ms));
```

No `sensor_*_set_rate_hz` in current drivers — period = task period or Bitstream SENSOR_CFG intervals.

---

## Lab-local conditioning

```c
ema = alpha * x + (1 - alpha) * ema;          /* filter */
y = 2 * (x - min) / (max - min) - 1;        /* normalize-ish */
imu_window_push(&w, &sample);               /* AI window */
```

---

## Fusion (orientation)

```c
cm55_imu_fusion_bridge_push_raw_components(ax, ay, az, gx, gy, gz, elapsed_ms);
cm55_imu_fusion_bridge_get_latest_result(&f); /* qw..qz, pitch, roll, orientation */
```

---

## Host / twin

| Tool | Link |
|---|---|
| Bitstream Studio | [Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| Hackathon demos | [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |
| Examples | [dev.tesaiot.dev](https://dev.tesaiot.dev/) |

SENSOR_CFG ideas: `enabled`, `sampling_interval_ms`, `publish_interval_ms`, `publish_mode`, `mask`

---

## Edge AI scope (this module)

| Do in M05 | Not a current SDK lab API |
|---|---|
| Stable samples + windows | Ethos / NNLite `run_model` |
| Fusion orientation | DEEPCRAFT training in-firmware |
| Events from thresholds | Full gesture classifier product |

---

## Lab API log

| งาน | API / เทคนิคที่ใช้ |
|---|---|
| Sensor A read | |
| Sensor B read | |
| Task period | |
| Filter / normalize | |
| Window + feature | |
| Fusion / host / event | |

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)
