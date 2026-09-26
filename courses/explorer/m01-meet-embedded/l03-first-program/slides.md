---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.3 — โปรแกรมแรก: เขียนบนจอและเปิดไฟ"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก AIoT in Action (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY-NC 4.0"
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

# บทเรียน 1.3 — โปรแกรมแรก: เขียนบนจอและเปิดไฟ

## เขียน MicroPython ให้ข้อความขึ้นจอ และสั่งหลอด LED กะพริบเป็นจังหวะ

**โมดูล 1 — รู้จักระบบสมองกลฝังตัวและเขียนโปรแกรมแรก**

หลักสูตร **Explorer: เปิดโลกระบบสมองกลฝังตัว** · ต่อจากบทเรียน 1.2

---

## เป้าหมาย

1. วางป้ายข้อความบนจอด้วย `ui.Label` และพิมพ์ลงลิ้นชัก Console ด้วย `lcd.print` แล้วรันผ่าน
2. สั่งหลอด LED กะพริบด้วย `gpio.led(n).on()` / `off()` และ `time.sleep_ms()` ให้ครบจำนวนรอบ
3. ทำนายผลก่อนรัน และอธิบายได้ว่าทำไมโปรแกรมควรจบด้วย `led.off()`

---

## ก่อนเริ่ม

- จากบทที่แล้ว คำสั่งไหนที่ทำให้ป้ายขึ้นจอทันทีหลังสร้าง
- ในอีมูเลเตอร์ ปุ่มไหนเปิดแผงฮาร์ดแวร์จำลองที่มีหลอดไฟ

---

## ดูของจริงก่อน

ก่อนอ่านโค้ด ให้ **ทำนาย** ก่อน เปิด [examples/02_blink.py](examples/02_blink.py) อ่านแค่สามบรรทัดบนสุดที่ตั้งค่า `ROUNDS` `ON_MS` `OFF_MS`

เขียนลงกระดาษว่า "ไฟจะกะพริบกี่ครั้ง แต่ละครั้งนานเท่าไร"

จากนั้น **รัน** ใน BENTO Emulator (กด **HW** เปิดแผงฮาร์ดแวร์จำลองก่อน แล้วกด **▶ Run**) หรือบนบอร์ดจริงด้วย **Program to Device** แล้วเทียบกับที่ทำนายไว้

---

## ภาพจอจาก BENTO Emulator

<figure><img src="img/screens/01_hello_screen.webp" alt="จอของ examples/01_hello_screen.py ขณะรันใน BENTO Emulator" width="380" height="228"><img src="img/screens/02_blink.webp" alt="จอของ examples/02_blink.py ขณะรันใน BENTO Emulator" width="380" height="228"></figure>

[01_hello_screen.py](examples/01_hello_screen.py) · [02_blink.py](examples/02_blink.py)

---

## แนวคิด — ข้อความหนึ่งบรรทัดไปได้สามที่

| คำสั่ง | ข้อความไปที่ไหน | ใครเห็น |
|---|---|---|
| `ui.Label("...")` | บนจอ ตรงตำแหน่ง x, y | คนที่มองจอ |
| `lcd.print("...")` | ลิ้นชัก Console บนจอ | คนที่เปิดลิ้นชัก |
| `print("...")` | คอนโซลฝั่งคอมพิวเตอร์ | คนที่นั่งหน้าคอม |

สามที่นี้เป็นคนละที่กัน มือใหม่หลายคนรันแล้วบอกว่า "ไม่เห็นอะไรเลย" ทั้งที่ข้อความไปรออยู่อีกที่หนึ่ง

ลองรัน [examples/01_hello_screen.py](examples/01_hello_screen.py) แล้วตามหาข้อความให้ครบทั้งสามที่

---

## แนวคิด — กะพริบหนึ่งครั้งคือสี่จังหวะ

**สั่งติด → รอ → สั่งดับ → รอ**

เวลาที่รอคือสิ่งที่กำหนดจังหวะ ไมโครคอนโทรลเลอร์ทำงานเร็วมาก ถ้าไม่มี `time.sleep_ms()` ไฟจะติดและดับเร็วเกินกว่าตาจะมองทัน

`led.on()` กับ `led.off()` สั่งค่าตรง ๆ อ่านบรรทัดเดียวก็รู้ว่าไฟจะเป็นอะไร นี่คือเหตุผลที่เราเลือกใช้สองคำสั่งนี้ก่อน

---

