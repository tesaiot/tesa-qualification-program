---
id: fw-stack.m04.l04
lang: en
title:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
summary:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งเฟรม heartbeat 1 Hz ผ่าน CANFD0 แบบ Classic CAN 2.0A ที่ 500 kbps"
    en: "Send a 1 Hz heartbeat on CANFD0 as Classic CAN 2.0A at 500 kbps"
  - th: "อ่านเฟรมที่เข้ามา แสดงเฟรมล่าสุด (ID และข้อมูล) และตัวนับเฟรมที่รับและส่ง"
    en: "Receive frames and show the latest frame (ID and data) with the receive and transmit counters"
develops:
  - {skill: proto.can, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_can_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 1fea8ca99a326a68f6d8356167bcbb8bc031dc75c15250bbc4c4380a40e15cb2
---

# CAN bus at 500 kbps: heartbeat out, frames in

## Objectives

1. Send a 1 Hz heartbeat on CANFD0 as Classic CAN 2.0A at 500 kbps
2. Receive frames and show the latest frame (ID and data) with the receive and transmit counters

## Concepts

### What the QWA309 base board gives you to practise with

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board. This lesson uses the base board's CAN transceiver, configuring the CANFD0 controller to run as plain Classic CAN 2.0A (no CAN FD features) at 500 kbps, then both sending and receiving frames in the same program.

### What Classic CAN 2.0A at 500 kbps is, and how its bit timing is set

CANFD0 runs from a 100 MHz source clock. One bit on the CAN bus is split into a fixed number of small time slices called time quanta. This exercise sets prescaler = 10, `timeSegment1` (TS1) = 15, `timeSegment2` (TS2) = 4 (the value actually stored in the register is always n−1, e.g. `CANBUS_BITRATE_PRESCALER = 10U - 1U`). One bit has 1 (sync) + TS1 + TS2 = 1 + 15 + 4 = 20 time quanta. The quantum frequency is 100 MHz ÷ 10 = 10 MHz, so the bit rate is 10 MHz ÷ 20 = 500 kbps. The sample point sits at (1 + TS1) ÷ 20 = 16 ÷ 20 = 80% of the bit length, a normal value for CAN. Every node on the bus must set this group of numbers to reach the same bit rate — they do not need to be the exact same set of numbers.

### Configuring everything in plain PDL code, with no Device Configurator

`can_pins_init()` sets P16.2 as RX (HSIOM `P16_2_CANFD0_TTCAN_RX1`, `CY_GPIO_DM_HIGHZ` mode) and P16.3 as TX (HSIOM `P16_3_CANFD0_TTCAN_TX1`, `CY_GPIO_DM_STRONG_IN_OFF` mode) directly with `Cy_GPIO_Pin_Init()`. `can_clock_init()` supplies the peripheral clock to the CANFD block with the sequence `Cy_SysClk_PeriGroupSlaveInit()` → `PeriPclkSetDivider()` → `PeriPclkAssignDivider()` → `PeriPclkEnableDivider()`. `can_init()` then calls `Cy_CANFD_EnableMRAM()` to enable the message RAM, followed by `Cy_CANFD_Init()` with a pre-assembled `g_cfg` config struct (bit timing, empty SID/EXTID filters, a global filter accepting every frame into FIFO 0, buffer sizes). All of it is plain code — none of it depends on ModusToolbox's Device Configurator.

### Fully polled, with no ISR — so it can run right inside LVGL's task

This exercise sets `g_cfg.txCallback = NULL`, `.rxCallback = NULL`, `.errorCallback = NULL` and never registers anything with the NVIC. Both sending and receiving happen through `can_timer_cb()`, bound with `lv_timer_create()` every `CAN_REFRESH_PERIOD_MS = 250` ms, running on the same LVGL gfx task that draws the screen (the same pattern as the DPS368 episode in lesson 3.1). `can_poll_rx()` reads status with `Cy_CANFD_GetInterruptStatus()` and checks the `CY_CANFD_RX_FIFO_0_NEW_MESSAGE` bit itself in code — it is not an ISR triggered by hardware. Avoiding interrupts this way means the CM55 core's interrupt-mux never needs extra configuration.

### Sending a heartbeat once a second with one-shot TX

`can_timer_cb()` calls `can_send()` every `CAN_TX_EVERY_TICKS = 4` timer ticks (4 × 250 ms = 1 second), sending a frame with ID `CAN_TX_ID = 0x123` and length `CAN_TX_DLC = 8` bytes through `Cy_CANFD_UpdateAndTransmitMsgBuffer()`. Right after init, the code sets the `DAR` (Disable Automatic Retransmission) bit in the `CCCR` register, which **turns off** automatic retransmission when no peer node ever ACKs. The source comment states plainly that this is done so a frame does not sit waiting for an ACK when testing a single board on its own. The effect: the `g_tx_count` counter increments every time a frame is **successfully queued for sending** — it does not mean anyone actually received that frame. On a bus with a real peer, frames still get ACKed normally.

### Receiving one frame per poll tick from the RX FIFO

`can_poll_rx()` calls `Cy_CANFD_GetFIFOTop()` and `Cy_CANFD_AckRxFifo()` **exactly once** per call, even though RX FIFO 0 is configured with 4 elements (`numberOfFIFOElements = 4U`, `CY_CANFD_FIFO_MODE_BLOCKING` mode). Since `can_timer_cb()` calls it every 250 ms, the exercise can receive roughly 4 frames per second at most. If a peer sends faster than that (say, 20 frames per second), the FIFO fills up and any extra incoming frames get silently dropped. The filter configuration (`nonMatchingFramesStandard/Extended = CY_CANFD_ACCEPT_IN_RXFIFO_0`) accepts every ID into FIFO 0 — it does not filter any IDs out.

### CAN arbitration: the lower ID always wins, and the frame survives intact

When multiple nodes start transmitting at the same time, each one sends the bits of its ID while reading back what actually appears on the bus and comparing. CAN's electrical wiring makes a 0 bit (dominant) always beat a 1 bit (recessive) whenever they collide. The node sending the lower-valued ID wins arbitration and keeps transmitting with the frame intact; the losing node must stop immediately, and a controller normally retransmits it automatically — but this exercise has DAR set, so a frame that loses arbitration is also not automatically retransmitted. A CAN frame's ID is therefore both the message's name and its priority at the same time. The CANH/CANL pair is a differential line that needs a 120 Ω terminator at both ends of the cable (the jumper at P9 on this board) to match the cable's impedance and reduce signal reflection at high speed.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — CAN Bus Monitor** — CANFD0 running Classic CAN 2.0A at 500 kbps (P16.2 RX / P16.3 TX, SN65HVD230) on CM55 in polled mode — a 1 Hz TX heartbeat plus an RX frame table on LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_can_monitor&q=prac_qwa309_can_monitor)

