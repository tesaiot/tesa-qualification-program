---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — เครื่องมือ บอร์ด และ master template"
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

# บทเรียน 1.1 — เครื่องมือ บอร์ด และ master template

## ติดตั้ง ModusToolbox เตรียม master template ของ TESAIoT Firmware Stack แล้ว build และ flash ครั้งแรก

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error
2. วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้
3. อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์

---

# ก่อนเริ่ม — สิ่งที่ต้องมี

- **TESAIoT Dev Kit** (PSoC Edge AI Kit SoM บนบอร์ดฐาน QWA309) และสาย USB-C สำหรับ KitProg3
- **ModusToolbox** ของ Infineon รุ่น 3.6 ขึ้นไปตาม README ของ master template (README ของชุด episode แนะนำ 3.8)
- **git** และเครื่องที่ build ภาษา C ได้ (Windows, macOS หรือ Linux)

---

# ดูของจริงก่อน

ถ้ายังไม่พร้อม build เอง ให้เปิดตัวอย่างบน [Developer Hub](https://dev.tesaiot.dev/) แล้ว flash เฟิร์มแวร์สำเร็จรูปจากหน้าตัวอย่าง (episode ในโมดูล 2–3 และแบบฝึก QWA309 ในโมดูล 4 มีเฟิร์มแวร์พร้อมใช้ทุกตัว)

---

# แนวคิด — สามโปรเจกต์บนชิปสองคอร์

PSoC Edge E84 เป็นชิปสองคอร์ (Cortex-M55 + Cortex-M33) ModusToolbox แบ่ง firmware เป็น**สามโปรเจกต์** แยก build/flash กัน แต่ประสานงานกันตอน boot

| โปรเจกต์ | คอร์ | `deps/` | หน้าที่ |
| --- | --- | --- | --- |
| `proj_cm33_s` | CM33 secure | ว่าง | ตั้ง MPC/PPC แล้วกระโดดไป non-secure |
| `proj_cm33_ns` | CM33 non-secure | ว่าง | เปิดคอร์ CM55 แล้วเข้า deep sleep |
| `proj_cm55` | CM55 | 15 แพ็กเกจ | LVGL, GPU, เซนเซอร์, Wi-Fi, episode |

`proj_cm33_s`/`proj_cm33_ns` ไม่ลิงก์ middleware เลย — งานจอ งาน Wi-Fi และ sensor bus ของทุก episode อยู่ใน `proj_cm55` ทั้งหมด

---

# แนวคิด — `proj_cm33_ns` ปลุก CM55 แล้วหลับ

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `082fd3e` · [`proj_cm33_ns/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm33_ns/main.c)

```c
/* Enable CM55. */
Cy_SysEnableCM55(MXCM55, CM55_APP_BOOT_ADDR,
                  CM55_BOOT_WAIT_TIME_USEC);
__enable_irq();

/* Put the CPU to Deep Sleep */
for (;;)
{
    Cy_SysPm_CpuEnterDeepSleep(
        CY_SYSPM_WAIT_FOR_INTERRUPT);
}
```

`CM55_BOOT_WAIT_TIME_USEC` = 10 µs หลังจากนี้ `proj_cm33_ns` ไม่ทำอะไรอีกเลย งานทั้งหมดตกไปที่ `proj_cm55`

---

# แนวคิด — `proj_cm55` เรียก episode เป็นขั้นตอนสุดท้าย

[`proj_cm55/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm55/main.c) — `cm55_gfx_task()`

```c
lv_init();
lv_port_disp_init();
lv_port_indev_init();

/* EPISODE ENTRY POINT —
 * main.c NEVER changes per episode.
 * apps/ provides a strong example_main(),
 * or the weak _default/ stub runs instead. */
lv_obj_t *parent = lv_scr_act();
example_main(parent);
```

`example_main(parent)` ถูกเรียก**ครั้งเดียว** หลัง GFX, I2C, จอ, sensor bus, VGLite และ LVGL พร้อมหมดแล้ว

---

# แนวคิด — sensor bus init แบบ best-effort

```c
cy_rslt_t r = sensor_i2c_controller_init();
if (CY_RSLT_SUCCESS != r)
{
    printf("[MASTER] Sensor I2C init failed "
           "(0x%08lx)\r\n", (unsigned long)r);
}

cy_rslt_t r3 = i3c_controller_init();
if (CY_RSLT_SUCCESS != r3)
{
    printf("[MASTER] I3C init failed "
           "(0x%08lx)\r\n", (unsigned long)r3);
}
```

ล้มเหลวแค่ `printf` แจ้งเตือนแล้ว boot ต่อ ไม่ assert หยุด — I2C คุม DPS368/SHT4x/BMI270, I3C คุม BMM350

---

# แนวคิด — สัญญา `example_main` แบบ weak/strong

`proj_cm55/apps/app_interface.h`:

```c
#include "app_interface.h"

/* Episode MUST provide a strong definition: */
void example_main(lv_obj_t *parent);
```

master มี `example_main()` แบบ **weak** ใน `apps/_default/` เป็นค่าเริ่มต้น เมื่อ episode ประกาศแบบ **strong** linker จะเลือกของ episode แทนอัตโนมัติ — ห้ามลบ `app_interface.h` ไม่งั้น episode คอมไพล์ไม่ผ่าน

---

# แนวคิด — โฟลเดอร์ `apps/` และการติดตั้ง episode

ทุก episode วางไฟล์ **ทั้งหมด** ลงใน `proj_cm55/apps/` เพียงโฟลเดอร์เดียว ไม่ต้องแก้ `Makefile` (`INCLUDES` ใช้ `find ./apps -type d` auto-discover)

ไฟล์ระบบสองอย่างที่ต้องอยู่คู่โฟลเดอร์นี้เสมอ: `app_interface.h` และ `_default/`

`tools/install_episode.sh` ทำให้อัตโนมัติในคำสั่งเดียว: ลบ episode เก่า (เก็บไฟล์ระบบไว้) → rsync episode ใหม่ → ล้าง build cache

---

# แนวคิด — ทรัพยากรที่พร้อมใช้ก่อน episode เริ่ม

เมื่อ `example_main(parent)` ถูกเรียก ทุกอย่างนี้พร้อมแล้วโดยไม่ต้อง init เอง

- LVGL 9 ครบ widget + ฟอนต์ Montserrat 12–40
- GPU VGLite เร่งทุก draw call
- Touch (GT911/FT5406/ILI2511) ผูกกับ LVGL แล้ว
- Sensor bus I2C (1.8V) และ I3C
- ไมโครโฟน PDM สอง channel
- Wi-Fi (`cy_wcm` + lwIP + mbedTLS), FreeRTOS tickless idle
- `printf()` ออก debug UART 115200 baud

---

# จุดที่มักพลาด

- Build ค้างที่ `proj_cm33_s` ด้วย `schema cydesignfile_v7 not found` → มีคน save `design.modus` ด้วย configurator 3.7 ทับ schema v6 เดิม
- `duplicate symbol example_main` ตอน link → มี strong `example_main` มากกว่าหนึ่งไฟล์ใน `apps/**`
- `multiple definition of APP_LOGO` → episode พก `app_logo.c` มาเองทั้งที่ master มีให้แล้ว
- Sensor I2C/I3C init ล้มเหลวแบบเงียบ → ดู log `[MASTER] Sensor I2C init failed` / `[MASTER] I3C init failed`

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `build.vendor-sdk` (ระดับ 2)
- `build.make-cmake` (ระดับ 2)
- `build.compilers` (ระดับ 1)
- `vcs.git` (ระดับ 1)
- `hw.architecture` (ระดับ 1)

---

# แล็บ: build และ flash ครั้งแรก — ขั้น 1

clone master template จาก branch `tesaiot_dev_kit_master` ของ Developer Hub

```sh
git clone -b tesaiot_dev_kit_master https://github.com/tesaiot/developer-hub.git tesaiot_dev_kit_master
cd tesaiot_dev_kit_master
make getlibs
```

---

# แล็บ: build และ flash ครั้งแรก — ขั้น 2

build และ flash ตามขั้นตอนใน [README ของ master template](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md)

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

---

# ฝึกเติม / แล็บ — ขั้น 3 (สำรอง)

ถ้ายังไม่พร้อม build เอง ให้เปิดตัวอย่างบน [Developer Hub](https://dev.tesaiot.dev/) แล้ว flash เฟิร์มแวร์สำเร็จรูปจากหน้าตัวอย่าง (episode ในโมดูล 2–3 และแบบฝึก QWA309 ในโมดูล 4 มีเฟิร์มแวร์พร้อมใช้ทุกตัว)

ทำสำเร็จเมื่อ:

- ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error
- วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้

---

# เช็กความเข้าใจ

- ไฟล์ของ episode ต้องวางไว้ที่ไหน และห้ามลบไฟล์ใดในโฟลเดอร์นั้น
- ใน master template งานจอและงาน Wi-Fi อยู่ใน `proj_cm55` ทั้งคู่ แล้ว `proj_cm33_ns` ทำอะไร และถ้าย้ายงานเครือข่ายไปไว้อีกคอร์จะได้และเสียอะไร
- `make build` ผ่านแต่ `make program` ไม่เจอบอร์ด ควรตรวจอะไรก่อน

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ master template (ภาษาไทย)](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md) · commit `082fd3e`
- [TESAIoT Developer Hub](https://dev.tesaiot.dev/) · [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
- [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)
