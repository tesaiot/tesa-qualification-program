---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — หลักออกแบบเชิงอุตสาหกรรมและกล่องหุ้มตามสเกลจริง"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 1.1 — หลักออกแบบเชิงอุตสาหกรรมและกล่องหุ้มตามสเกลจริง

## สี่เลนส์ของงานออกแบบ ลำดับ Concept → Block → Final และการตั้งหน่วย/สเกลใน Blender ให้ตรงฮาร์ดแวร์จริง

**โมดูล 1 — พื้นฐานการออกแบบเชิงอุตสาหกรรม**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. ตรวจแนวคิดผลิตภัณฑ์ด้วยสี่เลนส์ (Function, Form & Proportion, Material & Manufacturing, User Experience) และเลนส์ Electronics fit
2. คำนวณขนาดภายนอกของกล่องหุ้มจากขนาด PCB, clearance และความหนาผนัง
3. ตั้งหน่วย Blender เป็น Metric / Millimeters / Unit Scale 0.001 และ Apply Scale หลังปรับขนาด

> **คาถาประจำบทเรียน**
> ใน M01 ให้ **ล็อกขนาดให้ตรงฮาร์ดแวร์ก่อน** แล้วค่อยทำให้งาม — ถ้ากล่องหยาบ (block) ผิดตั้งแต่ต้น งานในโมดูลถัดไปจะแก้แพงทั้งหมด

---

## ทำไม Industrial Design สำคัญกับอุปกรณ์ Edge AI

กล่องหุ้ม (enclosure) ของอุปกรณ์ Edge AI/IoT ต้องรับมือกับอย่างน้อย 5 เรื่อง

| เรื่อง | ทำไมสำคัญ |
|---|---|
| ขนาด PCB + ความสูงชิ้นส่วน | ใส่ไม่ลง / กดปุ่มไม่ถึง |
| ช่องเซ็นเซอร์ / พอร์ต USB | ถูกบัง → ข้อมูลเพี้ยน หรือเสียบสายไม่ได้ |
| การจับถือ / วางโต๊ะ | ergonomics และจุด origin ใน Twin |
| การผลิตต้นแบบ (FDM/SLA) → ฉีดพลาสติกภายหลัง | ผนังหนา / fillet / bosses มีข้อจำกัดต่างกัน |
| Digital Twin | สเกลและแกนผิด → animation / telemetry ดูหลอก |

หลักสูตรนี้ใช้ **Blender** เพราะฟรี โอเพนซอร์ส และส่งออก glTF/GLB เข้า Twin host ได้ในโมดูล 4

---

## Industrial-grade Design — สี่เลนส์ (+ หนึ่งเลนส์เสริม)

| เลนส์ | คำถามที่ต้องตอบ | ตัวอย่างกับอุปกรณ์ Edge |
|---|---|---|
| **Function** | ใช้ทำอะไร ในสภาพแวดล้อมใด | มอนิเตอร์สิ่งแวดล้อม · สวมใส่ · ติดเครื่องจักร |
| **Form & Proportion** | สัดส่วนจับถนัดไหม สมดุลไหม | สูงเกินไปจนล้มง่าย · ขอบคม |
| **Material & Manufacturing** | พิมพ์ 3D / ฉีดพลาสติก / CNC ได้จริงไหม | ผนังบางเกิน · โพรงพิมพ์ยาก |
| **User Experience** | เปิดฝา ดู LED เสียบสายได้ไม่ต้องพึ่งคู่มือไหม | ช่อง USB หันผิดทาง |

> **Electronics fit (เลนส์เสริมสำหรับอุปกรณ์ที่มี PCB)** — ทุกมิลลิเมตรของกล่องต้องอ้างอิงชิ้นส่วนจริงหรือ placeholder ที่วัดแล้ว

---

## ลำดับงาน enclosure ที่ใช้ในหลักสูตรนี้

1. โมเดล **ชิ้นภายในก่อน** (PCB, battery, connectors)
2. สร้าง **เปลือกนอก** แล้วเว้นผนัง + clearance
3. เจาะช่องพอร์ต / LED / เซ็นเซอร์
4. แยกฝาบน–ฐาน · เตรียมจุดยึด (bosses) ในโมดูลหลัง
5. ตรวจ interference ก่อนพิมพ์

