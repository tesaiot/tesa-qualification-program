---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก Edge AI Developer (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY-NC 4.0"
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

# บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ
## เอา verdict ของโมเดล มารวมกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์

**โมดูล 6 — แอป Edge AI**

**โมดูล 6 (Apps) — ชุดบทเรียนปิดกล่อง (fusion + IoT)**

> คาถาประจำบทเรียน: **"โมเดลตอบว่า 'เจออะไร' — แต่การตัดสินใจที่เชื่อถือได้เกิดตอนเอา verdict มายืนยันกับเซนเซอร์ดิบอีกตัว แล้วส่งเหตุการณ์นั้นออกไปให้โลกภายนอกรู้"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

ยังใช้แนว **กลับด้าน** เหมือนทั้งคอร์ส — ชุดบทเรียนนี้เราจะรันแอปกันขโมย 3 เซนเซอร์ที่ทำงานได้จริงก่อน แล้วค่อยแกะว่ามัน "รวมสัญญาณหลายตัว" ยังไง แล้วต่อยอดให้มันคุยกับคลาวด์

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen17" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันแอปโหวตจริงก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">10_motion_alarm</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะการรวมสัญญาณ</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">verdict + เซนเซอร์ดิบ</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">ต่อ IoT เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">WiFi + MQTT</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">สู่ Capstone</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">8.1–8.2</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen17)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen17)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen17)"/>
</svg>
</div>

นี่คือขั้น **Investigate → Modify → Make** ของ PRIMM: เราเห็นแอปหลายเซนเซอร์ทำงานแล้ว (Run) ชุดบทเรียนนี้เปิดฝาดูวิธีรวมสัญญาณ (Investigate) แล้วเปลี่ยนจาก "โหวตดิบ 3 ตัว" เป็น "verdict ของโมเดล + เซนเซอร์ดิบ 1 ตัว → ส่งขึ้นคลาวด์" (Modify/Make)

> บทเรียน 6.1–6.2 เราสร้างแอปโมเดลเดียว บทเรียน 6.3–6.4 เราต่อ action pipeline — ชุดบทเรียนนี้เป็นก้าวสุดท้ายของ โมดูล 6 (Apps): ทำให้การตัดสินใจ **เชื่อถือได้ขึ้น** (fusion) แล้ว **ออกไปไกลกว่าบอร์ด** (IoT)

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วยการสตรีมเหตุการณ์ Edge AI ขึ้นคลาวด์:

1. **Sensor fusion คืออะไร** — ทำไม verdict ของโมเดลอย่างเดียวยังไม่พอ
2. **verdict + raw sensor** — เอาคำตอบของโมเดล (what) มายืนยันกับสัญญาณดิบ (how strong)
3. **IoT streaming** — `wifi.connect()` ต่อเน็ต แล้ว `mqtt.publish()` ส่งเหตุการณ์ออกไป
4. **degrade อย่างสง่างาม** — โค้ดชุดเดียวรันได้ทั้งบอร์ด (มีเน็ต) และ Emulator (ไม่มีเน็ต)
5. ลงมือ: เติม [`s17_fusion_iot.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py) — fuse verdict กับ gyro ดิบ แล้ว publish ขึ้น MQTT

ปลายทางของวันนี้: พอโมเดลจับ `shaking` **และ** gyro ดิบแรงพอ แอปจะยิงเหตุการณ์เดียว **ขึ้น MQTT broker** (หรือลง console ถ้าอยู่ Emulator)

> วันนี้เราต่อยอดจาก "verdict → action" (บทเรียน 6.3–6.4) ไปอีกสองชั้น: action ที่ **ผ่านการยืนยัน** (fusion) และ action ที่ **ไปถึงคลาวด์** (IoT)

---

# ชุดบทเรียนนี้อยู่ตรงไหนของคอร์ส

บทเรียน 6.5–6.6 เป็นบทเรียน **ปิดกล่อง โมดูล 6 (Apps)** — จากอ่านผล (บทเรียน 6.1–6.2) สู่สั่งการ (บทเรียน 6.3–6.4) จนถึงตัดสินใจแบบรวมสัญญาณ + ส่งออก (บทเรียน 6.5–6.6) ก่อนเข้าสู่ โมดูล 7 (Researcher)

<div style="text-align:center;margin:8px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <line x1="60" y1="60" x2="760" y2="60" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="150" cy="60" r="9" fill="#2e7d32"/>
  <text x="150" y="40" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">บทเรียน 6.1–6.2</text>
  <text x="150" y="86" font-size="11" fill="#777" text-anchor="middle">แอปโมเดลเดียว</text>
  <circle cx="360" cy="60" r="9" fill="#1565c0"/>
  <text x="360" y="40" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">บทเรียน 6.3–6.4</text>
  <text x="360" y="86" font-size="11" fill="#777" text-anchor="middle">action pipeline</text>
  <circle cx="570" cy="60" r="11" fill="#ef6c00"/>
  <text x="570" y="38" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">บทเรียน 6.5–6.6 (วันนี้)</text>
  <text x="570" y="86" font-size="11" fill="#777" text-anchor="middle">fusion + IoT</text>
  <circle cx="720" cy="60" r="9" fill="#6a1b9a"/>
  <text x="720" y="40" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">บทเรียน 7.1–7.2+</text>
  <text x="720" y="86" font-size="11" fill="#777" text-anchor="middle">ใต้ฝากระโปรง</text>
</svg>
</div>

- **บทเรียน 6.1–6.4** ให้เรา "อ่าน verdict แล้วสั่งการบนบอร์ด" — action จบในกล่องเดียว
- **บทเรียน 6.5–6.6** ต่อยอด: การตัดสินใจ **ผ่านการยืนยันด้วยเซนเซอร์ที่สอง** (fusion) แล้ว **ส่งออกนอกบอร์ด** (IoT) — บอร์ดกลายเป็นโหนดในระบบที่ใหญ่ขึ้น
- จบชุดบทเรียนนี้ โมดูล 6 (Apps) ครบ แล้วบทเรียน 7.1–7.2 เราจะมุดลงไปดูสแตก Edge AI จริงๆ (tri-core, ai_engine, IPC)

> "กลับด้าน" ยังทำงานเหมือนเดิม: เห็นแอปหลายเซนเซอร์สำเร็จก่อน ([`10_motion_alarm.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py)) แล้วย้อนเข้าใจ จนต่อยอดเป็นระบบ IoT ของเราเองได้

