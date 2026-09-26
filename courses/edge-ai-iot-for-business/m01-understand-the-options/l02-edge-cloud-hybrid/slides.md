---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — Edge, Cloud หรือ Hybrid"
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

# บทเรียน 1.2 — Edge, Cloud หรือ Hybrid

## เปรียบเทียบการประมวลผลบนอุปกรณ์ บนคลาวด์ และแบบผสม ในสี่มิติ แล้วเลือกให้เหมาะกับโจทย์

**โมดูล 1 — เข้าใจทางเลือก**

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เปรียบเทียบ edge, cloud และ hybrid ได้ครบสี่มิติ
2. เลือกสถาปัตยกรรมให้กรณีตัวอย่างพร้อมเหตุผล
3. ระบุคำถามที่ต้องถามทีมเทคนิคก่อนเลือก

---

## ก่อนเริ่ม

- จากบทที่แล้ว บันไดสามขั้นก่อนพูดถึง AI มีอะไรบ้าง
- โจทย์ของคุณต้องตอบสนองเร็วแค่ไหน ภายในเสี้ยววินาที ภายในนาที หรือพรุ่งนี้เช้าก็ยังทัน

---

## ดูของจริงก่อน

นึกถึงกล้องหน้าบ้านสองแบบ แบบแรกส่งวิดีโอทั้งวันขึ้นคลาวด์ให้เซิร์ฟเวอร์ที่อื่นตรวจว่ามีคนเดินผ่านไหม แบบที่สองตรวจเองในตัวกล้อง แล้วส่งขึ้นไปแค่ข้อความสั้น ๆ ว่า "มีคนที่ประตู 14:05" พร้อมภาพเฉพาะช่วงนั้น

สองแบบให้ผลที่ผู้ใช้เห็นคล้ายกัน แต่ต่างกันมากเรื่องปริมาณข้อมูลที่ต้องส่ง ข้อมูลส่วนตัวที่ออกจากบ้าน และอาการตอนเน็ตหลุด

แบบแรกคือ **cloud** แบบที่สองคือ **edge** และถ้ายังส่งสรุปขึ้นไปทำรายงานรวมบนคลาวด์ด้วย ก็คือ **hybrid**

---

## แนวคิด (1) — สามทางเลือก

- **Edge** อุปกรณ์วัดและตัดสินใจเอง ส่งออกเฉพาะผลหรือเหตุการณ์
- **Cloud** อุปกรณ์วัดแล้วส่งข้อมูลดิบขึ้นไป ให้เซิร์ฟเวอร์คิดแทน
- **Hybrid** อุปกรณ์ตัดสินใจเรื่องด่วนเอง แล้วส่งสรุปขึ้นคลาวด์เพื่อดูภาพรวม เก็บประวัติ และปรับปรุงโมเดลรอบถัดไป — โครงการจริงส่วนมากลงเอยที่แบบนี้

---

## แนวคิด (2) — สี่มิติที่ใช้เทียบ

| มิติ | Edge | Cloud | คำถามที่ช่วยตัดสิน |
|---|---|---|---|
| **ความหน่วง (latency)** | ตอบสนองทันทีโดยไม่รอเครือข่าย | ต้องรอข้อมูลไปกลับ | ถ้าช้าไปสองวินาที เสียหายไหม |
| **ความเป็นส่วนตัว (privacy)** | ข้อมูลดิบไม่ต้องออกจากอุปกรณ์ | ข้อมูลดิบถูกส่งและเก็บที่อื่น | ข้อมูลนี้ระบุตัวคนได้ไหม |
| **ต้นทุน (cost)** | อุปกรณ์แพงขึ้น แต่ค่าส่ง/ประมวลผลรายเดือนต่ำ | อุปกรณ์ถูกกว่า แต่มีค่าคลาวด์ต่อเนื่อง | จะมีอุปกรณ์กี่ตัว ใช้กี่ปี |
| **การเชื่อมต่อ (connectivity)** | ทำงานต่อได้แม้เน็ตหลุด | เน็ตหลุดเท่ากับหยุดคิด | หน้างานมีสัญญาณเสถียรไหม |

อีกสองเรื่องที่มักถูกลืม: **การอัปเดต** (โมเดลบนอุปกรณ์ต้องมีระบบอัปเดตทางไกลที่ปลอดภัย) และ **พลังงาน** (อุปกรณ์ใช้แบตต้องเลือกว่าจะใช้พลังงานไปกับการคิดหรือการส่ง)

---

## แนวคิด (3) — อ่านตารางให้เป็น

ไม่มีทางเลือกไหนชนะทุกมิติ งานของคุณคือบอกว่ามิติไหนสำคัญที่สุดสำหรับโจทย์นี้ แล้วยอมจ่ายในมิติที่สำคัญน้อยกว่า

- ระบบแจ้งการล้มของผู้สูงอายุ — ความเป็นส่วนตัวกับความหน่วงสำคัญที่สุด จึงเอนไปทาง **edge**
- รายงานสรุปการใช้พลังงานของอาคารประจำเดือน — ความหน่วงแทบไม่สำคัญ **cloud** จึงง่ายและคุ้มกว่า

---

## ฝึกเติม

เลือกทางเลือกให้สามกรณีนี้ และเขียนเหตุผลที่อ้างถึงอย่างน้อยสองมิติ

| กรณี | Edge / Cloud / Hybrid | เหตุผล (อย่างน้อย 2 มิติ) |
|---|---|---|
| สวนทุเรียนบนเขา สัญญาณมือถือขาดเป็นช่วง ต้องสั่งปั๊มน้ำตามความชื้นดิน | | |
| ร้านค้าปลีก 200 สาขา อยากเทียบยอดคนเข้าร้านรายสัปดาห์ | | |
| สายพานคัดแยกผลไม้ ต้องปัดลูกที่เสียออกภายในเสี้ยววินาที และอยากดูสถิติของเสียรายวัน | | |

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ — คำถามที่ควรถามทีมเทคนิค

1. ถ้าเน็ตหลุดหนึ่งวัน ระบบยังทำอะไรได้ และข้อมูลช่วงนั้นหายไหม
2. ข้อมูลดิบชนิดไหนออกจากอุปกรณ์บ้าง ไปเก็บที่ไหน นานเท่าไร
3. ค่าใช้จ่ายรายเดือนต่ออุปกรณ์หนึ่งตัวประมาณเท่าไร และขึ้นกับอะไร
4. ถ้าต้องแก้โมเดลหรือเฟิร์มแวร์ จะอัปเดตอุปกรณ์ที่อยู่หน้างานอย่างไร และปลอดภัยแค่ไหน

**สะท้อนคิด** โจทย์ของคุณจากบทที่แล้วควรเป็น edge, cloud หรือ hybrid มิติไหนที่ทำให้คุณตัดสินใจแบบนั้น

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0
