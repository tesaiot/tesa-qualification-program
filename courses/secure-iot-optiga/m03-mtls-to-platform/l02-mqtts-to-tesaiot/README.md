---
id: sec-iot.m03.l02
lang: th
title: {th: MQTTs ขึ้น TESAIoT Platform, en: MQTTs to the TESAIoT Platform}
summary: {th: ตามเส้นทางตั้งแต่ไฟล์ตั้งค่า งาน MQTT จนถึง broker และส่งข้อมูลขึ้นแพลตฟอร์มผ่านการเชื่อมต่อที่เข้ารหัส, en: 'Follow the path from config file to MQTT task to broker, and publish to the platform over an encrypted link.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l01]
objectives:
- {th: อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น, en: Explain the data path from config file through the MQTT task to the TESAIoT broker.}
- {th: เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด, en: Join WiFi with credentials from a store rather than hard-coded in source.}
- {th: เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน, en: Compare MQTTs and HTTPS for a device and choose for the job.}
develops:
- {skill: sec.tls, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: proto.mqtt, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/tesaiot/developer-hub', path: examples/embedded-devices/entry/device-servertls, ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21, license: Apache-2.0}
---

# บทเรียน 3.2: MQTTs ขึ้น TESAIoT Platform

> โมดูล 3 · mTLS สู่ TESAIoT Platform · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

บทที่แล้วดูช่องทางที่ปลอดภัย บทนี้ดูของที่วิ่งในช่องนั้นทั้งเส้น ตั้งแต่ไฟล์ตั้งค่าบนบอร์ด task ของ MQTT จนถึง broker
พร้อมต่อ WiFi โดยไม่มีรหัสผ่านสักตัวอยู่ในซอร์สโค้ด และตัดสินใจว่าเมื่อไรควรใช้ HTTPS แทน MQTTs

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น
2. เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด
3. เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 3.1: TLS และ mTLS](../l01-tls-and-mtls/README.md)
- **บนแพลตฟอร์ม:** อุปกรณ์หนึ่งเครื่องที่ลงทะเบียนบน TESAIoT Platform แล้ว และ **Server-TLS bundle สำหรับ MQTT** ของอุปกรณ์นั้น
  README ของตัวอย่าง [device-servertls](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) บอกว่า bundle มี `ca-chain.pem`, `endpoints.json` และไฟล์ข้อมูลรับรอง MQTT
  ต้องเลือก `include_password` ตอนดาวน์โหลดจึงจะได้รหัสผ่าน **ห้ามนำไฟล์เหล่านี้ขึ้น repository ใด ๆ**
- **บนคอมพิวเตอร์:** `mosquitto_sub` และ `mosquitto_pub` (แพ็กเกจ mosquitto-clients)
- **อ่านคู่กัน:** [บทเรียน 5.1 ของ TESAIoT Firmware Stack: ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS](../../../tesaiot-firmware-stack/m05-connect-to-platform/l01-server-tls/README.md)

## ดูของจริงก่อน

นี่คือไฟล์ `/.tesaiot_config` หน้าตาแบบที่บอร์ดอ่านตอนบูต รูปแบบเป็น `key=value` ทีละบรรทัด ชื่อ key ตรงกับตัว parse ใน
[tesaiot_config_store.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_store.c) ค่าในวงเล็บแหลมคือช่องที่คุณต้องเติมเอง

```ini
tls_mode=server_tls
broker=mqtt.tesaiot.dev
port=1883
device_id=<device_id จากแพลตฟอร์ม>
mqtt_pass=<รหัสผ่าน MQTT จาก bundle>
keepalive=60
wifi_ssid=<ชื่อ WiFi>
wifi_pass=<รหัส WiFi>
wifi_security=WPA2
```

**ทายก่อน:** บอร์ดจะต่อ broker ที่พอร์ตไหน 1883 ตามบรรทัด `port=` หรือพอร์ตอื่น แล้วรหัสผ่านสองตัวในไฟล์นี้จะไปโผล่ที่ไหนบ้างระหว่างการเชื่อมต่อ

## แนวคิด

### 1. เส้นทางจากไฟล์ตั้งค่าถึง broker

บท [C3 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html) ไล่เส้นทางนี้ไว้ ภาพข้างล่างสรุปเป็นขั้น

```text
/.tesaiot_config  (LittleFS, key=value)
   │  tesaiot_config_init() ตอนบูต  (mtb-only: เรียกจาก main())
   ▼
tesaiot_mqtt_connect()   ← ปุ่ม Connect บนหน้า TESAIoT (IPC_CMD_TESAIOT_CONNECT)
   │                       ← tesaiot.connect() บน variant mtb-mpy
   │                       ← งานลงทะเบียนของ HSM ก่อนแตะชิป (บทเรียน 5.1)
   ▼
mqtt_request_start()     สร้าง task "MQTT" ตอนถูกขอครั้งแรก ไม่ใช่ตอนบูต
   ▼
mqtt_client_task         รอ WiFi ด้วย app_wifi_is_ready() นานสุด 60 วินาที แล้วรอสัญญาณเริ่ม
   ▼
mqtt_client_config_init() เลือก host, พอร์ตจาก tls_mode, SNI, client id, ชื่อผู้ใช้/รหัสผ่าน, root CA
   │                       (ถ้าเป็น mTLS ต่อด้วย mqtt_mtls_setup_optiga() ของบทเรียน 3.1)
   ▼
cy_mqtt_connect()        ลองซ้ำตาม max_retries ── TLS 1.2 ──▶ mqtt.tesaiot.dev
   ├─ publisher_task  ◀── คิว ◀── tesaiot_mqtt_publish()   ค่าเริ่มต้น device/<device_id>/telemetry
   └─ subscriber      device/<device_id>/commands/#  เลือก handler ตามท้ายชื่อหัวข้อ บน event thread ของ MQTT
```

`tls_mode` เป็นตัวตัดสินหลายอย่างพร้อมกัน ตาม [mqtt_client_config.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_client_config.c)

| `tls_mode` | พอร์ต | client id | ชื่อผู้ใช้ | รหัสผ่าน |
|---|---|---|---|---|
| `mtls` (0), `mtls_sw` (1) | 8883 | `factory_uid` (ถ้าว่างใช้ `device_id`) | `mtls_device_id` | ว่าง ยืนยันตัวด้วยใบรับรอง |
| `server_tls` (2, ค่าเริ่มต้น) | 8884 | `device_id` | `device_id` | `mqtt_pass` |

คำตอบของคำทายข้อแรกจึงคือ **8884** บรรทัด `port=` ถูกเก็บไว้ แต่ไม่ถูกใช้กับ MQTT เลย บท C3 ตั้งเป็นกับดักข้อ 1 ไว้
ถ้า broker ของคุณฟังพอร์ตอื่น ต้องแก้ switch ในโค้ด ไม่มีทางแก้จากไฟล์ตั้งค่า
ส่วนรหัสผ่าน MQTT ไปโผล่ใน MQTT CONNECT ซึ่งวิ่ง **ข้างใน** TLS แล้ว และบน console พิมพ์ออกมาแค่ `PassLen`

กับดักอื่นที่ C3 และสัญญา CSR ของ SDK บันทึกไว้ และจะใช้ในแล็บ

- **คิวของ publisher ไม่รอ** `tesaiot_mqtt_publish()` ใส่คิวแบบรอศูนย์วินาที คิวเต็มข้อความทิ้งเงียบ ส่งรัว ๆ ข้อมูลหาย
- **handler ของ subscriber วิ่งบน event thread ของ MQTT** งานที่ block หรือแตะชิปต้องส่งต่อเข้าคิวไปให้ task ของคุณ
- **ต้องมีคนดูแล session** broker ตัด session ที่ 1.5 เท่าของ keepalive (90 วินาทีเมื่อ keepalive เป็น 60) ถ้าไม่มี PINGREQ
  สัญญา CSR ข้อ 5.3 เล่าว่าครั้งหนึ่งสาเหตุคือ task Subscriber stack ล้นหลัง CONNACK ทันที ให้ดู log ของอุปกรณ์ก่อน broker บอกได้แค่ว่าไม่มีอะไรมา
- **หัวข้อใช้ `device_id` เสมอ** ในโหมด mTLS client id คือ UID ของ Trust M แต่หัวข้อยังต้องเป็น `device/<device_id>/...` ถ้าใช้ UID ในหัวข้อ ACL จะปฏิเสธขณะที่การเชื่อมต่อยังค้างอยู่ ข้อความจึงดูเหมือนหายไปเฉย ๆ

### 2. WiFi จากที่เก็บ ไม่ใช่จาก `#define`

ETSI EN 303 645 ข้อ 5.4-3 ห้ามฝังค่าความปลอดภัยสำคัญไว้ในซอร์สโค้ด
ตัวอย่าง [10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) ทำตามนั้นอย่างเคร่งครัด
มันหาข้อมูลรับรองตามลำดับ ที่เก็บข้อมูลรับรองบน LittleFS (เฉพาะ variant mtb-mpy) แล้วจึง `wifi_ssid` `wifi_pass` `wifi_security` ใน `tesaiot_config_store` (มีทั้งสอง variant)
ถ้าไม่เจอทั้งสองที่ มัน **ปฏิเสธ** และบอกวิธีบันทึกข้อมูลรับรอง คอมเมนต์ในไฟล์เขียนไว้ว่า credential ที่คอมไพล์ติดตัวอย่าง คือ credential ในที่เก็บโค้ดสาธารณะ

รายละเอียดที่ควรลอกไปใช้ในงานของคุณ

- ไม่พิมพ์ passphrase เลย พิมพ์แค่ความยาว เพราะ console มักเป็นจอที่คนอื่นมองเห็น
- ล้างบัฟเฟอร์รหัสผ่านผ่าน pointer แบบ `volatile` เพื่อไม่ให้ compiler ตัดการเขียนทิ้งเพราะคิดว่าไม่มีใครอ่านต่อ
- ถาม `app_wifi_is_ready()` ก่อนเสมอ การเรียก `cy_wcm_is_connected_to_ap()` ก่อน WCM เริ่มทำงานทำให้บอร์ด hard fault
- ตัวอย่างนี้ **ปิดไว้เป็นค่าเริ่มต้น** เพราะมันเปิดวิทยุและเข้าร่วมเครือข่ายของใครบางคน ต้อง build ด้วย `EXAMPLE_WIFI_JOIN=1` เอง

และพูดให้ครบ ไฟล์ตั้งค่าอยู่บน LittleFS ในหน่วยความจำของบอร์ด ดีกว่าอยู่ในซอร์สเพราะไม่หลุดไปกับ repository หรือไฟล์ image ที่แจกจ่าย
แต่ SDK ไม่ได้บอกว่าไฟล์นี้ถูกเข้ารหัส ให้ถือว่าคนที่อ่าน flash ของบอร์ดได้ก็อ่านได้ นี่คือเหตุผลหนึ่งที่ mTLS ซึ่งกุญแจอยู่ในชิป ดีกว่ารหัสผ่าน MQTT ที่อยู่ในไฟล์

### 3. MQTTs หรือ HTTPS

สองทางนี้วิ่งบน TLS เหมือนกัน ต่างกันที่รูปแบบการคุย พอร์ตและวิธียืนยันตัวในตารางมาจาก README ของ device-servertls และ device-mtls บน Developer Hub

| | MQTTs | HTTPS |
|---|---|---|
| รูปแบบ | session เปิดค้าง publish และ subscribe | ถามตอบทีละคำขอ |
| คำสั่งจากแพลตฟอร์ม | มาถึงเองทาง subscription `commands/#` | อุปกรณ์ต้องถามเป็นระยะ เช่น OTA job endpoint ใน `c_ota_client` |
| พอร์ตและการยืนยันตัว | 8884 ชื่อผู้ใช้กับรหัสผ่าน · 8883 mTLS | 443 header `X-API-KEY` · 9444 mTLS |
| ต้นทุนบนบอร์ด | task ที่มีชีวิตตลอด keepalive และ stack ราว 16 KB สำหรับ handshake ตาม README ของ `tesaiot_mqtt` | เปิดปิดทีละครั้ง โมดูล HTTPS ใน `03_https_session.c` ถือได้ทีละการเชื่อมต่อ |
| เหมาะกับ | telemetry ต่อเนื่องและต้องรับคำสั่ง | ส่งเป็นครั้งคราว ดาวน์โหลดไฟล์ใหญ่ เรียก REST API |

ข้อควรระวังจาก [03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c)
คอมเมนต์ในไฟล์บอกว่าเส้นทาง HTTPS นั้นตั้ง `root_ca_verify_mode = CY_AWS_ROOTCA_VERIFY_NONE` คือเข้ารหัสแต่ **ไม่ตรวจใบของเซิร์ฟเวอร์**
และมีทางเข้า plaintext แยกเป็นอีกฟังก์ชันหนึ่ง (`claw_http_connect_insecure`) สำหรับ endpoint สาธารณะที่ไม่มีกุญแจเท่านั้น
ผู้เขียนตั้งใจเลือกโหมด plaintext ด้วยชื่อฟังก์ชัน ไม่ใช่ด้วยเลขพอร์ต เพื่อไม่ให้อีกฝั่งส่งพอร์ต 80 มาแล้วทำให้ API key ถูกส่งแบบไม่เข้ารหัส
ถ้าจะใช้ HTTPS ส่งข้อมูลของอุปกรณ์ ต้องปัก root CA ก่อน

## ตัวอย่างสมบูรณ์

ตัดจาก [10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) บรรทัด 176–190 และ 237–242
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    {
        /* ~660 bytes. Static for the same reason as the buffers above. */
        static tesaiot_config_t cfg;
        tesaiot_config_get(&cfg);
        if (cfg.wifi_ssid[0] != '\0') {
            (void)snprintf(s_ssid, sizeof(s_ssid), "%s", cfg.wifi_ssid);
            (void)snprintf(s_pass, sizeof(s_pass), "%s", cfg.wifi_pass);
            (void)snprintf(s_sec,  sizeof(s_sec),  "%s", cfg.wifi_security);
            wipe(cfg.wifi_pass, sizeof(cfg.wifi_pass));
            return "tesaiot_config_store";
        }
        wipe(cfg.wifi_pass, sizeof(cfg.wifi_pass));
    }

    return NULL;
```

```c
        /* SSID and security only. The passphrase is never printed: the console
         * is not the radio, and this console is often a shared screen. */
        printf("  credentials from %s\r\n", from);
        printf("    ssid=\"%s\" security=\"%s\" passphrase=%u byte(s), not shown\r\n",
               s_ssid, s_sec[0] ? s_sec : "(default: WPA2)",
               (unsigned)strlen(s_pass));
```

สังเกตสามจุด สำเนาของรหัสผ่านใน `cfg` ถูกล้างทันทีหลังคัดลอก **ทั้งสองทางออก** ฟังก์ชันคืนชื่อของที่เก็บที่ใช้ ไม่ใช่ค่ารหัสผ่าน
และข้อความที่พิมพ์บอกทุกอย่างที่ต้องใช้ debug (SSID ชนิดความปลอดภัย ความยาวรหัส) โดยไม่มีตัวรหัสเลย

ตัวอย่างบน Developer Hub ที่ทำเส้นทางเดียวกันบนคอมพิวเตอร์

- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)
- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) โปรเจกต์อ้างอิงบนบอร์ด (Cypress EULA ลิงก์เท่านั้น) ไฟล์ `tesaiot_mqtt.h` ของ SDK ระบุว่าโมดูลของ SDK พัฒนาต่อจากโปรเจกต์นี้

## ฝึกเติม

เขียนการเรียกหนึ่งบรรทัดที่ส่ง JSON `{"t":25.0}` ขึ้นหัวข้อ telemetry ค่าเริ่มต้นของอุปกรณ์ จาก task ของคุณเองบน CM33_NS
ลายเซ็นของฟังก์ชันตามบท C3 คือ `bool tesaiot_mqtt_publish(const char *topic, const char *payload, size_t payload_len);`

```c
static const char payload[] = "{\"t\":25.0}";

if (!tesaiot_mqtt_publish(____, payload, ____)) {
    /* ถึงตรงนี้แปลว่าอะไรได้บ้าง */
}
```

<details><summary>เฉลย</summary>

```c
if (!tesaiot_mqtt_publish(NULL, payload, sizeof(payload) - 1)) {
```

`NULL` (หรือสตริงว่าง) ทำให้ฟังก์ชันสร้างหัวข้อ `device/<device_id>/telemetry` เอง ความยาวไม่รวมตัวปิดท้ายสตริง
ค่า `false` แปลได้ว่ายังไม่เชื่อมต่อ คิวของ publisher ยังไม่พร้อม ไม่มี `device_id` จองหน่วยความจำไม่ได้ หรือคิวเต็ม
ค่า `true` แปลแค่ว่า **เข้าคิวแล้ว** ยังไม่ใช่ว่าถึง broker แล้ว หลักฐานว่าถึงจริงต้องดูจากฝั่งผู้รับ

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ไฟล์ตั้งค่ามี `tls_mode=server_tls` และ `port=1883` บอร์ดจะต่อ broker ที่พอร์ตใด *(เป้าหมายข้อ 1)*
   - ก) 1883
   - ข) 8883
   - ค) 8884
   - ง) 443

   <details><summary>เฉลย</summary>

   **ค** พอร์ตของ MQTT มาจาก `tls_mode` ใน `mqtt_client_config.c` บรรทัด `port=` ไม่ถูกใช้

   </details>

2. ทำไมตัวอย่าง `10_wifi_join.c` จึงปฏิเสธการทำงานเมื่อไม่พบข้อมูลรับรองในที่เก็บ แทนที่จะใช้ SSID สำรองในโค้ด *(เป้าหมายข้อ 2)*
   - ก) เพราะ SSID สำรองกินหน่วยความจำ
   - ข) เพราะ credential ที่คอมไพล์ติดโค้ดคือ credential ที่หลุดไปกับที่เก็บโค้ดสาธารณะ ซึ่งขัดกับ ETSI ข้อ 5.4-3
   - ค) เพราะ WiFi ไม่รองรับ SSID สำรอง
   - ง) เพราะ compiler ไม่ยอม

   <details><summary>เฉลย</summary>

   **ข** ตัวอย่างบอกวิธีบันทึกข้อมูลรับรองแทน และไม่มีทางเลือกที่สี่

   </details>

3. อุปกรณ์วัดอุณหภูมิทุก 10 วินาที และต้องรับคำสั่งปิดเปิดพัดลมจากแพลตฟอร์มภายในไม่กี่วินาที ควรเลือกอะไร *(เป้าหมายข้อ 3)*
   - ก) HTTPS ถามแพลตฟอร์มทุกชั่วโมง
   - ข) MQTTs ที่ publish telemetry และ subscribe `commands/#`
   - ค) HTTP แบบไม่เข้ารหัส เพราะเร็วกว่า
   - ง) ไม่ต้องเชื่อมต่อ

   <details><summary>เฉลย</summary>

   **ข** session ที่เปิดค้างทำให้คำสั่งมาถึงเองโดยไม่ต้องถาม ส่วน HTTPS เหมาะกับงานที่ส่งเป็นครั้งคราวหรือดาวน์โหลดไฟล์ใหญ่

   </details>