---

# ทบทวนเร็ว — verdict + action จากชุดบทเรียนก่อนหน้า

ก่อนเติม fusion เรียกของเดิมกลับมาในหัวก่อน ชุดบทเรียนนี้ยืนบน pattern เดิมเป๊ะ แค่เพิ่มสองชั้นบนสุด:

| แนวคิด | มาจากบทเรียน | ชุดบทเรียนนี้ใช้ยังไง |
|---|---|---|
| `edge_ai.select()` / `result()` | 1, 3, 15 | เลือกโมเดล + อ่าน verdict (เหมือนเดิม) |
| `label` + `conf >= CONF_FLOOR` | 3, 16 | เงื่อนไข "โมเดลมั่นใจพอ" (ชั้นแรกของ fusion) |
| edge-trigger (`fired`) | 3, 16 | ยิงเหตุการณ์ครั้งเดียวต่อการเจอ (ไม่ spam broker) |
| `sensors.bmi270.motion()` | 4, 7 | อ่านเซนเซอร์ดิบ (ชั้นที่สองของ fusion) |

ชุดบทเรียนนี้เพิ่มสองแนวคิดใหม่บนฐานนี้: **การรวม verdict กับเซนเซอร์ดิบ** (fusion) และ **การส่งเหตุการณ์ออกทางเน็ต** (`wifi` + `mqtt`)

> ถ้ายังไม่แม่นเรื่อง verdict → action เปิด [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py) อ่านทวนก่อน — ชุดบทเรียนนี้ต่อจากตรงนั้นพอดี

---

