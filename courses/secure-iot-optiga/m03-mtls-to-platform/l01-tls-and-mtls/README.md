---
id: sec-iot.m03.l01
lang: th
title: {th: TLS และ mTLS, en: TLS and mTLS}
summary: {th: เข้าใจ handshake ของ TLS 1.3 และสิ่งที่เพิ่มขึ้นเมื่ออุปกรณ์ต้องยืนยันตัวตนด้วยใบรับรองของตัวเอง, en: Understand the TLS 1.3 handshake and what changes when the device authenticates with its own certificate.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l02]
objectives:
- {th: วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน, en: Draw the TLS 1.3 handshake and mark where server and device prove their identity.}
- {th: อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา, en: Explain that with a secure element the handshake signature happens inside the chip and the private key never leaves.}
- {th: วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ, en: Diagnose at least three common causes of TLS connection failure.}
develops:
- {skill: sec.tls, to: 3}
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/tesaiot/developer-hub', path: examples/embedded-devices/intermediate/device-mtls, ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21, license: Apache-2.0}
---

# บทเรียน 3.1: TLS และ mTLS

> โมดูล 3 · mTLS สู่ TESAIoT Platform · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

TLS คือเหตุผลที่ telemetry ของเราเดินผ่าน WiFi ร้านกาแฟได้โดยไม่มีใครอ่านหรือแก้ระหว่างทาง
mTLS เพิ่มอีกหนึ่งอย่าง คือให้ **อุปกรณ์** พิสูจน์ตัวด้วยใบรับรองของตัวเองด้วย บทนี้จะดู handshake ทีละข้อความ
ชี้ว่าชิปความปลอดภัยถูกเรียกตรงไหน และฝึกอ่านอาการเมื่อการเชื่อมต่อล้ม

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน
2. อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา
3. วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 2.2: กติกาการเข้าถึงชิป](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md) และไฟล์ `cert01` ที่ตรวจ fingerprint แล้วจากแล็บ [บทเรียน 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **เครื่องมือ:** `openssl` บนคอมพิวเตอร์ แล็บหลักของบทนี้ทำบนคอมพิวเตอร์ ส่วนบนบอร์ดเป็นแล็บเสริมสำหรับคนที่อุปกรณ์ลงทะเบียนกับแพลตฟอร์มแล้ว
- **ถ้าจะทำแล็บเสริมบนบอร์ด:** แม่แบบของ SDK ต้อง apply patch ใน `third_party_patches/` ครบ ตามขั้นตอนใน
  [third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)
  และตรวจด้วย `PATCHED.sha256` ทุกบรรทัดต้องขึ้น `OK` README นั้นเตือนว่าถ้าขาด patch `secure-sockets/0003` เฟิร์มแวร์ยัง build และรันได้ แต่ mTLS จะไม่ได้ใช้กุญแจในชิป และ broker จะปฏิเสธอุปกรณ์
- **อ่านคู่กัน:** [บทเรียน 5.2 ของ TESAIoT Firmware Stack: ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS](../../../tesaiot-firmware-stack/m05-connect-to-platform/l02-mtls/README.md) ซึ่งใช้ตัวอย่างบนคอมพิวเตอร์

## ดูของจริงก่อน

นี่คือ log บน UART ตอนบอร์ดเชื่อมต่อแบบ mTLS ตามบท [C4 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html) (ข้อความตามซอร์ส ค่าจริงแทน `%`)

```text
[MQTT] Waiting for WiFi...
[MQTT] WiFi connected
[MQTT] Start request received
[MQTT-Config] Mode=0, Broker=%s:8883, Client=%s, User=%s, PassLen=%u
[mTLS] Setting up OPTIGA Trust M (cert=0xE0E0, key=0xE0F0)
[mTLS] Certificate read: %u bytes PEM
[mTLS] OPTIGA Trust M setup complete (key_id=%lu)
[MQTT] Instance created
[MQTT] Connecting to '%s:8883' as '%s'...
[PSA-Sign] Using Key OID 0xE0F0 for TLS CertificateVerify (slot=%lu)
[MQTT] Connected to broker
```

**ทายก่อน:** บรรทัดไหนคือตอนที่ชิปลงนาม และบรรทัดนั้นพิสูจน์ได้ไหมว่าการลงนาม **สำเร็จ**
เขียนคำตอบไว้ แล้วไปเทียบในแนวคิดข้อ 2

## แนวคิด

### 1. handshake ของ TLS 1.3 และจุดที่แต่ละฝั่งพิสูจน์ตัว

ภาพนี้สรุปจาก [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) หัวข้อ 2 ข้อความในวงเล็บปีกกา `{}` ถูกเข้ารหัสด้วยกุญแจของ handshake แล้ว

```text
 อุปกรณ์ (client)                                        broker (server)
 ClientHello + key_share + signature_algorithms  ──────▶
                                                  ◀──────  ServerHello + key_share
                                                           {EncryptedExtensions}
                                                           {CertificateRequest}   ← มีเฉพาะเมื่อเซิร์ฟเวอร์ขอ mTLS
                                                           {Certificate}          ← ใบของเซิร์ฟเวอร์และห่วงโซ่
                                                           {CertificateVerify}    ← เซิร์ฟเวอร์ลงนามบน transcript
                                                  ◀──────  {Finished}
 {Certificate}          ← mTLS: ใบของอุปกรณ์
 {CertificateVerify}    ← mTLS: อุปกรณ์ลงนามบน transcript (ในชิป)
 {Finished}                                     ──────▶
 [Application Data: MQTT CONNECT, PUBLISH ...]  ◀─────▶  [Application Data]
```

**เซิร์ฟเวอร์พิสูจน์ตัว** ด้วยสามข้อความ `Certificate` บอกว่าอ้างเป็นใคร อุปกรณ์เดินห่วงโซ่ไปหา trust anchor ที่ปักไว้
`CertificateVerify` คือลายเซ็นบน hash ของบทสนทนาทั้งหมดจนถึงตอนนั้น พิสูจน์ว่าเซิร์ฟเวอร์ถือกุญแจลับของใบนั้นจริง
และ `Finished` ยืนยันว่าทั้งสองฝั่งเห็นบทสนทนาเดียวกัน

**อุปกรณ์พิสูจน์ตัว** ได้ก็ต่อเมื่อเซิร์ฟเวอร์ส่ง `CertificateRequest` มา นั่นคือ mTLS อุปกรณ์ตอบด้วย `Certificate` และ `CertificateVerify` ของตัวเอง
ในโหมด server-TLS ไม่มี `CertificateRequest` อุปกรณ์จึงไปยืนยันตัวทีหลังใน MQTT CONNECT ด้วยชื่อผู้ใช้และรหัสผ่าน ซึ่งเดินในช่องที่เข้ารหัสแล้ว

**ข้อเท็จจริงที่ต้องแยกให้ออก** broker `mqtt.tesaiot.dev` คุย TLS 1.3 ได้ (เห็นในแล็บ) แต่ค่าตั้ง mbedTLS ของ CM33_NS ที่ commit `ef72c1b`
เปิดเฉพาะ `MBEDTLS_SSL_PROTO_TLS1_2` และปิด `MBEDTLS_SSL_PROTO_TLS1_3` คอมเมนต์ในไฟล์บอกเหตุผลว่า TLS 1.3 ต้องใช้ PSA crypto ซึ่งตอนนั้นขัดกับ WiFi
บอร์ดจึงคุย **TLS 1.2** กับ broker ต่างจาก 1.3 สองจุดที่สำคัญต่อความปลอดภัย

- ใน 1.2 เซิร์ฟเวอร์ลงนามบนพารามิเตอร์ ECDHE ในข้อความ `ServerKeyExchange` ไม่ได้ส่ง `CertificateVerify`
- ใน 1.2 ใบรับรองทั้งสองฝั่งเดินแบบ **ไม่เข้ารหัส** ใครดักแพ็กเก็ตได้ก็อ่านใบรับรองของอุปกรณ์ได้ ถ้าใบนั้นมี `device_id` อยู่ใน subject ผู้ดักก็รู้ว่าเป็นอุปกรณ์เครื่องไหน ใน 1.3 ส่วนนี้ถูกเข้ารหัสแล้ว

ฝั่งอุปกรณ์ใน 1.2 ส่ง `Certificate` แล้ว `ClientKeyExchange` แล้ว `CertificateVerify` ลายเซ็นของชิปอยู่ที่ข้อความสุดท้ายนี้เหมือนเดิม

### 2. ลายเซ็นเกิดในชิป กุญแจไม่ออกมา

บท C4 ไล่เส้นทางไว้ครบ ฟังก์ชัน `mqtt_mtls_setup_optiga()` ใน
[mqtt_mtls_setup.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_mtls_setup.c)
เตรียมของก่อน handshake ตามลำดับนี้ (สรุปความ ไม่ได้คัดลอกโค้ด)

1. ถือ touch-hold พร้อมเหตุผล "Preparing secure element for mTLS" เปิด application ของ OPTIGA แล้วเรียก `optiga_manager_init()` **ก่อน** งาน TLS ใด ๆ
2. เลือกตัวตน ถ้า `optiga_verify_cert_key_pair(0xE0E1, 0xE0F1)` ยืนยันว่าใบรับรองกับกุญแจของ TESAIoT เป็นคู่เดียวกัน ใช้คู่นั้น ไม่อย่างนั้นใช้คู่จากโรงงาน `0xE0E0` / `0xE0F0`
3. อ่านใบรับรองจากช่องที่เลือกเป็น PEM แล้วส่งให้ TLS stack ด้วย `cy_tls_set_client_cert()`
4. ลงทะเบียน driver ของชิปกับ PSA แล้วสร้าง **key handle แบบ opaque** ชนิด ECC P-256 ใช้ลงนามได้อย่างเดียว ที่ตำแหน่ง `PSA_KEY_LOCATION_OPTIGA`
   `psa_generate_key()` ตรงนี้ไม่ได้สร้างกุญแจในชิป มันแค่ลงทะเบียน **ชื่อ** ที่ driver แปลงเป็น OID ของกุญแจ
5. ส่ง handle ให้ TLS stack ด้วย `cy_tls_set_optiga_key_id()` ซึ่งมาจาก patch ของ secure-sockets

ระหว่าง handshake เมื่อต้องสร้าง `CertificateVerify` mbedTLS เรียก PSA, PSA ส่งต่อให้ driver `optiga_psa_sign()` และ driver เรียก `trustm_ecdsa_sign()` ด้วย OID ของกุญแจกับ hash
ฟังก์ชันนั้นถือประตูและ touch-hold ตลอดการลงนาม (กติกาจากบทเรียน 2.2) ไม่มีจุดไหนในเส้นทางที่ไบต์ของกุญแจลับออกจากชิป

ถ้า ciphersuite ใช้ SHA-384 driver จะตัด hash เหลือ 256 บิตซ้ายสุดก่อนส่งให้ชิป และนโยบายของ key handle ตั้งเป็น `PSA_ALG_ECDSA(PSA_ALG_ANY_HASH)` เพื่อรองรับกรณีนี้

**คำตอบของคำทาย** บรรทัด `[PSA-Sign] Using Key OID ...` พิมพ์ **ก่อน** การลงนาม บท C4 ย้ำว่ามันแปลแค่ว่า "เริ่มลงนามด้วย OID ที่หาเจอแล้ว"
สัญญาณว่าสำเร็จคือบรรทัดนั้น **และ** ไม่มีบรรทัด `[PSA-Sign] ERROR: trustm_ecdsa_sign status=0x....` ตามมา **และ** ได้ `[MQTT] Connected to broker`
(ใน log ตัวอย่างข้างบนเป็นกรณีคู่จากโรงงาน ถ้าคู่ของ TESAIoT ผ่านการตรวจ log จะมีบรรทัด `[mTLS] device pair verified — using TESAIoT identity` และ OID เป็น `0xE0F1`)

บท C4 ยังบอกวิธีพิสูจน์ว่าชิปเป็นคนลงนามจริง คือตัดชิปออกจากบัสแล้วเชื่อมต่อใหม่ ผลคือการตั้งค่า mTLS ล้มและไม่มีการเชื่อมต่อ เพราะ **ไม่มีกุญแจลับใน flash ให้ถอยไปใช้**
ขั้นนี้แตะฮาร์ดแวร์ของบอร์ด หลักสูตรนี้จึงให้อ่านผลจากเอกสาร ไม่สั่งให้ทำเอง

**mTLS พิสูจน์อะไร และไม่พิสูจน์อะไร** ถ้าอุปกรณ์ใช้คู่จากโรงงาน ใบ `CN=InfineonIoTNode` เหมือนกันทุกชิป handshake จึงพิสูจน์ได้แค่ว่าเป็น Trust M ของแท้
บท C4 สรุปว่าในระดับเฟิร์มแวร์ไม่มีอะไรผูกตัวตนที่อุปกรณ์อ้าง (client id, `device_id`) เข้ากับใบที่มันแสดง ตัวควบคุมที่ตัดสินจริงอยู่ฝั่ง broker
คือ ACL ที่ให้สิทธิ์ `device/{id}/#` เฉพาะ client ที่ใบรับรองถูกปักด้วย fingerprint ของกุญแจสาธารณะหรือ serial ไม่ใช่ด้วย subject
หลังลงทะเบียน (บทเรียน 5.1) ใบในช่อง `0xE0E1` มี subject เป็น `device_id` และออกโดย `TESAIoT MCU CA` ซึ่งผูกตัวตนได้แน่นกว่า

และสิ่งที่ TLS ทั้งแบบธรรมดาและ mTLS **ไม่ได้ป้องกัน**

- ข้อมูลที่พักอยู่บนอุปกรณ์หรือบนแพลตฟอร์ม TLS ปกป้องเฉพาะระหว่างทาง
- ปลายทางที่ถูกเจาะแล้ว ไม่ว่าจะเป็นอุปกรณ์หรือ broker
- ACL ที่ตั้งผิด mTLS บอกว่า "ใคร" แต่ ACL บอกว่า "ทำอะไรได้"
- ใบที่หมดอายุหรือถูกเพิกถอน ในค่าตั้ง mbedTLS ของ CM33_NS ที่ commit นี้ (บทเรียน 1.2)
- การเชื่อมต่อที่ไม่ตรวจใบของเซิร์ฟเวอร์เลย เช่นเส้นทาง HTTPS ใน [03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c) ที่คอมเมนต์บอกว่าตั้ง `CY_AWS_ROOTCA_VERIFY_NONE`
  ข้อมูลยังถูกเข้ารหัส แต่กันได้แค่คนแอบฟัง กันคนที่ดักกลางทางแบบ active ไม่ได้

### 3. อ่านอาการเมื่อการเชื่อมต่อล้ม

ตารางนี้รวมอาการที่ SDK และตัวอย่างบน Developer Hub บันทึกไว้จากการทดลองจริง อ่านจาก log ก่อน อย่าเพิ่งเดา

| อาการที่เห็น | สาเหตุ | ตรวจหรือแก้อย่างไร |
|---|---|---|
| handshake ล้มก่อน MQTT CONNECT ดูไม่เหมือนปัญหารหัสผ่าน | trust anchor ในเฟิร์มแวร์ไม่ตรงกับ CA ของ broker (คอมเมนต์ใน `tesaiot_root_ca.h`) | เทียบ fingerprint ของ CA ที่ broker ส่งกับค่าที่ปักไว้ แบบแล็บ 1.2 |
| อุปกรณ์ส่ง Certificate และ ClientKeyExchange แล้วปิดการเชื่อมต่อ ไม่มี CertificateVerify, mbedTLS รายงาน `-0x4F80` | ไม่ได้เรียก `optiga_manager_init()` ก่อน TLS ลงนามจึงล้มตั้งแต่ขอประตู | ตามบท C4 กับดักข้อ 3 ต้อง init ก่อนงาน TLS |
| `psa_sign_hash()` ปฏิเสธด้วย `PSA_ERROR_NOT_PERMITTED (-133)` ไม่มี CertificateVerify | นโยบายของกุญแจอนุญาตแค่ SHA-256 แต่ ciphersuite ที่ตกลงกันใช้ SHA-384 | นโยบาย `PSA_ALG_ECDSA(PSA_ALG_ANY_HASH)` (สัญญา CSR ข้อ 5.2 และคอมเมนต์ใน `mqtt_mtls_setup.c`) |
| `[PSA-Sign] ERROR: trustm_ecdsa_sign status=0x0102` | ชิปกับจอสัมผัสชนกันบน I2C | touch-hold ไม่ครอบทั้งธุรกรรม หรือมีการ resume ดิบ (บทเรียน 2.2) |
| TLS ปิดการเชื่อมต่อหลัง CONNECT ในโหมด server-TLS | ต่อพอร์ต 8883 ซึ่งเป็นพอร์ตของ mTLS | server-TLS ใช้ 8884 ตาม README ของ device-servertls บนบอร์ดพอร์ตมาจาก `tls_mode` ไม่ใช่ `port=` |
| เชื่อมต่อครั้งแรกของการบูตได้ ครั้งหลังจาก disconnect ล้มด้วย `-0x3E80` | TLS teardown ลบ key handle ใน PSA ไปแล้ว | เฟิร์มแวร์ปัจจุบันตรวจแล้วตั้งค่าใหม่ ถ้าเห็น log `PSA key ... no longer exists` แล้วต่อได้ แปลว่าปกติ |

## ตัวอย่างสมบูรณ์

ตัวอย่าง [device-mtls](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) บน Developer Hub
ทำ mTLS แบบเดียวกันบนคอมพิวเตอร์ (ภาษา C กับ Mongoose) ตัดจาก
[main.c](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c) บรรทัด 335–343 และ 385–387
(© 2025 TESAIoT Platform (TESA), Apache-2.0)

```c
  /* Resolve credential files */
  char ca[512], crt[512], key[512];
  join_path(ca,  sizeof(ca),  certs_dir, FILE_CA_CHAIN);
  join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
  join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
  if (!(file_exists(crt) && file_exists(key))) {
    (void)fprintf(stderr, "mTLS requires client_cert.pem and client_key.pem in %s\n", certs_dir);
    return 1;
  }
```

```c
  /* Mongoose TLS base conf (we may tweak CA per mode below) */
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.client_cert = crt; tls.client_key = key;
```

เทียบสองโลก บนคอมพิวเตอร์ กุญแจลับคือ **ไฟล์** `client_key.pem` ที่ TLS library อ่านเข้า RAM ใครคัดลอกไฟล์ได้ก็เป็นอุปกรณ์นี้ได้
บนบอร์ด ตำแหน่งเดียวกันในโค้ดคือ `cy_tls_set_optiga_key_id()` ที่ส่งแค่ **ชื่อ** ของกุญแจ แล้วทุกการลงนามวิ่งเข้าชิป
README ของตัวอย่างนี้ก็ระบุว่า bundle ที่มาจากการลงทะเบียนด้วย CSR จะไม่มีกุญแจลับอยู่ใน ZIP ด้วยเหตุผลด้านความปลอดภัย

อีกเรื่องที่ควรเห็นในไฟล์เดียวกัน เส้นทาง MQTTS ตั้ง `tls.ca_chain = NULL` เพื่อใช้ trust store ของระบบปฏิบัติการ คอมเมนต์เขียนไว้ตอนแพลตฟอร์มยังใช้โดเมนเดิมที่มี CA สาธารณะ
broker `mqtt.tesaiot.dev` ที่เราเห็นในบทเรียน 1.2 ใช้ CA ของ TESAIoT เอง ซึ่งไม่อยู่ใน trust store ของระบบ ถ้าจะใช้ตัวอย่างนี้กับ broker นี้ ต้องชี้ `ca_chain` ไปที่ไฟล์ CA ที่ตรวจแล้ว
แล็บข้อ 4 จะให้คุณเห็นอาการนี้เอง

ลองเปิดตัวอย่างบน Developer Hub

- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) สำหรับเทียบกับโหมด server-TLS

