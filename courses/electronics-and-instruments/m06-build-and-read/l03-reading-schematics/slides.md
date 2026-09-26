---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.3 — อ่านแผนผังวงจร"
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

# บทเรียน 6.3 — อ่านแผนผังวงจร

## อ่านสัญลักษณ์ ชื่อสัญญาณ และบล็อกของแผนผังวงจร แล้วตามสัญญาณจากขาชิปไปถึงชิ้นส่วน

**โมดูล 6 — ต่อวงจร บัดกรี อ่านแผนผัง และพื้นฐาน PCB กับ EMC**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้
2. ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้

---

## ก่อนเริ่ม

- แผนผังวงจร (schematic) ของบอร์ดที่คุณใช้ ถ้าไม่มีจริงเลย แนวคิดและฝึกเติมทำได้ด้วยแผนผังตัวอย่างในบทเรียน
- TESAIoT Dev Kit ที่ flash QWA309 Potentiometer Monitor และ Header I/O Test, มัลติมิเตอร์, logic analyzer

---

## ดูของจริงก่อน

เอกสารสาธารณะสองชิ้นพูดถึงลูกบิดตัวเดียวกันไม่ตรงกัน

- README ของตัวอย่าง Potentiometer Monitor: **VR1 = P15.5, VR2 = P15.4**
- README ของ overlay บอร์ด QWA309 ใน SDK: "PCBA silkscreen swaps VR1↔VR2; schematic is authoritative (VR1=P15.4)"

ทั้งสองเอกสาร **ตรงกันเรื่องชื่อขาของชิป** และไม่ตรงกันเฉพาะ **ชื่อที่คนตั้ง** — คำถามนี้ตอบด้วยการอ่านแผนผังและวัด ไม่ใช่เลือกเชื่อเอกสารที่ดูน่าเชื่อกว่า

---

## แนวคิด (1) — สัญลักษณ์และรหัสชิ้นส่วน

<figure>
<svg viewBox="0 0 400 160" width="400" role="img" aria-label="สัญลักษณ์พื้นฐานในแผนผังวงจร" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,30 20,30 22.5,24 27.5,36 32.5,24 37.5,36 42.5,24 47.5,36 50,30 60,30"/>
<text x="35" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (US)</text>
<path d="M80 30H90"/><rect x="90" y="24" width="30" height="12" rx="3"/><path d="M120 30H130"/>
<text x="105" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (IEC)</text>
<path d="M150 30H166M166 20V40M172 20V40M172 30H188"/>
<text x="169" y="60" text-anchor="middle" fill="currentColor" stroke="none">C</text>
<path d="M262 30H274M274 22V38L286 30Z M286 22V38M286 30H298"/>
<text x="280" y="60" text-anchor="middle" fill="currentColor" stroke="none">diode</text>
<path d="M318 30H330M330 22V38L342 30Z M342 22V38M342 30H354M334 18l6 -8m-4 0h4v4M341 18l6 -8m-4 0h4v4"/>
<text x="336" y="60" text-anchor="middle" fill="currentColor" stroke="none">LED</text>
<path d="M160 106V114M150 114H170M154 118H166M158 122H162"/>
<text x="160" y="144" text-anchor="middle" fill="currentColor" stroke="none">GND</text>
<path d="M255 110H268"/><circle cx="270" cy="110" r="2.5"/><circle cx="296" cy="110" r="2.5"/><path d="M298 110H311M272 108L295 98"/>
<text x="283" y="144" text-anchor="middle" fill="currentColor" stroke="none">SW</text>
</svg>
<figcaption>สัญลักษณ์ที่เจอบ่อย: ตัวต้านทาน ตัวเก็บประจุ ไดโอด LED กราวด์ สวิตช์</figcaption>
</figure>

---

## แนวคิด (2) — รหัสอ้างอิงและการเขียนค่า

| ตัวอักษร | ชนิด | ตัวอักษร | ชนิด |
|---|---|---|---|
| R | ตัวต้านทาน | U | ชิป (IC) |
| C | ตัวเก็บประจุ | J, P, CN | ขั้วต่อ |
| D | ไดโอด/LED | Q | ทรานซิสเตอร์/MOSFET |
| TP | จุดทดสอบ | Y, X | คริสตัล |

```text
4k7 = 4.7 kΩ    2R2 = 2.2 Ω    1M0 = 1.0 MΩ    100n = 100 nF
รหัสตัวต้านทานชิป: "103" = 10×10³ = 10 kΩ   "472" = 4.7 kΩ
```

---

## แนวคิด (3) — net, ชื่อสัญญาณ และหลายหน้า

**net** คือกลุ่มของจุดที่ต่อถึงกันทางไฟฟ้า

- เส้นตัดกันเป็นรูปตัว T มี **จุดดำ (junction dot)** = ต่อกัน · กากบาทไม่มีจุด = ไม่ต่อกัน
- **ป้ายชื่อ (net label)** จุดที่มีชื่อเดียวกันคือ net เดียวกัน แม้ไม่มีเส้นลากถึงกัน — ใช้ข้ามหน้ากระดาษ
- ทุกสัญลักษณ์ "3V3" หรือกราวด์ทั่วแผนผัง คือ net เดียวกัน

