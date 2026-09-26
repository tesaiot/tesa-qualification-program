---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.1 — ทดสอบ end-to-end บน Digital Twin"
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

# บทเรียน 6.1 — ทดสอบ end-to-end บน Digital Twin

## เกณฑ์ผ่านขั้นต่ำของ Capstone การวิเคราะห์ log ทีละชั้น โจทย์จากโดเมนจริง และกรณีศึกษา Smart Environmental Monitor

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 6 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตรวจระบบ Twin แบบ end-to-end ตามเกณฑ์ผ่านขั้นต่ำ (virtual device + script, co-sim, visualization, MQTT, README, ตารางเทส ≥ 3 เคส)
2. วิเคราะห์ log ทีละชั้น โดยเก็บ log ฝั่งเฟิร์มแวร์และฝั่งโฮสต์ในรอบเดียวกัน
3. แปลงโจทย์จากโดเมนจริง (IoT ทั่วไป บ้าน โรงงาน สุขภาพ) ลงท่อ Twin ชุดเดียวกัน

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 5.2 — แล็บ M05](../../m05-telemetry-cloud/l02-lab/README.md) มาแล้ว
- บทเรียนนี้คือ **Capstone** — รวมโมดูล 1–5 เป็นระบบที่สาธิตซ้ำได้

> **Key phrase**: Capstone หลักสูตรนี้ = *เลือกและเชื่อมชิ้นที่ทำมาแล้ว* ให้มีตารางผ่าน/ไม่ผ่าน — ไม่ใช่เขียน Twin ใหม่ทั้งก้อน

---

## ดูของจริงก่อน — สิ่งที่คุณมีอยู่แล้วจากแต่ละโมดูล

| โมดูล | Lab focus | นำมาใช้ในบทเรียนนี้ |
|---|---|---|
| 1 | แผนที่ Twin / backend XOR | อธิบายสถาปัตยกรรมเดโม |
| 2 | Studio workspace / Link | bring-up ที่ทำซ้ำได้ |
| 3 | Virtual device + event script (+ GLB) | แหล่งกระตุ้นเซ็นเซอร์ |
| 4 | Co-sim I/O · optional ex05 | พิสูจน์เฟิร์มแวร์ ↔ Twin |
| 5 | Telemetry · MQTT · ex08/ex09 | ท่อออก dashboard / cloud |
| **6** | **E2E mini-project** | รวม + ตารางเทส + README |

ถ้าชิ้นใดยังไม่ผ่านเกณฑ์ขั้นต่ำ ให้ซ่อมก่อนขยายฟีเจอร์ใน Capstone

---

## แนวคิด — เส้นทาง End-to-End บน Twin

```text
[1 Stimulus]   M03 event script / scene / switch / tilt
        ▼
[2 Firmware]   read → decide → act (LED / flag / publish)
        ▼
[3 Twin / Studio visualization]   telemetry panel · 3D · status
        ├──► [4a Live Data dashboard]  e.g. web-app ex06
        └──► [4b MQTT]  broker + pub/sub  e.g. ex09 / ex15
```

| ขั้น | หลักฐานที่ยอมรับ |
|---|---|
| 1 Stimulus | โน้ตสคริปต์/เวลา + สกรีนช็อตก่อน–หลัง |
| 3 Studio | กราฟ / สถานะ / 3D สอดคล้อง |
| 4a หรือ 4b | consumer ชั้นนอก **อย่างน้อยหนึ่งท่อ** |

---

## ตัวอย่างสมบูรณ์ — เกณฑ์ผ่านขั้นต่ำของ Capstone

| เกณฑ์ | ต้องมี |
|---|---|
| Virtual device + event script (หรือ timeline เทียบเท่า) | ใช่ |
| Firmware co-sim ทำงาน (Simulator และ/หรือ Board) | ใช่ |
| Visualization ใน Studio แสดงค่า/สถานะ | ใช่ |
| MQTT publish **หรือ** subscribe อย่างน้อยหนึ่งทาง | ใช่ |
| README วิธีรันซ้ำ (bring-up → demo → teardown) | ใช่ |
| ตารางเทส E2E ผ่านอย่างน้อย **3 เคส** | ใช่ |
| ไม่ฝัง secret (Wi‑Fi / broker password) ในไฟล์ส่ง | ใช่ |

