---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา"
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

# บทเรียน 4.1 — Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา

## bring-up ให้เสถียรก่อน พิสูจน์เส้นทาง input/output ใช้ web-app ภายนอกเป็นหลักฐานชั้นที่สอง วัด latency และไล่ปัญหาทีละชั้น

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 4 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. พิสูจน์เส้นทาง input (Twin → เฟิร์มแวร์) และ output (เฟิร์มแวร์ → Twin) ด้วยหลักฐานที่ตรวจตามรอยได้
2. วัด latency คร่าว ๆ ซ้ำสามครั้ง และระบุแหล่งหน่วงที่น่าจะเป็น
3. ไล่แยกปัญหาฝั่งเฟิร์มแวร์กับฝั่งโฮสต์ทีละชั้น โดยเปลี่ยนตัวแปรครั้งละอย่าง

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 3.2 — แล็บ M03](../../m03-virtual-device/l02-lab/README.md) มาแล้ว — มี Virtual Device + event script พร้อมกระตุ้นซ้ำ
- ต้องใช้บอร์ดจริง (TESAIoT PSoC Edge DevKit) หรือโหมด Simulator ของ Bitstream Studio

> **Key phrase**: Co-simulation = *เฟิร์มแวร์คิดและตอบ* ในเวลาเดียวกับที่ Twin *กระตุ้นและแสดงผล* — ไม่ใช่แค่เปิดกราฟดูค่า

---

## ดูของจริงก่อน — Co-simulation คืออะไร (และไม่ใช่อะไร)

| ไม่ใช่ | คือ |
|---|---|
| แทน unit test ทั้งหมด | สะพานก่อน / คู่กับบอร์ดจริง |
| แค่เปิด Simulator แล้วดู sine | กระตุ้น → เห็น logic ตอบ |
| ผสม UART + Simulator ใน UI เดียว | เลือก **หนึ่ง** backend ตามโมดูล 1 |
| เชื่อแค่แผงเดียวใน Studio | ยืนยันซ้ำด้วย consumer อื่นได้ |

---

## แนวคิด — สองเส้นทางแล็บที่ใช้ได้จริง

| Path | Firmware runs on | Twin / host role |
|---|---|---|
| **A — Simulator** | Virtual MCU (Bitstream Simulator) | Studio แสดงค่า `origin: sim` |
| **B — Board + Host** | DevKit จริง (HEX / build ของคุณ) | Studio แสดงค่า `origin: uart` |

```text
Path A:  [Simulator firmware] ──WS──► [Bridge] ──► [Bitstream Studio]
Path B:  [MCU firmware] ──UART──► [Bridge] ──► [Bitstream Studio]
```

ทั้งสอง path นับเป็น co-sim กับโฮสต์ Twin ได้ — ต่างกันที่แหล่งอินพุตฮาร์ดแวร์

---

## แนวคิด — สามชั้นที่สังเกตสตรีมเดียวกันได้

| ชั้นสังเกต | ตัวอย่าง | ใช้พิสูจน์อะไร |
|---|---|---|
| ใน Studio | Telemetry / BMI270 / 3D rotation | โฮสต์ decode + UI ทำงาน |
| บนบอร์ด / log | LED, UART print | เฟิร์มแวร์ตัดสินใจจริง |
| นอก Studio | Hackathon `web-app/` HTML | ท่อ Live Data ไปถึง consumer ทั่วไป |

ถ้าทั้งสามชั้น (หรืออย่างน้อย Studio + web-app) เห็นการเปลี่ยนแปลงสอดคล้องกันหลังกระตุ้น — คุณมีหลักฐาน co-sim ที่แข็งกว่า "แคปกราฟแผงเดียว"

---

## แนวคิด — Bring-up: เซสชันเสถียรก่อนเสมอ

