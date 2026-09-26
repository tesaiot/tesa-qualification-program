---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — Pull-up, pull-down และปุ่มกด"
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

# บทเรียน 2.2 — Pull-up, pull-down และปุ่มกด

## ต่อปุ่มแบบ active-low ด้วย pull-up และเห็นการเด้งของหน้าสัมผัสจริงบน logic analyzer

**โมดูล 2 — วงจรดิจิทัล**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายว่าทำไมขาเข้าที่ไม่มี pull-up หรือ pull-down จึงอ่านค่าไม่แน่นอน
2. ต่อปุ่มแบบ active-low และอธิบายว่าทำไมกดแล้วอ่านได้ 0
3. วัดระยะเวลาการเด้งของปุ่มด้วย logic analyzer แล้วเลือกเวลากันเด้งจากข้อมูลที่วัดได้

---

## ก่อนเริ่ม

- รู้จัก V_IH และ V_IL จากบทเรียน [ระดับลอจิกและเกตพื้นฐาน](../l01-logic-levels-and-gates/README.md)
- แล็บ: TESAIoT Dev Kit ที่ flash QWA309 Header I/O Test, เบรดบอร์ด, ปุ่มกดขาเสียบ, ตัวต้านทาน 10 kΩ และ 1 kΩ, มัลติมิเตอร์, logic analyzer ราคาประหยัดที่ใช้กับ PulseView ได้
- บทนี้เป็นครั้งแรกที่ใช้ logic analyzer

---

## ดูของจริงก่อน

รันโปรแกรมทดสอบ header แล้วกดปุ่ม **GPIO In** โดย **ไม่ต่ออะไรเข้า header เลย** ขาตั้งเป็นขาเข้าแบบไม่มี pull (high-Z)

ลองเอานิ้วแตะ หรือเอาสายจัมเปอร์ที่ต่อไว้ข้างเดียวแตะใกล้ ๆ ขาเหล่านั้น แล้วดูว่าค่าเปลี่ยนไหม

บางบอร์ดค่าจะแกว่งจนเห็นได้ชัด บางบอร์ดนิ่งอยู่ที่ 0 ทั้งที่ไม่มีอะไรต่อ ทั้งสองแบบบอกเรื่องเดียวกัน: **ค่าที่อ่านจากขาลอยเชื่อถือไม่ได้** นิ่งวันนี้ไม่ได้แปลว่าจะนิ่งพรุ่งนี้

---

## แนวคิด (1) — ขาลอย: ขาเข้าที่ไม่มีใครบอกค่า

ขาเข้าแบบ CMOS มีความต้านทานขาเข้าสูงมาก กระแสรั่วอยู่ในระดับ nA–µA ถ้าไม่มีอะไรต่อ ขาก็เหมือนตัวเก็บประจุเล็ก ๆ ที่ไม่มีใครคุม — ประจุจากนิ้ว สัญญาณข้างเคียง หรือสนามไฟฟ้ารอบตัว ทำให้แรงดันลอยไปที่ไหนก็ได้

ทางแก้: ให้ขาเข้ามี "ค่าเริ่มต้น" เสมอ

- **pull-up** ตัวต้านทานจากขาไปไฟเลี้ยง — ไม่มีใครขับ ขาเป็น 1
- **pull-down** ตัวต้านทานจากขาลง GND — ไม่มีใครขับ ขาเป็น 0

บน PSoC ต้องส่ง out-value = 1 ให้ `Cy_GPIO_Pin_FastInit()` เมื่อใช้โหมด `CY_GPIO_DM_PULLUP` — ถ้าส่ง 0 ขาจะอ่านได้ 0 ตลอดเหมือนปุ่มถูกกดค้าง

---

## แนวคิด (2) — ปุ่มแบบ active-low

