---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.3 — ไปต่อทางไหนดี และแบ่งปันอย่างไรให้ถูก"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก AIoT in Action (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY-NC 4.0"
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

# บทเรียน 2.3 — ไปต่อทางไหนดี และแบ่งปันอย่างไรให้ถูก

## เลือกเส้นทางเรียนต่อ เก็บผลงานเป็น portfolio และอ้างอิง TESA ให้ถูก

**โมดูล 2 — รับรู้ เชื่อมต่อ แล้วไปต่อ**

หลักสูตร **Explorer: เปิดโลกระบบสมองกลฝังตัว** · บทสุดท้าย

---

## เป้าหมาย

1. เลือกเส้นทางเรียนต่อที่ตรงกับเป้าหมายของคุณ พร้อมเหตุผล
2. อ้างอิง TESA ให้ถูกเมื่อแบ่งปันหรือดัดแปลงเนื้อหา
3. รวบรวมผลงานจาก Explorer เป็น portfolio

---

## ก่อนเริ่ม

- จากบทที่แล้ว ทำไม broker สาธารณะที่พอร์ต 1883 จึงไม่เหมาะกับข้อมูลจริง
- ในหกบทที่ผ่านมา บทไหนที่คุณอยากทำต่อมากที่สุด

---

## ดูของจริงก่อน

เปิดโฟลเดอร์หรืออัลบั้มที่คุณเก็บภาพหน้าจอจากบทก่อน ๆ ไว้ แล้วนับดูว่ามีกี่ชิ้น

ของเหล่านี้คือหลักฐานว่าคุณทำอะไรได้แล้ว ไม่ใช่แค่ "เคยอ่าน" มาแล้ว

---

## แนวคิด — ห้าเส้นทาง เลือกตามเป้าหมาย ไม่ใช่ตามความยาก

| ถ้าคุณอยาก... | เส้นทาง |
|---|---|
| ลองต่อเพื่อความสนุกหรือเข้าใจลูกหลาน | ผู้เริ่มต้น (explorer) |
| ตัดสินใจเรื่องผลิตภัณฑ์ โดยไม่ต้องเขียนโค้ด | ผู้ประกอบการ (entrepreneur) |
| เรียนเป็นระบบเพื่อทำโปรเจกต์หรือสมัครงาน | นักศึกษา (student) |
| ยกระดับทักษะเพื่องานที่ทำอยู่ | นักพัฒนา (developer) |
| นำไปสอนในสถานศึกษา | ผู้สอน (educator) |

> ไม่มีเส้นทางไหนดีกว่าเส้นทางอื่น เลือกจากคำถามว่า **"อีกสามเดือนข้างหน้า ฉันอยากทำอะไรได้"**

---

## แนวคิด — เรียนคนเดียวมักไม่จบ หาเพื่อนเรียน

งานวิจัยเรื่องคอร์สออนไลน์แบบเปิดพบว่าผู้ลงทะเบียนส่วนน้อยมากที่เรียนจนจบ

สิ่งที่ช่วยได้จริงคือโครงสร้าง เช่น เรียนเป็นรุ่นพร้อมคนอื่น มีกำหนดส่ง และมีคนคอยตอบ

ถ้ามีรุ่นเรียนหรือค่ายของ TESA เปิด ลองเข้าร่วม หรือชวนเพื่อนสองสามคนเรียนไปพร้อมกันก็ช่วยได้มาก

---

## แนวคิด — แบ่งปันได้ แต่ต้องอ้างอิง TESA ทุกครั้ง

เนื้อหาใน TESA Open Knowledge เผยแพร่ภายใต้สัญญาอนุญาต **CC BY-NC 4.0** — นำไปแบ่งปัน ใช้สอน และดัดแปลงได้ ถ้าไม่ใช่เพื่อการค้า (ใช้เพื่อการค้าต้องขออนุญาต TESA) และต้อง **อ้างอิงที่มา** ทุกครั้ง

> "Explorer: เปิดโลกระบบสมองกลฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (TESA)
> https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

