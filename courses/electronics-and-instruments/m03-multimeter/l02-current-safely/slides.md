---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — วัดกระแสอย่างปลอดภัย"
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

# บทเรียน 3.2 — วัดกระแสอย่างปลอดภัย

## ต่อมัลติมิเตอร์อนุกรมเพื่อวัดกระแส ย้ายสายวัดให้ถูกช่อง และเข้าใจว่าทำไมการวัดกระแสผิดวิธีทำให้ฟิวส์ขาด

**โมดูล 3 — มัลติมิเตอร์**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. วัดกระแสของหลอด LED หนึ่งดวงโดยต่อมัลติมิเตอร์อนุกรมและใช้ช่องเสียบที่ถูกต้อง
2. อธิบายว่าทำไมการต่อมัลติมิเตอร์ในโหมดวัดกระแสคร่อมแหล่งจ่ายจึงอันตราย
3. เทียบกระแสที่วัดได้กับค่าที่คำนวณจากกฎของโอห์ม และอธิบายความต่าง

---

## ก่อนเริ่ม

- ผ่านบทเรียน [วัดแรงดันและความต่อเนื่อง](../l01-voltage-and-continuity/README.md)
- แล็บ: LED สีแดง, ตัวต้านทาน 270 Ω (หรือ 330 Ω) และ 1 kΩ, เบรดบอร์ด, มัลติมิเตอร์ที่มีช่อง mA, บอร์ด

> **ความปลอดภัย** สิ่งที่ทำให้มัลติมิเตอร์เสียบ่อยที่สุดคือ **ลืมย้ายสายแดงกลับจากช่อง mA/A** แล้วเอาไปวัดแรงดัน — วัดกระแสเสร็จ ย้ายสายแดงกลับช่อง VΩ ทันที

---

## ดูของจริงก่อน

หันมิเตอร์ด้านหลังหรือเปิดฝาช่องแบตเตอรี่ ดูว่าฟิวส์มีกี่ตัวและเขียนค่าอะไรไว้ — ช่อง mA มักมีฟิวส์เล็กหลายร้อย mA ช่อง 10A มักมีฟิวส์ใหญ่แยก

ฟิวส์เหล่านี้มีไว้เพื่อสถานการณ์เดียว: เมื่อคนต่อมิเตอร์ในโหมดกระแสผิดวิธี ทำไมโหมดนี้จึงอันตรายกว่าโหมดอื่น — คำตอบอยู่ในหัวข้อที่ 2

---

## แนวคิด (1) — วัดกระแสต้องต่ออนุกรม

<figure>
<svg viewBox="0 0 400 230" width="400" role="img" aria-label="การต่อมิเตอร์วัดกระแสแบบอนุกรมที่ถูกต้องและการต่อคร่อมแหล่งจ่ายที่ห้ามทำ" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M50 22H70M60 22V30"/><text x="60" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M60 30V40H120V52"/>
<circle cx="120" cy="70" r="18"/>
<text x="120" y="75" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">A</text>
<text x="146" y="60" fill="currentColor" stroke="none">red → mA jack</text>
<text x="146" y="88" fill="currentColor" stroke="none">black → COM</text>
<path d="M120 88V100H60V110"/>
<polyline points="60,110 60,120 66,122.5 54,127.5 66,132.5 54,137.5 66,142.5 54,147.5 60,150 60,160"/>
<text x="44" y="140" text-anchor="end" fill="currentColor" stroke="none">R</text>
<path d="M60 160V173.0M52 173.0H68L60 185.0Z M52 185.0H68M60 185.0V200"/><path d="M71 174.0l7 -6m-4 0h4v4M71 181.0l7 -6m-4 0h4v4"/>
<path d="M60 200V208M50 208H70M54 212H66M58 216H62"/>
<path d="M290 22H310M300 22V30"/><text x="300" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M300 30V52"/>
<circle cx="300" cy="70" r="18"/>
<text x="300" y="75" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">A</text>
<path d="M300 88V140"/>
<path d="M300 140V148M290 148H310M294 152H306M298 156H302"/>
<path d="M270 40L330 100M330 40L270 100" stroke-width="3"/>
<text x="300" y="185" text-anchor="middle" fill="currentColor" stroke="none">never: ammeter across a supply</text>
<text x="300" y="202" text-anchor="middle" fill="currentColor" stroke="none">(≈ short circuit → fuse blows)</text>
</svg>
<figcaption>ซ้าย: วัดกระแสต้องตัดวงจรแล้วให้กระแสไหลผ่านมิเตอร์ (อนุกรม) ขวา: ห้ามต่อมิเตอร์โหมดกระแสคร่อมแหล่งจ่าย</figcaption>
</figure>

