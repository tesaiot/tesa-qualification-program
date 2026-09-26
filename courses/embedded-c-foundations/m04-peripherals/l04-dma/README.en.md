---
id: c-found.m04.l04
lang: en
title: {th: DMA, en: DMA}
summary: {th: ย้ายข้อมูลโดยไม่ใช้ CPU และรู้ข้อควรระวังเรื่องบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน, en: Move data without the CPU and know the pitfalls of buffers shared by DMA and the CPU.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l03]
objectives:
- {th: อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม, en: Explain how DMA offloads data movement from the CPU and when it is not worth it.}
- {th: ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ, en: 'Identify the risks of buffers shared by DMA and the CPU, such as caches and reading before the transfer completes.'}
develops:
- {skill: mcu.dma, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 51a2a7567e64aea4b3f49b96cfc3f39b89f58cb4818283040b275f81f1710852
---

## Objectives

By the end of this lesson, you will be able to

1. Explain how DMA offloads data movement from the CPU, and when it isn't worth using.
2. Identify the risks of buffers shared between DMA and the CPU, such as caches and reading before a transfer finishes.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). This lesson's lab is reading real code and settings from the SDK, because the SDK's example catalogue at this commit has no direct DMA example yet.

## Before you start

Two review questions from earlier lessons.

1. The ring buffer in lesson 1.3 had to write the data before advancing `head`. Why does this order matter when the writer is a different context?
2. What does a good ISR in lesson 4.1 do, and what does it hand off to a task?

## See it work first

Open [examples/10_dma_cache_sim.c](examples/10_dma_cache_sim.c). This simulation has a real memory area that "DMA" writes to, and a cache the CPU reads through — like a Cortex-M55 with a data cache. **Predict before you run it:** what value will the line `frame 2, stale cache:` print?

```sh
gcc -std=c11 -Wall -Wextra -o dma_cache_sim examples/10_dma_cache_sim.c
./dma_cache_sim
```

DMA has finished writing `BB`, but the CPU still sees `AA`, because it's reading from its cached copy until that copy is invalidated. And the line `frame 3, read too early:` shows a different bug: the CPU reads while DMA is only halfway through writing, getting half `CC` and half `BB`. Neither bug crashes the program — they just quietly hand back the wrong data.

## Concepts

### 1. How DMA does work for the CPU, and when it isn't worth it

**DMA (Direct Memory Access)** is hardware that moves data between a peripheral's registers and memory, or between two memory locations, without the CPU copying it byte by byte. The CPU sets up a **descriptor** once (source, destination, the size of each chunk, how many chunks, and the signal that triggers a move), then goes and does something else. DMA moves the data itself every time the peripheral signals a trigger, and reports with an interrupt when it's done. The PDL's documentation sums it up: "The DMA channel can be used in any project to transfer data without CPU intervention basing on a hardware trigger signal from another component." ([cy_dma.h @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_dma.h))

The PDL for this chip has two kinds of DMA driver: DataWire (`Cy_DMA_*` in `cy_dma.h`) and AXI DMAC (`Cy_AXIDMAC_*` in `cy_axidmac.h`). The setup order per the documentation is `Cy_DMA_Descriptor_Init()`, then `Cy_DMA_Channel_Init()`, then `Cy_DMA_Enable()` and `Cy_DMA_Channel_Enable()`, and the documentation warns "Even if a DMA channel is enabled, it is not operational until the DMA block is enabled."

Real DMA decisions found in the SDK itself:

| Job | What the SDK does | Why |
|---|---|---|
| Receiving a camera image line by line | DMA moves values from a GPIO port into a line buffer; then AXI DMAC moves lines together into a full image (the camera driver) | Data arrives faster than the CPU could take it byte-by-byte with interrupts |
| Reading and writing the radar's FIFO over SPI | Interrupt-driven `Cy_SCB_SPI_Transfer()` | The volume is small enough for the SPI's ISR to handle |
| Testing 8 bytes of SPI on a header | Bit-banged with `Cy_GPIO_Write()` (the Header I/O Test example on the Developer Hub) | Very short, occasional work — setting up DMA isn't worth it |

