---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.3 — เขียนโจทย์ให้นักพัฒนา: Decision Canvas หนึ่งหน้า"
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

# บทเรียน 2.3 — เขียนโจทย์ให้นักพัฒนา: Decision Canvas หนึ่งหน้า

## รวบรวมทุกการตัดสินใจจากห้าบทก่อนเป็น decision canvas หนึ่งหน้าที่ส่งให้ทีมพัฒนาหรือผู้รับจ้างได้

**โมดูล 2 — ตัดสินใจและส่งโจทย์** · บทเรียนสุดท้ายของหลักสูตร

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เติม decision canvas ของโครงการตัวเองให้ครบ 15 ช่อง โดยช่องที่ยังไม่รู้เขียนว่าต้องถามใคร
2. แยกโจทย์ที่ดีออกจากโจทย์ที่คลุมเครือได้ และแก้โจทย์คลุมเครือให้วัดผลได้
3. เขียนข้อความอ้างอิง TESA ที่ถูกต้องเมื่อแบ่งปันหรือดัดแปลงแม่แบบ

---

## ก่อนเริ่ม

จากบทที่แล้ว เรื่องไหนต้องตกลงกับพันธมิตรก่อนเซ็นสัญญา — และถ้ามีนักพัฒนามานั่งตรงหน้าคุณสิบนาที คุณจะเล่าโครงการให้เขาฟังว่าอย่างไร

---

## ดูของจริงก่อน — เทียบโจทย์สองแบบ

ส่งให้บริษัทรับพัฒนาเดียวกัน

**โจทย์ ก** "อยากได้ระบบ AI อัจฉริยะเฝ้าร้าน ใช้ง่าย ราคาไม่แพง ทำให้เสร็จเร็วที่สุด"

**โจทย์ ข** "วัดอุณหภูมิในตู้แช่ 12 ตู้ของร้านสามสาขา ถ้าอุ่นเกินเกณฑ์นานกว่า 15 นาทีให้ส่งข้อความหาผู้จัดการกะ ยอมให้เตือนผิดไม่เกินเดือนละ 2 ครั้งต่อสาขา ต้องทำงานต่อได้แม้เน็ตหลุด ไม่เก็บภาพหรือข้อมูลลูกค้า รอบแรกยังไม่ต้องมีแอปมือถือ ต้องได้ซอร์สโค้ดและเอกสารคืนเมื่อจบงาน"

ใบเสนอราคาของโจทย์ ก จะต่างกันได้เป็นสิบเท่าระหว่างผู้รับจ้างสองราย เพราะตีความ "อัจฉริยะ" ไม่เหมือนกัน ส่วนโจทย์ ข เทียบราคาและเทียบงานกันได้ และตอนส่งมอบก็ตรวจได้ว่าเสร็จจริงหรือยัง

---

## แนวคิด (1) — โจทย์ที่ดีตรวจรับงานได้

ทุกประโยคในโจทย์ควรตอบได้ว่า "ตอนส่งมอบ เราจะตรวจอย่างไรว่าทำตามนี้แล้ว" คำอย่าง อัจฉริยะ ใช้ง่าย ทันสมัย เร็วที่สุด ตรวจไม่ได้ ให้เปลี่ยนเป็นตัวเลขหรือเงื่อนไข เช่น "เตือนผิดไม่เกินเดือนละ 2 ครั้ง" หรือ "ผู้จัดการตั้งเกณฑ์ใหม่ได้เองภายใน 1 นาที"

ขอบเขตที่ดีบอกทั้งสิ่งที่ทำและสิ่งที่ **ไม่ทำ** ในรอบนี้ ช่วยกันงานงอก และทำให้ราคาเทียบกันได้

---

## แนวคิด (2) — Decision canvas หนึ่งหน้า

แม่แบบ [resources/decision-canvas.md](resources/decision-canvas.md) มี 15 ช่อง แต่ละช่องมาจากบทเรียนหนึ่งในหลักสูตรนี้

| ช่อง | มาจากบทเรียน |
|---|---|
| 1–4 ปัญหา · โจทย์สามส่วน · บันไดก่อน AI · ตัวชี้วัด | บทเรียน 1.1 |
| 5–7 สถาปัตยกรรม · หน้างาน · ข้อมูล | บทเรียน 1.2 |
| 8–9 ต้นทุนและเวลา | บทเรียน 1.3 |
| 10–11 ความเสี่ยง · กฎและมาตรฐาน | บทเรียน 2.1 |
| 12–13 ทางเลือกและสิ่งที่ต้องได้คืน | บทเรียน 2.2 |
| 14–15 ขอบเขตและผู้ตัดสินใจ | บทเรียนนี้ |

---

## แนวคิด (3) — แบ่งปันแม่แบบได้ แต่ต้องอ้างอิง TESA

แม่แบบนี้และเนื้อหาทั้งหลักสูตรเผยแพร่ภายใต้ CC BY 4.0 นำไปใช้ในบริษัท แจกให้ลูกค้า หรือใช้ในงานที่ปรึกษาได้ รวมถึงเชิงพาณิชย์ เงื่อนไขคือต้องอ้างอิงที่มาด้วยข้อความนี้:

> "«ชื่อบทเรียนหรือหลักสูตร»" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
> (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าคุณแก้แม่แบบ เช่น เพิ่มช่องของบริษัท ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง และบอกสั้น ๆ ว่าเปลี่ยนอะไร การอ้างอิงไม่ได้แปลว่า TESA รับรองโครงการหรือบริการของคุณ ห้ามเขียนให้เข้าใจแบบนั้น รายละเอียดและตัวอย่างอยู่ใน ATTRIBUTION.md

---

## ฝึกเติม

1. แก้ **โจทย์ ก** ข้างบนให้กลายเป็นโจทย์ที่ตรวจรับงานได้ ใช้ร้านของคุณเองหรือร้านสมมติก็ได้
2. คัดลอก [resources/decision-canvas.md](resources/decision-canvas.md) แล้วเติมให้ครบ 15 ช่องสำหรับโครงการของคุณ ใช้สิ่งที่ทำไว้ในห้าบทก่อน

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน และถือว่าจบหลักสูตรนี้

---

## ฝึกเติม/แล็บ

นำ decision canvas ที่เติมแล้วไปคุยกับนักพัฒนาหรือผู้รับจ้างอย่างน้อยหนึ่งราย ขอให้เขาชี้ช่องที่ยังไม่ชัดที่สุดสามช่อง แก้ช่องเหล่านั้น แล้วเก็บทั้งฉบับก่อนและหลังแก้ไว้เป็นหลักฐานการเรียนรู้

## ไปต่อ / สะท้อนคิด

ถ้าทีมของคุณจะพัฒนาเอง ให้ทีมดูเส้นทางนักพัฒนาใน catalog/tracks.yaml TESA มีหลักสูตรอบรมของ TESA Qualification Program (TQP) และเครือข่ายสมาชิกที่ช่วยต่อยอดได้

**สะท้อนคิด** หลังเติม canvas ครบ คุณยังอยากใช้ AI ในโครงการนี้อยู่ไหม คำตอบเปลี่ยนไปจากวันแรกของหลักสูตรหรือเปล่า เพราะอะไร

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0
