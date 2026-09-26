---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — กติกาการเข้าถึงชิป"
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

# บทเรียน 2.2 — กติกาการเข้าถึงชิป

## ใช้ประตูเข้าชิป lock และการกันหน้าจอสัมผัสออกจากบัสขณะชิปทำงาน ตามลำดับที่ SDK กำหนด

**โมดูล 2 — ชิปความปลอดภัย OPTIGA™ Trust M**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release
2. อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ
3. ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 2.1](../l01-secure-element-role/README.md) — build แม่แบบและรัน `ref_hsm` ได้แล้ว
- ทบทวน: task, priority, mutex และ `vTaskDelay()` ของ FreeRTOS
- บอร์ด: TESAIoT Dev Kit เปิด serial terminal ไว้

---

## ดูของจริงก่อน

ชิปความปลอดภัยกับตัวควบคุมจอสัมผัสใช้บัส I2C เส้นเดียวกัน ถูกสั่งจากคนละคอร์ เมื่อ CM55 อ่านจอสัมผัสขณะ CM33 คุยกับชิปอยู่ ธุรกรรมบางครั้งไม่จบ (ไลบรารีไม่มี timeout ในเส้นทางนั้น) — ลายเซ็นจึงไม่ล้มเหลว แต่ **ค้าง**

เส้นทาง mTLS แบบเก่าหยุดจอสัมผัสระหว่าง "ตั้งค่า" แล้วปล่อยตอนตั้งค่าเสร็จ

**ทายก่อน** ถ้าจุดที่หยุดจอสัมผัสดูถูกต้องแล้ว ทำไมบั๊กจึงยังเกิด — ลายเซ็นของ TLS เกิดขึ้น **ตอนไหน**

---

## แนวคิด (1) — ประตูเดียว สามชื่อ

| คู่ | ตอบคำถามว่า | ต่างจากคู่อื่นตรงไหน |
|---|---|---|
| `optiga_chip_enter()` / `exit()` | มี task อื่นถือชิปอยู่หรือไม่ | คืน `false` เฉพาะเมื่อมีคนอื่นถือ |
| `optiga_manager_lock()` / `unlock()` | ตัวจัดการพร้อมหรือยัง | คืน `false` ถ้ายังไม่ init |
| `optiga_manager_acquire()` / `release()` | ขอ `optiga_util_t *` พร้อมถือประตู | คืน `NULL` ถ้ายังไม่ init/รอไม่ได้ |

`optiga_manager_init()` ต้องมาก่อนทุกอย่าง — ก่อน init `enter()` **คืน `true`** ทั้งที่ไม่ได้ล็อกอะไร (ตั้งใจ) จึง **ห้ามใช้ `enter()` ถามว่าชิปพร้อมไหม**

ประตูนี้ **ซ้อนได้ในtask เดียวกัน** (ตัวนับความลึก) แต่ทุกการถือต้องมีการคืน — ลืม `release()` = ชิปถูกกันไว้ตลอดการบูตครั้งนั้น task อื่นรอ 10 วินาทีแล้วล้มทุกครั้ง (รวมการลงนาม TLS)

---

## แนวคิด (2) — touch-hold ต้องครอบทุกไบต์

คำตอบของคำทาย: ลายเซ็นสำคัญ **CertificateVerify** เกิดทีหลัง ข้างใน `cy_mqtt_connect()` — ถึงตอนนั้นจอสัมผัสกลับมาอ่านบัสแล้ว การ hold ต้องครอบ **ไบต์สุดท้ายที่คุยกับชิป** ไม่ว่ามันอยู่ที่ไหน

อาการที่ต้องจำ: `OPTIGA_COMMS_ERROR (0x0102)` = ธุรกรรมกับชิปวิ่งขณะ CM55 อ่านจอสัมผัสบนบัสเดียวกัน (พบจริง: เขียน metadata 8 ไบต์ผ่าน แต่เขียนใบรับรอง 580 ไบต์ล้มด้วย 0x0102 หลังลองซ้ำ 57 วินาที)

**กติกาของ hold** นับได้ (ซ้อนได้) · ครั้งแรกหน่วง ~50 ms · ใช้ใน task เท่านั้น · **hold ที่ไม่มีคนคืนทำให้จอหูหนวกถาวร** · ห้ามส่ง `IPC_CMD_TOUCH_RESUME` ตรง ๆ

**ลำดับการซ้อน** สิ่งที่ถือทีหลังต้องคืนก่อน (ถ้าเข้าด้วย lock แล้ว hold ขาออกต้อง release hold ก่อนแล้วค่อย unlock)

---

## แนวคิด (3) — งานยาวต้องออกจาก task วาดจอ

