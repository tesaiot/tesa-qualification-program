---
id: sec-iot.m01.l02
lang: th
title: {th: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว, en: Crypto basics for embedded systems}
summary: {th: 'แยกหน้าที่ของ hash, MAC, ลายเซ็นดิจิทัล การเข้ารหัสสองแบบ และใบรับรอง X.509', en: 'Tell apart hashes, MACs, digital signatures, the two kinds of encryption and X.509 certificates.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l01]
objectives:
- {th: เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย ความลับ ความถูกต้อง หรือการยืนยันตัวตน ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี, en: 'Pick the right primitive for confidentiality, integrity or authenticity in at least 4 of 5 cases.'}
- {th: 'อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้', en: 'Read an X.509 certificate and identify subject, issuer, validity and public key.'}
- {th: อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป, en: Explain why private keys belong in a secure element rather than general flash.}
develops:
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/optiga-trust-m', path: examples/optiga/example_optiga_crypt_ecdsa_sign.c, ref: release-v5.3.0, license: MIT}
---

# บทเรียน 1.2: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว

> โมดูล 1 · Threat model และพื้นฐานวิทยาการเข้ารหัส · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ตาราง STRIDE ในบทที่แล้วเต็มไปด้วยคำว่า TLS ใบรับรอง และลายเซ็น บทนี้จะแยกเครื่องมือเหล่านั้นออกจากกันทีละตัว
ว่าตัวไหนให้สมบัติอะไร ตัวไหน **ให้ไม่ได้** และทำไมกุญแจลับจึงควรอยู่ในชิป ไม่ใช่ในไฟล์

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย ความลับ ความถูกต้อง หรือการยืนยันตัวตน ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี
2. อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้
3. อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 1.1: Threat model ของอุปกรณ์ IoT](../l01-threat-modelling/README.md) เปิดตาราง threat model ของคุณไว้ข้าง ๆ
- **เครื่องมือ:** คอมพิวเตอร์ที่มี `openssl` ในเทอร์มินัล (Linux และ macOS มีอยู่แล้ว บน Windows ใช้ Git Bash หรือ WSL) และต่ออินเทอร์เน็ตได้
- **บอร์ด:** ไม่ต้องใช้ในบทนี้ ทุกการทดลองทำบนคอมพิวเตอร์ แต่ข้อมูลที่อ่านได้คือของจริงที่บอร์ดใช้

## ดูของจริงก่อน

เปิดเทอร์มินัลแล้วขอใบรับรองจาก broker ตัวเดียวกับที่บอร์ดเชื่อมต่อ

```bash
openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev -showcerts </dev/null
```

ผลที่ได้มีใบรับรองสองใบ ตอนเขียนบทเรียนนี้ (26 ก.ย. 2026) ใบแรกมี subject `CN = mqtt.tesaiot.dev` ออกโดย `CN = TESAIoT Intermediate CA`
ใบที่สองคือ `TESAIoT Intermediate CA` เอง ออกโดย `TESAIoT Root CA` ค่าวันที่ในเครื่องของคุณอาจต่างออกไป เพราะใบของเซิร์ฟเวอร์ถูกต่ออายุเป็นระยะ

**ทายก่อน:** เฟิร์มแวร์ของบอร์ดมีใบรับรองใบไหนฝังอยู่ในตัวแล้ว ใบของเซิร์ฟเวอร์ ใบ intermediate หรือใบ root
เขียนคำตอบลงบันทึกการเรียน แล้วหาคำตอบในแล็บข้อ 3

## แนวคิด

### 1. สามเป้าหมาย สี่ครอบครัวเครื่องมือ

เวลาเลือกเครื่องมือ ให้ถามก่อนว่าต้องการสมบัติไหน **ความลับ** (คนอื่นอ่านไม่ได้) **ความถูกต้อง** (รู้ได้ว่าถูกแก้หรือไม่)
หรือ **การยืนยันตัวตน** (รู้ได้ว่าใครเป็นคนสร้างข้อมูลนี้) แล้วค่อยเลือกจากตาราง

