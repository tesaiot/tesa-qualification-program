---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก Edge AI Developer (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY 4.0"
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

# บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT

## Apps III: sensor fusion + IoT · เอา verdict ของโมเดล มารวมกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์

**โมดูล 6 — แอป Edge AI**

> ต่อจากบทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ

---

# IoT — ทำไมต้องสตรีมขึ้นคลาวด์

Edge AI ตัดสินใจบนบอร์ดได้เอง (นั่นคือจุดเด่น) แต่บ่อยครั้งเราอยาก **รวมเหตุการณ์จากหลายบอร์ด** ไว้ที่เดียว เพื่อดูภาพรวม/แจ้งเตือน/เก็บสถิติ

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arIoT" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="30" width="160" height="50" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="100" y="52" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">บอร์ด A</text>
  <text x="100" y="70" font-size="10" fill="#888" text-anchor="middle">fused event</text>
  <rect x="20" y="100" width="160" height="50" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="100" y="122" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">บอร์ด B</text>
  <text x="100" y="140" font-size="10" fill="#888" text-anchor="middle">fused event</text>
  <rect x="360" y="62" width="180" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="450" y="88" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">MQTT broker</text>
  <text x="450" y="108" font-size="10" fill="#888" text-anchor="middle">ตัวรวมข้อความ (คลาวด์)</text>
  <rect x="700" y="30" width="180" height="50" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="790" y="52" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">Dashboard</text>
  <text x="790" y="70" font-size="10" fill="#888" text-anchor="middle">Grafana/Node-RED</text>
  <rect x="700" y="100" width="180" height="50" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="790" y="122" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">แจ้งเตือนมือถือ</text>
  <text x="790" y="140" font-size="10" fill="#888" text-anchor="middle">subscribe topic</text>
  <line x1="180" y1="55" x2="358" y2="82" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arIoT)"/>
  <line x1="180" y1="125" x2="358" y2="100" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arIoT)"/>
  <line x1="540" y1="82" x2="698" y2="55" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arIoT)"/>
  <line x1="540" y1="100" x2="698" y2="125" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arIoT)"/>
</svg>
</div>

- **สำคัญ**: เราสตรีมแค่ **เหตุการณ์ที่สรุปแล้ว** (fused event) ไม่ใช่ข้อมูลดิบทั้งสตรีม — ประหยัด bandwidth + รักษาความเป็นส่วนตัว
- นี่คือความงามของ Edge AI + IoT: **คิดที่ขอบ ส่งเฉพาะข้อสรุป** ไม่ใช่ยกทุกอย่างขึ้นคลาวด์แบบ Cloud AI

> ย้อนกลับไปบทเรียน 1.1–1.3: Edge AI มีอยู่เพื่อไม่ต้องอัปโหลดข้อมูลดิบ — IoT ที่ดีจึงส่งแค่ "verdict ที่ผ่านการยืนยัน" ไม่ใช่เสียง/ภาพดิบ นี่คือหลักที่เราจะยึด

---

# WiFi — ต่อเน็ตด้วยโมดูล wifi

โมดูล `wifi` คือหน้าต่างต่ออินเทอร์เน็ตของบอร์ด (WiFi รันบน CM33_NS) ชุดบทเรียนนี้ใช้แค่ 3 คำสั่ง:

| คำสั่ง | ทำอะไร |
|---|---|
| `wifi.connect(ssid, password)` | ต่อเข้า AP (บล็อกจนต่อได้หรือ timeout) |
| `wifi.is_connected()` | คืน `True/False` — ต่อสำเร็จหรือยัง |
| `wifi.ip()` | คืน IP ที่ได้มาเป็นข้อความ (เช็กว่าได้ที่อยู่จริง) |

```python
import wifi
if not wifi.is_connected():
    wifi.connect("<ชื่อ WiFi ของคุณ>", "<รหัส WiFi ของคุณ>")   # ใส่ค่าจริงของคุณตอนรัน (อย่า commit รหัสจริง)
if wifi.is_connected():
    print("WiFi ok:", wifi.ip())
```

- ตอนรันจริงให้ใส่ SSID/รหัสของ WiFi ที่คุณใช้ (โมดูลเดียวกัน)
- `wifi.connect()` ใช้เวลาสักครู่ (สแกน + จับมือ) — เรียกครั้งเดียวก่อนเข้าลูป ไม่ใช่ทุกรอบ

> โมดูลนี้มีคำสั่งอื่นอีก (`wifi.scan()`, `wifi.status()`, `wifi.ping()`) แต่ชุดบทเรียนนี้เอาแค่ต่อให้ติดพอ — ลองโชว์ `wifi.status()["rssi"]` เป็นโจทย์ต่อยอด

