---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — แล็บ: ขัดเกลาโมเดล วัสดุ PBR และเรนเดอร์"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
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

# บทเรียน 2.2 — แล็บ: ขัดเกลาโมเดล วัสดุ PBR และเรนเดอร์

## ล็อกสเกล เพิ่มความหนาผนัง เจาะช่องอย่างน้อยสองจุด แยกฝา/ฐาน ใส่วัสดุ PBR สองชนิด แล้วเรนเดอร์

**โมดูล 2 — การขึ้นรูป วัสดุ และการเรนเดอร์** · Hands-on ~3.5–4 ชั่วโมง

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

- พัฒนาไฟล์จากบทเรียน 1.2 ให้มีช่องเปิดอย่างน้อย **2** จุด
- แยก **ฝา** กับ **ฐาน** เป็นคนละ object
- ใส่วัสดุ PBR อย่างน้อย **2** ชนิด
- เรนเดอร์ภาพนำเสนออย่างน้อย **1** ภาพ (แนะนำ 2: beauty + technical)
- กรอก [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md)

---

## ก่อนเริ่ม

- [ ] มี `m01_block_enclosure.blend` (หรือเทียบเท่า) จากแล็บบทเรียน 1.2
- [ ] หน่วยยังเป็น Metric + mm ตามสูตรทีม · PCB placeholder ยังอยู่ในฉาก
- [ ] คัดลอกไฟล์เป็น `m02_enclosure_detail.blend` ก่อนแก้ — เก็บต้นฉบับบทเรียน 1 ไว้

---

## ฝึกเติม/แล็บ (1) — ล็อกสเกลแล้วเพิ่มผนัง

**ท่าที่ 1 — Lock scale, then thicken (บังคับ)**

1. เปิดไฟล์ · ตรวจ Dimensions ของ `PCB_placeholder` ยังตรง checklist บทเรียน 1
2. `Ctrl+A` → Scale บน enclosure
3. ทำให้ผนังหนาประมาณ **2 mm** (Solidify หรือเจาะโพรงตามบทเรียน 2.1)
4. Wireframe: PCB ยังอยู่ภายในและไม่ชนผนัง

**ผ่านเมื่อ:** ความหนาผนังชัด และสเกล PCB ไม่เปลี่ยนโดยไม่ตั้งใจ

---

## ฝึกเติม/แล็บ (2) — เจาะช่องอย่างน้อยสองจุด

**ท่าที่ 2 — Cut at least two openings (บังคับ)**

1. สร้าง cutter สำหรับช่องที่ 1 (เช่น USB)
2. Boolean **Difference** บน enclosure
3. ทำช่องที่ 2 (เซ็นเซอร์ / LED / ปุ่ม)
4. ตรวจขนาดช่องเผื่อ connector ตามแนวทางบทเรียน 1
5. Apply Boolean เมื่อพอใจ · ตั้งชื่อ object ให้สื่อความหมาย

**ผ่านเมื่อ:** มองเห็นช่อง ≥ 2 จากมุมนอกกล้อง

---

## ฝึกเติม/แล็บ (3) — Bevel และแยกฝา/ฐาน

**ท่าที่ 3 — Bevel and split lid/base (บังคับ)**

1. มนขอบนอกที่มือจับ (Bevel ≈ 0.5–1.5 mm)
2. แยกเป็น `Enclosure_base` และ `Enclosure_lid`
3. จัด Origin ของฝาที่ขอบบานพับหรือกึ่งกลางขอบหลัง (เตรียมหมุนในโมดูล 3)

**ผ่านเมื่อ:** Outliner มีอย่างน้อย 2 object ของกล่อง และเลื่อนฝาแยกจากฐานได้

---

## ฝึกเติม/แล็บ (4) — วัสดุ PBR สองชนิด

**ท่าที่ 4 — Two PBR materials (บังคับ)**

1. สร้าง `Plastic_matte_body` ตามค่าเริ่มต้นในบทเรียน (หรือเทียบเท่า)
2. สร้างวัสดุที่ 2 (ยาง / โลหะ / ปุ่ม)
3. Assign ให้ชิ้นส่วนที่เกี่ยวข้อง
4. จดค่า Base Color / Roughness / Metallic ใน look-dev sheet

**ผ่านเมื่อ:** Material ≥ 2 และมองเห็นความต่างของผิวใน Material Preview หรือ Rendered viewport

---

## ฝึกเติม/แล็บ (5) — แสง กล้อง เรนเดอร์

**ท่าที่ 5 — Lights, camera, render (บังคับ)**

1. เลือก EEVEE (หรือ Cycles ถ้าเครื่องไหว)
2. ตั้งไฟแบบ three-point **หรือ** World + Area หนึ่งดวง
3. จัดกล้อง three-quarter ที่เห็นพอร์ต
4. Render ≥ 1 ภาพ ความละเอียดอย่างน้อย 1280×720 (แนะนำ 1920×1080)
5. บันทึก PNG เช่น `m02_beauty.png` (แนะนำเพิ่ม `m02_ports.png` มุมเทคนิค)

**ผ่านเมื่อ:** มีไฟล์ภาพในโฟลเดอร์โปรเจกต์และ sheet กรอกครบ

---

## ผลงานที่ต้องส่ง

- [ ] `m02_enclosure_detail.blend`
- [ ] ช่องเปิด ≥ 2 · ฝา/ฐานแยก
- [ ] วัสดุ ≥ 2
- [ ] PNG render ≥ 1
- [ ] [material-lighting-sheet.md](../l01-modeling-materials-render/resources/material-lighting-sheet.md) กรอกครบ

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| Boolean รูเพี้ยน / ไม่เจาะ | Apply Scale · ลอง Solver Exact · ตรวจ cutter ทับผนังจริง |
| PCB ใส่ไม่ลงหลัง Solidify | ผนังหนาเข้าด้านในเกินไป — ขยายกล่องหรือ offset ออกนอก |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
