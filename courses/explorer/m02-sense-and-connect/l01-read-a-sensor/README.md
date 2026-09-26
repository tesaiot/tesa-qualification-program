---
id: explore.m02.l01
lang: th
title:
  th: อ่านเซนเซอร์แล้วดูค่าเปลี่ยน
  en: Read a sensor and watch the value change
summary:
  th: ขอค่าลูกบิดและค่าความเร่งจาก sensors.snapshot() แสดงบนจอ แล้วเขียนไฟเตือนเมื่อบอร์ดเอียง
  en: Read the knob and acceleration from sensors.snapshot(), show them on screen, and build a tilt warning light.
level: L1
time_min: {concept: 8, practise: 15, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [explore.m01.l03]
objectives:
  - th: อ่านค่าลูกบิด (pot) และค่าความเร่งแกน z (az) จาก sensors.snapshot() แล้วแสดงบนจอให้เปลี่ยนตามการหมุนหรือการเอียงได้
    en: Read the knob (pot) and z-axis acceleration (az) from sensors.snapshot() and show them on screen as they change.
  - th: อธิบายได้ว่าทำไมต้องตรวจคีย์ด้วย in และดัก OSError ก่อนใช้ค่าจากเซนเซอร์
    en: Explain why the code checks keys with in and catches OSError before using a sensor value.
  - th: เติมโปรแกรมไฟเตือนให้หลอดติดเมื่อ az ต่ำกว่าเกณฑ์ และดับเมื่อบอร์ดวางราบ
    en: Complete a warning-light program that lights the LED when az falls below a threshold and turns it off when the board lies flat.
develops:
  - {skill: sys.sensors-actuators, to: 1}
  - {skill: mcu.adc-dac, to: 1}
  - {skill: lang.micropython, to: 1}
assesses:
  - {skill: sys.sensors-actuators, level: 1, evidence: practice/tilt_alarm.py}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, emulator: bento-emulator}
status: alpha
translation: pending
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s01/12_every_sense_at_once.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## เป้าหมาย

1. อ่านค่า `pot` กับ `az` จาก `sensors.snapshot()` แล้วแสดงบนจอให้เปลี่ยนตามมือ
2. อธิบายได้ว่าทำไมต้องถามคีย์ด้วย `in` และดัก `OSError`
3. เติมโปรแกรมไฟเตือนเมื่อบอร์ดเอียงให้ทำงานถูก

## ก่อนเริ่ม

- ในบทที่แล้ว ทำไมเราต้องแปลงตัวเลขด้วย `str()` ก่อนส่งให้ `Seg7`
- จากบทแรก เซนเซอร์อยู่ในจังหวะไหนของ "รับรู้ ตัดสินใจ สั่งงาน"

## ดูของจริงก่อน

1. เปิด [examples/01_knob_and_tilt.py](examples/01_knob_and_tilt.py) ใน BENTO IDE แล้วรันใน BENTO Emulator
2. กด **HW** เปิดแผงฮาร์ดแวร์จำลอง แล้ว **หมุนลูกบิด POTEN** ดูวงแหวนบนจอกวาดตาม
3. ลาก **แผ่นเอียง** บนแผงเดียวกัน ดูตัวเลข `az` เปลี่ยน และสีเปลี่ยนเป็นส้มเมื่อเอียงมาก

ถ้าใช้บอร์ดจริง หมุนลูกบิดบนบอร์ด และเอียงบอร์ดด้วยมือ ผลจะเหมือนกัน

## แนวคิด

### 1. ถามครั้งเดียว ได้ทุกเซนเซอร์

`sensors.snapshot()` คืนข้อมูลก้อนเดียว (dict) ที่มีค่าเซนเซอร์หลายตัวซึ่งอ่านมาจากเวลาเดียวกัน หน้าตาประมาณนี้

```python
{
    "pot":     {"percent": 42.5, ...},             # ลูกบิดหมุน 0-100
    "bmi270":  {"ax": 0.1, "ay": -0.2, "az": 9.8, ...},   # ความเร่ง หน่วย m/s^2
    "capsense": {"btn0": False, "btn1": False, "slider": 0, ...},  # แผ่นสัมผัส
}
```

ค่าจริงมีช่องอื่นอยู่อีก เช่นตัวนับรอบ `sequence` ในแต่ละก้อนย่อย
ลูกบิดหมุนคือตัวต้านทานปรับค่าได้ บอร์ดอ่านแรงดันจากมันด้วย **ADC (analog-to-digital converter)** แล้วแปลงให้เป็นเปอร์เซ็นต์
ส่วน `bmi270` คือชิปวัดความเคลื่อนไหว ตอนวางราบ แรงโน้มถ่วงทำให้ `az` อยู่ราว 9.8 พอเอียง ค่านี้ลดลง

