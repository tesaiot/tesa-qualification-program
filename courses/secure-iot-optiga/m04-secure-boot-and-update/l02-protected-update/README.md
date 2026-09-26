---
id: sec-iot.m04.l02
lang: th
title: {th: Protected Update, en: Protected Update}
summary: {th: ขออัปเดตแบบป้องกันจากแพลตฟอร์ม เข้าใจตัวนับกันย้อนรุ่น และการเปลี่ยนแปลงบนชิปที่ย้อนกลับไม่ได้, en: 'Request a protected update from the platform, and understand the anti-rollback counter and irreversible chip changes.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m04.l01]
objectives:
- {th: อธิบายขั้นตอนของ Protected Update ตั้งแต่คำขอจนถึงการตรวจ manifest, en: Explain Protected Update from request to manifest verification.}
- {th: อธิบายหน้าที่ของตัวนับกันย้อนรุ่น และผลของ manifest lock, en: Explain the anti-rollback counter and the effect of a manifest lock.}
- {th: ระบุการเปลี่ยนแปลงบนชิปที่รีแฟลชแล้วก็กู้คืนไม่ได้ ตามที่ตัวอย่างของ SDK เตือนไว้, en: 'Identify the chip change that no reflash can undo, as the SDK example warns.'}
develops:
- {skill: sec.secure-boot, to: 3}
- {skill: iot.ota, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/tesaiot/developer-hub', path: examples/embedded-devices/advanced/c_ota_client, ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/optiga-trust-m', path: examples/tools/protected_update_data_set/README.md, ref: release-v5.3.0, license: MIT}
---

# บทเรียน 4.2: Protected Update

> โมดูล 4 · Secure boot และ Protected Update · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ใบรับรองของอุปกรณ์ต้องเปลี่ยนได้ตลอดอายุการใช้งาน แต่ถ้าใครก็เขียนช่องใบรับรองได้ ผู้โจมตีก็เขียนได้เหมือนกัน
Protected Update ของ OPTIGA™ Trust M แก้ปัญหานี้ด้วยการให้ **ชิปเป็นคนตรวจลายเซ็น** ก่อนยอมเขียน host ที่ถูกเจาะจึงปลอมการอัปเดตไม่ได้

ต้องแยกให้ชัดตั้งแต่ต้น Protected Update ในบทนี้คือการอัปเดต **object ในชิป** (ใบรับรอง กุญแจ ข้อมูล metadata) ไม่ใช่การอัปเดตเฟิร์มแวร์ของ MCU
เรื่องเฟิร์มแวร์เราจะเทียบกันตอนท้ายบทด้วยตัวอย่าง OTA บน Developer Hub

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายขั้นตอนของ Protected Update ตั้งแต่คำขอจนถึงการตรวจ manifest
2. อธิบายหน้าที่ของตัวนับกันย้อนรุ่น และผลของ manifest lock
3. ระบุการเปลี่ยนแปลงบนชิปที่รีแฟลชแล้วก็กู้คืนไม่ได้ ตามที่ตัวอย่างของ SDK เตือนไว้

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 4.1: Secure boot และ chain of trust](../l01-secure-boot/README.md) และตาราง metadata ใน [บทเรียน 2.1](../../m02-optiga-trust-m/l01-secure-element-role/README.md) (tag `C0` `C1` `D0`)
- **บอร์ด:** แม่แบบของ SDK ที่ build ได้ แล็บหลักไม่ส่งคำขอจริง ส่วนแล็บเสริมที่ส่งคำขอจริงต้องมีอุปกรณ์ที่ลงทะเบียนและเชื่อมต่อแพลตฟอร์มได้แล้ว และต้องได้รับอนุญาตจากผู้สอน
- **อ่านคู่กัน:** [บทเรียน 5.4 ของ TESAIoT Firmware Stack: อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client](../../../tesaiot-firmware-stack/m05-connect-to-platform/l04-ota-client/README.md)

## ดูของจริงก่อน

บท [D2 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html) ให้ลำดับบรรทัดบน UART เมื่อกด Protected Update บนจอแล้วสำเร็จ