# รันของจริงก่อน — แอปกันขโมย 3 เซนเซอร์

ก่อนแกะโค้ด รันแอปอ้างอิงให้เห็นการรวมสัญญาณด้วยตาก่อน (ทำได้บน Emulator และ PSoC Edge AI Kit ส่วนบน TESAIoT Dev Kit ตัวอย่างนี้ยังเปิดไมโครโฟน PDM ไม่ได้ ดูหมายเหตุหัวไฟล์):

1. เปิด **ide.tesaiot.dev** หรือ BENTO IDE เสียบบอร์ด
2. รัน [`10_motion_alarm.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py) — ระบบเฝ้าระวัง 3 เซนเซอร์
3. กดสวิตช์ **Arm** แล้วลอง: ยื่นมือเข้าเรดาร์ · เขย่าบอร์ด · ส่งเสียงดัง
4. สังเกต: มัน **ไม่ได้ปลุกทุกครั้งที่เซนเซอร์ตัวเดียวไหว** — ต้อง "โหวต 2 ใน 3" ถึงจะขึ้น `!! INTRUDER !!`
5. ลองทำให้เซนเซอร์ตัวเดียวไหว (แค่เขย่าเบาๆ) ดูว่ามัน **ไม่ยอมปลุก** — นั่นแหละคือ fusion

> จับความรู้สึกนี้ไว้: "เซนเซอร์ตัวเดียวไม่พอ ต้องให้หลายตัวเห็นตรงกันก่อนถึงจะเชื่อ" — ชุดบทเรียนนี้เราจะเอาหลักเดียวกันมาใช้กับ **verdict ของโมเดล + เซนเซอร์ดิบ**

---

# ปัญหาของโมเดลเดี่ยว — false positive

โมเดลไม่ได้ถูกเสมอ บางท่า/บางเสียงมันก็ "เดา" คลาสผิดด้วยความมั่นใจพอสมควร ถ้าเราสั่งการทุกครั้งที่ verdict เข้าเงื่อนไข action จะยิงพลาดบ่อย

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <rect x="14" y="20" width="400" height="130" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="214" y="46" font-size="14" font-weight="700" fill="#e65100" text-anchor="middle">โมเดลเดี่ยว (บทเรียน 6.3–6.4)</text>
  <text x="214" y="72" font-size="12" fill="#555" text-anchor="middle">verdict "shaking" 62% → ยิง action</text>
  <text x="214" y="94" font-size="12" fill="#c62828" text-anchor="middle">แต่จริงๆ แค่วางบอร์ดแรงไปหน่อย</text>
  <text x="214" y="120" font-size="11" fill="#888" text-anchor="middle">false positive → ปลุกพร่ำเพรื่อ</text>
  <rect x="446" y="20" width="400" height="130" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="646" y="46" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">fusion (ชุดบทเรียนนี้)</text>
  <text x="646" y="72" font-size="12" fill="#555" text-anchor="middle">verdict "shaking" 62%</text>
  <text x="646" y="94" font-size="12" fill="#555" text-anchor="middle">AND gyro ดิบ &gt; เกณฑ์ → ค่อยยิง</text>
  <text x="646" y="120" font-size="11" fill="#888" text-anchor="middle">สองสัญญาณเห็นตรงกัน → เชื่อได้</text>
</svg>
</div>

- โมเดลให้ **ป้ายคลาส + ความน่าจะเป็น** แต่มันไม่รู้ "แรงจริงแค่ไหน" ในหน่วยฟิสิกส์
- เซนเซอร์ดิบให้ **ตัวเลขจริง** (เช่น gyro องศา/วินาที) ที่โมเดลไม่เห็นตรงๆ
- เอาสองอย่างมา **ยืนยันซึ่งกันและกัน** = ตัดสินใจที่ทนต่อ false positive มากขึ้น

> นี่คือเหตุผลที่ระบบจริงไม่ค่อยเชื่อเซนเซอร์ตัวเดียว — รถยนต์ใช้ทั้งกล้อง+เรดาร์+lidar ก่อนเบรก เพราะแต่ละตัวพลาดคนละแบบ เอามารวมกันจึงน่าเชื่อถือ

---

# Sensor fusion คืออะไร

**Sensor fusion** = รวมข้อมูลจากหลายแหล่งเข้าเป็นการตัดสินใจเดียวที่ดีกว่าใช้แหล่งเดียว ชุดบทเรียนนี้เราทำแบบง่ายที่สุดแต่ทรงพลัง: **model verdict + raw sensor gate**

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arFus" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="30" width="230" height="54" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="135" y="54" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">verdict ของโมเดล</text>
  <text x="135" y="74" font-size="11" fill="#666" text-anchor="middle">label + conf (NPU/M55)</text>
  <rect x="20" y="100" width="230" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="135" y="124" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">เซนเซอร์ดิบ</text>
  <text x="135" y="144" font-size="11" fill="#666" text-anchor="middle">gyro energy (M33)</text>
  <polygon points="360,60 430,32 500,60 430,88" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="430" y="58" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">รวม (AND)</text>
  <text x="430" y="74" font-size="10" fill="#666" text-anchor="middle">เห็นตรงกัน?</text>
  <rect x="600" y="42" width="270" height="64" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="735" y="70" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">fused decision</text>
  <text x="735" y="90" font-size="11" fill="#666" text-anchor="middle">เชื่อถือได้ → ยิงเหตุการณ์</text>
  <line x1="250" y1="57" x2="358" y2="57" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arFus)"/>
  <line x1="250" y1="127" x2="430" y2="90" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arFus)"/>
  <line x1="500" y1="60" x2="598" y2="72" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arFus)"/>
</svg>
</div>

- **โมเดล** เก่งเรื่อง "รู้จำรูปแบบ" (นี่คือท่าเขย่าไหม) แต่ไม่รู้ค่าฟิสิกส์
- **เซนเซอร์ดิบ** เก่งเรื่อง "ค่าจริง" (แรงกี่องศา/วินาที) แต่ไม่รู้ว่ามันเป็นรูปแบบอะไร
- fusion = เอาจุดแข็งสองอย่างมาค้ำกัน — action ยิงเมื่อ **ทั้งคู่** เห็นตรงกันเท่านั้น

> เราเลือก fusion แบบ AND ในชุดบทเรียนนี้เพราะเข้าใจง่ายและกัน false positive ได้ทันที ในงานจริงมี fusion ที่ซับซ้อนกว่านี้ (ถ่วงน้ำหนัก · Kalman) แต่หลักคิดเริ่มจากตรงนี้

---

# สอง "รส" ของ fusion ที่ใช้บ่อย

fusion ในชุดบทเรียนนี้ (verdict + raw gate) เป็นแบบ **corroboration** แต่รู้ไว้ว่ามีอีกแบบที่แอปอ้างอิงใช้ ([`10_motion_alarm.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py)):

