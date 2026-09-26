---
id: c-found.m01.l03
lang: th
title: {th: 'struct, pointer และบัฟเฟอร์วงแหวน', en: 'Structs, pointers and ring buffers'}
summary: {th: จัดข้อมูลด้วย struct ส่งต่อด้วย pointer และรับข้อมูลต่อเนื่องด้วยบัฟเฟอร์วงแหวน, en: 'Organise data with structs, pass it by pointer, and stream it through a ring buffer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l02]
objectives:
- {th: ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้, en: Design a struct for one sensor sample and pass it by const pointer when it is read-only.}
- {th: เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน, en: Write a fixed-size ring buffer that never overwrites unread data.}
- {th: อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน, en: 'Explain the risk when an ISR and a task share a buffer, and how to guard it.'}
develops:
- {skill: lang.c, to: 3}
- {skill: prog.algo-ds, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้
2. เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน
3. อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากบทเรียน 1.2 สองข้อ

1. บัฟเฟอร์ 512 ไบต์ที่ประกาศเป็นตัวแปร local ใน task ที่มี stack 256 word จะเกิดอะไรขึ้น แล้วควรประกาศแบบไหนแทน
2. ทำไม `head - tail` ของตัวนับ `uint32_t` จึงยังถูกต้องแม้ `head` จะวนกลับผ่านศูนย์ไปแล้ว (คำใบ้อยู่ในบทเรียน 1.1)

## ดูของจริงก่อน

เปิด [examples/03_sensor_sample.c](examples/03_sensor_sample.c) **ทายก่อนรัน** ว่า `sizeof(imu_loose_t)` เท่ากับเท่าไร
สมาชิกของมันคือ `uint8_t` หนึ่งตัว `uint32_t` หนึ่งตัว `int16_t` สามตัว และ `uint8_t` อีกหนึ่งตัว รวมกันได้ 12 ไบต์ แล้วรัน

```sh
gcc -std=c11 -Wall -Wextra -o sensor_sample examples/03_sensor_sample.c
./sensor_sample
```

บนคอมพิวเตอร์ทั่วไปและบน Cortex-M จะได้ 16 ไม่ใช่ 12 เพราะคอมไพเลอร์เติมช่องว่าง (padding) ให้ `uint32_t` เริ่มที่ขอบ 4 ไบต์
พอเรียงสมาชิกใหม่จากใหญ่ไปเล็ก struct แบบเดียวกันเหลือ 12 ไบต์ ข้อมูลเซนเซอร์ที่เก็บเป็นพันชุดในบัฟเฟอร์ ต่างกัน 4 ไบต์ต่อชุดคือหลายกิโลไบต์

## แนวคิด

### 1. struct หนึ่งก้อนคือข้อมูลหนึ่งชุด และ const pointer คือสัญญา

ค่าที่เกิดพร้อมกันควรอยู่ด้วยกัน ความเร่งสามแกนที่อ่านจากการแปลงครั้งเดียวกัน เวลาที่อ่าน และธงว่าข้อมูลใช้ได้ไหม
ถ้ากระจายเป็นตัวแปรหลายตัว ฟังก์ชันจะรับพารามิเตอร์ยาวเหยียด และง่ายที่จะหยิบแกน X จากรอบนี้ไปคู่กับแกน Y จากรอบก่อน
SDK ใช้ struct แบบนี้ทั่วไป เช่น `health_t` ใน [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L77-L101)
เก็บตัวนับหกตัวที่อ่านในจังหวะเดียวกัน แล้วให้ `sample(health_t *h)` เติมผ่าน pointer

กติกาการส่ง struct ให้ฟังก์ชัน

| ฟังก์ชันจะ | ส่งแบบ | ตัวอย่าง |
|---|---|---|
| อ่านอย่างเดียว | `const T *` | `int32_t magnitude_sq(const imu_sample_t *s)` |
| เติมหรือแก้ค่าให้ผู้เรียก | `T *` (เป็น "ช่องส่งผลลัพธ์") | `bool radar_dsp_snapshot(ipc_radar_range_t *out)` ของ SDK |
| ต้องการสำเนาของตัวเอง และ struct เล็ก | by value | ได้สำเนา แก้สำเนาไม่กระทบตัวจริง แต่ต้องคัดลอกทุกไบต์ลง stack |

`const` ไม่ได้ทำให้โค้ดเร็วขึ้น แต่ทำให้คอมไพเลอร์ช่วยจับเมื่อเราเผลอแก้ของที่สัญญาว่าจะไม่แก้ และบอกผู้อ่านโค้ดทันทีว่าฟังก์ชันนี้ปลอดภัย
ตัวอย่าง [04_gpio_led_button.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L95-L113)
ของ SDK ใช้ตาราง `static const led_def_t s_leds[]` และหยิบแถวหนึ่งมาใช้ด้วย `const led_def_t *mirror` (บรรทัด 203) คือ pointer ไปยังข้อมูลที่ห้ามแก้

### 2. บัฟเฟอร์วงแหวน (ring buffer)

เมื่อข้อมูลไหลเข้ามาเป็นจังหวะ เช่นไบต์จาก UART หรือค่าจากเซนเซอร์ และผู้ใช้ข้อมูลทำงานคนละจังหวะกับผู้ผลิต
เราต้องมีที่พักข้อมูลขนาดคงที่ที่ไม่ต้อง `malloc` บัฟเฟอร์วงแหวนคืออาร์เรย์ที่ใช้ซ้ำเป็นวง ผู้เขียนเลื่อน `head` ผู้อ่านเลื่อน `tail`

```
 data:  [ . | . | A | B | C | . | . | . ]      A B C ยังไม่ถูกอ่าน
                  ^tail       ^head            count = head - tail = 3
```

การออกแบบในแบบฝึกของบทนี้ใช้สามเทคนิค

- **ขนาดเป็นกำลังของสอง** หาตำแหน่งด้วย `counter & MASK` แทน `%` ซึ่งช้ากว่าบน CPU บางรุ่น (บัฟเฟอร์ของเรดาร์ใน SDK ขนาด `0x4000` ก็ใช้วิธีนี้)
- **head และ tail เป็นตัวนับที่เดินไปเรื่อย ๆ** จำนวนข้อมูลคือ `head - tail` เสมอ แยกกรณี "ว่าง" (เท่ากัน) กับ "เต็ม" (ต่างกันเท่าความจุ) ได้โดยไม่ต้องเสียช่องไปหนึ่งช่อง
- **เต็มแล้วปฏิเสธ** `push` คืน `false` ผู้เรียกตัดสินเองว่าจะนับว่าข้อมูลหาย หรือจะรอ

นโยบายตอนเต็มเป็นการตัดสินใจ ไม่ใช่รายละเอียด task เรดาร์ของ SDK เลือกตรงข้ามกับเรา: เมื่อเต็มมัน "keep newest samples, drop oldest two"
([radar_task.c บรรทัด 466-480](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L466-L480))
เพราะสำหรับการตรวจจับคน ข้อมูลล่าสุดมีค่ากว่าข้อมูลเก่า แต่สำหรับไบต์ของโปรโตคอล การทิ้งไบต์เก่าทำให้เฟรมพังทั้งเฟรม
อีกเรื่องที่ต้องตัดสินคือค่าคืนตอน "ว่าง" TACP ของ SDK (variant mtb-mpy) คืน `-1` เมื่อว่างและ 0 ถึง 255 เมื่อมีข้อมูล
และเตือนว่าต้องเก็บใส่ `int` แล้วตรวจ -1 ก่อนแปลงเป็น `uint8_t` เพราะ "a byte of 0xFF is real data and is not the empty marker"
([08_tacp_host_protocol.c บรรทัด 46-48](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c#L46-L48))
แบบฝึกของเราเลี่ยงปัญหานี้ด้วยการแยกค่าคืน `bool` ออกจากข้อมูลที่ส่งกลับผ่าน pointer

### 3. เมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน

ISR แทรก task ได้ทุกเมื่อ แม้กลางบรรทัด `rb->head = rb->head + 1;` ซึ่งเป็นอ่าน แก้ เขียน ถ้าสองฝ่ายแก้ตัวแปรเดียวกัน ค่าหายได้
ถ้าผู้เขียนเลื่อน `head` ก่อนเขียนข้อมูลลงช่อง ผู้อ่านอาจหยิบช่องที่ยังว่างไปใช้ และถ้า task อ่านข้อมูลหลายไบต์ที่ ISR กำลังเขียนทับ
จะได้ข้อมูลครึ่งเก่าครึ่งใหม่ (torn read) วิธีป้องกันที่ SDK ใช้จริงมีสี่แบบ

| วิธี | ใช้เมื่อ | ที่ใช้ใน SDK |
|---|---|---|
| ring buffer แบบผู้เขียนหนึ่ง ผู้อ่านหนึ่ง: แต่ละฝ่ายแก้ตัวนับของตัวเองเท่านั้น เขียนข้อมูลก่อนแล้วจึงเลื่อนตัวนับ มี barrier คั่น | ไบต์หรือค่าเล็ก ๆ ไหลต่อเนื่อง | ring แบบ lock-free ของ TACP (variant mtb-mpy) ที่ `tacp_request_delete_main_from_isr()` ใส่ไบต์ลงได้จากบริบท ISR |
| ให้ ISR ส่งสำเนาเข้าคิวของ RTOS ด้วย `xQueueSendFromISR()` แล้วให้ task รับไปทำ | ข้อความเป็นก้อน ต้องการให้ task ตื่นทันที | [sensor_auto_task.c บรรทัด 274-299](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299) |
| seqlock: ผู้เขียนทำเลขลำดับเป็นเลขคี่ระหว่างเขียน ผู้อ่านคัดลอกแล้วตรวจว่าเลขลำดับไม่เปลี่ยนและเป็นเลขคู่ ถ้าไม่ใช่ก็อ่านใหม่ | snapshot ที่อ่านบ่อยและทนอ่านซ้ำได้ | [radar_dsp.c บรรทัด 284-320](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c#L284-L320) |
| critical section: ปิด interrupt สั้นที่สุดระหว่างอ่านหรือเขียน | ข้อมูลหลายตัวแปรที่ต้องเปลี่ยนพร้อมกัน | `taskENTER_CRITICAL()` ของ FreeRTOS |

ข้อที่ห้ามทำคือเรียก `malloc` หรือ `printf` ใน ISR (บทเรียน 1.2 และโมดูล 4) และคิดว่า `volatile` อย่างเดียวพอ
`volatile` บังคับให้อ่านเขียนจริง แต่ไม่ได้ทำให้การอ่าน แก้ เขียน กลายเป็นหนึ่งจังหวะ

## ตัวอย่างสมบูรณ์

[examples/03_sensor_sample.c](examples/03_sensor_sample.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** เทียบ struct สองแบบที่มีสมาชิกเหมือนกันแต่เรียงต่างกัน พิมพ์ `sizeof` และ `offsetof` ให้เห็นว่า padding อยู่ตรงไหน
- **ท่าที่ 2** `sample_fill()` รับ `imu_sample_t *` เพื่อเติมค่า ส่วน `magnitude_sq()` รับ `const imu_sample_t *` เพราะอ่านอย่างเดียว
- **ท่าที่ 3** struct อยู่ใน stack ของ `main` และส่งที่อยู่ต่อ ส่วน `try_to_reset()` รับแบบ by value จึงแก้ได้แค่สำเนา

ลองแก้ทีละอย่าง ทายก่อนรันทุกครั้ง

1. เปิดบรรทัด `s->ax = 0;` ใน `magnitude_sq()` คอมไพเลอร์บอกอะไร
2. สลับ `valid` กับ `seq` ไปไว้หน้าสุดของ `imu_sample_t` ขนาดเปลี่ยนไหม เพราะอะไร
3. เปลี่ยน `try_to_reset()` ให้รับ `imu_sample_t *` แล้วแก้ผ่าน pointer ผลบรรทัดสุดท้ายเปลี่ยนเป็นอะไร

อ่านต่อจากของจริงใน SDK: ฝั่งผู้อ่านของ seqlock ใน `radar_dsp.c` คัดลอก struct ทั้งก้อนผ่าน pointer `out` แล้ววนอ่านใหม่จนกว่าจะได้ชุดที่ไม่ขาดกลาง

```c
bool radar_dsp_snapshot(ipc_radar_range_t *out)
{
    if (out == NULL) {
        return false;
    }
    if (!s_ready) {
        memset(out, 0, sizeof(*out));
        out->initialized = s_inited ? 1 : 0;
        return false;
    }
    uint32_t s1, s2;
    do {
        s1 = s_snap_seq;
        memcpy(out, (const void *)&s_snap, sizeof(*out));
        s2 = s_snap_seq;
    } while ((s1 != s2) || (s1 & 1u));       /* retry on torn/odd            */
    return true;
}
```

ที่มา: [radar_dsp.c บรรทัด 303-320](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c#L303-L320)
(Apache-2.0, tesaiot-pse84-devkit-sdk) ฝั่งผู้เขียน (บรรทัด 284-297) เพิ่มเลขลำดับเป็นเลขคี่ เรียก `__DMB()` เขียนทุกช่อง เรียก `__DMB()` อีกครั้ง
แล้วจึงเพิ่มเลขลำดับเป็นเลขคู่ ให้สังเกตว่าฟังก์ชันคืน `false` เมื่อยังไม่มีเฟรมแรก ซึ่งต่างจาก "ไม่มีเป้าหมาย" ผลลัพธ์ที่บอกความจริงเป็นหัวข้อของบทเรียน 3.2

## ฝึกเติม

เปิด [practice/03_ring_buffer.c](practice/03_ring_buffer.c) มีช่องให้เติม 5 จุด มากกว่าสองบทก่อน เพราะคุณมีเครื่องมือครบแล้ว
`rb_count()` `rb_is_empty()` `rb_is_full()` `rb_push()` และ `rb_pop()` test ครอบคลุมสามกรณี

- **กรณีปกติ** เข้าก่อนออกก่อน และอ่านจากบัฟเฟอร์ว่างต้องได้ `false`
- **กรณีขอบ** ใส่ครบ 16 ไบต์แล้วไบต์ที่ 17 ต้องถูกปฏิเสธ และไบต์แรกต้องยังเป็นค่าเดิม
- **กรณีขอบ** ตัวนับเริ่มที่ `UINT32_MAX - 3` แล้ววิ่งผ่านศูนย์ระหว่างเขียนอ่าน 1000 รอบ

```sh
gcc -std=c11 -Wall -Wextra -o ring practice/03_ring_buffer.c && ./ring
```

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/03_ring_buffer.c](solution/03_ring_buffer.c)
สิ่งที่เฉลยเพิ่มจากโค้ดที่ test ต้องการคือ `atomic_thread_fence()` ของ C11 คั่นระหว่าง "เขียนข้อมูล" กับ "เลื่อน head"
และระหว่าง "อ่านข้อมูล" กับ "เลื่อน tail" บนคอมพิวเตอร์ test ผ่านได้แม้ไม่มีบรรทัดนี้ แต่เมื่อผู้เขียนเป็น ISR หรือเป็นอีกคอร์
มันคือสิ่งที่กันไม่ให้คอมไพเลอร์หรือ CPU สลับลำดับ บน Cortex-M ใน SDK ใช้ `__DMB()` ของ CMSIS ทำหน้าที่นี้
นี่คือตัวอย่างของสิ่งที่ test บนเครื่องโฮสต์พิสูจน์ไม่ได้ ซึ่งเราจะกลับมาคุยในบทเรียน 6.2

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** ดู struct ที่ส่งผ่าน pointer และ seqlock ทำงานจริงบนบอร์ด แล้วอ่านโค้ดเพื่อหาว่าใครเป็นเจ้าของข้อมูล

1. build แม่แบบของ SDK ด้วย `make build -j ENABLE_PAGE_EXAMPLES=1` แล้ว `make program` ถอดสาย USB ให้สุดแล้วเสียบใหม่
   (ขั้นตอนเต็มอยู่ใน [บทเรียน 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md))
2. บนจอ แตะ **SDK Examples** แล้วรัน `cm55/sensors/02_radar_presence` ตัวอย่างนี้อ่าน `radar_dsp_snapshot()` ทุก 200 ms
   สังเกตบรรทัดบนสุด เมื่อไม่มีเป้าหมายจะแสดง `no target  seq ...  bin width ... mm` และเลข `seq` จะเพิ่มขึ้นเรื่อย ๆ
   ยื่นมือเข้าหาบอร์ดช้า ๆ แล้วดูบรรทัดเปลี่ยนเป็น `target ... mm  bin ...`
3. จดค่า `seq` สองครั้งห่างกันประมาณสิบวินาที แล้วประมาณว่าเรดาร์ประกาศ snapshot ใหม่กี่ครั้งต่อวินาที
4. อ่าน [ipc_tesaiot_handler.c บรรทัด 330-363](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/ipc_tesaiot_handler.c#L330-L363)
   ฟังก์ชันนี้ทำงานในบริบท ISR คัดลอกข้อความลงตัวแปร `s_pending` ช่องเดียว แล้วปลุก task ด้วย semaphore
   ตอบในบันทึกว่า ถ้าข้อความที่สองมาถึงก่อน task จะอ่านข้อความแรกเสร็จ จะเกิดอะไรกับ `s_pending`
   แล้วค้นในไฟล์เดียวกันหรือไฟล์ของฝั่ง CM55 ว่ามีอะไรรับประกันว่าเหตุการณ์นั้นเกิดไม่ได้หรือไม่ (ถ้าหาไม่เจอ ให้เขียนว่าหาไม่เจอ ไม่ต้องเดา)
5. เทียบกับ [sensor_auto_task.c บรรทัด 274-299](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299)
   ซึ่งส่งสำเนา struct เข้าคิว วิธีไหนรับข้อความที่มาติดกันได้มากกว่า และแลกกับอะไร

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอผลของตัวอย่างเรดาร์ทั้งสองสถานะ ค่า `seq` ที่จดและการคำนวณ คำตอบข้อ 4 และ 5

## ไปต่อ

- ขยายแบบฝึกให้บัฟเฟอร์เก็บ `imu_sample_t` ทั้งก้อนแทนไบต์ แล้วคิดว่าต้องเปลี่ยนอะไรบ้าง (คำใบ้: ขนาดของช่อง และการคัดลอกทีละก้อน)
- โจทย์ท้าทาย: เพิ่มตัวนับ `dropped` ที่ `rb_push()` เพิ่มทุกครั้งที่ปฏิเสธ แล้วถามตัวเองว่าใครเป็นเจ้าของตัวนับนี้ ผู้เขียนหรือผู้อ่าน

บทถัดไปเข้าสู่โมดูล 2: [บทเรียน 2.1 ชุดเครื่องมือและการ build ครั้งแรก](../../m02-build-and-version/l01-toolchain-first-build/README.md)

## สะท้อนคิด

- ในงานที่คุณเคยทำ มีข้อมูลตัวไหนที่ควรทิ้งของเก่าเมื่อเต็ม และตัวไหนที่ห้ามทิ้งเลย
- ถ้า test ผ่านบนคอมพิวเตอร์ทุกครั้ง แต่บนบอร์ดข้อมูลเพี้ยนนาน ๆ ครั้ง คุณจะสงสัยอะไรก่อน

## แหล่งอ้างอิง

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (ring buffer และฟังก์ชัน _from_isr)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [SDK: tesaiot-radar/radar_dsp.c (seqlock ของ snapshot)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c)
- [SDK: cm55/sensors/02_radar_presence.c (อ่าน snapshot จากฝั่งจอ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c)
- [B3 — The IPC backbone: setup, deferred binding, snapshots (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b3__ipc__backbone.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
