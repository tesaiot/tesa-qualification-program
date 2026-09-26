---
id: fw-stack.m02.l03
lang: th
title:
  th: "รับข้อความด้วย textarea และ keyboard"
  en: "Text input with a textarea and keyboard"
summary:
  th: "lv_textarea + lv_keyboard — รับ input แบบ realtime และแบบ commit-on-OK พร้อม dropdown เลือกโหมด normal / number"
  en: "Text input with a textarea and keyboard"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l02]
objectives:
  - th: "เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK"
    en: "Connect lv_textarea to lv_keyboard and take input both in real time and on OK"
  - th: "สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown"
    en: "Switch the keyboard between normal and number modes from a dropdown"
  - th: "อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน"
    en: "Explain when a value should update immediately and when it should wait for confirmation"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep03_text_input_keyboard"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# รับข้อความด้วย textarea และ keyboard

## เป้าหมาย

1. เชื่อม lv_textarea กับ lv_keyboard และรับข้อความแบบ realtime และแบบยืนยันด้วย OK
2. สลับโหมดแป้นพิมพ์ระหว่าง normal กับ number จาก dropdown
3. อธิบายว่าเมื่อไรควรอัปเดตค่าทันที และเมื่อไรควรรอให้ผู้ใช้ยืนยัน

## แนวคิด

### ทำไมต้องมี on-screen keyboard

บอร์ดนี้ไม่มี hardware keyboard ติดมา ทุกครั้งที่ผู้ใช้ต้องพิมพ์ (ชื่อ Wi-Fi, password, ค่า setpoint) ต้องเรียก
`lv_keyboard` ซึ่งเป็น widget สำเร็จรูปของ LVGL ที่วาด layout แป้นพิมพ์เองไม่ได้ทำงานแบบแยกส่วนกับ textarea แต่ต้อง
ผูกเข้าด้วยกันผ่าน `lv_keyboard_set_textarea(kb, ta)` ให้ keyboard รู้ว่ากำลังพิมพ์ลง textarea ตัวไหนอยู่

### สองโหมดของการรับ input: realtime กับ commit-on-OK

EP03 วาง textarea สองช่องคู่กันเพื่อเทียบพฤติกรรม — **Input A (Realtime)** ผูก event `LV_EVENT_VALUE_CHANGED`
เข้ากับ label แสดงผล ทำให้ label เปลี่ยนทุกครั้งที่กดปุ่มบนคีย์บอร์ด (เหมาะกับ search box หรือ preview) ส่วน
**Input B (Confirmed on OK)** ไม่ sync label ตอนพิมพ์เลย ค่าจะไปอัปเดตก็ต่อเมื่อ event `LV_EVENT_READY` ยิง (ผู้ใช้
กดปุ่ม OK บนคีย์บอร์ด) ซึ่งเหมาะกับฟอร์มที่ต้อง validate ก่อน apply เช่น WiFi password ในโมดูลถัดไป การเลือกโหมด
ขึ้นกับว่าค่าที่ผิดพลาดระหว่างพิมพ์ (เช่นพิมพ์ยังไม่ครบ) จะสร้างปัญหาให้ระบบทันทีหรือไม่ — ถ้าไม่ ใช้ realtime ได้
ถ้าใช่ ต้องรอ commit

### callback ตัวเดียวรับหลาย event: ต้องแยกด้วย event code และ target

`text_input_logic_textarea_event_cb` ถูกผูกกับ **ทั้งสอง** textarea และรับ **สาม** event
(`LV_EVENT_CLICKED`, `LV_EVENT_FOCUSED`, `LV_EVENT_VALUE_CHANGED`) ภายในฟังก์ชันเดียว ตัว callback แยกพฤติกรรมด้วย
`lv_event_get_code(e)` และ `lv_event_get_target(e)` — ถ้าเป็น CLICKED หรือ FOCUSED จะเปิด keyboard และตั้ง
`state->active_textarea = target` เสมอไม่ว่าจะเป็น textarea ไหน แต่ถ้าเป็น VALUE_CHANGED จะอัปเดต label **เฉพาะ
เมื่อ `target == state->realtime_textarea`** เท่านั้น — Input B ก็ subscribe VALUE_CHANGED เหมือนกัน แต่ callback
เลือกไม่ทำอะไรกับมัน (ปล่อยผ่าน) นี่คือเหตุผลที่ค่า A เปลี่ยนทุกตัวอักษรแต่ค่า B ไม่เปลี่ยนจนกว่าจะกด OK ทั้งที่ event
ที่ถูกยิงเหมือนกันทุกประการ

