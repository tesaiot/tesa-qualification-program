---
id: pdesign.m04.l01
lang: th
title:
  th: ส่งออก GLB และนำเข้า Twin host
  en: Exporting GLB and Importing into the Twin Host
summary:
  th: ความหมายของ Twin-ready การเตรียมไฟล์ก่อน export ขั้นตอน glTF Binary การตรวจหลังนำเข้า จุดเซ็นเซอร์และจุดโต้ตอบ และเมทริกซ์ทดสอบขั้นต่ำ
  en: What Twin-ready means, preparing the file, exporting glTF Binary, post-import checks, sensor and interaction points, and the minimum test matrix.
level: L2
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m03.l02
objectives:
- th: เตรียมไฟล์ก่อน export (หน่วย Apply Scale origin ลบ cutter/ไฟทดสอบ ชื่อ object) และส่งออกเป็น glTF Binary (.glb)
  en: Prepare the file before export (units, apply scale, origin, remove cutters/test lights, object names) and export glTF Binary (.glb).
- th: นำ .glb เข้า Bitstream Studio แล้วตรวจสเกล แกน ชื่อชิ้นส่วน และคลิปตามรายการตรวจ
  en: Import the .glb into Bitstream Studio and check scale, axis, part names and clips against the checklist.
- th: ตั้งชื่อจุดเซ็นเซอร์และจุดโต้ตอบตามรูปแบบ `sensor_…` / `interact_…` และทดสอบด้วยคลิปหรือ telemetry
  en: Name sensor and interaction points as `sensor_…` / `interact_…` and test them with a clip or telemetry.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: iot.digital-twin
  to: 1
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — Blender to Twin Integration

