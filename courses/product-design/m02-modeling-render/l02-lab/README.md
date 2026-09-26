---
id: pdesign.m02.l02
lang: th
title:
  th: 'แล็บ: ขัดเกลาโมเดล วัสดุ PBR และเรนเดอร์'
  en: 'Lab: Refine Model, PBR, and Render'
summary:
  th: ล็อกสเกล เพิ่มความหนาผนัง เจาะช่องอย่างน้อยสองจุด แยกฝา/ฐาน ใส่วัสดุ PBR สองชนิด แล้วเรนเดอร์
  en: Lock scale, thicken the walls, cut at least two openings, split lid and base, add two PBR materials and render.
level: L2
time_min:
  lab: 240
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m02.l01
objectives:
- th: เจาะช่องเปิด ≥ 2 จุด และแยกฝา/ฐานเป็นคนละ object โดย PCB ยังใส่ได้
  en: Cut at least two openings and split lid and base into separate objects while the PCB still fits.
- th: ใส่วัสดุ PBR ≥ 2 ชนิด และเรนเดอร์ PNG ≥ 1 ภาพ พร้อมกรอก material-lighting-sheet.md
  en: Apply at least two PBR materials, render at least one PNG and fill in material-lighting-sheet.md.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: hwdev.enclosure
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
slides: slides.md
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M02/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M02 — Refine Model, PBR, and Render

**Course 3 · Module 2**  
**Type:** Hands-on (detail modeling · materials · lighting · render)  
**Suggested time:** ~3.5–4 ชั่วโมง  

Read first: [Lesson](../l01-modeling-materials-render/README.md) · [Look-dev sheet](../l01-modeling-materials-render/resources/material-lighting-sheet.md) · [← TOC](../../README.md) · [← M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [Boolean Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html) | cutouts |
| [Solidify](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) | wall thickness |
| [Bevel](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html) | soft edges |
| [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) | PBR |
| [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) / [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html) | render |

---

## Lab Goals

- พัฒนาไฟล์จาก M01 ให้มีช่องเปิดอย่างน้อย **2** จุด  
- แยก **ฝา** กับ **ฐาน** เป็นคนละ object  
- ใส่วัสดุ PBR อย่างน้อย **2** ชนิด  
- เรนเดอร์ภาพนำเสนออย่างน้อย **1** ภาพ (แนะนำ 2: beauty + technical)  
- กรอก [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md)  

---

## Prerequisites

- [ ] มี `m01_block_enclosure.blend` (หรือเทียบเท่า) จาก [M01](../../m01-design-fundamentals/l02-lab/README.md)  
- [ ] หน่วยยังเป็น Metric + mm ตามสูตรทีม  
- [ ] PCB placeholder ยังอยู่ในฉาก  

คัดลอกไฟล์เป็น `m02_enclosure_detail.blend` ก่อนแก้ — เก็บต้นฉบับ M01 ไว้

---

## Lab A — Lock scale, then thicken (required)

1. เปิดไฟล์ · ตรวจ Dimensions ของ `PCB_placeholder` ยังตรง checklist M01  
2. `Ctrl+A` → Scale บน enclosure  
3. ทำให้ผนังหนาประมาณ **2 mm** (Solidify หรือวิธีเจาะโพรงตามบทเรียน §2.2)  
4. Wireframe: PCB ยังอยู่ภายในและไม่ชนผนัง  

**Pass when:** ความหนาผนังชัด และสเกล PCB ไม่เปลี่ยนโดยไม่ตั้งใจ

---

## Lab B — Cut at least two openings (required)

1. สร้าง cutter สำหรับช่องที่ 1 (เช่น USB)  
2. Boolean **Difference** บน enclosure  
3. ทำช่องที่ 2 (เซ็นเซอร์ / LED / ปุ่ม)  
4. ตรวจขนาดช่องเผื่อ connector ตามแนวทาง M01  
5. Apply Boolean เมื่อพอใจ · ตั้งชื่อ object ให้สื่อความหมาย  

**Pass when:** มองเห็นช่อง ≥ 2 จากมุมนอกกล้อง

---

## Lab C — Bevel and split lid / base (required)

1. มนขอบนอกที่มือจับ (Bevel ≈ 0.5–1.5 mm)  
2. แยกเป็น `Enclosure_base` และ `Enclosure_lid`  
3. จัด Origin ของฝาที่ขอบบานพับหรือกึ่งกลางขอบหลัง (เตรียมหมุนใน M03)  

**Pass when:** Outliner มีอย่างน้อย 2 object ของกล่อง และเลื่อนฝาแยกจากฐานได้

---

## Lab D — Two PBR materials (required)

1. สร้าง `Plastic_matte_body` ตามค่าเริ่มต้นในบทเรียน (หรือเทียบเท่า)  
2. สร้างวัสดุที่ 2 (ยาง / โลหะ / ปุ่ม)  
3. Assign ให้ชิ้นส่วนที่เกี่ยวข้อง  
4. จดค่า Base Color / Roughness / Metallic ใน look-dev sheet  

**Pass when:** Material ≥ 2 และมองเห็นความต่างของผิวใน Material Preview หรือ Rendered viewport

---

## Lab E — Lights, camera, render (required)

1. เลือก EEVEE (หรือ Cycles ถ้าเครื่องไหว)  
2. ตั้งไฟแบบ three-point **หรือ** World + Area หนึ่งดวง  
3. จัดกล้อง three-quarter ที่เห็นพอร์ต  
4. Render ≥ 1 ภาพ ความละเอียดอย่างน้อย 1280×720 (แนะนำ 1920×1080)  
5. บันทึก PNG เช่น `m02_beauty.png`  
6. (แนะนำ) เรนเดอร์มุมเทคนิค `m02_ports.png`  

**Pass when:** มีไฟล์ภาพในโฟลเดอร์โปรเจกต์และ sheet กรอกครบ

---

## Lab F — Optional

- Emission อ่อน ๆ บน LED  
- เทียบผิวกับโมเดลใน [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  
- Render ด้วย Cycles เปรียบเทียบ EEVEE หนึ่งคู่  

---

## Deliverables checklist

- [ ] `m02_enclosure_detail.blend`  
- [ ] ช่องเปิด ≥ 2 · ฝา/ฐานแยก  
- [ ] วัสดุ ≥ 2  
- [ ] PNG render ≥ 1  
- [ ] [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md) กรอกครบ  

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| Boolean รูเพี้ยน / ไม่เจาะ | Apply Scale · ลอง Solver Exact · ตรวจ cutter ทับผนังจริง |
| Bevel ไม่สม่ำเสมอ | Apply Scale · ลดความกว้าง bevel |
| PCB ใส่ไม่ลงหลัง Solidify | ผนังหนาเข้าด้านในเกินไป — ขยายกล่องหรือ offset ออกนอก |
| วัสดุดูดำทั้งก้อน | เพิ่มไฟ / เปิด Material Preview · ตรวจ Metallic ไม่เป็น 1 โดยไม่ตั้งใจบนพลาสติก |
| Render ช้ามาก | สลับ EEVEE · ลด resolution ชั่วคราว |

[Lesson](../l01-modeling-materials-render/README.md) · [Look-dev sheet](../l01-modeling-materials-render/resources/material-lighting-sheet.md) · [TOC](../../README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)
