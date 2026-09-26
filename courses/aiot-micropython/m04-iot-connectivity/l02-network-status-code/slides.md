---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.2 — จอสถานะเครือข่าย: แกะโค้ดโมดูล wifi"
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

![ภาพพื้นหลังปกบทเรียน bg](../../assets/img/cover_s09.svg)

<!-- _class: cover -->

# บทเรียน 4.2 — จอสถานะเครือข่าย: แกะโค้ดโมดูล wifi

## WiFi และเครือข่ายพื้นฐาน · บอร์ดของเราออกจากโต๊ะทำงาน แล้วไปมีที่อยู่ในเครือข่าย

**โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT**

> ต่อจากบทเรียน 4.1 — WiFi และเครือข่าย: dBm DHCP IP และ DNS

---

## เรื่องที่เราให้ 70% ผู้เรียนเขียน 30%

<svg viewBox="0 0 940 236" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="14" width="614" height="48" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="327" y="45" text-anchor="middle" font-size="22" font-weight="700" fill="#1565c0">70% — เฟิร์มแวร์ + ไดรเวอร์ WiFi ทำให้แล้ว</text>
  <rect x="646" y="14" width="274" height="48" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="783" y="45" text-anchor="middle" font-size="22" font-weight="700" fill="#ef6c00">30% — งานของเรา</text>
  <rect x="20" y="80" width="440" height="144" rx="8" fill="#f4f8fc" stroke="#90a4ae" stroke-width="2"/>
  <text x="40" y="108" font-size="19" font-weight="700" fill="#37474f">หกในแปดตัวของโมดูล wifi ที่โครงวันนี้เรียก</text>
  <text x="40" y="136" font-size="18" font-family="monospace" fill="#1565c0">wifi.scan()</text>
  <text x="230" y="136" font-size="17" fill="#546e7a">→ list ของ tuple</text>
  <text x="40" y="160" font-size="18" font-family="monospace" fill="#1565c0">wifi.connect(ssid, pw)</text>
  <text x="290" y="160" font-size="17" fill="#546e7a">→ bool</text>
  <text x="40" y="184" font-size="18" font-family="monospace" fill="#1565c0">wifi.is_connected()  wifi.ip()  wifi.status()</text>
  <text x="40" y="208" font-size="18" font-family="monospace" fill="#1565c0">wifi.ping(ip, timeout_ms)</text>
  <text x="330" y="208" font-size="17" fill="#546e7a">→ ms หรือ -1</text>
  <rect x="480" y="80" width="440" height="144" rx="8" fill="#fffaf3" stroke="#ffb066" stroke-width="2"/>
  <text x="500" y="108" font-size="19" font-weight="700" fill="#a1683a">สิ่งที่เราต้องตัดสินใจเอง</text>
  <text x="500" y="136" font-size="18" fill="#7a4a1a">เลือกวงไหนจากที่สแกนเจอ · เรียงยังไง</text>
  <text x="500" y="160" font-size="18" fill="#7a4a1a">แปลง dBm เป็นภาพที่คนอ่านเข้าใจ</text>
  <text x="500" y="184" font-size="18" fill="#7a4a1a">ยิง ping ไปที่ไหน บ่อยแค่ไหน</text>
  <text x="500" y="208" font-size="18" fill="#7a4a1a">แปลผลเป็นข้อความที่ช่วยคนแก้ปัญหาได้</text>
</svg>

ไดรเวอร์ WiFi หนักกว่าโค้ดทั้งชุดบทเรียนนี้หลายพันบรรทัด — เราไม่ได้เขียนมัน เรา **ใช้มันให้เป็น** และนั่นคือทักษะที่ตรงกับงานจริงมากกว่า

> โมดูล `wifi` มี **แปดชื่อ** ไม่ใช่หก — อีกสองตัวคือ `wifi.disconnect()` กับ `wifi.softap()` ซึ่งโครงหลักไม่ได้เรียก แต่เราจะลงมือทั้งคู่ในสไลด์ถัดไป เพราะตัวหนึ่งคือวิธีพิสูจน์ว่าลิงก์หลุดจริง และอีกตัวคือทางออกเมื่อในห้องไม่มีวงให้ต่อ

---

## สามข้อที่เฟิร์มแวร์ยังทำได้ไม่ครบ — ต้องรู้ก่อนเขียน

<svg viewBox="0 0 940 292" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="10" width="908" height="82" rx="9" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="40" y="40" font-size="20" font-weight="700" fill="#c62828">1 · wifi.status() มีช่อง ssid กับ rssi — แต่มันคืนค่าตายตัวเสมอ</text>
  <text x="40" y="68" font-size="18" fill="#8f1f1f">ssid คืนสตริงว่าง และ rssi คืน 0 ทุกครั้ง ไม่ว่าจะต่ออยู่กับวงไหน · ความแรงจริงต้องเอามาจาก wifi.scan()</text>
  <rect x="16" y="102" width="908" height="82" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="40" y="132" font-size="20" font-weight="700" fill="#ef6c00">2 · wifi.connect() ล็อกโหมดความปลอดภัยเป็น WPA3/WPA2 ตายตัว</text>
  <text x="40" y="160" font-size="18" fill="#a1683a">เครือข่ายเปิดไม่มีรหัสผ่าน ต่อจาก Python ไม่ได้ ทั้งที่เมนูบนจอต่อได้ · ถ้า AP ห้องเปิด ต้องขอวงที่มีรหัส</text>
  <rect x="16" y="194" width="908" height="88" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="40" y="224" font-size="20" font-weight="700" fill="#2e7d32">3 · หน้า Wi-Fi Setting ที่มากับเครื่อง แสดงค่าที่ "แต่งขึ้น" บางช่อง</text>
  <text x="40" y="252" font-size="18" fill="#1b5e20">netmask ถูกฮาร์ดโค้ดเป็น 255.255.255.0 และ gateway/DNS ถูกเดาเป็น a.b.c.1 — ไม่ได้ถามระบบจริง</text>
  <text x="40" y="276" font-size="18" font-weight="700" fill="#1b5e20">ถ้าเฟิร์มแวร์เปิด wifi.ifconfig() ให้ โค้ดของผู้เรียนจะแม่นกว่าหน้าจอที่มากับเครื่อง</text>
