---
id: c-found.m03.l01
lang: en
title: {th: SWD และ GDB เบื้องต้น, en: SWD and GDB basics}
summary: {th: ต่อ debugger ผ่าน SWD ตั้ง breakpoint ดูค่า และเดินโปรแกรมทีละบรรทัด, en: 'Attach a debugger over SWD, set breakpoints, inspect values and step through code.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l03]
objectives:
- {th: เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้, en: Start a debug session over SWD and stop at a breakpoint in a given function.}
- {th: ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้, en: 'Use GDB to print variables, show a backtrace and step line by line.'}
- {th: อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์, en: Explain why halting at a breakpoint can change the behaviour of a timing-sensitive or multi-core system.}
develops:
- {skill: debug.jtag-swd, to: 3}
- {skill: debug.gdb, to: 3}
- {skill: debug.openocd, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: f491a26b762c2d85b4292a8aa3449fbe9bdb92b64610256a2ab06fd1d2ff0623
---

## Objectives

By the end of this lesson, you will be able to

1. Start a debug session on the board over SWD, and stop at a breakpoint in a given function.
2. Use GDB commands to inspect variables, view a backtrace, and step line by line.
3. Explain why halting at a breakpoint can change the behaviour of a timing-sensitive or multi-core system.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). Practice GDB on your computer first, then use it with the board.

## Before you start

Two review questions from modules 1 and 2.

1. The SDK's template sets `CONFIG=Release` in `common.mk` with an `=` sign. If you build with `make build CONFIG=Debug`, which value wins (lesson 2.2)?
2. If a loop `for (i = 0; i <= 8; i++)` writes into an 8-byte array inside a struct, where does the ninth byte land (lesson 1.3, on structs and padding)?

Additional things you need: GDB on your computer (installed separately, such as the `gdb` package on Linux, or `lldb` on macOS, whose commands differ slightly), and for the board, the Eclipse IDE for ModusToolbox™ that comes with ModusToolbox 3.6.

## See it work first

Open [examples/05_find_the_overrun.c](examples/05_find_the_overrun.c). **Predict before you run it:** what count will the `round 0` line print?

```sh
gcc -std=c11 -Wall -Wextra -g -O0 -o overrun examples/05_find_the_overrun.c
./overrun
```

The result is `round 0: count = 16 (expected 8)`. The program adds 8 to count each time, but something is overwriting count first. Reading the code line by line can find the answer, but a debugger answers faster and proves it, with a single command: "stop the instant anyone writes here."

## Concepts

### 1. The chain from GDB to the chip

```
GDB  <--TCP-->  OpenOCD (GDB server)  <--USB-->  KitProg3 on the board  <--SWD-->  the CPU in PSOC™ Edge
```

- **SWD (Serial Wire Debug)** is Arm's debug port, using two signal wires, SWDIO and SWCLK (plus ground). Over this wire, a debugger can halt the CPU, read and write memory and registers, and set the core's own hardware breakpoints and watchpoints.
- **KitProg3** is the debugger built into the board itself, connected through the same USB port used for flashing, which also carries the UART console.
- **OpenOCD** is the middle program that talks to KitProg3 and opens a port for GDB to connect to. ModusToolbox launches it for you when you start a debug session from the IDE.
- **GDB** is what you type commands into, or what the IDE drives behind the scenes.

The SDK's README warns clearly about one thing: **never call openocd directly with `-f target/cat1d.cfg`.** The SDK team tried it and got `wrote 0 bytes` followed by a checksum mismatch, because the image lives in external QSPI flash that ModusToolbox must configure first, and it corrupted the firmware that was running. Flash with `make program`, and start debugging through ModusToolbox's launch configuration.

### 2. GDB commands you'll use every day

| Command | What it does |
|---|---|
| `break fill_samples` or `break file.c:42` | Stop when execution reaches that function or line |
| `run` / `continue` (`c`) | Start / resume until the next breakpoint |
| `next` (`n`) / `step` (`s`) / `finish` | Advance a line, stepping over a function call / stepping into it / running until this function returns |
| `print x` (`p`), `print *ptr`, `print arr` | Show a value, follow a pointer, or view a whole struct or array |
| `info locals` / `info args` | Show every local variable and argument of the current frame |
| `bt` (backtrace) | See which functions led to this point |
| `watch -l expr` | Stop whenever anything writes to `expr`'s address (uses the core's hardware watchpoint) |
| `x/4xw addr` | View 4 words of memory in hexadecimal |

The watchpoint is the most powerful tool in this table. When a value is corrupted and you don't know who's writing it, don't chase it through the code by reading — let the hardware tell you. One thing to know when using this on the board: the SDK's template builds as **Release** by default (`common.mk` line 20). The compiler will keep variables in registers, eliminate some entirely, or reorder lines, so GDB may show `<optimized out>`, or `next` may skip past a line — that's not a broken debugger. If you need to see every variable, try building with `CONFIG=Debug` on the command line, which beats the `=` in `common.mk`, and note it in your build record. (This course has not yet confirmed on the board that this template's Debug build builds and boots completely — if it doesn't, keep debugging on Release.)

### 3. Halting the CPU does not halt the world

A breakpoint only halts the core being debugged. Everything around it keeps running: a button being pressed, data streaming into a UART, sensors, and the other core. A system that depends on timing behaves differently once halted — a button press that happens while halted can be missed entirely, bytes that arrive during that time overflow a buffer, and if a watchdog is enabled, halting for too long can reset the board mid-debug session (lesson 4.3).

