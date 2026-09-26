---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — ท่อ telemetry, MQTT บน Twin และ fault injection"
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

# บทเรียน 5.1 — ท่อ telemetry, MQTT บน Twin และ fault injection

## แยก Telemetry/State/Event แยกท่อ Live Data กับ MQTT ใช้ web-app ex08/ex09 ตรวจสตรีม และออกแบบการทดลองเครือข่ายเสีย

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 5 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จำแนกข้อมูลอุปกรณ์เป็น Telemetry, State และ Event และเลือก topic กับ retain ให้เหมาะแต่ละชนิด
2. แยกท่อ Live Data กับ MQTT และใช้อาการที่เห็นระบุว่าท่อไหนมีปัญหา
3. ออกแบบการทดลอง fault injection ที่เปลี่ยนตัวแปรครั้งละหนึ่งตัว และบันทึกผลทั้งสองฝั่ง

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 4.2 — แล็บ M04](../../m04-cosimulation/l02-lab/README.md) มาแล้ว — พิสูจน์แล้วว่าเฟิร์มแวร์ ↔ Twin มี I/O จริง
- ต้องใช้บอร์ดจริง (TESAIoT PSoC Edge DevKit) หรือโหมด Simulator

> **Key phrase**: Twin เป็นสนามซ้อมของท่อข้อมูล — ฝึก topic, payload, dashboard และ reconnect **ก่อน** ขึ้นคลาวด์จริงทั้งวัน

---

## ดูของจริงก่อน — สามชนิดข้อมูลจากอุปกรณ์

| ชนิด | ลักษณะ | ตัวอย่างในแล็บ Twin |
|---|---|---|
| **Telemetry** | สตรีมต่อเนื่องตามเวลา | อุณหภูมิทุก 1 s · BMI270 sample |
| **State** | สถานะปัจจุบันของระบบ | `mode=idle`, `led=on`, Link `connected` |
| **Event** | เกิดเป็นครั้งคราวเมื่อเงื่อนไขเป็นจริง | `threshold_exceeded`, `stale`, `reconnect` |

> **Key phrase**: Telemetry = *ลมหายใจ* · State = *ท่าทางปัจจุบัน* · Event = *เหตุการณ์ที่ควรบันทึก*

---

## แนวคิด — นิสัยการออกแบบ topic

| นิสัย | เหตุผล |
|---|---|
| Telemetry ใช้ topic/อัตราคงที่ | แดชบอร์ดคาดหวังจังหวะ |
| State ส่งเมื่อเปลี่ยน (หรือ retain ล่าสุด) | ลด spam · subscriber ใหม่รู้สถานะทันที |
| Event เก็บ timestamp + เหตุผลสั้น ๆ | debug / โมดูล 6 E2E ไล่ย้อนได้ |

```text
device/<deviceId>/devkit-twin/telemetry     ← telemetry stream
device/<deviceId>/state                      ← current mode / flags
device/<deviceId>/event/<name>               ← sparse events
```

---

## แนวคิด — ท่อข้อมูล (มุมมองแล็บ Twin)

```text
[Source]  Firmware / Simulator / Twin virtual device
        ▼
[Shape]   JSON fields · units · mask · channels
        ▼
[Transport]
  A) Live Data provider (WS) → Studio panels / web-app ex05–ex08
  B) MQTT broker             → web-app ex09–ex15 / cloud / external tools
        ▼
[Observe] Dashboard · subscriber log · gauges
```

---

## แนวคิด — สองท่อที่ห้ามสับสน

| ท่อ | ใช้เมื่อ | ตัวอย่าง consumer |
|---|---|---|
| **Live Data** (telemetry provider) | ดู sample ที่ decode แล้ว · route/origin/stale | ex05, ex06, ex08 |
| **MQTT** (broker pub/sub) | จำลองชั้น cloud / ระบบภายนอก | ex09, ex12, ex15 |

