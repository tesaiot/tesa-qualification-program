---
id: explore.m01.l03
lang: th
title:
  th: "โปรแกรมแรก: เขียนบนจอและเปิดไฟ"
  en: "First program: draw on the screen and light an LED"
summary:
  th: เขียน MicroPython ให้ข้อความขึ้นจอ พิมพ์ลงลิ้นชัก Console และสั่งหลอด LED กะพริบเป็นจังหวะพร้อมตัวนับรอบ
  en: Write MicroPython that puts text on the screen, prints to the Console drawer, and blinks an LED in rhythm with a counter.
level: L1
time_min: {concept: 8, practise: 15, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [explore.m01.l02]
objectives:
  - th: เขียนโปรแกรมที่วางป้ายข้อความบนจอด้วย ui.Label และพิมพ์ลงลิ้นชัก Console ด้วย lcd.print แล้วรันผ่านโดยไม่มีข้อผิดพลาด
    en: Write a program that places a text label with ui.Label and prints to the Console drawer with lcd.print, running without errors.
  - th: สั่งหลอด LED ติดและดับเป็นจังหวะด้วย gpio.led(n).on() และ off() กับ time.sleep_ms() ให้ครบจำนวนรอบที่กำหนด
    en: Blink an LED in rhythm with gpio.led(n).on(), off() and time.sleep_ms() for a given number of times.
  - th: ทำนายผลของโปรแกรมก่อนรัน และอธิบายได้ว่าทำไมโปรแกรมควรจบด้วย led.off()
    en: Predict a program's result before running it, and explain why the program should end with led.off().
develops:
  - {skill: lang.micropython, to: 1}
  - {skill: mcu.gpio, to: 1}
  - {skill: gui.embedded, to: 1}
assesses:
  - {skill: mcu.gpio, level: 1, evidence: practice/blink_count.py}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, emulator: bento-emulator}
status: alpha
translation: done
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s03/02_led_blink.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## เป้าหมาย

1. วางป้ายข้อความบนจอด้วย `ui.Label` และพิมพ์ลงลิ้นชัก Console ด้วย `lcd.print` แล้วรันผ่าน
2. สั่งหลอด LED กะพริบด้วย `gpio.led(n).on()` / `off()` และ `time.sleep_ms()` ให้ครบจำนวนรอบ
3. ทำนายผลก่อนรัน และอธิบายได้ว่าทำไมโปรแกรมควรจบด้วย `led.off()`

## ก่อนเริ่ม

- จากบทที่แล้ว คำสั่งไหนที่ทำให้ป้ายขึ้นจอทันทีหลังสร้าง
- ในอีมูเลเตอร์ ปุ่มไหนเปิดแผงฮาร์ดแวร์จำลองที่มีหลอดไฟ

## ดูของจริงก่อน

ก่อนอ่านโค้ด ให้ **ทำนาย** ก่อน เปิด [examples/02_blink.py](examples/02_blink.py) อ่านแค่สามบรรทัดบนสุดที่ตั้งค่า `ROUNDS` `ON_MS` และ `OFF_MS`
แล้วเขียนลงกระดาษว่า "ไฟจะกะพริบกี่ครั้ง แต่ละครั้งนานเท่าไร"

จากนั้น **รัน** ใน BENTO Emulator (กด **HW** เพื่อเปิดแผงฮาร์ดแวร์จำลองก่อน แล้วกด **▶ Run**) หรือบนบอร์ดจริงด้วย **Program to Device**
แล้วเทียบกับที่ทำนายไว้

## แนวคิด

### 1. ข้อความหนึ่งบรรทัดไปได้สามที่

| คำสั่ง | ข้อความไปที่ไหน | ใครเห็น |
|---|---|---|
| `ui.Label("...")` | บนจอ ตรงตำแหน่ง x, y ที่กำหนด | คนที่มองจอ |
| `lcd.print("...")` | ลิ้นชัก Console บนจอ (เปิดด้วยปุ่มสีเขียวมุมขวาล่าง) | คนที่เปิดลิ้นชัก |
| `print("...")` | คอนโซลฝั่งคอมพิวเตอร์ | คนที่นั่งหน้าคอม |

สามที่นี้เป็นคนละที่กัน มือใหม่หลายคนรันแล้วบอกว่า "ไม่เห็นอะไรเลย" ทั้งที่ข้อความไปรออยู่อีกที่หนึ่ง
ลองรัน [examples/01_hello_screen.py](examples/01_hello_screen.py) แล้วตามหาข้อความให้ครบทั้งสามที่

### 2. กะพริบหนึ่งครั้งคือสี่จังหวะ

สั่งติด รอ สั่งดับ รอ เวลาที่รอคือสิ่งที่กำหนดจังหวะ ไมโครคอนโทรลเลอร์ทำงานเร็วมาก ถ้าไม่มี `time.sleep_ms()`
ไฟจะติดและดับเร็วเกินกว่าตาจะมองทัน

