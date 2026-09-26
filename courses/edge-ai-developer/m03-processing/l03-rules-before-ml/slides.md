---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ"
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

# บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ
## เมตริกอนุพัทธ์ + การจำแนกด้วยกฎ (ก่อนถึง ML)

**โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์**

**Pillar 2 · Processing — ก้าวที่สอง**

> คาถาประจำบทเรียน: **"ก่อนจะให้โมเดลเรียนเส้นแบ่งเอง เราลากเส้นแบ่งด้วยมือก่อน — classifier ตัวแรกของเราไม่ใช้ AI สักนิด"**

จากค่าดิบ → ค่าอนุพัทธ์ (dew point / heat index) → คำตัดสินเป็นคลาส

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันตัวจำแนกที่ทำงานได้จริงก่อน แล้วค่อยแกะว่ามันตัดสินใจยังไง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันกฎสำเร็จรูป</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">dsp.comfort_zone</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">มันตั้งเส้นแบ่งยังไง</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เขียนกฎเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">บันไดกฎ 4 ช่อง</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">อยากให้เรียนเอง</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">-> ML (โมดูล 5)</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เราใช้แนว **PRIMM** เหมือนเดิม (Predict–Run–Investigate–Modify–Make) วันนี้ "ของที่ทำงานได้" คือกฎจำแนกความสบายที่ firmware แถมมาให้ (`dsp.comfort_zone`) เรารันมันก่อน เห็นมันตอบ `comfortable / hot / humid` แล้วค่อยถามว่า "มันรู้ได้ยังไงว่าตอนนี้ร้อน?"

> ชุดบทเรียนนี้เราจะได้ classifier ตัวแรกของทั้งคอร์ส แต่มันยัง **ไม่ใช่ ML** เลย — เราเขียนเงื่อนไขทุกเส้นด้วยมือ พอเข้าใจของมือแล้ว ตอนขึ้น ML คุณจะเห็นชัดว่าโมเดต่างจากกฎมือตรงไหน

---

# เป้าหมายของชุดบทเรียนนี้

ต่อจาก บทเรียน 3.1–3.2 ที่เราแปลงสัญญาณดิบเป็นค่าฟิสิกส์ วันนี้เราเดินอีกก้าวในขั้น Processing:

1. **Classifier คืออะไร** — จากค่าตัวเลข ออกมาเป็น "คลาส" (ป้ายชื่อ) ได้ยังไง
2. **ค่าอนุพัทธ์ (derived metrics)** — `dsp.dew_point` และ `dsp.heat_index` แปลง temp+humidity เป็นข้อมูลที่ "ตัดสินง่ายขึ้น"
3. **ตรรกะเส้นแบ่ง (threshold logic)** — เส้นแบ่งเดียว → **บันไดกฎ (threshold ladder)** หลายชั้น
4. **กฎ vs ML** — ทำไมเรียกวันนี้ว่า "ก่อน ML" และกฎมือมีจุดแข็ง/จุดอ่อนอะไร
5. ลงมือ: เขียน `classify()` ของตัวเอง ให้จอโชว์คำตัดสิน `comfortable/hot/humid/...` พร้อมสี

ปลายทางของวันนี้: บอร์ดอ่านอุณหภูมิ+ความชื้นจริง แล้วโชว์คำตัดสินเป็นคลาสที่เปลี่ยนตามอากาศตรงหน้า

> วันนี้เน้น "ตัดสินใจด้วยกฎที่เราเข้าใจทุกบรรทัด" — ความเข้าใจนี้คือฐานที่ทำให้ ML ในบทเรียน 5.3–5.5 ไม่ใช่กล่องดำ

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

