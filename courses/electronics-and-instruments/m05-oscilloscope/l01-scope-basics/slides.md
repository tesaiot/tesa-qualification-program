---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — ออสซิลโลสโคปเบื้องต้น"
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

# บทเรียน 5.1 — ออสซิลโลสโคปเบื้องต้น

## ตั้ง timebase, volts/div และ trigger และต่อสายกราวด์ของโพรบให้ถูก

**โมดูล 5 — ออสซิลโลสโคป**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้ง timebase, volts/div และ trigger ให้เห็นสัญญาณนิ่งบนจอ
2. อธิบายว่าทำไมสายกราวด์ของโพรบต้องต่อกับกราวด์ของวงจรและสั้นที่สุด
3. อธิบายว่าออสซิลโลสโคปให้ข้อมูลอะไรที่ logic analyzer ให้ไม่ได้

---

## ก่อนเริ่ม

- ออสซิลโลสโคป (ตั้งโต๊ะหรือแบบ USB) พร้อมโพรบ 10× และสปริงกราวด์
- TESAIoT Dev Kit ที่ flash QWA309 Header I/O Test — ใช้ปุ่ม PWM Out เป็นแหล่งสัญญาณ

> **ความปลอดภัย** ออสซิลโลสโคปตั้งโต๊ะส่วนใหญ่ต่อปากคีบกราวด์ของโพรบเข้ากับสายดินของปลั๊กไฟโดยตรง หนีบผิดจุดเท่ากับเอาสายลัดลงดิน หลักสูตรนี้วัดเฉพาะวงจรแรงดันต่ำที่กราวด์เดียวกับบอร์ด ห้ามใช้โพรบธรรมดาวัดไฟบ้านหรือวงจรที่กราวด์ลอย

---

## ดูของจริงก่อน

ต่อโพรบเข้าขา P13.3 ต่อกราวด์เข้า GND แล้วกดปุ่ม **PWM Out** โดยยังไม่ได้ตั้งอะไรเลย — ภาพน่าจะวิ่งไปมา เป็นเส้นตรง หรือเบลอ ทั้งที่สัญญาณจริงเป็นคลื่นสี่เหลี่ยม 25 Hz ธรรมดา

ออสซิลโลสโคปไม่ได้ "รู้" ว่าเราอยากดูอะไร ต้องบอกมันสามอย่าง: ดูช่วงเวลากว้างแค่ไหน ดูแรงดันช่วงไหน และเริ่มวาดภาพเมื่อไร

---

## แนวคิด (1) — timebase และ volts/div

จอส่วนใหญ่แบ่ง **10 ช่องแนวนอน** (เวลา) และ **8 ช่องแนวตั้ง** (แรงดัน)

```text
timebase: อยากเห็นคาบเวลา 40 ms ราว 2-3 คาบ → ทั้งจอ ~100 ms → 10 ms/div
volts/div: สัญญาณ 0-3.3 V ที่ 1 V/div สูง 3.3 ช่อง (ครึ่งถึงเกือบเต็มจอ)
```

ตั้ง **อัตราลดทอนของโพรบ** ในเมนูช่องให้ตรงกับสวิตช์บนโพรบ (1× หรือ 10×) ไม่ตรง ตัวเลขจะผิดสิบเท่า

**coupling** DC = แรงดันจริงทั้งหมด · AC = ตัดส่วนไฟตรงทิ้ง เหลือแต่ส่วนที่เปลี่ยน (ใช้ดู ripple เล็ก ๆ)

---

## แนวคิด (2) — trigger ทำให้ภาพนิ่ง

- **source** ช่องที่ใช้ตัดสิน · **slope** ขอบขาขึ้นหรือลง
- **level** ต้องอยู่ **ภายใน** ช่วงที่สัญญาณแกว่ง — กลางช่วงปลอดภัยที่สุด (เช่น 1.65 V สำหรับลอจิก 3.3 V)
- **mode**
  - Auto: วาดภาพเสมอแม้ไม่เจอ trigger — เหมาะหาสัญญาณครั้งแรก
  - Normal: วาดใหม่เฉพาะเมื่อเจอ trigger — เหมาะสัญญาณที่มาเป็นช่วง ๆ
  - Single: จับครั้งเดียวแล้วหยุด — เหมาะเหตุการณ์ครั้งเดียว เช่นการเด้งของปุ่ม

