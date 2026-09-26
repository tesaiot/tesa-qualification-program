---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ"
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

# บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ

## Processing II · เมตริกอนุพัทธ์ + การจำแนกด้วยกฎ (ก่อนถึง ML)

**โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์**

> ต่อจากบทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ

---

# โครงร่วมของทุกโปรแกรม MicroPython

ก่อนดูไฟล์จริง จับ "โครง" เดิมที่เราเจอมาตั้งแต่ บทเรียน 1.1–1.3 ให้ได้ก่อน — โปรแกรม BENTO เกือบทุกตัวเดินตามสี่จังหวะนี้:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="130" viewBox="0 0 880 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">ui · lcd · sensors · dsp</text>
  <rect x="238" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">การ์ด + classify()</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">อ่าน→แปลง→ตัดสิน→วาด</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่มออก</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> จังหวะ 3 (ลูป) ของชุดบทเรียนนี้คือ **"อ่านค่าดิบ → แปลงเป็น derived → ตัดสินด้วยกฎ → วาดคลาส"** จำสี่ก้าวในลูปนี้ไว้ เดี๋ยวเราไล่โค้ดทีละก้าว

---

# โครงของไฟล์ s07_rule_classifier.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"อ่าน temp+humidity → คำนวณ dew/heat → เอาเข้าบันไดกฎ → เอาคลาสที่ชนะขึ้นจอพร้อมสี → เทียบกับกฎสำเร็จรูป"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="180" viewBox="0 0 920 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS7" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="60" width="150" height="60" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="89" y="86" font-weight="700" fill="#455a64">อ่านค่าดิบ</text>
    <text x="89" y="104" font-size="10" fill="#999">dps368 · sht40</text>
    <rect x="194" y="60" width="160" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="274" y="80" font-weight="700" fill="#1565c0">แปลง derived</text>
    <text x="274" y="98" font-size="10" fill="#999">dew_point :รอบลูป</text>
    <text x="274" y="112" font-size="10" fill="#999">heat_index (เติม 1,2)</text>
    <rect x="384" y="60" width="160" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="464" y="86" font-weight="700" fill="#e65100">classify()</text>
    <text x="464" y="104" font-size="10" fill="#999">บันไดกฎ (เติม 3)</text>
    <rect x="574" y="60" width="160" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="654" y="80" font-weight="700" fill="#2e7d32">คลาส + สี</text>
    <text x="654" y="98" font-size="10" fill="#999">verdict.text (เติม 4)</text>
    <text x="654" y="112" font-size="10" fill="#999">verdict.color</text>
    <rect x="764" y="60" width="142" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="835" y="86" font-weight="700" fill="#6a1b9a">เทียบกฎ</text>
    <text x="835" y="104" font-size="10" fill="#999">dsp.comfort_zone</text>
  </g>
  <line x1="164" y1="90" x2="192" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS7)"/>
  <line x1="354" y1="90" x2="382" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS7)"/>
  <line x1="544" y1="90" x2="572" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS7)"/>
  <line x1="734" y1="90" x2="762" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS7)"/>
  <text x="460" y="150" font-size="11" fill="#888" text-anchor="middle">ช่องเติม 4 จุด = ก้าวแปลง + ก้าวตัดสิน + ก้าววาด — หัวใจของ classifier</text>
</svg>
</div>

> ตัวเลข "เติม 1..4" ชี้ไปที่ `# เติม:` ในไฟล์ฝึก จำโครงนี้ไว้ เดี๋ยวไล่ดูทีละช่อง

---

# ไล่โค้ด (1) — อ่านค่าดิบ + คำนวณ derived

**ช่องเติมที่ 1 และ 2**: ต้นลูป อ่านเซนเซอร์แล้วแปลงเป็นค่าอนุพัทธ์ที่กฎจะใช้:

