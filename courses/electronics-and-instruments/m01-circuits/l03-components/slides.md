---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.3 — ชิ้นส่วนพื้นฐาน: ตัวต้านทาน ตัวเก็บประจุ ไดโอด และทรานซิสเตอร์"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 1.3 — ชิ้นส่วนพื้นฐาน

## รู้จักหน้าที่ของชิ้นส่วนพื้นฐาน และใช้ทรานซิสเตอร์เป็นสวิตช์ขับโหลดที่ขาไมโครคอนโทรลเลอร์ขับเองไม่ได้

**โมดูล 1 — วงจรและอิเล็กทรอนิกส์พื้นฐาน**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณตัวต้านทานจำกัดกระแสของหลอด LED จากแรงดันแหล่งจ่าย แรงดันตกคร่อม LED และกระแสที่ต้องการ
2. อธิบายหน้าที่ของตัวเก็บประจุ decoupling และไดโอดกันไฟย้อน (flyback diode) ในวงจรขับโหลดแบบขดลวด
3. เลือกใช้ทรานซิสเตอร์หรือ MOSFET เป็นสวิตช์เมื่อโหลดต้องการกระแสเกินกว่าขาของไมโครคอนโทรลเลอร์จ่ายได้

---

## ก่อนเริ่ม

- ใช้กฎของโอห์ม วงจรอนุกรม และวงจรแบ่งแรงดันได้แล้ว
- แล็บ: LED สีแดง, ตัวต้านทาน 470 Ω และ 1 kΩ, ตัวต้านทาน 100 kΩ, ตัวเก็บประจุอิเล็กโทรไลต์ 100 µF, นาฬิกาจับเวลา, มัลติมิเตอร์, บอร์ด

> **ความปลอดภัย** ตัวเก็บประจุอิเล็กโทรไลต์มีขั้ว ขายาวกว่าคือขั้วบวก ต่อกลับขั้วอาจร้อน บวม หรือระเบิดได้ — ตรวจขั้วทุกครั้งตั้งแต่ตอนนี้

---

## ดูของจริงก่อน

ส่องบอร์ดด้วยแว่นขยายหรือกล้องมือถือ

- รอบชิปแต่ละตัวมีชิ้นส่วนสี่เหลี่ยมเล็ก ๆ วางชิดขา — ส่วนใหญ่คือตัวเก็บประจุ
- ข้าง ๆ หลอด LED แต่ละดวงมักมีตัวต้านทานเล็ก ๆ หนึ่งตัว

ถามตัวเองสองข้อ: ทำไมชิปทุกตัวต้องมีตัวเก็บประจุเป็นของตัวเองวางชิดขา และทำไมหลอด LED ต้องมีตัวต้านทานคู่กันเสมอ บทเรียนนี้ตอบทั้งสองข้อ

---

## แนวคิด (1) — LED และตัวต้านทานจำกัดกระแส

<figure>
<svg viewBox="0 0 360 170" width="360" role="img" aria-label="หลอด LED ต่ออนุกรมกับตัวต้านทานจำกัดกระแส" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M50 22H70M60 22V30"/><text x="60" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V or GPIO</text>
<path d="M60 30V40"/>
<polyline points="60,40 60,50 66,52.5 54,57.5 66,62.5 54,67.5 66,72.5 54,77.5 60,80 60,90"/>
<text x="76" y="70" fill="currentColor" stroke="none">R</text>
<path d="M60 90V105.0M52 105.0H68L60 117.0Z M52 117.0H68M60 117.0V134"/><path d="M71 106.0l7 -6m-4 0h4v4M71 113.0l7 -6m-4 0h4v4"/>
<text x="92" y="120" fill="currentColor" stroke="none">LED (V_f)</text>
<path d="M60 134V142M50 142H70M54 146H66M58 150H62"/>
<text x="180" y="60" fill="currentColor" stroke="none">R = (V_s − V_f) / I</text>
<text x="180" y="84" fill="currentColor" stroke="none">3.3 V, V_f 2.0 V, 5 mA</text>
<text x="180" y="104" fill="currentColor" stroke="none">R = 1.3 V / 5 mA = 260 Ω</text>
<text x="180" y="124" fill="currentColor" stroke="none">use 270 Ω → 4.81 mA</text>
</svg>
<figcaption>ตัวต้านทานรับแรงดันส่วนที่เหลือจาก V_f ของ LED และเป็นตัวกำหนดกระแส</figcaption>
</figure>

