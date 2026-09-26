---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย"
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

# บทเรียน 2.1 — หน้าจอ LVGL แรก: โลโก้ หัวเรื่อง และคำบรรยาย

## หน้าจอ LVGL ตัวแรก — วาด logo, title และ subtitle แบบ static บน active screen

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. build และ flash episode นี้ลง TESAIoT Dev Kit แล้วได้หน้าจอตรงกับภาพตัวอย่าง
2. อธิบายว่า master template เรียก example_main(parent) เมื่อไร และทำไมเราไม่เขียน main เอง
3. สร้าง object tree screen → image → label และจัดวางด้วย align ได้

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m01.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP01 — Basic Label บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/hmi_ep01_basic_label.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — LVGL widget คือ `lv_obj_t *` ทั้งหมด

LVGL แทน widget ทุกชนิด (screen, image, label, ปุ่ม, เมนู) ด้วย struct เดียวกันคือ `lv_obj_t`

`lv_screen_active()` คืนค่า `lv_obj_t *` ของหน้าจอที่กำลังแสดงอยู่ — ใช้เป็น parent เมื่อสร้าง widget ตัวแรก

---

# แนวคิด — object tree: screen → image → label

EP01 สร้าง `screen` → `logo` (image) → `title`, `subtitle` (label)

- `lv_obj_align(obj, align, x, y)` — จัดวางเทียบกับ **parent**
- `lv_obj_align_to(obj, target, align, x, y)` — จัดวางเทียบกับ **widget อื่น** เป็น anchor

title ใช้ `LV_ALIGN_OUT_BOTTOM_MID` เทียบกับ logo — ถ้าโลโก้เปลี่ยนขนาด title เลื่อนตามอัตโนมัติ

offset ที่ใช้: โลโก้ห่างขอบบน 24 px · title ใต้โลโก้ 48 px · subtitle ใต้ title 24 px

---

# แนวคิด — สีและฟอนต์

- `lv_color_hex(0xRRGGBB)` แปลงเลขฐาน 16 เป็น `lv_color_t` — พื้นหลังใช้ `0x0F172A` (slate-900)
- `LV_OPA_COVER` = ความทึบสูงสุด, `LV_PART_MAIN` = ส่วนหลักของ widget ที่ style ไปลง
- ฟอนต์ Montserrat ต้องถูกเปิดใน `lv_conf.h` ของ master ก่อน (episode นี้ใช้ 30 px กับ title, 20 px กับ subtitle)

---

# แนวคิด — ทำไมโลโก้ต้องฝังเป็น C array

บอร์ดนี้ไม่มีไฟล์ระบบหรือ SD card ให้เปิดไฟล์ภาพตอน runtime

โลโก้ถูกแปลงล่วงหน้าเป็น `lv_image_dsc_t APP_LOGO` — เก็บ header + pixel data ดิบ คอมไพล์ฝังรวมเข้าไปใน flash image เดียวกับโปรแกรม

`lv_image_set_src(logo, &APP_LOGO)` รับ pointer ไปยัง flash ตรง ๆ ไม่มีการอ่านไฟล์และไม่มี I/O latency

---

# แนวคิด — สัญญาการเข้า-ออกของ episode

master เรียก `example_main(lv_scr_act())` ครั้งเดียวหลัง FreeRTOS, display driver, GPU และ LVGL พร้อมหมดแล้ว

`main_example.c` implement `example_main()` แบบ strong แล้ว forward ไปที่ `ui_ep01_basic_label_create()` ทันที โดยไม่ใช้ `parent` ตรง ๆ (มี `(void)parent;`) เพราะฟังก์ชันสร้าง UI เรียก `lv_screen_active()` เอง

ยังเรียก `tesaiot_add_thai_support_badge()` ก่อน — ยืนยันว่าฟอนต์ Noto Sans Thai ถูก bundle มาพร้อมแล้ว

หลัง `example_main()` return master วน `lv_timer_handler()` ตลอดไป — EP01 ไม่มี event จึงวาดครั้งเดียวแล้วค้างภาพ

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `gui.embedded` (ระดับ 2)
- `lang.c` (ระดับ 2)
- `build.vendor-sdk` (ระดับ 2)

---

# ตัวอย่างสมบูรณ์ — `main_example.c`

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/main_example.c)

```c
void example_main(lv_obj_t *parent)
{
    /* Master template bundles Noto Sans Thai fonts — this
     * badge confirms Thai rendering is available. */
    tesaiot_add_thai_support_badge();

    (void)parent;   /* episode manages its own screen via
                     * lv_screen_active(). */

    ui_ep01_basic_label_create();
}
```

---

# ตัวอย่างสมบูรณ์ — `ui_ep01_basic_label.c`

[ไฟล์เต็มบน Developer Hub](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/ui_ep01_basic_label.c)

```c
lv_obj_t *screen = lv_screen_active();
lv_obj_set_style_bg_color(screen,
    lv_color_hex(0x0F172A), LV_PART_MAIN);
lv_obj_set_style_bg_opa(screen,
    LV_OPA_COVER, LV_PART_MAIN);

lv_obj_t *logo = lv_image_create(screen);
lv_image_set_src(logo, &APP_LOGO);
lv_obj_align(logo, LV_ALIGN_TOP_MID, 0, 24);

lv_obj_t *title = lv_label_create(screen);
lv_label_set_text(title, "EP01 - Basic Label");
lv_obj_align_to(title, logo,
    LV_ALIGN_OUT_BOTTOM_MID, 0, 48);
```

`lv_obj_align()` เทียบกับ parent ส่วน `lv_obj_align_to()` เทียบกับ widget อื่นเป็น anchor

---

# จุดที่มักพลาด

- ใช้ `lv_obj_align()` แทน `lv_obj_align_to()` เมื่ออยากวางเทียบกับ widget อื่น (จะไปเทียบกับ `screen` แทน)
- ลืมเปิดขนาดฟอนต์ใน `lv_conf.h` ก่อนใช้ — build ไม่ผ่านหรือได้ฟอนต์อื่นแทนแบบไม่มี error ชัดเจน
- คิดว่าต้องใช้ `parent` ที่ได้รับมาตรง ๆ — จริง ๆ ฟังก์ชันสร้าง UI เรียก `lv_screen_active()` เองได้เลย

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- master template ทำอะไรให้เราแล้วบ้างก่อนเรียก example_main()
- ทำไมโลโก้ถูกฝังเป็น C array (APP_LOGO) แทนการโหลดจากไฟล์
- ถ้าอยากย้าย title ลงอีก 20 px ต้องแก้ค่าใดในโค้ด

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep01_basic_label) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep01_basic_label&q=hmi_ep01_basic_label)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (hmi_ep01_basic_label) ที่ commit `9a8e3ed`
