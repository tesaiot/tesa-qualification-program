---
id: c-found.m01.l03
lang: en
title: {th: 'struct, pointer และบัฟเฟอร์วงแหวน', en: 'Structs, pointers and ring buffers'}
summary: {th: จัดข้อมูลด้วย struct ส่งต่อด้วย pointer และรับข้อมูลต่อเนื่องด้วยบัฟเฟอร์วงแหวน, en: 'Organise data with structs, pass it by pointer, and stream it through a ring buffer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l02]
objectives:
- {th: ออกแบบ struct สำหรับข้อมูลเซนเซอร์หนึ่งชุด และส่งให้ฟังก์ชันด้วย pointer แบบ const เมื่อไม่ต้องแก้, en: Design a struct for one sensor sample and pass it by const pointer when it is read-only.}
- {th: เขียนบัฟเฟอร์วงแหวนขนาดคงที่ที่อ่านและเขียนได้โดยไม่ทับข้อมูลที่ยังไม่ถูกอ่าน, en: Write a fixed-size ring buffer that never overwrites unread data.}
- {th: อธิบายความเสี่ยงเมื่อ ISR กับ task ใช้บัฟเฟอร์เดียวกัน และวิธีป้องกัน, en: 'Explain the risk when an ISR and a task share a buffer, and how to guard it.'}
develops:
- {skill: lang.c, to: 3}
- {skill: prog.algo-ds, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 6b73687db60c0851eb8ec9937cf03fc6e49e66bab856be46507bc323129480c5
---

## Objectives

By the end of this lesson, you will be able to

1. Design a struct for one sensor sample, and pass it to a function by const pointer when it doesn't need to be changed.
2. Write a fixed-size ring buffer that can be read from and written to without overwriting data that hasn't been read yet.
3. Explain the risk when an ISR and a task share the same buffer, and how to guard against it.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from lesson 1.2.

1. What happens to a 512-byte buffer declared as a local variable in a task with a 256-word stack, and what should it be declared as instead?
2. Why is `head - tail` on a `uint32_t` counter still correct even after `head` has wrapped around past zero (the hint is in lesson 1.1)?

## See it work first

Open [examples/03_sensor_sample.c](examples/03_sensor_sample.c). **Predict before you run it:** what is `sizeof(imu_loose_t)`? Its members are one `uint8_t`, one `uint32_t`, three `int16_t`, and one more `uint8_t`, which add up to 12 bytes. Then run it.

```sh
gcc -std=c11 -Wall -Wextra -o sensor_sample examples/03_sensor_sample.c
./sensor_sample
```

On a typical computer and on Cortex-M, you get 16, not 12, because the compiler inserts padding so the `uint32_t` starts on a 4-byte boundary. Reorder the same members from largest to smallest and the struct shrinks back to 12 bytes. When sensor data is stored by the thousand in a buffer, a 4-byte difference per sample adds up to several kilobytes.

## Concepts

### 1. A struct is one bundle of data, and a const pointer is a promise

Values that arise together should stay together. Three-axis acceleration read from the same conversion, the time it was read, and a flag saying whether the data is valid — if these are spread across several separate variables, a function ends up with a long, awkward parameter list, and it becomes easy to accidentally pair the X axis from this round with the Y axis from a previous one. The SDK uses structs like this throughout — for example, `health_t` in [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L77-L101) holds six counters read in the same instant, and `sample(health_t *h)` fills them in through a pointer.

Rules for passing a struct to a function:

| The function will | Pass it as | Example |
|---|---|---|
| Only read it | `const T *` | `int32_t magnitude_sq(const imu_sample_t *s)` |
| Fill in or change it for the caller | `T *` (an "output slot") | The SDK's `bool radar_dsp_snapshot(ipc_radar_range_t *out)` |
| Needs its own copy, and the struct is small | by value | Gets a copy; changing the copy doesn't touch the original, but every byte must be copied onto the stack |

`const` doesn't make code faster — it lets the compiler catch you when you accidentally change something you promised not to, and it tells anyone reading the code right away that this function is safe. The SDK's [04_gpio_led_button.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L95-L113) example uses a `static const led_def_t s_leds[]` table, and picks up one row with `const led_def_t *mirror` (line 203) — a pointer to data that must never be changed.

### 2. Ring buffers

When data arrives in a stream — bytes from a UART, or readings from a sensor — and the consumer runs on a different schedule from the producer, we need a fixed-size holding area that doesn't need `malloc`. A ring buffer is an array reused in a circle: the writer advances `head`, the reader advances `tail`.

```
 data:  [ . | . | A | B | C | . | . | . ]      A, B, C have not been read yet
                  ^tail       ^head            count = head - tail = 3
```

The design used in this lesson's exercise relies on three techniques.

- **A power-of-two size.** The position is computed with `counter & MASK` instead of `%`, which is slower on some CPUs (the SDK's radar buffer, sized `0x4000`, uses the same trick).
- **`head` and `tail` are counters that only ever increase.** The number of items is always `head - tail`, which distinguishes "empty" (equal) from "full" (differing by the capacity) without needing to sacrifice one slot.
- **Reject when full.** `push` returns `false`, and the caller decides for itself whether that counts as lost data or a reason to wait.

The policy for what happens when full is a design decision, not a detail. The SDK's radar task chooses the opposite of what we do here: when full, it "keep[s] newest samples, drop[s] oldest two" ([radar_task.c lines 466-480](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L466-L480)), because for detecting a person, the latest reading matters more than an old one — but for protocol bytes, dropping an old byte wrecks the whole frame. Another decision to make is what value to return when "empty": the SDK's TACP (the mtb-mpy variant) returns `-1` when empty and 0 to 255 when there's data, and warns that you must store it in an `int` and check for -1 before converting to `uint8_t`, because "a byte of 0xFF is real data and is not the empty marker" ([08_tacp_host_protocol.c lines 46-48](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c#L46-L48)). Our exercise avoids this problem by keeping the `bool` return value separate from the data handed back through a pointer.

### 3. When an ISR and a task share the same buffer

An ISR can interrupt a task at any moment — even in the middle of a line like `rb->head = rb->head + 1;`, which is a read, modify, write. If both sides change the same variable, an update can be lost. If the writer advances `head` before it has written the data into the slot, the reader might pick up a slot that's still empty; and if a task reads several bytes of data while an ISR is overwriting them, it gets a mix of old and new (a torn read). The SDK uses four real guards against this.

| Method | Use when | Where the SDK uses it |
|---|---|---|
| A single-writer, single-reader ring buffer: each side only ever changes its own counter, writes the data before advancing the counter, and a barrier separates the two | Bytes or small values arriving continuously | TACP's lock-free ring (mtb-mpy variant), where `tacp_request_delete_main_from_isr()` can push a byte in from ISR context |
| Have the ISR send a copy into an RTOS queue with `xQueueSendFromISR()`, and let a task pick it up | Chunk-sized messages, needing the task to wake immediately | [sensor_auto_task.c lines 274-299](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299) |
| A seqlock: the writer makes the sequence number odd while writing, the reader copies then checks that the sequence number hasn't changed and is even; if not, it reads again | A frequently read snapshot that can tolerate re-reads | [radar_dsp.c lines 284-320](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c#L284-L320) |
| A critical section: disable interrupts for the shortest possible time while reading or writing | Several variables of data that must change together | FreeRTOS's `taskENTER_CRITICAL()` |

Two things never to do: call `malloc` or `printf` inside an ISR (lesson 1.2 and module 4), and assume `volatile` alone is enough. `volatile` forces the read and write to actually happen, but it does not turn a read-modify-write into a single step.

## Worked example

[examples/03_sensor_sample.c](examples/03_sensor_sample.c) runs in three parts.

- **Part 1** compares two structs with the same members in a different order, printing `sizeof` and `offsetof` to show where the padding falls.
- **Part 2**: `sample_fill()` takes an `imu_sample_t *` to fill in values, while `magnitude_sq()` takes a `const imu_sample_t *` because it only reads.
- **Part 3**: the struct lives on `main`'s stack and its address is passed on, while `try_to_reset()` takes it by value, so it can only change its own copy.

Try changing things one at a time, predicting the result before you run it each time.

1. Uncomment the line `s->ax = 0;` inside `magnitude_sq()`. What does the compiler say?
2. Move `valid` and `seq` to the very front of `imu_sample_t`. Does the size change? Why?
3. Change `try_to_reset()` to take an `imu_sample_t *` and change the value through the pointer. What does the last line's result change to?

Keep reading in the real SDK: the reader side of the seqlock in `radar_dsp.c` copies the whole struct through the `out` pointer, then loops and re-reads until it gets a set that wasn't torn in the middle.

```c
bool radar_dsp_snapshot(ipc_radar_range_t *out)
{
    if (out == NULL) {
        return false;
    }
    if (!s_ready) {
        memset(out, 0, sizeof(*out));
        out->initialized = s_inited ? 1 : 0;
        return false;
    }
    uint32_t s1, s2;
    do {
        s1 = s_snap_seq;
        memcpy(out, (const void *)&s_snap, sizeof(*out));
        s2 = s_snap_seq;
    } while ((s1 != s2) || (s1 & 1u));       /* retry on torn/odd            */
    return true;
}
```

Source: [radar_dsp.c lines 303-320](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c#L303-L320) (Apache-2.0, tesaiot-pse84-devkit-sdk). The writer side (lines 284-297) bumps the sequence number to odd, calls `__DMB()`, writes every field, calls `__DMB()` again, then bumps the sequence number to even. Notice that the function returns `false` when there is no first frame yet, which is different from "no target" — a result that tells the truth is the subject of lesson 3.2.

## Practice

Open [practice/03_ring_buffer.c](practice/03_ring_buffer.c). There are 5 gaps to fill in — more than the previous two lessons, because you now have the full set of tools. `rb_count()`, `rb_is_empty()`, `rb_is_full()`, `rb_push()` and `rb_pop()`. The tests cover three cases.

- **The normal case:** first in, first out, and reading from an empty buffer must return `false`.
- **An edge case:** fill it with exactly 16 bytes, and the 17th byte must be rejected, with the first byte still unchanged.
- **An edge case:** the counter starts at `UINT32_MAX - 3` and runs past zero over 1000 rounds of writing and reading.

```sh
gcc -std=c11 -Wall -Wextra -o ring practice/03_ring_buffer.c && ./ring
```

## Solution

Try it yourself for at least 15 minutes first, then open [solution/03_ring_buffer.c](solution/03_ring_buffer.c). What the solution adds beyond what the tests require is a C11 `atomic_thread_fence()` between "write the data" and "advance head", and between "read the data" and "advance tail". On a computer, the tests pass even without this line — but when the writer is an ISR or another core, it's what stops the compiler or the CPU from reordering things. On Cortex-M in the SDK, CMSIS's `__DMB()` does this job. This is an example of something a test on the host computer cannot prove, which we'll come back to in lesson 6.2.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** watch a struct passed by pointer, and a seqlock, work for real on the board, then read the code to find out who owns the data.

1. Build the SDK's template with `make build -j ENABLE_PAGE_EXAMPLES=1`, then `make program`. Unplug the USB cable all the way and plug it back in. (The full steps are in [lesson 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md).)
2. On the screen, tap **SDK Examples** and run `cm55/sensors/02_radar_presence`. This example reads `radar_dsp_snapshot()` every 200 ms. Watch the top line: with no target, it shows `no target  seq ...  bin width ... mm`, and `seq` keeps climbing. Slowly move your hand toward the board and watch the line change to `target ... mm  bin ...`.
3. Note the `seq` value twice, about ten seconds apart, and estimate how many new snapshots the radar announces per second.
4. Read [ipc_tesaiot_handler.c lines 330-363](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/ipc_tesaiot_handler.c#L330-L363). This function runs in ISR context, copies a message into a single variable `s_pending`, then wakes a task with a semaphore. In your notes, answer: if a second message arrives before the task finishes reading the first, what happens to `s_pending`? Then search the same file, or the CM55-side files, for anything that guarantees this can't happen (if you can't find one, write that down instead of guessing).
5. Compare this with [sensor_auto_task.c lines 274-299](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299), which sends a copy of a struct into a queue. Which approach copes with back-to-back messages better, and what's the trade-off?

**Evidence to keep in your portfolio:** screenshots of both states of the radar example, the `seq` values you noted with your calculation, and your answers to questions 4 and 5.

## Going further

- Extend the exercise so the buffer holds whole `imu_sample_t` structs instead of bytes, and think through what has to change (hint: the size of each slot, and copying a whole struct at a time).
- Challenge: add a `dropped` counter that `rb_push()` increments every time it rejects a value, then ask yourself who owns this counter — the writer or the reader?

Next lesson, moving into module 2: [lesson 2.1, the toolchain and your first build](../../m02-build-and-version/l01-toolchain-first-build/README.md)

## Reflect

- In work you've done before, which piece of data should drop the old value when full, and which must never be dropped at all?
- If a test passes on a computer every time, but the board's data is occasionally corrupted, what would you suspect first?

## References

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (a ring buffer and its _from_isr function)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [SDK: tesaiot-radar/radar_dsp.c (the snapshot's seqlock)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_dsp.c)
- [SDK: cm55/sensors/02_radar_presence.c (reading the snapshot from the display side)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c)
- [B3 — The IPC backbone: setup, deferred binding, snapshots (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b3__ipc__backbone.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
