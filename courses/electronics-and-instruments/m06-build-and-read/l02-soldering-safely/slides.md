---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.2 — บัดกรีอย่างปลอดภัย"
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

# บทเรียน 6.2 — บัดกรีอย่างปลอดภัย

## บัดกรีจุดต่อที่ดี ตรวจงานด้วยตาและมัลติมิเตอร์ และทำงานอย่างปลอดภัยต่อตัวเองและบอร์ด

**โมดูล 6 — ต่อวงจร บัดกรี อ่านแผนผัง และพื้นฐาน PCB กับ EMC**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. บัดกรีหัวต่อ (header) หนึ่งแถวที่ไม่มีจุดเย็นหรือสะพานตะกั่ว และตรวจด้วยมัลติมิเตอร์
2. ระบุข้อปฏิบัติด้านความปลอดภัยของงานบัดกรีได้อย่างน้อยสี่ข้อ พร้อมเหตุผล

---

## ก่อนเริ่ม

- หัวแร้งปรับอุณหภูมิได้, แท่นวาง, ฟองน้ำ/ฝอยทองเหลือง, ตะกั่วมีฟลักซ์ในแกน, ลวดซับตะกั่ว
- แผ่นฝึก (perfboard) หรือบอร์ดเซนเซอร์ราคาถูกที่ยังไม่บัดกรี, หัวต่อตัวผู้ 1×8 ขา
- แว่นตานิรภัย, สายรัดข้อมือกันไฟฟ้าสถิต, เครื่องดูดควัน

> **ห้ามฝึกบัดกรีบน TESAIoT Dev Kit หรือ Eva Kit** ความร้อนที่ผิดจังหวะทำให้แผ่นทองแดงหลุดหรือชิปเสียได้ ฝึกบนแผ่นฝึกจนมั่นใจก่อน
> ปลายหัวแร้งร้อนราวสามร้อยกว่าองศา — วางบนแท่นทุกครั้งที่ไม่ได้ใช้ ถ้าหล่น **ห้ามคว้า**

---

## ดูของจริงก่อน

ส่องขาของหัวต่อบนบอร์ดสำเร็จรูปด้วยแว่นขยาย เทียบกับจุดบัดกรีของบอร์ดที่เพื่อนเพิ่งหัดบัดกรี

จุดของโรงงานมีรูปทรงเหมือนกันทุกจุด เป็นกรวยเรียบลาดจากขาลงไปถึงแผ่นทองแดง จุดที่ไม่ดีจะเห็นเป็นก้อนกลม ผิวขรุขระ มีช่องว่างระหว่างตะกั่วกับแผ่น หรือตะกั่วเชื่อมสองขาเข้าด้วยกัน — ข้อสังเกตนี้คือเครื่องมือตรวจชิ้นแรกของคุณ ตาที่ฝึกแล้วจะจับจุดเสียได้ก่อนมัลติมิเตอร์

---

## แนวคิด (1) — ตะกั่ว อุณหภูมิ และฟลักซ์

- ตะกั่วมีสารตะกั่ว Sn63/Pb37 หลอมที่ 183 °C · ตะกั่วไร้สารตะกั่ว SAC305 หลอมราว 217–220 °C
- อุณหภูมิหัวแร้ง: ราว 320–350 °C (มีสารตะกั่ว), 350–380 °C (ไร้สารตะกั่ว)
- **ฟลักซ์** ขจัดชั้นออกไซด์ ทำให้ตะกั่วเปียกและไหลเกาะผิว (wetting)

**ขั้นตอนบัดกรีหนึ่งจุด**

```text
1. เช็ดและเคลือบตะกั่วบาง ๆ ที่ปลายหัวแร้ง (tinning)
2. แตะปลายหัวแร้งให้สัมผัสทั้งขาและแผ่นทองแดงพร้อมกัน รอราวหนึ่งวินาที
3. ป้อนตะกั่วที่จุดต่อ (ฝั่งตรงข้ามหัวแร้ง) ไม่ใช่ที่ปลายหัวแร้ง
4. ตะกั่วไหลรอบขาเป็นกรวย ดึงตะกั่วออกก่อน แล้วจึงดึงหัวแร้งออก (ราว 2-3 วินาที)
5. อย่าขยับชิ้นงานจนตะกั่วแข็งตัว
```

---