```python
while True:
    p, t = sensors.dps368.pressure_temperature()   # ความดัน + อุณหภูมิ (ให้ไว้แล้ว)
    h = sensors.sht40.humidity()                    # ความชื้น %RH (ให้ไว้แล้ว)

    # เติม: dp = dsp.dew_point(t, h)      # จุดน้ำค้าง
    dp = 0.0
    pass
    # เติม: hi = dsp.heat_index(t, h)     # "รู้สึกเหมือน" กี่องศา
    hi = t
    pass
```

- ช่อง 1: แทน `pass` ด้วย `dp = dsp.dew_point(t, h)` · ช่อง 2: แทนด้วย `hi = dsp.heat_index(t, h)`
- ค่าตั้งต้น `dp = 0.0` / `hi = t` กันโปรแกรมพังตอนยังเติมไม่ครบ พอเติมแล้วบรรทัดจริงจะทับค่าตั้งต้น
- `dp` เอาไปโชว์บนการ์ด · `hi` เอาไปป้อนบันไดกฎ (คลาส hot/danger ตัดสินจาก `hi`)

> ทำไม `humidity()` คืนค่าตัวเดียว (float) ไม่ใช่ tuple? เพราะมันคืน %RH อย่างเดียว ส่วนอุณหภูมิเราเอามาจาก DPS368 แล้ว — ลองเรียก `sensors.sht40.humidity()` ใน REPL ดูได้

---

# ไล่โค้ด (2) — เขียนบันไดกฎ classify()

**ช่องเติมที่ 3** (หัวใจของชุดบทเรียน): เติมบันไดกฎในฟังก์ชัน `classify()`:

```python
def classify(t, h, hi):
    # เติม: เขียนบันไดเงื่อนไข ไล่จาก "อันตรายสุด" ลงมา แล้ว return ชื่อคลาส (str)
    #   if hi >= 41: return "danger"
    #   if hi >= 32: return "hot"
    #   if h  >= 70: return "humid"
    #   if t  <  20: return "cold"
    #   if h  <  30: return "dry"
    #   return "comfortable"
    pass
```

- แทน `pass` ด้วยบันไดทั้งชุด — ลำดับต้องไล่จากรุนแรง/เฉพาะ (danger) ลงไปกว้าง (comfortable)
- คลาสที่ return ต้องเป็นหนึ่งใน key ของ `COLORS` ไม่งั้นตอนระบายสีจะได้สีขาว (fallback)
- อยากปรับให้เป็น "กฎของคุณ" ก็เปลี่ยนเลขเส้นแบ่งได้เลย นี่คือ hyperparameter ของกฎ

> ถ้าลืมเติมช่องนี้: `classify()` คืน `None` → `verdict` โชว์ว่างเปล่า และ `COLORS.get(None)` ได้สีขาว นี่คืออาการที่บอกว่าบันไดยังไม่ทำงาน

---

# ไล่โค้ด (3) — เอาคลาสขึ้นจอ + ระบายสี

**ช่องเติมที่ 4**: เอาคลาสที่ classify คืนมา ขึ้นจอพร้อมสีประจำคลาส:

```python
zone = classify(t, h, hi)
# เติม: verdict.text(zone)
#       verdict.color(COLORS.get(zone, WHITE))
pass
```

- แทน `pass` ด้วยสองบรรทัด: `verdict.text(zone)` แล้ว `verdict.color(COLORS.get(zone, WHITE))`
- `COLORS.get(zone, WHITE)` = ถ้าคลาสอยู่ในแผนที่สี ใช้สีนั้น ถ้าไม่ (เช่นเติมบันไดพลาด) ใช้สีขาว
- นี่คือ **ชัยชนะที่เห็นได้**: ตัวหนังสือคำตัดสินเปลี่ยนคำ+เปลี่ยนสีตามอากาศจริง

> pattern "สร้าง widget ครั้งเดียว แล้วในลูปแค่ `.text()` / `.color()`" คือของเดิมจาก บทเรียน 1.1–1.3 — เราไม่สร้าง Seg7 ใหม่ทุกรอบ แค่เปลี่ยนข้อความกับสีของอันเดิม จอจะได้ไม่กระพริบ

