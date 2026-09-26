---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.1 — ต่อวงจรบนเบรดบอร์ด"
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

# บทเรียน 6.1 — ต่อวงจรบนเบรดบอร์ด

## รู้ว่ารูบนเบรดบอร์ดเชื่อมกันอย่างไร และต่อวงจรตามแผนผังให้ตรวจง่าย

**โมดูล 6 — ต่อวงจร บัดกรี อ่านแผนผัง และพื้นฐาน PCB กับ EMC**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง
2. ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ

---

## ก่อนเริ่ม

- ใช้โหมดความต่อเนื่องและโหมดไดโอดของมัลติมิเตอร์ได้
- แล็บ: เบรดบอร์ด, สายจัมเปอร์หลายสี, LED สีแดง×3, ตัวต้านทาน 1 kΩ×4, 10 kΩ×1, ปุ่มกด×1, TESAIoT Dev Kit

---

## ดูของจริงก่อน

พลิกเบรดบอร์ดดูด้านหลัง (หรือดูภาพจากผู้ผลิต) จะเห็นแถบโลหะเรียงอยู่ใต้รู — แถบสั้นจำนวนมากอยู่ตรงกลาง และแถบยาวสองสามเส้นอยู่ริมบนล่าง

ก่อนอ่านต่อ ลองทายว่ารูคู่ไหนต่อถึงกัน แล้วพิสูจน์ด้วยโหมดความต่อเนื่องของมัลติมิเตอร์ ถ้าคุณทายผิดสักคู่ ดีมาก — นั่นคือความผิดพลาดที่คุณจะไม่ทำตอนต่อวงจรจริง

---

## แนวคิด (1) — ข้างในเบรดบอร์ด

<figure>
<svg viewBox="0 0 420 250" width="420" role="img" aria-label="ผังการเชื่อมต่อภายในเบรดบอร์ด รางไฟตามยาวและแถวละห้ารู" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="20" y="22" font-weight="bold" fill="currentColor" stroke="none">+</text>
<text x="20" y="38" font-weight="bold" fill="currentColor" stroke="none">−</text>
<path d="M60 18H252" stroke-width="3"/>
<path d="M60 34H252" stroke-width="3" stroke-dasharray="4 3"/>
<circle cx="68" cy="56" r="2"/><circle cx="84" cy="56" r="2"/><circle cx="100" cy="56" r="2"/><circle cx="116" cy="56" r="2"/>
<circle cx="68" cy="120" r="2"/><circle cx="84" cy="120" r="2"/><circle cx="100" cy="120" r="2"/><circle cx="116" cy="120" r="2"/>
<path d="M68 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<circle cx="68" cy="160" r="2"/><circle cx="84" cy="160" r="2"/><circle cx="100" cy="160" r="2"/><circle cx="116" cy="160" r="2"/>
<circle cx="68" cy="224" r="2"/><circle cx="84" cy="224" r="2"/><circle cx="100" cy="224" r="2"/><circle cx="116" cy="224" r="2"/>
<path d="M68 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M60 140H252" stroke-dasharray="4 3"/>
<text x="260" y="144" fill="currentColor" stroke="none">centre channel</text>
<text x="260" y="26" fill="currentColor" stroke="none">power rails (long)</text>
<text x="260" y="84" fill="currentColor" stroke="none">5 holes in a column</text>
<text x="260" y="100" fill="currentColor" stroke="none">= one node</text>
</svg>
<figcaption>ห้ารูในแนวเดียวกัน (ไม่ข้ามร่องกลาง) ต่อกันเป็นจุดเดียว รางไฟด้านบนต่อกันตามยาว</figcaption>
</figure>

---

## แนวคิด (2) — กฎของเบรดบอร์ด

- **กลุ่มห้ารู** แนวเดียวกันที่ไม่ข้ามร่องกลาง = node เดียวกัน
- **ร่องกลาง (centre channel)** แยกสองฝั่ง ความกว้างพอดีกับชิปแบบ DIP
- **รางไฟ (power rails)** แถบยาวริมขอบ — **เบรดบอร์ดยาวบางรุ่นรางไฟขาดครึ่งกลาง** ต้องตรวจด้วยความต่อเนื่องก่อนใช้ทุกแผ่น
- ระยะห่างรู 2.54 mm (0.1 นิ้ว) เท่ากับขา header ทั่วไป

**ความผิดพลาดคลาสสิก** เสียบตัวต้านทานโดยขาทั้งสองอยู่ในกลุ่มห้ารูเดียวกัน — ตัวต้านทานถูกลัดทิ้ง วงจรทำงานเหมือนไม่มีมัน

---

## แนวคิด (3) — สีสายและการจัดวาง

| สี | ใช้กับ |
|---|---|
| แดง | ไฟเลี้ยงบวก (หลายแรงดันแยกสี เช่น แดง=5V ส้ม=3.3V) |
| ดำ (หรือน้ำเงิน) | กราวด์ |
| สีอื่น | สัญญาณ แยกตามหน้าที่ |

**หลักจัดวางที่ตรวจง่าย** ต่อทีละ net แล้วขีดทับบนแผนผังที่พิมพ์ไว้ · สายสั้นแนบเบรดบอร์ด · วางตามทิศทางของแผนผัง (ไฟบน กราวด์ล่าง)

