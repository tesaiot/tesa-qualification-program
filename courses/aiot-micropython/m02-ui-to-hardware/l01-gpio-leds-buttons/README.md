---
id: aiot-mpy.m02.l01
lang: th
title: {th: 'โมดูล gpio: LED ปุ่ม และบอร์ดที่บอกได้ว่ามีอะไร', en: 'The gpio module: LEDs, a button and a board that describes itself'}
summary: {th: เปิดโมดูล gpio ให้เห็นครบทั้ง 18 ชื่อ สั่ง LED และอ่านปุ่มจริงจาก Python แล้วเขียนโค้ดที่ถามบอร์ดเองว่ามีไฟกี่ดวง ไฟล์เดียวจึงรันได้ทั้ง Eva Kit และ Dev Kit, en: 'Open up all 18 names of the gpio module, drive the LEDs and read the real button from Python, and write code that asks the board how many LEDs it has so one file runs on both the Eva Kit and the Dev Kit.'}
level: L2
time_min: {concept: 20, practise: 25, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m01.l06]
objectives:
  - {th: สั่ง LED ด้วย gpio.led(n) ได้ครบทั้ง on() off() toggle() และ value(n) แล้ววนด้วย range(gpio.num_leds()) จนไฟล์เดียวดับไฟได้ครบทุกดวงทั้งบน Eva Kit (3 ดวง) และ Dev Kit (5 ดวง), en: 'Drive LEDs with gpio.led(n) using on(), off(), toggle() and value(n), looping over range(gpio.num_leds()) so one file turns off every LED on both the Eva Kit (3) and the Dev Kit (5).'}
  - {th: 'แยกได้ว่าเมธอดไหนตอบ "สิ่งที่วัดได้" (value() ของ LED และปุ่ม, is_pressed()) และตัวไหนตอบแค่ "สิ่งที่เราสั่งไป" (duty()) แล้วบอกได้ว่าหลัง toggle() หรือ hold() ค่าเหล่านี้ไม่ตรงกับหลอดที่ตาเห็นอย่างไร', en: 'Tell which methods report something measured (value() on an LED or the button, is_pressed()) and which only echo what you commanded (duty()), and state how they disagree with the visible LED after toggle() or hold().'}
  - {th: 'เลือกใช้ brightness(pct) หรือ hold(pct, ms) ให้ถูกกับดวงที่มีและไม่มีเส้น PWM ของฮาร์ดแวร์ และอธิบายได้ว่าทำไมบนบอร์ดนี้หรี่ไฟผ่าน gpio ไม่ใช่ผ่าน machine.PWM', en: 'Choose brightness(pct) or hold(pct, ms) correctly for LEDs with and without a hardware PWM route, and explain why dimming on this board goes through gpio rather than machine.PWM.'}
  - {th: เรียกปุ่มผู้ใช้ด้วยชื่อจาก gpio.button(0).name() ("USER Button 1") แทนป้ายบนแผ่นวงจร และบอกเหตุผลที่ชื่อนี้จงใจไม่ตรงกับป้าย, en: 'Refer to the user button by gpio.button(0).name() ("USER Button 1") instead of the silkscreen label, and give the reason the name deliberately differs from the label.'}
