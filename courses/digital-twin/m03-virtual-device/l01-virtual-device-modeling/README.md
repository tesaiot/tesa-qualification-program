---
id: twin.m03.l01
lang: th
title:
  th: Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin
  en: Virtual Devices, Behaviours, Event Scripts and 3D Models for the Twin
summary:
  th: กำหนดโมเดลอุปกรณ์ เซ็นเซอร์ พฤติกรรม และสคริปต์เหตุการณ์ตามเวลา แล้วเตรียมโมเดล 3D ใน Blender ให้ส่งออกเป็น GLB สำหรับ Twin
  en: Define the device model, sensors, behaviours and timed event scripts, then prepare a Blender 3D model for export to GLB for the Twin.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: true
  boards:
  - none
prerequisites:
- twin.m02.l02
objectives:
- th: กำหนด Virtual Device Model ที่มี identity เซ็นเซอร์อย่างน้อยสองชนิด (พร้อม unit, default, min/max) และเอาต์พุตที่สังเกตได้
  en: Define a Virtual Device Model with an identity, at least two sensors (unit, default, min/max) and an observable output.
- th: เขียน behavior แบบ WHEN/THEN ที่ทดสอบได้ทั้งขาเข้าและขาออก และไทม์ไลน์ event script ที่รันซ้ำได้
  en: Write a WHEN/THEN behaviour that is testable on input and output, and a repeatable event-script timeline.
- th: ระบุเงื่อนไขของโมเดล 3D ที่พร้อมใช้กับ Twin (สเกลจริง origin ชัด UV พร้อม) และขั้นตอนส่งออกเป็น glTF Binary (.glb)
  en: State what makes a 3D model Twin-ready (real scale, clear origin, UVs) and the steps to export glTF Binary (.glb).
develops:
- skill: iot.digital-twin
  to: 2
- skill: sys.simulation
  to: 2
- skill: test.sil-hil
  to: 1
- skill: hwdev.3d-modeling
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — Virtual Device Modeling

**Course 2 · Module 3**  
**Suggested time:** ประมาณ 4–5 ชั่วโมง (Virtual Device + behavior/script + แนะนำ Blender สำหรับ Twin 3D)  
**Format:** บทเรียนเชิงปฏิบัติ — ออกแบบ Virtual Device + พื้นฐาน Blender (Modeling / Texturing / Animation) เพื่อ visualization บน Twin