`led.on()` กับ `led.off()` สั่งค่าตรง ๆ อ่านบรรทัดเดียวก็รู้ว่าไฟจะเป็นอะไร นี่คือเหตุผลที่เราเลือกใช้สองคำสั่งนี้ก่อน

### 3. โปรแกรมที่ดีบอกได้ว่าจบที่สถานะไหน

ถ้าโปรแกรมจบตอนไฟกำลังติด ไฟจะค้างติดต่อไปโดยไม่มีใครตั้งใจ งานจริงอย่างไฟเตือนในโรงงานจะทำให้คนเข้าใจผิดได้
ตัวอย่างทุกไฟล์ในหลักสูตรนี้จึงเริ่มด้วย `led.off()` (เริ่มจากสถานะที่รู้แน่) และจบด้วย `led.off()` (จบที่สถานะที่รู้แน่)

## ตัวอย่างสมบูรณ์

[examples/02_blink.py](examples/02_blink.py) ย่อมาจาก
[`examples/s03/02_led_blink.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/02_led_blink.py)
ของหลักสูตร AIoT in Action

- **ท่าที่ 1 เลือกหลอด** ถามรายชื่อไฟจาก `gpio.board_info()` แล้วเลือกดวงที่ชื่อขึ้นต้นด้วย `RGB_` ถ้าไม่มีใช้ดวงแรก
- **ท่าที่ 2 เริ่มจากสถานะที่รู้แน่** `led.off()`
- **ท่าที่ 3 วางป้ายและตัวเลข** ป้ายบอกสถานะ กับ `ui.Seg7` ที่แสดงตัวเลขแบบนาฬิกาดิจิทัล
- **ท่าที่ 4 วนกะพริบ** ในลูป `for` สั่งติด อัปเดตป้าย รอ สั่งดับ นับรอบ รอ
- **ท่าที่ 5 จบที่สถานะที่รู้แน่** `led.off()` อีกครั้ง

ไฟล์ [examples/01_hello_screen.py](examples/01_hello_screen.py) ย่อมาจาก
[`examples/s01/01_first_line.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/01_first_line.py)
ใช้ท่าที่ 3 แบบเดียวกัน

**ภาพจอจาก BENTO Emulator** ของตัวอย่างในบทนี้ (คลิกชื่อไฟล์เพื่อเปิดโค้ด)

<div class="tok-screens">
<figure><img src="img/screens/01_hello_screen.webp" alt="จอของ examples/01_hello_screen.py ขณะรันใน BENTO Emulator" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_hello_screen.py"><code>01_hello_screen.py</code></a></figcaption></figure>
<figure><img src="img/screens/02_blink.webp" alt="จอของ examples/02_blink.py ขณะรันใน BENTO Emulator" width="800" height="480" loading="lazy"><figcaption><a href="examples/02_blink.py"><code>02_blink.py</code></a></figcaption></figure>
</div>

## ฝึกเติม

เปิด [practice/blink_count.py](practice/blink_count.py) มีช่องให้เติม 2 จุด (บรรทัดที่ขึ้นต้นด้วย `# เติม:`)

- เติมที่ 1 สั่งหลอดให้ติด
- เติมที่ 2 เพิ่มตัวนับขึ้นหนึ่ง แล้วเขียนเลขใหม่ลงจอ

ถ้าอยากฝึกแบบไม่ต้องพิมพ์ ลองเรียงบรรทัดโค้ดใน quiz ข้อที่ 3 ให้ถูกลำดับก่อน (แบบฝึก Parsons) แล้วค่อยกลับมาเติมไฟล์จริง

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/blink_count.py](solution/blink_count.py) เทียบ
คอมเมนต์ในเฉลยอธิบายว่า "ทำไม" ต้องนับตอนดับ และทำไมต้องใช้ `str()` ก่อนส่งให้ `Seg7`

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

## แล็บ

**แก้แล้วรันใหม่ (Modify)** ตั้ง `ON_MS = 50` และ `OFF_MS = 950` ใน [examples/02_blink.py](examples/02_blink.py) ทำนายก่อนว่าไฟจะดูเป็นอย่างไร แล้วรันจริง

**สร้างเอง (Make)** เขียนโปรแกรมใหม่ที่กะพริบเป็นรหัสสั้น–ยาว เช่น สั้นสามครั้ง ยาวสามครั้ง สั้นสามครั้ง
แล้วถ่ายภาพหน้าจอ (หรือคลิปสั้นถ้าใช้บอร์ดจริง) เก็บไว้เป็นหลักฐานใน portfolio ของคุณ

## ไปต่อ

ไฟกะพริบคือ "Hello, World" ของโลกระบบฝังตัว ถ้าอยากเห็นว่าหลอดดวงเดียวหรี่ความสว่างได้อย่างไร
ดูตัวอย่าง [`examples/s03/03_led_brightness.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py)
ในหลักสูตร AIoT in Action

## สะท้อนคิด

ตอนทำนายกับตอนรันจริงต่างกันไหม ถ้าต่าง ต่างเพราะอะไร การทำนายก่อนรันเปลี่ยนวิธีที่คุณอ่านโค้ดไหม
