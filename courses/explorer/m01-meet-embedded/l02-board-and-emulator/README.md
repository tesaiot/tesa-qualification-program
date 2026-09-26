---
id: explore.m01.l02
lang: th
title:
  th: รู้จักบอร์ดและอีมูเลเตอร์
  en: Meet the board and the emulator
summary:
  th: รู้จักบอร์ด Eva Kit กับ TESAIoT Dev Kit แล้วเปิด BENTO IDE รันโปรแกรมแรกใน BENTO Emulator โดยไม่ต้องมีบอร์ด
  en: Meet the Eva Kit and the TESAIoT Dev Kit, then open BENTO IDE and run a first program in the BENTO Emulator with no board.
level: L1
time_min: {concept: 8, practise: 12, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [explore.m01.l01]
objectives:
  - th: เปิด BENTO IDE แล้วรันไฟล์ตัวอย่างใน BENTO Emulator จนเห็นชื่อบอร์ดขึ้นบนจอจำลองได้
    en: Open BENTO IDE and run the example file in the BENTO Emulator until the board name appears on the simulated screen.
  - th: บอกความต่างระหว่าง Eva Kit กับ TESAIoT Dev Kit ได้อย่างน้อย 2 ข้อ
    en: State at least two differences between the Eva Kit and the TESAIoT Dev Kit.
  - th: อธิบายได้อย่างน้อย 1 เรื่องที่อีมูเลเตอร์ตอบได้ และ 1 เรื่องที่ต้องพิสูจน์บนบอร์ดจริง
    en: Explain at least one thing the emulator can answer and one thing that must be proven on a real board.
develops:
  - {skill: sys.simulation, to: 1}
  - {skill: hw.architecture, to: 1}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, emulator: bento-emulator}
status: alpha
translation: pending
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s01/10_board_knows_itself.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## เป้าหมาย

1. เปิด BENTO IDE แล้วรันไฟล์ตัวอย่างใน BENTO Emulator จนเห็นชื่อบอร์ดขึ้นบนจอจำลอง
2. บอกความต่างระหว่าง Eva Kit กับ TESAIoT Dev Kit ได้อย่างน้อย 2 ข้อ
3. อธิบายได้ว่าอะไรที่อีมูเลเตอร์ตอบได้ และอะไรที่ต้องพิสูจน์บนบอร์ดจริง

## ก่อนเริ่ม

- จากบทที่แล้ว ส่วนไหนของหม้อหุงข้าวดิจิทัลที่ "ตัดสินใจ"
- ถ้าไม่มีบอร์ดในมือ คุณคิดว่าจะเรียนเขียนโปรแกรมให้บอร์ดได้แค่ไหน

สิ่งที่ต้องมีในบทนี้มีแค่คอมพิวเตอร์ที่เปิดเบราว์เซอร์ Chrome หรือ Edge ได้ (บทเรียนนี้ออกแบบสำหรับจอคอมพิวเตอร์หรือแท็บเล็ต ไม่ใช่มือถือ)

## ดูของจริงก่อน

ทำตามนี้ก่อน แล้วค่อยมาอ่านคำอธิบาย

1. เปิด **BENTO IDE** ที่ https://ide.tesaiot.dev/
2. IDE เปิดมาที่มุมมอง **Blocks** (ต่อบล็อกแทนการพิมพ์) ให้กดปุ่ม **Python** ที่หัวจอ เพื่อสลับเป็นมุมมองโค้ด
3. คัดลอกโค้ดทั้งไฟล์จาก [examples/01_board_knows_itself.py](examples/01_board_knows_itself.py) ไปวางในช่องแก้โค้ด
4. กดปุ่ม **BENTO Emulator** บนแถบเครื่องมือ แผงอีมูเลเตอร์จะเลื่อนออกมาทางขวา แล้วกด **▶ Run** ในแผงนั้น
5. มองที่จอจำลอง คุณควรเห็นชื่อบอร์ดตัวสีฟ้า และบรรทัดบอกว่ามีไฟกี่ดวง ปุ่มกี่ปุ่ม

ถ้าเห็นแล้ว ยินดีด้วย คุณเพิ่งรันโปรแกรมบนไมโครคอนโทรลเลอร์ (จำลอง) เป็นครั้งแรก

**ถ้ามีบอร์ดอยู่ในมือ** ต่อบอร์ดเข้ากับคอมพิวเตอร์ด้วยสาย USB กด **Connect** ที่มุมขวาบนของ IDE เลือกพอร์ตของบอร์ด
แล้วบนจอบอร์ดให้แตะการ์ด **BENTO Playground** เปิดค้างไว้ จากนั้นกด **Program to Device** ผลจะขึ้นบนจอบอร์ดจริง
รายชื่อไฟทีละดวงอยู่ในลิ้นชัก Console ซึ่งเปิดได้ด้วยปุ่มสีเขียวมุมขวาล่างของหน้า Playground

## แนวคิด

### 1. บอร์ดสองรุ่นที่ใช้โค้ดชุดเดียวกัน

หลักสูตรใน TESA Open Knowledge ใช้บอร์ดที่มีชิป **PSoC™ Edge E84** ของ Infineon อยู่สองรุ่น

| | Eva Kit | TESAIoT Dev Kit |
|---|---|---|
| ชื่อทางเทคนิค | KIT_PSE84_EVAL_EPC2 | SoM KIT_PSE84_AI บนบอร์ดฐาน QWA309 |
| หลอด LED ที่ Python สั่งได้ | 3 ดวง | 5 ดวง |
| เซนเซอร์เพิ่มเติม | | วัดอุณหภูมิและความชื้น (SHT40) ความกดอากาศ (DPS368) และเรดาร์ |
| จอ | จอสัมผัส 800 x 480 จุด | จอสัมผัส 800 x 480 จุด |