develops: [{skill: mcu.gpio, to: 1}, {skill: mcu.pwm, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-03.html (slides 1–12), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 2.1 — โมดูล gpio: LED ปุ่ม และบอร์ดที่บอกได้ว่ามีอะไร

> โมดูล 2 — จากจอสู่ฮาร์ดแวร์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปิดโมดูล gpio ให้เห็นครบทั้ง 18 ชื่อ สั่ง LED และอ่านปุ่มจริงจาก Python แล้วเขียนโค้ดที่ถามบอร์ดเองว่ามีไฟกี่ดวง ไฟล์เดียวจึงรันได้ทั้ง Eva Kit และ Dev Kit

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. สั่ง LED ด้วย gpio.led(n) ได้ครบทั้ง on() off() toggle() และ value(n) แล้ววนด้วย range(gpio.num_leds()) จนไฟล์เดียวดับไฟได้ครบทุกดวงทั้งบน Eva Kit (3 ดวง) และ Dev Kit (5 ดวง)
2. แยกได้ว่าเมธอดไหนตอบ "สิ่งที่วัดได้" (value() ของ LED และปุ่ม, is_pressed()) และตัวไหนตอบแค่ "สิ่งที่เราสั่งไป" (duty()) แล้วบอกได้ว่าหลัง toggle() หรือ hold() ค่าเหล่านี้ไม่ตรงกับหลอดที่ตาเห็นอย่างไร
3. เลือกใช้ brightness(pct) หรือ hold(pct, ms) ให้ถูกกับดวงที่มีและไม่มีเส้น PWM ของฮาร์ดแวร์ และอธิบายได้ว่าทำไมบนบอร์ดนี้หรี่ไฟผ่าน gpio ไม่ใช่ผ่าน machine.PWM
4. เรียกปุ่มผู้ใช้ด้วยชื่อจาก gpio.button(0).name() ("USER Button 1") แทนป้ายบนแผ่นวงจร และบอกเหตุผลที่ชื่อนี้จงใจไม่ตรงกับป้าย

## ก่อนเริ่ม

ครึ่งแรกของชุดบทเรียน 2.1–2.3 เป็นเรื่องบนโต๊ะล้วน ๆ คือไฟ ปุ่ม และเวลา ยังไม่ต้องต่อ WiFi
เตรียมบันทึกการเรียนไว้จดสามอย่างของบอร์ดทีม: มีไฟกี่ดวง ดวงไหนสีอะไร และโค้ดเรียกปุ่มว่าอะไร
ส่วน Hotspot มือถือของทีม (ชื่อและรหัสชุดเดิมจากบทเรียน 1.4–1.6) กับชื่อทีมที่ผู้สอนแจก จะได้ใช้ตอนส่งขึ้น broker ในบทเรียน 2.3

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 1.6 — ลงมือทำ: พาค่าจริงออกจากบอร์ด และสรุปโมดูล 1](../../m01-ui-application/l06-link-lab/README.md)

## ดูของจริงก่อน

บน Eva Kit เปิดการ์ด **Controls** แล้วแตะวงกลมสีบนจอ หลอด LED จริงบนบอร์ดติดตามนิ้ว
ทีมที่ถือ Dev Kit ไม่มีการ์ดนี้ ให้รัน `11_lights_and_a_button.py` จากบทเรียน 1.3 ซ้ำอีกรอบแล้วมองหลอดแทน
ทั้งสองทางเห็นสิ่งเดียวกัน คือของจริงเปลี่ยนสถานะเพราะคำสั่ง แต่เป็นโปรแกรมที่คนอื่นเขียนไว้ให้
บทเรียนนี้เราเปิดโมดูลที่อยู่เบื้องหลังออกดูทั้งใบ เพื่อเขียนลูปของทีมเองในบทเรียน 2.2–2.3

## แนวคิด

โปรแกรมฝังตัวคือ **ลูปที่อ่านของจริง ตัดสิน แล้วสั่งของจริงกลับไป** เครื่องมือแรกคือโมดูล `gpio`
ที่ไม่ต้อง init ไม่ต้องบอกขา ไม่ต้องตั้งโหมด: `gpio.led(n).on()` `.off()` `.toggle()` `.value(1)`
และ `gpio.button(0).is_pressed()` ใช้ได้ทันที เลข `n` ใช้ได้ตั้งแต่ 0 ถึง `gpio.num_leds() - 1`
(Eva Kit 3 ดวง · Dev Kit 5 ดวง) นอกช่วงได้ `ValueError` และปุ่มมีตัวเดียวคือดัชนี 0 เรียก `gpio.button(1)` ก็ `ValueError` ทั้งสองบอร์ด

ทั้งโมดูลมี 18 ชื่อ ไม่มากกว่านี้: ฟังก์ชันห้าตัว (`board_info` `num_leds` `num_buttons` `led` `button`)
ชนิดสองตัว (`gpio.LED` `gpio.Button`) เมธอดของ LED แปดตัว และของปุ่มสามตัว สิ่งที่ต้องแยกให้ออกคือตัวไหนตอบ
"สิ่งที่วัดได้" ตัวไหนตอบแค่ "สิ่งที่เราสั่งไป" `led.value()` อ่านระดับขาจริง แต่หลัง `hold()` ได้ 0 เสมอ
ส่วน `led.duty()` คือเปอร์เซ็นต์ที่เราสั่งครั้งล่าสุด ไม่ได้ไปวัดหลอด และ `toggle()` ไม่แก้ตัวเลขนี้
ฝั่งปุ่ม `is_pressed()` แปลความหมายให้แล้ว (กด = `True`) ส่วน `value()` เป็นระดับไฟฟ้าดิบที่กดแล้วได้ 0

การหรี่ไฟไม่ได้ลดแรงดันที่ขา แต่สลับติดดับเร็วกว่าที่ตาจับได้ แล้วตาเห็นเป็นค่าเฉลี่ย
`brightness(pct)` ค่ากลาง 1–99 เลือกทางตามขาของหลอด: ดวงที่มีเส้น PWM ของฮาร์ดแวร์ (Eva ดวง 0–2 · Dev Kit ดวง RGB 2–4)
ค้างระดับไว้โดยไม่บล็อก ดวงอื่นได้พัลส์ราว 12 ms แล้วจบด้วยหลอดดับ ถ้าต้องค้างได้ทุกดวงใช้ `hold(pct, ms)`
ซึ่งบล็อกจนครบเวลา (ไม่ใส่ `ms` ได้ ปริยาย 500) แล้วจบด้วยหลอดดับ ระหว่างนั้นปุ่มไม่ถูกอ่าน ถ้าเพิ่งสั่ง `brightness()`
ค่ากลางบนดวง PWM ต้อง `off()` คั่นก่อน `hold()` ส่วน `brightness(100)` ทิ้งหลอดติดค้าง เฟิร์มแวร์ตัวนี้ไม่มี
`machine.PWM` `machine.ADC` `machine.SPI` และไม่ได้เปิด `machine.Timer` ให้ เรียกไปได้ `AttributeError`
คำตอบในเว็บที่ขึ้นต้นด้วย `machine.PWM(...)` จึงไม่ใช่ของบอร์ดเรา

นิสัยของงาน embedded คือ **ถามอุปกรณ์ ไม่ใช่เดาจากความจำ** `gpio.board_info()` คืน dict ห้าช่อง
(`name` `leds` `buttons` `led_names` `btn_names`) และ `for i in range(3)` จะพังเงียบ ๆ บน Dev Kit ที่มีห้าดวง
แต่ `for i in range(gpio.num_leds())` ย้ายบอร์ดแล้วยังถูก

ระวังกับดักชื่อสองแบบที่หลอกคนละเหตุผล บน Eva Kit ดวง 2 ชื่อ `RGB_RED` แต่ติดเป็นสีน้ำเงิน เพราะชื่อตกทอดจากตารางร่วม
ของเฟิร์มแวร์ ส่วนปุ่มชื่อ `USER Button 1` **ถูกเลือกโดยตั้งใจ** ให้ไม่ตรงกับป้ายบนแผ่นวงจร เพราะบน Dev Kit คำว่า "SW2"
ชี้ไปที่สวิตช์ตัดไฟบนฐาน ห้ามโยกสวิตช์ใดบนฐานที่บทเรียนไม่ได้สั่ง ทางของวิศวกรคือสั่ง `on()` ทีละดวงแล้วดูด้วยตา
จดผลไว้ครั้งเดียว แล้วตั้งชื่อค่าคงที่ของทีมเอง

## ตัวอย่างสมบูรณ์

เปิดตามลำดับนี้ แล้วจดผลลงบันทึกการเรียน

1. **`01_board_info.py`** ทายก่อนว่าบอร์ดของทีมจะตอบว่ามีไฟกี่ดวงและปุ่มชื่ออะไร แล้วรันเทียบ
   ดูรายชื่อหลอดตามเลขดัชนีบนจอ และ dict เต็มในคอนโซลฝั่งคอม จากนั้นปลดคอมเมนต์บรรทัด `gpio.button(1)`
   รันดูสักครั้งให้เห็น `ValueError` กับตา
2. **สั่ง `on()` ทีละดวง** แล้วมองบอร์ดจริง ทำตารางสามคอลัมน์: ดัชนี · ชื่อจาก `led_names` · สีที่ตาเห็น
   (Dev Kit: LED1/LED2 อยู่บนโมดูล ดวง RGB คือดวง 2–4)
3. **`03_led_brightness.py`** ท่าที่ 1 สั่ง `brightness(40)` ครั้งเดียว ให้มองหลอดเองว่าค้างหรือวูบ
   ท่าที่ 2 เทียบ `hold(10, …)` กับ `hold(90, …)` และดูเวลาจริงที่ `hold()` ใช้ ท่าที่ 3 สั่ง `on()` แล้ว `toggle()`
   ดูว่า `duty()` ยังตอบเลขเดิมทั้งที่หลอดดับ ลองแก้ `LOW` `HIGH` `HOLD_MS` แล้วรันใหม่

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/01_board_info.py](examples/01_board_info.py) | ถามบอร์ดก่อนว่ามีอะไรให้เล่นบ้าง |
| [examples/03_led_brightness.py](examples/03_led_brightness.py) | หรี่ไฟค้างไว้ให้นานพอที่ตาจะเทียบสองระดับได้ |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m01-ui-application/l03-inside-the-box/examples/11_lights_and_a_button.py](../../m01-ui-application/l03-inside-the-box/examples/11_lights_and_a_button.py) — หลอดไฟกับปุ่มจริง สั่งได้จาก Python บรรทัดเดียว

