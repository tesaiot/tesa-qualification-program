---
id: c-found.m02.l02
lang: th
title: {th: Make และตัวแปรของการ build, en: Make and build flags}
summary: {th: อ่าน Makefile เปิดปิดส่วนของเฟิร์มแวร์ด้วยตัวแปร และรันตัวอย่างของ SDK ทีละตัว, en: 'Read a Makefile, switch firmware parts with variables, and run SDK examples one at a time.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l01]
objectives:
- {th: เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย ENABLE_PAGE_EXAMPLES=1 และเลือกรันตัวอย่างฝั่ง CM33 ด้วย SDK_EXAMPLE_CM33 ได้, en: Enable the SDK example catalogue with ENABLE_PAGE_EXAMPLES=1 and select a CM33 example with SDK_EXAMPLE_CM33.}
- {th: 'อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ ?= กับ = และผลต่อการ build', en: 'Explain the difference between ?= and = assignments in Make and their effect on the build.'}
- {th: อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย, en: Explain why disabled examples add nothing to the firmware image.}
develops:
- {skill: build.make-cmake, to: 3}
- {skill: build.vendor-sdk, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย ENABLE_PAGE_EXAMPLES=1 และเลือกรันตัวอย่างฝั่ง CM33 ด้วย SDK_EXAMPLE_CM33 ได้
2. อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ ?= กับ = และผลต่อการ build
3. อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ส่วนแนวคิดและแบบฝึกใช้แค่ GNU Make บนคอมพิวเตอร์ ไม่ต้องคอมไพล์อะไร

## ก่อนเริ่ม

ทวนจากบทเรียน 2.1 สองข้อ

1. ทำไมต้องรัน `make getlibs` ในทั้งสามโปรเจกต์ แทนที่จะรันครั้งเดียวที่โฟลเดอร์บนสุด
2. บรรทัดไหนบน serial console ที่เป็นหลักฐานว่าบอร์ด mtb-only บูตสำเร็จ

## ดูของจริงก่อน

เปิด [examples/flags.mk](examples/flags.mk) ไฟล์นี้ไม่คอมไพล์อะไร มันแค่พิมพ์ว่า make เข้าใจตัวแปรแต่ละตัวอย่างไร
**ทายก่อนรัน** ว่าบรรทัด `SOURCES` จะมีกี่ไฟล์ในแต่ละแบบ แล้วรันทีละบรรทัด

```sh
make -f examples/flags.mk
make -f examples/flags.mk ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
ENABLE_PAGE_EXAMPLES=1 make -f examples/flags.mk
```

แบบแรกได้ 2 ไฟล์ อีกสองแบบได้ 4 ไฟล์ และ make บอกด้วยว่าค่ามาจากไหน (`file`, `command line`, `environment`)
สังเกตสองบรรทัดที่แปลกตา `FROZEN` ได้แค่ `hello ` ทั้งที่ `GREETING` ได้ `hello world` และ `TRAILING` ที่ดูเหมือนเป็น 1 แต่ `equals 1: no`
สามเรื่องนี้คือเรื่องทั้งหมดของบทเรียน

## แนวคิด

### 1. โครงของ Makefile ในแม่แบบ ModusToolbox

แม่แบบมี Makefile สองชั้น ชั้นบนสุด ([Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/Makefile))
บอกแค่ว่าแอปพลิเคชันนี้มีโปรเจกต์อะไรบ้าง `MTB_TYPE=APPLICATION` กับ `MTB_PROJECTS=proj_cm33_s proj_cm33_ns proj_cm55`
แล้ว include ระบบ build ของ ModusToolbox ส่วน Makefile ของแต่ละโปรเจกต์ เช่น
[proj_cm33_ns/Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile)
เรียงแบบนี้

| ส่วน | ตัวอย่างจากไฟล์ | ทำอะไร |
|---|---|---|
| ค่าร่วม | `include ../common.mk` | variant, ที่อยู่ของ workspace |
| ชื่อและคอร์ | `APPNAME=proj_cm33_ns` `CORE=CM33` | บอก ModusToolbox ว่า build ให้คอร์ไหน |
| component | `COMPONENTS+=FREERTOS RTOS_AWARE` | เปิดโฟลเดอร์ที่ชื่อขึ้นต้นด้วย `COMPONENT_` ที่ตรงกัน |
| ตัวแปรของเรา | `ENABLE_PAGE_EXAMPLES ?= 0` | ค่าเริ่มต้นที่ผู้ใช้เปลี่ยนได้ |
| ส่งต่อให้ C | `DEFINES+=ENABLE_PAGE_EXAMPLES=$(ENABLE_PAGE_EXAMPLES)` | กลายเป็น `-D` ให้โค้ดใช้ `#if` ได้ |
| ตัดโฟลเดอร์ออก | `CY_IGNORE += examples` | ไม่ให้ ModusToolbox หาซอร์สในโฟลเดอร์นั้น |
| ไลบรารี | `LDLIBS += .../libbento_hsm.a` | ส่งไฟล์ .a ให้ linker |
| ท้ายสุด | `include $(CY_TOOLS_DIR)/make/start.mk` (บรรทัด 530) | ระบบ build อ่านตัวแปรทั้งหมดข้างบนตรงนี้ |

ลำดับมีผลจริง ตารางแก้ปัญหาใน README ของแม่แบบบันทึกอาการ "Linker cannot find a function from `lib/`" ไว้ว่าเกิดจาก
`LDLIBS` ถูกตั้งหลัง `include start.mk` "ModusToolbox reads it while including that file; anything later never reaches the linker."

### 2. ตัวแปรของ make: `=` `:=` `?=` `+=` และใครชนะ

| เขียน | ความหมาย | ขยายค่าเมื่อ |
|---|---|---|
| `A = x` | recursive: เก็บข้อความไว้ ขยายทุกครั้งที่ถูกใช้ | ตอนใช้ ตัวแปรที่นิยามทีหลังจึงมีผล |
| `A := x` | simple: ขยายทันทีแล้วเก็บผล | ตอนอ่านบรรทัดนั้น |
| `A ?= x` | ให้ค่าเฉพาะเมื่อ `A` ยังไม่ถูกนิยาม | ค่าจาก environment นับว่านิยามแล้ว |
| `A += x` | ต่อท้ายค่าเดิม | ตามชนิดเดิมของ `A` |

ค่าจาก **command line** (`make build X=1`) ชนะการกำหนดค่าในไฟล์ทุกแบบ ส่วนค่าจาก **environment** แพ้ `=` และ `:=` ในไฟล์ แต่ชนะ `?=`
นี่คือเหตุผลที่ SDK ประกาศ `ENABLE_PAGE_EXAMPLES ?= 0` และ `SDK_EXAMPLE_CM33 ?=` (บรรทัด 321-322)
ถ้าเขียน `ENABLE_PAGE_EXAMPLES = 0` คำสั่ง `make build ENABLE_PAGE_EXAMPLES=1` ก็ยังได้ผล แต่การตั้งค่าไว้ใน environment ของเครื่อง build จะถูกกลืนหายเงียบ ๆ

อีกเรื่องที่ต้องรู้คือ `ifeq` ถูกตัดสิน **ตอน make อ่านบรรทัดนั้น** คอมเมนต์ในไฟล์เดียวกันเตือนว่า `ENABLE_PAGE_BENTO_BUDDY` "must be assigned BEFORE
the CY_IGNORE ifneq below evaluates it — otherwise the variable is empty at parse time" (บรรทัด 60-64)
และ `ifeq` เทียบข้อความตรงตัว ค่า `1 ` ที่มีช่องว่างต่อท้ายไม่เท่ากับ `1` เอกสาร SDK บันทึกกับดักนี้เป็น Appendix X #23
ฟีเจอร์หายไปทั้งก้อนโดยไม่มี error ที่ไหนเลย ส่วน `common.mk` ป้องกันไว้ด้วยการ `$(strip)` ค่าของ `BENTO_VARIANT`
แล้วจงใจให้ build ล้มด้วย `$(error ...)` ถ้าค่าไม่ใช่ `mtb-mpy` หรือ `mtb-only` (บรรทัด 80-89) เพราะ "a typo must not quietly select the wrong firmware"

### 3. ทำไมตัวอย่างที่ปิดไว้ไม่เพิ่มขนาดเฟิร์มแวร์เลย

ModusToolbox ไม่ได้อ่านรายการซอร์สจาก Makefile มัน **เดินทั้งโฟลเดอร์ของโปรเจกต์แล้วคอมไพล์ทุกไฟล์ที่เจอ** คอมเมนต์ใน Makefile ของ CM33 อธิบายผลที่ตามมา

```make
# Compiled ONLY with ENABLE_PAGE_EXAMPLES=1.
#
# MTB DISCOVERS SOURCES BY WALKING THE APP TREE. `SOURCES +=` adds; it does not
# subtract, and it cannot exclude a file the walk already found. Only CY_IGNORE
# removes one. Gating a subdirectory with `ifeq (...) SOURCES += wildcard`
# therefore does NOTHING — the files compile anyway, and the first symptom is a
# wall of "No such file or directory" for headers that subdirectory needs.
# Every exclusion below is a CY_IGNORE for that reason.
#
# sdk_examples_cm33_table.c is GENERATED by tools/gen_examples_table.py.
ifeq ($(ENABLE_PAGE_EXAMPLES),1)
INCLUDES += examples
# ... (บรรทัด 506-523: ยกเว้นบางกลุ่มแม้เปิดตัวอย่าง)
else
CY_IGNORE += examples
endif
```

ที่มา: [proj_cm33_ns/Makefile บรรทัด 494-527](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile#L494-L527)
(Apache-2.0, tesaiot-pse84-devkit-sdk) ตัดบรรทัด 506-523 ออกเพื่อความสั้น

เมื่อธงเป็น 0 โฟลเดอร์ `examples` ถูก `CY_IGNORE` ทั้งโฟลเดอร์ ไฟล์ในนั้นไม่ถูกคอมไพล์ จึงไม่มี object ไม่มีอะไรให้ linker ใส่ลงใน image
อีกชั้นหนึ่งอยู่ในโค้ด C: `main.c` เรียก `sdk_examples_cm33_start()` เฉพาะใน `#if ENABLE_PAGE_EXAMPLES` (บรรทัด 384-388)
ถ้าปิดธงแล้วยังมีการเรียกหลงอยู่ build จะล้มที่ขั้น link ซึ่งดีกว่าการได้ image ที่มีของครึ่ง ๆ กลาง ๆ
README ของแคตตาล็อกสรุปว่าเมื่อปิดธง "not one byte of this tree reaches the firmware image"

## ตัวอย่างสมบูรณ์

[examples/flags.mk](examples/flags.mk) ทำงานเป็นสี่ท่า

- **ท่าที่ 1** `?=` ให้ค่าเริ่มต้น แล้วพิมพ์ `$(origin ...)` บอกว่าค่ามาจากไฟล์ command line หรือ environment
- **ท่าที่ 2** `GREETING = hello $(WHO)` กับ `FROZEN := hello $(WHO)` ประกาศก่อน `WHO` ตัวแรกขยายตอนใช้จึงได้ `hello world` ตัวหลังขยายทันทีจึงได้ `hello `
- **ท่าที่ 3** รายการ `SOURCES` เปลี่ยนตาม `ENABLE_PAGE_EXAMPLES` และ `DEFINES` ส่งทั้งสองธงต่อให้โค้ด C
- **ท่าที่ 4** ค่า `TRAILING` มีช่องว่างต่อท้ายเพราะคอมเมนต์ท้ายบรรทัด `ifeq` จึงไม่เท่ากับ 1 จนกว่าจะ `$(strip)`

ลองแก้แล้วทายก่อนรัน

1. ย้ายบรรทัด `WHO = world` ขึ้นไปไว้ก่อน `FROZEN := ...` ผลของ `FROZEN` เปลี่ยนเป็นอะไร
2. เปลี่ยน `ENABLE_PAGE_EXAMPLES ?= 0` เป็น `ENABLE_PAGE_EXAMPLES = 0` แล้วรันทั้งสามแบบอีกครั้ง แบบไหนเปลี่ยนผล
3. รัน `make -f examples/flags.mk 'ENABLE_PAGE_EXAMPLES=1 '` (มีช่องว่างในเครื่องหมายคำพูด) ไฟล์นี้รับได้เพราะ `$(strip)`
   แล้ว `ifeq ($(ENABLE_PAGE_EXAMPLES),1)` ในบรรทัด 504 ของ Makefile จริงของ SDK ซึ่งไม่ได้ strip จะทำอะไรกับค่าเดียวกัน

## ฝึกเติม

เปิด [practice/feature.mk](practice/feature.mk) โจทย์คือทำให้ `feature/feature.c` ถูกคอมไพล์เฉพาะเมื่อ `ENABLE_FEATURE` เป็น 1
โดยค่าเริ่มต้นปิด เปิดได้ทั้งจาก command line และ environment และทนช่องว่างต่อท้ายได้ มีช่องให้เติม 2 จุด ตรวจงานด้วย

```sh
make -f practice/feature.mk check
```

ก่อนแก้คุณจะเห็น `FAIL` สองบรรทัด และ `make` จบด้วย error เพราะ check คืนค่าที่ไม่ใช่ 0 เมื่อมี `FAIL` แม้บรรทัดเดียว
(การตรวจที่พิมพ์ FAIL แต่คืน 0 จะเขียวเสมอเมื่อนำไปรันใน CI เรื่องนี้กลับมาในบทเรียน 6.2)
ลองแก้ทีละ TODO แล้วรัน check ทุกครั้ง จะเห็นว่าแต่ละ TODO ทำให้บรรทัดไหนเปลี่ยนจาก FAIL เป็น PASS

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/feature.mk](solution/feature.mk)
TODO 1 คือเปลี่ยน `:=` เป็น `?=` และ TODO 2 คือเริ่ม `SOURCES` โดยไม่มี `feature/feature.c` แล้วเพิ่มด้วย `+=` ใน `ifeq ($(strip $(ENABLE_FEATURE)),1)`
ให้สังเกตว่าบรรทัด "command line turns it on" ผ่านตั้งแต่ก่อนแก้ เพราะค่าจาก command line ชนะทั้ง `:=` และ `?=`
test ที่ผ่านตั้งแต่แรกไม่ได้พิสูจน์ว่าโค้ดของคุณถูก มันพิสูจน์แค่ว่ากรณีนั้นไม่ได้แยกคำตอบถูกออกจากคำตอบผิด เรื่องนี้กลับมาในบทเรียน 6.1

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** เปิดแคตตาล็อกตัวอย่าง เลือกรันตัวอย่างฝั่ง CM33 หนึ่งตัว และวัดว่าการเปิดตัวอย่างเปลี่ยนขนาดเฟิร์มแวร์เท่าไร

1. build แบบปิดตัวอย่างก่อน (ค่าเริ่มต้น) แล้วหาไฟล์ ELF ของ CM33_NS และวัดขนาดของแต่ละ section
   ```sh
   make build -j
   find proj_cm33_ns/build -name "*.elf"
   arm-none-eabi-size <ไฟล์ .elf ที่หาเจอ>
   ```
   จดคอลัมน์ `text` `data` `bss`
2. build ใหม่แบบเปิดตัวอย่าง และไม่เลือกตัวไหน แล้ววัดอีกครั้ง
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1
   ```
   flash ด้วย `make program` ถอดสายเสียบใหม่ แล้วอ่าน serial console ตัวรันจะพิมพ์รายการ `=== TESAIoT SDK examples on CM33_NS (...) ===`
   และบอกวิธีรันด้วย `SDK_EXAMPLE_CM33=<id>` จดรูปแบบของ id ที่มันพิมพ์ (เช่น `cm33/io/04_gpio_led_button`)
3. build อีกครั้งโดยเลือกตัวอย่างหนึ่งตัว เช่น `SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan` แล้วดูบรรทัด `[sdk-example] running ...`
   และบรรทัดผลลัพธ์ `[sdk-example] ... -> 0 (ok)` หรือรหัสอื่น
4. ลองชื่อที่ไม่มีอยู่จริงหนึ่งครั้ง เช่นตัวอย่างในหัวข้อ "Turning them on" ของ [README ของแคตตาล็อก](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
   ที่ใช้ `tesaiot_hsm/01_acquire_chip` ตัวรันตอบว่าอะไร แล้วเทียบกับรายการที่ตัวรันพิมพ์เอง ข้อไหนคือความจริงของ commit นี้
5. เทียบขนาดจากข้อ 1 กับข้อ 2 ส่วนต่างอยู่ใน section ไหน แล้วอธิบายด้วยแนวคิดข้อ 3 ว่าทำไมตอนปิดธงจึงไม่มีส่วนต่างนั้น

**หลักฐานที่เก็บไว้ใน portfolio:** ผลของ `arm-none-eabi-size` ทั้งสองครั้ง log ของตัวรันตัวอย่าง (รายการ ผลของตัวที่เลือก และผลของชื่อที่ไม่มีอยู่)
และคำอธิบายข้อ 5 สั้น ๆ

## ไปต่อ

- `./bento.sh menus` ของแม่แบบถาม make ทีละธงแทนการอ่าน Makefile ด้วยตา README ของแม่แบบบอกเหตุผลว่าบางธงถูกกำหนดสองครั้ง
  ในเงื่อนไขของบอร์ดกับใน else อ่านข้อความแล้วได้คำตอบผิด ลองหาธงแบบนั้นหนึ่งตัวใน `proj_cm55/Makefile` ด้วย `grep -n "ENABLE_PAGE_" proj_cm55/Makefile`
- เอกสาร [GNU Make](https://www.gnu.org/software/make/) หัวข้อ "The Two Flavors of Variables" และ "Overriding Variables" อธิบายเรื่องในแนวคิดข้อ 2 แบบเต็ม

บทถัดไป: [บทเรียน 2.3 Git สำหรับงานเฟิร์มแวร์](../l03-git-for-firmware/README.md)

## สะท้อนคิด

- ถ้าเพื่อนบอกว่า "ผมเปิด ENABLE_PAGE_EXAMPLES แล้วแต่ไม่เห็นอะไรเปลี่ยน" คุณจะถามอะไรเขาสามข้อแรก
- ธงของ build แบบไหนที่ควรทำให้ build ล้มเมื่อค่าผิด และแบบไหนที่ใช้ค่าเริ่มต้นเงียบ ๆ ได้

## แหล่งอ้างอิง

- [SDK: แคตตาล็อกตัวอย่าง (Turning them on, Which core)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [SDK: ตัวอย่างฝั่ง CM33 Non-secure (วิธีรัน)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: proj_cm33_ns/Makefile](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/Makefile)
- [SDK: sdk_examples_cm33_table.c (รายการ id ของตัวอย่างฝั่ง CM33 ที่ commit นี้)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sdk_examples_cm33_table.c)
- [GNU Make](https://www.gnu.org/software/make/)
