---
id: fw-stack.m05.l02
lang: th
title:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
summary:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ด้วย mTLS โดยใช้ client certificate และ private key ของอุปกรณ์"
    en: "Send telemetry with mTLS using the device client certificate and private key"
  - th: "เปรียบเทียบ Server-TLS กับ mTLS ในด้านความปลอดภัยและการดูแลกุญแจ"
    en: "Compare Server-TLS and mTLS for security and key handling"
develops:
  - {skill: sec.tls, to: 3}
  - {skill: sec.crypto, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/intermediate/device-mtls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
---

# ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS

## เป้าหมาย

1. ส่ง telemetry ด้วย mTLS โดยใช้ client certificate และ private key ของอุปกรณ์
2. เปรียบเทียบ Server-TLS กับ mTLS ในด้านความปลอดภัยและการดูแลกุญแจ

## แนวคิด

### mTLS คืออะไร: อุปกรณ์ต้องพิสูจน์ว่าถือ private key คู่กับใบรับรองของตัวเอง

mTLS (mutual TLS หรือ TLS สองทาง) เพิ่มขั้นตอนเข้าไปใน handshake ปกติ: หลังจากเซิร์ฟเวอร์ยื่นใบรับรองของตัวเองให้อุปกรณ์ตรวจแล้ว (เหมือน Server-TLS ในบทเรียนก่อน) เซิร์ฟเวอร์จะขอใบรับรองของอุปกรณ์กลับด้วย และอุปกรณ์ต้องพิสูจน์ว่าถือ private key ที่จับคู่กับใบรับรองนั้นจริง (โดยเซ็นข้อมูลบางส่วนของ handshake ด้วยกุญแจนั้น) จุดสำคัญคือ private key ไม่เคยถูกส่งผ่านเครือข่ายเลย มีแต่ "ลายเซ็น" ที่พิสูจน์ว่าอุปกรณ์ถือกุญแจอยู่เท่านั้น — ต่างจาก Server-TLS ที่อุปกรณ์ต้องส่งความลับ (API key หรือ password) ผ่านอุโมงค์ทุกครั้งที่เชื่อมต่อ

### ไฟล์ที่ต้องมี และโค้ดตรวจก่อนเชื่อมต่อเสมอ

ตัวอย่างนี้ (`device-mtls`) ต้องมีไฟล์ `client_cert.pem` และ `client_key.pem` อยู่ใน `certs_credentials/` เสมอ `main.c` เช็กด้วย `file_exists(crt) && file_exists(key)` ก่อนเริ่มส่งข้อมูลทุกครั้ง ถ้าไม่ครบจะพิมพ์ error แล้วออกจากโปรแกรมทันที ไม่มีการลองเชื่อมต่อแบบไม่มีใบรับรอง เมื่อไฟล์ครบ โค้ดตั้ง `tls.client_cert = crt; tls.client_key = key;` และยังคงเปิด `tls.verify_peer = 1U` เหมือนบทเรียนก่อน — อุปกรณ์ยังตรวจเซิร์ฟเวอร์เหมือนเดิม เพิ่มเติมคือต้องยื่นใบรับรองของตัวเองด้วย

### อุปกรณ์แบบ CSR: กุญแจไม่เคยออกจากเครื่องที่สร้างมันเลย

สำหรับอุปกรณ์ที่ขอใบรับรองผ่าน CSR (Certificate Signing Request) README ของตัวอย่างระบุว่า bundle ที่ดาวน์โหลดจาก Admin Portal จะ**ไม่มี** private key รวมมาด้วย เพราะกุญแจถูกสร้างขึ้นที่ฝั่งอุปกรณ์เองตอนสร้าง CSR (ด้วย `scripts/generate_csr.sh` ที่เรียก `openssl` แล้ว `chmod 600` ทันที) แพลตฟอร์มได้รับแค่ CSR ที่มี public key ไปลงนามเป็นใบรับรอง กุญแจส่วนตัวจึงไม่เคยเดินทางออกจากเครื่องที่สร้างมันเลย ถึง bundle ที่ดาวน์โหลดจะรั่วก็ไม่ทำให้กุญแจรั่วตามไปด้วย ผู้ใช้ต้องคัดลอกกุญแจนี้มาวางเป็น `certs_credentials/client_key.pem` เองก่อนใช้งาน (มีสคริปต์ช่วย `sync_csr_key.sh <DEVICE_ID>`)

### CA ที่ใช้ตรวจเซิร์ฟเวอร์ยังเป็น system trust เหมือนเดิม ไม่ใช้ ca-chain.pem ของ bundle

ต่างจากบทเรียนก่อนที่สาขา MQTTS ใช้ `ca-chain.pem` ของอุปกรณ์ตรวจ broker ตัวอย่าง mTLS นี้ตั้ง `tls.ca_chain = NULL;` ในทั้งสองสาขา (HTTPS และ MQTTS) พร้อมคอมเมนต์ในซอร์สว่าให้ใช้ system trust และห้ามบังคับใช้ CA ของอุปกรณ์เอง เพราะปลายทางทั้งสองยังใช้ใบรับรองจาก public CA เหมือนเดิม สิ่งที่ mTLS เพิ่มเข้ามาไม่ใช่วิธีตรวจเซิร์ฟเวอร์ (เหมือนเดิมทุกประการ) แต่คือการที่อุปกรณ์ต้องยื่นใบรับรองของตัวเองกลับไปด้วย

### พอร์ตของ mTLS ต่างจาก Server-TLS

แพลตฟอร์มแยก listener ของ mTLS ออกจาก Server-TLS ชัดเจน mTLS ใช้ HTTPS พอร์ต 9444 และ MQTTS พอร์ต 8883 (ตามค่า default ใน `config.h`: `DEFAULT_API_BASE_URL` ลงท้ายด้วย `:9444`, `DEFAULT_MQTT_PORT = 8883U`) ขณะที่ Server-TLS ใช้ 443 และ 8884 README เตือนไว้ว่าถ้าส่ง HTTPS mTLS ไปที่พอร์ต 443 แทน 9444 ปลายทางจะไม่ใช่ endpoint ของ mTLS และจะเจอปัญหา SAN/โดเมนไม่ตรงตามที่คาด

### เปรียบเทียบ Server-TLS กับ mTLS: จุดแลกเปลี่ยนด้านความปลอดภัยกับภาระดูแลกุญแจ

ทั้งสองแบบเข้ารหัสช่องทางเท่ากันและอุปกรณ์ตรวจเซิร์ฟเวอร์เหมือนกัน (`verify_peer = 1` เสมอ) ความต่างอยู่ที่วิธีพิสูจน์ตัวตนของอุปกรณ์ Server-TLS เริ่มต้นง่ายกว่าเพราะแค่มีความลับหนึ่งค่า แต่ความลับนั้นเดินทางผ่านเครือข่ายทุกครั้งที่เชื่อมต่อ (แม้จะอยู่ในอุโมงค์ที่เข้ารหัสแล้วก็ตาม) และถ้าความลับหลุด ผู้โจมตีก็ปลอมเป็นอุปกรณ์ได้ทันทีโดยไม่ต้องมีอะไรเพิ่ม ส่วน mTLS ไม่มีความลับเดินทางผ่านเครือข่ายระหว่างพิสูจน์ตัวตนเลย แต่แลกกับภาระดูแลใบรับรองและกุญแจ: ต้องมีระบบออกใบรับรอง ต่ออายุก่อนหมดอายุ และเก็บ private key ให้ปลอดภัย — ถ้า private key ของอุปกรณ์หนึ่งรั่ว ผู้โจมตีปลอมเป็นอุปกรณ์ตัวนั้นได้จนกว่าใบรับรองจะถูกเพิกถอนและออกคู่กุญแจใหม่ แต่ผลกระทบจำกัดอยู่ที่อุปกรณ์ตัวนั้นเพราะแต่ละตัวมีใบรับรองและ ACL ของ topic เป็นของตัวเอง (`device/<device_id>/…`) การไม่ให้กุญแจออกจากอุปกรณ์เลยตั้งแต่แรก อย่างที่ทำด้วย secure element ใน OPTIGA Trust M (บทเรียน 5.3) คือทางลดความเสี่ยงนี้ไปอีกขั้น

## ตัวอย่างสมบูรณ์

> **ก่อนรันตัวอย่าง (ตรวจเมื่อ 26 ก.ย. 2026):** `config.h` ของตัวอย่างที่ commit นี้ยังตั้งค่าเริ่มต้นเป็นโดเมนเดิมของแพลตฟอร์มที่ลงท้ายด้วย .com ซึ่งย้ายไปเป็น tesaiot.dev แล้ว
> โดเมนเดิมของ API ไม่ resolve แล้ว ส่วนของ MQTT ยังใช้ได้ชั่วคราว ให้ตั้ง `DEFAULT_API_BASE_URL` เป็น `https://tesaiot.dev:9444` และ `DEFAULT_MQTT_HOST` เป็น `mqtt.tesaiot.dev`
> (บันทึกไว้ที่ [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3))

ตัวอย่างนี้เป็นภาษา C ที่รันบนคอมพิวเตอร์ก่อน (GCC/Clang + OpenSSL, mbedTLS หรือ wolfSSL หรือ libcurl) เพื่อให้เห็นโปรโตคอลชัด แล้วจึงนำแนวคิดเดียวกันไปใช้บนบอร์ด โค้ดด้านล่างคัดลอกจากไฟล์จริง (Apache-2.0, tesaiot/developer-hub, commit `d2ed42c`)

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L336-L343) — ต้องมีทั้งใบรับรองและกุญแจของอุปกรณ์ก่อนเริ่มทำงาน:

