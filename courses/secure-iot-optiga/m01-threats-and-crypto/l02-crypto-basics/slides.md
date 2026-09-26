---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว"
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

# บทเรียน 1.2 — พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว

## แยกหน้าที่ของ hash, MAC, ลายเซ็นดิจิทัล การเข้ารหัสสองแบบ และใบรับรอง X.509

**โมดูล 1 — Threat model และพื้นฐานวิทยาการเข้ารหัส**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย (ความลับ ความถูกต้อง หรือการยืนยันตัวตน) ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี
2. อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้
3. อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 1.1](../l01-threat-modelling/README.md) — เปิดตาราง threat model ของคุณไว้ข้าง ๆ
- เครื่องมือ: คอมพิวเตอร์ที่มี `openssl`
- บอร์ด: ไม่ต้องใช้ในบทนี้ — ทุกการทดลองทำบนคอมพิวเตอร์

---

## ดูของจริงก่อน

```bash
openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev -showcerts </dev/null
```

ผลที่ได้มีใบรับรองสองใบ ใบแรก `CN = mqtt.tesaiot.dev` ออกโดย `CN = TESAIoT Intermediate CA` ใบที่สองคือ `TESAIoT Intermediate CA` เอง ออกโดย `TESAIoT Root CA`

**ทายก่อน** เฟิร์มแวร์ของบอร์ดมีใบรับรองใบไหนฝังอยู่ในตัวแล้ว — ใบของเซิร์ฟเวอร์ ใบ intermediate หรือใบ root

---

## แนวคิด (1) — สามเป้าหมาย สี่ครอบครัวเครื่องมือ

| เครื่องมือ | ใช้กุญแจอะไร | ให้อะไร | ให้ไม่ได้ |
|---|---|---|---|
| hash (SHA-256) | ไม่มีกุญแจ | ลายนิ้วมือของข้อมูล | ไม่รู้ว่าใครสร้าง |
| MAC (HMAC-SHA256) | กุญแจลับร่วมกัน | ความถูกต้อง+ตัวตน | พิสูจน์ต่อบุคคลที่สามไม่ได้ |
| ลายเซ็นดิจิทัล (ECDSA P-256) | คู่กุญแจ | ถูกต้อง+ตัวตน+พิสูจน์ได้ | ไม่ซ่อนข้อมูล |
| สมมาตร (AES) | กุญแจเดียวกัน | ความลับ เร็ว | ต้องตกลงกุญแจก่อน |
| ตกลงกุญแจ (ECDHE) | คู่กุญแจชั่วคราว | กุญแจร่วมโดยไม่ส่งกุญแจ | ไม่ยืนยันตัวตน |

`02_model_signature_hook.c` ของ SDK ตรวจ CRC ได้ครบแต่ยังคืน "ตรวจไม่ได้" (`-10`) ไม่ใช่ "ผ่าน" — hash/CRC ไม่มีกุญแจ ใครก็คำนวณใหม่ทับได้

---

## แนวคิด (2) — ใบรับรอง X.509 และห่วงโซ่ความเชื่อใจ

**สี่ฟิลด์ที่ต้องอ่านเป็น** subject · issuer · validity (notBefore–notAfter) · subjectPublicKeyInfo

ห่วงโซ่ของ broker: ใบเซิร์ฟเวอร์ ← TESAIoT Intermediate CA ← TESAIoT Root CA — อุปกรณ์เชื่อใบเซิร์ฟเวอร์เพราะเดินลายเซ็นย้อนไปจนเจอใบที่เชื่ออยู่แล้ว (**trust anchor**)

**ใบจากโรงงาน** ช่อง `0xE0E0` subject `CN=InfineonIoTNode` **เหมือนกันทุกชิป** — พิสูจน์ว่าเป็น Trust M ของแท้ แต่ไม่บอกว่าเป็นเครื่องไหน (serial/public key ต่างกันต่อชิป)

> **ยังไม่ตรวจ** ค่าตั้ง mbedTLS ของ CM33_NS ที่ commit นี้ปิด `MBEDTLS_HAVE_TIME_DATE` และ `MBEDTLS_X509_CRL_PARSE_C` — อุปกรณ์**ไม่ปฏิเสธใบเพราะหมดอายุหรือถูกเพิกถอน**

---

## แนวคิด (3) — ทำไมกุญแจลับควรอยู่ในชิป

กุญแจลับในไฟล์หรือ flash อ่านออกได้หลายทาง — ใครถือ image, เสียบพอร์ต debug, หรือถอดชิป flash ก็ได้กุญแจไปด้วย แล้วทำสำเนาไปกี่เครื่องก็ได้

OPTIGA™ Trust M เปลี่ยนคำถามจาก "กุญแจอยู่ที่ไหน" เป็น "ใครสั่งให้ชิปใช้กุญแจได้"

- กุญแจ**สร้างในชิป** ไม่มีคำสั่งอ่านออก (metadata: Change=never, ไม่มีสิทธิ์อ่าน)
- โปรแกรมส่ง **ชื่อช่อง (OID)** กับ digest เข้าไป แล้วได้ลายเซ็นกลับมา
- ฮาร์ดแวร์ผ่าน Common Criteria EAL6+ (high)