---

## แนวคิด (2) — ขั้นตอนที่ปลอดภัย และทางเลือกที่ดีกว่า

```text
1. ปิดไฟ
2. ย้ายสายแดงไปช่อง mA (หรือ 10A ถ้ากระแสมาก) หมุนปุ่มไปโหมดกระแสไฟตรง
3. ตัดวงจรหนึ่งจุด ต่อมิเตอร์เข้าไปแทน (แดงฝั่งกระแสไหลเข้า ดำฝั่งไหลออก)
4. เปิดไฟ อ่านค่า
5. ปิดไฟ ถอดมิเตอร์ ต่อวงจรคืน แล้ว "ย้ายสายแดงกลับช่อง VΩ"
```

**ทางเลือกที่ปลอดภัยกว่า** วัดแรงดันคร่อมตัวต้านทานที่รู้ค่าอยู่แล้ว แล้วใช้ I = V_R / R — ไม่ต้องตัดวงจร ไม่ต้องย้ายสาย และไม่มีทางทำฟิวส์ขาด งานอุตสาหกรรมนิยมใส่ **shunt resistor** ค่าต่ำไว้ตั้งแต่ออกแบบ

---

## แนวคิด (3) — ทำไมโหมดกระแสอันตราย

ในโหมดกระแส มิเตอร์คือตัวต้านทานค่าต่ำมาก (shunt) — **มิเตอร์ในโหมดกระแสจึงแทบเป็นสายไฟเส้นหนึ่ง**

| สถานการณ์ | กระแสที่อยากไหล | ผล |
|---|---|---|
| ช่อง mA (สมมุติ 5 Ω) คร่อมไฟ 3.3 V | 0.66 A | เกินฟิวส์ ฟิวส์ขาด |
| ช่อง 10A (สมมุติ 0.01 Ω) คร่อมแบตเตอรี่ลิเทียม 3.7 V | หลายสิบแอมแปร์ | สายร้อนจัด แบตเสียหายหรือไฟลุก |
| ช่อง A คร่อมไฟบ้าน | มหาศาล | ประกายไฟรุนแรง อันตรายถึงชีวิต |

**สายแดงอยู่ช่อง mA หรือ A เมื่อไร ห้ามแตะคร่อมอะไรทั้งสิ้น**

---

## แนวคิด (4) — ทำไมค่าที่วัดได้ไม่เท่ากับที่คำนวณ

**burden voltage** shunt ภายในมิเตอร์ทำให้กระแสในวงจรลดลงเล็กน้อยเมื่อใส่มิเตอร์เข้าไป

```text
LED แดง 3.3 V, V_f=2.0V, R=270Ω → คำนวณได้ 4.81 mA
มิเตอร์ mA มีความต้านทานรวม 10 Ω (สมมุติ):
I = 1.3 V / (270 + 10) Ω = 4.64 mA      ต่ำกว่าเดิมราว 3.6%
```

แหล่งความต่างอื่น: ความคลาด ±5% ของตัวต้านทาน, 3V3 จริงไม่ใช่ 3.30 V พอดี, V_f ขึ้นกับกระแสและอุณหภูมิ

**นิสัยที่ดี** คำนวณใหม่ด้วยค่าที่วัดได้จริง (R, 3V3, V_f) ก่อนเทียบกับค่าที่มิเตอร์อ่านได้

---

