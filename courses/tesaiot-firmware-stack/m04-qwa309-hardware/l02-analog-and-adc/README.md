---
id: fw-stack.m04.l02
lang: th
title:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
summary:
  th: "อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
  en: "Analog voltages with the 12-bit SAR ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์"
    en: "Read four potentiometers through the 12-bit SAR ADC and convert to volts and percent"
  - th: "แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC"
    en: "Plot them as a scrolling scope and explain ADC resolution"
develops:
  - {skill: mcu.adc-dac, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_pot_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต

## เป้าหมาย

1. อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์
2. แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC

## แนวคิด

### บอร์ดฐาน QWA309 มีอะไรให้ฝึก

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง สองแบบฝึกในบทเรียนนี้อ่าน potentiometer ทั้ง 4 ตัวเหมือนกัน (VR1–VR4 ที่ P15.4–P15.7) แต่แสดงผลต่างรูปแบบ: แบบแรกเป็นแผงตัวเลข+บาร์ แบบที่สองเป็นกราฟเลื่อนแบบออสซิลโลสโคป

### SAR ADC 12 บิตคืออะไร และตัวเลขหมายถึงอะไร

AUTANALOG SAR ADC เป็นตัวแปลงสัญญาณอนาล็อกเป็นดิจิทัลแบบ successive-approximation ในตัวชิป PSoC Edge อ่านค่าออกมาเป็นเลขจำนวนเต็ม 12 บิต คือ 0–4095 (`POT_ADC_FULL_SCALE = 4095`) เทียบกับแรงดันอ้างอิง (`POT_ADC_VREF_MV = 1800`) คือ **1.8 V ไม่ใช่ 3.3 V** ความละเอียดจึงอยู่ที่ 1800 mV ÷ 4095 ขั้น ≈ 0.44 mV ต่อหนึ่งขั้น ตัวเลขนี้ละเอียดกว่าความละเอียดที่ 3.3 V (≈ 0.81 mV) เพราะช่วงแรงดันที่ต้องแบ่งแคบกว่า แต่ความละเอียดสูงไม่ได้แปลว่าค่าจะนิ่ง — noise ของแหล่งจ่ายและแรงดันอ้างอิงเพียงไม่กี่ mV ก็มากกว่า 0.44 mV ต่อขั้นแล้ว จึงเห็นค่า raw กระเพื่อมขึ้นลง 1–3 ขั้นได้แม้ไม่ได้หมุน pot

### เริ่มต้น ADC ด้วยโค้ดของ UI module เอง ไม่พึ่ง framework

ต่างจากบัส I2C ที่ master template เปิดไว้ให้แล้ว (ดูบทเรียน 1.1) การอ่าน potentiometer ต้อง init SAR ADC เองทั้งหมด `pot_adc_init()` ตั้งขาทั้ง 4 (P15.4–P15.7) เป็นโหมด `CY_GPIO_DM_ANALOG` ด้วย `Cy_GPIO_Pin_FastInit()` ก่อน แล้วเรียก `Cy_AutAnalog_Init(&autonomous_analog_init)` โดยใช้ config `autonomous_analog_init` ที่ BSP สร้างไว้ให้ ตามด้วย `Cy_AutAnalog_Enable()` และ `Cy_AutAnalog_StartAutonomousControl()` เพื่อให้ ADC เริ่มแปลงค่าแบบต่อเนื่องในพื้นหลัง ถ้า `Cy_AutAnalog_Init()` ไม่สำเร็จ (`CY_AUTANALOG_SUCCESS` ไม่ตรง) ทั้งสองตัวอย่างจะไม่สร้าง timer อ่านค่า และขึ้นข้อความ "ADC init failed" บนจอแทน

### แปลงค่าดิบเป็นแรงดันและเปอร์เซ็นต์ด้วยเลขจำนวนเต็ม

`update_channel()` ของ Pot Monitor อ่านผลลัพธ์ด้วย `Cy_AutAnalog_SAR_ReadResult(POT_ADC_INDEX, CY_AUTANALOG_SAR_INPUT_GPIO, channel->adc_channel)` แล้วมาสก์บิตด้วย `0x0FFFU` เผื่อบิตอื่นติดมา จากนั้นแปลงด้วยเลขจำนวนเต็มล้วน (ไม่ใช้ float): `millivolts = raw * 1800 / 4095` และ `percent_tenths = raw * 1000 / 4095` (ได้หน่วยเป็นสิบเท่าของเปอร์เซ็นต์ เพื่อพิมพ์ทศนิยมหนึ่งตำแหน่งโดยไม่ใช้ float) ตัวอย่าง: raw = 2048 → 2048×1800/4095 = 900 mV (0.900 V) และ 2048×1000/4095 = 500 (50.0%) การหารแบบจำนวนเต็มปัดเศษทิ้งเสมอ (truncate) ไม่ปัดขึ้น

### สถานะ "Live" กับ "ADC settling" บอกอะไร — และไม่บอกอะไร

`pot_timer_cb()` ตรวจ `Cy_AutAnalog_SAR_GetHSchanResultStatus(POT_ADC_INDEX)` เทียบกับ `POT_ADC_READY_MASK` (รวมมาสก์ของช่อง GPIO0–GPIO3 ทั้งสี่) ถ้าบิตพร้อมครบทั้งสี่ช่องจะขึ้น "Live" สีเขียวมิ้นต์ ถ้ายังไม่ครบขึ้น "ADC settling" สีเหลือง ข้อควรสังเกตคือฟังก์ชันนี้เรียก `update_channel()` อ่านและแสดงค่าทั้ง 4 ช่องไปแล้วในลูปก่อนหน้า โดยไม่รอสถานะนี้ก่อน สถานะ "Live/settling" จึงเป็นแค่ป้ายบอกว่าฮาร์ดแวร์ conversion ครบรอบหรือยัง ไม่ใช่ตัวคุมว่าจะอัปเดตตัวเลขบนจอหรือไม่

### กราฟเลื่อนแบบออสซิลโลสโคป: จำนวนจุด × คาบสุ่ม = ความยาวหน้าต่างเวลา

ADC Scope แปลงค่าดิบเป็นเปอร์เซ็นต์แบบง่ายกว่า Pot Monitor คือ `pct = raw * 100 / SCOPE_FULL_SCALE` (จำนวนเต็ม 0–100 ไม่มีทศนิยม) แล้วส่งเข้ากราฟด้วย `lv_chart_set_next_value()` บน `lv_chart` ที่ตั้ง `lv_chart_set_update_mode(s_chart, LV_CHART_UPDATE_MODE_SHIFT)` — โหมดนี้เลื่อนจุดเก่าออกทางซ้ายทีละจุดเมื่อจุดใหม่เข้ามาทางขวา กราฟมี `SCOPE_POINTS = 100` จุด อ่านทุก `SCOPE_PERIOD_MS = 60` ms ความยาวหน้าต่างเวลาที่มองเห็นบนกราฟจึงเท่ากับจำนวนจุดคูณคาบสุ่ม คือ 100 × 60 ms = 6 วินาที ถ้าลดคาบเหลือ 30 ms จำนวนจุดเท่าเดิมจะครอบคลุมแค่ 3 วินาที เห็นรายละเอียดเวลาเพิ่มขึ้นแต่เห็นประวัติสั้นลง

### ชื่อช่อง VR1–VR4 ไม่ได้ผูกกับ index เดียวกันเสมอ

Pot Monitor กำหนด `pot_channels[]` ให้ VR1 = ช่อง index 1 (P15.5) และ VR2 = ช่อง index 0 (P15.4) — สลับกับลำดับที่คาดตามธรรมชาติ ส่วน ADC Scope กำหนด `s_ch[] = {0, 1, 2, 3}` กับชื่อ `s_name[] = {"VR1","VR2","VR3","VR4"}` ตามลำดับ index ตรงตัว ผลคือหมุน pot ที่ขา P15.4 ตัวเดียวกัน จะเห็นการ์ด **VR2** ขยับใน Pot Monitor แต่เห็นเส้น **VR1** ขยับใน ADC Scope ทั้งที่เป็น SAR channel index 0 ตัวเดียวกัน ชื่อที่ผู้ใช้เห็นบนจอ ขาจริงบนบอร์ด และ index ผลลัพธ์ในโค้ด เป็นสามสิ่งที่ต้องตรวจให้ตรงกันเองเสมอ ไม่ควรเชื่อชื่อบนจอของตัวอย่างหนึ่งไปเทียบกับอีกตัวอย่างหนึ่งตรง ๆ

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Potentiometer Monitor** — อ่าน 4 potentiometers (P15.4–P15.7) ผ่าน AUTANALOG SAR ADC 12-bit (Vref 1.8V) แสดงเป็น bar + แรงดัน + เปอร์เซ็นต์ real-time — practise แรกที่ใช้ ADC จริงบน TESAIoT Dev Kit
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor)
- **QWA309 — 4-Channel ADC Scope** — plot ค่า pot 4 ตัว (P15.4-7, SAR 12-bit) เป็นเส้น scrolling บน LVGL chart 0-100% — analog oscilloscope
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope)

โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริงที่ commit เดียวกัน (Apache-2.0, tesaiot/developer-hub)

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — ตั้งขาเป็น analog input แล้วเริ่ม AUTANALOG SAR ADC:

```c
static bool pot_adc_init(void)
{
    uint32_t init_status;

    pot_adc_init_pin(P15_4_PORT, P15_4_PIN);
    pot_adc_init_pin(P15_5_PORT, P15_5_PIN);
    pot_adc_init_pin(P15_6_PORT, P15_6_PIN);
    pot_adc_init_pin(P15_7_PORT, P15_7_PIN);

    init_status = Cy_AutAnalog_Init(&autonomous_analog_init);
    if (CY_AUTANALOG_SUCCESS != init_status)
    {
        return false;
    }

    Cy_AutAnalog_Enable();
    Cy_AutAnalog_StartAutonomousControl();

    return true;
}
```

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — แปลงค่าดิบเป็นแรงดันและเปอร์เซ็นต์ด้วยเลขจำนวนเต็ม:

```c
raw = (uint16_t)Cy_AutAnalog_SAR_ReadResult(POT_ADC_INDEX,
                                            CY_AUTANALOG_SAR_INPUT_GPIO,
                                            channel->adc_channel);
raw &= 0x0FFFU;

millivolts = ((uint32_t)raw * POT_ADC_VREF_MV) / POT_ADC_FULL_SCALE;
percent_tenths = ((uint32_t)raw * 1000U) / POT_ADC_FULL_SCALE;
bar_value = ((uint32_t)raw * 1000U) / POT_ADC_FULL_SCALE;
```

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c) — การแมป VR1/VR2 สลับกับลำดับ index ที่คาดไว้:

```c
static pot_channel_t pot_channels[POT_COUNT] =
{
    { "VR1", "P15.5  ADC5", 1U, 0x14B8A6, NULL, NULL, NULL, NULL },
    { "VR2", "P15.4  ADC4", 0U, 0x22C55E, NULL, NULL, NULL, NULL },
    { "VR3", "P15.6  ADC6", 2U, 0xF59E0B, NULL, NULL, NULL, NULL },
    { "VR4", "P15.7  ADC7", 3U, 0xF43F5E, NULL, NULL, NULL, NULL },
};
```

[`adc_scope_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/adc_scope_ui.c) — อ่านทุกช่องแล้วส่งเข้ากราฟเลื่อนแบบ SHIFT:

```c
static void scope_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    if (!s_adc_ok) { return; }
    for (uint8_t i = 0U; i < SCOPE_CH; i++) {
        uint16_t raw = (uint16_t)Cy_AutAnalog_SAR_ReadResult(SCOPE_ADC_INDEX,
                          CY_AUTANALOG_SAR_INPUT_GPIO, s_ch[i]) & 0x0FFFU;
        uint32_t pct = ((uint32_t)raw * 100U) / SCOPE_FULL_SCALE;
        lv_chart_set_next_value(s_chart, s_series[i], (int32_t)pct);
        lv_label_set_text_fmt(s_val[i], "%s %lu%%", s_name[i], (unsigned long)pct);
    }
}
```

## จุดที่มักพลาด

- **คิดว่าแรงดันอ้างอิงคือ 3.3 V** — SAR ADC ในตัวอย่างนี้ใช้ `POT_ADC_VREF_MV = 1800` (1.8 V) ถ้าคิดผิดเป็น 3.3 V การแปลงค่าดิบเป็นแรงดันจะผิดทั้งหมด
- **เข้าใจว่าค่าที่แกว่ง 1–3 ขั้นเป็นความเสียหายของ ADC** — ที่ความละเอียด ≈0.44 mV/ขั้น สัญญาณรบกวนเพียงไม่กี่ mV ก็ทำให้ค่ากระเพื่อมได้ตามปกติ ลดได้ด้วยการเฉลี่ยหลายตัวอย่าง (moving average) ไม่ใช่อาการเสีย
- **เทียบชื่อช่อง VR1–VR4 ข้ามตัวอย่างโดยไม่ดู index จริง** — Pot Monitor กับ ADC Scope แมปชื่อกับ SAR index ไม่ตรงกัน (VR1/VR2 สลับกัน) ต้องดู `pot_channels[]`/`s_ch[]` ในโค้ดหรือ schematic ของบอร์ดเสมอ
- **รอสถานะ "Live" ก่อนเชื่อค่าบนจอ** — ป้าย Live/ADC settling เป็นแค่ตัวบอกว่า hardware conversion ครบรอบหรือยัง โค้ดอัปเดตตัวเลขบนจอทุกรอบอยู่แล้วไม่ว่าป้ายจะขึ้นว่าอะไร

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

- ADC 12 บิต ที่ Vref 1.8 V แยกแรงดันได้ละเอียดกี่มิลลิโวลต์ต่อขั้น
- ทำไมค่าที่อ่านได้กระโดดเล็กน้อยแม้ไม่ได้หมุน pot

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
