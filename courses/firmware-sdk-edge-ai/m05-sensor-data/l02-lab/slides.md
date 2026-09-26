---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI"
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

# บทเรียน 5.2 — แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI

## อ่านเซ็นเซอร์สองชนิดด้วย task คาบคงที่ กรองหรือ normalize สร้างหน้าต่างข้อมูล แล้วเลือกต่อยอด (fusion, host telemetry หรือ event)

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 5 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. อ่านเซ็นเซอร์อย่างน้อยสองชนิดด้วย task คาบเวลาคงที่
2. กรองหรือ normalize ค่า และสร้างหน้าต่างข้อมูลที่ให้เวกเตอร์สรุปอย่างน้อยหนึ่งครั้งต่อวินาที

---

## ก่อนเริ่ม

- [ ] ผ่านโมดูล 3 (UART) และโมดูล 4 (สร้าง task ได้)
- [ ] บอร์ดมีเซ็นเซอร์ตามคิตที่ใช้
- [ ] รู้ว่าเซ็นเซอร์ใดถูก enable ในเฟิร์มแวร์/โปรเจกต์ของคุณ

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส — ดูรายละเอียดที่หมายเหตุต้นบทเรียน [บทเรียน 5.1](../l01-sensor-data-for-edge-ai/README.md)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Bring-up สองเซ็นเซอร์ (required) | ได้ค่าที่สมเหตุสมผลทั้งสองชนิดบน terminal |
| Lab B — task คาบคงที่ (required) | คาบอ่านสม่ำเสมอโดยไม่ busy-wait |
| Lab C — Filter + normalize (required) | อธิบายได้ว่า filter ลด noise อย่างไร |
| Lab D — Feature window (required) | ได้เวกเตอร์สรุปอย่างน้อยหนึ่งครั้งต่อวินาที |
| Lab E — เลือกต่อยอด (แนะนำ) | ทำครบหนึ่งตัวเลือกและมีหลักฐาน |

---

## ฝึกเติม/แล็บ (1) — Lab A: Bring-up two sensors

1. `sensor_sht40_startup` แล้วอ่าน `temperature` / `humidity` พิมพ์ UART
2. `sensor_bmi270_startup` (ถ้ายังไม่ถูก start จาก boot) แล้วอ่าน `acc_*`
3. ตรวจ `sensor_*_is_ready` ก่อนอ่าน

---

## ฝึกเติม/แล็บ (2) — Lab B: Fixed-rate sample task

สร้าง task อ่านเซ็นเซอร์ด้วย `vTaskDelayUntil` (เช่น SHT40 ทุก 500–1000 ms **หรือ** BMI270 ทุก 40 ms) แล้วบันทึกว่าเลือกคาบเท่าไรและทำไม

```c
TickType_t last = xTaskGetTickCount();
const TickType_t period = pdMS_TO_TICKS(40);
for (;;) {
    (void)sensor_bmi270_read(&imu);
    vTaskDelayUntil(&last, period);
}
```

---

## ฝึกเติม/แล็บ (3) — Lab C: Filter + normalize

1. ทำ EMA (หรือ median หน้าต่างสั้น) บนอุณหภูมิหรือแกน accel
2. Normalize ค่าอย่างน้อยหนึ่งช่องไปช่วงที่กำหนด (เช่นประมาณ [-1, 1] หรือ 0..1)
3. พิมพ์ทั้งค่าดิบและค่าหลังประมวลผล

---

## ฝึกเติม/แล็บ (4) — Lab D: Feature window

1. สร้าง ring buffer / window อย่างน้อย **16–32** ตัวอย่างจาก BMI270 **หรือ** อนุกรมอุณหภูมิ
2. เมื่อหน้าต่างเต็ม ให้คำนวณอย่างน้อยหนึ่งฟีเจอร์ (เช่น mean, variance, max−min)
3. พิมพ์ฟีเจอร์ทาง UART เป็นคาบ

---

## ฝึกเติม/แล็บ (5) — Lab E: เลือกต่อยอดหนึ่งอย่าง (แนะนำ)

**E1 Fusion orientation** — `cm55_imu_fusion_bridge_push_raw_components` + `get_latest_result` แล้วพิมพ์ pitch/roll หรือ `orientation`

**E2 Host telemetry** — Flash/เชื่อมตามชุดที่ใช้ แล้วเปิด Bitstream Studio หรือ Hackathon `web-app` ยืนยันว่าค่าเซ็นเซอร์บนโฮสต์ขยับตรงกับบอร์ด

**E3 Condition event** — เมื่อฟีเจอร์หรือ EMA เกินเกณฑ์ → เปิด LED + ข้อความ `EVENT ...`

---

## เช็กความเข้าใจ — สรุปรายงานสั้น (8–12 บรรทัด)

เตรียมคำตอบก่อนเขียนรายงาน:

1. เซ็นเซอร์ที่ใช้ + คาบ sampling
2. วิธี filter / normalize ที่เลือกใช้
3. ขนาดหน้าต่าง + ฟีเจอร์ที่คำนวณ
4. (ถ้ามี) ผล fusion หรือภาพหน้าจอโฮสต์
5. สิ่งที่จะส่งต่อไป cloud ในโมดูล 6 (payload แนวคิด)

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] Lab A–D ผ่าน
- [ ] Lab E อย่างน้อย 1 ข้อ
- [ ] กรอกตารางใน [sensor-ai-prep.md](../l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md)
- [ ] รายงานสั้นครบ

พร้อมแล้ว ไปต่อ **โมดูล 6 — MQTT และ MQTTs สำหรับสื่อสารกับคลาวด์**

[บทเรียนโมดูล 6 →](../../m06-mqtt/l01-mqtt-and-mqtts/README.md)

---

## แหล่งที่มา

"บทเรียน 5.2 — แล็บ: สตรีมเซ็นเซอร์และหน้าต่างข้อมูลพร้อม AI" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
