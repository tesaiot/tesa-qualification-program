---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — วินิจฉัยความผิดพลาดจากหลักฐาน"
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

# บทเรียน 3.2 — วินิจฉัยความผิดพลาดจากหลักฐาน

## แยกสาเหตุของความผิดพลาดด้วยตัวนับและผลลัพธ์ที่ตรงไปตรงมา แทนการเดาจาก log ที่ดูน่าเชื่อ

**โมดูล 3 — ดีบักด้วย SWD และ GDB**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 3.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ "ไม่มีผลลัพธ์" และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน
2. อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด
3. อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ

ใช้เวลาประมาณ 70 นาที

---

## ก่อนเริ่ม

ทวนจากบทเรียน 3.1 สองข้อ

1. เมื่อ CM33 หยุดที่ breakpoint อะไรยังทำงานต่อ และทำไมการหยุดจึงเปลี่ยนพฤติกรรมของระบบ
2. ในชุดเครื่องมือของแม่แบบนี้ เราต่อ debugger เข้า CM55 ได้หรือไม่ ถ้าไม่ได้ หลักฐานของ CM55 ต้องมาจากไหน

---

## ดูของจริงก่อน

เปิด [examples/06_pipeline_counters.c](examples/06_pipeline_counters.c) จำลองสายงานสามขั้นแบบเดียวกับ Edge AI ของ SDK สร้างความผิดพลาดสามแบบที่มองจากหน้าจอเหมือนกันหมด **ทายก่อนรัน**: กรณี `no verdict` ส่วนต่างของตัวนับตัวไหนจะเป็นศูนย์

```sh
gcc -std=c11 -Wall -Wextra -o pipeline examples/06_pipeline_counters.c
./pipeline
```

ทุกกรณีขึ้น `result=OK` เพราะผลลัพธ์ล่าสุดจากช่วงที่ยังดีอยู่ยังค้างอยู่ มีแต่ **ส่วนต่าง** ของตัวนับที่บอกว่าสายงานหยุดที่ขั้นไหน — SDK เขียนไว้ว่า **"A big number is not health; a big number that is not growing is a stall."**

---

## แนวคิด (1) — อาการเดียว สาเหตุหลายแบบ: ตั้งสมมติฐานก่อนแตะโค้ด

"หน้าจอขึ้น 0% และไม่มีอะไรเกิดขึ้น" — SDK บอกว่าอาการนี้ **"has four different causes and they need four different fixes"** ต้องเขียนสมมติฐานทุกข้อ แล้วเลือกหลักฐานที่ให้คำตอบต่างกันสำหรับแต่ละข้อ

| สมมติฐาน | ถ้าจริง ส่วนต่างในหนึ่งวินาที |
|---|---|
| ไม่มีข้อมูลไปถึงโมเดล | `feeds` +0 |
| task ประมวลผลไม่ทำงาน/ค้าง | `feeds` ขยับ `dq_calls` +0 |
| ประมวลผลได้แต่ไม่มีผล | `dq_calls` ขยับ `dq_ok` +0 |
| โมเดลไม่เคยโหลดสำเร็จตั้งแต่ต้น | ใช้ตัวนับอีกชุด |

> ลำดับการอ่านสำคัญ: เริ่มจากขั้นต้นของสายงาน และตรวจก่อนว่าการวัดเองใช้ได้ — ถ้าโมเดลเปลี่ยนระหว่างสองครั้งที่อ่าน ตัวนับถูกล้าง ส่วนต่างไม่มีความหมาย

---

## แนวคิด (1) ต่อ — เครื่องมือวัดที่อยู่ใต้จุดที่ค้าง ไม่มีวันเห็นการค้าง

เรื่องจริงจาก SDK: เรดาร์ค้างซ้ำ ๆ และตัวเฝ้าการค้างของเซนเซอร์เองรายงาน 0 ครั้ง เพราะมัน **"sits at the BOTTOM of the same loop that was stuck"**

> หลักฐานที่ใช้ได้ต้องอยู่ **นอก** สิ่งที่มันวัด

---

## แนวคิด (2) — อ่านตัวนับของ SDK: สะสม ส่วนต่าง และลำดับ

