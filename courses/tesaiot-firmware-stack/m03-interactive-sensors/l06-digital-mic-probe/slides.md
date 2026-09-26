---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.6 — ไมโครโฟน PDM สเตอริโอและ level meter"
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

# บทเรียน 3.6 — ไมโครโฟน PDM สเตอริโอและ level meter

## เก็บสัญญาณเสียงจากไมโครโฟน PDM สเตอริโอบนบอร์ด คำนวณระดับความดังซ้าย/ขวาแล้วแสดงเป็น level meter บนจอ LVGL

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เก็บสัญญาณจากไมโครโฟน PDM สเตอริโอ และคำนวณระดับเสียงซ้าย/ขวา
2. แสดงระดับเสียงเป็น level meter และอธิบายว่าคำนวณแบบ peak หรือ RMS
3. ทดสอบด้วยเสียงจากซ้ายและขวา แล้วยืนยันว่าช่องสัญญาณไม่สลับกัน

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m03.l05`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP06 — Digital Mic Probe บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/int_ep06_digital_mic_probe.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — PDM vs PCM

PDM: สตรีม 1 บิต 1-3 MHz ที่ความหนาแน่นของ pulse แทนขนาดสัญญาณ — ไมค์ MEMS ส่งแบบนี้ตรง ๆ

ชิปแปลง PDM→PCM ในฮาร์ดแวร์ (lowpass+decimate) — episode นี้ตั้ง 16 kHz, เฟรมละ 160 ตัวอย่าง/ช่อง (= 10 ms)

---

# แนวคิด — จับสัญญาณด้วย interrupt ไม่ใช่ DMA

README ต้นทาง: "DMA-driven — CPU ไม่ต้องยุ่ง"

**โค้ดจริง**: interrupt ต่อช่อง (ซ้าย=ch2, ขวา=ch3) ยิงเมื่อ FIFO ถึง trigger level → อ่านทีละตัวอย่างด้วย `Cy_PDM_PCM_Channel_ReadFifo()`

double-buffer (`buffer0`/`buffer1`) จัดการเองในซอฟต์แวร์ ไม่ใช่ DMA descriptor

---

# แนวคิด — avg คือ mean(|x|) ไม่ใช่ RMS

`compute_level()`: `peak_abs` + `avg_abs` = Σ|x| / N — **ไม่มีการยกกำลังสอง** จึงไม่ใช่ RMS

ขึ้นลงคล้าย RMS คำนวณเบากว่า แต่ต่ำกว่า RMS เสมอ (sine wave: mean|x| ≈ 0.9× RMS)

---

# แนวคิด — % บนจอ clamp floor/ceiling ไม่ใช่ avg/32767

คอมเมนต์ในซอร์ส: "Tuned for classroom speech level so UI% doesn't saturate too early"

`avg_abs` ≤ 80 → 0% · ≥ 8000 → 100% · ระหว่างนั้น scale เชิงเส้น — เสียงพูดเบา ๆ เต็มแถบได้จริง

---

# แนวคิด — balance meter ทำไว้แล้ว + UI poll ไม่ใช่ async_call

- `balance_lr = (L_avg-R_avg)*100/(L_avg+R_avg)` มีอยู่แล้ว ไม่ใช่แค่ "ลองแก้" ตาม README ต้นทาง
- UI ใช้ `lv_timer` poll ทุก 50 ms (20 Hz ไม่ใช่ 50 Hz) แบบ "sample ล่าสุดชนะ" — เสียงกระแทกสั้น <10ms อาจไม่ขึ้นบนจอ

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sys.dsp` (ระดับ 2)
- `sys.sensors-actuators` (ระดับ 2)
- `gui.hmi` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — % แบบ floor/ceiling

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`pdm_probe_logger.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_audio/pdm/pdm_probe_logger.c)

```c
/* Tuned for classroom speech level so UI% doesn't
 * saturate too early. */
#define PDM_UI_FLOOR_ABS              (80U)
#define PDM_UI_CEIL_ABS               (8000U)

static uint32_t to_ui_pct(uint32_t avg_abs)
{
    if (avg_abs <= PDM_UI_FLOOR_ABS) { return 0U; }
    if (avg_abs >= PDM_UI_CEIL_ABS)  { return 100U; }
    return ((avg_abs - PDM_UI_FLOOR_ABS) * 100U) /
           (PDM_UI_CEIL_ABS - PDM_UI_FLOOR_ABS);
}
```

---

# ตัวอย่างสมบูรณ์ — UI poll แบบ latest-sample-wins

[`mic_presenter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/app_ui/mic/mic_presenter.c)

```c
static void mic_presenter_ui_timer_cb(lv_timer_t *timer)
{
    mic_presenter_sample_t local = {0};
    bool has_sample = false;

    taskENTER_CRITICAL();
    has_sample = s_has_sample;
    if (has_sample) { local = s_latest_sample; }
    taskEXIT_CRITICAL();

    if (has_sample && s_view_ready) {
        mic_view_apply(&local);
    }
}
```

---

# จุดที่มักพลาด

- คิดว่าใช้ DMA — จริงคือ interrupt อ่าน FIFO + double-buffer ซอฟต์แวร์
- คิดว่า avg คือ RMS — จริงคือ mean(|x|) ไม่มีการยกกำลังสอง
- คิดว่า % มาจาก avg/32767 ตรง ๆ — จริง clamp ผ่านช่วง 80-8000
- คิดว่า UI จับเสียงกระแทกสั้นได้ทุกครั้ง — "sample ล่าสุดชนะ" อาจพลาดเฟรมสั้น ๆ

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- PDM ต่างจาก PCM อย่างไร
- RMS กับ peak ให้ภาพระดับเสียงต่างกันอย่างไร
- ทดสอบอย่างไรว่าช่องซ้ายและขวาไม่สลับกัน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/int_ep06_digital_mic_probe) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--int_ep06_digital_mic_probe&q=int_ep06_digital_mic_probe)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (int_ep06_digital_mic_probe) ที่ commit `9a8e3ed`
