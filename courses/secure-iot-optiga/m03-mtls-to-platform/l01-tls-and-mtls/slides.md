---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — TLS และ mTLS"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 3.1 — TLS และ mTLS

## เข้าใจ handshake ของ TLS 1.3 และสิ่งที่เพิ่มขึ้นเมื่ออุปกรณ์ต้องยืนยันตัวตนด้วยใบรับรองของตัวเอง

**โมดูล 3 — mTLS สู่ TESAIoT Platform**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน
2. อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา
3. วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 2.2](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md) และไฟล์ `cert01` ที่ตรวจ fingerprint แล้ว (แล็บ 1.2)
- เครื่องมือ: `openssl` — แล็บหลักทำบนคอมพิวเตอร์ ส่วนบนบอร์ดเป็นแล็บเสริม

---

## ดูของจริงก่อน

```text
[mTLS] Setting up OPTIGA Trust M (cert=0xE0E0, key=0xE0F0)
[mTLS] Certificate read: %u bytes PEM
[MQTT] Connecting to '%s:8883' as '%s'...
[PSA-Sign] Using Key OID 0xE0F0 for TLS CertificateVerify (slot=%lu)
[MQTT] Connected to broker
```

**ทายก่อน** บรรทัดไหนคือตอนที่ชิปลงนาม และบรรทัดนั้นพิสูจน์ได้ไหมว่าการลงนาม **สำเร็จ**

---

## แนวคิด (1) — handshake ของ TLS 1.3

```text
 อุปกรณ์ (client)                                 broker (server)
 ClientHello + key_share            ──────▶
                                    ◀──────  ServerHello + key_share
                                             {Certificate} {CertificateVerify}
                                             {CertificateRequest} ← เฉพาะเมื่อขอ mTLS
                                    ◀──────  {Finished}
 {Certificate}        ← mTLS: ใบของอุปกรณ์
 {CertificateVerify}  ← mTLS: อุปกรณ์ลงนามบน transcript (ในชิป)
 {Finished}                         ──────▶
```

**ข้อเท็จจริงที่ต้องแยก** broker คุย TLS 1.3 ได้ แต่ค่าตั้ง mbedTLS ของ CM33_NS ที่ commit `ef72c1b` เปิดเฉพาะ **TLS 1.2** — ใน 1.2 ใบรับรองทั้งสองฝั่งเดินแบบ**ไม่เข้ารหัส** (ต่างจาก 1.3)

---

## แนวคิด (2) — ลายเซ็นเกิดในชิป กุญแจไม่ออกมา

`mqtt_mtls_setup_optiga()` เตรียมของก่อน handshake:

```text
1. ถือ touch-hold + optiga_manager_init() ก่อนงาน TLS ใด ๆ
2. เลือกตัวตน: ถ้า optiga_verify_cert_key_pair(0xE0E1,0xE0F1) ผ่าน ใช้คู่ TESAIoT
   ไม่งั้นใช้คู่จากโรงงาน 0xE0E0/0xE0F0
3. อ่านใบรับรองเป็น PEM ส่งให้ TLS stack
4. สร้าง key handle แบบ opaque (PSA_KEY_LOCATION_OPTIGA) — ไม่ได้สร้างกุญแจใหม่ แค่ "ชื่อ"
```

ตอนสร้าง `CertificateVerify` mbedTLS → PSA → `optiga_psa_sign()` → `trustm_ecdsa_sign()` (ถือประตู+hold ตลอด) — **ไม่มีจุดไหนที่ไบต์ของกุญแจลับออกจากชิป**

**คำตอบคำทาย** `[PSA-Sign] Using Key OID ...` พิมพ์**ก่อน**การลงนาม สัญญาณว่าสำเร็จคือบรรทัดนี้ **+ไม่มี**บรรทัด ERROR **+** `[MQTT] Connected to broker`

---

## แนวคิด (3) — mTLS พิสูจน์อะไร และไม่พิสูจน์อะไร

ถ้าใช้คู่จากโรงงาน ใบ `CN=InfineonIoTNode` เหมือนกันทุกชิป → handshake พิสูจน์ได้แค่ว่าเป็น Trust M ของแท้ **ไม่มีอะไรผูกตัวตน (device_id) กับใบที่แสดง** — ตัวควบคุมจริงอยู่ฝั่ง broker (ACL ผูกกับ fingerprint ของกุญแจสาธารณะ ไม่ใช่ subject)

**TLS/mTLS ไม่ได้ป้องกัน**

- ข้อมูลที่พักอยู่บนอุปกรณ์หรือแพลตฟอร์ม (ปกป้องแค่ระหว่างทาง)
- ปลายทางที่ถูกเจาะแล้ว · ACL ที่ตั้งผิด
- ใบที่หมดอายุ/ถูกเพิกถอน (ในค่าตั้งนี้)
- การเชื่อมต่อที่ตั้ง `CY_AWS_ROOTCA_VERIFY_NONE` (เช่นบางเส้นทาง HTTPS) — เข้ารหัสแต่กันดักกลางทางแบบ active ไม่ได้