</svg>

ข้อ 1 กับข้อ 2 เป็น **กับดักที่ทำให้เสียเวลาทั้งบทเรียนถ้าไม่รู้ก่อน** — จะนั่งแก้โค้ดที่ไม่ได้ผิด

ข้อ 3 เป็นเรื่องที่น่าสนใจกว่านั้น: หน้าจอที่ดูน่าเชื่อถือ อาจแสดงค่าที่ไม่ได้มาจากการวัดจริง การรู้ว่า **ตัวเลขบนจอมาจากไหน** คือส่วนหนึ่งของงานวิศวกรรม ไม่ใช่การจับผิด

> ในโค้ดวันนี้เราก็เดาเกตเวย์เหมือนกัน — ต่างกันตรงที่เราจะ **ping เพื่อพิสูจน์** ว่าเดาถูก แล้วแสดงผลตามความจริง

---

## โมดูล `wifi` ทั้งแปดชื่อ — ตารางที่เปิดค้างไว้ได้ทั้งบทเรียน

<style scoped>
section table { font-size: .68em; }
section table td, section table th { padding: .16em .55em; }
</style>

| เรียกอย่างไร | คืนอะไร | สิ่งที่ต้องรู้ก่อนใช้ |
|---|---|---|
| `wifi.scan()` | list ของ tuple `(ssid, rssi, security, channel)` | คืน **ไม่เกิน 20 วง** ต่อครั้ง วงที่ 21 หายไปเงียบ ๆ · บล็อก 3-10 วินาที · ถ้าบอร์ดกำลังสแกนของตัวเองอยู่ มันจะรอให้เสร็จก่อนแล้วค่อยถามใหม่ ไม่โยน error ใส่เรา |
| `wifi.connect(ssid, password)` | `True` / `False` | รับ **สองอาร์กิวเมนต์แบบตำแหน่งเท่านั้น** · บล็อกได้ถึงราว 85 วินาทีเมื่อรหัสผิด · ล็อกโหมดเป็น WPA3/WPA2 ตายตัว จึง **ต่อวงเปิดที่ไม่มีรหัสผ่านจาก Python ไม่ได้** |
| `wifi.disconnect()` | `None` | ตัดลิงก์แล้วบอกคอร์จอให้ลดไอคอนลง · เรียกตอนยังไม่เคยต่อก็ไม่ error เงียบ ๆ ผ่านไป |
| `wifi.status()` | dict 5 คีย์ `mode` `connected` `ip` `ssid` `rssi` | `mode` คืน `"off"` / `"idle"` / `"sta"` เป็นช่องเดียวที่บอกมากกว่า `is_connected()` · แต่ **`ssid` คืนสตริงว่างและ `rssi` คืน 0 เสมอ** ทั้งคู่เป็นค่าตายตัวในเฟิร์มแวร์ |
| `wifi.is_connected()` | `True` / `False` | ถามสถานะจริงจากไดรเวอร์ทุกครั้ง ไม่ใช่ค่าที่จำไว้ |
| `wifi.ip()` | str | ยังไม่ต่อจะได้ `"0.0.0.0"` ซึ่ง **เป็นสตริงที่ไม่ว่าง จึงเป็นจริงใน `if`** · ต้องเทียบค่าตรง ๆ ห้ามเขียน `if wifi.ip():` |
| `wifi.ping(host, timeout=5000)` | int มิลลิวินาที หรือ `-1` | รับ **เลข IP เท่านั้น** ใส่ชื่อโฮสต์ได้ `ValueError` · ถ้ายังไม่ต่อเน็ตได้ `OSError` ไม่ใช่ `-1` |
| `wifi.softap(ssid, password)` | `True` / `False` | บอร์ดกลายเป็นตัวปล่อยสัญญาณเองที่ **192.168.4.1** · ไม่ใส่อาร์กิวเมนต์จะได้ชื่อ `PSoC-Edge-MPY` รหัส `micropython` · WPA2 ช่อง 1 |

หกแถวแรกคือของที่โครงหลักวันนี้เรียกจริง สองแถวล่างเราจะลองมือในสไลด์ถัดไป

<!-- อ่านตารางนี้ให้ครบก่อนเริ่มเขียน แล้วผู้เรียนจะประหยัดเวลาไปได้มาก — กับดักเกินครึ่งของชุดบทเรียนนี้อยู่ในคอลัมน์ขวา ไม่ได้อยู่ในโค้ดที่เราเขียนผิด -->

---

## สองตัวที่โครงหลักไม่ได้เรียก — และทำไมยังต้องรู้จัก

<style scoped>section svg{max-height:200px}</style>

