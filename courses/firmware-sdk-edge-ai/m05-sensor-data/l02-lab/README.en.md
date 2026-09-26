---
id: fw-sdk.m05.l02
lang: en
title:
  th: 'แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI'
  en: 'Lab: Sensor Streams and AI-Ready Windows'
summary:
  th: อ่านเซ็นเซอร์สองชนิดด้วย task คาบคงที่ กรองหรือ normalize สร้างหน้าต่างข้อมูล แล้วเลือกต่อยอด (fusion, host telemetry หรือ event)
  en: Read two sensors in a fixed-rate task, filter or normalise, build a data window, then pick an extension (fusion, host telemetry or an event).
level: L3
time_min:
  lab: 210
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m05.l01
objectives:
- th: อ่านเซ็นเซอร์อย่างน้อยสองชนิดด้วย task คาบเวลาคงที่
  en: Read at least two sensor types in a fixed-period task.
- th: กรองหรือ normalize ค่า และสร้างหน้าต่างข้อมูลที่ให้เวกเตอร์สรุปอย่างน้อยหนึ่งครั้งต่อวินาที
  en: Filter or normalise the values and build a window that yields a summary vector at least once per second.
develops:
- skill: ai.data-collection
  to: 2
- skill: sys.sensors-actuators
  to: 2
- skill: rtos.freertos
  to: 2
assesses:
- skill: ai.data-collection
  level: 2
  evidence: README.md#submit-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: ab1d721428fead304056e6228747652c12e37fa137063c1f7f6ff6b3eaa26b51
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M05/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M05 — Sensor Streams and AI-Ready Windows

**Course 1 · Module 5**
**Type:** Hands-on lab (read sensors → filter/window → optional host view)
**Suggested time:** 2.5–3.5 hours

Read first: [Lesson](../l01-sensor-data-for-edge-ai/README.md) · [Cheatsheet](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-rtos/l01-freertos-programming/README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [AI-ready Sensor Streams](../l01-sensor-data-for-edge-ai/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [Lesson](../l01-sensor-data-for-edge-ai/README.md) | `sensor_*`, fusion, SENSOR_CFG |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | The **Sensors** domain |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | `ex01`–`ex06` to see values on the host |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | The Sensor Telemetry deck |

---

## Lab Goals

- Call `sensor_*_startup` / `read` for at least **two kinds** (e.g. SHT40 + BMI270)
- Build a **fixed-rate reading task** with FreeRTOS
- Apply **a filter or normalisation** in at least one form in the lab code
- Build a **data window** from the IMU or a temperature series
- (Recommended) watch the stream in Bitstream Studio or the Hackathon web-app
- (Recommended) read a **fusion** result, or fire an **event** on a condition

---

## Prerequisites

- [ ] Have passed M03 (UART) and M04 (can create tasks)
- [ ] The board has sensors matching the kit used
- [ ] Know which sensors are enabled in your firmware/project

---

## Lab A — Bring-up two sensors (required)

1. Call `sensor_sht40_startup`, then read `temperature` / `humidity` and print to UART
2. Call `sensor_bmi270_startup` (if not already started at boot), then read `acc_*`
3. Check `sensor_*_is_ready` before reading

**Pass when:** you get reasonable-looking values for both kinds on the terminal

---

## Lab B — Fixed-rate sample task (required)

1. Create a task that reads a sensor with `vTaskDelayUntil` (e.g. SHT40 every 500–1000 ms, **or** BMI270 every 40 ms)
2. Record which period you chose and why

```c
TickType_t last = xTaskGetTickCount();
const TickType_t period = pdMS_TO_TICKS(40);
for (;;) {
    (void)sensor_bmi270_read(&imu);
    vTaskDelayUntil(&last, period);
}
```

**Pass when:** the reading period is consistent, with no busy-waiting

---

## Lab C — Filter + normalize (required)

1. Apply an EMA (or a short-window median) to temperature, or an acceleration axis
2. Normalise at least one channel's value into a given range (such as roughly [-1, 1], or 0..1)
3. Print both the raw and the processed value

**Pass when:** you can explain how the filter reduces noise, from what you observe on the terminal

---

## Lab D — Feature window (required)

1. Build a ring buffer / window of at least **16–32** samples from BMI270 **or** a temperature series
2. Once the window is full, compute at least one feature (such as mean, variance, max−min)
3. Print the feature over UART periodically

**Pass when:** you get a summary vector from a full window at least once per second (or at a reasonable period)

---

## Lab E — Choose one (recommended)

### E1 Fusion orientation

- `cm55_imu_fusion_bridge_push_raw_components` + `get_latest_result`
- Print pitch/roll or `orientation`

### E2 Host telemetry

- Flash/connect per your kit → open [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) or the Hackathon `web-app`
- Confirm the sensor value on the host moves in step with the board

### E3 Condition event

- When the feature or the EMA exceeds a threshold → turn on the LED + print `EVENT ...`

**Pass when:** you have completed one option with evidence (terminal / UI / LED)

---

## Short report (8–12 lines)

1. The sensors used + the sampling period
2. The filter / normalisation method
3. The window size + the feature(s) computed
4. (If any) the fusion result, or a host screenshot
5. What you plan to send on to the cloud in M06 (a conceptual payload)

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| `is_ready` is false | Not started up yet · the sensor isn't built into the project · a bus problem |
| Reading works only sometimes | The period is too fast · the bus is contended with another task · try `try_read` / reduce the rate |
| The magnetometer won't read through the I2C lock | The BMM350 is I3C — use `sensor_bmm350_*` per the SDK |
| Fusion doesn't update | Raw data hasn't been pushed yet · CM33 fusion isn't running in the config you're using |
| The host shows no value | Bitstream not Linked yet · the HEX/VSIX are mismatched versions · SENSOR_CFG disabled |

---

## Submit checklist

- [ ] Labs A–D passed
- [ ] At least 1 item from Lab E
- [ ] The table in [sensor-ai-prep.md](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) filled in
- [ ] The short report completed

[Lesson](../l01-sensor-data-for-edge-ai/README.md) · [Cheatsheet](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) · [Table of Contents](../../README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)