```text
[Subscriber] Protected Update bundle (%d bytes)
[PU-Ingest] Fragment count: %u
[PU-Ingest] OPTIGA acquired: OK
[PU-Ingest] STEP 3: Processing fragments...
[PU-Ingest] STEP 4: Executing OPTIGA Trust M Protected Update
[PU-Ingest] [4.1] Manifest verification OK (Trust Anchor signature valid)
[PU-Ingest] PROTECTED UPDATE COMPLETED SUCCESSFULLY!
[PU-Ingest] [ACK] Certificate ACK published successfully
```

**ทายก่อน:** ถ้า host ถูกเจาะ ผู้โจมตีพิมพ์บรรทัดไหนในนี้ปลอมได้บ้าง และอะไรคือหลักฐานที่เขา **ปลอมไม่ได้**

## แนวคิด

### 1. จากคำขอถึงการตรวจ manifest ในชิป

[PROTECTED_UPDATE_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/PROTECTED_UPDATE_CONTRACT.md) ของ SDK อธิบายว่า
OPTIGA™ Trust M ไม่รับใบรับรองที่เขียนเป็นไบต์ธรรมดาลงช่องที่ถูกป้องกัน ต้องมี **manifest** ที่ลงนามด้วยกุญแจที่ชิปเชื่ออยู่แล้ว (**trust anchor**)
กับ **fragment** หนึ่งชิ้นขึ้นไปที่บรรจุข้อมูลจริง ชิปตรวจ manifest กับ trust anchor ก่อนเขียนอะไรทั้งสิ้น
manifest เป็น COSE_Sign1 ที่ระบุ OID ของ anchor ไว้ใน header `kid` (สัญญา CSR ข้อ 4.5)

เครื่องมือสร้างชุดข้อมูลของ Infineon ([protected_update_data_set](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/tools/protected_update_data_set/README.md), MIT)
บอกว่าใน manifest มีอะไร `payload_version`, `trust_anchor_oid`, `target_oid`, อัลกอริทึมลายเซ็น (ค่าเริ่มต้น ES_256), ชนิดของ payload (data, key หรือ metadata)
และถ้าต้องการความลับ ก็เข้ารหัส fragment ด้วยกุญแจร่วมที่เก็บในชิปได้

ทั้งเส้นทางบนบอร์ดของเรา สรุปจากบท D2 และสัญญาของ SDK

```text
 อุปกรณ์                                               แพลตฟอร์ม
 1. อ่าน metadata ของ 0xE0E1 เก็บไว้ (C0, D0)
 2. SUBSCRIBE device/<id>/commands/#   ── ก่อนขอเสมอ
 3. tesaiot_publish_protected_update("E0E1","E0E8",ver,with_csr)
      ตรวจในเครื่องก่อน: ถ้าช่องถูกล็อกกับ anchor อื่นอยู่ ปฏิเสธเอง
      PUBLISH device/<id>/commands/request  ─────────▶  สร้าง manifest + fragment
                                                           version = max(ของเรา, ที่เคยใช้) + 1
                                                           ลงนามด้วยกุญแจของแพลตฟอร์ม
      ◀───── commands/protected_update (manifest, fragment_0..n, ใบของผู้ลงนาม)
 4. ตรวจ correlation id: ไม่มีคำขอค้าง = ทิ้ง (กันการเล่นซ้ำ)
 5. เขียนใบของผู้ลงนามลง 0xE0E8 ตั้งชนิดเป็น trust anchor
 6. optiga_util_protected_update_start(manifest)
      ▶ ชิปตรวจลายเซ็นของ manifest กับ 0xE0E8   ◀ จุดที่ host ปลอมไม่ได้
 7. ส่ง fragment ด้วย _continue / _final ชิปเขียนช่องเป้าหมาย
 8. ส่ง ACK แล้ว trustm_reset_state() ล้าง correlation id
 9. อ่าน metadata อีกครั้ง: D0 เปลี่ยนเป็น 21 E0 E8, C0 ยังเป็น 01
```

