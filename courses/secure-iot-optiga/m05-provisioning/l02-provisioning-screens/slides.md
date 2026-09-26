---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — หน้าจอลงทะเบียนบนอุปกรณ์"
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

# บทเรียน 5.2 — หน้าจอลงทะเบียนบนอุปกรณ์

## ส่งงานที่ใช้เวลาหลายวินาทีให้หน้าจอที่คอยถามสถานะ และปิดหน้าจอเก่าก่อนเปิดใหม่เสมอ

**โมดูล 5 — การลงทะเบียนอุปกรณ์อย่างปลอดภัย**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป
2. เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 5.1](../l01-csr-enrolment/README.md) และแนวคิดข้อ 3 ของ [บทเรียน 2.2](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md)
- บอร์ด: แม่แบบ build ด้วย `ENABLE_PAGE_EXAMPLES=1` — แล็บนี้ **ถอดข้อมูลรับรองของแพลตฟอร์มออกจากไฟล์ตั้งค่าก่อน** เพื่อให้การลงทะเบียนหยุดตั้งแต่ขั้นเชื่อมต่อ

---

## ดูของจริงก่อน

ถ้ารอผลของชิปแบบ inline จอจะค้าง **และ** `ui_busy_modal_service()` ก็วาดหน้าต่างอธิบายไม่ได้ — จอจึง "dead AND silent"

อีกเรื่อง: ถ้าหน้าต่างของรอบก่อนยังเปิดอยู่ การเปิดอีกหน้าต่างจะถูกปฏิเสธแบบเงียบ ๆ เพราะ `shell_open()` คืนทันทีเมื่อมีหน้าต่างอยู่แล้ว

**ทายก่อน** สำหรับคนที่ถือบอร์ด "จอค้างและเงียบ" กับ "แตะแล้วไม่มีอะไรเกิดขึ้น" ต่างกันไหม

---

## แนวคิด (1) — ทำไมต้องถามสถานะ ไม่ใช่รอ

งานเบื้องหลังหน้าจอ Enrol ใช้เวลานาน: ขอประตูเข้าชิปรอได้ถึง 10 วินาที, สร้างคู่กุญแจ+ลงนาม CSR เป็นธุรกรรมยาว, รอแพลตฟอร์มได้ถึง 60 วินาที

```text
 CM55 (จอ)                              CM33_NS
 ปุ่ม Enrol → hsm_enrol_open()
   ส่ง IPC_CMD_HSM_PROVISION ──▶ handle_hsm_provision()
   ◀── คืนทันที ──                ถ้ามีงานวิ่งอยู่ ปฏิเสธ REJECTED_BUSY
   lv_timer ถาม op=POLL ──▶      prov_task ตรวจทุก 50 ms
   ◀── state, step, ข้อความ ──   prov_say(state, step, "ข้อความสำหรับคนอ่าน")
```

จอไม่ต้องรู้เลยว่าชิปทำอะไรอยู่ — แค่ถามว่า "ตอนนี้ถึงไหน" แล้ววาด

---

## แนวคิด (2) — ปิดของเก่าก่อนเสมอ

`hsm_provision_ui_teardown()` ปิดหน้าต่างที่ค้างอยู่และ **ยกเลิก timer ที่ถามสถานะ** — เรียกซ้ำได้และปลอดภัยแม้ไม่มีอะไรเปิดอยู่ กันปัญหาสองแบบ

- **แตะแล้วเงียบ** ถ้าไม่ปิดของเก่า การเปิดใหม่ถูกปฏิเสธเงียบ ๆ
- **timer ค้างเขียนใส่หน้าจอที่ถูกสร้างใหม่** timer ของรอบก่อนยังยิงอยู่ อ้างวัตถุ LVGL ที่ถูกลบไปแล้ว

หน้าของ HSM เรียก `hsm_provision_ui_teardown()` เป็น **คำสั่งสุดท้าย** ของ callback ตอนหน้าถูกทำลาย (หลังลบ timer ของหน้าเองแล้ว)

---

## แนวคิด (3) — หน้าจอที่พูดความจริง

- หน้า **Protect** แสดงชุดการเปลี่ยนแปลงที่จะเกิด **ก่อน** ทำ และไม่เขียนอะไรจนกว่าจะกดยืนยัน
- หน้า **Enrol** ที่เจอช่องซึ่งถูกล็อก บอกว่า "This slot takes signed manifests only ... Nothing was changed." **ก่อน**สร้างกุญแจ
- ผลตัดสินสุดท้ายแยกสามกรณี: "can prove it holds the key" / "does not belong to this chip's key" / "the pair check could not run" — ต่างกันเพราะต้องการการตอบสนองต่างกัน (เหมือนหลักของ `02_model_signature_hook.c` ที่ไม่รวม "ไม่มีลายเซ็น" กับ "ตรวจไม่ได้" เป็นค่าเดียว)