[Lab](../l02-lab/README.md) · [Device checklist](resources/device-model-checklist.md) · [Blender cheatsheet](resources/blender-twin-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

> **หมายเหตุ:** ตารางในบทนี้อ้างปุ่ม scene ใน `ble-flet` ของ TESAIoT_Hackathon แต่ [README ของ repo นั้น](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) ระบุว่า `ble-flet/` ไม่ได้เผยแพร่ ให้ใช้แผงใน Bitstream Studio แทน (ตรวจสอบเมื่อ 26 ก.ย. 2026)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. สร้างและกำหนดค่า **Virtual Device Model** ให้สะท้อนบอร์ดเป้าหมายของหลักสูตร  
2. จำลองเซ็นเซอร์สำคัญ เช่น **IMU, Temperature, Pressure, Switches**  
3. กำหนด **Behavior Simulation** ให้เส้นทางอินพุต→สถานะตรวจสอบได้  
4. เขียน **Event Simulation Script** ที่รันซ้ำได้สำหรับ regression / การสาธิต  
5. อธิบายบทบาท **Blender** ในการสร้างโมเดล 3D สำหรับ Twin: **Modeling, Texturing, Animation** และเส้นทาง **export glTF/GLB**  
6. ใช้เอกสารออนไลน์ (Blender Manual / Fundamentals / [Tutorial ภาษาไทย](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)) และ [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) เพื่อศึกษาต่อด้วยตนเอง  

โมดูลนี้ต่อจาก [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) ที่โฮสต์พร้อมแล้ว — ตอนนี้คุณจะ**ออกแบบสิ่งที่ Twin จำลอง** (ข้อมูล + รูปทรง 3D) ก่อนพาเฟิร์มแวร์มา co-sim ลึกใน [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

> **แนวทาง “โมเดลบนกระดาษ + รันบนเครื่องมือจริง + เตรียม 3D”**  
> Virtual Device Configuration อธิบาย *พฤติกรรม/เซ็นเซอร์*  
> **Blender** เตรียม *เปลือกภาพ* ที่ Twin / Sensor Studio แสดง — หลักสูตรที่ 3 จะลงลึกงานออกแบบอุตสาหกรรม; ที่นี่เน้นทักษะพอสำหรับ Course 2

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M01 — Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) | Virtual Device อยู่ชั้นไหนของแพลตฟอร์ม |
| [M02 — VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | เปิด Simulator / Bitstream Studio ก่อนแล็บนี้ |
| [Course 1 M05 — Sensor prep](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | ชนิดเซ็นเซอร์และความหมายของค่า |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | โฮสต์ดูผลหลังตั้งโมเดล/ซีน |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `ble-flet` scene presets · `web-app/` |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | โมเดล GLB / texture / รูป สำหรับ Twin |
| **[Blender Manual 4.5 LTS](https://docs.blender.org/manual/en/4.5/)** | คู่มือทางการ Modeling / Materials / Animation |
| **[Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | คอร์สวิดีโอทางการจาก Blender Studio (อังกฤษ) |
| **[INC111-2021 Blender playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Tutorial ภาษาไทยบน YouTube — แนะนำสำหรับผู้เรียนที่ต้องการคำอธิบายภาษาไทย |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเซ็นเซอร์ฝั่งเฟิร์มแวร์ |
| [ตัวอย่างโมเดลแนวคิด](resources/sample-virtual-device.template.json) | โครง JSON สำหรับแผ่นผลงาน |
| [Blender cheatsheet](resources/blender-twin-cheatsheet.md) | ลิงก์ด่วน Modeling / Texturing / Animation / glTF |

---

## 1. What Is a Virtual Device Model

**Virtual Device Model** คือคำอธิบายซอฟต์แวร์ของอุปกรณ์หนึ่งเครื่องในโลก Twin โดยอย่างน้อยควรระบุ:

| ส่วน | คำถามที่ต้องตอบได้ |
|---|---|
| **Identity** | ชื่อ / รหัสอุปกรณ์คงที่สำหรับอ้างในรายงาน |
| **Sensors** | มีตัวอะไร · หน่วย · ค่าเริ่มต้น · ช่วงที่ยอมรับ |
| **Actuators / outputs** | LED, flag, log — สิ่งที่สังเกตผลได้ |
| **Noise / dynamics (ถ้ามี)** | ค่ากระโดดหรือมีสัญญาณรบกวนจำลองหรือไม่ |
| **Behaviors** | เมื่ออินพุต/คำสั่งเกิด แล้วสถานะเปลี่ยนอย่างไร |
| **Events / scripts** | สถานการณ์ตามเวลาที่รันซ้ำได้ |

โมเดล**ไม่ต้อง**จำลองทุกบล็อกในซิลิคอน — ต้อง**เพียงพอต่อการทดสอบ logic เฟิร์มแวร์**ตามโจทย์ของแล็บ

| หยาบเกินไป | ละเอียดเกินจำเป็น |
|---|---|
| เทสไม่สะท้อนพฤติกรรมจริง | เสียเวลาตั้งค่าโดยไม่ได้เพิ่มการเรียนรู้ |

> **Key phrase**  
> Virtual Device คือ *ข้อตกลง* ระหว่างสคริปต์เทสของคุณกับ Twin — ไม่ใช่ datasheet ทั้งเล่ม

### 1.1 Conceptual model document

เก็บโมเดลเป็นเอกสารที่ทีมอ่านซ้ำได้ — ตัวอย่างโครงใน [sample-virtual-device.template.json](resources/sample-virtual-device.template.json):

```json
{
  "deviceId": "tesa-edge-demo-01",
  "displayName": "TESA Edge Demo Device",
  "sensors": [
    { "id": "temp", "type": "temperature", "unit": "C", "default": 25.0, "min": -10.0, "max": 85.0 },
    { "id": "btn_user", "type": "switch", "default": 0 },
    { "id": "imu", "type": "imu", "axes": ["ax", "ay", "az"], "default": [0, 0, 1] }
  ],
  "actuators": [
    { "id": "led_status", "type": "led", "default": 0 }
  ],
  "behaviors": [
    { "when": "command.led == on", "then": "actuators.led_status = 1" },
    { "when": "sensors.temp > 40", "then": "emit event threshold_exceeded" }
  ]
}
```

> ไฟล์นี้เป็น **template แนวคิดสำหรับเรียน** — ฟิลด์จริงของเครื่องมืออาจชื่อต่างกัน ให้ map เข้า Simulator / scene / SENSOR_CFG ตามชุดที่ใช้

### 1.2 How the lab stack realizes the model

| ส่วนในโมเดล | สิ่งที่มักใช้รันจริงในคอร์สนี้ |
|---|---|
| Sensor list + rates | **SENSOR_CFG** / **scene presets** (Motion, Lab Quiet, Environment, …) |
| Continuous IMU / env values | **Bitstream Simulator** stream หรือบอร์ดจริง |
| Identity | ชื่ออุปกรณ์ / MAC topic / `deviceId` ในรายงาน |
| Behavior (command → output) | คำสั่งโฮสต์ / MQTT actuator / LED บนบอร์ดหรือ UI |
| Timed event script | ไทม์ไลน์ใน checklist + สลับซีน / กระตุ้นด้วยมือ / สคริปต์ตามเครื่องมือที่มี |

---

## 2. Modeling Sensors

### 2.1 Sensor families in this course

| ชนิด | ค่าที่มักจำลอง | เหมาะทดสอบ |
|---|---|---|
| **IMU** (เช่น BMI270) | accel / gyro (และ fusion ตามโหมด) | gesture, activity, orientation |
| **Temperature / Humidity** (เช่น SHT40) | สเกลาร์ต่อเนื่อง | threshold, calibration path |
| **Pressure** (เช่น DPS368) | สเกลาร์ต่อเนื่อง | environmental monitor |
| **Magnetometer** (เช่น BMM350) | แกนสนาม | heading / fusion lab |
| **Switches / buttons** | 0/1 หรือ edge | UI logic, debounce |

แนะนำลำดับเรียน:

1. สวิตช์ + อุณหภูมิ (สังเกตผลชัด)  
2. เพิ่ม IMU เมื่อท่อข้อมูลพร้อม  
3. รวม env sensors เป็นชุด monitor  

ทบทวนความหมายค่า: [Course 1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

### 2.2 Rates and scenes (practical knobs)

แทนการเปิดเผยทุกฟิลด์ wire ทันที โฮสต์แล็บมักมี **scene presets** ระดับ use-case:

| Scene (ตัวอย่างในแพ็กแล็บ) | ความหมายโดยประมาณ |
|---|---|
| **Motion** | IMU หนาแน่นขึ้น · env ช้า — เหมาะ posture / motion |
| **Realtime** | อัตราสูงขึ้นสำหรับดูรายละเอียดสั้น ๆ |
| **Lab Quiet** | ~1 Hz ทั้งชุด — ดีต่อการสาธิต / ประหยัด |
| **Environment** | เน้น SHT/DPS · ปิดหรือลด IMU |

ใน Bitstream / BLE labs การ apply scene มักหมายถึงชุด **SENSOR_CFG** (+ โหมด BMI270 / fusion ตามเครื่องมือ) — ผู้เรียนโฟกัสว่า *โมเดลต้องการโปรไฟล์ไหน* ไม่ต้องท่องทุกมิลลิวินาทีในวันแรก

### 2.3 Defaults, ranges, and honesty

เมื่อกรอกโมเดล ให้ระบุ:

| ฟิลด์ | ทำไมสำคัญ |
|---|---|
| `default` | ค่าตอนเริ่มสคริปต์ / ก่อนกระตุ้น |
| `min` / `max` | กันเทสที่อยู่นอกโลกจริงโดยไม่ตั้งใจ |
| unit | กันสับสน °C / Pa / g |
| “sim vs real” | ค่าจาก Simulator เป็น sine/สังเคราะห์ — ไม่ใช่ noise บอร์ดจริง |

---

## 3. Behavior Simulation

**Behavior** คือกฎที่บอกว่าเมื่อเกิดอินพุตหรือคำสั่งแล้ว อุปกรณ์จำลอง (หรือเฟิร์มแวร์+โฮสต์) จะตอบสนองอย่างไร

### 3.1 Patterns worth practicing

| แบบ | ตัวอย่าง | สังเกตผลที่ |
|---|---|---|
| **Command → actuator** | `led=on` → LED สถานะเปิด | UI / บอร์ด / log |
| **Sensor → event** | `temp > 40` → `threshold_exceeded` | event panel / MQTT / UART |
| **Switch → mode** | กดปุ่ม → เปลี่ยนโหมด publish | toolbar / stream rate |
| **Host write → device** | คำสั่งจาก Studio/MQTT | เฟิร์มแวร์ตอบสนอง |

เขียน behavior ให้ **ทดสอบได้ทั้งขาเข้าและขาออก** — ถ้ามีแต่ “ค่าขยับ” โดยไม่มีข้อตกลงว่าควรเกิดอะไร จะวัดไม่ได้ว่า logic ถูก

### 3.2 Keep behaviors small

ใน M03 ขออย่างน้อย **1 เส้นทาง** ที่เขียนเป็นประโยคชัด เช่น:

```text
WHEN user_button rising edge
THEN led_status = ON for 1 s AND log "btn"
```

หรือ:

```text
WHEN temperature > 40 °C for 2 s
THEN emit event "temp_high"
```

ขยายจำนวน behavior ใน M04/M06 เมื่อ co-sim และ E2E พร้อม

---

## 4. Event Simulation Scripts

**Event Simulation Script** ใช้สร้างสถานการณ์ตามเวลา ให้ regression และการสาธิตทำซ้ำได้

### 4.1 Timeline example

```text
t = 0–2 s   : idle (defaults)
t = 2–5 s   : temperature ramp +0.5 °C / step
t = 5.0 s   : press virtual switch ~200 ms
t = 6.0 s   : short IMU shake pulse
t = 7–10 s  : observe outputs / events
t = 10 s    : stop or loop
```

### 4.2 How to “run” a script in the lab

เลือกอย่างน้อยหนึ่งวิธีตามเครื่องมือที่มี:

| วิธี | เมื่อใช้ |
|---|---|
| **Manual timeline** | ทำตามนาฬิกา + โน้ต — ผ่านเกณฑ์ M03 ได้ |
| **Scene switch** | เริ่ม Lab Quiet → สลับ Motion ตอน t=6 เพื่อกระตุ้น IMU path |
| **Host / app controls** | ปุ่ม scene ใน `ble-flet` หรือแผง Studio |
| **Formal script file** | ถ้า Twin tooling ของรอบนั้นรองรับไฟล์สคริปต์ — แนบ path สัมพัทธ์ใน checklist |

สำคัญคือ **ลำดับเหตุการณ์ + ผลที่คาด + หลักฐาน** ไม่ใช่ภาษาสคริปต์เฉพาะ

### 4.3 Regression mindset

เก็บสคริปต์/ไทม์ไลน์ไว้ในโฟลเดอร์แล็บของคุณ:

```text
lab-notes/
  device-model.json      # จาก template
  event-script-v1.md     # ไทม์ไลน์
  evidence/              # สกรีนช็อตก่อน/หลัง
```

เมื่อแก้เฟิร์มแวร์ใน M04+ ให้รันสคริปต์ชุดเดิม — ถ้าผลเปลี่ยนโดยไม่ตั้งใจ คือสัญญาณ regression

---

## 5. Blender for Twin Visualization

Virtual Device ในส่วนก่อนหน้าอธิบาย **ข้อมูลและพฤติกรรม** — ส่วนนี้เตรียม **ตัวแทนภาพ 3 มิติ** ของผลิตภัณฑ์/บอร์ด เพื่อแสดงใน Digital Twin / Sensor Studio

**[Blender](https://www.blender.org/)** เป็นซอฟต์แวร์ 3D โอเพนซอร์สฟรี ที่หลักสูตรใช้เป็นเส้นทางหลักสู่ไฟล์ **glTF / GLB** ซึ่งโฮสต์เว็บและ Bitstream Studio รองรับ

| ชั้นงานใน M03 | สิ่งที่คุณฝึก | ปลายทาง Twin |
|---|---|---|
| **Modeling** | สร้างรูปทรง mesh ของเคส/บอร์ด | รูปทรงในฉาก 3D |
| **Texturing** | UV + material / texture | พื้นผิวที่ดูสมจริงบนโฮสต์ |
| **Animation** | keyframe / action สั้น ๆ | แสดงกลไกเปิด-ปิด หรือ motion demo |
| **Export** | `.glb` | โหลดใน Studio / เทียบกับ [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |

> **Course 2 vs Course 3**  
> ที่นี่ให้ **พื้นฐานที่ใช้งานกับ Twin ได้**  
> หลักสูตร Product Industrial Design (Blender & Twin) จะลงลึก casing, industrial workflow, validation และ prototype — อย่ารอ Course 3 ถ้าต้องการแค่โมเดลประกอบ telemetry ใน Course 2

แผ่นลิงก์ด่วน: [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)

### 5.1 Getting Blender and the UI

1. ดาวน์โหลดจาก [blender.org/download](https://www.blender.org/download/)  
2. อ่านภาพรวมอินเทอร์เฟซ: [User Interface (Manual 4.5)](https://docs.blender.org/manual/en/4.5/interface/index.html)  
3. คู่มือฉบับเต็ม: [Blender 4.5 LTS Manual](https://docs.blender.org/manual/en/4.5/) หรือ [latest](https://docs.blender.org/manual/en/latest/)  
4. เส้นทางวิดีโอทางการ (อังกฤษ): [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)  
5. เส้นทางวิดีโอ **ภาษาไทย**: [INC111-2021 YouTube playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)  

โหมดที่พบบ่อยตอนสร้างโมเดลอุปกรณ์:

| Mode | ใช้เมื่อ | อ่านเพิ่ม |
|---|---|---|
| **Object Mode** | ย้าย/หมุน/สเกลทั้งชิ้น, รวมอ็อบเจกต์ | [Scenes & Objects](https://docs.blender.org/manual/en/4.5/scene_layout/object/index.html) |
| **Edit Mode** | แก้จุด ขอบ หน้า (mesh) | [Mesh introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html) |
| **Shading workspace** | จัด material / texture nodes | [Materials](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html) |
| **Animation editors** | Timeline, Dope Sheet, Graph Editor | [Animation intro](https://docs.blender.org/manual/en/4.5/animation/introduction.html) |

### 5.2 Modeling (สร้างรูปทรง)

Modeling ใน Blender มักเริ่มจาก **mesh primitive** (cube, cylinder, plane…) แล้วเข้า **Edit Mode** เพื่อขึ้นรูป — ตาม [Mesh Modeling introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)

#### ทักษะหลักที่ควรรู้ใน Course 2

| ทักษะ | ทำไมสำคัญต่อ Twin | เอกสาร |
|---|---|---|
| เลือก / Extrude | สร้างผนังเคส, ขอบหนา | [Extrude](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/mesh/extrude.html) |
| Loop Cut / Bevel | ขอบมน, แบ่งหน้าสำหรับ UV | [Loop Cut](https://docs.blender.org/manual/en/4.5/modeling/meshes/tools/loop.html) · [Bevel](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/edge/bevel.html) |
| Modifiers (Mirror, Solidify, Subdivision) | สร้างสมมาตร/ความหนาโดยไม่ทำซ้ำมือ | [Modifiers](https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html) |
| Apply Scale / origin | กันโมเดลบิดเมื่อใส่ Twin หรือ animation | [Transforms](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/transform/index.html) |

เวิร์กช็อปวิดีโอ: [Fundamentals — Modeling chapter](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)

#### แนวทางสำหรับโมเดลอุปกรณ์ Edge / DevKit

1. ตั้งหน่วยเป็น **เมตร** (หรืออย่างน้อยสเกลสม่ำเสมอทั้งฉาก)  
2. วาง **origin** ที่จุดที่มีความหมาย (มุมบอร์ด, แกนหมุนฝา, จุดวางบนโต๊ะ)  
3. แยกชิ้นส่วนที่อาจขยับ (ฝา, ปุ่ม, LED) เป็น object คนละชิ้นถ้าจะ animate  
4. คุมจำนวน polygon — webview Twin ไม่ต้องการ denseness ระดับฟิล์ม  
5. เปรียบเทียบสไตล์กับโมเดลใน [ternion-3d-assets-free `/assets/models`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/models)  

> **Key phrase**  
> Modeling ที่ดีสำหรับ Twin = *อ่านรูปได้ + สเกลจริง + origin ชัด + พร้อม UV* — ไม่ใช่รายละเอียดที่ render ภาพโฆษณาเท่านั้น

ศึกษาต่อ (Modeling):

- [Modeling section index (4.5)](https://docs.blender.org/manual/en/4.5/modeling/index.html)  
- [Edit Mode mesh tools](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/index.html)  
- [Geometry Nodes](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/index.html) (ขั้นสูง — ไม่บังคับ M03)

### 5.3 Texturing (วัสดุและพื้นผิว)

Texturing ในบริบท Twin = ทำให้ผิวโมเดลมีสี / ความเงา / ลาย ที่ **export ออกไป glTF ได้**

#### แนวคิดหลัก

| แนวคิด | ความหมายสั้น | เอกสาร |
|---|---|---|
| **Material** | คำอธิบายผิวบน object | [Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html) |
| **Principled BSDF** | โหนด PBR มาตรฐานที่ glTF เข้าใจดี | [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) |
| **UV map** | พิกัดคลี่ผิว 2D ลงบน texture | [UV editing](https://docs.blender.org/manual/en/4.5/editors/uv/index.html) · [Unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html) |
| **Image texture** | ไฟล์รูป (albedo / roughness / …) | [Image Texture node](https://docs.blender.org/manual/en/4.5/render/shader_nodes/textures/image.html) |
| **Texture Paint** | วาดลายบนโมเดลโดยตรง | [Texture Paint](https://docs.blender.org/manual/en/4.5/sculpt_paint/texture_paint/index.html) |

#### Workflow ที่แนะนำสำหรับ Course 2

```text
Mesh ready
  → Unwrap UV (Smart UV Project หรือมือ)
  → Principled BSDF
  → Base Color (± Roughness / Metallic maps)
  → Check in Material Preview / EEVEE
  → Export GLB (materials + UVs on)
```

ตาม [glTF 2.0 exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html):

- วัสดุหลักที่ export ได้ดีคือ **Metal/Rough PBR** จาก Principled BSDF  
- ควบคุม UV ด้วยการต่อ **UV Map** (+ Mapping) เข้า Image Texture  
- Unlit/shadeless มี path แยกในคู่มือ exporter ถ้าต้องการผิวแบน  

แหล่ง texture / cubemap พร้อมใช้ในระบบ Ternion:

- Browse: [assets/textures](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/textures)  
- Sync ใน Studio: **Download Free Assets from GitHub** (ดู [M02 §2.6](../../m02-vscode-twin/l01-vscode-for-twin/README.md))

ศึกษาต่อ (Texturing / shading):

- [Shader Nodes](https://docs.blender.org/manual/en/4.5/render/shader_nodes/index.html)  
- [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) / [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html) (render ใน Blender — Twin ใช้ไฟล์ export เป็นหลัก)  
- [glTF materials section](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)

### 5.4 Animation (การเคลื่อนไหว)

Animation ช่วยสาธิต **พฤติกรรมผลิตภัณฑ์** บน Twin เช่น เปิดฝา, กดปุ่ม, หมุนแขน — สอดคล้องกับ behavior/event script ฝั่งข้อมูล

#### แนวคิดหลัก

| แนวคิด | ความหมายสั้น | เอกสาร |
|---|---|---|
| **Keyframe** | จุดเวลาที่บันทึกค่า transform/property | [Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html) |
| **Action** | ชุด keyframe ของอ็อบเจกต์ | [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html) |
| **Armature / bones** | โครงกระดูกสำหรับชิ้นส่วนซับซ้อน | [Armatures](https://docs.blender.org/manual/en/4.5/animation/armatures/index.html) |
| **Shape keys** | Morph รูปทรง (ฝาอ่อน, ยาง) | [Shape Keys](https://docs.blender.org/manual/en/4.5/animation/shape_keys/index.html) |
| **Constraints** | จำกัดการเคลื่อนตามกฎ | [Constraints](https://docs.blender.org/manual/en/4.5/animation/constraints/introduction.html) |

ภาพรวม: [Animation & Rigging introduction](https://docs.blender.org/manual/en/4.5/animation/introduction.html)

#### สิ่งที่มักพาไป Twin ได้ (ผ่าน glTF)

ตามคู่มือ [glTF 2.0](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html):

| รองรับโดยทั่วไป | มักไม่ไป / ถูกมองข้าม |
|---|---|
| Keyframe ของ location / rotation / scale | Animation ของไฟ / material บางชนิด |
| Skinning (armature) | Driver ซับซ้อนที่ไม่ได้ bake |
| Shape key animation | Logic เฉพาะใน Blender ที่ไม่ได้ export |

เคล็ดลับ export animation:

1. ทำให้ action เป็น **active** หรือจัด NLA ตามที่ exporter กำหนด  
2. ทดสอบเล่นใน Blender ก่อน export  
3. เปิดตัวเลือก Animation ในหน้าต่าง glTF export  
4. ตรวจใน Bitstream Studio / viewer ว่าคลิปเล่นได้  

> **เชื่อมกับ Virtual Device**  
> Timeline ใน §4 (event script) = *เหตุการณ์ข้อมูล*  
> Timeline ใน Blender = *เหตุการณ์ภาพ*  
> ใน Capstone (M06) พยายามให้สองเส้นนี้เล่าเรื่องเดียวกัน

ศึกษาต่อ (Animation):

- [Animation editors](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)  
- [NLA Editor](https://docs.blender.org/manual/en/4.5/editors/nla/index.html)  
- [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)

### 5.5 Export to Twin — glTF / GLB

รูปแบบที่แนะนำสำหรับ Bitstream Studio / Twin เว็บ: **glTF Binary (`.glb`)** ไฟล์เดียวรวม mesh + materials + (ถ้ามี) animation

| ขั้น | การกระทำ | อ้างอิง |
|---|---|---|
| 1 | Apply transforms ที่จำเป็น, ตรวจ origin | Manual transforms |
| 2 | UV + Principled พร้อม | §5.3 |
| 3 | Animation พร้อม (ถ้ามี) | §5.4 |
| 4 | **File → Export → glTF 2.0** | [glTF 2.0 add-on (4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) |
| 5 | เลือก **glTF Binary (.glb)** · เปิด Meshes / Materials / (Animations) | หน้าต่าง export |
| 6 | โหลดใน Bitstream Studio หรือเทียบกับแพ็ก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) | M02 Free Loader |

มาตรฐานอุตสาหกรรม: [Khronos glTF](https://www.khronos.org/gltf/)

รูปแบบอื่น (FBX/OBJ/STL) มีที่ใช้ตอน prototype/พิมพ์ 3D — Course 3 จะพูดลึกกว่า; ใน Course 2 ให้โฟกัส **GLB สำหรับ Twin**

### 5.6 Suggested self-study path (Blender)

ถ้าต้องการฝึกเพิ่มเอง (~2–4 ชม. เพิ่ม):

**ตัวเลือกภาษาไทย (แนะนำถ้าต้องการคำบรรยายไทย):** ดู [INC111-2021 playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY) คู่กับแบบฝึกใน Lab E — ใช้ Manual ภาษาอังกฤษเมื่อต้องการรายละเอียดเครื่องมือล่าสุด

**ตัวเลือกทางการ (อังกฤษ):**

1. [Fundamentals 4.5 — start](https://studio.blender.org/training/blender-fundamentals-45-lts/)  
2. ทำบท [Modeling](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/) จนได้ชิ้นส่วนง่าย ๆ  
3. อ่าน [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) + unwrap หนึ่งชิ้น  
4. ใส่ keyframe หมุน/เปิดฝา 2–3 วินาที  
5. Export `.glb` แล้วลองใน Studio  
6. เทียบคุณภาพกับโมเดลใน [assets/models](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/models)  

> UI ของ Blender เปลี่ยนตามเวอร์ชัน — ถ้าคลิปไทยใช้เวอร์ชันเก่า ให้ยึดปุ่ม/เมนูจาก [Manual 4.5+](https://docs.blender.org/manual/en/4.5/) เป็นหลัก และใช้คลิปเป็นแนวคิด workflow

---

## 6. Design Checklist Before You Build

ก่อนลงมือ Lab ตอบให้ได้:

1. อุปกรณ์นี้ทดสอบ **logic ข้อไหน** ของเฟิร์มแวร์/ผลิตภัณฑ์  
2. เซ็นเซอร์ขั้นต่ำที่ต้องมีมีอะไรบ้าง (อย่างน้อย 2 ชนิด)  
3. Behavior หนึ่งเส้นสังเกตที่จอไหน  
4. สคริปต์เหตุการณ์ใช้เวลากี่วินาที และใครรันซ้ำได้บ้างในทีม  
5. (แนะนำ) จะใช้โมเดล 3D จาก Blender หรือจาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  

แผ่นกรอก: [device-model-checklist.md](resources/device-model-checklist.md) · [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)

---

## Next Steps

1. ทำแล็บ Virtual Device: [แล็บ](../l02-lab/README.md)  
2. กรอก checklist + แนบโมเดล/ไทม์ไลน์  
3. (แนะนำ) Lab Blender — export GLB หนึ่งชิ้น  
4. เมื่อพร้อม ไปต่อ **M04 — Firmware–Twin Co-simulation**

---

## References and Further Reading

### Course / host

1. [M01 Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M02 VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md)  
2. [Course 1 M05 Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)  
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets)  
7. [sample-virtual-device.template.json](resources/sample-virtual-device.template.json)  
8. [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)  

### Blender — official manuals & training

9. [Blender download](https://www.blender.org/download/)  
10. [Blender Manual 4.5 LTS](https://docs.blender.org/manual/en/4.5/) · [Manual (latest)](https://docs.blender.org/manual/en/latest/)  
11. [Modeling — meshes introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)  
12. [Modeling section](https://docs.blender.org/manual/en/4.5/modeling/index.html)  
13. [Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html)  
14. [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html)  
15. [UV editing](https://docs.blender.org/manual/en/4.5/editors/uv/index.html) · [UV unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html)  
16. [Texture Paint](https://docs.blender.org/manual/en/4.5/sculpt_paint/texture_paint/index.html)  
17. [Animation introduction](https://docs.blender.org/manual/en/4.5/animation/introduction.html)  
18. [Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html) · [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)  
19. [Armatures](https://docs.blender.org/manual/en/4.5/animation/armatures/index.html) · [Shape Keys](https://docs.blender.org/manual/en/4.5/animation/shape_keys/index.html)  
20. [glTF 2.0 importer/exporter (4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)  
21. [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)  
22. [Fundamentals — Modeling chapter](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)  
23. **[INC111-2021 Blender tutorial playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)**  
24. [Khronos glTF](https://www.khronos.org/gltf/)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: สร้าง Virtual Device และ event script](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Device checklist](resources/device-model-checklist.md) · [Blender cheatsheet](resources/blender-twin-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)
