---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — แล็บ: แผนที่สถาปัตยกรรม Twin"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
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

# บทเรียน 1.2 — แล็บ: แผนที่สถาปัตยกรรม Twin

## นิยามคำด้วยภาษาตัวเอง วาด data flow และกรอกตารางตัดสินใจว่าเทสไหนใช้ Twin ได้ เทสไหนต้องบอร์ด

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 1 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. วาดแผนภาพ data flow ของระบบตัวอย่างหนึ่งชุด ตั้งแต่เซ็นเซอร์ถึง dashboard
2. กรอกตารางตัดสินใจอย่างน้อย 4 แถว โดยมีทั้งแถวที่ "Twin พอ" และ "ต้องบอร์ด"

---

## ก่อนเริ่ม

- [ ] อ่านจบ [บทเรียน 1.1](../l01-twin-architecture/README.md)
- [ ] เปิดแผ่นสรุป [twin-architecture-map.md](../l01-twin-architecture/resources/twin-architecture-map.md)
- แล็บเชิงแนวคิด + ไดอะแกรม — ไม่ต้องใช้บอร์ด (Part D เป็นทางเลือกเสริมถ้ามีโฮสต์ให้เปิดดู)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละส่วน

| ส่วน | เกณฑ์ผ่าน |
|---|---|
| Part A — Definitions | อ่านแล้วคนอื่นในทีมเข้าใจโดยไม่ต้องเปิดบทเรียน |
| Part B — Architecture diagram | มีลูกศรทิศทางข้อมูลชัด และชี้ได้ว่า Virtual Device อยู่กล่องไหน |
| Part C — Test decision table | มีอย่างน้อยหนึ่งแถวที่ตอบ "Twin พอ" และหนึ่งแถวที่ตอบ "ต้องบอร์ด" |
| Part D — Optional host peek | มีโน้ต 3–5 บรรทัดว่า "สิ่งที่เห็นบนจอ = ชั้นไหนในสถาปัตยกรรม" |

---

## ฝึกเติม/แล็บ (1) — Part A: Definitions (คำพูดของคุณเอง)

เขียน 2–3 ประโยคต่อข้อ:

1. **Virtual Device** คืออะไร
2. **Digital Twin** ในหลักสูตรนี้ครอบคลุมอะไรบ้าง *นอกจาก* ตัวอุปกรณ์
3. ทำไมต้องแยก **Firmware Logic** จากรายละเอียดฮาร์ดแวร์

---

## ฝึกเติม/แล็บ (2) — Part B: Architecture diagram

วาด (กระดาษ / Mermaid / กล่องข้อความ) แสดงอย่างน้อย: VS Code / Bitstream Studio · Firmware Logic · Communication path (UART และ/หรือ MQTT) · Twin Engine / Virtual Device (หรือ Simulator) · Visualization หรือ Dashboard · (ถ้ามี) Cloud / broker

ตัวอย่างโครงเปล่า:

```text
[VS Code + Bitstream Studio]
        │
[Firmware Logic] ──comm──► [Twin / Simulator state]
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              [Telemetry UI]          [web-app / MQTT]
```

---

## ฝึกเติม/แล็บ (3) — Part C: Test decision table

กรอกอย่างน้อย 4 แถว (แนะนำครบทุกแถว):

| สถานการณ์ทดสอบ | Twin / Sim พอไหม | ต้องบอร์ดจริงไหม | เหตุผลสั้น ๆ |
|---|---|---|---|
| Logic สลับโหมดจากปุ่ม | | | |
| อ่าน IMU แล้วคำนวณบนโค้ด | | | |
| ตรวจรูปแบบ MQTT JSON / topic | | | |
| Wi‑Fi หรือ BLE ระยะในห้องจริง | | | |
| ตรวจ pin map / ขาผิด | | | |
| วัดพลังงาน / battery life | | | |

---

## ฝึกเติม/แล็บ (4) — Part D: Optional host peek (แนะนำ)

เลือกอย่างน้อยหนึ่งอย่าง แล้วเก็บหลักฐานเป็นภาพหน้าจอของคุณเอง:

1. เปิด **Bitstream Studio** แล้วถ่ายภาพหน้าจอที่เห็นแผง Visualization และจุดที่สลับ Bitstream กับ Simulator — บันทึกว่าแต่ละส่วนตรงกับชั้นไหนในแผนภาพ Part B
2. เปิดหน้า dashboard ใน Hackathon `web-app/` (ตามคู่มือของชุดที่ใช้) แล้วถ่ายภาพหน้าจอพร้อมอธิบายว่ามันอยู่ชั้นไหนในแผนภาพ Part B

---

## เช็กความเข้าใจ

1. Virtual Device ต่างจาก Digital Twin อย่างไร (ตอบด้วยคำพูดของตัวเอง)
2. ในแผนภาพ Part B ของคุณ Simulator ควรวางไว้ใกล้กล่องใด
3. ทำไม Twin ถึง "ไม่แทน" การทดสอบ RF/pin map/พลังงาน

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] ส่วน A ครบ 3 ข้อ
- [ ] แผนภาพส่วน B
- [ ] ตารางส่วน C ≥ 4 แถว
- [ ] (แนะนำ) โน้ตส่วน D

พร้อมแล้ว ไปต่อ **โมดูล 2 — VS Code สำหรับพัฒนาร่วมกับ Twin**

[บทเรียนโมดูล 2 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

---

## แหล่งที่มา

"บทเรียน 1.2 — แล็บ: แผนที่สถาปัตยกรรม Twin" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
