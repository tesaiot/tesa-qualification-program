---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.2 — แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin"
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

# บทเรียน 6.2 — แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin

## ล็อกสถาปัตยกรรม ประกอบเดโมที่รันได้ รันเทส E2E สามเคส ฝึกไล่ log และจัดแพ็กส่งต่อ

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 6 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. ประกอบเดโม stimulus → firmware → Studio → dashboard/MQTT ที่รันซ้ำได้
2. รันเทส E2E อย่างน้อยสามเคส (Normal, Stimulus, Command/fault) และบันทึกผ่าน/ไม่ผ่านพร้อมเหตุผล
3. จัดแพ็ก README และหลักฐานให้ผู้อื่นรันซ้ำได้

---

## ก่อนเริ่ม

- [ ] Lab โมดูล 2 Link เสถียร
- [ ] Lab โมดูล 3 มี virtual device + event script (หรือเทียบเท่า)
- [ ] Lab โมดูล 4 co-sim ผ่านอย่างน้อย Path เดียว
- [ ] Lab โมดูล 5 เคย Start broker + subscriber ได้
- [ ] โฟลเดอร์ผลงาน + `lab-notes/`

---

## ดูของจริงก่อน — เลือกโดเมนเรื่องราว

เริ่มจาก **Smart Environmental Monitor** (IoT/สภาพแวดล้อม) หรือแมปเป็นโดเมนอื่น:

| Domain | เน้นเล่า | เซ็นเซอร์หลัก | Evidence เสริม |
|---|---|---|---|
| IoT | โหนด ↔ คลาวด์ | SHT40 + state | ex06 + ex15 |
| Home | ห้องสบาย / ปลอดภัย | SHT40 + switch | ex06 + MQTT cmd |
| Industrial | alarm บนไลน์ | temp/IMU | ex06 + ex08 + ex15 |
| Health-sim | ลิงก์เฝ้าระวัง (จำลอง) | BMI270 + SHT40 | ex05 + ex08 + ex09 |

กรอกรายละเอียดใน e2e-case-brief.md

---

## ฝึกเติม/แล็บ (1) — Lab A: Lock architecture

1. เลือก **โดเมน** (IoT / Home / Industrial / Health-sim)
2. วาด/เขียนแผนภาพ 4 ขั้นจากบทเรียน แล้วใส่ชื่อเหตุการณ์ตามโดเมน
3. ระบุ Path: Simulator / Board / Both
4. ระบุ topic MQTT และ consumer หน้าเว็บที่จะใช้เป็นหลักฐาน
5. คัดลอกโครง README จากบทเรียนลงโปรเจกต์ (ใส่บรรทัด Domain)

**Pass when:** เพื่อนในทีมอ่านแล้วรู้โดเมน + เครื่องมือที่จะเปิดก่อน โดยไม่ถามเพิ่ม

---

## ฝึกเติม/แล็บ (2) — Lab B: Assemble the running demo

1. Bring-up Studio (backend เดียว) + co-sim
2. รัน event script / scene ของคุณ
3. ยืนยันค่าบน Studio
4. Serve `web-app/` → เปิด **ex06** ให้เห็นเซ็นเซอร์ที่เกี่ยวข้อง
5. Start broker → publish (และ/หรือ subscribe) → ยืนยันบน **ex15** หรือ **ex09**

**Pass when:** เดโม Normal รันได้ต่อเนื่อง ≥ 1 นาทีโดยไม่หลุด Link เอง

---

## ฝึกเติม/แล็บ (3) — Lab C: Three E2E test cases

รันและกรอกตารางใน case brief:

| เคส | อย่างน้อยต้องพิสูจน์ |
|---|---|
| Normal | telemetry อัปเดตบน Studio + consumer |
| Stimulus | threshold / switch / script เปลี่ยน state หรือ event ชัด |
| Command / fault | คำสั่ง MQTT **หรือ** ตัด broker/สตรีมสั้น ๆ แล้วกู้คืน |

**Pass when:** อย่างน้อย 3 แถวมีผลจริง + ผ่าน = ใช่ (หรือ Fail พร้อมเหตุผลและ workaround ที่ยอมรับได้)

---

## ฝึกเติม/แล็บ (4) — Lab D: Log triage drill (แนะนำ)

จงใจทำให้พังหนึ่งอย่าง (ปิด broker / หยุด script / เปิดผิด panel) แล้ว:

1. ไล่ชั้นตามลำดับในบทเรียน 6.1
2. จดชั้นที่พบปัญหา
3. แก้กลับมาเดโมเขียว

**Pass when:** มีบรรทัดใน case brief ส่วนปัญหา/การแก้

---

## ฝึกเติม/แล็บ (5) — Lab E: Package for handoff

- [ ] README รันซ้ำได้
- [ ] case brief กรอกครบ
- [ ] หลักฐานสกรีนช็อต/คลิปของคุณเอง (Studio + ex06 และ MQTT consumer)
- [ ] ไม่มี password ในไฟล์ส่ง
- [ ] รายการตรวจจาก course-package.md

---

## เช็กความเข้าใจ — ไล่อาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. เดโมยาวแล้วหลุด — ควรกลับไปตรวจอะไร
2. ex06 ว่างแต่ Studio มีค่า — ควรตรวจอะไรก่อน
3. MQTT ว่าง — สาเหตุที่พบบ่อยคืออะไร
4. Stimulus ไม่เห็นบน consumer — ควรตรวจอะไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] Lab A–C, E ผ่าน
- [ ] (แนะนำ) Lab D
- [ ] ลิงก์/โฟลเดอร์โปรเจกต์ที่พร้อมส่งต่อ ไม่มี secret ในไฟล์

นี่คือแล็บสุดท้ายของหลักสูตร — หลังส่งงาน คุณมีระบบ Twin ที่ทดสอบ E2E ได้และเล่าได้ว่าท่อเดียวกันรองรับโดเมนอื่นได้อย่างไร

[กลับไปที่หน้าหลักสูตร](../../README.md)

---

## แหล่งที่มา

"บทเรียน 6.2 — แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