---

# MQTT — โมเดล publish / subscribe

**MQTT** เป็นโปรโตคอลส่งข้อความแบบ **publish/subscribe** ผ่านตัวกลางชื่อ **broker** เบามาก เหมาะกับอุปกรณ์ IoT

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arMq" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="50" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="74" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">บอร์ด (publisher)</text>
  <text x="115" y="94" font-size="10" fill="#888" text-anchor="middle">publish(topic, payload)</text>
  <rect x="345" y="46" width="200" height="64" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="445" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">broker</text>
  <text x="445" y="92" font-size="10" fill="#888" text-anchor="middle">test.mosquitto.org:1883</text>
  <rect x="680" y="50" width="190" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="775" y="74" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ผู้รับ (subscriber)</text>
  <text x="775" y="94" font-size="10" fill="#888" text-anchor="middle">subscribe(topic)</text>
  <line x1="210" y1="78" x2="343" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arMq)"/>
  <line x1="545" y1="78" x2="678" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arMq)"/>
  <text x="277" y="66" font-size="11" fill="#607d8b" text-anchor="middle">ส่งไป topic</text>
  <text x="612" y="66" font-size="11" fill="#607d8b" text-anchor="middle">แจกให้คนที่ sub</text>
</svg>
</div>

- **topic** = "ช่อง" ตั้งชื่อเป็นลำดับชั้น เช่น `tesaiot/edge-ai/s17` — ใครสนใจก็ subscribe ช่องนี้
- **payload** = เนื้อข้อความ (เราส่งเป็น JSON) — ใครก็อ่านต่อได้ ไม่ต้องรู้จักผู้ส่ง
- **broker** = ตัวกลาง ชุดบทเรียนนี้ใช้ broker สาธารณะ `test.mosquitto.org` (ฟรี ไม่ต้องล็อกอิน)

> publish/subscribe แยกผู้ส่งกับผู้รับออกจากกัน (decoupled) — บอร์ดไม่ต้องรู้ว่าใครฟังอยู่ แค่โยนข้อความเข้า topic ที่ตกลงกันไว้ นี่คือหัวใจว่าทำไม IoT ชอบ MQTT

---

# โมดูล mqtt — คำสั่งที่ใช้ชุดบทเรียนนี้

`mqtt` ห่อ MQTT ให้เหลือไม่กี่คำสั่ง ชุดบทเรียนนี้ใช้ 4 ตัวหลัก:

| คำสั่ง | ทำอะไร |
|---|---|
| `mqtt.connect(broker, port, client_id=...)` | ต่อเข้า broker (ต้องต่อ WiFi ก่อน) |
| `mqtt.publish(topic, payload)` | ส่งข้อความเข้า topic (QoS 0 โดยปริยาย) |
| `mqtt.is_connected()` | เช็กว่ายังต่อ broker อยู่ไหม |
| `mqtt.disconnect()` | ตัดการเชื่อมต่อให้เรียบร้อยตอนจบ |

```python
import mqtt
mqtt.connect("test.mosquitto.org", 1883, client_id="bento-s17")
mqtt.publish("tesaiot/edge-ai/s17", '{"event":"shaking","conf":0.92}')
```

- `client_id` ควรตั้งให้ไม่ซ้ำใคร (broker สาธารณะมีหลายคนใช้) — เราใส่คำนำหน้า `bento-`
- `mqtt.publish()` โยน `OSError` ได้ถ้าการเชื่อมต่อหลุด — ห่อด้วย `try/except` เสมอ

> มีคำสั่งอื่นอีก (`subscribe`, `get_message`) สำหรับ "รับ" ข้อความ แต่ชุดบทเรียนนี้เราโฟกัส "ส่ง" (publish) — การรับเก็บไว้เป็น โจทย์ต่อยอด

---

# payload JSON — โครงของเหตุการณ์

เราส่งเหตุการณ์เป็น **JSON** เพราะทุกระบบปลายทาง (dashboard, Node-RED, มือถือ) อ่านได้ทันที ประกอบ payload จากข้อมูล fusion:

```python
payload = '{"event":"%s","conf":%.2f,"gyro":%.0f,"ts":%d}' % (
    TARGET_CLASS,        # เหตุการณ์อะไร (จากโมเดล)
    conf_val,            # โมเดลมั่นใจแค่ไหน
    gmag,                # เซนเซอร์ดิบยืนยันแรงเท่าไร
    time.ticks_ms(),     # ประทับเวลา (บอกลำดับเหตุการณ์)
)
```

