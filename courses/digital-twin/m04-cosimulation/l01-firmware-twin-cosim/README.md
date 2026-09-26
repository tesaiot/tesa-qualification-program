---
id: twin.m04.l01
lang: th
title:
  th: 'Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา'
  en: 'Co-simulation: Prove I/O, Measure Latency, Isolate Faults'
summary:
  th: bring-up ให้เสถียรก่อน พิสูจน์เส้นทาง input/output ใช้ web-app ภายนอกเป็นหลักฐานชั้นที่สอง วัด latency และไล่ปัญหาทีละชั้น
  en: Stable bring-up first, prove the input and output paths, use an external web-app as second-layer evidence, measure latency and debug layer by layer.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m03.l02
objectives:
- th: พิสูจน์เส้นทาง input (Twin → เฟิร์มแวร์) และ output (เฟิร์มแวร์ → Twin) ด้วยหลักฐานที่ตรวจตามรอยได้
  en: Prove the input path (Twin to firmware) and the output path (firmware to Twin) with traceable evidence.
- th: วัด latency คร่าว ๆ ซ้ำสามครั้ง และระบุแหล่งหน่วงที่น่าจะเป็น
  en: Measure rough latency three times and name the likely source of delay.
- th: ไล่แยกปัญหาฝั่งเฟิร์มแวร์กับฝั่งโฮสต์ทีละชั้น โดยเปลี่ยนตัวแปรครั้งละอย่าง
  en: Isolate firmware-side and host-side faults layer by layer, changing one variable at a time.
develops:
- skill: test.sil-hil
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: soft.problem-solving
  to: 2
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — Firmware–Twin Co-simulation

**Course 2 · Module 4**  
**Suggested time:** ประมาณ 3 ชั่วโมง (bring-up + I/O both ways + latency notes + optional web-app evidence)  
**Format:** บทเรียนเชิงปฏิบัติ — รันเฟิร์มแวร์คู่ Twin/Simulator แล้วพิสูจน์เส้นทางอินพุต–เอาต์พุตแบบมีหลักฐาน

