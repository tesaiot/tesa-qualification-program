---
id: c-found.m01.l02
lang: en
title: {th: แผนที่หน่วยความจำ stack และ heap, en: 'Memory map, stack and heap'}
summary: {th: รู้ว่าข้อมูลแต่ละก้อนอยู่ที่ใด และป้องกัน stack ล้นกับการจองหน่วยความจำในที่ที่ไม่ควร, en: Know where each piece of data lives and prevent stack overflow and allocation in the wrong place.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l01]
objectives:
- {th: 'จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static', en: 'Classify the variables of an example program as stack, heap or static.'}
- {th: อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่, en: Read a task's remaining stack from the counters the SDK exposes and judge whether it is near overflow.}
- {th: อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง, en: Explain why dynamic allocation does not belong in an ISR or a real-time loop.}
develops:
- {skill: prog.memory, to: 3}
- {skill: lang.c, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: d37dfbe111eefca4d4755b5aaba6476205bbc877d4294672bb5ae920141fd608
---

## Objectives

By the end of this lesson, you will be able to

1. Classify the variables of an example program as stack, heap or static memory.
2. Read a task's remaining stack from the counters the SDK exposes, and judge whether it is close to overflowing.
3. Explain why dynamic allocation does not belong in an ISR or a real-time loop.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from lesson 1.1.

1. What happens when a `uint8_t` is added past 255, and why does the SDK's example widen to 64 bits before multiplying?
2. Which kinds of variables need to be `volatile`, and does `volatile` help with a `count++` that an interrupt can land in the middle of?

## See it work first

Open [examples/02_where_it_lives.c](examples/02_where_it_lives.c). **Predict before you run it:** which address is larger — `local_buf` (a local variable in `main`) or `g_zeroed` (a global variable)? Then run it.

```sh
gcc -std=c11 -Wall -Wextra -o where_it_lives examples/02_where_it_lives.c
./where_it_lives
```

The actual numbers on your machine won't match your classmate's, but you'll see the addresses fall into clear groups: constants and global variables sit close together, the block `malloc` hands back sits in another region, local variables sit further away still, and the `depth 1, 2, 3` lines show that the deeper the function calls go, the **lower** the stack frame's address gets. Microcontrollers have the exact same groups — the difference is there's no operating system randomising them: **the linker script places every group**, and we can read it.

## Concepts

### 1. The memory map: who places what, where

| Section | Holds | Where it lives on the PSOC™ Edge E84 in the SDK's template |
|---|---|---|
| `.text` `.rodata` | Code, `const` constants, string literals | External QSPI flash — the CPU runs code directly from there (XIP) |
| `.data` | Static variables with a non-zero initial value, e.g. `int g = 42;` | The initial value sits in flash and is copied into RAM at boot |
| `.bss` | Static variables with no initializer, or initialized to 0 | RAM zeroed at boot; takes no space in flash |
| heap | Blocks handed back by `malloc()` | Whatever RAM is left after `.bss` |
| stack | Local variables, return addresses | The top of that RAM region, growing down towards lower addresses |

All of this can be read straight out of the SDK's CM33 non-secure linker script
([pse84_ns_cm33.ld](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L346-L361)).
For example, `.data` is placed with `> m33_data AT > m33_nvm_sel`, meaning it runs from RAM but its master copy is kept in flash, and the copy table at line 190 is annotated "From load address in ext flash." The heap is whatever grows to fill the gap, from the end of `.bss` to just before the stack, and the stack starts at `__StackTop = ORIGIN(m33_data) + LENGTH(m33_data)` with a default size of `0x1000` bytes (line 47).

The consequence, noted in a comment in that same linker script from real board experience, is that **every byte `.bss` grows by is a byte the heap loses** ("every byte of .bss costs a byte of heap one for one", line 265). When a new screen was added, the heap shrank so far that mTLS started failing too, with `WARN: Malloc failed arena=121812 used=121308 free=504 largest_free=0`, and the comment concludes: "Eleven rounds of code review could not see that; the board said it in ten minutes." A static variable is never free — it always takes space from someone else.

### 2. Per-task stacks and the high-water mark

On a system running FreeRTOS, **each task has its own stack**, sized in words (4 bytes on a 32-bit CPU) when the task is created. For example, the mtb-only template's heartbeat task is created with `xTaskCreate(bento_heartbeat_task, "HB", 256, NULL, 1, NULL)` ([proj_cm33_ns/main.c line 309](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L309)). The `0x1000`-byte stack in the linker script, on the other hand, belongs to `main()` before the scheduler starts, and to interrupt handlers afterwards.

To know how deep a task has driven its stack, FreeRTOS uses a colouring trick: when a task is created, it paints the whole stack with the byte `0xA5` (`tskSTACK_FILL_BYTE` in tasks.c), and `uxTaskGetStackHighWaterMark()` counts how many words of untouched `0xA5` remain. This value is the **lowest it has ever been over the task's lifetime** — it can only go down, and the lower it is, the closer the task is to overflowing. The SDK exposes the same kind of counter in several places, such as `ai_engine_stack_words()` and `ai_engine_stack_free_words()` for the inference task, which the example [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L51-L62) explains returns the "ALL-TIME MINIMUM. It only ever falls," and warns that reading it has to scan the stack, so it should be read about once a second, not inside a display-drawing loop.

Don't rely only on the automatic checker. `configCHECK_FOR_STACK_OVERFLOW` is set to 2 on both cores, and the CM33 hook prints `FATAL: Stack overflow in task '...'`, but a comment in the linker script warns that it "only samples at a context switch" (line 307). A stack that overflows into neighbouring data between two checks can do damage before the hook ever fires. The approach that actually works is measuring the high-water mark while the system is under its heaviest load, and leaving headroom.

The rule of thumb this course uses in its exercises (this is our own rule, not a number from the SDK or FreeRTOS): fewer than 32 words free counts as **critical**; less than a quarter of the total free counts as **low** and calls for a bigger stack or moving large buffers off the stack.

### 3. The heap: why not allocate in an ISR or a real-time loop

The SDK's template sets `configHEAP_ALLOCATION_SCHEME` to heap_3 ([CM33's FreeRTOSConfig.h line 189](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L189)), under which FreeRTOS's `pvPortMalloc()` calls newlib's `malloc()` directly, suspending the scheduler for the duration (`vTaskSuspendAll()` then `xTaskResumeAll()`). Dynamic allocation does not belong in an ISR or a real-time loop, for four reasons.

