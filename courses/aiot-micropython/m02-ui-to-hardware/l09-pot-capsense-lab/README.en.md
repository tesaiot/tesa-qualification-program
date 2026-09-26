---
id: aiot-mpy.m02.l09
lang: en
title: {th: 'ลงมือทำ: เกจลูกบิดกับแถบสัมผัส', en: 'Hands-on: the potentiometer gauge and touch slider'}
summary: {th: เติมหกช่องว่างในไฟล์ฝึกจนเกจลูกบิดกับแถบสัมผัสทำงานครบบนบอร์ด วางค่าดิบเทียบค่ากรองแล้วบนจอเดียว แล้วอธิบายได้ว่าทำไมเฉลยจึงตัดสินเกณฑ์จากค่าที่กรองแล้ว และแก้อาการที่ไม่มี error ให้เห็นได้เอง, en: 'Fill the six blanks in the practice file until the knob and touch-slider gauge works fully on the board with raw and filtered values side by side, then explain why the solution judges the threshold on the filtered value and fix the symptoms that show no error.'}
level: L2
time_min: {concept: 10, practise: 20, lab: 35, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m02.l08]
objectives:
  - {th: 'เติมหกช่องว่างใน practice/s05_pot_capsense.py ทีละจุด รันทีละครั้ง จนเกจผ่านเกณฑ์ MVP บนบอร์ด: แถบเดินตามลูกบิดตลอดช่วง 0-100 เกณฑ์หยุดเองที่ 10 และ 95 ไฟเตือนติดทีละดวงเมื่อข้ามเกณฑ์ แถบสัมผัสเดินตามนิ้ว ไฟปุ่มทองแดงติดถูกดวง และตัวเลขบนจอเปลี่ยนวินาทีละครั้ง', en: 'Fill the six blanks in practice/s05_pot_capsense.py one at a time, running after each, until the gauge meets the MVP criteria on the board: the bar follows the knob over the full 0-100 range, the threshold stops by itself at 10 and 95, one warning lamp at a time lights when crossing the threshold, the touch bar follows the finger, the copper-button lamps light the correct one, and the on-screen numbers change once per second.'}
  - {th: อธิบายพฤติกรรมของเฉลยได้ว่าทำไมการอ่านห้าบรรทัดอยู่ใน try เดียวพร้อมธง fresh ทำไมไฟเตือนตัดสินจาก ema_pct ไม่ใช่ค่าดิบ (กัน alarm chattering) และถ้าเปลี่ยน alpha เป็น 0.05 กับ 0.8 สองบรรทัดขวาล่างจะต่างกันอย่างไร, en: 'Explain the solution behaviour, namely why the five reads share one try with a fresh flag, why the warning lamps judge ema_pct rather than the raw value (to avoid alarm chattering), and how the two bottom-right lines differ when alpha is changed to 0.05 and to 0.8.'}
  - {th: วินิจฉัยอาการที่ไม่มี error ให้เห็นจากตารางกับดักได้ถูกสาเหตุ (เช่น ค่ากรองเท่าค่าดิบ ui.Scale ไม่ขยับ ช่องเกณฑ์ขึ้น 0070 ปุ่มสัมผัสกลับด้าน) และเลือกไฟล์ตัวอย่างที่ตอบอาการนั้นได้, en: 'Diagnose symptoms that show no error from the trap table to their real cause (such as filtered equal to raw, a ui.Scale that never moves, a threshold box showing 0070, inverted touch buttons) and pick the example file that answers that symptom.'}