**ชื่อสัญญาณที่บอกความหมาย** เช่น `P13.3_GPIO_PWM5+_3V3` = ขา | หน้าที่ | โดเมนแรงดัน

**สัญญาณ active-low** มีเครื่องหมายกำกับ เช่น `_N`, `/`, ขึ้นต้นด้วย `n`, `#` → RESET_N, /CS, nWP

---

## แนวคิด (4) — ตามสัญญาณ และเมื่อเอกสารไม่ตรงกับบอร์ด

```text
ขั้นตอนตามสัญญาณ
1. หาสัญลักษณ์ MCU แล้วหาขาที่สนใจ
2. ตามเส้นจนเจอชิ้นส่วนหรือป้ายชื่อ ถ้าเจอป้ายชื่อ ค้นหาชื่อเดียวกันในทุกหน้า
3. จดรหัสอ้างอิง ค่า และทิศทางของทุกชิ้นส่วนที่ผ่าน
4. ตามจนถึงปลายทาง (มักเป็นไฟเลี้ยงหรือกราวด์) แล้วสรุปเป็นประโยค
```

**เมื่อป้ายบนแผ่นวงจร (silkscreen) ไม่ตรงกับแผนผัง** แผนผังคือเอกสารที่ใช้สร้างแผ่นวงจร จึงมักเชื่อถือได้มากกว่า แต่ก็เป็นเอกสารที่คนเขียนและอาจผิดได้ — **ข้อสรุปสุดท้ายต้องมาจากการวัด**

---

## ตัวอย่างสมบูรณ์ — LED1 และ SW3

**LED1**

```text
หน้า 1: IO1 → R12 (1kΩ) → ป้าย LED1
หน้า 2: ป้าย LED1 → D5 (แอโนดทางป้าย แคโทดทางกราวด์) → GND
สรุป: IO1=1 → กระแสไหล → LED ติด = active-high
กระแส: (3.3−2.0)/1kΩ = 1.3 mA
```

**SW3**

```text
หน้า 1: IO2 → ป้าย BTN_N ตรง ๆ ไม่มีตัวต้านทานคั่น
หน้า 2: ป้าย BTN_N → R40 (10kΩ) ขึ้น 3V3 และ SW3 ลงกราวด์
สรุป: ปล่อย=1(R40 ดึงขึ้น) กด=0(ลงกราวด์) = active-low ตรงกับ _N
กระแสตอนกด: 3.3/10kΩ = 0.33 mA
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. แปลค่า 4k7, 2R2, 100n, 1u0 และรหัสชิป "103" และ "4701"
2. เส้นแนวนอนกับแนวตั้งตัดกันเป็นกากบาท ไม่มีจุดดำ สองเส้นนี้ต่อกันไหม ถ้าเป็นตัว T มีจุดดำล่ะ

**แล็บ ส่วน A** (ถ้ามีแผนผังจริง) ตามสัญญาณของ LED และปุ่มผู้ใช้หนึ่งดวง/ปุ่ม จดรหัสอ้างอิงและค่าทุกชิ้นที่ผ่าน สรุป active-high/low แล้วเทียบกับ SDK

**แล็บ ส่วน B** (TESAIoT Dev Kit) หมุนลูกบิดที่ป้าย VR1 บนแผ่นวงจร ดูว่าการ์ดที่ขยับแสดงขาอะไร เทียบป้ายบนแผ่นวงจร โค้ดตัวอย่าง และคำอธิบายใน SDK

---

## เช็กความเข้าใจ

1. ค่าตัวต้านทานบนแผนผังเขียนว่า 4k7 หมายถึงเท่าไร
   - ก) 47 kΩ · ข) 4.7 kΩ · ค) 470 Ω · ง) 4.7 Ω

2. บนแผนผัง เส้นสองเส้นตัดกันเป็นรูปกากบาทโดยไม่มีจุดดำ หมายความว่าอะไร
   - ก) สองเส้นต่อกัน · ข) สองเส้นไม่ต่อกัน · ค) ต่อกันเฉพาะในหน้าเดียวกัน · ง) ต้องเปิดรายการชิ้นส่วนดู

3. ป้ายบนแผ่นวงจรกับแผนผังบอกตำแหน่งขาไม่ตรงกัน ควรทำอย่างไร
   - ก) เชื่อป้ายบนแผ่นวงจร เพราะเห็นกับตา · ข) ถือแผนผังเป็นหลักไว้ก่อน แล้วยืนยันด้วยการวัด · ค) เลือกเอกสารที่ใหม่กว่าโดยไม่ต้องวัด · ง) หยุดใช้บอร์ดนั้น

---

## ไปต่อ

บทเรียนสุดท้ายของหลักสูตร [พื้นฐาน PCB และ EMC](../l04-pcb-and-emc-basics/README.md) จะพาจากแผนผังไปสู่แผ่นวงจรจริง ว่าตำแหน่งของตัวเก็บประจุและรูปร่างของลายวงจรมีผลกับสัญญาณรบกวนอย่างไร

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
