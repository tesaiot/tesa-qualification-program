---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.8 — โมดูล tesaiot: MQTTs สู่แพลตฟอร์ม"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก AIoT in Action (AIC มหาวิทยาลัยบูรพา) · CC BY 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 330px; width: 100%; }
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
/* พื้นสำรองของสไลด์ปก: ถ้า img/cover_sNN.svg โหลดไม่ขึ้น ธีมจะคืนพื้นขาว
   แล้วตัวอักษรสีขาวของปกจะหายไปทั้งแผ่น — ปักสีเข้มไว้ให้ภาพเป็นแค่ของประดับ */
section.cover{background-color:#0b1426}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

![ภาพพื้นหลังปกบทเรียน bg](../../assets/img/cover_s11.svg)

<!-- _class: cover -->

# บทเรียน 4.8 — โมดูล tesaiot: MQTTs สู่แพลตฟอร์ม

## MQTTs (serverTLS) · จากพอร์ต 1883 ที่ใครก็อ่านได้ ไปพอร์ต 8884 ที่รู้ว่ากำลังคุยกับใคร

**โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT**

> ต่อจากบทเรียน 4.7 — TLS: ใบรับรอง ห่วงโซ่ความเชื่อถือ และการจับมือ

---

## เรื่องที่เราให้ 70% ผู้เรียนเขียน 30%

<svg viewBox="0 0 900 170" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="24" width="596" height="78" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="318" y="56" text-anchor="middle" font-size="23" font-weight="700" fill="#1565c0">70% — เฟิร์มแวร์ + แพลตฟอร์มทำให้แล้ว</text>
  <text x="318" y="88" text-anchor="middle" font-size="18" fill="#5472a3">TLS · ใบรับรอง · root CA · broker · ฐานข้อมูล · กราฟ</text>
  <rect x="624" y="24" width="256" height="78" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="752" y="56" text-anchor="middle" font-size="23" font-weight="700" fill="#ef6c00">30% — งานของเรา</text>
  <text x="752" y="88" text-anchor="middle" font-size="18" fill="#a1683a">ตัวตน · การรอ · หลักฐาน</text>
  <text x="450" y="136" text-anchor="middle" font-size="20" font-weight="700" fill="#455a64">โค้ดวันนี้สั้นกว่าบทเรียน 4.4–4.6 แต่ตอบผิดหนึ่งข้อแล้วต่อไม่ติดทั้งบทเรียน</text>
  <text x="450" y="160" text-anchor="middle" font-size="17" fill="#78909c">งานที่เหลือให้เราไม่ใช่การพิมพ์ แต่คือการรู้ว่าอะไรพิสูจน์อะไร</text>
</svg>

**สิ่งที่ทำให้แล้ว (70%)**
การจับมือ TLS ทั้งหมด · การตรวจใบรับรองย้อนขึ้นไปถึง root · root CA ที่ฝังมากับเฟิร์มแวร์ · การเลือกพอร์ตจาก `tls_mode` · การประกอบ topic จาก `device_id` · ฝั่งแพลตฟอร์ม: broker EMQX, บริดจ์ที่รอ subscribe อยู่แล้ว, ฐานข้อมูลอนุกรมเวลา และกราฟที่สร้างจากชื่อคีย์ JSON อัตโนมัติ

**สิ่งที่เป็นงานของเรา (30%)**
ตั้งค่าตัวตนของอุปกรณ์ให้ถูกทั้งสี่ค่า · **รอให้การเชื่อมต่อเสร็จจริงก่อนส่ง** · เลือกว่าจะส่งฟิลด์อะไรเป็นตัวเลข · และแสดงหลักฐานบนจอให้คนอื่นตรวจได้โดยไม่ต้องเปิดโค้ด

> ยิ่งไลบรารีทำให้เยอะ ความผิดพลาดที่เหลือยิ่ง **เงียบ** — เพราะสิ่งที่เหลือให้เราพลาดคือเรื่องที่ไลบรารีไม่มีทางรู้ว่าเราตั้งใจอะไร

---

## `import tesaiot` ได้มา 28 ชื่อ — ใช้ได้จริงเก้าตัว ทั้ง Eva Kit และ Dev Kit

<style scoped>section svg{max-height:225px} section p{margin:.12em 0;font-size:.93em} section blockquote{font-size:.93em}</style>

<svg viewBox="0 0 940 264" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="10" width="290" height="244" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="161" y="40" text-anchor="middle" font-size="20" font-weight="700" fill="#2e7d32">เก้าตัวที่ทำงาน</text>
  <text x="161" y="64" text-anchor="middle" font-size="16" fill="#1b5e20">ทั้งหมดอยู่บน CM33 ไม่ข้ามคอร์</text>
  <text x="36" y="96" font-size="17" font-family="monospace" fill="#1b5e20">config()  config_set()</text>
  <text x="36" y="122" font-size="17" font-family="monospace" fill="#1b5e20">config_reset()</text>
  <text x="36" y="148" font-size="17" font-family="monospace" fill="#1b5e20">config_reload()</text>
  <text x="36" y="174" font-size="17" font-family="monospace" fill="#1b5e20">connect()  disconnect()</text>
  <text x="36" y="200" font-size="17" font-family="monospace" fill="#1b5e20">is_connected()  publish()</text>
  <text x="36" y="226" font-size="17" font-family="monospace" fill="#1b5e20">slots()</text>
  <text x="36" y="248" font-size="16" fill="#2e7d32">ทั้งชุดบทเรียนนี้ใช้แค่กล่องนี้</text>
  <rect x="322" y="10" width="330" height="244" rx="9" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="487" y="40" text-anchor="middle" font-size="20" font-weight="700" fill="#c62828">สิบหกตัวที่ข้ามคอร์ไปหาชิป</text>
  <text x="487" y="64" text-anchor="middle" font-size="16" fill="#8f1f1f">ส่ง IPC ไป CM55 ที่ประกอบมาโดยไม่มี OPTIGA</text>
  <text x="342" y="96" font-size="17" font-family="monospace" fill="#8f1f1f">init()  device_id()  health()</text>
  <text x="342" y="122" font-size="17" font-family="monospace" fill="#8f1f1f">license_verify()  sign()</text>
  <text x="342" y="148" font-size="17" font-family="monospace" fill="#8f1f1f">cred_read/write/erase()</text>
  <text x="342" y="174" font-size="17" font-family="monospace" fill="#8f1f1f">random()  hash()  hmac()</text>
  <text x="342" y="200" font-size="17" font-family="monospace" fill="#8f1f1f">aes_keygen()  encrypt()  decrypt()</text>
  <text x="342" y="226" font-size="17" font-family="monospace" fill="#8f1f1f">counter_read()  counter_inc()</text>
  <text x="342" y="248" font-size="16" fill="#c62828">ยังไม่ได้วัดเวลาจริง — อย่าเรียกในลูป</text>
  <rect x="668" y="10" width="256" height="244" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="796" y="40" text-anchor="middle" font-size="20" font-weight="700" fill="#ef6c00">อีกสามตัว คนละเรื่อง</text>
  <text x="688" y="68" font-size="17" font-family="monospace" fill="#c62828">protected_update()</text>
  <text x="688" y="92" font-size="16" font-weight="700" fill="#c62828">ห้ามเรียกในชุดบทเรียนนี้</text>
  <text x="688" y="114" font-size="16" fill="#c62828">Eva: ปิดไว้ (OSError)</text>
  <text x="688" y="134" font-size="16" fill="#c62828">Dev Kit: เขียนลงชิปจริง</text>
  <text x="688" y="166" font-size="17" font-family="monospace" fill="#a1683a">http_post()</text>
  <text x="688" y="188" font-size="16" fill="#a1683a">HTTPS จาก CM33 ตาม tls_mode</text>
  <text x="688" y="220" font-size="17" font-family="monospace" fill="#a1683a">device_identity()</text>
  <text x="688" y="242" font-size="16" fill="#a1683a">ตัวตนบอร์ดให้หน้า Add Device</text>
</svg>

**พูดให้ตรง**: ทั้งสองบอร์ดประกอบเฟิร์มแวร์ของคอร์จอด้วย `ENABLE_OPTIGA ?= 0` สิบหกคำสั่งที่ข้ามคอร์จึงไม่มีชิปให้คุย · ซอร์สบอกว่าคอร์จอตอบ "ไม่มีให้" กลับมาโดยไม่รอชิป แล้วฝั่ง Python โยน `OSError` พร้อมข้อความ (เพดานรอ 10 วินาทีมีไว้กรณีคอร์จอไม่ตอบเลย) — **ยังไม่ได้วัดเวลาจริงบนบอร์ดไหน** ลอง `t=time.ticks_ms(); tesaiot.health(); print(time.ticks_diff(time.ticks_ms(), t))` บนโต๊ะก่อนสอน แล้วบอกผู้เรียนด้วยตัวเลขที่วัดได้

**เรื่องเดียวที่สองบอร์ดต่างกันจริง คือ `tesaiot.protected_update()`** — บน Eva ไม่ได้ถูกคอมไพล์เข้ามา (`OSError`) แต่บน Dev Kit (`ENABLE_OPTIGA_CLM=1`) มัน**ทำงานจริง**: ขอชุด Protected Update จากแพลตฟอร์มแล้วเขียนใบรับรองลงช่อง E0E1 ของชิป OPTIGA และ `csr=True` สร้างคู่กุญแจใหม่ทับของเดิม — **ห้ามเรียกในชุดบทเรียนนี้** ทั้งจากไฟล์ตัวอย่างและ REPL เพราะสิ่งที่เขียนลงชิปย้อนกลับเองไม่ได้

> **ชิป OPTIGA มีอยู่จริงและใช้ได้** ผ่านโมดูล `optiga` (สไลด์โบนัสท้ายบทเรียน) — Eva: I2C จาก CM33 ตรง ๆ · Dev Kit: ชิปอยู่บนบัสจอของ CM55 จอหยุดรับสัมผัสชั่วครู่ทุกครั้งที่เรียก และยังไม่ได้ตรวจว่าทุกบอร์ดมีชิปครบ — ลอง `optiga.uid()` ก่อน

<!-- ที่ต้องบอกกันไว้ก่อน เพราะถ้าไม่บอก ผู้เรียนจะไปเจอเองตอนนั่งดีบักแล้วเข้าใจว่าตัวเองเขียนผิด ทั้งที่ไม่ได้ผิดเลย · แหล่งที่ดู: ipc_service.c handle_tesaiot() ตอบ status 0xFD เมื่อไม่มี ENABLE_OPTIGA · modtesaiot.c tesaiot_ipc_send() รอสูงสุด TESAIOT_IPC_RESPONSE_TIMEOUT_MS = 10000 เฉพาะเมื่อไม่มีคำตอบ และ wrapper แต่ละตัว mp_raise_msg(OSError, "... failed") -->

---

## เก้าตัวที่ใช้ได้ — ตารางเต็มพร้อมกับดักของแต่ละตัว

| เรียกอย่างไร | คืนอะไร | สิ่งที่ต้องรู้ |
|---|---|---|
| `tesaiot.config()` | dict **19 คีย์** | คีย์ครบชุด: `tls_mode` `device_id` `factory_uid` `api_key` `broker` `port` `sni_hostname` `qos` `keepalive` `timeout_ms` `max_retries` `retry_interval_ms` `api_host` `api_port` `api_endpoint` `wifi_ssid` `sntp_server` `sntp_timezone` `debug_level` |
| `tesaiot.config_set(key, value)` | `True` / `False` | รับ **สตริงทั้งสองช่อง** ตัวเลขก็ต้องส่งเป็นสตริง · คีย์ผิดคืน `False` เงียบ ๆ ต้องรับค่ากลับมาดู · ตั้ง `"tls_mode","server_tls"` แล้วอ่านกลับได้ `"serverTLS"` เพราะมันแปลงชื่อให้ |
| `tesaiot.config_reset()` | `None` | ล้างกลับเป็นค่าโรงงาน **ทั้ง 19 คีย์** ตัวตนของอุปกรณ์หายหมด ต้องตั้งใหม่ทุกค่า |
| `tesaiot.config_reload()` | `True` / `False` | อ่านไฟล์ตั้งค่าจากแฟลชขึ้นมาใหม่ ทับค่าที่แก้ไว้ในหน่วยความจำ · ใช้ทิ้งการแก้ที่ยังไม่พอใจ (ข้อควรรู้: ในซอร์ส `tesaiot_config_store.c` ปัจจุบัน `config_set()` เซฟลงแฟลชทุกครั้ง reload จึงอาจย้อนค่าที่ตั้งด้วย `config_set()` ไม่ได้ — ต้องยืนยันบนบอร์ด) |
| `tesaiot.connect()` | `True` / `False` | `True` แปลว่า **งานเริ่มแล้ว** ไม่ใช่ต่อเสร็จแล้ว ต้องวนรอ `is_connected()` เอง |
| `tesaiot.disconnect()` | `True` / `False` | ตัวนี้คืน bool ไม่เหมือน `mqtt.disconnect()` ที่คืน `None` — สองโมดูลไม่เหมือนกัน |
| `tesaiot.is_connected()` | `True` / `False` | ตัวจริงที่ตอบว่าต่อเสร็จหรือยัง |
| `tesaiot.publish(payload, topic=None)` | `True` / `False` | **payload มาก่อน topic** และ topic ใส่หรือไม่ใส่ก็ได้ ไม่ใส่แล้วเฟิร์มแวร์ประกอบให้จาก `device_id` |
| `tesaiot.slots()` | dict 13 คู่ | ตอบได้ทันทีโดยไม่แตะชิป เพราะเป็นตารางชื่อในซอร์ส · ช่อง 4 ถูกกันไว้ จึงไม่อยู่ในรายการ |

**`tesaiot.publish()` กับ `mqtt.publish()` สลับลำดับกัน** — ชุดบทเรียนก่อนหน้าเขียน `mqtt.publish(topic, payload)` วันนี้เขียน `tesaiot.publish(payload)` สลับเมื่อไรได้ผลประหลาดทันทีโดยไม่มี error เพราะทั้งสองช่องรับสตริงเหมือนกัน

> `config_set()` เก็บค่าไว้เฉย ๆ **ยังไม่ได้ต่ออะไรทั้งนั้น** พิมพ์คีย์ผิดจะไม่มีใครเตือนจนกว่าจะต่อไม่ติด — จึงต้อง `print(tesaiot.config())` หนึ่งครั้งหลังตั้งค่าเสมอ

---

## แกะโค้ดจริง — ท่าที่ 1 ตั้งค่าตัวตนของอุปกรณ์

```python
# --- ท่าที่ 1: ตั้งค่าตัวตนของอุปกรณ์ ---
tesaiot.config_set("device_id", DEVICE_ID)
tesaiot.config_set("api_key", API_KEY)
tesaiot.config_set("mqtt_pass", MQTT_PASS)
tesaiot.config_set("broker", BROKER)
tesaiot.config_set("sni_hostname", BROKER)     # ต้องเป็นชื่อเดียวกับ broker
print("config ปัจจุบัน:", tesaiot.config())
```

<div style="display:flex;gap:18px;align-items:flex-start">
<div style="flex:1">

`config_set()` รับ **ทีละคู่ (key, value)** และแค่ **เก็บค่าไว้ในเฟิร์มแวร์** ยังไม่ได้ต่ออะไรทั้งสิ้น — พิมพ์ชื่อคีย์ผิดก็ไม่มีใครเตือน ค่าที่ผิดจะไปโผล่ตอนต่อไม่ติดเท่านั้น

จึงต้อง `print(tesaiot.config())` ทุกครั้งหลังตั้งค่า **ก่อน** จะไปท่าถัดไป — เป็นวิธีเดียวที่เห็นว่าค่าเข้าครบและสะกดถูก

`device_id` ต้อง **สั้นกว่า 31 ตัวอักษร** เกินแล้วถูกตัดเงียบ แล้วแพลตฟอร์มจะหาอุปกรณ์ไม่เจอ

</div>
<div style="width:290px">

<svg viewBox="0 0 290 210" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="12" width="270" height="186" rx="9" fill="#f5f7fa" stroke="#455a64" stroke-width="2"/>
  <text x="145" y="40" text-anchor="middle" font-size="19" font-weight="700" fill="#37474f">ตัวตน = สามอย่างรวมกัน</text>
  <rect x="18" y="54" width="254" height="34" rx="5" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="145" y="77" text-anchor="middle" font-size="16" fill="#0d47a1">device_id — ชื่อที่แพลตฟอร์มรู้จัก</text>
  <rect x="18" y="96" width="254" height="34" rx="5" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="145" y="119" text-anchor="middle" font-size="16" fill="#1b5e20">api_key — กุญแจของ API</text>
  <rect x="18" y="138" width="254" height="34" rx="5" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="145" y="161" text-anchor="middle" font-size="16" fill="#e65100">mqtt_pass — รหัสของ broker</text>
  <circle cx="252" cy="186" r="8" fill="#c62828"><animate attributeName="r" values="5;10;5" dur="1.8s" repeatCount="indefinite"/></circle>
  <text x="26" y="192" font-size="16" fill="#78909c">ขาดข้อใดข้อหนึ่ง = ถูกปฏิเสธ</text>
</svg>

</div>
</div>

> `sni_hostname` ไม่ใช่ค่าเสริม — มันคือชื่อที่ทำให้เซิร์ฟเวอร์ **หยิบใบรับรองใบที่ถูกมายื่นให้เรา** ตั้งไม่ตรงเมื่อไร การจับมือล้มโดยไม่มีข้อความบอก

---

## แกะโค้ดจริง — ท่าที่ 2 สั่งต่อ แล้ววนรอจนต่อเสร็จจริง

<style scoped>section pre{font-size:.58em;line-height:1.22} section svg{max-height:150px} section p{margin:.1em 0}</style>

```python
# --- connect() เป็น API แบบ asynchronous ---
tesaiot.connect()                       # คืนค่าทันที ยังไม่ได้แปลว่าต่อแล้ว
t0 = time.ticks_ms()
...
while not tesaiot.is_connected():       # ตัวจริงที่ตอบได้คือ is_connected()
    waited = time.ticks_diff(time.ticks_ms(), t0)
    if waited > WAIT_CEILING_S * 1000:  # WAIT_CEILING_S = 30 ตัวเลขเดียวกับบนจอ
        print("ต่อแพลตฟอร์มไม่สำเร็จใน 30 วินาที")
        break
    ...
    time.sleep_ms(500)
```

<svg viewBox="0 0 940 200" xmlns="http://www.w3.org/2000/svg">
  <line x1="40" y1="70" x2="900" y2="70" stroke="#b0bec5" stroke-width="4"/>
  <circle cx="90" cy="70" r="12" fill="#1565c0"/>
  <text x="90" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="#1565c0">connect()</text>
  <text x="90" y="100" text-anchor="middle" font-size="17" fill="#455a64">คืนค่าตรงนี้</text>
  <rect x="150" y="56" width="150" height="28" rx="5" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="225" y="76" text-anchor="middle" font-size="17" fill="#0d47a1">TCP จับมือ</text>
  <rect x="310" y="56" width="220" height="28" rx="5" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="420" y="76" text-anchor="middle" font-size="17" fill="#1b5e20">TLS จับมือ + ตรวจใบรับรอง</text>
  <rect x="540" y="56" width="170" height="28" rx="5" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="625" y="76" text-anchor="middle" font-size="17" fill="#e65100">MQTT CONNECT</text>
  <circle cx="760" cy="70" r="12" fill="#2e7d32"><animate attributeName="r" values="8;14;8" dur="2s" repeatCount="indefinite"/></circle>
  <text x="930" y="46" text-anchor="end" font-size="18" font-weight="700" fill="#2e7d32">is_connected() เป็น True ตรงนี้</text>
  <text x="930" y="100" text-anchor="end" font-size="17" fill="#455a64">หลายวินาทีหลังจากนั้น</text>
  <circle r="9" fill="#e91e63" cx="90" cy="70"><animateMotion path="M0,0 L135,0 L330,0 L535,0 L670,0" dur="3.6s" repeatCount="indefinite"/><animate attributeName="r" values="6;12;6" dur="3.6s" repeatCount="indefinite"/></circle>
  <text x="470" y="146" text-anchor="middle" font-size="20" font-weight="700" fill="#c62828">publish() ที่เขียนต่อท้าย connect() ทันที จะยิงลงช่วงกลางเส้นนี้ แล้วหายไปเงียบ ๆ</text>
  <text x="470" y="176" text-anchor="middle" font-size="18" fill="#78909c">ลูปรอทุกลูปต้องมี timeout — ไม่งั้นวันที่เน็ตล่ม โปรแกรมค้างตรงนี้ตลอดกาลโดยไม่มีใครรู้</text>
</svg>

`tesaiot.connect()` เป็น API แบบ **asynchronous** คืนค่าทันทีเพื่อไม่บล็อกโปรแกรม — ค่าที่คืนมา **ไม่ใช่สถานะสุดท้าย** สิ่งเดียวที่ตอบได้ว่าต่อเสร็จหรือยังคือ `tesaiot.is_connected()` · โจทย์ต่อ: ให้ลบลูปนี้ออกแล้วรันหนึ่งรอบ — จะเห็นด้วยตาว่า publish ที่ยิงเร็วเกินไป **ไม่ error และไม่ถึงแพลตฟอร์ม**

> "ฟังก์ชันคืนค่าแล้ว" กับ "งานเสร็จแล้ว" เป็นคนละเรื่องเสมอสำหรับ API แบบ async — ความต่างนั้นวัดได้เป็นวินาที

---

## แกะโค้ดจริง — ท่าที่ 3 และ 4 ส่งค่าจริง แล้วโชว์หลักฐานบนจอ

```python
m = sensors.bmi270.motion()                       # (ax, ay, az, gx, gy, gz)
payload = {"accel_x": round(m[0], 2),
           "heading": round(sensors.bmm350.heading(), 1),
           "pot": sensors.pot.percent()}
tesaiot.publish(json.dumps(payload))              # ไม่ต้องใส่ topic เฟิร์มแวร์ประกอบให้
cfg = tesaiot.config()
lcd.print("ส่งครั้งที่", sent, "| โหมด", cfg["tls_mode"], "-> 8884")
```

<svg viewBox="0 0 940 176" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="20" width="196" height="120" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="112" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="#2e7d32">ค่าจากเซนเซอร์</text>
  <text x="112" y="76" text-anchor="middle" font-size="18" fill="#1b5e20">ax · heading · pot</text>
  <text x="112" y="102" text-anchor="middle" font-size="17" fill="#4a7c4e">round() ก่อนเสมอ</text>
  <text x="112" y="128" text-anchor="middle" font-size="17" fill="#4a7c4e">ตัวเลขจริง ไม่ใช่สตริง</text>
  <rect x="238" y="20" width="216" height="120" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
  <text x="346" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="#7ee787">ส่งแบน ไม่ต้องห่อ</text>
  <text x="346" y="78" text-anchor="middle" font-size="17" font-family="monospace" fill="#a5d6ff">{"accel_x":0.12,</text>
  <text x="346" y="100" text-anchor="middle" font-size="17" font-family="monospace" fill="#a5d6ff">"heading":183.4}</text>
  <text x="346" y="128" text-anchor="middle" font-size="17" fill="#8b949e">แพลตฟอร์มห่อให้เอง ชื่อคีย์ตรงได้หน่วย</text>
  <rect x="482" y="20" width="212" height="120" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="588" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="#1565c0">เข้ารหัสแล้วส่ง</text>
  <text x="588" y="78" text-anchor="middle" font-size="18" fill="#0d47a1">พอร์ต 8884</text>
  <text x="588" y="104" text-anchor="middle" font-size="17" fill="#5472a3">topic ประกอบจาก device_id</text>
  <text x="588" y="130" text-anchor="middle" font-size="17" fill="#5472a3">เราไม่ต้องพิมพ์ topic เอง</text>
  <rect x="722" y="20" width="204" height="120" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="824" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="#ef6c00">จอบอร์ด</text>
  <text x="824" y="78" text-anchor="middle" font-size="18" fill="#e65100">ตัวนับเดินขึ้น</text>
  <text x="824" y="104" text-anchor="middle" font-size="18" fill="#e65100">tls_mode ที่ใช้จริง</text>
  <circle cx="900" cy="126" r="9" fill="#ef6c00"><animate attributeName="r" values="6;12;6" dur="1.6s" repeatCount="indefinite"/></circle>
  <line x1="214" y1="80" x2="234" y2="80" stroke="#90a4ae" stroke-width="2"/>
  <line x1="458" y1="80" x2="478" y2="80" stroke="#90a4ae" stroke-width="2"/>
  <line x1="698" y1="80" x2="718" y2="80" stroke="#90a4ae" stroke-width="2"/>
  <text x="470" y="166" text-anchor="middle" font-size="18" font-weight="700" fill="#455a64">ท่าที่ 4 ไม่ใช่ของประดับ — มันคือหลักฐานที่กรรมการอ่านได้โดยไม่ต้องเปิดโค้ด</text>
</svg>

`tesaiot.publish(payload)` รับ **ตัวข้อมูลอย่างเดียว** — ต่างจาก `mqtt.publish(topic, payload)` ของชุดบทเรียนที่แล้ว เพราะเฟิร์มแวร์ประกอบ topic ให้เองจาก `device_id` ที่เราตั้งไว้ในท่าที่ 1 (จะระบุ topic เองก็ได้ แต่ชุดบทเรียนนี้ไม่ต้อง) · ส่ง **ตัวเลขจริง** ไม่ใช่สตริง ไม่งั้น dashboard จะขึ้นค่าแต่วาดกราฟไม่ได้ — กับดักเดียวกับบทเรียน 4.4–4.6

> จอบอร์ดต้องตอบคำถาม MVP ได้เอง: **ทีมไหน · โหมดอะไร · ส่งไปกี่ครั้งแล้ว** สามอย่างนี้ทำให้คนอื่นตรวจงานเราได้โดยไม่ต้องถาม

---

## ข้อมูลไหลไปทางไหน — ตั้งแต่เซนเซอร์ถึงกราฟ

<svg viewBox="0 0 940 250" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="a11" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#455a64"/></marker></defs>
  <rect x="10" y="76" width="126" height="72" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="73" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#2e7d32">เซนเซอร์</text>
  <text x="73" y="130" text-anchor="middle" font-size="17" fill="#1b5e20">BMI270 · pot</text>
  <rect x="162" y="76" width="126" height="72" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="225" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#1565c0">โค้ดของเรา</text>
  <text x="225" y="130" text-anchor="middle" font-size="17" fill="#0d47a1">json.dumps</text>
  <rect x="314" y="76" width="140" height="72" rx="9" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2.5"/>
  <text x="384" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#6a1b9a">ชั้น TLS</text>
  <text x="384" y="130" text-anchor="middle" font-size="17" fill="#4a148c">เข้ารหัสทุกไบต์</text>
  <rect x="480" y="76" width="140" height="72" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="550" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#ef6c00">EMQX</text>
  <text x="550" y="130" text-anchor="middle" font-size="17" fill="#e65100">listener 8884</text>
  <rect x="646" y="76" width="140" height="72" rx="9" fill="#e0f7fa" stroke="#00695c" stroke-width="2"/>
  <text x="716" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#00695c">บริดจ์ + ฐานข้อมูล</text>
  <text x="716" y="130" text-anchor="middle" font-size="17" fill="#00695c">อนุกรมเวลา</text>
  <rect x="812" y="76" width="118" height="72" rx="9" fill="#eceff1" stroke="#455a64" stroke-width="2"/>
  <text x="871" y="106" text-anchor="middle" font-size="19" font-weight="700" fill="#455a64">กราฟ</text>
  <text x="871" y="130" text-anchor="middle" font-size="17" fill="#37474f">อัปเดตสด</text>
  <line x1="138" y1="112" x2="158" y2="112" stroke="#455a64" stroke-width="2.5" marker-end="url(#a11)"/>
  <line x1="290" y1="112" x2="310" y2="112" stroke="#455a64" stroke-width="2.5" marker-end="url(#a11)"/>
  <line x1="456" y1="112" x2="476" y2="112" stroke="#455a64" stroke-width="2.5" marker-end="url(#a11)"/>
  <line x1="622" y1="112" x2="642" y2="112" stroke="#455a64" stroke-width="2.5" marker-end="url(#a11)"/>
  <line x1="788" y1="112" x2="808" y2="112" stroke="#455a64" stroke-width="2.5" marker-end="url(#a11)"/>
  <circle r="9" fill="#e91e63" cx="148" cy="112"><animateMotion path="M0,0 L77,0 L236,0 L402,0 L568,0 L723,0" dur="4.4s" repeatCount="indefinite"/><animate attributeName="r" values="6;12;6" dur="4.4s" repeatCount="indefinite"/></circle>
  <text x="470" y="34" text-anchor="middle" font-size="20" font-weight="700" fill="#37474f">กล่องสีม่วงคือทั้งหมดที่เพิ่มมาจากบทเรียน 4.4–4.6 — ที่เหลือเหมือนเดิมทุกกล่อง</text>
  <text x="470" y="58" text-anchor="middle" font-size="18" fill="#6a1b9a">และมันอยู่ในเฟิร์มแวร์ ไม่ได้อยู่ในโค้ดที่เราเขียน</text>
  <text x="470" y="192" text-anchor="middle" font-size="19" font-weight="700" fill="#455a64">ดีบักตามลำดับนี้เสมอ: is_connected() → print(config()) → กราฟบนแพลตฟอร์ม</text>
  <text x="470" y="220" text-anchor="middle" font-size="18" fill="#78909c">ถ้า is_connected() ยัง False ปัญหายังไม่เดินทางไปถึงเรื่อง topic หรือรูปร่าง JSON เลย</text>
  <text x="470" y="244" text-anchor="middle" font-size="18" fill="#c62828">อย่าเริ่มเดาจากปลายทาง — กราฟว่างเปล่าบอกได้แค่ว่า "ไม่ถึง" ไม่ได้บอกว่าตกตรงไหน</text>
</svg>

> ระบบยาวหกกล่อง แต่การดีบักไม่เคยยาวกว่า **"หาให้เจอว่ากล่องสุดท้ายที่ยังเห็นข้อมูลคือกล่องไหน"** — ชุดบทเรียนนี้กล่องแรกที่ต้องตรวจคือ `is_connected()`

---

## อีกสี่ตัวที่โครงหลักไม่ได้เรียก — แต่ต้องเคยลอง

<style scoped>section pre{font-size:.56em;line-height:1.2} section svg{max-height:150px} section p{margin:.1em 0}</style>

```python
# --- ล้างแล้วตั้งใหม่: ทางออกเมื่อตั้งค่ามั่วจนไม่รู้ว่าเหลืออะไรอยู่ ---
tesaiot.config_reset()            # คืน None และล้างครบทั้ง 19 คีย์
tesaiot.config_set("device_id", DEVICE_ID)   # ต้องตั้งใหม่ทุกค่า

# --- ทิ้งการแก้ที่ยังไม่พอใจ แล้วดึงของเดิมจากแฟลชกลับมา ---
tesaiot.config_reload()           # True ถ้าอ่านไฟล์ตั้งค่าสำเร็จ

# --- ชื่อช่องเก็บความลับ ตอบได้โดยไม่ต้องแตะชิป ---
print(tesaiot.slots())            # {'device_id': 0, 'license': 1, ...}

# --- ปิดงานให้เรียบร้อย ตัวนี้คืน bool ไม่เหมือน mqtt.disconnect() ---
tesaiot.disconnect()
```

<svg viewBox="0 0 940 208" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="12" width="286" height="180" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="159" y="42" text-anchor="middle" font-size="20" font-weight="700" fill="#ef6c00">config_reset()</text>
  <text x="36" y="76" font-size="18" fill="#a1683a">ล้างครบทั้ง 19 คีย์</text>
  <text x="36" y="104" font-size="18" fill="#a1683a">ตัวตนของอุปกรณ์หายด้วย</text>
  <text x="36" y="132" font-size="18" fill="#a1683a">ต้องตั้งใหม่ทุกค่าก่อนต่อ</text>
  <text x="36" y="170" font-size="18" font-weight="700" fill="#c62828">ใช้ตอนหลงทางเท่านั้น</text>
  <rect x="318" y="12" width="286" height="180" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="461" y="42" text-anchor="middle" font-size="20" font-weight="700" fill="#1565c0">config_reload()</text>
  <text x="338" y="76" font-size="18" fill="#0d47a1">อ่านไฟล์จากแฟลชกลับมา</text>
  <text x="338" y="104" font-size="18" fill="#0d47a1">ทับค่าที่แก้ค้างไว้</text>
  <text x="338" y="132" font-size="18" fill="#0d47a1">ของที่ยังไม่ได้เซฟหายไป</text>
  <text x="338" y="170" font-size="18" font-weight="700" fill="#1565c0">ใช้ตอนอยากย้อนกลับ</text>
  <rect x="620" y="12" width="304" height="180" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="772" y="42" text-anchor="middle" font-size="20" font-weight="700" fill="#2e7d32">slots()</text>
  <text x="640" y="76" font-size="18" fill="#1b5e20">คืนชื่อช่องเก็บความลับ 13 ช่อง</text>
  <text x="640" y="104" font-size="18" fill="#1b5e20">ตอบทันที ไม่แตะชิป ไม่ค้าง</text>
  <text x="640" y="132" font-size="18" fill="#1b5e20">ช่อง 4 ถูกกันไว้ ไม่อยู่ในนี้</text>
  <text x="640" y="170" font-size="18" font-weight="700" fill="#2e7d32">แผนที่ของงานบทเรียนต่อ ๆ ไป</text>
</svg>

**`config_reset()` ล้างของจริง** ส่วน **`config_reload()` แค่ย้อนกลับไปหาของที่เซฟไว้** — ตั้งค่ามั่วจนงงว่าเหลืออะไรอยู่ ให้ `config_reset()` แล้วเริ่มใหม่จากศูนย์ ดีกว่าไล่แก้ทีละคีย์ · `slots()` **ตอบได้โดยไม่ต้องข้ามคอร์ไปถามชิป** เพราะอ่านตารางชื่อในเฟิร์มแวร์ — แผนที่ว่าถ้าวันหนึ่งเปิด OPTIGA ได้ ความลับแต่ละอย่างจะไปนอนช่องไหน · `tesaiot.disconnect()` **คืน `True`/`False`** ไม่เหมือน `mqtt.disconnect()` ที่คืน `None` อย่าจำรวมกัน

> [`01_config_store.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/01_config_store.py) ไล่คีย์ทั้ง 19 · [`02_config_reset_reload.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/02_config_reset_reload.py) สองตัวที่สลับกันง่าย · [`03_slots_and_the_dead_half.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/03_slots_and_the_dead_half.py) จับเวลาครึ่งที่ต้องมีชิป · [`04_disconnect_and_republish.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/04_disconnect_and_republish.py) ปิดแล้วเปิดใหม่

---

## วิธีรันบนบอร์ด

<svg viewBox="0 0 940 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="16" width="290" height="162" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="159" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="#1565c0">1 · ก่อนแตะโค้ด</text>
  <text x="159" y="84" text-anchor="middle" font-size="18" fill="#0d47a1">จดค่าประจำตัวสี่ตัวจากแพลตฟอร์ม</text>
  <text x="159" y="114" text-anchor="middle" font-size="18" fill="#0d47a1">ลงบันทึกการเรียน</text>
  <text x="159" y="144" text-anchor="middle" font-size="18" fill="#0d47a1">ต่อ WiFi ให้ได้ก่อนเสมอ</text>
  <text x="159" y="170" text-anchor="middle" font-size="17" fill="#5472a3">นับตัวอักษร device_id ให้ไม่เกิน 31</text>
  <rect x="324" y="16" width="290" height="162" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="469" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="#2e7d32">2 · แก้ห้าบรรทัดบนหัวไฟล์</text>
  <text x="469" y="84" text-anchor="middle" font-size="18" fill="#1b5e20">TEAM_NAME · DEVICE_ID</text>
  <text x="469" y="114" text-anchor="middle" font-size="18" fill="#1b5e20">API_KEY · MQTT_PASS · BROKER</text>
  <text x="469" y="144" text-anchor="middle" font-size="18" fill="#1b5e20">ที่เหลือเหมือนกันทุกบอร์ด</text>
  <text x="469" y="170" text-anchor="middle" font-size="17" fill="#4a7c4e">เติมช่องว่างทีละจุด แล้วรันทุกครั้ง</text>
  <rect x="634" y="16" width="292" height="162" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="780" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="#ef6c00">3 · รันแล้วดูสองจอ</text>
  <text x="780" y="84" text-anchor="middle" font-size="18" fill="#e65100">จอบอร์ด: ตัวนับกับ tls_mode</text>
  <text x="780" y="114" text-anchor="middle" font-size="18" fill="#e65100">จอคอม: dashboard ของแพลตฟอร์ม</text>
  <text x="780" y="144" text-anchor="middle" font-size="18" fill="#e65100">ขยับบอร์ดแล้วกราฟต้องขยับตาม</text>
  <circle cx="906" cy="168" r="9" fill="#ef6c00"><animate attributeName="r" values="6;12;6" dur="1.5s" repeatCount="indefinite"/></circle>
</svg>

1. เปิดหน้า **BENTO Playground** บนบอร์ดค้างไว้ แล้วต่อ WiFi ให้เรียบร้อยก่อน (`wifi.connect()` ของบทเรียน 4.1–4.3 บล็อกได้นานถึงราว 85 วินาทีถ้ารหัสผิด)
2. เปิด [`s11_secure_telemetry.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l09-secure-telemetry-lab/practice/s11_secure_telemetry.py) แก้ห้าบรรทัดบนหัวไฟล์ให้เป็นค่าของอุปกรณ์คุณ
3. เติมช่องว่างท่าที่ 1 ให้ครบ กด **Program to Device** แล้วดูว่า `print(tesaiot.config())` ขึ้นค่าครบและสะกดถูก **ก่อน** ไปท่าที่ 2
4. เติมท่าที่ 2 แล้วรัน — จับเวลาว่ากี่วินาที `is_connected()` จึงเป็น True แล้วจดลงบันทึกการเรียน
5. เติมท่าที่ 3 และ 4 แล้วเปิด dashboard ของแพลตฟอร์ม เลือกอุปกรณ์ของคุณ ดูกราฟขยับพร้อมกับตัวนับบนจอบอร์ด
6. ถ่ายภาพทั้งสองจอเก็บไว้เป็นหลักฐาน แล้วค่อยไปทำตารางเทียบ 1883 กับ 8884 ในบันทึกการเรียน

<style scoped>section table{font-size:.66em}</style>

### ตัวอย่างของบทเรียน 4.7–4.9 — สามไฟล์แรกคือชุดที่ย้ายลูปส่งข้อมูลขึ้นช่องที่เข้ารหัส

**ต้องทำในบทเรียน** · เปิดตามลำดับนี้ ทั้งชุดราว 29 นาที

| ลำดับ · เรื่อง · เวลา | ไฟล์ | ลงมือทำอะไร แล้วจะเข้าใจอะไร |
|---|---|---|
| **1 · อ่านค่าที่บอร์ดเก็บไว้ก่อนต่ออะไร** · 6 นาที | [`01_config_store.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/01_config_store.py) | กรอกกล่องค่าประจำตัวในบันทึกการเรียน จากค่าที่บอร์ดตอบจริง ไม่ใช่จากค่าที่จดมา · จะเข้าใจว่าต้องอ่านค่าที่บอร์ดเก็บไว้ให้ครบก่อน แล้วค่อยสั่งต่ออะไร |
| **2 · รอให้ต่อเสร็จเป็น** · 8 นาที | [`05_wait_for_connected.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/05_wait_for_connected.py) | เขียนลูปรอด้วย `is_connected()` และจับเวลาจริงลงบันทึกการเรียน · จะเข้าใจว่า `connect()` คืนค่าก่อนต่อเสร็จ จึงต้องรอเป็น ไม่ใช่เชื่อว่าคืนค่าแล้วคือพร้อม |
| **3 · ลูปส่ง telemetry บนช่องที่เข้ารหัส** · 15 นาที | [`06_secure_publish_loop.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l08-tesaiot-module/examples/06_secure_publish_loop.py) | ประกอบ MVP ของชุดบทเรียนนี้ — ตัวนับเดินขึ้นบนจอ พร้อมกราฟที่ขยับบน dashboard · จะเห็นว่าลูปส่ง telemetry ตัวเดิมย้ายขึ้นช่องที่เข้ารหัสได้ โดยรูปร่างของลูปไม่เปลี่ยน |

ทั้งสามไฟล์ **ยังรันไม่ได้จนกว่าบอร์ดจะมี `device_id` ของตัวเอง** (จากบัญชี TESAIoT Platform ของคุณ) นี่ไม่ใช่ข้อบกพร่องของไฟล์ แต่เป็นงานเตรียมการที่ต้องเสร็จก่อนบทเรียน ถ้ายังไม่ได้ค่าประจำตัว ให้อ่านโครงไปก่อนแล้วรันเมื่อได้ค่ามา

**ติดตรงไหน เปิดอันนี้**

| อาการที่เจอ | ไฟล์ที่ตอบอาการนั้น |
|---|---|
| ต่อไม่ติด และแยกไม่ออกว่าติดที่ WiFi หรือที่แพลตฟอร์ม | [`04_ping_two_targets.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l03-network-status-lab/examples/04_ping_two_targets.py) — พิสูจน์ให้จบก่อนว่าออกอินเทอร์เน็ตได้จริง แล้วค่อยโทษ TLS |
| ตอบไม่ได้ว่าวันนี้ต่างจากบทเรียน 4.4–4.6 ตรงไหน | [`03_connect_and_publish.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l05-mqtt-platform/examples/03_connect_and_publish.py) — เปิดคู่กับไฟล์ที่ 3 ข้างบน แล้วเทียบทีละบรรทัดว่าอะไรเปลี่ยน |

**อ่านเสริมนอกเวลา** — เรื่องนี้อยู่นอกเกณฑ์ผ่านของบทเรียน 4.7–4.9 แต่เป็นนิสัยที่ใช้ได้ทั้งบทเรียน 4.4–4.6 และชุดบทเรียนนี้: [`06_sent_is_not_delivered.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l05-mqtt-platform/examples/06_sent_is_not_delivered.py) สอนให้นับใบที่ **ถึงปลายทาง** ไม่ใช่นับใบที่เราสั่งส่ง · ส่วนตัวอย่างที่เทียบ 1883 กับ 8884 ให้เห็นด้วยตาว่า TLS ปกป้องอะไร **ยังไม่มีในคลัง** วันนี้จึงใช้ตารางเทียบในบันทึกการเรียน กับผลดักฟังในสไลด์แทน

ก่อนหน้านี้ชุดบทเรียนนี้มีตัวอย่างอีกสามไฟล์ที่บันทึกพฤติกรรมแปลกของ `tesaiot.config()` ไว้ (ตั้งค่าแล้วอ่านกลับได้อีกคำ · พิมพ์ผิดแล้วยังคืน `True` · คีย์ `port` ที่ไม่มีใครอ่าน) ทั้งสามถูกถอดออก เพราะเป็นรายงานบั๊กของเฟิร์มแวร์ ไม่ใช่นิสัยที่เอาไปใช้กับงานตัวเองได้ ความจริงเรื่องพอร์ตยังอยู่ในสไลด์ "พอร์ตมาจาก `tls_mode` ไม่ใช่คีย์ `port`" และในตารางกับดัก

> อย่าเติมครบทั้งห้าจุดแล้วค่อยรัน — บนเส้นทางที่มี TLS อยู่ตรงกลาง จุดที่พังได้มีมากกว่าชุดบทเรียนก่อนหน้า และไม่มีจุดไหนส่งเสียงเลย