```python
# --- disconnect(): วิธีพิสูจน์ว่า "หลุด" หน้าตาเป็นอย่างไรจริง ๆ ---
wifi.disconnect()                 # คืน None ไม่ใช่ True
print(wifi.is_connected())        # False
print(wifi.ip())                  # "0.0.0.0"  <- ไม่ว่าง จึงเป็นจริงใน if

# --- softap(): เมื่อหาวงที่ตั้งไว้ไม่เจอ บอร์ดปล่อยวงของตัวเองได้ ---
wifi.softap("bento-team01", "12345678")   # True แล้วบอร์ดอยู่ที่ 192.168.4.1
```

<svg viewBox="0 0 940 214" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="12" width="440" height="186" rx="9" fill="#eceff1" stroke="#546e7a" stroke-width="2"/>
  <text x="36" y="42" font-size="20" font-weight="700" fill="#37474f">โหมด sta — ที่เราใช้กันทั้งบทเรียน</text>
  <rect x="36" y="60" width="118" height="52" rx="7" fill="#ffffff" stroke="#546e7a" stroke-width="2"/>
  <text x="95" y="92" text-anchor="middle" font-size="18" font-weight="700" fill="#37474f">บอร์ด</text>
  <line x1="154" y1="86" x2="298" y2="86" stroke="#546e7a" stroke-width="3"/>
  <rect x="298" y="60" width="140" height="52" rx="7" fill="#ffffff" stroke="#546e7a" stroke-width="2"/>
  <text x="368" y="92" text-anchor="middle" font-size="18" font-weight="700" fill="#37474f">AP ที่มีอยู่</text>
  <text x="36" y="146" font-size="18" fill="#546e7a">บอร์ดไปขอเข้าร่วมวงที่มีอยู่แล้ว</text>
  <text x="36" y="176" font-size="18" fill="#546e7a">ได้เลข IP มาจาก DHCP ของ AP นั้น</text>
  <rect x="484" y="12" width="440" height="186" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="504" y="42" font-size="20" font-weight="700" fill="#2e7d32">โหมด softap — บอร์ดเป็นเจ้าของวงเอง</text>
  <rect x="504" y="60" width="118" height="52" rx="7" fill="#ffffff" stroke="#2e7d32" stroke-width="2"/>
  <text x="563" y="92" text-anchor="middle" font-size="18" font-weight="700" fill="#2e7d32">บอร์ด</text>
  <line x1="622" y1="86" x2="766" y2="86" stroke="#2e7d32" stroke-width="3"/>
  <rect x="766" y="60" width="140" height="52" rx="7" fill="#ffffff" stroke="#2e7d32" stroke-width="2"/>
  <text x="836" y="92" text-anchor="middle" font-size="18" font-weight="700" fill="#2e7d32">มือถือเรา</text>
  <text x="504" y="146" font-size="18" fill="#1b5e20">บอร์ดอยู่ที่ 192.168.4.1 เสมอ ไม่ต้องเดา</text>
  <text x="504" y="176" font-size="18" fill="#1b5e20">ไม่มีทางออกอินเทอร์เน็ต — คุยได้แค่ในวงนี้</text>
</svg>

`disconnect()` ทำให้เรา **สร้างสถานะ "หลุด" ขึ้นมาดูได้ตามสั่ง** ไม่ต้องรอให้เน็ตล่มเอง — บทเรียน 5.1–5.3 ต้องเขียนโค้ดที่ทนการหลุด ถ้าไม่เคยเห็นว่าหลุดแล้วค่าไหนเปลี่ยน จะเขียนเงื่อนไขถูกได้ยาก

`softap()` เป็นทางออกจริงเมื่อไม่มีวงให้ต่อ — เครื่องมือช่างและกล้องติดรถจำนวนมากตั้งค่าครั้งแรกด้วยวิธีนี้ ข้อแลกเปลี่ยนคือ **วิทยุมีชุดเดียว** เป็น AP แล้วจะเป็นลูกข่ายพร้อมกันไม่ได้ `ping()` ออกเน็ตจึงใช้ไม่ได้ในโหมดนี้ · ลองไฟล์ [`07_disconnect_rejoin.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l02-network-status-code/examples/07_disconnect_rejoin.py) กับ [`08_softap_fallback.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/aiot-micropython/m04-iot-connectivity/l02-network-status-code/examples/08_softap_fallback.py)

<!-- ไฟล์ตัวหลัง (08_softap_fallback) คือแผนสำรองของทั้งคอร์ส ถ้าวันไหนบอร์ดหาวงที่ตั้งไว้ไม่เจอ -->

---

## แกะโค้ดจริง — ท่าที่ 1 วางสองแผงให้ครบก่อนเข้าลูป

<style scoped>section pre{font-size:.58em;line-height:1.25} section svg{max-height:168px}</style>

```python
ui.screen()
time.sleep_ms(200)
ui.Label("สถานะเครือข่ายของทีม", x=24, y=8, color=COL_TEXT, value=24)
l_ssid = ui.Label("SSID: -", x=336, y=12, color=COL_TEXT, value=20)
l_ip = ui.Label("IP: -", x=24, y=48, color=COL_TEXT, value=20)
l_tick = ui.Label("กำลังสแกน", x=336, y=48, color=COL_DIM, value=20)
btn_scan = ui.Button("สแกนใหม่", x=552, y=8, w=216, h=88, color=0x3A4150, value=20)

tbl = ui.Table(x=24, y=104, w=480, h=288, cols=4)   # แถวละ 72 px: หัว + 3 แถว = 288
tbl.col_width(0, 144)        # กว้างพอสำหรับชื่อ 12 ตัวอักษร ซึ่งเป็นเพดานที่เราตัดไว้
tbl.col_width(1, 96)
tbl.col_width(2, 80)
tbl.col_width(3, 128)        # "มีรหัส" คือข้อความที่ยาวที่สุดในคอลัมน์นี้
```

