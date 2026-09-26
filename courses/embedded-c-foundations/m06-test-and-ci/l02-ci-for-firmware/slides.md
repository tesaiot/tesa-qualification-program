---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.2 — CI สำหรับเฟิร์มแวร์"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 6.2 — CI สำหรับเฟิร์มแวร์

## ให้ GitHub Actions build ตรวจรูปแบบโค้ด วิเคราะห์แบบสถิต และรัน test ทุกการเปลี่ยนแปลง

**โมดูล 6 — Unit test และ CI**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 6.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request
2. เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck
3. อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง

ใช้เวลาประมาณ 70 นาที — ต้องมีทุกอย่างจากบทเรียน 6.1 และ python3 แล็บต้องมีบัญชี GitHub

---

## ก่อนเริ่ม

ทวนสองข้อ

1. hook `pre-commit` ของบทเรียน 2.3 ตรวจทุก commit ในเครื่องคุณ ทำไมมันยังไม่พอสำหรับทีม (คำใบ้: `git commit --no-verify`)
2. บทเรียน 6.1 บอกว่า test ที่ผ่านพิสูจน์อะไรได้บ้าง และพิสูจน์ด้วยวิธีไหนว่ามันล้มเป็น

---

## ดูของจริงก่อน

repo ของ SDK มี workflow ของ GitHub Actions อยู่ไฟล์เดียว

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  notify:
    steps:
      - name: Ask the relay to re-read GitHub
        run: |
          code=$(curl -s -o /tmp/refresh.json -w '%{http_code}' ... "$RELAY/api/firmware/github/refresh")
          test "$code" = "200"