<div style="text-align:center;margin:6px 0">
<svg width="880" height="170" viewBox="0 0 880 170" font-family="DejaVu Sans, sans-serif">
  <rect x="14" y="16" width="420" height="140" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="224" y="42" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">corroboration gate (ชุดบทเรียนนี้)</text>
  <text x="224" y="68" font-size="12" fill="#555" text-anchor="middle">สัญญาณหลัก 1 ตัว (verdict โมเดล)</text>
  <text x="224" y="90" font-size="12" fill="#555" text-anchor="middle">+ ประตูยืนยัน 1 ตัว (raw gyro)</text>
  <text x="224" y="116" font-size="11" fill="#888" text-anchor="middle">ยิงเมื่อทั้งคู่ผ่าน (AND)</text>
  <text x="224" y="136" font-size="11" fill="#888" text-anchor="middle">โฟกัส: กัน false positive</text>
  <rect x="446" y="16" width="420" height="140" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="656" y="42" font-size="14" font-weight="700" fill="#1565c0" text-anchor="middle">majority vote (10_motion_alarm)</text>
  <text x="656" y="68" font-size="12" fill="#555" text-anchor="middle">3 เซนเซอร์ดิบ (radar/imu/mic)</text>
  <text x="656" y="90" font-size="12" fill="#555" text-anchor="middle">โหวต ≥ 2 ใน 3 → ปลุก</text>
  <text x="656" y="116" font-size="11" fill="#888" text-anchor="middle">ยอมให้เซนเซอร์ตัวหนึ่งพลาดได้</text>
  <text x="656" y="136" font-size="11" fill="#888" text-anchor="middle">โฟกัส: ทนต่อเซนเซอร์เสีย</text>