[Lab](../l02-lab/README.md) · [Checklist](resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. เรียกใช้ / ทดสอบเฟิร์มแวร์ร่วมกับ **Virtual Device** หรือ **Simulator** (และ/หรือบอร์ดจริงผ่านโฮสต์) ได้อย่างเสถียร  
2. เชื่อมต่อ **Input/Output** ระหว่าง Firmware กับ Digital Twin ให้ตรวจตามรอยได้  
3. ตรวจสอบ **Timing / Latency** และข้อมูลแบบเรียลไทม์อย่างมีหลักฐาน  
4. แยกปัญหาฝั่งเฟิร์มแวร์ vs ฝั่งโฮสต์/Twin ได้อย่างเป็นระบบ  
5. ใช้ **consumer ชั้นนอก** (Hackathon live web-app) เป็นหลักฐานว่าท่อข้อมูลไม่ติดอยู่แค่แผงเดียวใน Studio  

โมดูลนี้ต่อจาก [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) ที่คุณมี Virtual Device + สคริปต์เหตุการณ์แล้ว — ตอนนี้เอา **โค้ดเฟิร์มแวร์จริง** มาวิ่งคู่กับ Twin เพื่อพิสูจน์วงจรครบก่อนขยายไป telemetry/cloud ใน [M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

> **Key phrase**  
> Co-simulation = *เฟิร์มแวร์คิดและตอบ* ในเวลาเดียวกับที่ Twin *กระตุ้นและแสดงผล* — ไม่ใช่แค่เปิดกราฟดูค่า

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M02 — VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | Link Studio / Simulator / COM |
| [M03 — Virtual Device](../../m03-virtual-device/l01-virtual-device-modeling/README.md) | โมเดลเซ็นเซอร์ + event script ที่จะกระตุ้นซ้ำ |
| [Course 1 M04 — RTOS](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) | task / delay ที่ส่งผลต่อ timing |
| [Course 1 M05 — Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | ความหมายค่าที่ไหลใน co-sim |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | โฮสต์ visualization + Link |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX จับคู่ VSIX · โฟลเดอร์ **`web-app/`** (ตัวอย่าง live HTML) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ / API |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | โมเดล 3D ประกอบ visualization (ถ้าใช้) |

---

## 1. What Co-simulation Means Here

ใน Course 2 **Firmware–Twin Co-simulation** หมายถึง:

การให้ **ตรรกะเฟิร์มแวร์** ทำงานคู่กับ **สภาพแวดล้อม Twin / Simulator / โฮสต์** ในช่วงเวลาเดียวกัน เพื่อพิสูจน์ว่าโค้ด:

- อ่านอินพุตจำลอง (หรือจากบอร์ดผ่านโฮสต์) ได้ถูกต้อง  
- ตัดสินใจตาม behavior ที่ออกแบบใน M03  
- ขับเอาต์พุตที่สังเกตได้บน Twin / UI / LED / **หน้า web consumer**  

| ไม่ใช่ | คือ |
|---|---|
| แทน unit test ทั้งหมด | สะพานก่อน / คู่กับบอร์ดจริง |
| แค่เปิด Simulator แล้วดู sine | กระตุ้น → เห็น logic ตอบ |
| ผสม UART + Simulator ใน UI เดียว | เลือก **หนึ่ง** backend ตาม [M01](../../m01-twin-architecture/l01-twin-architecture/README.md) |
| เชื่อแค่แผงเดียวใน Studio | ยืนยันซ้ำด้วย consumer อื่นได้ (เช่น `web-app/ex05`) |

### 1.1 Two practical lab paths

| Path | Firmware runs on | Twin / host role |
|---|---|---|
| **A — Simulator** | Virtual MCU (Bitstream Simulator) | Studio แสดงค่า `origin: sim` |
| **B — Board + Host** | DevKit จริง (HEX / build ของคุณ) | Studio แสดงค่า `origin: uart` |

ทั้งสอง path นับเป็น co-sim กับโฮสต์ Twin ได้ — ต่างกันที่แหล่งอินพุตฮาร์ดแวร์

```text
Path A:  [Simulator firmware] ──WS──► [Bridge] ──► [Bitstream Studio]
Path B:  [MCU firmware] ──UART──► [Bridge] ──► [Bitstream Studio]
                      ▲
                      └── same observe / command habits as Twin lab
```

### 1.2 Three places you may observe the same stream

| ชั้นสังเกต | ตัวอย่าง | ใช้พิสูจน์อะไร |
|---|---|---|
| ใน Studio | Telemetry / BMI270 / 3D rotation | โฮสต์ decode + UI ทำงาน |
| บนบอร์ด / log | LED, UART print | เฟิร์มแวร์ตัดสินใจจริง |
| นอก Studio | Hackathon **`web-app/`** HTML | ท่อ Live Data ไปถึง consumer ทั่วไป (ไม่ผูกแผงเดียว) |

ถ้าทั้งสามชั้น (หรืออย่างน้อย Studio + web-app) เห็นการเปลี่ยนแปลงสอดคล้องกันหลังกระตุ้น — คุณมีหลักฐาน co-sim ที่แข็งกว่า “แคปกราฟแผงเดียว”

---

## 2. Bring-up: Stable Session First

ก่อนวัด I/O หรือ latency ให้มี **heartbeat ทั้งสองฝั่ง**

### 2.1 Checklist bring-up

1. เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) จาก workspace ที่ผูกแล้ว (M02)  
2. เลือก backend: **Simulator** *หรือ* **Bitstream** (ไม่ผสม)  
3. Link / Connect จนสถานะปกติ  
4. เห็นสตรีมเซ็นเซอร์หรือ log อย่างน้อยหนึ่งช่อง  
5. (Path B) ยืนยัน HEX/VSIX เวอร์ชันจับคู่จาก [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  

**ผ่านเมื่อ:** เซสชันนิ่ง ≥ 30–60 วินาที โดยไม่หลุด Link เอง

### 2.2 What “firmware on Virtual Device” means in this course

เอกสารหลักสูตรพูดถึงการรันเฟิร์มแวร์บน Virtual Device — ในแล็บมักหมายถึงอย่างใดอย่างหนึ่ง:

| ความหมาย | สิ่งที่คุณทำ |
|---|---|
| Simulator เป็นตัวแทน MCU | Start Simulator + Link |
| เฟิร์มแวร์บนบอร์ดคุยกับ Twin host | Flash + COM + Link |
| โปรไฟล์/พอร์ตจำลองของชุดที่ใช้ | ตามคู่มือของชุดที่ใช้ ถ้ามีชั้น abstraction พิเศษ |

อย่าสมมติว่าทุก API ฮาร์ดแวร์มี twin stub อัตโนมัติ — ถ้าไดรเวอร์ผูกซิลิคอนอย่างเดียว ให้ใช้โปรไฟล์ที่ชุดแล็บจัดให้ หรือทดสอบเฉพาะเส้นทางที่มีบนโฮสต์ (telemetry, command topics, LED ที่เห็นใน UI)

---

## 3. Connecting Inputs and Outputs

เส้นทางที่ต้องพิสูจน์ให้ชัด:

```text
[Stimulus]
  event script / UI / scene change / physical button / tilt board
        │
        ▼
[Sensor or pin value]     ← Virtual Device (M03) or real sensor
        │
        ▼
[Firmware read path]      ← task / driver / SENSOR_CFG
        │
        ▼
[Firmware decision]       ← behavior WHEN/THEN
        │
        ▼
[Firmware write path]     ← LED / flag / publish / log
        │
        ▼
[Twin / Studio / web-app observe]
```

### 3.1 Input path (Twin → Firmware)

| ขั้น | หลักฐานที่รับได้ |
|---|---|
| กระตุ้นจากสคริปต์ M03 หรือ UI | โน้ตเวลา + สกรีนช็อตก่อน |
| ค่าเข้าเฟิร์มแวร์ | UART log / ตัวแปร / การเปลี่ยนโหมด |
| ค่าสอดคล้องชนิดเซ็นเซอร์ | เทียบหน่วยกับ [C1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) |

ตัวอย่างการกระตุ้นที่ใช้บ่อย:

- สลับ scene **Lab Quiet → Motion** (IMU path)  
- กดปุ่มบนบอร์ดหรือคำสั่งโฮสต์  
- ทำตาม timeline ใน M03 event script  
- (บอร์ดจริง) เอียง / หมุนบอร์ดเพื่อให้ BMI270 fusion เปลี่ยน  

### 3.2 Output path (Firmware → Twin)

| ขั้น | หลักฐานที่รับได้ |
|---|---|
| เฟิร์มแวร์ตัดสินใจแล้วสั่งเอาต์พุต | log บรรทัดคำสั่ง / LED GPIO |
| Twin หรือ Studio สะท้อนสถานะ | กราฟ / แผง / 3D / dashboard |
| Consumer ชั้นนอกสะท้อนสถานะ | Hackathon `web-app/` (ดู §4) |
| Behavior จาก M03 ตรงกับที่เห็น | WHEN/THEN ใน checklist |

เกณฑ์ความสำเร็จเบื้องต้น:

1. ค่าที่กระตุ้นจาก Twin/สคริปต์ **ไปถึง** พฤติกรรมเฟิร์มแวร์  
2. คำสั่งจากเฟิร์มแวร์ **ทำให้** สถานะบนโฮสต์เปลี่ยนตามที่คาด  

### 3.3 Why an external web-app helps

แผงใน Bitstream Studio อาจ “ดูถูก” เพราะคุณกำลังทดสอบโฮสต์ตัวเดียวกันที่ decode สตรีมอยู่แล้ว  
หน้า HTML ใน **`TESAIoT_Hackathon/web-app/`** เป็น **client อิสระ** ที่ต่อ Live Data provider ของ Studio — ถ้ามันอัปเดตตามการเอียงบอร์ดหรือ scene Motion แสดงว่า:

- bridge / provider เปิดอยู่  
- sensor id และ fields ถูก publish  
- ท่อข้อมูลไม่พังเฉพาะ UI ภายใน extension  

ส่วนถัดไปเดินตัวอย่างหนึ่งแบบละเอียด: **`ex05_bmi270_orientation.html`**

---

## 4. Walkthrough — Hackathon web-app `ex05` (BMI270 orientation)

ตัวอย่างนี้เป็น **artificial horizon + Euler angles** จากเซ็นเซอร์ **BMI270** — เหมาะกับ M04 เพราะ:

- เห็น **output path** ชัด (fusion → องศา → ภาพ horizon)  
- บังคับให้ตั้ง **publish mask** ถูก (Euler หรือ Quaternion) — ฝึกแยก “มีสตรีมแต่ fields ผิด”  
- แสดง **connection state** และ **route** — ช่วยยืนยัน backend เดียวกับที่ Studio ใช้  

ไฟล์อยู่ที่รีโป [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) ภายใต้โฟลเดอร์ **`web-app/`**:

- `web-app/ex05_bmi270_orientation.html`  
- ใช้ร่วมกับ `web-app/shared/ex-demo.js` (ตัวช่วย `TelemetryClient`, `resolveOrientation`, `drawHorizon`)  

แผนที่ตัวอย่างอื่น (ไว้ดูคร่าว ๆ — รายละเอียด MQTT ไป M05):

| ไฟล์ | บทบาทสั้น ๆ |
|---|---|
| `ex04_bmi270_imu.html` | accel/gyro ดิบ — ยังไม่ใช่ orientation |
| **`ex05_bmi270_orientation.html`** | **M04 — fusion → horizon (ตัวอย่างหลักของบทนี้)** |
| `ex06_dashboard.html` | หลายเซ็นเซอร์บนจอเดียว |
| `ex08_stale_and_route.html` | stale + route (เตรียม M05) |

### 4.1 How to open it (lab flow)

1. ให้ Bitstream Studio **Link** แล้ว และมีสตรีม BMI270 (Path A หรือ B — อย่าผสม)  
2. Clone หรือเปิดโฟลเดอร์ Hackathon ที่มี **`web-app/`**  
3. ใน VS Code / Studio: ใช้คำสั่งประมาณ **Serve Web App Folder over HTTP** (หรือ static server อื่นที่คุณถนัด) แล้วชี้ไปที่โฟลเดอร์ `web-app/`  
4. เปิด `index.html` → เลือก **ex05 — BMI270 Orientation**  
5. ดู badge มุมบน: ควรไปที่ `connected` และมีข้อความประมาณ `route: …` เมื่อเชื่อมสำเร็จ  

ถ้าขึ้นข้อความแนว *provider not reachable* — ยังไม่ได้ start bridge / Studio services (กลับไป bring-up §2)

### 4.2 Prerequisites on the sensor mask

หน้า ex05 เขียนไว้ชัดว่า **accel/gyro อย่างเดียวไม่พอ**

ต้องเปิดใน sensor settings (Virt MCU / Bitstream) ให้ BMI270 publish อย่างน้อยหนึ่งชุดนี้:

| ชุด fields | ผลบนหน้าเว็บ |
|---|---|
| **Euler:** `headingRad`, `pitchRad`, `rollRad` | `resolveOrientation` ใช้ทันที · แสดง `source: euler` |
| **Quaternion:** `quatW` … `quatZ` | แปลงเป็น Euler ใน `ex-demo.js` · แสดง `source: quaternion` |

ถ้า mask มีแต่ accel/gyro:

- Studio อาจยังมีกราฟ IMU  
- แต่ horizon ของ ex05 จะค้างที่ *waiting for orientation fields…*  

นี่คือตัวอย่าง **fault isolation** ที่ดี: สตรีมมี แต่ consumer เงียบเพราะ **fields ไม่ตรงสัญญา** — ไม่ใช่เพราะ “web-app พัง”

### 4.3 What you see on the page

| ส่วน UI | ความหมายใน co-sim |
|---|---|
| `#state` / `#route` | Provider เชื่อมได้หรือยัง · route ที่ client รับ (สัมพันธ์ backend) |
| Artificial horizon (canvas) | visualization ของ pitch + roll |
| Heading / Pitch / Roll (°) | ค่าตัวเลขจาก sample ล่าสุด |
| `source: euler \| quaternion` | fields มาจากชุดไหน |
| `mask 0x…` | ยืนยันว่า publish mask ตรงกับที่ตั้ง |
| การไฮไลต์ **stale** | ไม่มี sample ใหม่ภายใน `staleAfterMs` ของ catalog |

### 4.4 Data path (same stream, second screen)

```text
[Stimulus: tilt board / Motion scene / M03 script]
        │
        ▼
[BMI270 on MCU or Simulator]  →  fusion / publish per SENSOR_CFG mask
        │
        ▼
[Bridge]  →  Bitstream Studio (decode + optional 3D)
        │
        └──► Live Data provider
                    │
                    ▼
         [TelemetryClient in ex05]
                    │
                    ▼
         onSensor('bmi270') → resolveOrientation → drawHorizon + ° text
```

เทียบกับแผนภาพ §3: ex05 คือชั้นสุดท้าย **[Twin / Studio / web-app observe]** แบบ consumer ภายนอก

### 4.5 How the page code works (teaching view)

โครงสำคัญใน `ex05_bmi270_orientation.html` (ย่อความ — ดูไฟล์จริงใน Hackathon):

1. **โหลด SDK** — `loadSdk()` ได้ `TelemetryClient` และ catalog entry ของ `bmi270`  
2. **ติดตาม stale** — `createStaleTracker(imu.staleAfterMs, …)` เปลี่ยนคลาสการ์ดเมื่อข้อมูลเก่า  
3. **badge การเชื่อมต่อ** — `wireConnectionBadge(client, stateEl, routeEl)`  
4. **สมัครเซ็นเซอร์** — `client.onSensor('bmi270', (s) => { … })`  
5. **แปลง orientation** — `resolveOrientation(s.fields)`  
   - มี Euler ครบ → ใช้เลย (`source: 'euler'`)  
   - ไม่มี Euler แต่มี quat → `quatToEuler` (`source: 'quaternion'`)  
   - ไม่ครบ → `null` (ไม่วาด)  
6. **วาด + แสดงตัวเลข** — `drawHorizon(ctx, canvas, pitch, roll)` และแปลงเรเดียน → องศา  
7. **connect** — `await connectTelemetry(client, routeEl)`  

แนวคิดที่ควรจำ:

```text
Studio Link  ≠  web-app connected
มี BMI270 raw  ≠  มี orientation fields
horizon ขยับ      =  output path ถึง consumer ชั้นนอกแล้ว
```

### 4.6 Map ex05 onto M04 I/O proofs

| คำถาม M04 | ทำอะไรกับ ex05 |
|---|---|
| **Input** ถึงเฟิร์มแวร์ไหม? | เอียงบอร์ด / สลับ scene Motion แล้วดูว่าค่า ° เปลี่ยน (คู่กับ UART log ถ้ามี) |
| **Output** โฮสต์สะท้อนไหม? | horizon + ตัวเลขขยับ; แคปคู่กับแผง BMI270 ใน Studio |
| **Latency**? | จับเวลาจากเริ่มเอียงจนตัวเลขบน ex05 เปลี่ยน (ทำ 3 รอบ) — มักช้ากว่า log นิดหน่อยเพราะ WS + UI |
| **Fault** ที่ไหน? | ดูตารางด้านล่าง |

| อาการบน ex05 | น่าสงสัย |
|---|---|
| `disconnected` / provider not reachable | Bridge / Studio services (§2) |
| `connected` แต่ waiting for orientation… | Mask ไม่มี Euler/Quat (§4.2) |
| ตัวเลขค้าง + การ์ด stale | สตรีมหยุด / เฟิร์มแวร์ไม่ publish / หลุด Link |
| Studio มี orientation แต่ ex05 ไม่ขยับ | เปิดผิดโฟลเดอร์ serve · tab เก่า · client ไม่ได้ connect |
| Simulator ปกติ บอร์ดไม่ขยับ | Path B: HEX / COM / ฮาร์ดแวร์ |

### 4.7 Evidence to keep for the checklist

บันทึกลง `lab-notes/` (หรือ checklist):

1. สกรีนช็อต Studio (Link + BMI270) **คู่กับ** หน้า ex05 ที่ `connected` และ horizon มีค่า  
2. บรรทัด `source: … · mask 0x…`  
3. โน้ตสั้น ๆ: กระตุ้นอย่างไร → ° เปลี่ยนอย่างไร  
4. (แนะนำ) ช่วงเวลา latency คร่าว ๆ 3 รอบ  

> **Key phrase**  
> ex05 ไม่ได้แทน unit test เฟิร์มแวร์ — มันคือ **กระจกชั้นที่สอง** ว่า publish ของ BMI270 ไปถึงโลกนอก Studio หรือยัง

---

## 5. Timing, Latency, and Real-time Observation

เป้าหมายของ M04 **ไม่ใช่** ตัวเลข latency ที่สวยที่สุด แต่คือการ **วัดและชี้แหล่งหน่วง** โดยไม่เดา

### 5.1 Simple measurements to record

| การวัด | วิธีคร่าว ๆ | จดอะไร |
|---|---|---|
| Stimulus → firmware log | จับเวลาจากกระตุ้นจนมีบรรทัด log | มิลลิวินาทีโดยประมาณ |
| Firmware act → Studio UI | จาก log จนกราฟ/LED บน Studio เปลี่ยน | มิลลิวินาทีโดยประมาณ |
| Firmware act → web-app (ex05) | จาก log / เริ่มเอียงจน ° บนหน้าเว็บเปลี่ยน | มิลลิวินาทีโดยประมาณ |
| Sample period | ดูอัตรา scene / SENSOR_CFG | Hz หรือ ms |

ทำซ้ำ 3 ครั้งแล้วจดช่วงค่า (min–max) — พอสำหรับแล็บ

ลำดับที่มักเห็น: **log เร็วสุด → Studio ใกล้เคียง → web-app ช้ากว่าเล็กน้อย** (ยังอยู่ในช่วงที่ยอมรับได้ถ้าสม่ำเสมอ)

### 5.2 Where latency usually comes from

| แหล่ง | สัญญาณ |
|---|---|
| RTOS task period / `vTaskDelay` | ค่ากระโดดตามคาบ |
| Sensor publish interval | scene Lab Quiet ช้ากว่า Motion |
| Bridge / WS / UI refresh | UI / web-app ช้ากว่า log |
| Human reaction when timing by eye | ค่ากระจายมาก — ใช้วิดีโอหรือ timestamp ใน log ถ้าเป็นไปได้ |

ทบทวน RTOS: [Course 1 M04](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md)

### 5.3 Real-time observation habits

1. เปิด **Telemetry** (หรือแผงที่กำหนด) คู่กับ **UART/Output log**  
2. (แนะนำ) เปิด **ex05** เป็นจอ consumer คู่ขนาน  
3. อย่าเปลี่ยน backend กลางการจับเวลา  
4. บันทึกสกรีนช็อตพร้อมนาฬิกาหรือหมายเลขรอบ  
5. ถ้าใช้ 3D / GLB จาก M03 — ยืนยันว่า animation/ภาพไม่ทำให้เข้าใจผิดว่าเป็น sensor truth  

แบบฟอร์ม: [cosim-checklist.md](resources/cosim-checklist.md)

---

## 6. Isolating Faults (Firmware vs Host)

เมื่อ co-sim พัง ให้ไล่ชั้นตามนี้:

```text
1. Extension / backend up?          → M02
2. Correct source (sim XOR uart)? → M01/M02
3. Stream present at all?
4. Stimulus actually applied?       → M03 script / tilt / scene
5. Firmware log shows read?
6. Firmware log shows write/decision?
7. Studio UI shows change?
8. web-app (ex05) shows change?     → mask / provider / serve
```

| อาการ | น่าสงสัยฝั่ง |
|---|---|
| ไม่มีสตรีมเลย | Host / Link / Simulator / COM |
| มีสตรีมแต่กระตุ้นแล้วเฟิร์มแวร์เงียบ | Input mapping / cfg / task |
| เฟิร์มแวร์ log ถูกแต่ UI ไม่ขยับ | Visualization / wrong panel / consumer |
| Studio ถูกแต่ ex05 waiting… | Publish mask (Euler/Quat) |
| บอร์ดอย่างเดียวพัง Simulator ปกติ | ฮาร์ดแวร์ / HEX / สาย |
| Simulator พัง บอร์ดปกติ | Sim VSIX / route |

> **Key phrase**  
> แก้ทีละชั้น — อย่าเปลี่ยนเฟิร์มแวร์และโหมด Studio พร้อมกันในรอบดีบักเดียว

---

## 7. How M04 Feeds M05 and M06

| หลัง M04 คุณมี | ใช้ต่อที่ |
|---|---|
| วงจร I/O พิสูจน์แล้ว | M05 — จัดรูปแบบ telemetry / MQTT |
| บันทึก latency / ประเด็น | M06 — E2E และรายงาน |
| สคริปต์ M03 ที่รันคู่เฟิร์มแวร์ได้ | regression เมื่อแก้โค้ด |
| ความคุ้นกับ `web-app/` + route badge | M05 ตัวอย่าง stale/route และ MQTT (ex08+) |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md) — รวมขั้นตอน optional เปิด **ex05**  
2. กรอก [cosim-checklist.md](resources/cosim-checklist.md)  
3. เมื่อพร้อม ไปต่อ [M05 — Telemetry and Cloud Simulation](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## References and Further Reading

1. [M02 VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M03 Virtual Device](../../m03-virtual-device/l01-virtual-device-modeling/README.md)  
2. [Course 1 M04 RTOS](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) · [Course 1 M05 Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)  
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — โดยเฉพาะ `web-app/ex05_bmi270_orientation.html`  
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**  
7. [Course 2 TOC](../../README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: I/O ครบวงจรแบบ co-simulation](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
