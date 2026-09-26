---
id: pdesign.m06.l02
lang: en
title:
  th: 'แล็บ Capstone: แพ็กเกจต้นแบบและ Design Report'
  en: 'Lab: Prototype Package and Design Report'
summary:
  th: แก้ตามผลโมดูล 5 ตรวจ mesh ส่งออก STL พิมพ์หรือทำแผนพิมพ์ ตรวจ fitment ทดสอบร่วมเฟิร์มแวร์/Twin และส่ง Design Report
  en: Apply module 5 fixes, check the mesh, export STL, print or plan the print, check fitment, test with firmware/Twin and hand in the design report.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
  - devkit
prerequisites:
- pdesign.m06.l01
objectives:
- th: ส่งออก STL ที่ผ่านการตรวจ mesh และพิมพ์ หรือทำแผนพิมพ์พร้อมหลักฐานการวัด
  en: Export mesh-checked STL files and print them, or produce a print plan with measurement evidence.
- th: บันทึกผล fitment และผลทดสอบร่วมเฟิร์มแวร์ / Twin / web-app ใน Design Report
  en: Record fitment results and the firmware / Twin / web-app test in the design report.
- th: จัดแพ็กเกจ .blend, .glb, STL, M05 checklist และ Design Report ให้ครบ
  en: 'Assemble the full package: .blend, .glb, STL, the M05 checklist and the design report.'
develops:
- skill: hwdev.enclosure
  to: 2
- skill: hwdev.design-basics
  to: 2
- skill: soft.communication
  to: 2
assesses:
- skill: hwdev.enclosure
  level: 2
  evidence: README.md#deliverables-checklist
- skill: soft.communication
  level: 2
  evidence: README.md#deliverables-checklist
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
slides: slides.md
source_sha256: 7f9cdad65ded5729d9370011c2cc80477654ca9568a991d3b83018172093e627
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — Prototype Package and Design Report

**Course 3 · Module 6**
**Type:** Capstone / handoff package
**Suggested time:** ~3 hours (+ separate time for printing/assembling)

Read first: [Lesson](../l01-prototyping-final-project/README.md) · [Design report](../l01-prototyping-final-project/resources/design-report-template.md) · [← TOC](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html) | manifold check |
| [M05 checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | Top 3 fixes before print |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | optional sensor proof in enclosure |

---

## Lab Goals

Submit the package that closes Course 3, complete with files, the report, and fitment/test evidence.

---

## Prerequisites

- [ ] M05 gave a Ready decision, or you have a fix plan already carried out
- [ ] You have the latest `.blend` + `.glb`
- [ ] A deliverables folder, for example `course3-final/`

---

## Lab A — Apply M05 fixes (required)

1. Open the Top 3 from M05
2. Fix them in Blender in priority order (at least what time allows)
3. Save the final `.blend`
4. Export a new `.glb` if the Twin model changed

**Pass when:** the report states which items were fixed and which are still outstanding

---

## Lab B — Mesh check and export STL (required)

1. Open **3D Print Toolbox**
2. Check All on the parts to be printed
3. Fix non-manifold geometry until it passes well enough for the lab
4. Export at least 1 STL (`enclosure_base.stl` and/or `enclosure_lid.stl`)
5. Open it in a slicer and check the units are mm

**Pass when:** there is an STL file and either a slicer screenshot, or a passing Check All list

---

## Lab C — Print or print plan (required)

| Track | What to do |
|---|---|
| **C1 — Printer available** | Print at least one part · photograph the printed piece |
| **C2 — No printer** | State the service/machine · the material · the expected time · and measurement evidence comparing the board with the model |

**Pass when:** there is a printed photo **or** a verifiable print plan + measurement evidence

---

## Lab D — Fitment with hardware (required)

1. Place/compare the PCB against the base
2. Check the ports, sensor openings, the lid
3. Take photos from at least 2 angles
4. Log each Pass/Fail result in Design Report §7

**Pass when:** there is a genuinely filled-in fitment table, with no whole section left blank

---

## Lab E — Firmware / Twin / web-app check (required)

Choose at least one piece of evidence:

- The LED/button working inside the box, or while held up against it
- Telemetry in Bitstream Studio
- Hackathon **ex05** or **ex06** after assembly

**Pass when:** the report states the result as "the sensor still reads correctly / reads but is degraded / could not be tested yet because…"

---

## Lab F — Design report package (required)

1. Fill in [design-report-template.md](../l01-prototyping-final-project/resources/design-report-template.md) completely
2. Attach the file list in §9
3. At least 3 next-iteration recommendations
4. Attach or summarise the M05 checklist
5. Confirm there is no password in the submitted files

---

## Deliverables checklist

| Item | Done? |
|---|---|
| `.blend` | |
| `.glb` | |
| STL (≥1) | |
| Design report | |
| M05 checklist | |
| Fitment photos / measurement evidence | |
| Firmware/Twin/web-app note | |

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| The slicer says the mesh is broken | 3D Print Toolbox · Make Manifold · check the normals |
| The STL is the wrong size | Apply Scale · check the mm units · check the scale in the slicer |
| The PCB won't fit | Go back to the Top 3 from M05 · don't file it down without noting that in the report |
| Sensors go quiet inside the box | The opening is blocked · the material is too thick · or a cable came loose — check one layer at a time |
| No printer available | Fully complete Track C2 — don't leave it blank |

[Lesson](../l01-prototyping-final-project/README.md) · [Design report](../l01-prototyping-final-project/resources/design-report-template.md) · [TOC](../../README.md)
