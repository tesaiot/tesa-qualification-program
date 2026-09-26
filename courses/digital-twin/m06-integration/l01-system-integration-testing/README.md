---
id: twin.m06.l01
lang: th
title:
  th: ทดสอบ end-to-end บน Digital Twin
  en: End-to-end Testing on the Digital Twin
summary:
  th: เกณฑ์ผ่านขั้นต่ำของ Capstone การวิเคราะห์ log ทีละชั้น โจทย์จากโดเมนจริง และกรณีศึกษา Smart Environmental Monitor
  en: The capstone's minimum rubric, layer-by-layer log analysis, domain stories and the Smart Environmental Monitor case study.
level: L3
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m05.l02
objectives:
- th: ตรวจระบบ Twin แบบ end-to-end ตามเกณฑ์ผ่านขั้นต่ำ (virtual device + script, co-sim, visualization, MQTT, README, ตารางเทส ≥ 3 เคส)
  en: Check a Twin system end to end against the minimum rubric (virtual device + script, co-sim, visualisation, MQTT, README, at least three test cases).
- th: วิเคราะห์ log ทีละชั้น โดยเก็บ log ฝั่งเฟิร์มแวร์และฝั่งโฮสต์ในรอบเดียวกัน
  en: Analyse logs layer by layer, capturing firmware-side and host-side logs in the same run.
- th: แปลงโจทย์จากโดเมนจริง (IoT ทั่วไป บ้าน โรงงาน สุขภาพ) ลงท่อ Twin ชุดเดียวกัน
  en: Map a real-domain story (general IoT, home, factory, health) onto the same Twin pipeline.
develops:
- skill: test.sil-hil
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: soft.communication
  to: 2
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — System Integration and Testing

**Course 2 · Module 6**  
**Suggested time:** ประมาณ 2 ชั่วโมง + ใช้เวลาเพิ่มเพื่อให้มินิโปรเจกต์สมบูรณ์ได้  
**Format:** Capstone — รวม M01–M05 เป็นระบบที่สาธิตซ้ำได้ พร้อมตารางเทส E2E และหลักฐาน