1. **Unsafe in an ISR context.** FreeRTOS only allows an ISR to call functions ending in `FromISR`, and `xTaskResumeAll()` is not one of them.
2. **Unpredictable timing.** `malloc()` has to search for free space, and how long that takes depends on the heap's condition at that moment — a loop that must stay on time can't predict its own timing any more.
3. **Fragmentation.** After allocating and freeing blocks of varying sizes for long enough, the heap may have hundreds of free bytes in total with no single free run big enough. That's why CM33's `vApplicationMallocFailedHook()` prints both `free` and `largest_free` — a plain "Malloc failed" doesn't say whether the heap is actually empty or just fragmented ([main.c lines 411-425](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L411-L425)).
4. **No way to handle failure.** In an ISR there's nowhere to wait, nowhere to retry, and nothing should be printed at all.

The fix is to allocate everything at system start-up, or to use static buffers. The SDK does exactly this in several places: littlefs in the mtb-only variant is built with `LFS2_NO_MALLOC`, "because every buffer is supplied statically; a code path that would need the heap fails to compile instead of quietly allocating" ([variants/mtb-only.mk lines 35-39](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/variants/mtb-only.mk#L35-L39)), and the `10_littlefs_basics.c` example declares a 512-byte buffer as `static char s_buf[512];`, with the reasoning "the runner task's stack is not the place for it."

## Worked example

[examples/02_where_it_lives.c](examples/02_where_it_lives.c) runs in three parts.

- **Part 1** prints the address of eight objects, labelled with which section they belong to, so you can check by eye that the addresses really do cluster by label.
- **Part 2** prints how much space each kind of block takes, and whether it comes from the stack, the heap, or read-only data.
- **Part 3** calls three nested functions; each one prints the address of its own local variable, showing the stack growing downward.

Try changing things and predicting the result before you run it.

1. Move `uint8_t local_buf[64]` out of `main`. What does its correct label change to?
2. Add `static` in front of `uint8_t local_buf[64]` (still inside `main`). Which group does its address move to?
3. Change the condition `level < 3` to `level < 100000` and run it. What does the program do, and what happens instead on a microcontroller with no operating system watching over it?

## Practice

Open [practice/02_stack_watermark.c](practice/02_stack_watermark.c). This file simulates the way FreeRTOS measures the stack, using one array. There are 3 gaps to fill in.

1. `stack_paint()` — paint every byte with `0xA5`.
2. `high_water_bytes()` — count the run of `0xA5` bytes continuing in from the end the stack has not reached.
3. `percent_used()` — compute the percentage the same way the 07_engine_health example does, and must not divide by zero.

```sh
gcc -std=c11 -Wall -Wextra -o watermark practice/02_stack_watermark.c && ./watermark
```

Notice the test that calls `simulate_use()` more shallowly after having gone deep before — the expected value doesn't change, because the high-water mark is the lowest value over the whole lifetime.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/02_stack_watermark.c](solution/02_stack_watermark.c). The part worth comparing is `percent_used()`: the solution checks both `total == 0` and `free > total` before subtracting, because subtracting unsigned values into a negative result wraps around into a huge number (knowledge from lesson 1.1).

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** read the stack counters of two real tasks on the board, and judge whether they are safe.

1. Build the SDK's template with examples enabled (the full steps are in [lesson 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md)).
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1
   make program
   ```
   Then unplug the USB cable all the way and plug it back in.
2. On the screen, tap the **SDK Examples** card, choose `cm55/display/00_display_bringup`, and press **Run this example**. Note down two values: `stack %lu words` for the GFX task, and `stack never used: %lu words (all-time low)`.
3. Choose `cm55/edge_ai/07_engine_health` and run it. Note the line `inference task stack: ... words granted, ... still free at its worst (...% used)`. This example reads these two values before even checking whether a model is running, so you get a stack reading even with no model active. (If you instead see a message that the task was never created, note that down too — that's a valid measurement as well.)
4. Calculate the percentage used for the GFX task yourself, and judge both tasks using the exercise's rule of thumb (critical, low, or safe).
5. Open [10_littlefs_basics.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c). Pick five variables, such as `s_buf`, `k_known_paths`, `s_allow_write`, `present`, `n`, and classify each as stack, heap, or static, with a one-sentence reason each.

**Evidence to keep in your portfolio:** screenshots of both examples' output, a table of the values you noted, the calculation, the judgement, and the table classifying the five variables.

## Going further

- Read the CM33 linker script's `.cy_csr_buffers` section ([lines 261-324](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L261-L324)). The team moved an 8 KB static buffer and one task's stack out of `.bss` into a separate RAM region, to give that space back to the heap, then added an `ASSERT` to fail the build if those buffers ever crept back. Try explaining why "failing the build" is better than just writing a warning in the documentation.
- The [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview) on memory management: compare heap_1 through heap_5, and notice that once you use heap_3, `configTOTAL_HEAP_SIZE` in the config file no longer sets the actual heap size.

Next lesson: [lesson 1.3, structs, pointers and a ring buffer](../l03-structs-pointers-buffers/README.md)

## Reflect

- In a program you've written before, which large buffer was a local variable — and what would happen if you moved that program into a task with a 256-word stack?
- If a program had run fine for an hour, then started reporting `Malloc failed` with no leak in sight, what evidence would you collect to tell whether the heap is truly empty or just fragmented?

## References

- [SDK: cm55/edge_ai/07_engine_health.c (ai_engine_stack_words and ai_engine_stack_free_words)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: cm33/storage/10_littlefs_basics.c (buffers and the storage API's contract)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c)
- [SDK: cm55/display/00_display_bringup.c (the GFX task's high-water mark)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/display/00_display_bringup.c)
- [SDK: the CM33 non-secure linker script (pse84_ns_cm33.ld)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld)
- [Appendix X — Traps and anti-patterns (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
- [Infineon FreeRTOS @ release-v10.6.202 (the version the SDK's template pulls in): task.h](https://github.com/Infineon/freertos/blob/release-v10.6.202/Source/include/task.h)
