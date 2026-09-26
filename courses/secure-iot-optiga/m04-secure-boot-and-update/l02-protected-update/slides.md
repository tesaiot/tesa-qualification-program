---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — Protected Update"
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

# บทเรียน 4.2 — Protected Update

## ขออัปเดตแบบป้องกันจากแพลตฟอร์ม เข้าใจตัวนับกันย้อนรุ่น และการเปลี่ยนแปลงบนชิปที่ย้อนกลับไม่ได้

**โมดูล 4 — Secure boot และ Protected Update**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายขั้นตอนของ Protected Update ตั้งแต่คำขอจนถึงการตรวจ manifest
2. อธิบายหน้าที่ของตัวนับกันย้อนรุ่น และผลของ manifest lock
3. ระบุการเปลี่ยนแปลงบนชิปที่รีแฟลชแล้วก็กู้คืนไม่ได้ ตามที่ตัวอย่างของ SDK เตือนไว้

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 4.1](../l01-secure-boot/README.md) และตาราง metadata ใน [บทเรียน 2.1](../../m02-optiga-trust-m/l01-secure-element-role/README.md)
- Protected Update ในบทนี้คือการอัปเดต **object ในชิป** (ใบรับรอง กุญแจ metadata) **ไม่ใช่**การอัปเดตเฟิร์มแวร์ของ MCU

---

## ดูของจริงก่อน

```text
[PU-Ingest] STEP 4: Executing OPTIGA Trust M Protected Update
[PU-Ingest] [4.1] Manifest verification OK (Trust Anchor signature valid)
[PU-Ingest] PROTECTED UPDATE COMPLETED SUCCESSFULLY!
```

**ทายก่อน** ถ้า host ถูกเจาะ ผู้โจมตีพิมพ์บรรทัดไหนในนี้ปลอมได้บ้าง และอะไรคือหลักฐานที่เขา **ปลอมไม่ได้**

---

## แนวคิด (1) — จากคำขอถึงการตรวจ manifest ในชิป

OPTIGA™ Trust M ไม่รับใบรับรองที่เขียนเป็นไบต์ธรรมดาลงช่องที่ถูกป้องกัน — ต้องมี **manifest** ที่ลงนามด้วยกุญแจที่ชิปเชื่ออยู่แล้ว (**trust anchor**) กับ **fragment** ที่บรรจุข้อมูลจริง

```text
1. subscribe device/<id>/commands/#  (ก่อนขอเสมอ)
2. tesaiot_publish_protected_update("E0E1","E0E8",ver,with_csr)
   → ตรวจในเครื่องก่อน (ช่องถูกล็อกกับ anchor อื่นอยู่ไหม)
3. เขียนใบของผู้ลงนามลง 0xE0E8 ตั้งชนิดเป็น trust anchor
4. optiga_util_protected_update_start(manifest)
   ▶ ชิปตรวจลายเซ็นของ manifest กับ 0xE0E8   ◀ จุดที่ host ปลอมไม่ได้
5. ส่ง fragment ชิปเขียนช่องเป้าหมาย
```

**คำตอบคำทาย** ทุกบรรทัด printf host ที่ถูกเจาะพิมพ์อะไรก็ได้ — เหตุการณ์ที่ปลอมไม่ได้คือ **ชิปตรวจลายเซ็นสำเร็จ** หลักฐานจริงคือ**อ่าน metadata กลับมา** ไม่ใช่เชื่อ log

---

## แนวคิด (2) — ตัวนับกันย้อนรุ่น และ manifest lock

**ตัวนับ version (tag `C1`)** ชิปจำ version ของแต่ละ object และปฏิเสธ manifest ที่ version ไม่มากกว่าเดิม — ขึ้นได้อย่างเดียว กันการเอา manifest เก่าที่ถูกลงนามมาเล่นซ้ำ

**manifest lock (tag `D0`)** apply สำเร็จ → Change เป็น `21 E0 E8` → ช่องนั้นรับเฉพาะ manifest ที่ลงนามโดย anchor นั้น — **กลับทางได้ตราบที่ LcsO ยังต่ำกว่า op**

**รหัสผิดพลาดตัวเดียวแปลได้หลายอย่าง** `0x800F` เกิดได้ทั้งจาก: ช่องถูกล็อกกับ anchor อื่น, version เก่า, **หรือ**ช่อง trust anchor ว่าง (กรณีที่พบบ่อยที่สุด) — อย่าเพิ่งสรุปว่าลายเซ็นผิด

**กันเล่นซ้ำด้วย correlation id** bundle ที่มาถึงตอนไม่มีคำขอค้าง ต้อง**ทิ้ง**

---

## แนวคิด (3) — สิ่งที่รีแฟลชแล้วกู้คืนไม่ได้

| สิ่งที่เปลี่ยน | ย้อนได้ไหม |
|---|---|
| **LcsO (tag `C0`)** `01→03→07→0F` | **ไม่ได้เลย** — ไม่มีตัวอย่างใดใน SDK เขียน และ Protected Update ในบทนี้ไม่แตะ |
| ตัวนับ version (tag `C1`) | ไม่ได้ ขึ้นอย่างเดียว |
| manifest lock (tag `D0`) | ได้เฉพาะเมื่อ LcsO < op — บนอุปกรณ์ส่งมอบแล้วถือว่าถาวร |