| อาการ | น่าสงสัยท่อ |
|---|---|
| `TelemetryClient` disconnected | Live Data / bridge / Serve web-app |
| Live Data ดี แต่ MQTT ว่าง | ยังไม่มี publisher บน topic นั้น |
| MQTT มีข้อความแต่ Live Data เงียบ | คนละท่อ — ไม่ได้แปลว่า "เซ็นเซอร์ตาย" |

---

## ตัวอย่างสมบูรณ์ — ex08: Stale, Route และ Origin

ก่อนเปิด broker ให้คุ้นคุณภาพของสตรีม Live Data ก่อน

| UI | ความหมาย |
|---|---|
| Connection route | backend ที่ provider ใช้ |
| Last sample origin | `uart` หรือ `sim` — ต้องสอดคล้องโหมดที่เลือก |
| Sensor pills + stale | แต่ละเซ็นเซอร์เงียบเกิน `staleAfterMs` หรือยัง fresh |

**ขั้นตอน:** Link Studio → Serve `web-app/` เปิด ex08 → ยืนยัน `connected` → หยุดสตรีมชั่วคราว (pill ควรเข้า **stale**) → กลับมาสตรีม (pill **fresh** อีกครั้ง)

**ผ่านเมื่อ:** อธิบายได้ว่า `stale` คือ **Event** ด้านโฮสต์เมื่อ telemetry ขาดช่วง — ไม่ใช่ค่าเซ็นเซอร์

---

## แนวคิด — MQTT Broker ในโฮสต์ Twin

**Toolbar / Server → Start broker** ในโฮสต์ Bitstream Studio จากนั้นหน้าเว็บ MQTT ต่อที่ `ws://127.0.0.1:8883/mqtt` (override ด้วย `?mqtt=`)

| บทบาทในเอกสารหลักสูตร | สิ่งที่ทำในแล็บ |
|---|---|
| MQTT ใน Twin | Studio Start broker + pub จาก Twin / Sensor Studio |
| Cloud / ระบบภายนอก | `web-app` subscriber หรือ broker สาธารณะ/LAN |

> อย่าสมมติว่า "Start broker" = มี telemetry อัตโนมัติ — ยังต้องมี **publisher** บน topic ที่ subscribe

---

## ตัวอย่างสมบูรณ์ — ex09: MQTT Subscriber

ตัวอย่างหลักของโมดูลนี้สำหรับชั้น MQTT — subscribe topic เริ่มต้น:

```text
device/devkit-twin-01/devkit-twin/telemetry
```

```text
[Bitstream Studio] Start broker
        ▼
[Publisher]  DevKit Twin MQTT tab / Sensor Studio nodes
        │  topic: device/<id>/devkit-twin/telemetry
        ▼
[Broker ws://127.0.0.1:8883/mqtt]
        ▼
[ex09 browser page]  →  Last payload + message count
```

**ผ่านเมื่อ:** มีอย่างน้อยหนึ่ง JSON ที่ฟิลด์ตรงกับที่ตั้งใจส่ง (หน่วยและชื่อ key)

---

## แนวคิด — ตัวอย่างใกล้เคียงและรูปแบบ pub/sub

| ไฟล์ | ใช้เมื่อ |
|---|---|
| ex09 | Subscribe หนึ่ง topic — ตัวอย่างหลัก |
| ex10 | Publish จากเบราว์เซอร์ |
| ex11 | Wildcards (`+` / `#`) |
| ex14 | QoS + retain ทดลองมือ |

| แบบ | ใคร publish | ใคร subscribe |
|---|---|---|
| Device → Cloud | Twin / เฟิร์มแวร์ | ex09 / dashboard |
| Cloud → Device | เครื่องมือโฮสต์ / ex10 | Twin หรือเฟิร์มแวร์ |

สำหรับบทเรียนนี้ให้ทำ **ex08 + ex09** ให้ชัวร์ แล้วเลือกอย่างน้อยหนึ่งจาก ex10–ex15 ตามเวลา

---

## แนวคิด — QoS, Retain และการ map ชนิดข้อมูล