## ฝึกเติม

เรียงข้อความ handshake ของ TLS 1.3 แบบ mTLS ให้ถูก แล้วเขียน **S** กำกับข้อความที่เซิร์ฟเวอร์พิสูจน์ตัว และ **D** กำกับข้อความที่อุปกรณ์พิสูจน์ตัว

`Finished (อุปกรณ์)` · `ServerHello` · `CertificateVerify (อุปกรณ์)` · `ClientHello` · `Certificate (เซิร์ฟเวอร์)` · `CertificateRequest` · `Certificate (อุปกรณ์)` · `CertificateVerify (เซิร์ฟเวอร์)` · `EncryptedExtensions` · `Finished (เซิร์ฟเวอร์)`

<details><summary>เฉลย</summary>

1. `ClientHello`
2. `ServerHello`
3. `EncryptedExtensions`
4. `CertificateRequest` (เซิร์ฟเวอร์ขอให้อุปกรณ์พิสูจน์ตัว ข้อความนี้เองยังไม่ได้พิสูจน์อะไร)
5. `Certificate (เซิร์ฟเวอร์)` **S**
6. `CertificateVerify (เซิร์ฟเวอร์)` **S**
7. `Finished (เซิร์ฟเวอร์)` **S** ยืนยันว่าบทสนทนาไม่ถูกแก้
8. `Certificate (อุปกรณ์)` **D**
9. `CertificateVerify (อุปกรณ์)` **D** ข้อความนี้คือที่ OPTIGA™ Trust M ลงนาม
10. `Finished (อุปกรณ์)` **D**

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ใน mTLS อุปกรณ์พิสูจน์ว่าถือกุญแจลับของใบรับรองจริงด้วยข้อความใด *(เป้าหมายข้อ 1)*
   - ก) ClientHello
   - ข) Certificate
   - ค) CertificateVerify
   - ง) EncryptedExtensions

   <details><summary>เฉลย</summary>

   **ค** `Certificate` แค่บอกว่าอ้างเป็นใคร ใครก็ส่งใบของคนอื่นได้ `CertificateVerify` คือลายเซ็นบน transcript ที่ทำได้เฉพาะคนถือกุญแจลับ

   </details>

