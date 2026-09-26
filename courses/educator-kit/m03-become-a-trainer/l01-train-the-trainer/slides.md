---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — อบรมผู้สอนและเส้นทางสู่ TQP Certified Trainer"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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

# บทเรียน 3.1 — อบรมผู้สอนและเส้นทางสู่ TQP Certified Trainer

## เตรียมตัวเข้าเวิร์กช็อป train-the-trainer สองวัน วางแผนการสาธิตการสอน และรู้เงื่อนไขของใบรับรอง TQP Certified Trainer

**โมดูล 3 — เป็นผู้สอนที่ได้รับการรับรอง** · บทเรียนสุดท้ายของชุดนี้

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. รู้เงื่อนไขของ TQP Certified Trainer
2. วางแผนการสาธิตการสอน 20 นาที
3. เข้าใจกติกาความเป็นกลางเรื่องการสอบ

## ก่อนเริ่ม

จากบทที่แล้ว บทบาทสี่อย่างในกลุ่มที่มีบอร์ดตัวเดียวคืออะไร — ในบทเรียนที่คุณจะสอน ผู้เรียนเห็นของที่ทำงานได้ภายในนาทีที่เท่าไร

---

## ดูของจริงก่อน

เปิด tqp/certification.md ดูแถว **Trainer** ในตารางขั้นของใบรับรอง และหัวข้อ "ความเป็นกลาง" สองส่วนนี้คือกติกาทั้งหมดที่บทนี้อธิบาย ถ้าข้อความในบทนี้กับไฟล์นั้นไม่ตรงกัน ให้ยึดไฟล์นั้น

---

## แนวคิด (1) — TQP Certified Trainer คืออะไร

TQP Certified Trainer คือการรับรองว่าผู้ถือ **สอนหลักสูตรที่สอดคล้องกับ TQP ได้** ออกร่วมในนาม TESA × Infineon มีอายุ **2 ปี** และมีเงื่อนไขสามข้อ

1. **ถือใบรับรองระดับ L4 ในเรื่องที่สอน** ผู้สอนต้องทำได้ในระดับที่สูงกว่าที่ผู้เรียนต้องไปถึง
2. **ผ่านหลักสูตรการสอน** คือชุดสำหรับผู้สอนนี้ ร่วมกับเวิร์กช็อป train-the-trainer
3. **สาธิตการสอนให้กรรมการดู**

ใบรับรองของ TQP ทุกขั้นยังไม่เปิดรับผู้สมัครจนกว่าจะประกาศใน tqp/certification.md ตามแผนการเปิด หลักสูตรผู้สอนอยู่ในระยะที่ 2 ระหว่างนี้คุณเตรียมตัวได้ด้วยการเรียนชุดนี้ให้ครบ และสอนจริงด้วยรูปแบบที่เลือกไว้ในโมดูลแรก

---

## แนวคิด (2) — เวิร์กช็อป train-the-trainer สองวัน (โครงร่าง)

| ช่วง | วันที่ 1 | วันที่ 2 |
|---|---|---|
| เช้า | ทบทวนชุดสำหรับผู้สอน: รูปแบบการนำไปใช้ ตารางเทียบ การอ้างอิง TESA | ฝึกประเมิน: rubric แบบจุดเดียว งานให้คะแนนที่ทนต่อเฉลยสาธารณะ |
| บ่าย | ลงมือบนบอร์ดและอีมูเลเตอร์ในบทบาทผู้เรียน ครบทุกบทบาทในกลุ่ม | ฝึกสาธิตการสอนกับเพื่อนผู้สอน รับผลป้อนกลับ แล้วสาธิตรอบจริง |
| ปิดวัน | สะท้อนคิดว่าตรงไหนผู้เรียนของคุณจะติด | วางแผนภาคการศึกษาแรก และช่องทางแลกเปลี่ยนในชุมชนผู้สอน |

โครงร่างนี้เป็นแผนของชุดสำหรับผู้สอน รายละเอียดจริงของแต่ละรุ่นจะประกาศโดย TESA

