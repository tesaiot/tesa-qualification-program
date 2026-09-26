---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ"
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

# บทเรียน 5.2 — แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ

## เขียนสถานการณ์ก่อนคลิก รันและจดปัญหา ผูกข้อมูลหรือบันทึกช่องว่าง แล้วกรอก checklist ก่อนทำต้นแบบ

**โมดูล 5 — สถานการณ์ใช้งานและการตรวจสอบเชิงดิจิทัล** · Hands-on ~2.5–3 ชั่วโมง

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

- รัน usage scenario อย่างน้อย **2** รายการบน Twin
- จดปัญหาหรือจุดเฝ้าระวังอย่างน้อย **3** ข้อ
- (แนะนำ) จับคู่สถานะเฟิร์มแวร์/telemetry อย่างน้อย 1 อย่าง หรืออธิบายว่าทำไมยังไม่ผูก
- กรอก [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) รวม **Top 3 fixes**

---

## ก่อนเริ่ม

- [ ] มี `.glb` ใน Bitstream Studio จากแล็บโมดูล 4
- [ ] มีคลิปเปิดฝา หรือระบุว่าใช้มุมกล้องแทนชั่วคราว
- [ ] โฟลเดอร์หลักฐาน `lab-notes/` หรือเทียบเท่า

---

## ฝึกเติม/แล็บ (1) — เขียนสถานการณ์ก่อนคลิก

**ท่าที่ 1 — Write scenarios before you click (บังคับ)** เลือกอย่างน้อย 2 สถานการณ์จากบทเรียน 5.1 — **ต้องมี S3 (เปิดฝาบริการ)** และอีกหนึ่งข้อ เขียนลงตาราง: ใครทำอะไร → ผลที่คาดหวัง

**ผ่านเมื่อ:** เพื่อนอ่านตารางแล้วรันซ้ำได้โดยไม่ถามเพิ่ม

---

## ฝึกเติม/แล็บ (2) — รันสถานการณ์และจดปัญหา

**ท่าที่ 2 — Run scenarios and log issues (บังคับ)** ทำตาม action → จด expected vs actual → แคปหน้าจออย่างน้อย 1 ภาพต่อสถานการณ์ → สะสมรายการปัญหา (เป้าหมายรวม ≥ 3 ข้อ)

**ผ่านเมื่อ:** มีบันทึกครบ 2 สถานการณ์และปัญหา ≥ 3 ข้อ

---

## ฝึกเติม/แล็บ (3) — ผูกข้อมูลหรือบันทึกช่องว่าง

**ท่าที่ 3 — Bind data or document the gap (บังคับ)** เลือกหนึ่งทาง

| ทางเลือก | ทำอะไร |
|---|---|
| Link ข้อมูล | Simulator/Board แล้วเปิด web-app คู่กับ Twin |
| ผูกใน Studio | สี/คลิป/ไฮไลต์กับ event หรือโหมด |
| ยังผูกไม่ได้ | เขียนเหตุผล + แผนในโมดูล 6 ลง checklist |

**ผ่านเมื่อ:** มีหลักฐานภาพ **หรือ** เหตุผลที่เขียนชัดใน checklist

---

## ฝึกเติม/แล็บ (4) — กรอก checklist ก่อนต้นแบบ

**ท่าที่ 4 — Fill pre-prototype checklist (บังคับ)**

1. กรอกทุกแถวหลักใน [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md)
2. เขียน **Top 3 design fixes before print**
3. ตัดสินใจ: Ready to print / Not ready (ระบุ blockers)

**ผ่านเมื่อ:** Top 3 ไม่ว่าง และมีคำตัดสิน Ready/Not ready

(ทางเลือก) เลือกปัญหา 1 ข้อจาก Top 3 → แก้ใน Blender → export GLB ใหม่ → import และรัน S3 ซ้ำสั้น ๆ → จดว่าดีขึ้นหรือยัง

---

## ผลงานที่ต้องส่ง

- [ ] 2 scenarios + screenshots
- [ ] ≥ 3 issues / watch-outs
- [ ] Pre-prototype checklist + Top 3 fixes
- [ ] หลักฐานการผูกข้อมูล หรือช่องว่างที่เขียนไว้
- [ ] (ถ้าแก้แล้ว) GLB ใหม่

---

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| ไม่รู้จะหาปัญหาอะไร | ใช้ตาราง Risk ในบทเรียน 5.1 · เปิด Wireframe ตอนเปิดฝา |
| ไม่มีสตรีมเซ็นเซอร์ | ใช้ทางเลือก C3 · หรือรันเฉพาะ S1–S3/S5 แล้วแผนผูกข้อมูลในโมดูล 6 |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
