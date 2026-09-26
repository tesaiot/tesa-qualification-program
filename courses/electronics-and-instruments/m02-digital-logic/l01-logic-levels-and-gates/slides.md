---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ระดับลอจิกและเกตพื้นฐาน"
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

# บทเรียน 2.1 — ระดับลอจิกและเกตพื้นฐาน

## รู้ว่าแรงดันเท่าไรนับเป็น 0 หรือ 1 และทำไมการต่ออุปกรณ์ต่างระดับแรงดันจึงอันตราย

**โมดูล 2 — วงจรดิจิทัล**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่านค่าระดับลอจิกขาเข้าและขาออกจากเอกสารข้อมูลของชิป แล้วบอกได้ว่าสองอุปกรณ์ต่อกันตรงได้หรือไม่
2. เขียนตารางความจริงของเกต AND, OR, NOT, XOR และใช้แก้โจทย์เงื่อนไขง่าย ๆ ได้

---

## ก่อนเริ่ม

- คำนวณวงจรแบ่งแรงดันได้ (บทเรียน [วงจรแบ่งแรงดัน](../../m01-circuits/l02-dividers-and-sensors/README.md))
- แล็บ: TESAIoT Dev Kit ที่ flash ตัวอย่าง QWA309 Header I/O Test, มัลติมิเตอร์, เบรดบอร์ด, ตัวต้านทาน 1 kΩ, 2.2 kΩ, 4.7 kΩ×2, 10 kΩ×3

---

## ดูของจริงก่อน

TESAIoT Dev Kit มี "โลกของแรงดัน" อย่างน้อยสองโลกบนบอร์ดเดียว

- บัส I2C ของเซนเซอร์บนบอร์ดทำงานที่ **1.8 V** — `machine.I2C` ของ MicroPython เป็นอีกบัสหนึ่งที่ **3.3 V** สำหรับบอร์ดเซนเซอร์ภายนอก
- ขาบน header ทำงานที่ **3.3 V** — สังเกตจากป้าย `_3V3` ที่ท้ายชื่อสัญญาณ

สมมุติมีบอร์ดเซนเซอร์ 3.3 V จะต่อบัสไหนได้ และถ้าต่อผิดบัสจะเกิดอะไรขึ้น บทนี้ให้เครื่องมือตอบคำถามนี้ด้วยตัวเลข

---

## แนวคิด (1) — แรงดันเท่าไรนับเป็น 0 หรือ 1

| ค่า | ความหมาย |
|---|---|
| V_OH(min) | ขาออกที่สั่งเป็น 1 จะให้แรงดัน **อย่างน้อย** เท่านี้ |
| V_OL(max) | ขาออกที่สั่งเป็น 0 จะให้แรงดัน **ไม่เกิน** เท่านี้ |
| V_IH(min) | ขาเข้ารับประกันว่าอ่านเป็น 1 เมื่อแรงดัน **ตั้งแต่** เท่านี้ |
| V_IL(max) | ขาเข้ารับประกันว่าอ่านเป็น 0 เมื่อแรงดัน **ไม่เกิน** เท่านี้ |

ระหว่าง V_IL กับ V_IH คือช่วงที่ไม่รับประกัน — ขาเข้าอาจอ่านเป็นอะไรก็ได้

```text
ส่วนเผื่อสัญญาณรบกวน: NM_H = V_OH(min) − V_IH(min)    NM_L = V_IL(max) − V_OL(max)
ถ้าค่าใดค่าหนึ่งติดลบ แปลว่าต่อกันตรงไม่ได้
```

---

## แนวคิด (2) — แถบระดับลอจิกจริง

<figure>
<svg viewBox="0 0 360 200" width="360" role="img" aria-label="แถบระดับลอจิกของระบบ 3.3 V และ 1.8 V ตามกฎ 0.7 และ 0.3 ของ VDD" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="21.5" width="60" height="148.5" rx="3"/>
<path d="M20 66.1H80M20 125.5H80"/>
<text x="50" y="47.775000000000006" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">1</text>
<text x="50" y="99.75" text-anchor="middle" fill="currentColor" stroke="none">?</text>
<text x="50" y="151.725" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">0</text>
<text x="86" y="70.05000000000001" fill="currentColor" stroke="none">V_IH 2.31 V</text>
<text x="86" y="129.45" fill="currentColor" stroke="none">V_IL 0.99 V</text>
<text x="86" y="25.5" fill="currentColor" stroke="none">3.3 V</text>
<text x="50" y="190" text-anchor="middle" fill="currentColor" stroke="none">3.3 V CMOS</text>
<rect x="200" y="89.0" width="60" height="81.0" rx="3"/>
<path d="M200 113.3H260M200 145.7H260"/>
<text x="230" y="105.15" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">1</text>
<text x="230" y="133.5" text-anchor="middle" fill="currentColor" stroke="none">?</text>
<text x="230" y="161.85" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">0</text>
<text x="266" y="117.3" fill="currentColor" stroke="none">V_IH 1.26 V</text>
<text x="266" y="149.7" fill="currentColor" stroke="none">V_IL 0.54 V</text>
<text x="266" y="93.0" fill="currentColor" stroke="none">1.8 V</text>
<text x="230" y="190" text-anchor="middle" fill="currentColor" stroke="none">1.8 V CMOS</text>
<path d="M15 170H350"/>
</svg>
<figcaption>แถบตัวอย่างตามกฎหยาบ V_IH = 0.7 × VDD และ V_IL = 0.3 × VDD ค่าจริงต้องอ่านจากเอกสารข้อมูลของชิป</figcaption>
</figure>

