---
id: pdesign.m05.l01
lang: th
title:
  th: Digital validation ก่อนสร้างต้นแบบ
  en: Digital Validation before Prototyping
summary:
  th: ออกแบบสถานการณ์ทดสอบก่อนคลิก สังเกตและปรับดีไซน์ ผูกโมเดลกับข้อมูลเฟิร์มแวร์/Edge AI ด้วยหลักฐาน และสรุป checklist ก่อนพิมพ์
  en: Design test scenarios before clicking, observe and improve the design, bind the model to firmware/Edge AI data with evidence, and finish a pre-print checklist.
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
- pdesign.m04.l02
objectives:
- th: เขียน usage scenario อย่างน้อยสองรายการ พร้อมสิ่งที่ต้องดูบน Twin และสัญญาณผ่าน ก่อนลงมือทดสอบ
  en: Write at least two usage scenarios, each with what to watch on the Twin and its pass signal, before testing.
- th: ผูกสถานะเฟิร์มแวร์หรือ Edge AI หนึ่งอย่างเข้ากับการตอบสนองของโมเดล (สี คลิป หรือไฮไลต์) พร้อมหลักฐาน หรืออธิบายว่าทำไมยังผูกไม่ได้
  en: Bind one firmware or Edge AI state to a model response (colour, clip or highlight) with evidence, or explain why it cannot be bound yet.
- th: สรุปผลเป็น pre-prototype checklist ที่มี Top 3 fixes เรียงตามความสำคัญ
  en: Summarise the results as a pre-prototype checklist with the top three fixes in priority order.
develops:
- skill: iot.digital-twin
  to: 2
- skill: hwdev.enclosure
  to: 2
- skill: biz.product-decision
  to: 1
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Scenario and Digital Validation

**Course 3 · Module 5**  
**Suggested time:** ประมาณ 3 ชั่วโมง — รันสถานการณ์ใช้งานบน Twin จับคู่ข้อมูลเฟิร์มแวร์/Edge AI แล้วกรอกรายการแก้ก่อนพิมพ์ต้นแบบ  
**Format:** บทเรียนลงมือทำ — อ่านแล้วทดสอบตามสถานการณ์ได้เลย; การพิมพ์ STL และรายงานอยู่ที่ [M06](../../m06-prototyping/l01-prototyping-final-project/README.md)

[Lab](../l02-lab/README.md) · [Pre-prototype checklist](resources/pre-prototype-checklist.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. ตั้ง **usage scenario** (จับ วาง เปิดฝา ฯลฯ) ตามที่ Twin รองรับ  
2. ประเมินการตอบสนองของผลิตภัณฑ์และนำผลไปปรับปรุงการออกแบบ  
3. จับคู่โมเดลกับข้อมูล **Edge AI / เฟิร์มแวร์** (สถานะ → สี / คลิป)  
4. ทำ **Digital Validation** และรายการปรับปรุงก่อนสร้างต้นแบบ  

> **Key phrase**  
> Digital validation = *หาบั๊กดีไซน์บนจอก่อนเสียพลาสติก* — ถ้าพบปัญหาใน M05 แล้วยังไม่จด แสดงว่ายังไม่พร้อมพิมพ์ใน M06

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M04 — Blender to Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) | GLB ใน Bitstream Studio พร้อมแล้ว |
| [M03 — Motion](../../m03-motion/l01-motion-and-interaction/README.md) | คลิป `lid_open` สำหรับสถานการณ์เปิดฝา |
| [Course 2 M04 / M05](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) | co-sim · telemetry · web-app consumers |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | รัน scenario บน Twin host |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/ex06` (dashboard) · ex05 (orientation) |
| **[Electronic enclosure design guide (3DDFM)](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)** | checklist กล่องหุ้ม / clearance / assembly |
| **[Protolabs — Enclosure for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | ผนัง · clearance ก่อนพิมพ์ |
| **[All About Circuits — 3D-printed enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | PCB-first validation mindset |
| **[DFM checklist thinking (Root3 Labs)](https://www.root3labs.com/dfm-checklist-prototype-to-production/)** | คำถามก่อนขึ้น tooling / ผลิตจริง |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | อ้างอิงเฟิร์มแวร์เมื่อจับคู่สถานะ |
| [Pre-prototype checklist](resources/pre-prototype-checklist.md) | แบบฟอร์มผลงานหลักของบทนี้ |

---

## 1. What Digital Validation Means in This Course

**Digital validation** ใน M05 คือการพิสูจน์บน Twin ว่ากล่องหุ้ม + คลิป + จุดเซ็นเซอร์ **ใช้ร่วมกับข้อมูลจริง/จำลองได้** ก่อนสั่งพิมพ์ใน M06

ไม่ใช่:

- แทนการทดสอบมาตรฐานอุตสาหกรรมทั้งหมด  
- แทนการจำลองแรงกระแทกแบบ FEA เต็มรูป (เว้นแต่มีเครื่องมือนั้น)

แต่คือ:

```text
[Usage scenarios on Twin]
        │
        ▼