```c
  char ca[512], crt[512], key[512];
  join_path(ca,  sizeof(ca),  certs_dir, FILE_CA_CHAIN);
  join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
  join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
  if (!(file_exists(crt) && file_exists(key))) {
    (void)fprintf(stderr, "mTLS requires client_cert.pem and client_key.pem in %s\n", certs_dir);
    return 1;
  }
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L386-L388) — TLS conf ผูกใบรับรอง/กุญแจของอุปกรณ์ ยังตรวจเซิร์ฟเวอร์เหมือนเดิม:

```c
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.client_cert = crt; tls.client_key = key;
  tls.verify_peer = 1U; tls.connect_timeout_ms = (uint32_t)(HTTP_CONNECT_TIMEOUT_SEC * 1000L); tls.total_timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L412-L419) — สาขา MQTTS: ไม่มี username/password เลย เพราะใบรับรองทำหน้าที่พิสูจน์ตัวตนแทน:

```c
    if (is_mode_mqtts() != 0) {
      /* Send via MQTTS (mTLS) */
      /* ... */
      tls.ca_chain = NULL; tls.sni_name = mqtt_host;
      char topic[MAX_TOPIC_SIZE]; (void)snprintf(topic, sizeof(topic), "device/%s/telemetry", device_id);
      iot_mqtt_req_t mreq; (void)memset(&mreq, 0, sizeof(mreq));
      mreq.host = mqtt_host; mreq.port = (uint16_t)mqtt_port; mreq.client_id = device_id; mreq.username = NULL; mreq.password = NULL;
      mreq.topic = topic; mreq.payload = json_buf; mreq.payload_len = strlen(json_buf); mreq.qos = 1U; mreq.retain = 0U; mreq.keepalive_sec = 30U; mreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

- [README ของตัวอย่าง](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) · commit `d2ed42c`
- ต้องมี credential ของอุปกรณ์จาก TESAIoT Platform ตามขั้นตอนใน README ห้ามนำ credential จริงขึ้น repo สาธารณะ

## จุดที่มักพลาด

- **ลืมว่า bundle ของอุปกรณ์แบบ CSR ไม่มี private key มาด้วย** — ถ้าเห็นข้อความ error ว่าไม่มีกุญแจ ต้องรัน `./scripts/sync_csr_key.sh <DEVICE_ID>` เพื่อคัดลอกกุญแจจากเครื่องที่สร้าง CSR เอง ไม่ใช่ไปขอกุญแจใหม่จากแพลตฟอร์ม เพราะแพลตฟอร์มไม่เคยมีกุญแจนี้ตั้งแต่แรก
- **ใช้พอร์ตของ Server-TLS กับ credential แบบ mTLS หรือกลับกัน** — mTLS ใช้ 9444 (HTTPS) และ 8883 (MQTTS) ถ้าไปที่ 443 หรือ 8884 ปลายทางจะไม่ใช่ endpoint ของ mTLS และจะเจอปัญหา SAN/โดเมนไม่ตรง
- **คิดว่า mTLS ทำให้ไม่ต้องตรวจใบรับรองของเซิร์ฟเวอร์อีกต่อไป** — `tls.verify_peer = 1U` ยังเปิดอยู่เหมือน Server-TLS ทุกประการ mTLS แค่เพิ่มการที่อุปกรณ์ต้องพิสูจน์ตัวเองด้วย ไม่ได้ลดการตรวจฝั่งเซิร์ฟเวอร์ลงเลย
- **เข้าใจว่า Server-TLS กับ mTLS ใช้ `X-API-KEY` เหมือนกัน** — mTLS ไม่ใช้ API key เลย (`hreq.api_key = NULL`) ถ้าเจอ HTTPS ตอบรหัสผิดพลาดในโหมด mTLS ต้องตรวจใบรับรอง/กุญแจของอุปกรณ์ ไม่ใช่ไปตรวจ API key

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- mTLS เพิ่มอะไรจาก Server-TLS
- ถ้า private key ของอุปกรณ์รั่ว ผลกระทบคืออะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [ตัวอย่างบน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- ตัวอย่างอยู่ใน tesaiot/developer-hub (Apache-2.0) และอ้างอิงด้วยลิงก์

