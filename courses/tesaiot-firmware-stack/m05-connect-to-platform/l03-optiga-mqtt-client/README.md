---
id: fw-stack.m05.l03
lang: th
title:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
summary:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [eva-kit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M"
    en: "Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M"
  - th: "เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง"
    en: "Connect MQTT over TLS with the certificate stored in OPTIGA, following the example"
develops:
  - {skill: sec.secure-element, to: 2}
  - {skill: sec.tls, to: 3}
  - {skill: sec.fundamentals, to: 2}
context: {platform: psoc-edge-e84, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/security/pse84_tesaiot_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป

## เป้าหมาย

1. อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M
2. เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง

## แนวคิด

### OPTIGA Trust M คืออะไร และทำไมกุญแจถึงไม่ออกจากชิป

OPTIGA™ Trust M เป็น secure element (ชิปความปลอดภัยแยกต่างหาก ระดับ CC EAL6+) ที่เชื่อมกับ PSoC Edge E84 ผ่าน I2C ชิปนี้สร้างและเก็บคู่กุญแจ ECC P-256 ไว้ภายในตัวเอง โดยที่เฟิร์มแวร์สั่งให้ชิป "เซ็นข้อมูล" ได้ แต่ไม่มีทางอ่านตัวกุญแจส่วนตัวออกมาได้เลย แม้จะ dump หน่วยความจำของ MCU ก็ตาม เพราะกุญแจไม่เคยเข้ามาอยู่ใน RAM ของ MCU ตั้งแต่แรก งานอื่นของ TLS เช่นการเข้ารหัสข้อมูลระหว่างส่งยังทำโดย mbedTLS บน MCU ตามปกติ มีแค่ขั้นตอนที่ต้องใช้กุญแจส่วนตัว (การเซ็นระหว่าง TLS handshake) เท่านั้นที่ถูกส่งต่อไปให้ชิปทำแทน

### OID: แผนที่ของกุญแจและใบรับรองในชิป

OPTIGA จัดเก็บข้อมูลเป็นช่อง (object) แต่ละช่องมีหมายเลข OID กำกับ ตัวอย่างนี้ใช้ช่องหลักดังนี้: `0xE0C2` เก็บ Factory UID (หมายเลขประจำฮาร์ดแวร์ อ่านได้อย่างเดียว 27 ไบต์) `0xE0E0` เก็บ Factory Certificate (ใบรับรองที่ provision มาจากโรงงาน) คู่กับกุญแจที่ `0xE0F0` `0xE0E1` เก็บ Device Certificate (ใบรับรองที่แพลตฟอร์ม TESAIoT ออกให้ผ่าน Protected Update) คู่กับกุญแจที่ `0xE0F1` และ `0xE0E3` เก็บ trust anchor (ROOT_CA) ที่ใช้ตรวจลายเซ็นของ Protected Update แต่ละใบรับรองต้องใช้คู่กับกุญแจที่ OID ตรงกันเสมอ (`0xE0E0`↔`0xE0F0`, `0xE0E1`↔`0xE0F1`) ใช้ผิดคู่จะเซ็น TLS handshake ไม่ตรงกับใบรับรองที่ยื่นออกไป

### สิทธิ์การเข้าถึง: อ่านกุญแจไม่ได้ แต่สั่งให้เซ็นได้

ตาราง OID Access Conditions ในเอกสารต้นทางกำหนดไว้ชัดเจนว่าช่องกุญแจ `0xE0F0` และ `0xE0F1` มีสิทธิ์ Read = Never (อ่านออกมาไม่ได้เด็ดขาด) แต่ Execute = Always (สั่งให้ใช้เซ็นได้เสมอ เช่นระหว่าง TLS handshake) ส่วนช่องใบรับรอง `0xE0E0` เป็น Change = Never (แก้ไม่ได้อีกหลัง provision) ขณะที่ `0xE0E1` เขียนใหม่ได้ (`Change = Always*`) แต่การเปลี่ยนสิทธิ์ metadata ถูกล็อกไว้เมื่อ lifecycle state (`LcsO`) เข้าสถานะ Operational (`0x07`) แล้ว การอ่านไม่ได้แต่ใช้ได้แบบนี้คือหัวใจของ "hardware root of trust": ต่อให้เฟิร์มแวร์มีช่องโหว่หรือถูก debug เข้าไปอ่านหน่วยความจำ ก็ยังคัดลอกกุญแจออกมาไม่ได้ ต่างจากกุญแจที่เก็บใน flash ของ MCU ซึ่งอ่านออกมาได้ด้วย debugger หรือช่องโหว่ของเฟิร์มแวร์

### Two-Certificate PKI และ SAFE MODE: ทำไมต้องมีใบรับรองสองชุด

ตัวอย่างนี้ใช้ใบรับรองสองชุดคู่กัน คือ Factory Certificate (`0xE0E0`+`0xE0F0`, provision มาจากโรงงาน ใช้สำหรับ bootstrap/กู้ระบบ) และ Device Certificate (`0xE0E1`+`0xE0F1`, แพลตฟอร์ม TESAIoT ออกให้ผ่าน Protected Update ใช้งานจริงในโหมดปกติ) หลังเปิดเครื่องหรือรีเซ็ตทุกครั้ง เฟิร์มแวร์เข้าสู่ "SAFE MODE" โดยตั้งค่า `g_force_factory_cert = true` เป็นค่าเริ่มต้น บังคับให้ใช้ Factory Certificate ก่อนเสมอ README ต้นทางอธิบายเหตุผลไว้ว่า ใบรับรองอุปกรณ์ (`0xE0E1`) อาจไม่ตรงกับกุญแจอุปกรณ์ (`0xE0F1`) หลังรีเซ็ต เพราะการจับคู่กุญแจที่เพิ่งถูก provision อยู่ในหน่วยความจำชั่วคราวจนกว่าใบรับรองจะถูกเขียนสำเร็จ ขณะที่ Factory Certificate กับ Factory Key ถูกจับคู่กันไว้ถูกต้องเสมอ การเริ่มต้นด้วย Factory Certificate จึงรับประกันว่าการเชื่อมต่อ MQTT ใช้งานได้เสมอสำหรับกู้ระบบ จากนั้นผู้ใช้งานจึงเลือกรัน Protected Update เพื่อสลับไปใช้ Device Certificate

### ลำดับขั้นตอนขอใบรับรองใช้งาน (Protected Update workflow)

ลำดับของการได้มาซึ่ง Device Certificate คือ (1) OPTIGA สร้างคู่กุญแจ ECC P-256 ขึ้นภายในชิปเอง (ที่ OID `0xE0F1`) (2) สร้าง CSR (Certificate Signing Request) ที่ลงนามด้วยกุญแจในชิปนั้น (3) เชื่อมต่อ MQTT ด้วย Factory Certificate ก่อน (ตาม SAFE MODE) แล้วส่ง CSR ขึ้นแพลตฟอร์ม (4) แพลตฟอร์มออกใบรับรองแล้วส่ง manifest ของ Protected Update ที่ลงนามแล้วกลับมา (5) OPTIGA ตรวจลายเซ็นของ manifest กับ trust anchor ที่ `0xE0E3` ก่อน ถ้าลายเซ็นไม่ตรงจะปฏิเสธไม่เขียนทับ ถ้าตรงจึงเขียนใบรับรองใหม่ลง OID `0xE0E1` ตลอดกระบวนการนี้ private key ที่ `0xE0F1` ไม่เคยออกจากชิปเลย มีแต่ CSR (ที่มี public key) และใบรับรองที่เดินทางผ่านเครือข่าย การตรวจลายเซ็น manifest ก่อนเขียนทุกครั้งคือสิ่งที่ทำให้การอัปเดตใบรับรองปลอมถูกปฏิเสธ

### การเชื่อมต่อ MQTT over TLS ด้วยกุญแจใน OPTIGA: ผูก TLS เข้ากับ secure element ตอน boot

ตอนเริ่มต้นโปรแกรม เฟิร์มแวร์อ่านใบรับรองปัจจุบันจาก OPTIGA (`read_certificate_from_optiga()`) แล้วลงทะเบียนไดรเวอร์ secure element ของ OPTIGA เข้ากับ PSA Crypto (`optiga_psa_register()` ตามด้วย `psa_crypto_init()`) จากนั้นสร้าง PSA key handle ที่ระบุ `PSA_KEY_LOCATION_OPTIGA` ผ่าน `psa_generate_key()` — คำว่า "generate" ในที่นี้หมายถึงการผูก (attach) handle ของ PSA เข้ากับ OID ที่มีกุญแจอยู่แล้วจากโรงงาน ไม่ได้สร้างกุญแจใหม่ในขั้นนี้ แล้วจึงผูก TLS layer เข้ากับกุญแจนั้นด้วย `cy_tls_set_optiga_key_id()` และตั้งใบรับรองของ TLS ด้วย `cy_tls_set_client_cert()` เมื่อเชื่อมต่อ MQTT broker ของแพลตฟอร์ม (พอร์ต `8883` เมื่อเปิด mutual-auth) ระหว่าง TLS handshake ขั้น CertificateVerify mbedTLS จะเรียกกลับเข้าไดรเวอร์นี้ให้เซ็นแฮชด้วยกุญแจที่ OID ที่เลือกไว้ (`0xE0F0` หรือ `0xE0F1` แล้วแต่ว่ากำลังใช้ใบรับรองใด) ผลลัพธ์คือลายเซ็น ECDSA ที่ส่งกลับไปให้ mbedTLS ใช้ในแพ็กเก็ต handshake ต่อ โดยไม่มีไบต์ของกุญแจเองไหลผ่าน RAM ของ MCU เลย

## ตัวอย่างสมบูรณ์

> **ก่อนรันตัวอย่าง (ตรวจเมื่อ 26 ก.ย. 2026):** `mqtt_client_config.h` ของตัวอย่างที่ commit นี้ยังตั้ง `MQTT_BROKER_ADDRESS` และ `MQTT_SNI_HOSTNAME` เป็นชื่อ MQTT เดิมของแพลตฟอร์มที่ลงท้ายด้วย .com
> ชื่อนี้ยังใช้ได้ชั่วคราว แต่แพลตฟอร์มย้ายไปเป็น tesaiot.dev แล้ว ให้ตั้งทั้งสองค่าเป็น `mqtt.tesaiot.dev` (บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

โค้ดของตัวอย่างนี้อยู่ใน Developer Hub (อ้างอิงที่ commit `d2ed42c`) — อ่าน [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/README.md) เพื่อเข้าใจตาราง OID, PKI สองใบรับรอง และ SAFE MODE ฉบับเต็ม แล้วไล่โค้ดตามลำดับนี้ (รันบนบอร์ด PSoC Edge E84 พร้อม OPTIGA™ Trust M โปรเจกต์นี้มี BSP ของ Eva Kit: APP_KIT_PSE84_EVAL_EPC2)

- [`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/main.c#L491-L536) — ลำดับตอน boot: อ่านใบรับรองจาก OPTIGA, ลงทะเบียน PSA secure-element driver, ผูก TLS เข้ากับกุญแจใน OPTIGA
- [`optiga_psa_se.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_psa_se.c#L285-L323) — ฟังก์ชันเซ็น (`optiga_psa_sign`) ที่ mbedTLS เรียกระหว่าง TLS handshake เพื่อขอให้ OPTIGA เซ็นแฮชด้วยกุญแจที่ OID ที่เลือกไว้
- [`optiga_trust_helpers.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_trust_helpers.c#L768-L824) — `trustm_gen_ecc_keypair()` ที่เรียก `optiga_crypt_ecc_generate_keypair()` พร้อม `export_private=false` คือส่วนที่ทำให้กุญแจที่สร้างในชิปไม่เคยถูกส่งออกมา
- [`mqtt_task.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/mqtt_task.c#L824-L834) — การเลือกใบรับรอง (`tesaiot_select_mqtt_certificate()`) แล้วสลับ OID ของกุญแจให้ตรงกับใบรับรองที่เลือกก่อนเชื่อมต่อทุกครั้ง
- ดูโฟลเดอร์เต็มที่ [`examples/security/pse84_tesaiot_client/`](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client)
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

โค้ดชุดนี้อยู่ภายใต้ Cypress (Infineon) EULA จึงอ้างอิงด้วยลิงก์เท่านั้น ไม่คัดลอกเนื้อโค้ดลงในบทเรียนนี้

## จุดที่มักพลาด

- **คิดว่าโค้ดตัวอย่างนี้ generate กุญแจใหม่ทุกครั้งที่บอร์ด boot** — `psa_generate_key()` ในที่นี้แค่ผูก PSA key handle เข้ากับ OID ที่มีกุญแจอยู่แล้วจากโรงงาน (`OPTIGA_TLS_ATTACH_ONLY`) ไม่ได้สร้างกุญแจใหม่ทุกครั้ง กุญแจจริงถูกสร้างครั้งเดียวตอน provision (สำหรับ Factory Key) หรือระหว่าง Protected Update workflow (สำหรับ Device Key)
- **ใช้ใบรับรองกับกุญแจคนละ OID กัน** — ใบรับรอง `0xE0E0` ต้องคู่กับกุญแจ `0xE0F0` และ `0xE0E1` ต้องคู่กับ `0xE0F1` เท่านั้น โค้ดใน `mqtt_task.c` จึงสลับ `optiga_psa_set_signing_key_oid()` ให้ตรงกับใบรับรองที่เลือกทุกครั้งก่อนเชื่อมต่อ ถ้าลืมสลับ TLS handshake จะเซ็นด้วยกุญแจที่ไม่ตรงกับใบรับรอง
- **คิดว่ารีเซ็ตบอร์ดแล้วจะได้ Device Certificate ทันที** — ทุกครั้งที่ reset เฟิร์มแวร์กลับไปที่ SAFE MODE (ใช้ Factory Certificate) ก่อนเสมอ ต้องรัน Protected Update ใหม่ทุกครั้งถ้าต้องการสลับไปใช้ Device Certificate
- **รัน `make getlibs` ใหม่แล้วลืมรัน `./apply_patches.sh`** — README ต้นทางเตือนว่า patch จะถูกล้างไปพร้อม library `secure-sockets` จะใช้กุญแจใน OPTIGA ระหว่าง TLS handshake ไม่ได้อีก ต้องรัน `./apply_patches.sh` ใหม่ทุกครั้งหลัง `make getlibs`

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม private key ที่อยู่ใน secure element ปลอดภัยกว่าใน flash
- Protected Update ใช้ทำอะไรกับ certificate

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client)
- โค้ดชุดนี้อยู่ภายใต้ Cypress (Infineon) EULA จึงอ้างอิงด้วยลิงก์เท่านั้น

