---
id: twin.m05.l02
lang: th
title:
  th: 'แล็บ: ท่อ telemetry และ MQTT บน Twin'
  en: 'Lab: Telemetry Pipeline and MQTT on Twin'
summary:
  th: ออกแบบ topic ตรวจคุณภาพ Live Data ด้วย ex08 ตั้ง broker แล้ว subscribe ด้วย ex09 และทดลอง lossy/reconnect
  en: Design topics, check Live Data quality with ex08, start a broker and subscribe with ex09, then try lossy/reconnect cases.
level: L3
time_min:
  lab: 240
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m05.l01
objectives:
- th: ออกแบบ topic สำหรับ Telemetry/State/Event และตรวจฟิลด์กับหน่วยบน dashboard
  en: Design topics for Telemetry/State/Event and check fields and units on a dashboard.
- th: ตั้ง broker ใน Studio แล้วทำ pub/sub ได้อย่างน้อยหนึ่งคู่
  en: Start the broker in Studio and complete at least one pub/sub pair.
- th: ทดลอง lossy / disconnect / schema break อย่างน้อยหนึ่งเคสและบันทึกผล
  en: Run at least one lossy, disconnect or schema-break case and record the result.
develops:
- skill: proto.mqtt
  to: 2
- skill: iot.cloud-platform
  to: 2
assesses:
- skill: proto.mqtt
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M05/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M05 — Telemetry Pipeline and MQTT on Twin

**Course 2 · Module 5**  
**Type:** Hands-on (classify · Live Data quality · MQTT pub/sub · fault injection)  
**Suggested time:** ~3.5–4 ชั่วโมง  

