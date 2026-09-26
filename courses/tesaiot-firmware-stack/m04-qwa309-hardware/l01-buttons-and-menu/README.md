---
id: fw-stack.m04.l01
lang: th
title:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
summary:
  th: "ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส"
  en: "Base-board buttons and a menu without touch"
level: L2
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง"
    en: "Read active-low pull-up buttons and count presses correctly"
  - th: "นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk"
    en: "Navigate an LVGL menu with two physical buttons (Move / Select) in kiosk style"
develops:
  - {skill: mcu.gpio, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_button_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ปุ่มกดบนบอร์ดฐานและเมนูที่ไม่ใช้จอสัมผัส

## เป้าหมาย

1. อ่านปุ่ม active-low แบบ pull-up และนับจำนวนครั้งที่กดได้ถูกต้อง
2. นำทางเมนู LVGL ด้วยปุ่มกายภาพสองปุ่ม (Move / Select) แบบ kiosk

## แนวคิด

### บอร์ดฐาน QWA309 มีอะไรให้ฝึก

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง สองแบบฝึกแรกใช้ปุ่มกดสองตัวบนบอร์ดฐานเป็นข้อมูลเข้าเหมือนกัน แต่ใช้ตรรกะอ่านค่าคนละแบบ: แบบแรกอ่าน "สถานะปัจจุบัน" (level) ตลอดเวลา ส่วนแบบที่สองจับ "จังหวะที่เพิ่งเปลี่ยน" (edge) เท่านั้น

### ปุ่มกด active-low พร้อม internal pull-up

ทั้งสองแบบฝึกตั้งขาปุ่มด้วย `Cy_GPIO_Pin_FastInit(port, pin, CY_GPIO_DM_PULLUP, 1UL, HSIOM_SEL_GPIO)` พารามิเตอร์ `CY_GPIO_DM_PULLUP` สั่งให้ชิปเปิด pull-up ตัวต้านทานในตัว ดึงขาขึ้น HIGH ตลอดเวลาที่ไม่มีอะไรมาแตะ ส่วน `HSIOM_SEL_GPIO` เลือกให้ขาทำหน้าที่ digital I/O ล้วน ๆ ไม่ผูกกับเพอริเฟอรัลตัวอื่น ปุ่มต่อขาลงกราวด์เมื่อกด จึงดึงระดับสัญญาณลงเป็น LOW และ `Cy_GPIO_Read()` คืนค่า 0 เมื่อกด — โค้ดจึงเขียนเงื่อนไข "กด" เป็น `0U == Cy_GPIO_Read(...)` ทั้งใน Push Button Monitor และ Hardware Button Menu การใช้ internal pull-up แบบนี้ทำให้ไม่ต้องมีตัวต้านทานภายนอกต่อเพิ่ม และสถานะตอนปล่อยปุ่มจะแน่นอนเสมอ (ไม่ลอย)

### กรองสัญญาณเด้งด้วยการนับรอบก่อนเชื่อค่าใหม่ (Push Button Monitor)

`button_monitor_ui.c` โพลปุ่มด้วย `lv_timer_create(button_timer_cb, BUTTON_REFRESH_PERIOD_MS, NULL)` ที่ `BUTTON_REFRESH_PERIOD_MS = 25` (ทุก 25 ms) ในแต่ละรอบ `update_button()` เทียบค่าที่อ่านได้ใหม่ (`sampled_pressed`) กับค่าครั้งก่อน ถ้าค่าเปลี่ยนจะรีเซ็ต `debounce_count` เป็น 0 และเริ่มนับใหม่ ถ้าค่ายังเหมือนเดิมจะนับ `debounce_count` ขึ้นทีละ 1 จนกว่าจะถึง `BUTTON_DEBOUNCE_TICKS = 2` โค้ดจึงยอมรับว่าสถานะเปลี่ยนจริง (`stable_pressed`) นั่นคือค่าต้องอ่านได้ระดับเดียวกันติดต่อกัน 3 ครั้ง ซึ่งที่รอบโพล 25 ms คือประมาณ 50 ms ก่อนสถานะจะเปลี่ยนจริง ช่วงเวลานี้กรองการเด้งของหน้าสัมผัสปุ่มที่สั้นกว่านั้นทิ้งไป `press_count` เพิ่มขึ้นเฉพาะตอนสถานะ "เสถียร" เปลี่ยนจากปล่อยเป็นกด (ไม่ใช่ทุกครั้งที่อ่านค่าได้ LOW) ส่วน `hold_time_ms` จะรีเซ็ตเป็น 0 เมื่อปล่อย และสะสมเพิ่มทีละ `BUTTON_REFRESH_PERIOD_MS` ทุกรอบที่ `stable_pressed` เป็นจริง ค่านี้จึงมีความละเอียดเป็นขั้นละ 25 ms ไม่ใช่ค่านาฬิกาต่อเนื่อง

### จับ "ขอบขาลง" แทนสถานะค้าง (Hardware Button Menu)

`hw_button_menu_ui.c` ใช้แนวทางต่างออกไป: `btn_pressed_edge()` มี debounce แบบเดียวกัน (`MENU_DEBOUNCE = 2` นับที่รอบโพล `MENU_POLL_MS = 30` ms) แต่คืนค่า `true` เฉพาะ "รอบที่สถานะเสถียรเพิ่งเปลี่ยนจากปล่อยเป็นกด" เท่านั้น ไม่ใช่คืน `true` ทุกรอบที่ปุ่มยังถูกกดอยู่ — นี่คือความต่างสำคัญจาก `update_button()` ของ Push Button Monitor ที่ผู้เรียกอ่าน `stable_pressed` เป็นระดับสัญญาณทุกรอบ ผลคือถ้ากดปุ่ม MOVE ค้างไว้นาน `menu_timer_cb()` จะขยับ highlight ไปข้างหน้าเพียงครั้งเดียวต่อการกดหนึ่งครั้ง เมนูมี `MENU_ITEMS = 4` รายการ และวนกลับด้วยเลขคณิตมอดุโล `(s_sel + 1U) % MENU_ITEMS` ปุ่ม SW6 (MOVE) กับ SW5 (SELECT) แต่ละตัวมีโครงสร้าง `btn_t` และตัวแปร debounce ของตัวเอง (`s_move`, `s_selb`) จึงกดสองปุ่มพร้อมกันได้โดยไม่รบกวนกัน กด SELECT เพียงเปลี่ยนข้อความสถานะ ไม่ขยับ highlight

### ชื่อปุ่มที่ไม่ตรงกันระหว่างคำอธิบายกับโค้ด: SW9/SW10 เทียบกับ SW5/SW6

ไฟล์ `metadata.json` และคอมเมนต์บนสุดของ `main_example.c` ของ Push Button Monitor เขียนว่าเป็นปุ่ม "SW9 (P17.5) และ SW10 (P17.7)" แต่โค้ดจริงใน `button_monitor_ui.c` ตั้งชื่อปุ่มในอาร์เรย์ `buttons[]` ว่า `"SW5"` (พิน P17.7) และ `"SW6"` (พิน P17.5) ซึ่งเป็นข้อความที่ปรากฏบนจอจริงด้วย ส่วน Hardware Button Menu ที่ใช้พินเดียวกันเรียกปุ่มทั้งสองว่า SW6 (P17.5, MOVE) และ SW5 (P17.7, SELECT) ตรงกับชื่อในโค้ดของ Push Button Monitor พอดี สรุปคือชื่อ SW9/SW10 เป็นข้อความสรุปที่คลาดเคลื่อนใน Developer Hub เอง ให้ยึดตามโค้ดที่รันจริงและลายพิมพ์บนบอร์ดเป็นหลัก

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Push Button Monitor** — อ่านปุ่มกด SW9 (P17.5) และ SW10 (P17.7) แบบ active-low pull-up แสดงสถานะกด/ปล่อย + นับจำนวนครั้งบน LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor)
- **QWA309 — Hardware Button Menu** — นำทางเมนู LVGL ด้วยปุ่มกายภาพ SW6=Move SW5=Select (ไม่ใช้ touch) — headless/kiosk UX pattern
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu)

โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริงที่ commit เดียวกัน (Apache-2.0, tesaiot/developer-hub)

[`button_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/button_monitor_ui.c) — ตั้งขาปุ่มเป็น input pull-up ก่อนเริ่มอ่านค่า:

```c
static void button_inputs_init(void)
{
    Cy_GPIO_Pin_FastInit(P17_5_PORT,
                         P17_5_PIN,
                         CY_GPIO_DM_PULLUP,
                         1UL,
                         HSIOM_SEL_GPIO);
    Cy_GPIO_Pin_FastInit(P17_7_PORT,
                         P17_7_PIN,
                         CY_GPIO_DM_PULLUP,
                         1UL,
                         HSIOM_SEL_GPIO);
}
```

[`button_monitor_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_button_monitor/button_monitor_ui.c) — debounce แบบนับรอบก่อนยอมรับว่าสถานะเปลี่ยนจริง (level):

```c
static void update_button(button_channel_t *button)
{
    bool sampled_pressed = (0U == Cy_GPIO_Read(button->port, button->pin_num));

    if (sampled_pressed == button->last_sample_pressed)
    {
        if (button->debounce_count < BUTTON_DEBOUNCE_TICKS)
        {
            button->debounce_count++;
        }
    }
    else
    {
        button->last_sample_pressed = sampled_pressed;
        button->debounce_count = 0U;
    }

    if ((button->debounce_count >= BUTTON_DEBOUNCE_TICKS) &&
        (sampled_pressed != button->stable_pressed))
    {
        button->stable_pressed = sampled_pressed;
        /* ... press_count++ on press / hold_time_ms reset on release ... */
    }
    /* ... hold_time_ms accumulation, apply_button_visual(button) ... */
}
```