2. `psa_generate_key()` ใน `mqtt_mtls_setup_optiga()` ทำอะไร *(เป้าหมายข้อ 2)*
   - ก) สร้างคู่กุญแจใหม่ในชิปทุกครั้งที่เชื่อมต่อ
   - ข) คัดลอกกุญแจลับจากชิปมาไว้ใน RAM
   - ค) ลงทะเบียน handle แบบ opaque ที่ driver แปลงเป็น OID ของกุญแจในชิป ไม่ได้สร้างอะไรในชิป
   - ง) สร้างกุญแจ AES สำหรับ TLS record

   <details><summary>เฉลย</summary>

   **ค** บท C4 ระบุว่า handle นี้ไม่เก็บเนื้อกุญแจ เก็บแค่ชื่อของกุญแจที่อยู่ในชิป

   </details>

3. log แสดง `[PSA-Sign] Using Key OID 0xE0F1 for TLS CertificateVerify` แล้วการเชื่อมต่อถูกปิด ข้อสรุปใดถูก *(เป้าหมายข้อ 3)*
   - ก) ชิปลงนามสำเร็จแล้ว ปัญหาอยู่ที่ broker แน่นอน
   - ข) บรรทัดนี้พิมพ์ก่อนการลงนาม ต้องดูต่อว่ามีบรรทัด ERROR ของ `trustm_ecdsa_sign` หรือไม่ ก่อนสรุป
   - ค) กุญแจหลุดออกจากชิป
   - ง) ต้องเปลี่ยนพอร์ตเป็น 8884

   <details><summary>เฉลย</summary>

   **ข** บรรทัดนี้แปลแค่ว่าเริ่มลงนามแล้ว ถ้าตามด้วย `status=0x0102` ให้กลับไปดูบทเรียน 2.2 ถ้าไม่มี ERROR ให้ดูฝั่ง broker และ ACL ต่อ

   </details>