## แนวคิด (2) — จุดที่ดี จุดที่เสีย

<figure>
<svg viewBox="0 0 420 175" width="420" role="img" aria-label="ภาพตัดขวางของจุดบัดกรีที่ดี จุดเย็น และสะพานตะกั่ว" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M20 110H120"/><path d="M50 110H90" stroke-width="4"/>
<path d="M70 40V120"/>
<path d="M32 110C50 108 64 96 66 70M108 110C90 108 76 96 74 70"/>
<text x="70" y="150" text-anchor="middle" fill="currentColor" stroke="none">good: shiny, concave</text>
<text x="70" y="166" text-anchor="middle" fill="currentColor" stroke="none">wets pin and pad</text>
<path d="M150 110H250"/><path d="M180 110H220" stroke-width="4"/>
<path d="M200 40V120"/>
<path d="M178 108C170 90 185 72 200 72C215 72 230 90 222 108"/>
<text x="200" y="150" text-anchor="middle" fill="currentColor" stroke="none">cold / not wetted:</text>
<text x="200" y="166" text-anchor="middle" fill="currentColor" stroke="none">dull ball, gap at pad</text>
<path d="M280 110H400"/>
<path d="M292 110H318M362 110H388" stroke-width="4"/>
<path d="M305 40V120M375 40V120"/>
<path d="M296 110C300 86 320 84 340 88C360 84 380 86 384 110"/>
<text x="340" y="150" text-anchor="middle" fill="currentColor" stroke="none">bridge: solder joins</text>
<text x="340" y="166" text-anchor="middle" fill="currentColor" stroke="none">two pins</text>
</svg>
<figcaption>ซ้าย: จุดที่ดีเป็นกรวยเว้าเข้า กลาง: จุดเย็นเป็นก้อนกลมไม่เกาะแผ่น ขวา: สะพานตะกั่วเชื่อมสองขา</figcaption>
</figure>

---

## แนวคิด (3) — ตรวจด้วยมัลติมิเตอร์ (ถอดไฟแล้วเสมอ)

- **ความต่อเนื่องจากขาถึงลายวงจร** ต้องดัง ถ้าไม่ดังคือจุดเย็นหรือลายขาด
- **ขาติดกันต้องไม่ต่อกัน** แตะขาคู่ที่อยู่ติดกันทีละคู่ ต้อง**ไม่**ดัง (ยกเว้นวงจรตั้งใจให้ต่อกัน)

**ไฟฟ้าสถิตตัวเลขเล็ก ผลใหญ่** แบบจำลองร่างกายคน: ตัวเก็บประจุ 100 pF คายผ่าน 1.5 kΩ

```text
ที่ 2,000 V: พลังงาน = ½ × 100pF × (2000V)² = 0.2 mJ
             กระแสสูงสุด ≈ 2000V / 1.5kΩ = 1.33 A
```

พลังงานน้อยจนคนไม่รู้สึก แต่กระแสระดับแอมแปร์วิ่งผ่านโครงสร้างจิ๋วในชิปเพียงเสี้ยว µs ก็ทำให้ขาเสื่อมได้

---

## แนวคิด (4) — ความปลอดภัยของคนและของบอร์ด

| ข้อปฏิบัติ | เหตุผล |
|---|---|
| วางหัวแร้งบนแท่นทุกครั้ง | ปลายร้อนหลายร้อยองศา ไหม้ได้ในเสี้ยววินาที |
| ดูดควันออกจากจุดทำงาน | ควันฟลักซ์ (rosin) เป็นสาเหตุที่พบบ่อยของโรคหืดจากการทำงาน (HSE) |
| ใส่แว่นตานิรภัย | ตะกั่วและปลายขาที่ตัดทิ้งกระเด็นเข้าตาได้ |
| ล้างมือ ไม่กินที่โต๊ะบัดกรี | ตะกั่วมีสารตะกั่วเป็นพิษ |
| สายรัดข้อมือกันไฟฟ้าสถิต | ชิปเสียได้จากไฟฟ้าสถิตที่คนไม่รู้สึก |
| ถอดไฟ/แบตเตอรี่ก่อนบัดกรี | ความร้อนทำให้เซลล์ลิเทียมเสียหายหรือติดไฟ |

---

## ตัวอย่างสมบูรณ์ — บัดกรีหัวต่อ 1×8 ขา

