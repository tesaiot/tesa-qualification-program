---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.3 — Git สำหรับงานเฟิร์มแวร์"
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

# บทเรียน 2.3 — Git สำหรับงานเฟิร์มแวร์

## เก็บประวัติของเฟิร์มแวร์ด้วย commit, branch และ tag โดยไม่เก็บไฟล์ build และข้อมูลลับ

**โมดูล 2 — Build ด้วย ModusToolbox และ Make และ Git สำหรับเฟิร์มแวร์**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 2.2

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี `.gitignore` ตัดไฟล์ build และ dependency ที่ดึงมา
2. ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล
3. ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ

ใช้เวลาประมาณ 70 นาที ต้องมี Git และ bash บนเครื่อง

---

## ก่อนเริ่ม

ทวนจากบทเรียน 2.1 และ 2.2 สองข้อ

1. โฟลเดอร์ไหนบ้างที่เกิดขึ้นหลัง `make getlibs` และ `make build` และมีขนาดราวเท่าไร
2. ถ้า Makefile ตั้ง `ENABLE_PAGE_EXAMPLES ?= 0` แล้วคุณเปิดตัวอย่างด้วย command line บันทึกการ build ของคุณต้องจดอะไรเพิ่ม

---

## ดูของจริงก่อน

ในโฟลเดอร์แม่แบบที่ build ไว้ ลองให้ Git นับว่าถ้า commit ทั้งหมดตอนนี้จะมีกี่ไฟล์

```sh
cd bento-firmware-template-mtb-only
git init
git status --short --untracked-files=all | wc -l
du -sh build proj_*/build 2>/dev/null
```

**ทายก่อนรัน**: ตัวเลขบรรทัดแรกมีกี่พัน — ไฟล์เหล่านั้นสร้างใหม่ได้ทุกไบต์ด้วย `make build` ถ้าเก็บลงประวัติ repository จะบวมขึ้นทุกครั้งที่ build

จากนั้นคัดลอก [examples/firmware.gitignore](examples/firmware.gitignore) ไปเป็น `.gitignore` แล้วนับใหม่ — ตัวเลขที่ลดลงคือของที่ไม่ควรอยู่ในประวัติ

---

## แนวคิด (1) — อะไรควรอยู่ใน repository และอะไรไม่ควร

หลักเดียว: **เก็บสิ่งที่สร้างใหม่ไม่ได้ ไม่เก็บสิ่งที่สร้างใหม่ได้**

```gitignore
# Build output. Every one of these is reproducible from what is committed.
build/
build-*/
mtb_shared/
*.o
*.a
```

| เก็บ | ไม่เก็บ |
|---|---|
| ซอร์ส `.c` `.h` Makefile และ `*.mk` | `build/` `build-*/` ของทุกโปรเจกต์ |
| `deps/*.mtb` ที่บอกจะดึงอะไรรุ่นไหน | `mtb_shared/` (ดึงใหม่ได้ด้วย `make getlibs`) |
| การตั้งค่า BSP ที่ Configurator สร้าง | `.o` `.elf` `.hex` `.map` |
| `LICENSE`, `NOTICE` | ไฟล์ข้อมูลลับของเครื่องคุณ |

> `.gitignore` มีผลแค่กับไฟล์ที่**ยังไม่เคยถูก track** — ไฟล์ที่ commit ไปแล้วต้องเอาออกด้วย `git rm --cached <path>`

---

## แนวคิด (2) — branch สำหรับงาน tag สำหรับของที่ปล่อย

