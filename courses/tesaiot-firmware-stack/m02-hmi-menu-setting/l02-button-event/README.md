---
id: fw-stack.m02.l02
lang: th
title:
  th: "ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
summary:
  th: "ปุ่ม UP / DOWN / RESET ที่ตอบสนองต่อ LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT — แยก UI logic ออกจาก counter logic"
  en: "Buttons and event callbacks: an UP / DOWN / RESET counter"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l01]
objectives:
  - th: "ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT"
    en: "Attach event callbacks to buttons with LV_EVENT_PRESSED and LV_EVENT_LONG_PRESSED_REPEAT"
  - th: "แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น"
    en: "Separate UI logic from counter logic into different files and explain why that makes testing easier"
  - th: "เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้"
    en: "Add one new button that reuses the same logic"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: prog.design-patterns, to: 1}
  - {skill: lang.c, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep02_button_event"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# ปุ่มและ event callback: ตัวนับ UP / DOWN / RESET

## เป้าหมาย

1. ผูก event callback กับปุ่มด้วย LV_EVENT_PRESSED และ LV_EVENT_LONG_PRESSED_REPEAT
2. แยก UI logic ออกจาก counter logic เป็นคนละไฟล์ และอธิบายว่าทำไมจึงทดสอบง่ายขึ้น
3. เพิ่มปุ่มใหม่หนึ่งปุ่มที่ใช้ logic ชุดเดิมได้

## แนวคิด

### event-driven programming ใน LVGL

หลัง EP01 ที่วาดหน้าจอ static ล้วน ๆ EP02 เพิ่มสิ่งที่ GUI แบบ embedded ทุกตัวต้องมีคือ **event callback** — ฟังก์ชันที่
LVGL เรียกเองเมื่อ event ตาม filter ที่เราลงทะเบียนไว้เกิดขึ้น ผูกด้วย `lv_obj_add_event_cb(obj, callback, filter,
user_data)` โดย `filter` กำหนดว่าจะรับ event ชนิดไหน (`LV_EVENT_PRESSED`, `LV_EVENT_LONG_PRESSED_REPEAT`,
`LV_EVENT_CLICKED` ฯลฯ) และ `user_data` คือ pointer ที่เราส่งเข้าไปเอง เพื่อให้ callback อ่านกลับออกมาได้ด้วย
`lv_event_get_user_data(e)` — เทคนิคนี้แทนที่การใช้ global variable เพราะปุ่มแต่ละปุ่มส่ง `user_data` ของตัวเองได้
โดย callback ตัวเดียวกันรับใช้หลายปุ่มพร้อมกัน

### tap กับ hold ต่างกันที่ event คนละตัว

`LV_EVENT_PRESSED` ยิงทันทีที่นิ้วแตะลงบน widget ไม่ต้องรอปล่อย ส่วน `LV_EVENT_LONG_PRESSED_REPEAT` ยิงซ้ำทุก N
มิลลิวินาทีตราบใดที่ยังกดค้างอยู่ (ค่า N ตั้งใน `lv_conf.h` ด้วย `LV_INDEV_DEF_LONG_PRESS_REP_TIME`) EP02 ผูก
callback ตัวเดียวกันเข้ากับทั้งสอง event ของปุ่มเดียวกัน (สอง `lv_obj_add_event_cb()` แยกกัน) แล้วให้ callback
เช็ค `lv_event_get_code(e)` เพื่อเลือก delta คนละค่า — tap ปกติขยับ 1 หน่วย ส่วนกดค้างขยับ 5 หน่วยต่อครั้งที่ event
ซ้ำ

### แยก UI ออกจาก logic: ทำไมถึงสำคัญ

ไฟล์ `ui_button_counter.c` รู้จัก LVGL เต็มตัว (สร้าง widget, จัดสี, จัดวาง) แต่ `counter_logic.c` **ไม่ include
`lvgl.h` เพื่อเรียก widget API โดยตรง** — มันรู้จักแค่ `lv_obj_t *` ของ label ที่ต้องอัปเดตข้อความ และมี state
เป็น `struct` ของตัวเอง (`counter_state_t`) แยกจาก UI การออกแบบนี้ทำให้ปุ่ม UP กับ DOWN **ใช้ callback ตัวเดียวกัน
ได้** (`counter_logic_button_event_cb`) ต่างกันแค่ payload ที่ส่งผ่าน `user_data` (`tap_delta`/`hold_repeat_delta`
เป็นบวกหรือลบ) — เพิ่มปุ่มใหม่ที่ใช้ logic เดิมจึงทำได้โดยไม่ต้องเขียน callback ใหม่เลย แค่สร้าง
`counter_button_action_t` ตัวใหม่แล้วผูกปุ่มเข้ากับ callback เดิม

### state เก็บที่ไหน และทำไมต้องเป็น `static`

`s_counter_state`, `s_up_action`, `s_down_action` ใน `ui_button_counter.c` เป็นตัวแปร **`static`** ระดับไฟล์ ไม่ใช่
ตัวแปร local ในฟังก์ชัน `ui_button_counter_create()` เหตุผลคือ `lv_obj_add_event_cb()` เก็บ **pointer** ของ
`user_data` ไว้เรียกใช้ภายหลัง (ทุกครั้งที่ผู้ใช้กดปุ่ม ซึ่งเกิดขึ้นนานหลังจากฟังก์ชันสร้าง UI คืนค่าไปแล้ว) ถ้า
`s_up_action` เป็นตัวแปร local บน stack มันจะถูกทำลายทันทีที่ `ui_button_counter_create()` return ทำให้ callback
อ่าน pointer ที่ตายไปแล้ว (dangling pointer) `counter_logic_init()` เองก็แค่เก็บ pointer ของ label ไว้ใน state
ไม่ได้ copy ข้อมูล จึงต้องอัปเดตผ่าน `state->value_label` ทุกครั้งด้วยเหตุผลเดียวกัน

### จัดปุ่มเป็นแถวด้วย flex layout

แถวปุ่มสามตัวใช้ `lv_obj_set_layout(btn_row, LV_LAYOUT_FLEX)` ร่วมกับ `lv_obj_set_flex_flow(btn_row,
LV_FLEX_FLOW_ROW)` ให้ LVGL เรียงลูกซ้ายไปขวาให้อัตโนมัติแบบ CSS flexbox ไม่ต้องคำนวณตำแหน่ง `x` ของแต่ละปุ่มเอง
`lv_obj_set_flex_align(..., LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER)` จัดกึ่งกลางทั้งแนว
หลักและแนวขวาง และ `lv_obj_set_style_pad_column(btn_row, 20, LV_PART_MAIN)` เว้นช่องไฟระหว่างปุ่ม 20 px ปุ่มแต่ละ
ใบยังใช้ label-on-button pattern คือสร้าง `lv_label_create(btn)` เป็นลูกของปุ่มแล้ว `lv_obj_align(lbl,
LV_ALIGN_CENTER, 0, 0)` เพื่อวางข้อความกึ่งกลางปุ่ม

### โลโก้ย่อขนาดด้วย `lv_image_set_scale`

`lv_image_set_scale(logo, 128)` ย่อโลโก้ลงครึ่งหนึ่ง เพราะ LVGL ใช้ **256 แทน 1.0x** (fixed-point scale) ค่า 128
จึงเท่ากับ 0.5x — ต่างจาก EP01 ที่ใช้โลโก้ขนาดเต็มไม่มีการ scale

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) โค้ดตัวอย่างด้านล่างคัดลอกจาก tesaiot/developer-hub (Apache-2.0) ที่ commit เดียวกัน

