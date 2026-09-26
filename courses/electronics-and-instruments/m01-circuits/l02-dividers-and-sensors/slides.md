---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก"
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

# บทเรียน 1.2 — วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก

## เข้าใจลูกบิดบนบอร์ดในฐานะวงจรแบ่งแรงดัน และแปลงค่าที่ ADC อ่านได้เป็นโวลต์

**โมดูล 1 — วงจรและอิเล็กทรอนิกส์พื้นฐาน**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณแรงดันขาออกของวงจรแบ่งแรงดันจากค่าตัวต้านทานสองตัว
2. แปลงค่าที่ ADC อ่านได้เป็นแรงดันจากความละเอียดและแรงดันอ้างอิง แล้วเทียบกับมัลติมิเตอร์
3. อธิบายผลของความต้านทานขาเข้าของ ADC (และของมิเตอร์) ต่อความแม่นยำของวงจรแบ่งแรงดัน

---

## ก่อนเริ่ม

- ผ่านบทเรียน [แรงดัน กระแส และความต้านทาน](../l01-voltage-current-resistance/README.md) มาแล้ว
- แล็บ: เบรดบอร์ด สายจัมเปอร์ ตัวต้านทาน 10 kΩ, 12 kΩ และ 1 MΩ สองตัว มัลติมิเตอร์ และบอร์ด
- ส่วนที่อ่านลูกบิดด้วย ADC ใช้ตัวอย่าง QWA309 ของ Developer Hub ซึ่งรันได้บน TESAIoT Dev Kit เท่านั้น

---

## ดูของจริงก่อน

เปิดตัวอย่าง QWA309 Potentiometer Monitor แล้ว flash ลงบอร์ด — จอแสดงการ์ดสี่ใบของลูกบิด (potentiometer) แต่ละใบมีค่าดิบ (raw) แรงดัน และเปอร์เซ็นต์

ลองหมุนลูกบิดจนสุดทั้งสองทาง แล้วสังเกต

- ค่าดิบวิ่งตั้งแต่ราว 0 ถึงราว 4095 — ทำไมต้องเป็นเลขนี้
- แรงดันสูงสุดที่จอแสดงคือราว 1.8 V ไม่ใช่ 3.3 V — ทำไม

ลูกบิดทั้งสี่ตัวต่อกับขา P15.4 ถึง P15.7 อ่านด้วย SAR ADC ขนาด 12 บิต แรงดันอ้างอิง 1.8 V

---

## แนวคิด (1) — วงจรแบ่งแรงดัน

<figure>
<svg viewBox="0 0 440 222" width="440" role="img" aria-label="วงจรแบ่งแรงดันป้อนขา ADC และโพเทนชิโอมิเตอร์ที่เป็นวงจรแบ่งแรงดันปรับได้" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M60 22H80M70 22V30"/><text x="70" y="17" text-anchor="middle" fill="currentColor" stroke="none">V_in</text>
<path d="M70 30V40"/>
<polyline points="70,40 70,50 76,52.5 64,57.5 76,62.5 64,67.5 76,72.5 64,77.5 70,80 70,90"/>
<text x="86" y="70" fill="currentColor" stroke="none">R1 (top)</text>
<path d="M70 90V110M70 100H150"/>
<circle cx="70" cy="100" r="2.5" fill="currentColor"/>
<rect x="150" y="88" width="70" height="24" rx="3"/>
<text x="185" y="105" text-anchor="middle" fill="currentColor" stroke="none">ADC pin</text>
<text x="110" y="94" text-anchor="middle" fill="currentColor" stroke="none">V_out</text>
<polyline points="70,110 70,120 76,122.5 64,127.5 76,132.5 64,137.5 76,142.5 64,147.5 70,150 70,160"/>
<text x="86" y="140" fill="currentColor" stroke="none">R2 (bottom)</text>
<path d="M70 160V168M60 168H80M64 172H76M68 176H72"/>
<text x="20" y="210" fill="currentColor" stroke="none">V_out = V_in × R2 / (R1 + R2)</text>
<path d="M320 22H340M330 22V30"/><text x="330" y="17" text-anchor="middle" fill="currentColor" stroke="none">1.8 V</text>
<path d="M330 30V60"/>
<polyline points="330,60 330,85 336,87.5 324,92.5 336,97.5 324,102.5 336,107.5 324,112.5 330,115 330,140"/>
<path d="M370 100L339 100M345.4 97.3L339 100L345.4 102.7"/>
<path d="M370 100H390"/>
<text x="394" y="104" fill="currentColor" stroke="none">wiper</text>
<path d="M330 140V170"/>
<path d="M330 170V178M320 178H340M324 182H336M328 186H332"/>
<text x="318" y="104" text-anchor="end" fill="currentColor" stroke="none">pot</text>
</svg>
<figcaption>ซ้าย: วงจรแบ่งแรงดันสองตัวต้านทาน ขวา: โพเทนชิโอมิเตอร์คือวงจรแบ่งแรงดันที่ขากลาง (wiper) เลื่อนได้</figcaption>
</figure>