### 2. ถามก่อนหยิบ

คีย์ในก้อนมีเท่าที่บอร์ดมีให้ ไม่ได้มีครบเสมอ ถ้าเขียน `s["pot"]` ตรง ๆ บนบอร์ดที่ไม่มีลูกบิด โปรแกรมจะหยุดด้วย `KeyError`
วิธีที่ปลอดภัยคือถามก่อนด้วย `if "pot" in s:` แล้วค่อยอ่าน

### 3. บอร์ดจริงอาจยังไม่พร้อม

หลังเปิดเครื่องใหม่ ๆ บอร์ดจริงอาจยังไม่พร้อมตอบเรื่องเซนเซอร์อยู่ครู่หนึ่ง ช่วงนั้น `snapshot()` จะโยน `OSError` ออกมา
ไม่ได้แปลว่าโค้ดผิด เราจึงครอบด้วย `try` / `except OSError` แล้วลองใหม่รอบหน้า

ในอีมูเลเตอร์ บรรทัดนี้แทบไม่เคยโยน `OSError` เลย นี่คือตัวอย่างที่ดีของหลักคิดในบทก่อน
**โปรแกรมที่ผ่านในอีมูเลเตอร์ยังต้องเขียนเผื่อบอร์ดจริงเสมอ**

## ตัวอย่างสมบูรณ์

[examples/01_knob_and_tilt.py](examples/01_knob_and_tilt.py) ย่อมาจาก
[`examples/s01/12_every_sense_at_once.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/12_every_sense_at_once.py)
ของหลักสูตร AIoT in Action

- **ท่าที่ 1 วางของบนจอครั้งเดียวนอกลูป** วงแหวน `ui.Arc` ป้ายค่า pot ป้ายค่า az และป้ายสถานะ
- **ท่าที่ 2 วนถามทุก 200 ms** จนครบ 20 วินาที โดยใช้ `time.ticks_ms()` กับ `time.ticks_diff()` จับเวลา
- **ท่าที่ 3 ขอค่าอย่างปลอดภัย** `try: s = sensors.snapshot()` ถ้า `OSError` ก็รอแล้วลองใหม่
- **ท่าที่ 4 ถามก่อนหยิบ** `if "pot" in s:` แล้วแปลงเปอร์เซ็นต์เป็นจำนวนเต็มด้วย `int()` ก่อนส่งให้วงแหวน
- **ท่าที่ 5 เปลี่ยนสีตามความหมาย** เขียวเมื่อวางราบ ส้มเมื่อเอียง

## ฝึกเติม

เปิด [practice/tilt_alarm.py](practice/tilt_alarm.py) บทนี้มีช่องให้เติม 4 จุด มากกว่าบทที่แล้ว เพราะคุณเคยเห็นทุกคำสั่งที่ต้องใช้มาแล้ว

- เติม 1 ขอค่าเซนเซอร์ทั้งก้อน
- เติม 2 เงื่อนไขว่ามีคีย์ `bmi270` อยู่ในก้อน
- เติม 3 ไฟติดพร้อมป้าย "เอียง"
- เติม 4 ไฟดับพร้อมป้าย "วางราบ"

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/tilt_alarm.py](solution/tilt_alarm.py) เทียบ

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

## แล็บ

**สร้างเอง** แก้ไฟเตือนให้ใช้ลูกบิดตั้งเกณฑ์แทนตัวเลขตายตัว เช่น หมุนลูกบิดไปที่ 50% แปลว่าเกณฑ์เป็นกลาง ๆ
ถ่ายภาพหน้าจอตอนไฟเตือนติด เก็บไว้ใน portfolio พร้อมเขียนหนึ่งบรรทัดว่าเกณฑ์ที่คุณเลือกมาจากไหน

## ไปต่อ

ค่าจากเซนเซอร์จริงไม่เคยนิ่งสนิท มีสัญญาณรบกวนปนมาเสมอ หลักสูตร AIoT in Action มีตัวอย่างที่ทำให้ค่านิ่งขึ้นด้วยฟิลเตอร์
เช่น [`examples/s05/06_ema_time_constant.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/06_ema_time_constant.py)
และวิธีแปลงค่าที่ ADC อ่านได้ให้เป็นโวลต์ใน [`examples/s05/05_adc_counts_to_volts.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)

## สะท้อนคิด

ถ้าจะใช้ไฟเตือนนี้กับชั้นวางของในโกดังจริง คุณจะตั้งเกณฑ์อย่างไร และจะทำอย่างไรไม่ให้ไฟกะพริบรัว ๆ ตอนที่ค่าแกว่งอยู่รอบเกณฑ์พอดี
