---
id: pdesign.m01.l02
lang: en
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
translation: done
slides: slides.md
source_sha256: 5a5fe8e5ec47b22c03618b2cda34f6af20d1e23ddc1b79a4d954bf921c4691be
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Block Model Enclosure at Hardware Scale

**Course 3 · Module 1**
**Type:** Hands-on (Blender scene units + PCB placeholder + enclosure block)
**Suggested time:** ~90–120 minutes

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

- Set the Blender scene to **Metric + Millimeters** per the team's convention
- Create a **PCB placeholder** at the measured size, or the lab default
- Build an **enclosure block** that covers the PCB with the clearance from the lesson
- Apply Scale · name the objects · save the `.blend` + a screenshot
- Fill in [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md)

---

## Prerequisites

- [ ] Install [Blender](https://www.blender.org/download/) (LTS recommended)
- [ ] Read [Lesson §5](../l01-industrial-design-fundamentals/README.md) at least once
- [ ] A project folder, for example `course3-m01-block/`
- [ ] (Recommended) Vernier calipers + the real board you're using

---

## Size source — pick one track

### Track A — Measure your board (preferred)

1. Measure the PCB's width × length × thickness (mm)
2. Estimate the tallest component's height (connector / sensor)
3. If it is an Infineon PSOC Edge kit, open the [kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) / [design files index](https://documentation.infineon.com/psocedge/docs/hgn1762692110909) to help with the measurement
4. Note where the numbers came from in the checklist

### Track B — Placeholder (if no board yet)

Use this practice size, and swap in the real one later:

| Part | X (mm) | Y (mm) | Z (mm) |
|---|---|---|---|
| `PCB_placeholder` | 80 | 55 | 1.6 |
| Tallest component allowance (air above PCB) | — | — | 3.0 |
| Clearance (each side) | 0.5 | 0.5 | — |
| Wall (planned) | 2.0 | 2.0 | 2.0 |

Compute the `Enclosure_block` outer size using the formula in Lesson §4.2, and write the numbers into the checklist **before** building in Blender.

---

## Lab A — New scene and units (required)

1. `File → New → General`
2. Scene Properties → **Units**:
   - Unit System = **Metric**
   - Length = **Millimeters**
   - Unit Scale = **0.001**
3. Save the file: `m01_block_enclosure.blend`
4. Note the Blender version in the checklist (`Help → About` / the splash screen)

**Pass when:** changing a Cube's Dimensions shows units in mm on the UI

---

## Lab B — PCB placeholder (required)

1. Add Cube → name it `PCB_placeholder`
2. Set **Dimensions** per Track A or B
3. `Object → Set Origin → Origin to Geometry`
4. `Ctrl+A` → **Scale** (Scale must read 1,1,1)
5. Position it above the World Origin so it is visible
6. (Recommended) Overlay → turn on Measurements in Edit Mode and spot-check one edge against the table

**Pass when:** Dimensions match the table, and Scale = 1,1,1

---

## Lab C — Enclosure block + fit check (required)

1. Compute the outer size (write it in the checklist)
2. Add Cube → name it `Enclosure_block`
3. Set Dimensions · Origin to Geometry · Apply Scale
4. Position it so the PCB sits inside
5. Switch to Wireframe and check from the Top / Front / Right views
6. Confirm: the PCB does not poke through the wall · there is roughly the expected clearance gap

**Pass when:** an isometric screenshot shows both parts, and a teammate can read the Dimensions from the checklist

---

## Lab D — Naming, colors, save (required)

1. Set a temporary viewport color or material, a different one for each part (PCB / Enclosure)
2. `File → Save`
3. Export a screenshot (or a Render Viewport) named `m01_block_iso.png`
4. Fill in the checklist completely

---

## Lab E — Optional extras

- Add a `Battery_block` or `Display_block` per its datasheet
- Write down the 4 concept notes from Lesson §3.1
- Compare sizes with the models in [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) (for scale reference only — do not substitute it for your own work)

---

## Deliverables checklist

- [ ] `m01_block_enclosure.blend`
- [ ] An isometric screenshot
- [ ] [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) filled in completely
- [ ] (If you have a board) the size source = a real measurement and/or kit documentation

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| The grid disappears / objects are too small to see | Check Unit Scale = 0.001 · zoom in · adjust the Grid overlay |
| Typing 80 gives something gigantic or tiny | The team is using mismatched unit conventions — reset per Lab A |
| Bevel / resizing goes wrong later | You forgot Apply Scale — do `Ctrl+A` → Scale |
| Not sure of the Infineon board's size | Measure it for real first · use the design files from the kits page · don't guess from a web photo alone |
| The enclosure looks too big | Check that you added the wall on both sides, and not twice |

[Lesson](../l01-industrial-design-fundamentals/README.md) · [Checklist](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) · [TOC](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)
