---
id: fw-stack.m01.l01
lang: th
title:
  th: "เครื่องมือ บอร์ด และ master template"
  en: "Toolchain, board and the master template"
summary:
  th: "ติดตั้ง ModusToolbox เตรียม master template ของ TESAIoT Firmware Stack แล้ว build และ flash ครั้งแรก"
  en: "Install ModusToolbox, set up the TESAIoT Firmware Stack master template, then build and flash for the first time"
level: L2
time_min: {concept: 15, lab: 45}
hardware: {emulator: false, boards: [devkit]}
prerequisites: []
objectives:
  - th: "ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error"
    en: "Install ModusToolbox, clone the master template and build it without errors"
  - th: "วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้"
    en: "Drop an episode into proj_cm55/apps/ and flash it through KitProg3"
  - th: "อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์"
    en: "Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip"
develops:
  - {skill: build.vendor-sdk, to: 2}
  - {skill: build.make-cmake, to: 2}
  - {skill: build.compilers, to: 1}
  - {skill: vcs.git, to: 1}
  - {skill: hw.architecture, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "README.md"
  ref: 082fd3e76595b62cfdb213499a093c233dbb4b53
---

# เครื่องมือ บอร์ด และ master template

## เป้าหมาย

1. ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error
2. วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้
3. อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์

## สิ่งที่ต้องมี

- **TESAIoT Dev Kit** (PSoC Edge AI Kit SoM บนบอร์ดฐาน QWA309) และสาย USB-C สำหรับ KitProg3
- **ModusToolbox** ของ Infineon รุ่น 3.6 ขึ้นไปตาม README ของ master template (README ของชุด episode แนะนำ 3.8)
- **git** และเครื่องที่ build ภาษา C ได้ (Windows, macOS หรือ Linux)

## แนวคิด

### สามโปรเจกต์บนชิปสองคอร์

PSoC Edge E84 เป็นชิปสองคอร์ (Arm Cortex-M55 + Cortex-M33) และ ModusToolbox แบ่ง firmware ของบอร์ดหนึ่งตัว
ออกเป็น **สามโปรเจกต์**  ซึ่งแต่ละตัวมี `main.c` ของตัวเอง และ build/flash แยกกันแต่ประสานงานกันตอน boot

| โปรเจกต์ | คอร์ | ไลบรารีใน `deps/` | หน้าที่ |
| --- | --- | --- | --- |
| `proj_cm33_s` | CM33 (secure) | ไม่มี (แค่ `assetlocks.json`) | ตั้งค่า MPC/PPC ให้หน่วยความจำและ peripheral บางส่วนเป็น non-secure แล้วกระโดดไปยัง reset handler ของฝั่ง non-secure |
| `proj_cm33_ns` | CM33 (non-secure) | ไม่มี (แค่ `assetlocks.json`) | เปิดคอร์ CM55 ที่ boot address ของมัน แล้วเข้า deep sleep รอตลอดไป |
| `proj_cm55` | CM55 | 15 แพ็กเกจ — `lvgl`, `freertos`, `wifi-core-freertos-lwip-mbedtls`, ไดรเวอร์จอ 3 แบบ, ไดรเวอร์ touch 3 แบบ, ไดรเวอร์เซนเซอร์ 4 ตัว | รันแอปจริงทั้งหมด: จอ LVGL, GPU VGLite, เซนเซอร์, Wi-Fi, ไมโครโฟน และโค้ดของ episode |

ตาราง `deps/` ยืนยันสิ่งที่ README ของ master พูดไว้: `proj_cm33_s` และ `proj_cm33_ns` ไม่ลิงก์ middleware ใดเลย
มีหน้าที่แค่ "ปลุกคอร์ถัดไป" ส่วนงานจอ งาน Wi-Fi และ sensor bus ของ**ทุก** episode (รวมถึง Wi-Fi manager ในโมดูล 2)
อยู่ใน `proj_cm55` ทั้งหมด — โปรเจกต์อื่นนอกชุดนี้อาจแบ่งงานต่างออกไป จึงต้องเช็ค `deps/` และ `main.c`
ของแต่ละโปรเจกต์เสมอ ไม่ใช่จำตายตัว

โค้ดตัวอย่างในหัวข้อนี้คัดลอกจาก tesaiot/developer-hub (Apache-2.0) ที่ commit `082fd3e`

`proj_cm33_ns/main.c` สั้นมาก เพราะมีงานเดียว:

```c
/* Enable CM55. */
/* CM55_APP_BOOT_ADDR must be updated if CM55 memory layout is changed.*/
Cy_SysEnableCM55(MXCM55, CM55_APP_BOOT_ADDR, CM55_BOOT_WAIT_TIME_USEC);

/* Enable global interrupts */
__enable_irq();

/* Put the CPU to Deep Sleep */
for (;;)
{
    Cy_SysPm_CpuEnterDeepSleep(CY_SYSPM_WAIT_FOR_INTERRUPT);
}
```

`CM55_APP_BOOT_ADDR` คือที่อยู่ของ firmware `proj_cm55` ใน flash และ `CM55_BOOT_WAIT_TIME_USEC` (10 ไมโครวินาที)
คือเวลารอให้คอร์ CM55 บูตก่อนไปต่อ หลังจากนั้น `proj_cm33_ns` ไม่ทำอะไรอีกเลยนอกจากนอนใน deep sleep — งานทั้งหมด
ของ episode จึงตกไปอยู่ที่ `proj_cm55`

### `proj_cm55`: ลำดับเตรียมระบบก่อนเรียกโค้ดของเรา

`main()` ของ `proj_cm55` สร้าง FreeRTOS task ชื่อ `cm55_gfx_task` แล้วเริ่ม scheduler task นี้ทำงานตามลำดับ
คือ init GFX subsystem (`Cy_GFXSS_Init`) → ตั้ง interrupt ของ Display Controller และ GPU → init บัส I2C ของจอ/touch
→ init จอตามชนิดที่เลือกใน `common.mk` → **init sensor bus แบบ best-effort** → init หน่วยความจำและ VGLite →
`lv_init()` + `lv_port_disp_init()` + `lv_port_indev_init()` แล้วจึงเรียกโค้ดของ episode เป็นขั้นตอนสุดท้าย:

```c
            /* Initialize LVGL library */
            lv_init();
            lv_port_disp_init();
            /* Initialize touch input for interactive UI controls. */
            lv_port_indev_init();

            /* ========================================================= *
             *   EPISODE ENTRY POINT — master template invariant          *
             * ========================================================= *
             *  main.c NEVER changes per episode. Whatever episode's code *
             *  currently lives in proj_cm55/apps/ provides a strong      *
             *  implementation of example_main(parent).                   *
             *                                                            *
             *  When apps/ is empty, the weak stub in                     *
             *  apps/_default/example_main_default.c takes over and       *
             *  shows instructions for downloading an episode.            *
             * ========================================================= */
            lv_obj_t *parent = lv_scr_act();
            example_main(parent);
```

`example_main(parent)` ถูกเรียก **ครั้งเดียว** หลังทุก subsystem พร้อมแล้ว — `parent` คือ active screen
(`lv_scr_act()`) ที่ episode ใช้เป็นจุดเริ่มสร้าง object tree ของตัวเอง โค้ดของ episode จึงไม่ต้อง (และไม่ควร)
เรียก `lv_init()` หรือ init จอ/touch ซ้ำ

การ init sensor bus เป็นแบบ **best-effort**: ถ้าล้มเหลวจะ `printf` แจ้งเตือนแล้วปล่อยให้ boot ต่อไป ไม่ assert
หยุดทั้งระบบ เพราะ master ไม่รู้ล่วงหน้าว่า episode ที่กำลังจะรันต้องใช้เซนเซอร์ตัวไหนบ้าง:

```c
        /* Initialize dedicated sensor buses. Best-effort — episodes that do not
         * use sensors will simply ignore these handles. Master template always
         * initializes ALL subsystems so any episode dropped in apps/ Just Works. */
        cy_rslt_t sensor_i2c_rslt = sensor_i2c_controller_init();
        if (CY_RSLT_SUCCESS != sensor_i2c_rslt)
        {
            printf("[MASTER] Sensor I2C init failed (0x%08lx) — sensor episodes unavailable\r\n",
                   (unsigned long)sensor_i2c_rslt);
        }

        cy_rslt_t i3c_rslt = i3c_controller_init();
        if (CY_RSLT_SUCCESS != i3c_rslt)
        {
            printf("[MASTER] I3C init failed (0x%08lx) — BMM350 compass episodes unavailable\r\n",
                   (unsigned long)i3c_rslt);
        }
```

I2C ใช้กับ DPS368 (ความดัน), SHT4x (อุณหภูมิ/ความชื้น), BMI270 (IMU 6 แกน) ส่วน I3C ใช้กับ BMM350
(magnetometer/เข็มทิศ) เท่านั้น ถ้า episode ในโมดูล 3 อ่านค่าจากเซนเซอร์ไม่ได้เลยตั้งแต่ต้น ให้ไล่ดู log บรรทัดนี้ก่อน

### สัญญาระหว่าง master กับ episode: `example_main` แบบ weak/strong

`proj_cm55/apps/app_interface.h` ประกาศสัญญาที่ทุก episode ต้องทำตาม:

```c
#include "app_interface.h"

/* Episode MUST provide a strong definition: */
void example_main(lv_obj_t *parent);
```

master มี `example_main()` แบบ **weak symbol** อยู่ใน `apps/_default/example_main_default.c` เป็นค่าเริ่มต้น
(วาดการ์ด "ยังไม่มี episode ติดตั้ง") เมื่อเราวางไฟล์ของ episode ที่มีการ**ประกาศ `example_main()` แบบ strong**
ลงใน `proj_cm55/apps/` ตัว linker จะเลือกใช้ของ episode แทนโดยอัตโนมัติ — `main.c` เรียก `example_main(parent)`
เหมือนเดิมทุกครั้ง ไม่ต้องแก้โค้ดของ master เลยไม่ว่าจะสลับไปกี่ episode ก็ตาม นี่คือเหตุผลที่ข้อ 2 บอกว่า
"ห้ามลบ `app_interface.h`" — ถ้าลบ episode จะคอมไพล์ไม่ผ่านเพราะไม่มี prototype ให้ match

### โฟลเดอร์ `apps/` และการติดตั้ง episode

ทุก episode ที่ดาวน์โหลดจาก Developer Hub ถูกออกแบบให้วางไฟล์ **ทั้งหมด** ลงใน `proj_cm55/apps/` เพียงโฟลเดอร์เดียว
โดยไม่ต้องแก้ `Makefile` เพราะ `INCLUDES` ของ master ใช้ `find ./apps -type d` ค้นหา subfolder ที่ episode
สร้างขึ้นเองอัตโนมัติ มีไฟล์ระบบสองอย่างที่ต้องอยู่คู่โฟลเดอร์นี้เสมอคือ `app_interface.h` (สัญญาด้านบน) และ
`_default/` (หน้าจอ placeholder ก่อนติดตั้ง episode) — สคริปต์ `tools/install_episode.sh` ของ master ทำสามขั้นตอน
ให้อัตโนมัติในคำสั่งเดียวคือ ลบไฟล์ episode เก่า (เก็บสองไฟล์ระบบไว้), rsync ไฟล์ของ episode ใหม่เข้าไป และล้าง
build cache ของ `apps/` เพื่อให้ build ครั้งถัดไปสะอาด

### ทรัพยากรที่ `proj_cm55` เตรียมให้ก่อน episode เริ่ม

เมื่อ `example_main(parent)` ถูกเรียก subsystem เหล่านี้พร้อมใช้งานแล้วทั้งหมดโดยไม่ต้อง init เอง — LVGL 9
พร้อม widget ครบชุดและฟอนต์ Montserrat ขนาด 12–40, GPU VGLite เร่งการวาดทุก draw call, touch controller
(GT911/FT5406/ILI2511 แล้วแต่รุ่นจอ) ผูกกับ LVGL ให้แล้ว, sensor bus I2C (โดเมน 1.8V) และ I3C ตามที่อธิบายด้านบน,
ไมโครโฟน PDM สอง channel, WiFi Connection Manager (`cy_wcm`) พร้อม lwIP และ mbedTLS สำหรับ TLS, FreeRTOS
พร้อม tickless idle สำหรับประหยัดพลังงาน และ `printf()` ออก debug UART ที่ 115200 baud

## จุดที่มักพลาด

- **Build ค้างที่ `proj_cm33_s` ด้วย `schema cydesignfile_v7 not found`** — เกิดเมื่อมีคนเปิด `design.modus`
  ด้วย Device Configurator ของ ModusToolbox 3.7 ขึ้นไปแล้วกด save ทับ ทำให้ schema เดิม (v6) ถูกอัปเกรดเป็น v7
  ซึ่งเครื่องที่ใช้ ModusToolbox 3.6 อ่านไม่ได้ ห้าม edit แล้ว save `design.modus` ด้วย configurator รุ่นใหม่กว่า
- **`duplicate symbol example_main` ตอน link** — มีไฟล์ที่ประกาศ `void example_main(lv_obj_t *parent)` แบบ strong
  มากกว่าหนึ่งไฟล์ใน `apps/**` (เช่น ลืมลบไฟล์ของ episode เก่าก่อนวาง episode ใหม่) แก้โดยลบไฟล์ที่ซ้ำออก
  เหลือ strong `example_main` ได้แค่ตัวเดียวต่อ build
- **`multiple definition of APP_LOGO`** — episode บางตัวมี `app_logo.c`/`app_logo.h` ติดมาเอง ทั้งที่ master
  มี `app_assets/app_logo.c` ให้อยู่แล้ว ให้ลบไฟล์โลโก้ของ episode ออก แล้ว `#include "app_logo.h"` ตามปกติ
- **Sensor I2C/I3C init ล้มเหลวแบบเงียบ** — ล้มแล้วแค่ `printf` แจ้งเตือนหนึ่งบรรทัดแล้ว boot ต่อ ไม่ assert หยุด
  ถ้าเซนเซอร์อ่านค่าไม่ได้เลยตั้งแต่ต้น ให้เปิด serial log ที่ 115200 baud หา `[MASTER] Sensor I2C init failed`
  หรือ `[MASTER] I3C init failed` ก่อนไปหาสาเหตุอื่น

## แล็บ: build และ flash ครั้งแรก

1. clone master template จาก branch `tesaiot_dev_kit_master` ของ Developer Hub

   ```sh
   git clone -b tesaiot_dev_kit_master https://github.com/tesaiot/developer-hub.git tesaiot_dev_kit_master
   cd tesaiot_dev_kit_master
   make getlibs
   ```


2. build และ flash ตามขั้นตอนใน [README ของ master template](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md)

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

3. ถ้ายังไม่พร้อม build เอง ให้เปิดตัวอย่างบน [Developer Hub](https://dev.tesaiot.dev/) แล้ว flash เฟิร์มแวร์สำเร็จรูป
   จากหน้าตัวอย่าง (episode ในโมดูล 2–3 และแบบฝึก QWA309 ในโมดูล 4 มีเฟิร์มแวร์พร้อมใช้ทุกตัว)

## เช็กความเข้าใจ

- ไฟล์ของ episode ต้องวางไว้ที่ไหน และห้ามลบไฟล์ใดในโฟลเดอร์นั้น
- ใน master template งานจอและงาน Wi-Fi อยู่ใน `proj_cm55` ทั้งคู่ แล้ว `proj_cm33_ns` ทำอะไร และถ้าย้ายงานเครือข่ายไปไว้อีกคอร์จะได้และเสียอะไร
- `make build` ผ่านแต่ `make program` ไม่เจอบอร์ด ควรตรวจอะไรก่อน

## แหล่งอ้างอิง

- [README ของ master template (ภาษาไทย)](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md) · commit `082fd3e`
- [`proj_cm33_ns/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm33_ns/main.c) · [`proj_cm33_s/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm33_s/main.c) · [`proj_cm55/main.c`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/proj_cm55/main.c)
- [`docs/EXTENDING.md`](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/docs/EXTENDING.md) — คู่มือสำหรับต่อยอด master template ระดับลึก รวม pitfall ที่อ้างถึงในบทเรียนนี้
- [TESAIoT Developer Hub](https://dev.tesaiot.dev/) · [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
- [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