- ใส่ทั้ง **verdict** (`event`, `conf`) และ **หลักฐานดิบ** (`gyro`) ลงไป — ปลายทางเห็นว่าตัดสินจากอะไร
- ประกอบ string เองด้วย `%` ก็พอสำหรับ payload สั้นๆ (MicroPython มี `json` ให้ใช้ด้วย ถ้าอยากเป๊ะ)
- payload สั้น = ส่งเร็ว ประหยัดพลังงาน — ส่งแค่ข้อสรุป ไม่ใช่สตรีมดิบ (หลักจากสไลด์ IoT)

> การใส่ทั้ง `conf` (จากโมเดล) และ `gyro` (จากเซนเซอร์ดิบ) ในข้อความเดียว = ปลายทางตรวจสอบการตัดสินใจ fusion ของเราย้อนหลังได้ นี่คือ observability ที่ดี

---

# รันได้ทั้งบอร์ดและ Emulator — degrade อย่างสง่างาม

บอร์ดจริงมี WiFi/MQTT ส่วน Emulator มี `wifi` แบบจำลองและ `mqtt` ที่ต่อ broker สาธารณะของจริงผ่าน WebSocket แต่ที่ไหนก็อาจเจอเน็ตไม่ติดหรือไม่มีโมดูลเน็ต — เราต้องเขียนให้โค้ด **ชุดเดียว** รันได้ทุกที่ ไม่พังถ้าไม่มีเน็ต

```python
try:
    import wifi, mqtt
    HAVE_NET = True
except ImportError:
    HAVE_NET = False          # ไม่มีโมดูลเน็ต → โหมด offline

def publish_event(conf_val, gmag):
    payload = build_payload(conf_val, gmag)
    if HAVE_NET and mqtt.is_connected():
        mqtt.publish(TOPIC, payload)          # บอร์ด: ส่งขึ้นคลาวด์จริง
    else:
        lcd.console('<span class=info> [SIM] ' + payload + '</span>')  # เน็ตไม่ติด: โชว์แทน
```

- `try/except ImportError` = ถ้าไม่มีโมดูล `wifi`/`mqtt` ก็ตั้งธง offline แทนที่จะ crash ตอน import
- โหมด offline ยัง **แสดง fusion + edge-trigger ครบ** แค่พิมพ์ payload ลง console แทนส่งจริง
- ทำให้ MVP สาธิตได้ทุกที่: กลไก fusion กับการส่งเห็นได้ทั้งบน Emulator และบอร์ด ถ้าเน็ตไม่ติดก็ยังเห็นกลไกผ่าน `[SIM]`

> นี่คือนิสัย multi-surface ของทั้งคอร์ส (บทเรียน 1.1–1.3): โค้ดบรรทัดเดียวกันต้องรันได้ทั้ง Emulator และบอร์ด — เราแค่ห่อส่วนที่ต้องมีฮาร์ดแวร์จริงด้วยการเช็กก่อน

---

# ลองเลยบนจอ Emulator — ไม่ต้องมีบอร์ด

เปิด [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py) บน BENTO Edge AI Emulator ในเบราว์เซอร์ได้ทันที WiFi เป็นแบบจำลองที่ต่อติด และ MQTT ส่งถึง broker สาธารณะจริงผ่าน WebSocket (ต่อไม่ได้จะใช้ broker จำลอง) ข้อควรรู้: แผง HW ของ Emulator ขยับเฉพาะ accel (ลากเอียงและปุ่ม Shake) ส่วน gyro ค้างใกล้ศูนย์ ประตู gyro จึงไม่เปิด ถ้าจะซ้อมบน Emulator ให้เปลี่ยนประตูเป็น accel ชั่วคราว เช่น `gmag = abs(ax) + abs(ay) + abs(az - 9.81)` กับ `MOTION_FLOOR = 5.0`

บนจอของแอปนี้จะเห็น verdict, ค่าประตูดิบ และบรรทัด MQTT TX หรือ `[SIM]` ในหน้าเดียว

- ด้านบนคือ verdict ของโมเดล (label + conf) เหมือนบนบอร์ดจริง
- ค่า gyro ดิบที่เอามา gate ก็โชว์ให้เห็นว่ามันข้ามเกณฑ์ `MOTION_FLOOR` หรือยัง
- พอ fused ครบทั้งสองด่าน บรรทัด `MQTT TX` (หรือ `[SIM]` ถ้าเน็ตไม่ติด) จะพิมพ์ payload JSON ที่ถูก publish

