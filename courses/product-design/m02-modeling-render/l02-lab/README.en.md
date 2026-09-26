---
id: pdesign.m02.l02
lang: en
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
source_sha256: e1bfad2fb28359cffdb0afbe48b17982302b1621f671f7774532235fb458cdbf
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M02/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M02 — Refine Model, PBR, and Render

**Course 3 · Module 2**
**Type:** Hands-on (detail modeling · materials · lighting · render)
**Suggested time:** ~3.5–4 hours

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

- Develop the file from M01 to have at least **2** openings
- Split the **lid** and the **base** into separate objects
- Add at least **2** PBR materials
- Render at least **1** presentation image (2 recommended: beauty + technical)
- Fill in [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md)

---

## Prerequisites

- [ ] Have `m01_block_enclosure.blend` (or equivalent) from [M01](../../m01-design-fundamentals/l02-lab/README.md)
- [ ] Units are still Metric + mm per the team's convention
- [ ] The PCB placeholder is still in the scene

Copy the file to `m02_enclosure_detail.blend` before editing — keep the original M01 file intact.

---

## Lab A — Lock scale, then thicken (required)

1. Open the file · check that `PCB_placeholder`'s Dimensions still match the M01 checklist
2. `Ctrl+A` → Scale on the enclosure
3. Thicken the wall to about **2 mm** (Solidify, or the hollowing-out approach from Lesson §2.2)
4. Wireframe: confirm the PCB is still inside and does not collide with the wall

**Pass when:** the wall thickness is clearly visible, and the PCB's scale has not changed unintentionally

---

## Lab B — Cut at least two openings (required)

1. Create a cutter for opening 1 (for example, USB)
2. Boolean **Difference** on the enclosure
3. Make opening 2 (sensor / LED / button)
4. Check the opening size allows margin for the connector, per the M01 guidance
5. Apply the Boolean once satisfied · give the object a meaningful name

**Pass when:** ≥ 2 openings are visible from outside the camera view

---

## Lab C — Bevel and split lid / base (required)

1. Round the outer edges the hand touches (Bevel ≈ 0.5–1.5 mm)
2. Split into `Enclosure_base` and `Enclosure_lid`
3. Position the lid's Origin at the hinge edge or the centre of the back edge (preparing for rotation in M03)

**Pass when:** the Outliner shows at least 2 objects for the box, and the lid can be moved separately from the base

---

## Lab D — Two PBR materials (required)

1. Create `Plastic_matte_body` using the lesson's starting values (or equivalent)
2. Create a second material (rubber / metal / buttons)
3. Assign it to the relevant part
4. Record the Base Color / Roughness / Metallic values in the look-dev sheet

**Pass when:** Materials ≥ 2, and the surface difference is visible in Material Preview or the Rendered viewport

---

## Lab E — Lights, camera, render (required)

1. Choose EEVEE (or Cycles if your machine can handle it)
2. Set up three-point lighting, **or** a World + one Area light
3. Frame a three-quarter camera angle that shows the ports
4. Render ≥ 1 image at a resolution of at least 1280×720 (1920×1080 recommended)
5. Save the PNG, for example `m02_beauty.png`
6. (Recommended) render a technical angle, `m02_ports.png`

**Pass when:** there are image files in the project folder, and the sheet is filled in completely

---

## Lab F — Optional

- A subtle Emission on the LED
- Compare the surfacing with the models in [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)
- Render one comparison pair with Cycles versus EEVEE

---

## Deliverables checklist

- [ ] `m02_enclosure_detail.blend`
- [ ] Openings ≥ 2 · lid/base split
- [ ] Materials ≥ 2
- [ ] PNG renders ≥ 1
- [ ] [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md) filled in completely

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| The Boolean hole is wrong / doesn't cut | Apply Scale · try the Exact solver · check the cutter really overlaps the wall |
| The bevel is uneven | Apply Scale · reduce the bevel width |
| The PCB no longer fits after Solidify | The wall grew too far inward — enlarge the box, or offset the wall outward |
| The material looks entirely black | Add more light / turn on Material Preview · check Metallic isn't accidentally 1 on plastic |
| Rendering is very slow | Switch to EEVEE · temporarily lower the resolution |

[Lesson](../l01-modeling-materials-render/README.md) · [Look-dev sheet](../l01-modeling-materials-render/resources/material-lighting-sheet.md) · [TOC](../../README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)
