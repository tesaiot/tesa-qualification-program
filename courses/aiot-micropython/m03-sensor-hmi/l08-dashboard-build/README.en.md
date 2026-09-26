---
id: aiot-mpy.m03.l08
lang: en
title: {th: 'ประกอบแดชบอร์ด: สี่การ์ดในลูปเดียว', en: 'Building the dashboard: four cards in one loop'}
summary: {th: แกะโค้ดจริงของแดชบอร์ดสี่การ์ดทีละท่า ตั้งแต่การเตรียมจอโดยไม่มี sensors.init() การเลือก widget ตามว่าใครเป็นคนเปลี่ยนค่า ไปจนถึงลูปเดียวที่อ่านเซนเซอร์สี่ตัวแบบ sync ทุก 200 ms พร้อมรู้จัก sensors.bmm350 ห้าชื่อและโมดูล mic แปดชื่อสำหรับการ์ดใบที่ห้า, en: 'Read the real four-card dashboard code move by move, from preparing the screen without sensors.init() and choosing widgets by who changes the value, to one loop that reads four sensors synchronously every 200 ms, and meet the five sensors.bmm350 names and eight mic names for a fifth card.'}
level: L2
time_min: {concept: 30, practise: 25, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m03.l07]
objectives:
  - {th: อธิบายลำดับสามบรรทัดตอนเริ่มโปรแกรม (ui.screen() แล้ว sleep_ms(200) แล้วอ่าน motion() ทิ้งหนึ่งครั้งใน try) และบอกได้ว่าทำไมไฟล์ไม่มี sensors.init() และทำไมการเงียบสิบกว่าวินาทีตอนอ่านครั้งแรกบน Eva Kit คือการรอ ไม่ใช่การค้าง, en: 'Explain the three start-up steps (ui.screen(), then sleep_ms(200), then one throw-away motion() read inside try), why the file has no sensors.init(), and why a silence of more than ten seconds on the first read on the Eva Kit is waiting, not a hang.'}
  - {th: 'ให้เหตุผลการเลือก widget ในการ์ดทั้งสี่ได้อย่างน้อยสามข้อ เช่น คูณ 10 ก่อนป้อน Chart, ใช้ Bar ไม่ใช่ Slider กับ CapSense, ใช้ไฟสองดวงแทนป้ายเปลี่ยนสี และใช้ Arc คู่กับ Seg7 และคำนวณชื่อทิศจาก DIRS ด้วยสูตร +22.5 หาร 45 ได้ถูกต้อง', en: 'Justify at least three widget choices in the four cards, such as scaling by 10 before feeding the Chart, using a Bar rather than a Slider for CapSense, two lamps instead of a colour-changing label, and pairing an Arc with a Seg7, and compute the direction name from DIRS with the +22.5, divide-by-45 formula.'}
  - {th: อธิบายโครงลูปหลักได้ครบห้าจังหวะ (จับเวลา t0 อ่านสี่เซนเซอร์แบบ sync อัปเดต widget เรียก ui.poll() และ sleep_ms(200)) และบอกได้ว่าทำไม except จึงคงค่าเดิมไว้แทนการเขียนศูนย์ทับ, en: 'Explain all five beats of the main loop (take t0, read four sensors synchronously, update widgets, call ui.poll(), sleep_ms(200)) and why the except branch keeps the last value instead of writing zero.'}
  - {th: เลือกคำสั่งของ mic และ sensors.bmm350 ให้ถูกงานได้ เช่น ใช้ mic.stats() ครั้งเดียวเมื่อต้องการทั้ง rms และ peak และรายงานค่า magnetic() เป็นค่าเบี่ยงจากเส้นฐานในหน่วยบอร์ด ไม่ใช่ uT, en: 'Choose the right mic and sensors.bmm350 calls for the job, such as one mic.stats() call when you need both rms and peak, and report magnetic() values as a deviation from a baseline in board units, not uT.'}
