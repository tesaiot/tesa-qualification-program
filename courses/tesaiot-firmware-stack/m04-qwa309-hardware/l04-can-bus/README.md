---
id: fw-stack.m04.l04
lang: th
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
---

# CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม

## เป้าหมาย

1. ส่งเฟรม heartbeat 1 Hz ผ่าน CANFD0 แบบ Classic CAN 2.0A ที่ 500 kbps
2. อ่านเฟรมที่เข้ามา แสดงเฟรมล่าสุด (ID และข้อมูล) และตัวนับเฟรมที่รับและส่ง

## แนวคิด

### บอร์ดฐาน QWA309 มีอะไรให้ฝึก

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง บทเรียนนี้ใช้ CAN transceiver บนบอร์ดฐาน ตั้งค่าคอนโทรลเลอร์ CANFD0 ให้ทำงานแบบ Classic CAN 2.0A ล้วน (ไม่ใช้ฟีเจอร์ CAN FD) ที่ความเร็ว 500 kbps แล้วทั้งส่งและรับเฟรมในโปรแกรมเดียว

### Classic CAN 2.0A ที่ 500 kbps คืออะไร และตั้ง bit timing อย่างไร

CANFD0 ได้ clock ต้นทาง 100 MHz หนึ่งบิตบนบัส CAN แบ่งเป็นช่วงเวลาเล็ก ๆ เรียก time quantum จำนวนคงที่ ตัวอย่างนี้ตั้ง prescaler = 10, `timeSegment1` (TS1) = 15, `timeSegment2` (TS2) = 4 (ค่าที่เก็บในรีจิสเตอร์จริงคือ n−1 เสมอ เช่น `CANBUS_BITRATE_PRESCALER = 10U - 1U`) หนึ่งบิตมี 1 (sync) + TS1 + TS2 = 1 + 15 + 4 = 20 time quanta ความถี่ quantum = 100 MHz ÷ 10 = 10 MHz ดังนั้น bit rate = 10 MHz ÷ 20 = 500 kbps จุดสุ่มตัวอย่าง (sample point) อยู่ที่ (1 + TS1) ÷ 20 = 16 ÷ 20 = 80% ของความยาวบิต ซึ่งเป็นค่าปกติสำหรับ CAN ทุก node บนบัสต้องตั้งค่าตัวเลขชุดนี้ให้ได้ bit rate เดียวกัน ไม่จำเป็นต้องเป็นชุดตัวเลขเดียวกันเป๊ะ

### ตั้งค่าทั้งหมดด้วยโค้ด PDL ล้วน ไม่แตะ Device Configurator

`can_pins_init()` ตั้ง P16.2 เป็น RX (HSIOM `P16_2_CANFD0_TTCAN_RX1`, โหมด `CY_GPIO_DM_HIGHZ`) และ P16.3 เป็น TX (HSIOM `P16_3_CANFD0_TTCAN_TX1`, โหมด `CY_GPIO_DM_STRONG_IN_OFF`) ด้วย `Cy_GPIO_Pin_Init()` โดยตรง `can_clock_init()` จ่าย peripheral clock ให้ CANFD ด้วยลำดับ `Cy_SysClk_PeriGroupSlaveInit()` → `PeriPclkSetDivider()` → `PeriPclkAssignDivider()` → `PeriPclkEnableDivider()` จากนั้น `can_init()` เรียก `Cy_CANFD_EnableMRAM()` เพื่อเปิดหน่วยความจำข้อความ แล้วเรียก `Cy_CANFD_Init()` ด้วย struct config `g_cfg` ที่ประกอบไว้ล่วงหน้า (bit timing, SID/EXTID filter ว่าง, global filter ให้รับทุกเฟรมเข้า FIFO 0, ขนาด buffer) ทั้งหมดเขียนเป็นโค้ดล้วน ไม่ต้องพึ่ง Device Configurator ของ ModusToolbox

### โหมด polled ล้วน ไม่มี ISR จึงรันในงาน LVGL ได้เลย

