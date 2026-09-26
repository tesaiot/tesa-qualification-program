---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — Make และตัวแปรของการ build"
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

# บทเรียน 2.2 — Make และตัวแปรของการ build

## อ่าน Makefile เปิดปิดส่วนของเฟิร์มแวร์ด้วยตัวแปร และรันตัวอย่างของ SDK ทีละตัว

**โมดูล 2 — Build ด้วย ModusToolbox และ Make และ Git สำหรับเฟิร์มแวร์**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 2.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เปิดแคตตาล็อกตัวอย่างของ SDK ด้วย `ENABLE_PAGE_EXAMPLES=1` และเลือกรันตัวอย่างฝั่ง CM33 ด้วย `SDK_EXAMPLE_CM33` ได้
2. อธิบายความต่างของการกำหนดค่าตัวแปร Make แบบ `?=` กับ `=` และผลต่อการ build
3. อธิบายว่าทำไมตัวอย่างที่ปิดไว้จึงไม่เพิ่มขนาดเฟิร์มแวร์เลย

ใช้เวลาประมาณ 70 นาที — แนวคิดและแบบฝึกใช้แค่ GNU Make บนคอมพิวเตอร์ ไม่ต้องคอมไพล์อะไร

---

## ก่อนเริ่ม

ทวนจากบทเรียน 2.1 สองข้อ

1. ทำไมต้องรัน `make getlibs` ในทั้งสามโปรเจกต์ แทนที่จะรันครั้งเดียวที่โฟลเดอร์บนสุด
2. บรรทัดไหนบน serial console ที่เป็นหลักฐานว่าบอร์ด mtb-only บูตสำเร็จ

---

## ดูของจริงก่อน

เปิด [examples/flags.mk](examples/flags.mk) — ไม่คอมไพล์อะไร แค่พิมพ์ว่า make เข้าใจตัวแปรแต่ละตัวอย่างไร **ทายก่อนรัน**: บรรทัด `SOURCES` จะมีกี่ไฟล์ในแต่ละแบบ

```sh
make -f examples/flags.mk
make -f examples/flags.mk ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
ENABLE_PAGE_EXAMPLES=1 make -f examples/flags.mk
```

แบบแรกได้ 2 ไฟล์ อีกสองแบบได้ 4 ไฟล์ และ make บอกด้วยว่าค่ามาจากไหน (`file`, `command line`, `environment`) สังเกต `FROZEN` ได้แค่ `hello ` ทั้งที่ `GREETING` ได้ `hello world` และ `TRAILING` ที่ดูเหมือนเป็น 1 แต่ `equals 1: no` — สามเรื่องนี้คือเรื่องทั้งหมดของบทเรียน

---

## แนวคิด (1) — โครงของ Makefile ในแม่แบบ ModusToolbox

Makefile สองชั้น: ชั้นบนสุดบอกว่ามีโปรเจกต์อะไรบ้าง (`MTB_PROJECTS=proj_cm33_s proj_cm33_ns proj_cm55`) ส่วนของแต่ละโปรเจกต์เรียงแบบนี้

| ส่วน | ตัวอย่าง | ทำอะไร |
|---|---|---|
| ค่าร่วม | `include ../common.mk` | variant, ที่อยู่ workspace |
| ชื่อและคอร์ | `APPNAME=proj_cm33_ns` `CORE=CM33` | บอกว่า build ให้คอร์ไหน |
| ตัวแปรของเรา | `ENABLE_PAGE_EXAMPLES ?= 0` | ค่าเริ่มต้นที่ผู้ใช้เปลี่ยนได้ |
| ส่งต่อให้ C | `DEFINES+=ENABLE_PAGE_EXAMPLES=...` | กลายเป็น `-D` ให้ `#if` ใช้ |
| ตัดโฟลเดอร์ออก | `CY_IGNORE += examples` | ไม่ให้หาซอร์สในโฟลเดอร์นั้น |
| ท้ายสุด | `include start.mk` | ระบบ build อ่านตัวแปรทั้งหมดตรงนี้ |

> ลำดับมีผลจริง: `LDLIBS` ที่ตั้งหลัง `include start.mk` จะไม่ถึง linker เลย

---

## แนวคิด (2) — ตัวแปรของ make: `=` `:=` `?=` `+=`

