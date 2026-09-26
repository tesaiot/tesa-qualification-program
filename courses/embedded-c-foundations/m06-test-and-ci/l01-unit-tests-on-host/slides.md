---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.1 — Unit test บนเครื่องโฮสต์"
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

# บทเรียน 6.1 — Unit test บนเครื่องโฮสต์

## แยกตรรกะออกจากฮาร์ดแวร์เพื่อทดสอบบนเครื่องโฮสต์ด้วย Unity

**โมดูล 6 — Unit test และ CI**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้
2. เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด
3. พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน

ใช้เวลาประมาณ 70 นาที — ทั้งบทรันบนคอมพิวเตอร์ ต้องมี gcc หรือ clang, make, git และ python3

---

## ก่อนเริ่ม

ทวนจากโมดูลก่อนหน้าสองข้อ

1. ตลอดหลักสูตรนี้ แบบฝึกทุกไฟล์ขึ้นสีแดงก่อนเติม และมี test บางข้อที่ผ่านตั้งแต่ยังไม่เติม test แบบนั้นพิสูจน์อะไรได้บ้าง
2. ตัวถอดรหัส UART และ SPI ในโมดูล 5 รันบนคอมพิวเตอร์ได้ทั้งที่เป็นเรื่องของฮาร์ดแวร์ เพราะอะไร

---

## ดูของจริงก่อน

ดึง Unity v2.7.0 มาไว้ในโฟลเดอร์ `examples` แล้วรัน test สองข้อแรก

```sh
cd examples
git clone --depth 1 --branch v2.7.0 https://github.com/ThrowTheSwitch/Unity.git unity
make test
```

**ทายก่อนรัน**: จะมีกี่ test และผลเป็นอย่างไร — ผลคือ `2 Tests 0 Failures 0 Ignored` และ `OK` ทั้งที่ `level_alarm.c` เป็น state machine ที่ตั้งใจใช้บนบอร์ด ไม่มีบอร์ดต่ออยู่เลย จากนั้นรัน

```sh
bash prove_red.sh test_level_alarm_first.c unity/src
```

สคริปต์นี้ใส่บั๊กลง `level_alarm.c` ทีละจุด แล้วรัน test ชุดเดิม ผลคือบั๊กสามในสี่ตัว **`SURVIVED`** — test ที่ผ่านทั้งสองข้อตรวจโค้ดได้น้อยกว่าที่ `OK` ทำให้รู้สึกมาก บทเรียนนี้คือการทำให้ทั้งสี่ตัวถูกจับได้

---

## แนวคิด (1) — ตะเข็บระหว่างตรรกะกับฮาร์ดแวร์

โค้ดเฟิร์มแวร์มีสองส่วนที่ควรแยกกัน: ส่วนที่ **ตัดสินใจ** (state machine ฟิลเตอร์ การคำนวณ) กับส่วนที่ **แตะฮาร์ดแวร์** (เรียก PDL อ่านรีจิสเตอร์) ถ้าส่วนตัดสินใจเรียก `Cy_GPIO_Read()` ตรง ๆ มันคอมไพล์บนคอมพิวเตอร์ไม่ได้ **ตะเข็บ (seam)** คือจุดที่เราตัดสองส่วนออกจากกัน

SDK มี host test ที่ใช้ตะเข็บแบบนี้จริง — `test_arduino_shield.c` ใส่ "Stub physical layer" แทนฟังก์ชันที่เรียกฮาร์ดแวร์ผ่าน struct `arduino_ops_t` เพราะตารางนั้น **"is the piece most likely to be wrong and most expensive to debug on a bench, and it is portable C precisely so it can be checked here"**

```c
static int pot_read_mv(void *ctx, int32_t *out_mv) {
    float v = 0.0f;
    if (!potentiometer_read_voltage(&v)) { return -1; }  /* ตัวจริงบนบอร์ด */
    *out_mv = (int32_t)(v * 1000.0f);
    return 0;
}
static const level_sensor_t k_pot = {pot_read_mv, NULL};  /* บนคอมพิวเตอร์: ตัวปลอมคืนค่าจากตาราง */
```

---

## แนวคิด (2) — Unity และสามชนิดของกรณี

