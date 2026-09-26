---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.3 — อ้างอิง TESA ในรายวิชาของคุณ"
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

# บทเรียน 1.3 — อ้างอิง TESA ในรายวิชาของคุณ

## ใส่ข้อความอ้างอิง TESA ให้ครบทุกจุดที่ใช้สื่อ รู้ว่าเมื่อไรต้องเติม (ดัดแปลง) และห้ามอ้างว่ารายวิชาได้รับการรับรองจาก TESA

**โมดูล 1 — นำไปใช้และเทียบมาตรฐาน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เขียนข้อความอ้างอิง TESA ลงเอกสารรายละเอียดรายวิชาได้ครบ
2. ใส่เครดิตในสไลด์ เอกสารแจก และหน้า LMS ได้ถูกรูปแบบ
3. รู้ว่าเมื่อไรต้องเติม (ดัดแปลง)
4. ไม่เขียนสิ่งที่ทำให้เข้าใจว่า TESA รับรองรายวิชา

## ก่อนเริ่ม

จากบทที่แล้ว ตารางเทียบของคุณใช้บทเรียนใดบ้าง บทเหล่านั้นอยู่ในหลักสูตรไหน — ในรายวิชาของคุณตอนนี้ สื่อที่ยืมมาจากที่อื่นมีการอ้างอิงไว้ที่ไหนบ้าง

---

## ดูของจริงก่อน

เปิดไฟล์ ATTRIBUTION.md ที่รากของคลังความรู้ ดูหัวข้อ "ข้อความที่ต้องใช้" และ "ตัวอย่างการใช้จริง" แล้วเปิดท้ายหน้าหลักสูตรใดก็ได้ เช่น Explorer จะเห็นหัวข้อ "อ้างอิง TESA" ที่เติมชื่อหลักสูตรไว้ให้แล้ว ทุกหลักสูตรในคลังมีหัวข้อนี้ คุณคัดลอกไปใช้ได้ทันที

---

## แนวคิด (1) — ทำไมต้องอ้างอิง

เนื้อหาใน TESA Open Knowledge ใช้สัญญาอนุญาต **CC BY-NC 4.0** (ไม่ใช่เพื่อการค้า) และ TESA ให้คำอนุญาตเพิ่มแก่สถาบันการศึกษา สถาบันของคุณจึงนำไปสอน ดัดแปลง และใช้ในรายวิชาที่เก็บค่าเล่าเรียนตามปกติได้ การใช้เชิงพาณิชย์อื่นต้องขออนุญาต TESA ก่อน เงื่อนไขที่ต้องทำทุกครั้งคือต้องอ้างอิงที่มาในแบบที่เจ้าของงานกำหนด — ข้อความที่ ATTRIBUTION.md กำหนดไว้ใช้ทุกที่ในทุกสื่อ:

