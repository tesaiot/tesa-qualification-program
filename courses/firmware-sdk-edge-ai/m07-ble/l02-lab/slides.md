---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 7.2 — แล็บ: การเชื่อมต่อ BLE"
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

# บทเรียน 7.2 — แล็บ: การเชื่อมต่อ BLE

## อ่านสถานะ peripheral สั่ง advertising ให้โฮสต์ค้นพบและเชื่อมต่อ ทดสอบลิงก์สั้น ๆ และ (ทางเลือก) ลอง scan

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 7 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. อ่านสถานะ BLE peripheral ก่อนและหลังโฮสต์เชื่อมต่อ แล้วบันทึกเป็นตาราง
2. สั่ง advertising และยืนยันด้วยโฮสต์ (GATT explorer) ว่าเห็นและเชื่อมต่ออุปกรณ์ได้

---

## ก่อนเริ่ม

- [ ] บอร์ด + HEX/เฟิร์มแวร์ที่ **เปิด BLE profile**
- [ ] PC หรือโทรศัพท์เปิด Bluetooth
- [ ] เตรียม GATT explorer ทั่วไป (nRF Connect / LightBlue / AIROC™ Bluetooth® Connect)
- [ ] ปิด Central อื่นที่อาจแย่งลิงก์ (nRF Connect ค้างอยู่ ฯลฯ)

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่ต่อสาธารณะ** — เป็นของผู้ดูแล ให้ใช้ GATT explorer ทั่วไปแทนตามที่บทเรียนเสนอไว้ · snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส — ดูรายละเอียดที่หมายเหตุต้นบทเรียน [บทเรียน 7.1](../l01-ble-connectivity/README.md)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Part A — Peripheral status | sync สำเร็จ และ `stack_ready` แสดงว่าสแต็กพร้อม |
| Part B — Advertising + host discover | โฮสต์เห็นและเชื่อมอุปกรณ์ได้ อย่างน้อยหนึ่งครั้ง พร้อมหลักฐาน |
| Part C — Link behaviour (short soak) | ทำ reconnect ได้โดยไม่ต้อง reflash |
| Part D — Optional scan observer | มีล็อกผลสแกนที่อ่านได้ (ทางเลือก) |

---

## ฝึกเติม/แล็บ (1) — Part A: Peripheral status

1. Flash เฟิร์มแวร์ตัวอย่าง (หรือ build ของคุณที่มี BLE)
2. จาก task บน CM55 เรียก:

```c
ipc_ble_periph_status_t st;
bool ok = cm55_ble_periph_status_get_sync(&st, 5000U);
```

3. บันทึกค่า: `profile_ble_active`, `stack_ready`, `connection_id`, `last_error`

---

## ฝึกเติม/แล็บ (2) — Part B: Advertising + host discover

1. สั่ง start ADV:

```c
uint8_t result = 0xFF;
(void)cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U);
```

2. บนโฮสต์: เปิด GATT explorer ทั่วไป (nRF Connect ฯลฯ) แล้วหาชื่ออุปกรณ์ที่ตั้งไว้ (มักขึ้นต้น `TESAIoT-`)
3. เมื่อเชื่อมแล้ว อ่าน status อีกครั้ง — คาดหวัง `connection_id != 0` และ/หรือ `tx_notify_enabled` ตามสถานะโฮสต์

---

## ฝึกเติม/แล็บ (3) — Part C: Link behaviour (short soak)

1. สตรีมหรืออ่านค่าสั้น ๆ บนโฮสต์ (~30–60 วินาที)
2. กด disconnect บนโฮสต์ แล้วสั่ง ADV start/restart ถ้าจำเป็น
3. เชื่อมใหม่ให้สำเร็จ

---

## ฝึกเติม/แล็บ (4) — Part D: Optional scan observer

1. ลงทะเบียน `cm55_ble_ipc_set_event_handler`
2. เรียก `cm55_ble_request_scan_all()` (หรือ `scan_name`) สั้น ๆ
3. บันทึกอย่างน้อย 1 รายการ adv (addr / rssi / name) จากล็อก

---

## เช็กความเข้าใจ — เตรียมส่งงาน

ตอบสั้น ๆ ก่อนกรอก deliverables checklist:

1. ค่า status ที่ต่างกันระหว่างก่อน/หลัง connect คืออะไรบ้าง
2. BLE ต่างจาก MQTT อย่างไรในโปรเจกต์ของคุณ (คนละชั้นขนส่ง / คนละโฮสต์แล็บ)
3. ถ้าโฮสต์ไม่เห็นอุปกรณ์หลังบูตนาน ควรตรวจอะไรก่อน

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] ตาราง status ก่อน/หลัง connect
- [ ] สกรีนช็อตโฮสต์ที่เห็นชื่ออุปกรณ์ (`TESAIoT-*` หรือชื่อที่ตั้งไว้)
- [ ] โน้ตสั้น: BLE ต่างจาก MQTT อย่างไรในโปรเจกต์ของคุณ
- [ ] (ถ้าทำ Part D) ตัวอย่างล็อกสแกน

พร้อมแล้ว ไปต่อ **โมดูล 8 — Capstone และแหล่งเรียนรู้ของหลักสูตร**

[บทเรียนโมดูล 8 →](../../m08-capstone/l01-capstone-and-resources/README.md)

---

## แหล่งที่มา

"บทเรียน 7.2 — แล็บ: การเชื่อมต่อ BLE" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