ถ้าภาพวิ่ง ตรวจตามลำดับ: source ถูกช่องไหม → level อยู่ในช่วงไหม → mode เหมาะไหม

---

## แนวคิด (3) — โพรบและกราวด์

<figure>
<svg viewBox="0 0 400 185" width="400" role="img" aria-label="สายกราวด์ของโพรบยาวทำให้เกิดวงลูปใหญ่ เทียบกับสปริงกราวด์สั้น" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="30" y="70" width="150" height="60" rx="3"/>
<text x="105" y="110" text-anchor="middle" fill="currentColor" stroke="none">board</text>
<rect x="60" y="14" width="60" height="18" rx="3"/>
<text x="90" y="10" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">probe</text>
<path d="M90 32V70"/>
<circle cx="90" cy="70" r="2.5" fill="currentColor"/>
<path d="M60 24C0 24 0 150 60 130"/>
<circle cx="60" cy="130" r="2.5" fill="currentColor"/>
<text x="64" y="146" font-size="11" fill="currentColor" stroke="none">GND clip</text>
<text x="105" y="175" text-anchor="middle" fill="currentColor" stroke="none">long ground lead = big loop</text>
<rect x="230" y="70" width="150" height="60" rx="3"/>
<text x="305" y="110" text-anchor="middle" fill="currentColor" stroke="none">board</text>
<rect x="260" y="14" width="60" height="18" rx="3"/>
<text x="290" y="10" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">probe</text>
<path d="M290 32V70"/>
<circle cx="290" cy="70" r="2.5" fill="currentColor"/>
<path d="M304 32V66"/>
<circle cx="304" cy="70" r="2.5" fill="currentColor"/>
<text x="310" y="52" font-size="11" fill="currentColor" stroke="none">GND spring</text>
<text x="305" y="175" text-anchor="middle" fill="currentColor" stroke="none">short ground spring = small loop</text>
</svg>
<figcaption>ซ้าย: สายกราวด์ยาวล้อมเป็นวงลูปใหญ่ ทำตัวเป็นตัวเหนี่ยวนำ+เสาอากาศ ขวา: สปริงกราวด์สั้น ลูปเล็ก ภาพขอบตรงกับของจริงกว่า</figcaption>
</figure>

---

## แนวคิด (4) — ทำไมสายกราวด์ต้องสั้น

```text
f = 1 / (2π √(L × C))
สายกราวด์ 15 cm ≈ 150 nH กับโพรบ 15 pF → f ≈ 106 MHz
สปริงกราวด์ 1 cm ≈ 10 nH กับโพรบ 15 pF → f ≈ 411 MHz
```

ขอบสัญญาณที่เร็วพอจะกระตุ้นวงนี้ให้สั่น (ringing) — **ไม่ได้อยู่บนบอร์ด** แต่เกิดจากวิธีวัดของเราเอง สปริงกราวด์ดันความถี่นี้สูงกว่าแบนด์วิดท์ของเครื่องทั่วไป

**แบนด์วิดท์และเวลาขาขึ้น** t_r ≈ 0.35 / BW — เครื่อง 100 MHz แสดงขอบเร็วสุดราว 3.5 ns

---

## แนวคิด (5) — ออสซิลโลสโคปกับ logic analyzer

| คำถาม | เครื่องที่ตอบได้ |
|---|---|
| แรงดันระดับ 1 จริงเป็นเท่าไร มีขอบเกินไหม | ออสซิลโลสโคป |
| ขอบขาขึ้นของ I2C ช้าเพราะ pull-up ใหญ่ไปไหม | ออสซิลโลสโคป |
| ไฟเลี้ยงกระเพื่อมเท่าไร มีหนามแหลมไหม | ออสซิลโลสโคป |
| ลำดับเหตุการณ์ของ 8–16 ขาพร้อมกัน นานหลายวินาที | logic analyzer |
| ถอดรหัส I2C หรือ UART ยาว ๆ | logic analyzer |