> ซ้อมบน Emulator ให้เห็น fusion กับ MQTT TX ก่อน แล้วค่อยย้ายไปบอร์ดจริงที่ต่อ WiFi ของจริงและใช้ประตู gyro — โค้ดชุดเดียวกัน เปลี่ยนแค่พื้นผิวที่รัน

---

# ไล่หนึ่งรอบเต็ม — sensor → model → fuse → cloud

รวมทุกจังหวะเป็นภาพเดียว: จากเซนเซอร์บนบอร์ด จนถึงข้อความที่โผล่บน dashboard — นี่คือวงจรที่แอปชุดบทเรียนนี้เดินทุก ~250 ms

<div style="text-align:center;margin:6px 0">
<svg width="920" height="190" viewBox="0 0 920 190" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arCyc17" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="8" y="60" width="132" height="64" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="74" y="86" font-size="12" font-weight="700" fill="#1565c0">เซนเซอร์</text>
    <text x="74" y="106" font-size="10" fill="#888">IMU</text>
    <rect x="164" y="60" width="132" height="64" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="230" y="84" font-size="12" font-weight="700" fill="#6a1b9a">โมเดล (M55)</text>
    <text x="230" y="104" font-size="10" fill="#888">verdict</text>
    <rect x="320" y="60" width="132" height="64" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="386" y="84" font-size="12" font-weight="700" fill="#2e7d32">fuse</text>
    <text x="386" y="104" font-size="10" fill="#888">+ gyro ดิบ</text>
    <rect x="476" y="60" width="132" height="64" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="542" y="84" font-size="12" font-weight="700" fill="#455a64">edge-trigger</text>
    <text x="542" y="104" font-size="10" fill="#888">fired?</text>
    <rect x="632" y="60" width="132" height="64" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="698" y="84" font-size="12" font-weight="700" fill="#e65100">publish</text>
    <text x="698" y="104" font-size="10" fill="#888">mqtt / sim</text>
    <rect x="788" y="60" width="124" height="64" rx="10" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="850" y="84" font-size="12" font-weight="700" fill="#00838f">คลาวด์</text>
    <text x="850" y="104" font-size="10" fill="#888">dashboard</text>
  </g>
  <line x1="140" y1="92" x2="162" y2="92" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arCyc17)"/>
  <line x1="296" y1="92" x2="318" y2="92" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arCyc17)"/>
  <line x1="452" y1="92" x2="474" y2="92" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arCyc17)"/>
  <line x1="608" y1="92" x2="630" y2="92" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arCyc17)"/>
  <line x1="764" y1="92" x2="786" y2="92" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arCyc17)"/>
  <text x="300" y="42" font-size="10" fill="#999" text-anchor="middle">CM55 + NPU</text>
  <text x="620" y="42" font-size="10" fill="#999" text-anchor="middle">โค้ด Python บน CM33</text>
  <path d="M850,124 C850,162 74,162 74,126" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arCyc17)"/>
  <text x="460" y="158" font-size="11" fill="#9e9e9e" text-anchor="middle">วนรอบใหม่ทุก ~250 ms</text>
</svg>
</div>

> ครึ่งซ้าย (เซนเซอร์ → verdict) เกิดบน CM55 เราไม่แตะ · ครึ่งขวา (fuse → trigger → publish) คือโค้ด Python ของเราบน CM33 — ชุดบทเรียนนี้เราคุมครึ่งขวาทั้งหมด แล้วต่อสายออกไปถึงคลาวด์

---

# โครงของไฟล์ s17_fusion_iot.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"ต่อเน็ต → หาโมเดล + สั่งรัน → วนอ่าน verdict + gyro ดิบ → พอสองสัญญาณเห็นตรงกัน ก็ publish เหตุการณ์ขึ้น MQTT → หยุดตอนออก"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="210" viewBox="0 0 920 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS17" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="170" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="99" y="47" font-weight="700" fill="#455a64">ต่อ WiFi/MQTT</text>
    <text x="99" y="66" font-size="11" fill="#999">(ให้ไว้แล้ว)</text>
    <rect x="224" y="24" width="150" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="299" y="47" font-weight="700" fill="#1565c0">select</text>
    <text x="299" y="66" font-size="11" fill="#999">ช่อง 1</text>
    <rect x="414" y="24" width="180" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="504" y="47" font-weight="700" fill="#e65100">result + gyro</text>
    <text x="504" y="66" font-size="11" fill="#999">ช่อง 2 + 3</text>
    <polygon points="664,51 714,23 764,51 714,79" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="714" y="47" font-weight="700" fill="#2e7d32" font-size="12">fused?</text>
    <rect x="810" y="24" width="96" height="54" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="858" y="55" font-size="11" fill="#455a64">ออก→stop</text>
    <rect x="414" y="140" width="200" height="58" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="514" y="164" font-weight="700" fill="#6a1b9a">publish_event</text>
    <text x="514" y="182" font-size="11" fill="#999">ช่อง 4 + 5 · ยิงครั้งเดียว</text>
  </g>
  <line x1="184" y1="51" x2="222" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS17)"/>
  <line x1="374" y1="51" x2="412" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS17)"/>
  <line x1="594" y1="51" x2="662" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS17)"/>
  <line x1="764" y1="51" x2="808" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS17)"/>
  <text x="788" y="43" font-size="11" fill="#607d8b">no</text>
  <path d="M714,79 C714,120 514,110 514,138" fill="none" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS17)"/>
  <text x="660" y="112" font-size="12" fill="#6a1b9a">yes → publish</text>
  <text x="470" y="206" font-size="11" fill="#888" text-anchor="middle">ช่อง 4 = fused decision · ช่อง 5 = mqtt.publish ภายใน publish_event</text>
