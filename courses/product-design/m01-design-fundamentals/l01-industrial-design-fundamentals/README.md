---
id: pdesign.m01.l01
lang: th
title:
  th: หลักออกแบบเชิงอุตสาหกรรมและกล่องหุ้มตามสเกลจริง
  en: Industrial Design Principles and a True-scale Enclosure
summary:
  th: สี่เลนส์ของงานออกแบบ ลำดับ Concept → Block → Final ขั้นตอนกล่องหุ้ม PCB clearance และการตั้งหน่วยกับสเกลใน Blender
  en: The four design lenses, Concept, Block and Final stages, the PCB enclosure workflow, clearances, and units and scale in Blender.
level: L2
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites: []
objectives:
- th: ตรวจแนวคิดผลิตภัณฑ์ด้วยสี่เลนส์ (Function, Form & Proportion, Material & Manufacturing, User Experience) และเลนส์ Electronics fit
  en: Review a product concept through the four lenses (Function, Form & Proportion, Material & Manufacturing, User Experience) plus Electronics fit.
- th: คำนวณขนาดภายนอกของกล่องหุ้มจากขนาด PCB, clearance และความหนาผนัง
  en: Calculate an enclosure's outer size from the PCB size, clearance and wall thickness.
- th: ตั้งหน่วย Blender เป็น Metric / Millimeters / Unit Scale 0.001 และ Apply Scale หลังปรับขนาด
  en: Set Blender units to Metric / Millimeters / Unit Scale 0.001 and apply scale after resizing.
develops:
- skill: hwdev.enclosure
  to: 2
- skill: hwdev.3d-modeling
  to: 1
- skill: hwdev.design-basics
  to: 1
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — Industrial Design Fundamentals

