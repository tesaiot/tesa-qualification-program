---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — แรงดัน กระแส และความต้านทาน"
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

# บทเรียน 1.1 — แรงดัน กระแส และความต้านทาน

## ใช้กฎของโอห์มและกฎกำลังไฟฟ้าคำนวณวงจรพื้นฐาน

**โมดูล 1 — วงจรและอิเล็กทรอนิกส์พื้นฐาน**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณแรงดัน กระแส หรือความต้านทานที่ไม่ทราบค่าในวงจรอนุกรมและขนานด้วยกฎของโอห์ม
2. คำนวณกำลังไฟฟ้าที่ตัวต้านทานรับ และเลือกพิกัดกำลังที่เหมาะสม

---

## ก่อนเริ่ม

- เครื่องคิดเลข กระดาษ และดินสอ ส่วนแนวคิดกับแบบฝึกไม่ต้องใช้บอร์ด
- แล็บ: บอร์ด TESAIoT Dev Kit หรือ Eva Kit, เบรดบอร์ด, สายจัมเปอร์, ตัวต้านทาน 1 kΩ, 2.2 kΩ และ 4.7 kΩ อย่างละตัว, มัลติมิเตอร์
- ยังไม่เคยใช้มัลติมิเตอร์ก็ไม่เป็นไร แล็บนี้ใช้แค่โหมดวัดแรงดันกับความต้านทาน

> **ความปลอดภัย** ใช้ไฟ 3.3 V จากบอร์ดเท่านั้น ห้ามให้สายจัมเปอร์ต่อขา 3V3 กับ GND ตรง ๆ (ลัดวงจร) และถอดสาย USB ทุกครั้งก่อนย้ายสายบนเบรดบอร์ด

---

## ดูของจริงก่อน

หาขา **3V3** กับ **GND** บน header ของบอร์ด — GND คือจุดอ้างอิงของทั้งบอร์ด "ขานี้ 3.3 V" แปลว่า "สูงกว่า GND อยู่ 3.3 V" เสมอ เหมือนความสูงของตึกที่วัดจากพื้นดิน

**ทายก่อน** ถ้าเอาตัวต้านทาน 1 kΩ ต่อระหว่าง 3V3 กับ GND จะมีกระแสไหลเท่าไร และตัวต้านทานจะร้อนไหม จดคำตอบไว้ แล้วเทียบกับที่คำนวณในหัวข้อถัดไป

---

## แนวคิด (1) — กฎของโอห์ม

- **แรงดัน (V)** หน่วยโวลต์ — แรงผลักให้ประจุเคลื่อนที่
- **กระแส (I)** หน่วยแอมแปร์ — ประจุที่ไหลผ่านจุดหนึ่งต่อวินาที
- **ความต้านทาน (R)** หน่วยโอห์ม — สิ่งที่ขัดขวางกระแส

```text
V = I × R        I = V / R        R = V / I
```

ใช้คู่หน่วย **mA กับ kΩ** จะได้โวลต์ออกมาพอดี

```text
I = V / R = 3.3 V / 1 kΩ = 3.3 mA
```

สายไฟความต้านทาน 0.1 Ω คร่อม 3.3 V: I = 3.3 / 0.1 = 33 A — นี่คือเหตุผลที่ลัดวงจร 3V3 กับ GND อันตราย

---

## แนวคิด (2) — อนุกรมและขนาน