- **ถ้าแก้ไขเนื้อหา** เติมคำว่า **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง
- **โค้ดตัวอย่าง** ดัดแปลงจาก AIoT in Action (MIT) ต้องคงบรรทัดลิขสิทธิ์ที่หัวไฟล์ไว้เสมอ
- **อย่าอ้างว่า TESA รับรอง** งานหรือคอร์สของคุณ

---

## แนวคิด — portfolio คือหลักฐาน

portfolio ไม่ต้องหรูหรา — โฟลเดอร์เดียวที่มีภาพหน้าจอ ไฟล์โค้ดที่คุณแก้ และแผนภาพที่วาดเองพร้อมคำอธิบายสั้น ๆ ก็พอ

ถ้าใช้ GitHub เป็น จะเก็บเป็น repository สาธารณะก็ได้ แต่ **ตรวจก่อนทุกครั้งว่าไม่มีรหัส WiFi หรือรหัสผ่านใด ๆ อยู่ในไฟล์**

TESA วางแผนออกหลักฐานการเรียนจบ (TQP T0 Open Knowledge Completion) สำหรับผู้ที่ผ่านเช็กท้ายบท โดยนับเฉพาะบทเรียนสถานะ `stable` — หลักสูตรนี้ (สถานะ alpha) ยังไม่ถึง

> T0 ยืนยันการเรียนจบ ไม่ใช่การรับรองสมรรถนะ

---

## ฝึกเติม

1. เขียนประโยคเดียว "อีกสามเดือนข้างหน้า ฉันอยาก..." แล้วเลือกเส้นทางหนึ่งจากตาราง
2. สมมติว่าคุณจะนำบทเรียน "โปรแกรมแรก" ไปทำเป็นโพสต์สอนเพื่อน โดยแก้ตัวอย่างให้กะพริบเป็นรหัสมอร์ส เขียนข้อความอ้างอิงที่จะวางท้ายโพสต์ให้ถูกต้อง (ใบ้: มีการแก้ไข ต้องมีคำว่า ดัดแปลง)

---

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน และถือว่าจบหลักสูตร Explorer

1. เจ้าของร้านอาหารอยากรู้ว่าควรลงทุนติดเซนเซอร์เฝ้าตู้แช่หรือไม่ โดยไม่อยากเขียนโค้ดเอง เส้นทางใดเหมาะที่สุด
2. คุณแก้ตัวอย่างไฟกะพริบให้เป็นรหัสมอร์ส แล้วโพสต์สอนเพื่อน ข้อความอ้างอิงข้อใดถูกต้องที่สุด
3. ข้อใดถูกเกี่ยวกับสัญญาอนุญาต CC BY-NC 4.0 ของเนื้อหาหลักสูตรนี้
4. ก่อนนำไฟล์โค้ดขึ้น portfolio สาธารณะ ต้องตรวจอะไรบ้าง (เลือกได้มากกว่าหนึ่งข้อ)

---

## แล็บ

รวบรวม portfolio ของ Explorer ให้มีอย่างน้อยสามชิ้น

- [ ] ตาราง "รับรู้ ตัดสินใจ สั่งงาน" จากบทแรก
- [ ] ภาพหน้าจอของโปรแกรมไฟกะพริบหรือไฟเตือนเมื่อเอียง
- [ ] แผนภาพเส้นทางข้อความ MQTT จากบทที่แล้ว

---

## ไปต่อ

เปิดหน้าหลักสูตรของเส้นทางที่คุณเลือก แล้วดูบทเรียนแรก

ถ้าเลือกเส้นทางนักศึกษาหรือนักพัฒนา คุณเขียน MicroPython กับบอร์ดนี้มาแล้ว บทแรก ๆ ของหลักสูตรถัดไปจะคุ้นมือ

ขอบคุณที่เรียน Explorer จนจบ

---

## แหล่งที่มาและเครดิต

"Explorer: เปิดโลกระบบสมองกลฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์
วิศวกรรมระบบสมองกลฝังตัว มหาวิทยาลัยบูรพา (BUU) · Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
