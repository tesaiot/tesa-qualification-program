---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 7.1 — BLE สำหรับผลิตภัณฑ์ Edge"
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

# บทเรียน 7.1 — BLE สำหรับผลิตภัณฑ์ Edge

## บทบาทของ BLE เทียบกับ MQTT คำศัพท์ GAP/GATT การแบ่งงาน CM33/CM55 การอ่านสถานะ สั่ง advertising และเส้นทาง scan

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 7 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เปรียบเทียบบทบาทของ BLE (local) กับ MQTT (cloud / broker) สำหรับผลิตภัณฑ์ Edge ได้อย่างน้อยสามด้าน
2. อธิบายคำ GAP, GATT, Peripheral, Central, Advertising และ Notification ด้วยตัวอย่างจากบอร์ดและโฮสต์
3. อธิบายการแบ่งงานระหว่างคอร์: CM33 เป็นเจ้าของ BLE stack ส่วน CM55 สั่งงานผ่าน IPC

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 6.2 — แล็บ M06](../../m06-mqtt/l02-lab/README.md) มาแล้ว
- ใช้บอร์ดจริง: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL)
- บทเรียนเชิงปฏิบัติ — เปรียบเทียบกับ MQTT (โมดูล 6) เชื่อมโฮสต์ท้องถิ่นผ่าน BLE

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส ฟังก์ชันอย่าง `cm55_ble_periph_status_get_sync`, `cm55_ble_periph_adv_ctrl_sync`, `cm55_trigger_ble_periph_*`, `cm55_ble_request_scan_*` จึงยังไม่มี header ให้เปิดดูหรือ build เอง — อ่านเป็นแนวคิดและลำดับการเรียกใช้ **โฮสต์ `ble-flet` เองก็ยังไม่เผยแพร่ต่อสาธารณะ** (เป็นของผู้ดูแล) ให้ใช้ GATT explorer ทั่วไปแทน เช่น nRF Connect, LightBlue หรือ AIROC™ Bluetooth® Connect

---

## ดูของจริงก่อน — BLE ในหน้าเดียว

**BLE** เป็นวิทยุระยะสั้นพลังงานต่ำ เหมาะกับโทรศัพท์ แท็บเล็ต และเดสก์ท็อปที่อยู่ใกล้บอร์ด — ไม่ต้องมี Wi‑Fi หรือ broker

| คำ | ความหมาย |
|---|---|
| Peripheral | อุปกรณ์ที่ *advertise* และรอให้โฮสต์เชื่อม (บอร์ด TESA มักเป็นบทบาทนี้) |
| Central | โฮสต์ที่ *สแกน* แล้วเชื่อม (phone / PC) |
| GAP | ชั้นค้นพบและเชื่อมต่อ (ชื่อ ADV, ที่อยู่, connection) |
| GATT | ชั้นบริการ/คุณลักษณะ (Service / Characteristic / Notify / Write) |
| Notification | Peripheral ส่งข้อมูลไป Central โดยไม่ต้องรอ poll ทุกครั้ง |

> **Key phrase**: MQTT พาข้อมูลขึ้นเครือข่าย — BLE พาข้อมูลเข้ามือถือ/พีซีที่อยู่ใกล้

---

## แนวคิด — BLE เทียบกับ MQTT (หลังโมดูล 6)

| | BLE | MQTT |
|---|---|---|
| ระยะ | ใกล้ (ห้อง / โต๊ะ) | ผ่านเครือข่าย / คลาวด์ |
| สะพานกลาง | ไม่บังคับ broker | ต้องมี **broker** |
| พลังงาน / setup | ไม่ต้อง join Wi‑Fi | ต้อง Wi‑Fi (+ TLS ถ้า MQTTs) |
| โฮสต์แล็บ | nRF Connect, LightBlue, AIROC app | MQTTX, Studio broker, web-app |
| ใน Capstone (โมดูล 8) | เส้นทาง local | เส้นทาง cloud |

เกณฑ์ขั้นต่ำของโมดูล 8: **MQTT หรือ BLE** — ใช้ทั้งสองได้เป็นโบนัส

---

## แนวคิด — BLE อยู่ตรงไหนใน TESA Firmware

บน Evaluation Kit วิทยุมักเป็น **AIROC™ Wi‑Fi & Bluetooth® combo** — สแต็ก BLE รันบน **CM33**; แอปเซ็นเซอร์บน **CM55** สั่งผ่าน IPC

| บทบาท | คอร์ | API ที่ผู้เรียนเรียกบ่อย |
|---|---|---|
| BLE stack + GATT peripheral | CM33 | `ble_periph_*` (เจ้าของจริง) |
| สถานะ / สั่ง ADV จากแอป | CM55 | `cm55_trigger_ble_periph_*`, `cm55_ble_periph_*_sync` |
| สแกน (observer) | CM33 รันสแกน · CM55 ขอและรับ event | `cm55_ble_request_scan_*` |

```text
[Phone / PC central] ──GATT──► [BLE peripheral on CM33]
                                    ▲  │ IPC
                              [App on CM55]  cm55_trigger_ble_periph_*
```

> **Honest note**: Wi‑Fi และ BLE ใช้วิทยุชุดเดียวกันบนหลายคิต — อย่าคาดหวัง throughput สูงสุดทั้งสองพร้อมกันโดยไม่ทดสอบ coexistence

---

## ตัวอย่างสมบูรณ์ — อ่านสถานะ peripheral (diagnostic first)

