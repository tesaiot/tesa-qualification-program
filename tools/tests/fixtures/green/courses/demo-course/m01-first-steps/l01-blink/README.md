---
id: demo.m01.l01
lang: th
title: {th: ไฟกะพริบ, en: Blinking LED}
summary: {th: สั่ง LED ให้กะพริบด้วย GPIO, en: Blink an LED with GPIO}
level: L1
time_min: {concept: 10, practise: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit]}
prerequisites: []
objectives:
  - {th: อธิบายว่าขา GPIO เป็นขาออกได้อย่างไร, en: Explain how a GPIO pin drives an output}
  - {th: เขียนลูปกะพริบ LED ที่คาบเวลา 1 วินาที, en: Write a loop that blinks an LED with a 1 s period}
develops: [{skill: mcu.gpio, to: 1}, {skill: lang.micropython, to: 1}]
assesses: [{skill: mcu.gpio, level: 1, evidence: practice/blink.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: https://github.com/example/source, path: slides/session-01.md, ref: abc1234}
---

## เป้าหมาย

ทำให้ LED กะพริบ ![LED บนบอร์ด](img/led.png)

## ตัวอย่างสมบูรณ์

[examples/01_blink.py](examples/01_blink.py) ใช้ `machine.Pin` ตั้งขาเป็นขาออก

![ภาพ LED จาก Wikimedia Commons](img/led_commons.png)

## ฝึกเติม

[practice/blink.py](practice/blink.py)

## เฉลย

[solution/blink.py](solution/blink.py)

## ไปต่อ

[บทเรียนถัดไป](../l02-pwm-period/README.md)