[`counter_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.c) — callback ตัวเดียวรองรับทั้ง tap และ hold โดยแยกด้วย event code:

```c
void counter_logic_button_event_cb(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    counter_button_action_t *action = (counter_button_action_t *)lv_event_get_user_data(e);

    if(action == NULL || action->state == NULL) {
        return;
    }

    if(code == LV_EVENT_PRESSED) {
        counter_logic_apply_delta(action->state, action->tap_delta);
        counter_logic_log_action("TAP", action->tap_delta, action->state->value);
        return;
    }

    if(code == LV_EVENT_LONG_PRESSED_REPEAT) {
        counter_logic_apply_delta(action->state, action->hold_repeat_delta);
        counter_logic_log_action("HOLD_REPEAT", action->hold_repeat_delta, action->state->value);
    }
}
```

[`ui_button_counter.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/ui_button_counter.c) — ปุ่ม UP ผูกกับ callback เดียวกันสองครั้ง คนละ event:

```c
/* Event payload: tap +1, hold-repeat +5. */
s_up_action.state = &s_counter_state;
s_up_action.tap_delta = 1;
s_up_action.hold_repeat_delta = 5;
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb, LV_EVENT_PRESSED, &s_up_action);
lv_obj_add_event_cb(btn_up, counter_logic_button_event_cb, LV_EVENT_LONG_PRESSED_REPEAT, &s_up_action);
```