4. ทำไมใน TLS 1.2 ผู้ที่ดักแพ็กเก็ตได้จึงอาจรู้ว่าเป็นอุปกรณ์เครื่องไหน แม้ข้อมูล MQTT จะถูกเข้ารหัส *(เป้าหมายข้อ 1)*
   - ก) เพราะรหัสผ่านถูกส่งแบบไม่เข้ารหัส
   - ข) เพราะใบรับรองของทั้งสองฝั่งใน handshake ของ TLS 1.2 เดินแบบไม่เข้ารหัส
   - ค) เพราะ TLS 1.2 ไม่มีการเข้ารหัสเลย
   - ง) เพราะ MQTT CONNECT อยู่นอก TLS

   <details><summary>เฉลย</summary>

   **ข** ใน TLS 1.3 ใบรับรองอยู่ในส่วนที่เข้ารหัสแล้ว เรื่องนี้ควรลงในช่องความเสี่ยงที่เหลือของ threat model เพราะเฟิร์มแวร์ที่ commit นี้คุย TLS 1.2

   </details>

## แล็บ

**เห็น handshake จริงจากคอมพิวเตอร์ของคุณ** ใช้ไฟล์ `cert01` ที่ fingerprint ตรงกับค่าใน SDK แล้ว (แล็บ 1.2 ข้อ 3) เป็น trust anchor

