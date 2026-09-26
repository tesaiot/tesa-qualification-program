---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.3 — รับข้อความด้วย textarea และ keyboard"
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

# บทเรียน 2.3 — รับข้อความด้วย textarea และ keyboard

## lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK
2. สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown
3. อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l02`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP03 — Text Input Keyboard บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/hmi_ep03_text_input_keyboard.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — ทำไมต้องมี on-screen keyboard

บอร์ดนี้ไม่มี hardware keyboard — ต้องใช้ `lv_keyboard` widget สำเร็จรูปของ LVGL

`lv_keyboard` ไม่ทำงานเดี่ยว ๆ ต้องผูกกับ textarea ด้วย `lv_keyboard_set_textarea(kb, ta)` ให้รู้ว่าพิมพ์ลงช่องไหน

---

# แนวคิด — สองโหมดของ input

- **Input A (Realtime)** — ผูก `LV_EVENT_VALUE_CHANGED` เข้ากับ label โดยตรง เปลี่ยนทุก keystroke
- **Input B (Confirmed on OK)** — ไม่ sync label ตอนพิมพ์ อัปเดตเมื่อ `LV_EVENT_READY` ยิง (กด OK) เท่านั้น

เลือกโหมดตามว่าค่าที่ยังพิมพ์ไม่ครบจะสร้างปัญหาทันทีหรือไม่

---

# แนวคิด — callback ตัวเดียว รับหลาย event

`text_input_logic_textarea_event_cb` ผูกกับ**ทั้งสอง** textarea รับ 3 event: `CLICKED`, `FOCUSED`, `VALUE_CHANGED`

- CLICKED/FOCUSED → เปิด keyboard + ตั้ง `active_textarea = target` เสมอ
- VALUE_CHANGED → อัปเดต label **เฉพาะเมื่อ** `target == realtime_textarea`

Input B ก็ subscribe VALUE_CHANGED เหมือนกัน แต่ callback เลือกไม่ทำอะไร

---

# แนวคิด — ตอน OK อัปเดต label ไหน

callback ของ keyboard เองรับ `LV_EVENT_READY` และ `LV_EVENT_CANCEL`

เมื่อ READY เช็คว่า `active_textarea` ตอนนั้นคือ confirmed หรือ realtime แล้วอัปเดต label ฝั่งนั้น

keyboard ตัวเดียวรับใช้ทั้งสอง textarea โดยรู้จาก state ที่ตั้งไว้ตอน FOCUSED

---

# แนวคิด — dropdown เปลี่ยนมากกว่าหน้าตาแป้นพิมพ์

เลือก "Number" เรียกทั้ง `lv_keyboard_set_mode(kb, LV_KEYBOARD_MODE_NUMBER)` **และ** `lv_textarea_set_accepted_chars(target, "0123456789")`

→ บล็อกตัวอักษรอื่นไม่ให้พิมพ์เข้า textarea ได้เลย ไม่ใช่แค่เปลี่ยนปุ่มบนคีย์บอร์ด

apply กับ textarea ทั้งสองช่องพร้อมกันทุกครั้งที่ dropdown เปลี่ยน

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `gui.embedded` (ระดับ 2)
- `gui.hmi` (ระดับ 2)
- `lang.c` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — callback ของ textarea

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`text_input_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.c)

```c
if(code == LV_EVENT_CLICKED || code == LV_EVENT_FOCUSED) {
    state->active_textarea = target;
    lv_keyboard_set_textarea(state->keyboard, target);
    text_input_apply_mode_for_target(state, target);
    text_input_show_keyboard(state);
    return;
}

/* Realtime output is bound only to Input A. */
if(code == LV_EVENT_VALUE_CHANGED &&
   target == state->realtime_textarea) {
    text_input_update_realtime_label(state);
}
```

---

# ตัวอย่างสมบูรณ์ — callback ของ keyboard

```c
if(code == LV_EVENT_READY) {
    if(state->active_textarea == state->confirmed_textarea) {
        text_input_update_confirmed_label(state);
    } else if(state->active_textarea == state->realtime_textarea) {
        text_input_update_realtime_label(state);
    }
    text_input_hide_keyboard(state);
    return;
}

if(code == LV_EVENT_CANCEL) {
    text_input_hide_keyboard(state);   /* ไม่ restore ค่าเดิม */
}
```

---

# จุดที่มักพลาด

- Cancel แค่ซ่อน keyboard ไม่ได้คืนค่าตัวอักษรที่พิมพ์ไปแล้ว — ต้อง backup/restore เอง
- โหมด Number บล็อกตัวอักษรที่ textarea ด้วย ไม่ใช่แค่เปลี่ยนปุ่ม — เคลียร์ด้วย `set_accepted_chars(ta, NULL)`
- callback รับสอง textarea ต้องเช็ค `target` ก่อนอัปเดต label ไม่งั้นอัปเดตผิดตัว
- ชื่อ callback ในโค้ดจริงต่างจากที่ README ต้นทางส่วน How อธิบายไว้ — ยึดโค้ดจริงเป็นหลัก

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- event ใดบอกว่าผู้ใช้กด OK บนแป้นพิมพ์
- ช่องกรอกรหัส Wi-Fi ควรใช้แบบ realtime หรือ commit-on-OK เพราะอะไร
- โหมด number ป้องกันความผิดพลาดแบบไหน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (hmi_ep03_text_input_keyboard) ที่ commit `9a8e3ed`