SDK ให้ตัวนับสองชุดที่ตอบคำถามต่างกัน

- **"ตอนนี้ยังทำงานอยู่ไหม"** `ai_engine_feeds()` `ai_engine_dq_calls()` `ai_engine_dq_ok()` — อ่านเป็น **ส่วนต่าง** สองครั้งห่างกัน 1 วินาที ด้วย `delta32()` แบบอิ่มตัว ("cleared on a model switch")
- **"เคยโหลดสำเร็จไหม"** `ai_engine_init_calls()` `ai_engine_last_init_rc()` — อ่าน **ครั้งเดียว** มีค่า sentinel `0x7FFFFFFF` แยก "ไม่เคยถูกเรียก" ออกจาก 0 ที่แปลว่า "สำเร็จ"

บรรทัด `[HB]` ทุกสิบวินาทีเป็นหลักฐานว่า CM33 ยังจัดตาราง task ได้ ถ้า CM55 ล้มด้วย fault ร้ายแรง มันกะพริบ LED เป็นรหัส (1=stack overflow, 2=malloc ล้ม, 3=HardFault) และเขียนค่า `0xDEAD0001-3` ไว้ใน SRAM — คอร์ที่ไม่มี console ก็ยังทิ้งหลักฐานได้ถ้าออกแบบไว้ก่อน

---

## แนวคิด (3) — ผลลัพธ์ที่บอกความจริง

ฟังก์ชันที่ไม่มีข้อมูลแล้วคืน 0 พร้อมบอกว่าสำเร็จ ทำให้คนปลายทางตัดสินใจผิดอย่างมั่นใจ — แคตตาล็อกของ SDK ตั้งกติกาว่า **"Every file returns an honest result code"** (`SDK_EX_OK`, `SDK_EX_UNAVAILABLE`, `SDK_EX_BUSY`, `SDK_EX_NO_DATA`, ...) และ **"If the hardware is absent the example says so rather than pretending to succeed"**

ตัวอย่างผลลัพธ์คลุมเครือที่ทำร้ายจริง

- **Appendix X #25** รหัส MQTT ถูกเขียนทับเมื่อลองใหม่ครบ — ข้อบกพร่องสามจุดในสามชั้นพิมพ์รหัสเดียวกันหมด
- **`radar_dsp_snapshot()`** คืน `false` เมื่อยังไม่มีเฟรมแรก ต่างจาก `target == 0` ที่แปลว่าไม่มีเป้าหมาย — SDK ตั้งใจแยกไว้

> **log ที่ดูน่าเชื่อไม่ใช่หลักฐาน** — บางบรรทัดมีอยู่ในซอร์สแต่ไม่เคยถูกพิมพ์: "If a document tells you to wait for one of them, the document is stale."

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 06_pipeline_counters.c

**ท่าที่ 1** `pipeline_tick()` จำลองสายงานหนึ่งจังหวะ ความผิดพลาดแต่ละแบบหยุดคนละขั้น
**ท่าที่ 2** `get_confidence()` คืน `RESULT_NO_DATA` ถ้ายังไม่เคยมีผล แต่ถ้าเคยมีแล้ว คืนผลล่าสุดซึ่งอาจเก่า
**ท่าที่ 3** `run_case()` อ่านตัวนับสองครั้งแล้วพิมพ์ทั้งค่าสะสมและส่วนต่าง

```c
typedef enum { RESULT_OK, RESULT_NO_DATA, RESULT_STALL } result_t;

result_t get_confidence(const pipeline_t *p, float *out) {
    if (!p->ever_had_result) {
        return RESULT_NO_DATA;      /* บอกความจริง ไม่ใช่คืน 0 */
    }
    *out = p->last_confidence;      /* อาจเก่า ผู้เรียกต้องรู้ */
    return RESULT_OK;
}
```

---

## ฝึกเติม

เปิด [practice/06_diagnose.c](practice/06_diagnose.c) — มีช่องให้เติม 5 จุด ตรรกะเดียวกับ 07_engine_health และ 10_model_load_diagnosis ของ SDK

