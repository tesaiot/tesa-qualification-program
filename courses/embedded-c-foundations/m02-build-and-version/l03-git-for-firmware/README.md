---
id: c-found.m02.l03
lang: th
title: {th: Git สำหรับงานเฟิร์มแวร์, en: Git for firmware work}
summary: {th: 'เก็บประวัติของเฟิร์มแวร์ด้วย commit, branch และ tag โดยไม่เก็บไฟล์ build และข้อมูลลับ', en: 'Keep firmware history with commits, branches and tags, without build outputs or secrets.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l02]
objectives:
- {th: สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี .gitignore ตัดไฟล์ build และ dependency ที่ดึงมา, en: Create a firmware repository whose .gitignore excludes build outputs and fetched dependencies.}
- {th: ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล, en: 'Use branches for new work and tags for released firmware, with commit messages that explain why.'}
- {th: ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ, en: 'Check before pushing that no WiFi password, key or token is in history, and explain why deleting it later is not enough.'}
develops:
- {skill: vcs.git, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี .gitignore ตัดไฟล์ build และ dependency ที่ดึงมา
2. ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล
3. ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ต้องมี Git และ bash บนเครื่อง

## ก่อนเริ่ม

ทวนจากบทเรียน 2.1 และ 2.2 สองข้อ

1. โฟลเดอร์ไหนบ้างที่เกิดขึ้นหลัง `make getlibs` และ `make build` และมีขนาดราวเท่าไร
2. ถ้า Makefile ตั้ง `ENABLE_PAGE_EXAMPLES ?= 0` แล้วคุณเปิดตัวอย่างด้วย command line บันทึกการ build ของคุณต้องจดอะไรเพิ่ม

## ดูของจริงก่อน

ในโฟลเดอร์แม่แบบที่คุณ build ไว้ในบทเรียน 2.1 ลองให้ Git นับว่าถ้า commit ทั้งหมดตอนนี้จะมีกี่ไฟล์

```sh
cd bento-firmware-template-mtb-only
git init
git status --short --untracked-files=all | wc -l
du -sh build proj_*/build 2>/dev/null
```

**ทายก่อนรัน** ว่าตัวเลขบรรทัดแรกมีกี่พัน แล้วดูว่าโฟลเดอร์ build รวมกันใหญ่เท่าไร ไฟล์เหล่านั้นสร้างใหม่ได้ทุกไบต์ด้วย `make build`
ถ้าเก็บลงประวัติ repository จะบวมขึ้นทุกครั้งที่ build และ diff จะเต็มไปด้วยไฟล์ที่ไม่มีใครอ่าน
จากนั้นคัดลอก [examples/firmware.gitignore](examples/firmware.gitignore) ไปเป็น `.gitignore` แล้วนับใหม่ ตัวเลขที่ลดลงคือของที่ไม่ควรอยู่ในประวัติ

## แนวคิด

### 1. อะไรควรอยู่ใน repository และอะไรไม่ควร

หลักเดียวคือ **เก็บสิ่งที่สร้างใหม่ไม่ได้ ไม่เก็บสิ่งที่สร้างใหม่ได้** .gitignore ระดับบนสุดของ SDK เขียนหลักนี้ไว้ในคอมเมนต์บรรทัดแรก

```gitignore
# Build output. Every one of these is reproducible from what is committed.
build/
build-*/
mtb_shared/
*.o
*.a
.DS_Store
```

ที่มา: [.gitignore ของ tesaiot-pse84-devkit-sdk บรรทัด 1-7](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.gitignore#L1-L7) (Apache-2.0, tesaiot-pse84-devkit-sdk)

| เก็บ | ไม่เก็บ |
|---|---|
| ซอร์ส `.c` `.h` Makefile และ `*.mk` | `build/` และ `build-*/` ของทุกโปรเจกต์ |
| `deps/*.mtb` ที่บอกว่าจะดึงอะไรที่รุ่นไหน | `mtb_shared/` (ดึงใหม่ได้ด้วย `make getlibs`) |
| การตั้งค่า BSP และไฟล์ที่ Configurator สร้าง ซึ่งแม่แบบของ SDK ก็เก็บไว้ | `.o` `.elf` `.hex` `.map` (hex ที่ปล่อยจริงให้แนบกับ release) |
| `LICENSE` และ `NOTICE` ของแม่แบบ (Apache-2.0 กำหนดให้คงไว้) | ไฟล์ข้อมูลลับของเครื่องคุณ |

สังเกตบรรทัด `*.a` ในไฟล์ของ SDK ผลคือ repository สาธารณะไม่มีไลบรารี prebuilt เลย มันมากับ zip ของ release (บทเรียน 2.1)
โปรเจกต์ของคุณต้องตัดสินใจเรื่องนี้เองอย่างตั้งใจ ไฟล์ตัวอย่างของเราจึงเขียนเป็นทางเลือกไว้ท้ายไฟล์
อีกข้อที่ต้องรู้: `.gitignore` มีผลแค่กับไฟล์ที่ **ยังไม่เคยถูก track** ไฟล์ที่ commit ไปแล้วต้องเอาออกด้วย `git rm --cached <path>`
และใครก็บังคับเพิ่มไฟล์ที่ถูก ignore ได้ด้วย `git add -f` เราจึงมี hook ตรวจซ้ำอีกชั้น

### 2. branch สำหรับงาน tag สำหรับของที่ปล่อย ข้อความ commit สำหรับเหตุผล

- **branch** แยกงานหนึ่งเรื่องออกจากสายหลัก `git switch -c fix/sw2-debounce` ทำเสร็จ ทดสอบบนบอร์ด แล้วค่อยรวมกลับ
  สายหลักจึงอยู่ในสภาพที่ build และ flash ได้เสมอ
- **tag** ตรึงชื่อไว้กับ commit ที่กลายเป็นเฟิร์มแวร์ที่ส่งมอบจริง ใช้แบบ annotated `git tag -a fw-v0.1.0 -m "..."` แล้ว `git push origin fw-v0.1.0`
  SDK ใช้หลักเดียวกัน release ของมันชื่อแบบ `fw-c-only-v1.10.0` และแนบ hex กับ `SHA256SUMS.txt` ไว้ที่ release ไม่ได้ commit hex
- **ข้อความ commit** บรรทัดแรกบอกว่าทำอะไร เนื้อความบอก **ทำไม** และหลักฐาน diff บอกได้ว่าเปลี่ยนอะไร แต่บอกไม่ได้ว่าทำไม
  อีกหกเดือนคนที่เจอบรรทัดแปลก ๆ จะอยากรู้เหตุผลมากกว่าอย่างอื่น

เทียบข้อความสองแบบของการเปลี่ยนแปลงเดียวกัน (ข้อความสมมติ ตัวเลขในนั้นเป็นตัวอย่าง ไม่ใช่ผลวัดจริง)

```text
แบบที่ไม่ช่วยใคร:   fix button

แบบที่ช่วย:        Debounce SW2 in time, not by reading the pin twice

                   Two reads 200 ns apart sample the same bounce, so one press
                   counted two or three times on the bench (10 presses -> 23).
                   Require 3 agreeing polls at 10 ms, as the SDK's
                   io/04_gpio_led_button.c does.
                   Evidence: 10 presses -> 10 counts, board A, commit abc1234.
                   Not verified: long presses over 5 s.
```

SDK เองเขียนเหตุผลแบบนี้ไว้ในคอมเมนต์ของโค้ดทุกไฟล์ที่เราอ่านมาตลอดโมดูล 1 นิสัยเดียวกันใช้กับข้อความ commit ได้
แม่แบบข้อความอยู่ใน [examples/commit-template.txt](examples/commit-template.txt)

### 3. ข้อมูลลับในประวัติ: ลบทีหลังไม่พอ

Git เก็บ **ทุกรุ่น** ของทุกไฟล์ ถ้าคุณ commit รหัส WiFi ไปหนึ่งครั้งแล้ว commit ถัดไปลบออก รหัสยังอยู่ใน commit ก่อนหน้า
ใครที่ clone หรือ fork ไปแล้วมีสำเนาครบ และ `git log -p` ของเขาจะแสดงมันออกมา การเขียนประวัติใหม่ด้วยเครื่องมืออย่าง `git filter-repo`
แล้ว force push ลบได้แค่ในสำเนาของคุณ ไม่ได้ลบในเครื่องคนอื่น ดังนั้นเมื่อความลับหลุดไปแล้ว สิ่งแรกที่ต้องทำคือ **เปลี่ยนรหัสหรือเพิกถอนกุญแจนั้น**
การล้างประวัติมาทีหลัง และทำเพื่อไม่ให้หลุดซ้ำเท่านั้น

ทางที่ถูกคือไม่ให้ความลับเข้าไปในซอร์สตั้งแต่ต้น ตัวอย่าง WiFi ของ SDK เขียนหลักนี้ไว้ตรง ๆ ว่า
"A credential compiled into an example is a credential in a public repository."
([10_wifi_join.c บรรทัด 71-84](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c#L71-L84))
มันจึงอ่าน SSID และรหัสจากที่เก็บบนบอร์ด ไม่ใช่จาก `#define` สำหรับค่าที่จำเป็นต้องอยู่ในไฟล์ระหว่างพัฒนา ให้ใช้ไฟล์ที่ถูก ignore
แล้ว commit ไฟล์ตัวอย่างที่มีแต่ค่าตัวแทน เช่น `"<your-password>"` ไว้ข้าง ๆ

ก่อน push ให้ค้นทั้งประวัติ ไม่ใช่แค่ไฟล์ปัจจุบัน

```sh
git grep -nIiE '(pass(word)?|secret|token|api_key)' $(git rev-list --all)   # ทุก commit ในทุก branch
git log -p --all -S 'PRIVATE KEY'                                         # commit ที่เพิ่มหรือลบข้อความนี้
```

คลังความรู้ TESA Open Knowledge ที่คุณกำลังอ่านก็ตรวจแบบเดียวกันกับทุกไฟล์ก่อนเผยแพร่ ด้วยตัวตรวจ `secrets` ใน `tools/validate.py`

## ตัวอย่างสมบูรณ์

ลำดับการตั้ง repository ของโปรเจกต์ที่แตกจากแม่แบบ ทำในโฟลเดอร์ `bento-firmware-template-mtb-only` ของคุณ

**ท่าที่ 1 เริ่ม repository ที่สะอาด**

```sh
git init
cp <ที่อยู่ของบทเรียนนี้>/examples/firmware.gitignore .gitignore
git status --short --untracked-files=all | wc -l        # ต้องลดลงจากตอนก่อนมี .gitignore
git add .
git commit -m "Import bento-firmware-template-mtb-only from fw-c-only-v1.10.0"
```

**ท่าที่ 2 ทำงานบน branch แล้ว tag สิ่งที่ปล่อย**

```sh
git switch -c docs/build-record
mkdir -p docs && cp <build-record ที่เติมในบทเรียน 2.1> docs/build-record.md
git add docs/build-record.md
git commit                                                # เขียนเหตุผลตามแม่แบบ commit-template.txt
git switch main && git merge --no-ff docs/build-record
git tag -a fw-v0.1.0 -m "First build of the template on board A; record in docs/build-record.md"
git log --oneline --decorate --graph -5
```

(ถ้าสายหลักของคุณชื่อ `master` ให้ใช้ชื่อนั้นแทน `main`)

**ท่าที่ 3 ติดตั้ง hook แล้วลองให้มันปฏิเสธ**

```sh
cp <ที่อยู่ของบทเรียนนี้>/solution/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
printf '#define WIFI_PASSWORD "not-a-placeholder"\n' > wifi_secrets_test.h
git add -f wifi_secrets_test.h && git commit -m "test"    # ต้องถูกปฏิเสธ
git reset -q wifi_secrets_test.h && rm wifi_secrets_test.h
```

ข้อความ `blocked: looks like a real secret` คือสิ่งที่ควรเห็น แล้วลองเปลี่ยนค่าเป็น `"<your-password>"` ดูว่าคราวนี้ hook ยอมหรือไม่
(ใช้ `git add -f` เพราะชื่อไฟล์นี้ถูก `.gitignore` ตัดอยู่แล้ว นี่คือเหตุผลที่ต้องมี hook อีกชั้น)

## ฝึกเติม

เปิด [practice/pre-commit.sh](practice/pre-commit.sh) มีช่องให้เติม 4 จุด มากกว่าบทก่อนตามจังหวะของโมดูล

1. หารายชื่อไฟล์ที่ถูก stage
2. ปฏิเสธไฟล์ใน `build/` `build-*/` `mtb_shared/` และ `.o`
3. ปฏิเสธบรรทัดที่เพิ่มใหม่ซึ่งให้ค่าจริงกับชื่อที่ดูเป็นความลับ แต่ยอมค่าตัวแทน `<...>` และค่าว่าง
4. ปฏิเสธบรรทัดหัวของไฟล์กุญแจส่วนตัว

ตรวจงานด้วย test ที่สร้าง repository ชั่วคราวใหม่ทุกกรณีและลบทิ้งเอง ไม่แตะ repository ของคุณ

```sh
bash examples/test_hook.sh practice/pre-commit.sh
```

ก่อนเติมจะเห็น `3 passed, 6 failed` สามกรณีที่ผ่านคือกรณีที่ hook ต้อง "ยอม" ซึ่ง hook ที่ไม่ทำอะไรเลยก็ผ่าน
ถ้ามี test แค่สามกรณีนั้น hook เปล่า ๆ จะดูเหมือนทำงานได้ นี่คือเหตุผลที่ต้องมีกรณีที่ต้อง "ปฏิเสธ" ด้วย

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/pre-commit.sh](solution/pre-commit.sh) จุดที่ควรเทียบ

- `--diff-filter=ACM` ไม่ตรวจไฟล์ที่ถูกลบ และคำสั่งนี้ทำงานได้แม้ใน commit แรกที่ยังไม่มี `HEAD`
- รูปแบบ `"[^"<]` คือหัวใจของการแยกค่าจริงออกจากค่าตัวแทน ค่าที่ขึ้นต้นด้วย `<` และค่าว่างผ่าน
- hook พิมพ์บรรทัดที่เจอความลับเพื่อให้คนแก้ได้ แต่ไม่พิมพ์เนื้อหาของกุญแจส่วนตัว เพราะ log ก็อาจถูกคัดลอกไปวางที่อื่น
- hook แบบนี้มี false positive ได้ เช่นตัวแปรชื่อ `TEST_PASSED` ยอมรับข้อจำกัดนี้ไว้ แล้วแก้ชื่อหรือรูปแบบเมื่อเจอ ไม่ใช่ปิด hook ทิ้ง

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** นำโปรเจกต์ที่แตกจากแม่แบบเข้า Git ให้พร้อมทำงานเป็นทีม โดยมีหลักฐานว่าไม่มีไฟล์ build และไม่มีความลับ

1. ทำท่าที่ 1 ถึง 3 จนได้ commit แรก branch หนึ่งเส้นที่รวมกลับแล้ว และ tag `fw-v0.1.0` บน commit ที่คุณ build และ flash สำเร็จ
2. build ใหม่ด้วย `make build -j` แล้วรัน `git status --short` ผลต้องว่าง ถ้ามีไฟล์โผล่มา ให้แก้ `.gitignore` แล้วอธิบายว่าไฟล์นั้นคืออะไร
3. รันคำสั่งค้นประวัติทั้งสองบรรทัดในแนวคิดข้อ 3 บันทึกว่าเจออะไร ถ้าเจอคำอย่าง `password` ในซอร์สของแม่แบบ ให้เปิดดูว่าเป็นค่าจริงหรือแค่ชื่อฟิลด์หรือคอมเมนต์
4. ถ้ามี remote (เช่น repository ส่วนตัวบน GitHub) ให้ push ทั้ง branch และ tag แล้วตรวจบนหน้าเว็บว่า tag ชี้ commit ที่ถูกต้อง

**หลักฐานที่เก็บไว้ใน portfolio:** ผลของ `git log --oneline --decorate --graph` ที่เห็น branch ที่รวมแล้วและ tag, ผลของ `git status --short` หลัง build ที่ว่าง,
ข้อความที่ hook ปฏิเสธ commit ทดสอบ และผลการค้นประวัติพร้อมคำอธิบาย

## ไปต่อ

- อ่าน [Pro Git](https://git-scm.com/book/en/v2) บท "Git Branching" และหัวข้อ "Tagging" แล้วลองตั้งกติกาชื่อ tag ของทีมคุณให้บอกได้ทั้ง variant และรุ่น แบบที่ SDK ทำ
- ลองย้ายการตรวจของ hook ไปรันใน CI ด้วย ซึ่งข้ามด้วย `--no-verify` ไม่ได้ เรื่องนี้คือบทเรียน 6.2

บทถัดไปเข้าสู่โมดูล 3: [บทเรียน 3.1 SWD และ GDB เบื้องต้น](../../m03-debugging/l01-swd-and-gdb/README.md)

## สะท้อนคิด

- ถ้าพรุ่งนี้คุณพบว่า token ของคลาวด์หลุดเข้าไปใน commit เมื่อสามสัปดาห์ก่อน และมีเพื่อน clone ไปแล้วห้าคน คุณจะทำอะไรเป็นอย่างแรก และทำไม
- ข้อความ commit ของคุณในสัปดาห์ที่ผ่านมา มีกี่ข้อความที่อีกหกเดือนคุณจะยังเข้าใจเหตุผล

## แหล่งอ้างอิง

- [Pro Git (หนังสือ Git ฉบับเปิด)](https://git-scm.com/book/en/v2)
- [SDK: แม่แบบ mtb-only README (สิ่งที่ getlibs ดึงมา และไฟล์ที่ต้องจัดหาเอง)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: .gitignore ระดับบนสุดของ repository](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.gitignore)
- [SDK: cm33/connectivity/10_wifi_join.c (ข้อมูลรับรองมาจากที่เก็บ ไม่ใช่จาก #define)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c)
- [SDK: release fw-c-only-v1.10.0 (ตัวอย่างการตั้งชื่อ tag และแนบ hex กับ SHA256SUMS)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/releases/tag/fw-c-only-v1.10.0)