[Lab](../l02-lab/README.md) · [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. ทดสอบระบบแบบ **End-to-End** (Firmware + Twin + Cloud/Dashboard)  
2. วิเคราะห์ **Log** และแก้ปัญหาแบบมีหลักฐาน  
3. ทำกรณีศึกษา / มินิโปรเจกต์ (เช่น **Smart Environmental Monitor**) และแมปเข้า **โดเมนจริง** — IoT ทั่วไป · ในบ้าน · โรงงาน · สุขภาพ  
4. ใช้ **Developer Guide / ตัวอย่างโปรเจกต์** และแพ็กเอกสารออนไลน์ของหลักสูตร  
5. ส่งมอบแล็บเต็มรูปแบบ: สร้าง Twin model, ทดสอบโค้ดผ่าน Twin, จำลองเซ็นเซอร์/สัญญาณ  

> **Key phrase**  
> Capstone Course 2 = *เลือกและเชื่อมชิ้นที่ทำมาแล้ว* ให้มีตารางผ่าน/ไม่ผ่าน — ไม่ใช่เขียน Twin ใหม่ทั้งก้อน

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M01](../../m01-twin-architecture/l01-twin-architecture/README.md)–[M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | ชิ้นส่วนที่ต้องรวม |
| [Course 1 M08 Capstone](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) | รูปแบบส่งมอบ / rubric ฝั่งเฟิร์มแวร์ |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Twin host · broker · visualization |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX · VSIX · **`web-app/`** (ex06 · ex15) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ / API |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB ประกอบเดโม 3D (ถ้าใช้) |
| [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) | แบบฟอร์มผลงาน |

---

## 1. Course 2 Lab Index (What You Already Have)

| Module | Lab focus | นำมาใช้ใน M06 |
|---|---|---|
| [M01](../../m01-twin-architecture/l02-lab/README.md) | แผนที่ Twin / backend XOR | อธิบายสถาปัตยกรรมเดโม |
| [M02](../../m02-vscode-twin/l02-lab/README.md) | Studio workspace / Link | bring-up ที่ทำซ้ำได้ |
| [M03](../../m03-virtual-device/l02-lab/README.md) | Virtual device + event script (+ GLB) | แหล่งกระตุ้นเซ็นเซอร์ |
| [M04](../../m04-cosimulation/l02-lab/README.md) | Co-sim I/O · optional `ex05` | พิสูจน์เฟิร์มแวร์ ↔ Twin |
| [M05](../../m05-telemetry-cloud/l02-lab/README.md) | Telemetry · MQTT · `ex08`/`ex09` | ท่อออก dashboard / cloud |
| **[M06](../l02-lab/README.md)** | **E2E mini-project** | รวม + ตารางเทส + README |

ถ้าชิ้นใดยังไม่ผ่านเกณฑ์ขั้นต่ำ ให้ซ่อมก่อนขยายฟีเจอร์ใน Capstone

---

## 2. End-to-End Path on Twin

เส้นทางขั้นต่ำที่ต้องมีหลักฐานผ่าน/ไม่ผ่าน:

```text
[1 Stimulus]
  M03 event script / scene / switch / tilt
        │
        ▼
[2 Firmware]
  read → decide → act (LED / flag / publish)
        │
        ▼
[3 Twin / Studio visualization]
  telemetry panel · 3D · status
        │
        ├──► [4a Live Data dashboard]  e.g. web-app ex06
        │
        └──► [4b MQTT]  broker + pub and/or sub  e.g. ex09 / ex15
```

| ขั้น | หลักฐานที่ยอมรับ |
|---|---|
| 1 Stimulus | โน้ตสคริปต์/เวลา + สกรีนช็อตก่อน–หลัง |
| 2 Firmware | UART/log หรือพฤติกรรมที่สังเกตได้บนโฮสต์ว่ามาจาก logic |
| 3 Studio | กราฟ / สถานะ / 3D สอดคล้อง |
| 4a หรือ 4b | consumer ชั้นนอก **อย่างน้อยหนึ่งท่อ** (Live Data และ/หรือ MQTT) |

อย่าใช้ความรู้สึกว่า “ดูเหมือนใช้ได้” เป็นเกณฑ์เดียว — ใช้ตารางใน [e2e-case-brief.md](resources/e2e-case-brief.md)

### 2.1 Minimum pass rubric

| เกณฑ์ | ต้องมี |
|---|---|
| Virtual device + event script (หรือ timeline เทียบเท่า) | ใช่ |
| Firmware co-sim ทำงาน (Simulator และ/หรือ Board) | ใช่ |
| Visualization ใน Studio แสดงค่า/สถานะ | ใช่ |
| MQTT publish **หรือ** subscribe อย่างน้อยหนึ่งทาง | ใช่ |
| README วิธีรันซ้ำ (bring-up → demo → teardown) | ใช่ |
| ตารางเทส E2E ผ่านอย่างน้อย **3 เคส** | ใช่ |
| ไม่ฝัง secret (Wi‑Fi / broker password) ในไฟล์ส่ง | ใช่ |

งานต่อยอด (ไม่บังคับ): ทั้ง Live Data **และ** MQTT บนเดโมเดียวกัน · fault/reconnect เคส · GLB จาก M03 · เปรียบเทียบ Path A vs B

---

## 3. Log Analysis — Layer by Layer

เมื่อเดโมพัง ให้ถามตามลำดับ (ขยายจาก M04/M05):

```text
1. Firmware still alive?           → heartbeat / UART / LED
2. Twin / Studio session up?     → Link · backend XOR
3. Stimulus actually applied?    → M03 script / scene
4. Value reached firmware?       → log read path
5. Firmware decided / wrote?     → log / LED / publish
6. Studio shows change?          → correct panel
7. Live Data consumer OK?        → ex06 / ex08 connected · not stale
8. Broker up + topic match?      → Start broker · ex09/ex15
9. Payload schema OK?            → fields / units (M05 drill)
```

| อาการ | ชั้นที่น่าสงสัยก่อน |
|---|---|
| ไม่มีสตรีมเลย | 2 — host / Link |
| สตรีมมี กระตุ้นแล้วเงียบ | 3–4 — script / cfg |
| Log ถูก UI ไม่ขยับ | 6–7 — panel / consumer |
| Live Data ดี MQTT ว่าง | 8 — คนละท่อ / broker / topic |
| MQTT มีข้อความแต่ค่าเพี้ยน | 9 — schema |

> **Key phrase**  
> แก้ทีละชั้น — แคป log ทั้งฝั่งเฟิร์มแวร์และโฮสต์ในรอบเดียวกัน

เก็บบรรทัดสำคัญใน case brief ส่วน “ปัญหาที่พบและการแก้”

---

## 4. Domain Stories — Same E2E Pipe, Different Worlds

โครง E2E ใน §2 **เหมือนกันทุกโดเมน** — ที่ต่างคือ *เรื่องราว*, ชื่อเซ็นเซอร์ในจินตนาการ, เกณฑ์แจ้งเตือน, และสิ่งที่ผู้ชมเข้าใจว่า “ทำไมต้องมี Twin”

เลือกโดเมนหนึ่งใน Capstone แล้วแมปลงเครื่องมือในแล็บ (SHT40 / DPS368 / BMI270 / สวิตช์ / MQTT) — **ไม่ต้องมีฮาร์ดแวร์เฉพาะโดเมน**

> **Key phrase**  
> โดเมน = *ภาษาของผู้ใช้* · ท่อ Twin = *ภาษาของวิศวกรเฟิร์มแวร์* — Capstone ต้องพูดได้ทั้งสองภาษา

### 4.0 How to pick a domain (quick)

| ถ้าทีมสนใจ… | เลือกโดเมน | จุดเด่นในการสาธิต |
|---|---|---|
| อุปกรณ์เชื่อมคลาวด์ทั่วไป | §4.1 IoT | fleet / gateway / dashboard |
| ชีวิตประจำวันในที่อยู่อาศัย | §4.2 Home | comfort · ความปลอดภัยในบ้าน |
| สายการผลิต / เครื่องจักร | §4.3 Industrial | threshold · operator command · downtime |
| การดูแลสุขภาพ / wellness (จำลอง) | §4.4 Health | orientation · สัญญาณชีพจำลอง · privacy |

จากนั้นใช้ §5 เป็นแม่แบบแล็บ (Smart Environmental Monitor) หรือเปลี่ยนชื่อโปรเจกต์ให้ตรงโดเมนที่เลือก — **เกณฑ์ผ่านยังเป็นชุดเดียวกัน**

### 4.1 Internet of Things (general)

**ภาพที่ผู้ชมเห็น:** โหนดเซ็นเซอร์ที่ขอบเครือข่าย ส่งค่าเข้า gateway / Twin แล้วขึ้นแดชบอร์ดคลาวด์จำลอง — “อุปกรณ์พูดกับระบบหลังบ้านได้”

| ชิ้น E2E | ตัวอย่างในโดเมนนี้ | แมปลงแล็บ |
|---|---|---|
| Stimulus | สภาพแวดล้อมเปลี่ยน · หรือเปิดโหมดทดสอบจากศูนย์ | scene Quiet → Active · event script |
| Sense | อุณหภูมิ · ความชื้น · ความดัน · IMU | SHT40 / DPS368 / BMI270 |
| Decide | เกินเกณฑ์ → `alert` event · เปลี่ยน `mode` | firmware threshold + state |
| Act / publish | telemetry เป็นจังหวะ + event เป็นครั้งคราว | MQTT `…/telemetry` · `…/event/alert` |
| Observe | แดชบอร์ดหลายช่อง · route/origin ชัด | Studio + **ex06** + **ex09/ex15** |

**สามฉากเดโม**

1. **Normal** — โหนดออนไลน์ ส่ง telemetry สม่ำเสมอ (`origin` สอดคล้อง Simulator หรือ Board)  
2. **Stimulus** — อุณหภูมิจำลองพุ่ง → event `threshold_exceeded` ขึ้น subscriber  
3. **Command / fault** — สั่ง `mode=maintenance` จาก MQTT **หรือ** ตัด broker สั้น ๆ แล้ว reconnect  

**Topic ตัวอย่าง (ปรับได้)**

```text
device/<id>/iot/telemetry
device/<id>/iot/state
device/<id>/iot/event/alert
device/<id>/iot/cmd                 ← subscribe คำสั่งกลับ
```

### 4.2 Inside the home (smart home)

**ภาพที่ผู้ชมเห็น:** เซ็นเซอร์ในห้องนั่งเล่น / ห้องนอน ช่วยเรื่องสบายและความปลอดภัย — ไม่ใช่แค่กราฟตัวเลข แต่เป็น “บ้านตอบสนอง”

| สถานการณ์บ้าน | Twin จำลองอย่างไร | สิ่งที่สาธิตบนโฮสต์ |
|---|---|---|
| ห้องร้อนเกินไป | script ดัน `temperatureC` สูง | LED/state = `cool_request` · MQTT event |
| เปิดหน้าต่าง / ประตู | สวิตช์หรือ GPIO จำลอง | state `window=open` · retain บน topic state |
| คนเดินในบ้านตอนกลางคืน | IMU / motion scene | event `motion_detected` สั้น ๆ |
| เจ้าของสั่งจากแอป | MQTT command | `mode=away` / `mode=home` |

**สามฉากเดโม**

1. **Normal** — อุณหภูมิ/ความชื้นนิ่ง สบาย ๆ บน ex06  
2. **Stimulus** — “แดดจัดในห้อง” (Warm scene) → แจ้งเตือน + เปลี่ยนโหมด  
3. **Command** — ส่ง `away` จากโฮสต์ → อุปกรณ์เข้าโหมดประหยัด/เฝ้าระวัง (แสดงบน Studio)

**จุดเล่าที่ดี:** ใช้ GLB ห้องหรืออุปกรณ์จาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) เป็นฉากประกอบ — ย้ำว่าภาพ 3D **ไม่แทน** ค่าเซ็นเซอร์จริง