<svg viewBox="0 0 940 210" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="10" width="500" height="190" rx="8" fill="#142240" stroke="#a0b4cc" stroke-width="2"/>
  <line x1="30" y1="52" x2="530" y2="52" stroke="#a0b4cc" stroke-width="2"/>
  <line x1="188" y1="10" x2="188" y2="200" stroke="#3a4a68" stroke-width="1"/>
  <line x1="296" y1="10" x2="296" y2="200" stroke="#3a4a68" stroke-width="1"/>
  <line x1="368" y1="10" x2="368" y2="200" stroke="#3a4a68" stroke-width="1"/>
  <text x="44" y="38" font-size="17" font-weight="700" fill="#ffffff">SSID</text>
  <text x="202" y="38" font-size="17" font-weight="700" fill="#ffffff">dBm</text>
  <text x="310" y="38" font-size="17" font-weight="700" fill="#ffffff">ช่อง</text>
  <text x="382" y="38" font-size="17" font-weight="700" fill="#ffffff">รหัส</text>
  <text x="44" y="86" font-size="17" fill="#ffffff">my-hotspot</text>
  <text x="202" y="86" font-size="17" fill="#ffffff">-48</text>
  <text x="310" y="86" font-size="17" fill="#ffffff">6</text>
  <text x="382" y="86" font-size="17" fill="#ffffff">มีรหัส</text>
  <text x="44" y="132" font-size="17" fill="#a0b4cc">Office-2.4</text>
  <text x="202" y="132" font-size="17" fill="#a0b4cc">-67</text>
  <text x="310" y="132" font-size="17" fill="#a0b4cc">1</text>
  <text x="382" y="132" font-size="17" fill="#a0b4cc">มีรหัส</text>
  <text x="44" y="178" font-size="17" fill="#a0b4cc">Guest-Zone-1</text>
  <text x="202" y="178" font-size="17" fill="#a0b4cc">-74</text>
  <text x="310" y="178" font-size="17" fill="#a0b4cc">11</text>
  <text x="382" y="178" font-size="17" fill="#a0b4cc">เปิด</text>
  <rect x="548" y="10" width="250" height="190" rx="8" fill="#142240" stroke="#00e676" stroke-width="2"/>
  <text x="566" y="34" font-size="17" font-weight="700" fill="#a0b4cc">สถานะลิงก์</text>
  <circle cx="578" cy="58" r="11" fill="#00e676"/>
  <text x="600" y="64" font-size="16" fill="#a0b4cc">ต่ออยู่</text>
  <circle cx="578" cy="90" r="11" fill="#5a2020"/>
  <text x="600" y="96" font-size="16" fill="#a0b4cc">ยังไม่ต่อ</text>
  <text x="566" y="126" font-size="16" fill="#ffffff">SSID · IP · ping x2</text>
  <text x="566" y="152" font-size="16" fill="#ffffff">-48 dBm (84%)</text>
  <rect x="566" y="164" width="180" height="10" rx="4" fill="#263550"/>
  <rect x="566" y="164" width="151" height="10" rx="4" fill="#4fc3f7"/>
  <line x1="566" y1="184" x2="746" y2="184" stroke="#ffffff" stroke-width="2"/>
  <text x="566" y="196" font-size="14" fill="#a0b4cc">-90</text>
  <text x="716" y="196" font-size="14" fill="#a0b4cc">-40</text>
  <text x="934" y="96" text-anchor="end" font-size="18" font-weight="700" fill="#455a64">16 widgets</text>
  <text x="934" y="120" text-anchor="end" font-size="17" fill="#78909c">จากเพดาน 64</text>
</svg>

ทุก widget ถูกสร้าง **ก่อน** เข้าลูป ในลูปแค่เปลี่ยนข้อความกับค่า · ตารางเดียวแทน `ui.Label` สิบตัว — **`col_width` คือสิ่งเดียวที่ต้องตั้งให้ถูก** ช่องแคบกว่าข้อความ = ตัดบรรทัด = แถวสูงสองเท่า แถวสุดท้ายตกขอบเงียบ ๆ · ปุ่ม `สแกนใหม่` อยู่บนแถบหัวเรื่อง เพราะ **มุมขวาล่างเฟิร์มแวร์ถือไว้ให้ปุ่ม Console** widget ที่ไปทับมันจะถูกบังจนกดไม่โดน

> 16 widgets จาก 64 — เหลือที่ให้ทีมเติมของตัวเองได้อีกมาก

---

## แกะโค้ดจริง — ท่าที่ 2 มันคือ tuple ไม่ใช่ dict

<style scoped>section svg{max-height:224px}</style>

```python
# --- ท่าที่ 2 + 3 อยู่ในฟังก์ชันเดียว เพราะปุ่ม "สแกนใหม่" ต้องเรียกซ้ำได้ทั้งชุด ---
def rescan():
    nets = wifi.scan()                              # บล็อกราว 3-10 วินาที
    nets.sort(key=lambda net: net[1], reverse=True) # net[1] คือ rssi
```

