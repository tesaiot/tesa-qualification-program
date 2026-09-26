---
id: pdesign.m06.l02
lang: th
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — Prototype Package and Design Report

**Course 3 · Module 6**  
**Type:** Capstone / handoff package  
**Suggested time:** ~3 ชั่วโมง (+ เวลาพิมพ์/ประกอบแยกต่างหาก)

Read first: [Lesson](../l01-prototyping-final-project/README.md) · [Design report](../l01-prototyping-final-project/resources/design-report-template.md) · [← TOC](../../README.md) · [← M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html) | manifold check |
| [M05 checklist](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | Top 3 fixes before print |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | optional sensor proof in enclosure |

---

## Lab Goals

ส่งแพ็กเกจปิด Course 3 ให้ครบไฟล์ รายงาน และหลักฐาน fitment/ทดสอบ

---

## Prerequisites

- [ ] M05 ตัดสิน Ready หรือมีแผนแก้ที่ทำแล้ว  
- [ ] มี `.blend` + `.glb` ล่าสุด  
- [ ] โฟลเดอร์ผลงาน เช่น `course3-final/`  

---

## Lab A — Apply M05 fixes (required)

1. เปิด Top 3 จาก M05  
2. แก้ใน Blender ตามลำดับความสำคัญ (อย่างน้อยที่ทำได้ในเวลา)  
3. Save `.blend` สุดท้าย  
4. Export `.glb` ใหม่ถ้าโมเดล Twin เปลี่ยน  

**Pass when:** รายงานระบุว่าแก้ข้อไหนแล้ว / ข้อไหนยังค้าง

---

## Lab B — Mesh check and export STL (required)

1. เปิด **3D Print Toolbox**  
2. Check All บนชิ้นที่จะพิมพ์  
3. แก้ non-manifold จนตรวจผ่านพอสำหรับแล็บ  
4. Export STL อย่างน้อย 1 ชิ้น (`enclosure_base.stl` และ/หรือ `enclosure_lid.stl`)  
5. เปิดใน slicer ตรวจหน่วยเป็น mm  

**Pass when:** มีไฟล์ STL และสกรีนช็อต slicer หรือรายการ Check All ที่ผ่าน

---

## Lab C — Print or print plan (required)

| Track | What to do |
|---|---|
| **C1 — Print available** | พิมพ์อย่างน้อยหนึ่งชิ้น · ถ่ายรูปชิ้นงาน |
| **C2 — No printer** | ระบุบริการ/เครื่อง · วัสดุ · เวลาที่คาด · และหลักฐานวัดเทียบบอร์ดกับโมเดล |

**Pass when:** มีรูปพิมพ์ **หรือ** แผนพิมพ์ที่ตรวจสอบได้ + หลักฐานการวัด

---

## Lab D — Fitment with hardware (required)

1. ใส่/เทียบ PCB กับฐาน  
2. ตรวจพอร์ต ช่องเซ็นเซอร์ ฝา  
3. ถ่ายรูปอย่างน้อย 2 มุม  
4. จดผล Pass/Fail ทีละข้อลง Design Report §7  

**Pass when:** มีตาราง fitment ที่กรอกจริง ไม่เว้นว่างทั้งหน้า

---

## Lab E — Firmware / Twin / web-app check (required)

เลือกอย่างน้อยหนึ่งหลักฐาน:

- LED/ปุ่มทำงานในกล่องหรือขณะวางเทียบ  
- Telemetry ใน Bitstream Studio  
- Hackathon **ex05** หรือ **ex06** หลังประกอบ  

**Pass when:** รายงานระบุผล “เซ็นเซอร์ยังอ่านได้ / อ่านได้แต่เพี้ยน / ยังทดสอบไม่ได้เพราะ…”

---

## Lab F — Design report package (required)

1. กรอก [design-report-template.md](../l01-prototyping-final-project/resources/design-report-template.md) ครบ  
2. แนบรายการไฟล์ใน §9  
3. ข้อเสนอแนะรอบถัดไป ≥ 3 ข้อ  
4. แนบหรือสรุป M05 checklist  
5. ตรวจไม่มีรหัสผ่านในไฟล์ส่ง  

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
| Slicer บอก mesh พัง | 3D Print Toolbox · Make Manifold · ตรวจ normals |
| STL ขนาดผิด | Apply Scale · หน่วย mm · ตรวจ scale ใน slicer |
| PCB ใส่ไม่ลง | กลับ Top 3 จาก M05 · อย่าตะไบโดยไม่จดในรายงาน |
| เซ็นเซอร์ในกล่องเงียบ | ช่องถูกบัง · วัสดุหนา · หรือสายหลุด — แยกทีละชั้น |
| ไม่มีเครื่องพิมพ์ | ใช้ Track C2 ให้ครบ ไม่ปล่อยว่าง |

[Lesson](../l01-prototyping-final-project/README.md) · [Design report](../l01-prototyping-final-project/resources/design-report-template.md) · [TOC](../../README.md)
