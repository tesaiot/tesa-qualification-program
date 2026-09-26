---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.3 — struct, pointer และบัฟเฟอร์วงแหวน"
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

# บทเรียน 1.3 — struct, pointer และบัฟเฟอร์วงแหวน

## จัดข้อมูลด้วย struct ส่งต่อด้วย pointer และรับข้อมูลต่อเนื่องด้วยบัฟเฟอร์วงแหวน

**โมดูล 1 — ภาษา C สำหรับไมโครคอนโทรลเลอร์และหน่วยความจำ**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 1.2

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้
2. เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน
3. อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

---

## ก่อนเริ่ม

ทวนจากบทเรียน 1.2 สองข้อ

1. บัฟเฟอร์ 512 ไบต์ที่ประกาศเป็นตัวแปร local ใน task ที่มี stack 256 word จะเกิดอะไรขึ้น แล้วควรประกาศแบบไหนแทน
2. ทำไม `head - tail` ของตัวนับ `uint32_t` จึงยังถูกต้องแม้ `head` จะวนกลับผ่านศูนย์ไปแล้ว

---

## ดูของจริงก่อน

เปิด [examples/03_sensor_sample.c](examples/03_sensor_sample.c) **ทายก่อนรัน**: `sizeof(imu_loose_t)` เท่ากับเท่าไร — สมาชิกคือ `uint8_t` หนึ่งตัว `uint32_t` หนึ่งตัว `int16_t` สามตัว และ `uint8_t` อีกตัว รวมกันได้ 12 ไบต์

```sh
gcc -std=c11 -Wall -Wextra -o sensor_sample examples/03_sensor_sample.c
./sensor_sample
```

บนคอมพิวเตอร์ทั่วไปและบน Cortex-M จะได้ **16 ไม่ใช่ 12** เพราะคอมไพเลอร์เติมช่องว่าง (padding) ให้ `uint32_t` เริ่มที่ขอบ 4 ไบต์ พอเรียงสมาชิกใหม่จากใหญ่ไปเล็ก struct แบบเดียวกันเหลือ 12 ไบต์ — ข้อมูลเซนเซอร์เก็บเป็นพันชุด ต่างกัน 4 ไบต์ต่อชุดคือหลายกิโลไบต์

---

## แนวคิด (1) — struct หนึ่งก้อนคือข้อมูลหนึ่งชุด

ค่าที่เกิดพร้อมกันควรอยู่ด้วยกัน — ความเร่งสามแกน เวลาที่อ่าน และธงว่าใช้ได้ไหม ถ้ากระจายเป็นตัวแปรหลายตัว ฟังก์ชันจะรับพารามิเตอร์ยาวเหยียด และง่ายที่จะหยิบแกน X จากรอบนี้ไปคู่กับแกน Y จากรอบก่อน

SDK ใช้ struct แบบนี้ทั่วไป เช่น `health_t` ใน [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L77-L101)

| ฟังก์ชันจะ | ส่งแบบ | ตัวอย่าง |
|---|---|---|
| อ่านอย่างเดียว | `const T *` | `int32_t magnitude_sq(const imu_sample_t *s)` |
| เติมหรือแก้ค่าให้ผู้เรียก | `T *` (ช่องส่งผลลัพธ์) | `bool radar_dsp_snapshot(ipc_radar_range_t *out)` |
| ต้องการสำเนาของตัวเอง | by value | แก้สำเนาไม่กระทบตัวจริง แต่ต้องคัดลอกทุกไบต์ลง stack |

`const` ไม่ได้ทำให้โค้ดเร็วขึ้น แต่ทำให้คอมไพเลอร์ช่วยจับเมื่อเราเผลอแก้ของที่สัญญาว่าจะไม่แก้

---

## แนวคิด (2) — บัฟเฟอร์วงแหวน (ring buffer)

เมื่อข้อมูลไหลเข้าเป็นจังหวะ (ไบต์จาก UART, ค่าจากเซนเซอร์) และผู้ใช้ข้อมูลทำงานคนละจังหวะกับผู้ผลิต เราต้องมีที่พักข้อมูลขนาดคงที่ที่ไม่ต้อง `malloc`

```text
 data:  [ . | . | A | B | C | . | . | . ]      A B C ยังไม่ถูกอ่าน
                  ^tail       ^head            count = head - tail = 3
```

สามเทคนิคของแบบฝึกบทนี้

