---
id: c-found.m01.l01
lang: en
title: {th: ภาษา C บนไมโครคอนโทรลเลอร์, en: C on a microcontroller}
summary: {th: ใช้ชนิดข้อมูลขนาดแน่นอน ตัวดำเนินการระดับบิต และ volatile กับรีจิสเตอร์ของอุปกรณ์, en: 'Use fixed-width types, bit operators and volatile with device registers.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: []
objectives:
- {th: เลือกชนิดข้อมูลขนาดแน่นอนจาก stdint.h ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้, en: Choose fixed-width stdint.h types for given values and explain overflow.}
- {th: เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง, en: 'Write correct read-modify-write set, clear and toggle operations with bit operators.'}
- {th: อธิบายว่าเมื่อใดต้องใช้ volatile กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt, en: Explain when volatile is required for variables shared with hardware or interrupts.}
develops:
- {skill: lang.c, to: 3}
- {skill: hw.architecture, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 57857a6353094bfa21e502adef8511cb9219dfb9115583dbcd08de2cd6e82590
---

## Objectives

By the end of this lesson, you will be able to

1. Choose fixed-width types from stdint.h that fit the values you store, and explain the effect of overflow.
2. Write correct set, clear and toggle bit operations using the read-modify-write pattern with bitwise operators.
3. Explain when `volatile` is required for variables shared with hardware or an interrupt.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). You can do the first half entirely on your own computer; the lab uses the TESAIoT Dev Kit board (PSOC™ Edge E84).

## Before you start

This course continues from someone who can already write Python or MicroPython. Try answering two questions in your head first.

1. In MicroPython, `x = 250 + 10` always gives 260. Do you think C on a microcontroller always gives 260 too? What does it depend on?
2. When you call `gpio.led(0).on()` and the LED turns on, something inside the chip must change. What do you think that something is, and where does it live?

What you need: a C compiler on your computer (gcc or clang) for the first half, and for the lab: the TESAIoT Dev Kit board, ModusToolbox™ 3.6, and the source of the [TESAIoT PSE84 Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) at commit `ef72c1b`.

## See it work first

Open [examples/01_types_and_bits.c](examples/01_types_and_bits.c) and **predict before you run it**: what number will the `count after +10` line print? Write your guess down, then compile and run it.

```sh
gcc -std=c11 -Wall -Wextra -o types_and_bits examples/01_types_and_bits.c
./types_and_bits
```

If you guessed 260, you weren't the only one. The program prints `count after +10 = 4`, because `uint8_t` can only hold 0 to 255 — a value past that wraps around. The next lines hold two more surprises: the bytes `0x30` and `0xF8` combine into -2000, and a 32-bit product is not the same as a 64-bit one. This lesson explains all three of those lines.

## Concepts

### 1. Fixed-width types and overflow

C makes no promise about how many bits an `int` is — that depends on the compiler and architecture. But device registers, bytes on a bus, and protocol packets are defined as an exact number of bits, so firmware work uses the types from `<stdint.h>`, such as `uint8_t`, `int16_t` and `uint32_t`, which are the same width on every machine.

| Value to store | Suitable type | Why |
|---|---|---|
| A byte on an I2C or UART bus | `uint8_t` | Matches the data size on the wire |
| A raw sensor value that can go negative, e.g. acceleration | `int16_t` | 16-bit two's complement, as the chip sends it |
| A cycle counter, time in milliseconds, an address | `uint32_t` | Wide enough, and matches the 32-bit CPU width |
| An intermediate product that might exceed 32 bits | `uint64_t` | Widen before multiplying, not after |

**Overflow** of an unsigned type is clearly defined to wrap around modulo 2<sup>N</sup> — for example, `uint8_t` 250 + 10 gives 4. Overflow of a signed type, on the other hand, is *undefined behaviour*: the compiler assumes it never happens, so never write code that relies on it.

The SDK relies on this in several places. For example, [`06_raw_register_access.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L243-L252) converts a value from the SHT40 sensor using a 64-bit intermediate variable, with a comment explaining why: "175000 * 65535 does not fit in 32 bits." And [`05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L110-L115) computes a cycle count with `sensor_auto_get_push_count() - before`, which stays correct even when the counter wraps around, because unsigned subtraction is modulo too.

### 2. Bitwise operators and read-modify-write

A single device register often packs several functions into different bit positions. If we overwrite the whole value, the bits belonging to other functions are lost along with it. The safe way is **read-modify-write**: read the current value, change only the bits that are ours, then write it back.

| What to do | Write it like this | Why the other bits don't change |
|---|---|---|
| Set a bit | `reg \|= mask;` | `x \| 0 == x` |
| Clear a bit | `reg &= ~mask;` | `x & 1 == x` |
| Toggle a bit | `reg ^= mask;` | `x ^ 0 == x` |
| Test a bit | `if (reg & mask)` | Nothing is written |
| Write a multi-bit field | Clear the field first, then OR in the value shifted and masked | Old bits in the field don't linger |

The comment in the SDK's example sums it up most concisely: "The safe shape for any register write: read it, change only the bits you own, write it back, read it again to confirm." ([06_raw_register_access.c lines 170-175](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L170-L175))

On real silicon we usually don't touch the register directly — instead we call functions from Infineon's **PDL (Peripheral Driver Library)** that do this for us, such as `Cy_GPIO_Set()`, `Cy_GPIO_Clr()` and `Cy_GPIO_Inv()`. The example [`04_gpio_led_button.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L62-L69) explains that these calls are a single register write with no prior read, and are "atomic per pin on this part," so there's no need to guard against tasks that control different pins on the same port racing each other. That's one reason to prefer PDL over writing `|=` to a GPIO register yourself. Another reason is LED and button polarity: the same example warns "POLARITY COMES FROM THE BSP, NOT FROM YOU" — use the name `CYBSP_LED_STATE_ON` instead of the number 1, because a later board revision might invert the polarity.

### 3. `volatile` is a promise to the compiler, not a lock

A compiler with optimisation enabled is entitled to keep a variable's value in a CPU register and drop reads or writes that look redundant or ineffective. If that variable is actually changed by "someone else" the compiler can't see, the program breaks silently. `volatile` says that **every read and every write must actually happen, in the order they appear in the code**. Use it whenever a value can change from outside the program's own flow of control, which includes

- **A device register** that hardware changes on its own (the PDL already declares its register structs this way).
- **A variable an ISR writes and a task reads**, such as `static volatile uint32_t radar_drdy_events`, which the radar's ISR increments ([radar_task.c line 97](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L97)).
- **A variable another core or DMA writes**, and a flag one task sets that another task reads, such as `volatile bool tesaiot_radar_presence_detected` ([line 51](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L51)).
- **A plain busy-wait counting loop**, such as `for (volatile uint32_t d = 0; d < 300000; d++) {}` in [proj_cm55/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L269) — without `volatile`, the compiler could delete the whole loop since it has no visible effect.

What `volatile` does **not** give you is atomicity. `count++` on a volatile variable is still a three-step read, modify, write, and an interrupt can still land in the middle of it. Guarding against that is the subject of lesson 1.3 and module 4.

## Worked example

[examples/01_types_and_bits.c](examples/01_types_and_bits.c) runs in three parts.

- **Part 1** prints the size of each type, then shows three kinds of overflow: `uint8_t` wrapping around, two bytes combining into a negative `int16_t`, and a product that must be widened to 64 bits before multiplying.
- **Part 2** uses a simulated "register" of type `volatile uint32_t`, setting, clearing and toggling bits one line at a time.
- **Part 3** writes a 3-bit MODE field with a single read and a single write, then reads the field back to check it.

Try changing things one at a time, predicting the result before you run it each time.

1. Change `uint8_t count` to `uint16_t` and run it. Why do you get 260 this time?
2. Remove the `(uint64_t)` cast from the `right` line and run it. What do the two numbers on that line become?
3. Change `mode` to 9 — what do you read back, and what does the mask protect?

Keep reading in the real SDK: the read-modify-write step in the `06_raw_register_access.c` example reads the BMI270's `PWR_CTRL` register, writes the same value back, then reads it again to confirm — all while holding the bus lock the whole time (locks are covered in lesson 5.2).

```c
uint8_t pwr_before = 0u, pwr_after = 0u;
bool w_ok = false, v_ok = false;

if (!sensor_i2c_lock(RAW_LOCK_TIMEOUT_MS)) {
    printf("  bus busy\r\n");
    return SDK_EX_BUSY;
}
if (sensor_i2c_read_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL, &pwr_before)) {
    /* The single-byte form... */
    w_ok = sensor_i2c_write_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                 pwr_before);
    /* ...and the general form, which is what you need for any
     * multi-byte register. Same byte again: still a no-op. */
    if (w_ok) {
        w_ok = sensor_i2c_write_reg(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                    &pwr_before, 1u);
    }
    v_ok = sensor_i2c_read_byte(ADDR_BMI270, BMI270_REG_PWR_CTRL,
                                &pwr_after);
}
sensor_i2c_unlock();
```

Source: [06_raw_register_access.c lines 176-196](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L176-L196) (Apache-2.0, tesaiot-pse84-devkit-sdk)

Why write the same value back? The file's header comment answers this: if you wrote `ACC_RANGE` (0x41) from here instead, the chip would change its measurement range but the driver wouldn't know — every acceleration value after that would be off by a factor of four, with no function ever returning an error. Read anything, but only write bits that nothing else relies on.

## Practice

Open [practice/01_bitops.c](practice/01_bitops.c). There are 2 gaps marked `TODO`: `bits_set()` and `bits_clear()`. Compile and run it before filling them in — you should see several failing tests. That's proof the tests are actually checking something.

```sh
gcc -std=c11 -Wall -Wextra -o bitops practice/01_bitops.c && ./bitops
```

Fill them in until the last line prints `PASS: 0 failure(s)`.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/01_bitops.c](solution/01_bitops.c). The answer is one line per function: `*reg |= mask;` and `*reg &= ~mask;`. The comments in the solution explain the most common bug: writing `*reg = mask;` or `*reg &= mask;`, which wipes out the bits belonging to other functions.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** run the SDK's GPIO and register examples on the board, and explain what you see using what you learned in this lesson.

If you haven't built the SDK's firmware template yet, do [lesson 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md) first. (An overview of building and flashing with ModusToolbox is in [TESAIoT Firmware Stack, lesson 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md).) The SDK's examples are disabled by default; enable and pick which one to run with make variables.

```sh
cd bento-firmware-template-mtb-only
make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
make program
```

1. **Unplug the USB cable all the way and plug it back in** after every flash (Appendix X #21 in the SDK docs: a reset through the debugger followed by a black screen, which looks like a failed flash even though it isn't). Open a serial console at 115200 8N1 before plugging it in.
2. Read the `[io/04]` log — you should see the number of LEDs the BSP defines, the line `read-back: on=1 off=0 (expect 1 and 0)`, then press the SW2 button on the board a few times within five seconds. Watch the `SW2 down` / `SW2 up` lines and the debounced press count.
3. Build again with `SDK_EXAMPLE_CM33=cm33/sensors/06_raw_register_access` and watch for three lines: the chip id read back (should be `0x24`), the raw X, Y, Z acceleration values, and the line `PWR_CTRL ... (verified, board unchanged)`.
4. In your lab notebook, answer: with the board lying flat, which raw axis is largest, and is it positive or negative? How is that value assembled from two bytes, and why does the example need to cast it to `uint16_t` before shifting?

**Evidence to keep in your portfolio:** the serial console log from both examples, and a short answer to question 4.

## Going further

- Open [`cy_gpio.h` from mtb-pdl-cat1 @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h) and find `Cy_GPIO_Pin_FastInit()` and the constants `CY_GPIO_DM_STRONG` and `CY_GPIO_DM_PULLUP`. Read how the `outVal` parameter affects pull-up mode, then compare it with the comment in `04_gpio_led_button.c` warning that passing 0 makes the button "appears permanently pressed".
- Challenge: write a `field_read(reg, msk, pos)` function to go with `field_write()` in the exercise, and add your own test for it.

Next lesson: [lesson 1.2, the memory map, stack and heap](../l02-memory-map-stack-heap/README.md) — asks where each variable in this lesson actually lives in memory.

## Reflect

- Which variable in a program you once wrote in Python would silently overflow if moved to C?
- If a teammate marked every variable `volatile` "just in case," how would you explain to them why that doesn't help, and might even slow things down?

## References

- [SDK: cm33/sensors/06_raw_register_access.c (read-modify-write on an I2C device)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/io/04_gpio_led_button.c (the PDL calls behind gpio.led()/gpio.button())](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [SDK: cm33/sensors/05_auto_push_task.c (an unsigned counter and subtracting its values)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c)
- [SDK: tesaiot-radar/radar_task.c (a volatile variable shared between an ISR and a task)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c)
- [Peripherals at a glance (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__peripherals__quickref.html)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