4. `tesaiot_mqtt_publish()` คืน `true` ข้อสรุปใดถูก *(เป้าหมายข้อ 1)*
   - ก) ข้อความถึง broker แล้วแน่นอน
   - ข) ข้อความเข้าคิวของ publisher แล้ว การพิสูจน์ว่าถึงต้องดูจากฝั่งผู้รับ
   - ค) แพลตฟอร์มบันทึกข้อมูลแล้ว
   - ง) ใบรับรองของ broker ผ่านการตรวจแล้ว

   <details><summary>เฉลย</summary>

   **ข** บท C3 เตือนด้วยว่าบรรทัด `[Publisher] Published to ...` ถูกปิดไว้ อย่ารอบรรทัดนั้นเป็นหลักฐาน

   </details>

## แล็บ

**เชื่อมต่อจริง แล้วพิสูจน์ด้วยหลักฐานจากฝั่งผู้รับ** จดผลทุกข้อลงบันทึกการเรียน และห้ามจดรหัสผ่านตัวจริงลงไป

- [ ] **1. WiFi จากที่เก็บ** ใส่ `wifi_ssid` `wifi_pass` `wifi_security` ลงไฟล์ตั้งค่าของบอร์ด บน mtb-only บท C3 ให้เขียนจากหน้าตั้งค่า TESAIoT บนจอ หรือใส่ไฟล์ไปกับ filesystem ของ image
  บน mtb-mpy เขียนจาก REPL ได้ แล้ว build ตัวอย่าง
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/connectivity/10_wifi_join DEFINES+=EXAMPLE_WIFI_JOIN=1
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  จดบรรทัด `credentials from ...` และ `passphrase=N byte(s), not shown` จากนั้นค้นทั้งโฟลเดอร์โปรเจกต์ของคุณด้วย `grep -r "<ชื่อ WiFi ของคุณ>" .` ต้องไม่เจอ
- [ ] **2. ตั้งค่า MQTT** เติม `tls_mode=server_tls`, `broker=mqtt.tesaiot.dev`, `device_id` และ `mqtt_pass` จาก bundle ใส่ `port=1883` ไว้ด้วยเพื่อทดสอบคำทาย
- [ ] **3. เชื่อมต่อ** แตะ Connect บนหน้า TESAIoT ของจอ แล้วจดบรรทัดบน UART ตามลำดับ เทียบกับรายการในบท C3 Step 3
  ในบรรทัด `[MQTT-Config] Mode=..., Broker=...:<พอร์ต>` พอร์ตเป็นเท่าไร ตรงกับคำทายไหม
