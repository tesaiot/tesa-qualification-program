---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — ลงทะเบียนด้วย CSR"
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

# บทเรียน 5.1 — ลงทะเบียนด้วย CSR

## สร้างคำขอใบรับรองจากกุญแจในชิป ส่งให้แพลตฟอร์ม และติดตามคำขอจนได้ใบรับรอง

**โมดูล 5 — การลงทะเบียนอุปกรณ์อย่างปลอดภัย**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป
2. ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK
3. ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 4.2](../../m04-secure-boot-and-update/l02-protected-update/README.md) และไฟล์ `lab_key.pem` จากแล็บ 1.2
- บนคอมพิวเตอร์: `openssl` · บนบอร์ด: แม่แบบของ SDK ที่ build ได้แล้ว

---

## ดูของจริงก่อน

กด HSM Security → Enrol Certificate — จอขึ้นเจ็ดประโยคตามลำดับ

```text
Connecting to the platform
Generating a key pair inside the secure element
Signing the request with the key that never leaves the chip
Sending the request to the platform
Waiting for the platform
Checking the certificate against the key in the chip
The device can prove it holds the key this certificate names
```

**ทายก่อน** ประโยคที่สามบอกว่ามีการ "ลงนามคำขอ" — ถ้าคำขอมีกุญแจสาธารณะอยู่แล้ว ทำไมยังต้องลงนามอีก และใครเป็นคนตรวจลายเซ็นนั้น

---

## แนวคิด (1) — CSR คืออะไร และทำไมกุญแจลับไม่ต้องออกจากชิป