---

## แนวคิด (3) — ต่อสองอุปกรณ์เข้าหากันได้ไหม

| ค่า | อุปกรณ์ A (1.8 V) | อุปกรณ์ B (3.3 V) |
|---|---|---|
| V_OH(min) | 1.35 V | 2.9 V |
| V_IH(min) | 1.26 V | 2.31 V |
| แรงดันขาเข้าสูงสุดที่ทนได้ | 2.1 V | 3.6 V |

**A → B** NM_H = 1.35 − 2.31 = **−0.96 V** ติดลบ ต่อกันตรงไม่ได้

**B → A** 2.9 V ผ่าน V_IH ของ A ได้สบาย แต่ **เกินค่าสูงสุดที่ขา A ทนได้ (2.1 V)** — กระแสไหลผ่านไดโอดป้องกันเข้าไฟเลี้ยง 1.8 V (back-powering) นี่คือกับดักที่อันตรายที่สุด เพราะ "มันอ่านค่าได้ถูก" ในวันแรก

**ทางแก้** ชิปแปลงระดับ, บัส open-drain + pull-up แยกฝั่ง, หรือวงจรแบ่งแรงดัน (สัญญาณช้าทางเดียว)

---

## แนวคิด (4) — เกตพื้นฐานและตารางความจริง

| A | B | NOT A | A AND B | A OR B | A XOR B |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 0 |

- **AND** เป็น 1 เมื่อทุกขาเข้าเป็น 1 · **OR** เป็น 1 เมื่อมีอย่างน้อยหนึ่งขาเข้าเป็น 1
- **XOR** เป็น 1 เมื่อสองขาเข้า **ต่างกัน** · NAND/NOR คือ AND/OR ตามด้วย NOT
- C: `&&`, `||`, `!` (เงื่อนไข), `&`, `|`, `~`, `^` (บิต) · MicroPython: `and`, `or`, `not`, `&`, `|`, `^`
- **ปุ่มแบบ active-low** "กดอยู่" = `NOT pin`

---

## ตัวอย่างสมบูรณ์ — เงื่อนไขพัดลมระบายความร้อน

**โจทย์** พัดลมทำงานเมื่อ "อุณหภูมิสูง **และ** ประตูปิด" **หรือ** "ผู้ใช้สั่งเปิดเอง"

```text
FAN = (T AND D) OR M
```

| T | D | M | FAN |
|---|---|---|---|
| 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |
| อื่น ๆ | | | 0 |

ถ้าสวิตช์ประตูเป็น active-low ต้องกลับค่าก่อนใช้

```c
bool door_closed = !door_pin;                 /* active-low: ปิดอ่านได้ 0 */
bool fan_on = (temp_high && door_closed) || manual;
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. V_OH(min)=2.4V, V_OL(max)=0.4V ต่อกับ V_IH(min)=2.0V, V_IL(max)=0.8V — หา NM_H, NM_L ต่อตรงได้ไหม
2. อุปกรณ์ 5V ส่งสัญญาณ 5V เข้าขา 3.3V ที่ไม่ทนแรงดัน 5V — ต่อตรงได้ไหม เพราะอะไร

**แล็บ ส่วน A** วัด V_OH/V_OL จริงของขา P13.0 ด้วยมัลติมิเตอร์ (โปรแกรม GPIO Out) แล้วตัดสินว่าต่อกับอุปกรณ์ A (1.8V) หรือ B (3.3V) ได้ไหม

**แล็บ ส่วน B** ต่อวงจรแบ่งแรงดันเข้า P13.0 ผ่านตัวต้านทาน 1 kΩ กันขา หาจุดสลับจริงของขาเข้าด้วยคู่ตัวต้านทานต่าง ๆ

---

## เช็กความเข้าใจ

1. ขาออกของอุปกรณ์ 1.8 V มี V_OH(min) = 1.35 V ต่อเข้าขาเข้าของอุปกรณ์ 3.3 V ที่มี V_IH(min) = 2.31 V ได้ไหม
   - ก) ได้ เพราะ 1.35 V มากกว่าศูนย์ · ข) ไม่ได้ ระดับ 1 ต่ำกว่า V_IH · ค) ได้ ถ้าใส่ตัวต้านทาน 1 kΩ อนุกรม · ง) ไม่ได้ เพราะ V_OL สูงเกินไป

2. ขาออก 3.3 V ต่อเข้าขาของชิป 1.8 V ที่ทนแรงดันขาเข้าได้สูงสุด 2.1 V ข้อใดถูก
   - ก) ปลอดภัย เพราะอ่านเป็น 1 ได้ถูก · ข) อ่านถูกก็จริง แต่แรงดันเกินค่าสูงสุดที่ขาทน อาจเสียหาย · ค) อ่านไม่ได้เลย · ง) ปลอดภัยถ้าชิปปิดไฟอยู่

3. เกต XOR ได้ขาเข้า A = 1 และ B = 1 ขาออกเป็นอะไร
   - ก) 0 · ข) 1 · ค) ไม่แน่นอน · ง) เท่ากับ A AND B

---

## ไปต่อ

บทเรียนถัดไป [Pull-up, pull-down และปุ่มกด](../l02-pullups-and-buttons/README.md) — ทำไมขาเข้าที่ปล่อยลอยจึงอ่านค่ามั่ว ต่อปุ่มแบบ active-low และใช้ logic analyzer ครั้งแรก

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
