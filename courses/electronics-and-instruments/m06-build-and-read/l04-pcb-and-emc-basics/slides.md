---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.4 — พื้นฐาน PCB และ EMC"
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

# บทเรียน 6.4 — พื้นฐาน PCB และ EMC

## เข้าใจหลักการวางชิ้นส่วน กราวด์ และเส้นทางสัญญาณที่ลดปัญหาสัญญาณรบกวนและการแผ่คลื่น

**โมดูล 6 — ต่อวงจร บัดกรี อ่านแผนผัง และพื้นฐาน PCB กับ EMC**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายหน้าที่ของระนาบกราวด์และตัวเก็บประจุ decoupling ที่วางชิดขาไฟของชิป
2. ระบุปัจจัยที่ทำให้บอร์ดแผ่คลื่นรบกวนหรือไวต่อสัญญาณรบกวนได้อย่างน้อยสามข้อ
3. อธิบายว่าทำไมผลิตภัณฑ์ที่มีวิทยุหรือวงจรอิเล็กทรอนิกส์ต้องผ่านการทดสอบมาตรฐานก่อนวางขาย

---

## ก่อนเริ่ม

- เข้าใจ decoupling, ลูปของสายกราวด์โพรบ, และอ่านแผนผังได้ (บทเรียนก่อนหน้า)
- แล็บ: บอร์ด, แว่นขยายหรือกล้องมือถือ, ออสซิลโลสโคปพร้อมโพรบ
- บทนี้เป็นพื้นฐาน การออกแบบ PCB และการทดสอบ EMC จริงเป็นวิชาเฉพาะที่ลึกกว่านี้มาก

---

## ดูของจริงก่อน

ส่องบอร์ดทั้งสองด้าน หาสิ่งเหล่านี้

- ตัวเก็บประจุเล็ก ๆ จำนวนมากที่อยู่ชิดชิปหลัก
- รู via เล็ก ๆ เรียงกันเป็นแถวหรือกระจายทั่วบอร์ด
- ฝาโลหะครอบชิ้นส่วน (shield can) และบริเวณเสาอากาศที่ไม่มีทองแดงรอบ ๆ
- ชิ้นส่วนเล็ก ๆ ชิดขั้วต่อ USB (ป้องกันไฟฟ้าสถิตหรือ ferrite bead)

ทำไมต้องมีสิ่งเหล่านี้ทั้งที่แผนผังจะทำงานได้แม้ไม่มี — เพราะแผนผังบอกว่า "อะไรต่อกับอะไร" แต่ไม่บอก "กระแสวิ่งทางไหน"

---

## แนวคิด (1) — กระแสต้องวิ่งกลับ

<figure>
<svg viewBox="0 0 400 155" width="400" role="img" aria-label="กระแสไหลกลับใต้เส้นสัญญาณบนระนาบกราวด์ต่อเนื่อง เทียบกับระนาบที่มีร่อง" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="20" width="160" height="110" rx="3" stroke-dasharray="4 3"/>
<text x="100" y="145" text-anchor="middle" fill="currentColor" stroke="none">solid ground plane</text>
<path d="M40 60H160" stroke-width="3"/>
<text x="40" y="52" fill="currentColor" stroke="none">signal</text>
<path d="M40 70H160" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="40" y="88" font-size="11" fill="currentColor" stroke="none">return current</text>
<rect x="220" y="20" width="160" height="110" rx="3" stroke-dasharray="4 3"/>
<text x="300" y="145" text-anchor="middle" fill="currentColor" stroke="none">plane with a slot</text>
<path d="M296 20V100M304 20V100" stroke-width="1"/>
<path d="M240 60H360" stroke-width="3"/>
<text x="240" y="52" fill="currentColor" stroke="none">signal</text>
<path d="M240 70H290V112H310V70H360" stroke-dasharray="4 3"/>
<text x="300" y="124" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">detour = big loop</text>
</svg>
<figcaption>ซ้าย: ระนาบกราวด์ต่อเนื่อง กระแสไหลกลับวิ่งใต้เส้นสัญญาณพอดี ขวา: ร่องบนระนาบบังคับให้กระแสอ้อม วงลูปใหญ่ขึ้น</figcaption>
</figure>