1. เปิด Bitstream Studio จาก workspace ที่ผูกแล้ว (โมดูล 2)
2. เลือก backend: **Simulator** *หรือ* **Bitstream** (ไม่ผสม)
3. Link / Connect จนสถานะปกติ
4. เห็นสตรีมเซ็นเซอร์หรือ log อย่างน้อยหนึ่งช่อง
5. (Path B) ยืนยัน HEX/VSIX เวอร์ชันจับคู่

**ผ่านเมื่อ:** เซสชันนิ่ง ≥ 30–60 วินาที โดยไม่หลุด Link เอง

---

## ตัวอย่างสมบูรณ์ — เส้นทางที่ต้องพิสูจน์ให้ชัด

```text
[Stimulus]  event script / UI / scene change / tilt board
        ▼
[Sensor or pin value]     ← Virtual Device or real sensor
        ▼
[Firmware read path]      ← task / driver / SENSOR_CFG
        ▼
[Firmware decision]       ← behavior WHEN/THEN
        ▼
[Firmware write path]     ← LED / flag / publish / log
        ▼
[Twin / Studio / web-app observe]
```

---

## แนวคิด — หลักฐานของเส้นทาง Input และ Output

**Input path (Twin → Firmware):** กระตุ้นจากสคริปต์/UI → ค่าเข้าเฟิร์มแวร์ (UART log/ตัวแปร) → ค่าสอดคล้องชนิดเซ็นเซอร์

**Output path (Firmware → Twin):**

| ขั้น | หลักฐานที่รับได้ |
|---|---|
| เฟิร์มแวร์ตัดสินใจแล้วสั่งเอาต์พุต | log บรรทัดคำสั่ง / LED GPIO |
| Twin หรือ Studio สะท้อนสถานะ | กราฟ / แผง / 3D / dashboard |
| Consumer ชั้นนอกสะท้อนสถานะ | Hackathon `web-app/` |

เกณฑ์สำเร็จ: ค่าที่กระตุ้นจาก Twin **ไปถึง** พฤติกรรมเฟิร์มแวร์ และคำสั่งจากเฟิร์มแวร์ **ทำให้** สถานะบนโฮสต์เปลี่ยนตามที่คาด

---

## แนวคิด — ทำไมต้องมี web-app ภายนอกเป็นพยาน

แผงใน Bitstream Studio อาจ "ดูถูก" เพราะกำลังทดสอบโฮสต์ตัวเดียวกันที่ decode สตรีมอยู่แล้ว หน้า HTML ใน `TESAIoT_Hackathon/web-app/` เป็น **client อิสระ** — ถ้ามันอัปเดตตามการเอียงบอร์ดหรือ scene Motion แสดงว่า:

- bridge / provider เปิดอยู่
- sensor id และ fields ถูก publish
- ท่อข้อมูลไม่พังเฉพาะ UI ภายใน extension

ตัวอย่างหลักของบทนี้: **`ex05_bmi270_orientation.html`** — artificial horizon + Euler angles จาก BMI270

---

## ตัวอย่างสมบูรณ์ — บทเรียนจาก ex05: mask ต้องตรงสัญญา

หน้า ex05 เขียนไว้ชัดว่า **accel/gyro อย่างเดียวไม่พอ** ต้องเปิดใน sensor settings ให้ BMI270 publish อย่างน้อยหนึ่งชุดนี้:

| ชุด fields | ผลบนหน้าเว็บ |
|---|---|
| Euler: `headingRad`, `pitchRad`, `rollRad` | ใช้ทันที · แสดง `source: euler` |
| Quaternion: `quatW` … `quatZ` | แปลงเป็น Euler ใน JS · แสดง `source: quaternion` |

ถ้า mask มีแต่ accel/gyro: horizon จะค้างที่ *waiting for orientation fields…* — นี่คือตัวอย่าง **fault isolation** ที่ดี: สตรีมมี แต่ consumer เงียบเพราะ fields ไม่ตรงสัญญา ไม่ใช่เพราะ "web-app พัง"