- **branch** แยกงานหนึ่งเรื่องออกจากสายหลัก — `git switch -c fix/sw2-debounce` ทำเสร็จ ทดสอบบนบอร์ด แล้วค่อยรวมกลับ สายหลักจึงอยู่ในสภาพที่ build/flash ได้เสมอ
- **tag** ตรึงชื่อไว้กับ commit ที่กลายเป็นเฟิร์มแวร์ที่ส่งมอบจริง `git tag -a fw-v0.1.0 -m "..."` — SDK ใช้หลักเดียวกัน ชื่อแบบ `fw-c-only-v1.10.0` แนบ hex กับ `SHA256SUMS.txt` ไว้ที่ release ไม่ได้ commit hex
- **ข้อความ commit** บรรทัดแรกบอกว่าทำอะไร เนื้อความบอก **ทำไม** — diff บอกได้ว่าเปลี่ยนอะไร แต่บอกไม่ได้ว่าทำไม

```text
แบบที่ไม่ช่วยใคร:   fix button
แบบที่ช่วย:        Debounce SW2 in time, not by reading the pin twice
                   Two reads 200 ns apart sample the same bounce...
                   Evidence: 10 presses -> 10 counts, board A, commit abc1234.
```

---

## แนวคิด (3) — ข้อมูลลับในประวัติ: ลบทีหลังไม่พอ

Git เก็บ **ทุกรุ่น** ของทุกไฟล์ ถ้า commit รหัส WiFi ไปหนึ่งครั้งแล้ว commit ถัดไปลบออก รหัสยังอยู่ใน commit ก่อนหน้า ใครที่ clone หรือ fork ไปแล้วมีสำเนาครบ

การเขียนประวัติใหม่ (`git filter-repo`) แล้ว force push ลบได้แค่ในสำเนาของคุณ **ไม่ได้ลบในเครื่องคนอื่น** — เมื่อความลับหลุดไปแล้ว สิ่งแรกที่ต้องทำคือ **เปลี่ยนรหัสหรือเพิกถอนกุญแจนั้น** การล้างประวัติมาทีหลังและทำเพื่อไม่ให้หลุดซ้ำเท่านั้น

ตัวอย่าง WiFi ของ SDK เขียนหลักนี้ตรง ๆ ว่า **"A credential compiled into an example is a credential in a public repository."** — มันอ่าน SSID/รหัสจากที่เก็บบนบอร์ด ไม่ใช่จาก `#define`

```sh
git grep -nIiE '(pass(word)?|secret|token|api_key)' $(git rev-list --all)
git log -p --all -S 'PRIVATE KEY'
```

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 1/2 repository สะอาด แล้ว branch/tag

```sh
# ท่าที่ 1: เริ่ม repository ที่สะอาด
git init
cp examples/firmware.gitignore .gitignore
git add . && git commit -m "Import bento-firmware-template-mtb-only from fw-c-only-v1.10.0"

# ท่าที่ 2: ทำงานบน branch แล้ว tag สิ่งที่ปล่อย
git switch -c docs/build-record
git add docs/build-record.md && git commit    # เขียนเหตุผลตามแม่แบบ commit-template.txt
git switch main && git merge --no-ff docs/build-record
git tag -a fw-v0.1.0 -m "First build of the template on board A"
```

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 3 ติดตั้ง hook แล้วลองให้มันปฏิเสธ

```sh
cp solution/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
printf '#define WIFI_PASSWORD "not-a-placeholder"\n' > wifi_secrets_test.h
git add -f wifi_secrets_test.h && git commit -m "test"    # ต้องถูกปฏิเสธ
git reset -q wifi_secrets_test.h && rm wifi_secrets_test.h
```

ข้อความ `blocked: looks like a real secret` คือสิ่งที่ควรเห็น แล้วลองเปลี่ยนค่าเป็น `"<your-password>"` ดูว่าคราวนี้ hook ยอมหรือไม่

(ใช้ `git add -f` เพราะชื่อไฟล์นี้ถูก `.gitignore` ตัดอยู่แล้ว — นี่คือเหตุผลที่ต้องมี hook อีกชั้น)

---

## ฝึกเติม

เปิด [practice/pre-commit.sh](practice/pre-commit.sh) มีช่องให้เติม 4 จุด

