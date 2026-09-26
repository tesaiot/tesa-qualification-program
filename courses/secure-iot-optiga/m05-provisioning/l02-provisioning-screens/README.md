---
id: sec-iot.m05.l02
lang: th
title: {th: หน้าจอลงทะเบียนบนอุปกรณ์, en: Provisioning screens on the device}
summary: {th: ส่งงานที่ใช้เวลาหลายวินาทีให้หน้าจอที่คอยถามสถานะ และปิดหน้าจอเก่าก่อนเปิดใหม่เสมอ, en: Hand seconds-long secure-element work to a polling screen and always tear the previous overlay down first.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l01]
objectives:
- {th: อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป, en: Explain why the provisioning screen polls instead of waiting on the chip.}
- {th: เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง, en: Order the overlay teardown and the enrol screen opening as the SDK example does.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: gui.embedded, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
---

# บทเรียน 5.2: หน้าจอลงทะเบียนบนอุปกรณ์

> โมดูล 5 · การลงทะเบียนอุปกรณ์อย่างปลอดภัย · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

การลงทะเบียนในบทที่แล้วใช้เวลาตั้งแต่หลายวินาทีจนถึงหนึ่งนาที ระหว่างนั้นคนที่ถือบอร์ดต้องรู้ว่าเครื่องกำลังทำอะไร และจอต้องไม่ค้าง
บทนี้ดูว่าหน้าจอ Enrol และ Protect ของ SDK ออกแบบอย่างไร ทำไมต้องถามสถานะเป็นระยะ และทำไมต้องปิดหน้าจอเก่าก่อนเปิดใหม่ **เสมอ**

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป
2. เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 5.1: ลงทะเบียนด้วย CSR](../l01-csr-enrolment/README.md) และแนวคิดข้อ 3 ของ [บทเรียน 2.2](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md) (งานยาวต้องออกจาก task วาดจอ)
- **ทบทวน LVGL:** ปุ่ม event และ state machine ของหน้าจอ จาก [TESAIoT Firmware Stack บทเรียน 2.2](../../../tesaiot-firmware-stack/m02-hmi-menu-setting/l02-button-event/README.md) และ [บทเรียน 2.7](../../../tesaiot-firmware-stack/m02-hmi-menu-setting/l07-final-wifi-manager/README.md)
- **บอร์ด:** แม่แบบของ SDK ที่ build ด้วย `ENABLE_PAGE_EXAMPLES=1` แล็บของบทนี้ **ถอดข้อมูลรับรองของแพลตฟอร์มออกจากไฟล์ตั้งค่าก่อน** เพื่อให้การลงทะเบียนหยุดตั้งแต่ขั้นเชื่อมต่อ และไม่มีการสร้างกุญแจ

## ดูของจริงก่อน

คอมเมนต์ต้นไฟล์ [01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c) บอกสองเรื่อง
เรื่องแรก ถ้ารอผลของชิปแบบ inline จอจะค้าง **และ** `ui_busy_modal_service()` ก็วาดหน้าต่างที่อธิบายว่าทำไมค้างไม่ได้ จอจึง "dead AND silent"
เรื่องที่สอง ถ้าหน้าต่างของรอบก่อนยังเปิดอยู่ การเปิดอีกหน้าต่างจะถูกปฏิเสธแบบเงียบ ๆ เพราะ `shell_open()` คืนทันทีเมื่อมีหน้าต่างอยู่แล้ว

**ทายก่อน:** สำหรับคนที่ถือบอร์ด "จอค้างและเงียบ" กับ "แตะแล้วไม่มีอะไรเกิดขึ้น" ต่างกันไหม ทั้งสองอาการนี้จะทำให้เขาทำอะไรต่อ

## แนวคิด

### 1. ทำไมต้องถามสถานะ ไม่ใช่รอ