| เขียน | ความหมาย | ขยายค่าเมื่อ |
|---|---|---|
| `A = x` | recursive: เก็บข้อความไว้ ขยายทุกครั้งที่ใช้ | ตอนใช้ (นิยามทีหลังมีผล) |
| `A := x` | simple: ขยายทันทีแล้วเก็บผล | ตอนอ่านบรรทัดนั้น |
| `A ?= x` | ให้ค่าเฉพาะเมื่อ `A` ยังไม่ถูกนิยาม | ค่าจาก environment นับว่านิยามแล้ว |
| `A += x` | ต่อท้ายค่าเดิม | ตามชนิดเดิมของ `A` |

ค่าจาก **command line** ชนะการกำหนดค่าในไฟล์ทุกแบบ ส่วนค่าจาก **environment** แพ้ `=`/`:=` ในไฟล์ แต่ชนะ `?=` — นี่คือเหตุผลที่ SDK ประกาศ `ENABLE_PAGE_EXAMPLES ?= 0` ถ้าเขียนเป็น `=` การตั้งค่าไว้ใน environment ของเครื่อง build จะถูกกลืนหายเงียบ ๆ

---

## แนวคิด (2) ต่อ — ifeq ตัดสินตอนอ่านบรรทัด และช่องว่างมีความหมาย

`ifeq` ถูกตัดสิน **ตอน make อ่านบรรทัดนั้น** — ตัวแปรที่ต้องใช้ต้องถูกกำหนดค่า **ก่อน** `ifeq` มาถึง ไม่งั้นค่าจะว่างเปล่าตอน parse

