---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.2 — แล็บ Capstone: แพ็กเกจต้นแบบและ Design Report"
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

# บทเรียน 6.2 — แล็บ Capstone: แพ็กเกจต้นแบบและ Design Report

## แก้ตามผลโมดูล 5 ตรวจ mesh ส่งออก STL พิมพ์หรือทำแผนพิมพ์ ตรวจ fitment ทดสอบร่วมเฟิร์มแวร์/Twin และส่ง Design Report

**โมดูล 6 — การทำต้นแบบและโครงงานปิดหลักสูตร (Capstone)** · ~3 ชั่วโมง + เวลาพิมพ์/ประกอบแยกต่างหาก

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

ส่งแพ็กเกจปิดหลักสูตรให้ครบไฟล์ รายงาน และหลักฐาน fitment/ทดสอบ

---

## ก่อนเริ่ม

- [ ] โมดูล 5 ตัดสิน Ready หรือมีแผนแก้ที่ทำแล้ว
- [ ] มี `.blend` + `.glb` ล่าสุด
- [ ] โฟลเดอร์ผลงาน เช่น `course3-final/`

---

## ฝึกเติม/แล็บ (1) — แก้ตามผลโมดูล 5

**ท่าที่ 1 — Apply M05 fixes (บังคับ)** เปิด Top 3 จากโมดูล 5 → แก้ใน Blender ตามลำดับความสำคัญ → Save `.blend` สุดท้าย → export `.glb` ใหม่ถ้าโมเดล Twin เปลี่ยน

**ผ่านเมื่อ:** รายงานระบุว่าแก้ข้อไหนแล้ว / ข้อไหนยังค้าง

---

## ฝึกเติม/แล็บ (2) — ตรวจ mesh และส่งออก STL

**ท่าที่ 2 — Mesh check and export STL (บังคับ)** เปิด 3D Print Toolbox → Check All บนชิ้นที่จะพิมพ์ → แก้ non-manifold จนตรวจผ่าน → Export STL อย่างน้อย 1 ชิ้น → เปิดใน slicer ตรวจหน่วยเป็น mm

**ผ่านเมื่อ:** มีไฟล์ STL พร้อมสกรีนช็อต slicer หรือ Check All ที่ผ่าน

---

## ฝึกเติม/แล็บ (3) — พิมพ์หรือแผนพิมพ์

**ท่าที่ 3 — Print or print plan (บังคับ)**

| แทร็ก | ทำอะไร |
|---|---|
| **มีเครื่องพิมพ์** | พิมพ์อย่างน้อยหนึ่งชิ้น · ถ่ายรูปชิ้นงาน |
| **ไม่มีเครื่องพิมพ์** | ระบุบริการ/เครื่อง · วัสดุ · เวลาที่คาด · หลักฐานวัดเทียบบอร์ดกับโมเดล |

**ผ่านเมื่อ:** มีรูปพิมพ์ **หรือ** แผนพิมพ์ที่ตรวจสอบได้

---

## ฝึกเติม/แล็บ (4) — fitment กับฮาร์ดแวร์

**ท่าที่ 4 — Fitment with hardware (บังคับ)** ใส่/เทียบ PCB กับฐาน → ตรวจพอร์ต ช่องเซ็นเซอร์ ฝา → ถ่ายรูปอย่างน้อย 2 มุม → จดผล Pass/Fail ทีละข้อลง Design Report ข้อ 7

**ผ่านเมื่อ:** มีตาราง fitment ที่กรอกจริง

---

## ฝึกเติม/แล็บ (5) — ทดสอบระบบและรายงานปิดหลักสูตร

**ท่าที่ 5 — Firmware / Twin / web-app check (บังคับ)** เลือกอย่างน้อยหนึ่งหลักฐาน: LED/ปุ่มทำงานในกล่อง · Telemetry ใน Bitstream Studio · web-app หลังประกอบ

**ท่าที่ 6 — Design report package (บังคับ)** กรอก [design-report-template.md](../l01-prototyping-final-project/resources/design-report-template.md) ครบ → แนบรายการไฟล์ข้อ 9 → ข้อเสนอแนะรอบถัดไป ≥ 3 ข้อ → แนบหรือสรุป checklist โมดูล 5 → ตรวจไม่มีรหัสผ่านในไฟล์ส่ง

**ผ่านเมื่อ:** รายงานระบุผล "เซ็นเซอร์ยังอ่านได้ / อ่านได้แต่เพี้ยน / ยังทดสอบไม่ได้เพราะ…"

---

## ผลงานที่ต้องส่ง (แพ็กเกจปิดหลักสูตร)

| รายการ | ส่งแล้ว? |
|---|---|
| `.blend` | |
| `.glb` | |
| STL (≥1) | |
| Design report | |
| Checklist โมดูล 5 | |
| รูป/หลักฐาน fitment | |
| บันทึกเฟิร์มแวร์/Twin/web-app | |

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| Slicer บอก mesh พัง | 3D Print Toolbox · Make Manifold · ตรวจ normals |
| PCB ใส่ไม่ลง | กลับ Top 3 จากโมดูล 5 · อย่าตะไบโดยไม่จดในรายงาน |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