```text
home/<roomId>/climate/telemetry
home/<roomId>/security/state
home/<roomId>/cmd
```

### 4.3 Industrial plant / factory floor

**ภาพที่ผู้ชมเห็น:** เครื่องจักรบนไลน์ผลิตมี “ฝาแฝดดิจิทัล” สำหรับซ้อมแจ้งเตือนและคำสั่งจากห้องควบคุม — ลดการทดลองบนเครื่องจริงทุกครั้ง

| สถานการณ์โรงงาน | Twin จำลองอย่างไร | สิ่งที่สาธิตบนโฮสต์ |
|---|---|---|
| อุณหภูมิแบริ่ง / ตู้คอนโทรลสูง | temp + threshold | event `overtemp` · หยุดโหมดรันจำลอง |
| สั่นผิดปกติ / เอียง | BMI270 accel หรือ orientation (`ex05`) | event `vibration_high` / tilt alarm |
| ความดันในระบบลม/ของเหลว | DPS368 เป็น proxy | กราฟ + MQTT telemetry |
| ช่างสั่งจาก SCADA จำลอง | MQTT command | `run` / `stop` / `ack_alarm` |
| สัญญาณขาดช่วงบนไลน์ | หยุด publish / stop broker | stale (ex08) · reconnect |

**สามฉากเดโม**

