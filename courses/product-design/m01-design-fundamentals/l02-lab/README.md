---
id: pdesign.m01.l02
lang: th
title:
  th: 'แล็บ: กล่องหุ้มแบบ block ตามสเกลฮาร์ดแวร์'
  en: 'Lab: Block Model Enclosure at Hardware Scale'
summary:
  th: ตั้งฉากและหน่วย สร้าง PCB placeholder สร้าง enclosure block ที่มี clearance แล้วตั้งชื่อและบันทึกไฟล์
  en: Set up the scene and units, create a PCB placeholder, build an enclosure block with clearance, then name and save the file.
level: L2
time_min:
  lab: 120
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m01.l01
objectives:
- th: ตั้งฉากเป็น Metric + Millimeters และสร้าง PCB placeholder ตามขนาดที่วัดหรือขนาดแล็บ (80 × 55 × 1.6 mm)
  en: Set the scene to Metric + Millimeters and create a PCB placeholder at the measured or lab size (80 × 55 × 1.6 mm).
- th: สร้าง enclosure block ที่มี clearance ตามสูตร Apply Scale ตั้งชื่อ object แล้วบันทึก .blend
  en: Build an enclosure block with the formula's clearance, apply scale, name the objects and save the .blend.
develops:
- skill: hwdev.enclosure
  to: 2
- skill: hwdev.3d-modeling
  to: 2
assesses:
- skill: hwdev.enclosure
  level: 2
  evidence: README.md#deliverables-checklist
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Block Model Enclosure at Hardware Scale

**Course 3 · Module 1**  
**Type:** Hands-on (Blender scene units + PCB placeholder + enclosure block)  
**Suggested time:** ~90–120 นาที  

Read first: [Lesson](../l01-industrial-design-fundamentals/README.md) · [Checklist](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) · [← TOC](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)

### Keep these tabs open while you work

| Resource | Why |
|---|---|
| [Scene Units (Blender Manual)](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units) | Metric / mm / Unit Scale |
| [Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html) | `Ctrl+A` |
| [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html) | pivots |
| [All About Circuits — enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/) | PCB-first mindset |
| [Protolabs — clearance / wall](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/) | 0.5 mm · ~2 mm wall |

---

## Lab Goals

- ตั้งฉาก Blender เป็น **Metric + Millimeters** ตามสูตรทีม  
- สร้าง **PCB placeholder** ตามขนาดที่วัดหรือขนาด Lab default  
- สร้าง **enclosure block** ที่หุ้ม PCB ได้โดยมี clearance ตามบทเรียน  
- Apply Scale · ตั้งชื่อ object · บันทึก `.blend` + สกรีนช็อต  
- กรอก [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md)  

---

## Prerequisites