---

## ตัวอย่างสมบูรณ์ — ปิดของเก่า → เปิดของใหม่ → คืนว่า "เริ่มแล้ว"

```c
/* Idempotent, and first. If an earlier run's overlay is still up, opening
 * another would be refused silently -- shell_open() returns when one
 * already exists -- and the tap would look like it did nothing. */
hsm_provision_ui_teardown();

if (s_open_protect_next) {
    s_open_protect_next = false;
    hsm_protect_open();
} else {
    s_open_protect_next = true;
    hsm_enrol_open();
}
/* The screen is up and its own poll timer owns the work from here.
 * That is asynchronous progress, not a completed job. */
return SDK_EX_STARTED;
```

ค่า `SDK_EX_STARTED` บอกตรง ๆ ว่างานยังวิ่งอยู่ เจ้าของงานตั้งแต่นี้คือ timer ของหน้าจอ ไม่ใช่ฟังก์ชันนี้

---

## ฝึกเติม / แล็บ

**ฝึกเติม** เติมช่องว่างของปุ่ม "ลงทะเบียน": (1) `hsm_provision_ui_teardown()` ก่อนเปิดอะไรทุกครั้ง (2) `hsm_enrol_open()` เปิดหน้าต่าง (3) `lv_timer_delete(s_clock_timer)` ลบ timer ของหน้าเอง (4) `hsm_provision_ui_teardown()` อยู่ท้ายสุดของ `destroy()`

**แล็บ** build+flash `01_hsm_screens` (ต้องถอด credential ออกจากไฟล์ตั้งค่าก่อน) — จดข้อความตามลำดับพร้อมเวลา ลองแตะ Back ระหว่างรอ จดว่าจอตอบสนองช่วงไหน (มองหา touch-hold reason) — กด Back แล้ว Run ซ้ำดูหน้า Protect ก่อนยืนยัน แล้วกด Back **โดยไม่ยืนยัน**

---

## เช็กความเข้าใจ

1. ถ้าหน้าจอ Enrol รอผลของชิปแบบ inline ใน task ของ LVGL ผลที่คนถือบอร์ดเห็นคืออะไร
   - ก) จอแสดงความคืบหน้าทีละขั้นตามปกติ · ข) จอค้างทั้งจอ และหน้าต่างที่อธิบายว่าทำไมค้างก็วาดไม่ได้ จอจึงทั้งตายและเงียบ · ค) ชิปทำงานเร็วขึ้น · ง) การลงทะเบียนถูกยกเลิกอัตโนมัติ

2. ลำดับใดถูกต้องเมื่อผู้ใช้แตะปุ่มเปิดหน้าจอลงทะเบียน
   - ก) `hsm_enrol_open()` แล้วค่อย `hsm_provision_ui_teardown()` · ข) `hsm_provision_ui_teardown()` แล้ว `hsm_enrol_open()` แล้วคืนค่าว่าเริ่มแล้ว · ค) `hsm_enrol_open()` แล้วรอจนเสร็จ · ง) ไม่ต้องปิดของเก่า

3. ทำไม `hsm_provision_ui_teardown()` ต้องเป็นคำสั่งสุดท้ายใน callback ที่ทำลายหน้า
   - ก) เพื่อให้ timer ที่ถามสถานะถูกยกเลิก ไม่ยิงใส่วัตถุ LVGL ที่ถูกคืนหน่วยความจำแล้ว · ข) เพราะมันช้าที่สุด · ค) เพื่อให้การลงทะเบียนเริ่มใหม่ · ง) เพราะมันล้าง correlation id

---

## ไปต่อ

ตอนนี้เรามีครบทุกชิ้นแล้ว threat model ช่องทาง mTLS ห่วงโซ่การบูต Protected Update การลงทะเบียน และหน้าจอที่พูดความจริง บทสุดท้ายรวมทั้งหมดเป็นอุปกรณ์หนึ่งชิ้น พร้อมหลักฐานว่ามันทำงานจริง

บทเรียนถัดไป: [บทเรียน 5.3: งานปลายทาง อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น](../l03-capstone-secure-device/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
