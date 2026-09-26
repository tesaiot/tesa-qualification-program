---
id: pdesign.m01.l01
lang: en
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
translation: done
slides: slides.md
source_sha256: 3b3e5faf138597b81735de2d2a9c879f49bb21b0f98de0a7006a0689076992ac
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — Industrial Design Fundamentals

**Course 3 · Module 1**
**Suggested time:** about 2 hours — learn the concepts, set up the Blender scene (units in millimetres), then build a rough enclosure at true scale
**Format:** a hands-on lesson — read it and follow along directly in Blender; for materials and PBR surfacing, go to [M02](../../m02-modeling-render/l01-modeling-materials-render/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/scale-and-block-checklist.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the principles of **industrial-grade design** that support real manufacturing
2. Work through the **Concept → Block Model → Final Model** sequence
3. Explain the **Casing / Enclosure / PCB Housing** workflow for smart devices
4. Handle basic **Topology, Mesh optimization and Scale accuracy** in Blender

> **Key phrase**
> In M01, **lock the dimensions to the hardware first**, then make it beautiful — if the rough block is wrong from the start, the fixes in M02–M06 all become expensive.

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[Blender Download](https://www.blender.org/download/)** | Installing the course's main tool |
| **[Blender 4.5 LTS Manual — Scene Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units)** | Setting Metric / mm / Unit Scale |
| **[Apply Scale / Transforms](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | Press `Ctrl+A` before measuring, beveling, or exporting |
| **[Mesh Structure](https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html)** | What vertex / edge / face · tris · quads · n-gons mean |
| **[Mesh Modeling intro](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)** | Telling Object Mode apart from Edit Mode |
| **[Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)** | Setting the pivot point / the point that sits on the table |
| **[Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | Official training videos (English) |
| **[INC111-2021 Blender (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Thai-language tutorial |
| **[IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/advocacy/what-industrial-design/)** | The professional definition of industrial design |
| **[All About Circuits — 3D-printed electronics enclosure](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | The PCB → shell → port-cutting workflow · clearances |
| **[Protolabs Network — Enclosure design for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | Walls around 2 mm · clearance around 0.5 mm |
| **[KIT_PSE84_EVAL kit guide (Infineon)](https://documentation.infineon.com/psocedge/docs/lne1762692969598)** | Finding documentation and design files for the board used |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Board references and firmware examples |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | Sample scale models for reference (not a substitute for the enclosure you design yourself) |
| [Course 2 M03 Blender intro](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | 3D Twin basics, if you have taken Course 2 |
| [Checklist](resources/scale-and-block-checklist.md) | The form to fill in while doing the lab |

---

## 1. Why Industrial Design Matters for Edge AI Devices

[Industrial Design](https://www.idsa.org/about-idsa/advocacy/what-industrial-design/) (per IDSA) is designing products that people genuinely use every day — not just "a pretty picture on screen", but something that must be **usable, manufacturable, and able to fit together with the engineering inside it**.

For **Edge AI / IoT** devices, the enclosure must handle at least:

| Topic | Why it matters |
|---|---|
| PCB size + component height (connectors, sensors) | It won't fit, or buttons can't be pressed |
| Sensor openings / USB ports | Blocked → distorted readings, or a cable can't be plugged in |
| Handling / placing on a desk | Ergonomics and the origin point in the Twin |
| Prototype manufacturing (FDM/SLA) → later injection moulding | Wall thickness / fillets / bosses each have their own constraints |
| Digital Twin | Wrong scale and axes → animation / telemetry look fake |

This course uses **[Blender](https://www.blender.org/)** because it is free, open source, and can export **glTF/GLB** to [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) in M04.

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

An "industrial-grade" product in this course means: **you can answer four dimensions before getting into surface detail**.

| Lens | Questions to answer | Edge device example |
|---|---|---|
| **Function** | What is it used for, and in what environment? | Environmental monitoring · wearable · mounted on machinery |
| **Form & Proportion** | Is the proportion comfortable to hold? Is it balanced? | Too tall and easily tipped over · sharp edges |
| **Material & Manufacturing** | Can it really be 3D printed / injection moulded / CNC machined? | Walls too thin · cavities hard to print |
| **User Experience** | Can you open the lid, see the LED, plug in a cable without a long manual? | The USB port facing the wrong way |

Read more on the professional definition: [IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/advocacy/what-industrial-design/)

For a device with a PCB inside, keep a fifth lens in mind throughout the course:

> **Electronics fit** — every millimetre of the enclosure must refer to a real part, or a placeholder that has actually been measured.

The enclosure workflow used in prototyping industry practice (summarised from [All About Circuits](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/) and [Protolabs Network](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)):

1. Model the **internal parts first** (PCB, battery, connectors)
2. Build the **outer shell**, then leave wall thickness + clearance
3. Cut openings for ports / LEDs / sensors
4. Split into a top lid and a base · prepare mounting points (bosses) in a later module
5. Check for interference before printing

---

## 3. Concept → Block → Final (Do Not Skip Stages)

| Stage | Deliverable | Do not do yet |
|---|---|---|
| **Concept** | Rough proportions, the shape's direction, who holds/places it and how | Shiny materials · small fillets · fine screws |
| **Block Model** | A block standing in for the PCB + battery + modules · an outer enclosure at true mm scale | Boolean port cutouts · UVs |
| **Final Model** | Production-ready detail (continues in M02+) | — |

### 3.1 Concept (15–20 minutes on paper is enough)

Before opening Blender, answer briefly in the checklist:

1. How does the user hold the device (in hand / on a desk / mounted on a wall)?
2. Which ports must be visible from the outside?
3. Which sensors need an air vent / a line of sight?
4. Which way does the lid open (top / side)?

### 3.2 Block Model (the heart of M01)

Block = **a rough shape at the correct size**

- PCB = a thin box sized width × length × thickness
- Enclosure = the outer box that covers the internal parts
- Leave internal spacing per the clearance guidance (see §4)

### 3.3 Final Model (not finished in M01)

Fillet detail, surfacing, neatly cut openings = **M02**
Lid-opening animation = **M03**

> **Key phrase**
> Surface detail done too early on the wrong scale = beautiful work that a real board cannot fit into

---

## 4. Enclosure and PCB Housing Workflow

### 4.1 Collect real sizes first

Recommended order:

1. **Measure the real board with vernier calipers** (width × length × thickness + the tallest component's height)
2. Or open the documentation for the evaluation kit used — such as the [KIT_PSE84_EVAL guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) and the **Hardware design files** from the [PSOC Edge kits page](https://documentation.infineon.com/psocedge/docs/hgn1762692110909)
3. Note where each number came from in the [checklist](resources/scale-and-block-checklist.md)

If you do not have a board in hand yet, use the **Lab placeholder** in the [lab](../l02-lab/README.md) (a clearly stated practice size) and swap in the real size later.

### 4.2 Lab clearance rules of thumb

Starting numbers, from 3D-printing enclosure guidance ([Protolabs Network](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/), [All About Circuits](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)):

| Parameter | Lab default | Notes |
|---|---|---|
| PCB ↔ inner wall clearance | **≥ 0.5 mm** per side | FDM often needs more margin (up to ~1 mm) |
| Wall thickness | **≈ 2.0 mm** | The recommended minimum for a general enclosure |
| Headroom above the tallest component | **≥ 2–3 mm** | Wiring / USB connector head / print tolerance |
| Port openings | Allow margin around the plug | Do not cut an opening exactly the size of the connector |

In **M01** you do not yet need to Solidify real walls — but you must draw the **outer box** at least this much bigger than the PCB:

```text
outer_X ≈ PCB_X + 2×clearance + 2×wall
outer_Y ≈ PCB_Y + 2×clearance + 2×wall
outer_Z ≈ PCB_Z_stack + top_air + bottom_air + wall(s)
```

A worked example (when PCB = 80 × 55 × 1.6 mm, clearance 0.5, wall 2, top air 3, bottom 1):

```text
inner needs ≈ 81 × 56 × (1.6+3+1) 
outer ≈ 81+4 × 56+4 × …  → roughly 85 × 60 × the computed height
```

Write down your formula and your own real numbers in the checklist — do not rely on the example numbers alone.

### 4.3 Interference check (manual, no physics required)

In the Blender Viewport:

1. Look from Orthographic top/side views ([Viewports](https://docs.blender.org/manual/en/4.5/editors/3dview/navigate/views.html))
2. Switch to Wireframe (`Z` → Wireframe) to see the PCB inside
3. Confirm the PCB does **not** unintentionally poke through the outer wall
4. If objects overlap incorrectly — enlarge the outer box, or shrink the object standing in for the PCB

---

## 5. Hands-on in Blender — Scene Units and Scale Accuracy

Follow along step by step (use together with the [lab](../l02-lab/README.md))

### 5.1 Install and open a clean file

1. Install from [blender.org/download](https://www.blender.org/download/) (the **LTS** line is recommended, to match the 4.5 manual where possible)
2. `File → New → General`
3. Delete the default Cube if you want an empty scene: select → `X` → Delete

Review the UI: [Interface](https://docs.blender.org/manual/en/4.5/interface/index.html) · video [Fundamentals](https://studio.blender.org/training/blender-fundamentals-45-lts/) · Thai [INC111-2021](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

### 5.2 Set metric millimeters (lab recipe)

In the [Scene Properties → Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units) panel:

1. Click the **Scene Properties** icon (the cone/scene icon on the right)
2. Under **Units**:
   - **Unit System** = `Metric`
   - **Length** = `Millimeters`
   - **Unit Scale** = `0.001`

> **Why set it to 0.001?**
> The Blender manual explains that Unit Scale converts between Blender's internal units and the numbers shown on the UI ([Scene Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units)).
> In product modelling / 3D printing work, this setting is commonly used so that typing `80` gives a millimetre-scale length on the UI that matches engineering thinking (the same approach as community guides such as [Blender for 3D Printing — Units](https://daler.github.io/blender-for-3d-printing/interface/transforms.html))

**Team rule:** everyone on the team must use the same unit convention, and record it in the checklist — so that exporting the Twin in M04 does not end up with different files at the wrong scale.

Checking the grid (if the lines disappear because the scale is small):

- Overlay → Grid · adjust the grid's Scale so it is visible over the ~10–100 mm working range

Turn on edge measurements in Edit Mode from Overlay → **Measurements** ([Mesh edit overlays](https://docs.blender.org/manual/en/4.5/modeling/meshes/mesh_analysis.html) / the overlay panel) to read edge lengths.

### 5.3 Create a PCB placeholder (exact dimensions)

1. `Add → Mesh → Cube`
2. Object Mode → the **Item** panel (`N`) → **Dimensions**
3. Enter values, for example `X=80 mm`, `Y=55 mm`, `Z=1.6 mm` (or your actually measured values)
4. Name the object: `PCB_placeholder`
5. **Object → Set Origin → Origin to Geometry** ([Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html))
6. Move it slightly above the floor (for example, set Location Z to the base thickness you plan to design)
7. **Object → Apply → Scale** (`Ctrl+A` → Scale) — read the reasoning in [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

After Apply Scale, the Scale value in the Item panel should read `1, 1, 1`, while Dimensions still shows the real size.

### 5.4 Create the enclosure block

1. `Add → Mesh → Cube`, named `Enclosure_block`
2. Set Dimensions per the formula in §4.2
3. Origin to Geometry · Apply Scale
4. Position it so the PCB sits centred in the internal space (check with Wireframe)
5. (Optional) Give it a temporarily different-coloured **Material**, just to tell the parts apart — no real PBR needed yet

You do not need to cut port openings in M01 yet — just a block that "covers it."

### 5.5 Optional: a stand-in part for a battery or a display

If the project has a **battery** or a **display**:

- Add another Cube sized roughly from the datasheet
- Place it in the enclosure and check it does not collide with the PCB

---

## 6. Topology and Mesh Optimization (What You Need in M01)

From [Mesh Structure](https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html):

| Element | Short meaning |
|---|---|
| **Vertex** | A point in space |
| **Edge** | A line connecting two points |
| **Face** | A surface (tri / quad / n-gon) |

For a **block enclosure** in M01:

| Do | Avoid |
|---|---|
| Use a Cube and adjust Dimensions | Unnecessary overlapping Subdivision |
| Keep parts as separate objects (`PCB_…`, `Enclosure_…`) | Merging everything into one blob from the start |
| Apply Scale after resizing | Leaving Scale at 2.0, 0.5, … |
| Flat shading on the box is enough | Smoothing everything until you can't see the assembly's edges |

**Optimization at the M01 level** = don't add polygons until the scale and clearance are locked down.
Reducing poly count for the Twin will be revisited again before exporting in M04.

**Non-manifold geometry / holes** matter when doing STL in M06 — for now, if you're using a solid Cube as a block, you don't need to worry about the manifold-ness of a hollow shell yet.

---

## 7. Origin and Axis Habits (Prepare for Twin)

Habits worth building from M01, to make the work in M03–M04 easier:

| Habit | Why |
|---|---|
| Place the Origin at the centre of the box's base, or at an assembly corner | Easy to place on a table in the Twin |
| Keep the axes perpendicular to the scene's floor | The lid rotation in M03 won't tilt the wrong way |
| Give objects short, clear English names | Easy to reference in a clip list / the Twin |
| The whole team uses the same units | Prevents files at different scales (e.g. off by 1000x) when work is combined |

Setting the origin: [Object Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)

---

## 8. How M01 Feeds the Rest of Course 3

| Carry forward from M01 | Use in |
|---|---|
| A correctly scaled block + checklist | M02 detailed shaping / PBR |
| Parts already separated into lid–base in your mind | M03 open–close animation |
| Origin / the team's units | M04 GLB → Bitstream Studio |
| The clearance you recorded | M05 validation · M06 printing and fitment |

---

## Next Steps

1. Do the lab step by step: [Lab](../l02-lab/README.md)
2. Fill in [scale-and-block-checklist.md](resources/scale-and-block-checklist.md)
3. When ready, continue to [M02 — Modeling, Materials, and Render](../../m02-modeling-render/l01-modeling-materials-render/README.md)

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

8. [IDSA — What is Industrial Design?](https://www.idsa.org/about-idsa/advocacy/what-industrial-design/)
9. [Six Steps for Designing a Custom 3D Printed Electronics Enclosure (All About Circuits)](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)
10. [How do you design enclosures for 3D printing? (Protolabs Network)](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)
11. [Blender for 3D Printing — Units](https://daler.github.io/blender-for-3d-printing/interface/transforms.html) (an approach to Unit Scale for mm-based work)

### Hardware / course portals

12. [KIT_PSE84_EVAL documentation](https://documentation.infineon.com/psocedge/docs/lne1762692969598) · [PSOC Edge kits + design files](https://documentation.infineon.com/psocedge/docs/hgn1762692110909)
13. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
14. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
15. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)
16. [Course 3 TOC](../../README.md) · [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: a block enclosure to hardware scale](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Checklist](resources/scale-and-block-checklist.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-modeling-render/l01-modeling-materials-render/README.md)