- [ ] **4. พิสูจน์ว่าข้อมูลถึง** subscribe จากคอมพิวเตอร์ **ก่อน** แล้วค่อยให้บอร์ด publish (ใช้คำตอบฝึกเติมใน task ของคุณ หรือ `tesaiot.publish()` บน mtb-mpy)
  ```bash
  mosquitto_sub -h mqtt.tesaiot.dev -p 8884 --cafile ca-chain.pem \
    -u '<device_id>' -P '<รหัสผ่าน MQTT>' -t 'device/<device_id>/telemetry' -v
  ```
  ถ้า broker ไม่อนุญาตให้บัญชีนี้ subscribe นั่นคือ ACL ทำงาน สัญญา CSR ของ SDK ข้อ 5.1 ระบุว่าบัญชีของอุปกรณ์ subscribe ได้เฉพาะ `commands` `config` `firmware`
  ให้ใช้บัญชีทดสอบหรือวิธีตรวจที่ผู้ดูแลแพลตฟอร์มของคุณกำหนด แล้วจดไว้ว่าหลักฐานมาจากไหน
- [ ] **5. session ต้องมีคนดูแล** ปล่อยบอร์ดเงียบเกิน 90 วินาทีแล้ว publish อีกครั้ง ผ่านไหม ถ้าไม่ผ่าน ดู log ของอุปกรณ์ก่อน (มี task ตายหรือ stack ล้นไหม) แล้วค่อยสงสัย broker
- [ ] **6. เลือกช่องทาง** เขียนตารางสามแถวสำหรับงานของคุณเอง (ตัวอย่าง ส่งค่าทุกนาที · ดาวน์โหลดเฟิร์มแวร์ 2 MB · รับคำสั่งฉุกเฉิน) แต่ละแถวเลือก MQTTs หรือ HTTPS พร้อมเหตุผลหนึ่งบรรทัด
- [ ] **7. อัปเดต threat model** ของบทเรียน 1.1 ในแถวที่เกี่ยวกับ WiFi รหัสผ่าน MQTT และ session ด้วยสิ่งที่เห็นในแล็บนี้