```text
V_out = V_in × R2 / (R1 + R2)
```

---

## แนวคิด (2) — ตัวอย่างและออกแบบย้อนกลับ

**ตัวอย่าง** 3.3 V, R1 = 10 kΩ (บน), R2 = 4.7 kΩ (ล่าง)

```text
V_out = 3.3 × 4.7 / (10 + 4.7) = 3.3 × 0.3197 = 1.055 V
```

**ออกแบบย้อนกลับ** อยากได้ 1.8 V จาก 3.3 V สัดส่วนที่ต้องการคือ 1.8 / 3.3 = 0.545 ถ้าเลือก R1 = 10 kΩ แล้ว R2 = 12 kΩ

```text
3.3 × 12 / 22 = 1.800 V พอดี — คู่นี้จะต่อจริงในแล็บ
```

โพเทนชิโอมิเตอร์คือตัวต้านทานที่ขากลาง (wiper) เลื่อนได้ ปลายสองข้างต่อคร่อมแหล่งจ่าย หมุนไปได้ 30% ของระยะ ขากลางก็ได้ราว 30% ของแรงดันที่คร่อมอยู่

---

## แนวคิด (3) — ADC: แรงดัน ↔ ตัวเลข

ADC แบบ N บิตแบ่งช่วง 0 ถึง V_ref ออกเป็น 2^N ขั้น — ADC 12 บิต มี 4096 ขั้น (ค่าดิบ 0–4095)

```text
1 LSB = 1.8 V / 4096 = 0.000439 V ≈ 0.44 mV

V = raw × V_ref / 2^N
raw 2048 → 2048 × 1.8 / 4096 = 0.900 V   (ครึ่งหนึ่งของช่วงพอดี)
raw 3000 → 3000 × 1.8 / 4096 = 1.318 V
```

**เปอร์เซ็นต์ไม่ต้องใช้ V_ref** = 100 × raw / เต็มสเกล — ถ้า V_ref จริงต่างจากที่โค้ดสมมุติ แรงดันที่คำนวณจะผิดตามสัดส่วนนั้น แต่เปอร์เซ็นต์ยังถูก จึงต้องเทียบกับมัลติมิเตอร์อย่างน้อยหนึ่งครั้ง

---

## แนวคิด (4) — เมื่อวงจรแบ่งแรงดันถูกโหลด

มองจากขา V_out วงจรแบ่งแรงดันเหมือนแหล่งจ่าย V_th ที่มีความต้านทานภายใน R_th = R1 ∥ R2 (วงจรสมมูลเทวินิน)

```text
V_out = V_th × R_load / (R_load + R_th)
```

**ตัวอย่าง** 3.3 V แบ่งด้วย 100 kΩ สองตัว ไม่มีโหลด = 1.65 V, R_th = 50 kΩ

| โหลด | V_out | คลาดจาก 1.65 V |
|---|---|---|
| 1 MΩ | 1.571 V | −4.8% |
| 10 MΩ (มัลติมิเตอร์ทั่วไป) | 1.642 V | −0.5% |