## ตัวอย่างสมบูรณ์ — สองวิธี หนึ่งวงจร

```text
วงจร 3V3 → 270 Ω → LED สีแดง → GND

1. วัดค่าจริงก่อน   R วัดได้ 268 Ω, 3V3=3.29V, V_f=1.98V
2. คำนวณใหม่        (3.29−1.98)/268 = 4.89 mA
3. วิธีที่ 1: V คร่อม R  วัดได้ 1.31 V → 1.31/268 = 4.89 mA ตรงกับคำนวณใหม่
4. วิธีที่ 2: มิเตอร์อนุกรม  อ่านได้ 4.71 mA
5. อธิบาย   ต่าง 0.18 mA (3.6%) ถ้ามิเตอร์มี R ภายใน≈10Ω:
            (3.29−1.98)/(268+10) = 4.71 mA พอดี — เป็นผลจาก burden ไม่ใช่วงจรผิด
6. ปิดงาน   ปิดไฟ ต่อวงจรคืน ย้ายสายแดงกลับ VΩ
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. ต้องการวัดกระแสราว 20 mA และราว 2 A ควรเสียบสายแดงช่องไหนในแต่ละกรณี
2. ช่อง mA มีความต้านทานภายใน 5 Ω และฟิวส์ 400 mA ถ้าเผลอแตะสายคร่อมไฟ 3.3 V จะมีกระแสเท่าไร เกิดอะไรขึ้น

**แล็บ** ต่อวงจร 3V3 → 270 Ω → LED → GND (เว้นช่องว่างไว้หนึ่งจุด)

1. วัดค่าจริงของ R ก่อนต่อวงจร · **ทาย** กระแสทั้งแบบค่าบนตัวและค่าที่วัดได้
2. วิธีที่ 1: วัด V_R แล้วคำนวณ I = V_R/R
3. วิธีที่ 2: ย้ายสายแดงไปช่อง mA ต่ออนุกรมแทนช่องว่าง วัดค่า
4. **ปิดงานทันที** ย้ายสายแดงกลับ VΩ ก่อนทำข้อถัดไป แล้วทำซ้ำกับ 1 kΩ

---

## เช็กความเข้าใจ

1. เรียงขั้นตอนการวัดกระแสของ LED ด้วยมิเตอร์แบบอนุกรมให้ถูกลำดับ — (ปิดไฟ · ย้ายสายแดงไป mA แล้วต่ออนุกรม · เปิดไฟอ่านค่า · ปิดไฟถอดมิเตอร์ · ย้ายสายแดงกลับ VΩ)

2. ทำไมการแตะสายวัดคร่อมแหล่งจ่ายขณะมิเตอร์อยู่ในโหมดกระแสจึงอันตราย
   - ก) จะแสดงค่าติดลบ · ข) มิเตอร์มีความต้านทานภายในต่ำมาก จึงเท่ากับลัดวงจรแหล่งจ่าย · ค) จะวัดแรงดันได้ไม่แม่น · ง) ไม่อันตราย มิเตอร์เปลี่ยนโหมดเอง

3. คำนวณกระแส LED ได้ 4.81 mA แต่ต่อมิเตอร์อนุกรมวัดได้ 4.64 mA คำอธิบายใดสมเหตุสมผลที่สุด
   - ก) LED เสีย · ข) มิเตอร์เสีย · ค) ความต้านทานภายในของมิเตอร์ (burden) รวมกับความคลาดของตัวต้านทานและแรงดันจริง · ง) กฎของโอห์มใช้กับ LED ไม่ได้

---

## ไปต่อ

มัลติมิเตอร์ตอบได้ดีว่า "แรงดันหรือกระแสเฉลี่ยเท่าไร" แต่มองไม่เห็นสัญญาณที่เปลี่ยนเร็ว โมดูลถัดไป [จับสัญญาณดิจิทัลครั้งแรก](../../m04-logic-analyzer/l01-capture-a-signal/README.md) จะใช้ logic analyzer ดูสัญญาณที่เปลี่ยนเป็นล้านครั้งต่อวินาที

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
