---
id: twin.m03.l02
lang: th
title:
  th: 'แล็บ: สร้าง Virtual Device และ event script'
  en: 'Lab: Build a Virtual Device and Event Script'
summary:
  th: สร้างโมเดลอุปกรณ์ กำหนด behavior เขียนสคริปต์เหตุการณ์ที่รันซ้ำได้ และ (แนะนำ) ฝึก Blender สั้น ๆ แล้วส่งออก GLB
  en: Create the device model, define a behaviour, write a repeatable event script and (recommended) a short Blender exercise exported to GLB.
level: L3
time_min:
  lab: 210
hardware:
  emulator: true
  boards:
  - none
prerequisites:
- twin.m03.l01
objectives:
- th: สร้างโมเดลอุปกรณ์ (device-model.json หรือเทียบเท่า) ที่มีเซ็นเซอร์ ≥ 2 ชนิดและ behavior ≥ 1 เส้นทาง
  en: Create a device model (device-model.json or equivalent) with at least two sensors and at least one behaviour.
- th: รัน event script ซ้ำและเก็บหลักฐานผลบน visualization
  en: Run the event script repeatedly and capture evidence on the visualisation.
develops:
- skill: sys.simulation
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: hwdev.3d-modeling
  to: 1
assesses:
- skill: sys.simulation
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M03/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M03 — Build a Virtual Device and Event Script

**Course 2 · Module 3**  
**Type:** Hands-on (Virtual Device + optional Blender → GLB)  
**Suggested time:** ~3–3.5 ชั่วโมง Virtual Device (+ ~1–1.5 ชม. Lab E) 