งานต่อยอด (ไม่บังคับ): ทั้ง Live Data **และ** MQTT บนเดโมเดียวกัน · fault/reconnect เคส · GLB จากโมดูล 3

---

## แนวคิด — วิเคราะห์ log ทีละชั้น

```text
1. Firmware still alive?           → heartbeat / UART / LED
2. Twin / Studio session up?       → Link · backend XOR
3. Stimulus actually applied?      → M03 script / scene
4. Value reached firmware?         → log read path
5. Firmware decided / wrote?       → log / LED / publish
6. Studio shows change?            → correct panel
7. Live Data consumer OK?          → ex06 / ex08 connected
8. Broker up + topic match?        → Start broker · ex09/ex15
9. Payload schema OK?              → fields / units
```

> **Key phrase**: แก้ทีละชั้น — แคป log ทั้งฝั่งเฟิร์มแวร์และโฮสต์ในรอบเดียวกัน

---

## แนวคิด — โจทย์จากโดเมนจริง (ท่อเดียวกันทุกโลก)

โครง E2E เหมือนกันทุกโดเมน — ที่ต่างคือ *เรื่องราว*, เกณฑ์แจ้งเตือน, และสิ่งที่ผู้ชมเข้าใจว่า "ทำไมต้องมี Twin" — **ไม่ต้องมีฮาร์ดแวร์เฉพาะโดเมน**

| โดเมน | "ฮีโร่" ที่เล่า | เซ็นเซอร์หลักในแล็บ | Consumer แนะนำ | Event ตัวอย่าง |
|---|---|---|---|---|
| IoT ทั่วไป | โหนดขอบ ↔ คลาวด์ | SHT40 + state | ex06 + ex15 | `threshold_exceeded` |
| ในบ้าน | ห้องสบาย / ปลอดภัย | SHT40 + switch | ex06 + MQTT cmd | `motion_detected` |
| โรงงาน | เครื่องจักร + alarm | temp/pressure + BMI270 | ex06 + ex08 + ex15 | `overtemp` / `tilt` |
| สุขภาพ (จำลอง) | ลิงก์เฝ้าระวัง | BMI270 + SHT40 | ex05 + ex08 + ex09 | `posture_alert` |

> **ขอบเขตโดเมนสุขภาพ**: ใช้ค่าจำลองเท่านั้น ห้ามอ้างว่าผ่านมาตรฐานการแพทย์ ห้ามใช้ข้อมูลคนไข้จริง

---

## แนวคิด — เลือกโดเมนอย่างไร

| ถ้าทีมสนใจ… | เลือกโดเมน | จุดเด่นในการสาธิต |
|---|---|---|
| อุปกรณ์เชื่อมคลาวด์ทั่วไป | IoT | fleet / gateway / dashboard |
| ชีวิตประจำวันในที่อยู่อาศัย | Home | comfort · ความปลอดภัยในบ้าน |
| สายการผลิต / เครื่องจักร | Industrial | threshold · operator command · downtime |
| การดูแลสุขภาพ / wellness (จำลอง) | Health | orientation · สัญญาณชีพจำลอง · privacy |

> **Key phrase**: โดเมน = *ภาษาของผู้ใช้* · ท่อ Twin = *ภาษาของวิศวกรเฟิร์มแวร์* — Capstone ต้องพูดได้ทั้งสองภาษา

---

## ตัวอย่างสมบูรณ์ — กรณีศึกษา Smart Environmental Monitor

| ชิ้น | ตัวอย่างในแล็บ |
|---|---|
| เซ็นเซอร์ | อุณหภูมิ / ความชื้น (SHT40) และ/หรือ pressure · สวิตช์หรือโหมด |
| พฤติกรรม | เกินเกณฑ์ → เปลี่ยน state / LED / event |
| Twin | Virtual device + script Lab Quiet → Warm / Alert |
| Cloud sim | MQTT telemetry topic + คำสั่งโหมดกลับ (อย่างน้อยหนึ่งทาง) |
| External proof | `ex06` (multi-sensor Live Data) และ/หรือ `ex15` (WS vs MQTT) |