**Course 3 · Module 1**  
**Suggested time:** ประมาณ 2 ชั่วโมง — เรียนรู้แนวคิด ตั้งค่า Scene ใน Blender (หน่วยเป็นมิลลิเมตร) แล้วสร้างกล่องหุ้มแบบหยาบตามขนาดจริง  
**Format:** บทเรียนลงมือทำ — อ่านแล้วทำตามใน Blender ได้เลย ส่วนผิววัสดุและ PBR ไปเรียนที่ [M02](../../m02-modeling-render/l01-modeling-materials-render/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/scale-and-block-checklist.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายหลัก **Industrial-grade Design** ที่รองรับการผลิตจริง  
2. ทำงานตามลำดับ **Concept → Block Model → Final Model**  
3. อธิบาย workflow ของ **Casing / Enclosure / PCB Housing** สำหรับอุปกรณ์อัจฉริยะ  
4. จัดการ **Topology, Mesh optimization และ Scale accuracy** เบื้องต้นใน Blender  

> **Key phrase**  
> ใน M01 ให้**ล็อกขนาดให้ตรงฮาร์ดแวร์ก่อน** แล้วค่อยทำให้งาม — ถ้ากล่องหยาบ (block) ผิดตั้งแต่ต้น งานใน M02–M06 จะแก้แพงทั้งหมด

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[Blender Download](https://www.blender.org/download/)** | ติดตั้งเครื่องมือหลักของคอร์ส |
| **[Blender 4.5 LTS Manual — Scene Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units)** | ตั้งหน่วย Metric / mm / Unit Scale |
| **[Apply Scale / Transforms](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | กด `Ctrl+A` ก่อนวัดขนาด ทำ bevel หรือ export |
| **[Mesh Structure](https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html)** | ความหมายของ vertex / edge / face · tris · quads · n-gons |
| **[Mesh Modeling intro](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)** | แยก Object Mode กับ Edit Mode |
| **[Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)** | ตั้งจุดหมุน / จุดวางบนโต๊ะ |
| **[Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | วิดีโอสอนทางการ (ภาษาอังกฤษ) |
| **[INC111-2021 Blender (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Tutorial ภาษาไทย |
| **[IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/what-is-industrial-design/)** | นิยามวิชาชีพ industrial design |
| **[All About Circuits — 3D-printed electronics enclosure](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | ลำดับงาน PCB → เปลือกกล่อง → เจาะช่อง · ระยะเผื่อ |
| **[Protolabs Network — Enclosure design for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | ผนังประมาณ 2 mm · ระยะเผื่อประมาณ 0.5 mm |
| **[KIT_PSE84_EVAL kit guide (Infineon)](https://documentation.infineon.com/psocedge/docs/lne1762692969598)** | หาเอกสารและไฟล์แบบของบอร์ดที่ใช้ |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | อ้างอิงบอร์ดและตัวอย่างเฟิร์มแวร์ |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | ดูตัวอย่างสเกลโมเดล (ไม่ใช้แทนกล่องที่คุณออกแบบเอง) |
| [Course 2 M03 Blender intro](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | พื้นฐาน Twin 3D ถ้าเคยเรียน Course 2 |
| [Checklist](resources/scale-and-block-checklist.md) | แบบฟอร์มกรอกตอนทำแล็บ |

---

## 1. Why Industrial Design Matters for Edge AI Devices

[Industrial Design](https://www.idsa.org/about-idsa/what-is-industrial-design/) (ตาม IDSA) คือการออกแบบผลิตภัณฑ์ที่คนใช้จริงทุกวัน — ไม่ใช่แค่ “รูปสวยในจอ” แต่ต้อง **ใช้งานได้ ผลิตได้ และประกอบกับวิศวกรรมภายในได้**

สำหรับอุปกรณ์ **Edge AI / IoT** กล่องหุ้ม (enclosure) ต้องรับมือกับอย่างน้อย:

| Topic | Why it matters |
|---|---|
| ขนาด PCB + ส่วนสูง (connectors, sensors) | ใส่ไม่ลง / กดปุ่มไม่ถึง |
| ช่องเซ็นเซอร์ / พอร์ต USB | ถูกบัง → ข้อมูลเพี้ยน หรือเสียบสายไม่ได้ |
| การจับถือ / วางโต๊ะ | ergonomics และจุด origin ใน Twin |
| การผลิตต้นแบบ (FDM/SLA) → ฉีดพลาสติกภายหลัง | ผนังหนา / fillet / bosses ต่างข้อจำกัด |
| Digital Twin | สเกลและแกนผิด → animation / telemetry ดูหลอก |

ในคอร์สนี้ใช้ **[Blender](https://www.blender.org/)** เพราะฟรี โอเพนซอร์ส และส่งออก **glTF/GLB** ไป [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) ได้ใน M04

```text
Concept sketch
    → Block model (this module)
        → Detailed model + materials (M02)
            → Motion clips (M03)
                → Twin + validation (M04–M05)
                    → Print / fitment / report (M06)
```

---

## 2. Industrial-grade Design — Four Lenses

ผลิตภัณฑ์ “industrial-grade” ในหลักสูตรนี้หมายถึง: **ตอบคำถามสี่มิติได้ก่อนลงรายละเอียดผิว**

| Lens | Questions to answer | Edge device example |
|---|---|---|
| **Function** | ใช้ทำอะไร ในสภาพแวดล้อมใด | มอนิเตอร์สิ่งแวดล้อม · สวมใส่ · ติดเครื่องจักร |
| **Form & Proportion** | สัดส่วนจับถนัดไหม สมดุลไหม | สูงเกินไปจนล้มง่าย · ขอบคม |
| **Material & Manufacturing** | พิมพ์ 3D / ฉีดพลาสติก / CNC ได้จริงไหม | ผนังบางเกิน · โพรงพิมพ์ยาก |
| **User Experience** | เปิดฝา ดู LED เสียบสายได้โดยไม่พึ่งคู่มือยาวไหม | ช่อง USB หันผิดทาง |

อ่านนิยามวิชาชีพเพิ่ม: [IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/what-is-industrial-design/)

สำหรับอุปกรณ์ที่มี PCB ภายใน ให้เพิ่มเลนส์ที่ห้าในใจตลอดคอร์ส:

> **Electronics fit** — ทุกมิลลิเมตรของกล่องต้องอ้างอิงชิ้นส่วนจริงหรือ placeholder ที่วัดแล้ว

แนวทางลำดับงาน enclosure ที่ใช้ในอุตสาหกรรมต้นแบบ (สรุปจากบทความ [All About Circuits](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/) และ [Protolabs Network](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)):

1. โมเดล **ชิ้นภายในก่อน** (PCB, battery, connectors)  
2. สร้าง **เปลือกนอก** แล้วเว้นผนัง + clearance  
3. เจาะช่องพอร์ต / LED / เซ็นเซอร์  
4. แยกฝาบน–ฐาน · เตรียมจุดยึด (bosses) ในโมดูลหลัง  
5. ตรวจ interference ก่อนพิมพ์  

---

## 3. Concept → Block → Final (Do Not Skip Stages)

| Stage | Deliverable | Do not do yet |
|---|---|---|
| **Concept** | สัดส่วนหยาบ ทิศทางรูปทรง ใครถือ/วางอย่างไร | วัสดุเงา · fillet เล็ก · สกรูละเอียด |
| **Block Model** | กล่องแทน PCB + แบต + โมดูล · enclosure นอกตามสเกล mm | Boolean ช่องพอร์ตสวย · UV |
| **Final Model** | รายละเอียดใช้งานจริง (ไปต่อ M02+) | — |

### 3.1 Concept (15–20 นาทีบนกระดาษก็พอ)

ก่อนเปิด Blender ให้ตอบสั้น ๆ ใน checklist:

1. ผู้ใช้ถือเครื่องอย่างไร (มือ / โต๊ะ / ติดผนัง)  
2. พอร์ตไหนต้องเห็นจากภายนอก  
3. เซ็นเซอร์ไหนต้องการช่องเปิดอากาศ / มุมมอง  
4. ฝาเปิดทางไหน (บน / ด้านข้าง)  

### 3.2 Block Model (หัวใจของ M01)

Block = **รูปทรงหยาบที่ขนาดถูกต้อง**

- PCB = กล่องบางตาม กว้าง × ยาว × หนา  
- Enclosure = กล่องด้านนอกที่หุ้มชิ้นส่วนภายใน  
- เว้นระยะภายในตามแนวทาง clearance (ดู §4)  

### 3.3 Final Model (ยังไม่จบใน M01)

รายละเอียด fillet, พื้นผิว, ช่องเจาะสวยงาม = **M02**  
Animation เปิดฝา = **M03**

> **Key phrase**  
> รายละเอียดผิวเร็วเกินไปบนสเกลผิด = งานสวยที่ใส่บอร์ดจริงไม่ได้

---

## 4. Enclosure and PCB Housing Workflow

### 4.1 Collect real sizes first

ลำดับที่แนะนำ:

1. **วัดบอร์ดจริงด้วยเวอร์เนีย** (กว้าง × ยาว × หนา + ความสูงชิ้นส่วนสูงสุด)  
2. หรือเปิดเอกสารชุดประเมินผลที่ใช้ — เช่น [KIT_PSE84_EVAL guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) และ **Hardware design files** จาก [PSOC Edge kits page](https://documentation.infineon.com/psocedge/docs/hgn1762692110909)  
3. จดแหล่งที่มาของตัวเลขลง [checklist](resources/scale-and-block-checklist.md)  

ถ้ายังไม่มีบอร์ดในมือ ใช้ **Lab placeholder** ใน [แล็บ](../l02-lab/README.md) (ขนาดฝึกที่ประกาศชัด) แล้วเปลี่ยนเป็นขนาดจริงภายหลังได้

### 4.2 Lab clearance rules of thumb

ตัวเลขเริ่มต้นจากแนวทาง enclosure สำหรับพิมพ์ 3D ([Protolabs Network](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/), [All About Circuits](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)):

| Parameter | Lab default | Notes |
|---|---|---|
| ระยะ PCB ↔ ผนังด้านใน | **≥ 0.5 mm** ต่อด้าน | FDM มักเผื่อมากกว่า (ถึง ~1 mm) |
| ความหนาผนัง (wall) | **≈ 2.0 mm** | ขั้นต่ำที่แนะนำสำหรับ enclosure ทั่วไป |
| ช่องว่างเหนือชิ้นส่วนสูงสุด | **≥ 2–3 mm** | สายไฟ / หัว USB / ความคลาดเคลื่อนพิมพ์ |
| ช่องพอร์ต | เผื่อรอบปลั๊ก | อย่าเจาะพอดีพิกเซลกับ connector |

ใน **M01** คุณยังไม่ต้อง Solidify ผนังจริง — แต่ต้องวาด **outer box** ให้ใหญ่กว่า PCB อย่างน้อย:

```text
outer_X ≈ PCB_X + 2×clearance + 2×wall
outer_Y ≈ PCB_Y + 2×clearance + 2×wall
outer_Z ≈ PCB_Z_stack + top_air + bottom_air + wall(s)
```

ตัวอย่างตัวเลข (เมื่อ PCB = 80 × 55 × 1.6 mm, clearance 0.5, wall 2, top air 3, bottom 1):

```text
inner needs ≈ 81 × 56 × (1.6+3+1) 
outer ≈ 81+4 × 56+4 × …  → ประมาณ 85 × 60 × ความสูงที่คำนวณ
```

จดสูตรและตัวเลขจริงของคุณใน checklist — อย่าจำจากตัวอย่างอย่างเดียว

### 4.3 Interference check (manual, no physics required)

ใน Blender Viewport:

1. ดูจากมุม Orthographic บน/ด้านข้าง ([Viewports](https://docs.blender.org/manual/en/4.5/editors/3dview/navigate/views.html))  
2. สลับ Wireframe (`Z` → Wireframe) เพื่อเห็น PCB ภายใน  
3. ยืนยันว่า PCB **ไม่ทะลุ** ผนังนอกโดยไม่ตั้งใจ  
4. ถ้าวัตถุทับกันผิดปกติ — ขยายกล่องนอก หรือย่อชิ้นแทน PCB  

---

## 5. Hands-on in Blender — Scene Units and Scale Accuracy

ทำตามทีละขั้น (ใช้คู่กับ [แล็บ](../l02-lab/README.md))

### 5.1 Install and open a clean file

1. ติดตั้งจาก [blender.org/download](https://www.blender.org/download/) (แนะนำสาย **LTS** ให้ตรงคู่มือ 4.5 เมื่อเป็นไปได้)  
2. `File → New → General`  
3. ลบ Cube เริ่มต้นถ้าต้องการฉากว่าง: เลือก → `X` → Delete  

ทบทวน UI: [Interface](https://docs.blender.org/manual/en/4.5/interface/index.html) · วิดีโอ [Fundamentals](https://studio.blender.org/training/blender-fundamentals-45-lts/) · ไทย [INC111-2021](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

### 5.2 Set metric millimeters (lab recipe)

ตามแผง [Scene Properties → Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units):

1. คลิกไอคอน **Scene Properties** (กรวย/ฉาก ทางขวา)  
2. ส่วน **Units**:  
   - **Unit System** = `Metric`  
   - **Length** = `Millimeters`  
   - **Unit Scale** = `0.001`  

> **ทำไมใส่ 0.001?**  
> คู่มือ Blender อธิบายว่า Unit Scale เป็นตัวแปลงระหว่างหน่วยภายในกับตัวเลขบน UI ([Scene Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units))  
> ในงานโมเดลผลิตภัณฑ์/พิมพ์ 3D นิยมตั้งแบบนี้เพื่อให้พิมพ์ตัวเลข `80` แล้วได้ความยาวระดับมิลลิเมตรบน UI สอดคล้องกับการคิดแบบวิศวกรรม (แนวทางเดียวกับคู่มือชุมชนเช่น [Blender for 3D Printing — Units](https://daler.github.io/blender-for-3d-printing/interface/transforms.html))

**กฎทีม:** ทั้งทีมต้องใช้สูตรหน่วยเดียวกัน และจดใน checklist — ตอน export Twin ใน M04 จะได้ไม่สเกลเพี้ยนคนละไฟล์

ตรวจกริด (ถ้าเส้นหายไปเพราะสเกลเล็ก):

- Overlay → Grid · ปรับ Scale ของกริดให้มองเห็นช่วงงาน ~10–100 mm  

เปิดการวัดขอบใน Edit Mode ได้จาก Overlay → **Measurements** ([Mesh edit overlays](https://docs.blender.org/manual/en/4.5/modeling/meshes/mesh_analysis.html) / overlay panel) เพื่ออ่านความยาวขอบ

### 5.3 Create a PCB placeholder (exact dimensions)

1. `Add → Mesh → Cube`  
2. Object Mode → แผง **Item** (`N`) → **Dimensions**  
3. ใส่ค่า เช่น `X=80 mm`, `Y=55 mm`, `Z=1.6 mm` (หรือค่าที่วัดจริง)  
4. ตั้งชื่อวัตถุ: `PCB_placeholder`  
5. **Object → Set Origin → Origin to Geometry** ([Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html))  
6. ย้ายให้อยู่เหนือพื้นเล็กน้อย (เช่น Location Z ตามความหนาฐานที่จะออกแบบ)  
7. **Object → Apply → Scale** (`Ctrl+A` → Scale) — อ่านเหตุผลใน [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

หลัง Apply Scale ค่า Scale ในแผง Item ควรเป็น `1, 1, 1` ในขณะที่ Dimensions ยังเป็นขนาดจริง

### 5.4 Create the enclosure block

1. `Add → Mesh → Cube` ชื่อ `Enclosure_block`  
2. ตั้ง Dimensions ตามสูตร §4.2  
3. Origin to Geometry · Apply Scale  
4. จัดตำแหน่งให้ PCB อยู่กลางช่องว่างภายใน (ดู Wireframe)  
5. (ทางเลือก) ใส่ **Material** สีต่างกันชั่วคราวแค่แยกชิ้น — ยังไม่ต้อง PBR จริง  

ยังไม่ต้องเจาะช่องพอร์ตใน M01 — แค่ block ที่ “หุ้มได้”

### 5.5 Optional: ชิ้นแทนแบตเตอรี่หรือจอแสดงผล

ถ้าโปรเจกต์มี **แบตเตอรี่** หรือ **จอแสดงผล** (display):

- สร้าง Cube เพิ่มตามขนาดคร่าว ๆ จาก datasheet  
- วางใน enclosure แล้วตรวจว่าไม่ชน PCB  

---

## 6. Topology and Mesh Optimization (What You Need in M01)

จาก [Mesh Structure](https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html):

| Element | Short meaning |
|---|---|
| **Vertex** | จุดในพื้นที่ |
| **Edge** | เส้นเชื่อมสองจุด |
| **Face** | พื้นผิว (tri / quad / n-gon) |

สำหรับ **block enclosure** ใน M01:

| Do | Avoid |
|---|---|
| ใช้ Cube แล้วปรับ Dimensions | Subdivision ทับซ้อนโดยไม่จำเป็น |
| เก็บชิ้นส่วนแยก object (`PCB_…`, `Enclosure_…`) | รวมเป็นก้อนเดียวตั้งแต่แรก |
| Apply Scale หลังปรับขนาด | ปล่อย Scale เป็น 2.0, 0.5, … |
| Flat shading ของกล่องก็พอ | Smooth ทุกอย่างจนมองไม่เห็นขอบประกอบ |

**Optimization ในระดับ M01** = อย่าเพิ่ม polygon จนกว่าสเกลและ clearance จะถูกล็อก  
การลด poly สำหรับ Twin จะทบทวนอีกครั้งก่อน export ใน M04

**Non-manifold / รูรั่ว** สำคัญตอน STL ใน M06 — ตอนนี้ถ้าใช้ Cube ตันเป็น block ยังไม่ต้องกังวล manifold ของเปลือกกลวง

---

## 7. Origin and Axis Habits (Prepare for Twin)

สิ่งที่ควรทำตั้งแต่ M01 เพื่อให้งานใน M03–M04 ง่ายขึ้น:

| Habit | Why |
|---|---|
| วาง Origin ที่กึ่งกลางฐานกล่อง หรือมุมประกอบ | วางบนโต๊ะใน Twin ได้ง่าย |
| ให้แกนตั้งฉากกับพื้นของฉาก | หมุนฝาใน M03 แล้วไม่เอียงผิดทาง |
| ตั้งชื่อ object เป็นภาษาอังกฤษสั้น ชัด | อ้างชื่อใน clip list / Twin ได้ง่าย |
| ทั้งทีมใช้หน่วยเดียวกัน | กันไฟล์คนละสเกล (เช่น ผิด 1000 เท่า) เมื่อรวมงาน |

ตั้ง origin: [Object Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)

---

## 8. How M01 Feeds the Rest of Course 3

| Carry forward from M01 | Use in |
|---|---|
| Block ถูกสเกล + checklist | M02 ขึ้นรูปละเอียด / PBR |
| ชิ้นส่วนแยกฝา–ฐานในใจแล้ว | M03 animation เปิด–ปิด |
| Origin / หน่วยทีม | M04 GLB → Bitstream Studio |
| Clearance ที่จดไว้ | M05 validation · M06 พิมพ์และ fitment |

---

## Next Steps

1. ทำแล็บทีละขั้น: [แล็บ](../l02-lab/README.md)  
2. กรอก [scale-and-block-checklist.md](resources/scale-and-block-checklist.md)  
3. เมื่อพร้อม ไปต่อ [M02 — Modeling, Materials, and Render](../../m02-modeling-render/l01-modeling-materials-render/README.md)

---

## References and Further Reading

### Blender (official)

1. [Download Blender](https://www.blender.org/download/)  
2. [Scene Properties — Units (4.5 LTS)](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units)  
3. [Apply Location / Rotation / Scale (4.5 LTS)](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)  
4. [Mesh Structure](https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html) · [Mesh Modeling](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)  
5. [Object Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)  
6. [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)  
7. [INC111-2021 Blender playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)  

### Industrial design & enclosure practice

8. [IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/what-is-industrial-design/)  
9. [Six Steps for Designing a Custom 3D Printed Electronics Enclosure (All About Circuits)](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)  
10. [How do you design enclosures for 3D printing? (Protolabs Network)](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)  
11. [Blender for 3D Printing — Units](https://daler.github.io/blender-for-3d-printing/interface/transforms.html) (แนวทาง Unit Scale กับงาน mm)  

### Hardware / course portals

12. [KIT_PSE84_EVAL documentation](https://documentation.infineon.com/psocedge/docs/lne1762692969598) · [PSOC Edge kits + design files](https://documentation.infineon.com/psocedge/docs/hgn1762692110909)  
13. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)  
14. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
15. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  
16. [Course 3 TOC](../../README.md) · [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: กล่องหุ้มแบบ block ตามสเกลฮาร์ดแวร์](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/scale-and-block-checklist.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)