---

## แนวคิด (3) — สาธิตการสอนที่ดีหน้าตาอย่างไร

การสาธิต 20 นาทีไม่ใช่การบรรยายสั้น แต่คือการแสดงว่าคุณจัดการเรียนรู้ได้ตามหลักในโมดูลที่สอง

- เปิดด้วยคำถามทวนบทก่อน (ไม่เกิน 2 นาที)
- ให้ผู้เรียนเห็นของที่ทำงานได้ และให้ทำนายก่อนรัน
- สอนแนวคิดเป็นช่วงสั้นไม่เกิน 6 นาที
- เดินตัวอย่างที่มีป้ายท่าที่ 1, 2, 3
- ปิดด้วยเช็กความเข้าใจที่ผูกกับเป้าหมาย และบอกว่าถ้าผู้เรียนตอบผิดข้อไหน คุณจะทำอะไรต่อ

---

## แนวคิด (4) — ความเป็นกลาง

การอบรมกับการรับรองต้องแยกกัน ตามกติกาใน tqp/certification.md

- **ผู้สอนไม่สอบคนที่ตนสอน ภายใน 2 ปี**
- **ไม่บังคับให้ผู้สมัครสอบต้องเรียนคอร์สของ TESA** เส้นทางอื่นที่เทียบเท่ายอมรับได้
- ผู้สอนไม่ได้รับเนื้อหาของการสอบ TQP และไม่ควรสัญญากับผู้เรียนว่าการเรียนกับตนจะทำให้สอบผ่าน
- รายวิชาของคุณไม่กลายเป็น "หลักสูตรที่ TESA รับรอง" เพราะคุณถือใบ Trainer

---

## ตัวอย่างสมบูรณ์

แผนสาธิต 20 นาที บทเรียน "อ่านเซนเซอร์แล้วดูค่าเปลี่ยน"

- **ท่าที่ 1 (0–2 นาที)** ถามทวน "ทำไมต้อง `str()` ก่อนส่งให้ Seg7"
- **ท่าที่ 2 (2–6 นาที)** เปิดอีมูเลเตอร์ ให้ทำนายว่าหมุนลูกบิดแล้วอะไรบนจอจะขยับ แล้วรัน
- **ท่าที่ 3 (6–11 นาที)** อธิบาย `sensors.snapshot()` และ "ถามก่อนหยิบ"
- **ท่าที่ 4 (11–16 นาที)** เดินตัวอย่างท่าที่ 1–5 และเล่าว่าบนบอร์ดจริงต่างจากอีมูเลเตอร์ตรงไหน
- **ท่าที่ 5 (16–20 นาที)** เช็กความเข้าใจสองข้อ และบอกว่าถ้าผู้เรียนตอบข้อ `OSError` ผิด จะพาไปดูอะไรต่อ

---

## ฝึกเติม / เช็กความเข้าใจ

เขียนแผนสาธิต 20 นาทีของบทเรียนที่คุณจะสอนจริง ในรูปแบบห้าท่าข้างบน แล้วซ้อมกับเพื่อนร่วมงานหนึ่งรอบ ขอผลป้อนกลับสองข้อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน และถือว่าจบชุดสำหรับผู้สอน

---

## ไปต่อ / สะท้อนคิด

กลับไปที่ catalog/tracks.yaml ดูเส้นทางผู้สอน และหลักสูตรที่คุณจะสอน แบ่งปันแผนการสอนของคุณกับชุมชนผ่าน GitHub Issues ของคลังนี้ อย่าลืมอ้างอิง TESA ในสิ่งที่ดัดแปลงจากคลัง

**สะท้อนคิด** ถ้าผู้เรียนของคุณไปสอบ TQP ในอีกหนึ่งปี อะไรที่คุณสอนแล้วเขาจะใช้ได้จริงในห้องสอบปฏิบัติ และอะไรที่คุณควรหยุดสอนเพราะไม่ได้ช่วยอะไร

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0