**ภาพจอจาก BENTO Emulator** ของตัวอย่างในบทนี้ (คลิกชื่อไฟล์เพื่อเปิดโค้ด)

<div class="tok-screens">
<figure><img src="img/screens/01_board_info.webp" alt="จอของ examples/01_board_info.py ขณะรันใน BENTO Emulator: ถามบอร์ดก่อนว่ามีอะไรให้เล่นบ้าง" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_board_info.py"><code>01_board_info.py</code></a> ถามบอร์ดก่อนว่ามีอะไรให้เล่นบ้าง</figcaption></figure>
<figure><img src="img/screens/03_led_brightness.webp" alt="จอของ examples/03_led_brightness.py ขณะรันใน BENTO Emulator: หรี่ไฟค้างไว้ให้นานพอที่ตาจะเทียบสองระดับได้" width="800" height="480" loading="lazy"><figcaption><a href="examples/03_led_brightness.py"><code>03_led_brightness.py</code></a> หรี่ไฟค้างไว้ให้นานพอที่ตาจะเทียบสองระดับได้</figcaption></figure>
</div>

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ทีมหนึ่งเขียน `for i in range(3): gpio.led(i).off()` บน Eva Kit แล้วเอาไฟล์เดิมไปรันบน Dev Kit จะเกิดอะไรขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ดับครบห้าดวง เพราะเฟิร์มแวร์ปรับ range ให้เอง
   - ข) ดับแค่ดวง 0–2 ส่วนดวง 3–4 อยู่สถานะเดิม โดยไม่มี error ให้เห็น
   - ค) โยน ValueError ทันทีที่ i เท่ากับ 3
   - ง) บอร์ดรีเซ็ตตัวเอง เพราะจำนวนดวงไม่ตรงกับโค้ด

   <details><summary>เฉลย</summary>

   **ข** — range(3) พังเงียบ ๆ บนบอร์ดที่มีห้าดวง เลข 0–2 ยังอยู่ในช่วงจึงไม่มี ValueError แต่ดวง 3–4 ไม่ถูกแตะเลย ถ้าเขียน range(gpio.num_leds()) ไฟล์เดียวกันจะวิ่งครบเองทั้งสองบอร์ด

   </details>