กฎที่จำง่าย: **อย่าให้ลายสัญญาณเร็ววิ่งข้ามร่องของระนาบกราวด์**

---

## แนวคิด (2) — Decoupling ต้องชิด

```text
ตัวเก็บประจุ 100 nF + ความเหนี่ยวนำรวม 1 nH เรโซแนนซ์ที่ f0 ≈ 15.9 MHz
ที่ 100 MHz: อิมพีแดนซ์จากความจุ ≈ 0.016 Ω, จากความเหนี่ยวนำ ≈ 0.63 Ω (ใหญ่กว่าเกือบ 40 เท่า)
```

เหนือความถี่เรโซแนนซ์ ตัวเก็บประจุทำตัวเหมือนตัวเหนี่ยวนำ — **ตำแหน่งและความยาวของลูปสำคัญกว่าค่าความจุ**

```text
ลายวงจรยาวเกินอีก 5 mm เพิ่ม L ราว 5 nH
กระแสเปลี่ยน 25 mA ภายใน 1 ns → แรงดันกระเพื่อมเพิ่ม 5nH×25mA/1ns = 0.125 V
```

---

## แนวคิด (3) — อะไรทำให้บอร์ดแผ่คลื่นหรือโดนรบกวน

**EMC** = ทำงานได้โดยไม่รบกวนอุปกรณ์อื่น (emission) และไม่เสียเมื่อถูกรบกวน (immunity)

| ปัจจัย | ทางแก้ที่พบบ่อย |
|---|---|
| พื้นที่ลูปใหญ่ | ระนาบกราวด์ต่อเนื่อง ลายสัญญาณชิดทางกลับ |
| ขอบสัญญาณเร็ว (ขอบ 1 ns ไปถึงราว 350 MHz) | ลด drive strength ใส่ตัวต้านทานอนุกรมเล็ก ๆ |
| สายเคเบิลเป็นเสาอากาศ (สาย 1 m ≈ λ/4 ที่ 75 MHz) | ferrite bead, สายมีชีลด์ต่อกราวด์ถูกจุด |
| จุดความต้านทานสูงหรือขาลอย | pull-up/pull-down, ตัวกรองที่ขา ADC |
| decoupling ไม่พอหรือไกล | ตัวเก็บประจุชิดขา หลายค่า via สั้น |

---

## แนวคิด (4) — ทำไมต้องทดสอบก่อนวางขาย

คลื่นวิทยุเป็นทรัพยากรที่ทุกคนใช้ร่วมกัน — อุปกรณ์ที่แผ่คลื่นเกินอาจรบกวนวิทยุการบิน อุปกรณ์การแพทย์ หรือเครือข่ายของคนทั้งอาคาร

- **การแผ่คลื่น** เช่น CISPR 32 · **ความทนทาน** เช่น CISPR 35, IEC 61000-4-2 (ไฟฟ้าสถิต)
- **วิทยุ** ตามกฎแต่ละประเทศ เช่น ETSI EN 300 328 (2.4 GHz, ยุโรป), FCC Part 15 (สหรัฐฯ), กสทช. (ไทย)
- **ความปลอดภัยทางไฟฟ้า** เช่น IEC 62368-1

**ข้อที่มักเข้าใจผิด** ใช้โมดูลวิทยุที่ผ่านการรับรองแล้ว **ไม่ได้แปลว่า**ผลิตภัณฑ์ทั้งชิ้นผ่านโดยอัตโนมัติ — บอร์ด สายไฟ แหล่งจ่าย และกล่อง ล้วนเปลี่ยนผลการแผ่คลื่นได้

---

## ตัวอย่างสมบูรณ์ — แก้ปัญหาการแผ่คลื่นเกินขีดจำกัด

**ปัญหา** ต้นแบบ WiFi แผ่คลื่นเกินที่ 75 MHz และ 125 MHz — ลายนาฬิกา 25 MHz ยาว 6 cm ข้ามร่องกราวด์, decoupling ห่างขาไฟ 15 mm, สาย USB 1 m ไม่มีตัวกรอง