ตัวอย่างนี้ตั้ง `g_cfg.txCallback = NULL`, `.rxCallback = NULL`, `.errorCallback = NULL` และไม่ลงทะเบียน NVIC ใด ๆ ทั้งการส่งและรับทำงานผ่าน `can_timer_cb()` ที่ผูกกับ `lv_timer_create()` ทุก `CAN_REFRESH_PERIOD_MS = 250` ms ซึ่งรันอยู่บน LVGL gfx task เดียวกับที่วาดจอ (แบบเดียวกับ episode DPS368 ในบทเรียน 3.1) `can_poll_rx()` อ่านสถานะด้วย `Cy_CANFD_GetInterruptStatus()` ตรวจบิต `CY_CANFD_RX_FIFO_0_NEW_MESSAGE` เองด้วยโค้ด ไม่ใช่ ISR ที่ถูกกระตุ้นโดยฮาร์ดแวร์ การเลี่ยง interrupt ทำให้ไม่ต้องตั้งค่า interrupt-mux ของแกน CM55 เพิ่ม

### ส่ง heartbeat หนึ่งครั้งต่อวินาทีด้วย one-shot TX

`can_timer_cb()` เรียก `can_send()` ทุก `CAN_TX_EVERY_TICKS = 4` รอบของ timer (4 × 250 ms = 1 วินาที) ส่งเฟรม ID `CAN_TX_ID = 0x123` ยาว `CAN_TX_DLC = 8` ไบต์ผ่าน `Cy_CANFD_UpdateAndTransmitMsgBuffer()` ก่อน init เสร็จ โค้ดตั้งบิต `DAR` (Disable Automatic Retransmission) ในรีจิสเตอร์ `CCCR` เพื่อ**ปิด**การส่งซ้ำอัตโนมัติเมื่อไม่มี node อื่นมา ACK — คอมเมนต์ในซอร์สระบุชัดว่าทำแบบนี้เพื่อไม่ให้เฟรมค้างรอ ACK เมื่อทดสอบบอร์ดตัวเดียวโดด ๆ ผลคือตัวนับ `g_tx_count` เพิ่มขึ้นทุกครั้งที่ **ส่งสำเร็จเข้าคิว** ไม่ได้แปลว่ามีใครรับเฟรมนั้นจริง บนบัสที่มี node อื่นเฟรมยังคง ACK ตามปกติ

### รับเฟรมจาก RX FIFO ทีละเฟรมต่อรอบโพล

`can_poll_rx()` เรียก `Cy_CANFD_GetFIFOTop()` กับ `Cy_CANFD_AckRxFifo()` **ครั้งเดียว**ต่อการเรียกหนึ่งครั้ง แม้ RX FIFO 0 จะตั้งไว้ 4 ช่อง (`numberOfFIFOElements = 4U`, โหมด `CY_CANFD_FIFO_MODE_BLOCKING`) เมื่อ `can_timer_cb()` เรียกทุก 250 ms จึงรับได้สูงสุดประมาณ 4 เฟรมต่อวินาที ถ้ามี node อื่นส่งเร็วกว่านั้น (เช่น 20 เฟรม/วินาที) FIFO จะเต็มและเฟรมใหม่ที่มาเกินจะถูกทิ้งไป ตัวกรองที่ตั้งไว้ (`nonMatchingFramesStandard/Extended = CY_CANFD_ACCEPT_IN_RXFIFO_0`) รับทุก ID เข้า FIFO 0 หมด ไม่ได้กรองบาง ID ออก

### CAN arbitration: ID น้อยกว่าชนะเสมอโดยเฟรมไม่เสียหาย