LED สีแดง V_f ราว 1.8–2.2 V; สีน้ำเงิน/เขียวสด/ขาว ราว 2.8–3.3 V (ค่าจริงต้องดูเอกสารข้อมูล)

---

## แนวคิด (2) — คำนวณ R และกับดักของ headroom น้อย

```text
R = (V_s − V_f) / I

ตัวอย่าง: 3.3 V, V_f = 2.0 V, 5 mA
R = 1.3 V / 5 mA = 260 Ω → ใช้ 270 Ω → I = 4.81 mA, กำลัง = 6.26 mW
```

ปัดขึ้นไปหาค่ามาตรฐานที่ใหญ่กว่าเสมอ (กระแสต่ำกว่าเป้าเล็กน้อย ปลอดภัยกว่า)

**กับดัก LED สีน้ำเงินที่ 3.3 V** V_f = 3.0 V เหลือ headroom แค่ 0.3 V — V_f ต่างกันได้ ±0.2 V ทำให้กระแสจริงแกว่งได้ห้าเท่า (0.67–3.33 mA) เมื่อ headroom น้อย ความสว่างคุมไม่ได้ — ทางแก้: เลี้ยงจากแหล่งจ่ายที่สูงกว่าแล้วใช้ทรานซิสเตอร์เป็นสวิตช์

---

## แนวคิด (3) — Decoupling: ทำไมชิปทุกตัวต้องมี

ตัวเก็บประจุประจุผ่านตัวต้านทานด้วยค่าคงที่เวลา **τ = R × C** ครบ 1τ ได้ 63.2% ของแรงดันแหล่งจ่าย ครบ 5τ ได้ราว 99.3%

**Decoupling** เมื่อชิปดึงกระแสกระชากสั้น ๆ ลายวงจรยาวมีความเหนี่ยวนำ จ่ายไม่ทัน

```text
สมมุติดึงเพิ่ม 50 mA ภายใน 2 ns ผ่านลาย L = 10 nH:
V = L × di/dt = 10 nH × (50 mA / 2 ns) = 0.25 V   ตกเกือบ 8% ของ 3.3 V

มีตัวเก็บประจุ 100 nF ชิดขา: กระชาก 50 mA นาน 10 ns ใช้ประจุ 0.5 nC
ΔV = Q / C = 0.5 nC / 100 nF = 5 mV   ตกแค่ 5 mV
```

ต้องวาง **ชิดขาไฟที่สุด** เพราะลายวงจรระหว่างตัวเก็บประจุกับขาก็มีความเหนี่ยวนำเช่นกัน

---

## แนวคิด (4) — ไดโอดกันไฟย้อน (flyback diode)

ขดลวด (รีเลย์ มอเตอร์) ไม่ยอมให้กระแสเปลี่ยนทันที เมื่อสวิตช์ตัดกระแส ขดลวดสร้างแรงดันสูงขึ้นเองตาม V = L × di/dt

```text
ขดลวด 100 mH กระแส 50 mA ถูกตัดภายใน 1 µs (อุดมคติ):
V = 100 mH × (50 mA / 1 µs) = 5,000 V
(ของจริงแรงดันจะพุ่งจนทรานซิสเตอร์พังหรือเกิดประกายก่อน)
```

ไดโอดคร่อมขดลวด (แคโทดทางฝั่งไฟบวก) ให้กระแสมีทางไหลวนต่อ จำกัดแรงดันไว้ราวแรงดันแหล่งจ่ายบวก 0.7 V

---

## แนวคิด (5) — ทรานซิสเตอร์และ MOSFET เป็นสวิตช์