[Unity](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0) เป็น framework สำหรับ unit test ภาษา C ขนาดเล็ก ใช้ได้ทั้งบนคอมพิวเตอร์และไมโครคอนโทรลเลอร์

| ส่วน | ทำอะไร |
|---|---|
| `setUp()` / `tearDown()` | เรียกก่อน/หลังทุก test ตั้งสถานะให้สะอาด |
| `static void test_...(void)` | test หนึ่งข้อ ใช้ `TEST_ASSERT_EQUAL_INT()` `TEST_ASSERT_TRUE()` ฯลฯ |
| `main()` | `UNITY_BEGIN();` ตาม `RUN_TEST()` ทีละข้อ แล้ว `return UNITY_END();` |

test ที่ดีครอบคลุมสามชนิด

- **กรณีปกติ** สิ่งที่เกิดบ่อยที่สุด
- **กรณีขอบ** ค่าที่อยู่ตรงเส้น เช่นเท่ากับเกณฑ์พอดี ช่วง hysteresis ตัวนับที่วนกลับ — บั๊กส่วนใหญ่อยู่ตรงนี้
- **กรณีผิดพลาด** เซนเซอร์อ่านไม่ได้ อินพุตเป็น NULL ระบบต้องบอกความจริง และ test ต้องยืนยันว่ามันบอก

---

## แนวคิด (3) — test ที่ล้มไม่เป็น คือ test ที่ไม่ได้ทดสอบอะไร

test ที่ผ่านบอกได้แค่ว่า "ไม่เจอความผิดพลาดที่ test นี้มองหา" ถ้า test มองหาไม่เป็น มันก็ผ่านเสมอ วิธีพิสูจน์คือ **จงใจใส่บั๊ก** (mutation) แล้วดูว่า test ล้มไหม ถ้าบั๊กรอด (survived) แปลว่ามีพฤติกรรมที่ไม่มี test ไหนเฝ้าอยู่

1. เขียน test ให้ล้มก่อน (red)
2. เขียนโค้ดให้ผ่าน (green) แล้วปรับให้สะอาด (refactor)
3. ก่อนเชื่อว่าเสร็จ ใส่บั๊กหนึ่งจุดที่ test นี้ควรจับ แล้วดูให้มันล้ม จากนั้นเอาบั๊กออก

> SDK ใช้หลักเดียวกันกับเครื่องมือของตัวเอง: ตัวตรวจความครอบคลุม API วัดจาก symbol table ของ object file จริง ไม่ใช่การค้นข้อความ เพราะ **"A mention in a comment produces no symbol and therefore no coverage"**

---

## ตัวอย่างสมบูรณ์ — ห้าไฟล์ทำงานร่วมกัน

[level_alarm.h/.c](examples/level_alarm.c) — state machine แจ้งเตือนระดับ สามสถานะ NORMAL, ACTIVE, FAULT ต้องเห็นค่าเกินเกณฑ์ติดกัน `confirm` ครั้งจึงเปลี่ยนสถานะ มี hysteresis ระหว่าง `on_mv` กับ `off_mv`

```c
typedef struct {
    int (*read_mv)(void *ctx, int32_t *out_mv);   /* ตะเข็บ: ปลอมได้บนโฮสต์ */
    void *ctx;
} level_sensor_t;

// ท่าที่ 1: กรณีปกติ
void test_stays_normal_below_threshold(void) {
    TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, level_alarm_state(&alarm));
}
```

[test_level_alarm_first.c](examples/test_level_alarm_first.c) — ท่าที่ 1 กรณีปกติ ท่าที่ 2 กรณีผิดพลาด ท่าที่ 3 `main()` ที่คืนจำนวน test ที่ล้ม

ลองแก้แล้วทายก่อนรัน: เปลี่ยน `>=` เป็น `>` ใน `level_alarm.c` แล้วรัน `make test` — test สองข้อแรกผ่านหรือล้ม เพราะอะไร (แล้วแก้กลับ)

---

## ฝึกเติม

เปิด [practice/test_level_alarm.c](practice/test_level_alarm.c) — มี test สองข้อแรกให้แล้ว และช่องให้เติม 4 ข้อ (ตอนนี้เรียก `TEST_FAIL_MESSAGE` จึงขึ้นสีแดง)

