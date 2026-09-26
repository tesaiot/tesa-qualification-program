---
id: demo.m01.l02
lang: th
title: {th: คาบเวลาของ PWM, en: The PWM period}
summary: {th: อ่านคาบเวลาและความถี่ของสัญญาณ PWM, en: Read the period and frequency of a PWM signal}
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [demo.m01.l01]
objectives:
  - {th: คำนวณคาบเวลาจากความถี่, en: Compute the period from the frequency}
  - {th: ตั้งค่า duty cycle ให้ได้ความสว่างที่ต้องการ, en: Set a duty cycle for a target brightness}
develops: [{skill: mcu.pwm, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython}
status: alpha
translation: pending
---

## แนวคิด

สัญญาณ PWM ความถี่ 1 kHz มีคาบเวลา 1 ms และคาบของสัญญาณคือเวลาที่ใช้ครบหนึ่งรอบ
คาบ (period) T = 1/f ดังนั้นสัญญาณ 50 Hz มีคาบ 20 ms
ทุกคาบเวลา ตัวจับเวลาจะนับใหม่ จำนวน tick ต่อคาบเวลาจึงคงที่ และช่วงที่คาบเกี่ยวกันไม่มี

ใน MQTT ค่า `clean_session` เป็นชื่อพารามิเตอร์ในโค้ด ส่วน TLS session resumption เป็นชื่อกลไก

```python
client = MQTTClient("id", "broker", clean_session=True)  # session 3 ในโค้ดไม่ถูกตรวจ
```

ต้นฉบับอยู่ที่ [หน้าเว็บเดิม](https://example.org/session-03.html)
