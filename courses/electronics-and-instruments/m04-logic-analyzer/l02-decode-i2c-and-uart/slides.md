---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — ถอดรหัส I2C และ UART"
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

# บทเรียน 4.2 — ถอดรหัส I2C และ UART

## ใช้ protocol decoder ของ sigrok อ่านธุรกรรม I2C และเฟรม UART จากบอร์ดจริง

**โมดูล 4 — Logic analyzer และ protocol analyzer**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้
2. ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด

---

## ก่อนเริ่ม

- ต่อ logic analyzer ตั้งอัตราสุ่ม และใช้ trigger ได้แล้ว (บทเรียน [จับสัญญาณดิจิทัลครั้งแรก](../l01-capture-a-signal/README.md))
- TESAIoT Dev Kit ที่ flash QWA309 Header I/O Test — มีปุ่ม **Scan** (สแกนบัส I2C) และ **UART Echo** (ส่งแพ็กเก็ตออกขา UART)

---

## ดูของจริงก่อน

กดปุ่ม **Scan** — โปรแกรมพิมพ์ตารางที่อยู่ 0x08 ถึง 0x77 แล้วสรุป "Found N device(s)"

โปรแกรมรู้ได้อย่างไรว่ามีอุปกรณ์อยู่ที่ที่อยู่ไหน — มันถามทีละที่อยู่ 112 ครั้ง แล้วฟังว่ามีใครตอบ "มีครับ" หรือไม่ วันนี้เราจะดักฟังบทสนทนาทั้ง 112 ครั้งนั้นบนสายจริง และพิสูจน์ด้วยตาตัวเองว่าตารางบนจอพูดความจริง

---

## แนวคิด (1) — เฟรม I2C บนสาย

<figure>
<svg viewBox="0 0 390 170" width="390" role="img" aria-label="เฟรม I2C ส่ง address 0x30 แบบเขียนพร้อม ACK" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="10" y="47" fill="currentColor" stroke="none">SCL</text>
<text x="10" y="107" fill="currentColor" stroke="none">SDA</text>
<polyline points="20,30 80,30 80,55 90,55 90,30 103,30 103,55 116,55 116,30 129,30 129,55 142,55 142,30 155,30 155,55 168,55 168,30 181,30 181,55 194,55 194,30 207,30 207,55 220,55 220,30 233,30 233,55 246,55 246,30 259,30 259,55 272,55 272,30 285,30 285,55 298,55 298,30 311,30 311,55 330,55 330,30 374,30"/>
<polyline points="20,90 70,90 70,115 84,115 84,115 110,115 110,90 136,90 136,90 162,90 162,115 188,115 188,115 214,115 214,115 240,115 240,115 266,115 266,115 292,115 292,115 336,115 336,115 346,115 346,90 374,90"/>
<text x="96.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="122.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="148.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="174.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="200.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="226.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="252.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="278.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">W</text>
<text x="304.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">A</text>
<text x="70" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">S</text>
<text x="168" y="158" text-anchor="middle" fill="currentColor" stroke="none">address 0x30</text>
<text x="278" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">R/W</text>
<text x="306" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">ACK</text>
<text x="346" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">P</text>
</svg>
<figcaption>เฟรม I2C: START (S) คือ SDA ตกขณะ SCL สูง address 7 บิต บิต R/W (0=เขียน) ACK แล้ว STOP (P)</figcaption>
</figure>

**address 7 บิตกับไบต์บนสาย** เลื่อนซ้ายหนึ่งบิตแล้วต่อ R/W — 0x30 เขียนเป็น 0x60 อ่านเป็น 0x61

---

## แนวคิด (2) — ขนาด pull-up ของ I2C

```text
R_p(min) = (V_CC − V_OL(max)) / I_OL = (3.3 − 0.4) V / 3 mA = 967 Ω
R_p(max) = t_r / (0.8473 × C_b)
  Fast-mode 400 kHz (t_r ≤ 300 ns), บัส 100 pF → 3.54 kΩ
  Standard-mode 100 kHz (t_r ≤ 1000 ns), บัส 100 pF → 11.8 kΩ
```

บัส 400 kHz ความจุ 100 pF จึงเลือกได้ระหว่าง 967 Ω ถึง 3.54 kΩ เช่น 2.2 kΩ (ค่าคงที่ 0.8473 = ln(0.7/0.3))

บัส I2C บน header ของ TESAIoT Dev Kit มีชิป CapSense (PSoC 4000T) ตอบที่ **0x08**

---

## แนวคิด (3) — เฟรม UART 8N1

<figure>
<svg viewBox="0 0 400 145" width="400" role="img" aria-label="เฟรม UART 8N1 ของไบต์ 0xA5" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,40 50,40 50,40 50,80 80,80 80,40 110,40 110,80 140,80 140,40 170,40 170,80 200,80 200,80 230,80 230,40 260,40 260,80 290,80 290,40 320,40 320,40 350,40 380,40"/>
<path d="M50 90V96" stroke-dasharray="4 3"/>
<text x="65.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">start</text>
<text x="65.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M320 90V96" stroke-dasharray="4 3"/>
<text x="335.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">stop</text>
<text x="335.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="10" y="30" font-size="11" fill="currentColor" stroke="none">idle</text>
<text x="200" y="135" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0xA5 = 1010 0101, sent LSB first · 115200 baud: 8.68 µs per bit</text>
</svg>
<figcaption>เฟรม UART 8N1: สายว่างเป็น 1 บิตเริ่มเป็น 0 ข้อมูล 8 บิตจาก LSB แล้วบิตหยุดเป็น 1</figcaption>
</figure>

