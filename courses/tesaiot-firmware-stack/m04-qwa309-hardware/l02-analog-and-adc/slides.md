---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 4.2 — อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต

## อ่านแรงดันอนาล็อกด้วย SAR ADC 12 บิต

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่าน potentiometer 4 ตัวผ่าน SAR ADC 12 บิต และแปลงเป็นแรงดันและเปอร์เซ็นต์
2. แสดงค่าเป็นกราฟเลื่อนแบบ oscilloscope และอธิบายความละเอียดของ ADC

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m01.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 10 + ฝึกตาม 25 + แล็บ 30 + เช็กความเข้าใจ 5 = 70 นาที

---

# ดูของจริงก่อน

แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดฐาน QWA309 โดยตรง — เปิดบน Developer Hub แล้ว flash เฟิร์มแวร์สำเร็จรูปดูก่อนว่าหน้าจอเป็นอย่างไร

- **QWA309 — Potentiometer Monitor** — อ่าน 4 potentiometers (P15.4–P15.7) ผ่าน AUTANALOG SAR ADC 12-bit (Vref 1.8V) แสดงเป็น bar + แรงดัน + เปอร์เซ็นต์ real-time — practise แรกที่ใช้ ADC จริงบน TESAIoT Dev Kit
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor)
- **QWA309 — 4-Channel ADC Scope** — plot ค่า pot 4 ตัว (P15.4-7, SAR 12-bit) เป็นเส้น scrolling บน LVGL chart 0-100% — analog oscilloscope
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_adc_scope) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope)

---

# แนวคิด — บอร์ดฐาน QWA309 มีอะไรให้ฝึก

potentiometer 4 ตัว (VR1–VR4 ที่ P15.4–P15.7) — สองแบบฝึกอ่านตัวเดียวกัน แต่แสดงผลต่างกัน: แผงตัวเลข+บาร์ กับ กราฟเลื่อนแบบออสซิลโลสโคป

---

# แนวคิด — SAR ADC 12 บิตคืออะไร

อ่านค่าเป็นเลข 0–4095 เทียบกับ Vref **1.8 V** (ไม่ใช่ 3.3 V) → ความละเอียด 1800/4095 ≈ 0.44 mV/ขั้น

ละเอียดกว่าที่ 3.3 V (≈0.81 mV) แต่ noise เพียงไม่กี่ mV ก็ทำให้ค่า raw กระเพื่อม 1–3 ขั้นได้ตามปกติ

---

# แนวคิด — เริ่มต้น ADC เองในโค้ด UI module

ต่างจาก I2C ที่ master template เปิดไว้ให้ (บทเรียน 1.1) ADC ต้อง init เองทั้งหมด

`Cy_GPIO_Pin_FastInit(..., CY_GPIO_DM_ANALOG, ...)` ทั้ง 4 ขา → `Cy_AutAnalog_Init()` → `Enable()` → `StartAutonomousControl()`

---

# แนวคิด — แปลงค่าดิบด้วยเลขจำนวนเต็ม

`millivolts = raw * 1800 / 4095` · `percent_tenths = raw * 1000 / 4095`

raw = 2048 → 900 mV, 50.0% — ไม่ใช้ float และการหารปัดเศษทิ้งเสมอ (truncate)

---

# แนวคิด — "Live" กับ "ADC settling" บอกอะไร

ตรวจ `Cy_AutAnalog_SAR_GetHSchanResultStatus()` ว่าครบ 4 ช่องหรือยัง — เป็นแค่ป้ายสถานะ

ตัวเลขบนจอถูกอัปเดตทุกรอบอยู่แล้ว ไม่ได้รอป้ายนี้ก่อน

---

# แนวคิด — กราฟเลื่อน: จำนวนจุด × คาบสุ่ม = ความยาวหน้าต่าง

`LV_CHART_UPDATE_MODE_SHIFT` · `SCOPE_POINTS = 100` จุด · `SCOPE_PERIOD_MS = 60` ms

หน้าต่างเวลา = 100 × 60 ms = 6 วินาที — ลดคาบเหลือ 30 ms จะเหลือ 3 วินาที

---

# แนวคิด — ชื่อช่อง VR1–VR4 ไม่ผูกกับ index เดียวกันเสมอ

Pot Monitor: VR1=index 1 (P15.5), VR2=index 0 (P15.4) — สลับกัน

ADC Scope: `s_ch[]={0,1,2,3}` ตรงตัว — หมุน pot ที่ P15.4 ตัวเดียวกัน เห็น VR2 ขยับในตัวหนึ่ง แต่ VR1 ขยับในอีกตัว

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `mcu.adc-dac` (ระดับ 2)
- `gui.hmi` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — แปลงค่าดิบด้วยเลขจำนวนเต็ม

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c)

```c
raw = (uint16_t)Cy_AutAnalog_SAR_ReadResult(POT_ADC_INDEX,
                                            CY_AUTANALOG_SAR_INPUT_GPIO,
                                            channel->adc_channel);
raw &= 0x0FFFU;

millivolts = ((uint32_t)raw * POT_ADC_VREF_MV) / POT_ADC_FULL_SCALE;
percent_tenths = ((uint32_t)raw * 1000U) / POT_ADC_FULL_SCALE;
```

---

# ตัวอย่างสมบูรณ์ — VR1/VR2 สลับ index

[`pot_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_pot_monitor/pot_monitor_ui.c)

```c
static pot_channel_t pot_channels[POT_COUNT] =
{
    { "VR1", "P15.5  ADC5", 1U, 0x14B8A6, /* ... */ },
    { "VR2", "P15.4  ADC4", 0U, 0x22C55E, /* ... */ },
    { "VR3", "P15.6  ADC6", 2U, 0xF59E0B, /* ... */ },
    { "VR4", "P15.7  ADC7", 3U, 0xF43F5E, /* ... */ },
};
```

---

# จุดที่มักพลาด

- คิดว่า Vref คือ 3.3 V — จริงคือ `POT_ADC_VREF_MV = 1800` (1.8 V)
- คิดว่าค่าแกว่ง 1–3 ขั้นคือ ADC เสีย — ที่ 0.44 mV/ขั้น noise เพียงไม่กี่ mV ก็ทำให้แกว่งได้ตามปกติ
- เทียบชื่อ VR1–VR4 ข้ามตัวอย่างโดยไม่ดู index จริง — สองตัวอย่างแมปชื่อกับ SAR index ไม่ตรงกัน
- รอป้าย "Live" ก่อนเชื่อค่าบนจอ — จริงคือจออัปเดตทุกรอบอยู่แล้วไม่ว่าป้ายจะขึ้นว่าอะไร

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

- ADC 12 บิต ที่ Vref 1.8 V แยกแรงดันได้ละเอียดกี่มิลลิโวลต์ต่อขั้น
- ทำไมค่าที่อ่านได้กระโดดเล็กน้อยแม้ไม่ได้หมุน pot

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

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)
