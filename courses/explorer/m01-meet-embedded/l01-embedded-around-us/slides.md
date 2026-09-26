---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — ระบบสมองกลฝังตัวซ่อนอยู่รอบตัวเรา"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก AIoT in Action (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY 4.0"
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

# บทเรียน 1.1 — ระบบสมองกลฝังตัวซ่อนอยู่รอบตัวเรา

## มองหาคอมพิวเตอร์ตัวเล็กในของใช้ประจำวัน

**โมดูล 1 — รู้จักระบบสมองกลฝังตัวและเขียนโปรแกรมแรก**

หลักสูตร **Explorer: เปิดโลกระบบสมองกลฝังตัว** · ไม่ต้องมีบอร์ด ไม่ต้องติดตั้งอะไร

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุส่วนรับรู้ ส่วนตัดสินใจ และส่วนสั่งงาน ของอุปกรณ์ในบ้านได้อย่างน้อย 3 ชิ้น
2. อธิบายได้ว่าไมโครคอนโทรลเลอร์ต่างจากคอมพิวเตอร์ทั่วไปอย่างไร
3. จำแนกได้ว่าอุปกรณ์ใดมีระบบสมองกลฝังตัว

ใช้แค่ตากับกระดาษหนึ่งแผ่น

---

## ก่อนเริ่ม

ลองตอบในใจสองข้อนี้ ไม่ต้องกลัวผิด

- ในบ้านคุณมีของกี่ชิ้นที่ "รู้" ว่าตอนนี้กี่โมง
- หม้อหุงข้าวรู้ได้อย่างไรว่าข้าวสุกแล้ว

คำตอบของสองข้อนี้คือเรื่องทั้งหมดของบทเรียนนี้

---

## ดูของจริงก่อน

เดินรอบบ้านหรือห้องทำงานสักสองนาที แล้วจดของที่มีปุ่ม มีไฟ มีจอ หรือส่งเสียงเตือนได้

เช่น เครื่องซักผ้า ไมโครเวฟ รีโมตแอร์ นาฬิกาข้อมือ ลิฟต์ ไฟจราจร เครื่องวัดความดัน

ของเกือบทุกชิ้นในรายการนี้มีคอมพิวเตอร์ตัวเล็ก ๆ ซ่อนอยู่ข้างใน ไม่มีคีย์บอร์ด ไม่มีเมาส์ และคนส่วนใหญ่ไม่เคยรู้ว่ามันอยู่ตรงนั้น

นี่แหละคือ **ระบบสมองกลฝังตัว (embedded system)**

---

## แนวคิด — รับรู้ ตัดสินใจ สั่งงาน

ระบบสมองกลฝังตัวเกือบทุกชิ้นทำงานวนสามจังหวะเดิมซ้ำไปเรื่อย ๆ

| จังหวะ | ตัวอย่างในหม้อหุงข้าวดิจิทัล |
|---|---|
| **รับรู้** (sense) ผ่าน **เซนเซอร์** | เซนเซอร์อุณหภูมิที่ก้นหม้อ |
| **ตัดสินใจ** (decide) ด้วย **ไมโครคอนโทรลเลอร์** | "ร้อนเกินจุดหนึ่งแล้ว แปลว่าน้ำหมด ข้าวสุก" |
| **สั่งงาน** (act) ผ่าน **แอคชูเอเตอร์** | ตัดไฟขดลวดความร้อน เปลี่ยนเป็นโหมดอุ่น |

หม้อหุงข้าวรุ่นดั้งเดิมที่มีคันโยกอันเดียวก็รู้ว่าข้าวสุกได้เหมือนกัน แต่ใช้กลไกตัดไฟตามความร้อน ไม่มีคอมพิวเตอร์อยู่ข้างใน

> ของสองชิ้นที่ทำงานเดียวกัน จึงอาจเป็นระบบสมองกลฝังตัวชิ้นหนึ่ง และไม่ใช่อีกชิ้นหนึ่ง

---

## แนวคิด — ลองกับเครื่องซักผ้า

- **รับรู้**: เซนเซอร์วัดระดับน้ำ
- **ตัดสินใจ**: โปรแกรมซักที่เลือกไว้
- **สั่งงาน**: มอเตอร์กับวาล์วน้ำ

