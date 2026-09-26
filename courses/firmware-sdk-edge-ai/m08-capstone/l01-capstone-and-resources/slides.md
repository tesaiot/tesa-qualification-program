---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 8.1 — วางแผน Capstone และใช้แผนที่เอกสาร"
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

# บทเรียน 8.1 — วางแผน Capstone และใช้แผนที่เอกสาร

## เกณฑ์ผ่านของ Capstone แผนที่ชีตและ API ของหลักสูตร สถาปัตยกรรมอ้างอิง และสถานการณ์สาธิตสามแบบ

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 8 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. วางแผน Capstone ให้ครอบคลุมเกณฑ์ผ่านขั้นต่ำ: build/flash, ≥ 2 FreeRTOS tasks, sensor path + LED/UART และ connectivity อย่างน้อยหนึ่งเส้น
2. ใช้แผนที่เอกสารของหลักสูตรหาชีตหรือบทเรียนที่ตอบความต้องการแต่ละข้อ
3. ออกแบบสถานการณ์สาธิตสามแบบ (Normal, Stimulus, Command) ที่พิสูจน์ระบบได้

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 7.2 — แล็บ M07](../../m07-ble/l02-lab/README.md) มาแล้ว
- ใช้บอร์ดจริง: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL)
- บทเรียนนี้ **รวมทักษะจากโมดูล 1–7** เป็นมินิโปรเจกต์ — ไม่ใช่เนื้อหาใหม่

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส (`cm55_*`, `sensor_*`, `led_controller_*`, `cm33_mqtt_*`, `cm55_ble_*`) — อ่านเป็นแนวคิดและลำดับการเรียกใช้ **โฮสต์ `ble-flet` ก็ยังไม่เผยแพร่ต่อสาธารณะ** ให้ใช้ GATT explorer ทั่วไปแทน

---

## ดูของจริงก่อน — Capstone คือการเลือกและเชื่อมชิ้นส่วนที่มีแล้ว

| โมดูล | แล็บ | สิ่งที่ได้เมื่อผ่าน |
|---|---|---|
| 1–2 | แผนที่โดเมน + Create/Build/Flash/Debug | โปรเจกต์รันบนบอร์ด |
| 3–4 | GPIO/UART + Multi-task | Driver API + FreeRTOS พื้นฐาน |
| 5 | Sensor + filter + window | ข้อมูลพร้อม AI / twin |
| 6–7 | Wi‑Fi/MQTT + BLE | เชื่อม cloud หรือ local |
| **8** | **Capstone mini-project** | **ระบบรวมที่สาธิตและทำซ้ำได้** |

> **Key phrase**: Capstone คือการ *เลือกและเชื่อม* ชิ้นส่วนที่มีแล้ว — ไม่ใช่เขียนทุกอย่างใหม่จากศูนย์

---

## แนวคิด — เกณฑ์ผ่านขั้นต่ำของ Capstone

| เกณฑ์ | ต้องมี |
|---|---|
| Build + flash ได้ตาม README ของคุณ | ใช่ |
| ≥ 2 FreeRTOS tasks | ใช่ |
| Sensor path + LED/UART indication | ใช่ |
| Connectivity — MQTT **หรือ** BLE (อย่างน้อยหนึ่งเส้น) พร้อมรับคำสั่งหรือยืนยันลิงก์ | ใช่ |
| ไม่ฝัง secret ในไฟล์ส่งสาธารณะ | ใช่ |

งานต่อยอด (ไม่บังคับ): ใช้ทั้ง MQTT และ BLE, threshold alert, mutex บนบัสร่วม, คิว/topic พร้อมต่อ Digital Twin, คุณภาพสาธิต

---

## แนวคิด — จังหวะทำงานที่แนะนำ

| ช่วง | โฟกัส |
|---|---|
| ก่อนเริ่ม Capstone | ตรวจว่า lab หลักโมดูล 2–7 ผ่านเกณฑ์ขั้นต่ำแล้ว |
| ชม. 1 | เขียนสถาปัตยกรรม task + เลือกเซ็นเซอร์ / connectivity |
| ชม. 2–3 | รวมโค้ดบนบอร์ด + ทดสอบ MQTT และ/หรือ BLE |
| ชม. 4 / ทำต่อเอง | README, หลักฐานสาธิต, เก็บงาน |

---

## แนวคิด — แผนที่เอกสาร: หาอะไรที่ไหน

| ความต้องการ | ไปที่ |
|---|---|
| ตัวอย่างออนไลน์ | TESAIoT Developer Hub — Example Explorer + API Reference |
| ชื่อฟังก์ชัน peripheral | ชีตของโมดูล 3 (peripheral-api-map.md) |
| FreeRTOS patterns | ชีตของโมดูล 4 (rtos-patterns.md) |
| Sensors / windows / fusion | ชีตของโมดูล 5 (sensor-ai-prep.md) |
| MQTT / Wi‑Fi triggers | ชีตของโมดูล 6 (mqtt-cloud.md) |
| BLE peripheral / scan | ชีตของโมดูล 7 (ble-connectivity.md) |

