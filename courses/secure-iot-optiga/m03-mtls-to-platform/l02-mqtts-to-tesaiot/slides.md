---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — MQTTs ขึ้น TESAIoT Platform"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 3.2 — MQTTs ขึ้น TESAIoT Platform

## ตามเส้นทางตั้งแต่ไฟล์ตั้งค่า งาน MQTT จนถึง broker และส่งข้อมูลขึ้นแพลตฟอร์มผ่านการเชื่อมต่อที่เข้ารหัส

**โมดูล 3 — mTLS สู่ TESAIoT Platform**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น
2. เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด
3. เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 3.1](../l01-tls-and-mtls/README.md)
- บนแพลตฟอร์ม: อุปกรณ์ที่ลงทะเบียนแล้ว และ Server-TLS bundle (เลือก `include_password` ตอนดาวน์โหลด) **ห้ามนำไฟล์เหล่านี้ขึ้น repository ใด ๆ**
- บนคอมพิวเตอร์: `mosquitto_sub`/`mosquitto_pub`

---

## ดูของจริงก่อน

```ini
tls_mode=server_tls
broker=mqtt.tesaiot.dev
port=1883
device_id=<device_id จากแพลตฟอร์ม>
mqtt_pass=<รหัสผ่าน MQTT จาก bundle>
wifi_ssid=<ชื่อ WiFi>
wifi_pass=<รหัส WiFi>
```

**ทายก่อน** บอร์ดจะต่อ broker ที่พอร์ตไหน — 1883 ตามบรรทัด `port=` หรือพอร์ตอื่น

---

## แนวคิด (1) — เส้นทางจากไฟล์ตั้งค่าถึง broker

```text
/.tesaiot_config → tesaiot_config_init() ตอนบูต
   ▼
tesaiot_mqtt_connect() ← ปุ่ม Connect
   ▼
mqtt_client_config_init()  เลือก host, พอร์ตจาก tls_mode, client id, user/pass, root CA
   ▼
cy_mqtt_connect() ── TLS 1.2 ──▶ mqtt.tesaiot.dev
```

| `tls_mode` | พอร์ต | client id | ชื่อผู้ใช้ | รหัสผ่าน |
|---|---|---|---|---|
| `mtls` (0) | 8883 | `factory_uid` | `mtls_device_id` | ว่าง (ใบรับรอง) |
| `server_tls` (2, ค่าเริ่มต้น) | 8884 | `device_id` | `device_id` | `mqtt_pass` |

**คำตอบคำทาย** = **8884** — บรรทัด `port=` ถูกเก็บไว้แต่ **ไม่ถูกใช้กับ MQTT เลย**

---

## แนวคิด (2) — กับดักที่พบบ่อย

- **คิวของ publisher ไม่รอ** `tesaiot_mqtt_publish()` ใส่คิวแบบรอศูนย์วินาที — คิวเต็มข้อความทิ้งเงียบ
- **handler ของ subscriber วิ่งบน event thread ของ MQTT** งาน block/แตะชิปต้องส่งต่อเข้าคิว
- **ต้องมีคนดูแล session** broker ตัด session ที่ 1.5×keepalive (90s) ถ้าไม่มี PINGREQ
- **หัวข้อใช้ `device_id` เสมอ** แม้ mode mTLS จะใช้ UID เป็น client id ก็ตาม — ถ้าใช้ UID ในหัวข้อ ACL จะปฏิเสธ ข้อความดูเหมือนหายไปเฉย ๆ

**WiFi จากที่เก็บ ไม่ใช่ `#define`** ETSI 5.4-3 ห้ามฝังค่าความปลอดภัยในซอร์ส — ไม่พิมพ์ passphrase เลย พิมพ์แค่ความยาว, ล้างบัฟเฟอร์ผ่าน `volatile` pointer

---

## แนวคิด (3) — MQTTs หรือ HTTPS

| | MQTTs | HTTPS |
|---|---|---|
| รูปแบบ | session เปิดค้าง | ถามตอบทีละคำขอ |
| คำสั่งจากแพลตฟอร์ม | มาเองทาง subscription | ต้องถามเป็นระยะ |
| พอร์ต/ยืนยันตัว | 8884 user/pass · 8883 mTLS | 443 header X-API-KEY · 9444 mTLS |
| เหมาะกับ | telemetry ต่อเนื่อง+รับคำสั่ง | ส่งเป็นครั้งคราว, ไฟล์ใหญ่ |