develops: [{skill: gui.hmi, to: 2}, {skill: gui.embedded, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: lang.micropython, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-08.html (slides 18–31), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 9be957cf4353dc5dcef28bbb92f69bf6d62a336e4c5d0c97b902d64cd92ff324
---

# Lesson 3.8 — Building the dashboard: four cards in one loop

> Module 3 — Sensor Visualization on HMI · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Read the real four-card dashboard code move by move, from preparing the screen without sensors.init() and choosing widgets by who changes the value, to one loop that reads four sensors synchronously every 200 ms, and meet the five sensors.bmm350 names and eight mic names for a fifth card.

## Objectives

By the end of this lesson you will be able to:

1. Explain the three start-up steps (ui.screen(), then sleep_ms(200), then one throw-away motion() read inside try), why the file has no sensors.init(), and why a silence of more than ten seconds on the first read on the Eva Kit is waiting, not a hang
2. Justify at least three widget choices in the four cards, such as scaling by 10 before feeding the Chart, using a Bar rather than a Slider for CapSense, two lamps instead of a colour-changing label, and pairing an Arc with a Seg7, and compute the direction name from DIRS with the +22.5, divide-by-45 formula
3. Explain all five beats of the main loop (take t0, read four sensors synchronously, update widgets, call ui.poll(), sleep_ms(200)) and why the except branch keeps the last value instead of writing zero
4. Choose the right mic and sensors.bmm350 calls for the job, such as one mic.stats() call when you need both rms and peak, and report magnetic() values as a deviation from a baseline in board units, not uT

## Before you start

Bring your paper layout and widget budget table from lesson 3.7 with you. This lesson reads through the real code of lesson 3.9's solution, `s08_dashboard.py`,
move by move — keep that file open in another window. On the board's screen, keep the **BENTO Playground** card open, and if you want to try the sound card,
be somewhere you can speak or clap near the board.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 3.7 — HMI design: cards, visual order, colour and the widget budget](../l07-hmi-design/README.md)

## Concepts

The firmware already does 70% of the work: drawing every widget with LVGL, managing the cross-core IPC queue, reading four sensors, converting the magnetic field
into degrees, and handling touch. The remaining 30% is ours: which values sit together, which value must stand out, what colour means what, how often to update,
and who gets a share of the budget. None of these five are Python syntax — they are pure design work.

**Move 1, preparing the screen.** `ui.screen()` clears every existing widget — skip it and leftovers from a previous script eat into the budget before anything even starts.
Follow it with `sleep_ms(200)` so CM55 can catch up, then read `sensors.bmi270.motion()` once, discarded, inside a try, so the wait happens right there,
before building any cards. The first read on the Eva Kit can stay silent for up to 16 seconds (the Dev Kit has not been measured) — that is waiting,
do not unplug the cable yet, and on the Dev Kit, never flip a switch on the base, because those are power switches. The file deliberately has no `sensors.init()`.
On the Eva Kit, the firmware rejects it with `OSError`, because the CM55 owns the I2C bus for the whole set of sensors. On the Dev Kit, that line passes but is unnecessary —
so one set of code runs on both boards.

**Moves 2–4, four cards.** Chart only takes integers, so we multiply the real value by 10 and set the axis to -150 to 150 (that is -15.0 to
+15.0 m/s²); feeding `int(ax)` directly would give a staircase graph. The first series gets its colour from the Chart's `color=`; the other two come from
`add_series()`, which returns an index for use with `set_next()`. The chart shows the trend, the number shows the current value, so they sit together. `ui.Compass`
uses `w` as its diameter, taking degrees through `.value()`, where 0 means north. The degree number gets font 28, the largest on the screen,
and the direction name comes from `DIRS[int((heading + 22.5) / 45.0) % 8]` — adding 22.5 shifts the bucket boundaries so north spans 337.5–22.5
degrees. The touch card uses **Bar, not Slider**, because a Slider is something a person drags, while a Bar is something the machine displays — the value comes from
a real finger on the CapSense strip, not from the screen. The two buttons use two lamps instead of a colour-changing label, because it still reads apart in black and white,
and the lamp dims when untouched, it does not vanish. The knob card uses an Arc to answer "where in the range is it", paired with a Seg7 for a number you can write down.
The one rule throughout all of this: pick a widget by "who changes this value", never by which one looks nicer.

**Move 5, the main loop.** The moment `ui.*` is first called, the firmware's automatic sensor task stops, so we read every sensor ourselves,
synchronously, in one go per round, touching the sensor as few times as possible. `motion()` gives six axes in one call; `capsense.read()` gives both buttons and
the slider in one call. Every read is wrapped in try, and except **never writes zero** — it just raises the `ok` flag, because zero looks exactly like a real
measured value, and lets the stale-value lamp be the one to tell the viewer. `ui.poll()` must be called every loop, or the screen hides widgets for about
two seconds before returning. `t0` at the top of the loop is the tool for measuring time spent per round; at 200 ms, ten minutes is about three thousand rounds — an expensive line will show itself on its own.

**New material for the compass card and a fifth card.** `sensors.bmm350` has five names, takes no arguments, and raises `OSError` when it cannot read.
Only `heading()` moves the calibration forward, and it returns a circular average of the last ten readings. The unit of
`magnetic()` still cannot be answered — footage from the board measures a combined magnitude of about 1532, while Earth's field sits at 25–65 µT. The rule is to write
"board units" and always compare against a baseline your team measures itself (direction is still correct, because atan2 only cares about the ratio). `cal_reset()`
and `cal_status()` have not yet been run by anyone on a real board. The `mic` module is baked into the firmware, with eight names; you must call `mic.start()` first;
the audio queue holds about 625 ms and hands out the oldest data first; `stats()` defaults to `fresh=True`, discarding stale data until `lag()` reads 0–48 ms.
`level()` is an octave scale — doubling rms raises level by about 9 units — and `rms()`, `peak()`, `level()` each read the mic fresh once,
about 32 ms each time. If you need several values, call `stats()` once.

## Worked example

Neither of these two files is part of the dashboard — they are pieces for the fifth card the team may choose to add. About 25 minutes.

1. **02_mic_sound_level_meter.py** — before running, predict about what level a quiet room, speaking, and a clap will give, then run and compare against
   the slides' numbers (7 · 54 · 92). Notice the bar, the number and the chart move together, then try changing `SENS` to 5 and measuring the same room again.
   The 0–100 number from `level()` is an octave scale — never read it as a percentage of full scale
2. **04_magnet_presence.py** — keep the board still while capturing the baseline, then bring a magnet close, and watch the deviation line spike past the threshold.
   Notice the threshold is computed from that room's own fluctuation (`spread * THRESH_K`, but never below `FLOOR_DEV`), not a hardcoded number.
   Try moving it near a steel desk or a computer screen and run again, and only ever record the value in "board units"

The other two sound files (`03_mic_clap_trigger.py` and `07_mic_window_stats.py`) and `05_door_open_switch.py`
belong to lesson 3.9. If you want to try switching `fresh` and watch the queue grow with your own eyes, open `07_mic_window_stats.py`.

| File | What this file teaches |
|---|---|
| [examples/02_mic_sound_level_meter.py](examples/02_mic_sound_level_meter.py) | A room sound-level meter |
| [examples/04_magnet_presence.py](examples/04_magnet_presence.py) | Detecting whether a magnet is nearby |

The slides for this lesson also refer to files that live in other lessons:

- [m03-sensor-hmi/l09-dashboard-lab/practice/s08_dashboard.py](../l09-dashboard-lab/practice/s08_dashboard.py) — the 4-card Mini-HMI dashboard, on the Eva Kit / Dev Kit (fill-in version)
- [shared/usecase/14_hard_iron_calibration.py](../../shared/usecase/14_hard_iron_calibration.py) — compass calibration, made into something measurable

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/02_mic_sound_level_meter.webp" alt="examples/02_mic_sound_level_meter.py running in the BENTO Emulator: A room sound-level meter" width="800" height="480" loading="lazy"><figcaption><a href="examples/02_mic_sound_level_meter.py"><code>02_mic_sound_level_meter.py</code></a> A room sound-level meter</figcaption></figure>
<figure><img src="img/screens/04_magnet_presence.webp" alt="examples/04_magnet_presence.py running in the BENTO Emulator: Detecting whether a magnet is nearby" width="800" height="480" loading="lazy"><figcaption><a href="examples/04_magnet_presence.py"><code>04_magnet_presence.py</code></a> Detecting whether a magnet is nearby</figcaption></figure>
</div>

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. A teammate puts sensors.init() back at the top of the file and runs it on the Eva Kit. What happens? *(choose one · objective 1)*
   - A) The firmware rejects it with OSError, because the CM55 owns the I2C bus for the whole set of sensors
   - B) It passes and makes the first read faster
   - C) It is necessary, or motion() will always return zero
   - D) The screen hangs for 16 seconds, then works normally

   <details><summary>Solution</summary>

   **A** — On the Eva Kit, the display core owns the sensor bus and keeps values ready for Python to read without needing init — init() raises OSError immediately. The long silence on the first read is waiting for the display core to start answering, which the file moves earlier by discarding one read before building any cards.

   </details>

