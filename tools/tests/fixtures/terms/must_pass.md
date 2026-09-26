---
id: demo.m01.l02
title: {th: คาบเวลาของ PWM, en: The PWM period}
source: {repo: https://example.org/course, path: slides/session-03.md, ref: abc1234}
slides: slides-session-03.md
---

# คาบเวลาของสัญญาณ

สัญญาณ PWM ความถี่ 1 kHz มีคาบเวลา 1 ms
คาบของสัญญาณคือเวลาที่ใช้ครบหนึ่งรอบ
คาบ (period) T = 1/f
สัญญาณ 50 Hz มีคาบ 20 ms และสัญญาณ 2 Hz มีคาบ 0.5 s
ทุกคาบเวลา ตัวจับเวลาจะนับใหม่
จำนวน tick ต่อคาบเวลาคงที่
ช่วงที่คาบเกี่ยวกันของสองงาน
ในคาบนี้ของสัญญาณ ค่าเฉลี่ยคือ duty cycle
ทุกคาบ (period) ของ PWM มีช่วงสูงหนึ่งช่วง
หนึ่งคาบของคลื่นใช้เวลา 1 วินาที

ใน MQTT ค่า `clean_session` และ `session 3` ในโค้ดไม่ใช่ถ้อยคำสอน
MQTT clean_session 1 คือชื่อพารามิเตอร์ ส่วน TLS session resumption คือกลไก

```python
client = MQTTClient("id", "broker", clean_session=True)  # session 3
# คาบเรียน 3 ในคอมเมนต์ของโค้ด
```

~~~text
Session 4
~~~

<pre>คาบ 3</pre> และ <code>session-05</code>

ต้นฉบับ [หน้าเดิม](https://example.org/session-03.html) หรือ https://example.org/session-04.html
<img src="img/session-06.png" alt="แผนผังการต่อวงจร">

[ref]: https://example.org/session-07.html