```text
1 บิต = 1/115200 = 8.68 µs   1 ไบต์ = 10 บิต = 86.8 µs   สูงสุด 11,520 ไบต์/วินาที
```

---

## แนวคิด (4) — อ่านภาพสัญญาณให้เจอความผิดพลาด

**ตั้ง baud ผิด** decoder วัดบิตผิดจังหวะ

| สิ่งที่เห็น | สาเหตุที่เป็นไปได้ |
|---|---|
| I2C: address ได้ NACK ทุกที่อยู่ | ไม่มีอุปกรณ์ ไฟเลี้ยงไม่มา SDA/SCL สลับกัน หรือ address ผิด |
| I2C: SDA หรือ SCL ค้างต่ำตลอด | อุปกรณ์ค้างกลางธุรกรรม หรือสายลัดกราวด์ |
| UART: ไม่มีอะไรบน RX ทั้งที่อีกฝั่งส่ง | ต่อ TX เข้า TX (ต้องไขว้ TX กับ RX) หรือลืมต่อ GND ร่วม |

**หา baud จากภาพ** ซูมหาพัลส์ที่แคบที่สุด (หนึ่งบิต) แล้วคำนวณ baud ≈ 1/ความกว้าง — พัลส์ 8.68 µs คือ 115200

---

## ตัวอย่างสมบูรณ์ — ถอดรหัสการสแกนบัส I2C

```text
1. ต่อสาย   GND→GND, CH0→SCL, CH1→SDA
2. อัตราสุ่ม   ยังไม่รู้ความเร็วบัส ใช้ 8 MHz ไว้ก่อน (ครอบคลุมถึง 400 kHz)
3. trigger   ขอบขาลงของ SDA (เกิดตอน START)
4. เพิ่ม decoder   I2C, SCL=CH0, SDA=CH1
5. อ่านผล   Start → Address write: 08 → ACK/NACK → Stop ซ้ำไปเรื่อย ๆ
6. ตรวจ   0x08 ควรได้ ACK (ชิป CapSense) นับที่อยู่ที่ ACK ทั้งหมด เทียบกับ "Found N device(s)"
7. ดูไบต์ดิบ   address แบบ 8 บิต ที่อยู่ 0x08 แบบเขียนต้องเป็น 0x10
```

ถ้าจำนวน ACK ไม่ตรงกับจอ ตรวจก่อนว่าจับครบทั้ง 112 ที่อยู่ และอัตราสุ่มเร็วพอไหม

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. อุปกรณ์มี address 7 บิตเป็น 0x44 ไบต์แรกบนสายแบบเขียนและแบบอ่านเป็นเท่าไร
2. UART 9600 8N1 หนึ่งบิตยาวเท่าไร หนึ่งไบต์ยาวเท่าไร ส่งได้สูงสุดกี่ไบต์ต่อวินาที

**แล็บ ส่วน A** สแกนบัส I2C ตามตัวอย่างสมบูรณ์ เติมตาราง (ความถี่ SCL, จำนวนที่ถูกถาม, ที่อยู่ที่ ACK)

**แล็บ ส่วน B** UART Echo — ตั้ง decoder baud 115200, 8N1 เทียบไบต์ที่ decoder อ่านกับบรรทัด `TX:` บนจอ แล้ว **ทำให้ผิดโดยตั้งใจ** เปลี่ยน baud เป็น 57600 และ 9600 ดูว่า decoder แสดงอะไร

---

## เช็กความเข้าใจ

1. อุปกรณ์มี address 7 บิตเป็น 0x30 ไบต์แรกบนสาย SDA เมื่อมาสเตอร์ขอเขียนคืออะไร
   - ก) 0x30 · ข) 0x60 · ค) 0x61 · ง) 0x18

2. ข้อใดถูกต้องเกี่ยวกับสัญญาณ I2C (เลือกได้มากกว่าหนึ่งข้อ)
   - ก) START คือ SDA ตกลงขณะ SCL สูง · ข) ACK คือฝั่งรับดึง SDA ลงในจังหวะนาฬิกาที่ 9 · ค) ข้อมูลบน SDA ควรเปลี่ยนขณะ SCL สูง · ง) STOP คือ SDA ขึ้นขณะ SCL สูง

3. สัญญาณจริงเป็น 115200 baud แต่ตั้ง decoder ไว้ที่ 9600 จะเห็นอะไร
   - ก) ไบต์ถูกต้องแต่แสดงช้าลง · ข) ไบต์เพี้ยนหรือหายไปจำนวนมาก และมี framing error · ค) decoder ปรับ baud ให้เองอัตโนมัติ · ง) สายสัญญาณจะเปลี่ยนเป็น 9600 ตาม

---

## ไปต่อ

logic analyzer บอกได้ว่าสัญญาณเป็น 0 หรือ 1 เมื่อไร แต่ไม่บอกว่าแรงดันจริงหน้าตาเป็นอย่างไร บทเรียนถัดไป [ออสซิลโลสโคปเบื้องต้น](../../m05-oscilloscope/l01-scope-basics/README.md) จะให้เราเห็นขอบสัญญาณ แรงดันเกิน และสัญญาณรบกวนที่ logic analyzer มองไม่เห็น

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
