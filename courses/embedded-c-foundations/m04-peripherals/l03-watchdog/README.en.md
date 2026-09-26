---
id: c-found.m04.l03
lang: en
title: {th: Watchdog, en: The watchdog}
summary: {th: ใช้ watchdog ให้ระบบฟื้นตัวเองเมื่อค้าง โดยป้อนในจุดที่พิสูจน์ว่าระบบยังทำงานจริง, en: 'Use a watchdog so the system recovers when it hangs, feeding it only where progress is proven.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l02]
objectives:
- {th: อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด, en: Explain what a watchdog does and what happens when it is not fed in time.}
- {th: ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก, en: Identify the correct feeding point in a multi-task program and explain why feeding from a timer ISR is a trap.}
- {th: ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด, en: Design reset-cause logging so you know when the watchdog fired.}
develops:
- {skill: mcu.watchdog, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: ea91f7a1e4eef360628fb42c2f0e8aa863c73128183265870776e9f5198e26d8
---

## Objectives

By the end of this lesson, you will be able to

1. Explain what a watchdog does, and what happens if it isn't fed within its set time.
2. Identify the correct place to feed a watchdog in a multi-task program, and explain why feeding it from a timer's ISR is a trap.
3. Design reset-cause logging so you can tell when the watchdog fired.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from earlier lessons.

1. The SDK's radar stall watchdog reports 0 stalls even while its task is stuck — where does it sit that causes this (lesson 3.2)?
2. Does a timer's ISR still run if every task is stuck in an endless loop (lessons 4.1 and 4.2)?

## See it work first

Open [examples/09_watchdog_sim.c](examples/09_watchdog_sim.c). This simulated system has three tasks and a watchdog that resets when it goes unfed for more than 10 ticks. At tick 40, the `sensor` task hangs, and the example tries two strategies: A feeds from a timer's ISR every tick; B has a supervisor feed it only once every task has reported progress. **Predict before you run it:** at which tick does strategy A reset?

```sh
gcc -std=c11 -Wall -Wextra -o watchdog_sim examples/09_watchdog_sim.c
./watchdog_sim
```

Strategy A **never resets at all**, even after the task has been hung for 60 ticks, because the timer's ISR neither knows nor cares what state the tasks are in. Strategy B resets within the set time, and can even say which task is missing. A watchdog fed from the wrong place is barely better than no watchdog at all.

## Concepts

### 1. What a watchdog is, and how it works on PSOC™ Edge

A watchdog is a counter running on its own clock, separate from the CPU. Software must "feed" (clear) it periodically; if it isn't fed before it reaches its set value, it resets the whole chip. The idea: if software can still feed it, it's still running; if it can't, it's hung, and starting over is better than staying hung forever.

The PDL has a WDT driver in [`cy_wdt.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_wdt.h). This board's BSP declares `CY_IP_MXS22SRSS` ([cy_device_headers_ns.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/cy_device_headers_ns.h#L733-L736)), which enables using the PDL's match-value style function set. The setup order per the driver's documentation is:

| Step | Function |
|---|---|
| Unlock, then disable before changing it | `Cy_WDT_Unlock()` then `Cy_WDT_Disable()` |
| Choose the clock source (for MXS22SRSS, either PILO or clk_bak) | `Cy_WDT_SetClkSource()` |
| Set the timeout | `Cy_WDT_SetMatch()`, and `Cy_WDT_SetIgnoreBits()` if you need it shorter |
| Enable, then lock to prevent accidental changes | `Cy_WDT_Enable()` then `Cy_WDT_Lock()` |
| Feed it | `Cy_WDT_ClearWatchdog()`, whose documentation says "Clears ("feeds") the watchdog, to prevent a XRES device reset" |

A warning from the PDL's documentation, worth knowing before enabling this: the watchdog's timeout must be longer than the chip's boot time ("a WDT reset can be generated faster than a device start-up"), a changed value takes effect a couple of low-frequency clock cycles late, and a low-accuracy oscillator needs a generous margin (the documentation cites an ILO on another chip family that can be off by ±30%). For this chip's PILO or clk_bak accuracy, check the chip's datasheet, and remember that during debugging, halting the CPU at a breakpoint can cause the watchdog to reset partway through (lesson 3.1).

**Status in the SDK's template:** we searched the mtb-only template's source at this commit and found no code that enables the hardware watchdog (`Cy_WDT_Enable` or `Cy_WDT_ClearWatchdog`). The only call present is `Cy_WDT_Unlock()`, inside the BSP-generated clock setup code ([cycfg_clocks.c line 584](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L584)). What the SDK actually uses is one task's software watchdog, which is the next topic.

### 2. Where to feed it: wherever progress is actually proven

A watchdog can only check what "whoever feeds it" knows. If it's fed from a timer's ISR, that only proves the timer's interrupt is still firing — which is usually still true even after every task has died. If each task feeds it itself, then whichever task happens to survive keeps feeding on behalf of the ones that died. The pattern that actually works is **checking in with a single supervisor**.

1. Each important task sets its own bit when it makes **real progress** (successfully reads a sensor, successfully sends a message) — not just when it wakes up.
2. A low-priority supervisor task checks periodically, feeds the watchdog only once every bit is set, then clears all the bits.
3. The watchdog's timeout is longer than the slowest task's round, plus margin.

A low-priority supervisor also catches another symptom for free: a high-priority task stuck in a loop that never yields the CPU. The supervisor never gets to run, the watchdog never gets fed, and it resets.

The SDK has a real software-watchdog example: [08_deepcraft_link.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c#L37-L45) explains that the model link's task was once found "asleep inside its own queue receive with a command outstanding" after switching models hundreds of times. `deepcraft_task_watchdog()` must be called at about 1 Hz "from a context that never blocks," and it detects the stuck work and wakes the task to continue. The same comment admits plainly that "The watchdog does not fix the underlying fault" — a watchdog is recovery, not a bug fix, and every time it fires must be logged.

### 3. Logging the reset cause: knowing when the watchdog fired

A watchdog that resets silently makes a system look like it "sometimes just reboots on its own." What's needed is a record that survives across the reset.

- **Read the cause.** `Cy_SysLib_GetResetReason()` returns a bitset, such as `CY_SYSLIB_RESET_HWWDT` (0x0001), `CY_SYSLIB_RESET_SOFT` (0x0010), and `CY_SYSLIB_RESET_SWWDT0`..`3` for the multi-counter watchdog (see the table in [`cy_syslib.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_syslib.h)). Test it with `&`, since several bits can be set at once. The SDK's own BSP uses this function while setting up clocks, and annotates that a value of 0 means "POR, XRES, or BOD" ([cycfg_clocks.c lines 571-575](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L571-L575)). After recording it, call `Cy_SysLib_ClearResetReason()`, or the next boot will see the same old cause.
- **Keep a trace in RAM that survives boot without being zeroed.** The SDK's linker script has a `.noinit` section that start-up code never touches ([pse84_ns_cm33.ld lines 339-343](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L339-L343)). The supervisor writes "which task hasn't checked in" into it every round, so after a reset you know who was stuck. Right after power-up, whatever's in that RAM is garbage, so you need a magic number to tell the two apart. The template's CM55 side follows the same principle — it writes a fault marker to a fixed SRAM address, commented "survives until power cycle."
- **Export it.** Print it at boot, count occurrences, and if there's connectivity, send it to a log-collecting system.

## Worked example

[examples/09_watchdog_sim.c](examples/09_watchdog_sim.c) runs in three parts.

- **Part 1**: each task runs one round then checks in by setting its bit (the `sensor` task hangs starting at tick 40).
- **Part 2**: strategy A feeds every tick regardless of state; strategy B feeds once every bit is set, then clears them.
- **Part 3**: a simulated watchdog keeps counting, and if it times out, prints that it reset, naming the task that didn't check in.

Try changing things and predicting the result before you run it.

1. In strategy B, remove the line `checkin = 0u;`. Does the watchdog still catch the hang? Why?
2. Change `WDT_TIMEOUT_TICKS` to 1. What does strategy B do? What does that tell you about choosing a watchdog's timeout?
3. Make the `ui` task only make progress every 5 ticks (checking in every 5 ticks), then find the smallest `WDT_TIMEOUT_TICKS` that doesn't reset incorrectly.

## Practice

Open [practice/09_watchdog.c](practice/09_watchdog.c). There are 5 gaps to fill in: a check-in supervisor, and boot logging that survives across a reset.

1. `wd_checkin()` sets a task's bit.
2. `supervisor_poll()` does not feed while any task is still missing.
3. `supervisor_poll()` clears the bits after feeding.
4. `boot_record_update()` tells garbage in RAM apart using a magic number.
5. `boot_record_update()` counts watchdog resets and records which task was missing.

```sh
gcc -std=c11 -Wall -Wextra -o watchdog practice/09_watchdog.c && ./watchdog
```

## Solution

Try it yourself for at least 15 minutes first, then open [solution/09_watchdog.c](solution/09_watchdog.c). Two things worth comparing: the solution tests the reset cause with `&`, not `==`, and a comment warns that `|=` inside `wd_checkin()`, when called from several tasks at once on a real board, needs a critical section or an FreeRTOS event group instead — knowledge from lesson 1.3 turning up in an unexpected place.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** read a real board's reset cause across several scenarios, and design watchdog feeding for the template.

1. In your own project (on a new branch, per lesson 2.3), add these three lines to `proj_cm33_ns/main.c`, right after `init_retarget_io();` (the SDK's B1 documentation says the UART is ready from this point):
   ```c
   uint32_t reset_reason = Cy_SysLib_GetResetReason();
   printf("[RST] reason=0x%08lx%s\r\n", (unsigned long)reset_reason,
          (reset_reason & CY_SYSLIB_RESET_HWWDT) ? " HWWDT" : "");
   ```
   Build and flash it.
2. Record the printed value across four scenarios: unplugging and replugging, pressing the board's reset button (if it has one), right after `make program`, and unplugging and replugging again afterward. Which values are 0? Which have bits set? Does a bit persist across a reset? (This code doesn't clear the cause yet — that's part of what you should notice.)
3. Compare the values you got against the table in `cy_syslib.h`. Which match what you expected, and which don't? Write down what you actually observed, separately from what you inferred.
4. Design (on paper) enabling the hardware watchdog for the template: name at least three tasks that would need to check in, from the tasks the template creates (see `main()` in proj_cm33_ns/main.c), the slowest round for each, the watchdog timeout you'd choose with margin, and where the supervisor would sit. (This course has not yet tested enabling the hardware watchdog on this template — if you try it for real, do it on a separate branch and record everything you find, including any effect on debugging.)

**Evidence to keep in your portfolio:** the diff of your change to main.c, a table of the reset-cause values across all four scenarios with explanations, and your watchdog design draft from step 4.

## Going further

- Read the Functional Description, Clearing WDT and Reset Detection sections in the header of [`cy_wdt.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_wdt.h), and calculate how often you'd need to feed it using the documentation's example match value.
- Compare a windowed watchdog (which also forbids feeding it too soon) against an ordinary one, in [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer). What extra kind of bug does a windowed watchdog catch?

Next lesson: [lesson 4.4, DMA](../l04-dma/README.md)

## Reflect

- Which system you've used before "sometimes just reboots on its own" — what would you now ask its developers?
- If a watchdog makes a product look like it never hangs, how would the team ever find out there's a bug that still needs fixing?

## References

- [SDK: cm55/edge_ai/08_deepcraft_link.c (deepcraft_task_watchdog)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c)
- [SDK: the BSP's cycfg_clocks.c (using Cy_SysLib_GetResetReason and Cy_WDT_Unlock)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer)
