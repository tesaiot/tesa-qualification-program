---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.1 — ไฟล์ผลิต ต้นแบบ fitment และ Design Report"
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

# บทเรียน 6.1 — ไฟล์ผลิต ต้นแบบ fitment และ Design Report

## ตรวจ mesh และส่งออก STL ทางเลือกเมื่อยังพิมพ์ไม่ได้ ตรวจ fitment กับบอร์ดจริง ทดสอบร่วมเฟิร์มแวร์ และเขียน Design Report

**โมดูล 6 — การทำต้นแบบและโครงงานปิดหลักสูตร (Capstone)**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. ตรวจ mesh ด้วย 3D Print Toolbox (manifold, normals, scale) แล้วส่งออก STL แยกฝาและฐาน
2. ตรวจ fitment กับบอร์ดจริงตามรายการ (PCB, พอร์ต, ช่องเซ็นเซอร์, ฝา, การยึด, สาย)
3. เขียน Design Report ที่ทำซ้ำได้ ครบหัวข้อบังคับ และมีข้อเสนอแนะรอบถัดไปอย่างน้อยสามข้อ

> **คาถาประจำบทเรียน**
> โมดูลนี้คือ *ปิดวงจากแนวคิดถึงของจับต้องได้* — ไฟล์ครบโดยไม่มีหลักฐานประกอบ/ทดสอบ ยังไม่นับว่าจบหลักสูตร

---

## ผลงานปิดหลักสูตรที่ต้องส่ง

| ผลงาน | บังคับ? | หมายเหตุ |
|---|---|---|
| Project `.blend` | ใช่ | เวอร์ชันสุดท้ายหลังแก้จากโมดูล 5 |
| Twin-ready `.glb` | ใช่ | จากโมดูล 4/5 |
| Print file **STL** (≥ 1 ชิ้น) | ใช่ | ฝาและ/หรือฐาน — แยกไฟล์ถ้าพิมพ์แยก |
| [Design report](resources/design-report-template.md) | ใช่ | กรอกครบทุกหัวข้อหลัก |
| [Pre-prototype checklist โมดูล 5](../../m05-digital-validation/l01-scenario-digital-validation/resources/pre-prototype-checklist.md) | ใช่ | แนบหรือสรุปในรายงาน |
| รูป/คลิป fitment | แนะนำอย่างยิ่ง | บอร์ดในกล่อง · พอร์ต · เซ็นเซอร์ |

```text
Concept (M1) → Detail + PBR (M2) → Motion (M3) → GLB/Twin (M4) → Validate (M5) → Print + Report (M6)
```

---

## ตัวอย่างสมบูรณ์ (1) — ตรวจ mesh และส่งออก STL

**ท่าที่ 1 — ตรวจ mesh ด้วย 3D Print Toolbox** `Edit → Preferences → Add-ons` เปิดใช้ 3D Print Toolbox → กด `N` แท็บ 3D-Print → เลือกชิ้นส่วน → **Check All** → แก้ปัญหาที่รายงาน โดยเฉพาะ Non-manifold → ใช้ Make Manifold เป็นจุดเริ่มแล้วตรวจซ้ำด้วยตา (เสริม: `Ctrl+A` Scale · Merge by Distance · `Shift+N` Recalculate Normals)

**ท่าที่ 2 — Export STL** แยก object ที่จะพิมพ์ (`Enclosure_base`, `Enclosure_lid`) → `File → Export → STL` → เปิด Selection Only · Apply Modifiers → ตั้งชื่อชัด เช่น `enclosure_base.stl` → นำเข้า slicer ตรวจขนาด mm อีกครั้งก่อนพิมพ์

ผนังยังควรประมาณ **≥ 2 mm** ตามแนวทาง enclosure พิมพ์ 3D

---

## ถ้ายังพิมพ์ไม่ได้ในตอนนี้

ยังส่ง STL + รายงานได้ โดยระบุใน Design Report

- แผนเครื่องพิมพ์/บริการที่จะใช้
- วัสดุที่ตั้งใจ (เช่น PLA)
- สิ่งที่จะตรวจตอนได้ชิ้นจริง

