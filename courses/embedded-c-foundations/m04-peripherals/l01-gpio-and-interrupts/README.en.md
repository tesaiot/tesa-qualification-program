---
id: c-found.m04.l01
lang: en
title: {th: GPIO และ interrupt, en: GPIO and interrupts}
summary: {th: ขับหลอดไฟ อ่านปุ่ม และรับเหตุการณ์ด้วย interrupt ตามกติกาของบริบท ISR, en: 'Drive LEDs, read buttons and handle events with interrupts under ISR rules.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l02]
objectives:
- {th: ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง, en: Configure GPIO pins with PDL calls as outputs and inputs with the correct drive mode.}
- {th: เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR, en: 'Write a short, non-blocking ISR that hands work to a task instead of doing it inside.'}
- {th: กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก, en: Debounce a button without blocking waits.}
develops:
- {skill: mcu.gpio, to: 3}
- {skill: mcu.interrupts, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 606ee0c3334c9e88929c5e7d78ee21fcafed8ab2d556bb73e96dff704fe3096d
---

## Objectives

By the end of this lesson, you will be able to

1. Configure GPIO pins with PDL calls as outputs and as inputs, with the correct drive mode.
2. Write a short, non-blocking ISR that hands work off to a task instead of doing heavy work inside itself.
3. Debounce a button without using a blocking wait.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from earlier modules.

1. If an ISR and a task share a variable, how must it be declared, and is `volatile` alone enough (lessons 1.1 and 1.3)?
2. When CM33 is halted at a breakpoint inside a button-reading loop, how can a button press get lost (lesson 3.1)?

## See it work first

Open [examples/07_debounce_trace.c](examples/07_debounce_trace.c). This file feeds in values "read from the pin" every 10 ms from a table, simulating one button press whose contact bounces both on press and release, plus one noisy reading. **Predict before you run it:** how many presses will a raw count see, and how many will the debounced count see?

```sh
gcc -std=c11 -Wall -Wextra -o debounce_trace examples/07_debounce_trace.c
./debounce_trace
```

The raw count comes to 6, while the debounced count is 1, with PRESS and RELEASE times about 30 ms behind the first touch. Notice there isn't a single `delay` anywhere in the code — the whole debouncer is a function called once per reading, which returns immediately every time.

## Concepts

### 1. Drive mode is the whole job of GPIO

A single PSOC™ Edge pin needs three things set: who owns the pin (HSIOM), how it drives (drive mode), and its initial value. The PDL bundles this into one call, `Cy_GPIO_Pin_FastInit(port, pin, driveMode, outVal, hsiom)`. The SDK's [04_gpio_led_button.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L46-L60) example has a section titled "DRIVE MODES ARE THE WHOLE JOB":

```c
static void leds_init(void)
{
    for (unsigned i = 0U; i < LED_COUNT; i++) {
        Cy_GPIO_Pin_FastInit(s_leds[i].port, s_leds[i].pin,
                             CY_GPIO_DM_STRONG,
                             CYBSP_LED_STATE_OFF,   /* dark from the first cycle */
                             HSIOM_SEL_GPIO);       /* take the pin back from TCPWM */
    }
}

static void button_init(void)
{
    /* outVal = CYBSP_BTN_OFF (1) is what energises the pull-up. */
    Cy_GPIO_Pin_FastInit(CYBSP_USER_BTN1_PORT, CYBSP_USER_BTN1_NUM,
                         CY_GPIO_DM_PULLUP, CYBSP_BTN_OFF, HSIOM_SEL_GPIO);
}
```

Source: [04_gpio_led_button.c lines 126-141](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L126-L141) (Apache-2.0, tesaiot-pse84-devkit-sdk)

| To use a pin as | Drive mode from `cy_gpio.h` | Worth knowing |
|---|---|---|
| An output driving an LED | `CY_GPIO_DM_STRONG` (push-pull) | Give `outVal` the off value, so the pin doesn't blink at start-up |
| A button input tied to ground | `CY_GPIO_DM_PULLUP` | `outVal` must be 1 — this is the value that actually "turns on" the pull-up; sending 0 makes the button look permanently pressed |
| An input with an external resistor | `CY_GPIO_DM_HIGHZ` | No internal pull |
| An active-high input, such as data-ready | `CY_GPIO_DM_PULLDOWN` | The SDK's radar driver uses this |
| An output that's never read back | `CY_GPIO_DM_STRONG_IN_OFF` | Turns off the input buffer |

On this board's BSP, the user button `CYBSP_USER_BTN1` is P7.0, set to `CY_GPIO_DM_PULLUP` with an initial value of 1, and LED1 and LED2 are on P10.7 and P10.5 as `CY_GPIO_DM_STRONG` ([cycfg_pins.h lines 274-303 for the button](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h#L274-L303) and [lines 466-500 for the LEDs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h#L466-L500)). The button's define name is BTN1, but the silkscreen on the board says SW2 — the SDK's comment says to "Print the silkscreen name to a user" and to use the polarity values from the BSP (`CYBSP_BTN_PRESSED` = 0, `CYBSP_LED_STATE_ON` = 1) instead of writing the numbers yourself.

### 2. A good ISR: short, no waiting, no printing, and it hands work off

An ISR interrupts everything of lower priority. While it runs, every lower-priority interrupt has to wait, and every task is halted. The SDK's rule is therefore explicit: "Never `printf` from an IPC callback (ISR context)" (the catalogue's README), and the TACP example explains that a function named `_from_isr` is one that "takes no mutex, allocates nothing, and prints nothing." The shortest ISR in the SDK is the radar's data-ready handler.

```c
/** Radar data-ready interrupt handler */
static void radar_data_ready_isr(void)
{
    if (radar_drdy_events < 0xFFFFFFFFu) {
        radar_drdy_events++;
    }
    Cy_GPIO_ClearInterrupt(CYBSP_RADAR_INT_PORT, CYBSP_RADAR_INT_NUM);
    NVIC_ClearPendingIRQ(radar_irq_cfg.intrSrc);
}
```

Source: [radar_task.c lines 109-117](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L109-L117) (Apache-2.0, tesaiot-pse84-devkit-sdk). It does two things: records that an event happened (a `volatile` counter that saturates at its maximum rather than wrapping around) and clears the pin's interrupt flag. Without clearing it, the ISR would be called again endlessly. All the real work lives in the radar's task.

When a task needs waking up right away, use the FreeRTOS API functions ending in `FromISR`, then call `portYIELD_FROM_ISR()` so control can switch straight to the woken task as soon as the ISR finishes. Examples in the SDK: [ipc_tesaiot_handler.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/ipc_tesaiot_handler.c#L360-L363) uses `xSemaphoreGiveFromISR()`, while [sensor_auto_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299) copies a request into a queue with `xQueueSendFromISR()`, annotated "No printf here — this is ISR context." Another FreeRTOS rule: an ISR that calls a `FromISR` API must have a priority no higher than `configMAX_SYSCALL_INTERRUPT_PRIORITY`, which CM33's [FreeRTOSConfig.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L126-L138) explains "sets the highest interrupt priority from which interrupt safe FreeRTOS API functions can be called."

Setting up a GPIO pin's interrupt has two layers: the pin layer (PDL) and the CPU's NVIC layer. The SDK's radar driver follows this order.

| Step | Calls (from `bento_bgt60trxx_platform.c` and `radar_task.c`) |
|---|---|
| Clear anything pending, configure the pin | `Cy_GPIO_ClearInterrupt()` then `Cy_GPIO_Pin_FastInit(..., CY_GPIO_DM_PULLDOWN, ...)` |
| Choose the edge, enable the pin's mask | `Cy_GPIO_SetInterruptEdge(..., CY_GPIO_INTR_RISING)` and `Cy_GPIO_SetInterruptMask(..., 1u)` |
| Bind the ISR to an interrupt source | `Cy_SysInt_Init(&cfg, isr)`, where `cfg.intrSrc` is the IRQ number and `cfg.intrPriority` is the priority |
| Enable it at the NVIC | `NVIC_ClearPendingIRQ()` then `NVIC_EnableIRQ()` |

### 3. Non-blocking debouncing: count "time", not "how many reads in a row"

A button's contacts bounce for several milliseconds after both press and release. Debouncing means trusting a new value only once it's **held steady long enough**. The SDK's example reads every 10 ms and trusts a value once it's seen three times in a row, for a total of 30 ms, warning: "Debounce in TIME, not by reading the pin twice in a row: two reads 200 ns apart are two samples of the same bounce." ([04_gpio_led_button.c lines 116-124](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L116-L124))

"Non-blocking" means the debouncer never waits itself — it keeps its state in a struct and gets called once per reading, with the caller deciding the timing. That could be a task that calls `vTaskDelay(pdMS_TO_TICKS(10))` between rounds (as the SDK's example does), or an LVGL timer (as the Developer Hub's Button Monitor example does, reading every 25 ms and trusting a value once two ticks agree). If a pin interrupt is used to help, the ISR should only "wake" the task that runs the debouncer — because a single bounce can trigger dozens of interrupts, and counting directly inside the ISR would give the same number as counting the raw signal.

## Worked example

[examples/07_debounce_trace.c](examples/07_debounce_trace.c) runs in three parts.

- **Part 1**: the `raw[]` table holds a value read every 10 ms, including bounces on both press and release, plus one noisy reading.
- **Part 2**: `debounce_step()` takes one value, updates the state in a struct, and returns an event — with no waiting inside.
- **Part 3**: counts rising edges in the raw signal against the number of debounced PRESS events, on the same data.

Try changing things and predicting the result before you run it.

1. Change `DEBOUNCE_POLLS` to 1. How many presses does it count now, and how is this different from having no debouncing at all?
2. Change it to 10. How much does the PRESS event's timing shift by, and how would a user feel about a button that slow to respond?
3. Extend the noisy reading in the last row to three consecutive readings. Does the result change? How would you choose `DEBOUNCE_POLLS` given that?

## Practice

Open [practice/07_debounce.c](practice/07_debounce.c). There are 3 gaps to fill in inside `debounce_step()`, and four test cases: a clean press, a bouncy press, a short noise spike, and a press held for a hundred thousand rounds.

```sh
gcc -std=c11 -Wall -Wextra -o debounce practice/07_debounce.c && ./debounce
```

## Solution

Try it yourself for at least 15 minutes first, then open [solution/07_debounce.c](solution/07_debounce.c). The most common mistake is not stopping the `agree` count at `DEBOUNCE_POLLS` — if `agree` is a small type (such as `uint8_t`) and the button is held down a long time, the counter wraps around. The hundred-thousand-round held-press test exists to catch exactly this. Another thing to notice: the noise test passes even before you fill anything in (empty code always returns `EV_NONE`), so that test only means something once the real press-case tests pass too.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** measure debounce quality on a real board, then design a button read that uses an interrupt and hands work off to a task.

1. Build with `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button`, then flash and unplug/replug the cable. (Full steps in [lesson 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md).)
2. During the five seconds the example watches the button, press SW2 three different ways, once each: slowly five times, as fast as you can, and with a light tap. Note the counted number against how many times you actually pressed it.
3. (If you have a QWA309 base board with working buttons) flash the Button Monitor example from the Developer Hub (link at the bottom of the page), which reads buttons on P17.5 and P17.7 with a timer every 25 ms, and run the same experiment. Compare the results with step 2.
4. On paper (or in code, if you're ready), design reading SW2 with a falling-edge interrupt: list every PDL call following the table in concept 2, using the BSP's `CYBSP_USER_BTN1_PORT`, `CYBSP_USER_BTN1_NUM` and `CYBSP_USER_BTN1_IRQ`. Write an ISR that clears the flag and wakes a task with `xSemaphoreGiveFromISR()`, with the task calling `debounce_step()`. Explain why the press isn't counted directly inside the ISR. (If you try this on the board, note which interrupt priority you used and what happened — this course has not yet tested this code on the board.)

**Evidence to keep in your portfolio:** the table of results for all three press styles (and for the Button Monitor, if you tried it), the serial console log, and your draft ISR and task design with an explanation.

## Going further

- Open [`cy_gpio.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h) and find `CY_GPIO_INTR_RISING`, `CY_GPIO_INTR_FALLING` and `CY_GPIO_INTR_BOTH`. Which edge should an interrupt-driven debouncer listen for?
- The [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) documentation's task notifications are a lighter alternative to a semaphore for waking a single task. The SDK has an example using `xTaskNotifyFromISR()` in OPTIGA's PAL (`pal_i2c.c`).

Next lesson: [lesson 4.2, timers and clocks](../l02-timers-and-clocks/README.md)

## Reflect

- Which everyday button have you run into that "registers twice from one press," and can you now guess where its designer went wrong?
- If an ISR needed to do a millisecond's worth of work, how would you split that work between the ISR and a task?

## References

- [SDK: cm33/io/04_gpio_led_button.c (drive modes and non-blocking debouncing)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [SDK: CM33-side examples (what to know about ISR context)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: tesaiot-radar/radar_task.c (the data-ready ISR and interrupt setup)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c)
- [SDK: the BSP's cycfg_pins.h (button and LED pins)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Interrupt (Wikipedia)](https://en.wikipedia.org/wiki/Interrupt)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open an example on the Developer Hub to read the code, download it, or flash a prebuilt firmware image.

- [QWA309 — Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) — reads two buttons on P17.5 and P17.7, active-low with pull-ups, using a timer every 25 ms, showing press/release state, press count, and hold time on LVGL. (The button names on the board's silkscreen don't agree across sources — go by the pin numbers.)
- [QWA309 — Hardware Button Menu](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu) — navigates an LVGL menu with physical buttons, SW6=Move, SW5=Select (no touch involved) — a headless/kiosk UX pattern.