develops: [{skill: sys.sensors-actuators, to: 2}, {skill: sys.dsp, to: 2}, {skill: gui.hmi, to: 2}, {skill: soft.problem-solving, to: 1}]
assesses: [{skill: sys.sensors-actuators, level: 2, evidence: practice/s05_pot_capsense.py}, {skill: sys.dsp, level: 2, evidence: practice/s05_pot_capsense.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-05.html (slides 42–67), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: d5951f8e4d2ae5ce2f6f29862a80fda9b2a2a8eb1b334d790efb456ec62fb04b
---

# Lesson 2.9 — Hands-on: the potentiometer gauge and touch slider

> Module 2 — From Screen to Hardware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the six blanks in the practice file until the knob and touch-slider gauge works fully on the board with raw and filtered values side by side, then explain why the solution judges the threshold on the filtered value and fix the symptoms that show no error.

## Objectives

By the end of this lesson you will be able to:

1. Fill the six blanks in practice/s05_pot_capsense.py one at a time, running after each, until the gauge meets the MVP criteria on the board: the bar follows the knob over the full 0-100 range, the threshold stops by itself at 10 and 95, one warning lamp at a time lights when crossing the threshold, the touch bar follows the finger, the copper-button lamps light the correct one, and the on-screen numbers change once per second
2. Explain the solution behaviour, namely why the five reads share one try with a fresh flag, why the warning lamps judge ema_pct rather than the raw value (to avoid alarm chattering), and how the two bottom-right lines differ when alpha is changed to 0.05 and to 0.8
3. Diagnose symptoms that show no error from the trap table to their real cause (such as filtered equal to raw, a ui.Scale that never moves, a threshold box showing 0070, inverted touch buttons) and pick the example file that answers that symptom

## Before you start

Following on from lesson 2.8, which took the gauge code apart into five moves, today you make values flow into that screen yourself. Before writing code, read all three pages of the "common traps" table in the slides.
On the board's screen, keep the BENTO Playground card open, and when plugging in the USB cable, lift every finger off the touch pad completely (the baseline is captured at boot).
On the Dev Kit, never flip a switch on the base, since it is a power switch, not a reset button. Have your learning log ready to record voltage readings and to photograph the screen.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 2.8 — Filtering: EMA vs Median, then the gauge code](../l08-filters/README.md)

## Concepts

The practice file already has the full four-card screen with 33 pieces written (one over the course budget of 32 — see the slides for a suggestion on which piece to cut). Do not touch it; our job is making values flow into it. The file presets starting values
(`pct = 0.0`, `slider = 0`, `events = []`), so it already runs before you fill in anything. Use this as a tool: fill in one blank at a time, run after each, and watch the screen "wake up" piece by piece.
If it breaks, you know right away it broke at whatever you just added.

The solution makes three decisions you must be able to explain. First, all five reads sit inside the same `try`; if the display core does not answer this round, the whole screen's values stay as one consistent set,
never half old and half new, and the `fresh` flag tells the value-quality line that what you see is from a previous round. Second, `over = ema_pct >= th` uses the **filtered** value.
If it used the raw value, the lamps would flicker back and forth whenever the value sat close to the threshold. Real control panels call this alarm chattering, and it is one reason people on the shop floor turn off warning sounds entirely.
Third, the bar and lamp update every 200 ms round, but the number is rewritten once per second, because the eye can read a position at once but cannot keep up with a number running five times a second.

The trap table has twenty-three rows, and many show no error at all. Some come from the order of operations against the hardware (a finger left resting during boot, or the display core not yet answering right after a reset).
Some come from a value silently clamped (`Median(window=4)` gives 5, `SMA(window=200)` gives 64). Some come from misunderstanding a widget (`ui.Scale` does not accept `.value()`;
a spinbox does not change value on a touch, so it needs +/- buttons; `.color()` on `ui.Bar` sets the track, not the value bar). When you get stuck, start from the symptom in the table, not by fixing code that was never wrong.

When there is a known, limited set of choices — such as the six filters — a "next" button hides the whole list. `ui.Roller` keeps the choices spread out and always highlights the selected one.
Two things worth knowing, already measured: `value=` at creation time is both the selected row and the Thai font size, so it is never set at creation — command `.value(n)` afterward instead —
and `.prop(ui.PROP_VISIBLE_ROWS, n)` overwrites the height set by `h=`, so pick one or the other.

## Worked example

**Must be finished within this lesson** (about 40 minutes total; if you have already done 01 and 06 in lessons 2.7 and 2.8, do only 05)

- `05_adc_counts_to_volts.py` (10 minutes) — before pressing forward, predict how much coarser the steps get as the bit count drops, and watch the last step, where the number claims more bits than the real steps you can actually catch. A number can look prettier without being more precise.
- `01_capsense_dimmer.py` from lesson 2.7 (15 minutes) — drag your finger and release it, and see that `slider()` equalling 0 does not mean the finger was released.
- `06_ema_time_constant.py` from lesson 2.8 (15 minutes) — read the tau of each alpha, then pick the MVP's alpha from the numbers.

**Open whichever answers what you're stuck on**

- Touching the pad and not sure whether the board registered it, or your hand is wet: `02_capsense_menu_wet_hand.py` — a touch pad has no resistance to feel, so it must always answer back through the screen, a light and a sound, and water on the pad makes the board read a finger as resting there continuously
- The filtered value still jumps along with a single outlier: `07_median_beats_mean.py` — press forward until the window reaches 7, and watch the median line absorb three spikes in a row, because a window of N can tolerate at most (N-1)//2 consecutive spikes
- The value still wiggles after you let go: `03_pot_setpoint_deadband.py` — adds the rule that a move smaller than this counts as no move at all, and pins the ends of the scale to 0 and 100

Optional further reading, outside the passing criteria: `04_pot_taper_volume.py` (halfway on a volume knob is not half of what the ear hears as loud) and `10_roller_picks_the_filter.py`
(pick a filter by swiping, with no sensor needed — try comparing it with the round-robin button of `08_six_filters_one_signal.py`)

| File | What this file teaches |
|---|---|
| [examples/02_capsense_menu_wet_hand.py](examples/02_capsense_menu_wet_hand.py) | A two-button touch menu, and the matter of a wet hand |
| [examples/03_pot_setpoint_deadband.py](examples/03_pot_setpoint_deadband.py) | A setpoint knob, with a dead band |
| [examples/04_pot_taper_volume.py](examples/04_pot_taper_volume.py) | Why a volume knob must follow a curve |
| [examples/05_adc_counts_to_volts.py](examples/05_adc_counts_to_volts.py) | A raw number from the ADC is not a voltage — it is a count of steps |
| [examples/07_median_beats_mean.py](examples/07_median_beats_mean.py) | One outlier destroys an average, but cannot touch a median |
| [examples/10_roller_picks_the_filter.py](examples/10_roller_picks_the_filter.py) | Choosing by swiping, not by pressing round after round |

The slides for this lesson also refer to files that live in other lessons:

- [m02-ui-to-hardware/l07-adc-capsense/examples/01_capsense_dimmer.py](../l07-adc-capsense/examples/01_capsense_dimmer.py) — a touch slider as a dimmer switch
- [m02-ui-to-hardware/l08-filters/examples/06_ema_time_constant.py](../l08-filters/examples/06_ema_time_constant.py) — what EMA's alpha means in real units of time
- [m03-sensor-hmi/l06-accel-chart-lab/examples/01_imu_vibration_monitor.py](../../m03-sensor-hmi/l06-accel-chart-lab/examples/01_imu_vibration_monitor.py) — watching a machine's vibration

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/02_capsense_menu_wet_hand.webp" alt="examples/02_capsense_menu_wet_hand.py running in the BENTO Emulator: A two-button touch menu, and the matter of a wet hand" width="800" height="480" loading="lazy"><figcaption><a href="examples/02_capsense_menu_wet_hand.py"><code>02_capsense_menu_wet_hand.py</code></a> A two-button touch menu, and the matter of a wet hand</figcaption></figure>
<figure><img src="img/screens/03_pot_setpoint_deadband.webp" alt="examples/03_pot_setpoint_deadband.py running in the BENTO Emulator: A setpoint knob, with a dead band" width="800" height="480" loading="lazy"><figcaption><a href="examples/03_pot_setpoint_deadband.py"><code>03_pot_setpoint_deadband.py</code></a> A setpoint knob, with a dead band</figcaption></figure>
<figure><img src="img/screens/04_pot_taper_volume.webp" alt="examples/04_pot_taper_volume.py running in the BENTO Emulator: Why a volume knob must follow a curve" width="800" height="480" loading="lazy"><figcaption><a href="examples/04_pot_taper_volume.py"><code>04_pot_taper_volume.py</code></a> Why a volume knob must follow a curve</figcaption></figure>
<figure><img src="img/screens/05_adc_counts_to_volts.webp" alt="examples/05_adc_counts_to_volts.py running in the BENTO Emulator: A raw number from the ADC is not a voltage — it is a count of steps" width="800" height="480" loading="lazy"><figcaption><a href="examples/05_adc_counts_to_volts.py"><code>05_adc_counts_to_volts.py</code></a> A raw number from the ADC is not a voltage — it is a count of steps</figcaption></figure>
<figure><img src="img/screens/07_median_beats_mean.webp" alt="examples/07_median_beats_mean.py running in the BENTO Emulator: One outlier destroys an average, but cannot touch a median" width="800" height="480" loading="lazy"><figcaption><a href="examples/07_median_beats_mean.py"><code>07_median_beats_mean.py</code></a> One outlier destroys an average, but cannot touch a median</figcaption></figure>
<figure><img src="img/screens/10_roller_picks_the_filter.webp" alt="examples/10_roller_picks_the_filter.py running in the BENTO Emulator: Choosing by swiping, not by pressing round after round" width="800" height="480" loading="lazy"><figcaption><a href="examples/10_roller_picks_the_filter.py"><code>10_roller_picks_the_filter.py</code></a> Choosing by swiping, not by pressing round after round</figcaption></figure>
</div>

## Practice

The practice file has six `# เติม:` (fill in) blanks, ordered the way the program runs. The raw value and voltage already move before you fill anything in, because the file already reads them; the rest wakes up piece by piece.

- Blank 1: `ema = dsp.EMA(alpha=0.2)` outside the loop. The screen does not change yet, but it must exist before blank 5, and `alpha=` must always be written by name
- Blank 2: `pct = sensors.pot.percent()` — the percentage number and the "raw" line start moving
- Blank 3: `slider = sensors.capsense.slider()` — the bottom-left touch bar follows your finger
- Blank 4: `pot_bar.value(int(max(0, min(100, pct))))` — the bar over the ruler on the top-left card follows the knob
- Blank 5: `ema_pct = ema.update(pct)` — the "filtered" line moves, and the two warning lamps start switching by threshold, because `over` is computed from `ema_pct`
- Blank 6: `events = ui.poll()` — the threshold's +/- buttons start responding. This blank is skipped most often, because the file already runs without it; the symptom is buttons that do not respond, with not a single line of error

Send each blank to the board and watch the screen before moving to the next. If you open the solution, read it until you understand it, then type it yourself — never copy and paste.

| Practice file | Topic |
|---|---|
| [practice/s05_pot_capsense.py](practice/s05_pot_capsense.py) | The knob + the touch slider + an EMA filter (fill-in version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.md#วิธีใช้เฉลย) first.

| Solution | Goes with |
|---|---|
| [solution/s05_pot_capsense.py](solution/s05_pot_capsense.py) | [practice/s05_pot_capsense.py](practice/s05_pot_capsense.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. You fill in the first five blanks; the screen is complete and the numbers move, but pressing the threshold +/- buttons does nothing at all, with no error whatsoever. What is the most likely cause? *(choose one · objective 1)*
   - A) Blank 6 has not been filled in yet; events is still [], and ui.poll() is never called, so events have no way of ever reaching the loop
   - B) ui.Spinbox must be tapped directly on the number to change its value
   - C) sensors.init() must be called first, or the buttons will not work
   - D) On-screen buttons cannot be used alongside a CapSense pad

   <details><summary>Solution</summary>

   **A** — The practice file sets events = [] so it can run before anything is filled in, which is why blank 6 is the one skipped most often. Without calling ui.poll(), buttons do not respond and some widgets stay hidden for as long as two seconds. An empty spinbox cannot be changed by a finger at all, which is exactly why it needs buttons beside it.

   </details>

