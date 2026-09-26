---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — รู้จักบอร์ดและอีมูเลเตอร์"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก AIoT in Action (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY 4.0"
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

# บทเรียน 1.2 — รู้จักบอร์ดและอีมูเลเตอร์

## เปิด BENTO IDE รันโปรแกรมแรกใน BENTO Emulator โดยไม่ต้องมีบอร์ด

**โมดูล 1 — รู้จักระบบสมองกลฝังตัวและเขียนโปรแกรมแรก**

หลักสูตร **Explorer: เปิดโลกระบบสมองกลฝังตัว** · ต่อจากบทเรียน 1.1

---

## เป้าหมาย

1. เปิด BENTO IDE แล้วรันไฟล์ตัวอย่างใน BENTO Emulator จนเห็นชื่อบอร์ดขึ้นบนจอจำลอง
2. บอกความต่างระหว่าง Eva Kit กับ TESAIoT Dev Kit ได้อย่างน้อย 2 ข้อ
3. อธิบายได้ว่าอะไรที่อีมูเลเตอร์ตอบได้ และอะไรที่ต้องพิสูจน์บนบอร์ดจริง

---

## ก่อนเริ่ม

- จากบทที่แล้ว ส่วนไหนของหม้อหุงข้าวดิจิทัลที่ "ตัดสินใจ"
- ถ้าไม่มีบอร์ดในมือ คุณคิดว่าจะเรียนเขียนโปรแกรมให้บอร์ดได้แค่ไหน

**สิ่งที่ต้องมี:** คอมพิวเตอร์ที่เปิดเบราว์เซอร์ Chrome หรือ Edge ได้ (บทเรียนนี้ไม่ได้ออกแบบสำหรับมือถือ)

---

## ดูของจริงก่อน

ทำตามนี้ก่อน แล้วค่อยมาอ่านคำอธิบาย

1. เปิด **BENTO IDE** ที่ https://ide.tesaiot.dev/
2. IDE เปิดมาที่มุมมอง **Blocks** ให้กดปุ่ม **Python** ที่หัวจอ เพื่อสลับเป็นมุมมองโค้ด
3. คัดลอกโค้ดจาก [examples/01_board_knows_itself.py](examples/01_board_knows_itself.py) ไปวางในช่องแก้โค้ด
4. กดปุ่ม **BENTO Emulator** บนแถบเครื่องมือ แล้วกด **▶ Run** ในแผงนั้น
5. มองที่จอจำลอง คุณควรเห็นชื่อบอร์ดตัวสีฟ้า และบรรทัดบอกว่ามีไฟกี่ดวง ปุ่มกี่ปุ่ม

ถ้าเห็นแล้ว ยินดีด้วย คุณเพิ่งรันโปรแกรมบนไมโครคอนโทรลเลอร์ (จำลอง) เป็นครั้งแรก

---

## ภาพจอจาก BENTO Emulator

<figure><img src="img/screens/01_board_knows_itself.webp" alt="จอของ examples/01_board_knows_itself.py ขณะรันใน BENTO Emulator" width="800" height="480"></figure>

[01_board_knows_itself.py](examples/01_board_knows_itself.py)

---

## แนวคิด — บอร์ดสองรุ่นที่ใช้โค้ดชุดเดียวกัน

หลักสูตรใน TESA Open Knowledge ใช้บอร์ดที่มีชิป **PSoC™ Edge E84** ของ Infineon อยู่สองรุ่น

| | Eva Kit | TESAIoT Dev Kit |
|---|---|---|
| หลอด LED ที่ Python สั่งได้ | 3 ดวง | 5 ดวง |
| เซนเซอร์เพิ่มเติม | — | อุณหภูมิ ความชื้น ความกดอากาศ เรดาร์ |
| จอ | สัมผัส 800×480 จุด | สัมผัส 800×480 จุด |

ตัวอย่างในบทนี้ไม่ได้จำว่าบอร์ดมีไฟกี่ดวง มันถาม `gpio.board_info()` ซึ่งคืนข้อมูลก้อนหนึ่งที่มีชื่อบอร์ด จำนวนไฟ และรายชื่อไฟ — โค้ดชุดเดียวจึงรันได้บนทั้งสองบอร์ด และในอีมูเลเตอร์ด้วย

---

## แนวคิด — MicroPython

