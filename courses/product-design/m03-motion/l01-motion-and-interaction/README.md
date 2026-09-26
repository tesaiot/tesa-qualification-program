---
id: pdesign.m03.l01
lang: th
title:
  th: แอนิเมชันเปิด–ปิดและการตรวจการชน
  en: Open/Close Animation and Interference Checks
summary:
  th: เตรียม pivot ของฝา keyframe เปิด–ปิด ตั้งชื่อ Action ตรวจการชนขณะเล่น และเตรียมคลิปสำหรับ Twin
  en: Prepare the lid pivot, keyframe open and close, name the Action, check interference during playback and prepare clips for the Twin.
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
- pdesign.m02.l02
objectives:
- th: ตั้ง origin ของฝาที่บานพับ และ Apply Rotation/Scale ก่อนใส่ keyframe
  en: Place the lid origin at the hinge and apply rotation/scale before keyframing.
- th: สร้างคลิปเปิด–ปิด และตั้งชื่อ Action เป็นภาษาอังกฤษสั้นที่อ้างถึงได้ เช่น `lid_open`
  en: Create open/close clips and give each Action a short English name such as `lid_open`.
- th: ตรวจการชนขณะเล่นแอนิเมชัน และเลือกวิธีแก้ (เลื่อนบานพับ ลดมุมเปิด หรือแก้รูปทรง)
  en: Check for interference during playback and choose a fix (move the hinge, reduce the angle or change the shape).
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — Motion and Interaction