2. After filling in blanks 1–4, the top bar already follows the knob, but no matter how far you turn past the threshold of 70, the "over" lamp never lights. Which explanation is correct? *(choose one · objective 1)*
   - A) over is computed from ema_pct, which is still 0.0 until blank 5, ema_pct = ema.update(pct), is filled in
   - B) ui.Led must have .color() commanded before it can light
   - C) The warning lamps must wait for the number to change once per second first
   - D) The threshold of 70 is higher than the knob can physically reach

   <details><summary>Solution</summary>

   **A** — In the solution, over = ema_pct >= th, so the warning lamps judge the filtered value. Before blank 5 is filled in, ema_pct is still its default of 0.0, so the "below threshold" lamp stays lit on its own.

   </details>

3. A friend suggests changing it to over = pct >= th, to make the warning lamp more responsive. What should you expect? *(choose one · objective 2)*
   - A) When the value sits close to the threshold, the lamps will flicker back and forth following the raw value's jitter (alarm chattering), until people on the shop floor stop paying attention to the warning
   - B) The lamp will be steadier, because the raw value has no lag
   - C) No difference, because the raw and filtered values are always equal
   - D) The program will raise TypeError

   <details><summary>Solution</summary>

   **A** — The raw value jitters at its lowest bits all the time; once the value sits close to the threshold, the lamp will keep switching. That is why the solution judges the filtered value, trading a small lag for a lamp people can trust.

   </details>