โปรแกรมที่เราเขียนเป็นภาษา **MicroPython** — Python ฉบับที่เล็กพอจะรันบนไมโครคอนโทรลเลอร์ได้ ไม่ต้องคอมไพล์ กดรันแล้วเห็นผลเลย

โมดูลของ BENTO ที่ใช้บ่อยในหลักสูตรนี้

- `ui` — วาดบนจอ
- `lcd` — ลิ้นชัก Console
- `gpio` — ไฟและปุ่ม
- `sensors`, `wifi`, `mqtt` — เซนเซอร์และเครือข่าย

---

## แนวคิด — อีมูเลเตอร์ตอบอะไรได้ และอะไรตอบไม่ได้

**BENTO Emulator** รันโปรแกรม MicroPython ของเราในเบราว์เซอร์ และวาดจอขนาดเท่าจอบอร์ด ปุ่ม **HW** เปิดแผงฮาร์ดแวร์จำลองที่มีหลอดไฟ ปุ่ม ลูกบิด และแผ่นเอียง

อีมูเลเตอร์ตอบคำถาม **"โปรแกรมรันจบไหม มีข้อผิดพลาดไหม หน้าจอหน้าตาแบบไหน"** ได้ดีมาก

แต่มันไม่ใช่บอร์ดจริง ค่าเซนเซอร์เป็นค่าจำลอง WiFi เป็นของจำลอง เรื่องจังหวะเวลาหรือข้อจำกัดฮาร์ดแวร์บางอย่างไม่มีทางโผล่ในเบราว์เซอร์

> **ใช้อีมูเลเตอร์เรียนแนวคิด ใช้บอร์ดจริงพิสูจน์และวัดผล**

---

## ตัวอย่างสมบูรณ์

[examples/01_board_knows_itself.py](examples/01_board_knows_itself.py) — ย่อมาจากตัวอย่างของหลักสูตร AIoT in Action

```python
info = gpio.board_info()           # ท่าที่ 1: ถามบอร์ดครั้งเดียว

ui.screen()                         # ท่าที่ 2: ล้างจอ
time.sleep_ms(200)

ui.Label(info["name"], x=24, y=64, color=COL_ACCENT, value=24)   # ท่าที่ 3
ui.poll()                           # ป้ายขึ้นจอทันที

lcd.clear()                         # ท่าที่ 4: รายละเอียดยาว ๆ ลงลิ้นชัก
for i, name in enumerate(info["led_names"]):
    lcd.print("gpio.led(" + str(i) + ") =", name)
```

---

## ฝึกเติม

ท้ายไฟล์ตัวอย่างมีโจทย์ "ตาคุณ" อยู่ ให้เพิ่มลูปพิมพ์รายชื่อปุ่มจาก `info["btn_names"]` แบบเดียวกับลูปพิมพ์รายชื่อไฟ

ก่อนรัน ลองทำนายว่าอีมูเลเตอร์จะรายงานปุ่มกี่ปุ่ม แล้วรันเทียบ

---

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

1. เรียงขั้นตอนรันโปรแกรมใน BENTO Emulator ให้ถูกลำดับ
2. หลังสร้าง `ui.Label` แล้ว ควรเรียกคำสั่งใดเพื่อให้ป้ายขึ้นจอทันที
3. ข้อใดคือความต่างระหว่าง Eva Kit กับ TESAIoT Dev Kit (เลือกได้มากกว่าหนึ่งข้อ)
4. คำถามใดที่ BENTO Emulator ตอบได้น่าเชื่อถือที่สุด

---

## ไปต่อ

- ลองกด **HW** แล้วดูว่าแผงฮาร์ดแวร์จำลองมีอะไรบ้าง บทต่อไปเราจะสั่งหลอดไฟบนแผงนั้น
- ถ้าอยากรู้ว่าบอร์ดจริงตอบต่างจากอีมูเลเตอร์อย่างไร เปิดไฟล์ต้นฉบับ
  [`10_board_knows_itself.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/10_board_knows_itself.py)
  ที่ถามบอร์ดต่อว่าโมดูล `machine` มีคำสั่งไหนบ้าง

บทถัดไป: [บทเรียน 1.3 — โปรแกรมแรก: เขียนบนจอและเปิดไฟ](../l03-first-program/README.md)

---

## แหล่งที่มาและเครดิต

"Explorer: เปิดโลกระบบสมองกลฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์
วิศวกรรมระบบสมองกลฝังตัว มหาวิทยาลัยบูรพา (BUU) · Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)