<figure>
<svg viewBox="0 0 380 206" width="380" role="img" aria-label="ปุ่มแบบ active-low พร้อมตัวต้านทาน pull-up และตัวต้านทานอนุกรมป้องกันขา" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="96" y="62" fill="currentColor" stroke="none">R_pu</text>
<text x="96" y="76" fill="currentColor" stroke="none">10 kΩ</text>
<path d="M80 90V110M80 100H130"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<polyline points="130,100 140,100 142.5,94 147.5,106 152.5,94 157.5,106 162.5,94 167.5,106 170,100 180,100"/>
<text x="155" y="90" text-anchor="middle" fill="currentColor" stroke="none">1 kΩ</text>
<path d="M180 100H220"/>
<circle cx="223" cy="100" r="3"/>
<text x="232" y="104" fill="currentColor" stroke="none">input pin (P13.0)</text>
<text x="72" y="104" text-anchor="end" fill="currentColor" stroke="none">BTN_N</text>
<path d="M80 110V124.0"/><circle cx="80" cy="124.0" r="2.5"/><path d="M80 140.0V154"/><circle cx="80" cy="140.0" r="2.5"/><path d="M79 138.0L68 122.0"/>
<text x="96" y="136" fill="currentColor" stroke="none">SW</text>
<path d="M80 154V162M70 162H90M74 166H86M78 170H82"/>
<text x="20" y="196" fill="currentColor" stroke="none">released: pin = 1 (3.3 V)   pressed: pin = 0 (0 V)</text>
</svg>
<figcaption>ปุ่มแบบ active-low: ปล่อยปุ่ม pull-up ดึงขาขึ้นเป็น 1 กดปุ่ม สวิตช์ต่อขาลงกราวด์เป็น 0</figcaption>
</figure>

---

## แนวคิด (3) — เลือกค่า R_pu

| R_pu | กระแสตอนกด | ความเร็วขอบ (τ=R×10pF) | แรงดันตกจากรั่ว 1 µA |
|---|---|---|---|
| 1 kΩ | 3.3 mA (เปลือง) | 10 ns | 1 mV |
| 10 kΩ | 0.33 mA | 100 ns | 10 mV |
| 100 kΩ | 33 µA | 1 µs | 0.1 V |
| 1 MΩ | 3.3 µA | 10 µs | 1 V (เหลือ 2.3 V < V_IH) |

**10 kΩ เป็นค่าที่ใช้กันมากที่สุด** — ช่วงราว 4.7 kΩ ถึง 47 kΩ ปลอดภัยทุกด้าน

ตัวต้านทาน **1 kΩ อนุกรมที่ขา** ไม่จำเป็นต่อการทำงาน แต่เป็นประกัน — ถ้าโปรแกรมเผลอตั้งขาเป็นขาออกแล้วมีคนกดปุ่ม จำกัดกระแสไม่เกิน 3.3 mA

---

## แนวคิด (4) — การเด้งของหน้าสัมผัส (contact bounce)

<figure>
<svg viewBox="0 0 380 185" width="380" role="img" aria-label="สัญญาณปุ่มที่เด้งหลายครั้งก่อนนิ่งที่ศูนย์" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="20,40 100,40 100,110 108,110 108,40 113,40 113,110 124,110 124,40 128,40 128,110 141,110 141,40 144,40 144,110 150,110 150,40 360,40"/>
<path d="M100 125V135M150 125V135M100 130H150"/>
<text x="125" y="150" text-anchor="middle" fill="currentColor" stroke="none">bounce</text>
<text x="20" y="30" fill="currentColor" stroke="none">pin (released = 1)</text>
<text x="300" y="102" text-anchor="middle" fill="currentColor" stroke="none">pressed = 0</text>
<text x="20" y="175" fill="currentColor" stroke="none">debounce time &gt; worst bounce you measured</text>
</svg>
<figcaption>ภาพจาก logic analyzer ตอนกดปุ่ม: ขาเปลี่ยนไปมาหลายครั้งในเวลาสั้น ๆ ก่อนนิ่ง</figcaption>
</figure>

**หลักเลือกเวลากันเด้งจากข้อมูล** วัดหลายครั้ง (≥10–20) หาค่าที่นานที่สุด แล้วคูณเผื่อ 2–3 เท่า

---

