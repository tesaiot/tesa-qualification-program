---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.3 — PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
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

# บทเรียน 5.3 — PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป

## PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป

**Eva Kit (PSoC Edge E84 Eval) · PSoC Edge E84 · ภาษา C**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M
2. เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l07`
- บอร์ด: Eva Kit (PSoC Edge E84 Eval)
- แพลตฟอร์ม: PSoC Edge E84
- เวลาโดยประมาณ: เนื้อหา 15 + แล็บ 45 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

รันบนบอร์ด PSoC Edge E84 พร้อม OPTIGA™ Trust M (โปรเจกต์นี้มี BSP ของ Eva Kit: APP_KIT_PSE84_EVAL_EPC2)

[README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client) · commit `d2ed42c`

---

# แนวคิด — OPTIGA Trust M คืออะไร

secure element แยกต่างหาก (CC EAL6+) เชื่อมผ่าน I2C — สร้างและเก็บคู่กุญแจ ECC P-256 ในตัวเอง

เฟิร์มแวร์สั่งให้ชิป "เซ็น" ได้ แต่อ่านกุญแจส่วนตัวออกมาไม่ได้เลย เพราะไม่เคยเข้า RAM ของ MCU

งานเข้ารหัสอื่นของ TLS ยังทำโดย mbedTLS บน MCU ตามปกติ

---

# แนวคิด — OID: แผนที่กุญแจและใบรับรองในชิป

`0xE0C2` Factory UID (อ่านอย่างเดียว) · `0xE0E0`+`0xE0F0` Factory cert+key

`0xE0E1`+`0xE0F1` Device cert+key (ออกผ่าน Protected Update) · `0xE0E3` trust anchor (ROOT_CA)

ใบรับรองต้องคู่กับกุญแจที่ OID ตรงกันเสมอ ใช้ผิดคู่ = เซ็นไม่ตรงกับใบรับรองที่ยื่น

---

# แนวคิด — อ่านกุญแจไม่ได้ แต่สั่งเซ็นได้

`0xE0F0`/`0xE0F1`: Read = Never, Execute = Always (เซ็นได้เสมอ)

`0xE0E0`: Change = Never (แก้ไม่ได้หลัง provision) · `0xE0E1`: เขียนใหม่ได้

หัวใจของ hardware root of trust — debug เข้าไปอ่านหน่วยความจำก็คัดลอกกุญแจออกมาไม่ได้

---

# แนวคิด — Two-Certificate PKI และ SAFE MODE

Factory cert (`0xE0E0`+`0xE0F0`) สำหรับ bootstrap/กู้ระบบ vs Device cert (`0xE0E1`+`0xE0F1`) ใช้งานจริง

ทุกครั้งที่ boot/reset: `g_force_factory_cert = true` (SAFE MODE) — บังคับใช้ Factory cert ก่อนเสมอ

เหตุผล: Device cert/key อาจไม่ตรงกันหลัง reset แต่ Factory cert/key จับคู่ถูกต้องเสมอ

---

# แนวคิด — ลำดับขั้นตอน Protected Update

(1) OPTIGA สร้างคู่กุญแจในชิป (ที่ `0xE0F1`) → (2) สร้าง CSR ลงนามด้วยกุญแจนั้น

(3) ต่อ MQTT ด้วย Factory cert → ส่ง CSR ขึ้นแพลตฟอร์ม → (4) รับ manifest ที่ลงนามแล้วกลับมา

(5) OPTIGA ตรวจลายเซ็น manifest กับ trust anchor (`0xE0E3`) ก่อน แล้วจึงเขียนใบรับรองใหม่ลง `0xE0E1`

private key ไม่เคยออกจากชิปตลอดกระบวนการ — มีแต่ CSR (public key) และใบรับรองที่เดินทาง

---

# แนวคิด — เชื่อมต่อ MQTT ด้วยกุญแจใน OPTIGA

boot: อ่าน cert จาก OPTIGA → `optiga_psa_register()` + `psa_crypto_init()` → ผูก PSA key handle ที่ `PSA_KEY_LOCATION_OPTIGA`

"generate" ในที่นี้คือผูก handle เข้ากับ OID ที่มีกุญแจอยู่แล้ว ไม่ได้สร้างกุญแจใหม่

`cy_tls_set_optiga_key_id()` + `cy_tls_set_client_cert()` — TLS handshake ขั้น CertificateVerify เรียกกลับให้ OPTIGA เซ็นแฮช ไม่มีไบต์กุญแจไหลผ่าน RAM ของ MCU เลย

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sec.secure-element` (ระดับ 2)
- `sec.tls` (ระดับ 3)
- `sec.fundamentals` (ระดับ 2)

---

## ก่อนรันตัวอย่าง — ตั้งโฮสต์เป็น tesaiot.dev

`mqtt_client_config.h` ของตัวอย่างที่ commit นี้ยังตั้ง `MQTT_BROKER_ADDRESS` และ `MQTT_SNI_HOSTNAME` เป็นชื่อ MQTT เดิมของแพลตฟอร์มที่ลงท้ายด้วย .com
ชื่อนี้ยังใช้ได้ชั่วคราว แต่แพลตฟอร์มย้ายไปเป็น tesaiot.dev แล้ว ให้ตั้งทั้งสองค่าเป็น `mqtt.tesaiot.dev` (บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

---

# ตัวอย่างสมบูรณ์ — ไล่โค้ดตามลำดับนี้

โค้ดอยู่ใน tesaiot/developer-hub · commit `d2ed42c` (อ้างอิงด้วยลิงก์เท่านั้น ดูหัวข้อถัดไป)

- [`main.c#L491-L536`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/main.c#L491-L536) — ลำดับตอน boot: อ่าน cert, ลงทะเบียน PSA driver, ผูก TLS เข้ากับกุญแจ
- [`optiga_psa_se.c#L285-L323`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_psa_se.c#L285-L323) — `optiga_psa_sign()` ที่ mbedTLS เรียกระหว่าง handshake
- [`optiga_trust_helpers.c#L768-L824`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_trust_helpers.c#L768-L824) — `trustm_gen_ecc_keypair()` กับ `export_private=false`
- [`mqtt_task.c#L824-L834`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/mqtt_task.c#L824-L834) — เลือกใบรับรองแล้วสลับ OID ของกุญแจให้ตรงกัน

---

# ตัวอย่างสมบูรณ์ — credential และลิขสิทธิ์

ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

[ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client)

โค้ดชุดนี้อยู่ภายใต้ Cypress (Infineon) EULA จึงอ้างอิงด้วยลิงก์เท่านั้น

---

# จุดที่มักพลาด

- คิดว่าโค้ดนี้ generate กุญแจใหม่ทุกครั้งที่ boot — จริงแค่ผูก PSA handle เข้ากับ OID ที่มีกุญแจอยู่แล้ว (`OPTIGA_TLS_ATTACH_ONLY`)
- ใช้ใบรับรองกับกุญแจคนละ OID กัน — ต้องสลับ `optiga_psa_set_signing_key_oid()` ให้ตรงกับใบรับรองที่เลือกทุกครั้ง
- คิดว่า reset แล้วจะได้ Device Certificate ทันที — ทุก reset กลับไป SAFE MODE (Factory cert) ก่อนเสมอ
- รัน `make getlibs` ใหม่แล้วลืม `./apply_patches.sh` — patch หายไปพร้อม library, ใช้กุญแจใน OPTIGA ไม่ได้อีก

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- ทำไม private key ที่อยู่ใน secure element ปลอดภัยกว่าใน flash
- Protected Update ใช้ทำอะไรกับ certificate

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
