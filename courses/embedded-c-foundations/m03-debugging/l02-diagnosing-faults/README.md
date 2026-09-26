---
id: c-found.m03.l02
lang: th
title: {th: วินิจฉัยความผิดพลาดจากหลักฐาน, en: Diagnosing faults from evidence}
summary: {th: แยกสาเหตุของความผิดพลาดด้วยตัวนับและผลลัพธ์ที่ตรงไปตรงมา แทนการเดาจาก log ที่ดูน่าเชื่อ, en: Separate fault causes with honest counters and result codes instead of guessing from reassuring logs.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l01]
objectives:
- {th: ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ 'ไม่มีผลลัพธ์' และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน, en: Form at least three hypotheses for a 'no result' symptom and pick evidence that separates them.}
- {th: อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด, en: Read the SDK's diagnostic counters and locate the failing stage.}
- {th: อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ, en: Explain why functions should return honest results such as unavailable or no data instead of pretending success.}
develops:
- {skill: debug.gdb, to: 3}
- {skill: soft.problem-solving, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ 'ไม่มีผลลัพธ์' และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน
2. อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด
3. อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากบทเรียน 3.1 สองข้อ

1. เมื่อ CM33 หยุดที่ breakpoint อะไรยังทำงานต่อ และทำไมการหยุดจึงเปลี่ยนพฤติกรรมของระบบ
2. ในชุดเครื่องมือของแม่แบบนี้ เราต่อ debugger เข้า CM55 ได้หรือไม่ ถ้าไม่ได้ หลักฐานของ CM55 ต้องมาจากไหน

## ดูของจริงก่อน

เปิด [examples/06_pipeline_counters.c](examples/06_pipeline_counters.c) โปรแกรมนี้จำลองสายงานสามขั้นแบบเดียวกับ Edge AI ของ SDK
แล้วสร้างความผิดพลาดสามแบบที่ถ้ามองจากหน้าจอจะเหมือนกันหมด **ทายก่อนรัน** ว่าในกรณี `no verdict` ส่วนต่างของตัวนับตัวไหนจะเป็นศูนย์
และคอลัมน์ `result` จะบอกอะไร

```sh
gcc -std=c11 -Wall -Wextra -o pipeline examples/06_pipeline_counters.c
./pipeline
```

ทุกกรณีขึ้น `result=OK` เพราะผลลัพธ์ล่าสุดจากช่วงที่ยังดีอยู่ยังค้างอยู่ ตัวเลขสะสมก็ใหญ่ทุกกรณี
มีแต่ **ส่วนต่าง** ของตัวนับในช่วงที่วัดที่บอกว่าสายงานหยุดที่ขั้นไหน SDK เขียนเรื่องนี้ไว้ในตัวอย่าง 01_first_inference ว่า
"A SNAPSHOT OUTLIVES ITS SESSION" และใน 07_engine_health ว่า "A big number is not health; a big number that is not growing is a stall."

## แนวคิด

### 1. อาการเดียว สาเหตุหลายแบบ: ตั้งสมมติฐานก่อนแตะโค้ด

"หน้าจอขึ้น 0% และไม่มีอะไรเกิดขึ้น" หัวไฟล์ของ [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L8-L49)
บอกว่าอาการนี้ "has four different causes and they need four different fixes" การแก้ที่ได้ผลจึงเริ่มจากเขียนสมมติฐานทุกข้อ
แล้วเลือก **หลักฐานที่ให้คำตอบต่างกันสำหรับแต่ละข้อ** หลักฐานที่ทุกสมมติฐานทำนายเหมือนกัน ไม่ช่วยแยกอะไรเลย

| สมมติฐาน | ถ้าจริง ส่วนต่างในหนึ่งวินาทีจะเป็น | แก้ที่ไหน |
|---|---|---|
| ไม่มีข้อมูลไปถึงโมเดล (เซนเซอร์หรือ CM33 ไม่ส่ง) | `feeds` +0 | ฝั่งแหล่งข้อมูล |
| task ประมวลผลไม่ทำงานหรือค้างข้างใน | `feeds` ขยับ `dq_calls` +0 | task และการเลือกโมเดล |
| ประมวลผลได้แต่ไม่มีผล (หน้าต่างข้อมูลยังไม่เต็ม หรือ NPU ค้าง) | `dq_calls` ขยับ `dq_ok` +0 | รอให้เต็ม หรือดู NPU |
| โมเดลไม่เคยโหลดสำเร็จตั้งแต่ต้น | ใช้ตัวนับอีกชุด (หัวข้อถัดไป) | การโหลดโมเดล |

ลำดับการอ่านสำคัญ: เริ่มจากขั้นต้นของสายงาน เพราะถ้าไม่มีข้อมูลเข้า การไม่มีรอบประมวลผลก็ไม่ใช่ข่าว
และตรวจก่อนว่าการวัดเองใช้ได้ ถ้าโมเดลเปลี่ยนระหว่างสองครั้งที่อ่าน ตัวนับถูกล้าง ส่วนต่างไม่มีความหมาย
ตัวอย่างของ SDK จึงรายงาน "the active model changed under the measurement" แทนที่จะตีความตัวเลข

เรื่องจริงจาก SDK ที่แสดงว่าทำไมต้องเลือกหลักฐานให้ดี: หัวไฟล์ [bento_bgt60trxx_platform.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c#L11-L36)
เล่าว่าเรดาร์ค้างซ้ำ ๆ และตัวเฝ้าการค้างของเซนเซอร์เองรายงาน 0 ครั้ง เพราะมัน "sits at the BOTTOM of the same loop that was stuck"
เครื่องมือวัดที่อยู่ใต้จุดที่ค้างไม่มีวันเห็นการค้าง หลักฐานที่ใช้ได้ต้องอยู่ **นอก** สิ่งที่มันวัด

### 2. อ่านตัวนับของ SDK: สะสม ส่วนต่าง และลำดับ

SDK ให้ตัวนับสองชุดที่ตอบคำถามต่างกัน

- **"ตอนนี้ยังทำงานอยู่ไหม"** `ai_engine_feeds()` `ai_engine_dq_calls()` `ai_engine_dq_ok()` ใน 07_engine_health อ่านเป็น **ส่วนต่าง**
  สองครั้งห่างกัน 1 วินาที ใช้ `delta32()` แบบอิ่มตัว ("Saturating, because a counter is cleared on a model switch")
- **"เคยโหลดสำเร็จไหม"** `ai_engine_init_calls()` `ai_engine_init_returns()` `ai_engine_inits()` `ai_engine_last_init_rc()` ใน
  [10_model_load_diagnosis.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c#L16-L27)
  อ่าน **ครั้งเดียว** เพราะการโหลดเกิดหรือไม่เกิด และมีค่า sentinel `0x7FFFFFFF` แยก "init ไม่เคยถูกเรียก" ออกจาก 0 ที่แปลว่า "init สำเร็จ"

อีกหลักฐานที่ใช้ได้เสมอบน variant mtb-only คือบรรทัด `[HB]` ทุกสิบวินาที (บท G2 ของเอกสาร SDK) ถ้ายังมา แปลว่า CM33 ยังจัดตาราง task ได้
ปัญหาอยู่ที่ task ใด task หนึ่ง หน้าจอ หรือ CM55 ไม่ใช่คอร์ตาย และถ้า CM55 ล้มด้วย fault ร้ายแรง
[proj_cm55/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L250-L299)
กะพริบ LED เป็นรหัส 1 ครั้งคือ stack overflow, 2 ครั้งคือ malloc ล้ม, 3 ครั้งคือ HardFault และเขียนค่า `0xDEAD0001` ถึง `0xDEAD0003` ไว้ที่ที่อยู่คงที่ใน SRAM
คอร์ที่ไม่มี console ก็ยังทิ้งหลักฐานได้ ถ้าเราออกแบบไว้ก่อน

### 3. ผลลัพธ์ที่บอกความจริง

ฟังก์ชันที่ไม่มีข้อมูลแล้วคืน 0 พร้อมบอกว่าสำเร็จ ทำให้คนที่อยู่ปลายทางตัดสินใจผิดอย่างมั่นใจ แคตตาล็อกตัวอย่างของ SDK
ตั้งเป็นกติกาว่า "Every file returns an honest result code" คือ `SDK_EX_OK`, `SDK_EX_UNAVAILABLE`, `SDK_EX_BUSY`, `SDK_EX_REFUSED`,
`SDK_EX_NO_DATA`, `SDK_EX_STARTED` และ "If the hardware is absent the example says so rather than pretending to succeed"
([README ของแคตตาล็อก หัวข้อ 5](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md))

ตัวอย่างว่าผลลัพธ์ที่คลุมเครือทำร้ายอย่างไร เอกสาร SDK บันทึกไว้เอง

- **Appendix X #25** รหัส `0x08060009` ของ MQTT ถูกเขียนทับเมื่อลองใหม่ครบ "overwriting whatever result already held"
  ความผิดพลาดของ TLS กับการถูกปฏิเสธสิทธิ์จึงพิมพ์รหัสเดียวกัน เอกสารบันทึกว่าข้อบกพร่องสามจุดในสามชั้นพิมพ์รหัสนี้เหมือนกันหมด
  และรหัสไม่เปลี่ยนเลยขณะแก้ทีละจุด
- **ตัวนับ mask ของ task เซนเซอร์** ใน [05_auto_push_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L27-L34)
  บิตที่หายไปอาจแปลว่า "คุณปิดมัน" หรือ "มันไม่ทำงาน" และ "the API cannot tell you which"
- **radar_dsp_snapshot()** คืน `false` เมื่อยังไม่มีเฟรมแรก ซึ่งต่างจาก `target == 0` ที่แปลว่าไม่มีเป้าหมาย สองอย่างนี้ SDK ตั้งใจแยกไว้

อีกด้านของความซื่อสัตย์คือ **log ที่ดูน่าเชื่อไม่ใช่หลักฐาน** บท A1 เตือนว่าบน mtb-only การบูตที่สำเร็จแทบไม่พิมพ์อะไร
และบรรทัดบางบรรทัดมีอยู่ในซอร์สแต่ไม่เคยถูกพิมพ์ "If a document tells you to wait for one of them, the document is stale."
หลักฐานที่ดีคือสิ่งที่ระบบ **ปล่อยออกมาจริง** ไม่ใช่สิ่งที่มีเขียนไว้ในโค้ด

## ตัวอย่างสมบูรณ์

[examples/06_pipeline_counters.c](examples/06_pipeline_counters.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** `pipeline_tick()` จำลองสายงานหนึ่งจังหวะ ความผิดพลาดแต่ละแบบหยุดคนละขั้น
- **ท่าที่ 2** `get_confidence()` คืน `RESULT_NO_DATA` ถ้ายังไม่เคยมีผล แต่ถ้าเคยมีแล้ว มันคืนผลล่าสุดซึ่งอาจเก่า
- **ท่าที่ 3** `run_case()` อ่านตัวนับสองครั้งแล้วพิมพ์ทั้งค่าสะสมและส่วนต่าง

ลองแก้แล้วทายก่อนรัน

1. ลดช่วงแรกที่ทำงานปกติจาก 50 เป็น 0 รอบ คอลัมน์ `result` ของกรณีที่ผิดพลาดเปลี่ยนเป็นอะไร และทำไมผลนี้ซื่อสัตย์กว่า
2. เพิ่มเวลาล่าสุดที่ได้ผลลงใน `get_confidence()` แล้วให้คืน `RESULT_NO_DATA` ถ้าผลเก่ากว่ากำหนด ตัดสินเองว่า "เก่าเกินไป" คือเท่าไร
3. เขียนตารางสมมติฐานแบบในแนวคิดข้อ 1 สำหรับกรณี "หน้าจอไม่อัปเดตค่าความชื้น" อย่างน้อยสามข้อ พร้อมหลักฐานที่แยกแต่ละข้อ

## ฝึกเติม

เปิด [practice/06_diagnose.c](practice/06_diagnose.c) มีช่องให้เติม 5 จุด เป็นตรรกะเดียวกับ 07_engine_health และ 10_model_load_diagnosis ของ SDK

1. `delta32()` แบบอิ่มตัว
2. `diagnose()` ตรวจว่าการวัดใช้ได้ (โมเดลไม่เปลี่ยน) ก่อน
3. `diagnose()` ตัดสินจากส่วนต่าง ขั้นต้นก่อนขั้นปลาย
4. `load_diagnosis()` ห้าสาเหตุตามลำดับ
5. `read_latest()` คืนผลที่บอกความจริง และไม่แตะค่าของผู้เรียกเมื่อไม่มีข้อมูล

```sh
gcc -std=c11 -Wall -Wextra -o diagnose practice/06_diagnose.c && ./diagnose
```

สังเกตว่ามี test บางข้อที่ผ่านตั้งแต่ก่อนเติม เช่น `delta32(10u, 15u) == 0u` และกรณี `STAGE_HEALTHY` เพราะโค้ดตั้งต้นคืน 0 และ HEALTHY อยู่แล้ว
test ที่ผ่านกับโค้ดที่ไม่ได้ทำอะไรเลย ไม่ได้พิสูจน์อะไร เรื่องนี้คือหัวใจของบทเรียน 6.1

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/06_diagnose.c](solution/06_diagnose.c)
คอมเมนต์ในเฉลยบอกว่าแต่ละผลลัพธ์ชี้ไปที่ส่วนไหนของระบบ เพราะการวินิจฉัยที่ดีไม่ได้จบที่ชื่อสาเหตุ แต่จบที่ "ไปดูต่อที่ไหน"
สังเกต `LOAD_NO_RC` กรณีที่บัญชีของตัวนับไม่ตรงกันเอง เฉลยรายงานมันเป็นสถานะของตัวเอง แทนที่จะปล่อยให้ตกไปเป็น `LOAD_OK`

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** วินิจฉัยสายงาน Edge AI บนบอร์ดจากตัวนับ แล้วตรวจสอบตัวอย่างวินิจฉัยของ SDK เองด้วยหลักฐาน

1. build แม่แบบด้วย `make build -j ENABLE_PAGE_EXAMPLES=1` แล้ว flash ถอดสายเสียบใหม่ เปิด serial console ไว้
2. รัน `cm55/edge_ai/07_engine_health` จาก **SDK Examples** โดยยังไม่เริ่มโมเดลใด บันทึกข้อความที่ได้ (ควรบอกว่าไม่มีโมเดลทำงาน และคืน NO_DATA)
3. เริ่มโมเดลหนึ่งตัวจากหน้า Edge AI ของเฟิร์มแวร์ แล้วกลับไปรัน `07_engine_health` อีกครั้ง บันทึกส่วนต่างทุกตัวและบรรทัด `VERDICT`
4. **ทายก่อน** แล้วรัน `cm55/edge_ai/10_model_load_diagnosis` บันทึกว่าบนจอเห็นอะไรจากตัวอย่างนี้
   แล้วเปิด [ไฟล์ของมัน](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c)
   เทียบกับสามอย่าง: กติกาในหัวข้อ 5 ของ README แคตตาล็อก (ฝั่ง CM55 "Never printf ... use sdk_example_logf()"),
   Appendix X #1 (printf บน CM55 เป็น no-op เมื่อลิงก์ libbento_edge_ai.a) และบรรทัดที่ประกาศฟังก์ชันนี้ใน
   [sdk_examples_table.c บรรทัด 41](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sdk_examples_table.c#L41)
   เทียบกับนิยามในไฟล์ตัวอย่าง ชนิดของค่าคืนและพารามิเตอร์ตรงกันไหม เขียนสิ่งที่คุณพบพร้อมบรรทัดที่เป็นหลักฐาน
   แล้วบอกว่าข้อสรุปไหน **เห็นกับตาบนบอร์ด** และข้อไหน **อนุมานจากการอ่านโค้ด**
5. บน serial console ตรวจว่า `[HB]` มาครบทุกสิบวินาทีตลอดการทดลอง ถ้าขาดช่วง ให้บันทึกเวลาและสิ่งที่ทำอยู่ตอนนั้น

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอผลของ 07 ทั้งสองครั้ง ตารางส่วนต่างและคำวินิจฉัยของคุณ
รายงานสั้นของข้อ 4 ที่แยก "เห็นจริง" ออกจาก "อนุมาน" และ log ของ `[HB]`

## ไปต่อ

- อ่าน Appendix X ข้อ #25 และ #27 ของเอกสาร SDK ทั้งสองข้อเป็นตัวอย่างของอาการที่ชี้ผิดที่ แล้วเขียนตารางสมมติฐานของแต่ละข้อ
- โจทย์ท้าทาย: ออกแบบ struct "กล่องดำ" สำหรับโปรเจกต์ของคุณเอง ดูตัวอย่างการออกแบบใน
  [diag_blackbox.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/shared/include/diag_blackbox.h)
  (ที่ commit นี้ในแม่แบบ mtb-only มีแต่ header ยังไม่มีไฟล์ .c ใดใช้มัน ซึ่งเป็นอีกตัวอย่างว่าการมีโค้ดอยู่ยังไม่ใช่หลักฐานว่ามันทำงาน)

บทถัดไปเข้าสู่โมดูล 4: [บทเรียน 4.1 GPIO และ interrupt](../../m04-peripherals/l01-gpio-and-interrupts/README.md)

## สะท้อนคิด

- ครั้งล่าสุดที่คุณแก้บั๊กแล้วมันกลับมา คุณแก้ตามสมมติฐานเดียวที่นึกได้ หรือแยกสมมติฐานด้วยหลักฐานก่อน
- ฟังก์ชันไหนในโค้ดของคุณที่คืน 0 หรือ `true` เมื่อไม่มีข้อมูล และผู้เรียกจะเข้าใจผิดได้อย่างไร

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/10_model_load_diagnosis.c (สี่สาเหตุของอาการไม่มีผลลัพธ์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c)
- [SDK: cm55/edge_ai/07_engine_health.c (อ่านส่วนต่างของตัวนับ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: แคตตาล็อกตัวอย่าง (Rules every example follows, result codes)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [B1 — CM33_NS boot walk-through (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