- [ ] **1. server-TLS บน TLS 1.3** ดูสถานะทีละข้อความ แล้วจับคู่แต่ละบรรทัดกับแผนภาพในแนวคิดข้อ 1
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev \
    -state -CAfile cert01 -partial_chain </dev/null 2>&1 | grep -E '^SSL_connect|Verify return'
  ```
  ต้องเห็น `read server certificate` ตามด้วย `TLSv1.3 read server certificate verify` และ `Verify return code: 0 (ok)` วงบรรทัดที่เซิร์ฟเวอร์พิสูจน์ตัว
- [ ] **2. บังคับ TLS 1.2 แบบที่บอร์ดใช้** เพิ่ม `-tls1_2` ในคำสั่งเดิม บรรทัดไหนหายไป บรรทัดไหนเพิ่มมา (มองหา `read server key exchange`) แล้วเขียนว่าใน 1.2 เซิร์ฟเวอร์ลงนามที่ไหน
- [ ] **3. พอร์ต mTLS โดยไม่มีใบของอุปกรณ์** ต่อพอร์ต 8883 แบบเดียวกัน
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8883 -servername mqtt.tesaiot.dev \
    -state -CAfile cert01 -partial_chain </dev/null 2>&1 | grep -E '^SSL_connect|alert|Verify return'
  ```
  หาบรรทัด `read server certificate request` แล้วดูว่าเซิร์ฟเวอร์ตอบอย่างไรเมื่ออุปกรณ์ (ในที่นี้คือ openssl) ไม่มีใบให้ ลองซ้ำด้วย `-tls1_2` แล้วเทียบข้อความ alert ของสองรุ่น