```text
1. เตรียมพื้นที่  เปิดดูดควัน ใส่แว่น+สายรัดข้อมือ ตั้งหัวแร้ง 330°C (มีสารตะกั่ว)
2. จัดแนว        เสียบหัวต่อ ยึดด้วยเทป
3. ขาแรก         บัดกรีขา 1 ตรวจแนว แล้วบัดกรีขา 8
4. ขาที่เหลือ     ไล่ขา 2-7 ใช้เวลาจุดละ 2-3 วินาที เช็ดหัวแร้งทุกสองสามจุด
5. ตรวจด้วยตา     ส่องทุกจุดด้วยแว่นขยาย
6. ตรวจด้วยมิเตอร์ ขาทุกขาถึงลายวงจร (8 ครั้ง) คู่ขาติดกันไม่ต่อกัน (7 ครั้ง)
7. แก้           เติมฟลักซ์ ให้ความร้อนใหม่ หรือซับตะกั่วออก แล้วตรวจซ้ำ
8. ปิดงาน        ปิดหัวแร้ง ทำความสะอาด ล้างมือ
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. จับคู่ลักษณะกับชื่อ: ก้อนกลมด้านมีร่อง / ตะกั่วเชื่อมขา 3-4 / แผ่นทองแดงยก / กรวยเว้าเรียบ
2. ทำไมต้องป้อนตะกั่วที่จุดต่อ ไม่ใช่ที่ปลายหัวแร้ง

**แล็บ**

1. ฝึกบนแผ่นฝึกก่อน (อย่างน้อย 10 จุด) จนจุดสุดท้ายเหมือนภาพจุดที่ดี
2. บัดกรีหัวต่อ 1×8 ขาตามตัวอย่างสมบูรณ์ ถ่ายภาพระยะใกล้ทุกจุด แล้วตรวจด้วยมัลติมิเตอร์
3. **ฝึกแก้** ตั้งใจทำสะพานตะกั่วหนึ่งจุด วัดยืนยันว่าต่อกัน แล้วแก้ วัดยืนยันว่าแยกกันแล้ว

---

## เช็กความเข้าใจ

1. จุดบัดกรีที่ดีของขาหัวต่อบนแผ่นทองแดงมีลักษณะอย่างไร
   - ก) ก้อนกลมใหญ่ครอบขา · ข) กรวยเว้าเข้าเรียบ ตะกั่วเกาะทั้งขาและแผ่นทองแดงโดยไม่มีร่อง · ค) ผิวขรุขระด้านและมีร่องรอบแผ่น · ง) ตะกั่วเชื่อมไปถึงขาข้าง ๆ

2. หลังบัดกรีหัวต่อหนึ่งแถว จะตรวจหาสะพานตะกั่วด้วยมัลติมิเตอร์อย่างไร
   - ก) เปิดไฟแล้ววัดแรงดันทุกขา · ข) ถอดไฟ ใช้โหมดความต่อเนื่องวัดคู่ขาที่ติดกันทีละคู่ ต้องไม่ดัง · ค) วัดกระแสผ่านแต่ละขา · ง) วัดความต่อเนื่องจากขาไปลายวงจร

3. ข้อใดเป็นข้อปฏิบัติด้านความปลอดภัยที่ถูกต้องในงานบัดกรี (เลือกได้มากกว่าหนึ่งข้อ)
   - ก) ดูดควันออกจากจุดทำงาน และไม่ก้มหน้าเข้าหาควัน · ข) ใส่สายรัดข้อมือกันไฟฟ้าสถิตและจับบอร์ดที่ขอบ · ค) กินขนมที่โต๊ะบัดกรีได้ถ้าใช้ตะกั่วไร้สารตะกั่ว · ง) ใส่แว่นตานิรภัย · จ) ถ้าหัวแร้งหล่น รีบคว้าไว้ก่อนตกพื้น

---

## ไปต่อ

บัดกรีเป็นแล้ว ต่อไปต้องรู้ว่าจะต่ออะไรเข้ากับอะไร บทเรียนถัดไป [อ่านแผนผังวงจร](../l03-reading-schematics/README.md) จะฝึกตามสัญญาณจากขาของไมโครคอนโทรลเลอร์ไปถึงชิ้นส่วนบนแผนผังจริงของบอร์ด

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