```text
Concept sketch → Block model (โมดูลนี้) → Detailed model + materials (M02)
    → Motion clips (M03) → Twin + validation (M04–M05) → Print / fitment / report (M06)
```

---

## Concept → Block → Final (ห้ามข้ามขั้น)

| ขั้น | สิ่งที่ต้องได้ | ยังไม่ต้องทำ |
|---|---|---|
| **Concept** | สัดส่วนหยาบ ทิศทางรูปทรง ใครถือ/วางอย่างไร | วัสดุเงา · fillet เล็ก · สกรูละเอียด |
| **Block Model** | กล่องแทน PCB + แบต + โมดูล · enclosure นอกตามสเกล mm | Boolean ช่องพอร์ตสวย · UV |
| **Final Model** | รายละเอียดใช้งานจริง (โมดูลถัดไป) | — |

**Block Model คือหัวใจของบทเรียนนี้** — ก่อนเปิด Blender ให้ตอบสั้น ๆ ก่อน: ผู้ใช้ถือเครื่องอย่างไร · พอร์ตไหนต้องเห็นจากภายนอก · เซ็นเซอร์ไหนต้องมีช่องเปิด · ฝาเปิดทางไหน

> รายละเอียดผิวเร็วเกินไปบนสเกลผิด = งานสวยที่ใส่บอร์ดจริงไม่ได้

---

## เก็บขนาดจริงก่อน แล้วคำนวณกล่องนอก

ลำดับที่แนะนำ: วัดบอร์ดจริงด้วยเวอร์เนีย (กว้าง × ยาว × หนา + ความสูงชิ้นส่วนสูงสุด) หรือเปิดเอกสารชุดประเมินผลที่ใช้ แล้วจดแหล่งที่มาของตัวเลขไว้เสมอ

| พารามิเตอร์ | ค่าเริ่มต้นในแล็บ | หมายเหตุ |
|---|---|---|
| ระยะ PCB ↔ ผนังด้านใน | ≥ 0.5 mm ต่อด้าน | FDM มักเผื่อมากกว่า (ถึง ~1 mm) |
| ความหนาผนัง (wall) | ≈ 2.0 mm | ขั้นต่ำที่แนะนำสำหรับ enclosure ทั่วไป |
| ช่องว่างเหนือชิ้นส่วนสูงสุด | ≥ 2–3 mm | สายไฟ / หัว USB / ความคลาดเคลื่อนพิมพ์ |
| ช่องพอร์ต | เผื่อรอบปลั๊ก | อย่าเจาะพอดีพิกเซลกับ connector |

```text
outer_X ≈ PCB_X + 2×clearance + 2×wall
outer_Y ≈ PCB_Y + 2×clearance + 2×wall
outer_Z ≈ PCB_Z_stack + top_air + bottom_air + wall(s)
```

ในบทเรียนนี้ยังไม่ต้อง Solidify ผนังจริง — แค่วาด outer box ให้ใหญ่กว่า PCB ตามสูตรนี้ก็พอ

---

## ตัวอย่างสมบูรณ์ (1) — ตั้งฉากและหน่วยใน Blender

- **ท่าที่ 1** ติดตั้ง Blender (แนะนำสาย LTS) แล้ว `File → New → General` ลบ Cube เริ่มต้นถ้าต้องการฉากว่าง
- **ท่าที่ 2** เปิด **Scene Properties → Units** ตั้ง Unit System = `Metric`, Length = `Millimeters`, Unit Scale = `0.001`
- **ท่าที่ 3** ตรวจกริด (Overlay → Grid) ให้เห็นช่วงงาน ~10–100 mm และเปิด Overlay → Measurements ใน Edit Mode เพื่ออ่านความยาวขอบ