</svg>
</div>

> ตัวเลขช่อง (1–5) ชี้จุดที่คุณต้องเติมในไฟล์ฝึก — ช่อง 1–2 เป็นของเดิม (ทวน) ช่อง 3–5 คือ fusion + IoT ของใหม่ของชุดบทเรียนนี้

---

# ไล่โค้ด (1) — select + ต่อเน็ต

**ช่องเติมที่ 1**: หาโมเดลจากชื่อ (ให้ไว้แล้ว) แล้วสั่งให้ CM55 เริ่มรัน — การต่อ WiFi/MQTT ทำให้แล้วด้านบน:

```python
model = find_model(MODEL_KEYWORD)   # ให้ไว้แล้ว: คืน dict ทั้งก้อน
labels = model['labels']

try:
    # เติม: สั่งให้ CM55 รันโมเดลนี้ ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มอนุมาน %s</span>' % model['name'])
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)
```

- แทน `pass` ด้วย `edge_ai.select(model['index'])` — เอา index จาก dict ไปสั่ง (เหมือนบทเรียน 1.6–1.7)
- ต้องอยู่ใน `try` เพราะ `select()` โยน `OSError` ได้ (ข้ามคอร์อาจพลาด)
- ถ้าลืมเติม: จอค้างที่ `---` เพราะไม่มีโมเดลรัน `result()` คืน `None` ตลอด

> `MODEL_KEYWORD` + `TARGET_CLASS` อยู่บนหัวไฟล์ — remix ได้ทันที เปลี่ยนเป็น Cough/Siren แอปก็เปลี่ยนเหตุการณ์ที่สตรีมโดยไม่แตะ logic

---

# ไล่โค้ด (2) — อ่าน verdict + gyro ดิบ

**ช่องเติมที่ 2 และ 3**: จังหวะ 2 (verdict เดิม) + จังหวะ fuse ครึ่งแรก (อ่านเซนเซอร์ดิบมาประกบ):

```python
# เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
r = None
pass
if r and r['seq'] != last_seq:
    last_seq = r['seq']
    verdict.text(r['label'] or '-')
    conf.text("conf: %.0f %%" % (r['conf'] * 100))

    # เติม: อ่านเซนเซอร์ดิบมายืนยัน -> ax,ay,az,gx,gy,gz = sensors.bmi270.motion()
    gx = gy = gz = 0.0
    pass
    gmag = abs(gx) + abs(gy) + abs(gz)
    raw_lab.text("gyro: %.0f" % gmag)
```

- ช่อง 2: แทน `pass` ด้วย `r = edge_ai.result()` (เหมือนบทเรียน 1.1–1.3 / 1.6–1.7)
- ช่อง 3: แทน `pass` ด้วย `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` — อ่านค่าดิบมาทำ gate
- เช็ก `seq` ก่อนเสมอ วาดจอ + อ่านเซนเซอร์เฉพาะตอนมี verdict ใหม่

> ช่อง 2 คือ "ของเดิม" ที่คุณทำเป็นแล้ว ช่อง 3 คือของใหม่ — เริ่มมีเซนเซอร์ **สองเส้นทาง** ในลูปเดียว: ผ่านโมเดล กับ อ่านดิบ

---

# ไล่โค้ด (3) — เงื่อนไข fused

**ช่องเติมที่ 4**: จังหวะ fuse ครึ่งหลัง — เอา verdict มา AND กับ gate ของเซนเซอร์ดิบ:

```python
    model_hit = (r['label'] == TARGET_CLASS
                 and r['conf'] >= edge_ai.CONF_FLOOR)   # โมเดลผ่าน
    raw_ok = gmag > MOTION_FLOOR                         # เซนเซอร์ดิบผ่าน

    # เติม: รวมสองสัญญาณด้วย AND -> fused = model_hit and raw_ok
    fused = False
    pass

    if fused and not fired:
        publish_event(r['conf'], gmag)     # สองสัญญาณเห็นตรงกัน → ส่ง
        fired = True
    elif not fused:
        fired = False
        state.text("รอเหตุการณ์ ...")
        state.color(DIM)
```

- แทน `pass` ด้วย `fused = model_hit and raw_ok` — หัวใจของ fusion อยู่บรรทัดนี้
- `and not fired` = edge-trigger ยิงครั้งเดียวต่อการเจอ (ไม่ spam broker)
- ถ้าลืมเติม: `fused` เป็น `False` ตลอด → ไม่มีอะไรถูกส่งเลย แม้โมเดล+เซนเซอร์จะเห็นตรงกัน

> บรรทัดนี้คือความต่างจากบทเรียน 6.3–6.4 — action ไม่ได้ยิงจาก verdict อย่างเดียว แต่ยิงจาก **verdict ที่เซนเซอร์ดิบรับรอง**

---

# ไล่โค้ด (4) — publish ขึ้น MQTT

**ช่องเติมที่ 5**: ภายใน `publish_event()` — ที่ที่ fused decision กลายเป็นข้อความบนคลาวด์:

```python
def publish_event(conf_val, gmag):
    payload = '{"event":"%s","conf":%.2f,"gyro":%.0f,"ts":%d}' % (
        TARGET_CLASS, conf_val, gmag, time.ticks_ms())
    state.text("! ส่งเหตุการณ์ !"); state.color(GREEN)
    if HAVE_NET and mqtt.is_connected():
        try:
            # เติม: ส่ง payload ขึ้น broker -> mqtt.publish(TOPIC, payload)
            pass
            lcd.console('<span class=ok> MQTT TX: ' + payload + '</span>')
        except OSError as e:
            lcd.console('<span class=error> ส่งไม่สำเร็จ: %s</span>' % e)
    else:
        lcd.console('<span class=info> [SIM] ' + payload + '</span>')   # offline
```

- แทน `pass` ด้วย `mqtt.publish(TOPIC, payload)` — ส่งเหตุการณ์ที่ผ่าน fusion ขึ้น topic
- ห่อด้วย `try/except OSError` เพราะการเชื่อมต่ออาจหลุด — แอปต้องไม่ล้มเพราะเน็ตสะดุด
- โหมด offline (เน็ตไม่ติด) ไปทาง `else` โชว์ `[SIM]` — กลไกครบ แค่ไม่ส่งจริง

> เติมครบ 5 ช่องเมื่อไร คุณได้แอป Edge AI ที่ตัดสินใจแบบ fused แล้วสตรีมขึ้นคลาวด์ — นี่คือ MVP ของบทเรียน 6.5–6.6 ของชุดบทเรียนนี้

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py) ในไฟล์มี `pass` วางไว้ **5 จุด** ตรงที่ต้องเติมคำสั่งจริง:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | หลัง find_model | `edge_ai.select(model['index'])` | จอค้าง `---` ไม่มี verdict |
| 2 | ในลูป | `r = edge_ai.result()` | จอไม่ขึ้นคลาสเลย |
| 3 | มี verdict ใหม่ | `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` | gyro ค้าง 0 ประตูไม่มีวันเปิด |
| 4 | รวมสัญญาณ | `fused = model_hit and raw_ok` | ไม่มีเหตุการณ์ถูกส่งเลย |
| 5 | ใน publish_event | `mqtt.publish(TOPIC, payload)` | fused แล้วแต่ไม่ถึง broker |

ขั้นตอน:

1. ตั้ง `MODEL_KEYWORD` / `TARGET_CLASS` / `MOTION_FLOOR` ที่อยากลอง (เริ่มจาก Motion/shaking/40)
2. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
3. บนบอร์ด: ใส่ SSID/รหัสจริงในหัวไฟล์ · บน Emulator: WiFi จำลองต่อติดเอง และเปลี่ยนประตูเป็น accel ชั่วคราวเพราะ gyro บน Emulator ค้างใกล้ศูนย์
4. กด **Run** / **Program to Device** แล้วเขย่าบอร์ดจริงจนเหตุการณ์ถูกส่ง

> ช่อง 1–2 คือของเดิม (ทวน) · ช่อง 3–5 คือ fusion + IoT ของใหม่ — เติมครบเมื่อไร แอปของคุณ "ตัดสินใจแบบเชื่อถือได้" แล้ว "พูดคุยกับคลาวด์" ได้