The excerpts below are copied from the actual files at the same commit (Apache-2.0, tesaiot/developer-hub).

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — the bit-timing numbers that combine to reach 500 kbps from a 100 MHz clock:

```c
/* 500 kbps from 100 MHz: prescaler 10, TS1 15, TS2 4, SJW 4 (register = n-1) */
#define CANBUS_BITRATE_PRESCALER   (10U - 1U)
#define CANBUS_BITRATE_TS1         (15U - 1U)
#define CANBUS_BITRATE_TS2         (4U - 1U)
#define CANBUS_BITRATE_SJW         (4U - 1U)
```

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — sets the DAR bit so TX does not sit waiting for an ACK when testing alone:

```c
if (CY_CANFD_SUCCESS != Cy_CANFD_Init(CANBUS_HW, CANBUS_CHANNEL, &g_cfg, &g_ctx)) {
    return false;
}
Cy_CANFD_ConfigChangesEnable(CANBUS_HW, CANBUS_CHANNEL);
/* One-shot TX: disable automatic retransmission so a frame is not held
 * pending an ACK when no peer node is on the bus. Lets the TX counter
 * advance during a single-node self-test; a real bus still ACKs normally. */
CANBUS_HW->CH[CANBUS_CHANNEL].M_TTCAN.CCCR |= CANFD_CH_M_TTCAN_CCCR_DAR_Msk;
```

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — polls RX FIFO 0 once per call, with no ISR involved:

```c
static void can_poll_rx(void)
{
    uint32_t irq = Cy_CANFD_GetInterruptStatus(CANBUS_HW, CANBUS_CHANNEL);
    if (0U != (irq & CY_CANFD_RX_FIFO_0_NEW_MESSAGE)) {
        if (CY_CANFD_SUCCESS == Cy_CANFD_GetFIFOTop(CANBUS_HW, CANBUS_CHANNEL, 0U, &g_rx_buf)) {
            g_last_rx_id  = g_r0.id;
            g_last_rx_dlc = g_r1.dlc;
            /* ... copy g_rx_words into g_last_rx[], g_rx_count++ ... */
        }
        Cy_CANFD_AckRxFifo(CANBUS_HW, CANBUS_CHANNEL, 0U);
        Cy_CANFD_ClearInterrupt(CANBUS_HW, CANBUS_CHANNEL, CY_CANFD_RX_FIFO_0_NEW_MESSAGE);
    }
}
```

## Common mistakes

- **Assuming a rising TX counter means someone received the frame** — DAR disables waiting for an ACK, so the counter only increments when a frame is successfully queued for sending. Confirming actual reception needs a real peer node or a USB-CAN analyzer.
- **Joining a real bus without fitting the 120 Ω terminator** — the signal reflects at the ends of the cable without it, corrupting bits especially at high speed. But fitting a terminator at every node makes the combined resistance too low; only the two physical ends of the bus should have one.
- **Expecting every frame a peer sends to be received** — `can_poll_rx()` only pulls one frame from the FIFO per 250 ms poll tick. If the peer sends faster than that, the 4-slot FIFO fills up and the extra frames disappear silently.
- **Thinking the lower ID wins arbitration purely because it is numerically smaller** — the real mechanism is electrical: a 0 bit (dominant) always beats a 1 bit (recessive) when they collide on the bus. An ID whose high bits are 0 wins as a direct consequence; the outcome happens to match "smaller number wins", but the cause is the signal level, not a numeric comparison.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why must a CAN bus have termination at the ends of the cable?
- What does a CAN frame's ID tell you, beyond just naming the message?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
