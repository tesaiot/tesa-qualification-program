---
id: pdesign.m03.l02
lang: th
title:
  th: 'แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น'
  en: 'Lab: Lid Animation and Short Sequences'
summary:
  th: ตั้งบานพับ keyframe คลิป `lid_open` สร้างคลิปปิด ตรวจการชน และบันทึกรายการคลิป
  en: Set the hinge, keyframe a `lid_open` clip, add a close clip, check interference and log the clip list.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m03.l01
objectives:
- th: สร้างคลิปเปิด/ปิดที่ตั้งชื่อแล้ว และบันทึกใน animation-clip-list.md
  en: Create named open/close clips and record them in animation-clip-list.md.
- th: บันทึกผลตรวจการชนพร้อมหลักฐานภาพหรือคลิปสั้น
  en: Record the interference check with an image or short clip as evidence.
develops:
- skill: hwdev.3d-modeling
  to: 2
assesses:
- skill: hwdev.3d-modeling
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
  path: C3/M03/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M03 — Lid Animation and Short Sequences

**Course 3 · Module 3**  
**Type:** Hands-on (pivot · keyframes · named clips · collision check)  
**Suggested time:** ~2.5–3 ชั่วโมง  

Read first: [Lesson](../l01-motion-and-interaction/README.md) · [Clip list](../l01-motion-and-interaction/resources/animation-clip-list.md) · [← TOC](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [Editing Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html) | `I` to insert keys |
| [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html) | playhead / Auto Key |
| [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html) | name clips |
| [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html) | hinge pivot |
| [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations) | naming for M04 |

---

## Lab Goals

- ตั้ง Origin ของฝาที่บานพับ  
- สร้างแอนิเมชันเปิด/ปิดอย่างน้อย 1 ชุด  
- ตรวจว่าชิ้นส่วนไม่ทะลุกันอย่างรุนแรงขณะเล่น  
- ตั้งชื่อ Action/clip เป็นภาษาอังกฤษสั้น เช่น `lid_open`  
- กรอก [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md)  

---

## Prerequisites

- [ ] มีไฟล์จาก M02 ที่แยก `Enclosure_lid` / `Enclosure_base` แล้ว  
- [ ] คัดลอกเป็น `m03_enclosure_motion.blend` ก่อนแก้  

ถ้ายังไม่แยกฝา–ฐาน ให้กลับไปทำ Lab C ใน [M02 lab](../../m02-modeling-render/l02-lab/README.md) ก่อน

---

## Lab A — Hinge origin (required)

1. เลือก `Enclosure_lid`  
2. วาง 3D Cursor ที่ขอบบานพับ (Edit Mode → `Shift+S` → Cursor to Selected)  
3. Object Mode → Origin to 3D Cursor  
4. `Ctrl+A` → Rotation & Scale  
5. ทดสอบหมุนด้วย `R` บนแกนที่ถูกต้อง — ต้องเปิดแบบบานพับ  

**Pass when:** เพื่อนในทีมหมุนฝาแล้วเข้าใจว่าบานพับอยู่ตรงไหนโดยไม่ต้องอธิบายยาว

---

## Lab B — Keyframe `lid_open` (required)

1. ตั้ง fps ของทีม (แนะนำ 24) และช่วงเฟรมประมาณ 1–3 วินาที  
2. เฟรมต้น: ฝาปิด → `I` → Rotation  
3. เฟรมปลาย: หมุนเปิด → `I` → Rotation  
4. Play ใน Timeline ตรวจการเคลื่อนไหว  
5. ตั้งชื่อ Action เป็น `lid_open` (หรือชื่อสื่อความหมายเทียบเท่า)  

**Pass when:** กด Play แล้วฝาเปิดจากปิดไปเปิดได้อย่างชัดเจน

---

## Lab C — Close clip or return motion (required)

เลือกอย่างใดอย่างหนึ่ง:

- **C1:** Action แยกชื่อ `lid_close`  
- **C2:** ช่วงเฟรมต่อจากเปิด แล้วกลับไปท่าปิด ในคลิปเดียวกัน (จดใน clip list ให้ชัด)

**Pass when:** มีทั้งสถานะเปิดและปิดที่เล่นซ้ำได้

---

## Lab D — Interference check (required)

1. เล่นแอนิเมชันช้า ๆ (เลื่อน playhead หรือลดความเร็วเล่น)  
2. สลับ Wireframe ตรวจจุดบานพับและชิ้นส่วนสูง  
3. จดใน clip list: ผ่าน / มีชนเล็กน้อย / ต้องแก้รูปทรง  
4. ถ้าชนรุนแรง: แก้ Origin มุมเปิด หรือกลับ M02  

**Pass when:** ไม่มีทะลุรุนแรง หรือมีบันทึกปัญหาพร้อมแผนแก้

---

## Lab E — Evidence + clip list (required)

1. กรอก [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) ครบทุกคลิป  
2. บันทึกหลักฐาน: สกรีนช็อตเฟรมปิด+เปิด หรือ viewport playblast สั้น ๆ  
3. Save `.blend`  

---

## Lab F — Optional extras

- คลิป `battery_reveal` (เลื่อนชิ้นแทนแบตเตอรี่)  
- Graph Editor ปรับ easing ให้นุ่มขึ้น  
- Parent ชิ้นส่วนเล็กติดกับฝา ([Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html))  

---

## Deliverables checklist

- [ ] `m03_enclosure_motion.blend`  
- [ ] Named open/close motion  
- [ ] Interference check บันทึกแล้ว  
- [ ] [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) กรอกครบ  
- [ ] หลักฐานภาพหรือคลิปสั้น  

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| ฝาหมุนแล้วลอยทั้งก้อน | Origin ยังไม่อยู่ที่บานพับ — ทำ Lab A ใหม่ |
| หมุนผิดแกน | ใช้ `R` แล้ว `X` / `Y` / `Z` · หรือหมุนใน Transform panel ทีละแกน |
| กด `I` แล้วไม่เห็นคีย์ | ดู Timeline · ปิด Only Show Selected ถ้าจำเป็น · ตรวจว่าเลือกวัตถุถูกชิ้น |
| Auto Key สร้างคีย์รก | ปิดปุ่มบันทึกใน Timeline แล้วลบคีย์เกินใน Dope Sheet |
| ชื่อ Action หายตอนเซฟ | ตรวจแผง Action · อย่าลบ Action โดยไม่ตั้งใจ |
| ชนที่บานพับ | เลื่อน Origin ออกนิด · หรือเว้นระยะฝา–ฐานในโมเดล |

[Lesson](../l01-motion-and-interaction/README.md) · [Clip list](../l01-motion-and-interaction/resources/animation-clip-list.md) · [TOC](../../README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)