ข้อมูลในตารางนี้มาจากหลักสูตร AIoT in Action ซึ่งใช้บอร์ดทั้งสองรุ่น

ตัวอย่างในบทนี้ไม่ได้จำว่าบอร์ดมีไฟกี่ดวง มันถาม `gpio.board_info()` ซึ่งคืนข้อมูลก้อนหนึ่ง (dict) ที่มีชื่อบอร์ด จำนวนไฟ และรายชื่อไฟ
เพราะแบบนี้ โค้ดชุดเดียวจึงรันได้บนทั้งสองบอร์ด และในอีมูเลเตอร์ด้วย

ชิป PSoC Edge E84 มีหน่วยประมวลผลมากกว่าหนึ่งคอร์ เฟิร์มแวร์ BENTO แบ่งงานให้คอร์ช่วยกัน เช่น คอร์หนึ่งรันโปรแกรม MicroPython ของเรา
อีกคอร์ดูแลจอและหน้าจอสัมผัส ตอนนี้แค่รู้ไว้ก่อน ว่าทำไมบางคำสั่งต้องรอให้ "อีกฝั่ง" ทำงานเสร็จ

### 2. MicroPython

โปรแกรมที่เราเขียนเป็นภาษา **MicroPython** คือภาษา Python ฉบับที่ทำให้เล็กพอจะรันบนไมโครคอนโทรลเลอร์ได้
ไม่ต้องคอมไพล์ กดรันแล้วเห็นผลเลย เหมาะกับการเริ่มต้น ส่วนงานระดับมืออาชีพที่ต้องรีดความเร็วหรือพลังงาน จะใช้ภาษา C ซึ่งมีหลักสูตรแยกต่างหาก

บอร์ดเหล่านี้มีโมดูลของ BENTO เองที่ใช้บ่อยในหลักสูตรนี้ ได้แก่ `ui` (วาดบนจอ) `lcd` (ลิ้นชัก Console) `gpio` (ไฟและปุ่ม)
`sensors` (เซนเซอร์) `wifi` และ `mqtt` (เครือข่าย)

### 3. อีมูเลเตอร์ตอบอะไรได้ และอะไรที่ตอบไม่ได้

**BENTO Emulator** รันโปรแกรม MicroPython ของเราในเบราว์เซอร์ และวาดจอขนาดเท่าจอบอร์ด ปุ่ม **HW** ในแผงอีมูเลเตอร์เปิดแผงฮาร์ดแวร์จำลอง
ที่มีหลอดไฟ ปุ่ม ลูกบิด และแผ่นเอียง ให้เราลองโปรแกรมได้โดยไม่ต้องมีบอร์ด

อีมูเลเตอร์ตอบคำถาม "โปรแกรมรันจบไหม มีข้อผิดพลาดไหม และหน้าจอออกมาหน้าตาแบบไหน" ได้ดีมาก
แต่มันไม่ใช่บอร์ดจริง ค่าเซนเซอร์เป็นค่าจำลอง WiFi เป็นของจำลอง และเรื่องจังหวะเวลาหรือข้อจำกัดของฮาร์ดแวร์บางอย่างไม่มีทางโผล่ในเบราว์เซอร์
หลักคิดที่เราใช้ตลอดหลักสูตรคือ **ใช้อีมูเลเตอร์เรียนแนวคิด ใช้บอร์ดจริงพิสูจน์และวัดผล**

## ตัวอย่างสมบูรณ์

[examples/01_board_knows_itself.py](examples/01_board_knows_itself.py) ย่อมาจากตัวอย่าง
[`examples/s01/10_board_knows_itself.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/10_board_knows_itself.py)
ของหลักสูตร AIoT in Action อ่านไล่ตามนี้

- **ท่าที่ 1 ถามบอร์ด** `info = gpio.board_info()` ถามครั้งเดียว เก็บไว้ในตัวแปร
- **ท่าที่ 2 ล้างจอ** `ui.screen()` ลบของเก่าบนจอ แล้วรอ 200 มิลลิวินาทีให้จอพร้อม
- **ท่าที่ 3 วางป้าย** `ui.Label(ข้อความ, x=..., y=..., color=..., value=ขนาดตัวอักษร)` แล้วเคาะ `ui.poll()` ให้ป้ายขึ้นทันที
- **ท่าที่ 4 เขียนลงลิ้นชัก** `lcd.print(...)` สำหรับรายละเอียดที่ยาวเกินจอ

## ฝึกเติม

ท้ายไฟล์ตัวอย่างมีโจทย์ "ตาคุณ" อยู่ ให้เพิ่มลูปพิมพ์รายชื่อปุ่มจาก `info["btn_names"]` แบบเดียวกับลูปพิมพ์รายชื่อไฟ
ก่อนรัน ลองทำนายว่าอีมูเลเตอร์จะรายงานปุ่มกี่ปุ่ม แล้วรันเทียบ

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

## ไปต่อ

- ลองกด **HW** แล้วดูว่าแผงฮาร์ดแวร์จำลองมีอะไรบ้าง บทต่อไปเราจะสั่งหลอดไฟบนแผงนั้น
- ถ้าอยากรู้ว่าบอร์ดจริงตอบต่างจากอีมูเลเตอร์อย่างไร เปิดไฟล์ต้นฉบับ
  [`examples/s01/10_board_knows_itself.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/10_board_knows_itself.py)
  ที่ถามบอร์ดต่อว่าโมดูล `machine` มีคำสั่งไหนบ้าง

## สะท้อนคิด

ถ้าคุณต้องตัดสินใจว่าจะซื้อบอร์ดดีไหม ข้อมูลอะไรจากบทนี้ที่ช่วยคุณตัดสินใจ และอะไรที่ยังต้องหาเพิ่ม