2. สั่ง `led.hold(80, 700)` แล้วคำสั่งนั้นทำงานจนจบ ข้อใดถูกต้อง เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 2)*
   - ก) หลอดดับแล้ว
   - ข) `led.value()` ตอบ 0
   - ค) `led.duty()` ยังตอบ 80
   - ง) `led.value()` ตอบ 80 เพราะอ่านความสว่างกลับมา
   - จ) `led.duty()` ตอบ 0 เพราะไปวัดหลอดที่ดับแล้ว

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — hold() จบด้วยขาต่ำเสมอ value() ที่อ่านระดับขาจึงได้ 0 ส่วน duty() คือเลขที่เราสั่งครั้งล่าสุด ไม่ได้ไปวัดหลอด จึงยังตอบ 80 ตัวเลขบนจอจึงไม่ใช่หลักฐานว่าหลอดกำลังสว่าง

   </details>

3. ทีมสั่ง `brightness(40)` บนดวงที่มีเส้น PWM ของฮาร์ดแวร์ แล้วเรียก `hold(80, 700)` ต่อทันที หลอดไม่เปลี่ยนและไม่ดับตอนจบ ควรแก้อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เปลี่ยน 700 เป็น 0.7 เพราะ hold() รับเวลาเป็นวินาที
   - ข) เรียก `off()` คั่นก่อน `hold()` เพื่อคืนขาจากเส้น PWM
   - ค) import machine.PWM ก่อน แล้วค่อยเรียก hold()
   - ง) เปลี่ยนไปใช้ brightness(100) แทน เพราะมันจบด้วยหลอดดับ

   <details><summary>เฉลย</summary>

   **ข** — หลัง brightness() ค่ากลางบนดวง PWM ขายังถูก PWM ถืออยู่ hold() ซึ่งกะพริบขา GPIO เองจึงไม่เห็นผล ต้อง off() คั่นก่อน ส่วน brightness(100) ทิ้งหลอดติดค้าง และบอร์ดนี้ไม่มี machine.PWM

   </details>