งานเบื้องหลังหน้าจอ Enrol ใช้เวลานานด้วยสามเหตุผลที่เราเห็นมาแล้ว การขอประตูเข้าชิปรอได้ถึงสิบวินาที (บทเรียน 2.2)
การสร้างคู่กุญแจแล้วลงนาม CSR เป็นธุรกรรมยาวกับชิป และการรอแพลตฟอร์มตอบใช้เวลาได้ถึง 60 วินาที (บท D2)
ถ้า task ของ LVGL รอสิ่งเหล่านี้เอง จอจะหยุดวาดทั้งจอ

บท [D2 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html) แสดงว่า SDK แบ่งงานเป็นสามชั้น

```text
 CM55 (จอ)                              CM33_NS
 ปุ่ม Enrol → hsm_enrol_open()
   เปิดหน้าต่างเต็มจอ
   ส่ง IPC_CMD_HSM_PROVISION (op=CSR) ─▶ handle_hsm_provision()
   ◀─────────────── คืนทันที ─────────   ถ้ามีงานวิ่งอยู่ ปฏิเสธด้วย HSM_PROV_REJECTED_BUSY
                                          ตั้ง pending_op
   lv_timer ถามด้วย op=POLL ─────────▶  prov_task ตรวจ pending_op ทุก 50 ms แล้วเรียก prov_run(op)
   ◀── state, step, ข้อความ ───────────   prov_say(state, step, "ประโยคสำหรับคนอ่าน")
   วาดสถานะ วาดข้อความ วนต่อ
```

ค่าที่วิ่งบน IPC ตามบท D2 คือ op `POLL 0`, `CSR 1`, `PU 2`, `FETCH_CSR 3`, `UNLOCK 4` state `IDLE/BUSY/DONE/FAILED`
และ step `KEYGEN 1`, `CSR 2`, `PUBLISH 3`, `WAIT 4`, `INSTALL 5`, `VERIFY 6` จอจึงไม่ต้องรู้เลยว่าชิปทำอะไรอยู่ มันแค่ถามว่า "ตอนนี้ถึงไหน" แล้ววาด

ระหว่างที่ชิปทำงาน เฟิร์มแวร์ถือ touch-hold พร้อมข้อความเหตุผล ข้อความนั้นขึ้นบนจอในช่วงที่จอไม่รับการแตะ
แต่ช่วงรอแพลตฟอร์ม 60 วินาทีไม่มีการถือ hold จอจึงยังตอบสนอง (กับดักข้อ 5 ของบท D1)
ประโยคบนจอทั้งเจ็ดที่เราเห็นในบทเรียน 5.1 มาจาก `prov_say()` ฝั่ง CM33_NS บท D2 ยืนยันว่าเป็นข้อความในซอร์สที่ตรวจแล้ว
ส่วนป้ายของแต่ละ step ที่อยู่ใน `libbento_cm55.a` บท D2 เตือนว่ายังพิสูจน์ไม่ได้ว่าป้ายไหนคู่กับ step ไหน เพราะไฟล์ของหน้าจอไม่ได้ส่งมาเป็นซอร์ส ให้ยึดประโยคเจ็ดประโยคเป็นหลักฐาน

### 2. ปิดของเก่าก่อนเสมอ

`hsm_provision_ui_teardown()` ปิดหน้าต่างที่ค้างอยู่และ **ยกเลิก timer ที่ถามสถานะ** ของมัน เรียกซ้ำได้และปลอดภัยแม้ไม่มีอะไรเปิดอยู่
มันกันปัญหาสองแบบ

- **แตะแล้วเงียบ** ถ้าไม่ปิดของเก่า การเปิดใหม่ถูกปฏิเสธเงียบ ๆ คนที่แตะคิดว่าเครื่องไม่รับคำสั่ง
- **timer ที่ค้างเขียนใส่หน้าจอที่ถูกสร้างใหม่** timer ของรอบก่อนยังยิงอยู่ และเขียนลงวัตถุ LVGL ที่ถูกลบหรือสร้างใหม่ไปแล้ว