[`hw_button_menu_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/hw_button_menu_ui.c) — debounce แบบเดียวกัน แต่คืน `true` แค่ครั้งเดียวต่อการกด (edge):

```c
static bool btn_pressed_edge(btn_t *b)
{
    bool raw = (0U == Cy_GPIO_Read(b->port, b->pin));   /* active low */
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

[`hw_button_menu_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_hw_button_menu/hw_button_menu_ui.c) — ใช้ผลจาก edge เพื่อขยับ highlight แค่ครั้งเดียวต่อการกด:

```c
static void menu_timer_cb(lv_timer_t *timer)
{
    (void)timer;
    if (btn_pressed_edge(&s_move)) {
        s_sel = (uint8_t)((s_sel + 1U) % MENU_ITEMS);
        highlight();
        lv_label_set_text_fmt(s_status, "MOVE -> %s", s_items[s_sel]);
    }
    if (btn_pressed_edge(&s_selb)) {
        lv_label_set_text_fmt(s_status, "SELECT: %s", s_items[s_sel]);
    }
}
```

## จุดที่มักพลาด

- **ลืมตั้ง pull-up แล้วปล่อยขาเป็น high-Z** — ถ้าตั้งขาปุ่มเป็น input ธรรมดาไม่มี pull-up ขณะที่ปุ่มต่อลงกราวด์เพียงด้านเดียว ตอนปล่อยปุ่มขาจะลอย (floating) ค่าที่อ่านได้จะแกว่งตามสัญญาณรบกวน ตัวนับอาจเพิ่มเองโดยไม่มีใครกด ต้องตั้ง `CY_GPIO_DM_PULLUP` เสมอ
- **คิดว่ากดปุ่มค้างแล้วเมนูจะเลื่อนซ้ำหลายครั้ง** — ใน Hardware Button Menu highlight เลื่อนแค่ครั้งเดียวต่อการกด เพราะ `btn_pressed_edge()` คืน `true` เฉพาะขอบขาลง ไม่ใช่ระดับสัญญาณ ถ้าต้องการ auto-repeat เมื่อกดค้างต้องเขียนตรรกะเพิ่มเอง
- **ผสมสองรูปแบบเข้าด้วยกัน** — ถ้านำโค้ดแบบอ่านระดับสัญญาณ (`stable_pressed` ของ Push Button Monitor) ไปใช้กับเมนูโดยตรง highlight จะขยับทุกรอบโพลตราบใดที่ยังกดปุ่มอยู่ (ทุก 30 ms) ไม่ใช่ครั้งเดียวต่อการกด ต้องเลือกรูปแบบ (level หรือ edge) ให้ตรงกับพฤติกรรมที่ต้องการ

> ชื่อปุ่มในคำอธิบายของ Developer Hub (SW9/SW10) ไม่ตรงกับโค้ดของแบบฝึก (SW5/SW6) ให้ยึดตามโค้ดและลายพิมพ์บนบอร์ด

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

- ทำไมปุ่ม active-low อ่านได้ 0 ตอนกด
- กดครั้งเดียวแต่ตัวนับขึ้นสองครั้ง สาเหตุคืออะไรและแก้อย่างไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