4. เพื่อนร่วมทีมที่ถือ Dev Kit ถามว่าให้กดปุ่มไหน คุณควรตอบอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) กดปุ่มที่พิมพ์ว่า SW2 บนฐาน
   - ข) กดปุ่มที่โค้ดเรียกว่า USER Button 1 ตามชื่อที่ btn.name() พิมพ์ขึ้นจอ
   - ค) โยกสวิตช์บนฐานทีละตัวจนกว่าจะเจอตัวที่ตัวเลขขึ้น
   - ง) ใช้ gpio.button(1) เพราะ Dev Kit มีปุ่มมากกว่า

   <details><summary>เฉลย</summary>

   **ข** — ชื่อ USER Button 1 ถูกเลือกโดยตั้งใจให้ไม่ตรงกับป้ายบนแผ่นวงจร เพราะบน Dev Kit สวิตช์ที่พิมพ์ว่า SW หลายตัวเป็นสวิตช์ตัดไฟเลี้ยง ห้ามโยกสวิตช์ที่บทเรียนไม่ได้สั่ง และ gpio.button(1) โยน ValueError ทั้งสองบอร์ด

   </details>

5. ข้อใดถูกต้องเกี่ยวกับการหรี่ไฟบนบอร์ดนี้ เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) brightness(40) บนดวงที่มีเส้น PWM ของฮาร์ดแวร์ ค้างระดับไว้โดยไม่บล็อก
   - ข) brightness(40) บนดวงที่ไม่มีเส้น PWM ได้พัลส์ราว 12 ms แล้วจบด้วยหลอดดับ
   - ค) hold(pct, ms) บล็อกจนครบเวลา ระหว่างนั้นปุ่มไม่ถูกอ่าน
   - ง) อยากหรี่ละเอียดกว่านี้ให้เรียก machine.PWM
   - จ) brightness(100) จบด้วยหลอดดับเหมือนค่ากลาง

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — brightness() เลือกทางตามขาของหลอด ดวงที่มีเส้น PWM ค้างได้ ดวงอื่นได้พัลส์สั้นแล้วดับ hold() ค้างได้ทุกดวงแต่บล็อก ส่วน machine.PWM ไม่มีในพอร์ตนี้ (เรียกแล้วได้ AttributeError) และ brightness(100) ทิ้งหลอดติดค้าง

   </details>

## ไปต่อ

บทเรียน 2.2 เปิดดูสิ่งที่อยู่หลังขา: ทำไมไฟสั่ง 1 แล้วติดแต่ปุ่มกดแล้วได้ 0 ทำไมกดครั้งเดียวนับได้หลายครั้ง
และทำไมลูปที่ดีต้องเลิกใช้ `sleep` เป็นตัวจับเวลา

บทเรียนถัดไป: [บทเรียน 2.2 — หลังไฟและปุ่ม: active-low กันเด้ง และลูปที่ไม่หยุด](../l02-active-low-debounce/README.md)

## สะท้อนคิด

- ถ้าต้องเขียนโค้ดชุดเดียวให้รันบนบอร์ดสามรุ่นที่มีไฟไม่เท่ากัน คุณจะถามบอร์ดเรื่องอะไรบ้างก่อนเริ่มสั่ง
- `duty()` ตอบสิ่งที่สั่ง `value()` ตอบระดับขา ถ้าต้องรายงานสถานะไฟขึ้นจอ คุณจะเชื่อตัวไหน หรือไม่เชื่อทั้งคู่ เพราะอะไร
