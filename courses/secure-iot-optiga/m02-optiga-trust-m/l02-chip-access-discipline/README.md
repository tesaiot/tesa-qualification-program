---
id: sec-iot.m02.l02
lang: th
title: {th: กติกาการเข้าถึงชิป, en: The chip-access discipline}
summary: {th: ใช้ประตูเข้าชิป lock และการกันหน้าจอสัมผัสออกจากบัสขณะชิปทำงาน ตามลำดับที่ SDK กำหนด, en: 'Use the chip gate, lock and touch-hold in the order the SDK requires.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l01]
objectives:
- {th: 'เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release', en: 'Order init, acquire, use and release correctly, and explain what happens if release is forgotten.'}
- {th: อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ, en: 'Explain why touch-hold must wrap the whole transaction, not just its setup.'}
- {th: ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที, en: Identify work that must leave the display task because chip transactions take seconds.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
---

# บทเรียน 2.2: กติกาการเข้าถึงชิป

> โมดูล 2 · ชิปความปลอดภัย OPTIGA™ Trust M · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ชิปความปลอดภัยบนบอร์ดมีตัวเดียว อยู่บนบัส I2C เส้นเดียว แต่มีอย่างน้อยสี่ส่วนของเฟิร์มแวร์ที่อยากใช้มัน
ตัวอย่าง [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c) นับให้ดู
คือเส้นทาง mTLS/MQTT หน้าจอลงทะเบียนของ HSM โมดูล `optiga` ของ MicroPython และโค้ดที่คุณกำลังจะเขียน
บทนี้คือกติกาที่ทำให้ทุกส่วนใช้ชิปร่วมกันได้โดยไม่ชนกัน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release
2. อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ
3. ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 2.1: ชิปความปลอดภัยทำอะไรให้เรา](../l01-secure-element-role/README.md) คุณควร build แม่แบบของ SDK และรันตัวอย่าง `ref_hsm` ได้แล้ว
- **ทบทวน:** task, priority, mutex และ `vTaskDelay()` ของ FreeRTOS ถ้าไม่แน่ใจ ทบทวนจากหลักสูตรพื้นฐานภาษา C ก่อน
- **บอร์ด:** TESAIoT Dev Kit ที่เสียบ USB และเปิด serial terminal ไว้ มือว่างหนึ่งข้างสำหรับแตะจอระหว่างแล็บ

## ดูของจริงก่อน

คอมเมนต์ต้นไฟล์ [04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c) เล่าบั๊กจริงไว้ว่า
บน TESAIoT Dev Kit ชิปความปลอดภัยกับตัวควบคุมจอสัมผัสใช้บัส I2C เส้นเดียวกัน และถูกสั่งจากคนละคอร์
เมื่อ CM55 อ่านจอสัมผัสขณะที่ CM33 คุยกับชิปอยู่ ธุรกรรมบางครั้งไม่จบ และไลบรารีของผู้ผลิตไม่มี timeout ในเส้นทางนั้น ลายเซ็นจึงไม่ล้มเหลว แต่ **ค้าง**
build เดียวกันเชื่อมต่อได้ในหนึ่งวินาทีรอบหนึ่ง แล้วค้างตลอดไปในรอบถัดไป

เส้นทาง mTLS ในตอนนั้นหยุดจอสัมผัสระหว่าง "ตั้งค่า" แล้วปล่อยตอนตั้งค่าเสร็จ

**ทายก่อน:** ถ้าจุดที่หยุดจอสัมผัสดูถูกต้องแล้ว ทำไมบั๊กจึงยังเกิด ลองนึกว่าลายเซ็นของ TLS เกิดขึ้น **ตอนไหน** เขียนคำทายไว้ แล้วหาคำตอบในแนวคิดข้อ 2

## แนวคิด

### 1. ประตูเดียว สามชื่อ

ตาม [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c)
และบท [D1 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html) คู่ฟังก์ชันสามคู่นี้ถือและคืน **ประตูเดียวกัน**

| คู่ | ตอบคำถามว่า | ต่างจากคู่อื่นตรงไหน |
|---|---|---|
| `optiga_chip_enter()` / `optiga_chip_exit()` | มี task อื่นถือชิปอยู่หรือไม่ | คืน `false` ด้วยเหตุผลเดียวคือมีคนอื่นถือ |
| `optiga_manager_lock()` / `optiga_manager_unlock()` | ตัวจัดการพร้อมหรือยัง และขอใช้ได้ไหม | คืน `false` ถ้ายังไม่ init |
| `optiga_manager_acquire()` / `optiga_manager_release()` | ขอ `optiga_util_t *` ที่ใช้สั่งชิป พร้อมถือประตู | คืน `NULL` ถ้ายังไม่ init หรือรอไม่ได้ |

**ลำดับที่ต่อรองไม่ได้** คือ `optiga_manager_init()` ต้องมาก่อนทุกอย่าง มันสร้าง mutex กับ `optiga_util_t` ที่ใช้ร่วมกัน เรียกซ้ำได้ และเรียกจาก task เท่านั้น (บท D1 เตือนว่าเรียกก่อน scheduler ไม่ได้)
ก่อน init `acquire()` คืน `NULL` และ `lock()` คืน `false` แต่ `optiga_chip_enter()` **คืน `true`** ทั้งที่ไม่ได้ล็อกอะไร ผู้เขียนตั้งใจให้เป็นแบบนั้น
เพื่อให้ `false` ของ `enter()` แปลได้อย่างเดียวว่า "มีคนอื่นถือชิป" จึง **ห้ามใช้ `enter()` เป็นคำถามว่าชิปพร้อมไหม** คำถามนั้นเป็นงานของ `lock()`

ประตูนี้ **ซ้อนได้ใน task เดียวกัน** เพราะฟังก์ชันช่วยในเฟิร์มแวร์เรียกกันเอง เช่นการสร้างกุญแจเรียกการอ่าน metadata ต่อ mutex ธรรมดาจะ deadlock ตั้งแต่การเรียกซ้อนครั้งแรก
แต่ทุกการถือยังต้องมีการคืนหนึ่งครั้ง ตัวนับความลึกทำให้การคืนครั้งนอกสุดเท่านั้นที่ปล่อยประตูจริง

task **อื่น** ที่มาขอจะรอได้นานสุดสิบวินาทีแล้วได้ `false` ดังนั้นถ้าลืม `release()` หลัง `acquire()` สักทางออกหนึ่ง
ชิปจะถูกกันไว้ตลอดการบูตครั้งนั้น ตามคำของ 03 ส่วนอื่นทั้งหมดที่ต้องใช้ชิป เช่นการลงนาม TLS จะรอสิบวินาทีแล้วล้มทุกครั้ง
กลับกัน ถ้า `acquire()` คืน `NULL` **ห้าม** เรียก `release()` เพราะตัวมันคืนประตูเองแล้ว การคืนเกินทำให้ตัวนับของ task ที่ถืออยู่จริงเพี้ยน

ข้อสุดท้าย ทุกฟังก์ชัน `optiga_util_*` และ `optiga_crypt_*` ทำงานแบบ asynchronous มันคืนค่าทันทีและผลจริงมาที่ callback
ต้อง **ถือประตูไว้ตลอดช่วงรอ** ถ้าคืนประตูระหว่างที่คำสั่งยังวิ่ง เท่ากับยกบัสให้ task อื่นกลางธุรกรรม

### 2. touch-hold ต้องครอบทุกไบต์ ไม่ใช่แค่ฟังก์ชันที่ดูเหมือนงานเข้ารหัส

คำตอบของคำทายอยู่ใน 04_touch_hold.c ลายเซ็นที่สำคัญคือ **CertificateVerify** และมันเกิดทีหลัง ข้างใน `cy_mqtt_connect()` ตอนที่ handshake ของ TLS วิ่ง
ถึงตอนนั้นจอสัมผัสกลับมาอ่านบัสแล้ว การ hold จึงต้องครอบ **ไบต์สุดท้ายที่คุยกับชิป** ไม่ว่ามันจะอยู่ที่ไหน
เฟิร์มแวร์ปัจจุบันจึงให้ `trustm_ecdsa_sign()` ถือทั้งประตูและ touch-hold เองตลอดการลงนาม (บท C4 และ D1)

อาการที่ต้องจำให้ขึ้นใจคือ `OPTIGA_COMMS_ERROR (0x0102)` บท D1 อธิบายว่ามันแปลว่าธุรกรรมกับชิปวิ่งขณะที่ CM55 อ่านจอสัมผัสบนบัสเดียวกัน
และมักตามด้วย `OPTIGA_UTIL_ERROR_INSTANCE_IN_USE (0x0305)` ในคำสั่งถัดไป บท D1 บันทึกเหตุการณ์จริงไว้ด้วยว่าการเขียน metadata 8 ไบต์ผ่าน
แต่การเขียนใบรับรอง 580 ไบต์ที่ตามมาล้มด้วย `0x0102` หลังลองซ้ำอยู่ 57 วินาที เพราะโค้ดที่ยกมาจากโปรเจกต์อ้างอิงซึ่งไม่มีจอสัมผัส ไม่มี touch-hold เลย
ทางแก้ของ SDK คือถือ hold ครอบทั้งฟังก์ชัน ไม่ใช่ทีละคำสั่ง เพราะการปล่อยระหว่างขั้นจะเปิดช่องเดิมขึ้นมาอีก

กติกาของ hold จากตัวอย่าง 04

- **นับได้** hold ซ้อนกันได้ ครั้งแรกเท่านั้นที่หยุดจอสัมผัส และครั้งสุดท้ายเท่านั้นที่ปล่อย ต้องคืนเท่ากับที่ถือทุกทางออก รวมทางที่ error
- **hold ครั้งแรกหน่วงราว 50 ms** โดยตั้งใจ เพื่อให้การอ่านจอที่ค้างอยู่จบก่อนชิปเริ่มคุย hold ที่ซ้อนไม่เสียเวลา
- **ใช้ใน task เท่านั้น** มัน sleep จึงไม่ปลอดภัยใน ISR
- **ระหว่าง hold จอไม่รับการแตะเลย** ให้ใช้ `optiga_manager_touch_hold_reason("...")` ข้อความนี้ถูกส่งไปแสดงบนจอ และจอแสดงเฉพาะข้อความของ hold ครั้งแรก
- **hold ที่ไม่มีคนคืนทำให้จอหูหนวกถาวร** สำหรับคนที่ถือบอร์ด จอที่ไม่รับการแตะดูไม่ต่างจากเครื่องค้าง และไม่มีคำสั่ง "บังคับปล่อย" การคืนเกินไม่ช่วยแก้ ตัวนับหยุดที่ศูนย์ แต่มันคือบั๊กของการจับคู่ที่จะไปโผล่ในรอบถัดไป
- **ห้ามส่งคำสั่ง `IPC_CMD_TOUCH_RESUME` ตรง ๆ** บท D1 อธิบายว่า CM55 ถือคำสั่งนี้เป็นการเปิดจอแบบไม่นับ มันจะยกเลิก hold ที่ task อื่นพึ่งอยู่

**ลำดับการซ้อน** SDK ใช้ได้ทั้ง hold ครอบ lock (ตัวอย่าง 04) และ lock ครอบ hold (`trustm_ecdsa_sign()` ในบท D1)
สิ่งที่ต้องเหมือนกันเสมอมีสองข้อ hold ต้องครอบทุกไบต์ที่คุยกับชิป และคู่ต้องซ้อนกันถูก คือ **สิ่งที่ถือทีหลังคืนก่อน**
บท D1 ตั้งเป็นกับดักข้อ 4 ไว้ว่าถ้าเข้าด้วย lock แล้ว hold ขาออกต้อง release hold ก่อนแล้วค่อย unlock

### 3. งานที่ใช้เวลาหลายวินาทีต้องออกจาก task ที่วาดจอ

ธุรกรรมกับชิปบางอย่างใช้เวลาเป็นวินาที การสร้างคู่กุญแจแล้วลงนาม CSR และการรับ Protected Update เป็นบทสนทนายาวกับชิป
การขอประตูอาจรอได้ถึงสิบวินาที ถ้าสิ่งเหล่านี้เกิดใน task ของ LVGL จอจะค้างทั้งจอ

[01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c) บอกผลร้ายที่หนักกว่าจอค้าง
ถ้ารอผลแบบ inline จอจะค้าง และ **พร้อมกันนั้น** `ui_busy_modal_service()` ก็วาดหน้าต่างที่อธิบายว่าทำไมค้างไม่ได้ จอจึงทั้งตายและเงียบ
ทางแก้ของ SDK คือคำสั่ง `IPC_CMD_HSM_PROVISION` คืนค่าทันที งานจริงไปวิ่งใน worker task ฝั่ง CM33_NS (บท D2 ระบุว่า `prov_task` ตรวจงานทุก 50 ms) และจอใช้ `lv_timer` ถามสถานะเป็นระยะ

งานที่ **ต้องไม่อยู่** ใน callback ของปุ่มหรือใน task วาดจอ

- `optiga_manager_lock()` และ `optiga_manager_acquire()` (อาจรอสิบวินาที)
- คำสั่งใด ๆ ที่คุยกับชิป และการรอ callback ของมัน
- การรอคำตอบจากเครือข่าย เช่นรอแพลตฟอร์มส่งใบรับรองกลับมา (บท D2 ระบุว่ารอได้ถึง 60 วินาที)
- handler ที่ถูกเรียกจาก event thread ของ MQTT ก็เช่นกัน บท C3 ให้ส่งงานที่แตะชิปเข้าคิวไปให้ task ของคุณเอง

และข้อที่กลับด้าน บท D1 เตือนว่า **อย่าถือ touch-hold ข้ามช่วงรอเครือข่าย** ช่วงรอ 60 วินาทีนั้นไม่มีไบต์ไหนคุยกับชิป การถือ hold ไว้คือการแช่แข็งจอเป็นนาทีโดยไม่มีเหตุผล

## ตัวอย่างสมบูรณ์

ส่วนแรกตัดจาก [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c) บรรทัด 136–145
และส่วนที่สองจาก [04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c) บรรทัด 94–104
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    optiga_util_t *util = optiga_manager_acquire();
    if (util == NULL) {
        /* Either the gate timed out or the instance is missing. acquire()
         * releases the gate itself before returning NULL, so there is nothing
         * to give back here — do not call release() on a NULL. */
        printf("  optiga_manager_acquire() = NULL — busy, or the manager is "
               "not up\r\n");
        return SDK_EX_BUSY;
    }
    printf("  optiga_manager_acquire() = %p (gate held)\r\n", (void *)util);
```

```c
    /* The chip work belongs here, between the outermost hold and its release.
     * Note the ordering against example 01: take the chip gate and hold touch
     * for the same span. Two rules, one lifetime.
     *
     *     optiga_manager_touch_hold_reason("Signing");
     *     if (optiga_manager_lock()) {
     *         ... chip operations, including the wait for the callback ...
     *         optiga_manager_unlock();
     *     }
     *     optiga_manager_touch_release();
     */
```

อ่านสองส่วนนี้คู่กัน กติกาสองข้อ อายุเดียวกัน ทั้งประตูและ hold ต้องครอบช่วงเวลาเดียวกัน คือตั้งแต่ก่อนไบต์แรกจนหลังไบต์สุดท้ายของธุรกรรม **รวมช่วงที่รอ callback**
(คำว่า "example 01" ในคอมเมนต์หมายถึงตัวอย่างการครอบครองชิป ซึ่งในแม่แบบปัจจุบันคือไฟล์ 03)

## ฝึกเติม

ฟังก์ชันข้างล่างอ่านข้อมูลจากช่องหนึ่งของชิปภายใต้กติกาทั้งสอง เป็นโค้ดที่เขียนขึ้นใหม่สำหรับบทเรียนนี้โดยใช้ API ของ SDK
สมมติว่า `optiga_manager_init()` ถูกเรียกไปแล้ว และ callback ที่ลงทะเบียนไว้ตอน init เป็นคนเขียน `s_status` เติมช่อง (1) ถึง (5)

```c
static volatile optiga_lib_status_t s_status;   /* callback ที่ลงทะเบียนตอน init เขียนค่านี้ */

bool read_object_held(uint16_t oid, uint8_t *buf, uint16_t *len)
{
    bool ok = false;

    ____(1)____("Reading the secure element");       /* กันจอสัมผัสออกจากบัส */

    optiga_util_t *util = ____(2)____();             /* ถือประตูและรับ util */
    if (util == NULL) {
        ____(3)____();                               /* ออกทางนี้ต้องคืนอะไร */
        return false;
    }

    s_status = OPTIGA_LIB_BUSY;
    if (optiga_util_read_data(util, oid, 0, buf, len) == OPTIGA_LIB_SUCCESS) {
        for (int i = 0; i < 200 && s_status == OPTIGA_LIB_BUSY; i++) {
            vTaskDelay(pdMS_TO_TICKS(10));           /* รอ callback สูงสุดราว 2 วินาที โดยยังถือประตู */
        }
        ok = (s_status == OPTIGA_LIB_SUCCESS);
    }

    ____(4)____();                                   /* คืนประตู */
    ____(5)____();                                   /* ปล่อยจอสัมผัส */
    return ok;
}
```

<details><summary>เฉลย</summary>

1. `optiga_manager_touch_hold_reason` ข้อความนี้จะขึ้นบนจอระหว่างที่จอไม่รับการแตะ
2. `optiga_manager_acquire`
3. `optiga_manager_touch_release` **ไม่ใช่** `optiga_manager_release` เพราะ `acquire()` ที่คืน `NULL` ปล่อยประตูเองแล้ว แต่ hold ที่เราถือไว้ยังต้องคืน
4. `optiga_manager_release` หลังรอ callback เสร็จแล้วเท่านั้น
5. `optiga_manager_touch_release` ถือ hold ก่อน จึงคืนทีหลัง

สังเกตว่าลูปรอมีเพดาน บท C4 และคอมเมนต์ใน `mqtt_mtls_setup.c` เล่าว่าลูปรอแบบ `while (status == BUSY);` ที่ไม่มี timeout ทำให้ CM33_NS ค้างทั้งคอร์มาแล้ว

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ทำไม `optiga_chip_enter()` จึงใช้เป็นคำถามว่า "ชิปพร้อมหรือยัง" ไม่ได้ *(เป้าหมายข้อ 1)*
   - ก) เพราะมันช้า
   - ข) เพราะก่อน init มันคืน `true` ทั้งที่ไม่ได้ล็อกอะไร มันคืน `false` เฉพาะเมื่อมีคนอื่นถือชิป
   - ค) เพราะมันใช้ได้เฉพาะใน ISR
   - ง) เพราะมันเขียน metadata

   <details><summary>เฉลย</summary>

   **ข** คำถามว่าตัวจัดการพร้อมหรือยังเป็นงานของ `optiga_manager_lock()`

   </details>

2. โค้ดหนึ่งเรียก `optiga_manager_acquire()` ได้ค่าไม่เป็น NULL แล้ว `return` ออกกลางทางเมื่ออ่านข้อมูลล้มเหลว โดยไม่เรียก `release()` ผลคืออะไร *(เป้าหมายข้อ 1)*
   - ก) ไม่มีผล ประตูปล่อยเองเมื่อฟังก์ชันจบ
   - ข) ชิปถูกกันไว้ตลอดการบูตครั้งนั้น task อื่นที่ขอจะรอสิบวินาทีแล้วล้ม รวมถึงการลงนาม TLS
   - ค) ชิปรีเซ็ตตัวเอง
   - ง) LcsO เปลี่ยนเป็น operational

   <details><summary>เฉลย</summary>

   **ข** ตัวอย่าง 03 เรียกสิ่งนี้ว่าการรั่วของชิปไปจนจบการบูต ทางแก้คือเขียนฟังก์ชันให้มีทางออกเดียว

   </details>

3. เส้นทาง mTLS แบบเก่าหยุดจอสัมผัสเฉพาะช่วงตั้งค่า ทำไมยังค้าง *(เป้าหมายข้อ 2)*
   - ก) เพราะการตั้งค่าใช้เวลานานเกินไป
   - ข) เพราะลายเซ็น CertificateVerify เกิดทีหลังใน `cy_mqtt_connect()` ตอนที่จอสัมผัสกลับมาอ่านบัสแล้ว
   - ค) เพราะชิปไม่รองรับ TLS
   - ง) เพราะใช้พอร์ตผิด

   <details><summary>เฉลย</summary>

   **ข** hold ต้องครอบไบต์สุดท้ายที่คุยกับชิป ไม่ใช่ครอบฟังก์ชันที่ดูเหมือนงานเข้ารหัส

   </details>

4. ในปุ่ม "ลงทะเบียน" บนหน้าจอ LVGL ข้อใดควรอยู่ใน callback ของปุ่ม *(เป้าหมายข้อ 3)*
   - ก) `optiga_manager_lock()` แล้วสร้างคู่กุญแจ
   - ข) รอใบรับรองจากแพลตฟอร์มจนกว่าจะมา
   - ค) ปิดหน้าต่างเก่า เปิดหน้าต่างใหม่ ส่งคำขอให้ worker task แล้วให้ `lv_timer` ถามสถานะ
   - ง) ถือ touch-hold ไว้จนกว่าการลงทะเบียนจะเสร็จ

   <details><summary>เฉลย</summary>

   **ค** งานยาวไปอยู่ใน worker ส่วนจอแค่ถามสถานะ นี่คือแบบของ `hsm_enrol_open()` ที่บทเรียน 5.2 จะลงลึก

   </details>

## แล็บ

**ดูกติกาทำงานจริง แล้วออกแบบปุ่มหนึ่งปุ่มให้ถูก**

- [ ] build ด้วย `SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership` แล้ว flash
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  จดทุกบรรทัดที่ขึ้นหลัง `--- tesaiot_hsm/01_chip_ownership ---` (ชื่อในบรรทัดหัวยังเป็นเลขเดิมของไฟล์) แล้วเขียนกำกับแต่ละบรรทัดว่าตัวนับความลึกของประตูเป็นเท่าไร
- [ ] build ใหม่ด้วย `SDK_EXAMPLE_CM33=cm33/security/04_touch_hold` ตัวรันจะเริ่มราวสามวินาทีหลังบูต ช่วงนั้นให้แตะจอรัว ๆ แล้วจดว่าเห็นข้อความ `Reading device certificate` บนจอหรือไม่ และการแตะช่วงนั้นมีผลไหม
  บันทึกบรรทัดใน console ที่บอกตัวนับ `count 2 -> 1` และ `count 1 -> 0`
- [ ] อ่านห้าฟังก์ชัน `*_held()` ในบท [D1](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html) จดข้อความ reason ทั้งหมดที่ขึ้นบนจอ และอธิบายว่าทำไมไม่มีฟังก์ชันไหนถือ hold ข้ามช่วงรอแพลตฟอร์ม
- [ ] **ออกแบบ** ปุ่ม "อ่านใบรับรอง" บนหน้าจอ LVGL วาดแผนภาพลำดับที่มีสี่ส่วน คือ callback ของปุ่ม (task วาดจอ) คิวหรือ IPC worker task ที่ถือประตูและ hold และ `lv_timer` ที่ถามสถานะ
  เขียนกำกับว่าแต่ละขั้นอยู่คอร์ไหน task ไหน และระบุสามอย่างที่ห้ามเกิดใน callback ของปุ่ม
- [ ] เอาคำตอบฝึกเติมของคุณมาเทียบกับแผนภาพ ฟังก์ชัน `read_object_held()` ควรถูกเรียกจากกล่องไหน

## ไปต่อ

ตอนนี้เรารู้ว่าชิปลงนามอย่างไรและต้องเข้าถึงอย่างไร โมดูลถัดไปจะตามลายเซ็นนั้นเข้าไปใน handshake ของ TLS
ว่าชิปถูกเรียกตอนไหน ใบรับรองไหนถูกส่ง และเมื่อการเชื่อมต่อล้มเหลว จะอ่านอาการอย่างไร

บทเรียนถัดไป: [บทเรียน 3.1: TLS และ mTLS](../../m03-mtls-to-platform/l01-tls-and-mtls/README.md)

## สะท้อนคิด

- ในเฟิร์มแวร์ที่คุณเคยเขียน มีทรัพยากรที่ใช้ร่วมกันตัวไหนที่ถูกป้องกันแค่ "ช่วงตั้งค่า" แต่ไม่ครอบช่วงใช้งานจริง
- ฟังก์ชันที่มีหลายทางออกในโค้ดของคุณ คืนทรัพยากรครบทุกทางไหม คุณรู้ได้อย่างไร
- ผู้ใช้ของคุณจะแยก "จอกำลังรองานยาว" ออกจาก "เครื่องค้าง" ได้อย่างไร

## แหล่งอ้างอิง

- [SDK: cm33/security/03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c)
- [SDK: cm33/security/04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c)
- [SDK: cm55/security/01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c)
- [D1 — The chip-access discipline: gate, lock, touch-hold (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html)
- [Chip gate & manager (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tesaiot__hsm__chip__manager.html)
- [C3 — TESAIoT cloud: config file → MQTT task → broker (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
