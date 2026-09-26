---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก"
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

# บทเรียน 2.2 — แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก

## ติดตั้ง Bitstream Studio ผูก workspace เปิดเซสชันแรก (Simulator หรือ Bitstream) แล้วสังเกตและสลับเส้นทาง

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 2 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. ติดตั้ง Bitstream Studio และผูก workspace กับโปรเจกต์เฟิร์มแวร์หรือแพ็กแล็บ
2. เปิดเซสชันแรกสำเร็จอย่างน้อยหนึ่งเส้นทาง (Simulator หรือ Bitstream) พร้อมสกรีนช็อตหลักฐาน

---

## ก่อนเริ่ม

- อ่านจบ [บทเรียน 2.1](../l01-vscode-for-twin/README.md)
- เปิดแผ่นสรุป [vscode-twin-setup.md](../l01-vscode-for-twin/resources/vscode-twin-setup.md) ไว้กรอกระหว่างแล็บ
- ทำได้ด้วยโหมด Simulator (ไม่ต้องมีบอร์ด) หรือใช้บอร์ด TESAIoT PSoC Edge DevKit จริง

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Install (required) | เปิด Bitstream Studio ได้ และเห็น toolbar แหล่งข้อมูล / Link |
| Lab B — Workspace bind (required) | อธิบายได้ว่าเฟิร์มแวร์อยู่โฟลเดอร์ไหน และโฮสต์ Twin เปิดจากหน้าต่างไหน |
| Lab C — First live session (required) | มีหลักฐาน live อย่างน้อยหนึ่งเส้นทาง (สกรีนช็อตหรือคลิปสั้น) |
| Lab D — Observe & switch (แนะนำ) | มีโน้ต 3–5 บรรทัดว่าแยกปัญหาเป็นชั้นอย่างไร |

---

## ฝึกเติม/แล็บ (1) — Lab A: Install

1. ติดตั้ง VS Code (หรือ Cursor)
2. ติดตั้ง Bitstream Studio — Path A: Marketplace, หรือ Path B: VSIX จาก Hackathon `vsix/`
3. Reload → Command Palette → **Open Bitstream Studio**
4. (ถ้าจะใช้โหมดไม่มีบอร์ด) ติดตั้ง **Bitstream Simulator** ตามคู่มือของชุดที่ใช้
5. ทำขั้นตอน CA/credentials **เฉพาะเมื่อ** คู่มือรอบนั้นระบุ

---

## ฝึกเติม/แล็บ (2) — Lab B: Workspace bind

1. สร้างหรือเปิดโฟลเดอร์ workspace ตามโครงในบทเรียน
2. วางหรือลิงก์โฟลเดอร์ `firmware/` (หรือ clone Hackathon เป็นอ้างอิงเวอร์ชัน)
3. เปิด Bitstream Studio จากหน้าต่าง workspace เดียวกัน
4. จด path โปรเจกต์ + เวอร์ชัน VSIX/HEX ลง setup sheet

---

## ฝึกเติม/แล็บ (3) — Lab C: First live session

ทำอย่างน้อย **หนึ่ง** เส้นทางให้จบ — แนะนำเริ่ม Simulator ถ้าบอร์ดยังไม่พร้อม

**C1 Simulator path** — Toolbar → Simulator → Start Simulator / Streaming → Link/Connect → เปิด Sensor Telemetry → แคปหน้าจอ: ค่าขยับ + สถานะ Link

**C2 Bitstream path (board)** — Flash HEX ที่จับคู่ VSIX → Toolbar → Bitstream · เลือก COM → Link/Connect จน handshake → ยืนยันกราฟ/ค่าจากบอร์ด → แคปหน้าจอ

---

## ฝึกเติม/แล็บ (4) — Lab D: Observe & switch (แนะนำ)

1. ถ้าทำได้ทั้ง Simulator และ Bitstream — สลับโหมดหนึ่งครั้ง แล้วยืนยันว่าข้อมูลเก่าถูกล้าง/ไม่ปะปน
2. เปิด Output / log สั้น ๆ เมื่อมี error แล้วจดข้อความ
3. (ทางเลือก) เปิดหน้า `web-app/` จาก Hackathon ตามคู่มือ — ชี้ว่าเป็น Visualization ชั้นนอก แล้วถ่ายภาพหน้าจอของคุณเองเป็นหลักฐาน

---

## เช็กความเข้าใจ — ไล่อาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. ไม่เห็นคำสั่ง Open Bitstream Studio — น่าจะเกิดจากอะไร
2. Session / Link ไม่ขึ้น — ควรตรวจอะไรก่อน
3. Simulator ไม่มีค่า — สาเหตุที่พบบ่อยคืออะไร
4. UI โหลดแต่กราฟนิ่ง — ควรตรวจอะไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] Lab A–C ผ่าน
- [ ] vscode-twin-setup.md กรอกครบ
- [ ] หลักฐานเซสชันแรก (สกรีนช็อต)
- [ ] (แนะนำ) Lab D

พร้อมแล้ว ไปต่อ **โมดูล 3 — การสร้างแบบจำลองอุปกรณ์เสมือน**

[บทเรียนโมดูล 3 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

---

## แหล่งที่มา

"บทเรียน 2.2 — แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
