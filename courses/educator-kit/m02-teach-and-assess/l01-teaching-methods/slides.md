---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — วิธีสอนที่ได้ผลกับการเขียนโปรแกรมระบบฝังตัว"
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

# บทเรียน 2.1 — วิธีสอนที่ได้ผลกับการเขียนโปรแกรมระบบฝังตัว

## ใช้ PRIMM ตัวอย่างที่มีป้ายขั้นตอน ไฟล์ฝึกที่ตัวช่วยค่อย ๆ ลดลง แบบฝึก Parsons การทดสอบย้อนหลังแบบเว้นระยะ และการแบ่งงานอีมูเลเตอร์/บอร์ดจริง

**โมดูล 2 — สอนและประเมิน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จัดกิจกรรมรอบตัวอย่างหนึ่งไฟล์ตาม PRIMM
2. ออกแบบไฟล์ฝึกที่ตัวช่วยลดลงตามลำดับ และแปลงเป็นแบบฝึก Parsons
3. แบ่งงานระหว่างอีมูเลเตอร์กับบอร์ดจริง
4. อธิบายงานวิจัยที่รองรับได้

## ก่อนเริ่ม

จากบทที่แล้ว ข้อความอ้างอิงแบบไหนที่ต้องใส่ในสไลด์ทุกหน้า — ในรายวิชาของคุณ ผู้เรียนเห็นโค้ดที่ทำงานได้ครั้งแรกในนาทีที่เท่าไรของชั่วโมงแรก

---

## ดูของจริงก่อน

เปิดบทเรียน "โปรแกรมแรก" และ "อ่านเซนเซอร์" ของ Explorer แล้วสังเกตสามอย่าง

- ส่วน "ดูของจริงก่อน" ให้ **ทำนายก่อนรัน**
- ส่วน "ตัวอย่างสมบูรณ์" มีป้าย **ท่าที่ 1, 2, 3**
- ไฟล์ฝึกบทแรกมีช่องว่าง 2 จุด บทถัดมามี 4 จุด

สามอย่างนี้ไม่ได้เกิดโดยบังเอิญ แต่ละอย่างมีงานวิจัยรองรับ

---

## แนวคิด (1) — PRIMM และตัวอย่างมีป้ายขั้นตอน

**PRIMM** (Predict, Run, Investigate, Modify, Make) จัดกิจกรรมรอบโค้ดตัวอย่างเป็นห้าขั้น: ทำนายผลก่อนรัน รันเพื่อเทียบ สืบว่าแต่ละส่วนทำอะไร แก้โค้ดเดิม แล้วจึงสร้างของใหม่ งานวิจัยของ Sentance, Waite และ Kallia (2019) รายงานว่าผู้เรียนกลุ่มที่ใช้ PRIMM ทำคะแนนได้ดีกว่ากลุ่มควบคุม แนวนี้เข้ากับหลักคิด "เริ่มจากของที่ทำงานได้ แล้วค่อยแกะ" ที่หลักสูตรใน TESA Open Knowledge ใช้

ตัวอย่างที่ติดป้ายเป้าหมายย่อย (subgoal label) เช่น "ท่าที่ 1 เลือกหลอด" ช่วยให้มือใหม่เรียนการแก้ปัญหาด้วยโปรแกรมได้ดีขึ้น (Morrison, Margulieux & Guzdial 2015) — ทุกตัวอย่างสมบูรณ์ในคลังจึงมีป้ายท่าที่เสมอ

---

## แนวคิด (2) — ตัวช่วยค่อย ๆ ลดลง และแบบฝึก Parsons

เริ่มจากตัวอย่างเต็ม แล้วค่อยเว้นว่างมากขึ้นจนผู้เรียนเขียนเองทั้งไฟล์ในงานปลายทาง (backward fading, Renkl & Atkinson 2003; Renkl, Atkinson & Große 2004) เหตุผลอีกข้อคือ **expertise reversal** ตัวช่วยที่มากเกินไปจะกลับเป็นภาระเมื่อผู้เรียนเก่งขึ้น (Kalyuga et al. 2003) แนวปฏิบัติในคลัง: หนึ่งโมดูลไปจาก ตัวอย่างเต็ม → ราว 2 ช่องว่าง → ราว 6 ช่องว่าง → ไฟล์เปล่าในงาน capstone

แบบฝึก **Parsons** ให้ผู้เรียนเรียงบรรทัดโค้ดที่ให้มาให้ถูกลำดับ ได้ผลการเรียนรู้ใกล้เคียงกับการเขียนเองแต่ใช้เวลาน้อยกว่า (Ericson, Margulieux & Rick 2017) เหมาะกับผู้เรียนที่ยังไม่มีบอร์ด ใน `quiz.yaml` ใช้ `type: order` สร้างได้ทันที