DMA is **not worth it** when the data is small enough that setting up a descriptor takes longer than just copying it, when the data needs to be processed byte-by-byte along the way anyway, when DMA channels are scarce and other peripherals need them more, and when the cost of managing the cache (next section) plus the added code complexity outweighs the CPU time saved.

### 2. The first risk: reading before DMA finishes writing

DMA and the CPU truly run at the same time. A buffer that DMA is currently writing must never be read by the CPU. The standard fix is **ping-pong**: two buffers, with DMA writing one while the CPU processes the other, swapping whenever DMA reports it's done. The SDK's camera driver does exactly this: the HREF signal's ISR sets DMA's destination to `line_buffer[row_buffer_flag]`, then flips `row_buffer_flag`; the VSYNC signal's ISR swaps the frame buffer and sets `*_frame_ready = true`, so whoever consumes the image knows it's ready ([mtb_dvp_camera_ov7675.c lines 627-670](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c#L627-L670)). If the CPU is slower than DMA, there needs to be a clear policy for which data gets dropped — and every drop (an overrun) needs to be **counted**, as this lesson's exercise does.

### 3. The second risk: the cache

Cortex-M55 has a data cache. The CPU reads and writes through its cached copy, while DMA reads and writes real memory, bypassing the cache. These two versions of the truth need to be reconciled by hand.

- **The CPU writes, then DMA reads** (such as a descriptor, or outgoing data) — **clean** it: write the cache's copy back to memory before telling DMA to start.
- **DMA writes, then the CPU reads** — **invalidate** it: throw away the cache's stale copy before reading, or you get an old value, as in the example above.
- Or, **place the buffer in memory that bypasses the cache**, and skip both steps entirely.

The SDK's camera driver uses all three approaches, with the reasoning written at every point.

```c
Cy_DMA_Descriptor_SetDstAddress(&CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0,
                                (uint8_t*)line_buffer[row_buffer_flag]);
#if defined (__DCACHE_PRESENT) && (__DCACHE_PRESENT != 0)
/* line_buffer is in .cy_sharedmem (non-cacheable) — no invalidate needed.
 * DMA descriptor is in cached .cy_socmem_data — clean IS needed. */
SCB_CleanDCache_by_Addr((uint32_t*)&CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0,
                        sizeof(CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0));
#endif
Cy_DMA_Channel_Enable(CYBSP_DMA_DVP_CAM_CONTROLLER_HW,
                      CYBSP_DMA_DVP_CAM_CONTROLLER_CHANNEL);

row_buffer_flag = !row_buffer_flag;
```

Source: [mtb_dvp_camera_ov7675.c lines 637-648](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c#L637-L648) (Apache-2.0, Copyright 2025 Infineon Technologies AG, adapted by the TESA team in tesaiot-pse84-devkit-sdk).

Five things worth noticing: the line buffer is placed with `__attribute__((section(".cy_sharedmem")))`, which the comment says bypasses the cache, so it needs no invalidation; the descriptor sits in cached memory, so it needs `SCB_CleanDCache_by_Addr()` (a CMSIS-Core function the PDL uses) every time the CPU changes it, before enabling the channel; the clean call is wrapped in `#if defined (__DCACHE_PRESENT)`, so the same code works on cores with and without a data cache; the PDL's `cy_dma.h` documentation states the same principle for chips with a CM7 core ("D cache needs to be cleaned before DMA transfer and should be invalidated after DMA transfer"); and the cache operates in lines (the PDL documentation cites 32 bytes for CM7), so a DMA buffer should be aligned to, and a full multiple of, a cache line, so that cleaning or invalidating it doesn't touch a neighbouring variable.

## Worked example

[examples/10_dma_cache_sim.c](examples/10_dma_cache_sim.c) runs in three parts.

- **Part 1**: DMA fills the buffer completely; the CPU's first read, with an empty cache, gets the real value.
- **Part 2**: DMA fills it a second time; the CPU reads without invalidating and gets the stale copy, then invalidates and reads again, getting the real value.
- **Part 3**: invalidation is done correctly, but the read happens too soon, getting half old and half new data, until it waits for DMA to finish.

Try changing things and predicting the result before you run it.

1. Remove the first line, `cache_invalidate(&b);`, from part 3. What does the `read too early` line show now, and how does having two bugs overlapping make diagnosis harder?
2. Make `cpu_read()` bypass the cache entirely (as if the buffer were placed in non-cacheable memory). Which bug disappears, and which one remains?
3. Add a `cpu_write()` function and a `cache_clean()` function, and simulate the case where the CPU prepares data for DMA to send out but forgets to clean it.

## Practice

Open [practice/10_ping_pong.c](practice/10_ping_pong.c). There are 6 gaps to fill in — the most in this module, since this is the module's closing lesson. The ping-pong manager must never let DMA overwrite a buffer the CPU is still using, must count overruns when the CPU falls behind, and must invalidate before handing a buffer back to the CPU to read.

```sh
gcc -std=c11 -Wall -Wextra -o ping_pong practice/10_ping_pong.c && ./ping_pong
```

The test deliberately has the CPU read the first buffer once before starting, so the cache holds a stale copy already. If you forget to invalidate, the test that expects to read `0x11` will fail.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/10_ping_pong.c](solution/10_ping_pong.c). We tried removing the invalidate line from the solution and ran the tests: `FAIL ... expected 17 got 0` — proof the test genuinely catches a cache bug. The comments in the solution note two real options on the board: invalidate with a CMSIS-Core function sized to the buffer, or place the buffer in non-cacheable memory, as the camera driver does.

## Check your understanding

Answer the 4 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering both objectives. Getting 3 or more right counts as finishing the lesson.

## Lab

**Task:** read the SDK's real DMA settings in its BSP and camera driver, and answer with evidence how the data actually flows.

1. Open the BSP's [cycfg_dmas.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.c) (or open the template's `design.modus` in ModusToolbox's Device Configurator), and note the values of the `CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0_config` descriptor: `dataSize`, `descriptorType`, `xCount`, `yCount`, `triggerInType`, `interruptType`.
2. Calculate how many elements one descriptor moves, and how many bytes per round, and explain what `CY_DMA_1ELEMENT` in `triggerInType` means for how much one trigger moves. (The meaning of these enum values is in [`cy_dma.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_dma.h).)
3. In [cycfg_dmas.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.h), find which DMA block and channel number the camera's channel uses, and what its IRQ is named. What other channels has the BSP set up?
4. In the camera driver, find every line that calls `SCB_CleanDCache_by_Addr()`, and write a table of what each one cleans and why the data buffer itself doesn't need invalidating.
5. Answer a design question: if `line_buffer` were moved into ordinary, cacheable RAM, what would need to be added to the code, and where? How would you know if you forgot (what symptom would show up in the image)?

**Evidence to keep in your portfolio:** a table of the descriptor's settings with your calculations, a table of every clean point, and your answer to question 5. (This course does not ask you to run the camera driver on the board, and has not confirmed that the template built with default settings even compiles this driver in — this lesson uses it purely as code to read.)

## Going further

- Read the header of [`cy_axidmac.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_axidmac.h) and compare it with DataWire DMA — how do they differ, and what does the camera driver use each one for?
- Challenge: extend the exercise to three buffers (triple buffering), and see whether the number of overruns in the same scenario drops — and at what memory cost.
- A link to the next module: UART, I2C and SPI in module 5 can all use DMA when data volumes are high. Try finding which SPI the BSP sets up `CYBSP_DMA_TX_SPI_CONTROLLER` for.

Next lesson, moving into module 5: [lesson 5.1, UART](../../m05-serial-buses/l01-uart/README.md)

## Reflect

- A cache bug doesn't show up on the computer you test on — only on a chip with a data cache. What kind of test or checklist would you write to catch this before it reaches a user?
- Which job in your own project has the CPU copying data byte by byte, and how much CPU time would you get back by moving it to DMA?

## References

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [SDK: the camera driver mtb_dvp_camera_ov7675.c (DMA, AXI DMAC, cache cleaning and ping-pong)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c)
- [SDK: the BSP's cycfg_dmas.c (descriptor and channel settings)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.c)
- [Direct memory access (Wikipedia)](https://en.wikipedia.org/wiki/Direct_memory_access)