> "«ชื่อบทเรียนหรือหลักสูตร»" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
> (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

การอ้างอิงเป็นเรื่องจริยธรรมทางวิชาการด้วย ผู้เรียนเห็นผู้สอนให้เครดิตแหล่งที่มาอย่างถูกต้อง ก็เรียนรู้ที่จะทำแบบเดียวกัน (นี่คือเหตุผลที่ตารางเทียบในบทที่แล้วจัดเรื่องนี้ไว้ในด้านจริยธรรม)

---

## แนวคิด (2) — ต้องอยู่ตรงไหนบ้าง

| ที่ | ใส่อะไร |
|---|---|
| **เอกสารรายละเอียดรายวิชา** (มคอ.3 หรือแบบฟอร์มที่สถาบันใช้แทน) | ข้อความเต็ม หนึ่งรายการต่อหนึ่งหลักสูตรหรือบทเรียนที่ใช้ พร้อมหมายเหตุว่ารายวิชาไม่ได้รับการรับรองจาก TESA หรือ Infineon |
| **สไลด์ทุกหน้าที่นำมาใช้หรือดัดแปลง** | บรรทัดเครดิตสั้นใน footer และข้อความเต็มในหน้าปกหรือหน้าสุดท้าย |
| **เอกสารแจกและใบงาน** | บรรทัดเครดิตสั้นท้ายทุกหน้า และข้อความเต็มพร้อม URL เต็มในหน้าแรกหรือหน้าสุดท้าย |
| **หน้า LMS** | ข้อความเต็มท้ายหน้าบทเรียนหรือหน้าแรกของรายวิชา |

บรรทัดเครดิตสั้น: `TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0` — ข้อความพร้อมวางทุกแบบอยู่ที่ [resources/syllabus-attribution.md](resources/syllabus-attribution.md)

---

## แนวคิด (3) — เมื่อไรต้องเติม (ดัดแปลง)

ถ้าคุณ **ตัด เพิ่ม แปล หรือเรียบเรียงใหม่** ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง และถ้าทำได้ ให้บอกสั้น ๆ ว่าเปลี่ยนอะไร เช่น "(ดัดแปลง: ตัดแล็บออก และเปลี่ยนตัวอย่างเป็นบอร์ดของรายวิชา)"

การเปลี่ยนแม่แบบสไลด์ให้เป็นของคณะโดยไม่แตะเนื้อหาก็นับเป็นการดัดแปลงรูปแบบ ใส่ไว้จะปลอดภัยกว่า

ถ้าหลักสูตรที่ใช้มีต้นทางจากผู้เขียนอื่น (ท้ายหน้าหลักสูตรจะบอกไว้) ต้องคงเครดิตต้นทางนั้นด้วย เช่นหลักสูตรที่ดัดแปลงจาก AIoT in Action ของ AIC

---

## แนวคิด (4) — อ้างอิงไม่เท่ากับได้รับการรับรอง

CC BY-NC 4.0 ไม่อนุญาตให้สื่อว่าเจ้าของงานรับรองหรือสนับสนุนงานของผู้ใช้ และชื่อ TESA, TQP และ "Certified by TESA and Infineon" เป็นเครื่องหมาย ไม่ได้อยู่ใต้สัญญาอนุญาต CC

- **เขียนได้** "รายวิชานี้ใช้สื่อเปิดจาก TESA Open Knowledge" พร้อมข้อความอ้างอิง
- **เขียนไม่ได้** "หลักสูตรที่ TESA รับรอง" "หลักสูตรเตรียมสอบ TQP" หรือใช้โลโก้ TESA และ TQP บนเอกสารรายวิชา **เว้นแต่** รายวิชานั้นผ่านการเทียบกับ TQP ผ่าน TESA และได้รับอนุญาตเป็นลายลักษณ์อักษรแล้ว

การรับรองของ TQP เป็นของบุคคลที่สอบผ่าน ไม่ใช่ของรายวิชา

---

## ตัวอย่างสมบูรณ์

อาจารย์ใช้โมดูลแรกของ Explorer ในสองสัปดาห์แรกของวิชาไมโครคอนโทรลเลอร์ แปลงสไลด์เป็นแม่แบบของคณะ และตัดบทเรียนที่ 3 ออก

- **ท่าที่ 1 เอกสารรายวิชา** วางข้อความแบบ "กรณีดัดแปลง" ลงหมวดสื่อประกอบการสอน ต่อด้วยเครดิตต้นทาง AIoT in Action ที่ท้ายหน้าหลักสูตร Explorer เพราะโค้ดตัวอย่างมาจากที่นั่น
- **ท่าที่ 2 สไลด์** คง footer เดิม เติมรหัสวิชาไว้ข้างหน้าในบรรทัดเดียวกัน และใส่ข้อความเต็มในหน้าสุดท้าย
- **ท่าที่ 3 LMS** วางข้อความเต็มท้ายหน้าของสองสัปดาห์นั้น
- **ท่าที่ 4 ตรวจคำ** ค้นเอกสารทั้งหมดว่าไม่มีคำว่า "รับรองโดย TESA" หรือ "เตรียมสอบ TQP"

---

## ฝึกเติม / เช็กความเข้าใจ

1. เปิด [resources/syllabus-attribution.md](resources/syllabus-attribution.md) แล้วเติมข้อความอ้างอิงสำหรับรายวิชาของคุณให้ครบทั้งสี่ที่
2. เขียนหมายเหตุ "(ดัดแปลง: ...)" ที่ตรงกับสิ่งที่คุณเปลี่ยนจริง ไม่เกินหนึ่งบรรทัด

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

ถ้าสถาบันของคุณอยากเทียบรายวิชากับ TQP ให้ติดต่อ TESA ผ่านช่องทางที่ระบุใน ATTRIBUTION.md และอย่าเขียนข้อความเรื่องการรับรองใด ๆ จนกว่าจะได้รับอนุญาตเป็นลายลักษณ์อักษร

**สะท้อนคิด** ถ้าผู้เรียนของคุณนำงานในรายวิชาไปเผยแพร่ใน portfolio สาธารณะ คุณจะสอนให้เขาอ้างอิงทั้ง TESA และตัวคุณอย่างไร

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