---

## แนวคิด (3) — ทดสอบย้อนหลังแบบเว้นระยะ และเรียนเป็นรุ่น

การฝึกตอบคำถาม (practice testing) กับการเว้นระยะทบทวน (distributed practice) เป็นสองเทคนิคที่ได้คะแนนประโยชน์สูงสุดในการทบทวนงานวิจัยเทคนิคการเรียนสิบวิธี (Dunlosky et al. 2013) จึงให้ทุกบทมีเช็กความเข้าใจ 3–5 ข้อ และให้ส่วน "ก่อนเริ่ม" ถามทวนบทก่อนเสมอ

การเรียนแบบ mastery ช่วยผลสัมฤทธิ์ได้จริงในภาพรวม แต่โปรแกรมแบบเรียนเองตามจังหวะตัวเองมักมีอัตราเรียนจบลดลง (Kulik, Kulik & Bangert-Drowns 1990) จึงใช้เกณฑ์ผ่านรายบท (80%) คู่กับการเรียนเป็นรุ่นที่มีกำหนดส่ง

---

## แนวคิด (4) — อีมูเลเตอร์สำหรับแนวคิด บอร์ดจริงสำหรับดีบักและการวัด

การทบทวนงานวิจัยเรื่องแล็บเสมือนและแล็บทางไกลเทียบกับแล็บลงมือจริง พบว่าส่วนใหญ่รายงานผลเท่ากันหรือดีกว่า (Brinson 2015) แต่ทักษะบางอย่างต้องเกิดบนบอร์ดจริง

| ใช้อีมูเลเตอร์ | ใช้บอร์ดจริง |
|---|---|
| ทำความเข้าใจแนวคิดและ API | ดีบักเมื่อผลบนบอร์ดต่างจากอีมูเลเตอร์ |
| ฝึกเติมไฟล์ฝึกและวนแก้เร็ว ๆ | วัดค่าจริงด้วยเครื่องมือวัด |
| ออกแบบหน้าจอ | เครือข่ายจริง พลังงาน และจังหวะเวลา |
| ผู้เรียนที่ยังไม่ได้คิวบอร์ด | แล็บปลายโมดูลและ capstone |

---

## ตัวอย่างสมบูรณ์

ใช้ตัวอย่าง `02_blink.py` ของ Explorer จัดตาม PRIMM

- **ท่าที่ 1 Predict (3 นาที)** อ่านค่า `ROUNDS` `ON_MS` `OFF_MS` แล้วเขียนคำทำนาย
- **ท่าที่ 2 Run (3 นาที)** รันในอีมูเลเตอร์ เทียบกับคำทำนาย
- **ท่าที่ 3 Investigate (8 นาที)** ถามว่า "ถ้าลบ `led.off()` บรรทัดสุดท้ายจะเกิดอะไร" "ทำไมต้อง `str()`"
- **ท่าที่ 4 Modify (8 นาที)** เปลี่ยนจังหวะเป็นติดสั้นดับยาว
- **ท่าที่ 5 Make (15 นาที)** เขียนไฟกะพริบรหัสมอร์สเอง บนบอร์ดถ้ามีคิว

---

## ฝึกเติม

เลือกโมดูลหนึ่งในรายวิชาของคุณ แล้ววางแผนไฟล์ฝึกสามไฟล์

| ไฟล์ | ตัวช่วย | ช่องว่างกี่จุด | มีแบบ Parsons ไหม |
|---|---|---|---|
| บทที่ 1 | ตัวอย่างเต็ม ให้แก้ค่าเดียว | 0–1 | |
| บทที่ 2 | | ราว 2 | |
| บทที่ 3 | | ราว 6 | |

จากนั้นเขียนแบบฝึก Parsons หนึ่งข้อในรูป `quiz.yaml` (`type: order`) จากไฟล์บทที่ 2

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

แหล่งอ่านเพิ่มสำหรับผู้สอน: Carpentries Instructor Training มีบทเรื่องการสอนแบบ live coding และการให้ผลป้อนกลับที่ใช้ได้ดีกับห้องปฏิบัติการ

**สะท้อนคิด** วิธีไหนในบทนี้ที่คุณใช้อยู่แล้วโดยไม่ได้ตั้งชื่อ และวิธีไหนที่ลองได้ตั้งแต่สัปดาห์หน้า

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
