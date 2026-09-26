---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — ตารางเทียบผลลัพธ์การเรียนรู้ (Curriculum Crosswalk)"
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

# บทเรียน 1.2 — ตารางเทียบผลลัพธ์การเรียนรู้ (Curriculum Crosswalk)

## เทียบบทเรียนแต่ละบทกับผลลัพธ์การเรียนรู้ของรายวิชา ด้าน K/S/E/C การประเมิน ชั่วโมง หน่วยสมรรถนะ TPQI และคุณลักษณะบัณฑิต WA

**โมดูล 1 — นำไปใช้และเทียบมาตรฐาน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เขียน CLO ที่วัดผลได้ พร้อมระดับ Bloom
2. จัด CLO ลงด้าน K/S/E/C ตามมาตรฐานคุณวุฒิ 2565
3. เติมตารางเทียบรายบทเรียนให้ครบทุกคอลัมน์

## ก่อนเริ่ม

จากบทที่แล้ว คุณเลือกรูปแบบการนำไปใช้แบบไหน และใช้บทเรียนใดบ้าง — ผลลัพธ์การเรียนรู้ของรายวิชาคุณตอนนี้เขียนด้วยกริยาอะไร "เข้าใจ" "รู้" หรือกริยาที่วัดได้

---

## ดูของจริงก่อน

เปิดหน้าบทเรียน "โปรแกรมแรก: เขียนบนจอและเปิดไฟ" ของ Explorer ดูส่วนหัว (front matter) ของไฟล์ คุณจะเห็น `objectives` ที่เขียนเป็นกริยาวัดผลได้ `develops` ที่บอก skill id และระดับ `time_min` ที่บอกเวลา และ `quiz.yaml` ที่มีข้อสอบผูกกับเป้าหมายทุกข้อ

ข้อมูลเหล่านี้ย้ายลงตารางเทียบของคุณได้เกือบทั้งหมด งานของคุณคือเชื่อมมันกับเอกสารของรายวิชาและกรอบมาตรฐาน

---

## แนวคิด (1) — เขียนผลลัพธ์ก่อน แล้วค่อยออกแบบการประเมิน

หลัก **constructive alignment** ให้ผลลัพธ์ การประเมิน และกิจกรรมการเรียนรู้ ชี้ไปทางเดียวกัน (Biggs 1996) และใช้ **Bloom ฉบับปรับปรุง** เลือกกริยาที่วัดได้ (Krathwohl 2002)

| แบบที่วัดไม่ได้ | แบบที่วัดได้ (กริยา + เงื่อนไข + เกณฑ์) | Bloom |
|---|---|---|
| เข้าใจ GPIO | สั่งหลอด LED กะพริบตามจำนวนรอบที่กำหนดด้วย `gpio.led().on()/off()` บนบอร์ดหรืออีมูเลเตอร์ โดยจบที่สถานะดับทุกครั้ง | ประยุกต์ (apply) |
| รู้จัก MQTT | อธิบายบทบาทของ broker, topic, publish และ subscribe ด้วยแผนภาพ ถูกครบทั้งสี่คำ | เข้าใจ (understand) |
| รู้เรื่องความปลอดภัย | เปรียบเทียบความเสี่ยงของ broker สาธารณะพอร์ต 1883 กับ MQTTs และเลือกทางที่เหมาะสมพร้อมเหตุผล | วิเคราะห์/ประเมิน |

---

## แนวคิด (2) — ผลลัพธ์สี่ด้านตามมาตรฐานคุณวุฒิ 2565

ประกาศคณะกรรมการมาตรฐานการอุดมศึกษา เรื่อง รายละเอียดผลลัพธ์การเรียนรู้ตามมาตรฐานคุณวุฒิระดับอุดมศึกษา พ.ศ. 2565 (ราชกิจจานุเบกษา เล่ม 139 ตอนพิเศษ 212 ง วันที่ 9 กันยายน 2565 ใช้บังคับตั้งแต่ 27 กันยายน 2565) กำหนดให้ผลลัพธ์การเรียนรู้ประกอบด้วยอย่างน้อยสี่ด้าน

- **K — ความรู้ (Knowledge)**
- **S — ทักษะ (Skills)**
- **E — จริยธรรม (Ethics)**
- **C — ลักษณะบุคคล (Character)**