1. **Normal** — ไลน์ “เขียว” ค่าอยู่ในย่าน · operator dashboard (ex06) อัปเดต  
2. **Stimulus** — inject overtemp/vibration → alarm state + event topic  
3. **Command / fault** — สั่ง `stop` จาก MQTT **หรือ** สูญเสียลิงก์สั้น ๆ แล้วกู้ (สำคัญต่อ downtime narrative)

**จุดเล่าที่ดี:** เน้นว่า Twin ใช้ **ซ้อม runbook** (ใครทำอะไรเมื่อ alarm) ก่อนแตะเครื่องจริง

```text
plant/<lineId>/machine/<id>/telemetry
plant/<lineId>/machine/<id>/alarm
plant/<lineId>/machine/<id>/cmd
```

### 4.4 Medical / health & wellness (lab simulation only)

**ภาพที่ผู้ชมเห็น:** อุปกรณ์ติดตามสุขภาพหรือโมดูล bedside จำลอง — ฝึกท่อข้อมูลและความน่าเชื่อถือของลิงก์ **ไม่ใช่** อุปกรณ์แพทย์ที่ผ่านการรับรองคลินิก

> **ขอบเขตของแล็บ**  
> ใช้ค่าจำลอง / เซ็นเซอร์พัฒนาการบน DevKit เท่านั้น · ห้ามอ้างว่าผ่านมาตรฐานการแพทย์ · ห้ามใช้ข้อมูลคนไข้จริงในแล็บ · เน้น privacy: ไม่ใส่ชื่อ–HN ใน topic/payload ที่ส่งต่อ

