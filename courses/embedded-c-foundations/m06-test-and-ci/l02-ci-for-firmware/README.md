---
id: c-found.m06.l02
lang: th
title: {th: CI สำหรับเฟิร์มแวร์, en: CI for firmware}
summary: {th: ให้ GitHub Actions build ตรวจรูปแบบโค้ด วิเคราะห์แบบสถิต และรัน test ทุกการเปลี่ยนแปลง, en: 'Have GitHub Actions build, format-check, statically analyse and test every change.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m06.l01]
objectives:
- {th: เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request, en: Write a GitHub Actions workflow that runs the host unit tests on every pull request.}
- {th: เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck, en: Add a clang-format check and cppcheck static analysis.}
- {th: อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง, en: Explain what CI on public runners can check and what still needs a real board.}
develops:
- {skill: test.cicd, to: 3}
- {skill: vcs.git, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request
2. เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck
3. อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ต้องมีทุกอย่างจากบทเรียน 6.1 และ python3
ถ้าจะรันครบทุกขั้นในเครื่อง ต้องมี cppcheck และ gcc-arm-none-eabi ด้วย (บน Ubuntu: `sudo apt-get install cppcheck gcc-arm-none-eabi`)
แล็บต้องมีบัญชี GitHub

## ก่อนเริ่ม

ทวนสองข้อ

1. hook `pre-commit` ของบทเรียน 2.3 ตรวจทุก commit ในเครื่องคุณ ทำไมมันยังไม่พอสำหรับทีม (คำใบ้: `git commit --no-verify`)
2. บทเรียน 6.1 บอกว่า test ที่ผ่านพิสูจน์อะไรได้บ้าง และพิสูจน์ด้วยวิธีไหนว่ามันล้มเป็น

## ดูของจริงก่อน

repo ของ SDK ที่หลักสูตรนี้ใช้มี workflow ของ GitHub Actions อยู่ไฟล์เดียวที่ commit ef72c1b ข้างล่างคือส่วนหัวกับขั้นแรกของมัน

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  contents: read
# ... (concurrency และ env ละไว้)
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Ask the relay to re-read GitHub
        run: |
          set -euo pipefail
          echo "POST $RELAY/api/firmware/github/refresh"
          code=$(curl -s -o /tmp/refresh.json -w '%{http_code}' -X POST --max-time 120 \
                   "$RELAY/api/firmware/github/refresh")
          echo "HTTP $code"; cat /tmp/refresh.json; echo
          test "$code" = "200"
```

ที่มา: [.github/workflows/notify-flash-relay.yml บรรทัด 20-46](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.github/workflows/notify-flash-relay.yml#L20-L46)
(Apache-2.0, tesaiot-pse84-devkit-sdk)

**ทายก่อนอ่านต่อ** สามข้อ workflow นี้รันเมื่อไร มัน build เฟิร์มแวร์ไหม และถ้า `curl` ได้ HTTP 500 ขั้นนี้จะเขียวหรือแดง

คำตอบ: รันเมื่อมีการเผยแพร่ release (หรือกดรันเอง) มัน **ไม่ได้** build เฟิร์มแวร์ แค่บอก relay ของ Remote Flash ให้ดึง release ใหม่
แล้วขั้นถัดไปของไฟล์เดียวกันตรวจด้วย sha256 ว่าไฟล์ `.hex` ไปถึงจริง ("Firing the refresh is not the same as the file arriving")
ถ้าได้ 500 บรรทัดสุดท้าย `test "$code" = "200"` คืนค่าไม่ใช่ 0 ขั้นนี้จึงแดง บรรทัดนั้นคือสิ่งที่ทำให้ขั้นนี้ล้มเป็น ถ้าไม่มีมัน `echo` ข้างบนจะพิมพ์ 500 แล้วจบด้วย 0
บทเรียนนี้ใช้หลักเดียวกันกับทุกการตรวจ

## แนวคิด

### 1. workflow, job, step และ "workflow บาง สคริปต์หนา"

GitHub Actions อ่านไฟล์ YAML จาก `.github/workflows/` ของ repo ศัพท์สามคำที่ต้องแยกให้ออก

| คำ | คืออะไร | ในไฟล์ |
|---|---|---|
| workflow | ไฟล์หนึ่งไฟล์ ถูกปลุกด้วยเหตุการณ์ เช่น `pull_request` หรือ `push` | `on:` |
| job | งานหนึ่งชิ้นบนเครื่องเสมือนใหม่ของตัวเอง job ต่างกันรันขนานกันได้และไม่เห็นไฟล์ของกัน | `jobs.<ชื่อ>.runs-on` |
| step | คำสั่งหนึ่งขั้นใน job ขั้นที่คืนค่าไม่ใช่ 0 ทำให้ job ล้ม | `steps:` ที่มี `uses:` (action สำเร็จรูป) หรือ `run:` (คำสั่ง shell) |

ข้อตกลงสามข้อที่ใช้ตลอดบทนี้

- **workflow บาง สคริปต์หนา** ใส่คำสั่งตรวจจริงไว้ใน [ci.sh](examples/ci.sh) ใน repo แล้วให้ workflow แค่ติดตั้งเครื่องมือกับเรียก `bash ci.sh <ขั้น>`
  คุณรันคำสั่งเดียวกันทุกตัวอักษรในเครื่องได้ก่อน push ไม่ต้องรอ CI เพื่อรู้ผล
- **สิทธิ์น้อยที่สุด** เอกสาร GitHub แนะนำว่า "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents"
  คือ `permissions: contents: read` แบบเดียวกับ workflow ของ SDK ข้างบน และเมื่อระบุสิทธิ์ข้อใดข้อหนึ่ง สิทธิ์ที่ไม่ได้ระบุจะเป็น `none`
- **ล็อกทุกอย่างที่เปลี่ยนเองได้** tag อย่าง `v7` ของ action ถูกย้ายไปชี้ commit อื่นได้ เอกสาร GitHub ระบุว่า
  "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release"
  ป้ายชื่อ runner แบบ `ubuntu-latest` ก็ย้ายได้ ([runner-images](https://github.com/actions/runner-images) บอกว่ามัน "point towards the newest stable OS version available")
  ซึ่งเปลี่ยนรุ่นของ cppcheck และคอมไพเลอร์ที่ apt ให้ บทนี้จึงใช้ `ubuntu-24.04` และตั้ง `timeout-minutes` เพราะถ้าไม่ตั้ง job ที่ค้างจะรันได้ถึง 360 นาที

### 2. การตรวจสี่ขั้น และทำให้ทุกขั้นล้มเป็น

| ขั้น | เครื่องมือ | จับอะไรได้ |
|---|---|---|
| `tests` | Unity + `prove_red.sh` จากบทเรียน 6.1 | ตรรกะผิด และ test ที่ไม่ได้ทดสอบอะไร |
| `format` | clang-format 18.1.3 กับ [.clang-format](examples/.clang-format) | โค้ดที่จัดรูปแบบต่างจากที่ทีมตกลง ทำให้ diff ของ pull request อ่านง่ายขึ้น |
| `static` | cppcheck | บั๊กที่เห็นได้โดยไม่ต้องรัน เช่นเขียนเลยขอบอาร์เรย์ |
| `cross` | arm-none-eabi-gcc สำหรับ Cortex-M33 และ Cortex-M55 | โค้ดที่คอมไพล์ได้บนคอมพิวเตอร์แต่ไม่ได้บนไมโครคอนโทรลเลอร์ |

กับดักที่พบบ่อยที่สุดของ CI คือ **ขั้นที่รายงานปัญหาแต่ยังเขียว** เราทดลองกับเครื่องมือทั้งสองรุ่นที่บทนี้ใช้ ได้ผลตรงกัน

- `clang-format --dry-run` เจอโค้ดที่จัดรูปแบบผิด พิมพ์คำเตือน แล้วคืน 0 ต้องเติม `--Werror` จึงคืน 1
- `cppcheck` เจอ `arrayIndexOutOfBounds` พิมพ์ `error:` แล้วคืน 0 ต้องเติม `--error-exitcode=1`
- คำสั่งที่ต่อท้ายด้วย `|| true` หรือ step ที่ตั้ง `continue-on-error: true` เขียวเสมอ ไม่ว่าข้างในจะเกิดอะไร
- ใน bash `( ขั้นตอน ) || rc=$?` ปิด `set -e` ของทุกคำสั่งใน subshell คำสั่งที่ล้มกลางทางจะถูกข้ามแล้วจบด้วย 0 ([ci.sh](examples/ci.sh) มีบันทึกไว้ในฟังก์ชัน `run_stage`)

ขั้น `cross` ใช้แฟล็กของ Cortex-M33 ตาม Makefile ของไลบรารีในแม่แบบของ SDK

```make
# Toolchain (same as project)
GCC_PATH := /Applications/mtb-gcc-arm-eabi/14.2.1/gcc/bin
CC := $(GCC_PATH)/arm-none-eabi-gcc
AR := $(GCC_PATH)/arm-none-eabi-ar

# Compiler flags for PSoC Edge Cortex-M33 (MUST match project: softfp)
CFLAGS := -mcpu=cortex-m33 -mthumb -mfloat-abi=softfp -mfpu=fpv5-sp-d16
```

ที่มา: [bento_libs/claw/kit-pse84-ai/tesaiot/Makefile บรรทัด 25-31](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/Makefile#L25-L31)
(Apache-2.0, tesaiot-pse84-devkit-sdk)

สังเกต `GCC_PATH` ที่ชี้โฟลเดอร์บน macOS ของเครื่องหนึ่ง บน runner ของ CI บรรทัดนี้ใช้ไม่ได้ทันที CI จึงช่วยหาสมมติฐานเกี่ยวกับเครื่องที่ซ่อนอยู่แบบนี้ได้
และคอมไพเลอร์ของ ModusToolbox ในบรรทัดนั้นคือ GCC 14.2.1 ส่วน `gcc-arm-none-eabi` จาก apt ของ Ubuntu 24.04 คือ 13.2.1 ขั้น `cross` จึงตรวจว่าตรรกะ **คอมไพล์ได้** สำหรับ CPU ของบอร์ด
ไม่ได้สร้างไบนารีเดียวกับที่ build จริง

### 3. CI บน runner สาธารณะตรวจอะไรได้ และอะไรต้องใช้บอร์ด

| CI บน runner สาธารณะตรวจได้ | ต้องใช้บอร์ดจริง |
|---|---|
| ตรรกะที่อยู่หลังตะเข็บ (บทเรียน 6.1) | timing ของ interrupt และตัวตั้งเวลา (บทเรียน 4.1, 4.2) |
| รูปแบบโค้ดและบั๊กที่วิเคราะห์ได้แบบสถิต | cache กับ DMA และลำดับของ barrier (บทเรียน 4.4) test บนคอมพิวเตอร์ของบทนั้นจำลองได้ แต่พิสูจน์ไม่ได้ |
| ตรรกะคอมไพล์ได้สำหรับ Cortex-M33 และ Cortex-M55 | สัญญาณจริงบนบัส UART, I2C, SPI (โมดูล 5) |
| ไฟล์ที่ไม่ควรเข้า repo เช่นที่ hook ของบทเรียน 2.3 ตรวจ | watchdog รีเซ็ตจริง และบอร์ดบูตขึ้นหลังถอดสายเสียบใหม่ (บทเรียน 4.3, 2.1) |

ทำไมไม่ build เฟิร์มแวร์ทั้งก้อนใน CI เลย Makefile เดียวกันบอกเหตุผลข้อหนึ่งไว้ตรง ๆ
"Source files (tesaiot_*.c) are proprietary" และแจก `libtesaiot.a` ที่ build แล้วให้แทน
([บรรทัด 10-11](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/Makefile#L10-L11))
ส่วน git repo ของ SDK เองก็ไม่มีไฟล์ `.a` เพราะ `.gitignore` ตัดทิ้ง บทเรียน 2.1 จึงให้ build จากไฟล์ zip ของ release
build เต็มจึงต้องใช้ ModusToolbox ที่ติดตั้งครบกับแพ็กเกจของ release ซึ่งทำบนเครื่องของคุณตาม [บทเรียน 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md)
และ [ขั้นตอน build และ flash ของหลักสูตรเฟิร์มแวร์ TESAIoT](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)

ทางต่อบอร์ดเข้ากับ CI คือ self-hosted runner ที่มีบอร์ดเสียบอยู่ (hardware-in-the-loop) แต่เอกสาร GitHub เตือนว่า
"Self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull requests against the repository and compromise the environment"
repo สาธารณะจึงควรเก็บการทดสอบบนบอร์ดไว้ใน repo ส่วนตัวหรือทำด้วยมือ แล้วบันทึกหลักฐานไว้

## ตัวอย่างสมบูรณ์

โฟลเดอร์ [examples/](examples/) มีห้าไฟล์

- [host-tests.yml](examples/host-tests.yml) workflow ที่เล็กที่สุดที่ใช้ได้จริง job เดียว รัน test ของบทเรียน 6.1 ความเห็นในไฟล์อธิบาย workflow, job และ step
- [ci.sh](examples/ci.sh) การตรวจสี่ขั้น ทุกขั้นจบด้วย `PASS`, `FAIL` หรือ `NOT CHECKED` (เครื่องมือไม่มี หรือไม่มีไฟล์ให้ตรวจ) และ `NOT CHECKED` คืนค่าที่ไม่ใช่ 0 เหมือน `FAIL`
- [.clang-format](examples/.clang-format) รูปแบบโค้ดของหลักสูตร ไฟล์ C ของบทเรียน 6.1 จัดรูปแบบด้วยไฟล์นี้แล้ว
- [check_workflow.py](examples/check_workflow.py) ตรวจโครงของ workflow สี่ job ตามกติกาของบทนี้ในเครื่อง (ไม่ได้รัน workflow จริง)
- [.gitignore](examples/.gitignore) กัน `.venv/` ที่สร้างตอนฝึก

รันทั้งสี่ขั้นกับโค้ดของบทเรียน 6.1 ในเครื่อง (ต้อง clone Unity ไว้ใน `examples/unity` ของบทเรียน 6.1 ก่อน)

```sh
cd examples
python3 -m venv .venv
.venv/bin/pip install clang-format==18.1.3 pyyaml==6.0.3
SRC_DIR=../../l01-unit-tests-on-host/examples TEST=../solution/test_level_alarm.c \
  CLANG_FORMAT=.venv/bin/clang-format bash ci.sh all
```

ผลที่เราได้คือ `tests`, `format`, `static` และ `cross` ขึ้น `PASS` ทั้งสี่ขั้น ถ้าเครื่องคุณไม่มี cppcheck ขั้น `static` จะขึ้น `NOT CHECKED` และคำสั่งจบด้วยค่าที่ไม่ใช่ 0 ซึ่งถูกต้อง

**ลองทำให้แต่ละขั้นแดง แล้วทายก่อนรัน** ทำในสำเนาของโฟลเดอร์ตัวอย่าง 6.1 ไม่ใช่ไฟล์จริง

1. `format` ลบช่องว่างรอบ `=` ในบรรทัด `a->count = 0u;` หนึ่งบรรทัด
2. `static` เพิ่มฟังก์ชันที่วน `for (int i = 0; i <= 4; i++)` เขียนลง `int history[4]`
3. `cross` เพิ่ม `_Static_assert(sizeof(long) == 8, "assumes a 64-bit long");` ใต้ `#include` ขั้น `tests` ยังผ่าน เพราะ `long` บนคอมพิวเตอร์ 64 บิตยาว 8 ไบต์ แต่ `cross` แดง เพราะบน Cortex-M ยาว 4 ไบต์ ขนาดของชนิดข้อมูลขึ้นกับสถาปัตยกรรม (บทเรียน 1.1)
4. `tests` ใช้ `TEST=test_level_alarm_first.c` test ทั้งสองข้อผ่าน แต่ขั้นนี้แดง เพราะ `prove_red.sh` พบบั๊กที่รอด

## ฝึกเติม

เปิด [practice/firmware-ci.yml](practice/firmware-ci.yml) job `tests` ให้มาแล้ว มีช่องให้เติม 6 จุด มากกว่าบทก่อนตามจังหวะของโมดูล

1. รันกับทุก pull request ด้วย
2. จำกัดสิทธิ์ของ `GITHUB_TOKEN` ให้อ่านได้อย่างเดียว
3. ล็อก action ทุกตัวด้วย commit SHA เต็ม
4. job `format` ติดตั้ง clang-format รุ่นที่ล็อกไว้ แล้วรัน `bash ci.sh format`
5. job `static-analysis` ติดตั้ง cppcheck แล้วรัน `bash ci.sh static`
6. job `cross-compile` ติดตั้ง gcc-arm-none-eabi แล้วรัน `bash ci.sh cross`

ตรวจในเครื่องก่อน push

```sh
cd examples
.venv/bin/python check_workflow.py ../practice/firmware-ci.yml
```

ก่อนเติม ตัวตรวจขึ้น `10 failed` งานจะเสร็จเมื่อขึ้น `0 failed` ตัวตรวจนี้จับ `|| true` และ `continue-on-error` ด้วย ลองใส่ดูแล้วดูมันแดง

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/firmware-ci.yml](solution/firmware-ci.yml) เราตรวจเฉลยแล้วว่าตัวตรวจขึ้น `21 passed, 0 failed`
สิ่งที่ควรเทียบ

- job `format` ติดตั้ง clang-format ด้วย pip ที่รุ่น 18.1.3 แทนตัวที่มากับ runner เพราะ image ของ `ubuntu-24.04` มี clang-format สามรุ่น (16.0.6, 17.0.6, 18.1.3 ตาม
  [รายการของ image](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) รุ่น 20260920) และรุ่นต่างกันจัดรูปแบบต่างกันได้
  pip ให้รุ่นเดียวกันทั้งบน runner บน Windows และบน macOS
- `concurrency` ที่ `cancel-in-progress: true` ยกเลิกรอบเก่าเมื่อ push ใหม่เข้า pull request เดิม ขณะที่ workflow ของ SDK ตั้ง `false`
  ให้รอบที่เริ่มแล้วทำจนจบ ค่าที่ถูกขึ้นกับงาน: การตรวจโค้ดรอบเก่าไม่มีประโยชน์เมื่อมีโค้ดใหม่ แต่การแจ้งเตือนที่ถูกยกเลิกกลางทางอาจไม่ถึงปลายทาง

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** ให้ GitHub ตรวจงานของคุณทุก pull request แล้วพิสูจน์ว่ามันแดงเป็น

1. สร้าง repo ของคุณเอง (ส่วนตัวหรือสาธารณะก็ได้) วางไฟล์ตามโครงนี้
   `ci.sh` และ `.clang-format` จากบทนี้ไว้ที่ราก, โฟลเดอร์ `host-tests/` ที่มีไฟล์จาก `examples/` ของบทเรียน 6.1 (ยกเว้น `unity/` และ `build/`)
   พร้อม `test_level_alarm.c` ที่คุณเติมครบแล้ว และ workflow ที่คุณเขียนไว้ที่ `.github/workflows/firmware-ci.yml`
   (ถ้าทำแล็บของบทเรียน 6.1 ด้วยตรรกะของคุณเอง ใช้ของคุณได้ ปรับชื่อไฟล์ใน `prove_red.sh` ให้ตรง)
2. push แล้วเปิดแท็บ Actions ทั้งสี่ job ต้องเขียว
3. เปิด pull request ที่ใส่บั๊กหนึ่งจุดจากหัวข้อตัวอย่างสมบูรณ์ ดู job ที่ควรแดงว่าแดงจริง แล้วปิด pull request นั้นโดยไม่ merge
4. ย้ายการตรวจหนึ่งอย่างจาก hook `pre-commit` ของบทเรียน 2.3 มาเป็นขั้นใน `ci.sh` แล้วพิสูจน์ด้วย pull request ว่า `--no-verify` ข้ามมันไม่ได้อีก
5. ถ้ามีบอร์ด เขียนสั้น ๆ ว่าการเปลี่ยนแปลงแบบไหนใน repo นี้ที่ CI เขียวแล้วคุณยังต้อง flash ลงบอร์ดเพื่อตรวจ และตรวจอะไร

**หลักฐานที่เก็บไว้ใน portfolio:** ลิงก์ของ repo ภาพหรือลิงก์ของรอบที่เขียวครบ ลิงก์ของ pull request ที่แดง พร้อมบอกว่าบั๊กคืออะไรและ job ไหนจับได้
และคำตอบของข้อ 5

## ไปต่อ

- อ่าน workflow ของ SDK ทั้งไฟล์ [notify-flash-relay.yml](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.github/workflows/notify-flash-relay.yml)
  ขั้นที่สองตรวจอะไร และทำไมผู้เขียนแยกมันออกจาก workflow อื่นที่รันเมื่อมี release เหมือนกัน
  (ความเห็นหัวไฟล์อ้างถึง `firmware-index.yml` ซึ่งไม่มีใน commit นี้ แต่เหตุผลอยู่ในความเห็นครบ)
- ลองเปิด `--enable=style` ของ cppcheck กับโค้ดของคุณ ข้อความไหนมีประโยชน์ ข้อไหนควรปิดด้วย `// cppcheck-suppress` พร้อมเหตุผล

จบโมดูล 6 และจบหลักสูตรนี้แล้ว กลับไปดู [Checkpoint ท้ายโมดูล](../README.md) และ [หน้าหลักสูตร](../../README.md)
หลักสูตรต่อไปที่ใช้ทุกอย่างจากที่นี่คือ [หลักสูตรเฟิร์มแวร์ TESAIoT](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)

## สะท้อนคิด

- ถ้า CI เขียวทุกรอบมาหกเดือน คุณจะรู้ได้อย่างไรว่ามันยังตรวจอะไรอยู่
- ส่วนไหนของงานคุณที่ยังพึ่ง "เครื่องของฉันผ่าน" และต้องทำอะไรจึงย้ายมันเข้า CI ได้

## แหล่งอ้างอิง

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
- [Cppcheck](https://cppcheck.sourceforge.io/)
- [GitHub Docs: Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [GitHub Docs: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [actions/runner-images](https://github.com/actions/runner-images)
