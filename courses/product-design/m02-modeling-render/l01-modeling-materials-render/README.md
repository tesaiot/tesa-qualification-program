---
id: pdesign.m02.l01
lang: th
title:
  th: รายละเอียดกล่อง วัสดุ PBR และภาพนำเสนอ
  en: Enclosure Detail, PBR Materials and Presentation Renders
summary:
  th: Apply Scale, Solidify, Boolean, Bevel และการแยกฝา/ฐาน วัสดุ Principled BSDF แสงสามจุด กล้อง และการเรนเดอร์
  en: Apply Scale, Solidify, Boolean, Bevel and splitting lid from base; Principled BSDF materials, three-point lighting, camera and rendering.
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
- pdesign.m01.l02
objectives:
- th: เพิ่มรายละเอียดกล่อง (Solidify ≈ 2 mm, Boolean Difference เจาะช่อง, Bevel, แยกฝา/ฐาน) โดยไม่ทำให้ขนาดที่ล็อกไว้ในโมดูล 1 เสีย
  en: Add enclosure detail (Solidify ≈ 2 mm, Boolean Difference openings, Bevel, split lid/base) without breaking the size locked in module 1.
- th: ตั้งวัสดุ Principled BSDF อย่างน้อยสองชนิด โดยเลือก Base Color, Roughness และ Metallic ให้เหมาะกับพลาสติกและโลหะ
  en: Set up at least two Principled BSDF materials, choosing Base Color, Roughness and Metallic for plastic and metal.
- th: จัดแสงและกล้อง แล้วเรนเดอร์ภาพนำเสนออย่างน้อยหนึ่งภาพด้วย EEVEE หรือ Cycles
  en: Light the scene, place a camera and render at least one presentation image with EEVEE or Cycles.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: hwdev.enclosure
  to: 2
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — Modeling, Materials, and Render

**Course 3 · Module 2**  
**Suggested time:** ประมาณ 4 ชั่วโมง — พัฒนากล่องหยาบจาก M01 ให้มีรายละเอียด ใส่วัสดุ PBR จัดแสง แล้วเรนเดอร์ภาพนำเสนอ  
**Format:** บทเรียนลงมือทำ — อ่านแล้วทำตามใน Blender ได้เลย; ภาพเคลื่อนไหวเปิดฝาไปที่ [M03](../../m03-motion/l01-motion-and-interaction/README.md)

