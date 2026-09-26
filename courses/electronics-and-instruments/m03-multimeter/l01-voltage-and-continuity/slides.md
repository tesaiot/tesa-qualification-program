---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — วัดแรงดันและความต่อเนื่อง"
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

# บทเรียน 3.1 — วัดแรงดันและความต่อเนื่อง

## เลือกโหมดและย่านวัด วัดแรงดันขนานกับจุดที่ต้องการ และตรวจสายขาดหรือลัดวงจรด้วยโหมดความต่อเนื่อง

**โมดูล 3 — มัลติมิเตอร์**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. วัดแรงดันที่จุดทดสอบบนบอร์ดโดยเลือกโหมดและย่านวัดถูกต้อง และบอกได้ว่าค่าที่อ่านได้แม่นแค่ไหน
2. ตรวจความต่อเนื่องของสายและหาจุดลัดวงจรบนวงจรที่ปิดไฟแล้ว

---

## ก่อนเริ่ม

- มัลติมิเตอร์แบบดิจิทัลพร้อมคู่มือ (ต้องอ่านสเปกความแม่นยำ)
- บอร์ด สาย USB เบรดบอร์ดที่ยังมีวงจรจากบทเรียน [แรงดัน กระแส และความต้านทาน](../../m01-circuits/l01-voltage-current-resistance/README.md)

> **ความปลอดภัย** หลักสูตรนี้ **ไม่วัดไฟบ้าน** ไม่ว่ากรณีใด มัลติมิเตอร์และสายวัดที่ดีพิมพ์พิกัด measurement category ไว้ (CAT II/III ตาม IEC 61010) แม้งานของเราเป็นไฟ 3.3 V เลือกเครื่องที่มีพิกัดไว้ก่อนเป็นนิสัยที่ดี

---

## ดูของจริงก่อน

หยิบมัลติมิเตอร์ขึ้นมาดูโดยยังไม่เสียบสาย

- ช่องเสียบสายมีกี่ช่อง ช่องไหนคือ COM, VΩ, mA/µA และมีช่อง 10A แยกไหม
- ปุ่มหมุนมีสัญลักษณ์ V⎓, V~, Ω, ความต่อเนื่อง, ไดโอด ตรงไหนบ้าง
- เครื่องเลือกย่านเอง (มีตัวเลข 200m, 2, 20, 200) หรือเลือกย่านอัตโนมัติ (AUTO)

จดคำตอบไว้ เราจะใช้ตอนเลือกย่านวัดในหัวข้อถัดไป

---

## แนวคิด (1) — โหมด ช่องเสียบ และความแม่นยำ

| สิ่งที่วัด | ปุ่มหมุน | สายแดง | ต่ออย่างไร |
|---|---|---|---|
| แรงดันไฟตรง | V⎓ | VΩ | ขนาน (คร่อมจุดที่วัด) |
| ความต้านทาน/ความต่อเนื่อง | Ω | VΩ | คร่อมชิ้นส่วน **ขณะปิดไฟ** |
| กระแส | mA/A | mA/10A | อนุกรม |

**เลือกย่านวัด** ย่านที่เล็กที่สุดที่ยังมากกว่าค่าที่คาด — เลือกผิดได้แค่ OL (overload) ไม่มีอะไรเสีย

```text
ความคลาด = ±(0.5% × 3.29 V + 2 × 0.01 V) = ±0.036 V
ค่าจริงอยู่ระหว่างราว 3.25 ถึง 3.33 V
```

---

## แนวคิด (2) — วัดแรงดัน: ต่อขนาน อ้างอิงกราวด์

<figure>
<svg viewBox="0 0 380 190" width="380" role="img" aria-label="มัลติมิเตอร์วัดแรงดันต่อขนานคร่อมตัวต้านทาน" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="64" y="70" text-anchor="end" fill="currentColor" stroke="none">R1</text>
<path d="M80 90V100"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<polyline points="80,100 80,110 86,112.5 74,117.5 86,122.5 74,127.5 86,132.5 74,137.5 80,140 80,150"/>
<text x="64" y="130" text-anchor="end" fill="currentColor" stroke="none">R2</text>
<path d="M80 150V160"/>
<circle cx="80" cy="160" r="2.5" fill="currentColor"/>
<path d="M80 160V168M70 168H90M74 172H86M78 176H82"/>
<path d="M80 100H160V112M80 160H160V148"/>
<circle cx="160" cy="130" r="18"/>
<text x="160" y="135" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">V</text>
<text x="186" y="112" fill="currentColor" stroke="none">red → VΩ jack</text>
<text x="186" y="152" fill="currentColor" stroke="none">black → COM</text>
<text x="186" y="132" fill="currentColor" stroke="none">meter across R2 (parallel)</text>
</svg>
<figcaption>วัดแรงดันด้วยการต่อขนาน (คร่อม) จุดที่ต้องการ ไม่ต้องตัดวงจร</figcaption>
</figure>

ไฟ 3.3 V ควรอยู่ 3.14–3.47 V (±5%), ไฟ 1.8 V ควรอยู่ 1.71–1.89 V

---