---

## ตัวอย่างสมบูรณ์ — จับคู่ ex05 กับข้อพิสูจน์ของ M04

| คำถาม | ทำอะไรกับ ex05 |
|---|---|
| Input ถึงเฟิร์มแวร์ไหม | เอียงบอร์ด / สลับ scene Motion แล้วดูว่าค่า ° เปลี่ยน |
| Output โฮสต์สะท้อนไหม | horizon + ตัวเลขขยับ; แคปคู่กับแผง BMI270 ใน Studio |
| Latency? | จับเวลาจากเริ่มเอียงจนตัวเลขบน ex05 เปลี่ยน (ทำ 3 รอบ) |
| Fault ที่ไหน | `disconnected` → bridge · `waiting for orientation` → mask · ค้าง+stale → สตรีมหยุด |

---

## แนวคิด — วัด latency และหาแหล่งหน่วง

| การวัด | วิธีคร่าว ๆ |
|---|---|
| Stimulus → firmware log | จับเวลาจากกระตุ้นจนมีบรรทัด log |
| Firmware act → Studio UI | จาก log จนกราฟ/LED บน Studio เปลี่ยน |
| Firmware act → web-app | จาก log / เริ่มเอียงจน ° บนหน้าเว็บเปลี่ยน |

ทำซ้ำ 3 ครั้งแล้วจดช่วงค่า (min–max) — ลำดับที่มักเห็น: **log เร็วสุด → Studio ใกล้เคียง → web-app ช้ากว่าเล็กน้อย**

แหล่งหน่วงที่พบบ่อย: คาบ `vTaskDelay` ของ RTOS task · sensor publish interval (Lab Quiet ช้ากว่า Motion) · bridge/WS/UI refresh

---

## ตัวอย่างสมบูรณ์ — ไล่แยกปัญหาทีละชั้น

```text
1. Extension / backend up?
2. Correct source (sim XOR uart)?
3. Stream present at all?
4. Stimulus actually applied?
5. Firmware log shows read?
6. Firmware log shows write/decision?
7. Studio UI shows change?
8. web-app (ex05) shows change?
```

> **Key phrase**: แก้ทีละชั้น — อย่าเปลี่ยนเฟิร์มแวร์และโหมด Studio พร้อมกันในรอบดีบักเดียว

---

## ฝึกเติม/แล็บ

[แล็บ: I/O ครบวงจรแบบ co-simulation](../l02-lab/README.md)

- Bring-up เซสชันให้เสถียรก่อน (≥ 30–60 วินาที)
- พิสูจน์เส้นทาง input และ output พร้อมหลักฐาน
- เปิด `web-app/ex05` เป็นพยานชั้นที่สอง (ถ้าเป็นไปได้)
- วัด latency 3 รอบ และไล่แยกปัญหาถ้ามีจุดใดไม่สอดคล้อง

---

## เช็กความเข้าใจ

1. "Co-simulation" ในบทเรียนนี้หมายถึงข้อใด
2. เมื่อวัด latency ลำดับความเร็วที่มักเห็นคือข้อใด
3. เฟิร์มแวร์ log ถูกต้องแต่ UI ไม่ขยับ น่าสงสัยฝั่งใด

---

## ไปต่อ

- Co-simulation คือเฟิร์มแวร์และ Twin ทำงานพร้อมกัน ไม่ใช่แค่เปิดกราฟดูค่า
- พิสูจน์ input และ output ด้วยหลักฐานตามรอยได้ — ใช้ web-app ภายนอกเป็นพยานชั้นที่สอง
- วัด latency ซ้ำสามครั้ง และแก้ปัญหาทีละชั้นเสมอ
- พร้อมแล้วสำหรับ **โมดูล 5 — ท่อ telemetry, MQTT บน Twin และ fault injection**

[บทเรียนโมดูล 5 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## แหล่งที่มา

"บทเรียน 4.1 — Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