> **ยังไม่ได้ทำงานจริง** `c_ota_client` มีฟิลด์ `file_hash`/`signature` ใน job document แต่ `ota_verify_firmware()` ยังเป็น TODO ที่คืน `OTA_OK` เสมอ — **ห้ามนำไปใช้กับอุปกรณ์จริงโดยไม่เติมการตรวจ**
>
> เส้นทางอัปเดตผ่าน BLE NUS ต้องยืนยัน Y/N บนจอ แต่คอมไพล์เฉพาะเมื่อ `ENABLE_PAGE_BENTO_BUDDY=1` และ **ในแม่แบบที่ส่งมอบ ไลบรารีนี้ยังไม่ได้ถูก link เข้าภาพเฟิร์มแวร์**

---

## ตัวอย่างสมบูรณ์ — คำขอ Protected Update

```c
#define EXAMPLE_PU_TARGET   "E0E1"   /* hex string, not 0xE0E1 */
#define EXAMPLE_PU_ANCHOR   "E0E8"
/* platform takes max(chip counter, its record, this) + 1 */
#define EXAMPLE_PU_VERSION  (1U)

int rc = tesaiot_publish_protected_update(EXAMPLE_PU_TARGET, EXAMPLE_PU_ANCHOR,
                                          (uint32_t)EXAMPLE_PU_VERSION, false);
```

ตัวอย่างนี้ **ปิดไว้เป็นค่าเริ่มต้น** ต้อง build ด้วย `DEFINES+=EXAMPLE_HSM_REQUEST_PU=1` — ไม่งั้นพิมพ์แค่แผนของคำขอแล้วข้ามไป (ความตั้งใจ: OID เป้าหมายควรถูกอ่านสองรอบก่อนกด)

เทียบกับบทเรียน 1.2: นี่คือกรณีเดียวกับ hook ตรวจโมเดล AI — ฟังก์ชันที่ชื่อ "verify" ต้องไม่คืนผ่านถ้ายังไม่ได้ตรวจจริง

---

## ฝึกเติม / แล็บ

**ฝึกเติม** ทำนายผล: ช่อง `0xE0E1` ถูกล็อกกับ `0xE0E9` แต่คำขอระบุ anchor `E0E8` → **(ข) ถูกปฏิเสธในเครื่องก่อนส่งคำขอ** · bundle ถูกต้องมาถึงหลังรีบูตตอนไม่มีคำขอค้าง → **(ง) เฟิร์มแวร์ทิ้ง bundle**

**แล็บหลัก** (ไม่ส่งจริง) build ตัวอย่าง 06 โดยไม่เปิดสวิตช์ — จดแผนของคำขอที่พิมพ์ วาดแผนภาพลำดับทำเครื่องหมายจุดที่ host ปลอมได้/ชิปตรวจลายเซ็น/ตัวนับเปลี่ยน

**แล็บเสริม** (ต้องได้รับอนุญาตจากผู้สอน) Protected Update จริง — อ่าน metadata ก่อน/หลัง **ถ้า `C0` เปลี่ยน หยุดและรายงานทันที**

---

## เช็กความเข้าใจ

1. ในเส้นทาง Protected Update ขั้นไหนที่ host ที่ถูกเจาะปลอมไม่ได้
   - ก) การพิมพ์บรรทัด "PROTECTED UPDATE COMPLETED SUCCESSFULLY!" · ข) การที่ชิปตรวจลายเซ็นของ manifest กับ trust anchor ของตัวเองสำเร็จ แล้วเขียนช่องเป้าหมาย · ค) การส่ง ACK ขึ้นแพลตฟอร์ม · ง) การ subscribe commands/#

2. ตัวนับ version (tag `C1`) ป้องกันอะไร
   - ก) ป้องกันไม่ให้ manifest ที่ลงนามถูกต้องแต่เป็นรุ่นเก่า ถูกนำมาใช้ซ้ำ · ข) ป้องกันการอ่านใบรับรอง · ค) ป้องกันการเชื่อมต่อ WiFi ซ้ำ · ง) ป้องกันการเขียน tag C0

3. ตามตัวอย่าง 06 การเปลี่ยนแปลงใดบนชิปที่ไม่มี reflash การลบ หรือการตัดไฟใดพากลับได้
   - ก) การเขียนใบรับรองลง 0xE0E1 · ข) การเลื่อน LcsO (metadata tag C0) · ค) การเชื่อมต่อ MQTT · ง) การอ่าน metadata

---

## ไปต่อ

Protected Update ต้องมีใบรับรองของอุปกรณ์อยู่ก่อน หรือส่ง CSR ไปพร้อมคำขอ โมดูลสุดท้ายจะดูการลงทะเบียนด้วย CSR ตั้งแต่สร้างกุญแจในชิปจนได้ใบรับรองกลับมา

บทเรียนถัดไป: [บทเรียน 5.1: ลงทะเบียนด้วย CSR](../../m05-provisioning/l01-csr-enrolment/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK และ TESAIoT Developer Hub (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