<svg viewBox="0 0 940 222" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="14" width="440" height="196" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="44" y="44" font-size="19" font-weight="700" fill="#2e7d32">ของจริงที่ scan() คืนมา</text>
  <text x="44" y="76" font-size="17" font-family="monospace" fill="#1b5e20">("my-hotspot", -48, 4, 6)</text>
  <text x="44" y="112" font-size="17" fill="#1b5e20">net[0] = ssid</text>
  <text x="250" y="112" font-size="17" fill="#1b5e20">net[1] = rssi</text>
  <text x="44" y="140" font-size="17" fill="#1b5e20">net[2] = security</text>
  <text x="250" y="140" font-size="17" fill="#1b5e20">net[3] = channel</text>
  <text x="44" y="172" font-size="17" fill="#4a7c4e">เรียงด้วย net[1] มากไปน้อย = แรงไปอ่อน</text>
  <rect x="480" y="14" width="440" height="196" rx="8" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="504" y="44" font-size="19" font-weight="700" fill="#c62828">สิ่งที่ตัวอย่างที่มากับเครื่องเขียนผิด</text>
  <text x="504" y="76" font-size="17" font-family="monospace" fill="#b71c1c">net['ssid']  net['rssi']</text>
  <text x="504" y="112" font-size="17" fill="#b71c1c">TypeError: tuple indices must be</text>
  <text x="504" y="134" font-size="17" fill="#b71c1c">integers, not str</text>
  <text x="504" y="172" font-size="17" fill="#8d6e63">ชุดตัวอย่างที่มากับเฟิร์มแวร์ ไฟล์</text>
  <text x="504" y="196" font-size="17" fill="#8d6e63">network/01_wifi_scan_connect.py บรรทัด 33</text>
</svg>

`sort()` แก้ลิสต์เดิมในที่ · `key=lambda net: net[1]` สั่งให้เรียงตามช่องที่สอง · `reverse=True` ทำให้ค่ามากมาก่อน — **RSSI ค่ามากคือแรงกว่า** เพราะ −48 มากกว่า −79

ทำไมสองบรรทัดนี้ต้องอยู่ในฟังก์ชัน: ปุ่ม `สแกนใหม่` ต้องทำงานทั้งชุด — สแกน เรียง ล้างตาราง เทใหม่ ถ้าปล่อยสองบรรทัดนี้ไว้กลางไฟล์ ปุ่มจะเรียกได้แค่ครึ่งเดียวของงาน

ตัวอย่างที่มากับเฟิร์มแวร์เขียนผิดจริง — ไฟล์ `network/01_wifi_scan_connect.py` บรรทัด 33 ยังเขียน `net['ssid']` อยู่จนวันนี้ บทเรียนคือ **โค้ดตัวอย่างไม่ใช่เอกสารอ้างอิง** อย่าลอกไปใช้

<!-- เจอ TypeError: tuple indices เมื่อไร ให้นึกถึงบรรทัดนี้ทันที — เกือบทุกครั้งคือเรื่องเดียวกัน -->

---

## แกะโค้ดจริง — ท่าที่ 3 เทลงตาราง แล้ววัดวงของทีมด้วย dBm

<style scoped>section pre{font-size:.58em;line-height:1.25} section svg{max-height:128px} section p{margin:.1em 0}</style>

```python
    tbl.clear_items()                           # ท่าที่ 3 (ยังอยู่ใน rescan)
    tbl.add_row("SSID", "dBm", "ช่อง", "รหัส")    # หัวสั้น เพราะช่องแคบ
    for i in range(min(TOP_N, len(nets))):
        ssid, rssi, security, channel = nets[i] # แกะสี่ช่องพร้อมกัน
        tbl.add_row(ssid[:12], str(rssi), str(channel),
                    "เปิด" if security == 0 else "มีรหัส")
        ui.poll()
    for ssid, rssi, security, channel in nets:  # แล้วค่อยขยับมาตรวัดฝั่งขวา
        if ssid == WIFI_SSID:                   # มาตรวัดเล่าเรื่องวงของทีมเอง
            pct, col = signal_of(rssi)
            bar_rssi.value(rssi)                # Bar รับพิสัย -90..-40 ตรง ๆ ได้
            l_rssi.color(col)
            l_rssi.text("ความแรง " + str(rssi) + " dBm (" + str(pct) + "%)")
```

$q=\operatorname{clamp}\!\left(\frac{\text{RSSI}-(-90)}{(-40)-(-90)}\times100,\;0,\;100\right)$ — ยืดช่วง −90 ถึง −40 dBm ให้เป็น 0 ถึง 100 เพื่อบอก **คุณภาพเป็นเปอร์เซ็นต์** ข้างตัวเลข dBm · **ตัวเลขจริง:** −67 dBm → $(-67+90)\times 2 = 46$

<svg viewBox="0 0 940 158" xmlns="http://www.w3.org/2000/svg">
  <text x="20" y="30" font-size="19" font-weight="700" fill="#37474f">−90 dBm = แท่งว่าง · −40 dBm = แท่งเต็ม · เลขในวงเล็บข้างค่า dBm คือคุณภาพเป็น %</text>
  <text x="24" y="70" font-size="18" fill="#37474f">-48 dBm</text>
  <rect x="140" y="56" width="300" height="18" rx="6" fill="#dfe6ee"/>
  <rect id="an14" x="140" y="56" width="252" height="18" rx="6" fill="#00a862"/>
  <animate attributeName="stroke-dashoffset" values="200;0" dur="2.4s" repeatCount="indefinite"/>
  <text x="456" y="70" font-size="18" font-weight="700" fill="#00a862">84</text>
  <text x="24" y="108" font-size="18" fill="#37474f">-67 dBm</text>
  <rect x="140" y="94" width="300" height="18" rx="6" fill="#dfe6ee"/>
  <rect id="an15" x="140" y="94" width="138" height="18" rx="6" fill="#ef8f00"/>
  <animate attributeName="stroke-dashoffset" values="200;0" dur="2.4s" begin="0.6s" repeatCount="indefinite"/>
  <text x="456" y="108" font-size="18" font-weight="700" fill="#ef8f00">46</text>
  <text x="24" y="146" font-size="18" fill="#37474f">-86 dBm</text>
  <rect x="140" y="132" width="300" height="18" rx="6" fill="#dfe6ee"/>
  <rect id="an16" x="140" y="132" width="24" height="18" rx="6" fill="#c62828"/>
  <animate attributeName="stroke-dashoffset" values="200;0" dur="2.4s" begin="1.2s" repeatCount="indefinite"/>
  <text x="456" y="146" font-size="18" font-weight="700" fill="#c62828">8</text>
  <text x="530" y="70" font-size="18" fill="#546e7a">แท่งกระเพื่อมเล็กน้อยตลอดเวลา</text>
  <text x="530" y="98" font-size="18" fill="#546e7a">เพราะคลื่นจริงไม่เคยนิ่ง — คนเดินผ่าน</text>
  <text x="530" y="126" font-size="18" fill="#546e7a">ประตูเปิดปิด ก็ทำให้เลขขยับได้ 3-5 dB</text>