`ifeq` เทียบข้อความตรงตัว — ค่า `1 ` ที่มีช่องว่างต่อท้ายไม่เท่ากับ `1` (Appendix X #23 ของเอกสาร SDK) ฟีเจอร์หายไปทั้งก้อนโดยไม่มี error ที่ไหนเลย

`common.mk` ของ SDK ป้องกันด้วยการ `$(strip)` ค่าของ `BENTO_VARIANT` แล้วจงใจให้ build ล้มด้วย `$(error ...)` ถ้าค่าไม่ใช่ `mtb-mpy` หรือ `mtb-only` เพราะ **"a typo must not quietly select the wrong firmware"**

---

## แนวคิด (3) — ทำไมตัวอย่างที่ปิดไว้ไม่เพิ่มขนาดเฟิร์มแวร์

ModusToolbox ไม่ได้อ่านรายการซอร์สจาก Makefile — มัน **เดินทั้งโฟลเดอร์ของโปรเจกต์แล้วคอมไพล์ทุกไฟล์ที่เจอ**

```make
# MTB DISCOVERS SOURCES BY WALKING THE APP TREE. `SOURCES +=` adds; it does
# not subtract. Only CY_IGNORE removes one. Gating with `ifeq SOURCES +=
# wildcard` therefore does NOTHING — files compile anyway.
ifeq ($(ENABLE_PAGE_EXAMPLES),1)
INCLUDES += examples
else
CY_IGNORE += examples
endif
```

เมื่อธงเป็น 0 โฟลเดอร์ `examples` ถูก `CY_IGNORE` ทั้งโฟลเดอร์ — ไม่มี object ไม่มีอะไรให้ linker ใส่ลงใน image อีกชั้นในโค้ด C: `main.c` เรียกฟังก์ชันตัวอย่างเฉพาะใน `#if ENABLE_PAGE_EXAMPLES` เท่านั้น

---

## ตัวอย่างสมบูรณ์ — สี่ท่าใน flags.mk

```make
# ท่าที่ 1: ?= ให้ค่าเริ่มต้นเฉพาะเมื่อยังไม่มีใครให้ค่ามาก่อน
ENABLE_PAGE_EXAMPLES ?= 0

# ท่าที่ 2: = ขยายทุกครั้งที่ใช้ ส่วน := ขยายครั้งเดียวตอนอ่านบรรทัด
GREETING = hello $(WHO)
FROZEN := hello $(WHO)
WHO = world

# ท่าที่ 4: กับดักช่องว่างต่อท้าย - TRAILING คือ "1 " เพราะคอมเมนต์ต่อท้าย
TRAILING := 1 # this comment leaves a trailing space in the value
ifeq ($(TRAILING),1)
    TRAILING_RAW := yes
else
    TRAILING_RAW := no
endif
```

**ท่าที่ 1** `?=` + `$(origin ...)` · **ท่าที่ 2** recursive vs simple · **ท่าที่ 3** `SOURCES` เปลี่ยนตามธง · **ท่าที่ 4** `ifeq` เทียบตรงตัว จนกว่าจะ `$(strip)`

---

## ฝึกเติม

เปิด [practice/feature.mk](practice/feature.mk) — โจทย์: ทำให้ `feature/feature.c` ถูกคอมไพล์เฉพาะเมื่อ `ENABLE_FEATURE` เป็น 1 ค่าเริ่มต้นปิด เปิดได้ทั้งจาก command line และ environment และทนช่องว่างต่อท้ายได้ มีช่องให้เติม 2 จุด

```sh
make -f practice/feature.mk check
```

ก่อนแก้คุณจะเห็น `FAIL` สองบรรทัด และ `make` จบด้วย error ลองแก้ทีละ TODO แล้วรัน check ทุกครั้ง จะเห็นว่าแต่ละ TODO ทำให้บรรทัดไหนเปลี่ยนจาก FAIL เป็น PASS

ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/feature.mk](solution/feature.mk)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ต้องการรันตัวอย่างอ่านปุ่มและ LED ฝั่ง CM33 ตอนบูต คำสั่งใดถูกต้อง
2. build ด้วย `ENABLE_PAGE_EXAMPLES=1` แต่ไม่ได้ตั้ง `SDK_EXAMPLE_CM33` จะเกิดอะไรบน serial console
3. Makefile มี `FLAG = 0` แล้วผู้ใช้รัน `FLAG=1 make build` (environment) ค่าของ `FLAG` คืออะไร และถ้าเปลี่ยนเป็น `FLAG ?= 0` จะเป็นอะไร
4. `A = x$(B)`, `C := x$(B)`, แล้ว `B = y` — เมื่อใช้งาน `A` กับ `C` มีค่าอะไร
5. ทำไมเมื่อ `ENABLE_PAGE_EXAMPLES=0` ตัวอย่างของ SDK ไม่เพิ่มขนาดเฟิร์มแวร์ (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** เปิดแคตตาล็อกตัวอย่าง เลือกรันตัวอย่างฝั่ง CM33 หนึ่งตัว และวัดว่าการเปิดตัวอย่างเปลี่ยนขนาดเฟิร์มแวร์เท่าไร

1. build แบบปิดตัวอย่างก่อน (`make build -j`) หา ELF ของ CM33_NS แล้ว `arm-none-eabi-size` จดคอลัมน์ `text` `data` `bss`
2. build ใหม่แบบเปิดตัวอย่าง `make build -j ENABLE_PAGE_EXAMPLES=1` ไม่เลือกตัวไหน วัดอีกครั้ง flash แล้วอ่าน console ตัวรันจะพิมพ์รายการตัวอย่างและวิธีรันด้วย `SDK_EXAMPLE_CM33=<id>`
3. build อีกครั้งโดยเลือกตัวอย่างหนึ่งตัว เช่น `SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan` ดูบรรทัด `[sdk-example] running ...` และผลลัพธ์
4. ลองชื่อที่ไม่มีอยู่จริงหนึ่งครั้ง ตัวรันตอบว่าอะไร เทียบกับรายการที่ตัวรันพิมพ์เอง
5. เทียบขนาดข้อ 1 กับข้อ 2 ส่วนต่างอยู่ใน section ไหน อธิบายด้วยแนวคิดข้อ 3

**หลักฐานที่เก็บไว้ใน portfolio:** ผลของ `arm-none-eabi-size` ทั้งสองครั้ง log ของตัวรันตัวอย่าง และคำอธิบายข้อ 5

---

## ไปต่อ

- `./bento.sh menus` ของแม่แบบถาม make ทีละธงแทนการอ่าน Makefile ด้วยตา — บางธงถูกกำหนดสองครั้งในเงื่อนไขของบอร์ดกับใน else ลองหาธงแบบนั้นด้วย `grep -n "ENABLE_PAGE_" proj_cm55/Makefile`
- เอกสาร [GNU Make](https://www.gnu.org/software/make/) หัวข้อ "The Two Flavors of Variables" และ "Overriding Variables"

บทถัดไป: [บทเรียน 2.3 — Git สำหรับงานเฟิร์มแวร์](../l03-git-for-firmware/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