</svg>
</div>

- **corroboration (AND)** — เข้มงวด: ต้องผ่านทุกด่าน เหมาะกับ "อย่าปลุกถ้าไม่ชัวร์"
- **majority vote (≥k of n)** — ยืดหยุ่น: ยอมให้ตัวหนึ่งพลาด เหมาะกับ "อย่าพลาดของจริงแม้เซนเซอร์ตัวหนึ่งเสีย"
- ฉบับเต็มของเรา (`examples/`) จะให้ลองสลับ raw gate เป็น `sensors.radar()` เพื่อชิมรสของ multi-modal ด้วย

> ไม่มีแบบไหน "ถูกกว่า" — เลือกตามความเสี่ยง งานปลุกภัยเลือก vote (พลาดไม่ได้) งานสั่งการอัตโนมัติเลือก AND (ยิงพลาดแล้วกวนใจ)

---

# คณิตของ fusion (1) — โหวต k จาก n

การ "โหวต 2 ใน 3" ที่เห็นตอนรัน [`10_motion_alarm.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py) เขียนเป็นสูตรสั้นๆ ได้แบบนี้ — ไม่ต้องกลัว เดี๋ยวเราค่อยๆ แกะทีละตัว:

$$\text{fire} \;=\; \Big[\; \sum_{i=1}^{n} s_i \;\ge\; k \;\Big]$$

อ่านสัญลักษณ์ทีละตัว (ภาษาคนธรรมดา):

- $n$ = จำนวนเซนเซอร์ทั้งหมด — แอปกันขโมยมี radar · imu · mic จึง $n=3$
- $s_i$ = ผลของเซนเซอร์ตัวที่ $i$ เป็นเลขฐานสอง: $s_i=1$ ถ้า "เห็นสัญญาณ", $s_i=0$ ถ้า "เงียบ"
- $\sum_{i=1}^{n} s_i$ = นับว่ามีกี่ตัวที่เห็นตรงกัน (บวก 1 ทุกตัวที่ไหว)
- $k$ = เกณฑ์เสียงข้างมากที่เราตั้ง — ชุดบทเรียนนี้ $k=2$ จึงกลายเป็น "2 ใน 3"
- $[\,\cdot\,]$ = วงเล็บ Iverson: เงื่อนไขจริงคืนค่า $1$ (ปลุก), เท็จคืนค่า $0$ (เงียบ)

ทำไมสำคัญกับชุดบทเรียนนี้: ตั้ง $k=2,\, n=3$ คือ majority vote ที่ทน "เซนเซอร์ตัวหนึ่งพลาด" ได้ ($1$ ตัวเงียบยัง fire ได้) — ตรงกับความรู้สึกตอนเขย่าเบาๆ แล้วมัน "ไม่ยอมปลุก"

> จำภาพนี้ไว้: ยิ่ง $k$ ใกล้ $n$ ยิ่งเข้มงวด (ต้องเห็นตรงกันหลายตัว) — พอ $k=n$ เมื่อไร มันก็กลายเป็น AND ที่เราใช้ในชุดบทเรียนนี้พอดี

---

# คณิตของ fusion (2) — ถ่วงน้ำหนัก + AND

บางเซนเซอร์เชื่อได้มากกว่าตัวอื่น เราจึงให้ "น้ำหนัก" $w_i$ ต่างกันได้ แล้วรวมเป็นคะแนนเดียว:

$$S \;=\; \sum_{i=1}^{n} w_i\, s_i \qquad\qquad \text{fire} \;=\; \big[\; S \ge \theta \;\big]$$

- $w_i$ = น้ำหนักความเชื่อถือของเซนเซอร์ตัวที่ $i$ — ยิ่งไว้ใจ ยิ่งให้มาก
- $S$ = คะแนนรวมแบบถ่วงน้ำหนัก (เซนเซอร์สำคัญออกเสียงดังกว่า)
- $\theta$ = เกณฑ์ (threshold) ที่คะแนนรวมต้องข้ามถึงจะ fire

corroboration gate (AND) ที่เราเขียนชุดบทเรียนนี้เป็น **กรณีพิเศษ** ของสูตรข้างบน — มีแค่สองสัญญาณ ($n=2$: verdict กับ raw gyro), ให้ $w_i=1$ เท่ากัน, แล้วตั้ง $\theta = n$:

$$\text{AND} \;\equiv\; \big(k = n\big) \;\equiv\; \Big(\theta = \sum_{i=1}^{n} w_i\Big)$$

- ตั้ง $\theta$ เท่าผลรวมน้ำหนัก → ต้องผ่าน **ทุกตัว** ถึง fire = นั่นคือ `model_hit and raw_ok`
- ลด $\theta$ ลง → ผ่อนเป็นโหวตเสียงข้างมาก · เพิ่ม $w_i$ ของ raw gyro → ให้เซนเซอร์ดิบมีสิทธิ์ยับยั้งแรงขึ้น

> เห็นไหมว่าทั้ง vote, AND และ weighted เป็นสูตรเดียวกัน ต่างกันแค่ค่า $k$, $w_i$, $\theta$ — โค้ด `fused = model_hit and raw_ok` ในชุดบทเรียนนี้คือมุมที่เข้มงวดที่สุดของสูตรนี้

---

# verdict (what) + raw sensor (how strong)

หัวใจของ fusion ชุดบทเรียนนี้: โมเดลกับเซนเซอร์ดิบ **ตอบคนละคำถาม** — เอามาประกบกันจึงได้ภาพครบ

| | โมเดล (`edge_ai`) | เซนเซอร์ดิบ (`sensors`) |
|---|---|---|
| ตอบอะไร | "นี่คือท่าอะไร" (label) | "แรงเท่าไรจริงๆ" (ตัวเลข) |
| หน่วย | ความน่าจะเป็น 0..1 (`conf`) | ฟิสิกส์ (องศา/วินาที, dBFS, เมตร) |
| รันที่ไหน | CM55 + NPU | CM33 (Python ของเรา) |
| จุดอ่อน | เดาผิดได้ (false positive) | ไม่รู้ว่ารูปแบบคืออะไร |

- โมเดลอาจตอบ `shaking` ตอนที่คุณแค่ยกบอร์ดเร็วๆ — `conf` อาจสูงพอผ่าน `CONF_FLOOR` ด้วยซ้ำ
- แต่ถ้าเราเช็ก gyro ดิบด้วย จะเห็นว่าตอนยกเบาๆ ค่ามันไม่ถึงเกณฑ์จริง → fusion บอกว่า "ยังไม่ใช่"

> จำประโยคนี้ไว้: **โมเดลบอก "อะไร" เซนเซอร์ดิบบอก "แค่ไหน"** — เอาสองมิตินี้มา AND กัน คือ fusion ที่ง่ายที่สุดและได้ผลจริง

---

# gate ด้วย raw feature — ทบทวน บทเรียน 3.3–3.4

ประตูยืนยัน (`gmag > MOTION_FLOOR`) คือ **rule classifier** ที่เราทำเป็นแล้วในบทเรียน 3.3–3.4 เราแค่เอามันมาต่อท้าย verdict ของโมเดล

```python
# ฟีเจอร์ดิบจาก IMU (เหมือนบทเรียน 2.1–2.2 + 3.3–3.4): พลังงานการหมุนรวม 3 แกน
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
gmag = abs(gx) + abs(gy) + abs(gz)     # องศา/วินาที รวม — ยิ่งสูง ยิ่งหมุนแรง

raw_ok = gmag > MOTION_FLOOR           # ประตูฟิสิกส์ (rule จากบทเรียน 3.3–3.4)
```

- `gmag` คือฟีเจอร์แบบเดียวกับที่ [`10_motion_alarm.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py) ใช้ (`abs(gx)+abs(gy)+abs(gz)` เทียบ baseline)
- นี่คือ "การประมวลผลสัญญาณ" ขั้นต้น (Processing/Analysis ในวงจร 5 ขั้น) เอามาค้ำ verdict
- `MOTION_FLOOR` เป็นค่าคงที่บนหัวไฟล์ — remix ได้: ตั้งสูง = เข้มงวด, ตั้งต่ำ = ไวขึ้น

