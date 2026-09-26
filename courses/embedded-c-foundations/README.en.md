# Embedded C Foundations on PSoC Edge

Level **L3** · status **alpha** · 6 modules, 17 lessons · about 30 hours

This course closes the largest gap in the catalogue: the core engineering skills the Embedded Systems Engineering Roadmap marks as required,
namely C, memory management, building, debugging, peripherals, basic buses and testing.
Every lesson points to real C examples in the [TESAIoT PSE84 Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0),
pinned at commit `ef72c1b`. Where the SDK has no example yet, the lesson says so and cites the chip vendor's documentation instead.

The lesson pages are Thai-first; English lesson pages are pending (`translation: pending`).

## Who it is for

- Developers who already write MicroPython or another language and want to move to C firmware
- Students who finished AIoT in Action or equivalent
- You need a TESAIoT Dev Kit (the SDK template at this commit targets KIT_PSE84_AI), ModusToolbox, and a logic analyzer for module 5
- Every example and practice file runs on a computer without a board; you need gcc or clang, make, git and python3. Each lesson's lab uses the board
- Firmware is built from the SDK's `fw-c-only-v1.10.0` release zip, not a git clone, because the git repository carries no prebuilt libraries (`*.a`); [lesson 2.1](m02-build-and-version/l01-toolchain-first-build/README.md) explains

## Outcomes

1. Write C that handles bits, registers and memory safely on a microcontroller, explaining where each piece of data lives.
2. Build, flash and version firmware reproducibly with ModusToolbox, Make and Git.
3. Debug firmware over SWD with GDB and diagnose faults from evidence rather than guesses.
4. Use GPIO, interrupts, timers, the watchdog and DMA correctly under ISR and RTOS rules.
5. Communicate over UART, I2C and SPI and verify the signals with a logic analyzer.
6. Separate logic from hardware to unit-test it on the host, and set up CI that checks every change.

## Modules and lessons

**Module 1 — C for microcontrollers and memory** ([m01-c-and-memory](m01-c-and-memory/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m01.l01 | C on a microcontroller | 70 min |
| c-found.m01.l02 | Memory map, stack and heap | 70 min |
| c-found.m01.l03 | Structs, pointers and ring buffers | 70 min |

**Module 2 — Building with ModusToolbox and Make, and Git for firmware** ([m02-build-and-version](m02-build-and-version/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m02.l01 | The toolchain and a first build | 70 min |
| c-found.m02.l02 | Make and build flags | 70 min |
| c-found.m02.l03 | Git for firmware work | 70 min |

**Module 3 — Debugging with SWD and GDB** ([m03-debugging](m03-debugging/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m03.l01 | SWD and GDB basics | 70 min |
| c-found.m03.l02 | Diagnosing faults from evidence | 70 min |

**Module 4 — Timers, interrupts, watchdog, DMA and clocks** ([m04-peripherals](m04-peripherals/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m04.l01 | GPIO and interrupts | 70 min |
| c-found.m04.l02 | Timers and clocks | 70 min |
| c-found.m04.l03 | The watchdog | 70 min |
| c-found.m04.l04 | DMA | 70 min |

**Module 5 — UART, I2C and SPI with a logic analyzer** ([m05-serial-buses](m05-serial-buses/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m05.l01 | UART | 70 min |
| c-found.m05.l02 | I2C | 70 min |
| c-found.m05.l03 | SPI | 70 min |

**Module 6 — Unit testing and CI** ([m06-test-and-ci](m06-test-and-ci/README.md))

| Lesson | Topic | Time |
|---|---|---|
| c-found.m06.l01 | Unit tests on the host | 70 min |
| c-found.m06.l02 | CI for firmware | 70 min |

## Status

The course is in alpha. All 17 lessons follow the same structure: goals, before you start, look at the real thing first, concepts, a complete example,
practice, solution, a comprehension check (each lesson's `quiz.yaml`), a lab and next steps.

- Every example and practice file was checked on a computer: each practice file fails its tests before it is filled in, and each solution passes.
  The exception is the GDB scripts of lesson 3.1, which can only be checked with a board attached
- The board labs are written from the SDK's code and documentation at commit `ef72c1b`, but have not yet been trialled on a real board.
  If a step does not match your board, report it as described in [CONTRIBUTING.md](../../CONTRIBUTING.md)
- Every SDK link is pinned to one commit and was checked to exist at that commit
- Every hardware and API fact is taken from the SDK source or from Infineon mtb-pdl-cat1 release-v3.24.0. Infineon examples are linked by repository and tag, not copied

## Main references

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [mtb-only firmware template: README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [The SDK's C example catalogue](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [A1 — From the zip to your first program (SDK documentation built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)

## Licence

- Content: CC BY 4.0
- This course's code (every lesson's `examples/`, `practice/` and `solution/` folders): Apache-2.0
- SDK code is not copied as files. Lessons quote short excerpts of at most 25 lines, each with a link to the file at commit `ef72c1b` and the credit (Apache-2.0, tesaiot-pse84-devkit-sdk)
- Infineon code is not copied; it stays under its own licence at the linked source
- Unity (MIT), used in module 6, is cloned by the learner at tag v2.7.0 and is not included in this repository

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Embedded C Foundations on PSoC Edge" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
