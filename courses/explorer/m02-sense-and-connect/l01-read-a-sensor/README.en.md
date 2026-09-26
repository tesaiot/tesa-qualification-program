---
id: explore.m02.l01
lang: en
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
translation: done
source_sha256: 3c8f2649f8fca61ea0f1172733e92c012ba3f82e9b094ff0c17ebac429c755ba
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s01/12_every_sense_at_once.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## Objectives

1. Read `pot` and `az` from `sensors.snapshot()` and show them on screen so they change as you touch things
2. Explain why the code checks keys with `in` and catches `OSError`
3. Complete a warning-light program that works correctly when the board is tilted

## Before you start

- In the previous lesson, why did we have to convert the number with `str()` before passing it to `Seg7`?
- From the first lesson, which step of "sense, decide, act" is a sensor in?

## See it work first

1. Open [examples/01_knob_and_tilt.py](examples/01_knob_and_tilt.py) in BENTO IDE and run it in the BENTO Emulator
2. Press **HW** to open the simulated hardware panel, then **turn the POTEN knob** and watch the ring on screen sweep along with it
3. Drag the **tilt pad** on the same panel and watch the `az` number change, and the colour turn orange when tilted a lot

If you use a real board, turn the knob on the board and tilt the board by hand; the result is the same.

## Concepts

### 1. Ask once, get every sensor

`sensors.snapshot()` returns a single bundle of data (a dict) with several sensor values all read at the same moment. It looks roughly like this.

```python
{
    "pot":     {"percent": 42.5, ...},             # knob rotation 0-100
    "bmi270":  {"ax": 0.1, "ay": -0.2, "az": 9.8, ...},   # acceleration, in m/s^2
    "capsense": {"btn0": False, "btn1": False, "slider": 0, ...},  # touch pad
}
```

The real value has other fields too, such as a round counter, `sequence`, inside each sub-bundle.
The knob is a variable resistor; the board reads a voltage from it with an **ADC (analog-to-digital converter)** and converts it to a percentage.
`bmi270` is a motion-sensing chip; when lying flat, gravity keeps `az` around 9.8, and this value drops as it is tilted.

### 2. Ask before you take

The keys in the bundle are only the ones the board actually has; they are not always all present. Writing `s["pot"]` directly on a board with no knob would stop the program with a `KeyError`.
The safe way is to ask first with `if "pot" in s:`, and only then read the value.

### 3. A real board may not be ready yet

Right after power-on, a real board may not be ready to answer about sensors for a moment. During that time, `snapshot()` throws an `OSError`.
It does not mean the code is wrong, so we wrap it with `try` / `except OSError` and try again next time round.

In the emulator, this line almost never throws an `OSError`. This is a good example of the principle from the previous lesson:
**a program that passes in the emulator must still be written to allow for a real board**.

## Worked example

[examples/01_knob_and_tilt.py](examples/01_knob_and_tilt.py) is a shortened version of
[`examples/s01/12_every_sense_at_once.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s01/12_every_sense_at_once.py)
from the AIoT in Action course.

- **Move 1: place things on screen once, outside the loop** The `ui.Arc` ring, a label for the pot value, a label for the az value, and a status label
- **Move 2: loop and ask every 200 ms** for a total of 20 seconds, using `time.ticks_ms()` and `time.ticks_diff()` to time it
- **Move 3: ask for the value safely** `try: s = sensors.snapshot()`; on `OSError`, wait and try again
- **Move 4: ask before you take** `if "pot" in s:`, then convert the percentage to an integer with `int()` before passing it to the ring
- **Move 5: change colour by meaning** Green when lying flat, orange when tilted

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/01_knob_and_tilt.webp" alt="examples/01_knob_and_tilt.py running in the BENTO Emulator" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_knob_and_tilt.py"><code>01_knob_and_tilt.py</code></a></figcaption></figure>
</div>

## Practice

Open [practice/tilt_alarm.py](practice/tilt_alarm.py). This lesson has 4 blanks to fill in, more than the previous lesson, because you have already seen every command you need.

- Blank 1: ask for the whole sensor bundle
- Blank 2: the condition that the key `bmi270` is in the bundle
- Blank 3: turn the light on together with the label "tilted"
- Blank 4: turn the light off together with the label "lying flat"

## Solution

Try it yourself for at least 15 minutes first, then open [solution/tilt_alarm.py](solution/tilt_alarm.py) and compare.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Lab

**Make** Change the warning light so it uses the knob to set the threshold instead of a fixed number, for example turning the knob to 50% means a middle-of-the-road threshold.
Take a screenshot with the warning light on, keep it in your portfolio, and write one line about where the threshold you chose came from.

## Going further

Real sensor values are never perfectly still; there is always some noise mixed in. The AIoT in Action course has an example that smooths the value out with a filter,
such as [`examples/s05/06_ema_time_constant.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/06_ema_time_constant.py),
and how to convert the raw ADC reading to volts in [`examples/s05/05_adc_counts_to_volts.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py).

## Reflect

If you were to use this warning light on a real warehouse shelf, how would you set the threshold, and how would you stop the light from flickering rapidly when the value hovers right around the threshold?