Read first: [Lesson](../l01-virtual-device-modeling/README.md) · [Device checklist](../l01-virtual-device-modeling/resources/device-model-checklist.md) · [Blender cheatsheet](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) · [Template](../l01-virtual-device-modeling/resources/sample-virtual-device.template.json) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M02 lab](../../m02-vscode-twin/l02-lab/README.md) | เซสชัน Studio / Simulator พร้อม |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | scene presets / web-app evidence |
| [Course 1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | ความหมายเซ็นเซอร์ |
| [Blender Manual 4.5](https://docs.blender.org/manual/en/4.5/) | Modeling / Texturing / Animation |
| [INC111-2021 playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY) | Tutorial วิดีโอภาษาไทย |
| [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) | ตัวอย่าง GLB / texture |

---

## Lab Goals

- มี Virtual Device ที่กำหนดเซ็นเซอร์อย่างน้อย **2 ชนิด**  
- มี behavior อย่างน้อย **1** เส้นทาง (อินพุต → สถานะที่สังเกตได้)  
- มีสคริปต์/ไทม์ไลน์เหตุการณ์รันซ้ำได้และเห็นผลใน visualization  
- กรอก [device-model-checklist.md](../l01-virtual-device-modeling/resources/device-model-checklist.md)  
- (แนะนำ) ฝึก Blender สั้น ๆ: model หรือ texture หรือ animation → export **GLB**  

**Suggested time:** ~3–3.5 ชม. (Virtual Device) + ~1–1.5 ชม. (Lab E Blender ถ้าทำ)

---

## Prerequisites

- [ ] Lab M02 ผ่าน (เปิด Bitstream Studio ได้)  
- [ ] เลือกเส้นทาง: **Simulator** และ/หรือบอร์ดที่สตรีมได้  
- [ ] มีโฟลเดอร์ `lab-notes/` สำหรับไฟล์โมเดล + หลักฐาน  
- [ ] (Lab E) ติดตั้ง [Blender](https://www.blender.org/download/)  

---

## Lab A — Create the model (required)

1. คัดลอก [sample-virtual-device.template.json](../l01-virtual-device-modeling/resources/sample-virtual-device.template.json) เป็นไฟล์ของคุณ เช่น `lab-notes/device-model.json`  
2. ตั้ง `deviceId` / `displayName` ให้ทีมจำได้  
3. เปิดใช้เซ็นเซอร์อย่างน้อย 2 ชนิดจากชุด: switch, temperature/pressure, IMU  
4. กำหนด `default` และช่วง `min`/`max` (หรือเทียบเท่า) ให้สมเหตุสมผล  
5. ระบุ actuator อย่างน้อย 1 ตัว (LED / flag / log sink)  

บนโฮสต์: เปิด Simulator หรือบอร์ด แล้วเลือก **scene** ที่สอดคล้องโมเดล (เช่น Lab Quiet สำหรับสาธิตช้า, Motion เมื่อมี IMU)

**Pass when:** ไฟล์โมเดลอ่านรู้เรื่อง และโฮสต์แสดงค่าที่เกี่ยวข้องกับเซ็นเซอร์ที่เลือกอย่างน้อยหนึ่งช่อง

---

## Lab B — Behavior (required)

กำหนดและสาธิตอย่างน้อยหนึ่งกฎ เช่น:

- คำสั่ง/ปุ่ม → LED หรือสถานะบน UI  
- อุณหภูมิเกินเกณฑ์ → event / ข้อความ log / การเปลี่ยนโหมด  

เขียนเป็นประโยค `WHEN … THEN …` ใน checklist

**Pass when:** เพื่อนในทีมกระตุ้นอินพุตแล้วชี้ผลบนจอได้โดยไม่เดา

---

## Lab C — Event script (required)

เขียนไทม์ไลน์อย่างน้อย 4 จังหวะ (ดูตัวอย่างในบทเรียน) แล้วรันจริง:

1. เริ่มจากค่า default / Lab Quiet  
2. กระตุ้นสเกลาร์หรือสวิตช์ตามเวลา  
3. กระตุ้น IMU หรือสลับไป Motion (ถ้าโมเดลมี IMU)  
4. บันทึกผลที่เห็น (สกรีนช็อตก่อน/หลัง หรือคลิปสั้น)  

อนุญาตให้รันแบบ **นาฬิกาจับเวลา + มือ** ถ้าเครื่องมือยังไม่มีไฟล์สคริปต์อัตโนมัติ — แต่ต้องทำซ้ำได้ในรอบที่ 2

**Pass when:** รันสคริปต์ซ้ำแล้วได้ลำดับผลเดียวกันโดยประมาณ

---

## Lab D — Optional polish

- เพิ่ม behavior ที่สอง (threshold + command)  
- เปรียบเทียบ scene Lab Quiet vs Motion บนเซ็นเซอร์ชุดเดียวกัน  
- เปิด Hackathon `web-app/` เป็นจอ Visualization ชั้นนอก  

---

## Lab E — Blender for Twin (recommended)

ใช้ [blender-twin-cheatsheet.md](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) เป็นแผนที่ลิงก์  
Tutorial ภาษาไทย: [INC111-2021 playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

เลือกอย่างน้อย **หนึ่ง** track ให้จบ:

### E1 — Modeling

1. ติดตั้ง [Blender](https://www.blender.org/download/)  
2. สร้างชิ้นส่วนง่าย (เคสกล่อง / บอร์ดแบน) จาก mesh primitive  
3. ใช้ Extrude / Bevel / Mirror ตาม [Modeling intro](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)  
4. ตั้ง origin + Apply Scale  

### E2 — Texturing

1. Unwrap UV ([UV unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html))  
2. ใส่ [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) + Base Color  
3. (ทางเลือก) ใช้ texture จาก [ternion-3d-assets-free textures](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/textures)  

### E3 — Animation

1. Keyframe หมุนหรือเปิดฝา 2–3 วินาที ([Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html))  
2. เล่นใน Timeline ให้เห็นชัด  

### E4 — Export & view

1. **Export → glTF 2.0 → `.glb`** ตาม [glTF exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)  
2. โหลดใน Bitstream Studio (หรือเทียบกับโมเดลใน free assets)  
3. บันทึกสกรีนช็อต + ชื่อไฟล์ `.glb` ใน checklist  

**Pass when (Lab E):** มีไฟล์ `.glb` และหลักฐานว่าเปิดในโฮสต์ได้ หรืออย่างน้อยเปิดใน Blender หลัง re-import ได้

---

## Deliverables checklist

- [ ] `device-model.json` (หรือเทียบเท่า)  
- [ ] Lab A–C ผ่าน  
- [ ] [device-model-checklist.md](../l01-virtual-device-modeling/resources/device-model-checklist.md) กรอกครบ  
- [ ] หลักฐานสคริปต์รัน (รูป/คลิป)  
- [ ] (แนะนำ) Lab D  
- [ ] (แนะนำ) Lab E + `.glb`  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| โมเดลเขียนแล้วแต่จอไม่เปลี่ยน | ยังไม่ Link / อยู่คนละโหมด Simulator–Bitstream |
| IMU ไม่ขยับ | อยู่ซีน Environment หรือ Lab Quiet — สลับ Motion หรือกระตุ้นตามสคริปต์ |
| Behavior ไม่เห็นผล | ยังไม่ได้กำหนดจุดสังเกต (LED/UI/log) ให้ชัด |
| ค่าดู “ปลอม” เกินไป | ปกติของ Simulator — จดในโมเดลว่าเป็น synthetic |
| ทำซ้ำไม่ได้ | เขียนเวลาเป็นวินาที และเริ่มจาก default เดียวกันทุกครั้ง |
| GLB ไม่มี texture | ลืม UV / ไม่ใช้ Principled / ปิด Materials ตอน export — ดู [glTF materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) |
| GLB ไม่มี animation | Action ไม่ได้ active / ไม่ได้เปิด Animation ใน export |
| โมเดลใหญ่เกินไปใน Studio | ลด subdivision · decimate · ตรวจสเกล |

[Lesson](../l01-virtual-device-modeling/README.md) · [Device checklist](../l01-virtual-device-modeling/resources/device-model-checklist.md) · [Blender cheatsheet](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) · [Table of Contents](../../README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)