> fusion ไม่ใช่เวทมนตร์ — มันคือ "โมเดล (บทเรียน 1.6–1.7) + rule เซนเซอร์ (บทเรียน 3.3–3.4)" ที่คุณทำเป็นทั้งคู่แล้ว เอามาต่อกัน ชุดบทเรียนนี้แค่ประกอบร่าง

---

# โครง 4 จังหวะของแอปชุดบทเรียนนี้

แอปชุดบทเรียนนี้ต่อจากโครง 3 จังหวะของบทเรียน 1.6–1.7 (select → result → action) แล้วแทรก **fuse** เข้าไปกลาง แล้วขยาย action เป็น **publish**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="180" viewBox="0 0 920 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arAnat17" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="16" y="56" width="200" height="82" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="116" y="88" font-size="15" font-weight="700" fill="#1565c0">1 · select</text>
    <text x="116" y="110" font-size="11" fill="#555">find_model → select()</text>
    <text x="116" y="126" font-size="10" fill="#888">+ ต่อ WiFi/MQTT</text>
    <rect x="240" y="56" width="200" height="82" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="340" y="88" font-size="15" font-weight="700" fill="#e65100">2 · result</text>
    <text x="340" y="110" font-size="11" fill="#555">verdict + วาดจอ</text>
    <text x="340" y="126" font-size="10" fill="#888">label · conf</text>
    <rect x="464" y="56" width="200" height="82" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="564" y="82" font-size="15" font-weight="700" fill="#2e7d32">3 · fuse</text>
    <text x="564" y="104" font-size="11" fill="#555">verdict AND raw gate</text>
    <text x="564" y="122" font-size="10" fill="#888">gyro ดิบ ← ของใหม่</text>
    <rect x="688" y="56" width="216" height="82" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="796" y="82" font-size="15" font-weight="700" fill="#6a1b9a">4 · publish</text>
    <text x="796" y="104" font-size="11" fill="#555">mqtt.publish(event)</text>
    <text x="796" y="122" font-size="10" fill="#888">ขึ้นคลาวด์ ← ของใหม่</text>
  </g>
  <line x1="216" y1="97" x2="238" y2="97" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAnat17)"/>
  <line x1="440" y1="97" x2="462" y2="97" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAnat17)"/>
  <line x1="664" y1="97" x2="686" y2="97" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAnat17)"/>
  <text x="460" y="28" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">เลือก ──▶ อ่าน ──▶ รวมสัญญาณ ──▶ ส่งออก</text>
  <text x="460" y="164" font-size="11" fill="#888" text-anchor="middle">จังหวะ 1–2 = ของเดิม · จังหวะ 3 (fuse) + 4 (publish) = หัวใจใหม่ของชุดบทเรียนนี้</text>
