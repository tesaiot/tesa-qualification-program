---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.3 — ต้นทุน BOM เวลา และทีม"
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

# บทเรียน 1.3 — ต้นทุน BOM เวลา และทีม

## แยกต้นทุนของผลิตภัณฑ์ IoT เป็นสามก้อน ประมาณต้นทุนต่อชิ้นจากตัวอย่างสมมติ และรู้ว่าต้องมีใครในทีม

**โมดูล 1 — เข้าใจทางเลือก**

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แยกต้นทุนเป็นสามก้อน คือครั้งเดียว ต่อชิ้น และต่อเนื่อง
2. คำนวณต้นทุนต่อชิ้นตลอดอายุการใช้งานจากตัวอย่างสมมติ
3. ระบุบทบาทในทีมที่ต้องมี

> **ข้อตกลงของบทนี้** เราไม่ใส่ราคาตลาดหรือสถิติตลาดใด ๆ เพราะราคาเปลี่ยนเร็วและต่างกันมากตามปริมาณและผู้ขาย ตัวเลขทุกตัวในตัวอย่างเป็น **ตัวเลขสมมติ** ตั้งขึ้นให้คำนวณง่าย ห้ามนำไปใช้เป็นราคาจริง ราคาจริงต้องขอใบเสนอราคาจากผู้ขายและผู้ผลิตรับจ้างเอง

---

## ก่อนเริ่ม / ดูของจริงก่อน

**ก่อนเริ่ม** จากบทที่แล้ว ต้นทุนของ edge กับ cloud ต่างกันอย่างไร และถ้ามีคนถามว่า "ทำอุปกรณ์นี้ราคาเท่าไร" คุณคิดว่าต้องถามอะไรกลับก่อนจะตอบได้

**ดูของจริงก่อน** เจ้าของกิจการหลายคนถามราคาชิ้นส่วนบนบอร์ด แล้วคูณด้วยจำนวนที่จะผลิต ได้ตัวเลขที่ดูน่าพอใจ แต่ตัวเลขนั้นมักเป็นแค่ส่วนเดียวของต้นทุนจริง ค่าพัฒนา ค่าทดสอบรับรอง ค่าคลาวด์ ค่าซิมการ์ด และค่าดูแลหลังขาย ไม่อยู่ในตัวเลขนั้นเลย

---

## แนวคิด (1) — ต้นทุนสามก้อน

| ก้อน | ภาษาอังกฤษ | ตัวอย่างรายการ |
|---|---|---|
| **ครั้งเดียว** | NRE | ออกแบบวงจร/PCB เขียนเฟิร์มแวร์ ทำแอป เก็บข้อมูล/ฝึกโมเดล แม่พิมพ์ตัวเครื่อง ค่าทดสอบรับรอง |
| **ต่อชิ้น** | BOM + assembly | ชิป/โมดูล เซนเซอร์ PCB ตัวเครื่อง แบตเตอรี่ ค่าประกอบ ค่าทดสอบสายการผลิต บรรจุภัณฑ์ |
| **ต่อเนื่อง** | recurring | ค่าคลาวด์ ค่าเชื่อมต่อ (ซิมการ์ด) ค่าอัปเดตความปลอดภัย ค่าซัพพอร์ต ค่ารับประกัน |

AI เพิ่มต้นทุนในก้อนครั้งเดียวมากที่สุด (เก็บข้อมูล ติดป้ายกำกับ ฝึก ทดสอบ) และเพิ่มก้อนต่อเนื่องด้วย (ดูแลโมเดลเมื่อหน้างานเปลี่ยน)

---

## แนวคิด (2) — ตัวอย่างสมมติ: เซนเซอร์เฝ้าตู้แช่

สมมติ: ต้นทุนครั้งเดียว (NRE) รวม **600,000 บาท** · ต้นทุนต่อชิ้น **900 บาท** · ต้นทุนต่อเนื่อง **120 บาท/เครื่อง/ปี** · ใช้งานเครื่องละ **3 ปี**

**ถ้าผลิต 1,000 เครื่อง** = 600,000/1,000 + 900 + (120×3) = 600 + 900 + 360 = **1,860 บาท**