| แนวคิด | สิ่งที่ลอง |
|---|---|
| QoS 0 | ส่งแล้วไปต่อ — เหมาะ telemetry หนาแน่น |
| Retain | publish พร้อม retain → เปิด subscriber ใหม่ควรได้ข้อความล่าสุดทันที |

| ชนิด | แนวทาง topic | Retain? |
|---|---|---|
| Telemetry | `…/telemetry` | มัก **ไม่** |
| State | `…/state` | มัก **ใช่** |
| Event | `…/event/<name>` | มัก **ไม่** |

> อย่าเปิด retain บน topic telemetry ความถี่สูงโดยไม่คิด — ผู้มาใหม่อาจเข้าใจผิดว่าเป็นสตรีมสด

---

## ตัวอย่างสมบูรณ์ — การทดลอง Lossy Network

| การทดลอง | วิธีในแล็บ Twin | ดูอะไร |
|---|---|---|
| ข้อความขาดช่วง | หยุด publisher ชั่วคราว | ex08 stale · ช่องว่างบนกราฟ |
| ตัดการเชื่อมต่อสั้น ๆ | Stop broker แล้ว Start ใหม่ | ex09 `reconnecting` → `connected` |
| Latency สูง | ลดอัตรา publish / scene Quiet | ช่วงเวลาระหว่าง message count |
| Payload ผิดรูป | ส่ง JSON ตัดฟิลด์ | dashboard error vs เงียบ |

เป้าหมายไม่ใช่ทำเครือข่ายพังเก่งที่สุด แต่คือ **ควบคุมตัวแปรหนึ่งตัว** แล้วบันทึกว่าคิว/UI/client รับมืออย่างไร

---

## แนวคิด — บันทึกอะไรสำหรับแต่ละเคส fault injection

1. สิ่งที่ฉีด / ตัด
2. สิ่งที่เห็นบน subscriber / Studio (timestamp)
3. พฤติกรรม: **drop** · **retry** · **reconnect** · **stale UI** · **backoff**
4. ยอมรับได้สำหรับโปรเจกต์หรือต้องแก้ก่อนโมดูล 6

> **Key phrase**: Fault injection ที่ดี = *เปลี่ยนอย่างเดียวต่อรอบ* แล้วมี log ทั้งสองฝั่ง

---

## ฝึกเติม/แล็บ

[แล็บ: ท่อ telemetry และ MQTT บน Twin](../l02-lab/README.md)

- จำแนกข้อมูลของโปรเจกต์เป็น Telemetry/State/Event พร้อม topic
- เปิด ex08 ยืนยันคุณภาพสตรีม แล้วเปิด ex09 ยืนยันว่า MQTT subscriber ได้ payload
- ออกแบบและรันการทดลอง fault injection อย่างน้อยหนึ่งเคส พร้อมบันทึกผล

---

## เช็กความเข้าใจ

1. `mode=idle` หรือ `led=on` เป็นข้อมูลชนิดใด และบทเรียนแนะนำ retain อย่างไร
2. Live Data ปกติ แต่ MQTT subscriber ว่าง สาเหตุที่น่าจะเป็นคืออะไร
3. ข้อใดเป็นหลักของ fault injection ที่ดีตามบทเรียน

---

## ไปต่อ

- แยกข้อมูลเป็น Telemetry/State/Event ช่วยออกแบบ topic อัตราส่ง และแดชบอร์ด
- Live Data กับ MQTT เป็นคนละท่อ — อาการที่เห็นบอกได้ว่าท่อไหนมีปัญหา
- Fault injection ที่ดีเปลี่ยนทีละตัวแปร พร้อม log ทั้งสองฝั่งเสมอ
- พร้อมแล้วสำหรับ **โมดูล 6 — การรวมระบบและการทดสอบ**

[บทเรียนโมดูล 6 →](../../m06-integration/l01-system-integration-testing/README.md)

---

## แหล่งที่มา

"บทเรียน 5.1 — ท่อ telemetry, MQTT บน Twin และ fault injection" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