ก่อน "เชื่อมกับมือถือ" ให้ยืนยันว่าโปรไฟล์ BLE บนเฟิร์มแวร์ทำงาน

```c
#include "cm55_ipc_app.h"
#include "ipc_ble_periph_types.h"

ipc_ble_periph_status_t st;

if (cm55_ble_periph_status_get_sync(&st, 5000U)) {
    /* ตรวจ stack_ready, connection_id, tx_notify_enabled */
} else {
    /* timeout / IPC ไม่ตอบ — ตรวจว่า firmware เปิด BLE profile */
}
```

| ฟิลด์ | ความหมายโดยประมาณ |
|---|---|
| `stack_ready` | สแต็กพร้อม |
| `connection_id` | มี GATT connection เมื่อไม่ใช่ 0 |
| `tx_notify_enabled` | Central เปิด notify แล้ว (ลิงก์ใช้งานจริง) |

---

## ตัวอย่างสมบูรณ์ — สั่ง advertising

Advertising ทำให้ Central มองเห็นอุปกรณ์ — ชื่อในแล็บ TESA มักขึ้นต้นด้วย **`TESAIoT-`**

```c
uint8_t result = 0xFF;

/* action: 0 = stop, 1 = start, 2 = restart */
if (cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U)) {
    /* result 0 = ok ตาม bridge */
}
```

> **Key phrase จาก firmware**: ขณะมี connection อยู่ การ stop ADV จะไม่ตัดลิงก์ — และ start ADV อาจไม่จำเป็นเพราะเชื่อมอยู่แล้ว

---

## แนวคิด — เส้นทาง scan (observer, ทางเลือก)

เมื่อบทบาทเป็น **สแกนหาอุปกรณ์อื่น** (ไม่ใช่แค่เป็น peripheral):

```c
cm55_ble_ipc_set_event_handler(on_ble_ipc, NULL);
cm55_ble_request_scan_all();  /* หรือ scan_name / scan_addr */
```

| API | ใช้เมื่อ |
|---|---|
| `cm55_ble_request_scan_all` | สแกนเต็ม ไม่กรอง |
| `cm55_ble_request_scan_name` | กรองตามชื่อย่อย |
| `cm55_ble_request_scan_addr` | กรองตามที่อยู่ 6 ไบต์ |

ยังไม่พบตัวเทียบใน SDK สาธารณะสำหรับเส้นทาง scan/observer — `ble_nus` ใน SDK เปิดเป็นบทบาท peripheral อย่างเดียว

---

## แนวคิด — เครื่องมือโฮสต์สำหรับแล็บ

| เครื่องมือ | หมายเหตุ |
|---|---|
| Hackathon `ble-flet` (Python + Flet + bleak) | แนะนำในต้นฉบับ — **ยังไม่เผยแพร่ต่อสาธารณะ** เป็นของผู้ดูแล |
| GATT explorer ทั่วไป (nRF Connect, LightBlue, AIROC™ Bluetooth® Connect) | ใช้ยืนยันว่าอุปกรณ์ advertise และเชื่อมได้ |
| Bitstream Studio | โฮสต์หลักของหลักสูตรสำหรับ USB/UART และ MQTT — ใช้เป็นคู่เทียบว่าเมื่อไรเลือก BLE local |

**ความปลอดภัยและวินัยแล็บ**: แล็บมักใช้ลิงก์สั้น ๆ ไม่ใช่ production secure pairing · อย่าเปิด GATT explorer สองตัวพร้อมกันไปที่บอร์ดเดียวกัน

---

## ฝึกเติม/แล็บ

[แล็บ: การเชื่อมต่อ BLE](../l02-lab/README.md)

- อ่านสถานะ peripheral จนยืนยันว่าโปรไฟล์ BLE พร้อม
- สั่ง advertising (stop/start/restart) แล้วสังเกตผลบนโฮสต์
- เชื่อมด้วย GATT explorer ทั่วไปอย่างน้อยหนึ่งตัว แล้วเก็บหลักฐาน
- (ถ้าเวลาเหลือ) ลองเส้นทาง scan/observer

---

## เช็กความเข้าใจ

1. ข้อใดตรงกับ Key phrase ของบทเรียนเรื่อง BLE กับ MQTT
2. อุปกรณ์ที่ "สแกนแล้วเชื่อม" เช่นโทรศัพท์หรือพีซี มีบทบาทใด (Advertising / Notification / Central / Peripheral)
3. ในเฟิร์มแวร์ของบทเรียนนี้ BLE stack รันบนคอร์ใด

---

## ไปต่อ

- BLE พาข้อมูลเข้ามือถือ/พีซีใกล้ตัว — MQTT พาข้อมูลขึ้นเครือข่าย คนละชั้นขนส่ง
- CM33 เป็นเจ้าของ BLE stack, CM55 สั่งผ่าน IPC (สถานะ, advertising, scan)
- Capstone ต้องมีอย่างน้อยหนึ่งเส้นทาง connectivity: **MQTT หรือ BLE**
- พร้อมแล้วสำหรับ **โมดูล 8 — Capstone และแหล่งเรียนรู้ของหลักสูตร**

[บทเรียนโมดูล 8 →](../../m08-capstone/l01-capstone-and-resources/README.md)

---

## แหล่งที่มา

"บทเรียน 7.1 — BLE สำหรับผลิตภัณฑ์ Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
