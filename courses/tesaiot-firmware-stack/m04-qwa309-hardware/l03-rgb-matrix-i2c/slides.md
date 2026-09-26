---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.3 — ควบคุม RGB dot matrix ผ่าน I2C"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 4.3 — ควบคุม RGB dot matrix ผ่าน I2C

## ควบคุม RGB dot matrix ผ่าน I2C

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ส่งคำสั่งไปยัง DFR0522 RGB matrix 8x16 ที่ address 0x10 บน bus 3.3 V
2. ผสม input จาก potentiometer กับ output บน matrix และจอในงานเดียว

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m01.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 10 + ฝึกตาม 25 + แล็บ 30 + เช็กความเข้าใจ 5 = 70 นาที

---

# ดูของจริงก่อน

แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดฐาน QWA309 โดยตรง — เปิดบน Developer Hub แล้ว flash เฟิร์มแวร์สำเร็จรูปดูก่อนว่าหน้าจอเป็นอย่างไร

- **QWA309 — DFR0522 RGB Dot Matrix** — ควบคุม DFRobot DFR0522 RGB matrix 8x16 (I2C 0x10) บน bus 3.3V ร่วมกับ display แสดง clear/fill/pixel/pattern ผ่าน LVGL UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix)
- **QWA309 — RGB Matrix FX** — เอฟเฟกต์แอนิเมชันบน DFR0522 8x16 (color cycle / pixel sweep / row wipe) auto-cycle + สถานะบน LCD
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix_fx) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix_fx&q=prac_qwa309_rgb_matrix_fx)
- **QWA309 — Pot → RGB Mixer** — 3 potentiometers เป็น R/G/B channel (>50% = เปิดสีนั้น) ผสมเป็น 1 ใน 8 สีของ DFR0522 matrix + แสดงบน LCD — รวม SAR pots + RGB I2C
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_rgb_mixer&q=prac_qwa309_pot_rgb_mixer)

---

# แนวคิด — บอร์ดฐาน QWA309 มีอะไรให้ฝึก

ทั้งสามแบบฝึกควบคุมจอ RGB dot-matrix ตัวเดียวกัน (DFRobot DFR0522) ผ่านไดรเวอร์ I2C ร่วมกันใน `rgb_panel.c`

ต่างกันที่วิธีสั่งงาน: กดปุ่มสั่งตรง ๆ, แอนิเมชันอัตโนมัติ, และผสมสีจาก potentiometer

---

# แนวคิด — DFR0522 คืออะไร คำสั่งมีอะไรบ้าง

จอ RGB dot-matrix 16×8 พิกเซล ที่ I2C address `0x10` รองรับ 8 สี (0–7)

เฟรมคำสั่ง: `0x02` (register) + function byte (clear/fill/pixel) + สี + x + y แพดเป็น `RGB_PANEL_TX_SIZE = 51` ไบต์เสมอ

---

# แนวคิด — เขียนไดรเวอร์ I2C ระดับไบต์เอง

`Cy_SCB_I2C_MasterSendStart()` → ลูป `MasterWriteByte()` ทีละไบต์ → `MasterSendStop()` เสมอไม่ว่าจะสำเร็จหรือไม่

ทั้งสามแบบฝึกเรียกไดรเวอร์เดียวกันผ่าน `rgb_panel_clear/fill/pixel()`

---

# แนวคิด — ใช้บัสร่วมกับจอ/ทัช ไม่ใช่ sensor I2C

`DISPLAY_I2C_CONTROLLER_HW` + `disp_touch_i2c_controller_context` — บัสเดียวกับจอ/ทัชที่ 3.3 V

sensor I2C ของ master อยู่บน 1.8 V domain คนละบัส ต่อผิดอาจสื่อสารไม่ได้หรือขาเสียหาย

---

# แนวคิด — ตรวจอุปกรณ์ก่อนเชื่อผล

ปุ่ม "Check 0x10" ส่งแค่ START+address+STOP ดู ACK/NACK

