---
id: pdesign.m04.l02
lang: th
title:
  th: 'แล็บ: ส่งออก GLB และนำเข้า Twin'
  en: 'Lab: Export GLB and Import to Twin'
summary:
  th: เตรียมไฟล์ ส่งออก .glb นำเข้า Twin host ทำเครื่องหมายจุดเซ็นเซอร์/โต้ตอบ แล้วทดสอบด้วยคลิปหรือข้อมูล
  en: Prepare the file, export .glb, import it into the Twin host, mark sensor/interaction points, then test with a clip or data.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m04.l01
objectives:
- th: ส่งออก enclosure_twin.glb และนำเข้า Bitstream Studio โดยขนาดและแกนใช้งานได้
  en: Export enclosure_twin.glb and import it into Bitstream Studio with usable scale and axis.
- th: กำหนดจุด sensor/interaction ≥ 1 จุดพร้อมชื่อ และทดสอบด้วยคลิปแอนิเมชันหรือ telemetry
  en: Mark at least one named sensor/interaction point and test with an animation clip or telemetry.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: iot.digital-twin
  to: 2
assesses:
- skill: hwdev.3d-modeling
  level: 2
  evidence: README.md#deliverables-checklist
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M04/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M04 — Export GLB and Import to Twin

**Course 3 · Module 4**  
**Type:** Hands-on (prepare · export · import · mark points · test)  
**Suggested time:** ~2.5–3 ชั่วโมง  

Read first: [Lesson](../l01-blender-to-twin/README.md) · [Export checklist](../l01-blender-to-twin/resources/export-twin-checklist.md) · [← TOC](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [glTF 2.0 exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) | export options |
| [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations) | stash / names |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Twin host |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | optional ex05 / ex06 |

---

## Lab Goals

- ได้ไฟล์ **`.glb`** จากโมเดล M02/M03  
- นำเข้า [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) แล้วขนาด/แนวแกนใช้งานได้  
- กำหนดจุด sensor หรือ interaction อย่างน้อย **1** จุดพร้อมชื่อ  
- ทดสอบอย่างน้อย: วางโมเดล + (คลิปแอนิเมชัน **หรือ** telemetry)  
- กรอก [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md)  

---

## Prerequisites

- [ ] ไฟล์จาก M03 (หรือ M02 ถ้ายังไม่มีคลิป — แจ้งใน checklist)  
- [ ] Bitstream Studio พร้อมใช้  
- [ ] คัดลอกงานเป็น `m04_enclosure_twin.blend` ก่อน export  

---

## Lab A — Prepare for export (required)

1. Apply Scale บนชิ้นที่จะส่ง  
2. ตรวจชื่อ object และชื่อคลิป (`lid_open` ฯลฯ)  
3. ถ้ามีหลาย Action: Stash ลง NLA ตาม [คู่มือ glTF](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)  
4. ซ่อน/ลบ cutter และของที่ไม่ต้องการส่ง  
5. Save `.blend`  

**Pass when:** เล่นคลิปใน Blender ยังถูก และ Scale เป็น 1,1,1

---

## Lab B — Export `.glb` (required)

1. `File → Export → glTF 2.0`  
2. เลือก **glTF Binary (.glb)**  
3. เปิด Apply Modifiers · Materials · Animations (ถ้ามี)  
4. Export เป็น `enclosure_twin.glb`  
5. จดตัวเลือก export ใน checklist  

**Pass when:** มีไฟล์ `.glb` และขนาดไม่เป็น 0 byte

---

## Lab C — Import into Twin host (required)

1. เปิด Bitstream Studio  
2. นำเข้า `enclosure_twin.glb` ตาม UI ของเวอร์ชันที่ใช้  
3. ตรวจ: มองเห็น · สเกลใช้ได้ · แนวแกนวางบนพื้นได้  
4. ถ้ามีคลิป — เล่น `lid_open` (หรือชื่อที่ส่งออก)  
5. แคปหน้าจอ  

**Pass when:** สกรีนช็อตแสดงโมเดลใน host และ checklist ติ๊ก Import OK

---

## Lab D — Mark sensor / interaction point (required)

1. เลือกอย่างน้อย 1 จุด (เช่น `sensor_bmi270_slot` หรือ `interact_lid`)  
2. บันทึก: ชื่อ · อยู่ตรงไหนบนกลอง · ผูกกับอะไร (เซ็นเซอร์ / คลิป / LED)  
3. แคปหรือวาดประกอบใน checklist  

**Pass when:** คนอื่นในทีมอ่านชื่อแล้วชี้จุดบนโมเดลถูก

---

## Lab E — Data or motion test (recommended — part of the complete deliverable)

เลือกอย่างน้อยหนึ่ง:

| Option | What to do |
|---|---|
| **E1 — Clip** | เล่นแอนิเมชันใน Twin ให้ครบรอบเปิด (และปิดถ้ามี) |
| **E2 — Telemetry** | Link Simulator หรือ Board แล้วให้มีสตรีมขณะโมเดลอยู่บนจอ |
| **E3 — Web-app** | เปิด Hackathon **ex05** หรือ **ex06** คู่กับ Twin แล้วแคปคู่ |

**Pass when:** มีหลักฐานไฟล์ภาพ/คลิปในโฟลเดอร์ผลงาน

---

## Lab F — Optional

- เทียบสเกลกับ GLB จาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  
- Re-import `.glb` กลับ Blender เพื่อยืนยันคลิปไม่หาย  
- ลด poly แล้ว export รอบสอง เปรียบเทียบขนาดไฟล์  

---

## Deliverables checklist

- [ ] `enclosure_twin.glb` (+ `.blend` ต้นทาง)  
- [ ] สกรีนช็อตใน Bitstream Studio  
- [ ] จุด sensor/interaction ≥ 1  
- [ ] ผลทดสอบ Lab E  
- [ ] [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md) กรอกครบ  

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| โมเดลยักษ์หรือจิ๋วใน Twin | ตรวจ Unit Scale ทีม · Apply Scale · export ใหม่ — อย่าแก้แค่ซูมแล้วจบ |
| ไม่มีแอนิเมชันใน GLB | Stash Action · เปิด Animations ตอน export · ตรวจชื่อคลิป |
| วัสดุดำ/หาย | ใช้ Principled · ตรวจ Materials ใน export · ไฟใน Twin |
| Boolean ดูไม่ถูกหลัง export | เปิด Apply Modifiers |
| Import ไม่ขึ้น | ตรวจนามสกุล `.glb` · ลองโมเดลตัวอย่างจาก free assets เพื่อแยกว่าพังที่ไฟล์หรือที่ host |
| Telemetry ไม่เกี่ยวกับโมเดล | คนละท่อ — โมเดลเป็นภาพ; ใช้ ex05/ex06 เป็นหลักฐานข้อมูล |

[Lesson](../l01-blender-to-twin/README.md) · [Export checklist](../l01-blender-to-twin/resources/export-twin-checklist.md) · [TOC](../../README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