- [ ] **4. ลืม trust anchor** รันข้อ 1 ใหม่โดยตัด `-CAfile cert01 -partial_chain` ออก บันทึกค่า `Verify return code` แล้วอธิบายว่าถ้าอุปกรณ์หรือโปรแกรมของคุณไม่มี CA ตัวนี้ จะเกิดอะไร
- [ ] **5. วินิจฉัย** เลือกอาการสามแถวจากตารางแนวคิดข้อ 3 เขียนว่าจะจำลองอาการนั้นอย่างไร (บนคอมพิวเตอร์หรือบนบอร์ด) และจะดูหลักฐานจากตรงไหน
- [ ] **แล็บเสริมบนบอร์ด** ถ้าอุปกรณ์ของคุณมี `device_id` บนแพลตฟอร์มและ patch ครบแล้ว ตั้ง `tls_mode=mtls` ในไฟล์ `/.tesaiot_config` แล้วสั่งเชื่อมต่อจากหน้า TESAIoT บนจอ
  จด log ทุกบรรทัดที่ขึ้นต้นด้วย `[mTLS]` และ `[PSA-Sign]` แล้วตัดสินตามเกณฑ์สามข้อในแนวคิดข้อ 2 ว่าการลงนามสำเร็จหรือไม่ บทเรียน 3.2 จะพาตั้งค่าไฟล์นี้ละเอียดขึ้น