<figure>
<svg viewBox="0 0 340 200" width="340" role="img" aria-label="วงจรอนุกรมและวงจรขนานจากแหล่งจ่าย 3.3 V" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M60 22H80M70 22V30"/><text x="70" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V</text>
<path d="M70 30V40"/>
<polyline points="70,40 70,50 76,52.5 64,57.5 76,62.5 64,67.5 76,72.5 64,77.5 70,80 70,90"/>
<text x="86" y="70" fill="currentColor" stroke="none">R1 1 kΩ</text>
<polyline points="70,90 70,100 76,102.5 64,107.5 76,112.5 64,117.5 76,122.5 64,127.5 70,130 70,140"/>
<text x="86" y="120" fill="currentColor" stroke="none">R2 2.2 kΩ</text>
<path d="M70 140V150"/>
<path d="M70 150V158M60 158H80M64 162H76M68 166H72"/>
<path d="M50 50L50 80M47.3 73.6L50 80L52.7 73.6"/>
<text x="44" y="70" text-anchor="end" fill="currentColor" stroke="none">I</text>
<text x="75" y="190" text-anchor="middle" fill="currentColor" stroke="none">series: R = R1 + R2</text>
<path d="M240 22H260M250 22V30"/><text x="250" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V</text>
<path d="M250 30V50M210 50H290M210 50V70M290 50V70"/>
<circle cx="250" cy="50" r="2.5" fill="currentColor"/>
<polyline points="210,70 210,80 216,82.5 204,87.5 216,92.5 204,97.5 216,102.5 204,107.5 210,110 210,120"/>
<text x="194" y="100" text-anchor="end" fill="currentColor" stroke="none">R1</text>
<polyline points="290,70 290,80 296,82.5 284,87.5 296,92.5 284,97.5 296,102.5 284,107.5 290,110 290,120"/>
<text x="306" y="100" fill="currentColor" stroke="none">R2</text>
<path d="M210 120V140M290 120V140M210 140H290M250 140V150"/>
<circle cx="250" cy="140" r="2.5" fill="currentColor"/>
<path d="M250 150V158M240 158H260M244 162H256M248 166H252"/>
<text x="250" y="190" text-anchor="middle" fill="currentColor" stroke="none">parallel: 1/R = 1/R1 + 1/R2</text>
</svg>
<figcaption>ซ้าย: อนุกรม กระแสเดียวกันไหลผ่านทุกตัว แรงดันแบ่งกัน ขวา: ขนาน แรงดันเท่ากันทุกตัว กระแสแยกกันไหล</figcaption>
</figure>

---

## แนวคิด (3) — อนุกรมและขนาน (ตัวอย่างตัวเลข)

**อนุกรม** 1 kΩ + 2.2 kΩ จาก 3.3 V

```text
R รวม = 1 kΩ + 2.2 kΩ = 3.2 kΩ
I     = 3.3 V / 3.2 kΩ = 1.03 mA
V_R1  = 1.03 mA × 1 kΩ   = 1.03 V
V_R2  = 1.03 mA × 2.2 kΩ = 2.27 V      ตรวจ: 1.03 + 2.27 = 3.30 V
```

**ขนาน** 1 kΩ ∥ 2.2 kΩ ที่ 3.3 V — ความต้านทานรวมน้อยกว่าตัวที่น้อยที่สุดเสมอ

```text
R รวม = (1 × 2.2) / (1 + 2.2) kΩ = 0.6875 kΩ = 687.5 Ω
I1 = 3.3 V / 1 kΩ = 3.3 mA · I2 = 3.3 V / 2.2 kΩ = 1.5 mA · I รวม = 4.8 mA
```

---

## แนวคิด (4) — กำลังไฟฟ้าและพิกัดกำลัง

```text
P = V × I = I² × R = V² / R
```

พิกัดกำลังของตัวต้านทานขาเสียบทั่วไปคือ 1/4 W — เลือกพิกัด **อย่างน้อยสองเท่า** ของกำลังที่คำนวณได้

**ตัวอย่าง 1** (คำถามตอน "ดูของจริงก่อน") 1 kΩ คร่อม 3.3 V

```text
P = V² / R = (3.3 V)² / 1000 Ω = 0.01089 W ≈ 10.9 mW
```

น้อยกว่า 1/4 W (250 mW) มาก แทบไม่อุ่นเลย

**ตัวอย่าง 2** 100 Ω คร่อม 5 V → P = (5 V)² / 100 Ω = 0.25 W เท่ากับพิกัด 1/4 W พอดี ตามหลักสองเท่าต้องเลือก 1/2 W

---

## ตัวอย่างสมบูรณ์ — วงจรผสม

<figure>
<svg viewBox="0 0 300 215" width="300" role="img" aria-label="วงจรผสม R1 อนุกรมกับ R2 ขนาน R3 จากแหล่งจ่าย 3.3 V" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V (3V3)</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="96" y="70" fill="currentColor" stroke="none">R1 1 kΩ</text>
<path d="M80 90V100M40 100H200M80 100V100"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<text x="208" y="104" fill="currentColor" stroke="none">A (V_A)</text>
<path d="M40 100V115M160 100V115"/>
<polyline points="40,115 40,125 46,127.5 34,132.5 46,137.5 34,142.5 46,147.5 34,152.5 40,155 40,165"/>
<text x="56" y="145" fill="currentColor" stroke="none">R2 2.2 kΩ</text>
<polyline points="160,115 160,125 166,127.5 154,132.5 166,137.5 154,142.5 166,147.5 154,152.5 160,155 160,165"/>
<text x="176" y="145" fill="currentColor" stroke="none">R3 4.7 kΩ</text>
<path d="M40 165V180M160 165V180M40 180H160M100 180V188"/>
<circle cx="100" cy="180" r="2.5" fill="currentColor"/>
<path d="M100 188V196M90 196H110M94 200H106M98 204H102"/>
<circle cx="200" cy="100" r="3"/>
</svg>
<figcaption>วงจรผสม: R1 ต่ออนุกรมกับกลุ่ม R2 ขนาน R3 จุด A คือจุดที่คำนวณและวัดแรงดันเทียบ GND</figcaption>
</figure>