</svg>
</div>

> จังหวะ 3 กับ 4 คือสิ่งที่ทำให้แอปชุดบทเรียนนี้ต่างจากบทเรียน 6.3–6.4 — เดิม action จบบนบอร์ด คราวนี้ action **ผ่านการยืนยัน** แล้ว **เดินทางออกไปหาคลาวด์**

---

# อ่านเซนเซอร์ดิบ — sensors.bmi270.motion()

จังหวะ fuse เริ่มที่อ่านสัญญาณดิบมาประกบ verdict `sensors.bmi270.motion()` คืน 6 ค่าในครั้งเดียว:

```python
import sensors
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
# ax,ay,az = ความเร่ง 3 แกน (m/s²) · gx,gy,gz = อัตราหมุน 3 แกน (°/s)
gmag = abs(gx) + abs(gy) + abs(gz)      # พลังงานการหมุนรวม
```

- `motion()` เป็นการอ่าน **ดิบ** บน CM33 — ไม่ผ่าน NPU ไม่ผ่านโมเดล เป็นตัวเลขฟิสิกส์ตรงๆ
- เราเลือกใช้ gyro (`gx,gy,gz`) เพราะ "เขย่า/หมุน" เห็นชัดที่อัตราหมุน — ตรงกับโมเดล Motion
- อยากใช้เซนเซอร์อื่นเป็น gate ก็ได้: `sensors.radar()["presence"]` (มีคนไหม) เป็น gate แบบ multi-modal