**ถ้าผลิต 5,000 เครื่อง** = 600,000/5,000 + 900 + 360 = 120 + 900 + 360 = **1,380 บาท**

ข้อสังเกต: (1) ยิ่งผลิตมาก ต้นทุนครั้งเดียวถูกเฉลี่ยจนเหลือน้อย ต้นทุนต่อชิ้น/ต่อเนื่องจึงกลายเป็นก้อนใหญ่ (2) ต้นทุนต่อเนื่องสามปีในตัวอย่างนี้เกือบครึ่งของต้นทุนต่อชิ้น — ตั้งราคาขายโดยลืมก้อนนี้ ยิ่งขายมากยิ่งขาดทุน

---

## แนวคิด (3) — สี่ช่วงเวลาที่ไม่ควรข้าม

1. **พิสูจน์แนวคิด (proof of concept)** ใช้บอร์ดพัฒนา ตอบคำถามเดียวว่า "วัดได้และตัดสินใจได้จริงไหม"
2. **ต้นแบบ (prototype)** ใกล้ของจริงขึ้น เริ่มคิดเรื่องตัวเครื่อง พลังงาน และความปลอดภัย
3. **นำร่อง (pilot)** ติดตั้งหน้างานจริงจำนวนน้อย เก็บข้อมูล และเรียนรู้ว่าอะไรพัง
4. **ผลิต (production)** ทดสอบรับรองมาตรฐาน เตรียมสายการผลิตและการดูแลหลังขาย

ช่วงที่คนประเมินเวลาต่ำเกินจริงบ่อยที่สุด: การเก็บข้อมูลหน้างานสำหรับ AI และการทดสอบรับรองมาตรฐาน — ถามระยะเวลาจากผู้ที่เคยทำจริงเสมอ

---

## แนวคิด (4) — ทีมที่ต้องมี

คนเดียวอาจทำหลายบทบาท

- **เจ้าของผลิตภัณฑ์** ตัดสินใจเรื่องขอบเขตและลำดับความสำคัญ (มักเป็นคุณ)
- **ฮาร์ดแวร์** ออกแบบวงจร PCB และเลือกชิ้นส่วน
- **เฟิร์มแวร์** เขียนโปรแกรมบนอุปกรณ์
- **คลาวด์และแอป** รับข้อมูล เก็บ แสดงผล และแจ้งเตือน
- **ข้อมูลและ AI** เก็บข้อมูล ฝึก และทดสอบโมเดล (เฉพาะโจทย์ที่ต้องใช้ AI)
- **ทดสอบและมาตรฐาน** ทดสอบคุณภาพ และประสานการรับรองมาตรฐาน
- **ผู้ผลิตรับจ้าง (EMS)** ประกอบและทดสอบในสายการผลิต เมื่อถึงช่วงผลิตจริง

---

## ฝึกเติม

ใช้ตัวเลขสมมติชุดเดิม แต่เปลี่ยนอายุการใช้งานเป็น **5 ปี** และผลิต **2,000 เครื่อง** คำนวณต้นทุนต่อเครื่องตลอดอายุ แล้วตอบว่าก้อนไหนใหญ่ที่สุด (ใบ้: 600,000/2,000 + 900 + 120×5)

จากนั้นเขียนคำถามที่จะถามผู้ขายหรือผู้รับจ้างเพื่อเปลี่ยนตัวเลขสมมติให้เป็นตัวเลขจริง อย่างน้อยสามข้อ เช่น "ราคาต่อชิ้นที่ 1,000 และ 5,000 ชิ้นต่างกันเท่าไร" "ชิ้นส่วนไหนมีผู้ขายรายเดียว"

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

บทถัดไปพูดเรื่องความเสี่ยงและกฎหมาย ซึ่งหลายเรื่องเป็นต้นทุนที่ซ่อนอยู่ในก้อนครั้งเดียวและก้อนต่อเนื่อง เช่น ค่าทดสอบรับรองมาตรฐานวิทยุ และค่าอัปเดตความปลอดภัยตลอดอายุผลิตภัณฑ์

**สะท้อนคิด** ในโครงการของคุณ ก้อนไหนที่คุณรู้น้อยที่สุด และใครคือคนที่ควรถามเป็นคนแรก

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