---

# แหล่งเรียนรู้เพิ่มเติม

อยากต่อยอดเรื่อง sensor fusion และ IoT/MQTT ลองดูของดีที่คนทำจริงเขาอธิบายไว้:

**วิดีโอ (ช่องการศึกษาที่น่าเชื่อถือ)**

- พื้นฐานโมเดลที่ให้ verdict (neural nets) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Sensor fusion & Kalman filter เบื้องต้น — ช่อง Computerphile: https://www.youtube.com/@Computerphile
- IoT/MQTT ด้วย Python — ช่อง Sentdex: https://www.youtube.com/@sentdex

**อ่าน/ภาพอ้างอิง**

- บทความ Sensor fusion: https://en.wikipedia.org/wiki/Sensor_fusion (ที่มา: Wikipedia, CC BY-SA 4.0)
- บทความ MQTT (โปรโตคอล pub/sub): https://en.wikipedia.org/wiki/MQTT (ที่มา: Wikipedia, CC BY-SA 4.0)
- เอกสารทางการโปรโตคอล MQTT: https://mqtt.org/ (ที่มา: mqtt.org / OASIS)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — เราไม่ได้ฝังคลิปไว้ในสไลด์ ให้กดลิงก์ไปดูที่ต้นทางเอง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · เหตุการณ์ Edge AI ที่ผ่านการยืนยันด้วยเซนเซอร์ดิบ ถูกสตรีมขึ้น MQTT broker (เห็นบน dashboard / mosquitto_sub)
</div>
</div>

**MVP ของบทเรียน 6.5–6.6 (เกณฑ์ผ่านของชุดบทเรียน):** คุณทำให้ **การตัดสินใจแบบ fused** (verdict `AND` gyro ดิบ) ถูก **publish ขึ้น MQTT** ได้จริง — บนบอร์ดหรือ Emulator (ถ้าเน็ตไม่ติดจะเห็น `[SIM]` บน console แทน)

- fusion ต้องเห็นผล: เขย่าเบาๆ (โมเดลไม่มั่นใจ/gyro ไม่ถึงเกณฑ์) → ไม่ส่ง · เขย่าจริง → ส่ง
- อธิบายได้ว่าทำไม fusion ใช้ `and` และทำไมต้อง edge-trigger ก่อน publish

> "ส่งได้" ไม่ใช่แค่ "เห็น TX บนจอ" — คุณต้องบอกได้ว่า fusion กรอง false positive ยังไง และเหตุการณ์นี้เดินทางจากบอร์ดถึง broker ทางไหน

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py) มีโครงครบทั้งไฟล์แล้ว (รวม WiFi/MQTT + degrade) เหลือแค่ 5 บรรทัดให้เติม
- **เฉลย** — [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/solution/s17_fusion_iot.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s17_fusion_iot_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/examples/s17_fusion_iot_full.py) เพิ่ม gate เป็นเรดาร์ (multi-modal) + นับจำนวนเหตุการณ์ + reconnect broker + โชว์ RSSI

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การรวม verdict กับเซนเซอร์ดิบแล้วสตรีมขึ้นคลาวด์ ซ่อนแนวคิดที่ปิดกล่อง โมดูล 6 (Apps) พอดี:

**ฝั่ง Edge AI / ระบบ**
- **Sensor fusion** — verdict (what) `AND` raw feature (how strong) → ตัดสินใจที่ทน false positive
- **Verdict → verified action** — ต่อจากบทเรียน 6.3–6.4: action ยิงเมื่อ **สองสัญญาณเห็นตรงกัน**
- **Edge-to-cloud** — ส่งเฉพาะ **เหตุการณ์ที่สรุปแล้ว** ไม่ใช่สตรีมดิบ (รักษา privacy + bandwidth)
- **Observability** — payload พก `conf` + `gyro` ให้ปลายทางตรวจสอบการตัดสินใจย้อนหลัง

**ฝั่ง MicroPython / โครงโปรแกรม**
- **`wifi` + `mqtt`** — ต่อเน็ต + publish/subscribe แบบ decoupled
- **degrade อย่างสง่างาม** — `try/except ImportError` + เช็ก `is_connected()` → โค้ดชุดเดียวรันทุกพื้นผิว
- **เก็บกวาดตอนจบ** — `finally: stop()` + `mqtt.disconnect()` คืนทุกอย่างสู่สถานะที่รู้แน่

