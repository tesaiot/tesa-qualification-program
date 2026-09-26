---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 8.2 — แล็บ Capstone: มินิโปรเจกต์"
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

# บทเรียน 8.2 — แล็บ Capstone: มินิโปรเจกต์

## สร้างมินิโปรเจกต์บนบอร์ดจริงที่รวม sensor, RTOS และ MQTT หรือ BLE สาธิตสามสถานการณ์ และส่งมอบ README ที่ทำซ้ำได้

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 8 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. ส่งมอบมินิโปรเจกต์บนบอร์ดจริงที่ผ่านเกณฑ์ขั้นต่ำทั้งห้าข้อ
2. สาธิตครบสามสถานการณ์ (Normal, Stimulus, Command) พร้อมหลักฐาน
3. เขียน README ที่ผู้อื่น build/flash ซ้ำได้โดยไม่เปิดเผยรหัสผ่าน

---

## ก่อนเริ่ม

- [ ] Lab หลักโมดูล 2–7 ผ่านเกณฑ์ขั้นต่ำ (อย่างน้อย path ที่จะใช้ใน Capstone)
- [ ] โปรเจกต์รวมโค้ดได้บนเครื่องคุณ
- [ ] Broker + Wi‑Fi **หรือ** โฮสต์ BLE ที่เลือกใช้
- [ ] เปิด capstone-brief.md สำหรับกรอก

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่ต่อสาธารณะ** — ให้ใช้ GATT explorer ทั่วไปแทน · snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส — ดูรายละเอียดที่หมายเหตุต้นบทเรียน [บทเรียน 8.1](../l01-capstone-and-resources/README.md)

---

## ดูของจริงก่อน — ลำดับการสร้างที่แนะนำ

1. **Architecture (30–45 นาที)** — กรอกตาราง Task / Topic / BLE ใน capstone brief
2. **Sensor + indication** — อ่านช่วงเวลาคงที่ + LED/UART
3. **RTOS wiring** — แยก task, ใส่คิวถ้ามี producer/consumer
4. **Connectivity** — เลือก MQTT และ/หรือ BLE แล้วทำให้ลิงก์และคำสั่งทำงาน
5. **Hardening** — ไม่ hardcode secret; ทดสอบกระตุ้นเซ็นเซอร์ / ส่งคำสั่ง / ถอดสายสั้น ๆ
6. **Evidence** — README + สกรีนช็อต/คลิป + (แนะนำ) dashboard บนโฮสต์

---

## แนวคิด — เกณฑ์ผ่านขั้นต่ำ

| เกณฑ์ | ต้องมี |
|---|---|
| Build + flash ได้จาก README ของคุณ | ใช่ |
| ≥ 2 Task ทำงานจริง | ใช่ |
| Sensor path + สถานะบน LED/UART | ใช่ |
| MQTT **หรือ** BLE ใช้งานได้ + รับคำสั่ง/ยืนยันลิงก์ | ใช่ |
| ไม่ฝังรหัสผ่านในไฟล์ส่งสาธารณะ | ใช่ |

**Stretch goals (ไม่บังคับ):** ใช้ทั้ง MQTT และ BLE · threshold → alert publish/notify · mutex ถูกต้องบนบัสร่วม · `to_twin` queue หรือ topic แยก

---

## ฝึกเติม/แล็บ — สร้างมินิโปรเจกต์

ครอบคลุมองค์ประกอบต่อไปนี้:

- Sensor path + indication
- ≥ 2 FreeRTOS tasks
- Connectivity: **MQTT และ/หรือ BLE** (อย่างน้อยหนึ่งเส้น พร้อมรับคำสั่งหรือยืนยันลิงก์)
- README ที่ผู้อื่นทำซ้ำได้
- หลักฐานสาธิต (รูป / คลิป / dashboard)

---

## ฝึกเติม/แล็บ — สาธิตสามสถานการณ์ (ทดสอบให้ครบทั้งสาม)

1. **Normal** — ค่าเซ็นเซอร์ไหล, LED/UART ปกติ, telemetry เข้าโฮสต์ (MQTT subscriber และ/หรือ BLE dashboard)
2. **Stimulus** — เปลี่ยนอุณหภูมิ/ขยับบอร์ด/หมุน POT → เห็นค่าหรือ event เปลี่ยน
3. **Command** — จาก PC/phone ส่งคำสั่ง (MQTT topic หรือ BLE write) → อุปกรณ์ตอบสนอง

---

## เช็กความเข้าใจ — เตรียม deliverables

ตรวจตัวเองก่อนว่าครบตามนี้หรือยัง:

1. โฟลเดอร์/ลิงก์โปรเจกต์
2. README: วิธี build, flash, Wi‑Fi/broker หรือ BLE host แบบไม่เปิดเผยรหัส, topic/UUID ที่ใช้
3. capstone-brief.md กรอกครบ
4. แผนภาพหรือตาราง Task
5. หลักฐานสาธิต 3 สถานการณ์
6. ยืนยันไม่มี secret ในไฟล์สาธารณะ

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่าครบทั้ง 5 เกณฑ์ผ่านขั้นต่ำ และมี deliverables ครบตามเช็กลิสต์

หลังส่ง Capstone แล้ว คุณจบหลักสูตรนี้ — เส้นทางต่อไป (นอกหลักสูตรนี้): **หลักสูตร Digital Twin / Product Design** ใช้สตรีมและโครงสร้างที่เตรียมใน Capstone เป็นอินพุต

[กลับไปที่หน้าหลักสูตร](../../README.md)

---

## แหล่งที่มา

"บทเรียน 8.2 — แล็บ Capstone: มินิโปรเจกต์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