CSR (PKCS #10) มีสามส่วน: **subject** · **กุญแจสาธารณะ** · **ลายเซ็น** ที่ผู้ขอลงบนสองส่วนแรกด้วยกุญแจลับคู่กัน

คำตอบคำทาย: ลายเซ็นนี้คือ **proof of possession** — ผู้ออกใบตรวจด้วยกุญแจสาธารณะในคำขอ ถ้าผ่าน แปลว่าผู้ขอถือกุญแจลับของคู่นั้นจริง **ผู้ออกใบไม่เคยต้องเห็นกุญแจลับเลย**

```text
1. สร้างคู่กุญแจในชิป แล้วสร้าง CSR แบบ PEM (consumer_must_provide.txt)
2. publish_csr() ห่อเป็น JSON publish ไปที่ device/<id>/commands/csr
3. แพลตฟอร์มลงนามตอบกลับที่ commands/certificate (ไม่มี manifest)
4. subscriber เขียนใบลงช่อง แล้วตรวจว่าใบเข้าคู่กับกุญแจในชิป
```

---

## แนวคิด (2) — ติดตามคำขอด้วย correlation id และ OID

- **subscribe `commands/#` ก่อน publish CSR เสมอ** คำตอบไม่ถูก retain — คำตอบที่มาก่อน subscription สำเร็จหายไปเลย
- **หัวข้อใช้ `device_id` เสมอ** ไม่ใช่ UID ของ Trust M
- **CSR ที่ถูกปฏิเสธเงียบ** ไม่มีอะไรตอบกลับ — CSR ต้องยาวกว่า 100 ไบต์

**กับดักสำคัญ** `trustm_requested_target_oid()`/`anchor_oid()` ถูกเขียนโดย `tesaiot_publish_protected_update()` **เท่านั้น** — หลังเรียก `publish_csr()` อย่างเดียว สองค่านี้จึงบอกเรื่องคำขอ PU ครั้งก่อน **ไม่เคยบอกเรื่อง CSR นี้**

`trustm_reset_state()` **ล้าง correlation id** — ถ้าเรียกตอนคำตอบยังไม่มา ใบรับรองที่มาถึงจะไม่มีอะไรให้จับคู่ และถูกทิ้ง

---

## แนวคิด (3) — สัญญาเรื่องบัฟเฟอร์ของ publish_csr()

```c
int publish_csr(uint8_t *csr, size_t csr_length, uint16_t target_oid,
                 uint16_t trust_anchor_oid, uint32_t payload_version);
```

พารามิเตอร์แรกเป็น `uint8_t *` **ไม่ใช่** `const` — เพราะฟังก์ชัน**สร้าง JSON ทับลงในบัฟเฟอร์ของคุณ**

1. บัฟเฟอร์ต้อง**เขียนได้** — PEM แบบ `const` ใน flash จะทำให้ fault
2. บัฟเฟอร์ต้อง**ใหญ่กว่า CSR** — CSR + ~45 ไบต์คงที่ + device id + correlation id (แนะนำเผื่อ 256 ไบต์)
3. `csr_length` คือ**ความยาวของ CSR** ไม่ใช่ขนาดบัฟเฟอร์
4. **CSR หายไปเมื่อฟังก์ชันคืนค่า** — ต้องเก็บสำเนาไว้ก่อนถ้าจะใช้อีก

---

## ตัวอย่างสมบูรณ์ — ปฏิเสธก่อนส่ง CSR ปลอม

```c
/* Refuse rather than publish a fabricated CSR. A CSR the platform signs is
 * a certificate on a real device; the wrong one is worse than none. */
if (s_csr_len == 0u) {
    printf("  publish_csr() NOT called: s_csr is empty. Build a CSR first...\r\n");
    return SDK_EX_NO_DATA;
}
if (s_csr_len + 256u > sizeof(s_csr)) {
    printf("  publish_csr() NOT called: %u-byte CSR in a %u-byte buffer "
           "leaves no room for the JSON envelope\r\n",
           (unsigned)s_csr_len, (unsigned)sizeof(s_csr));
    return SDK_EX_REFUSED;
}
```

ตัวอย่างใช้บัฟเฟอร์ `static` ขนาด 1280 ไบต์ และทำความยาวเป็นศูนย์ทันทีหลังเรียก `publish_csr()`

---

## ฝึกเติม / แล็บ

**ฝึกเติม** ตัดสินว่า `publish_csr()` เรียกได้ไหม: CSR 620 ไบต์ในบัฟเฟอร์ 1280 → **เรียกได้** (620+256=876≤1280) · บัฟเฟอร์เป็น `const char[]` → **ต้องแก้** (เขียนไม่ได้) · `csr_length` = `sizeof(buf)` แทน 620 → **ต้องแก้**

**แล็บหลัก** build ตัวอย่าง 05 ไม่เปิด publish จดค่า correlation id/OID ที่พิมพ์ · สร้าง CSR บนคอมพิวเตอร์ด้วย UUID ปลอมที่เห็นชัดว่าปลอม ตรวจว่า `self-signature verify OK` · คำนวณขนาดบัฟเฟอร์ที่ต้องใช้ตามกฎ +256 ไบต์ แล้วลบไฟล์กุญแจทดลอง

---

## เช็กความเข้าใจ

1. ทำไมแพลตฟอร์มออกใบรับรองให้ได้โดยไม่ต้องเห็นกุญแจลับของอุปกรณ์
   - ก) เพราะแพลตฟอร์มเดากุญแจลับจากกุญแจสาธารณะได้ · ข) เพราะ CSR มีกุญแจสาธารณะ และลายเซ็นบน CSR พิสูจน์ว่าผู้ขอถือกุญแจลับคู่นั้น · ค) เพราะกุญแจลับถูกส่งไปแบบเข้ารหัส · ง) เพราะใบรับรองไม่เกี่ยวกับกุญแจ

2. หลังเรียก `publish_csr()` อย่างเดียว `trustm_requested_target_oid()` บอกอะไร
   - ก) ช่องที่ใบรับรองจาก CSR นี้จะถูกเขียน · ข) OID ของคำขอ Protected Update ครั้งก่อน หรือค่าเริ่มต้น ไม่ได้บอกเรื่อง CSR นี้ · ค) UID ของชิป · ง) correlation id

3. ข้อใดเป็นสัญญาเรื่องบัฟเฟอร์ของ `publish_csr()`
   - ก) บัฟเฟอร์เป็น const ได้ และ csr_length คือขนาดบัฟเฟอร์ · ข) บัฟเฟอร์ต้องเขียนได้ ใหญ่กว่า CSR csr_length คือความยาว CSR และ CSR หายไปหลังเรียก · ค) ฟังก์ชันจองบัฟเฟอร์ใหม่ให้เอง · ง) ต้องส่ง CSR แบบ DER เท่านั้น

---

## ไปต่อ

การลงทะเบียนใช้เวลาหลายวินาทีและต้องรอแพลตฟอร์มได้ถึงหนึ่งนาที บทต่อไปดูว่าหน้าจอบนอุปกรณ์รับมือกับงานยาวแบบนี้อย่างไรโดยไม่ค้างและไม่เงียบ

บทเรียนถัดไป: [บทเรียน 5.2: หน้าจอลงทะเบียนบนอุปกรณ์](../l02-provisioning-screens/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
