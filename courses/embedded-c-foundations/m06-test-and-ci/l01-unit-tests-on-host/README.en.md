---
id: c-found.m06.l01
lang: en
title: {th: Unit test บนเครื่องโฮสต์, en: Unit tests on the host}
summary: {th: แยกตรรกะออกจากฮาร์ดแวร์เพื่อทดสอบบนเครื่องโฮสต์ด้วย Unity, en: Separate logic from hardware to test it on the host with Unity.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l03]
objectives:
- {th: แยกฟังก์ชันตรรกะ เช่น ฟิลเตอร์หรือ state machine ออกจากโค้ดที่แตะฮาร์ดแวร์ เพื่อให้คอมไพล์บนเครื่องโฮสต์ได้, en: Split logic such as a filter or state machine from hardware-touching code so it compiles on the host.}
- {th: เขียน unit test ด้วย Unity ครอบคลุมกรณีปกติ กรณีขอบ และกรณีผิดพลาด, en: 'Write Unity tests covering normal, edge and error cases.'}
- {th: พิสูจน์ว่า test ล้มเหลวได้จริงโดยจงใจใส่บั๊กหนึ่งจุด ก่อนเชื่อผลที่ผ่าน, en: Prove a test can fail by planting a bug before trusting a pass.}
develops:
- {skill: test.unit-tdd, to: 3}
- {skill: prog.state-machines, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 1ffa44b7604fb34f2a809f2da728d6cce87e5d69d77a3b26dd3ea27ae5bb2ffe
---

## Objectives

By the end of this lesson, you will be able to

1. Split a logic function — such as a filter or a state machine — from hardware-touching code, so it compiles on the host.
2. Write Unity tests covering normal, edge, and error cases.
3. Prove a test can genuinely fail, by planting one bug deliberately, before trusting a passing result.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). The whole lesson runs on your computer; you need gcc or clang, make, git and python3.

## Before you start

Two review questions from earlier modules.

1. Throughout this course, every exercise file starts red before you fill it in, and some tests already pass before anything is filled in (lessons 2.2, 3.2, 4.1 and 5.3). What can that kind of test prove, and what can't it?
2. The UART and SPI decoders in module 5 run on a computer even though they're about hardware — why is that possible?

## See it work first

Fetch Unity v2.7.0 into this lesson's `examples` folder (the folder's [.gitignore](examples/.gitignore) keeps it from being committed), then run the first two tests.

```sh
cd examples
git clone --depth 1 --branch v2.7.0 https://github.com/ThrowTheSwitch/Unity.git unity
make test
```

**Predict before you run it:** how many tests will there be, and what will the result say? The result is `2 Tests 0 Failures 0 Ignored` and `OK`, even though [examples/level_alarm.c](examples/level_alarm.c) is a state machine meant for the board, with no board connected at all. Now run one more command:

```sh
bash prove_red.sh test_level_alarm_first.c unity/src
```

This script plants four bugs into `level_alarm.c`, one at a time, in a temporary folder, then runs the same tests. The result: three of the four bugs `SURVIVED`. The two tests that pass check far less than that `OK` makes it feel like. This lesson is about getting all four caught.

## Concepts

### 1. The seam between logic and hardware

Firmware code has two parts that should stay separate: the part that **decides** (a state machine, a filter, protocol decoding, a calculation) and the part that **touches hardware** (calling the PDL, reading registers, waiting on an interrupt). If the decision-making part calls `Cy_GPIO_Read()` directly, it can't compile on a computer, and it can only be tested with a board attached. A **seam** is the point where we cut these two parts apart.

