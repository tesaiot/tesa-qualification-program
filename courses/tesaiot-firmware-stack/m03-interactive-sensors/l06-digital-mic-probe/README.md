---
id: fw-stack.m03.l06
lang: th
title:
  th: "ไมโครโฟน PDM สเตอริโอและ level meter"
  en: "Stereo PDM microphone and a level meter"
summary:
  th: "เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL"
  en: "Stereo PDM microphone and a level meter"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m03.l05]
objectives:
  - th: "เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา"
    en: "Capture the stereo PDM microphone and compute left/right sound levels"
  - th: "แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS"
    en: "Show the levels as a meter and explain whether it uses peak or RMS"
  - th: "ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน"
    en: "Test with sound from each side and confirm the channels are not swapped"
develops:
  - {skill: sys.dsp, to: 2}
  - {skill: sys.sensors-actuators, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "int_ep06_digital_mic_probe"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# ไมโครโฟน PDM สเตอริโอและ level meter

## เป้าหมาย

1. เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา
2. แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS
3. ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน

## แนวคิด

### PDM vs PCM: ทำไมไมค์ MEMS ถึงส่ง PDM

PDM (Pulse Density Modulation) คือสตรีม 1 บิตความเร็วสูง (1–3 MHz) ที่ **ความหนาแน่นของ pulse** แทนขนาดสัญญาณ
ต่างจาก PCM ที่แต่ละตัวอย่างเป็นตัวเลขหลายบิต (16/24-bit) ที่อัตราต่ำกว่ามาก (8–48 kHz) ไมค์ MEMS ขนาดเล็กส่ง PDM
ออกมาได้ตรง ๆ เพราะวงจรภายในเรียบง่ายกว่า ชิป PSoC Edge มี PDM/PCM converter แปลง PDM เป็น PCM ให้ในฮาร์ดแวร์
(lowpass + decimate) ก่อนส่งเข้า FIFO ให้ CPU อ่าน — episode นี้ตั้งค่าไว้ที่ 16 kHz, เฟรมละ 160 ตัวอย่างต่อช่อง
(`PDM_MIC_FRAME_SAMPLES_PER_CHANNEL = 160`) ซึ่งพอดี 10 ms ต่อเฟรมที่ 16 kHz

### การจับสัญญาณจริงคือ interrupt อ่าน FIFO + double-buffer ซอฟต์แวร์ ไม่ใช่ DMA ตามที่ README ต้นทางอธิบาย

README ต้นทางบอกว่า "DMA-driven — CPU ไม่ต้องยุ่ง, hardware เขียนลง circular buffer" และ "ผูก DMA channel → IRQ
handler" แต่โค้ดจริงที่ commit `9a8e3ed` **ไม่ใช้ DMA เลย** — ใช้ interrupt ของแต่ละช่อง (ซ้าย = channel 2, ขวา =
channel 3) ที่ยิงเมื่อ FIFO ถึง trigger level (`PDM_RX_FIFO_TRIG_LEVEL` = ครึ่งหนึ่งของขนาด FIFO) แล้ว
`process_channel_irq()` อ่านค่าออกจาก FIFO ทีละตัวอย่างด้วย `Cy_PDM_PCM_Channel_ReadFifo()` ใส่ลง buffer ที่กำลัง
เขียนอยู่ (`buffer0`/`buffer1` สลับกันแบบ ping-pong ที่**ซอฟต์แวร์จัดการเอง** ไม่ใช่ DMA descriptor) เมื่อครบ 160
ตัวอย่างทั้งสองช่อง (`PDM_READY_BOTH`) จะส่ง semaphore ปลุก task ที่รออยู่ให้ไปคำนวณระดับเสียงต่อ — CPU จึงต้อง
"ยุ่ง" กับทุกตัวอย่างจริง ๆ ผ่าน interrupt ไม่ใช่แค่รอ DMA เสร็จ

### ค่าเฉลี่ยที่คำนวณคือ mean of |x| ไม่ใช่ RMS แม้ทำหน้าที่คล้ายกัน

