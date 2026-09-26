---
id: sec-iot.m05.l01
lang: th
title: {th: ลงทะเบียนด้วย CSR, en: Enrolment with a CSR}
summary: {th: สร้างคำขอใบรับรองจากกุญแจในชิป ส่งให้แพลตฟอร์ม และติดตามคำขอจนได้ใบรับรอง, en: 'Create a certificate request from the on-chip key, send it to the platform and track it to a certificate.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m04.l02]
objectives:
- {th: อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป, en: Explain what a CSR contains and why the private key never leaves the chip.}
- {th: ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK, en: Track a request by correlation id and target OIDs as the SDK example does.}
- {th: ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก, en: State the buffer contract the CSR publishing function imposes on its caller.}
develops:
- {skill: sec.crypto, to: 3}
- {skill: sec.secure-element, to: 3}
- {skill: iot.cloud-platform, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
---

# บทเรียน 5.1: ลงทะเบียนด้วย CSR

> โมดูล 5 · การลงทะเบียนอุปกรณ์อย่างปลอดภัย · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

อุปกรณ์ออกจากโรงงานพร้อมใบรับรองของ Infineon ซึ่งบอกได้แค่ว่าเป็น Trust M ของแท้ (บทเรียน 3.1)
การลงทะเบียนคือการได้ใบรับรองที่ **แพลตฟอร์มของเรา** ออกให้ ผูกกับ `device_id` ของอุปกรณ์เครื่องนั้น โดยที่กุญแจลับไม่เคยออกจากชิปเลยสักครั้ง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป
2. ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK
3. ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 4.2: Protected Update](../../m04-secure-boot-and-update/l02-protected-update/README.md) และเรื่องใบรับรองใน [บทเรียน 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **บนคอมพิวเตอร์:** `openssl` และไฟล์ `lab_key.pem` ที่สร้างใหม่ได้ตามแล็บ 1.2 ข้อ 5
- **บนบอร์ด:** แม่แบบของ SDK ที่ build ได้ แล็บเสริมที่ลงทะเบียนจริงต้องมีอุปกรณ์ที่เชื่อมต่อแพลตฟอร์มได้แล้ว (บทเรียน 3.2) และได้รับอนุญาตจากผู้สอน
- **อ่านคู่กัน:** [บทเรียน 5.3 ของ TESAIoT Firmware Stack: PSoC Edge E84 กับ OPTIGA™ Trust M](../../../tesaiot-firmware-stack/m05-connect-to-platform/l03-optiga-mqtt-client/README.md)

## ดูของจริงก่อน

เมื่อกด HSM Security → Enrol Certificate บนจอ บท [D2 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html) บอกว่าจอจะขึ้นเจ็ดประโยคนี้ตามลำดับ

```text
Connecting to the platform
Generating a key pair inside the secure element
Signing the request with the key that never leaves the chip
Sending the request to the platform
Waiting for the platform
Checking the certificate against the key in the chip
The device can prove it holds the key this certificate names
```

**ทายก่อน:** ประโยคที่สามบอกว่ามีการ "ลงนามคำขอ" ถ้าคำขอมีกุญแจสาธารณะอยู่แล้ว ทำไมยังต้องลงนามอีก และใครเป็นคนตรวจลายเซ็นนั้น

## แนวคิด

### 1. CSR คืออะไร และทำไมกุญแจลับไม่ต้องออกจากชิป

CSR (certificate signing request) ตาม [RFC 2986 (PKCS #10)](https://www.rfc-editor.org/rfc/rfc2986) มีสามส่วนหลัก
**subject** ชื่อที่ขอให้ใส่ในใบ **กุญแจสาธารณะ** ที่ขอให้รับรอง และ **ลายเซ็น** ที่ผู้ขอลงบนสองส่วนแรกด้วยกุญแจลับคู่กัน

คำตอบของคำทายอยู่ที่ลายเซ็นนี้ มันคือ **proof of possession** ผู้ออกใบตรวจลายเซ็นด้วยกุญแจสาธารณะในคำขอ ถ้าผ่าน แปลว่าผู้ขอถือกุญแจลับของคู่นั้นจริง
ผู้ออกใบจึงไม่เคยต้องเห็นกุญแจลับเลย ใบที่ออกมาคือ subject กับกุญแจสาธารณะเดิม บวก issuer และช่วงเวลา แล้วลงนามโดย CA

บนบอร์ดของเรา บท D2 ระบุว่า subject เป็น `CN=<mqtt username>,O=TESAIoT` คู่กุญแจถูกสร้าง **ในชิป** แล้วคำขอถูกลงนามด้วยกุญแจที่ไม่ออกจากชิป
ขั้นตอนเต็มตามคอมเมนต์หัวไฟล์ [05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c)

1. อุปกรณ์สร้างคู่กุญแจในชิป แล้วสร้าง CSR แบบ PEM จากกุญแจสาธารณะ (ส่วนนี้เป็นงานของ consumer ตามรายการ `consumer_must_provide.txt`)
2. `publish_csr()` ห่อ CSR เป็น JSON แล้ว publish ไปที่ `device/<id>/commands/csr` บน session MQTT ที่เปิดอยู่
3. แพลตฟอร์มลงนามและตอบกลับบนอีกหัวข้อหนึ่ง ตามสัญญา PU ของ SDK คือ `commands/certificate` โดยตรง ไม่มี manifest
4. subscriber ของอุปกรณ์รับใบรับรองแล้วเขียนลงช่อง จากนั้นตรวจว่าใบเข้าคู่กับกุญแจในชิป (`optiga_verify_cert_key_pair`)

[CSR_SUBMISSION_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md) ของ SDK ให้กฎที่ "เคยทำให้ใครสักคนเสียเวลา debug มาแล้ว" ไว้ที่หัวเอกสาร

- **หัวข้อใช้ `device_id` (UUID) เสมอ ไม่ใช่ UID ของ Trust M** UID เป็น client id ของ MQTT ถ้าใช้ในหัวข้อ broker จะปฏิเสธขณะที่การเชื่อมต่อยังค้าง ข้อความจึงดูเหมือนหายไปเฉย ๆ
- **subscribe `device/<id>/commands/#` ก่อน publish CSR** คำตอบไม่ถูก retain คำตอบที่มาก่อน subscription สำเร็จหายไปเลย
- **ต้องมีคนดูแล session** ไม่มี PINGREQ broker ปิด session ที่ 90 วินาที คำตอบที่มาทีหลังก็หาย
- **CSR ที่ถูกปฏิเสธเงียบ** ไม่มีอะไรตอบกลับบนหัวข้อ เหตุผลอยู่ใน log ของแพลตฟอร์ม และ CSR ต้องยาวกว่า 100 ไบต์
- มีอีกทางคือ HTTPS สำหรับผู้ดูแลหรือระบบหลังบ้านที่ถือ JWT แต่อุปกรณ์ที่ใช้ใบจากโรงงานอยู่ใช้ทาง MQTT

### 2. ติดตามคำขอด้วย correlation id และ OID

`05_csr_enrolment.c` อธิบายตัวอ่านสามตัว และ **กับดักในสองตัว**

- `trustm_current_correlation_id()` คือ id ใหม่ที่ `publish_csr()` สร้างจาก TRNG ทุกครั้งที่เรียก คำตอบของแพลตฟอร์มถูกจับคู่กับ id นี้ `NULL` แปลว่าไม่มีอะไรค้างอยู่
- `trustm_requested_target_oid()` และ `trustm_requested_anchor_oid()` คือคู่ OID ที่คำขอ **Protected Update** ครั้งล่าสุดระบุ
  `publish_csr()` **ไม่ได้ตั้งค่าสองตัวนี้** มันถูกเขียนโดย `tesaiot_publish_protected_update()` เท่านั้น และอ่านได้ `0xE0E1` / `0xE0E8` หลังรีเซ็ต
  หลังเรียก `publish_csr()` อย่างเดียว สองค่านี้จึงบอกเรื่องของคำขอ PU ครั้งก่อนหรือค่าเริ่มต้น ไม่เคยบอกเรื่อง CSR นี้ อย่าใช้ติดป้ายการลงทะเบียนแบบ CSR อย่างเดียว

กติกาของการรีเซ็ต `trustm_reset_state()` **ล้าง correlation id** ถ้าเรียกตอนคำตอบยังไม่มา ใบรับรองที่มาถึงจะไม่มีอะไรให้จับคู่ และถูกทิ้งโดยไม่มีใครอ่าน
ให้รีเซ็ตเมื่อเสร็จ หรือเมื่อหมดเวลาที่ **คุณ** ตัดสินใจเอง ไม่ใช่ "เพื่อความสะอาด" และถ้าจะรอผลด้วยตัวนับ ให้เก็บค่าตัวนับ **ก่อน** publish ตามกับดักข้อ 4 ของบท D2
ไม่อย่างนั้นงานที่จบก่อนหน้าจะถูกนับเป็นคำตอบของคำขอนี้

บท D2 เตือนอีกข้อ `trustm_state_t` เป็นแค่ตัวแปรที่มีเวลาประทับ ไม่ใช่ state machine ไม่มี `switch` ที่ขับเคลื่อนจากมัน
และมีสี่ค่าที่ไม่มีใครเขียนในเส้นทางปกติ (`APPLYING_UPDATE`, `WAITING_FOR_CERTIFICATE`, `COMPLETE`, `APPLYING_FRAGMENTS`) หน้าจอที่รอ `COMPLETE` จะรอตลอดไป

### 3. สัญญาเรื่องบัฟเฟอร์ของ `publish_csr()`

ลายเซ็นของฟังก์ชันตาม [เอกสาร tesaiot_hsm_api](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/tesaiot_hsm_api.md) คือ

```c
int publish_csr(uint8_t *csr, size_t csr_length, uint16_t target_oid, uint16_t trust_anchor_oid, uint32_t payload_version);
```

พารามิเตอร์แรกเป็น `uint8_t *` ไม่ใช่ `const uint8_t *` และตัวอย่าง 05 บอกว่านี่ไม่ใช่การพิมพ์ตก `publish_csr()` **สร้าง JSON ทับลงในบัฟเฟอร์ของคุณ** เพื่อไม่ต้องจองหน่วยความจำก้อนใหญ่ก้อนที่สอง ผลคือ

1. บัฟเฟอร์ต้อง **เขียนได้** สตริง PEM แบบ `const` ที่อยู่ใน flash ทำให้ fault
2. บัฟเฟอร์ต้อง **ใหญ่กว่า CSR** ต้องจุ `{"device_id":"<id>","csr":"<CSR ที่ escape \n แล้ว>","correlation_id":"<uuid>"}`
   คือ CSR บวกหนึ่งไบต์ต่อการขึ้นบรรทัด บวกข้อความคงที่ราว 45 ไบต์ บวก device id และ correlation id ตัวอย่างแนะนำให้เผื่อ 256 ไบต์แล้วไม่ต้องคิดอีก
3. `csr_length` คือ **ความยาวของ CSR** ไม่ใช่ขนาดบัฟเฟอร์
4. **CSR ของคุณหายไปเมื่อฟังก์ชันคืนค่า** บัฟเฟอร์กลายเป็น JSON แล้ว ถ้าต้องใช้ CSR อีกให้เก็บสำเนาไว้ก่อน

`trust_anchor_oid` กับ `payload_version` ถูกรับไว้แต่ยังไม่ถูกใช้ (สงวนไว้) ตัวอย่างแนะนำให้ส่งค่าที่ตั้งใจจริงอยู่ดี เพื่อให้โค้ดยังถูกเมื่อวันหนึ่งมันเริ่มมีผล

## ตัวอย่างสมบูรณ์

ตัดจาก [05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c) บรรทัด 158–172 และ 178–184
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* Refuse rather than publish a fabricated CSR. A CSR the platform signs is
     * a certificate on a real device; the wrong one is worse than none. */
    if (s_csr_len == 0u) {
        printf("  publish_csr() NOT called: s_csr is empty. Build a CSR first —\r\n"
               "    generate the keypair in the chip, then produce the PEM. The\r\n"
               "    archive cannot do this for you (optiga_generate_csr_pem is\r\n"
               "    in consumer_must_provide.txt).\r\n");
        return SDK_EX_NO_DATA;
    }
    if (s_csr_len + 256u > sizeof(s_csr)) {
        printf("  publish_csr() NOT called: %u-byte CSR in a %u-byte buffer "
               "leaves no room for the JSON envelope built in place\r\n",
               (unsigned)s_csr_len, (unsigned)sizeof(s_csr));
        return SDK_EX_REFUSED;
    }
```

```c
    int rc = publish_csr(s_csr, s_csr_len,
                         (uint16_t)EXAMPLE_TARGET_OID,
                         (uint16_t)EXAMPLE_ANCHOR_OID,
                         (uint32_t)EXAMPLE_PAYLOAD_VER);

    /* s_csr now holds the JSON envelope, not the CSR. Do not reuse it as a CSR. */
    s_csr_len = 0u;
```

สามจุดที่ควรลอกไปใช้

1. **ไม่ส่ง CSR ปลอม** CSR ที่แพลตฟอร์มลงนามคือใบรับรองบนอุปกรณ์จริง ใบผิดแย่กว่าไม่มีใบ
2. **ตรวจที่ว่างก่อนเรียก** ด้วยกฎ CSR + 256 ไบต์ ตัวอย่างใช้บัฟเฟอร์ `static` ขนาด 1280 ไบต์
3. **ทำให้ความยาวเป็นศูนย์ทันทีหลังเรียก** เพื่อไม่ให้ใครเอาบัฟเฟอร์ที่เป็น JSON แล้วไปใช้เป็น CSR อีก

ตัวอย่างนี้ **ปิดการ publish ไว้เป็นค่าเริ่มต้น** ต้องมี session MQTT ที่เชื่อมต่อแพลตฟอร์มจริง และ CSR จริงที่สร้างจากกุญแจในชิป จึงจะเปิด `DEFINES+=EXAMPLE_HSM_PUBLISH_CSR=1`
คอมเมนต์บอกเหตุผลว่าคำขอที่ไม่มีทั้งสองอย่างเป็นแค่เสียงรบกวนบน broker ของคนอื่น

## ฝึกเติม

ใช้กฎของตัวอย่าง 05 ตัดสินแต่ละกรณีว่า **เรียก `publish_csr()` ได้** หรือ **ต้องแก้ก่อน** และแก้อย่างไร

1. `static uint8_t buf[1280];` เก็บ CSR ยาว 620 ไบต์ แล้วเรียก `publish_csr(buf, 620, 0xE0E1, 0xE0E8, 1)` ____
2. `static const char csr[] = "-----BEGIN CERTIFICATE REQUEST-----\n...";` แล้วเรียก `publish_csr((uint8_t *)csr, strlen(csr), ...)` ____
3. `static uint8_t buf[700];` เก็บ CSR ยาว 620 ไบต์ ____
4. `publish_csr(buf, sizeof(buf), 0xE0E1, 0xE0E8, 1)` โดย `buf` มี CSR ยาว 620 ไบต์ ____
5. หลัง `publish_csr()` คืน `0` โปรแกรมพิมพ์ `buf` ออกมาเพื่อ "ดู CSR ที่ส่งไป" ____
6. คำตอบยังไม่มา แต่โปรแกรมเรียก `trustm_reset_state()` เพื่อเริ่มสถานะใหม่ให้สะอาด ____

<details><summary>เฉลย</summary>

1. **เรียกได้** 620 + 256 = 876 ไม่เกิน 1280
2. **ต้องแก้** บัฟเฟอร์ `const` อยู่ใน flash เขียนไม่ได้ `publish_csr()` จะ fault ตอนสร้าง JSON ทับ ให้คัดลอกไปบัฟเฟอร์ที่เขียนได้ก่อน
3. **ต้องแก้** 620 + 256 = 876 เกิน 700 ไม่มีที่ให้ JSON ที่สร้างทับ
4. **ต้องแก้** `csr_length` ต้องเป็น 620 ไม่ใช่ขนาดบัฟเฟอร์
5. **ต้องแก้** ถึงตอนนั้น `buf` เป็น JSON ไปแล้ว ถ้าอยากเก็บ CSR ต้องคัดลอกไว้ก่อนเรียก
6. **ต้องแก้** การรีเซ็ตล้าง correlation id ใบรับรองที่มาถึงทีหลังจะถูกทิ้ง ให้รอจนเสร็จหรือจนหมดเวลาที่ตั้งใจไว้

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ทำไมแพลตฟอร์มออกใบรับรองให้ได้โดยไม่ต้องเห็นกุญแจลับของอุปกรณ์ *(เป้าหมายข้อ 1)*
   - ก) เพราะแพลตฟอร์มเดากุญแจลับจากกุญแจสาธารณะได้
   - ข) เพราะ CSR มีกุญแจสาธารณะ และลายเซ็นบน CSR พิสูจน์ว่าผู้ขอถือกุญแจลับคู่นั้น
   - ค) เพราะกุญแจลับถูกส่งไปแบบเข้ารหัส
   - ง) เพราะใบรับรองไม่เกี่ยวกับกุญแจ

   <details><summary>เฉลย</summary>

   **ข** นี่คือ proof of possession ใบที่ออกมาใส่กุญแจสาธารณะเดิม กุญแจลับจึงอยู่ในชิปต่อไป

   </details>

2. หลังเรียก `publish_csr()` อย่างเดียว `trustm_requested_target_oid()` บอกอะไร *(เป้าหมายข้อ 2)*
   - ก) ช่องที่ใบรับรองจาก CSR นี้จะถูกเขียน
   - ข) OID ของคำขอ Protected Update ครั้งก่อน หรือค่าเริ่มต้น `0xE0E1` ไม่ได้บอกเรื่อง CSR นี้
   - ค) UID ของชิป
   - ง) correlation id

   <details><summary>เฉลย</summary>

   **ข** ค่านี้ถูกเขียนโดย `tesaiot_publish_protected_update()` เท่านั้น ตัวติดตาม CSR คือ correlation id

   </details>

3. ข้อใดเป็นสัญญาเรื่องบัฟเฟอร์ของ `publish_csr()` *(เป้าหมายข้อ 3)*
   - ก) บัฟเฟอร์เป็น `const` ได้ และ `csr_length` คือขนาดบัฟเฟอร์
   - ข) บัฟเฟอร์ต้องเขียนได้ ใหญ่กว่า CSR พอให้ JSON ที่สร้างทับ `csr_length` คือความยาว CSR และ CSR หายไปหลังเรียก
   - ค) ฟังก์ชันจองบัฟเฟอร์ใหม่ให้เอง
   - ง) ต้องส่ง CSR แบบ DER เท่านั้น

   <details><summary>เฉลย</summary>

   **ข** ตัวอย่าง 05 เขียนไว้เป็นสี่ข้อ และแนะนำให้เผื่อ 256 ไบต์

   </details>

## แล็บ

**แล็บหลัก: ติดตามคำขอโดยไม่ส่งจริง และอ่าน CSR ด้วยตา**

- [ ] build ตัวอย่าง 05 โดยไม่เปิดการ publish
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/05_csr_enrolment
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  จดบรรทัด `correlation id on entry`, `requested target OID`, `requested anchor OID`, บรรทัดของ `trustm_update_state` และ `trustm_reset_state` แล้วข้อความ `SKIPPED publish_csr()`
  อธิบายว่าทำไมตัวอย่างกล้าเรียก `trustm_reset_state()` ตรงนั้น (ดูเงื่อนไขก่อนหน้า)
- [ ] สร้าง CSR บนคอมพิวเตอร์จากกุญแจทดลองของบทเรียน 1.2 ใช้ UUID ปลอมที่เห็นชัดว่าปลอม แล้วอ่านทุกส่วน
  ```bash
  openssl ecparam -name prime256v1 -genkey -noout -out lab_key.pem
  openssl req -new -key lab_key.pem -subj "/CN=00000000-0000-0000-0000-000000000000/O=TESAIoT" -out lab.csr
  openssl req -in lab.csr -noout -text
  openssl req -in lab.csr -noout -verify
  ```
  หา subject กุญแจสาธารณะ และอัลกอริทึมลายเซ็นในผลลัพธ์ บรรทัดสุดท้ายต้องบอกว่า self-signature verify OK นี่คือ proof of possession ที่ CA ตรวจ
- [ ] นับขนาด `wc -c < lab.csr` และจำนวนบรรทัด `grep -c '' lab.csr` แล้วคำนวณว่าบัฟเฟอร์ของ `publish_csr()` ต้องใหญ่อย่างน้อยเท่าไรตามสูตรของตัวอย่าง 05 เทียบกับกฎ +256 ไบต์ แล้วลบไฟล์กุญแจทดลองทิ้ง
- [ ] วาดแผนภาพลำดับของการลงทะเบียน แสดงหัวข้อ MQTT ทุกหัวข้อที่เกี่ยว (`commands/#`, `commands/csr`, `commands/certificate`) จุดที่ proof of possession ถูกตรวจ และจุดที่อุปกรณ์ตรวจว่าใบเข้าคู่กับกุญแจ

**แล็บเสริม: ลงทะเบียนจริง ทำเมื่อผู้สอนอนุญาตเท่านั้น**

การลงทะเบียนสร้างคู่กุญแจใหม่ในชิป กุญแจเดิมในช่องนั้นหายไปถาวร และเขียนใบรับรองใหม่ลงช่อง `0xE0E1` ด้วยการเขียนธรรมดา ถ้าช่องถูกล็อกโดย Protected Update ไว้ ปุ่มจะปฏิเสธก่อนทำอะไร

- [ ] อุปกรณ์เชื่อมต่อแพลตฟอร์มได้ในโหมดที่ใช้อยู่ (บทเรียน 3.2) กด HSM Security → Enrol Certificate แล้วจดประโยคบนจอทั้งเจ็ดเทียบกับ "ดูของจริงก่อน"
- [ ] จดบรรทัด `[CSR] Using DIRECT PUBLISH ...` และ `[Subscriber] Certificate from platform (N bytes)` บน UART ตามบท D2
- [ ] เปลี่ยน `tls_mode=mtls` แล้วเชื่อมต่อใหม่ มองหาบรรทัด `[mTLS] device pair verified — using TESAIoT identity` ในบทเรียน 3.1 ซึ่งแปลว่าเฟิร์มแวร์เลือกใช้ใบและกุญแจที่คุณเพิ่งลงทะเบียน

## ไปต่อ

การลงทะเบียนใช้เวลาหลายวินาทีและต้องรอแพลตฟอร์มได้ถึงหนึ่งนาที บทต่อไปดูว่าหน้าจอบนอุปกรณ์รับมือกับงานยาวแบบนี้อย่างไรโดยไม่ค้างและไม่เงียบ

บทเรียนถัดไป: [บทเรียน 5.2: หน้าจอลงทะเบียนบนอุปกรณ์](../l02-provisioning-screens/README.md)

## สะท้อนคิด

- ในระบบของคุณ มีที่ไหนที่ "ล้างสถานะให้สะอาด" แล้วทำให้คำตอบที่มาถึงทีหลังถูกทิ้ง
- ถ้า CSR ที่ถูกปฏิเสธไม่มีอะไรตอบกลับเลย ทีมของคุณจะรู้ได้อย่างไร และจะดูหลักฐานจากไหน
- ฟังก์ชันใน API ของคุณมีตัวไหนที่เขียนทับบัฟเฟอร์ของผู้เรียกโดยที่ชื่อหรือชนิดของพารามิเตอร์ไม่ได้บอก

## แหล่งอ้างอิง

- [SDK: cm33/security/05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c)
- [SDK: CSR_SUBMISSION_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- [SDK: PROTECTED_UPDATE_CONTRACT.md ข้อ 4.3 (ใบรับรองจากเส้นทาง CSR)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/PROTECTED_UPDATE_CONTRACT.md)
- [SDK: เอกสาร tesaiot_hsm_api](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/tesaiot_hsm_api.md)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [RFC 2986: PKCS #10 Certification Request Syntax](https://www.rfc-editor.org/rfc/rfc2986)
- ตัวอย่างบน Developer Hub: [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) ซึ่ง README ระบุว่า bundle จากการลงทะเบียนด้วย CSR ไม่มีกุญแจลับ
