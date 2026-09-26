---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — จับสัญญาณดิจิทัลครั้งแรก"
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

# บทเรียน 4.1 — จับสัญญาณดิจิทัลครั้งแรก

## ต่อ logic analyzer เลือกอัตราสุ่มตัวอย่างและ trigger แล้ววัดเวลาของสัญญาณ

**โมดูล 4 — Logic analyzer และ protocol analyzer**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ต่อสายกราวด์และสายสัญญาณของ logic analyzer กับบอร์ดได้ถูกต้อง
2. เลือกอัตราสุ่มตัวอย่างที่เร็วพอสำหรับสัญญาณที่ต้องการวัด และอธิบายผลเมื่อช้าเกินไป
3. วัดความกว้างพัลส์และความถี่ของสัญญาณไฟกะพริบจากภาพที่จับได้

---

## ก่อนเริ่ม

- logic analyzer ราคาประหยัดที่ใช้กับ sigrok ได้ (fx2lafw), ติดตั้ง PulseView
- TESAIoT Dev Kit ที่ flash QWA309 Header I/O Test

> **ความปลอดภัยของเครื่องมือ** logic analyzer ราคาประหยัดส่วนใหญ่ไม่มีการแยกกราวด์ กราวด์ของมันคือกราวด์ของคอมพิวเตอร์ ห้ามต่อกับวงจรที่กราวด์ไม่ใช่กราวด์เดียวกับคอมพิวเตอร์ หรือวงจรที่มีไฟบ้าน

---

## ดูของจริงก่อน

กดปุ่ม **PWM Out** — จอเขียนว่ากำลังขับ P13.3 และ P13.4 เป็นคู่กลับเฟส 50 รอบ ครึ่งคาบเวลา 20 ms "ความถี่ประมาณ 25 Hz"

ต่อ LED ไว้ที่ P13.3 จะเห็นไฟกะพริบถี่จนเกือบดูเหมือนติดค้าง — ตาบอกได้แค่ "กะพริบเร็ว" แต่ตอบไม่ได้ว่า 25 Hz จริงไหม แต่ละพัลส์กว้างเท่ากันหรือเปล่า มัลติมิเตอร์ก็ตอบไม่ได้เพราะมันเฉลี่ยค่า เครื่องมือที่ตอบได้คือ logic analyzer

---

## แนวคิด (1) — logic analyzer ทำงานอย่างไร

logic analyzer อ่านแรงดันของแต่ละช่องเป็นจังหวะคงที่ เทียบกับเกณฑ์ (threshold) แล้วเก็บเป็น 0 หรือ 1 — มันไม่รู้แรงดันจริง รู้แค่สูงหรือต่ำกว่าเกณฑ์

**กราวด์ก่อนเสมอ** ถ้าไม่ได้ต่อ GND เข้ากับ GND ของบอร์ด เครื่องไม่มีจุดอ้างอิง ภาพที่ได้จะมั่วหรือเป็นเส้นตรง ลำดับที่ดี: ต่อ GND → ต่อสายสัญญาณ → เปิดโปรแกรม (และถอดกลับด้าน)

**ระดับแรงดันต้องเข้ากัน** สัญญาณ 3.3 V เกือบทุกรุ่นอ่านได้ สัญญาณ 1.8 V บางรุ่นอยู่ใกล้เกณฑ์จนไม่น่าเชื่อถือ

---

## แนวคิด (2) — อัตราสุ่มตัวอย่างต้องเร็วแค่ไหน

กฎหยาบ: **อย่างน้อย 4 ตัวอย่างต่อพัลส์ที่แคบที่สุด** วัดเวลาแม่นให้ใช้ 10 ตัวอย่างขึ้นไป

| สัญญาณ | ช่วงที่แคบที่สุด | อัตราสุ่มที่เหมาะ |
|---|---|---|
| PWM 25 Hz ของโปรแกรมทดสอบ | 20 ms | 10 kHz ก็พอ |
| UART 115200 baud | 8.68 µs | 1 MHz (8.7 ตัวอย่าง/บิต) |
| I2C 400 kHz | ราว 1.25 µs | 4–10 MHz |

**ถ้าช้าเกินไป** พัลส์แคบกว่า T_s อาจหายไปเลย หรือเกิด **aliasing** — สัญญาณเร็วที่ถูกสุ่มช้าเกินไปกลายเป็นภาพของสัญญาณที่ช้ากว่าและไม่มีอยู่จริง

---

## แนวคิด (3) — aliasing: ภาพที่ดูสะอาดแต่โกหก

```text
คลื่นสี่เหลี่ยม 1 kHz สุ่มที่ 1.1 kHz
ภาพที่ได้ครบรอบทุก 11 ตัวอย่าง = 1100/11 = 100 Hz
ความถี่ปลอมนี้คือ |1100 − 1000| Hz
```

ภาพดูสะอาดและน่าเชื่อ — นั่นคือเหตุผลที่ aliasing อันตราย มันไม่ได้ดูเหมือนความผิดพลาด