เรายังอยู่ที่ **ขั้น 2 · Processing** เหมือน บทเรียน 3.1–3.2 แต่ขยับจาก "แปลงค่า" มาเป็น "ตัดสินใจจากค่า"

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="60" width="160" height="72" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="90" y="88" font-size="14" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="90" y="108" font-size="11" fill="#555">เก็บข้อมูลดิบ</text>
    <text x="90" y="122" font-size="10" fill="#888">โมดูล 2</text>
    <rect x="196" y="52" width="160" height="88" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3.5"/>
    <text x="276" y="82" font-size="14" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="104" font-size="11" fill="#555">แปลงค่า + ตัดสินด้วยกฎ</text>
    <text x="276" y="122" font-size="11" fill="#2e7d32" font-weight="700">3.1–3.2 · 3.3–3.4 (วันนี้)</text>
    <rect x="382" y="60" width="160" height="72" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="462" y="88" font-size="14" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="462" y="108" font-size="11" fill="#555">DSP · FFT · feature</text>
    <text x="462" y="122" font-size="10" fill="#888">โมดูล 4</text>
    <rect x="568" y="60" width="160" height="72" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="648" y="88" font-size="14" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="648" y="108" font-size="11" fill="#555">ML เรียนเส้นแบ่งเอง</text>
    <text x="648" y="122" font-size="10" fill="#888">โมดูล 5</text>
    <rect x="754" y="60" width="160" height="72" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="834" y="88" font-size="14" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="108" font-size="11" fill="#555">อนุมาน + action</text>
    <text x="834" y="122" font-size="10" fill="#888">โมดูล 6</text>
  </g>
  <line x1="170" y1="96" x2="194" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="96" x2="380" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="96" x2="566" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="96" x2="752" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="176" font-size="12" fill="#888" text-anchor="middle">กฎมือวันนี้ (ขั้น 2) คือ "ตัวเทียบ" ที่จะให้ ML ในขั้น 4 มาเอาชนะ</text>
</svg>
</div>

> น่าสนใจตรงที่ **การจำแนก** ปรากฏได้สองที่: ที่นี่ (ขั้น 2) ทำด้วยกฎมือ และที่ขั้น 4 ทำด้วย ML ที่เรียนเอง งานเดียวกัน คนละวิธีหาเส้นแบ่ง — วันนี้เราทำแบบแรกให้เข้าใจทะลุก่อน

---

# Classifier คืออะไร

**Classifier** คือฟังก์ชันที่รับข้อมูลตัวเลขเข้าไป แล้วคายออกมาเป็น "คลาส" — ป้ายชื่อหนึ่งจากชุดที่กำหนดไว้

<div style="text-align:center;margin:8px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arCl" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="42" width="200" height="66" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="120" y="70" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">ตัวเลขเข้า</text>
  <text x="120" y="90" font-size="11" fill="#666" text-anchor="middle">temp=34, RH=75</text>
  <rect x="300" y="42" width="220" height="66" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="410" y="70" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">classifier</text>
  <text x="410" y="90" font-size="11" fill="#666" text-anchor="middle">กฎ (วันนี้) หรือ โมเดล (ภายหลัง)</text>
  <rect x="600" y="42" width="200" height="66" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="700" y="70" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">คลาสออก</text>
  <text x="700" y="90" font-size="11" fill="#666" text-anchor="middle">"hot"</text>
  <line x1="220" y1="75" x2="296" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCl)"/>
  <line x1="520" y1="75" x2="596" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCl)"/>
  <text x="410" y="128" font-size="11" fill="#999" text-anchor="middle">รูปร่างเข้า-ออก เหมือนกันทั้งกฎมือและ ML — ต่างกันแค่ "ข้างในตัดสินยังไง"</text>
</svg>
</div>

- คลาสของเราวันนี้: `comfortable / hot / humid / cold / dry / danger` — 6 ป้าย
- โมเดล DEEPCRAFT ในบทเรียน 1.1–1.3 ก็เป็น classifier (`idle/circle/shaking`) เพียงแต่ "ข้างใน" เป็น neural network
- เข้า-ออกเหมือนกันเป๊ะ นั่นคือเหตุผลที่กฎมือเป็นบันไดขั้นแรกสู่ ML ได้ดี

> จำรูปนี้ไว้: **ตัวเลข → กล่องตัดสิน → คลาส** ทั้งคอร์สจะเจอกล่องนี้ซ้ำ วันนี้เราเปิดกล่องแล้วเขียนข้างในด้วยมือเอง

---

# กฎ (rule-based) กับ ML — สองวิธีหาเส้นแบ่ง

งานจำแนกคือการ "ลากเส้นแบ่ง" ในพื้นที่ของค่า สองสำนักลากเส้นคนละวิธี:

<div style="text-align:center;margin:6px 0">
<svg width="820" height="210" viewBox="0 0 820 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="392" height="190" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="208" y="34" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">กฎมือ (วันนี้)</text>
  <text x="208" y="60" font-size="12" fill="#555" text-anchor="middle">เราตั้งเส้นแบ่งเองด้วยความรู้</text>
  <text x="208" y="80" font-size="12" fill="#555" text-anchor="middle">if hi &gt;= 32: return "hot"</text>
  <text x="208" y="110" font-size="12" fill="#2e7d32" text-anchor="middle">อธิบายได้ทุกคำตัดสิน</text>
  <text x="208" y="130" font-size="12" fill="#2e7d32" text-anchor="middle">ไม่ต้องมีข้อมูลฝึก · รันได้ทันที</text>
  <text x="208" y="158" font-size="12" fill="#c62828" text-anchor="middle">แต่เขียนมือ พอเงื่อนไขเยอะจะบาน</text>
  <text x="208" y="178" font-size="12" fill="#c62828" text-anchor="middle">และไม่เก่งกับ pattern ที่ซับซ้อน</text>
  <rect x="416" y="10" width="392" height="190" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="612" y="34" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ML (โมดูล 5 (Training))</text>
  <text x="612" y="60" font-size="12" fill="#555" text-anchor="middle">โมเดล "เรียน" เส้นแบ่งจากข้อมูล</text>
  <text x="612" y="80" font-size="12" fill="#555" text-anchor="middle">เราให้ตัวอย่าง โมเดลหาเส้นเอง</text>
  <text x="612" y="110" font-size="12" fill="#6a1b9a" text-anchor="middle">จับ pattern ซับซ้อน/หลายมิติได้</text>
  <text x="612" y="130" font-size="12" fill="#6a1b9a" text-anchor="middle">ปรับตามข้อมูลใหม่ได้</text>
  <text x="612" y="158" font-size="12" fill="#ef6c00" text-anchor="middle">แต่ต้องมีข้อมูลฝึก + ฝึก + quantize</text>
  <text x="612" y="178" font-size="12" fill="#ef6c00" text-anchor="middle">และอธิบาย "ทำไม" ได้ยากกว่า</text>
</svg>
</div>

> อย่าเพิ่งด่ากฎมือว่าล้าสมัย ในงานจริงหลายอย่าง **กฎ threshold ง่ายๆ ชนะ ML** เพราะเบา อธิบายได้ ไม่ต้องมีข้อมูล วิศวกรเก่งคือคนที่รู้ว่าเมื่อไรควรใช้กฎ เมื่อไรควรใช้ ML — ชุดบทเรียนนี้ให้คุณรู้จักฝั่งกฎก่อน

---

# ค่าอนุพัทธ์ (derived metrics) — ทำไมต้องแปลงก่อนตัดสิน

ค่าดิบบางทีตัดสินยาก อุณหภูมิ 32°C ตอนแห้งกับตอนชื้นจัด "รู้สึก" ต่างกันมาก ค่าอนุพัทธ์รวมหลายค่าดิบเป็นตัวเดียวที่ "ตัดสินง่ายขึ้น"

<div style="text-align:center;margin:8px 0">
<svg width="820" height="160" viewBox="0 0 820 160" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDv" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="30" width="170" height="44" rx="8" fill="#e3f2fd" stroke="#1565c0"/>
  <text x="105" y="57" font-size="12" fill="#1565c0" text-anchor="middle">temp (C)</text>
  <rect x="20" y="90" width="170" height="44" rx="8" fill="#e3f2fd" stroke="#1565c0"/>
  <text x="105" y="117" font-size="12" fill="#1565c0" text-anchor="middle">humidity (%RH)</text>
  <rect x="300" y="60" width="220" height="44" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="410" y="80" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">dsp.dew_point / heat_index</text>
  <text x="410" y="97" font-size="10" fill="#888" text-anchor="middle">สูตรฟิสิกส์ (ไม่ใช่ ML)</text>
  <rect x="630" y="30" width="170" height="44" rx="8" fill="#e8f5e9" stroke="#2e7d32"/>
  <text x="715" y="52" font-size="12" fill="#2e7d32" text-anchor="middle">dew point (C)</text>
  <text x="715" y="67" font-size="10" fill="#888" text-anchor="middle">ชื้นจนกลั่นเป็นน้ำ</text>
  <rect x="630" y="90" width="170" height="44" rx="8" fill="#e8f5e9" stroke="#2e7d32"/>
  <text x="715" y="112" font-size="12" fill="#2e7d32" text-anchor="middle">feels-like (C)</text>
  <text x="715" y="127" font-size="10" fill="#888" text-anchor="middle">"รู้สึกเหมือน" กี่องศา</text>
  <line x1="190" y1="52" x2="298" y2="74" stroke="#607d8b" stroke-width="2" marker-end="url(#arDv)"/>
  <line x1="190" y1="112" x2="298" y2="90" stroke="#607d8b" stroke-width="2" marker-end="url(#arDv)"/>
  <line x1="520" y1="74" x2="628" y2="52" stroke="#607d8b" stroke-width="2" marker-end="url(#arDv)"/>
  <line x1="520" y1="90" x2="628" y2="112" stroke="#607d8b" stroke-width="2" marker-end="url(#arDv)"/>