เมื่อหลาย node เริ่มส่งพร้อมกัน แต่ละ node จะส่งบิตของ ID ออกไปพร้อมอ่านค่าที่ปรากฏจริงบนบัสกลับมาเทียบ สายไฟฟ้าของ CAN ทำให้บิต 0 (dominant) ชนะบิต 1 (recessive) เสมอเมื่อชนกัน node ที่ส่ง ID มีค่าน้อยกว่าจะชนะ arbitration และส่งเฟรมต่อได้โดยไม่เสียหาย ส่วน node ที่แพ้ต้องหยุดส่งทันทีและปกติ controller จะส่งซ้ำเองอัตโนมัติ — แต่ตัวอย่างนี้ตั้ง DAR ไว้ เฟรมที่แพ้ arbitration จึงไม่ถูกส่งซ้ำอัตโนมัติเช่นกัน ID ของเฟรม CAN จึงเป็นทั้งชื่อข้อความและลำดับความสำคัญในเวลาเดียวกัน สาย CANH/CANL เป็นสายคู่ differential ต้องมี terminator 120 Ω ที่ปลายสายทั้งสองด้าน (jumper ที่ P9 ของบอร์ดนี้) เพื่อจับคู่ impedance กับสาย ลดการสะท้อนของสัญญาณที่ความเร็วสูง

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — CAN Bus Monitor** — CANFD0 Classic CAN 2.0A @ 500 kbps (P16.2 RX / P16.3 TX, SN65HVD230) บน CM55 แบบ polled — TX heartbeat 1Hz + RX frame table บน LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_can_monitor&q=prac_qwa309_can_monitor)

โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริงที่ commit เดียวกัน (Apache-2.0, tesaiot/developer-hub)

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — ตัวเลข bit timing ที่รวมกันได้ 500 kbps จาก clock 100 MHz:

```c
/* 500 kbps from 100 MHz: prescaler 10, TS1 15, TS2 4, SJW 4 (register = n-1) */
#define CANBUS_BITRATE_PRESCALER   (10U - 1U)
#define CANBUS_BITRATE_TS1         (15U - 1U)
#define CANBUS_BITRATE_TS2         (4U - 1U)
#define CANBUS_BITRATE_SJW         (4U - 1U)
```

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — ตั้งบิต DAR เพื่อให้ TX ไม่ค้างรอ ACK เมื่อทดสอบบอร์ดตัวเดียว:

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

[`can_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/can_monitor_ui.c) — โพล RX FIFO 0 ครั้งเดียวต่อการเรียก ไม่ใช้ ISR:

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

## จุดที่มักพลาด

- **คิดว่าตัวนับ TX ที่เพิ่มขึ้นแปลว่ามีคนรับเฟรม** — DAR ปิดการรอ ACK ไว้ ตัวนับเพิ่มเมื่อส่งสำเร็จเข้าคิวเท่านั้น ต้องมี node อื่นหรือ USB-CAN analyzer มายืนยันว่ามีการรับจริง
- **ต่อบัสจริงโดยไม่ใส่ terminator 120 Ω** — สัญญาณจะสะท้อนกลับที่ปลายสาย ทำให้อ่านบิตผิดโดยเฉพาะที่ความเร็วสูง แต่ถ้าใส่ terminator ทุก node ความต้านทานรวมจะต่ำเกินไป ให้ใส่เฉพาะปลายสายสองด้านของบัส
- **คาดว่าจะรับได้ทุกเฟรมที่ node อื่นส่งมา** — `can_poll_rx()` ดึงจาก FIFO แค่ 1 เฟรมต่อรอบโพล 250 ms ถ้า peer ส่งเร็วกว่าอัตรานี้ FIFO ที่มี 4 ช่องจะเต็มและเฟรมส่วนเกินหายไปเงียบ ๆ
- **คิดว่า ID น้อยกว่าชนะ arbitration เพราะเป็นกติกาเปรียบเทียบตัวเลขเฉย ๆ** — กลไกจริงมาจากระดับไฟฟ้า: บิต 0 (dominant) ชนะบิต 1 (recessive) เสมอเมื่อชนกันบนบัส ID ที่มีบิตสูงเป็น 0 ตั้งแต่ต้นจึงชนะไปเอง ผลลัพธ์บังเอิญตรงกับ "เลขน้อยกว่าชนะ" แต่ต้นเหตุคือระดับสัญญาณ ไม่ใช่การเทียบค่าตัวเลข

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ทำไม CAN bus ต้องมี termination ที่ปลายสาย
- ID ของเฟรม CAN บอกอะไรนอกจากชื่อข้อความ

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
