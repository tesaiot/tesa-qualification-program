---
id: pdesign.m02.l01
lang: en
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
translation: done
source_sha256: 5cf7709962949ac64807d1d0db7b086a2e081ed65cdf297e3712b717b36fc199
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — Modeling, Materials, and Render

**Course 3 · Module 2**
**Suggested time:** about 4 hours — develop the rough block from M01 into detailed shape, add PBR materials, set up lighting, and render a presentation image
**Format:** a hands-on lesson — read it and follow along directly in Blender; the lid-opening animation goes to [M03](../../m03-motion/l01-motion-and-interaction/README.md)

[Lab](../l02-lab/README.md) · [Look-dev sheet](resources/material-lighting-sheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Develop a more complex shape from the block model (hard-surface / port openings / wall thickness)
2. Define materials, surfaces, and surface detail in a **PBR** approach
3. Light the scene and render a high-quality presentation image
4. Produce a **product visualization** suited to industry and teaching material

> **Key phrase**
> In M02, **add detail without breaking the size locked in M01** — a beautifully cut port opening that the board no longer fits into = not a pass yet

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M01 — Industrial Design Fundamentals](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) | The block model + the mm units you must keep |
| **[Boolean Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html)** | Cutting port / sensor openings |
| **[Solidify Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html)** | Setting wall thickness |
| **[Bevel (edit) / Bevel Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html)** | Rounded edges the user touches |
| **[Mirror Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html)** | Symmetric parts |
| **[Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | `Ctrl+A` before Boolean / Bevel |
| **[Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html)** | The main PBR material |
| **[Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html)** | Creating and assigning a material |
| **[EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html)** | Fast rendering to check results |
| **[Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html)** | Higher-quality rendering (if your machine can handle it) |
| **[Light objects](https://docs.blender.org/manual/en/4.5/render/lights/light_object.html)** | Area / Point / Sun |
| **[World & Environment](https://docs.blender.org/manual/en/4.5/render/lights/world.html)** | HDRI / a studio backdrop |
| **[Cameras](https://docs.blender.org/manual/en/4.5/render/cameras.html)** | Presentation camera angles |
| **[glTF materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)** | Preparing materials so they can be sent to the Twin in M04 |
| **[Blender Fundamentals — Modeling](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)** | Official video |
| **[INC111-2021 (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Thai-language tutorial |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | Sample materials/models for reference (reference only) |
| [Look-dev sheet](resources/material-lighting-sheet.md) | Recording material values, lighting, and render files |

---

## 1. From Block to Product Detail (Keep Scale)

In [M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) you have at least:

- `PCB_placeholder` at the true size
- `Enclosure_block` that covers it

In M02, you will:

1. Give the box **wall thickness** (not just a solid block)
2. **Cut openings** for ports / LEDs / sensors, at least 2 of them
3. **Round the edges** the user handles
4. **Split the top lid–base** into separate objects (preparing for M03 / printing in M06)
5. Add materials + lighting + render a presentation image

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

Do not change the PCB's Dimensions without noting why — if the box must grow, adjust it per the clearance formula from M01, and update the checklist.

---

## 2. Modeling Techniques You Will Use

### 2.1 Always Apply Scale first

Before Boolean / Bevel / Solidify:

1. Object Mode → select the object
2. `Ctrl+A` → **Scale**

If you forget and Scale is not `1,1,1`, bevels and cut holes tend to come out wrong — read [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

### 2.2 Solidify — wall thickness

The [Solidify Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) adds thickness to a mesh surface.

Approach used in the lab (continuing from M01):

| Step | What to do |
|---|---|
| 1 | Start from a solid box, or remove the inner faces later, depending on the workflow you choose |
| 2 | Add Solidify · Thickness ≈ **2.0 mm** (the default from the 3D-printing guidance in M01) |
| 3 | Turn on Even Thickness if the option exists and the result looks consistent |
| 4 | Check that the PCB is still inside and does not collide with the wall |

> For beginners: either a **solid box + Boolean to hollow out the inside**, or **Solidify from a shell**, both work — what matters is a wall thickness of around 2 mm, and that the PCB still fits.

### 2.3 Boolean — cutting port and sensor openings

The [Boolean Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html):

| Operation | Use in this lab |
|---|---|
| **Difference** | Cutting a hole out of the box (a USB port, a sensor opening, an LED window) |
| Union / Intersect | Used less in M02 — save these for when parts are combined |

Short steps:

1. Create a Cube/Cylinder as a `Cutter_USB` sized to the opening (allowing clearance around the connector)
2. Position the cutter so it overlaps the wall at the port's location
3. On the enclosure: Add Modifier → **Boolean** → Operation **Difference** → Object = the cutter
4. If the result looks odd, try the **Exact** solver
5. Once satisfied, apply the modifier · hide or delete the cutter

Do at least **2 openings** (for example USB + a sensor opening, or an LED)

### 2.4 Bevel — rounded edges

Edges that are too sharp are uncomfortable to hold and hard to print — use [Bevel](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html):

- Edit Mode: select an edge → `Ctrl+B`, drag the mouse
- Or a Bevel Modifier on the whole part (be careful not to round it so much the port openings deform)

Starting radius in the lab: about **0.5–1.5 mm** on the outer edges the hand touches

### 2.5 Mirror — symmetric parts (if any)

The [Mirror Modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html) is useful when a lid or button is left–right symmetric — it reduces duplicate work.

### 2.6 Split lid and base

From M02 onward, split at least:

| Object name | Role |
|---|---|
| `Enclosure_base` | The base / lower part |
| `Enclosure_lid` | The top lid |

An easy way: in Edit Mode, select the top faces → `P` → Selection to make it a new object · or cut with a plane + Boolean and then separate the parts.

Why: M03 rotates the lid · M06 prints the parts separately.

---

## 3. Materials with Principled BSDF (PBR)

**PBR** = Physically Based Rendering — a material responds to light in a near-realistic way as the lighting angle changes.

In Blender, the main node used is [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) (which works well with [glTF](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials) in M04)

### 3.1 Create a material

1. Select the object → the **Material Properties** tab
2. New → name it, for example `Plastic_matte_body`
3. Open the Shader Editor if you want to see the nodes ([Materials intro](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html))

### 3.2 Parameters you must understand

| Parameter | Meaning | Lab tip |
|---|---|---|
| **Base Color** | The base colour | Enclosure plastic: light grey / muted white |
| **Roughness** | Matte ↔ glossy (0 = very glossy, 1 = matte) | Matte plastic ≈ 0.45–0.7 |
| **Metallic** | 0 = not metal, 1 = metal | Plastic = **0** · a metal button/port = **1** |
| **Specular / IOR** (depending on version) | The reflectiveness of an insulator | Use the default first, then adjust |
| **Emission** (optional) | Light emitted from the surface | Simulating an LED — keep the intensity low |

### 3.3 Two materials minimum (lab presets)

Copy these starting values and adjust them — record the real values in the [look-dev sheet](resources/material-lighting-sheet.md)

**A — Matte plastic (the body)**

| Parameter | Starting value |
|---|---|
| Base Color | RGB ≈ 0.75, 0.75, 0.78 |
| Roughness | 0.55 |
| Metallic | 0.0 |

**B — Contrast accent (rubber feet / metal port / buttons)**

| Parameter | Rubber feet | Brushed metal accent |
|---|---|---|
| Base Color | 0.05, 0.05, 0.05 | 0.7, 0.7, 0.72 |
| Roughness | 0.7 | 0.35 |
| Metallic | 0.0 | 1.0 |

Assign the material to a separate part, or use several material slots on the same mesh (Edit Mode → Assign)

---

## 4. Lighting and Camera for Product Shots

### 4.1 Render engine

| Engine | Use when | Manual |
|---|---|---|
| **EEVEE** | Checking results quickly · most of the lab | [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) |
| **Cycles** | The final presentation image, if your machine can handle it | [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html) |

Set at Render Properties → Render Engine

### 4.2 Simple three-point light (the recommended starting point)

Referencing the studio-lighting concept + [Light objects](https://docs.blender.org/manual/en/4.5/render/lights/light_object.html):

| Light | Role | Starting idea |
|---|---|---|
| Key | The main light | An Area Light from the front-side · Power just enough to see the edges |
| Fill | Reduces dark shadows | A weaker Area light on the opposite side |
| Rim / back | Separates the object from the background | A thin light from behind |

Or use a **World HDRI** ([World](https://docs.blender.org/manual/en/4.5/render/lights/world.html)) as ambient light, adding one Area light to bring out the piece's edges.

Background: a light grey colour or a plain plane — don't let a pattern get in the way of reading the shape.

### 4.3 Camera

[Cameras](https://docs.blender.org/manual/en/4.5/render/cameras.html):

1. `Add → Camera`
2. Recommended angle: **three-quarter**, or something isometric-ish that shows both the lid and a side port
3. `Ctrl+Alt+Numpad0` aligns the camera to the current view (if your system supports it)
4. Turn on Lock Camera to View temporarily while framing the shot, then turn it off before rendering

Capture at least:

- 1 **beauty** shot (communicates the shape/material)
- (Recommended) 1 **technical** shot that clearly shows the port openings or the PCB's position

---

## 5. Render Output

1. Output Properties → Resolution, for example **1920 × 1080**
2. File Format = **PNG**
3. Set the Output path inside the project folder
4. `F12` or Render → Render Image
5. Image → Save As…

Record the engine, samples/quality, and file name in [material-lighting-sheet.md](resources/material-lighting-sheet.md)

---

## 6. Quality Gate Before M03

| Check | Pass means |
|---|---|
| Scale from M01 still valid | The PCB still fits, checked in Wireframe |
| Openings ≥ 2 | Ports/sensors/LEDs are clear |
| Lid and base are separate objects | Ready to animate in M03 |
| Materials ≥ 2 | Principled BSDF · values recorded in the sheet |
| At least one render | A PNG in the deliverables folder |
| Apply Scale done | No leftover odd Scale before the modifiers |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Fill in [material-lighting-sheet.md](resources/material-lighting-sheet.md)
3. When ready, continue to [M03 — Motion and Interaction](../../m03-motion/l01-motion-and-interaction/README.md)

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

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: refine the model, add PBR materials, and render](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Look-dev sheet](resources/material-lighting-sheet.md) · [← TOC](../../README.md) · [← M01](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) · [M03 →](../../m03-motion/l01-motion-and-interaction/README.md)
