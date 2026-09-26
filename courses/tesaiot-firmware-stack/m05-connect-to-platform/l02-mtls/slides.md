---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
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

# บทเรียน 5.2 — ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS

## ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS

**ไม่ต้องใช้บอร์ด (รันบนคอมพิวเตอร์) · คอมพิวเตอร์ (host PC) · ภาษา C**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ส่ง telemetry ด้วย mTLS โดยใช้ client certificate และ private key ของอุปกรณ์
2. เปรียบเทียบ Server-TLS กับ mTLS ในด้านความปลอดภัยและการดูแลกุญแจ

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l07`
- บอร์ด: ไม่ต้องใช้บอร์ด (รันบนคอมพิวเตอร์)
- แพลตฟอร์ม: คอมพิวเตอร์ (host PC)
- เวลาโดยประมาณ: เนื้อหา 15 + แล็บ 45 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด

[README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) · commit `d2ed42c`

---

# แนวคิด — mTLS คืออะไร

หลังเซิร์ฟเวอร์ยื่นใบรับรองให้ตรวจ (เหมือน Server-TLS) เซิร์ฟเวอร์ขอใบรับรองของอุปกรณ์กลับด้วย

อุปกรณ์ต้องพิสูจน์ว่าถือ private key คู่กับใบรับรองนั้น — private key เองไม่เคยถูกส่งผ่านเครือข่ายเลย

ต่างจาก Server-TLS ที่ต้องส่ง "ความลับ" (API key/password) ทุกครั้งที่เชื่อมต่อ

---

# แนวคิด — ไฟล์ที่ต้องมี และการตรวจก่อนเชื่อมต่อ

ต้องมี `client_cert.pem` และ `client_key.pem` ใน `certs_credentials/` เสมอ

`main.c`: `file_exists(crt) && file_exists(key)` — ถ้าไม่ครบ หยุดทันทีพร้อม error ไม่ลองเชื่อมต่อแบบไม่มีใบรับรอง

---

# แนวคิด — อุปกรณ์แบบ CSR: กุญแจไม่เคยออกจากเครื่องที่สร้างมัน

`scripts/generate_csr.sh` สร้างกุญแจด้วย `openssl` แล้ว `chmod 600` ทันที ที่ฝั่งอุปกรณ์เอง

แพลตฟอร์มได้แค่ CSR (มี public key) ไปลงนาม — bundle ที่ดาวน์โหลดจึง**ไม่มี** private key รวมมา

bundle รั่วก็ไม่ทำให้กุญแจรั่ว ต้องคัดลอกกุญแจมาวางเองด้วย `sync_csr_key.sh <DEVICE_ID>`

---

# แนวคิด — CA ที่ตรวจเซิร์ฟเวอร์ยังเป็น system trust

ต่างจาก MQTTS ใน Server-TLS ที่ใช้ `ca-chain.pem` ของอุปกรณ์ mTLS ตั้ง `tls.ca_chain = NULL` ทั้งสองสาขา

คอมเมนต์ในโค้ด: "Use system trust … Do not force device CA"

mTLS เพิ่มแค่การที่อุปกรณ์ต้องยื่นใบรับรองกลับ ไม่ได้เปลี่ยนวิธีตรวจเซิร์ฟเวอร์

---

# แนวคิด — พอร์ตของ mTLS ต่างจาก Server-TLS

mTLS: HTTPS พอร์ต 9444, MQTTS พอร์ต 8883

Server-TLS: HTTPS พอร์ต 443, MQTTS พอร์ต 8884

ส่ง HTTPS mTLS ไปพอร์ต 443 แทน 9444 → ปลายทางไม่ใช่ endpoint ของ mTLS (SAN/โดเมนไม่ตรง)

---

# แนวคิด — เปรียบเทียบ Server-TLS กับ mTLS

ทั้งคู่เข้ารหัสช่องทางเท่ากัน และตรวจเซิร์ฟเวอร์เหมือนกัน (`verify_peer = 1` เสมอ)

Server-TLS: เริ่มง่าย แต่ความลับเดินทางทุกครั้งที่เชื่อมต่อ — รั่วแล้วปลอมตัวได้ทันที

mTLS: ไม่มีความลับเดินทางเลย แต่ต้องดูแลใบรับรอง/กุญแจ — กุญแจรั่วกระทบแค่อุปกรณ์ตัวนั้น (ACL แยกตาม `device/<device_id>/…`)

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sec.tls` (ระดับ 3)
- `sec.crypto` (ระดับ 2)
- `iot.cloud-platform` (ระดับ 2)

---

## ก่อนรันตัวอย่าง — ตั้งโฮสต์เป็น tesaiot.dev

`config.h` ของตัวอย่างที่ commit นี้ยังตั้งค่าเริ่มต้นเป็นโดเมนเดิมของแพลตฟอร์มที่ลงท้ายด้วย .com ซึ่งย้ายไปเป็น tesaiot.dev แล้ว
โดเมนเดิมของ API ไม่ resolve แล้ว ส่วนของ MQTT ยังใช้ได้ชั่วคราว ให้ตั้ง `DEFAULT_API_BASE_URL` เป็น `https://tesaiot.dev:9444` และ `DEFAULT_MQTT_HOST` เป็น `mqtt.tesaiot.dev`
(บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

---

# ตัวอย่างสมบูรณ์ — ต้องมีใบรับรองและกุญแจก่อนเริ่ม

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `d2ed42c` · [`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L336-L343)

```c
join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
if (!(file_exists(crt) && file_exists(key))) {
  fprintf(stderr, "mTLS requires client_cert.pem "
                  "and client_key.pem in %s\n", certs_dir);
  return 1;
}
```

---

# ตัวอย่างสมบูรณ์ — ผูกใบรับรอง/กุญแจเข้ากับ TLS

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L386-L388)

```c
iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
tls.client_cert = crt; tls.client_key = key;
tls.verify_peer = 1U;
```

ยังตรวจเซิร์ฟเวอร์เหมือน Server-TLS ทุกประการ เพิ่มแค่ใบรับรอง/กุญแจของอุปกรณ์เอง

---

# ตัวอย่างสมบูรณ์ — สาขา MQTTS: ไม่มี username/password เลย

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L412-L419)

```c
/* ... */
tls.ca_chain = NULL; tls.sni_name = mqtt_host;
mreq.client_id = device_id;
mreq.username = NULL; mreq.password = NULL;
```

ใบรับรองทำหน้าที่พิสูจน์ตัวตนแทน username/password ทั้งหมด

---

# ตัวอย่างสมบูรณ์ — credential และลิงก์

ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

[ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)

ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

---

# จุดที่มักพลาด

- ลืมว่า bundle ของอุปกรณ์แบบ CSR ไม่มี private key มาด้วย — ต้องรัน `sync_csr_key.sh` ไม่ใช่ขอกุญแจใหม่จากแพลตฟอร์ม
- ใช้พอร์ตของ Server-TLS กับ credential แบบ mTLS หรือกลับกัน — เจอ SAN/โดเมนไม่ตรง
- คิดว่า mTLS ทำให้ไม่ต้องตรวจใบรับรองเซิร์ฟเวอร์อีก — `verify_peer = 1U` ยังเปิดเหมือนเดิม
- เข้าใจว่า Server-TLS กับ mTLS ใช้ `X-API-KEY` เหมือนกัน — mTLS ไม่ใช้ API key เลย

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- mTLS เพิ่มอะไรจาก Server-TLS
- ถ้า private key ของอุปกรณ์รั่ว ผลกระทบคืออะไร

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