| เครื่องมือ | ใช้กุญแจอะไร | ให้อะไร | ให้ไม่ได้ | บนโหนดของเรา |
|---|---|---|---|---|
| hash เช่น SHA-256 | ไม่มีกุญแจ | ลายนิ้วมือขนาดคงที่ของข้อมูล แก้หนึ่งบิตผลเปลี่ยนทั้งหมด | ไม่รู้ว่าใครสร้าง ใครก็คำนวณใหม่ได้ | fingerprint ของ CA ที่ปักไว้ในเฟิร์มแวร์ |
| MAC เช่น HMAC-SHA256 | กุญแจลับตัวเดียวที่สองฝั่งมีร่วมกัน | ความถูกต้อง และรู้ว่ามาจากคนที่มีกุญแจ | พิสูจน์ต่อบุคคลที่สามไม่ได้ เพราะทั้งสองฝั่งสร้างได้เท่ากัน | OPTIGA™ Trust M คำนวณ HMAC ได้ (`optiga_crypt_hmac`) |
| ลายเซ็นดิจิทัล เช่น ECDSA P-256 | คู่กุญแจ ลงนามด้วยกุญแจลับ ตรวจด้วยกุญแจสาธารณะ | ความถูกต้อง การยืนยันตัวตน และพิสูจน์ต่อคนอื่นได้ | ไม่ได้ซ่อนข้อมูล | ลายเซ็น CertificateVerify ใน mTLS, manifest ของ Protected Update |
| การเข้ารหัสแบบสมมาตร เช่น AES | กุญแจลับตัวเดียวกันทั้งเข้าและถอด | ความลับ และเร็ว | ต้องมีวิธีตกลงกุญแจกันก่อน | ข้อมูลใน TLS record |
| การตกลงกุญแจแบบอสมมาตร เช่น ECDHE | คู่กุญแจชั่วคราวของแต่ละฝั่ง | ได้กุญแจลับร่วมกันโดยไม่ต้องส่งกุญแจข้ามสาย | ไม่ได้ยืนยันว่าอีกฝั่งเป็นใคร ต้องใช้ลายเซ็นช่วย | ส่วน `ECDHE` ในชื่อ ciphersuite |

ตัวอย่างจริงของข้อควรระวังอยู่ใน [02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c) ของ SDK
ฟังก์ชันตรวจลายเซ็นของโมเดล AI ตรวจ CRC ของส่วนท้ายไฟล์ได้ครบ แต่ยังคืนค่า "ตรวจไม่ได้" (`-10`) ไม่ใช่ "ผ่าน" (`+1`)
คอมเมนต์ในไฟล์อธิบายว่าถ้าคืนผ่านเพราะ CRC ตรง เท่ากับเปลี่ยนลายเซ็นให้กลายเป็น checksum เพราะใครก็คำนวณ CRC ใหม่ทับได้
hash ของการเข้ารหัสอย่าง SHA-256 ก็ติดปัญหาเดียวกันถ้าไม่มีกุญแจมาเกี่ยว

### 2. ใบรับรอง X.509 และห่วงโซ่ความเชื่อใจ

