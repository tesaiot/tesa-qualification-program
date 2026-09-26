---
id: fw-stack.m02.l01
lang: th
title:
  th: "หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย"
  en: "First LVGL screen: logo, title and subtitle"
summary:
  th: "หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen"
  en: "First LVGL screen: logo, title and subtitle"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง"
    en: "Build and flash this episode to the TESAIoT Dev Kit and get the screen shown in the screenshot"
  - th: "อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง"
    en: "Explain when the master template calls example_main(parent) and why we do not write main ourselves"
  - th: "สร้าง object tree screen → image → label และจัดวางด้วย align ได้"
    en: "Build a screen → image → label object tree and place it with align"
develops:
  - {skill: gui.embedded, to: 2}
  - {skill: lang.c, to: 2}
  - {skill: build.vendor-sdk, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep01_basic_label"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย

## เป้าหมาย

1. build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง
2. อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง
3. สร้าง object tree screen → image → label และจัดวางด้วย align ได้

## แนวคิด

### LVGL widget คือ `lv_obj_t *` ทั้งหมด

LVGL (Light and Versatile Graphics Library) แทน widget ทุกชนิด — screen, image, label, ปุ่ม, เมนู — ด้วย struct
เดียวกันคือ `lv_obj_t` เราจึงสร้าง เปลี่ยน style และจัดวาง widget ทุกชนิดด้วย API ชุดเดียวกันไม่ว่าจะเป็น object
แบบไหน `lv_screen_active()` (หรือชื่อเดิม `lv_scr_act()`) คืนค่า `lv_obj_t *` ของหน้าจอที่กำลังแสดงอยู่ ใช้เป็น
parent เมื่อสร้าง widget ตัวแรกของ episode

### object tree: screen → image → label

EP01 สร้าง widget สามชิ้นเรียงกันเป็นต้นไม้ที่มี screen เป็นราก คือ `screen` (พื้นหลัง) → `logo` (image, ลูกของ
screen) → `title` และ `subtitle` (label สองตัว) การจัดวางใช้สองฟังก์ชันที่ความหมายต่างกัน — `lv_obj_align(obj,
align, x, y)` จัดวาง `obj` เทียบกับ **parent** ของมันเอง ส่วน `lv_obj_align_to(obj, target, align, x, y)` จัดวาง
`obj` เทียบกับ **widget อื่น** (`target`) เป็น anchor เช่น title ถูกวางใต้ logo ด้วย `LV_ALIGN_OUT_BOTTOM_MID`
ไม่ใช่ใต้ screen ตรง ๆ — ถ้าขนาดโลโก้เปลี่ยน title ก็จะเลื่อนตามโดยอัตโนมัติ เพราะ anchor คือ widget ไม่ใช่ตำแหน่ง
พิกัดตายตัว ระยะ offset ที่ใช้คือ 24 px (โลโก้ห่างขอบบน), 48 px (title ใต้โลโก้) และ 24 px (subtitle ใต้ title)

### สีและฟอนต์: หน่วยที่โค้ดใช้จริง

สีทุกจุดตั้งด้วย `lv_color_hex(0xRRGGBB)` แปลงเลขฐานสิบหกเป็น `lv_color_t` — พื้นหลังใช้ `0x0F172A` (slate-900
จาก Tailwind palette) กับ `lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, LV_PART_MAIN)` เพื่อให้พื้นทึบแสงเต็ม
(`LV_OPA_COVER` = ค่าความทึบสูงสุด) `LV_PART_MAIN` หมายถึงส่วนหลักของ widget ที่ style นี้จะไปลง ฟอนต์ต้องเป็น
Montserrat ที่ถูกเปิดไว้ใน `lv_conf.h` ของ master แล้วเท่านั้น (episode นี้ใช้ 30 px กับ title และ 20 px กับ
subtitle) เลือกขนาดที่ไม่ได้เปิดไว้จะ compile ไม่ผ่านหรือ fallback ไปฟอนต์อื่นเงียบ ๆ

### ทำไมโลโก้ต้องฝังเป็น C array ไม่ใช่โหลดจากไฟล์

บอร์ดนี้ไม่มีไฟล์ระบบหรือ SD card ให้ LVGL เปิดไฟล์ภาพตอน runtime รูปโลโก้จึงถูกแปลงล่วงหน้าเป็น
`lv_image_dsc_t APP_LOGO` — struct ที่เก็บทั้ง header (ขนาด, color format) และ pixel data ดิบ — คอมไพล์ฝังรวมเข้า
ไปใน flash image เดียวกับโปรแกรม `lv_image_set_src(logo, &APP_LOGO)` จึงรับ pointer ไปยังข้อมูลใน flash ตรง ๆ
ไม่มีการอ่านไฟล์ ไม่มี latency ของ I/O และไม่มี dependency กับ filesystem ใด ๆ

### สัญญาการเข้า-ออกของ episode

master template (ดูบทเรียน 1.1) เรียก `example_main(lv_scr_act())` เพียงครั้งเดียวหลัง FreeRTOS, display driver,
VGLite GPU และ LVGL พร้อมหมดแล้ว `main_example.c` ของ episode นี้ implement `example_main()` แบบ strong แล้ว
forward ต่อไปที่ `ui_ep01_basic_label_create()` ทันที โดยไม่ใช้ค่า `parent` ที่ได้รับมาตรง ๆ (มี `(void)parent;`
กำกับไว้) เพราะฟังก์ชันสร้าง UI เรียก `lv_screen_active()` เองภายใน — ออกแบบไว้แบบนี้เพื่อให้ episode อื่น copy
โค้ดสร้าง UI ไปใช้ได้โดยไม่ต้องแก้ signature นอกจากนี้ `main_example.c` ยังเรียก
`tesaiot_add_thai_support_badge()` ก่อนสร้างหน้าจอของ episode — เป็นฟังก์ชันช่วยของ master ที่ยืนยันว่าไฟล์ฟอนต์
Noto Sans Thai ถูก bundle มาพร้อมแล้ว ไม่ได้เป็นส่วนหนึ่งของ UI tree ที่ EP01 สอน หลัง `example_main()` return
master จะวน `lv_timer_handler()` ให้ตลอดไปเพื่อ redraw — EP01 ไม่มี event หรือ timer ของตัวเอง จึงวาดครั้งเดียว
แล้วค้างภาพนั้นไว้

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) อ่าน **Why / What / How** ฉบับเต็มก่อนใน [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) โค้ดตัวอย่างด้านล่างคัดลอกจาก tesaiot/developer-hub (Apache-2.0) ที่ commit เดียวกัน

