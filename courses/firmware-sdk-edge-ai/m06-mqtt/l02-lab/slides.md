---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.2 — แล็บ: Wi-Fi, MQTT connect, publish และ subscribe"
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

# บทเรียน 6.2 — แล็บ: Wi-Fi, MQTT connect, publish และ subscribe

## join Wi-Fi เชื่อม MQTT publish ข้อความหรือ telemetry แล้ว subscribe รับคำสั่งกลับ พร้อมบันทึกคอนฟิกโดยไม่เปิดเผยความลับ

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 6 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. เชื่อม Wi-Fi จนสถานะ CONNECTED แล้วเชื่อม MQTT กับ broker ที่เลือก
2. publish ข้อความหรือ telemetry แล้วเห็นบน subscriber ของโฮสต์
3. รับคำสั่งกลับที่อุปกรณ์ผ่าน subscribe และบันทึกคอนฟิกที่ใช้โดยไม่มีความลับในรายงาน

---

## ก่อนเริ่ม

- [ ] ผ่านโมดูล 5 อย่างน้อยอ่านเซ็นเซอร์ได้ (สำหรับ telemetry)
- [ ] SSID / รหัส Wi‑Fi ของห้อง (ไม่บันทึกลง Git)
- [ ] Broker host/port ที่เลือกใช้
- [ ] เครื่องมือ subscribe บน PC (MQTTX, mosquitto_sub, หรือ Hackathon web-app)

> **อย่า** publish รหัสผ่านหรือใบรับรองจริงลงรายงานสาธารณะ · snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส — ดูรายละเอียดที่หมายเหตุต้นบทเรียน [บทเรียน 6.1](../l01-mqtt-and-mqtts/README.md)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Wi‑Fi link (required) | ลิงก์ Wi‑Fi พร้อมก่อนแตะ MQTT |
| Lab B — MQTT connect + status (required) | สถานะ CONNECTED และมี client id ให้จด |
| Lab C — Publish and observe (required) | เห็น payload บนเครื่องมือโฮสต์อย่างน้อยหนึ่งครั้ง |
| Lab D — Subscribe / command path (required) | มีหลักฐานว่าข้อความจาก cloud/โฮสต์ถึงอุปกรณ์ |
| Lab E — เลือกต่อยอด (แนะนำ) | ส่งตาราง/สกรีนช็อต/ไฟล์ออกแบบสั้น ๆ |

---

## ฝึกเติม/แล็บ (1) — Lab A: Wi‑Fi link

1. เรียก `cm55_trigger_connect` หรือ `example_wifi_ui_connect` ตามโปรเจกต์
2. อ่าน `cm55_get_wifi_status` จน `IPC_WIFI_LINK_CONNECTED`
3. บันทึก SSID (ไม่ต้องบันทึกรหัสผ่าน)

---

## ฝึกเติม/แล็บ (2) — Lab B: MQTT connect + status

1. ตั้ง policy ให้ MQTT ใช้งานได้ (เช่น factory default)
2. `cm55_trigger_mqtt_connect`
3. อ่าน `cm55_get_mqtt_status` จน `state == CONNECTED (2)`
4. จด `broker_host`, `port`, `tls`, `effective_client_id`

```c
(void)cm55_trigger_mqtt_connect();
/* poll cm55_get_mqtt_status until connected or timeout */
```

---

## ฝึกเติม/แล็บ (3) — Lab C: Publish and observe

เลือกอย่างน้อยหนึ่งทาง:

**C1 Telemetry path** — เปิดเซ็นเซอร์ + policy `TELEMETRY_PUBLISH` แล้ว subscribe บนโฮสต์ที่ topic `bitstream/<MAC12>/sensors` (หรือ topic ที่คุณตั้งไว้) ยืนยันว่ามี JSON เข้ามา

**C2 Explicit publish** — ใช้เส้นทางใดเส้นทางหนึ่ง (`cm33_mqtt_stack_publish` หรือแผง Studio) ส่ง `{"hello":1}` เห็นข้อความบน subscriber

---

## ฝึกเติม/แล็บ (4) — Lab D: Subscribe / command path

1. Subscribe ฝั่งอุปกรณ์ที่ topic actuators (หรือใช้คอนฟิก topic table ที่มีอยู่)
2. จากโฮสต์ publish คำสั่งทดสอบไปยัง topic นั้น
3. บันทึกว่าอุปกรณ์ได้รับอย่างไร (log / LED / เหตุการณ์ตามที่เฟิร์มแวร์รองรับ)

---

## ฝึกเติม/แล็บ (5) — Lab E: เลือกต่อยอดหนึ่งอย่าง (แนะนำ)

**E1 MQTT vs MQTTs table** — กรอกตารางเปรียบเทียบจากการทดลองหรือจากเอกสารของชุดที่ใช้: พอร์ต, `tls`, CA

**E2 Hackathon web MQTT** — รัน `ex09`–`ex14` ตาม Hackathon README (broker ใน Studio ถ้าจำเป็น)

**E3 Payload design** — ออกแบบ JSON สำหรับ event จากโมดูล 5 (เกณฑ์อุณหภูมิ/ฟีเจอร์) แล้วลอง publish หนึ่งครั้ง

---

## เช็กความเข้าใจ — สรุปรายงานสั้น (10–15 บรรทัด)

เตรียมคำตอบก่อนเขียนรายงาน (ห้ามมีความลับในรายงาน):

1. Wi‑Fi SSID (ไม่มีรหัสผ่าน)
2. Broker host:port และ tls 0/1
3. Client id / MAC topic ที่ใช้
4. หลักฐาน publish + subscribe
5. ข้อจำกัดที่สังเกต (เช่น QoS ของ telemetry, ต้องมี Wi‑Fi ก่อน)

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] Lab A–D ผ่าน
- [ ] Lab E อย่างน้อย 1 ข้อ
- [ ] กรอก [mqtt-cloud.md](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md)
- [ ] รายงานสั้นไม่มีความลับ

พร้อมแล้ว ไปต่อ **โมดูล 7 — การเชื่อมต่อ Bluetooth Low Energy (BLE)**

[บทเรียนโมดูล 7 →](../../m07-ble/l01-ble-connectivity/README.md)

---

## แหล่งที่มา

"บทเรียน 6.2 — แล็บ: Wi-Fi, MQTT connect, publish และ subscribe" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
