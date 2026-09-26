---
id: c-found.m01.l01
lang: th
title: {th: ภาษา C บนไมโครคอนโทรลเลอร์, en: C on a microcontroller}
summary: {th: ใช้ชนิดข้อมูลขนาดแน่นอน ตัวดำเนินการระดับบิต และ volatile กับรีจิสเตอร์ของอุปกรณ์, en: 'Use fixed-width types, bit operators and volatile with device registers.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: []
objectives:
- {th: เลือกชนิดข้อมูลขนาดแน่นอนจาก stdint.h ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้, en: Choose fixed-width stdint.h types for given values and explain overflow.}
- {th: เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง, en: 'Write correct read-modify-write set, clear and toggle operations with bit operators.'}
- {th: อธิบายว่าเมื่อใดต้องใช้ volatile กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt, en: Explain when volatile is required for variables shared with hardware or interrupts.}
develops:
- {skill: lang.c, to: 3}
- {skill: hw.architecture, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เลือกชนิดข้อมูลขนาดแน่นอนจาก stdint.h ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้
2. เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง
3. อธิบายว่าเมื่อใดต้องใช้ volatile กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ครึ่งแรกทำบนคอมพิวเตอร์ของคุณได้เลย
ส่วนแล็บใช้บอร์ด TESAIoT Dev Kit (PSOC™ Edge E84)

## ก่อนเริ่ม

หลักสูตรนี้ต่อจากคนที่เขียน Python หรือ MicroPython ได้แล้ว ลองตอบในใจสองข้อ

1. ใน MicroPython `x = 250 + 10` ได้ 260 เสมอ คุณคิดว่าในภาษา C บนไมโครคอนโทรลเลอร์จะได้ 260 เสมอไหม ขึ้นกับอะไร
2. เวลาสั่ง `gpio.led(0).on()` แล้วไฟติด ในชิปต้องมีอะไรสักอย่างเปลี่ยนค่า คุณคิดว่าคืออะไร และอยู่ที่ไหน

สิ่งที่ต้องมี: คอมไพเลอร์ภาษา C บนคอมพิวเตอร์ (gcc หรือ clang) สำหรับครึ่งแรก และสำหรับแล็บคือบอร์ด TESAIoT Dev Kit
ModusToolbox™ 3.6 กับซอร์สของ [TESAIoT PSE84 Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) ที่ commit `ef72c1b`

## ดูของจริงก่อน

เปิด [examples/01_types_and_bits.c](examples/01_types_and_bits.c) แล้ว **ทายก่อนรัน** ว่าบรรทัด `count after +10` จะพิมพ์เลขอะไร
จดคำทายไว้ แล้วคอมไพล์และรัน

```sh
gcc -std=c11 -Wall -Wextra -o types_and_bits examples/01_types_and_bits.c
./types_and_bits
```

ถ้าคุณทายว่า 260 คุณไม่ได้ผิดคนเดียว โปรแกรมพิมพ์ `count after +10 = 4` เพราะ `uint8_t` เก็บได้แค่ 0 ถึง 255
ค่าที่เกินจึงวนกลับ บรรทัดถัดมายังมีเซอร์ไพรส์อีกสองอย่าง คือไบต์ `0x30` กับ `0xF8` กลายเป็น -2000
และผลคูณ 32 บิตไม่เท่ากับผลคูณ 64 บิต บทเรียนนี้คือคำอธิบายของทั้งสามบรรทัดนั้น

## แนวคิด

### 1. ชนิดข้อมูลขนาดแน่นอนและ overflow

ภาษา C ไม่ได้สัญญาว่า `int` กว้างกี่บิต มันขึ้นกับคอมไพเลอร์และสถาปัตยกรรม แต่รีจิสเตอร์ ไบต์บนบัส และแพ็กเก็ตของโปรโตคอล
ถูกนิยามเป็นจำนวนบิตที่แน่นอน งานเฟิร์มแวร์จึงใช้ชนิดจาก `<stdint.h>` เช่น `uint8_t` `int16_t` `uint32_t`
ซึ่งกว้างเท่ากันทุกเครื่อง

| ค่าที่จะเก็บ | ชนิดที่เหมาะ | เหตุผล |
|---|---|---|
| ไบต์บนบัส I2C หรือ UART | `uint8_t` | ตรงกับขนาดข้อมูลบนสาย |
| ค่าดิบของเซนเซอร์ที่ติดลบได้ เช่นความเร่ง | `int16_t` | two's complement 16 บิตตามที่ชิปส่งมา |
| ตัวนับรอบ เวลาเป็นมิลลิวินาที ที่อยู่ | `uint32_t` | กว้างพอ และตรงกับความกว้างของ CPU 32 บิต |
| ผลคูณกลางทางที่อาจเกิน 32 บิต | `uint64_t` | ขยายก่อนคูณ ไม่ใช่หลังคูณ |

**overflow** ของชนิด unsigned นิยามไว้ชัดว่าวนกลับแบบ modulo 2<sup>N</sup> เช่น `uint8_t` 250 + 10 ได้ 4
ส่วน overflow ของชนิด signed เป็น *undefined behaviour* คอมไพเลอร์ถือว่ามันไม่เกิด อย่าเขียนโค้ดที่พึ่งมัน

SDK ใช้ความรู้นี้จริงในหลายจุด ตัวอย่าง [`06_raw_register_access.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L243-L252)
แปลงค่าจากเซนเซอร์ SHT40 ด้วยตัวแปรกลาง 64 บิต และเขียนเหตุผลไว้ในคอมเมนต์ว่า "175000 * 65535 does not fit in 32 bits"
ส่วน [`05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L110-L115)
หาจำนวนรอบด้วย `sensor_auto_get_push_count() - before` ซึ่งถูกต้องแม้ตัวนับจะวนกลับ เพราะการลบของ unsigned ก็เป็น modulo เหมือนกัน

### 2. ตัวดำเนินการระดับบิตและ read-modify-write

รีจิสเตอร์ของอุปกรณ์หนึ่งตัวมักรวมหลายหน้าที่ไว้ในบิตคนละตำแหน่ง ถ้าเราเขียนค่าทั้งตัวทับ บิตของหน้าที่อื่นจะหายไปด้วย
วิธีที่ปลอดภัยคือ **read-modify-write** อ่านค่าเดิม แก้เฉพาะบิตที่เป็นของเรา แล้วเขียนกลับ

| ทำอะไร | เขียนแบบนี้ | ทำไมบิตอื่นไม่เปลี่ยน |
|---|---|---|
| ตั้งบิต (set) | `reg \|= mask;` | `x \| 0 == x` |
| ล้างบิต (clear) | `reg &= ~mask;` | `x & 1 == x` |
| สลับบิต (toggle) | `reg ^= mask;` | `x ^ 0 == x` |
| ทดสอบบิต | `if (reg & mask)` | ไม่ได้เขียนอะไร |
| เขียนฟิลด์หลายบิต | ล้างฟิลด์ก่อน แล้ว OR ค่าที่เลื่อนและตัดด้วย mask แล้ว | บิตเก่าในฟิลด์ไม่ค้าง |

คอมเมนต์ในตัวอย่างของ SDK สรุปไว้สั้นที่สุดว่า "The safe shape for any register write: read it, change only the bits you own,
write it back, read it again to confirm." ([06_raw_register_access.c บรรทัด 170-175](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L170-L175))

บนชิปจริงเรามักไม่แตะรีจิสเตอร์เอง แต่เรียกฟังก์ชันของ **PDL (Peripheral Driver Library)** ของ Infineon ที่ทำเรื่องนี้ให้
เช่น `Cy_GPIO_Set()` `Cy_GPIO_Clr()` `Cy_GPIO_Inv()` ตัวอย่าง [`04_gpio_led_button.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L62-L69)
อธิบายว่าคำสั่งเหล่านี้เป็นการเขียนรีจิสเตอร์ครั้งเดียวโดยไม่อ่านก่อน และ "atomic per pin on this part"
จึงไม่ต้องกันการแย่งกันระหว่าง task ที่คุมคนละขาของพอร์ตเดียวกัน นี่คือเหตุผลหนึ่งที่ควรใช้ PDL แทนการเขียน `|=` เองกับรีจิสเตอร์ GPIO
อีกเหตุผลคือค่าขั้วของหลอดและปุ่ม ตัวอย่างเดียวกันเตือนว่า "POLARITY COMES FROM THE BSP, NOT FROM YOU"
ให้ใช้ชื่อ `CYBSP_LED_STATE_ON` แทนเลข 1 เพราะบอร์ดรุ่นถัดไปอาจกลับขั้ว

### 3. volatile คือสัญญากับคอมไพเลอร์ ไม่ใช่กุญแจ

คอมไพเลอร์ที่เปิด optimisation มีสิทธิ์จำค่าตัวแปรไว้ในรีจิสเตอร์ของ CPU และตัดการอ่านหรือเขียนที่ดูเหมือนซ้ำหรือไร้ผลทิ้ง
ถ้าตัวแปรนั้นถูกเปลี่ยนโดย "คนอื่น" ที่คอมไพเลอร์มองไม่เห็น โปรแกรมจะทำงานผิดแบบเงียบ ๆ `volatile` บอกว่า
**ทุกการอ่านและทุกการเขียนต้องเกิดขึ้นจริงตามลำดับในโค้ด** ใช้เมื่อค่าอาจเปลี่ยนจากนอกโฟลว์ของโปรแกรม ได้แก่

- **รีจิสเตอร์ของอุปกรณ์** ที่ฮาร์ดแวร์เปลี่ยนค่าเอง (PDL ประกาศโครงสร้างรีจิสเตอร์ไว้ให้แล้ว)
- **ตัวแปรที่ ISR เขียนแล้ว task อ่าน** เช่น `static volatile uint32_t radar_drdy_events` ที่ ISR ของเรดาร์เพิ่มค่า
  ([radar_task.c บรรทัด 97](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L97))
- **ตัวแปรที่อีกคอร์หรือ DMA เขียน** และธงที่ task หนึ่งตั้งแล้วอีก task อ่าน เช่น `volatile bool tesaiot_radar_presence_detected`
  ([บรรทัด 51](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L51))
- **ลูปหน่วงเวลาแบบนับเลขเปล่า** เช่น `for (volatile uint32_t d = 0; d < 300000; d++) {}` ใน
  [proj_cm55/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L269)
  ถ้าไม่มี volatile คอมไพเลอร์ลบลูปที่ไม่มีผลทิ้งได้ทั้งลูป

สิ่งที่ volatile **ไม่ได้** ให้คือความเป็น atomic `count++` บนตัวแปร volatile ยังเป็นอ่าน แก้ เขียน สามจังหวะ
ซึ่ง interrupt แทรกกลางได้ การป้องกันเรื่องนั้นเป็นหัวข้อของบทเรียน 1.3 และโมดูล 4

## ตัวอย่างสมบูรณ์

[examples/01_types_and_bits.c](examples/01_types_and_bits.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** พิมพ์ขนาดของแต่ละชนิด แล้วแสดง overflow สามแบบ: `uint8_t` วนกลับ ไบต์สองตัวประกอบเป็น `int16_t` ที่ติดลบ
  และผลคูณที่ต้องขยายเป็น 64 บิตก่อนคูณ
- **ท่าที่ 2** ใช้ "รีจิสเตอร์" จำลองแบบ `volatile uint32_t` ตั้ง ล้าง และสลับบิตทีละบรรทัด
- **ท่าที่ 3** เขียนฟิลด์ MODE ขนาด 3 บิตแบบอ่านครั้งเดียว เขียนครั้งเดียว แล้วอ่านฟิลด์กลับมาตรวจ

ลองแก้ทีละอย่าง ทายผลก่อนรันทุกครั้ง

1. เปลี่ยน `uint8_t count` เป็น `uint16_t` แล้วรัน ทำไมคราวนี้ได้ 260
2. ลบ cast `(uint64_t)` ออกจากบรรทัด `right` แล้วรัน ตัวเลขสองตัวในบรรทัดนั้นเป็นอย่างไร
3. เปลี่ยน `mode` เป็น 9 ค่าที่อ่านกลับได้คืออะไร และ mask ช่วยอะไรไว้

อ่านต่อจากของจริงใน SDK: ขั้น read-modify-write ของตัวอย่าง `06_raw_register_access.c`
อ่านรีจิสเตอร์ `PWR_CTRL` ของ BMI270 เขียนค่าเดิมกลับ แล้วอ่านซ้ำเพื่อยืนยัน โดยถือ lock ของบัสตลอดทั้งขั้น
(เรื่อง lock อยู่ในบทเรียน 5.2)

```c
uint8_t pwr_before = 0u, pwr_after = 0u;
bool w_ok = false, v_ok = false;

if (!sensor_i2c_lock(RAW_LOCK_TIMEOUT_MS)) {
    printf("  bus busy\r\n");
    return SDK_EX_BUSY;
}
if (sensor_i2c_read_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL, &pwr_before)) {
    /* The single-byte form... */
    w_ok = sensor_i2c_write_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                 pwr_before);
    /* ...and the general form, which is what you need for any
     * multi-byte register. Same byte again: still a no-op. */
    if (w_ok) {
        w_ok = sensor_i2c_write_reg(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                    &pwr_before, 1u);
    }
    v_ok = sensor_i2c_read_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                &pwr_after);
}
sensor_i2c_unlock();
```

ที่มา: [06_raw_register_access.c บรรทัด 176-196](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L176-L196)
(Apache-2.0, tesaiot-pse84-devkit-sdk)

ทำไมเขียนค่าเดิมกลับ คอมเมนต์หัวไฟล์ตอบไว้: ถ้าเขียน `ACC_RANGE` (0x41) จากตรงนี้ ชิปจะเปลี่ยนช่วงวัดแต่ไดรเวอร์ไม่รู้
ค่าความเร่งทุกค่าหลังจากนั้นจะผิดไปสี่เท่าโดยไม่มีฟังก์ชันไหนคืน error เลย อ่านได้ทุกอย่าง แต่เขียนเฉพาะบิตที่ไม่มีใครพึ่งอยู่

## ฝึกเติม

เปิด [practice/01_bitops.c](practice/01_bitops.c) มีช่องให้เติม 2 จุดที่มีคำว่า `TODO` คือ `bits_set()` กับ `bits_clear()`
คอมไพล์และรันก่อนเติม คุณควรเห็น test ล้มหลายข้อ นั่นคือหลักฐานว่า test ตรวจอะไรบางอย่างจริง

```sh
gcc -std=c11 -Wall -Wextra -o bitops practice/01_bitops.c && ./bitops
```

เติมจนบรรทัดสุดท้ายพิมพ์ `PASS: 0 failure(s)`

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/01_bitops.c](solution/01_bitops.c)
คำตอบคือบรรทัดเดียวต่อฟังก์ชัน `*reg |= mask;` และ `*reg &= ~mask;` คอมเมนต์ในเฉลยอธิบายบั๊กที่พบบ่อยที่สุด
คือเขียน `*reg = mask;` หรือ `*reg &= mask;` ซึ่งลบบิตของหน้าที่อื่นทิ้ง

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** รันตัวอย่าง GPIO และ register ของ SDK บนบอร์ด แล้วอธิบายผลที่เห็นด้วยความรู้ของบทนี้

ถ้ายังไม่เคย build แม่แบบเฟิร์มแวร์ของ SDK ให้ทำ [บทเรียน 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md) ก่อน
(ภาพรวมของการ build และ flash ด้วย ModusToolbox อยู่ที่ [TESAIoT Firmware Stack บทเรียน 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md))
ตัวอย่างของ SDK ปิดไว้โดยค่าเริ่มต้น เปิดและเลือกตัวที่จะรันด้วยตัวแปรของ make

```sh
cd bento-firmware-template-mtb-only
make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
make program
```

1. **ถอดสาย USB ออกให้สุดแล้วเสียบใหม่** หลัง flash ทุกครั้ง (Appendix X #21 ในเอกสาร SDK: รีเซ็ตผ่าน debugger แล้วจอดำ
   ซึ่งดูเหมือน flash ล้มเหลวทั้งที่ไม่ใช่) เปิด serial console ที่ 115200 8N1 ไว้ก่อนเสียบ
2. อ่าน log ของ `[io/04]` ควรเห็นจำนวน LED ที่ BSP นิยาม บรรทัด `read-back: on=1 off=0 (expect 1 and 0)`
   แล้วกดปุ่ม SW2 บนบอร์ดสองสามครั้งในห้าวินาที ดูบรรทัด `SW2 down` / `SW2 up` และจำนวนการกดที่กันเด้งแล้ว
3. build ใหม่ด้วย `SDK_EXAMPLE_CM33=cm33/sensors/06_raw_register_access` แล้วดูสามบรรทัด: chip id ที่อ่านได้ (ควรเป็น `0x24`)
   ค่าดิบ X Y Z ของความเร่ง และบรรทัด `PWR_CTRL ... (verified, board unchanged)`
4. ตอบในบันทึกการทดลองว่า เมื่อวางบอร์ดราบ ค่าดิบแกนใดใหญ่ที่สุดและเป็นบวกหรือลบ ค่านั้นประกอบจากไบต์สองตัวอย่างไร
   และทำไมตัวอย่างต้อง cast เป็น `uint16_t` ก่อนเลื่อนบิต

**หลักฐานที่เก็บไว้ใน portfolio:** log จาก serial console ของทั้งสองตัวอย่าง และคำตอบข้อ 4 สั้น ๆ

## ไปต่อ

- เปิด [`cy_gpio.h` ของ mtb-pdl-cat1 @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h)
  แล้วหา `Cy_GPIO_Pin_FastInit()` กับค่าคงที่ `CY_GPIO_DM_STRONG` และ `CY_GPIO_DM_PULLUP` อ่านว่าพารามิเตอร์ `outVal` มีผลต่อโหมด pull-up อย่างไร
  แล้วเทียบกับคอมเมนต์ใน `04_gpio_led_button.c` ที่เตือนว่าส่ง 0 แล้วปุ่ม "appears permanently pressed"
- โจทย์ท้าทาย: เขียนฟังก์ชัน `field_read(reg, msk, pos)` คู่กับ `field_write()` ในแบบฝึก แล้วเพิ่ม test ของมันเอง

บทถัดไป: [บทเรียน 1.2 แผนที่หน่วยความจำ stack และ heap](../l02-memory-map-stack-heap/README.md) ถามต่อว่าตัวแปรแต่ละตัวในบทนี้อยู่ที่ไหนในหน่วยความจำ

## สะท้อนคิด

- ตัวแปรตัวไหนในโปรแกรมที่คุณเคยเขียนด้วย Python ที่ถ้าย้ายมาเป็น C แล้วจะ overflow เงียบ ๆ
- ถ้าเพื่อนร่วมทีมใส่ `volatile` ให้ทุกตัวแปร "เผื่อไว้" คุณจะอธิบายเขาอย่างไรว่าทำไมไม่ช่วย และอาจทำให้ช้าลง

## แหล่งอ้างอิง

- [SDK: cm33/sensors/06_raw_register_access.c (read-modify-write บนอุปกรณ์ I2C)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/io/04_gpio_led_button.c (คำสั่ง PDL เบื้องหลัง gpio.led()/gpio.button())](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [SDK: cm33/sensors/05_auto_push_task.c (ตัวนับแบบ unsigned และการลบค่า)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c)
- [SDK: tesaiot-radar/radar_task.c (ตัวแปร volatile ที่ ISR และ task ใช้ร่วมกัน)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c)
- [Peripherals at a glance (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__peripherals__quickref.html)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
