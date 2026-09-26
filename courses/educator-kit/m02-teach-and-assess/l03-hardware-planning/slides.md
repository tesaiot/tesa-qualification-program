---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.3 — วางแผนฮาร์ดแวร์"
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

# บทเรียน 2.3 — วางแผนฮาร์ดแวร์

## วางแผนบอร์ดหนึ่งตัวต่อผู้เรียนสามถึงสี่คนร่วมกับอีมูเลเตอร์ การหมุนเวียนบทบาทในกลุ่ม remote flash และรายการตรวจก่อนแล็บ

**โมดูล 2 — สอนและประเมิน**

หลักสูตร **ชุดสำหรับผู้สอน (Educator Kit)**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณฮาร์ดแวร์ที่ต้องใช้
2. ออกแบบการหมุนเวียนบทบาทในกลุ่ม
3. เลือกได้ว่าเมื่อใดใช้ remote flash

## ก่อนเริ่ม

จากบทที่แล้ว งานให้คะแนนแบบไหนที่ต้องทำบนบอร์ดต่อหน้าผู้ประเมิน — จากบทวิธีสอน กิจกรรมแบบไหนที่ทำในอีมูเลเตอร์ได้ และแบบไหนต้องใช้บอร์ดจริง

---

## ดูของจริงก่อน

เปิด BENTO IDE กดปุ่ม **BENTO Emulator** แล้วกด **HW** จะเห็นแผงฮาร์ดแวร์จำลองที่มีหลอดไฟ ปุ่ม ลูกบิด และแผ่นเอียง ผู้เรียนทุกคนใช้สิ่งนี้ได้พร้อมกันโดยไม่ต้องมีบอร์ด นี่คือเหตุผลที่รายวิชาไม่ต้องมีบอร์ดคนละตัว

---

## แนวคิด (1) — หนึ่งบอร์ดต่อสามถึงสี่คน ทุกคนมีอีมูเลเตอร์

อัตราที่แนะนำคือบอร์ดหนึ่งตัวต่อผู้เรียนสามถึงสี่คน และ **ทุกคน** ใช้อีมูเลเตอร์ในเครื่องของตัวเอง งานที่ทำในอีมูเลเตอร์ได้ (ทำความเข้าใจ API ฝึกเติม ออกแบบหน้าจอ) ไม่ต้องรอคิวบอร์ด บอร์ดถูกใช้เฉพาะงานที่ต้องใช้มันจริง ตัวเลขนี้เป็นแนวทาง ไม่ใช่ข้อบังคับ — มีบอร์ดมากกว่านี้ยิ่งดี ถ้ามีน้อยกว่านี้ ให้ย้ายงานเข้าอีมูเลเตอร์มากขึ้นและใช้ remote flash

---

## แนวคิด (2) — หมุนบทบาท ไม่ให้ใครนั่งดูอย่างเดียว

กลุ่มที่มีบอร์ดตัวเดียวมักจบที่คนเก่งที่สุดคนเดียวพิมพ์ทั้งแล็บ ป้องกันด้วยบทบาทที่หมุนทุก 15 นาที

| บทบาท | ทำอะไร |
|---|---|
| คนขับ (driver) | พิมพ์และรันบนบอร์ด |
| ผู้นำทาง (navigator) | อ่านโจทย์ บอกขั้นถัดไป ตรวจกับเป้าหมาย |
| ผู้ทดสอบ (tester) | รันโค้ดเดียวกันในอีมูเลเตอร์ เทียบผลกับบอร์ด |
| ผู้บันทึก (recorder) | เก็บหลักฐาน ภาพ log และคำทำนาย ลง portfolio ของกลุ่ม |

---

## แนวคิด (3) — Remote flash

สำหรับเฟิร์มแวร์ที่ต้องแฟลชเป็นไฟล์ `.hex` บริการ **TESAIoT Remote Flash** ให้เบราว์เซอร์ส่งไฟล์ไปแฟลชบอร์ดที่ต่ออยู่กับอีกเครื่องหนึ่ง ขั้นตอนคือ สร้างรหัสจับคู่ (pairing code) บนหน้าเว็บ ใส่รหัสในแอป TESAIoT Programmer บนเครื่องที่ต่อบอร์ด แล้วเลือกไฟล์ `.hex` และสั่งแฟลช ใช้ได้เมื่อ

- บอร์ดทั้งหมดต่ออยู่กับเครื่องกลางในห้องแล็บ และผู้เรียนส่งงานจากเครื่องของตัวเอง
- ผู้เรียนเรียนทางไกล และสถาบันมีบอร์ดต่อไว้ให้

ก่อนใช้กับทั้งห้อง ให้ทดลองจับคู่และแฟลชด้วยตัวเองก่อนหนึ่งรอบ

---

## แนวคิด (4) — สิ่งที่อีมูเลเตอร์ไม่บอก

อีมูเลเตอร์ตอบได้ดีว่าโปรแกรมรันจบไหมและหน้าจอหน้าตาอย่างไร แต่ WiFi เป็นของจำลอง ค่าเซนเซอร์เป็นค่าจำลอง และข้อจำกัดของฮาร์ดแวร์บางอย่าง เช่นเวลาที่บอร์ดยังไม่พร้อมตอบเรื่องเซนเซอร์หลังเปิดเครื่อง ไม่ปรากฏในเบราว์เซอร์ ผู้สอนควรรันตัวอย่างของแล็บบนบอร์ดจริงก่อนทุกครั้ง แล้วบอกผู้เรียนล่วงหน้าว่าผลต่างกันตรงไหน

---

## ตัวอย่างสมบูรณ์

รายวิชามีผู้เรียน 30 คน แล็บสัปดาห์ละ 3 ชั่วโมง

- **ท่าที่ 1 จำนวนบอร์ด** 30 ÷ 4 = 7.5 ปัดขึ้นเป็น 8 กลุ่ม บวกสำรอง 2 รวม 10 บอร์ด สาย USB ข้อมูล 12 เส้น
- **ท่าที่ 2 เครื่อง** ผู้เรียนใช้โน้ตบุ๊กของตัวเองสำหรับอีมูเลเตอร์ ห้องแล็บมีเครื่องต่อบอร์ด 8 เครื่อง
- **ท่าที่ 3 เวลา** ครึ่งแรกของแล็บทุกคนทำในอีมูเลเตอร์ ครึ่งหลังหมุนบทบาททุก 15 นาทีบนบอร์ด
- **ท่าที่ 4 เครือข่าย** ทดสอบก่อนเปิดภาคว่าเครือข่ายแล็บไม่ต้องล็อกอินผ่านหน้าเว็บ และไม่กันพอร์ตที่บทเรียน MQTT ใช้

---

## ฝึกเติม / เช็กความเข้าใจ

คัดลอก [resources/hardware-checklist.md](resources/hardware-checklist.md) แล้วเติมให้ครบสำหรับรายวิชาของคุณ พร้อมตารางหมุนบทบาทหนึ่งแล็บ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

บทถัดไปเป็นโมดูลสุดท้าย ว่าด้วยการอบรมผู้สอนและเส้นทางสู่ TQP Certified Trainer

**สะท้อนคิด** ถ้าวันแล็บบอร์ดเสียไปครึ่งหนึ่ง แผนสำรองของคุณคืออะไร และผู้เรียนยังได้ผลการเรียนรู้ข้อไหนครบ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"ชุดสำหรับผู้สอน (Educator Kit)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