---

# ไล่โค้ด (4) — เทียบกับกฎสำเร็จรูป

ท่อนสุดท้าย (ให้ไว้แล้ว) เอาคำตัดสินของเราไปเทียบกับ `dsp.comfort_zone` เพื่อ "ตรวจการบ้านตัวเอง":

```python
lab_builtin.text("dsp.comfort_zone: %s" % dsp.comfort_zone(t, h))
```

- ค่าอาจ **ไม่ตรงกัน** เพราะเราตั้งเส้นแบ่งคนละชุด (เราใช้ heat index, มันใช้อุณหภูมิดิบ; เลขเส้นก็ต่าง)
- ไม่ตรงกันไม่ได้แปลว่าผิด — แปลว่า "สองกฎนิยามความสบายต่างกัน" ซึ่งเป็นเรื่องปกติของกฎมือ
- ในฉบับเต็ม (`examples/`) เราเพิ่มไฟบอก `=` เมื่อตรงกัน `x` เมื่อต่างกัน ไว้สังเกตว่ากฎสองชุดเห็นพ้องกันบ่อยแค่ไหน

> จุดนี้คือประเด็นที่ควรคิดให้จบ: "เมื่อกฎสองชุดตัดสินต่างกันตรงไหน แล้วชุดไหนถูก?" คำตอบคือ **ไม่มีชุดไหน 'ถูก' โดยสมบูรณ์** — กฎขึ้นกับนิยามที่เราเลือก นี่คือข้อจำกัดที่ ML จะเข้ามาช่วยด้วยข้อมูลจริง

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้ (Emulator จำลองค่า temp/humidity ให้):

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิดไฟล์ [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py)
3. เติมช่องว่างทั้ง 4 จุดตามคำใบ้ `# เติม:`
4. กด **Run** — จะเห็นสามการ์ด (ค่าดิบ / derived / คำตัดสิน) + การ์ดคำตัดสินโชว์คลาสพร้อมสี
5. สังเกตว่าเมื่อค่าจำลองเปลี่ยน คลาสที่ชนะเปลี่ยนคำ+เปลี่ยนสีตาม

> Emulator ใช้ค่าจำลองแต่ `dsp.dew_point` / `heat_index` / `comfort_zone` คำนวณด้วยสูตรจริงเหมือนบอร์ด — เหมาะกับซ้อมตรรกะบันไดกฎที่บ้าน

---

# หน้าตา Emulator ที่เราจะใช้

<div style="text-align:center;margin:6px 0">

</div>

**BENTO Edge AI Emulator** คือจอ emulator ที่รันได้จริงในเบราว์เซอร์ ไม่ต้องมีบอร์ดก็เขียนโค้ดแล้วเห็นผลบนจอจำลองได้ทันที

- ซ้าย: หน้าต่างเขียนโค้ด MicroPython (เปิด [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py) ที่นี่)
- ขวา: จอจำลอง BENTO ที่จะโชว์การ์ดค่าดิบ / derived / คำตัดสินพร้อมสี เหมือนบอร์ดจริง
- ค่าจากเซนเซอร์เป็นค่าจำลอง แต่ `dsp.*` คำนวณด้วยสูตรฟิสิกส์จริง ตรรกะบันไดกฎจึงซ้อมได้เหมือนอยู่หน้าบอร์ด

> เปิดที่ **ide.tesaiot.dev** ได้เลย เครื่องใครก็รันได้ ไม่ต้องลงอะไร — เหมาะมากสำหรับกลับไปซ้อมต่อที่บ้าน

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง (AI Kit)

บนบอร์ดจริงใช้เซนเซอร์จริง DPS368 + SHT40 บน AI Kit:

1. เสียบบอร์ด AI Kit เข้าคอมด้วยสาย USB (ชุดบทเรียนนี้ต้องเป็น **AI Kit** เพราะ Eva Kit ไม่มี SHT40/DPS368)
2. เปิด [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py) ใน **BENTO IDE** กด **Program to Device**
3. **หายใจรดเซนเซอร์** → ความชื้นพุ่ง ดูคลาสขยับไป `humid`
4. **กำบอร์ดไว้ในมือสักครู่** → อุณหภูมิ+heat index ขึ้น ดูคลาสขยับไป `hot`
5. **เป่าลมเย็น / พาไปที่แอร์** → ดูคลาสกลับมา `comfortable` หรือ `cold`

> ค่าจากเซนเซอร์จริงจะสั่นเล็กน้อยตลอด ถ้าคลาสกระพริบคร่อมเส้นแบ่ง นั่นคือเหตุผลที่ฉบับเต็มใส่ **ฮิสเทอรีซิส** ไว้กันกระพริบ — เก็บไว้เป็นโจทย์ท้าทาย

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py) มี `pass` วางไว้ **4 จุด** ตรงที่ต้องเติมตรรกะจริง:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ต้นลูป | `dp = dsp.dew_point(t, h)` | dew point ค้างที่ 0.0 |
| 2 | ต้นลูป | `hi = dsp.heat_index(t, h)` | feels-like = temp ดิบ กฎ hot/danger เพี้ยน |
| 3 | ใน `classify()` | บันไดกฎ 6 ชั้น (danger→...→comfortable) | คลาสว่าง + สีขาว |
| 4 | หลัง classify | `verdict.text(zone)` + `verdict.color(...)` | คำตัดสินไม่ขึ้นจอ |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน `pass` (และค่าตั้งต้น) ด้วยโค้ดจริงตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. หายใจ/กำบอร์ด ดูคลาสเปลี่ยน ถ้าไม่ขึ้น กลับมาเช็ก indent กับลำดับชั้นในบันได

> สี่ช่องนี้คือ pipeline ย่อของ classifier ทั้งตัว: **แปลง (1,2) → ตัดสิน (3) → แสดง (4)** เติมครบเมื่อไร คุณมี classifier ตัวแรกที่เข้าใจทุกบรรทัด

---

# กฎมือ "อธิบายได้" — จุดแข็งที่ ML ยังตามยาก

จุดแข็งที่สุดของบันไดกฎคือ ทุกคำตัดสิน **สืบย้อนได้ว่าชั้นไหนยิงออกมา** ในฉบับเต็มเราให้ `classify()` คืนเหตุผลด้วย:

```python
def classify(t, h, hi):
    if hi >= HI_DANGER:
        return "danger", "feels-like %.0f >= %.0f" % (hi, HI_DANGER)
    ...
```

- จอโชว์ `why: feels-like 43 >= 41` — ผู้ใช้/วิศวกรเห็นเลยว่าทำไมถึงตัดสิน danger
- นี่คือ **explainability** ที่งานความปลอดภัย/การแพทย์ต้องการ: ตอบได้ว่า "ทำไม" ไม่ใช่แค่ "อะไร"
- ML ทั่วไปตอบ "ทำไม" ยากกว่ามาก (เป็นน้ำหนักในเครือข่าย) — เป็นเหตุผลจริงที่หลายระบบยังเลือกกฎ

> เวลาเลือกระหว่างกฎกับ ML อย่าถามแค่ "อันไหนแม่นกว่า" ถามด้วยว่า **"เราต้องอธิบายคำตัดสินได้ไหม"** — บางงานคำตอบข้อนี้สำคัญกว่าความแม่นเสียอีก

---

# ข้อจำกัดของกฎมือ — สะพานไปสู่ ML

กฎมือดีในหลายงาน แต่มันชนกำแพงเมื่อ pattern ซับซ้อนขึ้น — นี่คือเหตุผลที่คอร์สนี้พาไปต่อที่ Training:

- **กฎบาน** — จาก 2 ตัวแปร (t, h) ยังพอไล่ `if` ไหว แต่กับ 50 feature ของเสียง/การสั่น การเขียนกฎมือแทบเป็นไปไม่ได้
- **เส้นแบ่งมนุษย์ตั้งอาจไม่ดีที่สุด** — เราเดา 41, 32 จากมาตรฐาน แต่ข้อมูลจริงอาจบอกว่าเส้นที่ดีกว่าอยู่ตรงอื่น
- **ไม่ปรับตามข้อมูลใหม่** — อากาศบ้านคุณกับในตำราต่างกัน กฎมือไม่รู้ ต้องแก้เอง ML เรียนใหม่ได้

<div style="text-align:center;margin:6px 0">
<svg width="760" height="96" viewBox="0 0 760 96" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="48" x2="720" y2="48" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="130" cy="48" r="9" fill="#2e7d32"/>
  <text x="130" y="30" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">3.3–3.4 (วันนี้)</text>
  <text x="130" y="74" font-size="11" fill="#777" text-anchor="middle">กฎมือ 2 ตัวแปร</text>
  <circle cx="380" cy="48" r="9" fill="#ef6c00"/>
  <text x="380" y="30" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">4.5–4.6</text>
  <text x="380" y="74" font-size="11" fill="#777" text-anchor="middle">feature หลายมิติ</text>
  <circle cx="620" cy="48" r="9" fill="#6a1b9a"/>
  <text x="620" y="30" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">5.3–5.9</text>
  <text x="620" y="74" font-size="11" fill="#777" text-anchor="middle">ML เรียนเส้นแบ่งเอง</text>
</svg>
</div>

> วันนี้คุณจะได้ยินตัวเองพูดว่า "ถ้าเงื่อนไขเยอะกว่านี้ เขียน `if` ไม่ไหวแน่" — ความรู้สึกนั้นแหละคือ **แรงจูงใจที่แท้จริงของ ML** เก็บมันไว้ เดี๋ยวเราไปปลดล็อกกันที่ โมดูล 5 (Training)

---

# แหล่งเรียนรู้เพิ่มเติม

อยากต่อยอดเรื่อง derived metric และการจำแนกด้วยกฎ ลองตามลิงก์เหล่านี้ (เปิดดูได้ตามสะดวก):

**วิดีโอ (ช่องการศึกษาที่เชื่อถือได้)**
- Decision Trees อธิบายชัดเจน (บันไดเงื่อนไขแบบที่ ML เรียนเส้นแบ่งเอง) — ช่อง StatQuest: https://www.youtube.com/@statquest
- จาก if-then สู่การเรียนรู้ของเครื่อง (ภาพรวมการจำแนก) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- อัลกอริทึมและตรรกะเงื่อนไขในระบบจริง — ช่อง Computerphile: https://www.youtube.com/@Computerphile

**ภาพ / บทความอ้างอิง**
- จุดน้ำค้าง (Dew point) พร้อมสูตร Magnus: https://en.wikipedia.org/wiki/Dew_point (ที่มา: Wikipedia, CC BY-SA)
- ดัชนีความร้อน (Heat index) พร้อมตาราง NOAA: https://en.wikipedia.org/wiki/Heat_index (ที่มา: Wikipedia, CC BY-SA)
- ตารางดัชนีความร้อนของ NOAA (ภาพ): https://commons.wikimedia.org/wiki/Category:Heat_index (ที่มา: Wikimedia Commons, public domain — NOAA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · classifier ที่คุณเขียนเอง โชว์คำตัดสิน comfortable/hot/humid พร้อมสี ที่เปลี่ยนตามอากาศจริง
</div>
</div>

**MVP ของบทเรียน 3.3–3.4 (เกณฑ์ผ่านของชุดบทเรียน):** คุณเขียน `classify()` ด้วยบันไดกฎเอง แล้วบอร์ด/Emulator **โชว์คลาสที่เปลี่ยนตามจริง** เมื่อ temp/humidity เปลี่ยน (หายใจรด/กำบอร์ด)