2. Why does the CapSense card show finger position with ui.Bar instead of ui.Slider, even though they look similar? *(choose one · objective 2)*
   - A) The value comes from a finger on the real CapSense strip; a Slider would mislead viewers into thinking they can drag it on screen
   - B) Bar costs half the budget of Slider
   - C) Slider cannot accept values over 50
   - D) Bar draws faster, so it does not overflow CM55's queue

   <details><summary>Solution</summary>

   **A** — A Slider is something a person drags; a Bar is something the machine displays. Its look must match what it can actually do — pick the widget by who changes this value, not by which one looks nicer.

   </details>

3. heading equals 350.0 degrees. What direction name does DIRS[int((heading + 22.5) / 45.0) % 8] give, with DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]? *(choose one · objective 2)*
   - A) N
   - B) NW
   - C) W
   - D) IndexError, because the index is 8

   <details><summary>Solution</summary>

   **A** — (350 + 22.5) / 45 = 8.27, truncated to 8, then % 8 gives 0, which is N. Adding 22.5 shifts the bucket boundaries so north spans 337.5–22.5 degrees, and % 8 keeps the index from ever running out of bounds.

   </details>

4. Which statements about the dashboard's main loop are correct? Choose every correct one. *(choose all that apply · objective 3)*
   - A) motion() is used once instead of acceleration() and gyroscope(), to touch the sensor as few times as possible
   - B) On a failed read, except keeps the last value and raises the ok flag, never writing zero
   - C) ui.poll() must be called every loop, even on a page with no buttons at all
   - D) The firmware still reads sensors automatically the whole time, so there is no need to read them ourselves in the loop
   - E) On a failed read, write 0 to the screen so the viewer knows there is a problem

   <details><summary>Solution</summary>

   **A, B, C** — The moment ui.* is first called, the firmware's automatic reading stops, so we read ourselves synchronously and as few times as possible. Zero looks exactly like a real measured value, so the last value is kept and a stale-value lamp tells the viewer instead. poll is the moment CM55 gets to drain its queue — skip it and the screen hides widgets for about two seconds.

   </details>