**ข้อจำกัด** แถบโลหะมีความจุแฝงราวไม่กี่ pF — `f_c = 1/(2π×R×C)` เช่น 5 pF กับ 100 kΩ ได้ f_c ≈ 318 kHz ไม่เหมาะกับสัญญาณเร็วระดับหลาย MHz

---

## แนวคิด (4) — ตรวจก่อนจ่ายไฟ

ตรวจตามลำดับนี้ทุกครั้ง **ขณะที่เบรดบอร์ดยังไม่ต่อกับบอร์ดหรือแหล่งจ่าย**

```text
1. ตรวจด้วยตา       ไล่ทีละ net เทียบแผนผัง ขั้วของ LED/ตัวเก็บประจุถูกไหม
2. รางไฟกับกราวด์   ความต่อเนื่องระหว่างราง + กับ − ต้อง "ไม่ดัง"
3. ความต้านทาน       คำนวณไว้ก่อนว่าควรได้เท่าไร แล้ววัดเทียบ
4. ทดสอบ LED         โหมดไดโอด แดงที่แอโนด ดำที่แคโทด
5. ต่อไฟตามลำดับ     GND ก่อน แล้วไฟเลี้ยง แล้วสายสัญญาณ
```

---

## ตัวอย่างสมบูรณ์ — LED สามดวง + ปุ่ม active-low

```text
net GND   ขา GND ของ header, ราง −, แคโทดของ LED1-3, ขาหนึ่งของปุ่ม
net 3V3   ขา 3V3, ราง +, ปลายหนึ่งของ R_pu 10 kΩ
net LED1  P13.3 → 1 kΩ → แอโนดของ LED1 (เช่นเดียวกัน LED2@P13.4, LED3@P13.5)
net BTN_N ปลายอีกข้างของ R_pu, ขาอีกข้างของปุ่ม, และ 1 kΩ ไปยัง P13.0

คำนวณก่อนต่อ:
กระแส LED แต่ละดวงเมื่อขาเป็น 1: (3.3−2.0)/1kΩ ≈ 1.3 mA
ราง + กับ −: ปล่อยปุ่ม → OL (เปิดวงจร)   กดปุ่ม → 10 kΩ
```

**ตรวจ** ราง+/− ไม่ดัง, อ่าน OL, ได้ 10 kΩ เมื่อกดปุ่ม, LED ผ่านโหมดไดโอด → จึงต่อเข้าบอร์ด

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. รู a12 กับ e12 ต่อกันไหม e12 กับ f12 ล่ะ a12 กับ a13 ล่ะ
2. เสียบตัวต้านทานขาหนึ่งที่ b15 อีกขาที่ d15 จะเกิดอะไรขึ้น

**แล็บ**

1. สำรวจเบรดบอร์ดของคุณ — ตรวจรางไฟขาดครึ่งกลางไหม สุ่มตรวจกลุ่มห้ารู
2. วาดแผนผังของตัวอย่างสมบูรณ์ลงกระดาษ แล้วต่อทีละ net ขีดทับทุกครั้งที่ต่อเสร็จ
3. ตรวจก่อนจ่ายไฟครบห้าข้อ แล้วจ่ายไฟตามลำดับ GND → 3V3 → สัญญาณ
4. ให้เพื่อนตรวจ — จับเวลาว่าเพื่อนใช้กี่นาทีจึงยืนยันได้ว่าต่อถูกทุก net

---

## เช็กความเข้าใจ

1. บนเบรดบอร์ดมาตรฐาน รู a10 กับ e10 (ฝั่งเดียวกันของร่องกลาง แนวเดียวกัน) ต่อถึงกันหรือไม่
   - ก) ต่อกัน เป็นกลุ่มห้ารูเดียวกัน · ข) ไม่ต่อกัน · ค) ต่อกันเฉพาะเบรดบอร์ดยาว · ง) ต่อกันผ่านรางไฟ

2. เสียบตัวต้านทานโดยขาหนึ่งอยู่ b15 และอีกขาอยู่ d15 จะเกิดอะไรขึ้น
   - ก) ทำงานปกติ · ข) ตัวต้านทานถูกลัดทิ้ง เพราะทั้งสองขาอยู่ในกลุ่มห้ารูเดียวกัน · ค) ตัวต้านทานไหม้ทันที · ง) ค่าความต้านทานเพิ่มเป็นสองเท่า

3. ก่อนจ่ายไฟ วัดโหมดความต่อเนื่องระหว่างราง + กับราง − ผลแบบใดที่ควรได้
   - ก) เครื่องส่งเสียงดัง · ข) เครื่องไม่ส่งเสียง และความต้านทานใกล้เคียงค่าที่คำนวณจากวงจร · ค) อ่านได้ 0 Ω · ง) ไม่ต้องตรวจ

---

## ไปต่อ

เบรดบอร์ดเหมาะกับการทดลอง แต่วงจรที่ต้องทนการใช้งานจริงต้องบัดกรี บทเรียนถัดไป [บัดกรีอย่างปลอดภัย](../l02-soldering-safely/README.md) จะฝึกบัดกรีหัวต่อหนึ่งแถวให้ผ่านการตรวจด้วยตาและมัลติมิเตอร์

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