</svg>
</div>

- ในโลก ML ขั้นแปลงค่าดิบให้ "ตัดสินง่ายขึ้น" นี้เรียกว่า **feature engineering** — dew point/heat index คือ feature ที่คนคิดสูตรไว้ให้แล้ว
- บทเรียน 4.5–4.6 เราจะทำ feature ที่ซับซ้อนกว่านี้ (spectrogram) วันนี้เริ่มจาก feature ที่มีสูตรตรงๆ ก่อน

> บทเรียนสำคัญ: **classifier จะดีแค่ไหน ขึ้นกับว่าเราป้อน "ค่าอะไร" ให้มัน** ป้อนค่าดิบเปล่าๆ กฎอาจตัดสินพลาด แต่ป้อน heat index กฎจับ "ร้อนอบอ้าว" ได้แม่นขึ้นทันที

---

# dew point — จุดน้ำค้าง

**Dew point** (จุดน้ำค้าง) คืออุณหภูมิที่อากาศชื้นจนไอน้ำเริ่มกลั่นเป็นหยดน้ำ ยิ่ง dew point สูงเทียบกับอุณหภูมิ อากาศยิ่ง "อึดอัดชื้น"

`dsp.dew_point(t, rh)` ใช้สูตร Magnus–Tetens คืนค่าเป็นองศาเซลเซียส:

$$\gamma = \frac{a\,t}{b+t} + \ln\!\left(\frac{\mathrm{RH}}{100}\right),\qquad T_{dew} = \frac{b\,\gamma}{a-\gamma}\quad (a=17.27,\; b=237.7)$$

```python
import dsp
dp = dsp.dew_point(30.0, 75.0)   # ~25.1 C  ->  ชื้นมาก ใกล้อุณหภูมิจริง
dp = dsp.dew_point(30.0, 30.0)   # ~10.5 C  ->  แห้ง ห่างจากอุณหภูมิจริงเยอะ
```

- เราไม่ต้องจำสูตร แค่รู้ว่า `dsp` คำนวณให้ และ **dew point ที่เข้าใกล้อุณหภูมิ = อากาศอิ่มตัว/ชื้นมาก**
- เป็นตัวชี้ความชื้นที่ "ตรง" กว่า %RH เปล่าๆ เพราะ %RH เดียวกันที่คนละอุณหภูมิ ให้ความรู้สึกต่างกัน

> ตัวเลขในคอมเมนต์ (`~25.1 C`) มาจากสูตรจริงในเฟิร์มแวร์ (`moddsp.c`) ไม่ใช่เดา — ลองเรียกใน REPL เทียบดูได้

---

# อ่านสูตร dew point ทีละตัว (ไม่ต้องท่อง)

สูตร Magnus แบ่งเป็นสองก้าว: ก้าวแรกรวม `t` กับ `RH` เป็นตัวกลาง $\gamma$ (แกมมา) ก้าวสองแปลง $\gamma$ กลับเป็นอุณหภูมิจุดน้ำค้าง:

$$\gamma \;=\; \ln\!\left(\frac{\mathrm{RH}}{100}\right) + \frac{a\,t}{b+t}, \qquad T_{d} \;=\; \frac{b\,\gamma}{\,a-\gamma\,} \qquad (a=17.27,\; b=237.7)$$

