---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — ออกแบบการประเมิน"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 2.2 — ออกแบบการประเมิน

## แยกสื่อฝึกที่เปิดสาธารณะออกจากงานที่ใช้ให้คะแนน ผูกทุกการประเมินกับเป้าหมายของบทเรียน ใช้ rubric แบบจุดเดียว และรับมือกับเฉลยสาธารณะและเครื่องมือ AI

**โมดูล 2 — สอนและประเมิน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แยกสื่อฝึกสาธารณะออกจากงานให้คะแนน
2. เขียน rubric แบบจุดเดียวที่ผูกกับเป้าหมายทุกข้อ
3. ออกแบบงานให้คะแนนที่ยังวัดความสามารถจริงได้ในยุคที่เฉลยเปิดและมีเครื่องมือ AI

## ก่อนเริ่ม

จากบทที่แล้ว เทคนิคสองอย่างที่ได้คะแนนประโยชน์สูงในการทบทวนของ Dunlosky และคณะคืออะไร — ในรายวิชาของคุณตอนนี้ เฉลยของแบบฝึกเปิดให้ผู้เรียนดูได้ไหม และคุณรู้สึกอย่างไรกับเรื่องนั้น

---

## ดูของจริงก่อน

เปิดไฟล์ quiz.yaml ของบทเรียนโปรแกรมแรก ทุกข้อมีช่อง `objective` ที่ชี้กลับไปยังเป้าหมายของบทเรียน และเปิดไฟล์เฉลยของแบบฝึกซึ่งเปิดให้ทุกคนดู

คลังนี้ตั้งใจเปิดแบบฝึกและเฉลย เพราะมันเป็น **สื่อการเรียน** ไม่ใช่ **ข้อสอบ**

---

## แนวคิด (1) — สามกลุ่มของสื่อประเมิน

| กลุ่ม | ตัวอย่าง | ใครเข้าถึง |
|---|---|---|
| **สื่อฝึกสาธารณะ** | เช็กความเข้าใจ ไฟล์ฝึกและเฉลย แล็บ ตัวอย่าง rubric | ทุกคน อยู่ในคลังนี้ ใช้เพื่อการเรียน ไม่ใช่เพื่อให้คะแนนตัดสิน |
| **งานให้คะแนนในรายวิชา** | โจทย์แล็บหลายชุดสำหรับสุ่ม เกณฑ์ให้คะแนนละเอียด โจทย์ capstone | TESA จัดให้ผู้สอนเมื่อขอ ไม่เผยแพร่สาธารณะ ติดต่อ contact@tesa.or.th |
| **คลังข้อสอบของการสอบ TQP** | ข้อสอบจริง พารามิเตอร์โจทย์รายคน test vector ลับ | ไม่มีใครนอกหน่วยรับรอง รวมถึงผู้สอน |

ข้อสำคัญ **อย่าใช้เช็กความเข้าใจในคลังเป็นข้อสอบให้คะแนน** เพราะคำตอบเปิดอยู่แล้ว ใช้เป็นแบบฝึกและเกณฑ์ผ่านรายบท (80%) ก็พอ

---

## แนวคิด (2) — ทุกการประเมินผูกกับเป้าหมาย

ตามหลัก constructive alignment ในบทตารางเทียบ ทุกเป้าหมายต้องมีการวัดคู่กัน และการวัดต้องวัดสิ่งที่เป้าหมายพูดถึงจริง ถ้าเป้าหมายใช้กริยา "สั่งหลอดให้กะพริบ" การวัดต้องดูหลอดกะพริบ ไม่ใช่ถามนิยามของ GPIO

## แนวคิด (3) — Rubric แบบจุดเดียว

