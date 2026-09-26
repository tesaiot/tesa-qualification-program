# Product Industrial Design (Blender & Twin)

A hands-on course in designing smart-product enclosures with Blender: concept, block model, PBR materials, rendering and animation, then GLB export to a Digital Twin, digital validation and a physical prototype with a design report.

> Original content by Asst. Prof. Dr. Santi Nuratch, Department of Control Systems and Instrumentation Engineering, Faculty of Engineering, King Mongkut's University of Technology Thonburi (KMUTT) (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA). Imported from [drsanti/TESAIoT-Courses — C3](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C3) (commit `287c218`) under CC BY 4.0.

| | |
|---|---|
| Level | L2 · Guided |
| Status | alpha (imported, under review) |
| Estimated time | ~18 hours (sum of the source's module estimates) |
| Audience | public, student, developer, entrepreneur, educator |
| Language | Lessons are in Thai with English technical terms and English section headings; English lesson translations are pending. |

## Before you start

General computer skills; basic geometry helps. Course 2 (the Twin host and glTF) speeds up modules 4–6 but is not required for modules 1–3.

## What you need

- Blender 4.5 (every manual link is pinned to 4.5) with the bundled glTF 2.0 add-on and 3D Print Toolbox for module 6.
- Bitstream Studio (VS Marketplace 0.2.2 as of 2026-09-26) in VS Code as the Twin host from module 4.
- A 3D-printing slicer (the source names Cura) and a printer or print service; module 6 accepts a print plan with measurement evidence if you cannot print yet.
- Optional: the real board for fitment checks and web-app `ex05` / `ex06` from TESAIoT_Hackathon for in-enclosure sensor checks.
- Optional: a vernier caliper to measure the real board (Track A in the module 1 lab).

All tool versions are recorded in the `toolchain` field of [course.yaml](course.yaml).

## Learning outcomes

1. Design an enclosure to real hardware dimensions through Concept, Block and Final stages using clearance and wall-thickness rules.
2. Model detail, apply PBR materials, light the scene and render presentation images in Blender.
3. Create named open/close animation clips and check parts for interference while they move.
4. Export the model as GLB into the Twin (Bitstream Studio) with named sensor and interaction points.
5. Validate the design digitally with usage scenarios and list the top three fixes before prototyping.
6. Prepare STL files, check fitment against the real board and write a design report others can reproduce.

## Modules

| # | Module | Lesson | Lab |
|---|---|---|---|
| 1 | [Industrial Design Fundamentals](m01-design-fundamentals/README.md) | [Industrial Design Principles and a True-scale Enclosure](m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) | [Lab: Block Model Enclosure at Hardware Scale](m01-design-fundamentals/l02-lab/README.md) |
| 2 | [Modeling, Materials, and Render](m02-modeling-render/README.md) | [Enclosure Detail, PBR Materials and Presentation Renders](m02-modeling-render/l01-modeling-materials-render/README.md) | [Lab: Refine Model, PBR, and Render](m02-modeling-render/l02-lab/README.md) |
| 3 | [Motion and Interaction](m03-motion/README.md) | [Open/Close Animation and Interference Checks](m03-motion/l01-motion-and-interaction/README.md) | [Lab: Lid Animation and Short Sequences](m03-motion/l02-lab/README.md) |
| 4 | [Blender to Twin Integration](m04-blender-to-twin/README.md) | [Exporting GLB and Importing into the Twin Host](m04-blender-to-twin/l01-blender-to-twin/README.md) | [Lab: Export GLB and Import to Twin](m04-blender-to-twin/l02-lab/README.md) |
| 5 | [Scenario and Digital Validation](m05-digital-validation/README.md) | [Digital Validation before Prototyping](m05-digital-validation/l01-scenario-digital-validation/README.md) | [Lab: Scenarios and Pre-Prototype Checklist](m05-digital-validation/l02-lab/README.md) |
| 6 | [Prototyping and Final Project](m06-prototyping/README.md) | [Production Files, Prototype Fitment and the Design Report](m06-prototyping/l01-prototyping-final-project/README.md) | [Lab: Prototype Package and Design Report](m06-prototyping/l02-lab/README.md) |

## How to learn

Take the modules in order 1 → 6, lesson then lab. The checklists, look-dev sheet and design-report template in `resources/` are your deliverable forms. The main tool is Blender; modules 4–6 bring the model into the Twin with Bitstream Studio.

The source was written for instructor-led training; the wording has been adapted for self-study, but machine-specific values (Wi-Fi, broker, COM port, HEX version) are yours to set. Start from the defaults the lessons give (for example 921600 baud or the broker inside Bitstream Studio) and the tool documentation. The text keeps the source names **Course 1 / 2 / 3** (Course 1 = TESA Firmware SDK for Edge AI, Course 2 = Digital Twin, Course 3 = Product Industrial Design) and **M01–M08** for modules.

## Suggested order across the three courses

The source suggests Course 1 → Course 2 → Course 3: firmware on the board, then firmware ↔ Digital Twin ↔ cloud, then product design → Twin → physical prototype. If you only need Blender design work, modules 1–3 of Course 3 can come first; its Twin labs are much easier after Course 2.

- Course 1: [TESA Firmware SDK for Edge AI](../firmware-sdk-edge-ai/README.en.md)
- Course 2: [Firmware Development with the VS Code-based TESA Digital Twin](../digital-twin/README.en.md)
- Course 3: [Product Industrial Design (Blender & Twin)](../product-design/README.en.md)

## Source and licence

Imported from [drsanti/TESAIoT-Courses](https://github.com/drsanti/TESAIoT-Courses) folder `C3/` at commit [`287c218`](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C3). TESA funded the original work and holds the rights; it is published here under [CC BY-NC 4.0](../../LICENSES/CC-BY-NC-4.0.txt). TESA Open Knowledge kept the author's teaching text; it added the module/lesson structure, front matter, quizzes, firmware and tool notes, fixed links for the new layout, and reworded classroom-delivery phrases (training round, grading) for open learning. Third-party tools and documents keep their own licences.

## How to cite TESA

If you reuse this course in slides, teaching material, a course specification, handouts or a code repository, credit it with:

> "Product Industrial Design (Blender & Twin)" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0

If you change the material, add "(adapted)" and keep the original author credit:

> Original content by Asst. Prof. Dr. Santi Nuratch, Department of Control Systems and Instrumentation Engineering, Faculty of Engineering, King Mongkut's University of Technology Thonburi (KMUTT) (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA)
>
> The Bitstream Studio (VS Code) and Ternion tools used in this course are by Asst. Prof. Dr. Santi Nuratch (KMUTT).

Citing TESA does not mean that TESA or Infineon endorses your course or work. More formats and examples (slides, course specifications, handouts, code repositories) are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