</svg>

**`ui.Bar` ไม่ต้องแปลงอะไรเลย** เพราะตั้ง `min=-90, max=-40` ได้ตรง ๆ — ที่ต้องแปลงคือเลขที่ **คน** จะอ่าน ไม่ใช่เลขที่ widget จะรับ · `min(TOP_N, len(nets))` กันพังตอนสแกนเจอน้อยกว่าสามวง

> `signal_of()` คืนทั้งเปอร์เซ็นต์และสีพร้อมกัน เพราะมาจากตัวเลขเดียว — แยกกันคำนวณเมื่อไร วันหนึ่งมันจะไม่ตรงกัน

---

## แกะโค้ดจริง — ท่าที่ 4 บรรทัดที่บล็อกได้ 85 วินาที

<style scoped>section pre{font-size:.58em;line-height:1.25} section svg{max-height:150px}</style>

```python
l_tick.text("กำลังต่อ 85 วิ")            # ท่าที่ 4: บอกก่อน แล้วค่อยเรียกของที่บล็อก
ui.poll()
ok = wifi.connect(WIFI_SSID, WIFI_PASS)   # สองอาร์กิวเมนต์ตามลำดับเท่านั้น

if not ok:
    l_ssid.color(COL_BAD)
    l_ssid.text("ต่อไม่ติด")
    l_tick.text("ตรวจ SSID/รหัสผ่าน")
    ui.poll()
    raise SystemExit
...
led_up.value(1)                           # ต่อติดแล้วไฟดวงบนติด ดวงล่างหรี่
led_down.value(0)
```

<svg viewBox="0 0 940 176" xmlns="http://www.w3.org/2000/svg">
  <text x="20" y="30" font-size="19" font-weight="700" fill="#37474f">เส้นเวลาของ wifi.connect() หนึ่งครั้ง</text>
  <rect x="30" y="48" width="856" height="28" rx="6" fill="#eceff1" stroke="#b0bec5"/>
  <rect x="30" y="48" width="120" height="28" rx="6" fill="#2e7d32"/>
  <rect x="150" y="48" width="736" height="28" fill="#ffcdd2"/>
  <rect id="an17" x="30" y="48" width="60" height="28" rx="6" fill="#1b5e20"/>
  <animate attributeName="stroke-dashoffset" values="200;0" dur="3.4s" repeatCount="indefinite"/>
  <text x="90" y="102" text-anchor="middle" font-size="18" font-weight="700" fill="#1b5e20">3-8 วิ</text>
  <text x="90" y="126" text-anchor="middle" font-size="17" fill="#4a7c4e">รหัสถูก</text>
  <text x="518" y="102" text-anchor="middle" font-size="18" font-weight="700" fill="#c62828">นานถึง 85 วินาที แล้วคืน False</text>
  <text x="518" y="126" text-anchor="middle" font-size="17" fill="#8f1f1f">รหัสผิด · SSID พิมพ์ผิด · วงเป็นแบบเปิด</text>
  <text x="30" y="160" font-size="18" fill="#546e7a">ระหว่างนี้จอไม่อัปเดตเลย เพราะโค้ดของเราหยุดรอที่บรรทัดนี้ — จึงต้องเขียนข้อความบอกไว้ก่อนเรียก</text>
  <line x1="886" y1="42" x2="886" y2="82" stroke="#c62828" stroke-width="3"/>
  <text x="886" y="34" text-anchor="middle" font-size="17" fill="#c62828">ยอมแพ้</text>
</svg>

`wifi.connect()` รับ **สองอาร์กิวเมนต์แบบตำแหน่งเท่านั้น** — ไม่มี `timeout=` ไม่มี `security=` · `raise SystemExit` เมื่อต่อไม่ติดคือการตัดสินใจที่ตั้งใจ เพราะท่าที่ 5 ไม่มีความหมายถ้าไม่มีลิงก์ — **ล้มเร็วดีกว่าปล่อยให้ลูปวนแสดง timeout จนคนดูสับสน** · สองบรรทัดสุดท้ายคือ **สถานะลิงก์เป็นไฟ ไม่ใช่ตัวอักษรสี** — แปลงภาพเป็นขาวดำแล้วตัวอักษรเขียว/แดงกลายเป็นเทาเหมือนกัน ส่วนไฟติดกับไฟหรี่ยังแยกออกด้วยความสว่างและตำแหน่ง

> ในระบบฝังตัว ทุกบรรทัดที่บล็อกนานกว่าครึ่งวินาที ต้องมีการแจ้งผู้ใช้กำกับเสมอ

---

## แกะโค้ดจริง — ท่าที่ 5 ลูปสถานะสด ยิงสองปลายทาง