ข้อควรระวัง: บาง path HTTPS ตั้ง `CY_AWS_ROOTCA_VERIFY_NONE` (เข้ารหัสแต่ไม่ตรวจใบเซิร์ฟเวอร์) — มีทาง plaintext แยกฟังก์ชัน (`claw_http_connect_insecure`) เฉพาะ endpoint สาธารณะที่ไม่มีกุญแจ

---

## ตัวอย่างสมบูรณ์ — WiFi จากที่เก็บ ไม่พิมพ์รหัสผ่าน

```c
static tesaiot_config_t cfg;
tesaiot_config_get(&cfg);
if (cfg.wifi_ssid[0] != '\0') {
    snprintf(s_ssid, sizeof(s_ssid), "%s", cfg.wifi_ssid);
    snprintf(s_pass, sizeof(s_pass), "%s", cfg.wifi_pass);
    wipe(cfg.wifi_pass, sizeof(cfg.wifi_pass));   /* ล้างทั้งสองทางออก */
    return "tesaiot_config_store";
}
```

```c
/* The passphrase is never printed: the console is not the radio, and
 * this console is often a shared screen. */
printf("  ssid=\"%s\" security=\"%s\" passphrase=%u byte(s), not shown\r\n",
       s_ssid, s_sec, (unsigned)strlen(s_pass));
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม** เขียนการเรียก `tesaiot_mqtt_publish(NULL, payload, sizeof(payload)-1)` — `NULL` ให้ฟังก์ชันสร้างหัวข้อ telemetry เอง `false` ที่คืนมาแปลได้หลายอย่าง (ยังไม่เชื่อมต่อ, คิวเต็ม, ไม่มี device_id) `true` แปลแค่ว่า**เข้าคิวแล้ว**

**แล็บ**

1. ใส่ WiFi credentials ลงที่เก็บ (ไม่ใช่ซอร์ส) build ด้วย `EXAMPLE_WIFI_JOIN=1` — `grep -r` ทั้งโปรเจกต์ต้องไม่เจอ SSID/รหัส
2. ตั้งค่า MQTT รวม `port=1883` ไว้ทดสอบคำทาย เชื่อมต่อ ดูพอร์ตจริงใน log
3. subscribe จากคอมพิวเตอร์**ก่อน** แล้วให้บอร์ด publish พิสูจน์ว่าข้อมูลถึงจากฝั่งผู้รับ
4. ปล่อยเงียบเกิน 90 วินาที publish อีกครั้ง ผ่านไหม

---

## เช็กความเข้าใจ

1. ไฟล์ตั้งค่ามี `tls_mode=server_tls` และ `port=1883` บอร์ดจะต่อ broker ที่พอร์ตใด
   - ก) 1883 · ข) 8883 · ค) 8884 · ง) 443

2. ทำไมตัวอย่าง `10_wifi_join.c` จึงปฏิเสธการทำงานเมื่อไม่พบข้อมูลรับรองในที่เก็บ แทนที่จะใช้ SSID สำรองในโค้ด
   - ก) เพราะ SSID สำรองกินหน่วยความจำ · ข) เพราะ credential ที่คอมไพล์ติดโค้ดคือ credential ที่หลุดไปกับที่เก็บโค้ดสาธารณะ ซึ่งขัดกับ ETSI ข้อ 5.4-3 · ค) เพราะ WiFi ไม่รองรับ SSID สำรอง · ง) เพราะ compiler ไม่ยอม

3. `tesaiot_mqtt_publish()` คืน `true` ข้อสรุปใดถูก
   - ก) ข้อความถึง broker แล้วแน่นอน · ข) ข้อความเข้าคิวของ publisher แล้ว การพิสูจน์ว่าถึงต้องดูจากฝั่งผู้รับ · ค) แพลตฟอร์มบันทึกข้อมูลแล้ว · ง) ใบรับรองของ broker ผ่านการตรวจแล้ว

---

## ไปต่อ

อุปกรณ์ของเราเชื่อมต่อได้อย่างปลอดภัยแล้ว คำถามต่อไปคือ เฟิร์มแวร์ที่รันอยู่เป็นตัวที่เราตั้งใจให้รันจริงไหม โมดูล 4 จะดูห่วงโซ่ความเชื่อใจตั้งแต่บูต

บทเรียนถัดไป: [บทเรียน 4.1: Secure boot และ chain of trust](../../m04-secure-boot-and-update/l01-secure-boot/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