4. If dsp.EMA(alpha=0.2) is changed to alpha=0.05, then to alpha=0.8, what happens to the bottom-right "filtered" line? *(choose one · objective 2)*
   - A) 0.05 is very steady but follows your hand so slowly it feels laggy; 0.8 is almost the raw value, filtering only a little
   - B) 0.05 is almost the raw value; 0.8 is very steady but slow to follow
   - C) Both give the same result, because EMA clamps alpha to 0.2
   - D) 0.05 makes the filtered value start from zero and climb for several seconds every time it runs

   <details><summary>Solution</summary>

   **A** — alpha is the weight of the new value; the lower it is, the more it trusts the past, so it is steady but lagging; the higher it is, the closer to the raw value. And the first sample is used directly as the starting value, so the filtered value never has to climb up from zero.

   </details>

5. Which symptom-to-fix pairs from the trap table are correct? Choose every correct one. *(choose all that apply · objective 3)*
   - A) The EMA line equals RAW every round → move the creation of dsp.EMA to a single point outside the loop
   - B) ui.Scale never moves at all → the thing that must move is the ui.Bar placed over it
   - C) The threshold box shows 0070 → call sp_th.digits(2, 0)
   - D) The touch buttons report inverted → press Program to Device to run the script again
   - E) You want the bar to turn red past the threshold → call .color() on ui.Bar

   <details><summary>Solution</summary>

   **A, B, C** — Inverted buttons happen because the baseline is captured at boot; you must lift every finger off and unplug and replug the USB cable — running the script again does not help — and .color() on ui.Bar sets the track, not the value bar, which is why the solution reports state with lamps and text instead.

   </details>

