---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — แล็บ: ท่อ telemetry และ MQTT บน Twin"
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

# บทเรียน 5.2 — แล็บ: ท่อ telemetry และ MQTT บน Twin

## ออกแบบ topic ตรวจคุณภาพ Live Data ด้วย ex08 ตั้ง broker แล้ว subscribe ด้วย ex09 และทดลอง lossy/reconnect

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 5 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. ออกแบบ topic สำหรับ Telemetry/State/Event และตรวจฟิลด์กับหน่วยบน dashboard
2. ตั้ง broker ใน Studio แล้วทำ pub/sub ได้อย่างน้อยหนึ่งคู่
3. ทดลอง lossy / disconnect / schema break อย่างน้อยหนึ่งเคสและบันทึกผล

---

## ก่อนเริ่ม

- [ ] Lab โมดูล 4 bring-up ผ่าน (Link เสถียร · รู้ Simulator XOR Bitstream)
- [ ] โฟลเดอร์ Hackathon มี `web-app/`
- [ ] รู้วิธี Serve Web App Folder over HTTP (จากโมดูล 4)
- [ ] โฟลเดอร์ `lab-notes/` สำหรับหลักฐาน

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Classify & design topics | เพื่อนในทีมอ่าน topic แล้วเดาชนิดข้อมูลถูก |
| Lab B — Live Data quality with ex08 | อธิบายได้ว่า stale เป็น host-side Event และ origin สอดคล้องโหมด |
| Lab C — MQTT broker + ex09 | message count ≥ 1 และ JSON ตรงชนิดที่ตั้งใจ |
| Lab E — Lossy / reconnect (แนะนำ) | ระบุพฤติกรรมที่เห็นโดยไม่เดา |

---

## ฝึกเติม/แล็บ (1) — Lab A: Classify & design topics

ออกแบบ (บนกระดาษหรือใน lab notes):

1. **Telemetry** — topic + ตัวอย่าง JSON 1 ก้อน + อัตราโดยประมาณ
2. **State** — topic + เมื่อไรจะส่ง (เปลี่ยนโหมด / LED / Link)
3. **Event** — topic หรือชื่อ event + เงื่อนไขสั้น ๆ

```text
device/<id>/devkit-twin/telemetry
device/<id>/state
device/<id>/event/<name>
```

---

## ฝึกเติม/แล็บ (2) — Lab B: Live Data quality with ex08

1. Link Studio (โหมดเดียว)
2. Serve `web-app/` → เปิด `ex08_stale_and_route.html`
3. จด `route`, `COM open`, `last origin`
4. ทำให้เซ็นเซอร์อย่างน้อยหนึ่งตัวเข้า **stale** แล้วกลับ **fresh**
5. แคป event log + pills

---

## ฝึกเติม/แล็บ (3) — Lab C: MQTT broker + ex09

1. ใน Bitstream Studio: **Start broker**
2. เปิด `ex09_mqtt_subscriber.html` — รอ `connected`
3. Publish ไป topic ที่หน้าเว็บ subscribe (ค่าเริ่มต้น `device/devkit-twin-01/devkit-twin/telemetry`)
4. ยืนยัน Last payload ตรงฟิลด์และหน่วย
5. แคปคู่: แหล่ง publish + หน้า ex09

---

## ฝึกเติม/แล็บ (4) — Lab D: Pipeline / schema drill (แนะนำ)

เลือกอย่างน้อยหนึ่ง:

- ตัดฟิลด์จาก payload แล้วดูว่า subscriber/dashboard พังตรงไหน
- ส่งค่าหน่วยผิดโดยตั้งใจ แล้วจดว่า UI "ยังสวยแต่ผิดความหมาย"
- เปิด ex14 ลอง QoS + retain บน `lab/qos-demo` แล้วให้เพื่อนเปิด subscriber หลังคุณ retain

---

## ฝึกเติม/แล็บ (5) — Lab E: Lossy / reconnect (แนะนำ)

เลือกอย่างน้อยหนึ่งเคส แล้วกรอกตารางใน lab notes:

| เคส | ตัวอย่างการทำ |
|---|---|
| Stop / Start broker สั้น ๆ | ดู ex09 `reconnecting` → `connected` |
| หยุด publisher ชั่วคราว | ดูช่องว่าง · หรือ ex08 stale |
| ปิดแท็บ ex09 แล้วเปิดใหม่ | ถ้ามี retain บน state topic — ได้ค่าล่าสุดหรือไม่ |

---

## เช็กความเข้าใจ — ไล่อาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. ex09 ค้าง connecting — ควรตรวจอะไรก่อน
2. connected แต่ Waiting for messages — สาเหตุที่พบบ่อยคืออะไร
3. Live Data ดี MQTT ว่าง — ควรแก้อะไรก่อน (เฟิร์มแวร์หรือ broker/topic)
4. origin สับสน — เกิดจากอะไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] Lab A–C ผ่าน
- [ ] Lab E (หรืออย่างน้อย Lab D ถ้าเวลาไม่พอ)
- [ ] telemetry-mqtt-lab-notes.md กรอกครบ
- [ ] หลักฐานสกรีนช็อตของคุณเอง: ex08 + ex09 (+ schema/lossy ตามที่ทำ)

พร้อมแล้ว ไปต่อ **โมดูล 6 — การรวมระบบและการทดสอบ**

[บทเรียนโมดูล 6 →](../../m06-integration/l01-system-integration-testing/README.md)

---

## แหล่งที่มา

"บทเรียน 5.2 — แล็บ: ท่อ telemetry และ MQTT บน Twin" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