บท D2 จึงให้หน้าของ HSM เรียก `hsm_provision_ui_teardown()` เป็น **คำสั่งสุดท้าย** ของ callback ตอนหน้าถูกทำลาย หลังจากลบ timer ของหน้าเองแล้ว
ไม่อย่างนั้น timer ที่ถามสถานะอาจยิงหลังวัตถุถูกคืนหน่วยความจำไปแล้ว

### 3. หน้าจอที่พูดความจริง

สองหน้าจอนี้ออกแบบให้คนที่ถือบอร์ดตัดสินใจได้ถูก

- หน้า **Protect** แสดงชุดการเปลี่ยนแปลงที่จะเกิด **ก่อน** ทำ และไม่เขียนอะไรจนกว่าจะกดยืนยัน (คอมเมนต์ใน 01_hsm_screens.c)
- หน้า **Enrol** ที่เจอช่องซึ่งถูกล็อก บอกว่า "This slot takes signed manifests only ... Nothing was changed." ก่อนสร้างกุญแจ (บทเรียน 4.2)
- ผลตัดสินสุดท้ายแยกสามกรณี "The device can prove it holds the key this certificate names" หรือ "Installed, but the certificate does not belong to this chip's key" หรือ "Installed; the pair check could not run" ตามบท D2
  สามประโยคนี้ต่างกันเพราะต้องการการตอบสนองต่างกัน เหมือนหลักของรหัสผลใน `02_model_signature_hook.c` ที่ไม่รวม "ไม่มีลายเซ็น" กับ "ตรวจไม่ได้" เป็นค่าเดียว

## ตัวอย่างสมบูรณ์

ตัดจาก [01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c) บรรทัด 55–74 และ 78–80
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* Idempotent, and first. If an earlier run's overlay is still up, opening
     * another would be refused silently -- shell_open() returns when one
     * already exists -- and the tap would look like it did nothing. */
    hsm_provision_ui_teardown();

    if (s_open_protect_next) {
        s_open_protect_next = false;
        hsm_protect_open();
        sdk_example_logf("opened Protected Update.");
        sdk_example_logf("it shows the pending change set BEFORE running it --"
                         " nothing is written until you confirm.");
        sdk_example_logf("tap this example again for the Enrol screen.");
    } else {
        s_open_protect_next = true;
        hsm_enrol_open();
        sdk_example_logf("opened Enrol Certificate.");
        sdk_example_logf("key pair -> CSR -> proof of possession -> certificate;"
                         " each step polls, none of it blocks this task.");
        sdk_example_logf("tap this example again for the Protected Update screen.");
    }
```

```c
    /* The screen is up and its own poll timer owns the work from here. That is
     * asynchronous progress, not a completed job. */
    return SDK_EX_STARTED;
```

ลำดับที่ต้องจำคือ **ปิดของเก่า → เปิดของใหม่ → คืนค่าว่า "เริ่มแล้ว"** ไม่ใช่ "เสร็จแล้ว"
ค่า `SDK_EX_STARTED` บอกผู้เรียกตรง ๆ ว่างานยังวิ่งอยู่ และเจ้าของงานตั้งแต่นี้คือ timer ของหน้าจอ ไม่ใช่ฟังก์ชันนี้

## ฝึกเติม

หน้าจอของคุณมีปุ่ม "ลงทะเบียน" และมี timer ของหน้าเองชื่อ `s_clock_timer` เติมช่องว่างให้ถูกลำดับ (โค้ดเขียนขึ้นใหม่สำหรับบทเรียนนี้ ใช้ API ของ SDK และ LVGL 9)

```c
static lv_timer_t *s_clock_timer;

