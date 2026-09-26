---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — แล็บ: I/O ครบวงจรแบบ co-simulation"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY 4.0"
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

# บทเรียน 4.2 — แล็บ: I/O ครบวงจรแบบ co-simulation

## bring-up co-sim พิสูจน์เส้นทาง input และ output จด latency และ (แนะนำ) ใช้ web-app ex05 เป็นกระจกชั้นที่สอง

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 4 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. รันเฟิร์มแวร์คู่ Twin/โฮสต์ให้มี heartbeat ทั้งสองฝั่ง
2. เก็บหลักฐานทั้งเส้นทาง input และ output และจด latency อย่างน้อยหนึ่งจุด

---

## ก่อนเริ่ม

- [ ] Lab โมดูล 2 เซสชันแรกผ่าน
- [ ] Lab โมดูล 3 มี device model + event script (หรือ timeline)
- [ ] เลือก path: Simulator และ/หรือ Board + HEX
- [ ] โฟลเดอร์ `lab-notes/` สำหรับหลักฐาน

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Bring-up co-sim | ทั้งโฮสต์และแหล่งเฟิร์มแวร์มีสัญญาณชีวิตชัด |
| Lab B — Input path | คนในทีมอธิบายลูกศร Twin/stimulus → firmware ได้พร้อมหลักฐาน |
| Lab C — Output path | มีหลักฐานคู่ (firmware side + host side) |
| Lab D — Latency note (แนะนำ) | มีตัวเลขช่วงและสมมติฐานแหล่งหน่วง |

---

## ฝึกเติม/แล็บ (1) — Lab A: Bring-up co-sim

1. เปิด Bitstream Studio
2. เลือก **Simulator** *หรือ* **Bitstream** (อย่างใดอย่างหนึ่ง)
3. Link จนมีสตรีม/heartbeat
4. รอ ≥ 30 วินาทีโดยไม่หลุด
5. แคปหน้าจอสถานะ Link + กราฟ/ค่า

---

## ฝึกเติม/แล็บ (2) — Lab B: Input path

1. ใช้สคริปต์/ไทม์ไลน์จากโมดูล 3 หรือกระตุ้นด้วย scene/UI/ปุ่ม
2. ให้เฟิร์มแวร์แสดงว่าอ่านค่าได้ (UART log, การเปลี่ยนโหมด, หรือค่าที่ echo บนโฮสต์อย่างชัดว่ามาจาก logic อ่าน)
3. บันทึก: สิ่งที่กระตุ้น → สิ่งที่เฟิร์มแวร์รายงาน

---

## ฝึกเติม/แล็บ (3) — Lab C: Output path

1. ให้เฟิร์มแวร์เปลี่ยนเอาต์พุตอย่างน้อยหนึ่งอย่าง (LED, flag, publish, log marker)
2. ยืนยันว่า Bitstream Studio (หรือ `web-app/`) สะท้อนผล
3. เทียบกับ behavior WHEN/THEN จากโมดูล 3

---

## ฝึกเติม/แล็บ (4) — Lab D: Latency note (แนะนำ)

1. เลือกจุดวัดหนึ่งจุด (เช่น stimulus → first log line)
2. ทำ 3 รอบ จดค่าโดยประมาณ
3. เดาสาเหตุหน่วง 1 ข้อ (task period / scene rate / UI)
4. กรอกใน checklist

---

## ฝึกเติม/แล็บ (5) — Lab E: ทางเลือกเสริม

- เปรียบเทียบ Path A (Simulator) กับ Path B (Board) บนสคริปต์เดียวกัน
- ถ้ามี GLB จากโมดูล 3 — โหลดประกอบฉากแล้วจดว่าภาพช่วยสาธิตอะไร (ไม่แทน sensor truth)

**E1 Hackathon web-app `ex05` (แนะนำ)**

1. Serve โฟลเดอร์ `web-app/` แล้วเปิด `ex05_bmi270_orientation.html`
2. ยืนยัน badge เป็น `connected` และมี `route:`
3. เปิด BMI270 **Euler** และ/หรือ **Quaternion** ใน publish mask
4. เอียงบอร์ด หรือสลับ scene Motion — horizon + ° ต้องขยับ
5. แคปหน้าจอ **คู่กับ** แผง BMI270 ใน Studio; จด `source:` และ `mask 0x…`

---

## เช็กความเข้าใจ — ไล่อาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. Link ไม่ขึ้น — ควรตรวจอะไรก่อน
2. มีกราฟแต่กระตุ้นแล้วเงียบ — สาเหตุที่พบบ่อยคืออะไร
3. ex05 ค้าง *waiting for orientation* — ต้องแก้อะไร
4. ค่า latency สุ่มมาก — ควรวัดด้วยวิธีใดแทน

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] Lab A–C ผ่าน
- [ ] cosim-checklist.md กรอกครบ
- [ ] หลักฐาน input + output (สกรีนช็อต/คลิป/log ของคุณเอง)
- [ ] (แนะนำ) Lab D latency และ Lab E / E1 (`ex05`)

พร้อมแล้ว ไปต่อ **โมดูล 5 — ท่อ telemetry, MQTT บน Twin และ fault injection**

[บทเรียนโมดูล 5 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## แหล่งที่มา

"บทเรียน 4.2 — แล็บ: I/O ครบวงจรแบบ co-simulation" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