Read first: [Lesson](../l01-telemetry-cloud-simulation/README.md) · [Lab notes](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M04 lab](../../m04-cosimulation/l02-lab/README.md) · [ex05 walkthrough](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | consumer Live Data พื้นฐาน |
| [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | MQTT บนเฟิร์มแวร์ / QoS |
| [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) | **ex08**, **ex09**–ex15 |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Start broker · Twin publish |

---

## Lab Goals

- แยกและส่งแนวคิด **Telemetry / State / Event** อย่างละอย่างน้อยหนึ่งอย่าง  
- ตรวจบน dashboard หรือ subscriber ว่าฟิลด์/หน่วยตรง  
- ตั้ง **MQTT broker** ใน Studio แล้วทำ pub/sub อย่างน้อยหนึ่งคู่  
- ทดลอง **lossy / disconnect / schema break** อย่างน้อยหนึ่งเคส  
- กรอก [telemetry-mqtt-lab-notes.md](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md)  

---

## Prerequisites

- [ ] M04 bring-up ผ่าน (Link เสถียร · รู้ Simulator XOR Bitstream)  
- [ ] โฟลเดอร์ Hackathon มี `web-app/`  
- [ ] รู้วิธี **Serve Web App Folder over HTTP** (M04)  
- [ ] โฟลเดอร์ `lab-notes/` สำหรับหลักฐาน  

---

## Lab A — Classify & design topics (required)

ออกแบบ (บนกระดาษหรือใน lab notes):

1. **Telemetry** — topic + ตัวอย่าง JSON 1 ก้อน + อัตราโดยประมาณ  
2. **State** — topic + เมื่อไรจะส่ง (เปลี่ยนโหมด / LED / Link)  
3. **Event** — topic หรือชื่อ event + เงื่อนไขสั้น ๆ  

ใช้โครงตัวอย่างจากบทเรียนได้ เช่น:

```text
device/<id>/devkit-twin/telemetry
device/<id>/state
device/<id>/event/<name>
```

**Pass when:** เพื่อนในทีมอ่าน topic แล้วเดาชนิดข้อมูลถูกโดยไม่ต้องเดาจาก payload อย่างเดียว

---

## Lab B — Live Data quality with `ex08` (required)

1. Link Studio (โหมดเดียว)  
2. Serve `web-app/` → เปิด **`ex08_stale_and_route.html`**  
3. จด `route`, `COM open`, `last origin`  
4. ทำให้เซ็นเซอร์อย่างน้อยหนึ่งตัวเข้า **stale** แล้วกลับ **fresh**  
5. แคป event log + pills  

**Pass when:** อธิบายได้ว่า stale เป็น host-side **Event** เมื่อ telemetry ขาด — และ `origin` สอดคล้องโหมด Studio

---

## Lab C — MQTT broker + `ex09` subscriber (required)

1. ใน Bitstream Studio: **Start broker**  
2. เปิด **`ex09_mqtt_subscriber.html`** — รอ `connected`  
3. Publish ไป topic ที่หน้าเว็บ subscribe (ค่าเริ่มต้น `device/devkit-twin-01/devkit-twin/telemetry` หรือตาม `?device=` / `?topic=`)  
   - แหล่ง publish: DevKit Twin MQTT tab / Sensor Studio connectivity / เครื่องมืออื่นที่มี  
4. ยืนยัน **Last payload** ตรงฟิลด์และหน่วย  
5. แคปคู่: แหล่ง publish + หน้า ex09  

**Pass when:** message count ≥ 1 และ JSON อธิบายได้ว่าเป็น Telemetry (หรือชนิดที่ตั้งใจ)

---

## Lab D — Pipeline / schema drill (recommended)

เลือกอย่างน้อยหนึ่ง:

- ตัดฟิลด์จาก payload แล้วดูว่า subscriber/dashboard พังตรงไหน  
- ส่งค่าหน่วยผิดโดยตั้งใจ แล้วจดว่า UI “ยังสวยแต่ผิดความหมาย”  
- เปิด **ex14** ลอง QoS + retain บน `lab/qos-demo` แล้วให้เพื่อนเปิด subscriber (เช่น ex11) หลังคุณ retain  

**Pass when:** มีโน้ต “สิ่งที่พัง / สิ่งที่ไม่พัง” อย่างน้อยหนึ่งบรรทัดใน lab notes

---

## Lab E — Lossy / reconnect (recommended — part of the complete deliverable)

เลือกอย่างน้อยหนึ่งเคส แล้วกรอกตารางใน lab notes:

| เคส | ตัวอย่างการทำ |
|---|---|
| Stop / Start broker สั้น ๆ | ดู ex09 `reconnecting` → `connected` |
| หยุด publisher ชั่วคราว | ดูช่องว่าง · หรือ ex08 stale |
| ปิดแท็บ ex09 แล้วเปิดใหม่ | ถ้ามี retain บน state topic — ได้ค่าล่าสุดหรือไม่ |

**Pass when:** ระบุพฤติกรรมที่เห็น (drop / retry / reconnect / stale) โดยไม่เดา

---

## Lab F — Optional ladder

ถ้าเหลือเวลา เลือกต่อ:

- **ex10** publish จากเบราว์เซอร์  
- **ex12** gauges  
- **ex15** dashboard รวม  
- Publish จากเฟิร์มแวร์จริงหลัง Wi‑Fi ([C1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)) เข้า broker ของแล็บ  

---

## Deliverables checklist

- [ ] Lab A–C ผ่าน  
- [ ] Lab E (หรืออย่างน้อย Lab D ถ้าเวลาไม่พอ)  
- [ ] [telemetry-mqtt-lab-notes.md](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) กรอกครบ  
- [ ] หลักฐานสกรีนช็อต: ex08 + ex09 (+ schema/lossy ตามที่ทำ)  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| ex08 disconnected | Studio/bridge · Serve ถูกโฟลเดอร์ `web-app/` |
| ex09 ค้าง connecting | **Start broker** · ตรวจ `ws://127.0.0.1:8883/mqtt` |
| connected แต่ Waiting for messages | ยังไม่มี publisher · topic ไม่ตรง · ตรวจ `?device=` / `?topic=` |
| Live Data ดี MQTT ว่าง | คนละท่อ — อย่าแก้เฟิร์มแวร์ก่อนเช็ค broker/topic |
| origin สับสน | อย่าผสม Simulator + Bitstream · เคลียร์แล้ว Link ใหม่ |
| Retain ทำให้ค่า “ค้าง” | ตรวจว่าทดลองบน topic lab ไม่ใช่ telemetry หนาแน่น |

[Lesson](../l01-telemetry-cloud-simulation/README.md) · [Lab notes](../l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md) · [Table of Contents](../../README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)