กฎหยาบ: ให้ความต้านทานของโหลดมากกว่า R_th อย่างน้อยราว 100 เท่า ความคลาดจะต่ำกว่าราว 1%

---

## ตัวอย่างสมบูรณ์ — ออกแบบวงจรอ่านเซนเซอร์

**โจทย์** เซนเซอร์ให้ 0–5 V อ่านด้วย ADC 12 บิต V_ref = 1.8 V

```text
ขั้นที่ 1  เลือกสัดส่วน 1/3 ด้วย R1 = 20 kΩ, R2 = 10 kΩ
           V_adc สูงสุด = 5 × 10 / 30 = 1.667 V   ต่ำกว่า 1.8 V เหลือที่ว่างราว 7%

ขั้นที่ 2  ตรวจผลข้างเคียง
           กระแสจากเซนเซอร์ = 5 V / 30 kΩ = 0.167 mA
           R_th = 20 ∥ 10 = 6.67 kΩ, โหลด 10 MΩ คลาดเพียง 0.07%

ขั้นที่ 3  แปลงค่ากลับ raw = 3500
           V_adc = 3500 × 1.8 / 4096 = 1.538 V
           V_sensor = V_adc × 3 = 4.614 V

ขั้นที่ 4  เทียบกับมิเตอร์ ถ้าต่างเกินราว 1% สงสัย R จริง, V_ref จริง, เวลาสุ่มของ ADC
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. 3.3 V, R1 = 4.7 kΩ (บน), R2 = 10 kΩ (ล่าง) V_out เท่าไร
2. ADC 12 บิต V_ref = 1.8 V raw 1024 คือกี่โวลต์ raw สูงสุด 4095 คือกี่โวลต์ ทำไมไม่ถึง 1.8 V พอดี

**แล็บ ส่วน A** วงจรแบ่งแรงดันบนเบรดบอร์ด: R1 = 10 kΩ จาก 3V3 → จุด M, R2 = 12 kΩ จาก M → GND

1. **ทาย** แรงดันที่จุด M (1.80 V ถ้า 3V3 = 3.30 V พอดี) แล้ววัดจริง
2. เปลี่ยนตัวต้านทานเป็น 1 MΩ ทั้งสองตัว แล้วคำนวณย้อนหาความต้านทานขาเข้าของมิเตอร์จากค่าที่วัดได้

**แล็บ ส่วน B** (TESAIoT Dev Kit) รัน QWA309 Potentiometer Monitor หมุนลูกบิด 4 ตำแหน่ง จดค่า raw และ mV เทียบกับที่คำนวณเอง

---

## เช็กความเข้าใจ

1. วงจรแบ่งแรงดันจาก 3.3 V ใช้ R1 = 10 kΩ (บน) และ R2 = 20 kΩ (ล่าง) แรงดันขาออกเป็นเท่าไร
   - ก) 1.1 V · ข) 2.2 V · ค) 1.65 V · ง) 3.3 V

2. ADC 12 บิต แรงดันอ้างอิง 1.8 V อ่านได้ค่าดิบ 2048 แรงดันที่ขาประมาณเท่าไร
   - ก) 0.90 V · ข) 1.65 V · ค) 2.048 V · ง) 0.45 V

3. วงจรแบ่งแรงดัน 100 kΩ สองตัวจาก 3.3 V ต่อเข้ากับโหลด 1 MΩ แรงดันขาออกประมาณเท่าไร
   - ก) 1.65 V · ข) 1.57 V · ค) 1.50 V · ง) 0.30 V

---

## ไปต่อ

บทเรียนถัดไป [ชิ้นส่วนพื้นฐาน](../l03-components/README.md) — ใช้กฎของโอห์มกับหลอด LED ดูว่าตัวเก็บประจุกับไดโอดทำหน้าที่อะไร และเลือกทรานซิสเตอร์เมื่อขาของไมโครคอนโทรลเลอร์จ่ายกระแสไม่พอ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