## แนวคิด — โปรแกรมที่ดีบอกได้ว่าจบที่สถานะไหน

ถ้าโปรแกรมจบตอนไฟกำลังติด ไฟจะค้างติดต่อไปโดยไม่มีใครตั้งใจ งานจริงอย่างไฟเตือนในโรงงานจะทำให้คนเข้าใจผิดได้

ตัวอย่างทุกไฟล์ในหลักสูตรนี้จึง

- **เริ่ม** ด้วย `led.off()` (เริ่มจากสถานะที่รู้แน่)
- **จบ** ด้วย `led.off()` (จบที่สถานะที่รู้แน่)

---

## ตัวอย่างสมบูรณ์

[examples/02_blink.py](examples/02_blink.py) ย่อมาจากตัวอย่างของหลักสูตร AIoT in Action

```python
led = gpio.led(LED)
led.off()                  # ท่าที่ 2: เริ่มจากสถานะที่รู้แน่ว่าคืออะไร

rounds = 0
for k in range(ROUNDS):    # ท่าที่ 4: วนกะพริบ
    led.on()
    state.text("ติด")
    ui.poll()
    time.sleep_ms(ON_MS)

    led.off()
    rounds = rounds + 1
    seg.text(str(rounds))  # Seg7 รับข้อความ ไม่ใช่ตัวเลข จึงต้อง str()
    ui.poll()
    time.sleep_ms(OFF_MS)

led.off()                  # ท่าที่ 5: จบที่สถานะที่รู้แน่
```

---

## ฝึกเติม

เปิด [practice/blink_count.py](practice/blink_count.py) มีช่องให้เติม 2 จุด (บรรทัดที่ขึ้นต้นด้วย `# เติม:`)

- เติมที่ 1 สั่งหลอดให้ติด
- เติมที่ 2 เพิ่มตัวนับขึ้นหนึ่ง แล้วเขียนเลขใหม่ลงจอ

ถ้าอยากฝึกแบบไม่ต้องพิมพ์ ลองเรียงบรรทัดโค้ดใน quiz ข้อที่ 3 ให้ถูกลำดับก่อน (แบบฝึก Parsons) แล้วค่อยกลับมาเติมไฟล์จริง

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/blink_count.py](solution/blink_count.py) เทียบ

---

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

1. คำสั่ง `lcd.print("สวัสดี")` ทำให้ข้อความไปปรากฏที่ใด
2. โค้ด `ui.Label("สวัสดี", x=24, y=8, color=0xE8EAED, value=28)` ตัวเลข `value=28` หมายถึงอะไร
3. เรียงบรรทัดในลูปกะพริบให้ถูกลำดับ (กะพริบหนึ่งครั้ง)
4. ถ้า `ROUNDS = 6, ON_MS = 250, OFF_MS = 250` โปรแกรมกะพริบใช้เวลาประมาณเท่าไร
5. ทำไมตัวอย่างจึงเรียก `led.off()` อีกครั้งหลังจบลูป

---

## แล็บ

**แก้แล้วรันใหม่ (Modify):** ตั้ง `ON_MS = 50` และ `OFF_MS = 950` ใน [examples/02_blink.py](examples/02_blink.py) ทำนายก่อนว่าไฟจะดูเป็นอย่างไร แล้วรันจริง

**สร้างเอง (Make):** เขียนโปรแกรมใหม่ที่กะพริบเป็นรหัสสั้น–ยาว เช่น สั้นสามครั้ง ยาวสามครั้ง สั้นสามครั้ง แล้วถ่ายภาพหน้าจอ (หรือคลิปสั้นถ้าใช้บอร์ดจริง) เก็บไว้เป็นหลักฐานใน portfolio ของคุณ

---

## ไปต่อ

ไฟกะพริบคือ "Hello, World" ของโลกระบบฝังตัว ถ้าอยากเห็นว่าหลอดดวงเดียวหรี่ความสว่างได้อย่างไร ดูตัวอย่าง [`03_led_brightness.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py) ในหลักสูตร AIoT in Action

บทถัดไปเข้าสู่โมดูล 2: [บทเรียน 2.1 — อ่านเซนเซอร์แล้วดูค่าเปลี่ยน](../../m02-sense-and-connect/l01-read-a-sensor/README.md)

---

## แหล่งที่มาและเครดิต

"Explorer: เปิดโลกระบบสมองกลฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์
วิศวกรรมระบบสมองกลฝังตัว มหาวิทยาลัยบูรพา (BUU) · Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)