ใบรับรอง X.509 ([RFC 5280](https://www.rfc-editor.org/rfc/rfc5280)) คือเอกสารที่ผู้ออก (issuer) ลงนามรับรองว่า
"กุญแจสาธารณะนี้เป็นของ subject นี้ ในช่วงเวลานี้" ฟิลด์ที่ต้องอ่านเป็นมีสี่ตัว

- **subject** เจ้าของใบ เช่น `CN = mqtt.tesaiot.dev`
- **issuer** ผู้ที่ลงนามใบนี้ เช่น `CN = TESAIoT Intermediate CA`
- **validity** ช่วงเวลา `notBefore` ถึง `notAfter`
- **subjectPublicKeyInfo** อัลกอริทึมและกุญแจสาธารณะของ subject

ห่วงโซ่ของ broker คือ ใบของเซิร์ฟเวอร์ ← TESAIoT Intermediate CA ← TESAIoT Root CA อุปกรณ์เชื่อใบของเซิร์ฟเวอร์ได้
เพราะเดินลายเซ็นย้อนขึ้นไปจนเจอใบที่มันเชื่ออยู่แล้วในเฟิร์มแวร์ ใบนั้นเรียกว่า **trust anchor**

ฝั่งอุปกรณ์ก็มีใบรับรองของตัวเองสองชุด ตามที่บท [C4 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html) และ `mqtt_mtls_setup.c` บันทึกไว้

- ใบจากโรงงานในช่อง `0xE0E0` มี subject `CN=InfineonIoTNode` **เหมือนกันทุกชิป** ออกโดย `Infineon OPTIGA(TM) Trust M CA 300`
  ฟิลด์ที่ต่างกันต่อชิปมีแค่ serial number กับกุญแจสาธารณะ ใบนี้จึงพิสูจน์ได้ว่า "นี่คือ Trust M ของแท้" แต่ไม่ได้บอกว่าเป็นอุปกรณ์เครื่องไหน
- ใบของ TESAIoT ในช่อง `0xE0E1` ที่ได้หลังลงทะเบียน มี subject เป็น `device_id` ออกโดย `TESAIoT MCU CA`

เรื่อง **อายุ** ของใบมีข้อที่ต้องรู้: ในค่าตั้ง mbedTLS ของ CM33_NS ที่ commit นี้
([mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h))
ตัวเลือก `MBEDTLS_HAVE_TIME_DATE` ถูกปิด ซึ่งตามคำอธิบายในไฟล์เดียวกันคือส่วนที่ใช้ตรวจช่วงเวลาของใบ X.509
การ parse CRL (`MBEDTLS_X509_CRL_PARSE_C`) ก็ถูกปิด ในค่าตั้งนี้อุปกรณ์จึงไม่ได้ปฏิเสธใบเพราะหมดอายุหรือถูกเพิกถอน
ให้เขียนเรื่องนี้ลงช่อง "ความเสี่ยงที่ยังเหลือ" ของ threat model

### 3. ทำไมกุญแจลับควรอยู่ในชิป

กุญแจลับที่อยู่ในไฟล์หรือใน flash อ่านออกได้หลายทาง ใครถือ image ของเฟิร์มแวร์ ใครเสียบพอร์ต debug ได้ หรือใครถอดชิป flash ไปอ่านได้ ก็ได้กุญแจไปด้วย
เมื่อได้กุญแจแล้วเขาคือ "อุปกรณ์ของเรา" ทุกประการ ทำสำเนาไปกี่เครื่องก็ได้ ETSI EN 303 645 ข้อ 5.4-1 จึงให้เก็บค่าความปลอดภัยอย่างปลอดภัย และยกชิปความปลอดภัยเป็นตัวอย่างหนึ่ง

OPTIGA™ Trust M เปลี่ยนคำถามจาก "กุญแจอยู่ที่ไหน" เป็น "ใครสั่งให้ชิปใช้กุญแจได้"

- กุญแจถูก **สร้างในชิป** และไม่มีคำสั่งอ่านออก ใน dump ตัวอย่างของ Infineon ([trust_m3_json.txt](https://github.com/Infineon/optiga-trust-m-overview/blob/a45b86bda014efeebfb85f084f779cedb07b32dc/data/object_dumps/trust_m3_json.txt), MIT)
  metadata ของช่อง `0xE0F0` มีแค่ Change = never และ Execute = always ไม่มีสิทธิ์อ่าน
- โปรแกรมส่ง **ชื่อช่อง** ของกุญแจ (OID) กับ digest เข้าไป แล้วได้ลายเซ็นกลับมา ตามตัวอย่างในหัวข้อถัดไป
- ฮาร์ดแวร์ของชิปผ่านการรับรอง Common Criteria EAL6+ (high) ตามที่ [Infineon ระบุ](https://github.com/Infineon/optiga-trust-m-overview) จึงต้านการโจมตีทางกายภาพได้ดีกว่า flash ทั่วไปมาก

และต้องพูดให้ครบว่าชิป **ไม่ได้** กันอะไร

- ถ้าเฟิร์มแวร์บน MCU ถูกยึด ผู้โจมตีสั่งชิปลงนามอะไรก็ได้ตราบที่ยังคุมบอร์ดอยู่ ชิปกันการ **ขโมยและโคลน** กุญแจ ไม่ได้กันการ **ใช้ผิด** ขณะที่บอร์ดถูกยึด
- สาย I2C ระหว่าง MCU กับชิปไม่ได้เข้ารหัสในค่าตั้งเริ่มต้นของ SDK (`OPTIGA_COMMS_DEFAULT_PROTECTION_LEVEL` เป็น `OPTIGA_COMMS_NO_PROTECTION` ใน `optiga_lib_config_mtb.h`)
  กุญแจไม่เคยวิ่งบนสาย แต่ digest และลายเซ็นวิ่ง Infineon มีฟีเจอร์ Shielded Connection สำหรับกรณีที่ต้องกันการดักสายนี้

## ตัวอย่างสมบูรณ์

นี่คือการลงนามด้วยกุญแจในชิป ตัดจากตัวอย่างของ Infineon
([example_optiga_crypt_ecdsa_sign.c @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/optiga/example_optiga_crypt_ecdsa_sign.c) บรรทัด 80–93, © 2021-2024 Infineon Technologies AG, MIT)
SDK ของบอร์ดใช้ host library รุ่นนี้ตามไฟล์ `proj_cm55/deps/optiga-trust-m.mtb`

```c
/* SPDX-FileCopyrightText: 2021-2024 Infineon Technologies AG
 * SPDX-License-Identifier: MIT */
        /**
         * 2. Sign the digest using Private key from Key Store ID E0F0
         */
        optiga_lib_status = OPTIGA_LIB_BUSY;
        return_status = optiga_crypt_ecdsa_sign(
            me,
            digest,
            sizeof(digest),
            OPTIGA_KEY_ID_E0F0,
            signature,
            &signature_length
        );

        WAIT_AND_CHECK_STATUS(return_status, optiga_lib_status);
```

อ่านทีละส่วน

- `digest` คือ SHA-256 ของข้อมูล 32 ไบต์ ลายเซ็นลงบน digest ไม่ใช่บนข้อมูลดิบ
- `OPTIGA_KEY_ID_E0F0` คือ **ชื่อช่อง** ของกุญแจ ไม่ใช่ตัวกุญแจ ไม่มีบรรทัดไหนที่กุญแจโผล่ขึ้นมาใน RAM ของ MCU
- `signature` คือผลลัพธ์ที่ออกมา เป็นข้อมูลสาธารณะ ใครก็เอาไปตรวจด้วยกุญแจสาธารณะได้
- คำสั่งนี้ทำงานแบบ **asynchronous** มันคืนค่าทันที ผลจริงมาทาง callback ที่ตั้ง `optiga_lib_status` แล้ว `WAIT_AND_CHECK_STATUS` รอให้ค่านั้นเลิกเป็น `OPTIGA_LIB_BUSY`
  เรื่องนี้จะกลับมาในบทเรียน 2.2 ว่าทำไมระหว่างรอต้องถือประตูเข้าชิปไว้ตลอด

ในเฟิร์มแวร์ของบอร์ด หน้าที่เดียวกันนี้อยู่ใน `trustm_ecdsa_sign()` ที่ TLS เรียกตอนสร้าง CertificateVerify (บทเรียน 3.1)

## ฝึกเติม

เลือกเครื่องมือหนึ่งตัวต่อหนึ่งสถานการณ์ แล้วบอกสมบัติที่ได้ นี่คือเกณฑ์ของเป้าหมายข้อ 1 ต้องถูกอย่างน้อย 4 ใน 5

1. แพลตฟอร์มส่งใบรับรองใหม่ให้อุปกรณ์ และอุปกรณ์ต้องแน่ใจว่าใบนั้นมาจากแพลตฟอร์มจริง ไม่ใช่คนอื่นส่งมา ____
2. ต้องเก็บ "ลายนิ้วมือ" ของ CA ไว้ในเอกสาร เพื่อให้คนอื่นเทียบกับใบที่เซิร์ฟเวอร์ส่งมา ____
3. ค่าอุณหภูมิที่เดินทางผ่าน WiFi ของร้านกาแฟต้องไม่ให้คนข้างโต๊ะอ่านได้ ____
4. เซนเซอร์สองตัวของบริษัทเดียวกันแชร์กุญแจลับกันอยู่แล้ว และต้องรู้ว่าข้อความไม่ถูกแก้กลางทาง ____
5. อุปกรณ์กับเซิร์ฟเวอร์ต้องได้กุญแจ AES ร่วมกัน โดยไม่ส่งกุญแจข้ามเครือข่าย ____

<details><summary>เฉลย</summary>

1. **ลายเซ็นดิจิทัล** ให้ความถูกต้องและการยืนยันตัวตน นี่คือหลักของ Protected Update ในบทเรียน 4.2
2. **hash (SHA-256)** ลายนิ้วมือไม่ต้องมีกุญแจ เพราะความเชื่อใจมาจากช่องทางที่เราได้ค่านี้มา (เอกสารที่เราเชื่อ)
3. **การเข้ารหัสแบบสมมาตร** เช่น AES ภายใน TLS ให้ความลับ
4. **MAC (HMAC)** เมื่อมีกุญแจร่วมกันอยู่แล้ว MAC เร็วกว่าลายเซ็น แต่พิสูจน์ต่อบุคคลที่สามไม่ได้
5. **การตกลงกุญแจ (ECDHE)** ได้กุญแจร่วมโดยไม่ส่งกุญแจ แต่ต้องมีลายเซ็นกำกับ ไม่อย่างนั้นอาจตกลงกุญแจกับผู้โจมตีตรงกลาง

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ทำไมฟังก์ชันตรวจลายเซ็นใน `02_model_signature_hook.c` จึงไม่คืน "ผ่าน" แม้ CRC ของส่วนท้ายไฟล์จะถูกต้อง *(เป้าหมายข้อ 1)*
   - ก) เพราะ CRC ช้าเกินไป
   - ข) เพราะใครก็คำนวณ CRC ใหม่ได้ มันบอกว่าข้อมูลไม่เสียระหว่างทาง แต่ไม่บอกว่าใครเขียน
   - ค) เพราะ CRC ต้องใช้กุญแจลับ
   - ง) เพราะ CRC ใช้ได้กับข้อมูลที่เข้ารหัสแล้วเท่านั้น

   <details><summary>เฉลย</summary>

   **ข** การยืนยันว่าใครเป็นผู้สร้างต้องอาศัยกุญแจ ถ้าไม่มีการตรวจด้วยกุญแจ การคืน "ผ่าน" คือการโกหกว่าตรวจแล้ว

   </details>

2. ใบรับรองจากโรงงานในช่อง `0xE0E0` มี subject `CN=InfineonIoTNode` ทุกชิป ข้อสรุปใดถูก *(เป้าหมายข้อ 2)*
   - ก) ใบนี้บอกได้ว่าเป็นอุปกรณ์เครื่องไหน
   - ข) ใบนี้ปลอมแน่นอน
   - ค) ใบนี้พิสูจน์ว่าเป็น Trust M ของแท้ แต่ต้องใช้ serial หรือกุญแจสาธารณะถ้าจะแยกเครื่อง
   - ง) ใบนี้ไม่มีกุญแจสาธารณะ

   <details><summary>เฉลย</summary>

   **ค** ฟิลด์ที่ต่างกันต่อชิปมีแค่ serial กับกุญแจสาธารณะ ใครจะผูกสิทธิ์กับเครื่อง ต้องผูกกับสองค่านี้ ไม่ใช่กับ subject

   </details>