**คำตอบของคำทาย** ทุกบรรทัดใน log เป็นแค่ `printf` host ที่ถูกเจาะพิมพ์อะไรก็ได้ บท D2 ชี้ว่าเหตุการณ์ที่ปลอมไม่ได้คือ **ชิปตรวจลายเซ็นของแพลตฟอร์มกับ trust anchor ของตัวเองสำเร็จ**
ซึ่งเฟิร์มแวร์รายงานต่อทันทีหลังบรรทัด `[4.1]` แต่ถ้าจะให้เป็นหลักฐานจริง ให้ถามชิปเองด้วยการอ่าน metadata กลับมา (ขั้น 9) ไม่ใช่เชื่อ log

สิ่งที่ `tesaiot_publish_protected_update()` คืน `0` แปลว่า **ขอแล้ว** ไม่ใช่ **เสร็จแล้ว** ตามคอมเมนต์ของตัวอย่าง 06 ชิปยังไม่เปลี่ยนจนกว่า manifest จะมาถึงและถูก apply
OID เป็น **สตริงฐานสิบหก** `"E0E1"` ไม่ใช่ตัวเลข `0xE0E1`

### 2. ตัวนับกันย้อนรุ่น และ manifest lock

**ตัวนับ version (tag `C1`)** ชิปจำ version ของแต่ละ object และปฏิเสธ manifest ที่ version ไม่มากกว่าเดิม ตัวนับขึ้นได้อย่างเดียว
หน้าที่ของมันคือกันการเอา manifest เก่าที่ลงนามถูกต้องมาเล่นซ้ำ เพื่อคืนใบรับรองรุ่นเก่า
สัญญาของ SDK บอกว่าแพลตฟอร์มคำนวณ version ให้เป็น `max(ของเรา, ที่เคยใช้) + 1` อุปกรณ์จึงส่ง `1` ทุกครั้งได้
แต่ตัวอย่าง 06 เตือนว่าถ้า version ที่ใช้จริง **ต่ำกว่า** ตัวนับในชิป ชิปจะปฏิเสธในแบบที่ดูเหมือนลายเซ็นผิด

**manifest lock (tag `D0`)** การ apply สำเร็จตั้งเงื่อนไข Change ของช่องเป้าหมายเป็น `Int(anchor)` หรือ `21 E0 E8`
จากนั้นช่องนั้นรับเฉพาะการเขียนที่มากับ manifest ที่ลงนามโดย anchor นั้น การเขียนธรรมดาถูกปฏิเสธ นี่คือจุดประสงค์ของฟีเจอร์
ผลที่เห็นบนบอร์ดคือ ถ้ากดลงทะเบียน (Enrol) ใส่ช่องที่ถูกล็อก หน้าจอจะขึ้นว่า "This slot takes signed manifests only. Use Protect, or clear the requirement first. Nothing was changed." ก่อนสร้างกุญแจใด ๆ

ล็อกนี้ **กลับทางได้ ตราบที่ LcsO ยังต่ำกว่า op** บท D2 วัดบนบอร์ดจริงว่า `D0` ของ `0xE0E1` อ่านได้ `21 e0 e8` ก่อน และ `e1 fc 07` หลังการเขียนกลับ
บนบอร์ดที่อยู่ในสถานะ creation เมนู HSM Security → Unlock ทำขั้นนี้ แต่ตัวอย่าง 06 บอกว่าฟังก์ชันเคลียร์ล็อกไม่ได้อยู่ใน 18 ฟังก์ชันที่ `libbento_hsm.a` export
คำแนะนำของ SDK จึงเป็น "วางแผนว่าจะไม่ต้องใช้มัน" และเลือกช่องเป้าหมายอย่างตั้งใจ รัน Protected Update ใส่ช่องใบรับรองที่ใช้งานจริง ก็คือล็อกใบรับรองที่ใช้งานจริง