<figure>
<svg viewBox="0 0 360 245" width="360" role="img" aria-label="MOSFET ต่อด้านล่างขับขดลวดรีเลย์พร้อมไดโอดกันไฟย้อน" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M150 22H170M160 22V30"/><text x="160" y="17" text-anchor="middle" fill="currentColor" stroke="none">5 V</text>
<path d="M160 30V40M160 40H110M160 40H210"/>
<circle cx="160" cy="40" r="2.5" fill="currentColor"/>
<path d="M110 40V52M210 40V52"/>
<path d="M110 52V60.0a4 4 0 0 1 0 8a4 4 0 0 1 0 8a4 4 0 0 1 0 8a4 4 0 0 1 0 8V100"/>
<text x="96" y="80" text-anchor="end" fill="currentColor" stroke="none">relay coil</text>
<path d="M210 100V82.0M202 82.0H218L210 70.0Z M202 70.0H218M210 70.0V52"/>
<text x="226" y="80" fill="currentColor" stroke="none">flyback diode</text>
<path d="M110 100V112H210V100"/>
<circle cx="160" cy="112" r="2.5" fill="currentColor"/>
<path d="M160 112V130"/>
<path d="M160 130V140H150M150 136V164M144 138V162M150 160H160V170"/>
<path d="M150 150H160V160M151 150l5 -3M151 150l5 3"/>
<text x="170" y="152" fill="currentColor" stroke="none">N-MOSFET (logic level)</text>
<path d="M144 150H120"/>
<polyline points="70,150 80,150 82.5,144 87.5,156 92.5,144 97.5,156 102.5,144 107.5,156 110,150 120,150"/>
<text x="95" y="140" text-anchor="middle" fill="currentColor" stroke="none">100 Ω</text>
<path d="M70 150H40"/>
<circle cx="37" cy="150" r="3"/>
<text x="37" y="138" text-anchor="middle" fill="currentColor" stroke="none">GPIO</text>
<path d="M120 150V165"/>
<circle cx="120" cy="150" r="2.5" fill="currentColor"/>
<polyline points="120,165 120,170 126,172.5 114,177.5 126,182.5 114,187.5 126,192.5 114,197.5 120,200 120,205"/>
<text x="104" y="190" text-anchor="end" fill="currentColor" stroke="none">100 kΩ</text>
<path d="M120 205V215H160M160 170V215"/>
<circle cx="160" cy="215" r="2.5" fill="currentColor"/>
<path d="M160 215V223M150 223H170M154 227H166M158 231H162"/>
</svg>
<figcaption>ขา GPIO สั่ง MOSFET ด้านล่าง (low-side) ให้ต่อขดลวดรีเลย์ลงกราวด์ ไดโอดคร่อมขดลวดให้กระแสมีทางไหลต่อตอนปิด ตัวต้านทาน 100 kΩ ดึงเกตลงกราวด์ระหว่างที่ชิปยังไม่เริ่มทำงาน</figcaption>
</figure>

---

## แนวคิด (6) — NPN กับ MOSFET: เลือกอย่างไร

**NPN (BJT)** คุมด้วยกระแสเบส — รีเลย์ 5 V, 70 mA, β บังคับ 20: กระแสเบส 70/20 = 3.5 mA, R_เบส = (3.3−0.7)/3.5 mA = 743 Ω → ใช้ 750 Ω (แต่โหลดกระแสสูงต้องการกระแสเบสหลาย mA ซึ่งขาจ่ายไม่ไหว)

**MOSFET ชนิด N** คุมด้วยแรงดันเกต แทบไม่กินกระแสขณะค้าง เหมาะกับโหลดกระแสสูง ต้องเลือก **logic-level** (R_DS(on) ระบุที่ V_GS ต่ำเท่าขาที่มี เช่น 2.5 V)

```text
แถบไฟ LED 12 V, 500 mA, R_DS(on) = 0.05 Ω ที่ V_GS = 2.5 V
แรงดันตกคร่อม MOSFET = 0.5 A × 0.05 Ω = 25 mV
กำลังที่ MOSFET = (0.5 A)² × 0.05 Ω = 12.5 mW — ไม่ต้องระบายความร้อน
```