```text
วิเคราะห์: 75/125 MHz คือฮาร์มอนิกที่ 3 และ 5 ของ 25 MHz
          สาย USB 1 m มี λ/4 ตรงกับ 75 MHz พอดี
          decoupling ไกล 15 mm เพิ่ม L ~15 nH เหนือไม่กี่ MHz แทบไม่ช่วยแล้ว

แก้ตามลำดับความคุ้ม:
1. เดินลายนาฬิกาใหม่ให้สั้นไม่ข้ามร่อง หรือใช้บอร์ด 4 ชั้น
2. ใส่ตัวต้านทานอนุกรม 22-33 Ω ชิดขาต้นทางนาฬิกา
3. ย้าย decoupling ชิดขาไฟ ใช้ via สั้น
4. ใส่ ferrite bead ที่ USB
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. ตัวเก็บประจุ 10 nF มีความเหนี่ยวนำรวม 0.8 nH เรโซแนนซ์ที่ความถี่เท่าไร เหนือความถี่นั้นทำตัวอย่างไร
2. ขอบสัญญาณขึ้นใน 2 ns พลังงานกระจายไปถึงความถี่ราวเท่าไร

**แล็บ ส่วน A** อ่านบอร์ดด้วยตา — หา decoupling caps, stitching via, shield can, พื้นที่เสาอากาศ, ตัวกรอง USB

**แล็บ ส่วน B** ลูปคือเสาอากาศ — ทำวงลูปจากสายกราวด์ของโพรบ (ไม่แตะบอร์ด) วัดสัญญาณรบกวนที่รับได้เหนือบอร์ด เทียบขนาดลูปใหญ่กับเล็ก

---

## เช็กความเข้าใจ

1. ทำไมตัวเก็บประจุ decoupling ต้องวางชิดขาไฟของชิปที่สุด
   - ก) เพื่อให้ค่าความจุเพิ่มขึ้น · ข) เพื่อให้ลูประหว่างขาไฟ ตัวเก็บประจุ และกราวด์เล็ก ความเหนี่ยวนำต่ำ · ค) เพื่อให้ประกอบง่าย · ง) เพื่อป้องกันไฟฟ้าสถิตที่ขั้วต่อ

2. ระนาบกราวด์ต่อเนื่องใต้ลายสัญญาณช่วยเรื่องใดมากที่สุด
   - ก) กระแสไหลกลับวิ่งใต้ลายสัญญาณพอดี ลูปเล็ก แผ่คลื่นและรับสัญญาณรบกวนน้อย · ข) ทำให้บอร์ดแข็งแรงขึ้น · ค) ลดแรงดันไฟเลี้ยง · ง) ทำให้สัญญาณวิ่งเร็วกว่าความเร็วแสง

3. ผลิตภัณฑ์ใช้โมดูล WiFi ที่ผ่านการรับรองแล้ว ข้อใดถูกต้องเกี่ยวกับการทดสอบก่อนวางขาย
   - ก) ไม่ต้องทดสอบอะไรอีก · ข) ผลิตภัณฑ์ทั้งชิ้นยังต้องผ่านการทดสอบ EMC และความปลอดภัย เพราะบอร์ด สาย และกล่องเปลี่ยนการแผ่คลื่นได้ · ค) ทดสอบเฉพาะความปลอดภัยทางไฟฟ้าก็พอ · ง) ทดสอบเฉพาะในประเทศที่ผลิต

---

## ไปต่อ

คุณผ่านครบทั้งหกโมดูลของหลักสูตรนี้แล้ว ทักษะที่ได้ใช้ต่อได้ทันทีกับหลักสูตรที่ทำงานกับบอร์ดจริง เช่น TESAIoT Firmware Stack — ทุกครั้งที่โปรแกรมบอกว่า "ส่งแล้ว" คุณมีเครื่องมือพิสูจน์ด้วยตัวเองว่ามันจริงหรือไม่

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