- **ขนาดเป็นกำลังของสอง** หาตำแหน่งด้วย `counter & MASK` แทน `%`
- **head/tail เป็นตัวนับที่เดินไปเรื่อย ๆ** จำนวนข้อมูลคือ `head - tail` เสมอ แยก "ว่าง" กับ "เต็ม" ได้โดยไม่เสียช่อง
- **เต็มแล้วปฏิเสธ** `push` คืน `false` ผู้เรียกตัดสินเองว่าจะนับว่าข้อมูลหาย หรือจะรอ

---

## แนวคิด (2) ต่อ — นโยบายตอนเต็มเป็นการตัดสินใจ

task เรดาร์ของ SDK เลือกตรงข้ามกับแบบฝึกของเรา: เมื่อเต็มมัน **"keep newest samples, drop oldest two"** เพราะสำหรับการตรวจจับคน ข้อมูลล่าสุดมีค่ากว่าข้อมูลเก่า แต่สำหรับไบต์ของโปรโตคอล การทิ้งไบต์เก่าทำให้เฟรมพังทั้งเฟรม

อีกเรื่องที่ต้องตัดสิน: ค่าคืนตอน "ว่าง" — TACP ของ SDK คืน `-1` เมื่อว่างและ 0-255 เมื่อมีข้อมูล ต้องเก็บใส่ `int` แล้วตรวจ -1 ก่อนแปลงเป็น `uint8_t` เพราะ **"a byte of 0xFF is real data and is not the empty marker"**

แบบฝึกของเราเลี่ยงปัญหานี้ด้วยการแยกค่าคืน `bool` ออกจากข้อมูลที่ส่งกลับผ่าน pointer

---

## แนวคิด (3) — เมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน

ISR แทรก task ได้ทุกเมื่อ แม้กลางบรรทัด `rb->head = rb->head + 1;` ซึ่งเป็นอ่าน-แก้-เขียน ถ้าสองฝ่ายแก้ตัวแปรเดียวกัน ค่าหายได้ และถ้า task อ่านข้อมูลหลายไบต์ที่ ISR กำลังเขียนทับ จะได้ข้อมูลครึ่งเก่าครึ่งใหม่ (torn read)

| วิธี | ใช้เมื่อ |
|---|---|
| ring แบบผู้เขียนหนึ่ง ผู้อ่านหนึ่ง เขียนข้อมูลก่อนแล้วจึงเลื่อนตัวนับ | ไบต์หรือค่าเล็กไหลต่อเนื่อง |
| `xQueueSendFromISR()` ส่งสำเนาเข้าคิว RTOS | ข้อความเป็นก้อน ต้องปลุก task ทันที |
| seqlock: เลขลำดับเป็นคี่ระหว่างเขียน ผู้อ่านตรวจว่าไม่เปลี่ยนและเป็นคู่ | snapshot ที่อ่านบ่อย |
| critical section ปิด interrupt สั้นที่สุด | ข้อมูลหลายตัวแปรที่ต้องเปลี่ยนพร้อมกัน |

ข้อห้าม: เรียก `malloc`/`printf` ใน ISR และคิดว่า `volatile` อย่างเดียวพอ (ไม่ทำให้อ่าน-แก้-เขียนเป็นหนึ่งจังหวะ)

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 03_sensor_sample.c

**ท่าที่ 1** เทียบ struct สองแบบสมาชิกเหมือนกันแต่เรียงต่างกัน พิมพ์ `sizeof`/`offsetof` ให้เห็น padding
**ท่าที่ 2** `sample_fill()` รับ `imu_sample_t *` เติมค่า ส่วน `magnitude_sq()` รับ `const imu_sample_t *`
**ท่าที่ 3** struct อยู่ใน stack ของ `main`, `try_to_reset()` รับ by value จึงแก้ได้แค่สำเนา

อ่านต่อจากของจริงใน SDK — ฝั่งผู้อ่านของ seqlock ใน `radar_dsp.c`:

```c
bool radar_dsp_snapshot(ipc_radar_range_t *out)
{
    if (out == NULL) { return false; }
    uint32_t s1, s2;
    do {
        s1 = s_snap_seq;
        memcpy(out, (const void *)&s_snap, sizeof(*out));
        s2 = s_snap_seq;
    } while ((s1 != s2) || (s1 & 1u));   /* retry on torn/odd */
    return true;
}
```

---

## ฝึกเติม

