---
id: pdesign.m05.l02
lang: th
title:
  th: 'แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ'
  en: 'Lab: Scenarios and Pre-Prototype Checklist'
summary:
  th: เขียนสถานการณ์ก่อนคลิก รันและจดปัญหา ผูกข้อมูลหรือบันทึกช่องว่าง แล้วกรอก checklist ก่อนทำต้นแบบ
  en: Write scenarios before clicking, run them and log issues, bind data or document the gap, then complete the pre-prototype checklist.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m05.l01
objectives:
- th: รัน usage scenario ≥ 2 รายการบน Twin และจดปัญหาหรือจุดเฝ้าระวัง ≥ 3 ข้อ
  en: Run at least two usage scenarios on the Twin and log at least three issues or watch-outs.
- th: กรอก pre-prototype checklist พร้อม Top 3 fixes
  en: Complete the pre-prototype checklist with the top three fixes.
develops:
- skill: hwdev.enclosure
  to: 2
- skill: biz.product-decision
  to: 1
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M05/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M05 — Scenarios and Pre-Prototype Checklist

**Course 3 · Module 5**  
**Type:** Hands-on (scenarios · issues · optional fix · checklist)  
**Suggested time:** ~2.5–3 ชั่วโมง  

Read first: [Lesson](../l01-scenario-digital-validation/README.md) · [Pre-prototype checklist](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) · [← TOC](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | run scenarios |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | optional ex06 / ex05 |
| [Enclosure design guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/) | what to inspect |
| [M04 export checklist](../../m04-blender-to-twin/l01-blender-to-twin/resources/export-twin-checklist.md) | sensor point names |

---

## Lab Goals

- รัน usage scenario อย่างน้อย **2** รายการบน Twin  
- จดปัญหาหรือจุดเฝ้าระวังอย่างน้อย **3** ข้อ  
- (แนะนำ) จับคู่สถานะเฟิร์มแวร์/telemetry อย่างน้อย 1 อย่าง หรืออธิบายว่าทำไมยังไม่ผูก  
- กรอก [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) รวม **Top 3 fixes**  
- (ถ้าเวลาพอ) แก้โมเดล 1 จุดแล้ว export GLB ใหม่  

---

## Prerequisites

- [ ] มี `.glb` ใน Bitstream Studio จาก [M04](../../m04-blender-to-twin/l02-lab/README.md)  
- [ ] มีคลิปเปิดฝา หรือระบุว่าใช้มุมกล้องแทนชั่วคราว  
- [ ] โฟลเดอร์หลักฐาน `lab-notes/` หรือเทียบเท่า  

---

## Lab A — Write scenarios before you click (required)

เลือกอย่างน้อย 2 สถานการณ์จากบทเรียน §2.1 — **ต้องมี S3 (Lid service)** และอีกหนึ่งข้อ

| Scenario ID | Who / action | Expected result |
|---|---|---|
| S3 — Lid service | | |
| (second) | | |

**Pass when:** เพื่อนอ่านตารางแล้วรันซ้ำได้โดยไม่ถามเพิ่ม

---

## Lab B — Run scenarios and log issues (required)

สำหรับแต่ละสถานการณ์:

1. ทำตาม action  
2. จด expected vs actual  
3. แคปหน้าจออย่างน้อย 1 ภาพต่อสถานการณ์  
4. สะสมรายการปัญหา (เป้าหมายรวม ≥ 3 ข้อจากทุกสถานการณ์)

**Pass when:** มีบันทึกครบ 2 สถานการณ์และปัญหา ≥ 3 ข้อ

---

## Lab C — Bind data or document the gap (required)

เลือกหนึ่งทาง:

| Option | What to do |
|---|---|
| **C1** | Link Simulator/Board · เปิด ex06 หรือ ex05 · แคปคู่กับ Twin |
| **C2** | ผูกสถานะใน Studio (สี/คลิป/ไฮไลต์) กับ event หรือโหมด |
| **C3** | ยังผูกไม่ได้ — เขียนเหตุผล + แผนใน M06 ลง checklist |

**Pass when:** มีหลักฐานภาพ **หรือ** เหตุผลที่เขียนชัดใน checklist

---

## Lab D — Fill pre-prototype checklist (required)

1. กรอกทุกแถวหลักใน [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md)  
2. เขียน **Top 3 design fixes before print**  
3. ตัดสินใจ: Ready to print / Not ready (ระบุ blockers)

**Pass when:** Top 3 ไม่ว่าง และมีคำตัดสิน Ready/Not ready

---

## Lab E — Optional quick fix loop

1. เลือกปัญหา 1 ข้อจาก Top 3  
2. แก้ใน Blender  
3. Export GLB ตาม [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)  
4. Import ใหม่ · รัน S3 ซ้ำสั้น ๆ  
5. จดว่าดีขึ้นหรือยัง  

---

## Deliverables checklist

- [ ] 2 scenarios + screenshots  
- [ ] ≥ 3 issues / watch-outs  
- [ ] Pre-prototype checklist + Top 3 fixes  
- [ ] Lab C evidence or written gap  
- [ ] (optional) new GLB after fix  

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| ไม่รู้จะหาปัญหาอะไร | ใช้ตาราง Risk ในบทเรียน §3 · เปิด Wireframe ตอนเปิดฝา |
| ไม่มีสตรีมเซ็นเซอร์ | ใช้ C3 · หรือรันเฉพาะ S1–S3/S5 แล้วแผนผูกข้อมูลใน M06 |
| คลิปเปิดฝาไม่มี | หมุนมุมกล้องจำลองการเปิด · จดว่าต้องกลับ M03 |
| Checklist ผ่านหมดเร็วเกินไป | ให้เพื่อนในทีมทบทวน S3 อีกครั้ง — มักพบบานพับหรือพอร์ตที่พลาด |
| แก้โมเดลแล้วสเกลพัง | Apply Scale · ตรวจ Unit · export ใหม่ทั้งไฟล์ |

[Lesson](../l01-scenario-digital-validation/README.md) · [Pre-prototype checklist](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) · [TOC](../../README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)