[Lab](../l02-lab/README.md) · [Look-dev sheet](resources/material-lighting-sheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. พัฒนารูปทรงที่ซับซ้อนขึ้นจาก block model (hard-surface / ช่องพอร์ต / ความหนาผนัง)  
2. กำหนดวัสดุ พื้นผิว และรายละเอียดผิวในแนว **PBR**  
3. จัดแสงและเรนเดอร์ภาพคุณภาพสูงสำหรับนำเสนอ  
4. สร้าง **Product visualization** ที่เหมาะกับงานอุตสาหกรรมและสื่อการสอน  

> **Key phrase**  
> ใน M02 ให้**เพิ่มรายละเอียดโดยไม่ทำลายขนาดที่ล็อกไว้ใน M01** — ช่องพอร์ตสวยแต่บอร์ดใส่ไม่ได้ = ยังไม่ผ่าน

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M01 — Industrial Design Fundamentals](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) | block model + หน่วย mm ที่ต้องคงไว้ |
| **[Boolean Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html)** | เจาะช่องพอร์ต / เซ็นเซอร์ |
| **[Solidify Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html)** | กำหนดความหนาผนัง |
| **[Bevel (edit) / Bevel Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html)** | ขอบมนที่ผู้ใช้สัมผัส |
| **[Mirror Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html)** | ชิ้นส่วนสมมาตร |
| **[Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | `Ctrl+A` ก่อน Boolean / Bevel |
| **[Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html)** | วัสดุ PBR หลัก |
| **[Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html)** | สร้างและกำหนด material |
| **[EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html)** | เรนเดอร์เร็วสำหรับดูผล |
| **[Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html)** | เรนเดอร์คุณภาพสูงกว่า (ถ้าเครื่องไหว) |
| **[Light objects](https://docs.blender.org/manual/en/4.5/render/lights/light_object.html)** | Area / Point / Sun |
| **[World & Environment](https://docs.blender.org/manual/en/4.5/render/lights/world.html)** | HDRI / พื้นหลังสตูดิโอ |
| **[Cameras](https://docs.blender.org/manual/en/4.5/render/cameras.html)** | มุมกล้องนำเสนอ |
| **[glTF materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)** | เตรียมวัสดุให้ส่ง Twin ได้ใน M04 |
| **[Blender Fundamentals — Modeling](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)** | วิดีโอทางการ |
| **[INC111-2021 (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Tutorial ภาษาไทย |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | ดูตัวอย่างวัสดุ/โมเดล (อ้างอิงเท่านั้น) |
| [Look-dev sheet](resources/material-lighting-sheet.md) | บันทึกค่าวัสดุ แสง และไฟล์ render |

---

## 1. From Block to Product Detail (Keep Scale)

ใน [M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) คุณมีอย่างน้อย:

- `PCB_placeholder` ตามขนาดจริง  
- `Enclosure_block` ที่หุ้มได้  

ใน M02 คุณจะ:

1. ทำให้กล่องมี**ผนังหนา** (ไม่ใช่ก้อนตันอย่างเดียว)  
2. **เจาะช่อง** พอร์ต / LED / เซ็นเซอร์ อย่างน้อย 2 จุด  
3. **มนขอบ** ที่ผู้ใช้จับ  
4. **แยกฝาบน–ฐาน** เป็น object คนละชิ้น (เตรียม M03 / พิมพ์ M06)  
5. ใส่วัสดุ + แสง + เรนเดอร์ภาพนำเสนอ  

```text
M01 block (solid sizes locked)
    → Solidify / shell thickness
    → Boolean cutouts
    → Bevel edges
    → Split lid / base
    → Materials (Principled BSDF)
    → Lights + camera
    → Render PNG
```

อย่าเปลี่ยน Dimensions ของ PCB โดยไม่จดเหตุผล — ถ้าต้องขยายกล่อง ให้แก้ตามสูตร clearance ใน M01 แล้วอัปเดต checklist

---

## 2. Modeling Techniques You Will Use

### 2.1 Always Apply Scale first

ก่อน Boolean / Bevel / Solidify:

1. Object Mode → เลือกวัตถุ  
2. `Ctrl+A` → **Scale**  

ถ้าลืม Scale ไม่เป็น `1,1,1` ขอบมนและรูเจาะมักเพี้ยน — อ่าน [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

### 2.2 Solidify — ความหนาผนัง

[Solidify Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) เพิ่มความหนาให้ผิว mesh

แนวทางในแล็บ (ต่อจาก M01):

| Step | What to do |
|---|---|
| 1 | เริ่มจากกล่องตัน หรือลบหน้าด้านในทีหลังตาม workflow ที่เลือก |
| 2 | ใส่ Solidify · Thickness ≈ **2.0 mm** (ค่าเริ่มต้นจากแนวทางพิมพ์ 3D ใน M01) |
| 3 | เปิด Even Thickness ถ้ามีตัวเลือกและผลดูสม่ำเสมอ |
| 4 | ตรวจว่า PCB ยังอยู่ภายในและไม่ชนผนัง |

> สำหรับผู้เริ่มต้น: ใช้ **กล่องตัน + Boolean เจาะโพรงด้านใน** หรือ **Solidify จากเปลือก** ก็ได้ — สำคัญคือความหนาผนังประมาณ 2 mm และ PCB ยังใส่ได้

### 2.3 Boolean — เจาะช่องพอร์ตและเซ็นเซอร์

[Boolean Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html):

| Operation | Use in this lab |
|---|---|
| **Difference** | เจาะรูออกจากกล่อง (พอร์ต USB, ช่องเซ็นเซอร์, หน้าต่าง LED) |
| Union / Intersect | น้อยกว่าใน M02 — เก็บไว้เมื่อรวมชิ้นส่วน |

ขั้นตอนสั้น:

1. สร้าง Cube/Cylinder เป็น `Cutter_USB` ตามขนาดช่อง (เผื่อ clearance รอบ connector)  
2. วาง cutter ให้ทับผนังตรงตำแหน่งพอร์ต  
3. บน enclosure: Add Modifier → **Boolean** → Operation **Difference** → Object = cutter  
4. ถ้าผลแปลก ลอง Solver **Exact**  
5. เมื่อพอใจ ค่อย Apply modifier · ซ่อนหรือลบ cutter  

ทำอย่างน้อย **2 ช่อง** (เช่น USB + ช่องเซ็นเซอร์ หรือ LED)

### 2.4 Bevel — ขอบมน

ขอบคมเกินไปจับไม่สบายและพิมพ์ยาก — ใช้ [Bevel](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html):

- Edit Mode: เลือกขอบ → `Ctrl+B` ลากเมาส์  
- หรือ Bevel Modifier ทั้งชิ้น (ระวังอย่ามนจนช่องพอร์ตเสียรูป)

รัศมีเริ่มต้นในแล็บ: ประมาณ **0.5–1.5 mm** ที่ขอบนอกที่มือจับ

### 2.5 Mirror — ชิ้นสมมาตร (ถ้ามี)

[Mirror Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html) ใช้เมื่อฝาหรือปุ่มสมมาตรซ้าย–ขวา — ลดงานซ้ำ

### 2.6 Split lid and base

ตั้งแต่ M02 ให้แยกอย่างน้อย:

| Object name | Role |
|---|---|
| `Enclosure_base` | ฐาน / ตัวล่าง |
| `Enclosure_lid` | ฝาบน |

วิธีง่าย: ใน Edit Mode เลือกหน้าด้านบน → `P` → Selection เป็น object ใหม่ · หรือตัดด้วย plane + Boolean แล้วแยกชิ้น

เหตุผล: M03 หมุนฝา · M06 พิมพ์แยกชิ้น

---

## 3. Materials with Principled BSDF (PBR)

**PBR** = Physically Based Rendering — วัสดุตอบสนองแสงใกล้ความจริงเมื่อเปลี่ยนมุมไฟ

ใน Blender ใช้โหนดหลัก [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) (เข้ากันดีกับ [glTF](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials) ใน M04)

### 3.1 Create a material

1. เลือกวัตถุ → แท็บ **Material Properties**  
2. New → ตั้งชื่อ เช่น `Plastic_matte_body`  
3. เปิด Shader Editor ถ้าต้องการเห็นโหนด ([Materials intro](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html))  

### 3.2 Parameters you must understand

| Parameter | Meaning | Lab tip |
|---|---|---|
| **Base Color** | สีพื้น | พลาสติกตัวเครื่อง: เทาอ่อน / ขาวหม่น |
| **Roughness** | ด้าน ↔ เงา (0 = เงามาก, 1 = ด้าน) | พลาสติกด้าน ≈ 0.45–0.7 |
| **Metallic** | 0 = ไม่ใช่โลหะ, 1 = โลหะ | พลาสติก = **0** · โลหะปุ่ม/พอร์ต = **1** |
| **Specular / IOR** (ตามเวอร์ชัน) | ความเงาสะท้อนของฉนวน | ใช้ค่าเริ่มต้นก่อน แล้วค่อยปรับ |
| **Emission** (ทางเลือก) | แสงออกจากผิว | LED จำลอง — ความเข้มต่ำพอ |

### 3.3 Two materials minimum (lab presets)

คัดลอกค่าเริ่มต้นนี้แล้วปรับได้ — จดค่าจริงใน [look-dev sheet](resources/material-lighting-sheet.md)

**A — Matte plastic (ตัวเครื่อง)**

| Parameter | Starting value |
|---|---|
| Base Color | RGB ≈ 0.75, 0.75, 0.78 |
| Roughness | 0.55 |
| Metallic | 0.0 |

**B — Contrast accent (ยางขาตั้ง / โลหะพอร์ต / ปุ่ม)**

| Parameter | Rubber feet | Brushed metal accent |
|---|---|---|
| Base Color | 0.05, 0.05, 0.05 | 0.7, 0.7, 0.72 |
| Roughness | 0.7 | 0.35 |
| Metallic | 0.0 | 1.0 |

กำหนด material คนละชิ้น หรือใช้หลาย material slots บน mesh เดียวกัน (Edit Mode → Assign)

---

## 4. Lighting and Camera for Product Shots

### 4.1 Render engine

| Engine | Use when | Manual |
|---|---|---|
| **EEVEE** | ดูผลเร็ว · แล็บส่วนใหญ่ | [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) |
| **Cycles** | ภาพนำเสนอสุดท้ายถ้าเครื่องไหว | [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html) |

ตั้งที่ Render Properties → Render Engine

### 4.2 Simple three-point light (เริ่มต้นที่แนะนำ)

อ้างอิงแนวคิดไฟสตูดิโอ + [Light objects](https://docs.blender.org/manual/en/4.5/render/lights/light_object.html):

| Light | Role | Starting idea |
|---|---|---|
| Key | ไฟหลัก | Area Light ด้านหน้า–ข้าง · Power พอเห็นขอบ |
| Fill | ลดเงามืด | Area อ่อนกว่าฝั่งตรงข้าม |
| Rim / back | แยกวัตถุจากพื้นหลัง | ไฟด้านหลังบาง ๆ |

หรือใช้ **World HDRI** ([World](https://docs.blender.org/manual/en/4.5/render/lights/world.html)) เป็นแสงแวดล้อม แล้วเติมไฟ Area หนึ่งดวงเพื่อเน้นขอบชิ้นงาน

พื้นหลัง: สีเทาอ่อนหรือพื้น plane เรียบ — อย่าให้ลายรบกวนการอ่านรูปทรง

### 4.3 Camera

[Cameras](https://docs.blender.org/manual/en/4.5/render/cameras.html):

1. `Add → Camera`  
2. มุมแนะนำ: **three-quarter** หรือ isometric-ish ที่เห็นฝา + พอร์ตด้านข้าง  
3. `Ctrl+Alt+Numpad0` จัดกล้องตามมุมมองปัจจุบัน (ถ้าระบบรองรับ)  
4. เปิด Lock Camera to View ชั่วคราวขณะจัดมุม แล้วปิดก่อนเรนเดอร์  

ถ่ายอย่างน้อย:

- 1 ภาพ **beauty** (สื่อสารรูปทรง/วัสดุ)  
- (แนะนำ) 1 ภาพ **technical** ที่เห็นช่องพอร์ตหรือตำแหน่ง PCB ชัด  

---

## 5. Render Output

1. Output Properties → Resolution เช่น **1920 × 1080**  
2. File Format = **PNG**  
3. ตั้ง Output path ในโฟลเดอร์โปรเจกต์  
4. `F12` หรือ Render → Render Image  
5. Image → Save As…  

จด engine, samples/คุณภาพ, ชื่อไฟล์ลง [material-lighting-sheet.md](resources/material-lighting-sheet.md)

---

## 6. Quality Gate Before M03

| Check | Pass means |
|---|---|
| Scale from M01 still valid | PCB ยังใส่ได้ใน Wireframe |
| Openings ≥ 2 | พอร์ต/เซ็นเซอร์/LED ชัด |
| Lid and base are separate objects | พร้อม animate ใน M03 |
| Materials ≥ 2 | Principled BSDF · ค่าจดใน sheet |
| At least one render | PNG ในโฟลเดอร์ผลงาน |
| Apply Scale done | ไม่มี Scale เพี้ยนก่อน modifier |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. กรอก [material-lighting-sheet.md](resources/material-lighting-sheet.md)  
3. เมื่อพร้อม ไปต่อ [M03 — Motion and Interaction](../../m03-motion/l01-motion-and-interaction/README.md)

---

## References and Further Reading

### Blender modeling

1. [Boolean Modifier (4.5 LTS)](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html)  
2. [Solidify Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html)  
3. [Bevel Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html)  
4. [Mirror Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html)  
5. [Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)  
6. [Fundamentals — Modeling](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)  

### Materials, lights, render

7. [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html)  
8. [Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html)  
9. [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) · [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html)  
10. [Light objects](https://docs.blender.org/manual/en/4.5/render/lights/light_object.html) · [World](https://docs.blender.org/manual/en/4.5/render/lights/world.html)  
11. [Cameras](https://docs.blender.org/manual/en/4.5/render/cameras.html)  
12. [glTF materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)  

### Course portals

13. [INC111-2021 Blender (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)  
14. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  
15. [M01 enclosure clearance refs](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [Course 3 TOC](../../README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: ขัดเกลาโมเดล วัสดุ PBR และเรนเดอร์](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Look-dev sheet](resources/material-lighting-sheet.md) · [← TOC](../../README.md) · [← M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)