อ่านทีละสัญลักษณ์แบบภาษาคน:

- $t$ — อุณหภูมิอากาศตอนนี้ (°C) อ่านจาก DPS368
- $\mathrm{RH}$ — ความชื้นสัมพัทธ์เป็นเปอร์เซ็นต์ (0–100) อ่านจาก SHT40
- $\gamma$ — ตัวกลางที่ไม่มีความหมายทางกายภาพตรงๆ เป็นแค่ "ขั้นพัก" ที่รวม $t$ กับ $\mathrm{RH}$ ให้อยู่ในรูปเดียวก่อนแปลงกลับ
- $a,\,b$ — ค่าคงที่ของสูตร Magnus (จูนไว้ให้เข้ากับพฤติกรรมไอน้ำในอากาศ) ไม่ต้องจำ `dsp` ใส่ให้แล้ว
- $T_{d}$ — คำตอบที่เราต้องการ: อุณหภูมิจุดน้ำค้าง (°C)

**ทำไมต้องรู้แค่นี้ก็พอ:** พจน์ $\ln(\mathrm{RH}/100)$ คือหัวใจ — ตอนอากาศชื้นจัด $\mathrm{RH}\to100$ ทำให้ $\ln(\mathrm{RH}/100)\to0$ (ค่าลบน้อยลง) $\gamma$ จึงโตขึ้น แล้วดัน $T_{d}$ ให้ **เข้าใกล้ $t$** พอ $T_{d}$ เกือบเท่า $t$ = อากาศอิ่มตัว น้ำเริ่มกลั่น

> นี่คือเหตุผลที่บันไดกฎวันนี้ดูที่ **ระยะห่าง $t - T_{d}$** เป็นสัญญาณความชื้น: ห่างมาก = แห้งสบาย, ห่างน้อย = ชื้นอึดอัด สูตรทำงานหนักแทนเรา เราแค่เอา "ระยะห่าง" ไปตั้งเส้นแบ่ง

---

# heat index — "รู้สึกเหมือน" ร้อนกว่าจริง

**Heat index** (ดัชนีความร้อน) รวมอุณหภูมิกับความชื้นเป็น "อุณหภูมิที่ร่างกายรู้สึก" ตอนชื้นจัด เหงื่อระเหยยาก เลยรู้สึกร้อนกว่าตัวเลขจริง

`dsp.heat_index(t, rh)` ใช้ Rothfusz regression คืนค่าเป็นองศาเซลเซียส:

```python
import dsp
hi = dsp.heat_index(32.0, 40.0)   # ~32 C   -> ชื้นน้อย รู้สึกใกล้อุณหภูมิจริง
hi = dsp.heat_index(32.0, 80.0)   # ~44 C   -> ชื้นจัด รู้สึกร้อนกว่าจริง ~12 องศา
```

- อุณหภูมิดิบเท่ากัน (32°C) แต่ heat index ต่างกันราว 12 องศาเพราะความชื้น
- นี่คือเหตุผลที่บันไดกฎของเราตัดสิน "ร้อน/อันตราย" จาก **heat index** ไม่ใช่จากอุณหภูมิดิบ

> สังเกตพลังของ derived metric: ถ้าเราจำแนกจากอุณหภูมิดิบอย่างเดียว จะพลาด "ร้อนอบอ้าวตอนชื้น" ทั้งที่มันคือภาวะอันตรายจริง — feature ที่ดีทำให้กฎง่ายๆ ฉลาดขึ้น

---

# dsp มีอะไรให้ — สามฟังก์ชันสิ่งแวดล้อม

โมดูล `dsp` มีฟังก์ชันแปลงค่า+จำแนกสิ่งแวดล้อมสำเร็จรูปให้แล้ว ทั้งหมดเป็นคณิต/ฟิสิกส์ล้วน รันบน CM33 ไม่ใช้ NPU:

| คำสั่ง | รับ | คืน |
|---|---|---|
| `dsp.dew_point(t, rh)` | อุณหภูมิ°C, %RH | จุดน้ำค้าง °C |
| `dsp.heat_index(t, rh)` | อุณหภูมิ°C, %RH | "รู้สึกเหมือน" °C |
| `dsp.comfort_zone(t, rh)` | อุณหภูมิ°C, %RH | คลาส str: `cold/hot/dry/humid/comfortable/acceptable` |