3. ข้อใดอธิบายสิ่งที่ OPTIGA™ Trust M **ไม่ได้** ป้องกัน *(เป้าหมายข้อ 3)*
   - ก) การอ่านกุญแจลับออกมาทำสำเนา
   - ข) การใช้กุญแจลงนามโดยเฟิร์มแวร์ที่ถูกยึดไปแล้ว ขณะที่ผู้โจมตียังคุมบอร์ดอยู่
   - ค) การถอดชิป flash ไปอ่านกุญแจ
   - ง) การเอาไฟล์เฟิร์มแวร์ไปหากุญแจ

   <details><summary>เฉลย</summary>

   **ข** ชิปทำตามคำสั่งของ MCU ที่ต่ออยู่ มันกันการขโมยกุญแจ แต่ไม่รู้ว่า MCU ถูกยึดหรือไม่

   </details>

4. ในค่าตั้ง mbedTLS ของ CM33_NS ที่ commit `ef72c1b` อุปกรณ์จะปฏิเสธใบรับรองของเซิร์ฟเวอร์ที่หมดอายุหรือไม่ *(เป้าหมายข้อ 2)*
   - ก) ปฏิเสธเสมอ
   - ข) ไม่ปฏิเสธด้วยเหตุผลเรื่องวันที่ เพราะ `MBEDTLS_HAVE_TIME_DATE` ถูกปิด
   - ค) ปฏิเสธเฉพาะเมื่อมี CRL
   - ง) ขึ้นกับ broker

   <details><summary>เฉลย</summary>

   **ข** ค่าตั้งนี้ปิดการตรวจช่วงเวลาของใบ และปิดการ parse CRL ด้วย ต้องบันทึกเป็นความเสี่ยงที่เหลือ

   </details>