---

## ตัวอย่างสมบูรณ์ — สถาปัตยกรรมอ้างอิงของ Capstone

```text
[sensor_*_read task] --samples--> [filter / window]
        │                              │
        │                              ▼
        │                        [decision / event]
        │                         │         │
        ▼                         ▼         ▼
   [UART / LED]         [MQTT publish]  [BLE notify / host]
        ▲                    ▲
        └── [MQTT and/or BLE command path]
```

ตัวอย่างหน่วงใน task (จากโมดูล 4/5):

```c
TickType_t last = xTaskGetTickCount();
for (;;) {
    /* read → filter → maybe publish */
    vTaskDelayUntil(&last, pdMS_TO_TICKS(200));
}
```

---

## แนวคิด — ธีม Capstone ที่แนะนำ

**Environmental / Activity monitor (ขนาดเล็ก)** ต้องมีอย่างน้อย:

1. **Sensor path** — อ่านเป็นช่วงเวลาคงที่ + filter หรือ window (โมดูล 5)
2. **Local indication** — LED และ/หรือ UART (โมดูล 3)
3. **RTOS** — ≥ 2 tasks + คิวหรือ mutex เมื่อจำเป็น (โมดูล 4)
4. **Connectivity** — อย่างน้อยหนึ่งเส้น: **MQTT** publish + subscribe คำสั่ง (โมดูล 6) **หรือ** **BLE** peripheral ที่โฮสต์เชื่อมได้ (โมดูล 7)

ทางเลือกเสริม: ใช้ทั้ง MQTT และ BLE · event/alert เมื่อเกินเกณฑ์ · โครงสร้าง `to_twin` สำหรับต่อ Digital Twin

---

## แนวคิด — สามสถานการณ์สาธิต

| สถานการณ์ | หมายถึง |
|---|---|
| **Normal** | ค่าเซ็นเซอร์ไหลปกติ, LED/UART ทำงานปกติ, telemetry เข้าโฮสต์ |
| **Stimulus** | เปลี่ยนอุณหภูมิ/ขยับบอร์ด/หมุน POT → เห็นค่าหรือ event เปลี่ยน |
| **Command** | จาก PC/phone ส่งคำสั่ง (MQTT topic หรือ BLE write) → อุปกรณ์ตอบสนอง |

ทั้งสามสถานการณ์ต้องพิสูจน์ได้ด้วยหลักฐานจริง (สกรีนช็อต/คลิป) ไม่ใช่แค่คำอธิบาย

---

## ฝึกเติม/แล็บ

[แล็บ Capstone: มินิโปรเจกต์](../l02-lab/README.md)

- กรอกสถาปัตยกรรม (Task / Topic / BLE) ใน capstone brief ก่อนลงมือ
- รวม sensor + indication + RTOS + connectivity เข้าด้วยกันบนบอร์ดจริง
- สาธิตครบสามสถานการณ์ (Normal, Stimulus, Command) พร้อมหลักฐาน
- ส่งมอบ README ที่ผู้อื่น build/flash ซ้ำได้โดยไม่เปิดเผยรหัสผ่าน

---

## เช็กความเข้าใจ

1. ข้อใดเป็นเกณฑ์ผ่านขั้นต่ำของ Capstone (เลือกได้หลายข้อ): ไม่ฝัง secret · ≥ 2 FreeRTOS tasks · MQTT หรือ BLE อย่างน้อยหนึ่งเส้น · ใช้ทั้ง MQTT และ BLE พร้อมกัน
2. ต้องการชื่อฟังก์ชัน peripheral ควรเปิดชีตของโมดูลใดก่อน
3. สถานการณ์สาธิต "Command" หมายถึงข้อใด

---

## ไปต่อ

หลังจบหลักสูตรนี้ คุณควรอธิบายได้ว่า:

1. TESA Firmware SDK วางชั้น HAL/Driver/Utility/Application อย่างไร
2. ModusToolbox™ + VS Code ใช้สร้าง ไล่บั๊ก และ flash อย่างไร
3. GPIO/peripherals, FreeRTOS, sensor prep, MQTT และ BLE ต่อกันเป็นผลิตภัณฑ์ Edge อย่างไร

**เส้นทางต่อไป (นอกหลักสูตรนี้):** หลักสูตร Digital Twin / Product Design — ใช้สตรีมและโครงสร้างที่เตรียมใน Capstone เป็นอินพุต

---

## แหล่งที่มา

"บทเรียน 8.1 — วางแผน Capstone และใช้แผนที่เอกสาร" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