On the PSOC™ Edge E84 this is even more visible because two cores are running. The SDK documentation's chapter G2 records that when CM33 is halted, the `[HB]` line stops immediately, but "the screen stays as it was (CM55 keeps running its last frame)" — the core that wasn't halted is still waiting for an answer over IPC from the one that was. And a comment in the SDK's [diag_blackbox.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/shared/include/diag_blackbox.h#L1-L22) notes that the openocd config this template uses "exposes no CM55 debug target" — in this template's toolset, we can debug CM33, but evidence from CM55 has to come from the counters and logs it writes for itself, which is the subject of lesson 3.2.

The most important trap in the mtb-only template is the SDK documentation's Appendix X #16: **attaching a debugger to a board that's already running leaves CM33 stuck in the boot ROM's loop** until power is cut. A comment in [proj_cm33_ns/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L292-L309) recounts spending hours blaming the firmware before this was understood, and chapter G2 recommends that if you need a debugger with this variant, "flash and halt-on-reset from a fresh programming session rather than attaching to a live board."

## Worked example

Practice on your computer with [examples/05_find_the_overrun.c](examples/05_find_the_overrun.c), which is written in three parts.

- **Part 1**: `fill_samples()` fills an 8-slot array through a loop that has one bug.
- **Part 2**: `main()` calls it three times, adding 8 to count each time.
- **Part 3**: prints the result against what it should be.

An interactive session on your computer (type each line after `(gdb)`):

```text
$ gdb -q ./overrun
(gdb) break fill_samples
(gdb) run
(gdb) info args
(gdb) print *r
(gdb) next
(gdb) print i
(gdb) watch -l r->count
(gdb) continue
(gdb) bt
(gdb) print i
(gdb) quit
```

After `continue`, GDB stops on the line inside `fill_samples`'s loop, showing the old and new value of `r->count`. `print i` gives 8, which tells you the write that overwrites count is `r->samples[8]` — a slot outside the array — and `bt` shows it came from `main`. Try changing `<=` to `<`, recompile, and run the whole program and this session again — does the watchpoint still trigger, and where?

## Practice

Open [practice/05_watch.gdb](practice/05_watch.gdb), a GDB script that automates the session above. There are 3 gaps to fill in (marked `____`): the function name to stop at, the variable to watch, and the command to view the call stack. Run it with

```sh
gdb -q -batch -x practice/05_watch.gdb ./overrun
```

The expected result is a stop at the watchpoint inside `fill_samples`'s loop, with `print i` giving 8.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/05_watch.gdb](solution/05_watch.gdb). The most common mistake is writing `watch r->count` without `-l`, which makes GDB watch it tied to `fill_samples`'s frame and delete the watchpoint once that function returns. `-l` computes the address once and watches that address instead, which is what you want when asking "who is writing to this piece of memory?"

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** halt CM33 in the SDK's GPIO example with a breakpoint, and watch the debounce variables while you press the button.

1. Build the template with the GPIO example selected. If you want to try Debug, add `CONFIG=Debug` and note it in your build record.
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
   ```
2. Open the template in the Eclipse IDE for ModusToolbox and start a debug session using the **Debug (KitProg3_MiniProg4)** launch configuration for the CM33 non-secure project from the Quick Panel (the full name depends on your project's name). This programs the board and starts from reset. **Never use the attach-to-a-running-board variant** (Appendix X #16).
3. Set a breakpoint at `example_io_gpio_led_button`, then resume. Once halted, type `bt` in the Debugger Console or check the Call Stack window. Note which functions called into it (you should see the SDK's example runner).
4. Use `next` to step past `leds_init()` and `button_init()` one line at a time, then set another breakpoint at the line `presses++;`. Press SW2 once. When it halts, look at the values of `stable`, `cand`, `agree` and `presses`.
5. While CM33 is halted, watch the serial console and the screen. Which lines stop, and what keeps moving? Note it down, then explain it using concept 3.
6. Remove all breakpoints, resume, and press the button five more times. Does the final `presses` count printed match how many times you pressed it? Compare with when breakpoints were still active.

**Evidence to keep in your portfolio:** a screenshot of the call stack when halted in step 3, a screenshot of the variables window in step 4, notes on what stopped versus what kept moving in step 5, and the count result in step 6. If GDB shows `<optimized out>`, note which variable it was and which build configuration you used.

## Going further

- The [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) manual's "Setting Watchpoints" section explains when a watchpoint becomes a hardware watchpoint, and how many can exist at once depending on the core. Try setting several on the board and see what GDB says once you exceed the limit.
- The [OpenOCD](https://openocd.org/doc/html/index.html) manual's "GDB and OpenOCD" section explains how GDB connects to OpenOCD. Useful for background, but for this board, always start through ModusToolbox, per the SDK's warning.
- Read the SDK documentation's chapter [G2 — The heartbeat: living without a REPL](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__g2__heartbeat.html) in full — the real story of a measurement tool that "is also the murder weapon."

Next lesson: [lesson 3.2, diagnosing faults from evidence](../l02-diagnosing-faults/README.md)

## Reflect

- What kind of bug do you think a debugger helps with the least, needing counters or logs instead?
- If a breakpoint makes a bug disappear (often called a heisenbug), what does that tell you about its cause?

## References

- [GDB documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)
- [OpenOCD User's Guide](https://openocd.org/doc/html/index.html)
- [SDK: the mtb-only template README (flashing through KitProg)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: the repository's main README (the warning about openocd)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [G2 — The heartbeat: living without a REPL (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__g2__heartbeat.html)
- [Appendix X — Traps and anti-patterns (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [Infineon mtb-example-psoc-edge-hello-world @ release-v2.1.0: using the code example (Debugging section)](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/blob/release-v2.1.0/docs/using_the_code_example.md)