```python
while True:                                     # ท่าที่ 5 — ลูปเดินทุก 200 ms
    now = time.ticks_ms()
    events = ui.poll()                          # ลืมบรรทัดนี้ = widget หายใน 2 วิ
    for ev in events:                           # นิ้วมาถึงเมื่อไรก็รับได้ทันที
        if ev["type"] == "clicked" and ev["handle"] == btn_scan.id():
            l_tick.text("กำลังสแกน")            # บอกก่อน แล้วค่อยเรียกของที่บล็อก
            ui.poll()
            nets = rescan()
    if wifi.is_connected():
        if time.ticks_diff(now, t_ping) >= PING_EVERY_MS:   # ping เดินนาฬิกาตัวเอง
            t_ping = now
            try:
                ms_gw = wifi.ping(gw, PING_TIMEOUT_MS)
                ms_net = wifi.ping(NET_TEST_IP, PING_TIMEOUT_MS)
            except OSError:
                ms_gw, ms_net = -1, -1
            l_gw.text(ms_text("เกตเวย์", ms_gw))
    time.sleep_ms(200)
```

ลูปเดินทุก 200 ms **แต่ ping เดินตามนาฬิกาของตัวเองทุก 3 วินาที** — งานคนละจังหวะอยู่ในลูปเดียวกันได้ ถ้าแต่ละงานถามนาฬิกาเอง แทนที่จะใช้ `sleep` ยาว ๆ ขวางทาง · ถ้าเขียน `sleep_ms(3000)` ก้อนเดียว ปุ่มบนจอจะกดแล้วรอถึงสามวินาทีกว่าจะตอบ ซึ่งคนกดจะสรุปว่าปุ่มเสีย

---

## แกะโค้ดจริง — ท่าที่ 5 (ต่อ) สองนาฬิกาในลูปเดียว

<svg viewBox="0 0 940 168" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="10" width="420" height="148" rx="8" fill="#142240" stroke="#00e676" stroke-width="2"/>
  <text x="172" y="38" font-size="18" font-weight="700" fill="#00e676">สถานะลิงก์</text>
  <text x="172" y="68" font-size="17" fill="#ffffff">SSID: my-hotspot</text>
  <text x="172" y="94" font-size="17" fill="#ffffff">IP: 192.168.1.42</text>
  <text x="172" y="120" font-size="17" fill="#ffffff">เกตเวย์ 3 ms</text>
  <text x="172" y="146" font-size="17" fill="#ffffff">อินเทอร์เน็ต 24 ms</text>
  <text id="anT1" x="372" y="146" font-size="17" fill="#ff5252" opacity="0.4">หรือ timeout</text>
  <animate attributeName="r" values="6;11;6" dur="6s" repeatCount="indefinite"/>
  <circle id="an18" cx="556" cy="26" r="6" fill="#00e676"/>
  <animate attributeName="r" values="6;11;6" dur="3s" repeatCount="indefinite"/>
  <text x="612" y="46" font-size="18" font-weight="700" fill="#455a64">ทุก 3 วินาที</text>
  <text x="612" y="74" font-size="17" fill="#546e7a">แต่ ui.poll() ทุก 200 ms</text>
  <text x="612" y="102" font-size="17" fill="#546e7a">ห้าม sleep_ms(3000) ก้อนเดียว</text>
  <text x="612" y="130" font-size="17" fill="#c62828">ไม่งั้น widget หายภายใน 2 วินาที</text>
</svg>

`try/except` ครอบไว้เพราะ **ความผิดพลาดชั่วคราวของเครือข่ายเป็นเรื่องปกติ ไม่ใช่ข้อยกเว้น** · ส่วนตัวเลขนับถอยหลัง "วัดใหม่ใน N วิ" เขียนใหม่เมื่อ **วินาทีเปลี่ยน** เท่านั้น ไม่ใช่ทุกรอบลูป — ตัวเลขที่กระพริบห้าครั้งต่อวินาที คนอ่านไม่ทันและไม่มีใครได้ประโยชน์

> ยิงเกตเวย์ก่อนแล้วค่อยยิงอินเทอร์เน็ต — ลำดับนี้ทำให้อ่านผลสองบรรทัดแล้วรู้ทันทีว่าขาดตรงไหน

---

## ข้อมูลไหลไปทางไหน — ตั้งแต่คลื่นถึงตัวเลขบนจอ

