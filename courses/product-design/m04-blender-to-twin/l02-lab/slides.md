---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — แล็บ: ส่งออก GLB และนำเข้า Twin"
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

# บทเรียน 4.2 — แล็บ: ส่งออก GLB และนำเข้า Twin

## เตรียมไฟล์ ส่งออก .glb นำเข้า Twin host ทำเครื่องหมายจุดเซ็นเซอร์/โต้ตอบ แล้วทดสอบด้วยคลิปหรือข้อมูล

**โมดูล 4 — จาก Blender สู่ Digital Twin** · Hands-on ~2.5–3 ชั่วโมง

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

- ได้ไฟล์ **`.glb`** จากโมเดลโมดูล 2/3
- นำเข้า Bitstream Studio แล้วขนาด/แนวแกนใช้งานได้
- กำหนดจุด sensor หรือ interaction อย่างน้อย **1** จุดพร้อมชื่อ
- ทดสอบอย่างน้อย: วางโมเดล + (คลิปแอนิเมชัน **หรือ** telemetry)
- กรอก [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md)

---

## ก่อนเริ่ม

- [ ] ไฟล์จากโมดูล 3 (หรือโมดูล 2 ถ้ายังไม่มีคลิป — แจ้งใน checklist)
- [ ] Bitstream Studio พร้อมใช้
- [ ] คัดลอกงานเป็น `m04_enclosure_twin.blend` ก่อน export

---

## ฝึกเติม/แล็บ (1) — เตรียมไฟล์ก่อน export

**ท่าที่ 1 — Prepare for export (บังคับ)**

1. Apply Scale บนชิ้นที่จะส่ง
2. ตรวจชื่อ object และชื่อคลิป (`lid_open` ฯลฯ)
3. ถ้ามีหลาย Action: Stash ลง NLA
4. ซ่อน/ลบ cutter และของที่ไม่ต้องการส่ง แล้ว Save `.blend`

**ผ่านเมื่อ:** เล่นคลิปใน Blender ยังถูก และ Scale เป็น 1,1,1

---

## ฝึกเติม/แล็บ (2) — ส่งออก `.glb`

**ท่าที่ 2 — Export `.glb` (บังคับ)** `File → Export → glTF 2.0` → เลือก glTF Binary (.glb) → เปิด Apply Modifiers · Materials · Animations (ถ้ามี) → Export เป็น `enclosure_twin.glb`

**ผ่านเมื่อ:** มีไฟล์ `.glb` และขนาดไม่เป็น 0 byte

---

## ฝึกเติม/แล็บ (3) — นำเข้าและทำเครื่องหมายจุด

**ท่าที่ 3 — Import into Twin host (บังคับ)** เปิด Bitstream Studio → นำเข้า `enclosure_twin.glb` → ตรวจ: มองเห็น · สเกลใช้ได้ · แนวแกนวางบนพื้นได้ → เล่น `lid_open` ถ้ามีคลิป → แคปหน้าจอ

**ท่าที่ 4 — Mark sensor / interaction point (บังคับ)**

1. เลือกอย่างน้อย 1 จุด (เช่น `sensor_bmi270_slot` หรือ `interact_lid`)
2. บันทึก: ชื่อ · อยู่ตรงไหนบนกล่อง · ผูกกับอะไร
3. แคปหรือวาดประกอบใน checklist

**ผ่านเมื่อ:** คนอื่นในทีมอ่านชื่อแล้วชี้จุดบนโมเดลถูก

---

## ฝึกเติม/แล็บ (4) — ทดสอบด้วยข้อมูลหรือการเคลื่อนไหว

**ท่าที่ 5 — Data or motion test (แนะนำ — ส่วนหนึ่งของผลงานที่ครบ)** เลือกอย่างน้อยหนึ่ง

| ทางเลือก | ทำอะไร |
|---|---|
| **เล่นคลิป** | เล่นแอนิเมชันใน Twin ให้ครบรอบเปิด (และปิดถ้ามี) |
| **Telemetry** | Link Simulator หรือ Board แล้วให้มีสตรีมขณะโมเดลอยู่บนจอ |

**ผ่านเมื่อ:** มีหลักฐานไฟล์ภาพ/คลิปในโฟลเดอร์ผลงาน

---

## ผลงานที่ต้องส่ง

- [ ] `enclosure_twin.glb` (+ `.blend` ต้นทาง)
- [ ] สกรีนช็อตใน Bitstream Studio
- [ ] จุด sensor/interaction ≥ 1
- [ ] ผลทดสอบข้อมูล/การเคลื่อนไหว
- [ ] [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md) กรอกครบ

---

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| โมเดลยักษ์หรือจิ๋วใน Twin | ตรวจ Unit Scale ทีม · Apply Scale · export ใหม่ — อย่าแก้แค่ซูมแล้วจบ |
| ไม่มีแอนิเมชันใน GLB | Stash Action · เปิด Animations ตอน export |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