`compute_level()` คำนวณ `peak_abs` (ค่าสูงสุดของ |sample|) และ `avg_abs` = ผลรวม |sample| หารด้วยจำนวนตัวอย่าง —
เป็นค่าเฉลี่ยของ**ค่าสัมบูรณ์** ไม่มีการยกกำลังสองหรือถอดรากที่สองเลย จึง**ไม่ใช่ RMS** (root-mean-square) แม้จะขึ้น
ลงตามความดังคล้ายกันและคำนวณเบากว่า (ไม่มีการคูณ) แต่ให้ค่าต่ำกว่า RMS ของสัญญาณเดียวกันเสมอ (คลื่นไซน์บริสุทธิ์
mean|x| ≈ 0.9 เท่าของ RMS)

### เปอร์เซ็นต์ที่ขึ้นจอไม่ได้มาจาก peak/32767 ตรง ๆ แต่ map ผ่าน floor/ceiling ที่ปรับให้เหมาะกับเสียงพูดในห้องเรียน

`to_ui_pct()` ไม่ได้หาร `avg_abs` ด้วย `INT16_MAX` (32767) ตรง ๆ ตามที่ README ต้นทางอธิบายไว้ (และสูตรนั้นในอันที่
จริงก็ใช้ peak ไม่ใช่ avg) — โค้ดจริง map `avg_abs` แบบ clamp เชิงเส้นระหว่าง `PDM_UI_FLOOR_ABS = 80` (ให้ 0%)
กับ `PDM_UI_CEIL_ABS = 8000` (ให้ 100%) คอมเมนต์ในซอร์สระบุเหตุผลตรง ๆ ว่า "Tuned for classroom speech level so
UI% doesn't saturate too early" — เสียงพูดปกติในห้องเรียนมีขนาดเล็กกว่าค่า full-scale ของ int16 มาก ถ้าหารด้วย
32767 ตรง ๆ แถบจะขึ้นแค่ไม่กี่ % เสมอ ต้อง "บีบ" ช่วงที่ใช้งานจริงให้เต็มแถบ

### balance meter ถูกทำไว้แล้วจริง ไม่ใช่แค่หัวข้อ "ลองแก้" ตามที่ README ต้นทางแนะนำ

README ต้นทางแนะนำในหัวข้อ Experiment Ideas ว่า "Balance meter — แสดง (L-R)/(L+R) เป็นเข็ม bar กลางจอ" ราวกับเป็น
สิ่งที่ยังไม่มี แต่โค้ดจริงคำนวณ `balance_lr = (L_avg - R_avg) * 100 / (L_avg + R_avg)` ไว้แล้วใน
`pdm_probe_logger.c` และ view แสดงตัวอักษร "L" เมื่อ balance > 3 หรือ "R" เมื่อ < -3 ฟีเจอร์นี้จึงพร้อมใช้ตั้งแต่
build แรก ไม่ต้องเขียนเพิ่ม

### UI ใช้ `lv_timer` poll แบบ "sample ล่าสุดชนะ" ที่ 50 ms ไม่ใช่ `lv_async_call` ที่ 50 Hz

เหมือน pattern ที่พบซ้ำในบทเรียน 2.5 (WiFi scan): `mic_presenter.c` ไม่ใช้ `lv_async_call()` ตามที่ README ต้นทาง
อธิบาย ("lv_async_call ในจังหวะ 50 Hz") แต่สร้าง `lv_timer` ที่คาบ 50 ms (เท่ากับ 20 ครั้ง/วินาที ไม่ใช่ 50
ครั้ง/วินาทีตามที่ระบุ) มาอ่าน sample ล่าสุดที่ถูกเขียนไว้ภายใต้ `taskENTER_CRITICAL()`/`EXIT` ผู้ผลิต (logger
task) ส่งค่าใหม่ทุก 10 ms แต่ policy คือ "sample ล่าสุดชนะ" (เขียนทับของเก่า) — เสียงกระแทกสั้น ๆ ที่เกิดและหายไป
ภายในกรอบ 10 ms หนึ่งเฟรมอาจไม่มีวันถูก UI เห็นเลย ถ้า timer 50 ms มาอ่านหลังจากเฟรมนั้นถูกเขียนทับไปแล้ว

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md) เพื่อเข้าใจ PDM/PCM แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะกลไกจับสัญญาณและสูตรคำนวณต่างจากที่ README ต้นทางอธิบาย