เปิด [practice/03_ring_buffer.c](practice/03_ring_buffer.c) — มีช่องให้เติม 5 จุด: `rb_count()` `rb_is_empty()` `rb_is_full()` `rb_push()` `rb_pop()`

test ครอบคลุมสามกรณี

- **กรณีปกติ** เข้าก่อนออกก่อน และอ่านจากบัฟเฟอร์ว่างต้องได้ `false`
- **กรณีขอบ** ใส่ครบ 16 ไบต์แล้วไบต์ที่ 17 ต้องถูกปฏิเสธ และไบต์แรกยังเป็นค่าเดิม
- **กรณีขอบ** ตัวนับเริ่มที่ `UINT32_MAX - 3` แล้ววิ่งผ่านศูนย์ระหว่างเขียนอ่าน 1000 รอบ

```sh
gcc -std=c11 -Wall -Wextra -o ring practice/03_ring_buffer.c && ./ring
```

ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/03_ring_buffer.c](solution/03_ring_buffer.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. `print_sample()` แค่อ่านค่าจาก `imu_sample_t` แล้วพิมพ์ ควรประกาศพารามิเตอร์แบบใด
2. `struct { uint8_t a; uint32_t b; uint8_t c; }` บน Cortex-M ด้วย GCC มักมีขนาดเท่าไร และลดได้อย่างไร
3. บัฟเฟอร์วงแหวนความจุ 16 ใช้ตัวนับ `uint32_t` แบบเดินไปเรื่อย ๆ `head = 5`, `tail = 0xFFFFFFF9` มีข้อมูลที่ยังไม่อ่านกี่ตัว
4. เรียงขั้นของ `rb_push()` ที่ไม่ทับข้อมูลเก่าและปลอดภัยเมื่อผู้อ่านเป็นอีกบริบท
5. ISR ได้รับข้อความจากอีกคอร์และต้องส่งให้ task ทำงานต่อ วิธีใดเหมาะสม (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** ดู struct ที่ส่งผ่าน pointer และ seqlock ทำงานจริงบนบอร์ด แล้วอ่านโค้ดเพื่อหาว่าใครเป็นเจ้าของข้อมูล

1. build แม่แบบของ SDK ด้วย `make build -j ENABLE_PAGE_EXAMPLES=1` แล้ว `make program` ถอดสาย USB ให้สุดแล้วเสียบใหม่
2. บนจอแตะ **SDK Examples** รัน `cm55/sensors/02_radar_presence` — ตัวอย่างนี้อ่าน `radar_dsp_snapshot()` ทุก 200 ms สังเกตบรรทัด `no target  seq ...` แล้วยื่นมือเข้าหาบอร์ดช้า ๆ
3. จดค่า `seq` สองครั้งห่างกันราว 10 วินาที ประมาณว่าเรดาร์ประกาศ snapshot ใหม่กี่ครั้งต่อวินาที
4. อ่าน [ipc_tesaiot_handler.c บรรทัด 330-363](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/ipc_tesaiot_handler.c#L330-L363) — ตอบว่าถ้าข้อความที่สองมาถึงก่อน task อ่านข้อความแรกเสร็จ จะเกิดอะไรกับ `s_pending`
5. เทียบกับ `sensor_auto_task.c` ที่ส่งสำเนา struct เข้าคิว — วิธีไหนรับข้อความติดกันได้มากกว่า และแลกกับอะไร

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอผลของตัวอย่างเรดาร์ทั้งสองสถานะ ค่า `seq` ที่จด คำตอบข้อ 4 และ 5

---

## ไปต่อ

- ขยายแบบฝึกให้บัฟเฟอร์เก็บ `imu_sample_t` ทั้งก้อนแทนไบต์ แล้วคิดว่าต้องเปลี่ยนอะไรบ้าง (คำใบ้: ขนาดของช่อง และการคัดลอกทีละก้อน)
- โจทย์ท้าทาย: เพิ่มตัวนับ `dropped` ที่ `rb_push()` เพิ่มทุกครั้งที่ปฏิเสธ แล้วถามตัวเองว่าใครเป็นเจ้าของตัวนับนี้ ผู้เขียนหรือผู้อ่าน

บทถัดไปเข้าสู่โมดูล 2: [บทเรียน 2.1 — ชุดเครื่องมือและการ build ครั้งแรก](../../m02-build-and-version/l01-toolchain-first-build/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