The SDK has a real host test that uses exactly this kind of seam. [test_arduino_shield.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/test_arduino_shield.c#L17-L50) tests the capability table for the header on a real QWA309, by supplying a "Stub physical layer" in place of the functions that call hardware, through the `arduino_ops_t` struct. The [test's Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/Makefile) explains why that table "is the piece most likely to be wrong and most expensive to debug on a bench, and it is portable C precisely so it can be checked here." The joystick decoder `f310_parse()` has its own host test too, buildable with a single gcc command ([test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c)).

This lesson's example follows the same pattern. [level_alarm.h](examples/level_alarm.h) reads a value through a `level_sensor_t` holding a `read_mv` function pointer. On a computer, the test supplies a fake that returns values from a table; on the board, we supply a real one — such as this draft, which reads a potentiometer with `potentiometer_read_voltage()` from the SDK's [sensor_potentiometer.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_potentiometer.h#L18-L28) (this draft illustrates the pattern; this course hasn't tested it on the board — `potentiometer_init()` must be called first, and the header notes the driver is "Only compiled when BSP_HAS_POTENTIOMETER=1"):

```c
static int pot_read_mv(void *ctx, int32_t *out_mv)
{
    (void)ctx;
    float v = 0.0f;
    if (!potentiometer_read_voltage(&v)) {   /* SDK's sensor_potentiometer.h: bool potentiometer_read_voltage(float *voltage) */
        return -1;
    }
    *out_mv = (int32_t)(v * 1000.0f);
    return 0;
}
static const level_sensor_t k_pot = {pot_read_mv, NULL};
```

### 2. Unity and three kinds of case

[Unity](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0) is a small C unit test framework — three files in `src/` that work on both a computer and a microcontroller. The layout of one test file:

| Part | What it does |
|---|---|
| `setUp()` / `tearDown()` | Called before and after every test, to reset state to a clean slate. The `unity.h` header notes that if you use Unity directly, "these will need to be provided for each test executable" |
| `static void test_...(void)` | One test, using assertions such as `TEST_ASSERT_EQUAL_INT(expected, actual)`, `TEST_ASSERT_TRUE(cond)`, `TEST_ASSERT_EQUAL_HEX8(e, a)` |
| `main()` | `UNITY_BEGIN();`, followed by `RUN_TEST(test_...)` for each test, then `return UNITY_END();`, which returns the number of failed tests as the program's exit code |

A good set of tests covers three kinds of case.

- **Normal cases:** what happens most often, such as a value below the threshold, which must never alarm.
- **Edge cases:** values right on the line — exactly at the threshold, one missed reading short, the hysteresis band, a counter wrapping around. Most bugs live here.
- **Error cases:** the sensor fails to read, the input is NULL, storage is full. The system must tell the truth (lesson 3.2), and the test must confirm that it does.

### 3. A test that cannot fail is a test that tests nothing

A passing test can only say "this test didn't find the fault it was looking for." If a test isn't looking for something, it always passes. The way to prove otherwise is to **deliberately plant a bug** (a mutation) and see whether the test fails. If the bug survives, there's behaviour no test is watching. A small routine you can do every time:

1. Write a test that fails first (red) — for example, calling a function that doesn't exist yet, or expecting a value the code doesn't yet return.
2. Write the code until it passes (green), then clean it up (refactor). This is the small TDD loop.
3. Before trusting that it's done, plant one bug this test is supposed to catch, confirm it fails, then remove the bug.

The SDK follows the same principle with its own tooling. The example catalogue explains that its API coverage checker measures coverage from a real object file's symbol table, not by searching text, because "A mention in a comment produces no symbol and therefore no coverage" — so the checker genuinely fails when a new API has no example ([the catalogue's README, section 6](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)).

## Worked example

The [examples/](examples/) folder has five files that work together.