| สถานการณ์สุขภาพ (จำลอง) | Twin จำลองอย่างไร | สิ่งที่สาธิตบนโฮสต์ |
|---|---|---|
| อุณหภูมิแวดล้อมรอบผู้ป่วย / ห้อง | SHT40 | climate comfort บน dashboard |
| ท่าทาง / การล้ม (แนวคิด) | BMI270 orientation — [M04 ex05](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | horizon เอียงผิดปกติ → event |
| กิจกรรม / การเคลื่อนไหว | IMU scene Motion | telemetry rate สูงขึ้น |
| พยาบาล/แอปสั่งโหมดวัด | MQTT command | `mode=active_monitor` |
| สัญญาณขาด = ความเสี่ยง | stale / disconnect | ex08 + reconnect drill (M05) |

**สามฉากเดโม**

1. **Normal** — สตรีมนิ่ง · แสดงว่าลิงก์และ schema ถูกต้อง  
2. **Stimulus** — เอียง/Motion แรง → event `posture_alert` (ชื่อจำลอง) ขึ้น subscriber  
3. **Fault** — ตัดสตรีมสั้น ๆ → UI แสดง stale/reconnect — เล่าว่าทำไม health link ต้องมี watchdog

**Topic ตัวอย่าง (หลีกเลี่ยงข้อมูลระบุตัวตน)**

```text
care/device/<id>/vitals_sim/telemetry    ← ค่าจำลองเท่านั้น
care/device/<id>/state
care/device/<id>/event/posture_alert
care/device/<id>/cmd
```

### 4.5 One mapping table (all domains → same lab kit)

| โดเมน | “ฮีโร่” ที่เล่า | เซ็นเซอร์หลักในแล็บ | Consumer แนะนำ | Event ตัวอย่าง |
|---|---|---|---|---|
| IoT ทั่วไป | โหนดขอบ ↔ คลาวด์ | SHT40 + state | ex06 + ex15 | `threshold_exceeded` |
| ในบ้าน | ห้องสบาย / ปลอดภัย | SHT40 + switch | ex06 + MQTT cmd | `motion_detected` |
| โรงงาน | เครื่องจักร + alarm | temp/pressure + BMI270 | ex06 + ex08 + ex15 | `overtemp` / `tilt` |
| สุขภาพ (จำลอง) | ลิงก์เฝ้าระวัง | BMI270 + SHT40 | ex05 + ex08 + ex09 | `posture_alert` |

เขียนชื่อโดเมนที่เลือกไว้บนหน้าแรกของ [e2e-case-brief.md](resources/e2e-case-brief.md)

---

## 5. Case Study — Smart Environmental Monitor (Twin)

โจทย์แนะนำเริ่มต้นของหลักสูตร (เทียบเท่าโดเมน **IoT / สภาพแวดล้อม**) — จำลองมอนิเตอร์สิ่งแวดล้อมบน Twin แล้วพิสูจน์ E2E  
ถ้าเลือกโดเมน §4.2–§4.4 ให้ใช้โครงเดียวกัน แค่เปลี่ยนชื่อสถานการณ์และ event ตามตารางด้านบน

### 5.1 Suggested story

| ชิ้น | ตัวอย่างในแล็บ |
|---|---|
| เซ็นเซอร์ | อุณหภูมิ / ความชื้น (SHT40) และ/หรือ pressure · สวิตช์หรือโหมด |
| พฤติกรรม | เกินเกณฑ์ → เปลี่ยน state / LED / event |
| Twin | Virtual device + script Lab Quiet → Warm / Alert |
| Host view | Studio telemetry + optional 3D |
| Cloud sim | MQTT telemetry topic + คำสั่งโหมดกลับ (อย่างน้อยหนึ่งทาง) |
| External proof | **`ex06`** (multi-sensor Live Data) และ/หรือ **`ex15`** (WS vs MQTT) |

### 5.2 Architecture sketch for your README

```text
[Event script] ──stimulus──► [Virtual sensors]
                                  │
                                  ▼
                         [Firmware co-sim]
                          decide / act
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            [Bitstream Studio]          [MQTT broker]
                    │                           │
                    ▼                           ▼
              web-app ex06              ex09 / ex15 / gauges
```

### 5.3 Three demo scenarios (required)

| # | ชื่อ | สิ่งที่ผู้ชมต้องเห็น |
|---|---|---|
| 1 | **Normal** | ค่า environmental อัปเดตสม่ำเสมอบน Studio + consumer |
| 2 | **Stimulus / threshold** | สคริปต์หรือสวิตช์ทำให้ state/event เปลี่ยนชัด |
| 3 | **Command or fault** | คำสั่ง MQTT เข้าอุปกรณ์/Twin **หรือ** ตัด broker/สตรีมสั้น ๆ แล้วกู้คืน |

รายละเอียดกรอกใน [e2e-case-brief.md](resources/e2e-case-brief.md)

### 5.4 Host evidence — `ex06` and `ex15`

| หน้า | ท่อ | ใช้เป็นหลักฐาน |
|---|---|---|
| **`ex06_dashboard.html`** | Live Data | การ์ดหลายเซ็นเซอร์ · `route` · ค่า primary fields |
| **`ex15_ws_mqtt_dashboard.html`** | สลับ MQTT (`:8883`) / WebSocket (`:9998`) | แสดงว่าท่อ cloud-sim กับ bus คนละช่อง — เลือก transport ให้ตรงเดโม |

ขั้นตอนสั้นสำหรับหลักฐาน:

1. Serve Hackathon `web-app/`  
2. เปิด ex06 ระหว่าง Normal + Stimulus — แคปคู่กับ Studio  
3. Start broker → เปิด ex15 โหมด MQTT (หรือ ex09) ระหว่าง publish — แคป payload/กราฟ  
4. แนบไฟล์หลักฐานในโฟลเดอร์ผลงาน  

> ex15 ช่วยสอนผู้ชมว่า **WS bus ≠ MQTT broker** — อย่าสลับ transport กลางการสาธิตโดยไม่บอก

---

## 6. Deliverables and Documentation

### 6.1 What to submit

| ชิ้น | คำอธิบาย |
|---|---|
| โปรเจกต์ / ลิงก์ | เฟิร์มแวร์ + twin assets ที่ใช้ |
| **README** | วิธีรันซ้ำทีละขั้น (ดู §6.2) · ระบุโดเมนที่เลือก |
| [e2e-case-brief.md](resources/e2e-case-brief.md) | กรอกครบ 3 เคส + โดเมน |
| หลักฐานเดโม | สกรีนช็อต/คลิป Studio + ex06 และ/หรือ ex15/ex09 |
| (ถ้ามี) script / device model | จาก M03 ที่ล็อกเวอร์ชันแล้ว |

แผนที่เอกสารทั้งคอร์ส: [course-package.md](resources/course-package.md)

### 6.2 README outline (copy into your project)

```text
# <Project name> (Course 2 Capstone)
Domain: IoT | Home | Industrial | Health-sim | Other: …

## Hardware / path
Simulator | Board + HEX version | Studio version

## Bring-up
1. Open workspace …
2. Link backend (one only) …
3. Start broker (if MQTT) …
4. Serve web-app …

## Demo script
1. Normal — …
2. Stimulus — …
3. Command / fault — …

## Topics / payloads
(no passwords · no personal health identifiers)

## Known limits
…
```

### 6.3 Where to look when stuck

| ความต้องการ | ไปที่ |
|---|---|
| ตัวอย่างโค้ดเฟิร์มแวร์ / API | [Developer Hub](https://dev.tesaiot.dev/) |
| Host / broker / twin UI | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| HEX / VSIX / web-app | [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |
| MQTT บนบอร์ดจริง | [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) |
| Capstone ฝั่ง SDK อย่างเดียว | [Course 1 M08](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) |

---

## 7. After Course 2

หลังจบโมดูลนี้ คุณควรพาโปรเจกต์จากระดับ “รันบน Twin ได้” ไปสู่ระดับ **มีชุดทดสอบที่ทำซ้ำได้** และเล่าได้ว่าโดเมนไหนที่ท่อเดียวกันไปรองรับ

ทางเลือกถัดไปที่พบบ่อย:

| ทิศทาง | ทำอะไรต่อ |
|---|---|
| ยืนยันบนฮาร์ดแวร์เต็มรูป | กลับ [Course 1](../../../firmware-sdk-edge-ai/README.md) — flash · Wi‑Fi · MQTT/BLE จริง |
| ขยาย visualization / 3D | [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) + M03 Blender path |
| ขยาย cloud | broker ของแล็บ → นโยบายคลาวด์ขององค์กร (อย่า commit secret) |
| โดเมนเฉพาะ (โรงงาน / สุขภาพ) | ศึกษาข้อกำหนดจริงขององค์กร — Twin ในคอร์สเป็นสนามซ้อม ไม่แทนการรับรอง |

---

## Next Steps

1. เลือกโดเมนจาก §4 แล้วทำ [แล็บ](../l02-lab/README.md) — Capstone E2E  
2. กรอก [e2e-case-brief.md](resources/e2e-case-brief.md)  
3. ตรวจรายการส่งมอบด้วย [course-package.md](resources/course-package.md)  

---

## References and Further Reading

1. [M01](../../m01-twin-architecture/l01-twin-architecture/README.md)–[M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) · [Course 2 TOC](../../README.md)  
2. [Course 1 M08 Capstone](../../../firmware-sdk-edge-ai/m08-capstone/l01-capstone-and-resources/README.md) · [Course 1 M06 MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)  
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `web-app/ex06` · `ex15`  
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Case brief](resources/e2e-case-brief.md) · [Course package](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