อย่าปล่อยช่อง fitment ว่าง — ใช้การประกอบจำลองกับบอร์ด + กล่องกระดาษ/พลาสติกชั่วคราว หรือวัดช่องจากโมเดลเทียบบอร์ดจริงแล้วถ่ายรูปหลักฐาน

---

## ตัวอย่างสมบูรณ์ (2) — Fitment กับบอร์ดจริง

**ท่าที่ 3 — ตรวจ fitment**

| ตรวจ | ผ่านเมื่อ |
|---|---|
| PCB เข้าโดยไม่ต้องงัด | ไม่ต้องงัดแรงจนเสี่ยงหักขา |
| พอร์ตตรงแนว | เสียบได้หรือมองเห็นชัดว่าจะเสียบได้ |
| ช่องเซ็นเซอร์ตรงแนว | ตรงชิป/ช่องระบายตามที่ออกแบบ |
| ฝาปิดได้พอดี | ไม่หลวมจนหลุดง่าย และไม่ต้องเคาะแรง |
| จุดยึด/สกรู (ถ้ามี) | ใส่สกรูหรือแผนยึดได้ตามดีไซน์ |

**ท่าที่ 4 — ถ่ายภาพหลักฐาน** ชิ้นพิมพ์หรือ STL ใน slicer · บอร์ดวางในฐาน · ฝาประกอบ/ช่องพอร์ต · (แนะนำ) เครื่องทำงานในกล่อง

---

## ทดสอบร่วมเฟิร์มแวร์และ Edge AI

หลังใส่บอร์ดในกล่อง (หรือวางเทียบ)

| ทดสอบ | วิธี | หลักฐาน |
|---|---|---|
| Power / LED / ปุ่ม | เฟิร์มแวร์พื้นฐานยังตอบ | รูปหรือคลิปสั้น |
| เซ็นเซอร์ยังอ่านได้ | ไม่ถูกกล่องบังจนค่าตาย | Studio หรือ web-app |
| Twin ยังใช้ได้ | เปิด GLB คู่กับของจริง | สกรีนช็อต |

จดว่าเซ็นเซอร์ในกล่อง**ยังอ่านได้หรือถูกลดทอน** — นี่คือบทเรียนสำคัญของ enclosure จริง

---

## Design Report — หัวข้อบังคับ

คัดลอกแล้วกรอก [design-report-template.md](resources/design-report-template.md)

1. ข้อมูลโครงงาน
2. วัตถุประสงค์การออกแบบ
3. สรุป Concept → Final
4. สเกลและวัสดุ
5. Twin integration
6. Digital validation และปัญหาที่พบ (ดึงจากโมดูล 5)
7. ผลการทดสอบ Prototype / Fitment
8. ข้อเสนอแนะรอบถัดไป **อย่างน้อย 3 ข้อ**
9. ภาคผนวกไฟล์

> รายงานที่ดีอ่านแล้วทำซ้ำได้ — ไม่ใช่แค่คำสวยโดยไม่มีตัวเลขสเกลหรือชื่อไฟล์

---

## เกณฑ์ผ่านขั้นต่ำ

| เกณฑ์ | บังคับ |
|---|---|
| `.blend` + `.glb` + STL (≥1) | ใช่ |
| Design report ครบ | ใช่ |
| แนบหรือสรุป checklist โมดูล 5 | ใช่ |
| พูดถึงสเกล/หน่วยอย่างตรงไปตรงมา | ใช่ |
| Fitment หรือแผนพิมพ์ที่ชัดเจน + หลักฐานการวัด | ใช่ |
| พิจารณาเฟิร์มแวร์/Twin/web-app ในการทดสอบ | ใช่ |
| ข้อเสนอแนะรอบถัดไป ≥ 3 ข้อ | ใช่ |
| ไม่มีรหัสผ่านในไฟล์ที่ส่ง | ใช่ |

---

## เช็กความเข้าใจ / ไปต่อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ Capstone: แพ็กเกจต้นแบบและ Design Report](../l02-lab/README.md) (~3 ชั่วโมง + เวลาพิมพ์/ประกอบแยกต่างหาก) — ส่งแพ็กเกจปิดหลักสูตรให้ครบไฟล์ รายงาน และหลักฐาน fitment/ทดสอบ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