สังเกตว่า `s_up_action` เป็นตัวแปร `static` ระดับไฟล์ (ดูเหตุผลในแนวคิดด้านบน) และปุ่ม DOWN เรียก
`counter_logic_button_event_cb` **ตัวเดียวกัน** เพียงแค่ส่ง `s_down_action` ที่มี `tap_delta = -1` แทน — ไม่มี
callback ใหม่ให้เขียน

[`counter_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/counter_logic.h) และ [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/main_example.c) มีโครงเดียวกับ EP01 คือ forward ไปที่ `ui_button_counter_create()`

## จุดที่มักพลาด

- **ส่ง `user_data` เป็นตัวแปร local (stack)** — ต้องเป็น `static` หรือ global เพราะ `lv_obj_add_event_cb()` เก็บ
  pointer ไว้เรียกใช้ทีหลัง ถ้าเป็นตัวแปรบน stack มันจะตายไปตั้งแต่ฟังก์ชันสร้าง UI return แล้ว callback จะอ่าน
  pointer ที่ dangling
- **ลืมว่าปุ่ม RESET เช็คทั้ง `LV_EVENT_PRESSED` และ `LV_EVENT_CLICKED`** — ต่างจากปุ่ม UP/DOWN ที่เช็คแค่
  `LV_EVENT_PRESSED` เพียงอย่างเดียว ถ้า copy callback ของ UP/DOWN ไปทำปุ่มใหม่ที่ต้องการพฤติกรรมแบบ RESET ต้องดู
  ว่าจะเช็ค event code ไหนบ้างให้ตรงกับพฤติกรรมที่ต้องการ
- **คิดว่าต้อง `lv_obj_add_event_cb()` ครั้งเดียวเพื่อรับทั้ง tap และ hold** — ต้อง register **สองครั้ง** คนละ
  `filter` (`LV_EVENT_PRESSED` กับ `LV_EVENT_LONG_PRESSED_REPEAT`) เพราะ `filter` รับ event code เดียวต่อการเรียก
  หนึ่งครั้ง
- **ลืมว่า `lv_image_set_scale` ใช้ฐาน 256 ไม่ใช่ 100** — 256 = 1.0x ไม่ใช่เปอร์เซ็นต์ ค่า 128 คือ 0.5x ไม่ใช่ 128%

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP02 — Button Event บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/hmi_ep02_button_event.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- LV_EVENT_PRESSED กับ LV_EVENT_LONG_PRESSED_REPEAT ต่างกันอย่างไรเมื่อกดค้าง
- counter_logic.c รู้จัก LVGL หรือไม่ และทำไมจึงออกแบบแบบนั้น
- ถ้าตัวนับต้องไม่ติดลบ ควรแก้ที่ไฟล์ใด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep02_button_event) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep02_button_event&q=hmi_ep02_button_event)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