- ใช้ **derived metric** อย่างน้อยหนึ่งตัว (`heat_index` หรือ `dew_point`) ในการตัดสิน
- อธิบายได้ว่าบันไดกฎ **ลำดับชั้นสำคัญยังไง** และคลาสไหนตัดสินจากค่าอะไร

> "ตัดสินได้" ไม่ใช่แค่ "เห็นตัวหนังสือเปลี่ยน" — คุณต้องชี้ได้ว่าคลาส `hot` มาจากเงื่อนไข `hi >= 32` และบอกได้ว่าทำไมใช้ `hi` ไม่ใช่ `t`

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุด + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py) มีโครงครบทั้งไฟล์ เหลือแค่ 4 จุดให้เติม (บันไดกฎยาวสุด)
- **เฉลย** — [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/solution/s07_rule_classifier.py) เติมครบพร้อมคอมเมนต์อธิบายทุกชั้น (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s07_rule_classifier_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/examples/s07_rule_classifier_full.py) เพิ่ม rule trace (`why`), เทียบกฎสำเร็จรูปพร้อมไฟตรง/ต่าง, และฮิสเทอรีซิสกันคลาสกระพริบ

> ลองเขียนบันไดกฎเองให้สุดก่อนนะ พลาดลำดับชั้นก็ไม่เป็นไร นั่นแหละคือจุดที่เราจะได้เรียนรู้เรื่อง dead branch ด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การเขียน classifier ด้วยกฎ ซ่อนแนวคิดที่จะใช้ยาวไปถึง โมดูล 5 (Training) และ Apps:

**ฝั่ง Edge AI / การจำแนก**
- **Classifier = ตัวเลข → คลาส** — รูปเดียวกับโมเดล ML ต่างที่ "ข้างใน"
- **Derived metric / feature** — แปลงค่าดิบให้ตัดสินง่ายขึ้น (dew point, heat index) = feature engineering
- **Threshold ladder** — เส้นแบ่งหลายชั้น ลำดับสำคัญ; ตั้งเส้นเอง = hyperparameter ของกฎ
- **Explainability** — กฎอธิบายคำตัดสินได้ทุกครั้ง (จุดแข็งเหนือ ML หลายงาน)

**ฝั่ง MicroPython / โครงโปรแกรม**
- **โครงร่วม** — import → สร้างครั้งเดียว → ลูป (อ่าน→แปลง→ตัดสิน→วาด) → `ui.poll`
- **สร้าง widget ครั้งเดียว** — ในลูปแค่ `.text()` / `.color()` จอไม่กระพริบ
- **ค่าคงที่รวมที่เดียว** — เส้นแบ่งเป็นตัวแปรชื่อชัด ปรับที่เดียวขยับทั้งกฎ (ไม่ฝัง magic number)

> ทั้งหมดนี้คือฐานของ ML: พอเข้าใจว่ากฎมือ "ตั้งเส้นแบ่งเอง" แล้ว คุณจะเข้าใจทันทีว่า ML คือการ "ให้เครื่องหาเส้นแบ่งจากข้อมูลแทนเรา" — คนละวิธี งานเดียวกัน

---

# ใช้จริงที่ไหน — กฎ threshold ในโลกจริง