> ทั้งหมดยังยืนบนคำสั่งเดิมของ `edge_ai` + `sensors` — ชุดบทเรียนนี้แค่ต่อ "IoT layer" บนแอปที่คุณทำเป็นแล้ว

---

# ใช้จริงที่ไหน — fusion + IoT ในโลกจริง

pattern "รวมสัญญาณให้เชื่อถือได้ แล้วสตรีมเหตุการณ์ขึ้นคลาวด์" คือแก่นของระบบ Edge AI + IoT จริงทุกตัว:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">โรงงาน — เฝ้าเครื่องจักร</text>
  <text x="28" y="56" font-size="11" fill="#555">โมเดลเสียง "ผิดปกติ" + IMU สั่นเกินเกณฑ์ → fused</text>
  <text x="28" y="76" font-size="11" fill="#555">publish เหตุการณ์ → dashboard ทั้งไลน์การผลิต</text>
  <text x="28" y="96" font-size="11" fill="#888">= verdict + raw gate + MQTT ของเราวันนี้</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">บ้าน — กันขโมยไม่ปลุกพลาด</text>
  <text x="464" y="56" font-size="11" fill="#555">โมเดล motion + เรดาร์ยืนยันมีคน → ค่อยแจ้ง</text>
  <text x="464" y="76" font-size="11" fill="#555">ส่งเฉพาะเหตุการณ์ ไม่สตรีมภาพ → privacy</text>
  <text x="464" y="96" font-size="11" fill="#888">= corroboration gate ของเราวันนี้</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">เกษตร — ฝูงสัตว์/ไร่</text>
  <text x="28" y="164" font-size="11" fill="#555">โมเดลท่าทาง + อุณหภูมิดิบ → fused event</text>
  <text x="28" y="184" font-size="11" fill="#555">บอร์ดหลายร้อยตัว → broker เดียว รวมภาพ</text>
  <text x="28" y="202" font-size="11" fill="#888">= many publishers → 1 broker ของเราวันนี้</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — fused event → cloud</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกระบบ = รวมสัญญาณ + ยืนยัน + ส่งข้อสรุป</text>
  <text x="464" y="184" font-size="11" fill="#555">ต่างกันแค่ "โมเดล + gate + topic" ปลายทาง</text>
  <text x="464" y="202" font-size="11" fill="#888">คือ Capstone (8.1–8.2) ของเรา</text>
</svg>
</div>

> สังเกตว่าทุกระบบใช้ pattern เดียวกับแอปชุดบทเรียนนี้เป๊ะ — ต่างกันแค่โมเดล, ประตูยืนยัน, และ topic ปลายทาง เราแค่กำลังเริ่มจากปลายทางเพื่อย้อนไปสร้างระบบเต็มเองได้

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py) ให้ครบทั้ง 5 ช่อง รันได้จริงบน Emulator หรือบอร์ด
2. **หา false positive ที่ fusion กรองได้**: หาท่าที่ทำให้โมเดลตอบ `shaking` แต่ gyro ดิบไม่ถึง `MOTION_FLOOR` (หรือกลับกัน) แล้วยืนยันว่า **ไม่มีเหตุการณ์ถูกส่ง**
3. **remix**: เปลี่ยน `MODEL_KEYWORD`/`TARGET_CLASS`/`MOTION_FLOOR` เป็นชุดอื่น แล้วอธิบายว่า topic/payload เปลี่ยนยังไง

ใบ้ข้อ 2 — fusion เป็น `and` ดังนั้นแค่ด่านเดียวไม่ผ่านก็พอ: โมเดลมั่นใจแต่ gyro เบา = ไม่ส่ง หรือ gyro แรงแต่โมเดลตอบผิดคลาส = ไม่ส่ง นี่คือหัวใจว่า fusion กัน false positive ยังไง

**วันนี้เราได้:** เข้าใจ sensor fusion (verdict + raw gate) · อ่านเซนเซอร์ดิบมายืนยัน verdict · ต่อ WiFi + publish MQTT · เขียนโค้ดชุดเดียวที่ degrade ได้ทั้งบอร์ดและ Emulator · ปิดกล่อง โมดูล 6 (Apps)

> ชุดบทเรียนถัดไป (บทเรียน 7.1–7.2) เราปิด โมดูล 6 (Apps) แล้วเปิด **โมดูล 7 (Researcher) — ใต้ฝากระโปรง**: มุดลงไปดูสแตก Edge AI จริงๆ (tri-core, `ai_engine`, IPC model-link, TFLite-Micro → NPU) ว่า verdict ที่เราใช้ทั้งคอร์สเกิดขึ้นได้ยังไงใต้พื้น เจอกันครับ
