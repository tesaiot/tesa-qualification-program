---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET"
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

# บทเรียน 2.2 — ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET

## ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT
2. แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น
3. เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP02 — Button Event บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/hmi_ep02_button_event.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — event-driven programming ใน LVGL

`lv_obj_add_event_cb(obj, callback, filter, user_data)` ผูก event callback

- `filter` กำหนดชนิด event (`LV_EVENT_PRESSED`, `LV_EVENT_LONG_PRESSED_REPEAT`, ...)
- `user_data` คือ pointer ที่เราส่งเอง อ่านกลับด้วย `lv_event_get_user_data(e)`
- แทนที่ global variable — callback ตัวเดียวรับใช้หลายปุ่มพร้อมกันได้

---

# แนวคิด — tap กับ hold ต่างกันที่ event

- `LV_EVENT_PRESSED` — ยิงทันทีที่แตะลง ไม่ต้องรอปล่อย
- `LV_EVENT_LONG_PRESSED_REPEAT` — ยิงซ้ำทุก N ms ตอนกดค้าง (`LV_INDEV_DEF_LONG_PRESS_REP_TIME` ใน `lv_conf.h`)

EP02 ผูก callback เดียวกันกับทั้งสอง event (register สองครั้ง) แล้วเช็ค `lv_event_get_code(e)` เพื่อเลือก delta

---

# แนวคิด — แยก UI ออกจาก logic

`ui_button_counter.c` รู้จัก LVGL เต็มตัว แต่ `counter_logic.c` รู้จักแค่ `lv_obj_t *` ของ label กับ state ของตัวเอง

ปุ่ม UP กับ DOWN **ใช้ callback ตัวเดียวกัน** ต่างกันแค่ payload (`tap_delta`/`hold_repeat_delta`) ที่ส่งผ่าน `user_data`

เพิ่มปุ่มใหม่ที่ใช้ logic เดิม = สร้าง action struct ใหม่ ไม่ต้องเขียน callback ใหม่

---

# แนวคิด — ทำไม state ต้องเป็น `static`

`s_counter_state`, `s_up_action`, `s_down_action` เป็นตัวแปร `static` ระดับไฟล์

`lv_obj_add_event_cb()` เก็บ **pointer** ของ `user_data` ไว้เรียกทีหลัง (ตอนผู้ใช้กดปุ่ม — นานหลังฟังก์ชันสร้าง UI return แล้ว)

ถ้าเป็นตัวแปร local บน stack จะตายทันทีที่ฟังก์ชัน return → callback อ่าน dangling pointer

---

# แนวคิด — flex layout และโลโก้ scale

- `lv_obj_set_layout(row, LV_LAYOUT_FLEX)` + `LV_FLEX_FLOW_ROW` เรียงปุ่มซ้าย→ขวาอัตโนมัติ
- `lv_obj_set_style_pad_column(row, 20, ...)` เว้นช่องไฟระหว่างปุ่ม
- ปุ่มใช้ label-on-button pattern: label เป็นลูกของปุ่ม จัดกึ่งกลางด้วย `lv_obj_align`
- `lv_image_set_scale(logo, 128)` — LVGL ใช้ 256 = 1.0x ดังนั้น 128 = 0.5x

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `gui.embedded` (ระดับ 2)
- `prog.design-patterns` (ระดับ 1)
- `lang.c` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — `counter_logic_button_event_cb`

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`counter_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.c)

```c
void counter_logic_button_event_cb(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    counter_button_action_t *action =
        (counter_button_action_t *)lv_event_get_user_data(e);

    if(action == NULL || action->state == NULL) {
        return;
    }
    if(code == LV_EVENT_PRESSED) {
        counter_logic_apply_delta(action->state, action->tap_delta);
        return;
    }
    if(code == LV_EVENT_LONG_PRESSED_REPEAT) {
        counter_logic_apply_delta(action->state, action->hold_repeat_delta);
    }
}
```

---

# ตัวอย่างสมบูรณ์ — ผูกปุ่ม UP กับ callback

[`ui_button_counter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.c)

```c
/* Event payload: tap +1, hold-repeat +5. */
s_up_action.state = &s_counter_state;
s_up_action.tap_delta = 1;
s_up_action.hold_repeat_delta = 5;
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb,
                    LV_EVENT_PRESSED, &s_up_action);
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb,
                    LV_EVENT_LONG_PRESSED_REPEAT, &s_up_action);
```

ปุ่ม DOWN เรียก callback **ตัวเดียวกัน** แค่ส่ง `s_down_action` ที่ `tap_delta = -1` แทน

---

# จุดที่มักพลาด

- ส่ง `user_data` เป็นตัวแปร local (stack) → ต้อง `static`/global เพราะ callback เก็บ pointer ไว้ใช้ทีหลัง
- ปุ่ม RESET เช็คทั้ง `LV_EVENT_PRESSED` และ `LV_EVENT_CLICKED` ต่างจาก UP/DOWN ที่เช็คแค่ `LV_EVENT_PRESSED`
- ต้อง register `lv_obj_add_event_cb()` **สองครั้ง** คนละ filter เพื่อรับทั้ง tap และ hold
- `lv_image_set_scale` ใช้ฐาน 256 ไม่ใช่ 100 — 128 คือ 0.5x ไม่ใช่ 128%

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- LV_EVENT_PRESSED กับ LV_EVENT_LONG_PRESSED_REPEAT ต่างกันอย่างไรเมื่อกดค้าง
- counter_logic.c รู้จัก LVGL หรือไม่ และทำไมจึงออกแบบแบบนั้น
- ถ้าตัวนับต้องไม่ติดลบ ควรแก้ที่ไฟล์ใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (hmi_ep02_button_event) ที่ commit `9a8e3ed`
