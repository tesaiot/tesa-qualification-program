---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — วัด PWM"
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

# บทเรียน 5.2 — วัด PWM

## วัด period ความถี่ และ duty cycle ของสัญญาณ PWM ที่หรี่หลอด LED และเทียบกับค่าที่โปรแกรมสั่ง

**โมดูล 5 — ออสซิลโลสโคป**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. วัดคาบเวลา (period) ความถี่ และ duty cycle ของ PWM จากรูปคลื่นได้
2. เทียบ duty cycle ที่วัดได้กับค่าที่โปรแกรมสั่ง และอธิบายเมื่อไม่ตรงกัน

---

## ก่อนเริ่ม

- ตั้งออสซิลโลสโคปให้ภาพนิ่งได้ (บทเรียน [ออสซิลโลสโคปเบื้องต้น](../l01-scope-basics/README.md)) และใช้ logic analyzer วัดเวลาได้
- TESAIoT Dev Kit ที่ flash QWA309 Header I/O Test, ออสซิลโลสโคปสองช่อง (หรือ logic analyzer), มัลติมิเตอร์

---

## ดูของจริงก่อน

หลักสูตร AIoT in Action มีตัวอย่างที่หรี่ LED ด้วย `led.brightness(pct)` แล้วอ่านค่ากลับด้วย `led.duty()` — มีการทดลองหนึ่งที่สั่ง `on()` แล้วตามด้วย `toggle()` หลอดดับไปแล้ว แต่ `duty()` ยังตอบเลขเดิม

ความเห็นในโค้ดสรุปว่า "duty() = สิ่งที่สั่ง ไม่ใช่สิ่งที่วัด" — นี่คือคำถามของบทนี้ ตัวเลขที่โปรแกรมบอก กับสัญญาณที่ออกจากขาจริง ตรงกันไหม เราจะตอบด้วยเครื่องมือวัด ไม่ใช่เชื่อตัวเลขบนจอ

---

## แนวคิด (1) — สามตัวเลขของ PWM

<figure>
<svg viewBox="0 0 380 200" width="380" role="img" aria-label="สัญญาณ PWM ความถี่เดียวกันที่ duty cycle 25 50 และ 75 เปอร์เซ็นต์" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="40,46 60,46 60,20 85,20 85,46 160,46 160,20 185,20 185,46 260,46 260,20 285,20 285,46 370,46"/>
<text x="30" y="46" text-anchor="end" fill="currentColor" stroke="none">25%</text>
<polyline points="40,96 60,96 60,70 110,70 110,96 160,96 160,70 210,70 210,96 260,96 260,70 310,70 310,96 370,96"/>
<text x="30" y="96" text-anchor="end" fill="currentColor" stroke="none">50%</text>
<polyline points="40,146 60,146 60,120 135,120 135,146 160,146 160,120 235,120 235,146 260,146 260,120 335,120 335,146 370,146"/>
<text x="30" y="146" text-anchor="end" fill="currentColor" stroke="none">75%</text>
<path d="M60 172V180M160 172V180M60 176H160"/>
<text x="110" y="192" text-anchor="middle" fill="currentColor" stroke="none">period T</text>
<text x="260" y="192" text-anchor="middle" fill="currentColor" stroke="none">duty D = t_high / T</text>
</svg>
<figcaption>PWM สามแถวมีคาบเวลาเท่ากัน ต่างกันที่สัดส่วนเวลาที่เป็น 1 (duty cycle)</figcaption>
</figure>

```text
T = คาบเวลา   f = 1/T   D = t_high/T   V_avg = D × V_high
ตัวอย่าง: T=2ms, t_high=0.5ms → f=500Hz, D=25%, V_avg=0.825V (บนขา 3.3V)
```

---

## แนวคิด (2) — PWM จากฮาร์ดแวร์กับซอฟต์แวร์

**ฮาร์ดแวร์ (timer)** นับขึ้นด้วยนาฬิกา f_clk ครบ N ครั้งก็เริ่มใหม่

```text
f_PWM = f_clk / N     D = compare / N     ความละเอียด = 1/N
ตัวอย่าง: f_clk=1MHz, N=1000 → PWM 1kHz, ความละเอียด duty 0.1%
```

**ซอฟต์แวร์** โปรแกรมเขียนขา 1 หน่วง เขียน 0 หน่วง วนไป — ใช้ขาไหนก็ได้ แต่เวลาของคำสั่งอื่นปนเข้าไปในจังหวะ คาบเวลาจึงยาวกว่าที่ตั้งเล็กน้อยและแกว่งได้ (jitter)

**คู่สัญญาณกลับเฟส** (H-bridge) **ห้ามเป็น 1 พร้อมกัน** ไม่งั้นลัดวงจรแหล่งจ่าย (shoot-through) — ระบบจริงต้องเว้น **dead time**

---

## แนวคิด (3) — ทำไมค่าที่วัดได้ไม่ตรงกับค่าที่สั่ง