[`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/main_example.c) — จุดที่ master ส่ง control เข้ามา:

```c
void example_main(lv_obj_t *parent)
{
    /* Master template bundles Noto Sans Thai fonts — this badge
     * confirms to the developer that Thai rendering is available. */
    tesaiot_add_thai_support_badge();

    (void)parent;   /* The episode manages its own screen composition via lv_screen_active(). */

    ui_ep01_basic_label_create();
}
```

[`ui_ep01_basic_label.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c) — สร้าง object tree ทั้งหมดของ episode:

```c
lv_obj_t *screen = lv_screen_active();
lv_obj_set_style_bg_color(screen, lv_color_hex(0x0F172A), LV_PART_MAIN);
lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, LV_PART_MAIN);

lv_obj_t *logo = lv_image_create(screen);
lv_image_set_src(logo, &APP_LOGO);
lv_obj_align(logo, LV_ALIGN_TOP_MID, 0, 24);

lv_obj_t *title = lv_label_create(screen);
lv_label_set_text(title, "EP01 - Basic Label");
lv_obj_set_style_text_color(title, lv_color_hex(0xF8FAFC), LV_PART_MAIN);
lv_obj_set_style_text_font(title, &lv_font_montserrat_30, LV_PART_MAIN);
lv_obj_align_to(title, logo, LV_ALIGN_OUT_BOTTOM_MID, 0, 48);
```

สังเกต API ที่สำคัญ — `lv_image_create(parent)` สร้าง image widget ที่มี `screen` เป็น parent, `lv_image_set_src()`
รับ pointer ไปยัง `lv_image_dsc_t` ที่ฝังใน flash (ไม่ใช่ path ไฟล์), `lv_obj_align()` จัดวางเทียบกับ parent ส่วน
`lv_obj_align_to()` จัดวางเทียบกับ widget อื่นเป็น anchor — ไฟล์เต็มยังมี `subtitle` อีกหนึ่ง label ที่วางด้วย
รูปแบบเดียวกัน ให้ดูใน [ไฟล์เต็มบน Developer Hub](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c)

- [`ui_ep01_basic_label.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.h) — ประกาศ `ui_ep01_basic_label_create(void)` ตัวเดียว

## จุดที่มักพลาด

- **ใช้ `lv_obj_align()` แทน `lv_obj_align_to()`** — ถ้าอยากวาง title เทียบกับโลโก้ (ซึ่งอาจเปลี่ยนขนาด) ต้องใช้
  `lv_obj_align_to(title, logo, ...)` ไม่ใช่ `lv_obj_align(title, ...)` ซึ่งจะจัดวางเทียบกับ `screen` แทน
- **ลืมเปิดขนาดฟอนต์ใน `lv_conf.h`** — `lv_font_montserrat_30`/`_20` ต้องถูกเปิดไว้ในโปรเจกต์ master ก่อน ถ้า
  episode เลือกขนาดที่ไม่ได้เปิดจะ build ไม่ผ่านหรือได้ฟอนต์อื่นแทนแบบไม่มี error ชัดเจน
- **คิดว่าต้องใช้ `parent` ที่ได้รับมาตรง ๆ** — โค้ดใน `main_example.c` ใส่ `(void)parent;` เพราะฟังก์ชันสร้าง UI
  เรียก `lv_screen_active()` เองข้างใน ทั้งสองค่าคือ active screen เดียวกัน แต่การไม่ใช้ `parent` ตรง ๆ ทำให้
  episode พกไปวางในโปรเจกต์อื่นได้โดยไม่ต้องแก้ signature ของฟังก์ชันสร้าง UI

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP01 — Basic Label บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/hmi_ep01_basic_label.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- master template ทำอะไรให้เราแล้วบ้างก่อนเรียก example_main()
- ทำไมโลโก้ถูกฝังเป็น C array (APP_LOGO) แทนการโหลดจากไฟล์
- ถ้าอยากย้าย title ลงอีก 20 px ต้องแก้ค่าใดในโค้ด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
