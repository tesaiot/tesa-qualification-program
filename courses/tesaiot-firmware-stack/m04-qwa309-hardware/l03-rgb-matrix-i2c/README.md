---
id: fw-stack.m04.l03
lang: th
title:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
summary:
  th: "ควบคุม RGB dot matrix ผ่าน I2C"
  en: "Driving an RGB dot matrix over I2C"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V"
    en: "Send commands to the DFR0522 8x16 RGB matrix at address 0x10 on the 3.3 V bus"
  - th: "ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว"
    en: "Combine potentiometer input with matrix and screen output in one program"
develops:
  - {skill: proto.i2c, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_rgb_matrix"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ควบคุม RGB dot matrix ผ่าน I2C

## เป้าหมาย

1. ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V
2. ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว

## แนวคิด

### บอร์ดฐาน QWA309 มีอะไรให้ฝึก

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง ทั้งสามแบบฝึกในบทเรียนนี้ควบคุมจอ RGB dot-matrix ตัวเดียวกัน (DFRobot DFR0522) ผ่านไดรเวอร์ I2C ระดับต่ำร่วมกันในไฟล์ `rgb_panel.c` แต่ต่างกันที่วิธีสั่งงาน: กดปุ่มสั่งตรง ๆ, แอนิเมชันอัตโนมัติ, และผสมสีจาก potentiometer

### DFR0522 คืออะไร และคำสั่งที่ส่งไปมีอะไรบ้าง

DFR0522 เป็นจอ RGB dot-matrix ขนาด 16×8 พิกเซล (`RGB_PANEL_WIDTH = 16`, `RGB_PANEL_HEIGHT = 8`) สั่งงานผ่าน I2C ที่ address `0x10` (`RGB_PANEL_I2C_ADDRESS`) รองรับ 8 สี (`RGB_PANEL_COLOR_OFF` ถึง `RGB_PANEL_COLOR_WHITE` ค่า 0–7) คำสั่งแต่ละครั้งประกอบเป็นเฟรม: byte แรกเป็น command register คงที่ `0x02` ตามด้วย function byte ที่บอกว่าจะ clear (`0x01`), fill ทั้งแผง (`0x09`) หรือจุดพิกเซลเดียว (`0x08`) แล้วตามด้วยค่าสี พิกัด x และ y โดยเฟรมทั้งหมดถูก pad ให้มีขนาดคงที่ `RGB_PANEL_TX_SIZE = 51` ไบต์ (payload 50 ไบต์ + 1 ไบต์ command register) ไม่ว่าจะสั่งอะไรก็ส่งความยาวเท่ากันทุกครั้ง

### เขียนไดรเวอร์ I2C ระดับไบต์เอง ไม่ผ่าน wrapper สำเร็จรูป

`rgb_panel_write()` ใน `rgb_panel.c` ควบคุม I2C ด้วย PDL ระดับต่ำสุดสามฟังก์ชัน: `Cy_SCB_I2C_MasterSendStart()` ส่ง address พร้อมโหมดเขียน ตามด้วยลูป `Cy_SCB_I2C_MasterWriteByte()` ส่งทีละไบต์จนครบ `RGB_PANEL_TX_SIZE` แล้วปิดท้ายด้วย `Cy_SCB_I2C_MasterSendStop()` เสมอ ไม่ว่าการเขียนไบต์จะสำเร็จหรือไม่ (เพื่อคืนบัสให้อยู่ในสถานะปกติ ไม่ค้าง) แต่ละไบต์มี timeout `RGB_PANEL_BYTE_TIMEOUT_MS = 5` ms ทั้งสามแบบฝึกเรียกใช้ไดรเวอร์ตัวเดียวกันนี้ผ่านฟังก์ชันสาธารณะสามตัวคือ `rgb_panel_clear()`, `rgb_panel_fill()` และ `rgb_panel_pixel()`

### ใช้บัส I2C ร่วมกับจอ/ทัช ไม่ใช่ sensor I2C ของ master

ทั้งสามแบบฝึกสั่งงาน DFR0522 ผ่าน `DISPLAY_I2C_CONTROLLER_HW` และ context `disp_touch_i2c_controller_context` ซึ่งเป็น SCB I2C ตัวเดียวกับที่ใช้กับจอแสดงผลและทัชสกรีน ไม่ใช่ sensor I2C ที่ master template เปิดไว้ให้ (ดูบทเรียน 3.1) เหตุผลคือ sensor I2C อยู่บน 1.8 V domain ขณะที่ DFR0522 อยู่บน bus 3.3 V ร่วมกับจอ/ทัช การต่อผิด domain แรงดันอาจสื่อสารไม่ได้หรือทำให้ขาเสียหาย และเพราะบัสนี้ framework init ไว้ให้แล้วตั้งแต่ก่อน `example_main()` จึงเรียกใช้ context ที่มีอยู่แล้วได้ทันทีโดยไม่ต้อง init ซ้ำ (การ init ซ้ำอาจทำให้ทัชสกรีนเสียการทำงาน)

### ตรวจว่ามีอุปกรณ์อยู่จริงก่อนเชื่อผลลัพธ์

ปุ่ม "Check 0x10" ใน DFR0522 RGB Dot Matrix เรียก `check_panel_device()` ซึ่งส่งแค่ START พร้อม address แล้ว STOP ทันที ไม่ส่งข้อมูลใด ๆ เป็นการทดสอบว่ามีอุปกรณ์ตอบ ACK ที่ address นั้นหรือไม่ ผลลัพธ์เป็นค่า enum `cy_en_scb_i2c_status_t` ที่ถูกแปลเป็นข้อความอ่านง่ายด้วย `i2c_status_to_text()` เช่น "ADDRESS NACK" (ไม่มีอุปกรณ์ตอบเลย), "DATA NACK" (มีอุปกรณ์ตอบ address แต่ปฏิเสธข้อมูล), "TIMEOUT" หรือ "ARBITRATION LOST" การแยกแยะแบบนี้สำคัญ เพราะ "ADDRESS NACK" ชี้ไปที่ปัญหาสาย ไฟเลี้ยง หรือ address ผิด ในขณะที่ error หลัง address ตอบแล้วชี้ไปที่ปัญหาระดับคำสั่งหรือ timing แทน

### ผสมสี R/G/B จาก potentiometer ด้วยการแพ็กบิต (Pot → RGB Mixer)

Pot → RGB Mixer อ่าน potentiometer 3 ตัวแรก (channel index 0–2 บน P15.4–P15.6) ทุก `MIX_REFRESH_MS = 120` ms แต่ละช่องถ้าค่าดิบ ≥ `MIX_THRESHOLD = 2048` (ประมาณ 50%) จะเปิดบิตของตัวเอง: `bits |= (1U << i)` โดย `i = 0` คือ R, `i = 1` คือ G, `i = 2` คือ B บิตทั้งสามรวมกันแล้ว cast ตรงเป็น `rgb_panel_color_t` ได้เลย เพราะ enum สีของ DFR0522 แพ็กบิตในลำดับเดียวกันพอดี (เช่น R+B เปิดพร้อมกัน = บิต 0b101 = 5 = `RGB_PANEL_COLOR_PURPLE`) โค้ดเขียนแผงใหม่เฉพาะเมื่อสีเปลี่ยนจากรอบก่อน (`if (color != s_last_color)`) เพื่อไม่ให้ส่งเฟรม 51 ไบต์ซ้ำ ๆ บนบัสที่ใช้ร่วมกับทัชทุก 120 ms โดยไม่จำเป็น `s_last_color` เริ่มต้นที่ `RGB_PANEL_COLOR_WHITE` เพื่อบังคับให้เขียนครั้งแรกเสมอ

### แอนิเมชันด้วย state machine เฟรมนับถอยหลัง (RGB Matrix FX)

RGB Matrix FX วนเอฟเฟกต์ 3 แบบอัตโนมัติด้วย `lv_timer` ที่ `FX_PERIOD_MS = 140` ms ตัวแปร `s_frame` นับตั้งแต่ 0 ถึง `FX_FRAMES_PER_EFFECT - 1` (24 เฟรม) ต่อหนึ่งเอฟเฟกต์ แล้วสลับ `s_effect` ไปตัวถัดไปด้วยมอดุโล 3 `fx_step()` เลือกการทำงานตาม `s_effect`: เอฟเฟกต์ 0 (Colour Cycle) เรียก `rgb_panel_fill()` ทั้งแผงด้วยสีจากอาร์เรย์ `s_cycle[7]` วนตาม `s_frame % 7`, เอฟเฟกต์ 1 (Pixel Sweep) เคลียร์แผงแล้วจุดพิกเซลเดียวที่ตำแหน่ง `x = (s_frame * 2) % FX_COLS`, `y = (s_frame / 2) % FX_ROWS`, เอฟเฟกต์ 2 (Row Wipe) เติมสีทั้งแผงที่เปลี่ยนช้าลง (`s_frame / 4`) ทุกเอฟเฟกต์เรียกไดรเวอร์ `rgb_panel` ตัวเดียวกับอีกสองแบบฝึก

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — DFR0522 RGB Dot Matrix** — ควบคุม DFRobot DFR0522 RGB matrix 8x16 (I2C 0x10) บน bus 3.3V ร่วมกับ display แสดง clear/fill/pixel/pattern ผ่าน LVGL UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix)
- **QWA309 — RGB Matrix FX** — เอฟเฟกต์แอนิเมชันบน DFR0522 8x16 (color cycle / pixel sweep / row wipe) auto-cycle + สถานะบน LCD
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix_fx&q=prac_qwa309_rgb_matrix_fx)
- **QWA309 — Pot → RGB Mixer** — 3 potentiometers เป็น R/G/B channel (>50% = เปิดสีนั้น) ผสมเป็น 1 ใน 8 สีของ DFR0522 matrix + แสดงบน LCD — รวม SAR pots + RGB I2C
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_rgb_mixer&q=prac_qwa309_pot_rgb_mixer)

โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริงที่ commit เดียวกัน (Apache-2.0, tesaiot/developer-hub)

[`rgb_panel.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/rgb_panel.c) — ไดรเวอร์ I2C ระดับไบต์ที่ทั้งสามแบบฝึกเรียกใช้ร่วมกัน:

```c
status = Cy_SCB_I2C_MasterSendStart(base,
                                    RGB_PANEL_I2C_ADDRESS,
                                    CY_SCB_I2C_WRITE_XFER,
                                    RGB_PANEL_BYTE_TIMEOUT_MS,
                                    context);

if (status == CY_SCB_I2C_SUCCESS)
{
    for (uint32_t i = 0U; i < RGB_PANEL_TX_SIZE; i++)
    {
        status = Cy_SCB_I2C_MasterWriteByte(base,
                                            tx_buffer[i],
                                            RGB_PANEL_BYTE_TIMEOUT_MS,
                                            context);
        if (status != CY_SCB_I2C_SUCCESS) { break; }
    }
}

stop_status = Cy_SCB_I2C_MasterSendStop(base,
                                        RGB_PANEL_BYTE_TIMEOUT_MS,
                                        context);
```

[`rgb_matrix_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/rgb_matrix_ui.c) — ตรวจว่ามีอุปกรณ์ตอบ ACK ที่ address 0x10 หรือไม่ ก่อนส่งคำสั่งจริง:

```c
static cy_en_scb_i2c_status_t check_panel_device(void)
{
    cy_en_scb_i2c_status_t status;

    status = Cy_SCB_I2C_MasterSendStart(DISPLAY_I2C_CONTROLLER_HW,
                                        RGB_PANEL_I2C_ADDRESS,
                                        CY_SCB_I2C_WRITE_XFER,
                                        DEVICE_CHECK_TIMEOUT_MS,
                                        &disp_touch_i2c_controller_context);
    (void)Cy_SCB_I2C_MasterSendStop(DISPLAY_I2C_CONTROLLER_HW,
                                    DEVICE_CHECK_TIMEOUT_MS,
                                    &disp_touch_i2c_controller_context);
    return status;
}
```

[`pot_rgb_mixer_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/pot_rgb_mixer_ui.c) — แพ็กบิต R/G/B จาก threshold แล้วเขียนแผงเฉพาะตอนสีเปลี่ยน:

```c
uint8_t bits = 0U;
for (uint8_t i = 0U; i < 3U; i++) {
    uint16_t raw = mix_read(s_ch[i].ch);
    /* ... update bar/label ... */
    if (raw >= MIX_THRESHOLD) { bits |= (uint8_t)(1U << i); }
}

/* bits: b0=R b1=G b2=B  ->  DFR0522 colour enum is the same RGB packing. */
rgb_panel_color_t color = (rgb_panel_color_t)bits;
if (color != s_last_color) {
    s_last_color = color;
    (void)rgb_panel_fill(DISPLAY_I2C_CONTROLLER_HW,
                         &disp_touch_i2c_controller_context, color);
}
```

[`rgb_fx_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/rgb_fx_ui.c) — เลือกเอฟเฟกต์ตาม `s_effect` แล้ววาดหนึ่งเฟรม:

```c
switch (s_effect) {
case 0U:  /* colour cycle — one fill per frame */
    (void)rgb_panel_fill(FX_HW, FX_CTX, s_cycle[s_frame % 7U]);
    break;
case 1U: { /* pixel sweep — clear then light one pixel */
    (void)rgb_panel_clear(FX_HW, FX_CTX);
    uint8_t x = (uint8_t)((s_frame * 2U) % FX_COLS);
    uint8_t y = (uint8_t)((s_frame / 2U) % FX_ROWS);
    (void)rgb_panel_pixel(FX_HW, FX_CTX, x, y, s_cycle[s_frame % 7U]);
    break;
}
```

## จุดที่มักพลาด

- **ต่อ DFR0522 เข้ากับ sensor I2C ของ master แทนบัส 3.3 V ของจอ/ทัช** — sensor I2C อยู่บน 1.8 V domain ต่อผิดแรงดันอาจสื่อสารไม่ได้หรือทำให้ขาเสียหาย ต้องใช้ `DISPLAY_I2C_CONTROLLER_HW` เสมอ
- **สรุปว่า "ADDRESS NACK" กับ error หลังจากนั้นคือปัญหาเดียวกัน** — ADDRESS NACK แปลว่าไม่มีอุปกรณ์ตอบเลย (ตรวจสาย ไฟ address) ส่วน error ที่เกิดหลัง address ตอบแล้วเป็นปัญหาระดับคำสั่งหรือ timing คนละสาเหตุกัน
- **เขียนแผงทุกรอบโพลโดยไม่เช็กว่าสีเปลี่ยนหรือไม่** — Pot → RGB Mixer เขียนเฉพาะตอนสีเปลี่ยนเพื่อลดภาระบัสที่ใช้ร่วมกับทัช ถ้าสีแรกที่คำนวณได้ตรงกับค่าเริ่มต้น `s_last_color` (WHITE) พอดี แผงจะยังไม่ถูกเขียนจนกว่าสีจะเปลี่ยนจริง
- **ลืมว่า `rgb_panel_fill()`/`rgb_panel_pixel()` ตรวจขอบเขตพารามิเตอร์และคืน `CY_SCB_I2C_BAD_PARAM` ก่อนส่งเสมอ** — สีหรือพิกัดที่อยู่นอกช่วงจะถูกดักตั้งแต่ในไดรเวอร์ ไม่ถึงขั้นส่งข้อมูลผิดออกไปทางบัส

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

- อุปกรณ์สองตัวบน I2C bus เดียวกันแยกกันด้วยอะไร
- ถ้า matrix ไม่ตอบ ต้องตรวจอะไรก่อน (สาย ไฟ address)

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