## ไปต่อ

อุปกรณ์ของเราเชื่อมต่อได้อย่างปลอดภัยแล้ว คำถามต่อไปคือ เฟิร์มแวร์ที่รันอยู่เป็นตัวที่เราตั้งใจให้รันจริงไหม
โมดูล 4 จะดูห่วงโซ่ความเชื่อใจตั้งแต่บูต และการอัปเดตที่กันการย้อนรุ่น

บทเรียนถัดไป: [บทเรียน 4.1: Secure boot และ chain of trust](../../m04-secure-boot-and-update/l01-secure-boot/README.md)

## สะท้อนคิด

- ในงานของคุณ มีค่าตั้งไหนที่ถูกเก็บไว้แต่ไม่ถูกใช้ แบบ `port=` บ้าง และใครจะถูกหลอกโดยค่านั้น
- ถ้าข้อความหายระหว่างทาง ระบบของคุณจะรู้ได้อย่างไร จากฝั่งไหน
- รหัสผ่านที่อยู่ในไฟล์ตั้งค่าบนบอร์ด ปลอดภัยกว่าในซอร์สโค้ดแค่ไหน และยังเสี่ยงต่อใคร

## แหล่งอ้างอิง

- [C3 — TESAIoT cloud: config file → MQTT task → broker (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- [SDK: โมดูล tesaiot_mqtt](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/README.md)
- [SDK: tesaiot_mqtt/mqtt_client_config.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_client_config.c) (ลิงก์ ไม่ได้คัดลอก)
- [SDK: tesaiot_config/tesaiot_config_store.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_store.c)
- [SDK: cm33/connectivity/10_wifi_join.c (ข้อมูลรับรองจากที่เก็บ ไม่ใช่ #define)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c)
- [SDK: cm33/connectivity/03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c)
- [SDK: CSR_SUBMISSION_CONTRACT.md (ACL, keepalive, หัวข้อ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- [TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition)
- ตัวอย่างบน Developer Hub: [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น)
