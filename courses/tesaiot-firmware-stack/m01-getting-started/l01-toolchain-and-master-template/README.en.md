---
id: fw-stack.m01.l01
lang: en
title:
  th: "เครื่องมือ บอร์ด และ master template"
  en: "Toolchain, board and the master template"
summary:
  th: "ติดตั้ง ModusToolbox เตรียม master template ของ TESAIoT Firmware Stack แล้ว build และ flash ครั้งแรก"
  en: "Install ModusToolbox, set up the TESAIoT Firmware Stack master template, then build and flash for the first time"
level: L2
time_min: {concept: 15, lab: 45}
hardware: {emulator: false, boards: [devkit]}
prerequisites: []
objectives:
  - th: "ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error"
    en: "Install ModusToolbox, clone the master template and build it without errors"
  - th: "วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้"
    en: "Drop an episode into proj_cm55/apps/ and flash it through KitProg3"
  - th: "อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์"
    en: "Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip"
develops:
  - {skill: build.vendor-sdk, to: 2}
  - {skill: build.make-cmake, to: 2}
  - {skill: build.compilers, to: 1}
  - {skill: vcs.git, to: 1}
  - {skill: hw.architecture, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "README.md"
  ref: 082fd3e76595b62cfdb213499a093c233dbb4b53
source_sha256: 8270c925985367fe6d30893fcfdd93e82fa667c1862f66a92c6f9583d77844ec
---

# Toolchain, board and the master template

## Objectives

1. Install ModusToolbox, clone the master template and build it without errors
2. Drop an episode into proj_cm55/apps/ and flash it through KitProg3
3. Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip

## What you need

- **TESAIoT Dev Kit** (the PSoC Edge AI Kit SoM on the QWA309 base board) and a USB-C cable for KitProg3
- Infineon **ModusToolbox** 3.6 or later, as the master template README says (the episode series README recommends 3.8)
- **git** and a computer that can build C (Windows, macOS or Linux)

## Concepts

### Three projects on a dual-core chip

The PSoC Edge E84 is a dual-core chip (Arm Cortex-M55 + Cortex-M33), and ModusToolbox splits a single board's
firmware into **three projects**, each with its own `main.c`, built and flashed separately but coordinating at boot.

| Project | Core | Libraries in `deps/` | Role |
| --- | --- | --- | --- |
| `proj_cm33_s` | CM33 (secure) | none (just `assetlocks.json`) | Configures MPC/PPC so some memory and peripheral regions become non-secure, then jumps to the non-secure side's reset handler |
| `proj_cm33_ns` | CM33 (non-secure) | none (just `assetlocks.json`) | Starts the CM55 core at its boot address, then enters deep sleep forever |
| `proj_cm55` | CM55 | 15 packages — `lvgl`, `freertos`, `wifi-core-freertos-lwip-mbedtls`, 3 display drivers, 3 touch drivers, 4 sensor drivers | Runs the entire real application: the LVGL screen, the VGLite GPU, sensors, Wi-Fi, the microphone and the episode's code |

The `deps/` listing confirms what the master's README says: `proj_cm33_s` and `proj_cm33_ns` link no middleware at
all — their only job is to "wake up the next core". The display work, the Wi-Fi work and the sensor bus of
**every** episode (including the Wi-Fi manager in module 2) all live in `proj_cm55`. A project outside this series
may split the work differently, so always check the `deps/` folder and `main.c` of each project rather than
assuming.

The code excerpts in this section are copied from tesaiot/developer-hub (Apache-2.0) at commit `082fd3e`

`proj_cm33_ns/main.c` is very short, because it has exactly one job:

```c
/* Enable CM55. */
/* CM55_APP_BOOT_ADDR must be updated if CM55 memory layout is changed.*/
Cy_SysEnableCM55(MXCM55, CM55_APP_BOOT_ADDR, CM55_BOOT_WAIT_TIME_USEC);

/* Enable global interrupts */
__enable_irq();

/* Put the CPU to Deep Sleep */
for (;;)
{
    Cy_SysPm_CpuEnterDeepSleep(CY_SYSPM_WAIT_FOR_INTERRUPT);
}
```

`CM55_APP_BOOT_ADDR` is where the `proj_cm55` firmware sits in flash, and `CM55_BOOT_WAIT_TIME_USEC` (10
microseconds) is how long it waits for the CM55 core to boot before continuing. After that, `proj_cm33_ns` does
nothing else but sleep in deep sleep — all of the episode's work falls to `proj_cm55`.

### `proj_cm55`: the sequence that readies the system before our code runs

`main()` in `proj_cm55` creates a FreeRTOS task called `cm55_gfx_task` and starts the scheduler. That task runs, in
order: init the GFX subsystem (`Cy_GFXSS_Init`) → set up the Display Controller and GPU interrupts → init the
display/touch I2C bus → init the display for whichever panel is selected in `common.mk` → **init the sensor bus,
best-effort** → init memory and VGLite → `lv_init()` + `lv_port_disp_init()` + `lv_port_indev_init()`, and only then
call the episode's code as the final step:

```c
            /* Initialize LVGL library */
            lv_init();
            lv_port_disp_init();
            /* Initialize touch input for interactive UI controls. */
            lv_port_indev_init();

            /* ========================================================= *
             *   EPISODE ENTRY POINT — master template invariant          *
             * ========================================================= *
             *  main.c NEVER changes per episode. Whatever episode's code *
             *  currently lives in proj_cm55/apps/ provides a strong      *
             *  implementation of example_main(parent).                   *
             *                                                            *
             *  When apps/ is empty, the weak stub in                     *
             *  apps/_default/example_main_default.c takes over and       *
             *  shows instructions for downloading an episode.            *
             * ========================================================= */
            lv_obj_t *parent = lv_scr_act();
            example_main(parent);
```

`example_main(parent)` is called **exactly once**, after every subsystem is ready — `parent` is the active screen
(`lv_scr_act()`) that the episode uses as the starting point for its own object tree. The episode's code therefore
must not (and should not) call `lv_init()` or re-init the display/touch.

Sensor bus init is **best-effort**: on failure it `printf`s a warning and lets boot continue, it does not assert
and halt the whole system, because the master has no way to know in advance which sensors the episode that is
about to run will need:

```c
        /* Initialize dedicated sensor buses. Best-effort — episodes that do not
         * use sensors will simply ignore these handles. Master template always
         * initializes ALL subsystems so any episode dropped in apps/ Just Works. */
        cy_rslt_t sensor_i2c_rslt = sensor_i2c_controller_init();
        if (CY_RSLT_SUCCESS != sensor_i2c_rslt)
        {
            printf("[MASTER] Sensor I2C init failed (0x%08lx) — sensor episodes unavailable\r\n",
                   (unsigned long)sensor_i2c_rslt);
        }

        cy_rslt_t i3c_rslt = i3c_controller_init();
        if (CY_RSLT_SUCCESS != i3c_rslt)
        {
            printf("[MASTER] I3C init failed (0x%08lx) — BMM350 compass episodes unavailable\r\n",
                   (unsigned long)i3c_rslt);
        }
```

I2C serves DPS368 (pressure), SHT4x (temperature/humidity) and BMI270 (6-axis IMU); I3C serves only BMM350
(magnetometer/compass). If a module-3 episode cannot read any sensor at all from the start, check this log line
first.

### The contract between the master and an episode: `example_main` as weak/strong

`proj_cm55/apps/app_interface.h` declares the contract every episode must follow:

```c
#include "app_interface.h"

/* Episode MUST provide a strong definition: */
void example_main(lv_obj_t *parent);
```

The master has a **weak-symbol** `example_main()` in `apps/_default/example_main_default.c` as the default (it
draws the "no episode installed" card). Once we drop an episode's files that **declare `example_main()` as
strong** into `proj_cm55/apps/`, the linker automatically picks the episode's version instead — `main.c` calls
`example_main(parent)` exactly the same way every time, so the master's code never needs to change no matter how
many episodes you swap through. This is why item 2 says "never delete `app_interface.h`" — remove it and the
episode fails to compile, because there is no prototype left for it to match.

### The `apps/` folder and installing an episode

Every episode downloaded from the Developer Hub is designed so that **all** of its files go into the single
`proj_cm55/apps/` folder, with no `Makefile` edits needed, because the master's `INCLUDES` uses `find ./apps
-type d` to auto-discover whatever subfolders the episode creates. Two system files must always stay alongside it:
`app_interface.h` (the contract above) and `_default/` (the placeholder screen shown before an episode is
installed). The master's `tools/install_episode.sh` script automates three steps in one command: delete the old
episode's files (keeping the two system files), rsync the new episode's files in, and clear the `apps/` build
cache so the next build is clean.

### What `proj_cm55` has ready before an episode starts

By the time `example_main(parent)` is called, these subsystems are already usable without any init of your own —
LVGL 9 with its full widget set and Montserrat fonts sized 12–40, the VGLite GPU accelerating every draw call, a
touch controller (GT911/FT5406/ILI2511 depending on the display) already bound to LVGL, the I2C sensor bus (1.8V
domain) and I3C bus described above, a stereo PDM microphone, the WiFi Connection Manager (`cy_wcm`) with lwIP and
mbedTLS for TLS, FreeRTOS with tickless idle for power saving, and `printf()` going out the debug UART at 115200
baud.

## Common mistakes

- **Build hangs in `proj_cm33_s` with `schema cydesignfile_v7 not found`** — happens when someone opens
  `design.modus` with the Device Configurator from ModusToolbox 3.7 or later and saves over it, upgrading the
  original schema (v6) to v7, which a machine on ModusToolbox 3.6 cannot read. Never edit and save `design.modus`
  with a newer configurator.
- **`duplicate symbol example_main` at link time** — more than one file under `apps/**` declares `void
  example_main(lv_obj_t *parent)` as strong (for example, forgetting to delete the previous episode's files before
  dropping in a new one). Fix by deleting the duplicate file; a build can have only one strong `example_main`.
- **`multiple definition of APP_LOGO`** — some episodes ship their own `app_logo.c`/`app_logo.h` even though the
  master already provides `app_assets/app_logo.c`. Delete the episode's logo files and `#include "app_logo.h"` as
  usual.
- **Sensor I2C/I3C init fails silently** — a failure just `printf`s one warning line and boot continues; it does
  not assert and halt. If a sensor reads nothing at all from the start, open the serial log at 115200 baud and
  look for `[MASTER] Sensor I2C init failed` or `[MASTER] I3C init failed` before chasing other causes.

## Lab: build and flash for the first time

1. Clone the master template from the `tesaiot_dev_kit_master` branch of the Developer Hub

   ```sh
   git clone -b tesaiot_dev_kit_master https://github.com/tesaiot/developer-hub.git tesaiot_dev_kit_master
   cd tesaiot_dev_kit_master
   make getlibs
   ```


2. Build and flash following the steps in the [master template README](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md)

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

3. If you are not ready to build it yourself yet, open the example on the [Developer Hub](https://dev.tesaiot.dev/) and flash the ready-made firmware
   from the example page (every episode in modules 2–3 and every QWA309 practice code in module 4 has ready-to-use firmware)

## Check your understanding

- Where must an episode's files go, and which files in that folder must you never delete?
- In the master template, the display work and the Wi-Fi work both live in `proj_cm55`. So what does `proj_cm33_ns` do, and what would you gain and lose by moving the network work to the other core?
- `make build` succeeds but `make program` cannot find the board. What should you check first?

## References

- [Master template README (in Thai)](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md) · commit `082fd3e`
- [`proj_cm33_ns/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm33_ns/main.c) · [`proj_cm33_s/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm33_s/main.c) · [`proj_cm55/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm55/main.c)
- [`docs/EXTENDING.md`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/docs/EXTENDING.md) — the deep-dive guide for extending the master template, including the pitfalls cited in this lesson
- [TESAIoT Developer Hub](https://dev.tesaiot.dev/) · [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
- [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