**Course 3 · Module 4**  
**Suggested time:** ประมาณ 3 ชั่วโมง — ส่งออก GLB จาก Blender นำเข้า Twin host กำหนดจุดเซ็นเซอร์/โต้ตอบ แล้วทดสอบกับ telemetry หรือคลิปแอนิเมชัน  
**Format:** บทเรียนลงมือทำ — อ่านแล้วทำตามได้เลย; การจำลองสถานการณ์ใช้งานเต็มรูปแบบอยู่ที่ [M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

[Lab](../l02-lab/README.md) · [Export checklist](resources/export-twin-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. ส่งออกโมเดลในรูปแบบ **glTF/GLB** (และทางเลือก FBX/OBJ) ให้พร้อมใช้กับ Twin  
2. นำโมเดลเข้าสู่ **TESA Digital Twin** ผ่านโฮสต์หลักของคอร์ส ([Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio))  
3. กำหนดจุดโต้ตอบ (**interaction points**) จุดเซ็นเซอร์ และตำแหน่งประกอบ  
4. ทดสอบโมเดลร่วมกับข้อมูล **telemetry / การเคลื่อนไหว / ค่าเซ็นเซอร์**  

> **Key phrase**  
> GLB ที่ดี = *ขนาดถูก · แกนถูก · ชื่อคลิปชัด · วัสดุส่งออกได้* — นำเข้า Twin แล้วค่อยแต่งฉาก ไม่ใช่แก้สเกลทีหลังทีละร้อยเท่า

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M03 — Motion and Interaction](../../m03-motion/l01-motion-and-interaction/README.md) | คลิป `lid_open` / รายการ clip list |
| [Course 2 M03 — Blender for Twin](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | ภาพรวม export GLB สั้น ๆ |
| **[glTF 2.0 exporter (Blender 4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)** | ตัวเลือก Mesh / Materials / Animations |
| **[glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)** | Stash Action · ชื่อคลิป |
| **[glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)** | Principled BSDF ที่ส่งออกได้ |
| **[Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | ก่อน export |
| **[Khronos glTF](https://www.khronos.org/gltf/)** | มาตรฐานไฟล์ที่ Twin / เว็บใช้ |
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | นำเข้า / แสดงโมเดล 3D + telemetry |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | ตัวอย่าง GLB อ้างอิงสเกลและวัสดุ |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/` เช่น **ex05** เทียบข้อมูลเซ็นเซอร์ |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | อ้างอิงบอร์ดเมื่อจับคู่จุดเซ็นเซอร์ |
| [Export checklist](resources/export-twin-checklist.md) | แบบฟอร์มผลงาน |

---

## 1. What “Twin-ready” Means Here

ใน Course 3 โฮสต์ Digital Twin หลักคือ **Bitstream Studio** (VS Code extension) — รับไฟล์ **glTF Binary (`.glb`)** สำหรับ preview / Sensor Studio / Animation Lab ตามเครื่องมือที่มี

```text
[Blender .blend]
   export glTF 2.0
        │
        ▼
   enclosure_twin.glb
        │
        ▼
[Bitstream Studio / Twin host]
   place model · mark sensor/interaction · play clip
        │
        ├── optional: live telemetry (Simulator or Board)
        └── optional: Hackathon web-app ex05 / ex06 as second screen
```

| Format | Use when |
|---|---|
| **`.glb`** | **เป้าหมายหลัก** — ไฟล์เดียว รวม mesh + materials + animations |
| `.gltf` + bins/textures | เมื่อต้องการแยก texture แก้ไขภายนอก |
| FBX / OBJ | สำรองส่งเครื่องมืออื่น — ไม่ใช่เส้นทางหลักของ Twin เว็บ |
| STL | เก็บไว้พิมพ์ใน M06 — ไม่แทน GLB สำหรับ Twin |

มาตรฐาน: [Khronos glTF](https://www.khronos.org/gltf/)

---

## 2. Prepare the Blend File Before Export

ทำตามลำดับนี้ทุกครั้งก่อนกด Export

### 2.1 Scale, origin, and cleanup

| Step | Action | Why |
|---|---|---|
| 1 | ตรวจหน่วยทีมยังตรง M01 (Metric + mm + Unit Scale ที่ตกลง) | กันสเกลเพี้ยนใน Twin |
| 2 | `Ctrl+A` → **Scale** (และ Rotation ถ้าจำเป็น) บนชิ้นที่จะส่ง | [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html) |
| 3 | Origin ของฝาอยู่ที่บานพับ (จาก M03) | คลิปหมุนถูกจุด |
| 4 | ลบ/ซ่อน cutter, ไฟทดสอบ, กล้องที่ไม่ต้องการส่ง | ไฟล์เบาและไม่รก |
| 5 | ชื่อ object เป็นภาษาอังกฤษสั้น | อ้างใน Twin / checklist |

### 2.2 Materials that survive export

ใช้ **Principled BSDF** ตามที่ฝึกใน M02 — glTF รองรับพารามิเตอร์หลักได้ดี ([glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials))

| Do | Avoid for Twin export |
|---|---|
| Base Color / Roughness / Metallic ชัด | Shader ซับซ้อนที่ glTF ไม่รู้จัก |
| UV พอสำหรับลายสำคัญ (ถ้ามี texture) | พึ่งเฉพาะ procedural node ที่ bake ไม่ได้ |
| ทดสอบ Material Preview ก่อน export | สมมติว่า EEVEE กับ Twin เหมือนกันทุกอย่าง |

### 2.3 Animations that will be included

ตาม [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations):

- Action จะถูกส่งออกถ้าเป็น **active action** หรือถูก **Stash** ลง NLA track  
- ถ้ามีหลายคลิป (`lid_open`, `lid_close`) ให้ Stash ให้ครบก่อน export  
- ชื่อ track/action มีผลต่อชื่อคลิปใน GLB — ใช้ชื่อเดียวกับ [clip list](../../m03-motion/l01-motion-and-interaction/resources/animation-clip-list.md)

### 2.4 Optional: reduce polycount

ถ้าไฟล์ใหญ่หรือ Twin กระตุก:

- ลด subdivision ที่ไม่จำเป็น  
- อย่าลดจนช่องพอร์ตอ่านไม่ออก  
- เปรียบเทียบขนาดไฟล์กับตัวอย่างใน [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) เป็นแนวคร่าว ๆ

---

## 3. Export glTF Binary (.glb) — Step by Step

อ้างอิงคู่มือเต็ม: [glTF 2.0](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)

1. เลือกเฉพาะชิ้นที่จะส่ง (หรือส่งทั้ง scene ตามที่ทีมตกลง)  
2. `File → Export → glTF 2.0`  
3. Format: **glTF Binary (.glb)**  
4. แนะนำเปิดอย่างน้อย:

| Export option | Lab tip |
|---|---|
| **Selected Objects** (ถ้าเลือกชิ้นแล้ว) | กันพาไฟ/พื้นทดสอบไปด้วย |
| **Data → Mesh → Apply Modifiers** | ส่งผล Boolean/Solidify/Bevel ที่ยังไม่ Apply ในฉาก |
| **Materials** | รวม Principled |
| **Animations** (ถ้ามีคลิป M03) | เปิด และตรวจ Mode ตามด้านล่าง |

5. Animation Mode (เมื่อมีหลายคลิป):

| Mode | Use when |
|---|---|
| **Actions** (default) | มี active action หรือ stash ใน NLA แล้ว |
| **NLA Tracks** | จัดการหลายแทร็กเป็นคลิปแยกชัด |

6. ตั้งชื่อไฟล์ เช่น `enclosure_twin.glb` แล้ว Export  
7. ตรวจขนาดไฟล์และเปิดดูในเครื่องมือ preview ของระบบ (หรือ import กลับ Blender ชั่วคราว) ว่าคลิปยังเล่นได้

จดตัวเลือกที่ใช้จริงลง [export-twin-checklist.md](resources/export-twin-checklist.md)

---

## 4. Import into Bitstream Studio (Twin Host)

### 4.1 Bring-up

1. ติดตั้ง/เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) จาก VS Code  
2. เปิด workspace ของคุณ (ทบทวนแนวทางโฮสต์จาก [Course 2](../../../digital-twin/README.md) ถ้าเคยเรียน)  
3. นำเข้าไฟล์ `.glb` ตาม UI ของรอบนั้น เช่น  
   - แผง **Assets / Model / Free Loader**  
   - หรือ **Sensor Studio / 3D preview / Animation Lab**  

รายละเอียดปุ่มอาจต่างตามเวอร์ชัน — ให้ทำตามคู่มือของเวอร์ชันที่ใช้ และจดชื่อแผงที่ใช้ใน checklist

### 4.2 First checks after import

| Check | Pass means |
|---|---|
| Model visible | เห็นกล่องใน viewport |
| Scale usable | ไม่จิ๋ว/ยักษ์ผิดปกติเมื่อเทียบของจริงหรือ PCB ในใจ |
| Up-axis / orientation | วางบน “พื้น” ได้โดยไม่ต้องหมุนแก้ยาว |
| Named parts readable | แยกฝา/ฐานได้ถ้า Twin แสดง hierarchy |
| Animation (if exported) | เล่น `lid_open` ได้หรือมีรายการคลิป |

ถ้าสเกลผิดรอบเดียว: **กลับไปแก้ใน Blender แล้ว export ใหม่** — อย่าซูมแก้ใน Twin แล้วถือว่าจบ (ยอมรับได้แค่เป็น workaround ชั่วคราวเท่านั้น)

### 4.3 Compare with a known-good GLB (optional)

โหลดโมเดลจาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) คู่กัน เพื่อเทียบว่า pipeline นำเข้าของเครื่องคุณทำงาน — จากนั้นสลับกลับไปโมเดลของคุณ

---

## 5. Interaction Points and Sensor Nodes

เป้าหมายของข้อนี้: ให้ทีมออกแบบกับทีมเฟิร์มแวร์**พูดภาษาเดียวกัน**

### 5.1 What to mark

| Point type | Example on your enclosure | Link to firmware / Twin |
|---|---|---|
| **Sensor node** | ช่องเหนือ IMU / อุณหภูมิ | ชื่อเซ็นเซอร์ เช่น `bmi270`, `sht40` |
| **Interaction point** | ฝา · ปุ่ม · LED window | คลิป `lid_open` · สถานะ LED |
| **Mount / placement** | ฐานวางโต๊ะ · รูสกรู | origin การวางในฉาก |

ในแล็บอย่างน้อยระบุ **1 จุด** ที่อธิบายได้ชัด (ตำแหน่งบนโมเดล + ชื่อที่ผูกกับข้อมูล)

### 5.2 Naming convention (lab)

```text
sensor_bmi270_slot
sensor_sht40_vent
interact_lid
interact_user_button
led_status_window
```

จดคู่ชื่อ ↔ ความหมายใน checklist — อย่าใช้ชื่อสุ่ม

### 5.3 How you “define” them in the lab

ขึ้นกับเครื่องมือที่มี อย่างใดอย่างหนึ่งนับได้:

- Empty / locator ใน Blender ที่ export ไปด้วย  
- โน้ตตำแหน่ง + สกรีนช็อตใน Twin  
- การผูกคลิปแอนิเมชันหรือ material กับสถานะใน UI  

สำคัญคือ**มีหลักฐานและชื่อคงที่** ไม่ใช่แค่ชี้ในอากาศตอนพรีเซนต์

---

## 6. Test with Telemetry or Motion Data

### 6.1 Minimum test matrix

| Test | How | Pass |
|---|---|---|
| **A — Static placement** | โมเดลนิ่งใน Twin | ขนาด/แกนใช้ได้ |
| **B — Clip playback** | เล่น `lid_open` ใน host | ฝาเปิดตามที่ออกแบบ |
| **C — Live or sim data** (แนะนำ) | Link Simulator หรือ Board + ดู telemetry | ค่าเซ็นเซอร์ไหลขณะโมเดลอยู่บนจอ |

### 6.2 Suggested second screen — Hackathon web-app

หลังโมเดลอยู่ใน Twin แล้ว (ไม่แทนขั้นตอน export):

1. Serve โฟลเดอร์ `web-app/` จาก [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
2. เปิด **ex05** (orientation) หรือ **ex06** (dashboard) ตามเซ็นเซอร์ที่มี  
3. แคปคู่: Twin มีโมเดล + web-app มีค่า  

ใช้สอนว่าโมเดล 3D เป็น**เปลือกภาพ** — ความจริงของเซ็นเซอร์อยู่ที่สตรีมข้อมูล ([Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) มี walkthrough ex05)

### 6.3 Example bindings (pick one)

| If you have… | Binding idea |
|---|---|
| BMI270 stream | หมุน/เอียง preview ตาม orientation (ถ้า host รองรับ) หรือเทียบกับ ex05 |
| Threshold / mode event | เปลี่ยนสีส่วน `led_status_window` หรือเล่นคลิปสั้น |
| Lid interaction in UI | ปุ่มใน Twin สั่งเล่น `lid_open` |

ไม่ต้องครบทุกข้อใน 3 ชั่วโมง — เลือกอย่างน้อยหนึ่งเส้นทางที่มีหลักฐาน

---

## 7. Quality Gate Before M05

| Check | Pass means |
|---|---|
| `.glb` file exists | ชื่อและที่เก็บจดใน checklist |
| Import OK in Bitstream Studio | สกรีนช็อต |
| Scale / axis usable | ไม่ต้องเดาสเกลใหม่ |
| ≥ 1 sensor or interaction point documented | ชื่อ + ตำแหน่ง |
| Clip names match M03 list (if any) | ไม่เปลี่ยนชื่อตอน export โดยไม่จด |
| Optional telemetry evidence | Studio และ/หรือ web-app |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. กรอก [export-twin-checklist.md](resources/export-twin-checklist.md)  
3. เมื่อพร้อม ไปต่อ [M05 — Scenario and Digital Validation](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## References and Further Reading

### Blender / glTF

1. [glTF 2.0 importer/exporter (4.5 LTS)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)  
2. [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)  
3. [glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)  
4. [Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)  
5. [Khronos glTF](https://www.khronos.org/gltf/)  
6. [Blender Fundamentals — Importing & Exporting](https://studio.blender.org/training/blender-fundamentals-45-lts/blender_4-5_lts_importing-exporting/)  

### Twin host and evidence

7. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
8. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  
9. [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) — `web-app/ex05`, `ex06`  
10. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)  
11. [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) · [Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 3 TOC](../../README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: ส่งออก GLB และนำเข้า Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Export checklist](resources/export-twin-checklist.md) · [← TOC](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