## แล็บ

**อ่านใบจริง ลงนามจริง** จดผลทุกข้อลงบันทึกการเรียน

- [ ] **1. เก็บห่วงโซ่** บันทึกใบรับรองที่ broker ส่งมาลงไฟล์
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev -showcerts </dev/null 2>/dev/null \
    | awk '/BEGIN CERT/,/END CERT/' > chain.pem
  csplit -s -z -f cert chain.pem '/-----BEGIN CERTIFICATE-----/' '{*}'
  ```
- [ ] **2. อ่านสี่ฟิลด์** ของแต่ละใบ (`cert00`, `cert01`) แล้วกรอกตาราง subject, issuer, notBefore, notAfter, อัลกอริทึมกุญแจ
  ```bash
  openssl x509 -in cert00 -noout -subject -issuer -dates
  openssl x509 -in cert00 -noout -text | grep -A1 'Public Key Algorithm'
  ```
- [ ] **3. เทียบกับ trust anchor ในเฟิร์มแวร์** คำนวณ SHA-256 fingerprint ของใบ intermediate แล้วเทียบกับค่า
  `e3ff5011703755b697227a17945837b7b43616a060d14b37995b62c24e0d7e98` ที่ SDK บันทึกไว้ใน
  [tesaiot_config_defaults.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_defaults.h)
  เป็นค่าของ CA ที่ปักไว้ใน `tesaiot_root_ca.h`
  ```bash
  openssl x509 -in cert01 -noout -fingerprint -sha256
  ```
  ตรงกันไหม แล้วคำทายใน "ดูของจริงก่อน" ถูกหรือเปล่า
- [ ] **4. hash กับ MAC** ลองแก้ข้อความหนึ่งตัวอักษรแล้วดูว่าผลเปลี่ยนแค่ไหน จากนั้นลอง HMAC ด้วยกุญแจทดลอง
  ```bash
  printf 'temp=25.0' | openssl dgst -sha256
  printf 'temp=25.1' | openssl dgst -sha256
  printf 'temp=25.0' | openssl dgst -sha256 -hmac lab-key-not-a-secret
  ```
- [ ] **5. ลายเซ็น** สร้างคู่กุญแจ P-256 บนคอมพิวเตอร์ ลงนาม ตรวจ แล้วแก้ข้อความแล้วตรวจอีกครั้ง
  ```bash
  printf 'temp=25.0' > msg.txt
  openssl ecparam -name prime256v1 -genkey -noout -out lab_key.pem
  openssl ec -in lab_key.pem -pubout -out lab_pub.pem
  openssl dgst -sha256 -sign lab_key.pem -out msg.sig msg.txt
  openssl dgst -sha256 -verify lab_pub.pem -signature msg.sig msg.txt
  printf 'temp=99.9' > msg.txt
  openssl dgst -sha256 -verify lab_pub.pem -signature msg.sig msg.txt
  ```
  ครั้งแรกต้องได้ `Verified OK` ครั้งที่สองต้องได้ `Verification failure`
- [ ] **6. ถามตัวเอง** ไฟล์ `lab_key.pem` อยู่บนดิสก์ของคุณ ใครก็ตามที่คัดลอกไฟล์นี้ไปได้ จะลงนามแทนคุณได้ทุกอย่าง
  เขียนสองสามประโยคว่าบนบอร์ด OPTIGA™ Trust M เปลี่ยนเรื่องนี้อย่างไร และยังเหลือความเสี่ยงอะไร แล้วลบไฟล์กุญแจทดลองทิ้ง

## ไปต่อ

เราเห็นแล้วว่าชิปทำให้กุญแจไม่ต้องออกมาข้างนอก บทต่อไปจะเปิดดูข้างในชิปจริงบน TESAIoT Dev Kit ว่ามี object อะไร metadata บอกอะไร
และคำสั่งไหนเปลี่ยนชิปแบบย้อนกลับไม่ได้

บทเรียนถัดไป: [บทเรียน 2.1: ชิปความปลอดภัยทำอะไรให้เรา](../../m02-optiga-trust-m/l01-secure-element-role/README.md)

## สะท้อนคิด

- ในงานที่ผ่านมา คุณเคยใช้ hash หรือ CRC ในที่ที่จริง ๆ ต้องการการยืนยันตัวตนไหม
- ถ้าอุปกรณ์ของคุณไม่รู้วันที่ปัจจุบัน คุณจะรับมือกับใบรับรองที่หมดอายุอย่างไร
- ใครในองค์กรของคุณบ้างที่เข้าถึงไฟล์ image ของเฟิร์มแวร์ได้ และถ้ากุญแจอยู่ในนั้น จะมีกี่คนที่ "เป็นอุปกรณ์ของคุณ" ได้

## แหล่งอ้างอิง

- [RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [SDK: cm33/security/02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c) (Apache-2.0)
- [SDK: proj_cm33_ns/configs/mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0) รุ่นที่ SDK ใช้
- [Infineon optiga-trust-m-overview (MIT): คุณสมบัติของชิปและ object dump ตัวอย่าง](https://github.com/Infineon/optiga-trust-m-overview/tree/a45b86bda014efeebfb85f084f779cedb07b32dc)
- [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf) ข้อ 5.4
