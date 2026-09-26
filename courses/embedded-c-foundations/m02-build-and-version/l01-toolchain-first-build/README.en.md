---
id: c-found.m02.l01
lang: en
title: {th: ชุดเครื่องมือและการ build ครั้งแรก, en: The toolchain and a first build}
summary: {th: ติดตั้ง ModusToolbox ตรวจความพร้อม ดึง dependency แล้ว build และแฟลชแม่แบบเฟิร์มแวร์ของ SDK, en: 'Install ModusToolbox, check readiness, fetch dependencies, then build and flash the SDK firmware template.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l03]
objectives:
- {th: รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ, en: 'Run the readiness check, fetch every project''s dependencies, build and flash the firmware template.'}
- {th: 'อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้', en: 'Explain what CM33_S, CM33_NS and CM55 each run in this template.'}
- {th: บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้, en: Record the tool versions and SDK commit used so others can reproduce the build.}
develops:
- {skill: build.vendor-sdk, to: 3}
- {skill: build.compilers, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 7809f5cab5b79b74422894b95e4be4e21b7db825d9a2ac12a557cbf03016a192
---

## Objectives

By the end of this lesson, you will be able to

1. Run the readiness check, fetch every project's dependencies, and successfully build and flash the firmware template.
2. Explain what the CM33_S, CM33_NS and CM55 cores each run in this template.
3. Record the tool versions and the SDK commit used to build, so others can reproduce it.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5), not counting the roughly 1.9 GB of dependencies to download, which depends on your internet speed. It's a good idea to start the download at the beginning of the lesson and read the concepts section while you wait.

## Before you start

Two review questions from module 1.

1. Where does the initial value of a `.data` variable live before the board is powered on, and who copies it into RAM?
2. The board's external flash splits its space between separate images for CM33 secure, CM33 non-secure and CM55 (see the header of `10_littlefs_basics.c`, which you read in lesson 1.2). Why do you think it needs three separate images?

What you need:

- **ModusToolbox™ 3.6** (the SDK's README pins this exact version), with the Arm GCC 14.2.1 that comes with it.
- **Git** and **bash 4 or later** (on macOS, install a newer bash via Homebrew, per the SDK's README).
- About **4 GB** of free space, and the TESAIoT Dev Kit board with a USB-C cable connected to KitProg3.

## See it work first

The template you'll build comes as a zip file from an SDK release, not from `git clone`, because the public repository at commit `ef72c1b` does not store the six prebuilt libraries (`.a` files — the repository's top-level `.gitignore` excludes `*.a`). Those libraries come bundled in the zip. This course uses release `fw-c-only-v1.10.0`, which we've verified matches commit `ef72c1b` byte-for-byte in every file this lesson references (checked with `cmp` on 2026-09-26).

Download these three files from the [fw-c-only-v1.10.0 release page](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/releases/tag/fw-c-only-v1.10.0) into an empty folder to use as your workspace: `bento-firmware-template-mtb-only.zip`, `SHA256SUMS.txt` and `manifest.json`, then run

```sh
shasum -a 256 -c SHA256SUMS.txt       # on Linux, sha256sum -c also works (a .hex file you didn't download will show "not found" — that's fine)
unzip bento-firmware-template-mtb-only.zip
cd bento-firmware-template-mtb-only
./setup.sh --check
```

**Predict before you run it:** which lines will show `FAIL` or `warn` on a fresh machine that has never used this SDK before? Most will see `variant: mtb-only`, a compiler line, and `mtb_shared not found`, followed by a size of about 1.9 GB. This script deliberately prints every command it's about to run first, so you can follow along by hand if you don't have the script. If the compiler line doesn't pass, fix your PATH per the SDK's README before continuing.

If you want to read the full source and documentation, clone the repository separately and `git checkout ef72c1b658178eee8c38b1e47d28b006f80a59b5` — but don't build from that clone, since it won't have the prebuilt libraries to link against.

## Concepts

### 1. This template is three projects, on three cores

| Project | Core | What it runs (mtb-only variant) |
|---|---|---|
| `proj_cm33_s` | Cortex-M33, secure side | Secure boot and setting up TrustZone protection. The template's README says "you will not touch this" |
| `proj_cm33_ns` | Cortex-M33, non-secure side | FreeRTOS, WiFi, sensors on the I2C bus, cloud connectivity, and it owns the board's one UART console |
| `proj_cm55` | Cortex-M55 (has the NPU) | The LVGL display and every UI screen, Edge AI, radar |

Per Infineon's README for the hello-world example for this chip, the boot order is an extended boot: the CM33 secure project launches from a fixed location in external flash, CM33 secure sets up protection and launches CM33 non-secure, and CM33 non-secure is the one that starts CM55. All three images are written to external QSPI flash and run from there execute-in-place. The build produces a single file, `build/app_combined.hex`, which combines all three.

The two cores of our work talk to each other through an IPC mailbox. The six prebuilt libraries are also split by core: three for CM55 are hard-float, and three for CM33_NS are soft-float. The SDK's documentation says that linking across cores fails right at the link step, "which is the good outcome." One thing to remember that matters for later lessons: **CM55 has no console.** `printf` on CM55 goes nowhere (Appendix X #1) — every message from the board goes out through CM33_NS.

### 2. Dependencies are fetched separately per project, and must be patched before building

ModusToolbox tracks the libraries each project declares in its `deps/*.mtb` files, and `make getlibs` fetches them into an `mtb_shared` folder next to the template ([the template's README, section 2](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)). This template has **no top-level getlibs** — it must be run in all three projects. Running it only in `proj_cm33_ns` gets you 33 of 41 assets, and the build later stops in ninja because it can't find optiga-trust-m's files.

After fetching, you must apply the SDK team's patches to `mtb_shared`, in the order listed in `third_party_patches/series`, using `patch -F0`, then verify the result with SHA-256 ([third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)). That README explains why `-F0` isn't optional: GNU patch's default behaviour tolerates a mismatched context and still reports success, and ten of the eleven patches "fail silently" when missing — for example, mTLS silently falls back to a software key and the broker rejects the device. The exit status tells you the patch landed somewhere; the digest tells you it landed in the right place.

### 3. A reproducible build starts from a pinned version

The SDK's README pins ModusToolbox at 3.6, with the reasoning that a newer Configurator regenerates the BSP settings from `design.modus` and then issues a notice that turns `-Werror=cpp` into an error in a file you never touched. A newer version is therefore not automatically better. This course cites the SDK at commit `ef72c1b` in every link, for the same reason: a file that exists at one commit can change or disappear at the next one — and note that "the source you read" (a git commit) and "the package you build" (a release zip) are two separate things. Always record both.

A reproducible build needs to answer three questions: which tool versions were used, which source commit, and what was changed but not yet committed — plus evidence of what it produced, such as the size and SHA-256 of `app_combined.hex`. The SDK's README follows the same rule for the files it distributes: every release ships a prebuilt hex, meant to be checked with SHA-256 against that same release's `SHA256SUMS.txt`.

## Worked example

The full sequence from the zip to a working board, run inside the `bento-firmware-template-mtb-only` folder. Each step matches the SDK documentation's chapter A1 ([A1 — From the zip to your first program](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)).

**Step 1: check what you received, and check your machine** (inside the folder extracted from the zip)

```sh
(cd lib && ./verify.sh)      # signature and digest of every prebuilt library, must end with exit 0
./bento.sh doctor            # the toolchain and anything the template doesn't bundle
```

If `verify.sh` fails, stop — the package you received isn't the one that was signed (SDK documentation, chapter A1), or you're running inside a git clone that has no `.a` files.

**Step 2: fetch dependencies per project, then patch and prove they landed correctly**

```sh
for p in proj_cm33_s proj_cm33_ns proj_cm55; do (cd $p && make getlibs); done

(cd ../mtb_shared \
 && for p in $(cat ../bento-firmware-template-mtb-only/third_party_patches/series); do
        patch -p1 -F0 --forward < "../bento-firmware-template-mtb-only/third_party_patches/$p" || exit 1
    done \
 && shasum -a 256 -c ../bento-firmware-template-mtb-only/third_party_patches/PATCHED.sha256)
```

On Linux, if you don't have `shasum`, use `sha256sum -c` instead. Every line of verification must show `OK`.

**Step 3: build, flash, and look for evidence the board is running**

```sh
make build -j                # the first build of all three cores takes about ten minutes
make program                 # writes through KitProg3
```

Then **unplug the USB cable all the way, wait a moment, and plug it back in**. Open a serial console at 115200 8N1 before plugging it in. On this variant, a successful boot prints almost nothing — the only evidence is the line `[HB] t=...s tasks=...` every ten seconds, and the version tag on the Home screen ending in `-mtb_only`.

Traps the SDK documentation has collected (Appendix X) that you'll run into on day one:

- **#21, a black screen after flashing.** Resetting through the debugger leaves the display off, which looks like a failed flash even though it isn't. Unplug and replug every time.
- **#22 (mtb-only).** The display sometimes needs a second unplug-replug on a cold boot. If `[HB]` is running but the screen is black, try once more before concluding anything.
- **#16, never attach a debugger to an mtb-only board that's already running.** It leaves CM33 stuck in the boot ROM's loop. We'll come back to this in lesson 3.1.
- The SDK's README warns: **never call openocd directly** with `-f target/cat1d.cfg`. The SDK team tried it and got `wrote 0 bytes` followed by a checksum mismatch, which corrupted the firmware that was running. Use `make program` only.

## Practice

This lesson practices with tools, not code. Answer these by reading from your own machine and from files in the SDK, not from memory.

1. What does `./setup.sh --check` verify, and what does it **not** verify (look at the [setup.sh](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/setup.sh) file — does it touch the patches at all)?
2. After getlibs, how many top-level folders do you count in `../mtb_shared`?
3. How many patch files are listed in `third_party_patches/series`, and which one does the README say is the only one that stops the build?
4. Open [resources/build-record.md](resources/build-record.md) and fill in the "machine and tools" and "source built" sections completely.

## Solution

Try it yourself for at least 15 minutes first.

1. As of this commit, `setup.sh` checks the variant, `arm-none-eabi-gcc` on the PATH, `make`, and `mtb_shared` (plus the MicroPython port, for the mtb-mpy variant). Its normal mode runs getlibs across all three projects, and `--build` continues on to build — but it **does not apply patches**. Patching is your responsibility, and skipping it gets the build rejected by the `verify_asset_patches.sh` checker, which names the missing file.
2. The number depends on your fetch. What matters is that getlibs finishes in all three projects without error. If you get fewer than a classmate, check whether you ran it in all three projects.
3. Count from the `series` file on your machine. That folder's README states "Only `secure-sockets/0002` stops a build" — the rest fail silently.
4. Compare with one classmate. Whichever fields differ are what might make your build results differ too.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** build and flash the mtb-only template for the first time, and write a build record a classmate can reproduce.

1. Follow the three steps in the worked example section until you see at least two `[HB]` lines.
2. Check that the `t=` number increases by 10 each time, and that the task count is stable once booting finishes (it will rise for a moment as various tasks are created).
3. Fill in every field of [resources/build-record.md](resources/build-record.md), including the SHA-256 of `build/app_combined.hex`.
4. Have a classmate build from your record on their machine, then compare SHA-256 values. If they don't match, find out where they diverge before deciding what's wrong (a build across different machines can produce different bytes for reasons like embedded timestamps or paths — if that happens, write down what you found; that's a valuable result on its own).

**Evidence to keep in your portfolio:** the getlibs log and the patch verification log (the `OK` lines), the `[HB]` lines from the console, a screenshot of the Home screen showing the version tag, and the completed build record file.

## Going further

- Open [A0 — What you can build, and where each piece lives](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html) and check which prebuilt library links into which core — does it match the table in concept 1?
- Compare with Infineon's [mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0), which has the same three-project structure but is much smaller. That example says it was tested with ModusToolbox 3.7, while the SDK's template is pinned at 3.6 — if you needed both on one machine, how would you manage the version difference?
- An overview of building and flashing a different way, using the Developer Hub's master template, is in [TESAIoT Firmware Stack, lesson 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md).

Next lesson: [lesson 2.2, Make and build flags](../l02-make-and-build-flags/README.md)

## Reflect

- Which step today would have cost you the most time if no one had told you about it first, and how would you write it down in a team notebook?
- How is "the build succeeded" different from "the board is running", and what evidence did you use today to decide the board was running?

## References

- [SDK: the mtb-only template README (first run, CLI, three cores)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: the repository's main README (tool versions and prebuilt firmware)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [SDK: third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)
- [A0 — What you can build, and where each piece lives (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html)
- [A1 — From the zip to your first program (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)
- [Appendix X — Traps and anti-patterns (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [Infineon ModusToolbox software (GitHub)](https://github.com/Infineon/modustoolbox-software)
- [Infineon mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open an example on the Developer Hub to read the code, download it, or flash a prebuilt firmware image.

- Related lesson: [TESAIoT Firmware Stack 1.1 · Tools, the board and the master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