| สาเหตุ | อาการ |
|---|---|
| ความละเอียดของตัวนับ | duty ถูกปัดเป็นขั้น (N=100 สั่ง 33.3% ได้จริง 33%) |
| PWM จากซอฟต์แวร์ | คาบเวลายาวกว่าที่ตั้ง และแกว่ง |
| ขั้วกลับ | duty ที่วัดได้เป็น 100% ลบค่าที่สั่ง |
| ตัวเลขในโปรแกรมไม่ใช่การวัด | โปรแกรมรายงานค่าที่สั่งครั้งล่าสุด (`duty()`) |
| ขาไม่ได้ต่อกับ PWM ของฮาร์ดแวร์ | ได้พัลส์สั้นแล้วหยุด |

**วิธีวัดให้แม่น** วัดที่ระดับ **50%** ของแรงดัน, เฉลี่ยหลายคาบเวลา, ความละเอียดเวลาต้องละเอียดกว่าขั้นของ duty ที่อยากตรวจ

---

## ตัวอย่างสมบูรณ์ — วัด PWM Out และเทียบกับค่าที่สั่ง

```text
1. ค่าที่สั่ง   t_high=20ms, T=40ms, f=25Hz, D=50%
2. ต่อ         CH1→P13.3, CH2→P13.4, 10ms/div, 1V/div, trigger ขาขึ้น CH1@1.65V
3. วัด CH1 (เฉลี่ย 10 คาบเวลา)  T=40.10ms, t_high=20.05ms
   f = 1/40.10ms = 24.94 Hz
   D = 20.05/40.10 = 50.0%
   คาบเวลายาวกว่าที่สั่ง 0.25%
4. อธิบาย      ลักษณะของ PWM จากซอฟต์แวร์ (เวลาคำสั่งปนทุกครึ่งคาบเวลา)
5. ตรวจคู่กลับเฟส  ซูมที่ขอบ ดูว่ามีช่วงที่ทั้งสองเส้นเป็น 1 พร้อมกันไหม
6. นับรอบ      ต้องได้ 50 พัลส์บน CH1
```

---

## ฝึกเติม / แล็บ

**ฝึกเติม**

1. PWM คาบเวลา 2 ms ความกว้างพัลส์ 0.5 ms — หาความถี่ duty และแรงดันเฉลี่ยบนขา 3.3 V
2. ตัวจับเวลาใช้นาฬิกา 10 MHz ต้องการ PWM 10 kHz ต้องนับกี่ครั้งต่อคาบเวลา ค่าเปรียบเทียบสำหรับ duty 33% คือเท่าไร

**แล็บ ส่วน A** PWM Out บน P13.3/P13.4 — ทำตามตัวอย่างสมบูรณ์ด้วยข้อมูลจริง

**แล็บ ส่วน B** PWM3 Out บน P15.2/P15.3 — วัดแบบเดียวกัน เทียบกับส่วน A

**แล็บ ส่วน C** มัลติมิเตอร์กับ PWM — วัด P13.3 ด้วยโหมดแรงดันไฟตรงระหว่างที่วิ่ง อธิบายว่าทำไมมันแกว่งรอบราว 1.65 V

---

## เช็กความเข้าใจ

1. PWM มีคาบเวลา 2 ms และความกว้างพัลส์ 0.5 ms ความถี่และ duty cycle เป็นเท่าไร
   - ก) 500 Hz และ 25% · ข) 2 kHz และ 25% · ค) 500 Hz และ 75% · ง) 250 Hz และ 50%

2. ขา 3.3 V ขับ PWM duty 40% ความถี่สูง ต่อวงจรกรองที่เฉลี่ยสัญญาณ จะได้แรงดันเฉลี่ยเท่าไร
   - ก) 1.32 V · ข) 1.98 V · ค) 3.3 V · ง) 0.40 V

3. โปรแกรมสั่ง duty 30% แต่วัดที่ขาได้ 70% ทุกค่าที่ลองสั่ง ผลรวมของค่าที่สั่งกับค่าที่วัดได้เป็น 100% เสมอ สาเหตุที่น่าจะเป็นที่สุดคืออะไร
   - ก) ความละเอียดของตัวนับไม่พอ · ข) ขั้วของสัญญาณกลับ · ค) ความถี่ของ PWM สูงเกินไป · ง) ออสซิลโลสโคปเสีย

---

## ไปต่อ

โมดูลถัดไปเริ่มที่ [ต่อวงจรบนเบรดบอร์ด](../../m06-build-and-read/l01-breadboarding/README.md) — ต่อวงจรที่ใหญ่ขึ้นให้ถูกตั้งแต่ครั้งแรก และตรวจด้วยเครื่องมือทั้งหมดที่ใช้เป็นแล้วก่อนเสียบไฟ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

แผนภาพในบทเรียนนี้เป็นงานวาดของหลักสูตรนี้เอง (CC BY 4.0)

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