## แนวคิด (3) — ความต่อเนื่องและความต้านทาน (ปิดไฟเท่านั้น)

โหมด Ω และความต่อเนื่องปล่อยกระแสเล็ก ๆ ของเครื่องเองผ่านสิ่งที่วัด — **ถอดไฟและรอให้ตัวเก็บประจุคายประจุก่อนเสมอ**

- **โหมดความต่อเนื่อง** ดังเมื่อความต้านทานต่ำกว่าเกณฑ์ — ตรวจสายขาด, รางไฟขาดครึ่งกลาง, ไฟเลี้ยงลัดกราวด์ (ต้อง**ไม่**ดัง)
- **ความต้านทาน in-circuit** เครื่องเห็นทุกทางที่ต่อคร่อมสองจุดนั้น (10 kΩ ∥ 10 kΩ อ่านได้ 5 kΩ — ไม่ได้แปลว่าเสีย)
- **บอร์ดจริงไม่ใช่ 0 หรืออนันต์** ราง 3V3–GND มักได้หลายร้อยโอห์มถึงหลายกิโลโอห์มจาก decoupling caps ที่กำลังถูกประจุ — "ลัดวงจร" คือค่าใกล้ 0 Ω ที่ไม่ขยับ

---

## ตัวอย่างสมบูรณ์ — ไล่หาจุดลัด

**สถานการณ์** วงจร R1=1kΩ, R2=2.2kΩ∥R3=4.7kΩ แรงดันที่จุด A เป็น 0 V ทั้งที่ควรได้ 1.98 V

```text
1. เริ่มจากแหล่งจ่าย   วัดราง 3V3 ได้ 3.29 V — แหล่งจ่ายปกติ
2. วัดทีละจุดตามทางกระแส   ขา R1 ฝั่ง 3V3 = 3.29 V, ฝั่งจุด A = 0 V
                            → แรงดันตกคร่อม R1 ทั้งหมด หรือจุด A ถูกดึงลงกราวด์
3. ถอดไฟ โหมดความต่อเนื่อง   วัด A ถึง GND: ดังทันที ใกล้ 0 Ω
4. หาตัวการ   สายจัมเปอร์เลื่อนไปคอลัมน์ติดกับราง GND
5. แก้แล้วตรวจก่อนเสียบไฟ   ราง 3V3–GND ได้ราว 2.50 kΩ = R1+(R2∥R3)
6. เสียบไฟ วัดซ้ำ   จุด A = 1.97 V อยู่ในความคลาด
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. เครื่องเลือกย่านเองมีย่าน 200mV, 2V, 20V, 200V จะวัดไฟ 1.8 V ควรใช้ย่านไหน ความละเอียดเท่าไร
2. วัดตัวต้านทาน 4.7 kΩ ที่มีอีกตัว 4.7 kΩ ขนานอยู่ในวงจร จะอ่านได้เท่าไร

**แล็บ ส่วน A** (เปิดไฟ) วัดขา 3V3 และ 5V ของ header เทียบกับช่วงที่ยอมรับได้

**แล็บ ส่วน B** (ปิดไฟ) ตรวจความต่อเนื่องของสายจัมเปอร์และรางเบรดบอร์ด แล้วเล่นเกมหาจุดลัด — ให้เพื่อนแอบเสียบสายลัดสองคอลัมน์ แล้วหาให้เจอด้วยจำนวนการวัดน้อยที่สุด (แบ่งวงจรครึ่ง ๆ)

---

## เช็กความเข้าใจ

1. มัลติมิเตอร์แบบเลือกย่านเองมีย่าน 200 mV, 2 V, 20 V, 200 V จะวัดขา 3V3 ควรเลือกย่านใด
   - ก) 200 mV · ข) 2 V · ค) 20 V · ง) 200 V

2. การวัดแรงดันที่ขาหนึ่งเทียบกราวด์ ต้องต่อมัลติมิเตอร์อย่างไร
   - ก) ตัดวงจรแล้วต่ออนุกรม สายแดงที่ช่อง mA · ข) สายดำที่ COM แตะ GND สายแดงที่ช่อง VΩ แตะขาที่วัด โดยไม่ต้องตัดวงจร · ค) ปิดไฟก่อน แล้วใช้โหมด Ω · ง) สายแดงแตะ GND สายดำแตะขาที่วัด แล้วตั้งโหมดความต่อเนื่อง

3. ทำไมต้องถอดไฟก่อนวัดความต้านทานหรือความต่อเนื่อง
   - ก) เพราะมิเตอร์ใช้กระแสของมันเองวัด แรงดันในวงจรจะทำให้ค่าผิดและอาจทำให้เครื่องเสียหาย · ข) เพราะโหมด Ω ใช้แบตเตอรี่มาก · ค) เพราะเสียงจะดังตลอด · ง) ไม่จำเป็นต้องถอดไฟ

---

## ไปต่อ

บทเรียนถัดไป [วัดกระแสอย่างปลอดภัย](../l02-current-safely/README.md) — โหมดที่ทำให้มัลติมิเตอร์เสียบ่อยที่สุด และวิธีที่ทำให้ไม่เกิดกับเครื่องของคุณ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
