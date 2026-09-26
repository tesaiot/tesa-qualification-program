---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
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

# บทเรียน 4.1 — ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส

## ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง
2. นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m01.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 10 + ฝึกตาม 25 + แล็บ 30 + เช็กความเข้าใจ 5 = 70 นาที

---

# ดูของจริงก่อน

แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดฐาน QWA309 โดยตรง — เปิดบน Developer Hub แล้ว flash เฟิร์มแวร์สำเร็จรูปดูก่อนว่าหน้าจอเป็นอย่างไร

- **QWA309 — Push Button Monitor** — อ่านปุ่มกด SW9 (P17.5) และ SW10 (P17.7) แบบ active-low pull-up แสดงสถานะกด/ปล่อย + นับจำนวนครั้งบน LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor)
- **QWA309 — Hardware Button Menu** — นำทางเมนู LVGL ด้วยปุ่มกายภาพ SW6=Move SW5=Select (ไม่ใช้ touch) — headless/kiosk UX pattern
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu)

---

# แนวคิด — บอร์ดฐาน QWA309 มีอะไรให้ฝึก

ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก — บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง

สองแบบฝึกแรกใช้ปุ่มกดสองตัวเดียวกันเป็นข้อมูลเข้า แต่อ่านค่าคนละแบบ: อ่าน **สถานะปัจจุบัน** (level) เทียบกับจับ **จังหวะที่เพิ่งเปลี่ยน** (edge)

---

# แนวคิด — ปุ่มกด active-low พร้อม internal pull-up

`Cy_GPIO_Pin_FastInit(port, pin, CY_GPIO_DM_PULLUP, 1UL, HSIOM_SEL_GPIO)` เปิด pull-up ในตัวชิป ดึงขาขึ้น HIGH เมื่อไม่มีอะไรมาแตะ

ปุ่มต่อลงกราวด์เมื่อกด ขาจึงลง LOW และ `Cy_GPIO_Read()` คืนค่า 0 — เขียนเงื่อนไข "กด" เป็น `0U == Cy_GPIO_Read(...)`

---

# แนวคิด — debounce แบบนับรอบ (Push Button Monitor)

โพลทุก `BUTTON_REFRESH_PERIOD_MS = 25` ms ค่าต้องอ่านได้ระดับเดียวกันติดกัน 3 ครั้ง (`BUTTON_DEBOUNCE_TICKS = 2`) ≈ 50 ms จึงยอมรับว่าสถานะเปลี่ยนจริง

`press_count` เพิ่มเฉพาะตอนสถานะเสถียรเปลี่ยนเป็นกด · `hold_time_ms` สะสมทีละ 25 ms ขณะกดค้าง

---

# แนวคิด — จับ "ขอบขาลง" แทนสถานะค้าง (Hardware Button Menu)

`btn_pressed_edge()` debounce แบบเดียวกัน (`MENU_DEBOUNCE = 2` ที่ 30 ms) แต่คืน `true` แค่รอบที่เพิ่งเปลี่ยนจากปล่อยเป็นกด

กดค้างนานเท่าไร highlight ก็เลื่อนแค่ครั้งเดียวต่อการกด — วนด้วย `(s_sel + 1U) % MENU_ITEMS` (4 รายการ)

---

# แนวคิด — ชื่อปุ่มไม่ตรงกัน: SW9/SW10 เทียบกับ SW5/SW6

`metadata.json` และคอมเมนต์ของ Push Button Monitor เขียนว่า "SW9 (P17.5) และ SW10 (P17.7)"

แต่โค้ดจริงใน `buttons[]` ใช้ `"SW5"` (P17.7) และ `"SW6"` (P17.5) — ตรงกับ Hardware Button Menu และลายพิมพ์บนบอร์ด ให้ยึดตามโค้ด

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `mcu.gpio` (ระดับ 2)
- `gui.hmi` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — debounce แบบนับรอบ (level)

[`button_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/button_monitor_ui.c)

```c
bool sampled_pressed =
    (0U == Cy_GPIO_Read(button->port, button->pin_num));

if (sampled_pressed == button->last_sample_pressed) {
    if (button->debounce_count < BUTTON_DEBOUNCE_TICKS) {
        button->debounce_count++;
    }
} else {
    button->last_sample_pressed = sampled_pressed;
    button->debounce_count = 0U;
}

if ((button->debounce_count >= BUTTON_DEBOUNCE_TICKS) &&
    (sampled_pressed != button->stable_pressed)) {
    button->stable_pressed = sampled_pressed;   /* commit */
}
```

---

# ตัวอย่างสมบูรณ์ — จับขอบขาลง (edge)

[`hw_button_menu_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/hw_button_menu_ui.c)

```c
static bool btn_pressed_edge(btn_t *b)
{
    bool raw = (0U == Cy_GPIO_Read(b->port, b->pin));
    bool edge = false;
    if (raw == b->last) {
        if (b->cnt < MENU_DEBOUNCE) { b->cnt++; }
        if ((b->cnt >= MENU_DEBOUNCE) && (raw != b->stable)) {
            b->stable = raw;
            if (raw) { edge = true; }   /* press edge */
        }
    } else {
        b->cnt = 0U;
    }
    b->last = raw;
    return edge;
}
```

---

# จุดที่มักพลาด

- ลืมตั้ง pull-up แล้วปล่อยขาเป็น high-Z — ขาลอยตอนปล่อย ค่าจะแกว่งตามสัญญาณรบกวน
- คิดว่ากดค้างแล้วเมนูเลื่อนซ้ำ — จริงคือเลื่อนครั้งเดียวต่อการกด เพราะจับที่ edge ไม่ใช่ level
- ผสมสองรูปแบบเข้าด้วยกัน — ต้องเลือก level หรือ edge ให้ตรงกับพฤติกรรมที่ต้องการ

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

> ชื่อปุ่มในคำอธิบายของ Developer Hub (SW9/SW10) ไม่ตรงกับโค้ดของแบบฝึก (SW5/SW6) ให้ยึดตามโค้ดและลายพิมพ์บนบอร์ด

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- ทำไมปุ่ม active-low อ่านได้ 0 ตอนกด
- กดครั้งเดียวแต่ตัวนับขึ้นสองครั้ง สาเหตุคืออะไรและแก้อย่างไร

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