static void enrol_btn_cb(lv_event_t *e)
{
    (void)e;
    ____(1)____();          /* ก่อนเปิดอะไรทุกครั้ง */
    ____(2)____();          /* เปิดหน้าต่าง Enrol งานจริงวิ่งที่ CM33_NS */
    /* ไม่มีการรอผลในฟังก์ชันนี้ */
}

void my_page_destroy(void)
{
    if (s_clock_timer != NULL) {
        ____(3)____(s_clock_timer);   /* ลบ timer ของหน้าเอง */
        s_clock_timer = NULL;
    }
    ____(4)____();          /* ปิดหน้าต่างลงทะเบียนและ timer ที่ถามสถานะ เป็นคำสั่งสุดท้าย */
}
```

<details><summary>เฉลย</summary>

1. `hsm_provision_ui_teardown` เรียกซ้ำได้และปลอดภัยแม้ไม่มีหน้าต่างเปิดอยู่
2. `hsm_enrol_open`
3. `lv_timer_delete` (ชื่อใน LVGL 9 ที่ `page_hsm_destroy()` ในบท D2 ใช้)
4. `hsm_provision_ui_teardown` อยู่ท้ายสุด ตามแบบของ `page_hsm_destroy()` เพื่อไม่ให้ timer ใดยิงใส่วัตถุที่ถูกลบไปแล้ว

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ถ้าหน้าจอ Enrol รอผลของชิปแบบ inline ใน task ของ LVGL ผลที่คนถือบอร์ดเห็นคืออะไร *(เป้าหมายข้อ 1)*
   - ก) จอแสดงความคืบหน้าทีละขั้นตามปกติ
   - ข) จอค้างทั้งจอ และหน้าต่างที่อธิบายว่าทำไมค้างก็วาดไม่ได้ จอจึงทั้งตายและเงียบ
   - ค) ชิปทำงานเร็วขึ้น
   - ง) การลงทะเบียนถูกยกเลิกอัตโนมัติ

   <details><summary>เฉลย</summary>

   **ข** นี่คือเหตุผลที่ `IPC_CMD_HSM_PROVISION` คืนทันที และ `lv_timer` ถามสถานะเป็นระยะ

   </details>

2. ลำดับใดถูกต้องเมื่อผู้ใช้แตะปุ่มเปิดหน้าจอลงทะเบียน *(เป้าหมายข้อ 2)*
   - ก) `hsm_enrol_open()` แล้วค่อย `hsm_provision_ui_teardown()`
   - ข) `hsm_provision_ui_teardown()` แล้ว `hsm_enrol_open()` แล้วคืนค่าว่าเริ่มแล้ว
   - ค) `hsm_enrol_open()` แล้วรอจนเสร็จ
   - ง) ไม่ต้องปิดของเก่า เพราะ LVGL จัดการเอง

   <details><summary>เฉลย</summary>

   **ข** ถ้ายังมีหน้าต่างเก่า การเปิดใหม่ถูกปฏิเสธเงียบ ๆ ตามคอมเมนต์ของตัวอย่าง

   </details>

3. ทำไม `hsm_provision_ui_teardown()` ต้องเป็นคำสั่งสุดท้ายใน callback ที่ทำลายหน้า *(เป้าหมายข้อ 2)*
   - ก) เพื่อให้ timer ที่ถามสถานะถูกยกเลิก ไม่ยิงใส่วัตถุ LVGL ที่ถูกคืนหน่วยความจำแล้ว
   - ข) เพราะมันช้าที่สุด
   - ค) เพื่อให้การลงทะเบียนเริ่มใหม่
   - ง) เพราะมันล้าง correlation id

   <details><summary>เฉลย</summary>

   **ก** บท D2 ให้เหตุผลว่า timer ที่ยิงหลังวัตถุถูกคืนจะอ้างถึงหน่วยความจำที่ไม่มีแล้ว

   </details>

## แล็บ

**ดูหน้าจอถามสถานะจริง โดยไม่ลงทะเบียนจริง**

- [ ] **ตั้งบอร์ดให้ปลอดภัยก่อน** ลบหรือเว้นว่าง `device_id` กับ `mqtt_pass` ในไฟล์ `/.tesaiot_config` (บทเรียน 3.2) เก็บค่าจริงไว้ที่อื่นที่ไม่ใช่ repository
  บท D2 ระบุว่าการลงทะเบียนเชื่อมต่อแพลตฟอร์ม **ก่อน** สร้างกุญแจ ถ้าต่อไม่ได้ มันหยุดที่ขั้นนั้นโดยยังไม่ได้สร้างกุญแจ (ข้อความที่ D2 บันทึกไว้สำหรับกรณีไม่มีคำตอบคือ "No answer from the platform after 30 seconds.")
- [ ] build ด้วย `ENABLE_PAGE_EXAMPLES=1` flash แล้วถอดสาย USB นับสิบ เสียบใหม่ เปิดการ์ด SDK Examples บนจอ เลือก `cm55/security/01_hsm_screens` แล้ว Run
- [ ] หน้าต่าง Enrol เปิดขึ้น จดทุกข้อความที่ขึ้นตามลำดับพร้อมเวลาโดยประมาณ ระหว่างรอให้ลองแตะปุ่ม Back และจดว่าจอตอบสนองช่วงไหน และไม่ตอบสนองช่วงไหน (มองหาข้อความเหตุผลของ touch-hold)
- [ ] กด Back แล้ว Run ซ้ำ จะได้หน้าต่าง Protect จดสิ่งที่หน้านี้แสดง **ก่อน** ให้ยืนยัน แล้วกด Back **โดยไม่ยืนยัน**
- [ ] อ่าน log ของตัวอย่างบนหน้า SDK Examples หลังกด Back ข้อความ `each step polls, none of it blocks this task` สอดคล้องกับที่คุณสังเกตไหม
- [ ] วาดตาราง state × step ของหน้าจอลงทะเบียนสำหรับงานของคุณเอง (ใช้ step หกค่าของบท D2) และเขียนประโยคที่จอควรแสดงในแต่ละช่อง โดยเฉพาะช่อง FAILED ให้บอกว่าอะไร **ไม่** ถูกเปลี่ยน
- [ ] คืนค่า `device_id` กับ `mqtt_pass` ในไฟล์ตั้งค่า แล้วเชื่อมต่อแพลตฟอร์มอีกครั้งตามบทเรียน 3.2 เพื่อเตรียมงานปลายทาง

## ไปต่อ

ตอนนี้เรามีครบทุกชิ้นแล้ว threat model ช่องทาง mTLS ห่วงโซ่การบูต Protected Update การลงทะเบียน และหน้าจอที่พูดความจริง
บทสุดท้ายรวมทั้งหมดเป็นอุปกรณ์หนึ่งชิ้น พร้อมหลักฐานว่ามันทำงานจริง

บทเรียนถัดไป: [บทเรียน 5.3: งานปลายทาง อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น](../l03-capstone-secure-device/README.md)

## สะท้อนคิด

- ในผลิตภัณฑ์ของคุณ มีงานไหนที่ใช้เวลาเกินหนึ่งวินาทีแต่ยังรออยู่ใน task ที่วาดจอ
- ข้อความ error บนจอของคุณบอกหรือเปล่าว่าอะไร **ไม่ได้** ถูกเปลี่ยน
- ถ้าผู้ใช้แตะปุ่มซ้ำสองครั้งเร็ว ๆ ระบบของคุณทำอะไร และคุณทดสอบกรณีนั้นแล้วหรือยัง

## แหล่งอ้างอิง

- [SDK: cm55/security/01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c)
- [SDK: เอกสาร hsm_provision_ui.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/cm55_core/hsm_provision_ui.md)
- [Security / HSM: Tutorials (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security__tut.html)
- [D1 — The chip-access discipline: gate, lock, touch-hold (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