- สองตัวแรกคือ **derived metric** (แปลงค่า) · ตัวที่สามคือ **classifier สำเร็จรูป** (ตัดสินเป็นคลาส)
- `dsp.comfort_zone` คือ "ของที่ทำงานได้" ที่เราจะรันก่อน แล้วแกะ แล้วเขียนเวอร์ชันของเราเองแข่งกับมัน

> เซนเซอร์ที่ป้อนค่าพวกนี้: **DPS368** (ความดัน+อุณหภูมิ) กับ **SHT40** (ความชื้น) — AI Kit มีทั้งคู่ Eva Kit ไม่มี ชุดบทเรียนนี้จึงรันบน AI Kit หรือ Emulator

---

# แกะ dsp.comfort_zone — กฎที่ฝังในเฟิร์มแวร์

`dsp.comfort_zone` ที่เรารันตอนเปิดบทเรียน ข้างในมันคือ **บันไดกฎ** เขียนด้วย C — ไม่มี AI สักนิด เทียบเป็น Python ได้ประมาณนี้:

```python
def comfort_zone(t, rh):          # กฎจริงใน moddsp.c (แปลงเป็น Python ให้อ่านง่าย)
    if t < 18:            return "cold"
    if t > 27:            return "hot"
    if rh < 30:           return "dry"
    if rh > 70:           return "humid"
    if 20 <= t <= 25 and 30 <= rh <= 60:
                          return "comfortable"
    return "acceptable"
```

- เห็นไหมว่ามันคือ `if` ไล่ทีละขั้น — **นี่แหละบันไดกฎ** ที่เราจะเขียนเองในไฟล์ฝึก
- มันตัดสินจาก **ค่าดิบ** (t, rh) ล้วน เราจะทำให้เวอร์ชันของเรา "ฉลาดขึ้น" ด้วยการใช้ heat index (derived) ด้วย

> การ "แกะของสำเร็จรูปให้เห็นว่าข้างในไม่มีเวทมนตร์" คือหัวใจของการเรียนแบบกลับด้าน — พอเห็นว่ากฎนี้เป็นแค่ `if` ไม่กี่บรรทัด คุณจะกล้าเขียนของตัวเองทันที

---

# threshold logic — เส้นแบ่งเดียว

หน่วยย่อยที่สุดของกฎคือ **เส้นแบ่งเดียว (single threshold)**: ค่าหนึ่งค่าเทียบกับเลขหนึ่งเลข แล้วแบ่งโลกเป็นสองฝั่ง

```python
if heat_index >= 32:
    verdict = "hot"          # ฝั่งเกินเส้น
else:
    verdict = "not hot"      # ฝั่งไม่ถึงเส้น
```

<div style="text-align:center;margin:6px 0">
<svg width="720" height="96" viewBox="0 0 720 96" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="50" x2="680" y2="50" stroke="#cfd8dc" stroke-width="4"/>
  <line x1="420" y1="24" x2="420" y2="76" stroke="#ef6c00" stroke-width="3"/>
  <text x="420" y="18" font-size="13" font-weight="700" fill="#ef6c00" text-anchor="middle">เส้นแบ่ง = 32</text>
  <text x="220" y="70" font-size="13" fill="#2e7d32" text-anchor="middle">not hot</text>
  <text x="560" y="70" font-size="13" fill="#c62828" text-anchor="middle">hot</text>
  <text x="60" y="44" font-size="11" fill="#888">น้อย</text>
  <text x="660" y="44" font-size="11" fill="#888" text-anchor="end">มาก</text>
</svg>
</div>

- เส้นแบ่งเดียวแบ่งได้แค่ 2 คลาส ถ้าอยากได้ 6 คลาส เราต้องวางเส้นหลายเส้น = **บันไดกฎ**
- ที่ตั้งเส้น (32) เรียกว่า **hyperparameter ของกฎ** — เราเลือกเอง จากความรู้/มาตรฐาน ไม่ได้เรียนจากข้อมูล

> เก็บคำถามนี้ไว้: "ตั้งเส้นที่ 32 เอามาจากไหน?" ในกฎมือเราตอบได้ (มาตรฐาน heat index) แต่พอเป็น ML โมเดลจะหาเส้นเองจากข้อมูล — นั่นคือความต่างที่เราจะเห็นชัดในโมดูล 5 (Training)