```

**ทายก่อนอ่านต่อ**: workflow นี้รันเมื่อไร มัน build เฟิร์มแวร์ไหม ถ้า `curl` ได้ HTTP 500 ขั้นนี้จะเขียวหรือแดง

คำตอบ: รันเมื่อมี release (หรือกดรันเอง) มัน **ไม่ได้** build เฟิร์มแวร์ แค่บอก relay ให้ดึง release ใหม่ ถ้าได้ 500 บรรทัด `test "$code" = "200"` คืนค่าไม่ใช่ 0 ขั้นนี้จึงแดง — บรรทัดนั้นคือสิ่งที่ทำให้ขั้นนี้ **ล้มเป็น** ถ้าไม่มีมัน `echo` จะพิมพ์ 500 แล้วจบด้วย 0

---

## แนวคิด (1) — workflow, job, step และ "workflow บาง สคริปต์หนา"

| คำ | คืออะไร |
|---|---|
| workflow | ไฟล์หนึ่งไฟล์ ถูกปลุกด้วยเหตุการณ์ เช่น `pull_request` (`on:`) |
| job | งานหนึ่งชิ้นบนเครื่องเสมือนใหม่ของตัวเอง รันขนานกันได้ |
| step | คำสั่งหนึ่งขั้นใน job ขั้นที่คืนค่าไม่ใช่ 0 ทำให้ job ล้ม |

- **workflow บาง สคริปต์หนา** ใส่คำสั่งตรวจจริงไว้ใน `ci.sh` ให้ workflow แค่ติดตั้งเครื่องมือกับเรียก `bash ci.sh <ขั้น>` — รันคำสั่งเดียวกันในเครื่องได้ก่อน push
- **สิทธิ์น้อยที่สุด** — "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only" (`permissions: contents: read`)
- **ล็อกทุกอย่างที่เปลี่ยนเองได้** — "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release" และ `ubuntu-latest` ก็เปลี่ยนรุ่นได้ บทนี้จึงใช้ `ubuntu-24.04` และตั้ง `timeout-minutes`

---

## แนวคิด (2) — การตรวจสี่ขั้น และทำให้ทุกขั้นล้มเป็น

| ขั้น | เครื่องมือ | จับอะไรได้ |
|---|---|---|
| `tests` | Unity + `prove_red.sh` (6.1) | ตรรกะผิด และ test ที่ไม่ได้ทดสอบอะไร |
| `format` | clang-format 18.1.3 | โค้ดที่จัดรูปแบบต่างจากที่ทีมตกลง |
| `static` | cppcheck | บั๊กที่เห็นได้โดยไม่ต้องรัน เช่นเขียนเลยขอบอาร์เรย์ |
| `cross` | arm-none-eabi-gcc (M33/M55) | โค้ดที่คอมไพล์ได้บนคอมพิวเตอร์แต่ไม่ได้บนไมโครคอนโทรลเลอร์ |

**กับดักที่พบบ่อยที่สุดคือขั้นที่รายงานปัญหาแต่ยังเขียว**

- `clang-format --dry-run` เจอปัญหา พิมพ์คำเตือน แล้วคืน 0 ต้องเติม `--Werror`
- `cppcheck` เจอ `arrayIndexOutOfBounds` พิมพ์ `error:` แล้วคืน 0 ต้องเติม `--error-exitcode=1`
- `|| true` หรือ `continue-on-error: true` ทำให้เขียวเสมอ
- `( ขั้นตอน ) || rc=$?` ปิด `set -e` ของทุกคำสั่งใน subshell

---

## แนวคิด (2) ต่อ — cross-compile ตรวจอะไร ไม่ตรวจอะไร

```make
# Compiler flags for PSoC Edge Cortex-M33 (MUST match project: softfp)
CFLAGS := -mcpu=cortex-m33 -mthumb -mfloat-abi=softfp -mfpu=fpv5-sp-d16
```

`GCC_PATH` ในไฟล์จริงชี้โฟลเดอร์บน macOS ของเครื่องหนึ่ง บน runner ของ CI บรรทัดนี้ใช้ไม่ได้ทันที — CI ช่วยหาสมมติฐานเกี่ยวกับเครื่องที่ซ่อนอยู่แบบนี้ได้

คอมไพเลอร์ของ ModusToolbox คือ GCC 14.2.1 ส่วน `gcc-arm-none-eabi` จาก apt ของ Ubuntu 24.04 คือ 13.2.1 — ขั้น `cross` จึงตรวจว่าตรรกะ **คอมไพล์ได้** สำหรับ CPU ของบอร์ด **ไม่ได้สร้างไบนารีเดียวกับที่ build จริง**

---

## แนวคิด (3) — CI บน runner สาธารณะตรวจอะไรได้ อะไรต้องใช้บอร์ด

| CI บน runner สาธารณะตรวจได้ | ต้องใช้บอร์ดจริง |
|---|---|
| ตรรกะที่อยู่หลังตะเข็บ | timing ของ interrupt และตัวตั้งเวลา |
| รูปแบบโค้ดและบั๊กที่วิเคราะห์แบบสถิต | cache กับ DMA และลำดับของ barrier |
| ตรรกะคอมไพล์ได้สำหรับ Cortex-M33/M55 | สัญญาณจริงบน UART, I2C, SPI |
| ไฟล์ที่ไม่ควรเข้า repo | watchdog รีเซ็ตจริง และบอร์ดบูตขึ้นจริง |

ทำไมไม่ build เฟิร์มแวร์ทั้งก้อนใน CI: **"Source files (tesaiot_*.c) are proprietary"** แจก `libtesaiot.a` ที่ build แล้วแทน และ git repo ไม่มีไฟล์ `.a` เลย ต้อง build จาก zip ของ release

> self-hosted runner ที่มีบอร์ดเสียบ (HIL) เสี่ยง: **"Self-hosted runners should almost never be used for public repositories ... any user can open pull requests ... and compromise the environment"**

---

## ตัวอย่างสมบูรณ์ — ห้าไฟล์ทำงานร่วมกัน

[host-tests.yml](examples/host-tests.yml) workflow เล็กที่สุดที่ใช้ได้จริง · [ci.sh](examples/ci.sh) การตรวจสี่ขั้น จบด้วย `PASS`/`FAIL`/`NOT CHECKED` · [.clang-format](examples/.clang-format) รูปแบบโค้ด · [check_workflow.py](examples/check_workflow.py) ตรวจโครง workflow ในเครื่อง

```sh
cd examples
python3 -m venv .venv
.venv/bin/pip install clang-format==18.1.3 pyyaml==6.0.3
SRC_DIR=../../l01-unit-tests-on-host/examples TEST=../solution/test_level_alarm.c \
  CLANG_FORMAT=.venv/bin/clang-format bash ci.sh all