**รหัสผิดพลาดตัวเดียวแปลได้หลายอย่าง** ตัวอย่าง 06 ระบุว่าชิปตอบ `0x800F` ทั้งกรณีช่องถูกล็อกกับ anchor อื่น และกรณี version เก่า
สัญญา PU ของ SDK เพิ่มอีกกรณีที่เจอบ่อยที่สุด คือช่อง trust anchor **ว่าง** (ใบของผู้ลงนามไม่ได้ถูกเขียนลง `0xE0E8`) ก็ได้ `0x800F` เช่นกัน
ดังนั้นเมื่อเห็นรหัสนี้ ให้อ่าน metadata ของช่องเป้าหมายและอ่านข้อมูลของ `0xE0E8` กลับมาก่อน อย่าเพิ่งสรุปว่าลายเซ็นผิด

**กันการเล่นซ้ำด้วย correlation id** ทุกคำขอมี correlation id ถ้า bundle มาถึงตอนที่ไม่มีคำขอค้างอยู่ (`trustm_current_correlation_id()` เป็น `NULL`) เฟิร์มแวร์ต้องทิ้ง
บท D2 บันทึกเหตุการณ์ที่ bundle เก่าถูก apply ซ้ำโดยไม่มีใครขอ ผลคือช่องถูกล็อกซ้ำ และตัวนับถูกใช้ไปหนึ่งขั้น
เอกสารของ SDK สองฉบับอธิบายพฤติกรรมของ broker ต่างกัน (D2 บอกว่ามีการส่ง bundle ล่าสุดซ้ำทุกครั้งที่เชื่อมต่อ สัญญา PU บอกว่าแพลตฟอร์มล้าง retained message ทุกครั้งที่เชื่อมต่อ)
บทเรียนจากความขัดแย้งนี้คือ เฟิร์มแวร์ต้องไม่พึ่งพฤติกรรมของ broker แบบใดแบบหนึ่ง การตรวจ correlation id คือสิ่งที่ป้องกันได้เสมอ

### 3. สิ่งที่รีแฟลชแล้วกู้คืนไม่ได้

ตัวอย่าง [06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c) เปิดไฟล์ด้วยหัวข้อ
"READ THIS BEFORE YOU SET EITHER SWITCH" และแยกสิ่งที่เปลี่ยนไว้สามระดับ

| สิ่งที่เปลี่ยน | ย้อนได้ไหม | ใครทำให้เปลี่ยน |
|---|---|---|
| **LcsO (tag `C0`)** `01 → 03 → 07 → 0F` | **ไม่ได้เลย** ไม่มี reflash การลบ หรือการตัดไฟใดพากลับ เมื่อถึง `op` การเขียน metadata หยุดถาวร | การเขียน metadata ที่มี tag `C0` ไม่มีตัวอย่างใดใน SDK ทำ และ Protected Update ในบทนี้ไม่แตะ |
| **ตัวนับ version (tag `C1`)** ของช่องเป้าหมาย | ไม่ได้ ขึ้นอย่างเดียว | ทุก Protected Update ที่ apply สำเร็จ |
| **manifest lock (tag `D0`)** ของช่องเป้าหมาย | ได้ **เฉพาะเมื่อ LcsO ต่ำกว่า op** บนอุปกรณ์ที่ส่งมอบแล้วถือว่าถาวร | ทุก Protected Update ที่ apply สำเร็จ |

ข้อที่รีแฟลชกู้ไม่ได้ในความหมายตรงตัวคือ **LcsO** ตัวอย่าง 06 บอกว่าการเลื่อนวงจรชีวิตควรอยู่ในเครื่องมือแยกที่ตั้งชื่อชัด รันโดยคนที่ตัดสินใจแล้วว่าจะส่งมอบบอร์ดนั้น
ไม่ใช่ในตัวอย่างที่ใครก็กดรันเพื่อ "ดูว่าเกิดอะไรขึ้น"

อีกฟังก์ชันหนึ่งที่ต้องระวังคือ `tesaiot_run_protected_update_isolated_test()` ตัวอย่าง 06 ระบุว่ามันเป็น **เมนูแบบโต้ตอบ** ที่รอ `scanf()` จาก console และไม่คืนค่าจนกว่าผู้ใช้จะเลือกออก
ห้ามเรียกจาก task ที่ไม่มีคนเฝ้า จากทางบูต หรือจากที่ที่มี watchdog มันเขียน metadata ของ OID สำหรับทดสอบ และอ่าน LcsO มาแสดงแต่ไม่เขียน