"ADDRESS NACK" = ไม่มีอุปกรณ์ตอบ (สาย/ไฟ/address) ต่างจาก error หลัง address ตอบแล้ว (คำสั่ง/timing)

---

# แนวคิด — ผสม R/G/B ด้วยการแพ็กบิต (Pot → RGB Mixer)

`raw ≥ MIX_THRESHOLD (2048)` → เปิดบิตของช่องนั้น b0=R b1=G b2=B แล้ว cast ตรงเป็น `rgb_panel_color_t`

เขียนแผงเฉพาะตอนสีเปลี่ยน (`color != s_last_color`) เพื่อลดภาระบัส

---

# แนวคิด — แอนิเมชันด้วย state machine (RGB Matrix FX)

`s_frame` นับ 0–23 ต่อเอฟเฟกต์ (`FX_FRAMES_PER_EFFECT=24`) แล้ว `s_effect` วนมอดุโล 3

Colour Cycle / Pixel Sweep / Row Wipe — ทุกเอฟเฟกต์เรียก `rgb_panel` ตัวเดียวกัน

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `proto.i2c` (ระดับ 2)
- `sys.sensors-actuators` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — ไดรเวอร์ I2C ระดับไบต์

[`rgb_panel.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_rgb_matrix/rgb_panel.c) — ทั้งสามแบบฝึกเรียกไดรเวอร์นี้ร่วมกัน:

```c
status = Cy_SCB_I2C_MasterSendStart(base, RGB_PANEL_I2C_ADDRESS,
                    CY_SCB_I2C_WRITE_XFER,
                    RGB_PANEL_BYTE_TIMEOUT_MS, context);

if (status == CY_SCB_I2C_SUCCESS) {
    for (uint32_t i = 0U; i < RGB_PANEL_TX_SIZE; i++) {
        status = Cy_SCB_I2C_MasterWriteByte(base, tx_buffer[i],
                    RGB_PANEL_BYTE_TIMEOUT_MS, context);
        if (status != CY_SCB_I2C_SUCCESS) { break; }
    }
}

stop_status = Cy_SCB_I2C_MasterSendStop(base,
                RGB_PANEL_BYTE_TIMEOUT_MS, context);
```

---

# ตัวอย่างสมบูรณ์ — ผสมสีด้วยการแพ็กบิต

[`pot_rgb_mixer_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_rgb_mixer/pot_rgb_mixer_ui.c)

```c
uint8_t bits = 0U;
for (uint8_t i = 0U; i < 3U; i++) {
    uint16_t raw = mix_read(s_ch[i].ch);
    if (raw >= MIX_THRESHOLD) { bits |= (uint8_t)(1U << i); }
}

rgb_panel_color_t color = (rgb_panel_color_t)bits;
if (color != s_last_color) {
    s_last_color = color;
    (void)rgb_panel_fill(DISPLAY_I2C_CONTROLLER_HW,
                         &disp_touch_i2c_controller_context, color);
}
```

---

# จุดที่มักพลาด

- ต่อ DFR0522 เข้า sensor I2C (1.8 V) แทนบัส 3.3 V ของจอ/ทัช — ต้องใช้ `DISPLAY_I2C_CONTROLLER_HW` เสมอ
- สรุปว่า "ADDRESS NACK" กับ error หลังจากนั้นคือปัญหาเดียวกัน — คนละสาเหตุ (สาย/ไฟ vs คำสั่ง/timing)
- เขียนแผงทุกรอบโพลโดยไม่เช็กว่าสีเปลี่ยนหรือไม่ — เปลืองบัสที่ใช้ร่วมกับทัช
- ลืมว่า `rgb_panel_fill/pixel()` ตรวจขอบเขตพารามิเตอร์และคืน `BAD_PARAM` ก่อนส่งเสมอ

---

# ตัวอย่างสมบูรณ์ — build และ flash

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- อุปกรณ์สองตัวบน I2C bus เดียวกันแยกกันด้วยอะไร
- ถ้า matrix ไม่ตอบ ต้องตรวจอะไรก่อน (สาย ไฟ address)

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 2 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)