- [level_alarm.h](examples/level_alarm.h) and [level_alarm.c](examples/level_alarm.c): a level-alarm state machine with three states — NORMAL, ACTIVE, FAULT. It requires seeing values over the threshold for `confirm` consecutive readings before changing state, with hysteresis between `on_mv` and `off_mv`.
- [test_level_alarm_first.c](examples/test_level_alarm_first.c): two Unity tests, in three parts. **Part 1**: a normal case. **Part 2**: an error case. **Part 3**: `main()`, returning the number of failed tests.
- [Makefile](examples/Makefile): builds and runs with `-Werror`, the same way the SDK's host tests do; the test file can be chosen with `TEST=`.
- [prove_red.sh](examples/prove_red.sh): plants four kinds of bug one at a time, and reports whether the tests caught it (`killed`) or not (`SURVIVED`).

Try changing things and predicting the result before you run it: change `>=` to `>` by hand in `level_alarm.c`, then run `make test`. Do the first two tests pass or fail, and why? (Then change it back.)

## Practice

Open [practice/test_level_alarm.c](practice/test_level_alarm.c). The first two tests are already there, and there are 4 gaps to fill in — each currently calls `TEST_FAIL_MESSAGE`, so they show red.

1. A value exactly equal to the threshold must count.
2. High values must be consecutive; one miss restarts the count.
3. Hysteresis must keep it ACTIVE for values between the two thresholds.
4. A failed read that recovers must return to NORMAL.

```sh
cd examples
make test TEST=../practice/test_level_alarm.c
bash prove_red.sh ../practice/test_level_alarm.c unity/src
```

The work is done once `make test` reports `6 Tests 0 Failures` **and** `prove_red.sh` shows `killed` on all four lines.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/test_level_alarm.c](solution/test_level_alarm.c). We checked the solution: it gets `6 Tests 0 Failures`, and `prove_red.sh` catches all four kinds of bug, while the first two tests alone caught only one. Notice the line in the hysteresis test that checks it's genuinely ACTIVE before starting the rest of the test — if that starting condition isn't true, the rest of the test passes or fails without proving anything.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** take one piece of logic from earlier work in this course, move it behind a seam, write Unity tests for it, and prove them with mutation.

1. Choose one: the debouncer from lesson 4.1, the watchdog supervisor from lesson 4.3, or the UART decoder from lesson 5.1. Move the logic function into its own `.c` and `.h` files, with no `#include` of the PDL or FreeRTOS.
2. Write at least five Unity tests: at least one normal case, at least two edge cases, at least one error case.
3. Write three kinds of bug you think are realistic for that code (use `prove_red.sh` as a model, or edit by hand one at a time), and record whether each was caught or survived. If one survives, add tests until it's caught.
4. If you have a board, write a real reader for that seam (for example, using `Cy_GPIO_Read()` for the debouncer), then build it into the SDK's template. The same logic file must work in both places, unchanged.

**Evidence to keep in your portfolio:** the logic file, the test file, the `make test` output, a table of the bugs planted and their results (killed or survived, before and after adding tests), and, if you did step 4, the log from the board.

## Going further

- Read the SDK's [test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c) test file in full, then sort its tests into normal, edge, and error. Which category has the fewest?
- The [Unity test framework](https://www.throwtheswitch.org/unity) documentation covers an automatic test-runner generator, and Ceedling, which bundles in mocking. Compare it against writing your own `main()`.

Next lesson: [lesson 6.2, CI for firmware](../l02-ci-for-firmware/README.md), which has a machine run these tests automatically on every change.

## Reflect

- Of the tests you've written before, how many have you actually seen fail, even once?
- Which part of your firmware do you think of as "impossible to test on a computer"? Try finding a piece of logic inside it that can be pulled out.

## References

- [ThrowTheSwitch Unity @ v2.7.0](https://github.com/ThrowTheSwitch/Unity/tree/v2.7.0)
- [Unity test framework](https://www.throwtheswitch.org/unity)
- [SDK: arduino_shield/test (a host test using a hardware stub)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/arduino_shield/test/test_arduino_shield.c)
- [SDK: usb_hid_joystick/tests/test_hid_f310_parser.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/usb_hid_joystick/tests/test_hid_f310_parser.c)