**เทียบกับการอัปเดตเฟิร์มแวร์** ETSI EN 303 645 ข้อ 5.3-10 (M) ให้ตรวจความแท้และความถูกต้องของอัปเดตทุกครั้งที่มาทางเครือข่าย ตัวอย่าง [c_ota_client](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client)
อ่าน job document ที่มีฟิลด์ `file_hash` และ `signature` แต่ฟังก์ชันตรวจยังไม่ได้ทำงานจริง (ดูตัวอย่างสมบูรณ์) และถ้าไม่ได้ตั้งไฟล์ CA มันปิดการตรวจใบของเซิร์ฟเวอร์ด้วย
ตัวอย่างนี้เป็นจุดเริ่มที่ดีสำหรับโครงของ OTA แต่ **ห้ามนำไปใช้กับอุปกรณ์จริงโดยไม่เติมการตรวจ**

อีกเส้นทางใน SDK คือการอัปเดตผ่าน BLE ตามหน้า [Firmware update (BLE NUS)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__ble__nus__fw__update.html)
ทุกการ flash ที่สั่งจากเดสก์ท็อปต้องผ่านหน้าจอยืนยัน Y/N บนบอร์ดที่แสดง 8 ตัวแรกของ SHA-256 ของเป้าหมาย ไม่มีทางข้าม และหมดเวลาแล้วไม่ถือว่าตอบ Y
ข้อ 5.3-10 ของ ETSI นับการยืนยันโดยผู้ใช้เป็นความสัมพันธ์เชื่อใจแบบหนึ่ง แต่ต้องรู้ว่าเส้นทางนี้คอมไพล์เฉพาะเมื่อ `ENABLE_PAGE_BENTO_BUDDY=1`
และ README ของตัวอย่างฝั่ง CM33 บอกว่าในแม่แบบที่ส่งมอบ ไลบรารีนี้ยังไม่ได้ถูก link เข้าภาพเฟิร์มแวร์

## ตัวอย่างสมบูรณ์

**คำขอ Protected Update** ตัดจาก [06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c) บรรทัด 110–122 และ 167–173
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
/* Hex strings, as the API takes them. "E0E1" is the TESAIoT device certificate
 * slot and "E0E8" the trust anchor this project pairs with it. Change the
 * target to the isolated test slot if you are only rehearsing. */
#define EXAMPLE_PU_TARGET   "E0E1"
#define EXAMPLE_PU_ANCHOR   "E0E8"

/* The platform takes max(chip counter, its own record, this) + 1, so a value
 * that is merely plausible is fine; a value LOWER than the chip's counter is
 * not, and the chip's refusal will look like a signature failure. */
#define EXAMPLE_PU_VERSION  (1U)

/* false: update the object, do not enrol a new key at the same time. */
#define EXAMPLE_PU_WITH_CSR  false
```

```c
    /* The request. Returns 0 when it was published, -1 when it was not — and
     * -1 also covers the local refusals it makes on your behalf, such as a
     * target already locked to a different anchor. Its own printf says which. */
    int rc = tesaiot_publish_protected_update(EXAMPLE_PU_TARGET,
                                              EXAMPLE_PU_ANCHOR,
                                              (uint32_t)EXAMPLE_PU_VERSION,
                                              EXAMPLE_PU_WITH_CSR);
