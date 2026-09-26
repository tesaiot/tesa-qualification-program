---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — สี่รูปแบบการนำหลักสูตรไปใช้"
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

# บทเรียน 1.1 — สี่รูปแบบการนำหลักสูตรไปใช้

## เลือกรูปแบบการนำ TESA Open Knowledge ไปใช้ในสถาบันของคุณ พร้อมแผนเวลาสำหรับช่วงสอน 1.5 และ 3 ชั่วโมง

**โมดูล 1 — นำไปใช้และเทียบมาตรฐาน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เลือกรูปแบบการนำไปใช้ที่เหมาะกับบริบทของคุณ พร้อมเหตุผล
2. จัดบทเรียนลงในช่วงสอน 1.5 หรือ 3 ชั่วโมงได้
3. ออกแบบโครงสร้างที่ช่วยให้ผู้เรียนเรียนจบ

## ก่อนเริ่ม

รายวิชาของคุณตอนนี้มีหัวข้อไมโครคอนโทรลเลอร์ IoT หรือ Edge AI อยู่แล้วหรือยัง ถ้ามี อยู่ในสัปดาห์ไหน และสถาบันของคุณมีบอร์ดพัฒนาอยู่กี่ชุด ผู้เรียนต่อห้องกี่คน

---

## ดูของจริงก่อน

เปิดหน้าหลักสูตร AIoT in Action และ Explorer ดูสองอย่าง

1. บทเรียนแต่ละบทบอกเวลาเป็นนาทีแยกช่วง (`time_min`)
2. ทุกบทมีเป้าหมาย เช็กความเข้าใจ และบางบทมีไฟล์ฝึกกับเฉลย

สิ่งที่คุณได้จาก TESA Open Knowledge คือ **ชิ้นส่วนที่ต่อกันได้** ไม่ใช่รายวิชาสำเร็จรูปที่ต้องสอนตามทั้งก้อน

---

## แนวคิด (1) — สี่รูปแบบ

| รูปแบบ | เหมาะเมื่อ | สิ่งที่ต้องเตรียม |
|---|---|---|
| **วิชาเลือกเต็ม** | เปิดวิชาใหม่ได้ และมีบอร์ดพอสำหรับแล็บ | ตารางเทียบผลลัพธ์ทั้งวิชา การประเมินครบ แผนฮาร์ดแวร์ |
| **แทรกโมดูลในวิชาเดิม** | ปรับรายวิชาใหญ่ไม่ได้ แต่อยากให้เนื้อหาทันสมัย | เทียบว่าโมดูลแทนหัวข้อไหน และใช้ชั่วโมงเท่าเดิมไหม |
| **ห้องเรียนกลับด้าน (flipped)** | ชั่วโมงแล็บน้อย บอร์ดมีจำกัด | กำหนดส่งเช็กความเข้าใจก่อนชั่วโมงแล็บ |
| **สอนร่วมกับ TESA** | เริ่มต้นใหม่ ผู้สอนยังไม่คุ้นกับบอร์ด | ติดต่อ TESA ล่วงหน้า ตกลงบทบาทและการประเมิน |

ไม่มีรูปแบบไหนดีที่สุด ส่วนมากสถาบันเริ่มจาก "แทรกโมดูล" หนึ่งภาคการศึกษา เก็บข้อมูลว่าได้ผลแค่ไหน แล้วค่อยขยายเป็นวิชาเลือกเต็ม

---

## แนวคิด (2) — หน่วยของการวางแผนคือบทเรียน ไม่ใช่หลักสูตร

บทเรียนแต่ละบทใช้เวลา 20–75 นาที และบอกเวลาแยกเป็นช่วง แนวคิด ฝึก แล็บ และเช็ก คุณจึงจัดบทเรียนลงช่วงสอนได้เหมือนต่อบล็อก หลักที่ใช้คือ **แต่ละช่วงกิจกรรมยาวไม่เกิน 6–10 นาที** ยกเว้นแล็บ แล้วสลับรูปแบบกิจกรรม เพราะความสนใจของผู้เรียนลดลงเร็วเมื่อฟังยาว ๆ