5. A team is building a fifth card with mic and wants to add a value from sensors.bmm350. Which statements are correct? Choose every correct one. *(choose all that apply · objective 4)*
   - A) If you need both rms and peak, call mic.stats() once and unpack the values
   - B) Calling mic.peak() then mic.rms() back to back gives values from the same audio window
   - C) Values from bmm350.magnetic() should be reported as a deviation from a baseline in board units, not uT
   - D) Passing sens=9 to mic.start() raises ValueError immediately
   - E) Calling only magnetic() makes the calibration converge faster

   <details><summary>Solution</summary>

   **A, C** — rms(), peak(), level() each read the mic fresh once, about 32 ms apart, from different time windows; stats() gives three values from a single window. The unit of magnetic() still cannot be determined, so it must be compared against a baseline you measure yourself. sens outside 1–5 falls back to 3 silently, and only heading() moves the calibration forward.

   </details>

## Lab

**Walk through all five moves of the solution.** Open `s08_dashboard.py` in lesson 3.9's solution folder and answer in your learning log.

- [ ] Point to the line that moves the ten-plus-second wait on the Eva Kit to before any card is built, and explain why there is no `sensors.init()`
- [ ] Compare the Panel coordinates for all four cards in the file against your team's paper layout — which differ, and why
- [ ] Compute the direction name from `DIRS` by hand for heading 10, 100 and 350 degrees
- [ ] Write one line of reasoning for choosing Bar over Slider, and two lamps over a colour-changing label
- [ ] Point out how many lines in the loop "ask a sensor" per round, and which line keeps the screen from hiding its widgets
- [ ] If adding a sound card, write a plan for which `mic` call runs how many times per round, and how much of the 200 ms budget would be left

## Going further

Lesson 3.9 has you fill seven blanks in the practice file `s08_dashboard.py` one at a time, then prove it by running continuously for 10 minutes,
recording the round count every two minutes to tell "hung" apart from "slow".

Next lesson: [Lesson 3.9 — Hands-on: the mini-HMI dashboard and the 10-minute soak test](../l09-dashboard-lab/README.md)

## Reflect

- Which card in the solution chose a widget differently from what you drew in lesson 3.7, and whose reasoning is better?
- If a sensor fails to read for three seconds, how would you want a viewer to know, without reading an error?
- A measurement system that still cannot say what its own unit is — which decisions can its numbers be used for, and which cannot they?
