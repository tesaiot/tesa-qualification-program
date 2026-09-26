---
id: fw-stack.m02.l04
lang: th
title:
  th: "โครง navigation: แถบเมนู หน้า และการสลับหน้า"
  en: "Navigation shell: menu bar, pages and page routing"
summary:
  th: "โครง navigation หลัก — top nav bar พร้อมปุ่มสลับหน้า + icon action buttons + หน้าต่าง ๆ ที่ lv_menu สร้างไว้ครั้งเดียวแล้วสลับตามเมนูที่เลือก (README ของ episode เล่าแบบ stage container แต่โค้ดใช้ lv_menu ให้ยึดตามโค้ด)"
  en: "Navigation shell: menu bar, pages and page routing"
level: L2
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l03]
objectives:
  - th: "สร้างเมนูนำทางด้วย lv_menu ที่สร้างทุกหน้าไว้ครั้งเดียว แล้วสลับหน้าที่แสดงตามเมนูที่เลือก"
    en: "Build navigation with lv_menu that creates every page once and switches the visible page from the menu"
  - th: "แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode"
    en: "Keep layout, navigation logic and pages apart, following the episode file structure"
  - th: "เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่"
    en: "Add one page to the menu without changing the existing pages"
develops:
  - {skill: gui.hmi, to: 2}
  - {skill: prog.design-patterns, to: 2}
  - {skill: prog.state-machines, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep04_menu_navigation"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# โครง navigation: แถบเมนู หน้า และการสลับหน้า

## เป้าหมาย

1. สร้างเมนูนำทางด้วย lv_menu ที่สร้างทุกหน้าไว้ครั้งเดียว แล้วสลับหน้าที่แสดงตามเมนูที่เลือก
2. แยก layout, navigation logic และหน้าแต่ละหน้าออกจากกันตามโครงไฟล์ของ episode
3. เพิ่มหน้าใหม่หนึ่งหน้าเข้าเมนูโดยไม่แก้หน้าที่มีอยู่

## แนวคิด

### โค้ดจริงใช้ widget `lv_menu` ไม่ใช่ container สี่ชั้นตามที่ README ต้นทางอธิบาย

README ของ episode บน Developer Hub ส่วน How เล่าว่าโค้ดสร้าง header/nav/stage/footer เป็น container เปล่าสี่อัน
แล้ว `lv_obj_clean()` + rebuild เนื้อหาเองทุกครั้งที่สลับหน้า แต่โค้ดจริงที่ commit `9a8e3ed` ใช้
**`lv_menu`** ซึ่งเป็น widget สำเร็จรูปของ LVGL สำหรับทำ multi-page navigation โดยเฉพาะ — สร้างทุกหน้าไว้ล่วงหน้า
ด้วย `lv_menu_page_create(menu, title)` แล้วสลับการแสดงผลด้วย `lv_menu_set_page(menu, target_page)` โดยไม่ต้องลบ
หรือสร้าง widget ใหม่เลยสักครั้ง บทเรียนนี้อธิบายตามโค้ดจริง ไม่ใช่ตามคำบรรยายในส่วน How ของ README ต้นทาง

### โครงหน้าจอ: header คงที่ + top nav คงที่ + `lv_menu` ตรงกลาง + footer

`ui_menu_navigation_create()` จัดหน้าจอเป็นคอลัมน์แนวตั้งด้วย `LV_FLEX_FLOW_COLUMN` ประกอบด้วย header (ไอคอน
settings + หัวเรื่อง), top nav (ปุ่ม Home/WiFi/Display/Info/Back ที่ "แสดงตลอดเวลาเพื่อให้นำทางง่ายในชั้นเรียน"
ตามคอมเมนต์ในซอร์ส), พื้นที่ content ที่มี `lv_menu` วางอยู่ข้างใน และ footer status strip ตัว `lv_menu` เองถูก
ตั้งค่า `lv_menu_set_mode_header(menu, LV_MENU_HEADER_TOP_FIXED)` และ
`lv_menu_set_mode_root_back_button(menu, LV_MENU_ROOT_BACK_BUTTON_DISABLED)` แล้วซ่อน header ภายในของมันเองทั้งสอง
จุด (`lv_menu_get_main_header()`, `lv_menu_get_sidebar_header()`) ด้วย `LV_OBJ_FLAG_HIDDEN` เพราะ header กับ top nav
ที่เราวาดเองด้านนอกทำหน้าที่แทนไปแล้ว — ถ้าลืมซ่อน จะเห็น header ซ้อนกันสองชั้น

### สองทางเข้าไปหน้าเดียวกัน: top nav กับ sidebar

นอกจาก top nav ที่แสดงตลอดเวลาแล้ว โค้ดยังสร้าง **sidebar page** ("Navigate") ที่ซ่อนอยู่ เปิด/ปิดได้ด้วยปุ่ม
settings icon ในมุมซ้ายของ header sidebar มีลิงก์ไปหน้าเดียวกันกับ top nav (WiFi/Display/Device) — ทั้งสองทางเข้า
เรียกคนละ callback (เช่น `menu_nav_logic_wifi_btn_event_cb` จาก top nav ปุ่ม WiFi และปุ่มเดียวกันจาก sidebar link
ก็เรียก callback ตัวเดียวกันนี้) แต่ทั้งคู่ไปจบที่ `menu_nav_set_page()` ฟังก์ชันเดียวกัน — ปลายทางเดียวกัน สอง
ทางเข้า

### active state ต้องซิงก์สองที่พร้อมกัน

เพราะมีทางเข้าสองทาง (top nav + sidebar) ทุกครั้งที่เปลี่ยนหน้า `menu_nav_apply_active_state()` ต้องอัปเดต style
ของ **ทั้งปุ่ม top nav และ sidebar link พร้อมกัน** โดยเทียบกับ `state->current_page` — ถ้าอัปเดตแค่ฝั่งใดฝั่งหนึ่ง
ผู้ใช้ที่สลับหน้าจาก sidebar จะเห็นปุ่ม top nav highlight หน้าเดิมค้างอยู่ (หรือกลับกัน)

### ทำไมต้องเลื่อนการสลับหน้าออกไปด้วย `lv_async_call`

จุดที่ละเอียดที่สุดของ episode นี้คือ `menu_nav_queue_page_switch()` ไม่เรียก `lv_menu_set_page()` ทันทีในตัว
callback แต่เก็บ `pending_page` ไว้ก่อนแล้วเรียก `lv_async_call(menu_nav_async_apply_pending_page, state)` — คอมเมนต์
ในซอร์สระบุเหตุผลตรง ๆ ว่า "Always defer actual page switching to avoid lv_menu state race after sidebar
transitions" `lv_async_call()` คือการฝากฟังก์ชันไว้ให้ LVGL เรียกใน tick ถัดไปแทนที่จะรันทันทีตรงจุดนั้น เพราะปุ่มบน
top nav ทุกปุ่มเรียก `menu_nav_set_page(state, page_id, true)` ซึ่งอาจจะยุบ sidebar (`collapse_sidebar = true`)
ก่อนสลับหน้า — ถ้าสลับหน้าแบบ synchronous ทันทีในฟังก์ชันเดียวกับที่เพิ่งสั่งยุบ sidebar จะชนกับ layout state
ภายในของ `lv_menu` ที่ยังปรับตัวไม่เสร็จ การ defer ออกไปหนึ่ง tick จึงทำให้ sidebar transition เสร็จก่อนแล้วค่อย
สลับหน้า

### footer status label ปรับเป็น `printf`-style ผ่าน `lv_label_set_text_fmt`

`menu_nav_update_status()` เรียก `lv_label_set_text_fmt(state->status_label, "Page: %s | Sidebar: %s", ...)` ทุก
ครั้งหลังสลับหน้าหรือ toggle sidebar เพื่อให้ footer เป็นแหล่งเดียวที่บอกสถานะทั้งสองอย่างพร้อมกัน

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md) เพื่อเข้าใจจุดประสงค์ของ episode แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** เพื่อให้ตรงกับที่ build จริง (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน)