[`app_audio/pdm/pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.c) — mean-abs ไม่ใช่ RMS และเปอร์เซ็นต์ที่ clamp floor/ceiling:

```c
/* Tuned for classroom speech level so UI% doesn't saturate too early. */
#define PDM_UI_FLOOR_ABS              (80U)
#define PDM_UI_CEIL_ABS               (8000U)

static uint32_t to_ui_pct(uint32_t avg_abs)
{
    if (avg_abs <= PDM_UI_FLOOR_ABS) { return 0U; }
    if (avg_abs >= PDM_UI_CEIL_ABS)  { return 100U; }
    return ((avg_abs - PDM_UI_FLOOR_ABS) * 100U) / (PDM_UI_CEIL_ABS - PDM_UI_FLOOR_ABS);
}
```

[`app_audio/pdm/pdm_mic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_mic.c) — จับสัญญาณด้วย interrupt อ่าน FIFO ไม่ใช่ DMA:

```c
static void process_channel_irq(pdm_channel_state_t *state, uint8_t channel_index, uint8_t ready_bit)
{
    /* ... */
    for (uint32_t index = 0U; index < PDM_RX_FIFO_TRIG_LEVEL; index++)
    {
        int16_t sample = (int16_t)Cy_PDM_PCM_Channel_ReadFifo(CYBSP_PDM_HW, channel_index);
        /* เขียนลง state->active[out_idx++] จนครบเฟรม แล้วสลับ active/full */
    }
    Cy_PDM_PCM_Channel_ClearInterrupt(CYBSP_PDM_HW, channel_index, CY_PDM_PCM_INTR_RX_TRIGGER);
}
```

[`app_ui/mic/mic_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_ui/mic/mic_presenter.c) — poll ทุก 50 ms แบบ latest-sample-wins:

```c
static void mic_presenter_ui_timer_cb(lv_timer_t *timer)
{
    mic_presenter_sample_t local = {0};
    bool has_sample = false;

    taskENTER_CRITICAL();
    has_sample = s_has_sample;
    if (has_sample) { local = s_latest_sample; }
    taskEXIT_CRITICAL();

    if (has_sample && s_view_ready) { mic_view_apply(&local); }
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/main_example.c) เรียก `mic_presenter_start()` ก่อน `pdm_probe_logger_start()` ตรงตามที่ README ต้นทางอธิบาย (สร้าง consumer ก่อน producer)
- ดูโฟลเดอร์เต็มที่ [`int_ep06_digital_mic_probe/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe)

## จุดที่มักพลาด

- **คิดว่าใช้ DMA ตามที่ README ต้นทางอธิบาย** — โค้ดจริงใช้ interrupt อ่าน FIFO ทีละตัวอย่างพร้อม double-buffer
  ที่ซอฟต์แวร์จัดการเอง ให้ยึดโค้ดจริงเมื่ออธิบายกลไกจับสัญญาณ
- **เข้าใจว่า avg ที่คำนวณคือ RMS** — เป็นแค่ค่าเฉลี่ยของค่าสัมบูรณ์ (mean|x|) ไม่มีการยกกำลังสอง ให้ค่าต่ำกว่า RMS
  เสมอสำหรับสัญญาณเดียวกัน
- **คิดว่า UI % มาจาก `avg*100/32767` ตรง ๆ** — จริงถูก clamp ผ่านช่วง 80–8000 ที่ปรับให้เหมาะกับเสียงพูดเบา ๆ ใน
  ห้องเรียน ค่าที่เบากว่า 80 ขึ้น 0% เสมอ และค่าที่แรงกว่า 8000 ขึ้น 100% เสมอ
- **คิดว่า UI จะจับเสียงกระแทกสั้น ๆ ได้ทุกครั้ง** — policy "sample ล่าสุดชนะ" ที่ UI timer 50 ms อาจพลาดเฟรม 10
  ms ที่มีเสียงกระแทกไปเลยถ้าถูกเฟรมถัดไปเขียนทับก่อน UI มาอ่าน

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP06 — Digital Mic Probe บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/int_ep06_digital_mic_probe.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- PDM ต่างจาก PCM อย่างไร
- RMS กับ peak ให้ภาพระดับเสียงต่างกันอย่างไร
- ทดสอบอย่างไรว่าช่องซ้ายและขวาไม่สลับกัน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
