---
id: pdesign.m06.l01
lang: en
title:
  th: ไฟล์ผลิต ต้นแบบ fitment และ Design Report
  en: Production Files, Prototype Fitment and the Design Report
summary:
  th: ตรวจ mesh และส่งออก STL ทางเลือกเมื่อยังพิมพ์ไม่ได้ ตรวจ fitment กับบอร์ดจริง ทดสอบร่วมเฟิร์มแวร์ และเขียน Design Report
  en: Check the mesh and export STL, options when you cannot print yet, check fitment against the real board, test with firmware and write the design report.
level: L2
time_min:
  concept: 35
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m05.l02
objectives:
- th: ตรวจ mesh ด้วย 3D Print Toolbox (manifold, normals, scale) แล้วส่งออก STL แยกฝาและฐาน
  en: Check the mesh with 3D Print Toolbox (manifold, normals, scale) and export separate STL files for lid and base.
- th: ตรวจ fitment กับบอร์ดจริงตามรายการ (PCB, พอร์ต, ช่องเซ็นเซอร์, ฝา, การยึด, สาย)
  en: Check fitment against the real board item by item (PCB, ports, sensor openings, lid, fasteners, cables).
- th: เขียน Design Report ที่ทำซ้ำได้ ครบหัวข้อบังคับ และมีข้อเสนอแนะรอบถัดไปอย่างน้อยสามข้อ
  en: Write a reproducible design report with every required section and at least three next-iteration recommendations.
develops:
- skill: hwdev.enclosure
  to: 2
- skill: hwdev.design-basics
  to: 2
- skill: soft.communication
  to: 2
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
source_sha256: 1397698ecaf44bcea349877b0ffa4aaa3d129145a8b12c931c9e055cd3a0e97f
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — Prototyping and Final Project

**Course 3 · Module 6**
**Suggested time:** about 3 hours + separate time for printing/assembling the prototype
**Format:** Capstone — prepare print files, build/check a prototype, test with firmware, then submit a Design Report to close the course