## ตัวอย่างสมบูรณ์ — ต่อปุ่มและเลือกเวลากันเด้ง

```text
1. วงจร  3V3 → R_pu 10 kΩ → BTN_N → ปุ่ม → GND  และ BTN_N → 1 kΩ → P13.0
2. กระแสตอนกด  3.3 V / 10 kΩ = 0.33 mA  กำลัง = 1.09 mW
3. ระดับที่ขาเห็น  ปล่อย: 3.3 V   กด: 0 V  ห่างจาก V_IH และ V_IL มาก

4. ข้อมูลการเด้ง (ตัวอย่าง วัด 10 ครั้ง, ms)
   0.2  0.4  1.6  0.3  0.9  0.1  2.4  0.5  0.7  1.1
   ค่ามากที่สุด = 2.4 ms

5. เลือกเวลากันเด้ง  2.4 ms × 3 = 7.2 ms → ปัดเป็น 10 ms
6. ตรวจกับโค้ด  อ่านทุก 5 ms ยอมรับเมื่อค่าเดิมต่อเนื่องสองรอบ ≈ 10 ms ตรงตามที่เลือก
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. pull-up 4.7 kΩ ที่ 3.3 V ตอนกดปุ่มมีกระแสเท่าไร กำลังที่ตัวต้านทานเท่าไร
2. วัดการเด้งได้ (ms) 0.6, 0.3, 3.1, 0.8, 1.2 ควรเลือกเวลากันเด้งเท่าไร เพราะอะไรจึงไม่ใช้ค่าเฉลี่ย

**แล็บ ส่วน A** ทดลองขาลอยกับขาที่มี pull-up — ไม่ใส่ R_pu แตะสาย BTN_N ด้วยนิ้ว จดว่าบิตเปลี่ยนกี่ครั้ง แล้วใส่ R_pu 10 kΩ ทำซ้ำ

**แล็บ ส่วน B** วัดการเด้งด้วย logic analyzer — ต่อ CH0 เข้า BTN_N, sample rate ≥ 1 MHz, trigger ที่ขอบขาลง วัดอย่างน้อย 10 ครั้งตอนกดและปล่อย

---

## เช็กความเข้าใจ

1. ขาเข้าที่ไม่ได้ต่ออะไรและไม่ได้เปิด pull-up หรือ pull-down อ่านได้ 0 นิ่งตลอดการทดสอบ ข้อสรุปใดถูกต้อง
   - ก) ขาลอยในบอร์ดนี้เป็น 0 เสมอ ใช้ได้ · ข) ค่าของขาลอยขึ้นกับประจุและสัญญาณรบกวนรอบตัว นิ่งตอนทดสอบไม่รับประกันว่าจะนิ่งตลอดไป · ค) ชิปมี pull-down ภายในเปิดอยู่แน่นอน · ง) ขานั้นเสีย

2. ปุ่มต่อจากขาลง GND และมี pull-up 10 kΩ ไป 3.3 V เมื่อกดปุ่ม ขาอ่านได้อะไร และมีกระแสผ่าน pull-up เท่าไร
   - ก) อ่านได้ 1 กระแส 0 mA · ข) อ่านได้ 0 กระแส 0.33 mA · ค) อ่านได้ 0 กระแส 33 mA · ง) อ่านได้ 1 กระแส 0.33 mA

3. วัดการเด้งของปุ่มได้ 0.3, 0.5, 2.8, 0.4 และ 1.0 ms ควรเลือกเวลากันเด้งเท่าไร
   - ก) 1 ms (ราวค่าเฉลี่ย) · ข) 2.8 ms พอดี · ค) ราว 6–10 ms (ค่ามากที่สุดคูณเผื่อ 2–3 เท่า) · ง) 500 ms

---

## ไปต่อ

โมดูลถัดไปเริ่มที่ [วัดแรงดันและความต่อเนื่อง](../../m03-multimeter/l01-voltage-and-continuity/README.md) — ใช้มัลติมิเตอร์ให้คล่องและปลอดภัย

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