## ไปต่อ

ตอนนี้เรารู้ว่าช่องทางปลอดภัยอย่างไร บทต่อไปจะตามเส้นทางของข้อมูลทั้งเส้น ตั้งแต่ไฟล์ตั้งค่าบนบอร์ด task ของ MQTT จนถึง broker
พร้อมต่อ WiFi ด้วยข้อมูลรับรองจากที่เก็บ และเปรียบเทียบ MQTTs กับ HTTPS

บทเรียนถัดไป: [บทเรียน 3.2: MQTTs ขึ้น TESAIoT Platform](../l02-mqtts-to-tesaiot/README.md)

## สะท้อนคิด

- ในงานของคุณ ถ้าใบรับรองของอุปกรณ์เดินแบบไม่เข้ารหัสใน handshake ใครได้ประโยชน์จากข้อมูลนั้นบ้าง
- ถ้าตัวตนของอุปกรณ์พิสูจน์ได้ด้วย mTLS แล้ว ทำไมยังต้องมี ACL ฝั่ง broker
- log บรรทัดไหนในระบบของคุณที่ดูเหมือนสำเร็จ แต่จริง ๆ พิมพ์ก่อนงานจะเกิด

## แหล่งอ้างอิง

- [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [SDK: tesaiot_mqtt/mqtt_mtls_setup.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_mtls_setup.c) (ลิงก์ ไม่ได้คัดลอก)
- [SDK: proj_cm33_ns/configs/mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h)
- [SDK: third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)
- [SDK: CSR_SUBMISSION_CONTRACT.md ข้อ 5.2 (CertificateVerify กับกุญแจใน OPTIGA)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- ตัวอย่างบน Developer Hub (Apache-2.0): [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
