---
id: c-found.m04.l02
lang: en
title: {th: Timer และสัญญาณนาฬิกา, en: Timers and clocks}
summary: {th: ทำงานเป็นจังหวะด้วย timer ของฮาร์ดแวร์และของ RTOS และเข้าใจว่าสัญญาณนาฬิกากำหนดความแม่นยำอย่างไร, en: Run periodic work with hardware and RTOS timers and understand how clocks set accuracy.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l01]
objectives:
- {th: คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้, en: Compute timer settings from the clock frequency and the desired interval.}
- {th: เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล, en: 'Choose between a hardware timer and an RTOS software timer for a task, with reasons.'}
- {th: อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ, en: Explain how the rate of a background task affects system load.}
develops:
- {skill: mcu.timers, to: 3}
- {skill: mcu.clock, to: 2}
- {skill: rtos.freertos, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 3ee4856f3633fd13d750e5a3c4c05e16aea55106cf3d7f17f5ab574990adf2f8
---

## Objectives

By the end of this lesson, you will be able to

1. Compute a timer's settings from the clock frequency and the interval you want.
2. Choose between a hardware timer and an RTOS software timer for a given job, with reasons.
3. Explain how the rate at which a background task runs affects the load on the whole system.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from earlier lessons.

1. The debouncer in lesson 4.1 reads the button every 10 ms. Who sets that 10 ms rhythm — the debouncer itself, or its caller?
2. `175000 * 65535` overflows 32 bits — what about `65536 * 1000000` (lesson 1.1)?

## See it work first

Open [examples/08_timer_math.c](examples/08_timer_math.c). Every number in this file is read from files the Device Configurator generated in the SDK's BSP. **Predict before you run it:** how often, in milliseconds, does the BSP's `GENERAL_PURPOSE_TIMER` setting overflow?

```sh
gcc -std=c11 -Wall -Wextra -o timer_math examples/08_timer_math.c
./timer_math
```

The answer is exactly 1000 ms, and the following lines show that this same 100 MHz clock, through different dividers, becomes the timing for PWM, UART at 115200, I2C at 400 kHz, and the radar's SPI at 25 MHz. The UART's frequency doesn't divide evenly, coming out -0.22% off — the result of integer division.

## Concepts

### 1. From clock to time: two formulas

On the PSOC™ Edge E84, in the SDK's template, a group of peripherals (TCPWM0, SCB2 as the UART console, SCB3 as the radar's SPI, and others) uses the CLK_HF10 clock, set to 100 MHz ([cycfg_clocks.c lines 153-154](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L153-L154), and the peripheral-group table in [pse84_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/pse84_config.h#L6956-L7010)). Each peripheral has its own divider, set with `Cy_SysClk_PeriPclkSetDivider()`, whose PDL documentation says a value N "causes integer division of (divider value + 1)".

- The frequency the timer counts at: **f<sub>cnt</sub> = f<sub>src</sub> / (N + 1)**
- The time for one full cycle of a timer counting from 0 to period: **T = (period + 1) / f<sub>cnt</sub>**

A real example from the BSP: `GENERAL_PURPOSE_TIMER` is TCPWM0 counter 2, using a 16-bit divider value of 9999, giving 100 MHz / 10000 = 10 kHz, with `period = 9999` and an interrupt enabled at terminal count ([cycfg_peripherals.c lines 1115-1125](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L1115-L1125)). 10000 beats at 10 kHz is 1 second. At this commit, no code in the template actually starts this timer yet — it's something the BSP has prepared and left ready. The functions to start it live in [`cy_tcpwm_counter.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_tcpwm_counter.h), such as `Cy_TCPWM_Counter_Init()`, `Cy_TCPWM_Counter_Enable()` and `Cy_TCPWM_TriggerStart_Single()`.

The same interval can be reached with many different divider-and-period pairs. A smaller divider gives finer resolution (each tick is shorter), but the period must be large enough. And the accuracy of everything downstream **can never exceed the source's**: if the source is off by 1%, every timer derived from it is off by 1% too. The extreme case is the watchdog, which uses a low-accuracy internal oscillator — the PDL documentation states an error of ±30% (lesson 4.3).

### 2. A hardware timer, or an RTOS software timer

FreeRTOS in the template sets `configTICK_RATE_HZ` to 1000 ([CM33's FreeRTOSConfig.h line 66](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L66)) — one tick is 1 ms, so anything tied to ticks can't be finer than one tick.

| You need | Use | Why |
|---|---|---|
| A PWM waveform on a pin, or measuring pulse width (capture) at microsecond timing | A hardware timer (TCPWM) | Hardware counts on its own regardless of CPU load, but there's a limited number of them, and ISR work must stay short |
| Periodic work at a millisecond scale or coarser, inside a task | `vTaskDelayUntil()` in that task | A task has its own stack and can wait or call a blocking API |
| Calling a short function once or periodically without creating a whole task | An FreeRTOS software timer (`xTimerCreate()`) | The callback runs in the timer service task (priority 3 in the template's config); it must never block, because every timer shares that one task |
| Periodic work on CM55's screen | LVGL's `lv_timer_create()` | Every one of the SDK's CM55-side examples uses this, because the work must run inside the GFX task and must never block |

A frequent mistake is confusing `vTaskDelay()` with `vTaskDelayUntil()`. FreeRTOS's task.h documentation explains that `vTaskDelay()` "specifies a wake time relative to the time at which the function is called," while `xTaskDelayUntil()` "specifies the absolute (exact) time at which it wishes to unblock" ([Infineon FreeRTOS release-v10.6.202's task.h](https://github.com/Infineon/freertos/blob/release-v10.6.202/Source/include/task.h)). A loop that does 5 ms of work then calls `vTaskDelay(100 ms)` therefore repeats every 105 ms, not 100 ms, drifting further with every round. The template already enables `INCLUDE_vTaskDelayUntil` in its config file.

### 3. A background task's rate is the whole system's load

A task that reads a sensor every P milliseconds, taking C milliseconds each round, occupies the CPU and the I2C bus in roughly the proportion C/P. The SDK's [05_auto_push_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L12-L75) example tells the real story of a task that reads every sensor and sends the results to CM55 (every 100 ms by default).

- **The delay comes after reading, not during it.** The example measures how many real rounds it actually got versus how many it expected, warning that if it's fewer, "the reads themselves are costing more than the interval."
- **A cliff at 50 ms.** `sensor_auto_set_rate()` accepts 20 to 5000 ms, but below 50 ms the loop "reads ONLY the accelerometer," because the other sensors take too much bus time to fit inside a 20 ms budget. Setting it to 20 ms to make everything faster instead makes five of the six sensors stop reporting, silently.
- **Two readers on one bus.** "Two readers on one bus at two rates is a bug waiting for a deadline; one publisher and many consumers is not." If a value up to 100 ms old is acceptable, read from the cache with `sensor_auto_get_bmi270()`, which never touches the bus at all.

Rate is also tied to correctness. Edge AI's IMU model was trained on 50 Hz data. The 08_deepcraft_link example warns that if data is allowed to arrive every 100 ms instead, "every verdict is computed over five times the intended span of time and is confidently wrong." The wrong rate doesn't just waste power — it makes the results wrong.

## Worked example

[examples/08_timer_math.c](examples/08_timer_math.c) runs in three parts.

- **Part 1**: `divided_hz()` applies the PDL's N + 1 divider formula.
- **Part 2**: calculates the cycle time of `GENERAL_PURPOSE_TIMER` and `PWM_LED_CTRL` from the BSP's values (for the PWM, we assume it counts 0..period the same way a plain counter does — check the chip's manual to be sure).
- **Part 3**: calculates the UART's baud rate, the I2C's SCL frequency, and the SPI's SCLK from the same clock.

Try changing things and predicting the result before you run it.

1. To make `GENERAL_PURPOSE_TIMER` fire every 250 ms without changing the divider, what should period be?
2. If the UART's divider changed from 86 to 85, what is the real baud rate and the error for each — which one is closer to 115200?
3. Why can this program use `double`, while the same kind of function in the SDK's firmware is usually written with integers (hint: CM33's `printf` in the template has no float support)?

## Practice

Open [practice/08_timer_math.c](practice/08_timer_math.c). There are 4 gaps to fill in, written entirely with integers, the way firmware is.

1. `divided_hz()`, following the divider formula.
2. `overflow_us()`, which needs a 64-bit intermediate.
3. `pick_timer()`, finding the smallest divider that gives exactly the right interval with a 16-bit period, and saying plainly when it can't.
4. `baud_error_ppm()`, the error in parts per million.

```sh
gcc -std=c11 -Wall -Wextra -o timer_math practice/08_timer_math.c && ./timer_math
```

Notice the 1-second test expects a divider of 1599 and a period of 62499, not 9999 and 9999 as in the BSP — both pairs give exactly 1 second, but the exercise's rule is to pick the smallest divider. A clearly written requirement makes sure there's only one right answer.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/08_timer_math.c](solution/08_timer_math.c). Worth comparing: every place that multiplies before dividing uses `uint64_t` or `int64_t`, and `pick_timer()` never touches the caller's value when it can't find an answer — the same principle as the honest results from lesson 3.2.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** measure a background task's real rate on the board, and explain the gap between the set rate and the measured one.

1. Build with `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/sensors/05_auto_push_task`, then flash and unplug/replug the cable.
2. From the serial console, note the initial `rate`, the sensor mask, and the line `measured ... cycles in 1000 ms (expected about ...)`, both at the default rate and once the example switches to 25 ms.
3. From "expected" and "measured", calculate how many milliseconds each round actually took, and estimate how much time the sensor reads themselves consume per round (C), using: actual round time = C + the delay.
4. Answer: at the 25 ms rate, which sensors are still being read, and why is the measured cycle count close to, or far from, what was expected?
5. Check that the example restores everything afterward (the `--- restored ---` line). If it doesn't, the example reports `RESTORE INCOMPLETE` — note that down.

**Evidence to keep in your portfolio:** the full example log, your calculation table from step 3, and your explanation for step 4.

## Going further

- The [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) documentation's software timers section explains the timer command queue, and why a callback must never block.
- Challenge: write a task that runs every 20 ms using `vTaskDelayUntil()`, and measure with `xTaskGetTickCount()` how far it drifts over 1000 rounds, compared with `vTaskDelay()`.
- Open the header of [cy_tcpwm_counter.h](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_tcpwm_counter.h), read about counting modes (up, down, up/down), and explain whether the period + 1 formula needs to change in another mode.

Next lesson: [lesson 4.3, the watchdog](../l03-watchdog/README.md)

## Reflect

- Which periodic job in your own project uses `vTaskDelay()` when it should use `vTaskDelayUntil()`, and how would you tell that it's drifting?
- If a user asked you to "read the sensor twice as fast," what would you ask them before changing the value?

## References

- [SDK: cm33/sensors/05_auto_push_task.c (a background task's rate and the 50 ms limit)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c)
- [SDK: the BSP's cycfg_peripheral_clocks.c (each peripheral's divider)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripheral_clocks.c)
- [SDK: the BSP's cycfg_peripherals.c (TCPWM and SCB settings)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