บทเรียนด้านระบบฝังตัวส่วนใหญ่เสริมด้าน K และ S เป็นหลัก ส่วน E และ C มาจากกิจกรรมอย่างการอ้างอิงแหล่งที่มาให้ถูก การไม่ใส่รหัสผ่านในงานที่เผยแพร่ การทำงานเป็นทีมในแล็บ และ portfolio ที่ซื่อตรงต่อสิ่งที่ทำจริง

---

## แนวคิด (3) — สองกรอบภายนอกที่มักถูกถาม

- **TPQI** คุณวุฒิวิชาชีพ "นักพัฒนาระบบสมองกลฝังตัว ระดับ 4" มีสองหน่วยสมรรถนะ คือ ICT-CSOS-107B (พัฒนาฮาร์ดแวร์) และ ICT-FYNH-108B (พัฒนาซอฟต์แวร์) — ใส่เฉพาะบทเรียนที่เกี่ยวข้องจริง บทเรียนระดับ L1–L2 มักยังไม่ถึงเกณฑ์ แต่เป็นฐานของมัน
- **TABEE** การรับรองหลักสูตรวิศวกรรมของสภาวิศวกรใช้เกณฑ์คุณลักษณะบัณฑิตตาม Washington Accord (สภาวิศวกรอยู่ในรายชื่อ provisional signatory) กำหนดไว้ใน IEA Graduate Attributes and Professional Competencies ฉบับ 2021 มี 11 ข้อ WA1–WA11

แผนที่ทักษะของ TESA ใช้ระดับ L1–L5 ที่ตัวเลขตรงกับระดับคุณวุฒิวิชาชีพ ดูรายละเอียดที่ tqp/levels.md

---

## ตัวอย่างสมบูรณ์

สามแถวตัวอย่าง (ใช้บทเรียนที่มีอยู่จริงในคลัง)

| บทเรียน | CLO + Bloom | K/S/E/C | การประเมิน | WA |
|---|---|---|---|---|
| `explore.m01.l03` | สั่งหลอด LED กะพริบตามจำนวนรอบที่กำหนด และจบที่สถานะดับ (ประยุกต์) | S | quiz.yaml + ไฟล์ฝึก | WA5 |
| `explore.m02.l02` | อธิบายบทบาทของ broker, topic, publish, subscribe ด้วยแผนภาพ (เข้าใจ) | K | แผนภาพใน portfolio + quiz.yaml | WA1 |
| `explore.m02.l03` | อ้างอิงแหล่งที่มาของสื่อที่นำมาดัดแปลงได้ถูกต้องตามสัญญาอนุญาต (ประยุกต์) | E | ข้อความอ้างอิงในงานที่ส่ง | WA7 |

- **ท่าที่ 1** คัดลอก `objectives` และ `develops` จากหน้าบทเรียน
- **ท่าที่ 2** เขียน CLO ของรายวิชาที่บทเรียนนั้นรับใช้
- **ท่าที่ 3** เลือกด้าน K/S/E/C ที่เด่นที่สุด ไม่ต้องใส่ทุกด้านทุกแถว
- **ท่าที่ 4** ใส่หน่วย TPQI และ WA เฉพาะที่อธิบายได้ว่าเกี่ยวจริง

---

## ฝึกเติม / เช็กความเข้าใจ

คัดลอก [resources/crosswalk-template.md](resources/crosswalk-template.md) แล้วเติมอย่างน้อยสามแถวสำหรับรายวิชาของคุณ ใช้บทเรียนที่เลือกไว้ในบทที่แล้ว

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

ถ้าสถาบันของคุณกำลังเตรียมรับการประเมินจาก TABEE ตารางนี้ใช้เป็นหลักฐานประกอบได้ แต่คำตัดสินว่าหลักฐานเพียงพอหรือไม่เป็นของผู้ประเมิน และรูปแบบเอกสารรายละเอียดรายวิชาที่แต่ละสถาบันใช้อาจต่างกัน ให้ตรวจกับหน่วยงานวิชาการของสถาบัน

**สะท้อนคิด** CLO ข้อไหนของรายวิชาคุณที่ยังไม่มีบทเรียนหรือการประเมินรองรับเลย ช่องว่างนั้นควรเติมด้วยอะไร

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
