---
id: c-found.m02.l01
lang: th
title: {th: ชุดเครื่องมือและการ build ครั้งแรก, en: The toolchain and a first build}
summary: {th: ติดตั้ง ModusToolbox ตรวจความพร้อม ดึง dependency แล้ว build และแฟลชแม่แบบเฟิร์มแวร์ของ SDK, en: 'Install ModusToolbox, check readiness, fetch dependencies, then build and flash the SDK firmware template.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l03]
objectives:
- {th: รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ, en: 'Run the readiness check, fetch every project''s dependencies, build and flash the firmware template.'}
- {th: 'อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้', en: 'Explain what CM33_S, CM33_NS and CM55 each run in this template.'}
- {th: บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้, en: Record the tool versions and SDK commit used so others can reproduce the build.}
develops:
- {skill: build.vendor-sdk, to: 3}
- {skill: build.compilers, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ
2. อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้
3. บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ไม่รวมเวลาดาวน์โหลด dependency ราว 1.9 GB
ซึ่งขึ้นกับความเร็วอินเทอร์เน็ตของคุณ แนะนำให้เริ่มดาวน์โหลดตั้งแต่ต้นบทแล้วอ่านแนวคิดระหว่างรอ

## ก่อนเริ่ม

ทวนจากโมดูล 1 สองข้อ

1. ค่าเริ่มต้นของตัวแปร `.data` อยู่ที่ไหนตอนบอร์ดยังไม่เปิด และใครคัดลอกมันไปไว้ใน RAM
2. flash ภายนอกของบอร์ดแบ่งพื้นที่ให้ image ของ CM33 secure, CM33 non-secure และ CM55 แยกกัน (ดูหัวไฟล์ `10_littlefs_basics.c` ที่อ่านในบทเรียน 1.2)
   คุณคิดว่าทำไมต้องแยกเป็นสาม image

สิ่งที่ต้องมี

- **ModusToolbox™ 3.6** (README ของ SDK กำหนดรุ่นนี้เท่านั้น) พร้อม Arm GCC 14.2.1 ที่มากับมัน
- **Git** และ **bash 4 ขึ้นไป** (macOS ต้องลง bash ใหม่ผ่าน Homebrew ตาม README ของ SDK)
- พื้นที่ว่างราว **4 GB** และบอร์ด TESAIoT Dev Kit กับสาย USB-C ที่ต่อเข้า KitProg3

## ดูของจริงก่อน

แม่แบบที่ build ได้มาเป็นไฟล์ zip ใน release ของ SDK ไม่ใช่ `git clone` เพราะ repository สาธารณะที่ commit `ef72c1b`
ไม่ได้เก็บไลบรารี prebuilt (`.a`) หกตัวไว้ (ไฟล์ `.gitignore` ระดับบนสุดของ repository ตัด `*.a` ออก) ไลบรารีเหล่านั้นมากับ zip
หลักสูตรนี้ใช้ release `fw-c-only-v1.10.0` ซึ่งเราตรวจแล้วว่าไฟล์ทุกไฟล์ที่บทเรียนอ้าง ตรงกันทุกไบต์กับ commit `ef72c1b`
(ตรวจด้วย `cmp` เมื่อ 2026-09-26)

ดาวน์โหลดสามไฟล์นี้จาก [หน้า release fw-c-only-v1.10.0](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/releases/tag/fw-c-only-v1.10.0)
ลงโฟลเดอร์ว่างที่จะใช้เป็น workspace: `bento-firmware-template-mtb-only.zip`, `SHA256SUMS.txt` และ `manifest.json` แล้วรัน

```sh
shasum -a 256 -c SHA256SUMS.txt       # บน Linux ใช้ sha256sum -c ได้ (ไฟล์ .hex ที่ไม่ได้โหลดจะขึ้นว่าหาไม่เจอ ไม่เป็นไร)
unzip bento-firmware-template-mtb-only.zip
cd bento-firmware-template-mtb-only
./setup.sh --check
```

**ทายก่อนรัน** ว่าบรรทัดไหนจะขึ้น `FAIL` หรือ `warn` ในเครื่องใหม่ที่ยังไม่เคยใช้ SDK นี้ ส่วนใหญ่จะเห็น `variant: mtb-only`
บรรทัดของ compiler และ `mtb_shared not found` ตามด้วยขนาดราว 1.9 GB สคริปต์นี้ตั้งใจพิมพ์ทุกคำสั่งที่มันจะรันออกมาให้เห็นก่อน
เพื่อให้คุณทำตามด้วยมือได้เมื่อไม่มีสคริปต์ ถ้าบรรทัดของ compiler ไม่ผ่าน ให้แก้ PATH ตาม README ของ SDK ก่อนไปต่อ

ถ้าต้องการอ่านซอร์สและเอกสารฉบับเต็ม ให้ clone repository แยกไว้อีกที่ แล้ว `git checkout ef72c1b658178eee8c38b1e47d28b006f80a59b5`
แต่อย่า build จาก clone นั้น เพราะจะไม่มีไลบรารี prebuilt ให้ลิงก์

## แนวคิด

### 1. แม่แบบนี้คือสามโปรเจกต์ บนสามคอร์

| โปรเจกต์ | คอร์ | รันอะไร (variant mtb-only) |
|---|---|---|
| `proj_cm33_s` | Cortex-M33 ฝั่ง secure | secure boot และตั้งค่าการป้องกันด้วย TrustZone README ของแม่แบบบอกว่า "you will not touch this" |
| `proj_cm33_ns` | Cortex-M33 ฝั่ง non-secure | FreeRTOS, WiFi, เซนเซอร์บนบัส I2C, การเชื่อมต่อคลาวด์ และเป็นเจ้าของ UART console ตัวเดียวของบอร์ด |
| `proj_cm55` | Cortex-M55 (มี NPU) | จอ LVGL และทุกหน้า UI, Edge AI, เรดาร์ |

ลำดับการเริ่มทำงานตาม README ของตัวอย่าง hello world ของ Infineon สำหรับชิปนี้คือ extended boot ปล่อยโปรเจกต์ CM33 secure
จากตำแหน่งคงที่ใน flash ภายนอก CM33 secure ตั้งค่าการป้องกันแล้วปล่อย CM33 non-secure และ CM33 non-secure เป็นคนเปิด CM55
ทั้งสาม image ถูกเขียนลง flash QSPI ภายนอกและรันจากตรงนั้นแบบ execute in place ผลของ build คือไฟล์ `build/app_combined.hex` ไฟล์เดียวที่รวมทั้งสาม

สองคอร์ของงานเราคุยกันผ่าน IPC mailbox ไลบรารีที่แจกแบบ prebuilt หกตัวแบ่งตามคอร์ด้วย สามตัวของ CM55 เป็น hard-float
อีกสามตัวของ CM33_NS เป็น soft-float เอกสาร SDK บอกว่าลิงก์ข้ามคอร์แล้วจะล้มตั้งแต่ขั้น link "which is the good outcome"
ข้อควรจำที่ส่งผลกับบทต่อ ๆ ไป: **CM55 ไม่มี console** `printf` บน CM55 ไม่ออกไปไหน (Appendix X #1) ข้อความทุกอย่างของบอร์ดออกทาง CM33_NS

### 2. dependency ถูกดึงแยกทีละโปรเจกต์ และต้องแพตช์ก่อน build

ModusToolbox เก็บไลบรารีที่แต่ละโปรเจกต์ประกาศไว้ในไฟล์ `deps/*.mtb` แล้ว `make getlibs` ดึงมาไว้ในโฟลเดอร์ `mtb_shared`
ข้างแม่แบบ ([README ของแม่แบบ หัวข้อ 2](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md))
แม่แบบนี้ **ไม่มี getlibs ระดับบนสุด** ต้องรันในทั้งสามโปรเจกต์ ถ้ารันแค่ใน `proj_cm33_ns` จะได้ 33 จาก 41 asset
แล้ว build ไปหยุดใน ninja เพราะหาไฟล์ของ optiga-trust-m ไม่เจอ

หลังดึงเสร็จ ต้องใส่แพตช์ของทีม SDK ลงใน `mtb_shared` ตามลำดับในไฟล์ `third_party_patches/series` ด้วย `patch -F0`
แล้วตรวจผลด้วย SHA-256 ([third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md))
README นั้นอธิบายว่าทำไม `-F0` ไม่ใช่ตัวเลือก: ค่าเริ่มต้นของ GNU patch ยอมให้บริบทคลาดเคลื่อนได้แล้วยังคืนค่าสำเร็จ
และแพตช์สิบในสิบเอ็ดตัว "fail silently" เมื่อหายไป เช่น mTLS ถอยไปใช้กุญแจซอฟต์แวร์แล้ว broker ปฏิเสธอุปกรณ์
exit status บอกว่าแพตช์ลงไปที่ไหนสักที่ ส่วน digest บอกว่ามันลงถูกที่

### 3. build ที่ทำซ้ำได้ เริ่มจากรุ่นที่ตรึงไว้

README ของ SDK ตรึง ModusToolbox ไว้ที่ 3.6 พร้อมเหตุผลว่า Configurator รุ่นใหม่กว่าจะสร้างการตั้งค่า BSP ใหม่จาก `design.modus`
แล้วออก notice ที่ `-Werror=cpp` เปลี่ยนเป็น error ในไฟล์ที่คุณไม่เคยแตะ รุ่นที่ใหม่กว่าจึงไม่ได้ดีกว่า
เช่นเดียวกับที่หลักสูตรนี้อ้าง SDK ที่ commit `ef72c1b` ทุกลิงก์ เพราะไฟล์ที่ commit หนึ่งอาจเปลี่ยนหรือหายไปที่ commit ถัดไป
และสังเกตว่า "ซอร์สที่อ่าน" (commit ใน git) กับ "แพ็กเกจที่ build" (zip ของ release) เป็นของสองชิ้น บันทึกให้ครบทั้งสองชิ้นเสมอ

build ที่ทำซ้ำได้ต้องตอบได้สามคำถาม ใช้เครื่องมือรุ่นอะไร ใช้ซอร์สที่ commit ไหน และมีอะไรที่แก้แต่ยังไม่ commit
บวกกับหลักฐานว่าได้ผลลัพธ์อะไร เช่นขนาดและ SHA-256 ของ `app_combined.hex` README ของ SDK ใช้หลักเดียวกันกับไฟล์ที่แจก:
ทุก release แนบ hex ที่ build แล้ว และให้ตรวจด้วย SHA-256 เทียบกับ `SHA256SUMS.txt` ของ release เดียวกัน

## ตัวอย่างสมบูรณ์

ลำดับเต็มจาก clone ถึงบอร์ดทำงาน รันในโฟลเดอร์ `bento-firmware-template-mtb-only` แต่ละท่าตรงกับบท A1 ของเอกสาร SDK
([A1 — From the zip to your first program](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html))

**ท่าที่ 1 ตรวจสิ่งที่ได้รับ และตรวจเครื่อง** (ในโฟลเดอร์ที่แตกจาก zip)

```sh
(cd lib && ./verify.sh)      # ลายเซ็นและ digest ของไลบรารี prebuilt ทุกตัว ต้องจบด้วย exit 0
./bento.sh doctor            # toolchain และสิ่งที่แม่แบบไม่ได้แนบมา
```

ถ้า `verify.sh` ไม่ผ่าน ให้หยุด แพ็กเกจที่ได้มาไม่ใช่ตัวที่ถูกเซ็นไว้ (บท A1 ของเอกสาร SDK) หรือคุณกำลังรันใน clone ของ git ที่ไม่มีไฟล์ `.a`

**ท่าที่ 2 ดึง dependency ทีละโปรเจกต์ แล้วใส่แพตช์และพิสูจน์ว่าลงถูก**

```sh
for p in proj_cm33_s proj_cm33_ns proj_cm55; do (cd $p && make getlibs); done

(cd ../mtb_shared \
 && for p in $(cat ../bento-firmware-template-mtb-only/third_party_patches/series); do
        patch -p1 -F0 --forward < "../bento-firmware-template-mtb-only/third_party_patches/$p" || exit 1
    done \
 && shasum -a 256 -c ../bento-firmware-template-mtb-only/third_party_patches/PATCHED.sha256)
```

บน Linux ถ้าไม่มี `shasum` ใช้ `sha256sum -c` แทนได้ ทุกบรรทัดของการตรวจต้องขึ้น `OK`

**ท่าที่ 3 build flash แล้วดูหลักฐานว่าบอร์ดทำงาน**

```sh
make build -j                # build ครั้งแรกของทั้งสามคอร์ใช้เวลาราวสิบนาที
make program                 # เขียนผ่าน KitProg3
```

แล้ว **ถอดสาย USB ให้สุด รอสักครู่ แล้วเสียบใหม่** เปิด serial console ที่ 115200 8N1 ไว้ก่อนเสียบ
บน variant นี้การบูตที่สำเร็จแทบไม่พิมพ์อะไร หลักฐานเดียวคือบรรทัด `[HB] t=...s tasks=...` ทุกสิบวินาที
และป้ายรุ่นบนหน้าจอ Home ที่ลงท้ายด้วย `-mtb_only`

กับดักที่เอกสาร SDK รวบรวมไว้ (Appendix X) และคุณจะเจอในวันแรก

- **#21 จอดำหลัง flash** รีเซ็ตผ่าน debugger ทำให้ไฟจอไม่ติด ดูเหมือน flash ล้มเหลวทั้งที่ไม่ใช่ ถอดสายเสียบใหม่ทุกครั้ง
- **#22 (mtb-only)** ไฟจอบางครั้งต้องถอดเสียบรอบที่สองตอนบูตเย็น ถ้า `[HB]` เดินอยู่แต่จอดำ ให้ลองอีกรอบก่อนสรุปอะไร
- **#16 อย่า attach debugger กับบอร์ด mtb-only ที่กำลังทำงาน** มันทำให้ CM33 ไปค้างในลูปของ boot ROM เรื่องนี้กลับมาในบทเรียน 3.1
- README ของ SDK เตือนว่า **อย่าเรียก openocd ตรง ๆ** ด้วย `-f target/cat1d.cfg` ทีม SDK ลองแล้วได้ `wrote 0 bytes` ตามด้วย checksum ไม่ตรง
  และทำให้เฟิร์มแวร์ที่รันอยู่เสีย ให้ใช้ `make program` เท่านั้น

## ฝึกเติม

บทนี้ฝึกกับเครื่องมือ ไม่ใช่กับโค้ด ตอบคำถามเหล่านี้โดยอ่านจากเครื่องของคุณและจากไฟล์ใน SDK ไม่ใช่จากความจำ

1. `./setup.sh --check` ตรวจอะไรบ้าง และตรวจอะไร **ไม่** ได้ (ดูไฟล์ [setup.sh](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/setup.sh) ว่ามันแตะแพตช์หรือไม่)
2. หลัง getlibs นับจำนวนโฟลเดอร์ระดับแรกใน `../mtb_shared` ได้เท่าไร
3. ในไฟล์ `third_party_patches/series` มีแพตช์กี่ไฟล์ และตัวไหนที่ README บอกว่าเป็นตัวเดียวที่ทำให้ build หยุด
4. เปิด [resources/build-record.md](resources/build-record.md) แล้วเติมส่วน "เครื่องและเครื่องมือ" กับ "ซอร์สที่ build" ให้ครบ

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที

1. จาก `setup.sh` ที่ commit นี้ มันตรวจ variant, `arm-none-eabi-gcc` บน PATH, `make`, และ `mtb_shared` (กับ port ของ MicroPython ถ้าเป็น variant mtb-mpy)
   โหมดปกติจะรัน getlibs ให้ครบสามโปรเจกต์ และ `--build` จะ build ต่อ แต่ **ไม่ได้ใส่แพตช์** ขั้นแพตช์เป็นหน้าที่ของคุณ
   และถ้าข้ามไป build จะถูกตัวตรวจ `verify_asset_patches.sh` ปฏิเสธพร้อมบอกชื่อไฟล์ที่ขาด
2. ตัวเลขขึ้นกับการดึงของคุณ สิ่งที่ต้องได้คือ getlibs ทั้งสามโปรเจกต์จบโดยไม่มี error ถ้าได้น้อยกว่าที่เพื่อนได้มาก ให้ตรวจว่ารันครบทั้งสามโปรเจกต์หรือยัง
3. นับจากไฟล์ `series` ในเครื่องของคุณ README ของโฟลเดอร์นั้นระบุว่า "Only `secure-sockets/0002` stops a build" ที่เหลือล้มแบบเงียบ
4. เทียบกับเพื่อนหนึ่งคน ช่องไหนที่ต่างกันคือสิ่งที่อาจทำให้ผลการ build ต่างกัน

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** build และ flash แม่แบบ mtb-only ครั้งแรก แล้วเขียนบันทึกการ build ที่เพื่อนทำซ้ำได้

1. ทำตามสามท่าในหัวข้อตัวอย่างสมบูรณ์จนเห็นบรรทัด `[HB]` อย่างน้อยสองบรรทัด
2. ตรวจว่าตัวเลข `t=` เพิ่มทีละ 10 และจำนวน task คงที่หลังบูตเสร็จ (ช่วงแรกจะเพิ่มขึ้นระหว่างที่ task ต่าง ๆ ถูกสร้าง)
3. เติม [resources/build-record.md](resources/build-record.md) ให้ครบทุกช่อง รวม SHA-256 ของ `build/app_combined.hex`
4. ให้เพื่อนหนึ่งคน build จากบันทึกของคุณบนเครื่องของเขา แล้วเทียบ SHA-256 ถ้าไม่ตรงกัน ให้หาว่าต่างกันตรงไหนก่อนสรุปว่าอะไรผิด
   (การ build ข้ามเครื่องอาจได้ไบต์ไม่ตรงกันด้วยเหตุผลอย่างเวลาหรือ path ที่ฝังอยู่ในไฟล์ ถ้าเจอ ให้บันทึกสิ่งที่พบไว้ นั่นคือผลการทดลองที่มีค่า)

**หลักฐานที่เก็บไว้ใน portfolio:** log ของ getlibs และการตรวจแพตช์ (บรรทัด `OK`) บรรทัด `[HB]` จาก console ภาพหน้าจอ Home ที่เห็นป้ายรุ่น
และไฟล์ build record ที่เติมครบ

## ไปต่อ

- เปิด [A0 — What you can build, and where each piece lives](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html)
  แล้วหาว่าไลบรารี prebuilt ตัวไหนลิงก์เข้าคอร์ไหน ตรงกับตารางในแนวคิดข้อ 1 หรือไม่
- เทียบกับตัวอย่าง [mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0)
  ของ Infineon ซึ่งมีโครงสามโปรเจกต์แบบเดียวกันแต่เล็กกว่ามาก ตัวอย่างนั้นระบุว่าทดสอบกับ ModusToolbox 3.7
  ส่วนแม่แบบของ SDK ตรึงที่ 3.6 ถ้าจะใช้ทั้งสองในเครื่องเดียว ต้องจัดการเรื่องรุ่นอย่างไร
- ภาพรวมของการ build และ flash อีกแบบด้วย master template ของ Developer Hub อยู่ใน [TESAIoT Firmware Stack บทเรียน 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)

บทถัดไป: [บทเรียน 2.2 Make และตัวแปรของการ build](../l02-make-and-build-flags/README.md)

## สะท้อนคิด

- ขั้นไหนในวันนี้ที่ถ้าไม่มีคนบอกไว้ก่อน คุณจะเสียเวลากับมันมากที่สุด และคุณจะเขียนมันลงบันทึกของทีมอย่างไร
- "build ผ่าน" กับ "บอร์ดทำงาน" ต่างกันอย่างไร แล้ววันนี้คุณใช้หลักฐานอะไรตัดสินว่าบอร์ดทำงาน

## แหล่งอ้างอิง

- [SDK: แม่แบบ mtb-only README (First run, CLI, สามคอร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: README หลักของ repository (รุ่นเครื่องมือ และเฟิร์มแวร์สำเร็จรูป)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [SDK: third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)
- [A0 — What you can build, and where each piece lives (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html)
- [A1 — From the zip to your first program (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [Infineon ModusToolbox software (GitHub)](https://github.com/Infineon/modustoolbox-software)
- [Infineon mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- บทเรียนที่เกี่ยวข้อง: [TESAIoT Firmware Stack 1.1 · เครื่องมือ บอร์ด และ master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