```

ตัวอย่างนี้ **ปิดไว้เป็นค่าเริ่มต้น** ต้อง build ด้วย `DEFINES+=EXAMPLE_HSM_REQUEST_PU=1` จึงจะส่งคำขอจริง ถ้าไม่เปิด มันพิมพ์แผนของคำขอ (ช่องไหน anchor ไหน version เท่าไร) แล้วบอกว่าข้ามไป
การพิมพ์แผนก่อนทำเป็นความตั้งใจของผู้เขียน เพราะนี่คือคำสั่งเดียวใน SDK ที่ OID เป้าหมายควรถูกอ่านสองรอบก่อนกด

**ฟังก์ชันตรวจเฟิร์มแวร์ใน OTA client** ตัดจาก [ota_client.c](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client/ota_client.c) บรรทัด 375–386
(© 2026 TESAIoT Platform (TESA), Apache-2.0)

```c
ota_error_t ota_verify_firmware(ota_client_t *ctx)
{
    if (!ctx) return OTA_ERR_PARSE;

    ctx->state = OTA_STATE_VERIFYING;
    OTA_LOG("Verifying firmware integrity...");

    /* TODO: Calculate SHA256 hash and compare with ctx->job.file_hash */

    ctx->state = OTA_STATE_IDLE;
    return OTA_OK;
}
```

`ota_run_update_cycle()` ในไฟล์เดียวกันเรียก ดาวน์โหลด → `ota_verify_firmware()` → `apply_firmware` ตามลำดับ ฟังก์ชันตรวจที่คืน `OTA_OK` เสมอ ทำให้ทุกไฟล์ที่ดาวน์โหลดมาถูก apply
เทียบกับบทเรียน 1.2 นี่คือกรณีเดียวกับ hook ตรวจโมเดล AI ฟังก์ชันที่ชื่อว่า "verify" ต้องไม่คืนผ่านถ้ายังไม่ได้ตรวจจริง

## ฝึกเติม

ทำนายผลของแต่ละสถานการณ์ เลือกจาก **(ก)** ขอสำเร็จและชิป apply **(ข)** ถูกปฏิเสธในเครื่องก่อนส่งคำขอ **(ค)** ชิปปฏิเสธตอนตรวจ manifest **(ง)** เฟิร์มแวร์ทิ้ง bundle เพราะไม่มีคำขอค้าง

1. ช่อง `0xE0E1` ถูกล็อกกับ `0xE0E9` อยู่แล้ว แต่คำขอระบุ anchor `"E0E8"` ____
2. bundle ที่ถูกต้องมาถึงหลังรีบูต ตอนที่ `trustm_current_correlation_id()` เป็น `NULL` ____
3. ใบของผู้ลงนามไม่ได้ถูกเขียนลง `0xE0E8` แต่ขั้นอื่นทำครบ ____
4. อุปกรณ์ subscribe `commands/#` แล้วขอ ใบของผู้ลงนามถูกเขียนลง `0xE0E8` และ version ที่แพลตฟอร์มใช้มากกว่าตัวนับในชิป ____
5. มีคนเอา manifest รุ่นก่อนหน้าที่เคย apply สำเร็จแล้ว มาส่งพร้อม correlation id ที่ตรงกับคำขอที่ค้างอยู่ ____

<details><summary>เฉลย</summary>

1. **(ข)** `tesaiot_publish_protected_update()` อ่านชิปก่อนและปฏิเสธเองเมื่อช่องถูกผูกกับ anchor อื่น คืน `-1` ตัวอย่าง 06 ชี้ว่านี่มีประโยชน์เพราะถ้าปล่อยไปถึงชิป รหัส `0x800F` จะแยกไม่ออกจาก version เก่า
2. **(ง)** นี่คือการกันการเล่นซ้ำ bundle ที่ไม่มีใครขอต้องไม่ถูก apply
3. **(ค)** ชิปไม่มีอะไรไว้ตรวจลายเซ็น ได้ `0x800F` ทั้งที่ลายเซ็นถูก สัญญา PU เรียกกรณีนี้ว่าสาเหตุที่พบบ่อยที่สุด
4. **(ก)**
5. **(ค)** version ของ manifest เก่าไม่มากกว่าตัวนับในชิป ตัวนับกันย้อนรุ่นทำงาน แม้ลายเซ็นจะถูกต้องก็ตาม

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ในเส้นทาง Protected Update ขั้นไหนที่ host ที่ถูกเจาะปลอมไม่ได้ *(เป้าหมายข้อ 1)*
   - ก) การพิมพ์บรรทัด `PROTECTED UPDATE COMPLETED SUCCESSFULLY!`
   - ข) การที่ชิปตรวจลายเซ็นของ manifest กับ trust anchor ของตัวเองสำเร็จ แล้วเขียนช่องเป้าหมาย
   - ค) การส่ง ACK ขึ้นแพลตฟอร์ม
   - ง) การ subscribe `commands/#`

   <details><summary>เฉลย</summary>

   **ข** ทุกอย่างที่ host ทำหรือพิมพ์ ผู้ที่คุม host ปลอมได้ แต่ชิปไม่ยอมเขียนถ้าลายเซ็นไม่ผ่าน หลักฐานจึงอยู่ที่การอ่านสถานะจากชิปเอง

   </details>