[Observe problems]  →  thin walls · blocked sensors · lid clash · bad port
        │
        ▼
[Bind firmware / Edge AI signals]  →  color / clip / highlight
        │
        ▼
[Pre-prototype checklist]  →  Top 3 fixes before print
```

แนวคิด enclosure/DFM ที่ใช้ประกอบการตรวจ: [3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [Protolabs enclosure guide](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)

---

## 2. Usage Scenarios — Design the Test First

ก่อนเล่นคลิป ให้เขียนสถานการณ์เป็นประโยคสั้น ๆ: **ใคร ทำอะไร คาดหวังเห็นอะไร**

### 2.1 Scenario catalog (pick at least two)

| Scenario ID | User action | What you watch on Twin | Pass signal |
|---|---|---|---|
| **S1 — Desk place** | วางเครื่องบนโต๊ะในแนวใช้งานปกติ | ฐานนิ่ง · origin ดูถูกต้อง | ไม่ล้มในมุมมอง / วางแล้วอ่านพอร์ตได้ |
| **S2 — Handheld** | ถือเครื่อง (จำลองมุมกล้องใกล้มือ) | ปุ่ม/LED อยู่ในจุดที่นิ้วถึง | ไม่มีขอบคมบังปุ่มสำคัญ |
| **S3 — Lid service** | เปิดฝาซ้ำ 3 รอบด้วยคลิป | การชน · มุมเปิด · เห็น PCB | ไม่ทะลุ · เปิดแล้วเห็นช่องบริการ |
| **S4 — Sensor access** | กระตุ้นเซ็นเซอร์ (scene/Motion/เอียงบอร์ด) | จุด `sensor_…` + ค่าบน dashboard | ช่องเซ็นเซอร์ไม่ถูกบัง · มีสตรีม |
| **S5 — Port plug** | จำลองเสียบสาย (มองช่องพอร์ต) | ช่อง USB/พอร์ต | ช่องใหญ่พอและหันทิศถูก |
| **S6 — Alert state** | ทำให้เกิด event เกินเกณฑ์ (จาก Course 2) | สี/ไฮไลต์บนโมเดลหรือคลิปสั้น | ทีมเฟิร์มแวร์กับดีไซน์ชี้จุดเดียวกันได้ |

ในแล็บบังคับอย่างน้อย **S3** และอีกหนึ่งข้อจาก S1/S2/S4/S5 (แนะนำเพิ่ม S4 หรือ S6 ถ้ามีสตรีม)

### 2.2 How to run a scenario (lab loop)

1. เปิดโมเดลใน [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
2. อ่านประโยคสถานการณ์ดัง ๆ (หรือเขียนบน checklist)  
3. ทำ action (เล่นคลิป / เปลี่ยนมุม / กระตุ้นเซ็นเซอร์)  
4. จด **สิ่งที่คาด** vs **สิ่งที่เห็น**  
5. ถ้าพัง: จ่ายเป็นรายการแก้ (อย่าแก้เงียบ ๆ โดยไม่บันทึก)

### 2.3 Optional impact / drop (concept only)

ถ้า Twin หรือเครื่องมือที่มี**ไม่มี**ฟิสิกส์กระแทก:

- ใช้สถานการณ์แนวคิด: “ถ้าตกจากโต๊ะ มุมไหนของกล่องรับแรงก่อน?”  
- จดสมมติฐาน + จุดที่ผนังบาง — **ไม่ต้องอ้างว่าจำลองแรงจริงแล้ว**

---

## 3. Observe and Improve the Design

ระหว่าง/หลัง scenario ให้มองหาอาการเหล่านี้ (สรุปจากแนวทาง enclosure ทั่วไป):

| Risk | What it looks like | Typical fix before print |
|---|---|---|
| ผนังบางเกินไป | ขอบดูคม/บางใน Twin หรือ Thickness < ~2 mm | เพิ่มความหนา · เติม rib ใน M02/M06 |
| ช่องเซ็นเซอร์ถูกบัง | ช่องไม่อยู่เหนือชิป · มีชิ้นส่วนบัง | เลื่อนช่อง · ตัด opener ใหม่ |
| พอร์ตเสียบยาก | ช่องเล็ก/เอียงผิด | ขยายช่อง · เผื่อ clearance |
| ฝาชนชิ้นสูง | คลิปเปิดแล้วทะลุ USB/จอ | ลดมุมเปิด · เลื่อนบานพับ · สูงกล่อง |
| ประกอบลำบาก | ไม่มีที่ใส่สกรู/แยกฝาไม่ชัด | แผน bosses ใน M06 · แยกชิ้นพิมพ์ |
| สเกลเพี้ยน | เทียบบอร์ดจริงแล้วไม่คล้าย | กลับ M01/M04 แก้แล้ว export ใหม่ |

ต้องจดปัญหาอย่างน้อย **3 ข้อ** ใน lab — แม้บางข้อจะเป็น “ผ่าน แต่ควรระวัง”

ถ้าเวลาพอ: กลับ Blender แก้ **อย่างน้อย 1 จุด** แล้ว export GLB รอบใหม่ (ทบทวน [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md))

---

## 4. Bind the Model to Edge AI / Firmware Data

เป้าหมาย: Twin เป็น**ภาษาเดียวกัน**ของทีมออกแบบกับทีมเฟิร์มแวร์

### 4.1 Binding patterns (pick one or more)

| Firmware / Twin signal | Visual response on model |
|---|---|
| อุณหภูมิสูง / threshold event | เน้นบริเวณช่องเซ็นเซอร์ หรือเปลี่ยนสีตัวเครื่อง |
| BMI270 orientation | หมุน preview ตามท่า (ถ้า host รองรับ) หรือเทียบจอสองหน้า |
| Mode / LED on device | Emission หรือสีที่ `led_status_window` |
| คำสั่งเปิดฝาจาก UI | เล่นคลิป `lid_open` |

ทบทวนท่อข้อมูล: [Course 2 M05](../../../digital-twin/m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) · จุดที่ตั้งชื่อไว้ใน [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

### 4.2 Second screen — Hackathon dashboard

แนะนำระหว่างรัน S4/S6:

1. Serve `web-app/` จาก [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
2. เปิด **ex06** (multi-sensor dashboard) หรือ **ex05** (orientation)  
3. แคปคู่: Twin scenario + ค่าเซ็นเซอร์สด  

ถ้าไม่มีสตรีมในรอบนั้น ให้ใช้ **สคริปต์สถานะจำลอง** ใน Studio (ถ้ามี) หรือบันทึกว่าผูกข้อมูลเป็นแผนสำหรับ M06 / Course 2 — อย่าปล่อยช่องว่างโดยไม่เขียนเหตุผล

### 4.3 Evidence rule

| Binding claim | Evidence required |
|---|---|
| “โมเดลตอบตามเซ็นเซอร์” | สกรีนช็อต/คลิปที่เห็นทั้งโมเดลและการเปลี่ยนค่า |
| “ช่องเซ็นเซอร์ตรงตำแหน่ง” | ภาพ Twin ชี้จุด + ชื่อ `sensor_…` + (ถ้ามี) บอร์ดจริง |
| “ยังไม่ผูกได้ในรอบนี้” | เหตุผลสั้น + สิ่งที่จะทำใน M06 |

---

## 5. Digital Validation Checklist (Before Prototype)

กรอกฉบับเต็มใน [pre-prototype-checklist.md](resources/pre-prototype-checklist.md)

### 5.1 Minimum validation columns

| Area | Key question |
|---|---|
| **Scale** | ขนาดยังตรงบอร์ด/สูตร M01 อยู่หรือไม่ |
| **Internal fit** | PCB + แบตเตอรี่ + สาย อยู่ร่วมกันได้หรือไม่ |
| **Sensor openings** | ช่องตรงตำแหน่งเซ็นเซอร์จริงหรือไม่ |
| **Ports** | เสียบสาย/มองเห็น LED ได้หรือไม่ |
| **Walls** | หนาพอสำหรับพิมพ์ (~2 mm เป็นจุดเริ่ม) |
| **Motion** | ฝา/ปุ่มชนชิ้นอื่นหรือไม่ |
| **Twin stability** | import GLB เสถียร เล่นคลิปได้ |
| **Data link** | มีการจับคู่สถานะอย่างน้อยหนึ่งอย่าง หรือมีเหตุผลที่ยังไม่ทำ |

อ้างอิงคำถาม enclosure/DFM เพิ่ม: [3DDFM checklist section](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [Root3 DFM questions](https://www.root3labs.com/dfm-checklist-prototype-to-production/)

### 5.2 Top 3 fixes before print

ท้าย checklist ต้องมี **3 รายการแก้เรียงความสำคัญ** เช่น:

1. ขยายช่อง USB +0.5 mm ต่อด้าน  
2. ลดมุมเปิดฝาจาก 110° เป็น 95°  
3. เพิ่มความหนาผนังฝาเป็น 2.0 mm  

ถ้าทุกอย่างผ่าน: เขียนว่า “Ready to print” และระบุสิ่งที่ยังเฝ้าระวังตอนประกอบจริง

---

## 6. Quality Gate Before M06

| Check | Pass means |
|---|---|
| ≥ 2 scenarios run | มีบันทึก expected vs actual |
| ≥ 3 design issues or watch-outs logged | ไม่เว้นว่าง |
| Pre-prototype checklist filled | รวม Top 3 fixes |
| Optional: 1 model fix re-exported | ถ้าแก้แล้ว มี GLB ใหม่ |
| Optional: telemetry/web-app pair shot | หลักฐานการจับคู่ข้อมูล |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. กรอก [pre-prototype-checklist.md](resources/pre-prototype-checklist.md)  
3. เมื่อพร้อม ไปต่อ [M06 — Prototyping and Final Project](../../m06-prototyping/l01-prototyping-final-project/README.md)

---

## References and Further Reading

1. [M04 Blender to Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M03 Motion](../../m03-motion/l01-motion-and-interaction/README.md) · [Course 3 TOC](../../README.md)  
2. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
3. [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) — `ex05`, `ex06`  
4. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)  
5. [Electronic Enclosure Design Guide (3DDFM)](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)  
6. [Enclosure design for 3D printing (Protolabs Network)](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)  
7. [Six steps for 3D-printed electronics enclosures (All About Circuits)](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)  
8. [DFM checklist questions (Root3 Labs)](https://www.root3labs.com/dfm-checklist-prototype-to-production/)  
9. [Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 2 M05](../../../digital-twin/m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Pre-prototype checklist](resources/pre-prototype-checklist.md) · [← TOC](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)