<svg viewBox="0 0 940 216" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="60" width="150" height="76" rx="10" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="85" y="92" text-anchor="middle" font-size="19" font-weight="700" fill="#0277bd">คลื่นในอากาศ</text>
  <text x="85" y="116" text-anchor="middle" font-size="17" fill="#01579b">2.4 / 5 GHz</text>
  <rect x="190" y="60" width="160" height="76" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="270" y="88" text-anchor="middle" font-size="19" font-weight="700" fill="#ef6c00">CYW55513</text>
  <text x="270" y="112" text-anchor="middle" font-size="17" fill="#e65100">ชิปวิทยุ + ไดรเวอร์</text>
  <rect x="380" y="60" width="170" height="76" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="465" y="88" text-anchor="middle" font-size="19" font-weight="700" fill="#1565c0">CM33</text>
  <text x="465" y="112" text-anchor="middle" font-size="17" fill="#0d47a1">โค้ด Python ของเรา</text>
  <rect x="580" y="60" width="140" height="76" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="650" y="92" text-anchor="middle" font-size="19" font-weight="700" fill="#6a1b9a">IPC</text>
  <text x="650" y="116" text-anchor="middle" font-size="17" fill="#4a148c">กล่องจดหมาย</text>
  <rect x="750" y="60" width="180" height="76" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="840" y="88" text-anchor="middle" font-size="19" font-weight="700" fill="#2e7d32">CM55 → จอ</text>
  <text x="840" y="112" text-anchor="middle" font-size="17" fill="#1b5e20">Label + Bar ที่คนอ่าน</text>
  <line x1="162" y1="98" x2="178" y2="98" stroke="#6a1b9a" stroke-width="3"/>
  <polygon points="188,98 176,92 176,104" fill="#6a1b9a"/>
  <line x1="352" y1="98" x2="368" y2="98" stroke="#6a1b9a" stroke-width="3"/>
  <polygon points="378,98 366,92 366,104" fill="#6a1b9a"/>
  <line x1="552" y1="98" x2="568" y2="98" stroke="#6a1b9a" stroke-width="3"/>
  <polygon points="578,98 566,92 566,104" fill="#6a1b9a"/>
  <line x1="722" y1="98" x2="738" y2="98" stroke="#6a1b9a" stroke-width="3"/>
  <polygon points="748,98 736,92 736,104" fill="#6a1b9a"/>
  <circle id="an19" r="9" fill="#e91e63" cx="85" cy="158"/>
  <animateMotion href="#an19" path="M0,0 L185,0 L380,0 L565,0 L755,0" dur="4.2s" repeatCount="indefinite"/>
  <text x="470" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#455a64">RSSI หนึ่งค่า เดินทางผ่านห้าจุดกว่าจะเป็นแท่งสีบนจอ</text>
  <text x="470" y="190" text-anchor="middle" font-size="18" fill="#78909c">WiFi ทั้งหมดอยู่ฝั่ง CM33 เท่านั้น — CM55 แตะวงจรเครือข่ายไม่ได้เลย</text>
  <text x="470" y="212" text-anchor="middle" font-size="18" fill="#78909c">จอไม่ขึ้นเลข ไม่ได้แปลว่าเน็ตพัง ให้ไล่ดูว่าขาดตอนที่จุดไหน</text>
</svg>

> เวลาดีบัก ให้ถามว่า "ขาดที่ช่วงไหนของห้าช่วงนี้" แล้วปัญหาจะเหลือแค่หนึ่งในห้า ไม่ใช่ทั้งระบบ

---

## วิธีรันบนบอร์ด

<svg viewBox="0 0 940 190" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="18" width="216" height="70" rx="8" fill="#ede7f6" stroke="#4527a0" stroke-width="2"/>
  <text x="122" y="46" text-anchor="middle" font-size="19" font-weight="700" fill="#4527a0">1 · เปิด Playground</text>
  <text x="122" y="72" text-anchor="middle" font-size="17" fill="#5e35b1">ค้างหน้านี้ไว้ตลอดบทเรียน</text>
  <rect x="246" y="18" width="216" height="70" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="354" y="46" text-anchor="middle" font-size="19" font-weight="700" fill="#1565c0">2 · แก้ SSID + รหัส</text>
  <text x="354" y="72" text-anchor="middle" font-size="17" fill="#0d47a1">สองบรรทัดบนสุดของไฟล์</text>
  <rect x="478" y="18" width="216" height="70" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="586" y="46" text-anchor="middle" font-size="19" font-weight="700" fill="#ef6c00">3 · เติม 6 ช่องว่าง</text>
  <text x="586" y="72" text-anchor="middle" font-size="17" fill="#e65100">ทีละจุด แล้วรันทุกครั้ง</text>
  <rect id="an20" x="710" y="18" width="216" height="70" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <animate href="#an20" attributeName="stroke-width" values="2;4;2" dur="1.8s" repeatCount="indefinite"/>
  <text x="818" y="46" text-anchor="middle" font-size="19" font-weight="700" fill="#2e7d32">4 · Program to Device</text>
  <text x="818" y="72" text-anchor="middle" font-size="17" fill="#1b5e20">แล้วมองจอบอร์ด</text>
  <rect x="14" y="104" width="912" height="72" rx="8" fill="#fffde7" stroke="#f9a825" stroke-width="2"/>
  <text x="38" y="132" font-size="19" font-weight="700" fill="#a1683a">สิ่งที่จะเห็นตามลำดับ — และห้ามตกใจ</text>
  <text x="38" y="160" font-size="18" fill="#7a4a1a">ตารางว่าง → นิ่ง 3-10 วิ (สแกน) → สามแถวขึ้นพร้อมกัน → นิ่งอีกครั้ง (ต่อ) → ไฟเขียวติด แล้ว ping เดิน</text>
</svg>

โครงหน้าจอถูกวางให้ต่อยอดจากแดชบอร์ดบทเรียน 3.7–3.9 ได้ทันที — ถ้าทีมอยากเอาการ์ด IMU กลับมาวางคู่กัน ให้ลด `TOP_N` จาก 3 เหลือ 2 แล้วตั้ง `h` ของตารางเป็น 216 (หัวตารางบวกสองแถว แถวละ 72) พื้นที่ที่ว่างขึ้นมาพอวางการ์ดเดิมได้

ถ้าจอค้างอยู่ที่ `กำลังต่อ 85 วิ` นานเกินหนึ่งนาทีครึ่ง ให้กด **RESTART** แล้วตรวจ SSID กับรหัสผ่านทีละตัวอักษร — อย่ารอต่อ

> ระหว่างพิมพ์ตามทีละท่า จับเวลาและจดตัวเลขที่เห็นบนจอไว้ด้วย (ถ้าเรียนเป็นกลุ่ม สลับกันพิมพ์กับจด)
