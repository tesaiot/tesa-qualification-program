---
id: c-found.m06.l01
lang: th
title: {th: Unit test บนเครื่องโฮสต์, en: Unit tests on the host}
summary: {th: แยกตรรกะออกจากฮาร์ดแวร์เพื่อทดสอบบนเครื่องโฮสต์ด้วย Unity, en: Separate logic from hardware to test it on the host with Unity.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l03]
objectives:
- {th: แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้, en: Split logic such as a filter or state machine from hardware-touching code so it compiles on the host.}
- {th: เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด, en: 'Write Unity tests covering normal, edge and error cases.'}
- {th: พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน, en: Prove a test can fail by planting a bug before trusting a pass.}
develops:
- {skill: test.unit-tdd, to: 3}
- {skill: prog.state-machines, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้
2. เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด
3. พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ทั้งบทรันบนคอมพิวเตอร์ ต้องมี gcc หรือ clang, make, git และ python3

## ก่อนเริ่ม

ทวนจากโมดูลก่อนหน้าสองข้อ

1. ตลอดหลักสูตรนี้ แบบฝึกทุกไฟล์ขึ้นสีแดงก่อนคุณเติม และมี test บางข้อที่ผ่านตั้งแต่ยังไม่เติม (บทเรียน 2.2, 3.2, 4.1 และ 5.3) test แบบนั้นพิสูจน์อะไรได้บ้าง
2. ตัวถอดรหัส UART และ SPI ในโมดูล 5 รันบนคอมพิวเตอร์ได้ทั้งที่เป็นเรื่องของฮาร์ดแวร์ เพราะอะไร

## ดูของจริงก่อน

ดึง Unity รุ่น v2.7.0 มาไว้ในโฟลเดอร์ `examples` ของบทนี้ (ไฟล์ [.gitignore](examples/.gitignore) ของโฟลเดอร์กันไม่ให้มันถูก commit) แล้วรัน test สองข้อแรก

```sh
cd examples
git clone --depth 1 --branch v2.7.0 https://github.com/ThrowTheSwitch/Unity.git unity
make test
```

**ทายก่อนรัน** ว่าจะมีกี่ test และผลเป็นอย่างไร ผลคือ `2 Tests 0 Failures 0 Ignored` และ `OK` ทั้งที่ [examples/level_alarm.c](examples/level_alarm.c)
เป็น state machine ที่ตั้งใจจะใช้บนบอร์ด ไม่มีบอร์ดต่ออยู่เลย จากนั้นรันอีกคำสั่งหนึ่ง

```sh
bash prove_red.sh test_level_alarm_first.c unity/src
```

สคริปต์นี้ใส่บั๊กลงใน `level_alarm.c` ทีละจุดในโฟลเดอร์ชั่วคราว แล้วรัน test ชุดเดิม ผลคือบั๊กสามในสี่ตัว `SURVIVED`
test ที่ผ่านทั้งสองข้อตรวจโค้ดได้น้อยกว่าที่ `OK` ทำให้รู้สึกมาก บทเรียนนี้คือการทำให้ทั้งสี่ตัวถูกจับได้

## แนวคิด

### 1. ตะเข็บระหว่างตรรกะกับฮาร์ดแวร์

โค้ดเฟิร์มแวร์มีสองส่วนที่ควรแยกกัน ส่วนที่ **ตัดสินใจ** (state machine ฟิลเตอร์ การถอดรหัสโปรโตคอล การคำนวณ) กับส่วนที่ **แตะฮาร์ดแวร์** (เรียก PDL อ่านรีจิสเตอร์ รอ interrupt)
ถ้าส่วนตัดสินใจเรียก `Cy_GPIO_Read()` ตรง ๆ มันคอมไพล์บนคอมพิวเตอร์ไม่ได้ และทดสอบได้ก็ต่อเมื่อมีบอร์ด ตะเข็บ (seam) คือจุดที่เราตัดสองส่วนออกจากกัน

SDK มี host test ที่ใช้ตะเข็บแบบนี้จริง [test_arduino_shield.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/test_arduino_shield.c#L17-L50)
ทดสอบตาราง capability ของ header บน QWA309 ตัวจริง โดยใส่ "Stub physical layer" แทนฟังก์ชันที่เรียกฮาร์ดแวร์ผ่าน struct `arduino_ops_t`
และ [Makefile ของ test](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/Makefile)
อธิบายเหตุผลว่าตารางนั้น "is the piece most likely to be wrong and most expensive to debug on a bench, and it is portable C precisely so it can be checked here"
ตัวถอดรหัสจอยสติ๊ก `f310_parse()` ก็มี host test ของตัวเองที่ build ด้วย gcc คำสั่งเดียว
([test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c))

ตัวอย่างของบทนี้ใช้รูปแบบเดียวกัน [level_alarm.h](examples/level_alarm.h) อ่านค่าผ่าน `level_sensor_t` ที่มี function pointer `read_mv`
บนคอมพิวเตอร์ test ใส่ตัวปลอมที่คืนค่าจากตาราง บนบอร์ดเราใส่ตัวจริง เช่นร่างข้างล่างที่อ่านโพเทนชิโอมิเตอร์ด้วย `potentiometer_read_voltage()` จาก
[sensor_potentiometer.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_potentiometer.h#L18-L28)
ของ SDK (ร่างนี้แสดงรูปแบบ หลักสูตรยังไม่ได้ทดสอบบนบอร์ด ต้องเรียก `potentiometer_init()` ก่อน และหัวไฟล์ระบุว่าไดรเวอร์ "Only compiled when BSP_HAS_POTENTIOMETER=1")

```c
static int pot_read_mv(void *ctx, int32_t *out_mv)
{
    (void)ctx;
    float v = 0.0f;
    if (!potentiometer_read_voltage(&v)) {   /* sensor_potentiometer.h ของ SDK: bool potentiometer_read_voltage(float *voltage) */
        return -1;
    }
    *out_mv = (int32_t)(v * 1000.0f);
    return 0;
}
static const level_sensor_t k_pot = {pot_read_mv, NULL};
```

### 2. Unity และสามชนิดของกรณี

[Unity](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0) เป็น framework สำหรับ unit test ภาษา C ขนาดเล็ก สามไฟล์ใน `src/` ใช้ได้ทั้งบนคอมพิวเตอร์และบนไมโครคอนโทรลเลอร์
โครงของไฟล์ test หนึ่งไฟล์

| ส่วน | ทำอะไร |
|---|---|
| `setUp()` / `tearDown()` | เรียกก่อนและหลังทุก test ใช้ตั้งสถานะให้สะอาด หัวไฟล์ `unity.h` ระบุว่าถ้าใช้ Unity ตรง ๆ "these will need to be provided for each test executable" |
| `static void test_...(void)` | test หนึ่งข้อ ใช้ assertion เช่น `TEST_ASSERT_EQUAL_INT(expected, actual)` `TEST_ASSERT_TRUE(cond)` `TEST_ASSERT_EQUAL_HEX8(e, a)` |
| `main()` | `UNITY_BEGIN();` ตามด้วย `RUN_TEST(test_...)` ทีละข้อ แล้ว `return UNITY_END();` ซึ่งคืนจำนวน test ที่ล้ม ใช้เป็น exit code ของโปรแกรม |

test ที่ดีครอบคลุมสามชนิด

- **กรณีปกติ** สิ่งที่เกิดบ่อยที่สุด เช่นค่าต่ำกว่าเกณฑ์ ต้องไม่แจ้งเตือน
- **กรณีขอบ** ค่าที่อยู่ตรงเส้น เช่นเท่ากับเกณฑ์พอดี จำนวนครั้งที่ขาดไปหนึ่ง ช่วง hysteresis ตัวนับที่วนกลับ บั๊กส่วนใหญ่อยู่ตรงนี้
- **กรณีผิดพลาด** เซนเซอร์อ่านไม่ได้ อินพุตเป็น NULL ที่เก็บเต็ม ระบบต้องบอกความจริง (บทเรียน 3.2) และ test ต้องยืนยันว่ามันบอก

### 3. test ที่ล้มไม่เป็น คือ test ที่ไม่ได้ทดสอบอะไร

test ที่ผ่านบอกได้แค่ว่า "ไม่เจอความผิดพลาดที่ test นี้มองหา" ถ้า test มองหาไม่เป็น มันก็ผ่านเสมอ วิธีพิสูจน์คือ **จงใจใส่บั๊ก** (mutation) แล้วดูว่า test ล้มไหม
ถ้าบั๊กรอด (survived) แปลว่ามีพฤติกรรมที่ไม่มี test ไหนเฝ้าอยู่ ขั้นตอนเล็ก ๆ ที่ทำได้ทุกครั้ง

1. เขียน test ให้ล้มก่อน (red) เช่นเรียกฟังก์ชันที่ยังไม่มี หรือคาดหวังค่าที่โค้ดยังไม่คืน
2. เขียนโค้ดให้ผ่าน (green) แล้วปรับให้สะอาด (refactor) นี่คือวงจรย่อของ TDD
3. ก่อนเชื่อว่าเสร็จ ใส่บั๊กหนึ่งจุดที่ test นี้ควรจับ แล้วดูให้มันล้ม จากนั้นเอาบั๊กออก

SDK ใช้หลักเดียวกันกับเครื่องมือของตัวเอง แคตตาล็อกตัวอย่างอธิบายว่าตัวตรวจความครอบคลุมของ API วัดจาก symbol table ของ object file จริง
ไม่ใช่การค้นข้อความ เพราะ "A mention in a comment produces no symbol and therefore no coverage" ตัวตรวจจึงล้มได้จริงเมื่อ API ใหม่ไม่มีตัวอย่าง
([README ของแคตตาล็อก หัวข้อ 6](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md))

## ตัวอย่างสมบูรณ์

โฟลเดอร์ [examples/](examples/) มีห้าไฟล์ที่ทำงานร่วมกัน

- [level_alarm.h](examples/level_alarm.h) และ [level_alarm.c](examples/level_alarm.c) state machine แจ้งเตือนระดับ มีสามสถานะ NORMAL, ACTIVE, FAULT
  ต้องเห็นค่าเกินเกณฑ์ติดกัน `confirm` ครั้งจึงเปลี่ยนสถานะ และมี hysteresis ระหว่าง `on_mv` กับ `off_mv`
- [test_level_alarm_first.c](examples/test_level_alarm_first.c) test สองข้อด้วย Unity เป็นสามท่า
  **ท่าที่ 1** กรณีปกติ **ท่าที่ 2** กรณีผิดพลาด **ท่าที่ 3** `main()` ที่คืนจำนวน test ที่ล้ม
- [Makefile](examples/Makefile) build และรันด้วย `-Werror` แบบเดียวกับ host test ของ SDK เลือกไฟล์ test ได้ด้วย `TEST=`
- [prove_red.sh](examples/prove_red.sh) ใส่บั๊กสี่แบบทีละตัว แล้วรายงานว่า test จับได้ (`killed`) หรือไม่ (`SURVIVED`)

ลองแก้แล้วทายก่อนรัน: เปลี่ยน `>=` เป็น `>` ใน `level_alarm.c` ด้วยมือ แล้วรัน `make test` test สองข้อแรกผ่านหรือล้ม เพราะอะไร (แล้วแก้กลับ)

## ฝึกเติม

เปิด [practice/test_level_alarm.c](practice/test_level_alarm.c) มี test สองข้อแรกให้แล้ว และช่องให้เติม 4 ข้อ ตอนนี้แต่ละข้อเรียก `TEST_FAIL_MESSAGE` จึงขึ้นสีแดง

1. ค่าเท่ากับเกณฑ์พอดีต้องนับ
2. ค่าสูงต้องติดกัน ขาดหนึ่งครั้งเริ่มนับใหม่
3. hysteresis ต้องค้าง ACTIVE ในช่วงระหว่างสองเกณฑ์
4. อ่านล้มแล้วฟื้นต้องกลับเป็น NORMAL

```sh
cd examples
make test TEST=../practice/test_level_alarm.c
bash prove_red.sh ../practice/test_level_alarm.c unity/src
```

งานจะเสร็จเมื่อ `make test` ได้ `6 Tests 0 Failures` **และ** `prove_red.sh` ขึ้น `killed` ครบทั้งสี่บรรทัด

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/test_level_alarm.c](solution/test_level_alarm.c)
เราตรวจเฉลยแล้วว่า `6 Tests 0 Failures` และ `prove_red.sh` จับบั๊กได้ครบทั้งสี่แบบ ขณะที่ test สองข้อแรกอย่างเดียวจับได้แบบเดียว
สังเกตบรรทัดใน test ของ hysteresis ที่ตรวจว่าเป็น ACTIVE จริงก่อนเริ่มส่วนที่เหลือ ถ้าเงื่อนไขตั้งต้นไม่จริง ส่วนที่เหลือของ test จะผ่านหรือล้มโดยไม่ได้พิสูจน์อะไร

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** นำตรรกะหนึ่งชิ้นจากงานในหลักสูตรนี้ไปอยู่หลังตะเข็บ เขียน test ด้วย Unity และพิสูจน์ด้วย mutation

1. เลือกหนึ่งอย่าง: ตัวกันเด้งจากบทเรียน 4.1, ผู้ดูแล watchdog จากบทเรียน 4.3 หรือตัวถอดรหัส UART จากบทเรียน 5.1
   ย้ายฟังก์ชันตรรกะไปไว้ในไฟล์ `.c` กับ `.h` ของมันเอง โดยไม่มี `#include` ของ PDL หรือ FreeRTOS
2. เขียน test ด้วย Unity อย่างน้อยห้าข้อ ปกติหนึ่ง ขอบอย่างน้อยสอง ผิดพลาดอย่างน้อยหนึ่ง
3. เขียนบั๊กสามแบบที่คุณคิดว่าเป็นไปได้จริงสำหรับโค้ดนั้น (ใช้ `prove_red.sh` เป็นแบบ หรือแก้มือทีละตัว) แล้วบันทึกว่าแต่ละตัวถูกจับหรือรอด
   ถ้ารอด เพิ่ม test จนจับได้
4. ถ้ามีบอร์ด เขียนตัวอ่านจริงสำหรับตะเข็บนั้น (เช่นใช้ `Cy_GPIO_Read()` กับตัวกันเด้ง) แล้ว build เข้ากับแม่แบบของ SDK ตรรกะไฟล์เดียวกันต้องใช้ได้ทั้งสองที่โดยไม่แก้

**หลักฐานที่เก็บไว้ใน portfolio:** ไฟล์ตรรกะ ไฟล์ test ผลของ `make test` ตารางบั๊กที่ใส่และผล (killed หรือ survived ก่อนและหลังเพิ่ม test)
และถ้าทำข้อ 4 ให้แนบ log จากบอร์ด

## ไปต่อ

- อ่าน test ของ SDK ทั้งไฟล์ [test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c)
  แล้วจัดกลุ่ม test ของมันเป็นปกติ ขอบ และผิดพลาด กลุ่มไหนมีน้อยที่สุด
- เอกสาร [Unity test framework](https://www.throwtheswitch.org/unity) มีตัวสร้าง test runner อัตโนมัติ และ Ceedling ที่รวม mock ให้ ลองเทียบกับการเขียน `main()` เอง

บทถัดไป: [บทเรียน 6.2 CI สำหรับเฟิร์มแวร์](../l02-ci-for-firmware/README.md) ให้เครื่องรัน test เหล่านี้ให้ทุกครั้งที่มีการเปลี่ยนแปลง

## สะท้อนคิด

- test ที่คุณเคยเขียน มีกี่ข้อที่คุณเคยเห็นมันล้มจริงสักครั้ง
- ส่วนไหนของเฟิร์มแวร์ที่คุณคิดว่า "ทดสอบบนคอมพิวเตอร์ไม่ได้" ลองหาดูว่ามีตรรกะชิ้นไหนในนั้นที่แยกออกมาได้

## แหล่งอ้างอิง

- [ThrowTheSwitch Unity @ v2.7.0](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0)
- [Unity test framework](https://www.throwtheswitch.org/unity)
- [SDK: arduino_shield/test (host test ที่ใช้ stub แทนฮาร์ดแวร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/test_arduino_shield.c)
- [SDK: usb_hid_joystick/tests/test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c)