> เซนเซอร์ตัวเดียวกับที่ป้อนโมเดล (IMU) แต่เราอ่าน **คนละเส้นทาง**: โมเดลเห็นหน้าต่างสัญญาณผ่าน NPU ส่วนเราอ่านค่าปัจจุบันดิบๆ — สองมุมมองของสัญญาณเดียวกัน

---

# เงื่อนไข fused — สองด่านต้องผ่านทั้งคู่

การตัดสินใจแบบ fused = verdict ของโมเดลผ่าน **และ** เซนเซอร์ดิบผ่าน ทั้งสองด่านต้องจริงพร้อมกัน:

```python
model_hit = (r['label'] == TARGET_CLASS            # 1) ใช่คลาสเป้าหมาย
             and r['conf'] >= edge_ai.CONF_FLOOR)  #    + โมเดลมั่นใจพอ
raw_ok    = gmag > MOTION_FLOOR                     # 2) เซนเซอร์ดิบแรงพอจริง

fused = model_hit and raw_ok                        # AND — ต้องผ่านทั้งคู่
```

- ด่านแรก (`model_hit`) คือของเดิมจากบทเรียน 1.6–1.7 / 6.3–6.4 — โมเดลตอบถูกคลาส + มั่นใจถึงเกณฑ์
- ด่านสอง (`raw_ok`) คือของใหม่ — ค่าฟิสิกส์ยืนยันว่า "แรงจริง" ไม่ใช่โมเดลเดาเอา
- `and` ทำให้ false positive ของโมเดลถูกกรองออก ถ้าเซนเซอร์ดิบไม่เห็นด้วย

> ลองคิดกลับกัน: ถ้าคุณ **เขย่าแรงมาก** แต่โมเดลบังเอิญตอบ `idle` — `fused` ก็ยังเป็น `False` เพราะ `model_hit` ไม่ผ่าน สอง

---

# edge-trigger — ยิงเหตุการณ์ครั้งเดียว

เหมือนบทเรียน 6.3–6.4 เราไม่อยากส่ง MQTT รัวทุกเฟรมที่ยัง fused อยู่ — ใช้ธง `fired` ยิง "ตอนขอบขาขึ้น" ครั้งเดียว

```python
if fused and not fired:        # เพิ่งเข้าเงื่อนไข fused → ส่งครั้งเดียว
    publish_event(r['conf'], gmag)
    fired = True
elif not fused:                # ออกจากเงื่อนไขแล้ว → รีเซ็ต
    fired = False
```

- ยิ่งสำคัญกับ IoT: broker สาธารณะและ bandwidth มีจำกัด — spam ทุกเฟรม = โดน rate-limit / เปลืองพลังงาน
- `fired` ตั้ง `True` ตอนส่ง เคลียร์ `False` ตอนหลุดเงื่อนไข → หนึ่งเหตุการณ์ = หนึ่งข้อความ MQTT

> pattern เดียวกับปุ่มกด (บทเรียน 1.6–1.7) และ debounce (บทเรียน 6.3–6.4) — เหตุการณ์ที่ส่งออกนอกบอร์ดยิ่งต้องคุมจังหวะ เพราะปลายทางคือระบบที่เราไม่ได้คุมคนเดียว