พอเห็นแบบนี้ครั้งหนึ่งแล้ว คุณจะเริ่มเห็นมันในทุกอย่างรอบตัว

---

## แนวคิด — ไมโครคอนโทรลเลอร์ไม่ใช่คอมพิวเตอร์ย่อส่วน

คอมพิวเตอร์บนโต๊ะถูกออกแบบให้ทำได้ทุกอย่าง เปิดเว็บ พิมพ์งาน เล่นเกม

**ไมโครคอนโทรลเลอร์** ถูกออกแบบให้ทำงานเดียว ให้ดี ให้ตรงเวลา และให้กินไฟน้อย

- **งานเฉพาะ** — โปรแกรมเดียวรันตั้งแต่เปิดเครื่องจนปิดเครื่อง ไม่มีใครมาติดตั้งแอปเพิ่ม
- **ตรงเวลา** — ถุงลมนิรภัยต้องพองในเวลาที่กำหนด ช้าไปนิดเดียวก็ไม่มีประโยชน์ งานแบบนี้เรียกว่า **เวลาจริง (real-time)**
- **ประหยัดพลังงานและตัวเล็ก** — หลายชิ้นใช้ถ่านก้อนเดียวได้เป็นปี ทั้งระบบอยู่บนชิปเดียว

---

## แนวคิด — แล้วอะไรไม่ใช่

ของที่ไม่มีการตัดสินใจเลย เช่น สวิตช์ไฟธรรมดาที่แค่ต่อหรือตัดวงจร หรือไฟฉายที่กดแล้วติด **ไม่ถือเป็นระบบสมองกลฝังตัว** แม้จะมีไฟฟ้าวิ่งอยู่ก็ตาม

> ถ้าไม่มีส่วนที่ "คิด" ก็ยังไม่ใช่

---

## ฝึกเติม

หยิบกระดาษมาตีตารางสามช่อง แล้วเติมให้ครบอย่างน้อยสามแถวจากของที่คุณจดไว้ตอน "ดูของจริงก่อน"

| อุปกรณ์ | รับรู้อะไร | ตัดสินใจอะไร | สั่งอะไร |
|---|---|---|---|
| ตัวอย่าง: แอร์ | อุณหภูมิห้อง | "ห้องยังร้อนกว่าที่ตั้งไว้" | คอมเพรสเซอร์ พัดลม |
| | | | |
| | | | |

ถ้าช่องไหนเติมไม่ได้ ลองถามว่า "มันรู้ได้อย่างไร" และ "มันทำอะไรต่อ"

---

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่านบทเรียนนี้

1. ในเครื่องซักผ้า ชิ้นส่วนใดทำหน้าที่ "สั่งงาน" (actuator)
2. เรียงจังหวะการทำงานของแอร์ที่ตั้งอุณหภูมิไว้ 25 องศา ให้ถูกลำดับ
3. ข้อใดคือความต่างระหว่างไมโครคอนโทรลเลอร์กับคอมพิวเตอร์บนโต๊ะ (เลือกได้มากกว่าหนึ่งข้อ)
4. อุปกรณ์ใดต่อไปนี้มีระบบสมองกลฝังตัว (เลือกได้มากกว่าหนึ่งข้อ)

---

## ไปต่อ

ลองคิดต่อว่า ถ้าเซนเซอร์อุณหภูมิในหม้อหุงข้าวเสีย แล้วรายงานค่าเย็นตลอดเวลา อะไรจะเกิดขึ้น

คำถามแบบนี้คือสิ่งที่วิศวกรระบบฝังตัวต้องคิดทุกวัน ระบบที่ดีต้องรู้ตัวเมื่อเซนเซอร์ของตัวเองโกหก

บทถัดไป: [บทเรียน 1.2 — รู้จักบอร์ดและอีมูเลเตอร์](../l02-board-and-emulator/README.md) — เราจะได้เห็นไมโครคอนโทรลเลอร์ของจริงหนึ่งตัว และลองสั่งมันผ่านเบราว์เซอร์

---

## แหล่งที่มาและเครดิต

"Explorer: เปิดโลกระบบสมองกลฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์
วิศวกรรมระบบสมองกลฝังตัว มหาวิทยาลัยบูรพา (BUU) · Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)