```text
[Event script] ──stimulus──► [Virtual sensors] ──► [Firmware co-sim]
                                                          │
                              ┌───────────────────────────┴──────────┐
                              ▼                                      ▼
                      [Bitstream Studio]                     [MQTT broker]
                              │                                      │
                       web-app ex06                    ex09 / ex15 / gauges
```

---

## ตัวอย่างสมบูรณ์ — สามสถานการณ์สาธิต (required)

| # | ชื่อ | สิ่งที่ผู้ชมต้องเห็น |
|---|---|---|
| 1 | Normal | ค่า environmental อัปเดตสม่ำเสมอบน Studio + consumer |
| 2 | Stimulus / threshold | สคริปต์หรือสวิตช์ทำให้ state/event เปลี่ยนชัด |
| 3 | Command or fault | คำสั่ง MQTT เข้าอุปกรณ์/Twin **หรือ** ตัด broker/สตรีมสั้น ๆ แล้วกู้คืน |

**หลักฐานโฮสต์แนะนำ:** `ex06_dashboard.html` (Live Data — การ์ดหลายเซ็นเซอร์) และ `ex15_ws_mqtt_dashboard.html` (สลับ MQTT :8883 / WebSocket :9998)

> ex15 ช่วยสอนว่า **WS bus ≠ MQTT broker** — อย่าสลับ transport กลางการสาธิตโดยไม่บอก

---

## แนวคิด — สิ่งที่ต้องส่งมอบ

| ชิ้น | คำอธิบาย |
|---|---|
| โปรเจกต์ / ลิงก์ | เฟิร์มแวร์ + twin assets ที่ใช้ |
| README | วิธีรันซ้ำทีละขั้น · ระบุโดเมนที่เลือก |
| e2e-case-brief.md | กรอกครบ 3 เคส + โดเมน |
| หลักฐานเดโม | สกรีนช็อต/คลิป Studio + ex06 และ/หรือ ex15/ex09 |
| (ถ้ามี) script / device model | จากโมดูล 3 ที่ล็อกเวอร์ชันแล้ว |

---

## ตัวอย่างสมบูรณ์ — โครง README ที่แนะนำ

```text
# <Project name> (Course 2 Capstone)
Domain: IoT | Home | Industrial | Health-sim | Other: …

## Hardware / path
Simulator | Board + HEX version | Studio version

## Bring-up
1. Open workspace … 2. Link backend (one only) …
3. Start broker (if MQTT) … 4. Serve web-app …

## Demo script
1. Normal — … 2. Stimulus — … 3. Command / fault — …

## Topics / payloads
(no passwords · no personal health identifiers)
```

---

## ฝึกเติม/แล็บ

[แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin](../l02-lab/README.md)

- เลือกโดเมนหนึ่งข้อ แล้วแมปลงเครื่องมือในแล็บที่มีอยู่
- รวมชิ้นส่วนจากโมดูล 1–5 ให้ครบตามเกณฑ์ผ่านขั้นต่ำ
- สาธิตครบสามสถานการณ์พร้อมหลักฐาน แล้วเขียน README ที่รันซ้ำได้

---

## เช็กความเข้าใจ

1. ข้อใดอยู่ในเกณฑ์ผ่านขั้นต่ำของ Capstone (เลือกได้หลายข้อ)
2. หลักของการวิเคราะห์ log ในบทเรียนนี้คือข้อใด
3. ถ้าเลือกโดเมน "โรงงาน" สำหรับ Capstone ต้องเตรียมฮาร์ดแวร์อย่างไรตามบทเรียน

---

## ไปต่อ

หลังจบโมดูลนี้ คุณควรพาโปรเจกต์จากระดับ "รันบน Twin ได้" ไปสู่ระดับ **มีชุดทดสอบที่ทำซ้ำได้**

| ทิศทางถัดไป | ทำอะไรต่อ |
|---|---|
| ยืนยันบนฮาร์ดแวร์เต็มรูป | กลับหลักสูตร Firmware SDK — flash · Wi‑Fi · MQTT/BLE จริง |
| ขยาย visualization / 3D | เส้นทาง Blender ต่อจากโมดูล 3 |
| ขยาย cloud | broker ของแล็บ → นโยบายคลาวด์ขององค์กร (อย่า commit secret) |

---

## แหล่งที่มา

"บทเรียน 6.1 — ทดสอบ end-to-end บน Digital Twin" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