> **ทำไมใส่ Unit Scale 0.001** เพราะคู่มือ Blender ใช้ค่านี้แปลงหน่วยภายในกับตัวเลขบน UI ให้พิมพ์ `80` แล้วได้ระดับมิลลิเมตรตรงกับความคิดแบบวิศวกรรม — ทั้งทีมต้องใช้สูตรหน่วยเดียวกัน มิเช่นนั้นตอน export Twin ในโมดูล 4 จะสเกลเพี้ยนคนละไฟล์

---

## ตัวอย่างสมบูรณ์ (2) — PCB placeholder และ enclosure block

- **ท่าที่ 4 สร้าง PCB placeholder** `Add → Mesh → Cube` → ตั้ง Dimensions เช่น X=80 mm, Y=55 mm, Z=1.6 mm (หรือค่าที่วัดจริง) → ตั้งชื่อ `PCB_placeholder` → `Set Origin → Origin to Geometry` → `Ctrl+A → Apply Scale`
- **ท่าที่ 5 สร้าง enclosure block** `Add → Mesh → Cube` ชื่อ `Enclosure_block` → ตั้ง Dimensions ตามสูตรกล่องนอก → Origin to Geometry · Apply Scale → จัดตำแหน่งให้ PCB อยู่กลางช่องว่างภายใน (ดูจาก Wireframe)

หลัง Apply Scale ค่า Scale ในแผง Item ควรเป็น `1, 1, 1` ขณะที่ Dimensions ยังเป็นขนาดจริง — ยังไม่ต้องเจาะช่องพอร์ตในบทเรียนนี้ แค่ block ที่ "หุ้มได้"

(ทางเลือก) ถ้ามีแบตเตอรี่หรือจอแสดงผล ให้สร้าง Cube เพิ่มตามขนาดคร่าว ๆ จาก datasheet แล้ววางตรวจว่าไม่ชน PCB

---

## Topology และนิสัยการตั้ง Origin

| ทำ | เลี่ยง |
|---|---|
| ใช้ Cube แล้วปรับ Dimensions | Subdivision ทับซ้อนโดยไม่จำเป็น |
| เก็บชิ้นส่วนแยก object (`PCB_…`, `Enclosure_…`) | รวมเป็นก้อนเดียวตั้งแต่แรก |
| Apply Scale หลังปรับขนาด | ปล่อย Scale เป็น 2.0, 0.5, … |
| วาง Origin กึ่งกลางฐานกล่อง แกนตั้งฉากกับพื้น | ตั้งชื่อ object กำกวมหรือเป็นภาษาไทย |

**Optimization ในระดับบทเรียนนี้** คืออย่าเพิ่ม polygon จนกว่าสเกลและ clearance จะถูกล็อก — ถ้าใช้ Cube ตันเป็น block ยังไม่ต้องกังวลเรื่อง manifold ของเปลือกกลวง (จะสำคัญตอน export STL ในโมดูล 6)

---

## บทเรียนนี้ส่งต่อให้โมดูลถัดไปอย่างไร

| สิ่งที่ทำไว้ในบทเรียนนี้ | ใช้ต่อในโมดูล |
|---|---|
| Block ถูกสเกล + checklist | โมดูล 2 ขึ้นรูปละเอียด / PBR |
| ชิ้นส่วนแยกฝา–ฐานในใจแล้ว | โมดูล 3 animation เปิด–ปิด |
| Origin / หน่วยทีม | โมดูล 4 GLB → Bitstream Studio |
| Clearance ที่จดไว้ | โมดูล 5 validation · โมดูล 6 พิมพ์และ fitment |

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

---

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ: กล่องหุ้มแบบ block ตามสเกลฮาร์ดแวร์](../l02-lab/README.md) (~90–120 นาที)

- ตั้งฉาก Metric + Millimeters ตามสูตรทีม
- สร้าง PCB placeholder ตามขนาดที่วัดหรือขนาดแล็บ (80 × 55 × 1.6 mm)
- สร้าง enclosure block ที่หุ้ม PCB ได้โดยมี clearance ตามบทเรียนนี้
- Apply Scale · ตั้งชื่อ object · บันทึก `.blend` + สกรีนช็อต
- กรอก [scale-and-block-checklist.md](resources/scale-and-block-checklist.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
