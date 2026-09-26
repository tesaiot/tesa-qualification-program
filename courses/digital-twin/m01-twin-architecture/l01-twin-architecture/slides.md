---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง"
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

# บทเรียน 1.1 — Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง

## ความหมายของ Virtual Device และ Digital Twin สถาปัตยกรรมเป็นชั้น เส้นทาง live สองเส้น (Bitstream กับ Simulator) และเกณฑ์ตัดสินใจว่าเมื่อไรต้องใช้บอร์ดจริง

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 1 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แยกความหมายของ Physical Device, Virtual Device, Digital Twin Platform และ Host ด้วยคำพูดของตัวเอง
2. อธิบายว่า Bitstream (UART/บอร์ด) กับ Simulator เป็นเส้นทาง live ที่ใช้ทีละเส้น และบอกเหตุผลที่ไม่ผสมกัน
3. ตัดสินใจว่าสถานการณ์ทดสอบหนึ่งใช้ Twin/Simulator ได้พอ หรือต้องยืนยันบนบอร์ดจริง พร้อมเหตุผล

---

## ก่อนเริ่ม

- บทเรียนแรกของหลักสูตรนี้ — ไม่บังคับผ่านบทเรียนก่อนหน้าในคอร์สนี้ (แต่ต้นฉบับแนะนำให้ผ่าน [หลักสูตร Firmware SDK](../../../firmware-sdk-edge-ai/README.md) หรือมีพื้นฐาน C/MCU/MQTT เทียบเท่ามาก่อน)
- **ไม่ต้องใช้บอร์ด** — บทเรียนเชิงแนวคิดล้วน ยังไม่บังคับสร้าง Virtual Device เต็มรูป
- ทำได้ด้วยโหมด Simulator ของ Bitstream Studio (ถ้ามี extension) หรือบอร์ด TESAIoT PSoC Edge DevKit

---

## ดูของจริงก่อน — ทำไมต้องมี Digital Twin

การพัฒนาเฟิร์มแวร์ IoT / Edge AI วันนี้มักมีเซ็นเซอร์หลายตัว, RTOS หลาย task, connectivity (Wi‑Fi/MQTT/BLE) และโฮสต์ดูค่าแบบเรียลไทม์ — ถ้าทดสอบทุกเคสบนบอร์ดจริงอย่างเดียว จะเจอต้นทุนสูง เวลาช้า และความเสี่ยงต่อฮาร์ดแวร์

| ประโยชน์ | ความหมายในแล็บ |
|---|---|
| จำลองฮาร์ดแวร์ | อ่านค่าเซ็นเซอร์/สถานะโดยไม่ต้องต่อทุกพินจริง |
| ทดสอบ logic ซ้ำได้ | สคริปต์เขย่า IMU / กดสวิตช์ / ตัดเน็ต ได้ซ้ำ |
| ลดความเสี่ยงบอร์ด | เคสขอบทำบน Twin ก่อน flash จริง |

> **Key phrase**: Twin ไม่ได้แทนที่บอร์ด 100% — มันเป็น **สะพาน** ระหว่างทฤษฎีเฟิร์มแวร์กับการทดสอบที่ทำซ้ำได้

---

## แนวคิด — Virtual Device เทียบกับ Digital Twin

| คำ | ความหมายในหลักสูตรนี้ |
|---|---|
| **Physical Device** | บอร์ด + เซ็นเซอร์จริง (เช่น PSoC Edge kit) |
| **Virtual Device** | แบบจำลองซอฟต์แวร์ของ *อุปกรณ์หนึ่งตัว* — พิน, เซ็นเซอร์, สถานะ, พฤติกรรมตอบสนอง |
| **Digital Twin (Platform)** | สภาพแวดล้อมที่รวม Virtual Device + การสื่อสาร + visualization + สคริปต์เหตุการณ์ + (บ่อยครั้ง) MQTT/cloud จำลอง |
| **Host / Twin UI** | VS Code extension และแอปโฮสต์ที่ใช้ดูผล — หลักคือ **Bitstream Studio** |

```text
Physical Device  ≈  "ของจริงบนโต๊ะ"
Virtual Device   ≈  "โมเดลอุปกรณ์หนึ่งเครื่องในซอฟต์แวร์"
Digital Twin     ≈  "โรงงานจำลองทั้งระบบ" (โมเดล + สื่อสาร + จอ + สคริปต์ + cloud sim)
```

---

## แนวคิด — สถาปัตยกรรมเป็นชั้น (conceptual engines)

| ชั้น (แนวคิด) | หน้าที่ | สิ่งที่มักเปิดในแล็บนี้ |
|---|---|---|
| Digital Twin Engine | จัดการ state ของ Virtual Device, เวลาจำลอง | สถานะเซ็นเซอร์/โหมดใน Studio · Simulator stream |
| Communication Engine | ช่องทางข้อมูลระหว่างเฟิร์มแวร์ ↔ โฮสต์ ↔ cloud | UART/bridge, MQTT broker ใน Studio, BLE host |
| Graphics / Visualization | กราฟ, แผง, 3D, orientation | Sensor Telemetry · Sensor Studio · 3D preview |
| Scripting & Events | จำลองเหตุการณ์ซ้ำได้ | event script / behavior (โมดูล 3) · fault injection (โมดูล 5) |