logic analyzer ตอบว่า "เกิดอะไรเมื่อไร" ส่วนออสซิลโลสโคปตอบว่า "สัญญาณหน้าตาเป็นอย่างไร"

---

## ตัวอย่างสมบูรณ์ — ตั้งเครื่องให้เห็นสัญญาณนิ่ง

```text
1. โพรบ    สวิตช์ 10× ตั้งเมนูช่องเป็น 10× ชดเชยโพรบก่อน
2. ต่อ     กราวด์/สปริงที่ GND ใกล้ P13.3 ที่สุด ปลายโพรบที่ P13.3
3. แนวตั้ง  DC coupling, 1 V/div, เส้น 0V ที่ช่องสองจากล่าง (สูง 3.3 ช่อง)
4. แนวนอน  คาบเวลา 40 ms → 10 ms/div (ทั้งจอ 100 ms)
5. trigger source CH1, ขาขึ้น, level 1.65 V, mode Normal
6. กด PWM Out  ภาพนิ่งระหว่างสัญญาณวิ่ง ค้างภาพสุดท้ายหลังหยุด
7. วัด     แรงดันสูงสุด, คาบเวลา, ความถี่ ด้วย cursor
8. ซูมขอบ  trigger Single, timebase ระดับ ns ดูหน้าตาขอบขาขึ้นลูกแรก
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. อยากเห็นคลื่น 1 kHz อย่างน้อยสองคาบเต็มบนจอ 10 ช่อง ควรใช้ timebase เท่าไร
2. เครื่องแบนด์วิดท์ 50 MHz แสดงเวลาขาขึ้นได้เร็วสุดประมาณเท่าไร

**แล็บ**

1. ชดเชยโพรบ — ถ่ายภาพจอสามแบบ (ชดเชยน้อยไป พอดี มากไป)
2. ภาพนิ่ง — ทำตามตัวอย่างสมบูรณ์
3. กราวด์ยาวกับสั้น — ซูมขอบใน Single วัด overshoot และความถี่การสั่นทั้งสองแบบ

---

## เช็กความเข้าใจ

1. สัญญาณมีคาบเวลา 40 ms อยากเห็นราวสองถึงสามคาบเวลาบนจอที่มี 10 ช่องแนวนอน ควรตั้ง timebase เท่าไร
   - ก) 1 ms/div · ข) 10 ms/div · ค) 100 ms/div · ง) 40 ms/div

2. ทำไมห้ามหนีบปากคีบกราวด์ของโพรบออสซิลโลสโคปตั้งโต๊ะไว้ที่ขา 3V3 ของบอร์ดที่เสียบ USB กับคอมพิวเตอร์
   - ก) จะอ่านค่าติดลบ · ข) ปากคีบกราวด์ต่อลงดินผ่านปลั๊กไฟ เท่ากับลัดวงจร 3V3 ลงกราวด์ · ค) โพรบ 10× รับ 3.3 V ไม่ได้ · ง) ไม่มีปัญหาถ้าตั้ง AC coupling

3. ข้อใดคือข้อมูลที่ออสซิลโลสโคปให้ได้ แต่ logic analyzer ทั่วไปให้ไม่ได้ (เลือกได้มากกว่าหนึ่งข้อ)
   - ก) แรงดันจริงของระดับ 1 และ 0 · ข) ขอบเกินและการสั่นที่ขอบ · ค) ลำดับการเปลี่ยนของ 16 ขาพร้อมกันนานหลายวินาที · ง) ขอบขาขึ้นที่ช้าเพราะ pull-up ของ I2C ใหญ่เกินไป

---

## ไปต่อ

บทเรียนถัดไป [วัด PWM](../l02-measuring-pwm/README.md) — ใช้ทั้งออสซิลโลสโคปและ logic analyzer วัดคาบเวลาและ duty cycle แล้วเทียบกับค่าที่โปรแกรมสั่ง

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
