---
id: c-found.m02.l02
lang: en
title: {th: Make และตัวแปรของการ build, en: Make and build flags}
summary: {th: อ่าน Makefile เปิดปิดส่วนของเฟิร์มแวร์ด้วยตัวแปร และรันตัวอย่างของ SDK ทีละตัว, en: 'Read a Makefile, switch firmware parts with variables, and run SDK examples one at a time.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l01]
objectives:
- {th: เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย ENABLE_PAGE_EXAMPLES=1 และเลือกรันตัวอย่างฝั่ง CM33 ด้วย SDK_EXAMPLE_CM33 ได้, en: Enable the SDK example catalogue with ENABLE_PAGE_EXAMPLES=1 and select a CM33 example with SDK_EXAMPLE_CM33.}
- {th: 'อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ ?= กับ = และผลต่อการ build', en: 'Explain the difference between ?= and = assignments in Make and their effect on the build.'}
- {th: อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย, en: Explain why disabled examples add nothing to the firmware image.}
develops:
- {skill: build.make-cmake, to: 3}
- {skill: build.vendor-sdk, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 0ce83a4a87132c92158860716c81369e4cc3718cac40434a7016fa7fb9b45012
---

## Objectives

By the end of this lesson, you will be able to

1. Enable the SDK's example catalogue with `ENABLE_PAGE_EXAMPLES=1`, and select a CM33-side example to run with `SDK_EXAMPLE_CM33`.
2. Explain the difference between `?=` and `=` assignments in Make, and their effect on the build.
3. Explain why disabled examples add nothing to the firmware size at all.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). The concepts and practice sections only need GNU Make on your computer — nothing to compile.

## Before you start

Two review questions from lesson 2.1.

1. Why must `make getlibs` be run in all three projects, rather than once at the top-level folder?
2. Which line on the serial console is the evidence that an mtb-only board booted successfully?

## See it work first

Open [examples/flags.mk](examples/flags.mk). This file doesn't compile anything — it just prints how make understands each variable. **Predict before you run it:** how many files will the `SOURCES` line show in each case? Then run them one at a time.

```sh
make -f examples/flags.mk
make -f examples/flags.mk ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
ENABLE_PAGE_EXAMPLES=1 make -f examples/flags.mk
```

The first gives 2 files, the other two give 4, and make also tells you where each value came from (`file`, `command line`, `environment`). Notice two odd-looking lines: `FROZEN` ends up as just `hello ` even though `GREETING` is `hello world`, and `TRAILING` looks like it's 1 but shows `equals 1: no`. These two surprises are what this whole lesson is about.

## Concepts

### 1. The Makefile structure in the ModusToolbox template

The template has a two-layer Makefile. The top-level one ([Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/Makefile)) only says which projects this application has — `MTB_TYPE=APPLICATION` and `MTB_PROJECTS=proj_cm33_s proj_cm33_ns proj_cm55` — then includes ModusToolbox's build system. Each project's own Makefile, such as [proj_cm33_ns/Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile), is laid out like this:

| Section | Example from the file | What it does |
|---|---|---|
| Shared values | `include ../common.mk` | The variant, the workspace location |
| Name and core | `APPNAME=proj_cm33_ns` `CORE=CM33` | Tells ModusToolbox which core to build for |
| Components | `COMPONENTS+=FREERTOS RTOS_AWARE` | Enables the matching `COMPONENT_`-prefixed folders |
| Our own variables | `ENABLE_PAGE_EXAMPLES ?= 0` | A default the user can override |
| Passed to C | `DEFINES+=ENABLE_PAGE_EXAMPLES=$(ENABLE_PAGE_EXAMPLES)` | Becomes a `-D` the code can use with `#if` |
| Excluding a folder | `CY_IGNORE += examples` | Stops ModusToolbox from looking for source in that folder |
| Libraries | `LDLIBS += .../libbento_hsm.a` | Hands the `.a` file to the linker |
| At the very end | `include $(CY_TOOLS_DIR)/make/start.mk` (line 530) | The build system reads every variable above right here |

Order genuinely matters. The template's README troubleshooting table records the symptom "Linker cannot find a function from `lib/`" as being caused by `LDLIBS` set after `include start.mk`: "ModusToolbox reads it while including that file; anything later never reaches the linker."

### 2. Make variables: `=`, `:=`, `?=`, `+=`, and who wins

| Written as | Meaning | Expanded when |
|---|---|---|
| `A = x` | Recursive: stores the text, expands every time it's used | At use — a variable defined later still takes effect |
| `A := x` | Simple: expands immediately and stores the result | At that line |
| `A ?= x` | Assigns only when `A` is not already defined | A value from the environment counts as already defined |
| `A += x` | Appends to the existing value | Following `A`'s existing type |

A **command-line** value (`make build X=1`) beats every assignment inside a file. An **environment** value loses to `=` and `:=` in a file, but beats `?=`. That's why the SDK declares `ENABLE_PAGE_EXAMPLES ?= 0` and `SDK_EXAMPLE_CM33 ?=` (lines 321-322). If it were written `ENABLE_PAGE_EXAMPLES = 0`, the command `make build ENABLE_PAGE_EXAMPLES=1` would still work — but a value set in the build machine's environment would be silently swallowed.

Another thing worth knowing: `ifeq` is decided **the moment make reads that line.** A comment in the same file warns that `ENABLE_PAGE_BENTO_BUDDY` "must be assigned BEFORE the CY_IGNORE ifneq below evaluates it — otherwise the variable is empty at parse time" (lines 60-64). And `ifeq` compares text literally — a value of `1 ` with a trailing space is not equal to `1`. The SDK's documentation records this trap as Appendix X #23: a whole feature disappears with no error anywhere. `common.mk` guards against this by `$(strip)`-ing the value of `BENTO_VARIANT`, then deliberately failing the build with `$(error ...)` if the value isn't `mtb-mpy` or `mtb-only` (lines 80-89), because "a typo must not quietly select the wrong firmware."

### 3. Why disabled examples add nothing to the firmware size

ModusToolbox doesn't read a source list out of the Makefile — it **walks the whole project folder and compiles every file it finds.** A comment in CM33's Makefile explains the consequence.

```make
# Compiled ONLY with ENABLE_PAGE_EXAMPLES=1.
#
# MTB DISCOVERS SOURCES BY WALKING THE APP TREE. `SOURCES +=` adds; it does not
# subtract, and it cannot exclude a file the walk already found. Only CY_IGNORE
# removes one. Gating a subdirectory with `ifeq (...) SOURCES += wildcard`
# therefore does NOTHING — the files compile anyway, and the first symptom is a
# wall of "No such file or directory" for headers that subdirectory needs.
# Every exclusion below is a CY_IGNORE for that reason.
#
# sdk_examples_cm33_table.c is GENERATED by tools/gen_examples_table.py.
ifeq ($(ENABLE_PAGE_EXAMPLES),1)
INCLUDES += examples
# ... (lines 506-523: excludes a few groups even with examples enabled)
else
CY_IGNORE += examples
endif
```

Source: [proj_cm33_ns/Makefile lines 494-527](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile#L494-L527) (Apache-2.0, tesaiot-pse84-devkit-sdk); lines 506-523 trimmed for brevity.

When the flag is 0, the whole `examples` folder is `CY_IGNORE`d — the files in it never get compiled, so there are no object files, nothing at all for the linker to put in the image. There's a second layer in the C code itself: `main.c` calls `sdk_examples_cm33_start()` only inside `#if ENABLE_PAGE_EXAMPLES` (lines 384-388). If the flag were off but a stray call remained, the build would fail at the link step — which is better than getting an image with half-finished pieces in it. The catalogue's README sums it up: with the flag off, "not one byte of this tree reaches the firmware image."

## Worked example

[examples/flags.mk](examples/flags.mk) runs in four parts.

- **Part 1**: `?=` sets a default, then prints `$(origin ...)` to show whether the value came from the file, the command line, or the environment.
- **Part 2**: `GREETING = hello $(WHO)` and `FROZEN := hello $(WHO)` are both declared before `WHO` is set. The first expands at use, so it becomes `hello world`; the second expands immediately, so it becomes `hello `.
- **Part 3**: the `SOURCES` list changes with `ENABLE_PAGE_EXAMPLES`, and `DEFINES` passes both flags on to the C code.
- **Part 4**: `TRAILING`'s value has a trailing space because of a comment at the end of the `ifeq` line, so it isn't equal to 1 until it's `$(strip)`ped.

Try changing things and predicting the result before you run it.

1. Move the line `WHO = world` above `FROZEN := ...`. What does `FROZEN` become now?
2. Change `ENABLE_PAGE_EXAMPLES ?= 0` to `ENABLE_PAGE_EXAMPLES = 0`, then run all three cases again. Which one changes its result?
3. Run `make -f examples/flags.mk 'ENABLE_PAGE_EXAMPLES=1 '` (note the space inside the quotes). This file accepts it because of `$(strip)` — what would the real SDK Makefile's `ifeq ($(ENABLE_PAGE_EXAMPLES),1)` at line 504, which does not strip, do with the same value?

## Practice

Open [practice/feature.mk](practice/feature.mk). The task is to make `feature/feature.c` compile only when `ENABLE_FEATURE` is 1, off by default, overridable from either the command line or the environment, and tolerant of a trailing space. There are 2 gaps to fill in. Check your work with

```sh
make -f practice/feature.mk check
```

Before fixing anything, you'll see 2 `FAIL` lines, and `make` will end with an error, because `check` returns a non-zero status whenever even one line says `FAIL`. (A check that prints FAIL but returns 0 always looks green in CI — we'll come back to this in lesson 6.2.) Fix each TODO one at a time and run `check` after each one; you'll see which line flips from FAIL to PASS.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/feature.mk](solution/feature.mk). TODO 1 is changing `:=` to `?=`, and TODO 2 is starting `SOURCES` without `feature/feature.c`, then adding it with `+=` inside `ifeq ($(strip $(ENABLE_FEATURE)),1)`. Notice that the "command line turns it on" line passed even before you fixed anything, because a command-line value beats both `:=` and `?=`. A test that passes from the very start doesn't prove your code is right — it only proves that particular case doesn't separate a right answer from a wrong one. We'll come back to this in lesson 6.1.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** enable the example catalogue, choose one CM33-side example to run, and measure how much enabling examples changes the firmware size.

1. Build first with examples disabled (the default), then find CM33_NS's ELF file and measure the size of each section.
   ```sh
   make build -j
   find proj_cm33_ns/build -name "*.elf"
   arm-none-eabi-size <the .elf file you found>
   ```
   Note down the `text`, `data` and `bss` columns.
2. Build again with examples enabled, and none selected, then measure again.
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1
   ```
   Flash it with `make program`, unplug and replug the cable, then read the serial console. The runner will print a list starting `=== TESAIoT SDK examples on CM33_NS (...) ===`, and tell you how to run one with `SDK_EXAMPLE_CM33=<id>`. Note the shape of the ids it prints (for example, `cm33/io/04_gpio_led_button`).
3. Build again, this time picking one example, such as `SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan`, and watch for the line `[sdk-example] running ...` and the result line `[sdk-example] ... -> 0 (ok)` or another code.
4. Try a name that doesn't actually exist, such as the example under "Turning them on" in the [catalogue's README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md), which uses `tesaiot_hsm/01_acquire_chip`. What does the runner say? Compare it with the list the runner prints itself — which one is the truth for this commit?
5. Compare the sizes from step 1 and step 2. Which section holds the difference, and using concept 3, explain why there's no such difference when the flag is off.

**Evidence to keep in your portfolio:** both `arm-none-eabi-size` results, the example runner's log (the list, the result of the one you chose, and the result for the nonexistent name), and a short explanation for question 5.

## Going further

- The template's `./bento.sh menus` asks make for each flag one at a time instead of reading the Makefile by eye. The template's README explains why: some flags are set twice, once inside a board condition and once in the `else`, and reading the text by eye gets you the wrong answer. Try finding one such flag in `proj_cm55/Makefile` with `grep -n "ENABLE_PAGE_" proj_cm55/Makefile`.
- The [GNU Make](https://www.gnu.org/software/make/) documentation's "The Two Flavors of Variables" and "Overriding Variables" sections cover concept 2 in full.

Next lesson: [lesson 2.3, Git for firmware work](../l03-git-for-firmware/README.md)

## Reflect

- If a classmate said "I turned on ENABLE_PAGE_EXAMPLES but nothing changed," what would be the first three questions you'd ask them?
- Which kind of build flag should fail the build when its value is wrong, and which kind can quietly fall back to a default?

## References

- [SDK: the example catalogue (Turning them on, Which core)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [SDK: CM33 non-secure examples (how to run them)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: proj_cm33_ns/Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile)
- [SDK: sdk_examples_cm33_table.c (the list of CM33-side example ids at this commit)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sdk_examples_cm33_table.c)
- [GNU Make](https://www.gnu.org/software/make/)