---

## แนวคิด (4) — อ่านอาการเมื่อการเชื่อมต่อล้ม

| อาการ | สาเหตุ |
|---|---|
| handshake ล้มก่อน MQTT CONNECT | trust anchor ไม่ตรงกับ CA ของ broker |
| ส่ง Certificate+ClientKeyExchange แล้วปิด ไม่มี CertificateVerify | ไม่ได้เรียก `optiga_manager_init()` ก่อน TLS |
| `psa_sign_hash()` ปฏิเสธ `PSA_ERROR_NOT_PERMITTED` | นโยบายกุญแจอนุญาตแค่ SHA-256 แต่ใช้ SHA-384 |
| `trustm_ecdsa_sign status=0x0102` | ชิปกับจอสัมผัสชนกันบน I2C (บทเรียน 2.2) |
| TLS ปิดหลัง CONNECT ในโหมด server-TLS | ต่อพอร์ต 8883 (ของ mTLS) แทน 8884 |

---

## ตัวอย่างสมบูรณ์ — mTLS บนคอมพิวเตอร์ (device-mtls)

```c
/* Resolve credential files */
char ca[512], crt[512], key[512];
join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
if (!(file_exists(crt) && file_exists(key))) {
  fprintf(stderr, "mTLS requires client_cert.pem and client_key.pem in %s\n", certs_dir);
  return 1;
}
```

บนคอมพิวเตอร์ กุญแจลับคือ **ไฟล์** `client_key.pem` ที่อ่านเข้า RAM — ใครคัดลอกไฟล์ได้ก็เป็นอุปกรณ์นี้ได้ บนบอร์ด ตำแหน่งเดียวกันคือ `cy_tls_set_optiga_key_id()` ที่ส่งแค่ **ชื่อ** ของกุญแจ — bundle จากการลงทะเบียนด้วย CSR **ไม่มีกุญแจลับใน ZIP**

---

## ฝึกเติม / แล็บ

**ฝึกเติม** เรียงข้อความ handshake ของ TLS 1.3 แบบ mTLS แล้วกำกับ **S**=เซิร์ฟเวอร์พิสูจน์ตัว **D**=อุปกรณ์พิสูจน์ตัว: ClientHello → ServerHello → EncryptedExtensions → CertificateRequest → Certificate(S) → CertificateVerify(S) → Finished(S) → Certificate(D) → CertificateVerify(D) → Finished(D)

**แล็บ** `openssl s_client` ที่พอร์ต 8884 ดู state ทีละข้อความ เทียบกับแผนภาพ · บังคับ `-tls1_2` ดูว่าบรรทัดไหนหายไป/เพิ่มมา · ต่อพอร์ต 8883 โดยไม่มีใบ client ดู alert · ตัด `-CAfile` ออกดู `Verify return code`

---

## เช็กความเข้าใจ

1. ใน mTLS อุปกรณ์พิสูจน์ว่าถือกุญแจลับของใบรับรองจริงด้วยข้อความใด
   - ก) ClientHello · ข) Certificate · ค) CertificateVerify · ง) EncryptedExtensions

2. `psa_generate_key()` ใน `mqtt_mtls_setup_optiga()` ทำอะไร
   - ก) สร้างคู่กุญแจใหม่ในชิปทุกครั้งที่เชื่อมต่อ · ข) คัดลอกกุญแจลับจากชิปมาไว้ใน RAM · ค) ลงทะเบียน handle แบบ opaque ที่ driver แปลงเป็น OID ของกุญแจในชิป ไม่ได้สร้างอะไรในชิป · ง) สร้างกุญแจ AES สำหรับ TLS record

3. ทำไมใน TLS 1.2 ผู้ที่ดักแพ็กเก็ตได้จึงอาจรู้ว่าเป็นอุปกรณ์เครื่องไหน แม้ข้อมูล MQTT จะถูกเข้ารหัส
   - ก) เพราะรหัสผ่านถูกส่งแบบไม่เข้ารหัส · ข) เพราะใบรับรองของทั้งสองฝั่งใน handshake ของ TLS 1.2 เดินแบบไม่เข้ารหัส · ค) เพราะ TLS 1.2 ไม่มีการเข้ารหัสเลย · ง) เพราะ MQTT CONNECT อยู่นอก TLS

---

## ไปต่อ

ตอนนี้เรารู้ว่าช่องทางปลอดภัยอย่างไร บทต่อไปจะตามเส้นทางของข้อมูลทั้งเส้น ตั้งแต่ไฟล์ตั้งค่าบนบอร์ดจนถึง broker

บทเรียนถัดไป: [บทเรียน 3.2: MQTTs ขึ้น TESAIoT Platform](../l02-mqtts-to-tesaiot/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK และ TESAIoT Developer Hub (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