```

**ลองทำให้แต่ละขั้นแดง** (ในสำเนา ไม่ใช่ไฟล์จริง): `format` ลบช่องว่างรอบ `=` · `static` วนเขียนเลยขอบ `int history[4]` · `cross` เพิ่ม `_Static_assert(sizeof(long)==8, ...)` (ผ่านบนคอมพิวเตอร์ 64 บิต แต่แดงบน Cortex-M ที่ `long` ยาว 4 ไบต์) · `tests` ใช้ไฟล์ที่ `prove_red.sh` พบบั๊กที่รอด

---

## ฝึกเติม

เปิด [practice/firmware-ci.yml](practice/firmware-ci.yml) — job `tests` ให้มาแล้ว มีช่องให้เติม 6 จุด

1. รันกับทุก pull request ด้วย
2. จำกัดสิทธิ์ของ `GITHUB_TOKEN` ให้อ่านได้อย่างเดียว
3. ล็อก action ทุกตัวด้วย commit SHA เต็ม
4. job `format` ติดตั้ง clang-format รุ่นที่ล็อกไว้ แล้วรัน `bash ci.sh format`
5. job `static-analysis` ติดตั้ง cppcheck แล้วรัน `bash ci.sh static`
6. job `cross-compile` ติดตั้ง gcc-arm-none-eabi แล้วรัน `bash ci.sh cross`

```sh
cd examples
.venv/bin/python check_workflow.py ../practice/firmware-ci.yml
```

ก่อนเติม ตัวตรวจขึ้น `10 failed` งานเสร็จเมื่อขึ้น `0 failed` ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/firmware-ci.yml](solution/firmware-ci.yml)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ทีมตกลงให้ทุก pull request ผ่าน unit test ก่อน merge ส่วนใดของ workflow ที่ทำให้ GitHub รันมันเมื่อเปิดหรือ push เข้า pull request
2. ข้อใดทำให้ workflow ให้ผลเหมือนเดิมเมื่อรันซ้ำในอีกหลายเดือน (เลือกได้หลายข้อ)
3. ขั้น format รัน `clang-format --dry-run` กับไฟล์ที่จัดรูปแบบผิด log มีคำเตือน แต่ job เขียว สาเหตุที่น่าจะเป็นที่สุดคืออะไร
4. ข้อใดทำให้ขั้นตรวจใน CI เขียวได้แม้เครื่องมือพบปัญหา (เลือกได้หลายข้อ)
5. CI บน runner สาธารณะเขียวครบทั้งสี่ขั้น ข้อใดยังต้องตรวจบนบอร์ดจริง (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** ให้ GitHub ตรวจงานของคุณทุก pull request แล้วพิสูจน์ว่ามันแดงเป็น

1. สร้าง repo ของคุณเอง วาง `ci.sh`, `.clang-format` ไว้ที่ราก, โฟลเดอร์ `host-tests/` จากบทเรียน 6.1 พร้อม `test_level_alarm.c` ที่เติมครบ และ workflow ที่ `.github/workflows/firmware-ci.yml`
2. push แล้วเปิดแท็บ Actions ทั้งสี่ job ต้องเขียว
3. เปิด pull request ที่ใส่บั๊กหนึ่งจุดจากหัวข้อตัวอย่างสมบูรณ์ ดู job ที่ควรแดงว่าแดงจริง แล้วปิดโดยไม่ merge
4. ย้ายการตรวจหนึ่งอย่างจาก hook `pre-commit` ของบทเรียน 2.3 มาเป็นขั้นใน `ci.sh` แล้วพิสูจน์ด้วย pull request ว่า `--no-verify` ข้ามมันไม่ได้อีก
5. ถ้ามีบอร์ด เขียนสั้น ๆ ว่าการเปลี่ยนแปลงแบบไหนที่ CI เขียวแล้วยังต้อง flash ลงบอร์ดเพื่อตรวจ

**หลักฐานที่เก็บไว้ใน portfolio:** ลิงก์ของ repo ภาพหรือลิงก์ของรอบที่เขียวครบ ลิงก์ของ pull request ที่แดง และคำตอบข้อ 5

---

## ไปต่อ

- อ่าน workflow ของ SDK ทั้งไฟล์ [notify-flash-relay.yml](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.github/workflows/notify-flash-relay.yml) ขั้นที่สองตรวจอะไร และทำไมผู้เขียนแยกมันออกจาก workflow อื่น
- ลองเปิด `--enable=style` ของ cppcheck กับโค้ดของคุณ ข้อความไหนมีประโยชน์ ข้อไหนควรปิดด้วย `// cppcheck-suppress` พร้อมเหตุผล

จบโมดูล 6 และจบหลักสูตรนี้แล้ว กลับไปดู [Checkpoint ท้ายโมดูล](../README.md) และ [หน้าหลักสูตร](../../README.md)
หลักสูตรต่อไปที่ใช้ทุกอย่างจากที่นี่คือ [หลักสูตรเฟิร์มแวร์ TESAIoT](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