[`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.c) — เลื่อนการสลับหน้าออกไปด้วย `lv_async_call`:

```c
static void menu_nav_async_apply_pending_page(void *user_data)
{
    menu_nav_state_t *state = (menu_nav_state_t *)user_data;

    if(state == NULL || !state->page_switch_pending) {
        return;
    }

    state->page_switch_pending = false;
    menu_nav_apply_page_now(state, state->pending_page);
}

static void menu_nav_queue_page_switch(menu_nav_state_t *state, menu_nav_page_id_t page_id)
{
    if(state == NULL || state->menu == NULL) {
        return;
    }

    state->pending_page = page_id;

    if(!state->page_switch_pending) {
        state->page_switch_pending = true;
        lv_async_call(menu_nav_async_apply_pending_page, state);
    }
}
```

ซ่อน header ภายในของ `lv_menu` เองสองจุด เพราะ header/top nav ที่วาดเองทำหน้าที่แทนแล้ว:

```c
lv_obj_t *main_header = lv_menu_get_main_header(state->menu);
if(main_header != NULL) {
    lv_obj_add_flag(main_header, LV_OBJ_FLAG_HIDDEN);
}

lv_obj_t *sidebar_header = lv_menu_get_sidebar_header(state->menu);
if(sidebar_header != NULL) {
    lv_obj_add_flag(sidebar_header, LV_OBJ_FLAG_HIDDEN);
}
```

[`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_navigation.c) — สร้าง `lv_menu` และหน้าทั้งสี่ไว้ล่วงหน้า:

```c
lv_obj_t *menu = lv_menu_create(content);
lv_menu_set_mode_header(menu, LV_MENU_HEADER_TOP_FIXED);
lv_menu_set_mode_root_back_button(menu, LV_MENU_ROOT_BACK_BUTTON_DISABLED);

lv_obj_t *home_page = create_full_content_page(menu, "Home", "Home", ...);
lv_obj_t *page_wifi = create_full_content_page(menu, "WiFi Manager", "WiFi Manager", ...);
lv_obj_t *page_display = create_full_content_page(menu, "Display Setting", "Display Setting", ...);
lv_obj_t *page_device = create_full_content_page(menu, "Device Info", "Device Info", ...);

lv_menu_set_page(menu, home_page);
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/main_example.c), [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/menu_nav_logic.h) และ [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav/ui_menu_layout.h) (layout constants ของทุก component) — ดูโฟลเดอร์เต็มที่ [`hmi_ep04_menu_navigation/nav/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/nav)

## จุดที่มักพลาด

- **เชื่อคำบรรยายในส่วน How ของ README ต้นทางทั้งหมด** — README บอกว่าใช้ container header/nav/stage/footer แล้ว
  `lv_obj_clean()` + rebuild ตอนสลับหน้า แต่โค้ดจริงใช้ `lv_menu` ที่สร้างทุกหน้าไว้ล่วงหน้าแล้วสลับด้วย
  `lv_menu_set_page()` เท่านั้น ไม่มีการ clean/rebuild เลย — เวลาโค้ดกับคำบรรยายขัดกัน ให้ยึดโค้ดจริงเป็นหลัก
- **ลืมซ่อน header ภายในของ `lv_menu`** — ถ้าไม่เรียก `lv_obj_add_flag(main_header, LV_OBJ_FLAG_HIDDEN)` (และของ
  sidebar) จะเห็น header ซ้อนกันสองชั้นเพราะ `lv_menu` มี header ของตัวเองมาด้วย
- **เรียก `lv_menu_set_page()` ทันทีหลัง toggle sidebar โดยไม่ผ่าน `lv_async_call`** — จะชนกับ layout state ภายใน
  ของ `lv_menu` ที่ยังปรับตัวไม่เสร็จหลัง sidebar transition ทำให้พฤติกรรมไม่แน่นอน
- **อัปเดต active-state style แค่ฝั่งเดียว (top nav หรือ sidebar)** — ต้องอัปเดตทั้งสองฝั่งพร้อมกันทุกครั้งเพราะมี
  ทางเข้าสองทางไปหน้าเดียวกัน

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP04 — Menu Navigation บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/hmi_ep04_menu_navigation.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- lv_menu เก็บหน้าทั้งหมดไว้อย่างไร และการสร้างทุกหน้าไว้ครั้งเดียวมีข้อดีข้อเสียอะไร
- ถ้าเพิ่มหน้าใหม่ ต้องแก้ไฟล์ใดบ้าง
- ถ้าเปลี่ยนเป็นสร้างหน้าใหม่ทุกครั้งที่สลับเมนู โดยไม่ลบหน้าเก่า จะเกิดอะไรกับหน่วยความจำ

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep04_menu_navigation) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep04_menu_navigation&q=hmi_ep04_menu_navigation)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