---

## ตัวอย่างสมบูรณ์ — ขับรีเลย์ 5 V จากขา GPIO 3.3 V

```text
1. ขาจ่ายตรงได้ไหม  ไม่ได้ (ต้องการ 5 V, 70 mA เกินขา GPIO)
2. เลือกสวิตช์  MOSFET ชนิด N logic-level, R_DS(on)=0.1 Ω ที่ V_GS=2.5V
   แรงดันตก 70 mA × 0.1 Ω = 7 mV, กำลัง (70 mA)² × 0.1 Ω = 0.49 mW
3. ตัวต้านทานเกต 100 Ω  จำกัดกระแสกระชากไม่เกิน 3.3/100 = 33 mA
   เกต 500 pF: τ = 100 Ω × 500 pF = 50 ns เร็วพอสำหรับรีเลย์
4. ตัวต้านทานดึงเกตลง 100 kΩ  กันขาลอยตอนรีเซ็ต กินกระแสตอนเปิด 3.3/100k = 33 µA
5. ไดโอดกันไฟย้อน  เช่น 1N4148 คร่อมขดลวด แคโทดฝั่ง 5 V
6. Decoupling  100 nF ชิดรีเลย์ + 10 µF อีกหนึ่งตัว
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. 5 V, LED สีแดง V_f = 2.0 V, 10 mA — หา R ค่ามาตรฐาน E12, กระแสจริง, กำลัง
2. R = 47 kΩ, C = 1 µF, 3.3 V — หา τ, เวลาที่ถือว่าเต็ม (5τ), แรงดันที่ t = τ

**แล็บ ส่วน A: LED กับตัวต้านทาน**

1. ต่อ 3V3 → 470 Ω → LED สีแดง → GND · **ทาย** กระแสก่อนเสียบไฟ
2. วัด V_R และ V_f ด้วยมัลติมิเตอร์ คำนวณกระแสจริง I = V_R / R เทียบกับที่ทายไว้

**แล็บ ส่วน B: ค่าคงที่เวลาที่มองเห็นได้ด้วยตา** ต่อ 3V3 → 100 kΩ → ตัวเก็บประจุ 100 µF (ตรวจขั้ว!) จับเวลาจนแรงดันถึง 63% ของค่าสุดท้าย

---

## เช็กความเข้าใจ

1. แหล่งจ่าย 3.3 V หลอด LED มี V_f = 2.1 V ต้องการกระแส 4 mA ตัวต้านทานที่คำนวณได้คือเท่าไร
   - ก) 300 Ω · ข) 825 Ω · ค) 525 Ω · ง) 3 Ω

2. ตัวเก็บประจุ decoupling 100 nF ที่วางชิดขาไฟของชิปทำหน้าที่หลักอะไร
   - ก) กรองสัญญาณข้อมูลที่ขา I/O · ข) จ่ายกระแสกระชากช่วงสั้น ๆ ให้ชิปจากตรงนั้นเลย · ค) เพิ่มแรงดันไฟเลี้ยง · ง) ป้องกันไฟกลับขั้ว

3. ต้องการสั่งมอเตอร์ 12 V ที่กินกระแส 800 mA จากขา GPIO 3.3 V วิธีใดเหมาะที่สุด
   - ก) ต่อขา GPIO โดยตรง · ข) NPN เล็กไม่มีไดโอด · ค) MOSFET ชนิด N logic-level พร้อมไดโอดกันไฟย้อน · ง) ตัวต้านทาน 15 Ω อนุกรม

---

## ไปต่อ

โมดูลถัดไปเข้าสู่ [ระดับลอจิกและเกตพื้นฐาน](../../m02-digital-logic/l01-logic-levels-and-gates/README.md) — ดูว่าแรงดันแบบไหนที่ชิปนับเป็น 0 หรือ 1 และทำไมบอร์ดที่มีทั้งระบบ 1.8 V และ 3.3 V ต้องระวังเวลาต่ออุปกรณ์ภายนอก

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