แม่แบบแผนเวลาสำหรับช่วงสอน 1.5 และ 3 ชั่วโมงอยู่ที่ [resources/slot-plans.md](resources/slot-plans.md)

---

## แนวคิด (3) — เรียนเองล้วนมักไม่จบ

ข้อมูลจากคอร์สออนไลน์แบบเปิดของ MIT และ Harvard บน edX ปี 2017–18 รายงานว่าผู้ลงทะเบียนเรียนจบเพียงราวสามเปอร์เซ็นต์ (Reich & Ruipérez-Valiente 2019, *Science*) และการทดลองขนาดใหญ่พบว่าการกระตุ้นแบบเบา ๆ เช่น ส่งข้อความเตือนหรือให้วางแผน ช่วยได้น้อยเมื่อขยายขนาด (Kizilcec et al. 2020, *PNAS*)

สิ่งที่ช่วยได้คือ **โครงสร้าง** เรียนเป็นรุ่นพร้อมกัน มีกำหนดส่ง มีผู้สอนตอบคำถาม และมีหลักฐานการเรียนจบ ถ้าให้ผู้เรียนใช้ TESA Open Knowledge นอกห้องเรียน ให้วางกำหนดส่งรายบทเรียน และวัดการเรียนจบรายบท ไม่ใช่รายหลักสูตร

---

## ตัวอย่างสมบูรณ์

อาจารย์คนหนึ่งสอนวิชาไมโครคอนโทรลเลอร์ 15 สัปดาห์ สัปดาห์ละ 3 ชั่วโมง ต้องการเพิ่มเรื่อง IoT โดยไม่ขยายวิชา

- **ท่าที่ 1 เลือกรูปแบบ** แทรกโมดูล ใช้โมดูล IoT ของ AIoT in Action แทนหัวข้อการสื่อสารอนุกรมแบบเดิมสามสัปดาห์
- **ท่าที่ 2 เทียบเวลา** รวม `time_min` ของบทเรียนในโมดูลนั้น เทียบกับ 9 ชั่วโมงที่มี ส่วนที่เกินให้เป็นงานก่อนเข้าห้องแบบ flipped
- **ท่าที่ 3 วางโครงสร้าง** เช็กความเข้าใจท้ายบทต้องส่งก่อนชั่วโมงแล็บ แล็บทำเป็นกลุ่มบนบอร์ด ส่งหลักฐานลง portfolio
- **ท่าที่ 4 เขียนเอกสาร** เพิ่มแถวในตารางเทียบผลลัพธ์การเรียนรู้ (บทเรียน 1.2) และใส่ข้อความอ้างอิง TESA ในเอกสารรายละเอียดรายวิชา (บทเรียน 1.3)

---

## ฝึกเติม

เลือกรายวิชาหนึ่งของคุณ แล้วเติมตาราง

| คำถาม | คำตอบของคุณ |
|---|---|
| รูปแบบที่เลือก และเหตุผลสองข้อ | |
| หลักสูตรหรือโมดูลที่จะใช้ | |
| ชั่วโมงที่มี เทียบกับผลรวม `time_min` | |
| โครงสร้างที่ช่วยให้เรียนจบ (กำหนดส่ง รุ่น ผู้ตอบคำถาม) | |

จากนั้นเลือกบทเรียนหนึ่งบท แล้ววางลงแม่แบบใน [resources/slot-plans.md](resources/slot-plans.md)

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

แหล่งที่เป็นต้นแบบของชุดสำหรับผู้สอนนี้ ได้แก่ Arm Education Kits และคู่มือผู้สอนของ Microsoft IoT for Beginners ซึ่งเล่าการใช้แบบ flipped ไว้ด้วย

**สะท้อนคิด** ถ้าเริ่มภาคการศึกษาหน้า ข้อจำกัดที่ใหญ่ที่สุดของคุณคือเวลา บอร์ด หรือความคุ้นเคยของผู้สอน และรูปแบบที่เลือกแก้ข้อจำกัดนั้นหรือเลี่ยงมัน

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