### ตอน OK: อัปเดต label ไหนขึ้นกับ `active_textarea` ตัวไหนถูกโฟกัสอยู่

`text_input_logic_keyboard_event_cb` ผูกกับตัว keyboard เอง (ไม่ใช่ textarea) รับ `LV_EVENT_READY` และ
`LV_EVENT_CANCEL` เมื่อ READY ยิง โค้ดเช็คว่า `state->active_textarea` ตอนนั้นคือ confirmed หรือ realtime
textarea แล้วอัปเดต label ของฝั่งนั้น — พูดอีกแบบคือ **keyboard ตัวเดียวรับใช้ทั้งสอง textarea** โดยรู้ว่ากำลังพิมพ์
ให้ตัวไหนอยู่จาก state ที่ callback ของ textarea ตั้งไว้ตอน FOCUSED ไม่ใช่จากการผูก callback แยกกันต่อ textarea

### dropdown เปลี่ยนโหมด ไม่ได้แค่เปลี่ยนหน้าตาแป้นพิมพ์

`text_input_apply_mode_for_target()` ถูกเรียกทั้งตอนเปลี่ยน dropdown และตอน textarea ได้ focus เมื่อเลือก
"Number" มันเรียก `lv_keyboard_set_mode(kb, LV_KEYBOARD_MODE_NUMBER)` **และ**
`lv_textarea_set_accepted_chars(target, "0123456789")` พร้อมกัน — แปลว่าโหมด Number ไม่ได้แค่เปลี่ยนปุ่มบนแป้นพิมพ์
แต่ยัง**บล็อกตัวอักษรอื่นไม่ให้พิมพ์เข้า textarea ได้เลย** แม้จะพิมพ์จาก physical keyboard ก็ตาม
`text_input_apply_mode_for_all()` เรียก apply กับ textarea ทั้งสองช่องพร้อมกันทุกครั้งที่ dropdown เปลี่ยน แม้จะ
ยังไม่ได้โฟกัสช่องไหนอยู่ก็ตาม

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) โค้ดตัวอย่างด้านล่างคัดลอกจาก tesaiot/developer-hub (Apache-2.0) ที่ commit เดียวกัน — ชื่อ callback ตรงนี้อ้างอิงจากซอร์สโค้ดจริง ไม่ใช่จากคำอธิบายในส่วน How ของ README ต้นทาง ซึ่งเรียกชื่อไว้ต่างออกไปเล็กน้อย

[`text_input_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.c) — callback ของ textarea แยก CLICKED/FOCUSED ออกจาก VALUE_CHANGED:

```c
void text_input_logic_textarea_event_cb(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    text_input_state_t *state = (text_input_state_t *)lv_event_get_user_data(e);
    lv_obj_t *target = (lv_obj_t *)lv_event_get_target(e);

    if(state == NULL || target == NULL) {
        return;
    }

    /* Keyboard opens only from input widgets (not from dropdown). */
    if(code == LV_EVENT_CLICKED || code == LV_EVENT_FOCUSED) {
        state->active_textarea = target;
        lv_keyboard_set_textarea(state->keyboard, target);
        text_input_apply_mode_for_target(state, target);
        text_input_show_keyboard(state);
        return;
    }

    /* Realtime output is bound only to Input A. */
    if(code == LV_EVENT_VALUE_CHANGED && target == state->realtime_textarea) {
        text_input_update_realtime_label(state);
    }
}
```

callback ของ keyboard เอง แยก READY (commit) กับ CANCEL:

```c
if(code == LV_EVENT_READY) {
    /* Confirm behavior depends on which input currently owns keyboard focus. */
    if(state->active_textarea == state->confirmed_textarea) {
        text_input_update_confirmed_label(state);
    } else if(state->active_textarea == state->realtime_textarea) {
        text_input_update_realtime_label(state);
    }
    text_input_hide_keyboard(state);
    return;
}

if(code == LV_EVENT_CANCEL) {
    text_input_hide_keyboard(state);
}
```

[`ui_text_input_keyboard.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.c) — การผูก event ของ Input A ทั้งสามตัวเข้ากับ callback เดียว:

```c
/* Input A: open keyboard + realtime update while typing. */
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_CLICKED, &s_text_input_state);
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_FOCUSED, &s_text_input_state);
lv_obj_add_event_cb(realtime_input, text_input_logic_textarea_event_cb, LV_EVENT_VALUE_CHANGED, &s_text_input_state);
```

Input B ลงทะเบียนสาม event เดียวกันทุกประการ (ดูไฟล์เต็ม) เพียงแต่ callback เลือกไม่ทำอะไรกับ VALUE_CHANGED ของมัน

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/main_example.c), [`text_input_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/text_input_logic.h), [`ui_text_input_keyboard.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_keyboard.h) และ [`ui_text_input_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/ui_text_input_layout.h) (layout constant ทั้งหมดเพื่อเลี่ยง magic number)

## จุดที่มักพลาด

- **คิดว่า Cancel จะคืนค่าเดิมให้ textarea** — โค้ดจริงของ `LV_EVENT_CANCEL` แค่ซ่อน keyboard เท่านั้น ไม่ได้เรียก
  API ใดเพื่อคืนค่าตัวอักษรที่พิมพ์ไปแล้ว เพราะ textarea แก้ไขตัวอักษรจริงตั้งแต่ตอนพิมพ์ (ไม่ใช่ buffer ชั่วคราว)
  ถ้าต้องการพฤติกรรม "cancel แล้วคืนค่าเดิม" ต้องเก็บ backup ข้อความเองตอน FOCUSED แล้ว restore เองใน callback
- **ลืมว่าโหมด Number บล็อกตัวอักษรที่ textarea ด้วย ไม่ใช่แค่เปลี่ยนปุ่ม** — `lv_textarea_set_accepted_chars()`
  ถูกเรียกคู่กับ `lv_keyboard_set_mode()` เสมอ ถ้าอยากให้พิมพ์ตัวอักษรอื่นได้อีกครั้งต้องเรียก
  `lv_textarea_set_accepted_chars(ta, NULL)` เพื่อล้าง filter
- **ผูก callback ของ Input A ให้ Input B โดยไม่เช็ค `target`** — เพราะ callback ตัวเดียวรับทั้งสอง textarea การ
  ลืมเช็ค `target == state->realtime_textarea` ก่อนอัปเดต label จะทำให้ label ผิดตัวอัปเดตข้าม input
- **สับสนชื่อ callback ระหว่าง README ส่วน How กับโค้ดจริง** — README ต้นทางอธิบายว่ามี callback แยกเป็น
  `text_input_logic_focus_cb`, `text_input_logic_realtime_change_cb` ฯลฯ แต่โค้ดจริงที่ commit `9a8e3ed` รวม
  ทุก event ของ textarea ไว้ใน `text_input_logic_textarea_event_cb` ฟังก์ชันเดียว — เวลาอ่านโค้ดให้ยึดโค้ดจริงเป็นหลัก

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP03 — Text Input Keyboard บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/hmi_ep03_text_input_keyboard.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- event ใดบอกว่าผู้ใช้กด OK บนแป้นพิมพ์
- ช่องกรอกรหัส Wi-Fi ควรใช้แบบ realtime หรือ commit-on-OK เพราะอะไร
- โหมด number ป้องกันความผิดพลาดแบบไหน

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep03_text_input_keyboard) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep03_text_input_keyboard&q=hmi_ep03_text_input_keyboard)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