Rubric แบบจุดเดียวเขียนเฉพาะเกณฑ์ผ่านของแต่ละเป้าหมาย แล้วให้ผู้ประเมินเขียนหลักฐานว่าต่ำกว่าหรือเกินตรงไหน เขียนง่าย อ่านง่าย และใช้กับแล็บที่แต่ละกลุ่มทำไม่เหมือนกันได้ แม่แบบอยู่ที่ [resources/lab-rubric-template.md](resources/lab-rubric-template.md)

---

## แนวคิด (4) — เมื่อเฉลยเปิดและมีเครื่องมือ AI

แบบฝึกเติมช่องว่างที่มีเฉลยสาธารณะ ใครก็คัดลอกได้ และเครื่องมือ AI เขียนโค้ดสั้น ๆ ได้ในไม่กี่วินาที การประเมินที่ยังวัดความสามารถจริงได้มักมีลักษณะเหล่านี้

- **ทำบนบอร์ดต่อหน้าผู้ประเมิน** และพารามิเตอร์ต่างกันรายกลุ่ม เช่น จำนวนรอบ จังหวะ หรือเกณฑ์ที่สุ่มให้
- **ให้อธิบายและแก้ต่อหน้า** ขอให้เปลี่ยนเงื่อนไขหนึ่งข้อแล้วแก้ทันที คนที่เข้าใจจะแก้ได้ คนที่คัดลอกมาจะติด
- **ประเมินกระบวนการ** คำทำนายก่อนรัน log การดีบัก และบันทึกว่าลองอะไรแล้วไม่ได้ผล
- **หาจุดเสีย** ให้โค้ดที่มีบั๊กที่ตั้งใจใส่ไว้ แล้วให้หาและอธิบาย

นโยบายเรื่องเครื่องมือ AI เป็นของแต่ละสถาบัน บอกผู้เรียนให้ชัดตั้งแต่ต้นว่าใช้ได้แค่ไหน และให้ระบุเมื่อใช้

---

## ตัวอย่างสมบูรณ์

งานให้คะแนนสำหรับบท "อ่านเซนเซอร์แล้วดูค่าเปลี่ยน" ที่ทนต่อเฉลยสาธารณะ

- **ท่าที่ 1** แต่ละกลุ่มจับสลากเกณฑ์ `LIMIT` และเงื่อนไขเพิ่ม เช่น "ไฟต้องกะพริบเมื่อเอียง ไม่ใช่ติดค้าง"
- **ท่าที่ 2** ทำบนบอร์ดในห้อง 30 นาที ส่งไฟล์และคลิปสั้น
- **ท่าที่ 3** ผู้ประเมินขอให้เปลี่ยนเกณฑ์ต่อหน้า แล้วให้อธิบายว่าทำไมต้องดัก `OSError`
- **ท่าที่ 4** ให้คะแนนด้วย rubric แบบจุดเดียวที่มีแถวครบทุกเป้าหมายของบทเรียน

---

## ฝึกเติม

1. คัดลอก [resources/lab-rubric-template.md](resources/lab-rubric-template.md) แล้วเขียน rubric ของแล็บหนึ่งแล็บในรายวิชาของคุณ
2. ออกแบบงานให้คะแนนหนึ่งชิ้นที่ใช้อย่างน้อยสองลักษณะจากแนวคิดข้อ 4

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

ถ้าต้องการงานให้คะแนนชุดที่ TESA เตรียมไว้สำหรับหลักสูตรใด ให้ติดต่อ TESA พร้อมระบุชื่อสถาบัน รายวิชา และหลักสูตรที่ใช้ TESA จะไม่ส่งเนื้อหาของการสอบ TQP ให้ใคร และผู้สอนไม่เป็นผู้สอบผู้เรียนของตนในการสอบ TQP ตามกติกาความเป็นกลาง

**สะท้อนคิด** งานให้คะแนนชิ้นไหนในรายวิชาของคุณตอนนี้ที่เครื่องมือ AI ทำแทนผู้เรียนได้ทั้งหมด จะเปลี่ยนมันอย่างไรโดยไม่เพิ่มภาระตรวจจนเกินไป

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
