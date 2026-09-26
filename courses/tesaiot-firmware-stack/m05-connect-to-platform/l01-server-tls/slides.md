---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 5.1 — ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS

## ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS

**ไม่ต้องใช้บอร์ด (รันบนคอมพิวเตอร์) · คอมพิวเตอร์ (host PC) · ภาษา C**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C
2. อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l07`
- บอร์ด: ไม่ต้องใช้บอร์ด (รันบนคอมพิวเตอร์)
- แพลตฟอร์ม: คอมพิวเตอร์ (host PC)
- เวลาโดยประมาณ: เนื้อหา 15 + แล็บ 45 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด

[README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls) · commit `d2ed42c`

---

# แนวคิด — Server-TLS ยืนยันตัวตนของใคร

เซิร์ฟเวอร์ยื่นใบรับรองให้อุปกรณ์ตรวจก่อนเสมอ — ตรวจกับ CA ที่เชื่อถือได้ + ชื่อโฮสต์

นี่คือสิ่งเดียวที่ Server-TLS ยืนยัน: **ตัวตนของเซิร์ฟเวอร์** ไม่ใช่ตัวตนของอุปกรณ์

`main.c`: `tls.client_cert`/`client_key` = `NULL` เสมอ แต่ `verify_peer = 1U` ยังเปิดอยู่ตลอด

---

# แนวคิด — สองทางพิสูจน์ตัวตนของอุปกรณ์

เลือกผ่าน `COMM_MODE`: HTTPS ส่ง header `X-API-KEY` (ไม่ส่ง Bearer) / MQTTS ใช้ `username=device_id` + `password`

ทั้งสองทางยังเป็น Server-TLS เหมือนกัน ต่างแค่วิธีที่อุปกรณ์พิสูจน์ตัวเอง

ความลับ (API key/password) เดินทางในอุโมงค์ TLS ที่เข้ารหัสแล้วเสมอ ไม่ส่งแบบข้อความเปล่า

---

# แนวคิด — ca-chain.pem กับ system trust

MQTTS: ใช้ `ca-chain.pem` ของอุปกรณ์ตรวจ broker พร้อม `tls.sni_name = mqtt_host`

HTTPS: เขียนทับเป็น `tls.ca_chain = NULL` — ใช้ system trust แทน เพราะปลายทางสาธารณะมี public CA

รายละเอียดต่างกันตามทางเชื่อมต่อภายในตัวอย่างเดียวกัน ไม่ใช่กฎตายตัว

---

# แนวคิด — พอร์ตแยกตามวิธีพิสูจน์ตัวตน

Server-TLS: MQTT พอร์ต 8884, HTTPS พอร์ต 443

mTLS (บทเรียนถัดไป): ใช้พอร์ตอื่น — ใช้ผิดพอร์ตจะเจอ TLS ปิดหลัง CONNECT ทันที

---

# แนวคิด — ลำดับขั้นตอน และจุดที่ล้มเหลว

(1) อ่าน credential → (2) TLS handshake (`verify_peer` เสมอ) → (3) ส่ง credential ในอุโมงค์ → (4) publish JSON

ขั้น 2 ล้ม (เวลาเครื่องผิด/ใบรับรองหมดอายุ) → handshake ล้มก่อนถึงขั้น 3 เสมอ

ขั้น 2 ผ่านแต่ขั้น 3 ผิด → broker ตอบ Code 5 "Not authorized" (คนละสาเหตุกับปัญหา TLS)

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sec.tls` (ระดับ 2)
- `proto.mqtt` (ระดับ 2)
- `iot.cloud-platform` (ระดับ 2)

---

## ก่อนรันตัวอย่าง — ตั้งโฮสต์เป็น tesaiot.dev

`config.h` ของตัวอย่างที่ commit นี้ยังตั้งค่าเริ่มต้นเป็นโดเมนเดิมของแพลตฟอร์มที่ลงท้ายด้วย .com ซึ่งย้ายไปเป็น tesaiot.dev แล้ว
โดเมนเดิมของ API ไม่ resolve แล้ว ส่วนของ MQTT ยังใช้ได้ชั่วคราว ให้ตั้ง `DEFAULT_API_BASE_URL` เป็น `https://tesaiot.dev` และ `DEFAULT_MQTT_HOST` เป็น `mqtt.tesaiot.dev`
(บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

---

# ตัวอย่างสมบูรณ์ — TLS conf เริ่มต้น

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `d2ed42c` · [`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L297-L301)

```c
iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
tls.ca_chain = file_exists(PATH_CA_CHAIN) ? PATH_CA_CHAIN : NULL;
tls.client_cert = NULL; tls.client_key = NULL; /* serverTLS */
tls.verify_peer = 1U;
```

ไม่มีใบรับรองฝั่งอุปกรณ์ แต่ยังตรวจฝั่งเซิร์ฟเวอร์เสมอ

---

# ตัวอย่างสมบูรณ์ — สาขา MQTTS

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L331-L341)

```c
/* MQTTS (Server‑TLS): username/password + CA verify */
mreq.username = (mqtt_user[0] != '\0') ? mqtt_user : dev_id;
mreq.password = (mqtt_pass[0] != '\0') ? mqtt_pass : NULL;
mreq.topic = topic; mreq.payload = json;
mreq.qos = 1U;
tls.sni_name = mqtt_host;
const int rc = iot_mqtts_publish(&mreq, &tls);
```

ใช้ `ca-chain.pem` ของอุปกรณ์ตรวจ broker + พิสูจน์ตัวเองด้วย username/password

---

# ตัวอย่างสมบูรณ์ — สาขา HTTPS

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L344-L354)

```c
/* HTTPS (Server‑TLS): Bearer/X-API-KEY */
/* ... */
tls.ca_chain = NULL;
tls.sni_name = NULL;
/* For Server‑TLS HTTPS, send only X-API-KEY (omit Bearer) */
hreq.api_key = api_key;
const int rc = iot_https_post(&hreq, &tls);
```

ใช้ trust store ของระบบแทน `ca-chain.pem` + พิสูจน์ตัวเองด้วย `X-API-KEY`

---

# ตัวอย่างสมบูรณ์ — credential และลิงก์

ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

[ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)

ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

---

# จุดที่มักพลาด

- คิดว่า Server-TLS ยืนยันตัวตนอุปกรณ์ด้วย — จริงยืนยันแค่เซิร์ฟเวอร์ อุปกรณ์ต้องมี API key/password แยก
- ใช้พอร์ตผิดโหมด (8883 แทน 8884) — TLS ปิด connection หลัง CONNECT ทันที
- เจอ Code 5 แล้วคิดว่าเป็นปัญหา TLS — จริงคือ TLS ผ่านแล้ว เป็นขั้นพิสูจน์ตัวตนอุปกรณ์
- คิดว่า `ca-chain.pem` ใช้ตรวจทุกทางเสมอ — ตัวอย่างนี้ HTTPS ใช้ system trust แทน

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- Server-TLS ยืนยันตัวตนของใคร และไม่ได้ยืนยันของใคร
- ถ้าเวลาในเครื่องผิด TLS อาจล้มเหลวเพราะอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 2 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)