- [ ] ติดตั้ง [Blender](https://www.blender.org/download/) (แนะนำ LTS)  
- [ ] อ่าน [Lesson §5](../l01-industrial-design-fundamentals/README.md) อย่างน้อยหนึ่งรอบ  
- [ ] โฟลเดอร์โปรเจกต์ เช่น `course3-m01-block/`  
- [ ] (แนะนำ) เวอร์เนีย + บอร์ดจริงที่ใช้  

---

## Size source — pick one track

### Track A — Measure your board (preferred)

1. วัด ก × ย × หนา ของ PCB (mm)  
2. ประมาณความสูงชิ้นส่วนสูงสุด (connector / sensor)  
3. ถ้าเป็นชุด Infineon PSOC Edge ให้เปิด [kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) / [design files index](https://documentation.infineon.com/psocedge/docs/hgn1762692110909) ประกอบการวัด  
4. จดแหล่งที่มาใน checklist  

### Track B — Placeholder (if no board yet)

ใช้ขนาดฝึกนี้แล้วเปลี่ยนเป็นของจริงภายหลังได้:

| Part | X (mm) | Y (mm) | Z (mm) |
|---|---|---|---|
| `PCB_placeholder` | 80 | 55 | 1.6 |
| Tallest component allowance (air above PCB) | — | — | 3.0 |
| Clearance (each side) | 0.5 | 0.5 | — |
| Wall (planned) | 2.0 | 2.0 | 2.0 |

คำนวณ `Enclosure_block` outer ตามสูตรในบทเรียน §4.2 แล้วจดตัวเลขลง checklist **ก่อน** สร้างใน Blender

---

## Lab A — New scene and units (required)

1. `File → New → General`  
2. Scene Properties → **Units**:  
   - Unit System = **Metric**  
   - Length = **Millimeters**  
   - Unit Scale = **0.001**  
3. บันทึกไฟล์: `m01_block_enclosure.blend`  
4. จด Blender version ใน checklist (`Help → About` / splash)  

**Pass when:** เปลี่ยน Dimensions ของ Cube แล้วเห็นหน่วยเป็น mm บน UI

---

## Lab B — PCB placeholder (required)

1. Add Cube → ชื่อ `PCB_placeholder`  
2. ตั้ง **Dimensions** ตาม Track A หรือ B  
3. `Object → Set Origin → Origin to Geometry`  
4. `Ctrl+A` → **Scale** (Scale ต้องเป็น 1,1,1)  
5. จัด Location ให้อยู่เหนือ World Origin พอมองเห็น  
6. (แนะนำ) Overlay → เปิด Measurements ใน Edit Mode แล้วสุ่มวัดขอบหนึ่งด้านให้ตรงตาราง  

**Pass when:** Dimensions ตรงตาราง และ Scale = 1,1,1

---

## Lab C — Enclosure block + fit check (required)

1. คำนวณ outer size (จดใน checklist)  
2. Add Cube → ชื่อ `Enclosure_block`  
3. ตั้ง Dimensions · Origin to Geometry · Apply Scale  
4. จัดตำแหน่งให้ PCB อยู่ภายใน  
5. สลับ Wireframe ตรวจจากมุม Top / Front / Right  
6. ยืนยัน: PCB ไม่โผล่ผนัง · มีช่องว่างคร่าว ๆ ตาม clearance  

**Pass when:** สกรีนช็อต isometric เห็นทั้งสองชิ้น และเพื่อนในทีมอ่าน Dimensions ได้จาก checklist

---

## Lab D — Naming, colors, save (required)

1. ตั้ง viewport color หรือ material ชั่วคราวคนละสี (PCB / Enclosure)  
2. `File → Save`  
3. Export สกรีนช็อต (หรือ Render Viewport) ชื่อ `m01_block_iso.png`  
4. กรอก checklist ให้ครบ  

---

## Lab E — Optional extras

- เพิ่ม `Battery_block` หรือ `Display_block` ตาม datasheet  
- เขียนโน้ต concept 4 ข้อจากบทเรียน §3.1  
- เปรียบเทียบขนาดกับโมเดลใน [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) (ดูสเกลเท่านั้น — อย่าแทนที่งานคุณ)  

---

## Deliverables checklist

- [ ] `m01_block_enclosure.blend`  
- [ ] สกรีนช็อต isometric  
- [ ] [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) กรอกครบ  
- [ ] (ถ้ามีบอร์ด) แหล่งขนาด = วัดจริง และ/หรือเอกสาร kit  

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| กริดหาย / วัตถุเล็กจนมองไม่เห็น | ตรวจ Unit Scale = 0.001 · ซูม · ปรับ Grid overlay |
| พิมพ์ 80 แล้วได้ยักษ์หรือจิ๋ว | ทีมใช้สูตรหน่วยไม่ตรงกัน — รีเซ็ตตาม Lab A |
| Bevel / ปรับขนาดเพี้ยนในภายหลัง | ลืม Apply Scale — ทำ `Ctrl+A` → Scale |
| ไม่แน่ใจขนาดบอร์ด Infineon | วัดจริงก่อน · ใช้ design files จากหน้า kits · อย่าเดาจากรูปเว็บอย่างเดียว |
| Enclosure ดูใหญ่เกิน | ตรวจว่าบวก wall สองด้านครบและไม่บวกซ้ำ |

[Lesson](../l01-industrial-design-fundamentals/README.md) · [Checklist](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) · [TOC](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)
