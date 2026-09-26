---
id: demo.m01.l01
lang: en
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
source_sha256: dce2bc0fb0e824674ce5e493b3f49589ce0895220e25346c55f31fc7dd88e964
---

## Goal

Make the LED blink. ![The LED on the board](img/led.png)

Full example: [examples/01_blink.py](examples/01_blink.py).