**Course 3 · Module 3**  
**Suggested time:** ประมาณ 3 ชั่วโมง — สร้างภาพเคลื่อนไหวเปิด–ปิดชิ้นส่วน ตรวจการชน และตั้งชื่อคลิปให้พร้อมใช้กับ Twin  
**Format:** บทเรียนลงมือทำ — อ่านแล้วทำตามใน Blender ได้เลย; การส่งออก GLB ไป Twin อยู่ที่ [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

[Lab](../l02-lab/README.md) · [Clip list](resources/animation-clip-list.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. สร้างภาพเคลื่อนไหวสำหรับเปิด–ปิดชิ้นส่วนหรือแสดงโครงสร้างภายใน  
2. จำลองการเคลื่อนไหวเพื่อประเมินความเหมาะสมในการใช้งาน (ชิ้นส่วนไม่ทะลุกัน)  
3. สร้างชุดลำดับการเคลื่อนไหว (**named clips / actions**) สำหรับ Twin หรือสื่อการสอน  

> **Key phrase**  
> Animation ใน M03 คือ**เครื่องมือตรวจกลไก** ไม่ใช่แค่ทำให้ดูสวย — ถ้าฝาเปิดแล้วทะลุฐาน แสดงว่าดีไซน์ยังไม่พร้อมพิมพ์

### How this differs from Course 2 M03

| Course | M03 focus |
|---|---|
| [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | Virtual Device · sensor script · event simulation |
| **Course 3 M03 (this module)** | **Animation ของผลิตภัณฑ์ใน Blender** (เปิดฝา / หมุนชิ้นส่วน / คลิปสั้น) |

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M02 — Modeling, Materials, Render](../../m02-modeling-render/l01-modeling-materials-render/README.md) | ต้องมี `Enclosure_lid` / `Enclosure_base` แยกชิ้นแล้ว |
| **[Insert / edit keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html)** | กด `I` ใส่คีย์เฟรม |
| **[Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)** | เล่น / เลื่อนเฟรม / Auto Key |
| **[Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)** | เก็บแอนิเมชันเป็น Action ตั้งชื่อได้ |
| **[Dope Sheet](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)** | จัดคีย์เฟรมทั้งคลิป |
| **[Graph Editor](https://docs.blender.org/manual/en/4.5/editors/graph_editor/index.html)** | ปรับความนุ่มของ motion (optional) |
| **[Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)** | จุดหมุนของฝา (บานพับ) |
| **[Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html)** | (ทางเลือก) ผูกชิ้นส่วนกับฝา |
| **[glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)** | เตรียมชื่อคลิปให้ export ใน M04 |
| **[Blender Fundamentals — Animation](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | วิดีโอทางการ (เลือกบท Animation) |
| **[INC111-2021 (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Tutorial ภาษาไทย |
| [Clip list worksheet](resources/animation-clip-list.md) | บันทึกชื่อคลิป ความยาว แกนหมุน |

---

## 1. Why Animate the Product?

ภาพเคลื่อนไหวในงาน enclosure ช่วยตอบคำถามที่ภาพนิ่งตอบไม่ครบ:

| Question | What motion shows |
|---|---|
| เปิดฝาแล้วมือหรือสายชนไหม? | เส้นทางหมุนของฝา |
| ช่องภายในพอใส่ PCB / แบตเตอรี่ไหม? | เปิดฝาแล้วเห็นช่องว่าง |
| ผู้ใช้เข้าใจวิธีเปิดอย่างไร? | คลิปสั้นสำหรับสื่อการสอน |
| Twin จะเล่นสถานะอะไรได้บ้าง? | ชื่อคลิป เช่น `lid_open` |

ในระยะแรกของคอร์สนี้ **ใช้คีย์เฟรมของ Location / Rotation เป็นหลัก**  
Armature (กระดูก) เก็บไว้เมื่อกลไกซับซ้อนจริง ๆ — ส่วนใหญ่ฝากล่องหมุนรอบขอบด้านหลังก็พอ

---

## 2. Prepare the Lid Pivot (Do This Before Keyframes)

จาก M02 คุณควรมี object แยกแล้ว เช่น `Enclosure_lid` และ `Enclosure_base`

### 2.1 Place the origin at the hinge

จุด Origin ของฝา = จุดหมุน ([Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html))

ขั้นตอนที่แนะนำ:

1. เลือก `Enclosure_lid`  
2. เข้า Edit Mode · เลือกขอบหรือจุดที่ต้องการเป็นบานพับ (มักเป็นขอบหลังด้านใน)  
3. `Shift+S` → Cursor to Selected  
4. Object Mode → `Object → Set Origin → Origin to 3D Cursor`  
5. กลับ Cursor ไปที่ World Origin ถ้าต้องการ (`Shift+S` → Cursor to World Origin)

ทดสอบ: กด `R` แล้วหมุนรอบแกนที่ถูกต้อง (มักเป็น **X** หรือ **Y** ตามทิศวางโมเดล) — ฝาควรเปิดเหมือนบานพับ ไม่ลอยไปทั้งก้อน

### 2.2 Apply Rotation and Scale

ก่อนใส่คีย์เฟรม:

- `Ctrl+A` → **Rotation & Scale** บนฝา (และฐานถ้าจำเป็น)  
- อ่าน [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

ถ้า Rotation ในแผง Item ไม่เป็นศูนย์ทั้งที่ฝาดูตรง อาจสับสนตอนใส่คีย์ — Apply ช่วยให้ค่าเริ่มต้นอ่านง่าย

---

## 3. Keyframe Workflow — Lid Open / Close

อ้างอิงตัวอย่างอย่างเป็นทางการใน [Editing Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html) และควบคุมเวลาด้วย [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)

### 3.1 Set frame rate and range

| Setting | Lab default | Where |
|---|---|---|
| Frame rate | **24 fps** หรือ 30 fps (ทีมเดียวกัน) | Output Properties |
| Clip length | **1–3 วินาที** ต่อคลิป | เช่น 24–72 เฟรมที่ 24 fps |
| Scene End | ให้ยาวพอเล่นคลิป | Timeline Start/End |

ตัวอย่างคลิป `lid_open` ที่ 24 fps ความยาว 1.5 วินาที ≈ เฟรม 1 → 36

### 3.2 Insert keys (closed → open)

1. ไปเฟรม **1** (ฝาปิด)  
2. เลือก `Enclosure_lid`  
3. กด `I` → เลือก **Rotation** (หรือ LocRot ถ้าต้องขยับด้วย)  
4. ไปเฟรมปลายคลิป (เช่น **36**)  
5. หมุนฝาเปิดในมุมที่ใช้งานจริง (เช่น 90° หรือ 110°)  
6. กด `I` → **Rotation** อีกครั้ง  
7. กด **Space** (หรือปุ่ม Play ใน Timeline) เพื่อเล่น  

ถ้าอยากให้ Blender ใส่คีย์อัตโนมัติขณะหมุน: เปิด **Auto Key** ใน Timeline ([Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)) — จำไว้ว่าเปิดแล้วทุกการขยับจะติดคีย์

### 3.3 Optional second clip — close

สร้างคลิปปิดแยก หรือต่อในช่วงเฟรมถัดไป:

- เฟรม 36 = เปิด  
- เฟรม 72 = ปิด (คัดลอกค่า rotation จากเฟรม 1)

สำหรับ Twin มักแยกชื่อชัดกว่า: `lid_open` และ `lid_close`

### 3.4 Name the Action

Animation ใน Blender ถูกเก็บใน **Action** ([Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html))

1. เปิด Dope Sheet → โหมด **Action** (หรือแผง Action ใน Animation workspace)  
2. ตั้งชื่อ Action เป็นภาษาอังกฤษสั้น เช่น `lid_open`  
3. หลีกเลี่ยงชื่อว่าง / ชื่อซ้ำ / ภาษาไทยในชื่อไฟล์คลิปที่ส่ง Twin  

ชื่อที่ดี:

| Good name | Avoid |
|---|---|
| `lid_open` | `Anim1`, `asdf`, `เปิดฝา` |
| `lid_close` | `final_final2` |
| `battery_reveal` | ชื่อยาวมีช่องว่างเยอะ |

จดทุคลิปใน [animation-clip-list.md](resources/animation-clip-list.md)

---

## 4. Collision / Interference Check While Playing

เล่นแอนิเมชันช้า ๆ แล้วตรวจ:

| Check | Pass means |
|---|---|
| Lid vs base | ไม่ทะลุกันรุนแรงตรงบานพับ |
| Lid vs tall components | ไม่ชนหัว USB / เซ็นเซอร์ / จอ |
| Cable / finger space (concept) | มีช่องให้จินตนาการมือเปิดได้ |
| Extreme angle | มุมเปิดไม่เกินที่กลไกจริงทำได้ |

ถ้าชน:

1. เลื่อนบานพับ (Origin)  
2. ลดมุมเปิด  
3. หรือกลับไปแก้รูปทรงใน M02 (ระยะห่างผนัง / ความสูงชิ้นส่วน)

> **Key phrase**  
> Motion ที่ชน = **บั๊กดีไซน์** ที่จับได้ถูกกว่าตอนพิมพ์แล้วค่อยรู้

ไม่จำเป็นต้องเปิด Physics simulation ใน M03 — การดูด้วยตา + Wireframe ก็เพียงพอสำหรับแล็บ

---

## 5. Useful Product Motions (Pick What Fits)

| Motion idea | Typical keys | Twin / teaching use |
|---|---|---|
| เปิด–ปิดฝา | Rotation on hinge | หลักของแล็บนี้ |
| เผย PCB ภายใน | Lid open + camera hold | สื่อการสอนโครงสร้าง |
| ถอดแบตเตอรี่ (แนวคิด) | Location ของ `Battery_block` | แสดงช่องบริการ |
| สถานะ LED / ชิ้นหมุน | Rotation เล็กน้อยหรือ Emission (จาก M02) | demo สถานะทำงาน |

เลือกอย่างน้อย **หนึ่งชุดเปิด/ปิด** ให้ผ่านเกณฑ์ — ส่วนอื่นเป็นงานต่อยอด

---

## 6. Sequences for Twin and Teaching Media

### 6.1 Keep clips short and purposeful

| Guideline | Why |
|---|---|
| 1–3 วินาทีต่อคลิป | จัดการง่าย · export เบา · ผู้ชมเข้าใจจุดเดียว |
| หนึ่งคลิป = หนึ่งเจตนา | `lid_open` ไม่ปนการหมุนกล้องยาว |
| ชื่อคงที่ทั้งทีม | M04 / Bitstream Studio อ้างชื่อเดียวกัน |

### 6.2 Prepare for glTF export (preview of M04)

ตาม [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations):

- แอนิเมชันที่ export ได้ดีคือ **keyframe ของ transform** (และบางกรณี shape keys)  
- ถ้ามีหลาย Action ที่จะส่งออก มักต้อง **Stash** ลง NLA ตามโหมด export  
- ชื่อ track / action มีผลต่อชื่อคลิปในไฟล์ GLB  

ใน M03 ให้ทำให้เล่นใน Blender ถูกและตั้งชื่อคลิปครบ — รายละเอียดปุ่ม export อยู่ที่ M04

### 6.3 Optional playblast for evidence

บันทึกหลักฐานสั้น ๆ โดยไม่ต้องเรนเดอร์เต็ม:

- Viewport → View → Viewport Render Animation (ชื่อเมนูตามเวอร์ชัน)  
- หรือบันทึกหน้าจอขณะกด Play  

แนบไฟล์หรือสกรีนช็อตลำดับเฟรมคู่กับ clip list

---

## 7. Quality Gate Before M04

| Check | Pass means |
|---|---|
| Lid origin at hinge | หมุนแล้วเป็นบานพับ |
| At least one open/close motion | เล่นใน Timeline ได้ |
| No severe mesh intersection | ตรวจตอนเล่น |
| Named action/clip | เช่น `lid_open` |
| Clip list filled | [animation-clip-list.md](resources/animation-clip-list.md) |
| Scale from M01–M02 unchanged | PCB ยังใส่ได้ |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. กรอก [animation-clip-list.md](resources/animation-clip-list.md)  
3. เมื่อพร้อม ไปต่อ [M04 — Blender to Twin Integration](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

---

## References and Further Reading

### Blender animation (official)

1. [Editing Keyframes (4.5 LTS)](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html)  
2. [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)  
3. [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)  
4. [Dope Sheet](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)  
5. [Graph Editor](https://docs.blender.org/manual/en/4.5/editors/graph_editor/index.html)  
6. [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)  
7. [Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html)  
8. [glTF 2.0 — Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)  
9. [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)  
10. [INC111-2021 Blender (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)  

### Course links

11. [M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [Course 3 TOC](../../README.md)  
12. [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) (Virtual Device — คนละโฟกัส)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Clip list](resources/animation-clip-list.md) · [← TOC](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)
