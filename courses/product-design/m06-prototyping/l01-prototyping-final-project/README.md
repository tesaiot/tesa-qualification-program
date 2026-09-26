---
id: pdesign.m06.l01
lang: th
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
slides: slides.md
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — Prototyping and Final Project

**Course 3 · Module 6**  
**Suggested time:** ประมาณ 3 ชั่วโมง + เวลาพิมพ์/ประกอบต้นแบบแยกต่างหาก  
**Format:** Capstone — เตรียมไฟล์พิมพ์ สร้าง/ตรวจต้นแบบ ทดสอบกับเฟิร์มแวร์ แล้วส่ง Design Report ปิดหลักสูตร

[Lab](../l02-lab/README.md) · [Design report](resources/design-report-template.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. เตรียมไฟล์ผลิต (**STL / STEP**) จาก Blender  
2. สร้าง / ตรวจ **Prototype** และ **fitment** กับวงจรหรือบอร์ดจริง  
3. ทดสอบร่วมเฟิร์มแวร์และ Edge AI (รวมหลักฐานโฮสต์ / `web-app/`)  
4. สรุปผลด้วย **Design Report** และข้อเสนอแนะรอบถัดไป  

> **Key phrase**  
> M06 = *ปิดวงจากแนวคิดถึงของจับต้องได้* — ไฟล์ครบโดยไม่มีหลักฐานประกอบ/ทดสอบ ยังไม่นับว่าจบคอร์ส

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M05 — Digital Validation](../../m05-digital-validation/l01-scenario-digital-validation/README.md) | Top 3 fixes · Ready/Not ready ก่อนพิมพ์ |
| [M04 — GLB / Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) | ไฟล์ Twin-ready ที่ต้องส่งควบคู่ STL |
| [M01 — Scale & block](../../m01-design-fundamentals/l01-industrial-design-fundamentals/README.md) | หน่วย mm · clearance ที่ล็อกไว้ |
| **[3D Print Toolbox (Blender Manual)](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)** | ตรวจ non-manifold / Make Manifold |
| **[STL export (Blender Manual latest)](https://docs.blender.org/manual/en/latest/files/import_export/stl.html)** | `File → Export → STL` (ตามเวอร์ชัน) |
| **[Protolabs — Enclosure for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | ผนัง · clearance · bosses |
| **[All About Circuits — enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | ลำดับก่อนพิมพ์ |
| **[3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)** | fitment / assembly mindset |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Twin ควบคู่ตอนทดสอบ |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX · Flasher · `web-app/ex05` · `ex06` |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ตอนทดสอบในกล่อง |
| [Design report template](resources/design-report-template.md) | แบบฟอร์มผลงานหลัก |
| [M05 pre-prototype checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | แนบกับรายงาน |

---

## 1. Capstone Deliverables (Course 3 Package)

| Deliverable | Required? | Notes |
|---|---|---|
| Project `.blend` | Yes | เวอร์ชันสุดท้ายหลังแก้จาก M05 |
| Twin-ready `.glb` | Yes | จาก M04/M05 |
| Print file **STL** (≥ 1 part) | Yes | ฝาและ/หรือฐาน — แยกไฟล์ถ้าพิมพ์แยก |
| [Design report](resources/design-report-template.md) | Yes | กรอกครบทุกหัวข้อหลัก |
| [M05 pre-prototype checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | Yes | แนบหรือสรุปในรายงาน |
| Fitment / demo photos or clip | Strongly recommended | บอร์ดในกล่อง · พอร์ต · เซ็นเซอร์ |
| STEP (or CAD exchange) | Optional | ถ้ามีเครื่องมือแปลงสำหรับ CNC |

```text
Concept (M01) → Detail + PBR (M02) → Motion (M03)
    → GLB / Twin (M04) → Validate (M05) → Print + Report (M06)
```

---

## 2. Production Files — STL (and Optional STEP)

### 2.1 When to use which format

| Format | Use when |
|---|---|
| **STL** | พิมพ์ 3D ทั่วไป (FDM/SLA ตามรอบ) — **เส้นทางหลักของแล็บ** |
| **STEP** | ส่งต่อ CAD / CNC — มักต้องผ่านเครื่องมือแปลงหรือโมเดล CAD คู่ ไม่ใช่ปุ่มเดียวใน Blender ทุกเวอร์ชัน |

### 2.2 Mesh checks before export

เครื่องพิมพ์ต้องการ mesh ที่ **watertight / manifold** — ขอบแต่ละเส้นเชื่อมกับหน้าประมาณ 2 หน้า ไม่มีรูรั่วที่ไม่ตั้งใจ

ใช้ add-on **[3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)**:

1. `Edit → Preferences → Add-ons` → ค้นหา **3D Print Toolbox** → เปิดใช้  
2. ใน 3D Viewport กด `N` → แท็บ **3D-Print**  
3. เลือกชิ้นส่วน → **Check All**  
4. แก้ปัญหาที่รายงาน โดยเฉพาะ **Non-manifold**  
5. ใช้ **Make Manifold** เป็นจุดเริ่ม แล้วตรวจซ้ำด้วยตา  

ช่วยเพิ่ม:

- `Ctrl+A` → Scale ก่อน export  
- Edit Mode → Merge by Distance ถ้ามีจุดซ้ำ  
- `Shift+N` Recalculate Normals Outside  

ผนังยังควรประมาณ **≥ 2 mm** ตามแนวทาง enclosure พิมพ์ ([Protolabs](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/))

### 2.3 Export STL — step by step

1. แยก object ที่จะพิมพ์ (`Enclosure_base`, `Enclosure_lid`)  
2. เลือกชิ้นหนึ่ง (หรือใช้ batch ตามเวอร์ชัน)  
3. `File → Export → STL`  
4. เปิดตัวเลือกประมาณ: **Selection Only** · **Apply Modifiers** (ถ้ายังมี modifier)  
5. ตั้งชื่อชัด เช่น `enclosure_base.stl`, `enclosure_lid.stl`  
6. นำเข้า slicer (เช่น Cura) ตรวจขนาด mm อีกครั้งก่อนกดพิมพ์  

### 2.4 If you cannot print yet

ยังส่ง STL + รายงานได้ โดยระบุใน Design Report:

- แผนเครื่องพิมพ์/บริการ  
- วัสดุที่ตั้งใจ (เช่น PLA)  
- สิ่งที่จะตรวจตอนได้ชิ้นจริง  

อย่าปล่อยช่อง fitment ว่าง — ใช้การประกอบจำลองกับบอร์ด + กล่องกระดาษ/พลาสติกชั่วคราว หรือวัดช่องจากโมเดลเทียบบอร์ดจริงแล้วถ่ายรูปหลักฐาน

---

## 3. Prototype Build and Fitment

### 3.1 Fitment checklist (with real board)

| Check | Pass means |
|---|---|
| PCB inserts without forcing | ไม่ต้องงัดแรงจนเสี่ยงหักขา |
| Ports align | USB/สายเสียบได้หรือมองเห็นชัดว่าจะเสียบได้ |
| Sensor openings align | ช่องตรงชิป/ช่องระบายตามที่ออกแบบ |
| Lid closes reasonably | ไม่หลวมจนหลุดง่าย และไม่ต้องเคาะแรง |
| Fasteners / bosses (if any) | ใส่สกรูหรือแผนยึดได้ตามดีไซน์ |
| Internal cables | มีที่เดินสายตามที่เผื่อไว้ใน M01 |

แนวคิด assembly/clearance: [3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [All About Circuits enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)

### 3.2 Photograph evidence

ถ่ายอย่างน้อย:

1. ชิ้นพิมพ์หรือ STL ใน slicer (ถ้ายังไม่พิมพ์)  
2. บอร์ดวางในฐาน (หรือเทียบขนาด)  
3. ฝาประกอบ / ช่องพอร์ต  
4. (แนะนำ) เครื่องทำงานในกล่อง  

---

## 4. Test with Firmware and Edge AI

หลังใส่บอร์ดในกลอง (หรือวางเทียบ):

| Test | How | Evidence |
|---|---|---|
| Power / LED / button | เฟิร์มแวร์พื้นฐานยังตอบ | รูปหรือคลิปสั้น |
| Sensors still read | อุณหภูมิ / IMU ฯลฯ ไม่ถูกกล่องบังจนค่าตาย | Studio หรือ web-app |
| Twin still useful | เปิด GLB คู่กับของจริง | สกรีนช็อต |

### 4.1 Recommended host evidence

1. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) — Link + telemetry  
2. Hackathon `web-app/` — **ex05** หรือ **ex06** ([TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon))  
3. ถ้าใช้ HEX จากแพ็กแล็บ — ระบุเวอร์ชันในรายงาน  

จดว่าเซ็นเซอร์ในกล่อง**ยังอ่านได้หรือถูกลดทอน** — นี่คือบทเรียนสำคัญของ enclosure จริง

---

## 5. Design Report

คัดลอกแล้วกรอก [design-report-template.md](resources/design-report-template.md)

หัวข้อบังคับโดยสรุป:

1. ข้อมูลโครงงาน  
2. วัตถุประสงค์การออกแบบ  
3. สรุป Concept → Final  
4. สเกลและวัสดุ  
5. Twin integration  
6. Digital validation และปัญหาที่พบ (ดึงจาก M05)  
7. ผลการทดสอบ Prototype / Fitment  
8. ข้อเสนอแนะรอบถัดไป **อย่างน้อย 3 ข้อ**  
9. ภาคผนวกไฟล์  

> รายงานที่ดีอ่านแล้วทำซ้ำได้ — ไม่ใช่แค่คำสวยโดยไม่มีตัวเลขสเกลหรือชื่อไฟล์

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

งานต่อยอด (ไม่บังคับ): พิมพ์จริงครบฝา+ฐาน · ประกอบกับบอร์ดสำเร็จ · สตรีมเซ็นเซอร์ในกล่องผ่าน ex05/ex06 · STEP สำหรับงานต่อ

---

## 7. After Course 3

คุณพาผลิตภัณฑ์จาก **แนวคิด → โมเดล → Twin → checklist → ต้นแบบ** และเชื่อมกับข้อมูลเฟิร์มแวร์/Edge AI ได้ในระดับแล็บ

| Next direction | Where to go |
|---|---|
| เฟิร์มแวร์ลึกขึ้น | [Course 1](../../../firmware-sdk-edge-ai/README.md) |
| Twin / telemetry / MQTT | [Course 2](../../../digital-twin/README.md) |
| ผลิตจริง / injection | DFM และผู้ผลิต — Twin ในคอร์สเป็นสนามซ้อม |
| โมเดล/asset อ้างอิง | [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |

---

## Next Steps

1. ทำ [แล็บ](../l02-lab/README.md) — ส่งแพ็กเกจปิดคอร์ส  
2. กรอก [design-report-template.md](resources/design-report-template.md)  
3. แนบ checklist จาก [M05](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md)  

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

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ Capstone: แพ็กเกจต้นแบบและ Design Report](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Design report](resources/design-report-template.md) · [← TOC](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