[Lab](../l02-lab/README.md) · [Design report](resources/design-report-template.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Prepare production files (**STL / STEP**) from Blender
2. Build / check a **prototype** and its **fitment** against a real circuit or board
3. Test alongside firmware and edge AI (including host / `web-app/` evidence)
4. Summarise the results in a **Design Report** with next-iteration recommendations

> **Key phrase**
> M06 = *closing the loop from concept to something you can hold* — complete files with no assembly/test evidence still do not count as finishing the course.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M05 — Digital Validation](../../m05-digital-validation/l01-scenario-digital-validation/README.md) | The Top 3 fixes · Ready/Not ready decision before printing |
| [M04 — GLB / Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) | The Twin-ready file that must be delivered alongside the STL |
| [M01 — Scale & block](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) | The mm units · the clearance you locked in |
| **[3D Print Toolbox (Blender Manual)](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)** | Checking non-manifold geometry / Make Manifold |
| **[STL export (Blender Manual latest)](https://docs.blender.org/manual/en/latest/files/import_export/stl.html)** | `File → Export → STL` (menu varies by version) |
| **[Protolabs — Enclosure for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | Walls · clearance · bosses |
| **[All About Circuits — enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | The order of steps before printing |
| **[3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)** | Fitment / assembly mindset |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Keeping the Twin alongside during testing |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX · Flasher · `web-app/ex05` · `ex06` |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware examples when testing inside the box |
| [Design report template](resources/design-report-template.md) | The main deliverable form |
| [M05 pre-prototype checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | Attach it to the report |

---

## 1. Capstone Deliverables (Course 3 Package)

| Deliverable | Required? | Notes |
|---|---|---|
| Project `.blend` | Yes | The final version after fixes from M05 |
| Twin-ready `.glb` | Yes | From M04/M05 |
| Print file **STL** (≥ 1 part) | Yes | Lid and/or base — separate files if printed separately |
| [Design report](resources/design-report-template.md) | Yes | Every main section filled in |
| [M05 pre-prototype checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | Yes | Attached, or summarised in the report |
| Fitment / demo photos or clip | Strongly recommended | The board inside the box · ports · sensors |
| STEP (or another CAD exchange format) | Optional | If you have a conversion tool for CNC |

```text
Concept (M01) → Detail + PBR (M02) → Motion (M03)
    → GLB / Twin (M04) → Validate (M05) → Print + Report (M06)
```

---

## 2. Production Files — STL (and Optional STEP)

### 2.1 When to use which format

| Format | Use when |
|---|---|
| **STL** | General 3D printing (FDM/SLA, depending on the round) — **the lab's main path** |
| **STEP** | Passing on to CAD / CNC — usually needs a conversion tool or a paired CAD model, not a single button in every version of Blender |

### 2.2 Mesh checks before export

A printer needs a **watertight / manifold** mesh — each edge connects to about 2 faces, with no unintended holes.

Use the **[3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)** add-on:

1. `Edit → Preferences → Add-ons` → search for **3D Print Toolbox** → enable it
2. In the 3D Viewport press `N` → the **3D-Print** tab
3. Select the part → **Check All**
4. Fix reported issues, especially **Non-manifold**
5. Use **Make Manifold** as a starting point, then check again by eye

Additional help:

- `Ctrl+A` → Scale before exporting
- Edit Mode → Merge by Distance if there are duplicate points
- `Shift+N` Recalculate Normals Outside

Walls should still be about **≥ 2 mm**, per printed-enclosure guidance ([Protolabs](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/))

### 2.3 Export STL — step by step

1. Separate the objects you will print (`Enclosure_base`, `Enclosure_lid`)
2. Select one part (or use batch export, depending on the version)
3. `File → Export → STL`
4. Turn on roughly: **Selection Only** · **Apply Modifiers** (if any modifiers remain)
5. Give it a clear name, for example `enclosure_base.stl`, `enclosure_lid.stl`
6. Import it into a slicer (e.g. Cura) and check the mm size again before printing

### 2.4 If you cannot print yet

You can still submit the STL + report by stating in the Design Report:

- The printer/service you plan to use
- The intended material (e.g. PLA)
- What you will check once you have the real part

Do not leave the fitment section blank — use a mock assembly with the board + a temporary paper/plastic box, or measure the openings from the model against the real board and photograph the evidence.

---

## 3. Prototype Build and Fitment

### 3.1 Fitment checklist (with real board)

| Check | Pass means |
|---|---|
| PCB inserts without forcing | No need to pry it in hard enough to risk breaking a pin |
| Ports align | A USB/cable can plug in, or it's clearly visible that it can |
| Sensor openings align | The opening lines up with the chip/vent as designed |
| Lid closes reasonably | Not so loose it falls off, and doesn't need to be forced shut |
| Fasteners / bosses (if any) | A screw or fastening plan fits per the design |
| Internal cables | There is routing space allowed for in M01 |

Assembly/clearance concepts: [3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [All About Circuits enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)

### 3.2 Photograph evidence

Take photos of at least:

1. The printed part, or the STL in the slicer (if not yet printed)
2. The board sitting in the base (or held up for a size comparison)
3. The lid assembled / the port openings
4. (Recommended) the device working inside the box

---

## 4. Test with Firmware and Edge AI

After placing the board in the box (or comparing it against it):

| Test | How | Evidence |
|---|---|---|
| Power / LED / button | Basic firmware still responds | A photo or short clip |
| Sensors still read | Temperature / IMU etc. are not so blocked by the box that the value dies | The Studio or web-app |
| Twin still useful | Open the GLB alongside the real thing | A screenshot |

### 4.1 Recommended host evidence

1. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) — Link + telemetry
2. Hackathon `web-app/` — **ex05** or **ex06** ([TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon))
3. If using a HEX from the lab pack — state the version in the report

Note whether sensors inside the box **still read correctly or are degraded** — this is an important lesson of a real enclosure.

---

## 5. Design Report

Copy and fill in [design-report-template.md](resources/design-report-template.md)

The required sections, in summary:

1. Project information
2. Design objectives
3. Concept → Final summary
4. Scale and materials
5. Twin integration
6. Digital validation and issues found (drawn from M05)
7. Prototype / fitment test results
8. Next-iteration recommendations, **at least 3**
9. File appendix

> A good report can be read and reproduced — not just pretty words with no scale numbers or file names.

---

## 6. Rubric (Minimum Pass)

| Criterion | Required |
|---|---|
| `.blend` + `.glb` + STL (≥1) | Yes |
| Design report complete | Yes |
| M05 checklist attached or summarized | Yes |
| Scale / units discussed honestly | Yes |
| Fitment or clear print plan + measurement evidence | Yes |
| Firmware / Twin / web-app considered in testing section | Yes |
| Next-iteration recommendations ≥ 3 | Yes |
| No secrets (Wi‑Fi / passwords) in submitted files | Yes |

Extension work (optional): a full print of lid+base · successful assembly with the board · sensor streaming inside the box via ex05/ex06 · a STEP file for further work

---

## 7. After Course 3

You have taken a product from **concept → model → Twin → checklist → prototype**, and connected it with firmware/edge AI data at lab level.

| Next direction | Where to go |
|---|---|
| Deeper firmware | [Course 1](../../../firmware-sdk-edge-ai/README.md) |
| Twin / telemetry / MQTT | [Course 2](../../../digital-twin/README.md) |
| Real production / injection moulding | DFM and manufacturers — the Twin in this course is a practice field |
| Reference models/assets | [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |

---

## Next Steps

1. Do the [lab](../l02-lab/README.md) — submit the package that closes the course
2. Fill in [design-report-template.md](resources/design-report-template.md)
3. Attach the checklist from [M05](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md)

---

## References and Further Reading

1. [3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)
2. [Blender import/export overview](https://docs.blender.org/manual/en/latest/files/import_export/index.html)
3. [Protolabs enclosure for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)
4. [All About Circuits — 3D-printed electronics enclosure](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)
5. [3DDFM electronic enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)
6. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
7. [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)
8. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
9. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)
10. [Course 3 TOC](../../README.md) · [Course 1](../../../firmware-sdk-edge-ai/README.md) · [Course 2](../../../digital-twin/README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Capstone lab: a prototype package and Design Report](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Design report](resources/design-report-template.md) · [← TOC](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