**โจทย์** 3.3 V ผ่าน R1 = 1 kΩ ไปที่จุด A แล้ว R2 = 2.2 kΩ ขนาน R3 = 4.7 kΩ ลง GND

---

## ตัวอย่างสมบูรณ์ — คำนวณทีละขั้น

```text
ขั้นที่ 1  R2 ∥ R3 = (2.2 × 4.7) / (2.2 + 4.7) kΩ = 1.499 kΩ ≈ 1.50 kΩ

ขั้นที่ 2  R รวม = 1 kΩ + 1.499 kΩ = 2.499 kΩ ≈ 2.50 kΩ
           I     = 3.3 V / 2.499 kΩ = 1.32 mA        (ผ่าน R1)
           V_R1  = 1.32 mA × 1 kΩ = 1.32 V
           V_A   = 3.3 V − 1.32 V = 1.98 V

ขั้นที่ 3  I2 = 1.98 / 2.2 kΩ = 0.90 mA   I3 = 1.98 / 4.7 kΩ = 0.42 mA
           ตรวจ KCL: 0.90 + 0.42 = 1.32 mA ตรงกับกระแสผ่าน R1

ขั้นที่ 4  กำลัง: R1 1.74 mW · R2 1.78 mW · R3 0.83 mW · รวม 4.36 mW
```

สังเกตนิสัย: คำนวณเสร็จแล้ว **ตรวจด้วยกฎอีกข้อหนึ่งเสมอ** (KVL, KCL หรือกำลังรวม)

---

## ฝึกเติม / แล็บ

**ฝึกเติม** (ลองก่อนดูเฉลยใน README)

1. 4.7 kΩ คร่อม 3.3 V กระแสเท่าไร (mA และ µA)
2. วงจรไฟแสดงสถานะต้องการ 2 mA จาก 3.3 V ความต้านทานรวมต้องเป็นเท่าไร
3. ความต้านทานรวมของ (ก) 10 kΩ สองตัวขนาน (ข) 3.3 kΩ สามตัวอนุกรม

**แล็บ** ต่อวงจรในตัวอย่างสมบูรณ์บนเบรดบอร์ด (R1 = 1 kΩ, R2 = 2.2 kΩ, R3 = 4.7 kΩ)

1. วัดตัวต้านทานทั้งสามตัวก่อนต่อวงจร (โหมด Ω)
2. ต่อวงจร GND ก่อน แล้วค่อยต่อ 3V3 · **ทาย** ค่าที่จะวัดได้ก่อนเสียบไฟ
3. วัดแรงดันจริงของ 3V3, V_A และ V_R1 แล้วคำนวณกระแสจากค่าที่วัดได้ เทียบกับที่ทายไว้

---

## เช็กความเข้าใจ

1. ตัวต้านทาน 2.2 kΩ ต่อคร่อมแหล่งจ่าย 3.3 V มีกระแสไหลเท่าไร
   - ก) 1.5 mA · ข) 7.26 mA · ค) 0.67 mA · ง) 1.5 A

2. ตัวต้านทาน 1 kΩ ต่อขนานกับ 3.3 kΩ ความต้านทานรวมใกล้ค่าใดที่สุด
   - ก) 4.3 kΩ · ข) 767 Ω · ค) 2.15 kΩ · ง) 1.15 kΩ

3. ตัวต้านทาน 47 Ω ต่อคร่อม 3.3 V ควรเลือกพิกัดกำลังเท่าไร ถ้าใช้หลักเผื่ออย่างน้อยสองเท่า
   - ก) 1/8 W · ข) 1/4 W · ค) 1/2 W · ง) เลือกอะไรก็ได้

---

## ไปต่อ

บทเรียนถัดไป [วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก](../l02-dividers-and-sensors/README.md) — จุด A ในแล็บนี้ก็คือวงจรแบ่งแรงดันแบบหนึ่ง เราจะเอาหลักเดียวกันไปอธิบายลูกบิดบนบอร์ด และแปลงตัวเลขที่ ADC อ่านได้กลับเป็นโวลต์

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