**หน่วยความจำ** จำนวนตัวอย่าง = f_s × เวลาที่จับ — สุ่ม 1 MHz นาน 5 s ได้ 5 ล้านตัวอย่างต่อช่อง ตั้งเร็วเกินจำเป็นกินหน่วยความจำและจับได้สั้นลง

---

## แนวคิด (4) — trigger และการวัดเวลา

**trigger** คือเงื่อนไข "เริ่มเก็บตรงนี้" เช่น ขอบขาขึ้นของช่อง 0 — ทำให้เหตุการณ์อยู่ตำแหน่งเดิมทุกครั้งที่จับ

```text
ความกว้างพัลส์ (t_high) = เวลาขอบขาลง − เวลาขอบขาขึ้นก่อนหน้า
คาบเวลา (T)             = เวลาขอบขาขึ้นถัดไป − เวลาขอบขาขึ้นแรก
ความถี่ (f)              = 1 / T
duty cycle              = t_high / T
```

วัดหลายคาบเวลาแล้วหารด้วยจำนวนคาบเวลาจะแม่นกว่าวัดคาบเวลาเดียว เพราะความคลาดราวหนึ่ง T_s ที่ขอบถูกหารเฉลี่ยไปด้วย

---

## ตัวอย่างสมบูรณ์ — จับสัญญาณ PWM Out

```text
1. รู้ก่อนว่าคาดอะไร   คาบเวลา ≈ 40 ms, ความถี่ ≈ 25 Hz, duty ≈ 50%, 50 รอบ
2. ต่อสาย   GND→GND, CH0→P13.3, CH1→P13.4
3. เลือกอัตราสุ่ม   ช่วงแคบสุด 20 ms → 10 kHz ได้ 200 ตัวอย่าง/ช่วง (เกินพอ)
4. เลือกเวลาจับ   ≥3 s
5. ตั้ง trigger   ขอบขาขึ้นของ CH0
6. วัด (ตัวอย่าง)  ขอบขึ้นลูกที่ 11 ที่ 401.0 ms
   คาบเวลาเฉลี่ย = 401.0/10 = 40.10 ms, f = 24.94 Hz, duty = 20.05/40.10 = 50.0%
7. ตีความ   ยาวกว่า 40 ms อยู่ 0.25% — มาจากเวลาของคำสั่งซอฟต์แวร์ที่หน่วงเวลา
8. นับรอบ   ต้องได้ 50 ขอบพอดี และ CH0/CH1 ต้องไม่เป็น 1 พร้อมกัน
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. จะจับ UART 115200 baud ให้ได้ ≥8 ตัวอย่าง/บิต ต้องใช้อัตราสุ่มอย่างน้อยเท่าไร
2. คลื่นสี่เหลี่ยม 900 Hz ถูกสุ่มที่ 1 kHz ภาพที่เห็นจะมีความถี่เท่าไร

**แล็บ ส่วน A** สัญญาณกะพริบช้า (GPIO Out) — sample rate 10 kHz, 20 s, trigger ขอบขาขึ้น CH0 **ทาย** ความกว้างพัลส์ก่อนดูผล (ยาวหรือสั้นกว่า 700 ms)

**แล็บ ส่วน B** สัญญาณเร็วขึ้น (PWM Out) — วัดคาบเวลาเฉลี่ย 10 คาบเวลา, ความถี่, duty แล้วลองลดอัตราสุ่มจนเห็นความผิดปกติ

---

## เช็กความเข้าใจ

1. ต่อสายสัญญาณของ logic analyzer เข้าขาของบอร์ดแล้ว แต่ลืมต่อสาย GND ผลที่น่าจะเกิดคืออะไร
   - ก) ภาพถูกต้องปกติ เพราะ USB ต่อกราวด์ให้เอง · ข) ภาพมั่ว เป็นเส้นคงที่ หรือเปลี่ยนเมื่อขยับสาย · ค) บอร์ดจะรีเซ็ต · ง) เครื่องวัดแรงดันจริงได้แทน 0/1

2. ต้องการจับสัญญาณ UART 115200 baud ให้ได้อย่างน้อย 8 ตัวอย่างต่อบิต อัตราสุ่มข้อใดต่ำที่สุดที่ใช้ได้
   - ก) 115.2 kHz · ข) 230.4 kHz · ค) 500 kHz · ง) 1 MHz

3. คลื่นสี่เหลี่ยม 1 kHz ถูกสุ่มที่ 1.1 kHz ภาพที่ได้จะแสดงความถี่เท่าไร
   - ก) 1 kHz · ข) 1.1 kHz · ค) 100 Hz · ง) 2.1 kHz

---

## ไปต่อ

บทเรียนถัดไป [ถอดรหัส I2C และ UART](../l02-decode-i2c-and-uart/README.md) — ให้โปรแกรมอ่านความหมายของสัญญาณแทนเรา ตั้งแต่ address บน I2C ไปจนถึงไบต์บน UART

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