---

# บันไดกฎ (threshold ladder) — หลายเส้นต่อกัน

พอต้องการหลายคลาส เราเรียง `if` เป็นชั้นๆ ไล่จากบนลงล่าง **ขั้นแรกที่เงื่อนไขจริงชนะทันที** แล้ว `return` จบ:

```python
def classify(t, h, hi):
    if hi >= 41:  return "danger"        # ชั้น 1 (อันตรายสุด อยู่บนสุด)
    if hi >= 32:  return "hot"           # ชั้น 2
    if h  >= 70:  return "humid"         # ชั้น 3
    if t  <  20:  return "cold"          # ชั้น 4
    if h  <  30:  return "dry"           # ชั้น 5
    return "comfortable"                 # ตกทุกชั้น = สบาย
```

- อ่านเป็นประโยค: "ถ้ารู้สึกร้อนถึงขั้นอันตราย → danger ไม่งั้นถ้ารู้สึกร้อน → hot ไม่งั้นถ้าชื้น → humid ..."
- แต่ละ `return` ตัดจบทันที คลาสล่างๆ จะได้ก็ต่อเมื่อผ่านทุกชั้นบนมาแล้ว
- นี่คือ **ช่องเติมหลักของชุดบทเรียนนี้** — งาน 30% ของคุณคือเขียนบันไดนี้เอง

> บันไดกฎอ่านง่ายและ "อธิบายได้" ทุกคำตัดสิน แต่มีกับดักหนึ่งข้อที่ทำคนพลาดบ่อย — **ลำดับของชั้น** ไปดูหน้าถัดไป

---

# ทำไม "ลำดับ" ของบันไดถึงสำคัญ

บันไดกฎ return ขั้นแรกที่เจอ ดังนั้นถ้าวางชั้นผิดลำดับ คลาสที่ควรชนะจะโดนชั้นบนแย่งไปก่อน

<div style="text-align:center;margin:6px 0">
<svg width="840" height="200" viewBox="0 0 840 200" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="14" width="400" height="176" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="212" y="38" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">ลำดับถูก (danger บนสุด)</text>
  <text x="32" y="66" font-size="12" fill="#555">if hi &gt;= 41: return "danger"</text>
  <text x="32" y="88" font-size="12" fill="#555">if hi &gt;= 32: return "hot"</text>
  <text x="32" y="120" font-size="12" fill="#555">อินพุต: hi = 43 (ชื้นจัด+ร้อน)</text>
  <text x="32" y="148" font-size="13" font-weight="700" fill="#2e7d32">-&gt; "danger" ถูกต้อง</text>
  <text x="32" y="172" font-size="11" fill="#888">ชั้น danger อยู่บน จับได้ก่อน</text>
  <rect x="428" y="14" width="400" height="176" rx="12" fill="#fdecea" stroke="#c62828" stroke-width="2"/>
  <text x="628" y="38" font-size="14" font-weight="700" fill="#c62828" text-anchor="middle">ลำดับผิด (hot บนสุด)</text>
  <text x="448" y="66" font-size="12" fill="#555">if hi &gt;= 32: return "hot"</text>
  <text x="448" y="88" font-size="12" fill="#555">if hi &gt;= 41: return "danger"</text>
  <text x="448" y="120" font-size="12" fill="#555">อินพุต: hi = 43 (ชื้นจัด+ร้อน)</text>
  <text x="448" y="148" font-size="13" font-weight="700" fill="#c62828">-&gt; "hot" ผิด! (43 เข้า 32 ก่อน)</text>
  <text x="448" y="172" font-size="11" fill="#888">danger ไม่มีวันถูกเรียก = bug เงียบ</text>
</svg>
</div>

> กฎเหล็ก: **เงื่อนไขที่เฉพาะ/รุนแรงกว่าต้องอยู่บน เงื่อนไขกว้างต้องอยู่ล่าง** ถ้าวางสลับ ชั้นล่างจะกลายเป็น "โค้ดที่ไม่มีวันทำงาน" (dead branch) — บั๊กชนิดที่ compiler ไม่เตือน ต้องจับด้วยการทดสอบ
