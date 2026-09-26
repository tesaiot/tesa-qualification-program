---
id: fw-stack.m05.l01
lang: th
title:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
summary:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C"
    en: "Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example"
  - th: "อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์"
    en: "Explain what the CA certificate does when verifying the server"
develops:
  - {skill: sec.tls, to: 2}
  - {skill: proto.mqtt, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/entry/device-servertls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS

## เป้าหมาย

1. ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C
2. อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์

## แนวคิด

### Server-TLS ยืนยันตัวตนของใคร และอุปกรณ์พิสูจน์ตัวเองด้วยอะไร

Server-TLS (หรือ TLS ทางเดียว) คือ TLS handshake ที่ฝั่งเซิร์ฟเวอร์ยื่นใบรับรอง (certificate) ของตัวเองให้อุปกรณ์ตรวจก่อนเสมอ อุปกรณ์ตรวจว่าใบรับรองนั้นถูกลงนามโดย CA ที่เชื่อถือได้และตรงกับชื่อโฮสต์ที่ตั้งใจเชื่อมต่อ — นี่คือสิ่งเดียวที่ Server-TLS ยืนยัน คือตัวตนของเซิร์ฟเวอร์ ส่วนตัวตนของอุปกรณ์ TLS handshake เองไม่ได้พิสูจน์ให้ อุปกรณ์ต้องพิสูจน์ตัวเองอีกชั้นด้วย "ความลับ" ที่มันถือ ซึ่งถูกส่งผ่านอุโมงค์ที่เข้ารหัสแล้วอีกที ในโค้ดของตัวอย่างนี้ (`main.c`) เห็นได้ชัดจากการที่ `tls.client_cert` และ `tls.client_key` ถูกตั้งเป็น `NULL` เสมอ (ไม่มีใบรับรองฝั่งอุปกรณ์) ในขณะที่ `tls.verify_peer = 1U` ยังเปิดอยู่ตลอด — อุปกรณ์ยังตรวจเซิร์ฟเวอร์ แต่ไม่ได้ยื่นใบรับรองของตัวเอง

### สองทางที่ตัวอย่างนี้ใช้พิสูจน์ตัวตนของอุปกรณ์: API key กับ username/password

ตัวอย่างนี้ (`device-servertls`) เลือกโหมดส่งข้อมูลได้สองแบบผ่าน environment variable `COMM_MODE` คือ HTTPS กับ MQTTS ทั้งคู่ยังเป็น Server-TLS เหมือนกัน (เซิร์ฟเวอร์พิสูจน์ตัวเองด้วยใบรับรองเหมือนกัน) แต่อุปกรณ์พิสูจน์ตัวเองต่างกันตามทาง — HTTPS ส่งเฉพาะ header `X-API-KEY` ที่อ่านจาก `api_key.txt` (โค้ดมีคอมเมนต์ว่า "omit Bearer" คือไม่ต้องส่ง Bearer token ซ้ำ) ส่วน MQTTS ใช้ `username = device_id` กับ `password` จาก `mqtt_password.txt` ที่ backend ตรวจ hash กับฐานข้อมูล ทั้งสองแบบความลับ (API key หรือ password) เดินทางอยู่ภายในอุโมงค์ TLS ที่เข้ารหัสแล้วเสมอ ไม่ได้ส่งแบบข้อความเปล่า

### ca-chain.pem คือ trust anchor ของ broker แต่ปลายทาง HTTPS ในตัวอย่างนี้ใช้ trust store ของระบบแทน

`main.c` ตั้งค่า TLS เริ่มต้นด้วย `tls.ca_chain = file_exists(PATH_CA_CHAIN) ? PATH_CA_CHAIN : NULL;` — ถ้ามีไฟล์ `ca-chain.pem` (จาก bundle ที่ดาวน์โหลดจาก Admin Portal) อยู่ในโฟลเดอร์ `certs_credentials/` โค้ดจะใช้ไฟล์นี้เป็น trust anchor ตอนเชื่อมต่อ MQTTS (พร้อมตั้ง `tls.sni_name = mqtt_host`) เพื่อตรวจว่าใบรับรองของ broker ออกโดย CA ภายในของแพลตฟอร์มจริง แต่พอเข้าสาขา HTTPS โค้ดจะเขียนทับค่านี้ทันทีด้วย `tls.ca_chain = NULL;` พร้อมคอมเมนต์ในซอร์สว่าให้ใช้ system trust เพราะปลายทาง HTTPS สาธารณะของแพลตฟอร์มใช้ใบรับรองจาก public CA ที่ระบบปฏิบัติการเชื่อถืออยู่แล้ว จึงไม่ต้องพก `ca-chain.pem` ของตัวเองมาตรวจซ้ำ — เป็นรายละเอียดที่ต่างกันตามทางเชื่อมต่อภายในตัวอย่างเดียวกัน ไม่ใช่กฎตายตัวว่า Server-TLS ต้องใช้ `ca-chain.pem` เสมอไป

### พอร์ตแยกตามวิธีพิสูจน์ตัวตน ไม่ใช่แยกตามโปรโตคอล

แพลตฟอร์มแยก listener ตามวิธีที่อุปกรณ์พิสูจน์ตัวเอง Server-TLS ใช้ MQTT พอร์ต 8884 และ HTTPS พอร์ต 443 (ตามค่า default ใน `config.h`: `DEFAULT_MQTT_PORT = 8884U`, `DEFAULT_API_BASE_URL`) ส่วน mTLS (บทเรียนถัดไป) ใช้พอร์ตอื่น ถ้าใช้ credential แบบ username/password ของ Server-TLS ไปเชื่อมที่พอร์ต 8883 (พอร์ตของ mTLS) TLS จะถูกปิดหลัง CONNECT เพราะ listener ฝั่งนั้นคาดหวังใบรับรองของอุปกรณ์ ไม่ใช่ username/password

### ลำดับขั้นตอน และสิ่งที่ล้มเหลวถ้าขาดขั้นตอนใดขั้นตอนหนึ่ง

ลำดับของตัวอย่างนี้คือ (1) อ่าน credential จากไฟล์ใน `certs_credentials/` — device_id, api_key หรือ mqtt username/password และ `endpoints.json` ถ้ามี (2) เปิด TLS handshake ไปยังปลายทางที่กำหนด โดยตรวจใบรับรองเซิร์ฟเวอร์เสมอ (`verify_peer = 1U` ไม่เคยถูกปิด) (3) เมื่อ handshake สำเร็จ ส่ง credential ของอุปกรณ์ภายในอุโมงค์ (header หรือ MQTT CONNECT packet) (4) ส่ง payload JSON `{device_id, timestamp, data}` ไปยัง topic `device/<device_id>/telemetry` (MQTTS) หรือ endpoint `/api/v1/telemetry` (HTTPS) ถ้าขาดขั้นตอนที่ 1 (ไม่มีไฟล์ credential) โปรแกรมจะหยุดทันทีพร้อม error ถ้าขั้นตอนที่ 2 ล้มเหลว (เช่นใบรับรองเซิร์ฟเวอร์หมดอายุ หรือเวลาของอุปกรณ์ผิดจนใบรับรองดูเหมือนยังไม่ถึงเวลาใช้งาน) handshake จะล้มก่อนถึงขั้นตอนที่ 3 เสมอ ส่วนถ้าขั้นตอนที่ 2 ผ่านแต่ขั้นตอนที่ 3 ผิด (เช่น password หมดอายุ) broker จะตอบกลับด้วยรหัสปฏิเสธ (MQTT CONNACK code 5 "Not authorized") ซึ่งเป็นคนละสาเหตุกับปัญหา TLS — README ของตัวอย่างแยกสองกรณีนี้ไว้ชัดเจนในหัวข้อ Troubleshooting

## ตัวอย่างสมบูรณ์

> **ก่อนรันตัวอย่าง (ตรวจเมื่อ 26 ก.ย. 2026):** `config.h` ของตัวอย่างที่ commit นี้ยังตั้งค่าเริ่มต้นเป็นโดเมนเดิมของแพลตฟอร์มที่ลงท้ายด้วย .com ซึ่งย้ายไปเป็น tesaiot.dev แล้ว
> โดเมนเดิมของ API ไม่ resolve แล้ว ส่วนของ MQTT ยังใช้ได้ชั่วคราว ให้ตั้ง `DEFAULT_API_BASE_URL` เป็น `https://tesaiot.dev` และ `DEFAULT_MQTT_HOST` เป็น `mqtt.tesaiot.dev`
> (บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด โค้ดด้านล่างคัดลอกจากไฟล์จริง (Apache-2.0, tesaiot/developer-hub, commit `d2ed42c`)

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L297-L301) — TLS conf เริ่มต้น: ไม่มีใบรับรองฝั่งอุปกรณ์ แต่ยังตรวจฝั่งเซิร์ฟเวอร์เสมอ:

```c
  /* Mongoose TLS conf */
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.ca_chain = file_exists(PATH_CA_CHAIN) ? PATH_CA_CHAIN : NULL;
  tls.client_cert = NULL; tls.client_key = NULL; /* serverTLS */
  tls.verify_peer = 1U; tls.connect_timeout_ms = (uint32_t)(HTTP_CONNECT_TIMEOUT_SEC * 1000L); tls.total_timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L331-L341) — สาขา MQTTS: ใช้ `ca-chain.pem` ของอุปกรณ์ตรวจ broker และพิสูจน์ตัวเองด้วย username/password:

```c
    if (is_mode_mqtts() != 0) {
      /* MQTTS (Server‑TLS): username/password + CA verify */
      char topic[MAX_TOPIC_SIZE]; (void)snprintf(topic, sizeof(topic), "device/%s/telemetry", dev_id);
      iot_mqtt_req_t mreq; (void)memset(&mreq, 0, sizeof(mreq));
      mreq.host = mqtt_host; mreq.port = (uint16_t)mqtt_port; mreq.client_id = dev_id;
      mreq.username = (mqtt_user[0] != '\0') ? mqtt_user : dev_id; /* fallback to device_id */
      mreq.password = (mqtt_pass[0] != '\0') ? mqtt_pass : NULL;
      mreq.topic = topic; mreq.payload = json; mreq.payload_len = strlen(json);
      mreq.qos = 1U; mreq.retain = 0U; mreq.keepalive_sec = 30U; mreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
      tls.sni_name = mqtt_host;
      const int rc = iot_mqtts_publish(&mreq, &tls);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L344-L354) — สาขา HTTPS: ใช้ trust store ของระบบแทน `ca-chain.pem` และพิสูจน์ตัวเองด้วย `X-API-KEY`:

```c
    } else {
      /* HTTPS (Server‑TLS): Bearer/X-API-KEY */
      /* ... */
      tls.ca_chain = NULL;
      tls.sni_name = NULL;
      iot_http_req_t hreq; (void)memset(&hreq, 0, sizeof(hreq));
      hreq.url = url; hreq.body = json; hreq.body_len = strlen(json);
      /* For Server‑TLS HTTPS, send only X-API-KEY (omit Bearer) */
      hreq.api_key = api_key; /* include device API key header */
      hreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
      const int rc = iot_https_post(&hreq, &tls);
```

- [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls) · commit `d2ed42c`
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

## จุดที่มักพลาด

- **คิดว่า Server-TLS ยืนยันตัวตนของอุปกรณ์ด้วย** — Server-TLS ยืนยันแค่ฝั่งเซิร์ฟเวอร์เท่านั้น อุปกรณ์ต้องพิสูจน์ตัวเองแยกต่างหากด้วย API key หรือ username/password ถ้าลืมจุดนี้ อาจปกป้อง API key/password ไม่ดีพอ เพราะเข้าใจผิดว่าใบรับรองทำหน้าที่แทนอยู่แล้ว
- **ใช้พอร์ตผิดโหมด (8883 แทน 8884 หรือกลับกัน)** — พอร์ตแยกตามวิธีพิสูจน์ตัวตนของอุปกรณ์ ไม่ใช่แยกตามว่าใช้ TLS หรือไม่ ใช้พอร์ตของ mTLS กับ credential แบบ Server-TLS จะเจอ TLS ปิด connection หลัง CONNECT ทันที
- **เจอ MQTT CONNACK Code 5 (Not authorized) แล้วคิดว่าเป็นปัญหา TLS/certificate** — Code 5 เกิด**หลัง**จาก TLS handshake สำเร็จแล้วเท่านั้น จึงเป็นปัญหาที่ขั้นพิสูจน์ตัวตนของอุปกรณ์ (username/password ผิดหรือยังไม่ได้ sync ใหม่) ไม่ใช่ปัญหาใบรับรอง
- **คิดว่า `ca-chain.pem` ต้องถูกใช้ตรวจทุกทางเชื่อมต่อเสมอ** — ในตัวอย่างนี้เฉพาะ MQTTS เท่านั้นที่ใช้ `ca-chain.pem` ของอุปกรณ์ ส่วน HTTPS ใช้ trust store ของระบบปฏิบัติการแทน เป็นทางเลือกเฉพาะของตัวอย่างนี้ ไม่ใช่กฎทั่วไปของ Server-TLS

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- Server-TLS ยืนยันตัวตนของใคร และไม่ได้ยืนยันของใคร
- ถ้าเวลาในเครื่องผิด TLS อาจล้มเหลวเพราะอะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)
- ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