1. `delta32()` แบบอิ่มตัว
2. `diagnose()` ตรวจว่าการวัดใช้ได้ (โมเดลไม่เปลี่ยน) ก่อน
3. `diagnose()` ตัดสินจากส่วนต่าง ขั้นต้นก่อนขั้นปลาย
4. `load_diagnosis()` ห้าสาเหตุตามลำดับ
5. `read_latest()` คืนผลที่บอกความจริง ไม่แตะค่าของผู้เรียกเมื่อไม่มีข้อมูล

```sh
gcc -std=c11 -Wall -Wextra -o diagnose practice/06_diagnose.c && ./diagnose
```

สังเกตว่ามี test บางข้อที่ผ่านตั้งแต่ก่อนเติม — test ที่ผ่านกับโค้ดที่ไม่ได้ทำอะไรเลย ไม่ได้พิสูจน์อะไร (หัวใจของบทเรียน 6.1) ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/06_diagnose.c](solution/06_diagnose.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. อาการ "หน้าจอ Edge AI ขึ้น 0% และไม่เปลี่ยน" ข้อใดเป็นสมมติฐานที่แยกกันได้ด้วยหลักฐานต่างกัน (เลือกได้หลายข้อ)
2. ตัวเฝ้าการค้างของเซนเซอร์เรดาร์อยู่ท้ายลูปของ task เรดาร์ แล้ว task ค้างกลางลูป ตัวเฝ้าจะรายงานอะไร และบทเรียนคืออะไร
3. `07_engine_health` วัดหนึ่งวินาทีได้ `feeds +50, dq_calls +50, dq_ok +0` ความผิดพลาดอยู่ขั้นใด
4. เรียงลำดับการตรวจของการวินิจฉัยการโหลดโมเดลแบบ `10_model_load_diagnosis`
5. ฟังก์ชันอ่านความชื้นจาก cache ยังไม่เคยอ่านเซนเซอร์สำเร็จเลย ควรทำอย่างไร

---

## แล็บ

**งาน:** วินิจฉัยสายงาน Edge AI บนบอร์ดจากตัวนับ แล้วตรวจสอบตัวอย่างวินิจฉัยของ SDK เองด้วยหลักฐาน

1. build ด้วย `ENABLE_PAGE_EXAMPLES=1` flash ถอดสายเสียบใหม่ เปิด serial console
2. รัน `cm55/edge_ai/07_engine_health` โดยยังไม่เริ่มโมเดลใด บันทึกข้อความ (ควรบอกไม่มีโมเดลทำงาน, NO_DATA)
3. เริ่มโมเดลหนึ่งตัว แล้วรัน `07_engine_health` อีกครั้ง บันทึกส่วนต่างทุกตัวและบรรทัด `VERDICT`
4. **ทายก่อน** แล้วรัน `cm55/edge_ai/10_model_load_diagnosis` เทียบกับกติกาของ README แคตตาล็อกและ Appendix X #1 — บอกว่าข้อสรุปไหน **เห็นกับตาบนบอร์ด** และข้อไหน **อนุมานจากการอ่านโค้ด**
5. ตรวจว่า `[HB]` มาครบทุกสิบวินาทีตลอดการทดลอง ถ้าขาดช่วง บันทึกเวลาและสิ่งที่ทำอยู่

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอผลของ 07 ทั้งสองครั้ง ตารางส่วนต่างและคำวินิจฉัย รายงานข้อ 4 และ log ของ `[HB]`

---

## ไปต่อ

- อ่าน Appendix X ข้อ #25 และ #27 ของเอกสาร SDK — ทั้งสองข้อเป็นตัวอย่างของอาการที่ชี้ผิดที่ แล้วเขียนตารางสมมติฐานของแต่ละข้อ
- โจทย์ท้าทาย: ออกแบบ struct "กล่องดำ" สำหรับโปรเจกต์ของคุณเอง ดูตัวอย่างใน [diag_blackbox.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/shared/include/diag_blackbox.h) (มีแต่ header ยังไม่มีไฟล์ .c ใดใช้มัน — การมีโค้ดอยู่ยังไม่ใช่หลักฐานว่ามันทำงาน)

บทถัดไปเข้าสู่โมดูล 4: [บทเรียน 4.1 — GPIO และ interrupt](../../m04-peripherals/l01-gpio-and-interrupts/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