2. ตัวนับ version (tag `C1`) ป้องกันอะไร *(เป้าหมายข้อ 2)*
   - ก) ป้องกันไม่ให้ manifest ที่ลงนามถูกต้องแต่เป็นรุ่นเก่า ถูกนำมาใช้ซ้ำ
   - ข) ป้องกันการอ่านใบรับรอง
   - ค) ป้องกันการเชื่อมต่อ WiFi ซ้ำ
   - ง) ป้องกันการเขียน tag `C0`

   <details><summary>เฉลย</summary>

   **ก** ลายเซ็นบอกว่าใครออก manifest แต่ไม่บอกว่ามันใหม่หรือเก่า ตัวนับทำหน้าที่ส่วนนั้น

   </details>

3. บอร์ดพัฒนาที่ `C0` ของ `0xE0E1` เป็น `01` เพิ่งผ่าน Protected Update ข้อใดถูก *(เป้าหมายข้อ 2)*
   - ก) ช่องนี้ถูกล็อกถาวร
   - ข) ช่องนี้รับเฉพาะ manifest ที่ลงนามโดย anchor แต่ล็อกยังเคลียร์ได้เพราะ LcsO ยังต่ำกว่า op ส่วนตัวนับ version ย้อนไม่ได้
   - ค) ทั้งล็อกและตัวนับย้อนได้ด้วยการ reflash
   - ง) LcsO เปลี่ยนเป็น op แล้ว

   <details><summary>เฉลย</summary>

   **ข** ต้องแยกสองอย่างนี้ให้ออก ล็อกเป็นเงื่อนไขใน metadata ส่วนตัวนับขึ้นอย่างเดียว

   </details>

4. ตามตัวอย่าง 06 การเปลี่ยนแปลงใดบนชิปที่ไม่มี reflash การลบ หรือการตัดไฟใดพากลับได้ *(เป้าหมายข้อ 3)*
   - ก) การเขียนใบรับรองลง `0xE0E1`
   - ข) การเลื่อน LcsO (metadata tag `C0`)
   - ค) การเชื่อมต่อ MQTT
   - ง) การอ่าน metadata

   <details><summary>เฉลย</summary>

   **ข** และเมื่อถึง `op` การเขียน metadata หยุดถาวร ล็อกของ Protected Update จึงกลายเป็นถาวรไปด้วย

   </details>

## แล็บ

**แล็บหลัก: อ่านแผนของคำขอโดยไม่ส่งจริง**

- [ ] build ตัวอย่าง 06 โดย **ไม่** เปิดสวิตช์ใด
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/06_protected_update
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  จดบรรทัด `target OID`, `anchor OID`, `version`, `with_csr`, `life cycle` และข้อความ `SKIPPED both paths` แล้วอธิบายเป็นภาษาของคุณว่าแต่ละบรรทัดบอกอะไร
- [ ] วาดแผนภาพลำดับของ Protected Update จากคำขอถึงการอ่าน metadata กลับ ทำเครื่องหมายสามจุด จุดที่ host ปลอมได้ จุดที่ชิปตรวจลายเซ็น และจุดที่ตัวนับเปลี่ยน
- [ ] เขียนรายการตรวจสามข้อที่คุณจะทำก่อนตีความรหัส `0x800F` ว่า "ลายเซ็นผิด"
- [ ] **OTA** อ่าน [ota_client.c](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client/ota_client.c) แล้วเขียนแผนเติม `ota_verify_firmware()` เป็นขั้น (เทียบ SHA-256 กับ `file_hash` แล้วตรวจ `signature` ด้วยกุญแจสาธารณะที่อุปกรณ์เชื่อ)
  ระบุว่ากุญแจสาธารณะนั้นควรมาจากไหน และทำไม `file_hash` อย่างเดียวไม่พอ (บทเรียน 1.2)

