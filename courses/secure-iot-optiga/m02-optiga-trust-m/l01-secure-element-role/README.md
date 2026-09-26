---
id: sec-iot.m02.l01
lang: th
title: {th: ชิปความปลอดภัยทำอะไรให้เรา, en: What a secure element does for us}
summary: {th: รู้ว่า OPTIGA™ Trust M เก็บและทำอะไร และอ่านสถานะของ HSM จาก SDK โดยไม่เริ่มธุรกรรม, en: 'Learn what OPTIGA™ Trust M stores and does, and read HSM state from the SDK without starting a transaction.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l02]
objectives:
- {th: ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข, en: 'Name at least three secure-element functions, such as key storage, signing and random numbers.'}
- {th: อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK, en: 'Read HSM state with calls that need no chip transaction, following the SDK reference example.'}
- {th: อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น, en: Explain which chip operations are irreversible and why the lessons will not touch them.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: sec.crypto, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/optiga-trust-m-overview', path: data/object_dumps/trust_m3_json.txt, ref: a45b86bda014efeebfb85f084f779cedb07b32dc, license: MIT}
---

# บทเรียน 2.1: ชิปความปลอดภัยทำอะไรให้เรา

> โมดูล 2 · ชิปความปลอดภัย OPTIGA™ Trust M · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

บนบอร์ด TESAIoT Dev Kit มีชิป OPTIGA™ Trust M อยู่หนึ่งตัว ต่ออยู่บนบัส I2C เดียวกับตัวควบคุมจอสัมผัส และถูกสั่งงานจากคอร์ CM33_NS
บทนี้จะเปิดดูว่าในชิปมีอะไร ทำอะไรได้ อ่านสถานะแบบไหนที่ "ฟรี" และคำสั่งไหนที่ทำแล้วไม่มีทางย้อน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข
2. อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK
3. อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 1.2: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **บอร์ด:** TESAIoT Dev Kit พร้อมสาย USB ที่เสียบพอร์ต KitProg และโปรแกรม serial terminal สำหรับอ่าน console ของ CM33_NS
- **ซอฟต์แวร์:** TESAIoT PSE84 Dev Kit SDK ที่ commit `ef72c1b` และ ModusToolbox 3.6 (README ของ SDK ระบุว่าต้องเป็นรุ่นนี้)

```bash
git clone https://github.com/tesaiot/tesaiot-pse84-devkit-sdk.git
cd tesaiot-pse84-devkit-sdk
git checkout ef72c1b658178eee8c38b1e47d28b006f80a59b5
cd bento-firmware-template-mtb-only
./setup.sh --build
```

`setup.sh` พิมพ์ทุกคำสั่งที่มันรันให้เห็นก่อน การ build ครั้งแรกใช้เวลาราวสิบนาที
หลัง flash ทุกครั้ง **ถอดสาย USB ออกจนสุด นับสิบ แล้วเสียบใหม่** README ของ SDK อธิบายว่าไฟหน้าจอต้องการขอบสัญญาณแบบเย็น รีเซ็ตผ่าน debugger อย่างเดียวจอจะดำ

## ดูของจริงก่อน

นี่คือส่วนหัวของตัวอย่าง [ref_hsm.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c) ที่เราจะรันวันนี้
ผู้เขียน SDK เปิดไฟล์ด้วยประโยคว่า "THIS IS A REFERENCE LIST, NOT A JOB." แล้วตามด้วย

> It enrols nothing, publishes nothing, and writes nothing — to the chip or anywhere else.

และมีย่อหน้า SAFETY บอกว่าไฟล์นี้ไม่อ่านไม่เขียน metadata tag `C0` ซึ่งเป็นสถานะวงจรชีวิตของชิปที่ "moves one way only and which no reflash undoes"

**ทายก่อน:** ทำไมตัวอย่างแรกที่ SDK ให้เรารันกับชิปความปลอดภัย จึงเป็นตัวอย่างที่ตั้งใจ **ไม่ทำอะไรกับชิปเลย**
เขียนคำตอบหนึ่งประโยค แล้วกลับมาเทียบตอนจบหัวข้อแนวคิดข้อ 3

## แนวคิด

### 1. ชิปนี้ทำอะไรได้บ้าง

Infineon อธิบาย OPTIGA™ Trust M ว่าเป็น security controller บนฮาร์ดแวร์ที่ผ่านการรับรอง Common Criteria EAL6+ (high)
([optiga-trust-m-overview](https://github.com/Infineon/optiga-trust-m-overview)) หน้าที่ที่เราใช้บนบอร์ดนี้มีหกกลุ่ม ทุกกลุ่มมีฟังก์ชันจริงใน host library ของ Infineon (`optiga_crypt.h` และ `optiga_util.h`)

| หน้าที่ | ฟังก์ชันใน host library | SDK ของบอร์ดใช้ทำอะไร |
|---|---|---|
| สร้างและเก็บกุญแจลับ | `optiga_crypt_ecc_generate_keypair` | สร้างคู่กุญแจใหม่ตอนลงทะเบียนด้วย CSR (บทเรียน 5.1) |
| ลงลายเซ็นและตรวจลายเซ็น | `optiga_crypt_ecdsa_sign`, `optiga_crypt_ecdsa_verify` | ลงนาม CertificateVerify ใน mTLS (บทเรียน 3.1) และตรวจว่าใบรับรองเข้าคู่กับกุญแจ |
| สุ่มเลขด้วย TRNG | `optiga_crypt_random` | ตัวช่วยใน `tesaiot_crypto.c` เรียกด้วย `OPTIGA_RNG_TYPE_TRNG` (บท D1 ระบุว่าเป็นไฟล์อ้างอิงที่ส่งมาแต่ไม่ได้คอมไพล์ในแม่แบบ) |
| ตกลงกุญแจและสร้างกุญแจย่อย | `optiga_crypt_ecdh`, `optiga_crypt_hkdf`, `optiga_crypt_hmac` | มีให้ใช้ ยังไม่ใช่เส้นทางหลักของแม่แบบ |
| อ่านเขียนข้อมูลและ metadata | `optiga_util_read_data`, `optiga_util_read_metadata`, `optiga_util_write_metadata` | อ่านใบรับรองออกมาใช้ใน TLS |
| อัปเดตแบบป้องกัน | `optiga_util_protected_update_start` / `_continue` / `_final` | รับใบรับรองใหม่ที่ลงนามจากแพลตฟอร์ม (บทเรียน 4.2) |

SDK ไม่ได้ให้เราเรียกฟังก์ชันเหล่านี้ตรง ๆ ทั้งหมด ส่วนที่เกี่ยวกับการครอบครองชิป การลงทะเบียน และ Protected Update ถูกห่อไว้ใน `libbento_hsm.a`
ซึ่งตาม [เอกสาร tesaiot_hsm](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/README.md) export ฟังก์ชันออกมา 18 ตัว

### 2. Object, metadata และสถานะวงจรชีวิต

ข้างในชิปแบ่งเป็นช่อง (object) แต่ละช่องมีที่อยู่สองไบต์เรียกว่า OID ตารางนี้รวมจาก dump ตัวอย่างของ Infineon
([trust_m3_json.txt](https://github.com/Infineon/optiga-trust-m-overview/blob/a45b86bda014efeebfb85f084f779cedb07b32dc/data/object_dumps/trust_m3_json.txt), MIT)
กับการใช้งานที่ SDK บันทึกไว้ใน `tesaiot_config.h` และบท [C4](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)

| OID | ค่าจากโรงงาน (dump ตัวอย่างของ Infineon) | TESAIoT ใช้ทำอะไร |
|---|---|---|
| `0xE0C2` | UID ของชิป 27 ไบต์ อ่านได้เสมอ เปลี่ยนไม่ได้ | ที่มาของค่า `factory_uid` ที่ใช้เป็น client id ของ MQTT ในโหมด mTLS |
| `0xE0E0` | ใบรับรองจาก Infineon, Change = never | ตัวตนจากโรงงาน |
| `0xE0F0` | กุญแจ ECC P-256 คู่กับ `0xE0E0`, Change = never, Execute = always | ลงนาม TLS เมื่อยังไม่ได้ลงทะเบียน |
| `0xE0E1` | ช่องใบรับรอง, Change = LcsO < op | ใบรับรองอุปกรณ์ของ TESAIoT |
| `0xE0F1` | ช่องกุญแจ, Change = LcsO < op | กุญแจคู่กับ `0xE0E1` สร้างตอนลงทะเบียน |
| `0xE0E8` | ช่อง trust anchor, Change = LcsO < op | anchor ที่ใช้ตรวจ manifest ของ Protected Update |

**metadata** ของแต่ละช่องเป็น TLV ที่ขึ้นต้นด้วย `20` tag ที่ต้องอ่านเป็นในหลักสูตรนี้มีไม่กี่ตัว (ดูได้จาก dump และจาก [example_optiga_util_protected_update.c](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/optiga/example_optiga_util_protected_update.c) ของ Infineon)

| tag | ความหมาย | ค่าที่พบบ่อย |
|---|---|---|
| `C0` | LcsO สถานะวงจรชีวิตของ object | `01` creation, `03` initialization, `07` operational, `0F` termination |
| `C1` | version ของ object ใช้กันการย้อนรุ่นใน Protected Update | ขึ้นได้อย่างเดียว |
| `D0` | Change access condition ใครเขียนได้ | `FF` never, `E1 FC 07` = LcsO < op, `21 E0 E8` = ต้องมี manifest ที่ตรวจด้วย `0xE0E8` |
| `D1` / `D3` | Read / Execute access condition | `00` always |
| `E8` | ชนิดของ object | `11` trust anchor, `12` ใบรับรองของอุปกรณ์ |

สังเกต `E1 FC 07` ให้ดี มันแปลว่า "เขียนได้ตราบที่ LcsO ยังน้อยกว่า operational" ช่องส่วนใหญ่ที่เราใช้จึงเขียนได้ก็เพราะชิปยังอยู่ที่ creation (`01`)
บท D2 ของเอกสาร SDK บอกว่าบอร์ดทุกตัวบนโต๊ะทดลองควรอ่าน `C0` ได้ `01`

### 3. สิ่งที่ย้อนกลับไม่ได้ และการอ่านสถานะแบบฟรี

**ย้อนกลับไม่ได้** ตามที่ตัวอย่าง [06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c) เขียนไว้ชัด

1. **LcsO (tag `C0`)** เดินทางเดียว `cr (0x01) -> in (0x03) -> op (0x07) -> te (0x0F)` ไม่มี reflash ไม่มีการลบ ไม่มีการตัดไฟใดพากลับได้
   สิ่งที่ทำให้มันเดินคือการเขียน metadata ที่มี tag `C0` อยู่ข้างใน เมื่อถึง `op` การเขียน metadata จะหยุดได้ตลอดไป
   ช่องที่เงื่อนไข Change เป็น `LcsO < op` ก็จะเขียนแบบธรรมดาไม่ได้อีก
2. **ตัวนับ version (tag `C1`)** ของ object ที่ผ่าน Protected Update ขึ้นได้อย่างเดียว manifest ครั้งต่อไปต้องมีเลขมากกว่าเดิม
3. **Change = never** ของ `0xE0E0` และ `0xE0F0` ตัวตนจากโรงงานเปลี่ยนไม่ได้เลย ข้อนี้ไม่ใช่สิ่งที่เราทำ แต่ต้องรู้ว่าไม่มีทางแก้

ส่วน **ล็อกของ Protected Update** (tag `D0` = `21 E0 E8`) กลับทางได้ **ตราบที่ LcsO ยังต่ำกว่า op** ตัวอย่าง 06 ย้ำว่าต้องบอกเสมอว่ากำลังพูดถึงบอร์ดแบบไหน
"ล็อกถาวร" จริงสำหรับอุปกรณ์ที่ส่งมอบแล้ว และไม่จริงสำหรับบอร์ดพัฒนา

ไม่มีตัวอย่างใดใน SDK เขียน tag `C0` และตัวอย่าง 06 ระบุว่าไม่มีฟังก์ชันใดใน 18 ตัวของ `libbento_hsm.a` เขียนมันเช่นกัน
หลักสูตรนี้ **ไม่สั่งให้คุณเขียน `C0` หรือเลื่อน LcsO ไม่ว่ากรณีใด** เพราะผลคือบอร์ดที่ใช้เรียนต่อไม่ได้ และไม่มีทางกู้
ตัวอย่าง 06 ให้หลักไว้ว่าการเลื่อนวงจรชีวิตควรอยู่ในเครื่องมือแยกต่างหากที่ตั้งชื่อชัด และรันโดยคนที่ตัดสินใจแล้วว่าจะส่งมอบบอร์ดนั้น

**อ่านสถานะแบบฟรี** `ref_hsm.c` แบ่งคำถามเป็นสองแบบ

- สามฟังก์ชันอ่านตัวแปรธรรมดา ไม่แตะชิป เรียกจาก task ไหน บ่อยแค่ไหนก็ได้ แม้ระหว่างที่การลงทะเบียนกำลังวิ่ง
  คือ `trustm_requested_target_oid()`, `trustm_requested_anchor_oid()` และ `trustm_current_correlation_id()`
- `optiga_manager_lock()` **ไม่ฟรี** มันเข้าไปถือประตูเข้าชิป ถ้าได้ `true` ต้องคืนด้วย `optiga_manager_unlock()` ทุกครั้ง
  และถ้าได้ `false` อาจแปลว่าเพิ่งรอครบสิบวินาทีมา จึงห้ามเรียกจาก tick ของ UI

## ตัวอย่างสมบูรณ์

ตัดจาก [ref_hsm.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c) บรรทัด 65–89
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* NULL when nothing is in flight; otherwise the id the platform's reply is
     * matched against. This is the "is an enrolment outstanding?" test, and it
     * is the value trustm_reset_state() destroys — so check it before you
     * reset anything. Print it guarded: %s given NULL faults on this
     * platform's newlib. */
    const char *cid = trustm_current_correlation_id();
    printf("  trustm_current_correlation_id()= %s\r\n",
           (cid != NULL) ? cid : "(none — nothing in flight)");

    /* ── Chip readiness — a balanced probe, not a free read ──────────────── */

    if (optiga_manager_lock()) {
        /* True means both "the manager is up" and "the gate is now ours". The
         * unlock is not optional and there is no path out of here without it. */
        printf("  optiga_manager_lock()          = true  (manager up, chip free)\r\n");
        optiga_manager_unlock();
        printf("  optiga_manager_unlock()        — gate returned\r\n");
    } else {
        /* Either optiga_manager_init() has never run, or another task has held
         * the chip for the full 10-second timeout. Those are different problems
         * and the return value does not separate them; if you need to know,
         * track whether your own code has called init(). */
        printf("  optiga_manager_lock()          = false (manager not "
               "initialised, or another task holds the chip)\r\n");
    }
```

สามเรื่องที่ควรเห็นในโค้ดนี้

1. **การพิมพ์ NULL ต้องมีตัวกัน** `printf("%s", NULL)` ทำให้ newlib บนแพลตฟอร์มนี้ fault ตามคอมเมนต์ ตัวอย่างจึงแทนด้วยข้อความ
2. **ถือแล้วต้องคืน** ในกิ่ง `true` ไม่มีทางออกจากฟังก์ชันโดยไม่ผ่าน `optiga_manager_unlock()`
3. **ค่า false ไม่บอกสาเหตุ** มันแปลได้ทั้ง "ยังไม่มีใคร init ตัวจัดการ" และ "มี task อื่นถือชิปอยู่ครบสิบวินาที" ถ้าต้องแยกสองกรณีนี้ โค้ดของคุณต้องจำเองว่าเรียก `optiga_manager_init()` แล้วหรือยัง

## ฝึกเติม

จัดแต่ละการกระทำเข้ากลุ่ม **ฟรี** (ไม่แตะชิป) **ถือประตู** (ต้องคืน) **ธุรกรรมกับชิป** (ชิปทำงานจริง) หรือ **ย้อนไม่ได้**

1. `trustm_requested_anchor_oid()` ____
2. `optiga_manager_lock()` ____
3. `optiga_crypt_ecdsa_sign(me, digest, 32, OPTIGA_KEY_ID_E0F0, sig, &len)` ____
4. เขียน metadata ที่มี tag `C0` ค่า `07` ลงช่องหนึ่ง ____
5. Protected Update ที่ถูก apply สำเร็จ ส่วนที่เป็นตัวนับ version ของช่องนั้น ____
6. `trustm_current_correlation_id()` ____

<details><summary>เฉลย</summary>

1. **ฟรี** อ่านตัวแปร ค่าเริ่มต้นหลังรีเซ็ตคือ `0xE0E8`
2. **ถือประตู** ได้ `true` แล้วต้อง `optiga_manager_unlock()`
3. **ธุรกรรมกับชิป** และต้องทำภายใต้ประตูที่ถืออยู่ (บทเรียน 2.2)
4. **ย้อนไม่ได้** LcsO ของช่องนั้นเดินไป operational ห้ามทำในหลักสูตรนี้
5. **ย้อนไม่ได้** ตัวนับขึ้นอย่างเดียว ส่วนล็อกของช่องนั้นยังกลับได้ถ้า LcsO ต่ำกว่า op
6. **ฟรี** NULL แปลว่าไม่มีคำขอค้างอยู่

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ข้อใด **ไม่ใช่** หน้าที่ที่ OPTIGA™ Trust M ทำให้ SDK ของบอร์ด *(เป้าหมายข้อ 1)*
   - ก) สร้างเลขสุ่มด้วย TRNG
   - ข) ลงลายเซ็น ECDSA ด้วยกุญแจที่อยู่ในชิป
   - ค) เข้ารหัสภาพบนจอ LCD
   - ง) เก็บกุญแจลับที่สร้างขึ้นในชิป

   <details><summary>เฉลย</summary>

   **ค** การวาดจอเป็นงานของ CM55 ชิปความปลอดภัยไม่เกี่ยว

   </details>

2. `ref_hsm.c` บอกว่าฟังก์ชันใด **ไม่ใช่** การอ่านแบบฟรี *(เป้าหมายข้อ 2)*
   - ก) `trustm_requested_target_oid()`
   - ข) `trustm_current_correlation_id()`
   - ค) `optiga_manager_lock()`
   - ง) `trustm_requested_anchor_oid()`

   <details><summary>เฉลย</summary>

   **ค** มันถือประตูเข้าชิป ได้ `true` ต้องคืน และถ้าได้ `false` อาจเพิ่งรอมาสิบวินาที

   </details>

3. บอร์ดพัฒนาตัวหนึ่งมี tag `C0` ของช่อง `0xE0E1` เป็น `01` และ `D0` เป็น `21 E0 E8` ข้อใดถูก *(เป้าหมายข้อ 3)*
   - ก) ช่องนี้ล็อกถาวร ไม่มีทางเขียนแบบธรรมดาได้อีก
   - ข) ช่องนี้รับเฉพาะ manifest ที่ตรวจด้วย `0xE0E8` แต่ล็อกยังเคลียร์ได้เพราะ LcsO ยังต่ำกว่า op
   - ค) ชิปเสียแล้ว
   - ง) ช่องนี้เขียนแบบธรรมดาได้ตามปกติ

   <details><summary>เฉลย</summary>

   **ข** ล็อกของ Protected Update เป็นเงื่อนไขใน metadata ไม่ใช่ฟิวส์ ตราบที่ LcsO ยังเป็น creation การเขียน metadata ยังทำได้

   </details>

4. ทำไมหลักสูตรนี้จึงไม่สั่งให้เขียน tag `C0` *(เป้าหมายข้อ 3)*
   - ก) เพราะชิปไม่รองรับ
   - ข) เพราะ LcsO เดินทางเดียว ไม่มี reflash ใดพากลับได้ และเมื่อถึง op การเขียน metadata จะหยุดถาวร
   - ค) เพราะต้องใช้รหัสผ่านจาก Infineon
   - ง) เพราะจะทำให้ WiFi ใช้ไม่ได้

   <details><summary>เฉลย</summary>

   **ข** ผลคือบอร์ดที่ใช้เรียนต่อไม่ได้และไม่มีทางกู้ ตัวอย่าง 06 ของ SDK ให้หลักว่างานนี้ควรอยู่ในเครื่องมือแยกที่ตั้งชื่อชัด

   </details>

## แล็บ

**อ่านสถานะของ HSM โดยไม่เริ่มอะไรเลย** จดทุกบรรทัดที่ได้ลงบันทึกการเรียน

- [ ] build แม่แบบโดยเปิดตัวอย่างและเลือก `ref_hsm` ให้รันบน CM33_NS (id ของตัวอย่างอยู่ในตาราง `sdk_examples_cm33_table.c`)
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/ref_hsm
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  แล้วถอดสาย USB นับสิบ เสียบใหม่ เปิด serial terminal ที่พอร์ต KitProg
- [ ] **ทายก่อนดูผล** ว่า `trustm_requested_target_oid()` กับ `trustm_requested_anchor_oid()` จะได้ค่าอะไร (อ่านคอมเมนต์ในไฟล์) และ `optiga_manager_lock()` จะได้ `true` หรือ `false`
- [ ] ตัวรันตัวอย่างรอสามวินาทีหลังบูต พิมพ์รายการตัวอย่างทั้งหมด แล้วจึงรันตัวที่เลือก ผลตามซอร์สมีหน้าตาแบบนี้
  ```text
  --- tesaiot_hsm/ref_tesaiot_hsm (reference list) ---
    trustm_requested_target_oid()  = 0x....
    trustm_requested_anchor_oid()  = 0x....
    trustm_current_correlation_id()= ...
    optiga_manager_lock()          = ...
  ```
  เทียบกับที่ทาย ถ้า `optiga_manager_lock()` ได้ `false` ให้อธิบายว่าเป็นกรณีไหนในสองกรณี และคุณรู้ได้อย่างไร
- [ ] build ใหม่ด้วย `SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership` ตัวอย่างนี้เรียก `optiga_manager_init()` ก่อนแล้วจึงถือประตู ดูว่าบรรทัด `optiga_manager_lock()` เปลี่ยนไปอย่างไร แล้วอธิบายด้วยเหตุผลข้อ 3 ของตัวอย่างสมบูรณ์
- [ ] เขียนตารางสองคอลัมน์ "สิ่งที่ตัวอย่างนี้บอกเราได้" กับ "สิ่งที่มันบอกไม่ได้" อย่างน้อยฝั่งละสองข้อ

**ข้อห้ามของแล็บนี้** ไม่เปิด `EXAMPLE_HSM_REQUEST_PU` และ `EXAMPLE_HSM_ISOLATED_TEST` ของตัวอย่าง 06 และไม่เขียน metadata ใด ๆ

อยากเห็นโปรเจกต์อ้างอิงอีกแบบ ดู [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) บน Developer Hub
เป็นเฟิร์มแวร์แบบเมนูที่มีเมนูอ่าน UID กับใบรับรองจากโรงงาน และเมนูอ่าน metadata โปรเจกต์นี้มาพร้อม BSP ของ PSOC™ Edge E84 Evaluation Kit (`APP_KIT_PSE84_EVAL_EPC2`)
และอยู่ภายใต้ Cypress (Infineon) EULA หลักสูตรนี้จึงอ้างอิงด้วยลิงก์เท่านั้น ไม่คัดลอกโค้ดมา

## ไปต่อ

เราเห็นแล้วว่าแค่ถามว่า "ชิปว่างไหม" ก็ต้องถือประตูแล้วคืน บทต่อไปจะลงลึกเรื่องประตูนั้น ว่าทำไมมีสามชื่อ ทำไมต้องกันจอสัมผัสออกจากบัส
และงานแบบไหนห้ามทำใน task ที่วาดจอ

บทเรียนถัดไป: [บทเรียน 2.2: กติกาการเข้าถึงชิป](../l02-chip-access-discipline/README.md)

## สะท้อนคิด

- ในโปรเจกต์ของคุณ มีคำสั่งไหนที่ทำแล้วย้อนไม่ได้ และมันถูกซ่อนอยู่ในตัวอย่างที่ใครก็กดรันได้หรือเปล่า
- ถ้าคุณต้องเขียนหน้าจอสถานะของ HSM คุณจะใช้ค่าไหนจากตัวอย่างนี้ และจะเลี่ยงการเรียกอะไรในรอบวาดจอ
- ค่า `false` ที่แปลได้สองอย่าง เคยทำให้คุณแก้ปัญหาผิดจุดในงานอื่นบ้างไหม

## แหล่งอ้างอิง

- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3) และรุ่นที่ SDK ใช้ [@ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0)
- [Infineon optiga-trust-m-overview (MIT)](https://github.com/Infineon/optiga-trust-m-overview/tree/a45b86bda014efeebfb85f084f779cedb07b32dc)
- [SDK: เอกสาร tesaiot_hsm](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/README.md)
- [SDK: cm33/security/ref_hsm.c (อ่านสถานะโดยไม่เริ่มธุรกรรม)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c)
- [SDK: cm33/security/06_protected_update.c (สิ่งที่ย้อนกลับไม่ได้)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c)
- [SDK: ตัวอย่างฝั่ง CM33 (ข้อควรทราบเรื่องสถานะ LcsO)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: tesaiot_config.h (แผนที่ OID ของ TESAIoT)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/include/tesaiot_config.h)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- ตัวอย่างบน Developer Hub: [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น)