## Lab

**The MVP for lessons 2.7–2.9.** Do this on a real board, and record the results in your learning log.

- [ ] Turning the knob makes the bar follow across the full range from 0 to 100, and the numbers on the ruler under the bar are readable at every tick
- [ ] The raw / percentage / voltage values all appear and agree logically (the far right is roughly 65535 and 100%); for voltage, record the reading you actually get to compare against a multimeter
- [ ] Pressing +/- changes the number in the threshold box and stops on its own at the range edges of 10 and 95
- [ ] Turning the knob past the threshold switches the lamps, one at a time only — never both lit at once
- [ ] Dragging a finger on the touch slider makes the bottom bar follow the finger's position, and touching a copper button lights the correct lamp (not inverted)
- [ ] The two bottom-right lines show the raw and filtered values at the same time, and the filtered line is visibly steadier
- [ ] The on-screen number changes once per second, not five times a second (stare for ten seconds and count)
- [ ] The team can answer how the result differs if `alpha` is changed to 0.05 and to 0.8 (try it for real and stare at the two bottom-right lines for ten seconds)
- [ ] Attach a photo of the screen taken while holding the knob turned, to your learning log

## Going further

Team homework: pick one of the four extensions in the slides — an alpha playground (RAW, EMA 0.05, EMA 0.5 on one screen), Median against a spike from tapping the board,
the knob commanding real lights split into ranges by `gpio.num_leds()` with hysteresis against flicker, or a touch button that switches screens by checking the rising edge of the pin. All four build on the same solution file.
Module 3 begins at lesson 3.1, moving from a knob someone turns to a sensor measuring the real world with `sensors.bmi270.motion()` and `dsp.tilt()` — keep the alpha your team chose for later use.

Next lesson: [Lesson 3.1 — The accelerometer and tilt: roll and pitch](../../m03-sensor-hmi/l01-accelerometer-tilt/README.md)

## Reflect

- If you had to send the knob's value to the cloud every 5 seconds, would you send the raw value or the filtered one, and what does sending the filtered value cost you in lost information?
- If the destination is an alarm system, what is the price of the lag your team's chosen filter adds?