classifier แบบกฎไม่ใช่ของเล่นในห้องเรียน มันคือหัวใจของอุปกรณ์ควบคุมนับล้านชิ้นที่ทำงานอยู่ตอนนี้:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">เทอร์โมสตัท / แอร์ / HVAC</text>
  <text x="28" y="56" font-size="11" fill="#555">if temp &gt; setpoint: เปิดคอมเพรสเซอร์</text>
  <text x="28" y="76" font-size="11" fill="#555">กฎ threshold ล้วน อธิบายได้ เชื่อถือได้</text>
  <text x="28" y="94" font-size="11" fill="#888">แบบเดียวกับบันไดกฎวันนี้</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">โรงเรือน / เกษตรแม่นยำ</text>
  <text x="464" y="56" font-size="11" fill="#555">dew point เตือนเชื้อรา · RH คุมพัดลม/พ่นหมอก</text>
  <text x="464" y="76" font-size="11" fill="#555">derived metric ตัดสินแทนค่าดิบ</text>
  <text x="464" y="94" font-size="11" fill="#888">dsp.dew_point/heat_index วันนี้</text>
  <rect x="12" y="112" width="420" height="88" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="136" font-size="13" font-weight="700" fill="#e65100">อาชีวอนามัย / โรงงาน</text>
  <text x="28" y="158" font-size="11" fill="#555">heat index เตือนเสี่ยงฮีตสโตรกคนงาน (WBGT)</text>
  <text x="28" y="178" font-size="11" fill="#555">เกณฑ์กฎหมายกำหนดเส้นแบ่งชัด -> กฎเหมาะกว่า ML</text>
  <text x="28" y="196" font-size="11" fill="#888">คลาส danger วันนี้</text>
  <rect x="448" y="112" width="420" height="88" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="136" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกับ ML — fusion</text>
  <text x="464" y="158" font-size="11" fill="#555">กฎ threshold + verdict ของโมเดล = ตัดสินที่ดีขึ้น</text>
  <text x="464" y="178" font-size="11" fill="#555">เช่น โมเดลว่า "cough" + กฎ RH สูง = เตือน</text>
  <text x="464" y="196" font-size="11" fill="#888">คือ โมดูล 6 (Apps, 6.5–6.6 sensor fusion)</text>
</svg>
</div>

> สังเกตข้อ 3: บางงาน **กฎหมายกำหนดเส้นแบ่งไว้แล้ว** (เช่นค่า WBGT เตือนความร้อน) งานพวกนี้ต้องใช้กฎ ไม่ใช่ ML เพราะต้องตรงตามเกณฑ์เป๊ะและอธิบายได้ — วิศวกรที่ดีเลือกเครื่องมือให้ตรงงาน

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s07_rule_classifier.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l04-rule-classifier-lab/practice/s07_rule_classifier.py) ให้ครบทั้ง 4 จุด รันได้จริง (Emulator หรือ AI Kit)
2. ทำให้เกิดคลาสอย่างน้อย **3 คลาสต่างกัน** (เช่น หายใจรด→`humid`, กำบอร์ด→`hot`, ปกติ→`comfortable`) แล้วจดว่าต้องทำอะไรถึงได้แต่ละคลาส
3. **ปรับเส้นแบ่งหนึ่งเส้น** (เช่น เปลี่ยน `hi >= 32` เป็น `>= 30`) แล้วอธิบายว่าคำตัดสินเปลี่ยนยังไง และทำไม

ใบ้ข้อ 3 — ลองหาค่าที่ "คร่อมเส้น" (เช่น heat index ~31–33) แล้วดูว่าเปลี่ยนเส้นแบ่งเล็กน้อยพลิกคำตัดสินได้จริง นี่คือสัมผัสแรกของ "การจูนเส้นแบ่ง" ที่ ML ทำอัตโนมัติในชุดบทเรียนหลัง

**วันนี้เราได้:** เข้าใจว่า classifier คืออะไร · แปลงค่าดิบเป็น derived metric (`dew_point`/`heat_index`) · เขียนบันไดกฎ threshold เอง · เห็นจุดแข็ง (อธิบายได้) และจุดอ่อน (กฎบาน) ของกฎมือ ที่ปูทางสู่ ML

> ชุดบทเรียนถัดไป (บทเรียน 4.1–4.2) เราเข้าสู่ **Pillar 3 · Analysis** — เริ่มจากตัวกรองสัญญาณ (EMA/median/Kalman) ทำสัญญาณสั่นๆ ให้เนียนขึ้นแบบเห็นกับตา เจอกันครับ
