---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ชิปความปลอดภัยทำอะไรให้เรา"
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

# บทเรียน 2.1 — ชิปความปลอดภัยทำอะไรให้เรา

## รู้ว่า OPTIGA™ Trust M เก็บและทำอะไร และอ่านสถานะของ HSM จาก SDK โดยไม่เริ่มธุรกรรม

**โมดูล 2 — ชิปความปลอดภัย OPTIGA™ Trust M**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข
2. อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK
3. อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 1.2: พื้นฐานวิทยาการเข้ารหัส](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- บอร์ด: TESAIoT Dev Kit พร้อมสาย USB และ serial terminal
- ซอฟต์แวร์: TESAIoT PSE84 Dev Kit SDK ที่ commit `ef72c1b` และ ModusToolbox 3.6

หลัง flash ทุกครั้ง **ถอดสาย USB ออกจนสุด นับสิบ แล้วเสียบใหม่** (ไฟหน้าจอต้องการขอบสัญญาณแบบเย็น)

---

## ดูของจริงก่อน

`ref_hsm.c` ที่เราจะรันวันนี้เปิดไฟล์ด้วยประโยคว่า "THIS IS A REFERENCE LIST, NOT A JOB."

> It enrols nothing, publishes nothing, and writes nothing — to the chip or anywhere else.

และมี SAFETY note ว่าไฟล์นี้ไม่แตะ metadata tag `C0` ซึ่งเป็นสถานะวงจรชีวิตของชิปที่ "moves one way only and which no reflash undoes"

**ทายก่อน** ทำไมตัวอย่างแรกที่ SDK ให้เรารันกับชิปความปลอดภัย จึงตั้งใจ **ไม่ทำอะไรกับชิปเลย**

---

## แนวคิด (1) — ชิปนี้ทำอะไรได้บ้าง

OPTIGA™ Trust M คือ security controller ที่ผ่านการรับรอง Common Criteria EAL6+ (high)

| หน้าที่ | ฟังก์ชันใน host library | SDK ของบอร์ดใช้ทำอะไร |
|---|---|---|
| สร้าง/เก็บกุญแจลับ | `optiga_crypt_ecc_generate_keypair` | สร้างคู่กุญแจตอนลงทะเบียนด้วย CSR |
| ลงลายเซ็น/ตรวจ | `optiga_crypt_ecdsa_sign/verify` | ลงนาม CertificateVerify ใน mTLS |
| สุ่มเลขด้วย TRNG | `optiga_crypt_random` | ตัวช่วยใน `tesaiot_crypto.c` |
| อ่าน/เขียนข้อมูล+metadata | `optiga_util_read/write_*` | อ่านใบรับรองใช้ใน TLS |
| อัปเดตแบบป้องกัน | `optiga_util_protected_update_*` | รับใบรับรองใหม่ที่ลงนามจากแพลตฟอร์ม |

ส่วนที่เกี่ยวกับการครอบครองชิป/ลงทะเบียน/Protected Update ถูกห่อไว้ใน `libbento_hsm.a` (export 18 ฟังก์ชัน)

---

## แนวคิด (2) — Object, metadata และสถานะวงจรชีวิต

| OID | ค่าจากโรงงาน | TESAIoT ใช้ทำอะไร |
|---|---|---|
| `0xE0C2` | UID ของชิป 27 ไบต์ อ่านได้เสมอ เปลี่ยนไม่ได้ | client id ของ MQTT ในโหมด mTLS |
| `0xE0E0` / `0xE0F0` | ใบรับรอง/กุญแจจาก Infineon | ตัวตนจากโรงงาน |
| `0xE0E1` / `0xE0F1` | ช่องใบรับรอง/กุญแจ (เขียนได้เมื่อ LcsO < op) | ใบรับรอง/กุญแจของ TESAIoT |
| `0xE0E8` | ช่อง trust anchor | anchor ที่ตรวจ manifest ของ Protected Update |

**metadata tag สำคัญ** `C0`=LcsO (01 creation → 03 → 07 op → 0F) · `C1`=version (กันย้อนรุ่น) · `D0`=Change access · `E8`=ชนิด object

`E1 FC 07` แปลว่า "เขียนได้ตราบที่ LcsO < op" — ช่องส่วนใหญ่เขียนได้เพราะชิปยังอยู่ที่ creation (`01`)

---

## แนวคิด (3) — สิ่งที่ย้อนกลับไม่ได้ และการอ่านสถานะแบบฟรี

**ย้อนกลับไม่ได้**

1. **LcsO (tag `C0`)** เดินทางเดียว `01→03→07→0F` — ไม่มี reflash/ลบ/ตัดไฟใดพากลับได้ เมื่อถึง `op` การเขียน metadata หยุดถาวร
2. **ตัวนับ version (tag `C1`)** ขึ้นได้อย่างเดียว
3. **Change=never** ของ `0xE0E0`/`0xE0F0` เปลี่ยนไม่ได้เลย

ส่วน **ล็อกของ Protected Update** (`D0`=`21 E0 E8`) กลับทางได้ **ตราบที่ LcsO < op**

**หลักสูตรนี้ไม่สั่งให้คุณเขียน `C0` หรือเลื่อน LcsO ไม่ว่ากรณีใด** — ผลคือบอร์ดใช้เรียนต่อไม่ได้ ไม่มีทางกู้

**อ่านสถานะแบบฟรี** `trustm_requested_target_oid()`, `trustm_requested_anchor_oid()`, `trustm_current_correlation_id()` — ไม่แตะชิป ส่วน `optiga_manager_lock()` **ไม่ฟรี** ต้องคืนด้วย `unlock()` เสมอ

---

## ตัวอย่างสมบูรณ์ — ตัดจาก ref_hsm.c

```c
const char *cid = trustm_current_correlation_id();
printf("  trustm_current_correlation_id()= %s\r\n",
       (cid != NULL) ? cid : "(none — nothing in flight)");

/* Chip readiness — a balanced probe, not a free read */
if (optiga_manager_lock()) {
    printf("  optiga_manager_lock()          = true  (manager up, chip free)\r\n");
    optiga_manager_unlock();
    printf("  optiga_manager_unlock()        — gate returned\r\n");
} else {
    printf("  optiga_manager_lock()          = false (manager not "
           "initialised, or another task holds the chip)\r\n");
}
```

**สามเรื่องที่ควรเห็น** พิมพ์ NULL ต้องมีตัวกัน · ถือแล้วต้องคืน · ค่า false ไม่บอกสาเหตุ

---

## ฝึกเติม / แล็บ

**ฝึกเติม** จัดกลุ่ม: `trustm_requested_anchor_oid()` (ฟรี) · `optiga_manager_lock()` (ถือประตู) · `optiga_crypt_ecdsa_sign(...)` (ธุรกรรมกับชิป) · เขียน tag `C0`=`07` (ย้อนไม่ได้)

**แล็บ** อ่านสถานะของ HSM โดยไม่เริ่มอะไรเลย

1. build+flash `ref_hsm` บน CM33_NS แล้วถอด/เสียบ USB
2. **ทายก่อนดูผล** ว่า `trustm_requested_target_oid()`, `optiga_manager_lock()` จะได้ค่าอะไร
3. เทียบผลจริงกับที่ทาย
4. build ใหม่ด้วย `03_chip_ownership` ดูว่า `optiga_manager_lock()` เปลี่ยนไปอย่างไร

**ข้อห้าม** ไม่เปิด `EXAMPLE_HSM_REQUEST_PU`/`EXAMPLE_HSM_ISOLATED_TEST` และไม่เขียน metadata ใด ๆ

---

## เช็กความเข้าใจ

1. ข้อใด **ไม่ใช่** หน้าที่ที่ OPTIGA™ Trust M ทำให้ SDK ของบอร์ด
   - ก) สร้างเลขสุ่มด้วย TRNG · ข) ลงลายเซ็น ECDSA ด้วยกุญแจที่อยู่ในชิป · ค) เข้ารหัสภาพบนจอ LCD · ง) เก็บกุญแจลับที่สร้างขึ้นในชิป

2. `ref_hsm.c` บอกว่าฟังก์ชันใด **ไม่ใช่** การอ่านแบบฟรี
   - ก) `trustm_requested_target_oid()` · ข) `trustm_current_correlation_id()` · ค) `optiga_manager_lock()` · ง) `trustm_requested_anchor_oid()`

3. ทำไมหลักสูตรนี้จึงไม่สั่งให้เขียน tag `C0`
   - ก) เพราะชิปไม่รองรับ · ข) เพราะ LcsO เดินทางเดียว ไม่มี reflash ใดพากลับได้ และเมื่อถึง op การเขียน metadata จะหยุดถาวร · ค) เพราะต้องใช้รหัสผ่านจาก Infineon · ง) เพราะจะทำให้ WiFi ใช้ไม่ได้

---

## ไปต่อ

เราเห็นแล้วว่าแค่ถามว่า "ชิปว่างไหม" ก็ต้องถือประตูแล้วคืน บทต่อไปจะลงลึกเรื่องประตูนั้น ว่าทำไมมีสามชื่อ

บทเรียนถัดไป: [บทเรียน 2.2: กติกาการเข้าถึงชิป](../l02-chip-access-discipline/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