ธุรกรรมบางอย่างใช้เวลาเป็นวินาที (สร้างคู่กุญแจ+ลงนาม CSR, รอ Protected Update) การขอประตูอาจรอถึง 10 วินาที — ถ้าเกิดใน task ของ LVGL จอจะค้างทั้งจอ **และ** `ui_busy_modal_service()` วาดหน้าต่างอธิบายไม่ได้ จอจึงทั้งตายและเงียบ

ทางแก้ของ SDK: `IPC_CMD_HSM_PROVISION` คืนค่าทันที งานจริงไปวิ่งใน worker task (`prov_task` ตรวจงานทุก 50 ms) จอใช้ `lv_timer` ถามสถานะเป็นระยะ

**งานที่ต้องไม่อยู่ใน callback ของปุ่ม/task วาดจอ** `optiga_manager_lock/acquire()` · คำสั่งคุยชิปและการรอ callback · การรอคำตอบเครือข่าย (ถึง 60 วินาที)

**กลับด้าน** อย่าถือ touch-hold ข้ามช่วงรอเครือข่าย — ไม่มีไบต์ไหนคุยกับชิปช่วงนั้น

---

## ตัวอย่างสมบูรณ์ — สองกติกา อายุเดียวกัน

```c
optiga_util_t *util = optiga_manager_acquire();
if (util == NULL) {
    /* acquire() releases the gate itself before returning NULL --
     * there is nothing to give back here. */
    printf("  optiga_manager_acquire() = NULL — busy, or the manager is not up\r\n");
    return SDK_EX_BUSY;
}
```

```c
/* optiga_manager_touch_hold_reason("Signing");
 * if (optiga_manager_lock()) {
 *     ... chip operations, including the wait for the callback ...
 *     optiga_manager_unlock();
 * }
 * optiga_manager_touch_release(); */
```

ทั้งประตูและ hold ต้องครอบช่วงเวลาเดียวกัน — ตั้งแต่ก่อนไบต์แรกจนหลังไบต์สุดท้าย **รวมช่วงที่รอ callback**

---

## ฝึกเติม / แล็บ

**ฝึกเติม** เติมช่องว่างของฟังก์ชัน `read_object_held()`: (1) `touch_hold_reason` กันจอ (2) `acquire` ถือประตู (3) ทางออก NULL เรียก `touch_release` **ไม่ใช่** `release` (4) `release` คืนประตูหลังรอ callback (5) `touch_release` คืน hold ทีหลัง

**แล็บ**

1. build+flash `03_chip_ownership` จดตัวนับความลึกของประตูแต่ละบรรทัด
2. build ใหม่ `04_touch_hold` แตะจอรัว ๆ ระหว่างทำงาน จดว่าเห็น reason message ไหม
3. **ออกแบบ** ปุ่ม "อ่านใบรับรอง" — วาดลำดับสี่ส่วน: callback ปุ่ม, worker task ที่ถือประตู/hold, `lv_timer` ถามสถานะ ระบุสามอย่างที่ห้ามเกิดใน callback

---

## เช็กความเข้าใจ

1. ทำไม `optiga_chip_enter()` จึงใช้เป็นคำถามว่า "ชิปพร้อมหรือยัง" ไม่ได้
   - ก) เพราะมันช้า · ข) เพราะก่อน init มันคืน true ทั้งที่ไม่ได้ล็อกอะไร คืน false เฉพาะเมื่อมีคนอื่นถือชิป · ค) เพราะใช้ได้เฉพาะใน ISR · ง) เพราะมันเขียน metadata

2. โค้ดเรียก `acquire()` ได้ค่าไม่เป็น NULL แล้ว `return` ออกกลางทางโดยไม่เรียก `release()` ผลคืออะไร
   - ก) ไม่มีผล ประตูปล่อยเอง · ข) ชิปถูกกันไว้ตลอดการบูตครั้งนั้น task อื่นรอ 10 วินาทีแล้วล้ม รวมการลงนาม TLS · ค) ชิปรีเซ็ตตัวเอง · ง) LcsO เปลี่ยนเป็น operational

3. เส้นทาง mTLS แบบเก่าหยุดจอสัมผัสเฉพาะช่วงตั้งค่า ทำไมยังค้าง
   - ก) การตั้งค่าใช้เวลานานเกินไป · ข) ลายเซ็น CertificateVerify เกิดทีหลังใน cy_mqtt_connect() ตอนที่จอสัมผัสกลับมาอ่านบัสแล้ว · ค) ชิปไม่รองรับ TLS · ง) ใช้พอร์ตผิด

---

## ไปต่อ

ตอนนี้เรารู้ว่าชิปลงนามอย่างไรและต้องเข้าถึงอย่างไร โมดูลถัดไปจะตามลายเซ็นนั้นเข้าไปใน handshake ของ TLS

บทเรียนถัดไป: [บทเรียน 3.1: TLS และ mTLS](../../m03-mtls-to-platform/l01-tls-and-mtls/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