> **Honest mapping**: UI ของแต่ละเวอร์ชัน extension อาจต่างกัน — **จำบทบาทของชั้น** ไม่ใช่จำพิกัดปุ่มทุกจอ

---

## แนวคิด — สองเส้นทาง telemetry (mental model สำคัญ)

ใน Bitstream Studio: **Bitstream (UART/บอร์ด)** กับ **Simulator** เป็นเส้นทาง live ที่**ใช้ทีละเส้น** — ไม่ผสมใน UI

```text
Toolbar source = Bitstream  →  COM open  →  samples origin: uart
Toolbar source = Simulator →  COM closed →  samples origin: sim
```

| คำถาม | คำตอบสั้น |
|---|---|
| Twin ต้องมีบอร์ดไหม | ไม่เสมอ — Simulator = เส้นทางไม่มีบอร์ด |
| บอร์ดยังจำเป็นไหม | ใช่ — RF, analog, พลังงาน, ขาพินจริง |
| ทำไมห้ามผสม | กันข้อมูล uart/sim ปะปนในกราฟเดียวกัน |

---

## แนวคิด — ท่อข้อมูล (data pipeline)

```text
[Source]  board sensors หรือ virtual/sim sensors
        ▼
[Firmware Logic]  — filter · window · decide · encode
        ▼
[Communication]   — UART / MQTT / BLE
        ▼
[Twin Host]       — decode · state · route
        ├─► Visualization (Telemetry / Studio / 3D)
        ├─► External dashboard (Hackathon web-app)
        └─► Cloud / broker (โมดูล 5)
```

| ชนิด | ความหมาย |
|---|---|
| Telemetry | ค่าวัดที่ไหลเป็นช่วงเวลาคงที่ (อุณหภูมิ, accel, …) |
| State | สถานะระบบ (connected, mode, streaming) |
| Event | เหตุการณ์จุดเดียว (threshold crossed, button, alert) |

---

## ตัวอย่างสมบูรณ์ — เมื่อไร Twin พอ เมื่อไรต้องบอร์ดจริง

| สถานการณ์ | Twin/Sim พอไหม | ต้องบอร์ดจริงไหม |
|---|---|---|
| Logic สลับโหมดจากปุ่ม | มักพอ | ไม่จำเป็นระยะแรก |
| รูปแบบ JSON / MQTT topic | พอ (ดีมาก) | ยืนยันรอบสุดท้ายถ้าใช้ Wi‑Fi จริง |
| อ่าน IMU แล้วคำนวณบนโค้ด | พอสำหรับ logic | ยืนยัน noise/bias จริงบนบอร์ด |
| Wi‑Fi ระยะ / BLE ห้องจริง | ไม่แทน | **ต้อง** |
| ตรวจ pin map / บัดกรีผิด | ไม่แทน | **ต้อง** |

จาก [README.md](README.md) หัวข้อ 5.1 — เวิร์กโฟลว์ที่แนะนำ: พัฒนาบน Twin ก่อน ใช้ชุดเทสเดียวกันให้มากที่สุด แล้วยืนยันรอบสุดท้ายบนฮาร์ดแวร์จริง

---

## ฝึกเติม/แล็บ

[แล็บ: แผนที่สถาปัตยกรรม Twin](../l02-lab/README.md)

- แยกความหมาย Physical Device / Virtual Device / Digital Twin ด้วยคำพูดของตัวเอง
- วาดหรือกรอกแผนภาพสถาปัตยกรรมตามแนวคิด engine ที่เรียนมา
- ฝึกตัดสินใจจากตาราง test decision: สถานการณ์ไหนใช้ Twin พอ สถานการณ์ไหนต้องบอร์ดจริง

---

## เช็กความเข้าใจ

1. "แบบจำลองซอฟต์แวร์ของอุปกรณ์หนึ่งตัว ทั้งพิน เซ็นเซอร์ สถานะ และพฤติกรรมตอบสนอง" คือข้อใด
2. ทำไม Bitstream Studio ให้ใช้ Bitstream หรือ Simulator ทีละเส้น
3. สถานการณ์ใดที่บทเรียนระบุว่า Twin "ไม่แทน" และต้องใช้บอร์ดจริง

---

## ไปต่อ

- Digital Twin คือสภาพแวดล้อมที่รวม Virtual Device + การสื่อสาร + visualization + สคริปต์
- Bitstream กับ Simulator เป็นเส้นทาง live ที่ใช้ทีละเส้นเสมอ
- เลือกใช้ Twin ก่อน แล้วยืนยันรอบสุดท้ายบนบอร์ดจริงสำหรับ RF/analog/พลังงาน/pin map
- พร้อมแล้วสำหรับ **โมดูล 2 — VS Code สำหรับพัฒนาร่วมกับ Twin**

[บทเรียนโมดูล 2 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

---

## แหล่งที่มา

"บทเรียน 1.1 — Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
