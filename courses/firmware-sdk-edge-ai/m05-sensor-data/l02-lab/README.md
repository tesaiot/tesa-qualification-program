---
id: fw-sdk.m05.l02
lang: th
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

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI](../l01-sensor-data-for-edge-ai/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Lesson](../l01-sensor-data-for-edge-ai/README.md) | `sensor_*`, fusion, SENSOR_CFG |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Domain **Sensors** |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | `ex01`–`ex06` ดูค่าบนโฮสต์ |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Sensor Telemetry deck |

---

## Lab Goals

- เรียก `sensor_*_startup` / `read` อย่างน้อย **สองชนิด** (เช่น SHT40 + BMI270)  
- สร้าง **task อ่านคาบคงที่** ด้วย FreeRTOS  
- ทำ **filter หรือ normalize** อย่างน้อยหนึ่งแบบในโค้ดแล็บ  
- สร้าง **หน้าต่างข้อมูล (window)** จาก IMU หรืออุณหภูมิ  
- (แนะนำ) ดูสตรีมบน Bitstream Studio หรือ Hackathon web-app  
- (แนะนำ) อ่านผล **fusion** หรือยิง **event** เมื่อเข้าเงื่อนไข  

---

## Prerequisites

- [ ] ผ่าน M03 (UART) และ M04 (สร้าง task ได้)  
- [ ] บอร์ดมีเซ็นเซอร์ตามคิตที่ใช้  
- [ ] รู้ว่าเซ็นเซอร์ใดถูก enable ในเฟิร์มแวร์/โปรเจกต์ของคุณ  

---

## Lab A — Bring-up two sensors (required)

1. `sensor_sht40_startup` แล้วอ่าน `temperature` / `humidity` พิมพ์ UART  
2. `sensor_bmi270_startup` (ถ้ายังไม่ถูก start จาก boot) แล้วอ่าน `acc_*`  
3. ตรวจ `sensor_*_is_ready` ก่อนอ่าน  

**Pass when:** ได้ค่าที่สมเหตุสมผลทั้งสองชนิดบน terminal

---

## Lab B — Fixed-rate sample task (required)

1. สร้าง task อ่านเซ็นเซอร์ด้วย `vTaskDelayUntil` (เช่น SHT40 ทุก 500–1000 ms **หรือ** BMI270 ทุก 40 ms)  
2. บันทึกว่าเลือกคาบเท่าไรและทำไม  

```c
TickType_t last = xTaskGetTickCount();
const TickType_t period = pdMS_TO_TICKS(40);
for (;;) {
    (void)sensor_bmi270_read(&imu);
    vTaskDelayUntil(&last, period);
}
```

**Pass when:** คาบอ่านสม่ำเสมอโดยไม่ busy-wait

---

## Lab C — Filter + normalize (required)

1. ทำ EMA (หรือ median หน้าต่างสั้น) บนอุณหภูมิหรือแกน accel  
2. Normalize ค่าอย่างน้อยหนึ่งช่องไปช่วงที่กำหนด (เช่นประมาณ [-1, 1] หรือ 0..1)  
3. พิมพ์ทั้งค่าดิบและค่าหลังประมวลผล  

**Pass when:** อธิบายได้ว่า filter ลด noise อย่างไรจากการสังเกตบน terminal

---

## Lab D — Feature window (required)

1. สร้าง ring buffer / window อย่างน้อย **16–32** ตัวอย่างจาก BMI270 **หรือ** อนุกรมอุณหภูมิ  
2. เมื่อหน้าต่างเต็ม ให้คำนวณอย่างน้อยหนึ่งฟีเจอร์ (เช่น mean, variance, max−min)  
3. พิมพ์ฟีเจอร์ทาง UART เป็นคาบ  

**Pass when:** ได้เวกเตอร์สรุปจากหน้าต่างเต็มอย่างน้อยหนึ่งครั้งต่อวินาที (หรือตามคาบที่สมเหตุสมผล)

---

## Lab E — Choose one (recommended)

### E1 Fusion orientation

- `cm55_imu_fusion_bridge_push_raw_components` + `get_latest_result`  
- พิมพ์ pitch/roll หรือ `orientation`  

### E2 Host telemetry

- Flash/เชื่อมตามชุดที่ใช้ → เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) หรือ Hackathon `web-app`  
- ยืนยันว่าค่าเซ็นเซอร์บนโฮสต์ขยับตรงกับบอร์ด  

### E3 Condition event

- เมื่อฟีเจอร์หรือ EMA เกินเกณฑ์ → เปิด LED + ข้อความ `EVENT ...`  

**Pass when:** ทำครบหนึ่งตัวเลือกและมีหลักฐาน (terminal / UI / LED)

---

## Short report (8–12 lines)

1. เซ็นเซอร์ที่ใช้ + คาบ sampling  
2. วิธี filter / normalize  
3. ขนาดหน้าต่าง + ฟีเจอร์ที่คำนวณ  
4. (ถ้ามี) ผล fusion หรือภาพหน้าจอโฮสต์  
5. สิ่งที่จะส่งต่อไป cloud ใน M06 (payload แนวคิด)

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| `is_ready` เป็น false | ยังไม่ startup · เซ็นเซอร์ไม่ถูก build เข้าโปรเจกต์ · บัสมีปัญหา |
| อ่านได้เป็นครั้งคราว | คาบถี่เกิน · บัสแย่งกับ task อื่น · ลอง `try_read` / ลดอัตรา |
| Mag อ่านไม่ได้ผ่าน I2C lock | BMM350 เป็น I3C — ใช้ `sensor_bmm350_*` ตาม SDK |
| Fusion ไม่อัปเดต | ยังไม่ push raw · CM33 fusion ยังไม่รันในคอนฟิกที่ใช้ |
| โฮสต์ไม่มีค่า | ยังไม่ Link Bitstream · HEX/VSIX คนละเวอร์ชัน · SENSOR_CFG disabled |

---

## Submit checklist

- [ ] Lab A–D ผ่าน  
- [ ] Lab E อย่างน้อย 1 ข้อ  
- [ ] กรอกตารางใน [sensor-ai-prep.md](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md)  
- [ ] รายงานสั้นครบ  

[Lesson](../l01-sensor-data-for-edge-ai/README.md) · [Cheatsheet](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) · [Table of Contents](../../README.md) · [M06 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)