**แล็บเสริม: Protected Update จริง ทำเมื่อผู้สอนอนุญาตเท่านั้น**

สิ่งที่จะเปลี่ยนถาวรบนชิปของคุณ คือตัวนับ version ของช่อง `0xE0E1` ขึ้นหนึ่งขั้น สิ่งที่จะเปลี่ยนแต่กลับได้บนบอร์ดสถานะ creation คือล็อกของช่องนั้น
ปุ่ม Protected Update บนจอเรียก `tesaiot_publish_protected_update()` ด้วย `with_csr = true` ตามบท D2 จึงสร้างคู่กุญแจใหม่ในชิปด้วย LcsO จะไม่ถูกแตะ

- [ ] อุปกรณ์ต้องเชื่อมต่อแพลตฟอร์มได้ (บทเรียน 3.2) บน variant mtb-mpy อ่าน `optiga.read_metadata(0xE0E1)` จดค่า tag `C0` และ `D0` **ถ้า `C0` ไม่ใช่ `01` หยุดและแจ้งผู้สอน**
- [ ] HSM Security → Protected Update บนจอ จดข้อความบนจอและบรรทัด `[PU-Ingest]` บน UART เทียบกับ "ดูของจริงก่อน"
- [ ] อ่าน metadata อีกครั้ง `D0` ต้องเปลี่ยนเป็นค่าที่ระบุ anchor และ `C0` ต้องเท่าเดิม ถ้า `C0` เปลี่ยน หยุดและรายงานทันที
- [ ] ปิดเปิดบอร์ดแล้วเชื่อมต่อใหม่ ดูว่ามีบรรทัด `Ignoring a Protected Update bundle nobody asked for` หรือไม่ ถ้าเห็น STEP 3 และ STEP 4 ทั้งที่ไม่ได้กดอะไร แปลว่าการกันเล่นซ้ำผิดปกติ ให้รายงาน
- [ ] ลองกด Enrol ใส่ช่องที่ถูกล็อก จดข้อความบนจอ แล้วให้ผู้สอนตัดสินใจว่าจะใช้เมนู Unlock คืนสภาพหรือไม่

## ไปต่อ

Protected Update ต้องมีใบรับรองของอุปกรณ์อยู่ก่อน หรือส่ง CSR ไปพร้อมคำขอ โมดูลสุดท้ายจะดูการลงทะเบียนด้วย CSR ตั้งแต่สร้างกุญแจในชิปจนได้ใบรับรองกลับมา
แล้วรวมทุกอย่างเป็นอุปกรณ์ที่ปลอดภัยหนึ่งชิ้น

บทเรียนถัดไป: [บทเรียน 5.1: ลงทะเบียนด้วย CSR](../../m05-provisioning/l01-csr-enrolment/README.md)

## สะท้อนคิด

- ในระบบของคุณ log บรรทัดไหนที่ทีมเชื่อว่าเป็นหลักฐาน ทั้งที่มันเป็นแค่ข้อความที่โปรแกรมพิมพ์
- ถ้าต้องส่งมอบอุปกรณ์ที่เลื่อน LcsO แล้ว คุณจะออกแบบขั้นตอนอนุมัติอย่างไรให้ไม่มีใครทำโดยบังเอิญ
- ฟังก์ชันที่ชื่อว่า verify ในโค้ดของคุณ ตรวจอะไรจริง ๆ บ้าง

## แหล่งอ้างอิง

- [SDK: cm33/security/06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c)
- [SDK: PROTECTED_UPDATE_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/PROTECTED_UPDATE_CONTRACT.md)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [SDK: cm33/security/02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c)
- [Firmware update (BLE NUS) (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__ble__nus__fw__update.html)
- [Infineon: protected_update_data_set tool README @ release-v5.3.0 (MIT)](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/tools/protected_update_data_set/README.md)
- [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf) ข้อ 5.3
- ตัวอย่างบน Developer Hub: [TESAIoT OTA HTTPS Client (C Version)](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) (Apache-2.0) · [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น)