1. หารายชื่อไฟล์ที่ถูก stage
2. ปฏิเสธไฟล์ใน `build/` `build-*/` `mtb_shared/` และ `.o`
3. ปฏิเสธบรรทัดที่เพิ่มใหม่ซึ่งให้ค่าจริงกับชื่อที่ดูเป็นความลับ แต่ยอมค่าตัวแทน `<...>` และค่าว่าง
4. ปฏิเสธบรรทัดหัวของไฟล์กุญแจส่วนตัว

```sh
bash examples/test_hook.sh practice/pre-commit.sh
```

ก่อนเติมจะเห็น `3 passed, 6 failed` — สามกรณีที่ผ่านคือกรณีที่ hook ต้อง "ยอม" ซึ่ง hook ที่ไม่ทำอะไรเลยก็ผ่าน นี่คือเหตุผลที่ต้องมีกรณีที่ต้อง "ปฏิเสธ" ด้วย ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/pre-commit.sh](solution/pre-commit.sh)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ในโปรเจกต์ที่แตกจากแม่แบบ mtb-only ไฟล์หรือโฟลเดอร์ใดไม่ควร commit (เลือกได้หลายข้อ)
2. เพิ่ม `build/` ลงใน `.gitignore` แล้ว แต่ `git status` ยังแสดงว่าไฟล์ใน `build/` ถูกแก้ไข เพราะอะไร และแก้อย่างไร
3. เฟิร์มแวร์ที่ส่งให้ลูกค้าวันนี้มาจาก commit หนึ่ง วิธีใดทำให้หา commit นั้นเจอได้แน่นอนในอีกหนึ่งปี
4. ข้อความ commit ใดมีประโยชน์ที่สุดกับผู้อ่านในอนาคต
5. พบว่ารหัส WiFi จริงถูก commit ไปเมื่อสองสัปดาห์ก่อนใน repository ที่เพื่อนหลายคน clone ไปแล้ว ควรทำอะไรเป็นอย่างแรก

---

## แล็บ

**งาน:** นำโปรเจกต์ที่แตกจากแม่แบบเข้า Git ให้พร้อมทำงานเป็นทีม โดยมีหลักฐานว่าไม่มีไฟล์ build และไม่มีความลับ

1. ทำท่าที่ 1-3 จนได้ commit แรก branch หนึ่งเส้นที่รวมกลับแล้ว และ tag `fw-v0.1.0` บน commit ที่ build และ flash สำเร็จ
2. build ใหม่ด้วย `make build -j` แล้วรัน `git status --short` ผลต้องว่าง ถ้ามีไฟล์โผล่มา แก้ `.gitignore` แล้วอธิบายว่าไฟล์นั้นคืออะไร
3. รันคำสั่งค้นประวัติทั้งสองบรรทัดในแนวคิดข้อ 3 บันทึกว่าเจออะไร
4. ถ้ามี remote ให้ push ทั้ง branch และ tag แล้วตรวจบนหน้าเว็บว่า tag ชี้ commit ที่ถูกต้อง

**หลักฐานที่เก็บไว้ใน portfolio:** ผลของ `git log --oneline --decorate --graph`, ผลของ `git status --short` หลัง build ที่ว่าง, ข้อความที่ hook ปฏิเสธ commit ทดสอบ และผลการค้นประวัติ

---

## ไปต่อ

- อ่าน [Pro Git](https://git-scm.com/book/en/v2) บท "Git Branching" และหัวข้อ "Tagging" แล้วลองตั้งกติกาชื่อ tag ของทีมคุณให้บอกได้ทั้ง variant และรุ่น แบบที่ SDK ทำ
- ลองย้ายการตรวจของ hook ไปรันใน CI ด้วย ซึ่งข้ามด้วย `--no-verify` ไม่ได้ (บทเรียน 6.2)

บทถัดไปเข้าสู่โมดูล 3: [บทเรียน 3.1 — SWD และ GDB เบื้องต้น](../../m03-debugging/l01-swd-and-gdb/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