**ชิปไม่ได้กัน** การใช้กุญแจลงนามโดยเฟิร์มแวร์ที่ถูกยึดไปแล้ว (ขณะยังคุมบอร์ดอยู่) และสาย I2C ไม่ได้เข้ารหัสในค่าตั้งเริ่มต้น (`OPTIGA_COMMS_NO_PROTECTION`)

---

## ตัวอย่างสมบูรณ์ — ลงนามด้วยกุญแจในชิป

จาก `example_optiga_crypt_ecdsa_sign.c` (Infineon, MIT) — SDK ของบอร์ดใช้ host library รุ่นนี้

```c
/* 2. Sign the digest using Private key from Key Store ID E0F0 */
optiga_lib_status = OPTIGA_LIB_BUSY;
return_status = optiga_crypt_ecdsa_sign(
    me, digest, sizeof(digest),
    OPTIGA_KEY_ID_E0F0, signature, &signature_length
);
WAIT_AND_CHECK_STATUS(return_status, optiga_lib_status);
```

- `digest` = SHA-256 ของข้อมูล 32 ไบต์ — ลงนามบน digest ไม่ใช่ข้อมูลดิบ
- `OPTIGA_KEY_ID_E0F0` คือ **ชื่อช่อง** ไม่ใช่ตัวกุญแจ — กุญแจไม่โผล่ใน RAM ของ MCU เลย
- คำสั่งเป็น asynchronous — คืนค่าทันที ผลจริงมาทาง callback

---

## ฝึกเติม / แล็บ

**ฝึกเติม** เลือกเครื่องมือให้ถูกสถานการณ์ (ต้องถูก ≥4/5)

1. แพลตฟอร์มส่งใบรับรองใหม่ ต้องแน่ใจว่ามาจากแพลตฟอร์มจริง → **ลายเซ็นดิจิทัล**
2. เก็บ "ลายนิ้วมือ" ของ CA ไว้เทียบ → **hash**
3. อุณหภูมิผ่าน WiFi ร้านกาแฟต้องไม่ให้คนข้างโต๊ะอ่าน → **การเข้ารหัสสมมาตร**

**แล็บ** เก็บห่วงโซ่ใบรับรองจาก broker, อ่านสี่ฟิลด์ของแต่ละใบ, เทียบ fingerprint กับค่าที่ SDK บันทึกไว้, ลองแก้ข้อความหนึ่งตัวอักษรดู hash เปลี่ยนแค่ไหน, สร้างคู่กุญแจ P-256 ลงนามและตรวจบนคอมพิวเตอร์ (ครั้งแรก `Verified OK`, แก้ข้อความแล้ว `Verification failure`) แล้วลบไฟล์กุญแจทดลองทิ้ง

---

## เช็กความเข้าใจ

1. ทำไมฟังก์ชันตรวจลายเซ็นใน `02_model_signature_hook.c` จึงไม่คืน "ผ่าน" แม้ CRC จะถูกต้อง
   - ก) เพราะ CRC ช้าเกินไป · ข) เพราะใครก็คำนวณ CRC ใหม่ได้ มันไม่บอกว่าใครเขียน · ค) เพราะ CRC ต้องใช้กุญแจลับ · ง) เพราะ CRC ใช้ได้กับข้อมูลเข้ารหัสแล้วเท่านั้น

2. ใบรับรองจากโรงงานในช่อง `0xE0E0` มี subject `CN=InfineonIoTNode` ทุกชิป ข้อสรุปใดถูก
   - ก) ใบนี้บอกได้ว่าเป็นอุปกรณ์เครื่องไหน · ข) ใบนี้ปลอมแน่นอน · ค) ใบนี้พิสูจน์ว่าเป็น Trust M ของแท้ แต่ต้องใช้ serial หรือกุญแจสาธารณะถ้าจะแยกเครื่อง · ง) ใบนี้ไม่มีกุญแจสาธารณะ

3. ในค่าตั้ง mbedTLS ของ CM33_NS ที่ commit `ef72c1b` อุปกรณ์จะปฏิเสธใบรับรองของเซิร์ฟเวอร์ที่หมดอายุหรือไม่
   - ก) ปฏิเสธเสมอ · ข) ไม่ปฏิเสธด้วยเหตุผลเรื่องวันที่ เพราะ `MBEDTLS_HAVE_TIME_DATE` ถูกปิด · ค) ปฏิเสธเฉพาะเมื่อมี CRL · ง) ขึ้นกับ broker

---

## ไปต่อ

เราเห็นแล้วว่าชิปทำให้กุญแจไม่ต้องออกมาข้างนอก บทต่อไปจะเปิดดูข้างในชิปจริงบน TESAIoT Dev Kit ว่ามี object อะไร metadata บอกอะไร และคำสั่งไหนเปลี่ยนชิปแบบย้อนกลับไม่ได้

บทเรียนถัดไป: [บทเรียน 2.1: ชิปความปลอดภัยทำอะไรให้เรา](../../m02-optiga-trust-m/l01-secure-element-role/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) และ Infineon optiga-trust-m (MIT) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