1. ค่าเท่ากับเกณฑ์พอดีต้องนับ
2. ค่าสูงต้องติดกัน ขาดหนึ่งครั้งเริ่มนับใหม่
3. hysteresis ต้องค้าง ACTIVE ในช่วงระหว่างสองเกณฑ์
4. อ่านล้มแล้วฟื้นต้องกลับเป็น NORMAL

```sh
cd examples
make test TEST=../practice/test_level_alarm.c
bash prove_red.sh ../practice/test_level_alarm.c unity/src
```

งานจะเสร็จเมื่อ `make test` ได้ `6 Tests 0 Failures` **และ** `prove_red.sh` ขึ้น `killed` ครบทั้งสี่บรรทัด ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/test_level_alarm.c](solution/test_level_alarm.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ฟังก์ชันหนึ่งอ่านปุ่มด้วย `Cy_GPIO_Read()` แล้วตัดสินใจกันเด้งในฟังก์ชันเดียวกัน วิธีใดทำให้ทดสอบตรรกะกันเด้งบนคอมพิวเตอร์ได้โดยไม่แก้ตรรกะ
2. ไฟล์ `.c` ใดบ้างที่ควรคอมไพล์ได้ทั้งบนคอมพิวเตอร์และบนบอร์ดโดยไม่แก้ (เลือกได้หลายข้อ)
3. state machine ของบทนี้เปลี่ยนเป็น ACTIVE เมื่อค่ามากกว่าหรือเท่ากับ `on_mv` ติดกัน `confirm` ครั้ง test ข้อใดเป็นกรณีขอบ
4. `prove_red.sh` รายงาน SURVIVED สำหรับบั๊ก 'no reset on a gap' หมายความว่าอะไร
5. ข้อใดเป็นหลักฐานที่ดีว่า test ชุดหนึ่งทดสอบอะไรจริง (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** นำตรรกะหนึ่งชิ้นจากงานในหลักสูตรนี้ไปอยู่หลังตะเข็บ เขียน test ด้วย Unity และพิสูจน์ด้วย mutation

1. เลือกหนึ่งอย่าง: ตัวกันเด้ง (4.1), ผู้ดูแล watchdog (4.3) หรือตัวถอดรหัส UART (5.1) — ย้ายฟังก์ชันตรรกะไปไว้ในไฟล์ `.c`/`.h` ของตัวเอง โดยไม่มี `#include` ของ PDL หรือ FreeRTOS
2. เขียน test ด้วย Unity อย่างน้อยห้าข้อ ปกติหนึ่ง ขอบอย่างน้อยสอง ผิดพลาดอย่างน้อยหนึ่ง
3. เขียนบั๊กสามแบบที่คิดว่าเป็นไปได้จริง แล้วบันทึกว่าแต่ละตัวถูกจับหรือรอด ถ้ารอด เพิ่ม test จนจับได้
4. ถ้ามีบอร์ด เขียนตัวอ่านจริงสำหรับตะเข็บนั้น แล้ว build เข้ากับแม่แบบของ SDK ตรรกะไฟล์เดียวกันต้องใช้ได้ทั้งสองที่โดยไม่แก้

**หลักฐานที่เก็บไว้ใน portfolio:** ไฟล์ตรรกะ ไฟล์ test ผลของ `make test` ตารางบั๊กที่ใส่และผล และถ้าทำข้อ 4 ให้แนบ log จากบอร์ด

---

## ไปต่อ

- อ่าน test ทั้งไฟล์ [test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c) แล้วจัดกลุ่ม test เป็นปกติ ขอบ และผิดพลาด กลุ่มไหนมีน้อยที่สุด
- เอกสาร [Unity test framework](https://www.throwtheswitch.org/unity) มีตัวสร้าง test runner อัตโนมัติ และ Ceedling ที่รวม mock ให้

บทถัดไป: [บทเรียน 6.2 — CI สำหรับเฟิร์มแวร์](../l02-ci-for-firmware/README.md) ให้เครื่องรัน test เหล่านี้ให้ทุกครั้งที่มีการเปลี่ยนแปลง

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 (Unity v2.7.0 เป็น MIT ผู้เรียน clone เอง ไม่ได้รวมไว้ในหลักสูตร)
โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์ บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
