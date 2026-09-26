# โมดูล 6 — แอป Edge AI

> Edge AI apps · [หน้าหลักสูตร](../README.md)

สร้างแอปที่โฟกัสโมเดลเดียว ต่อ verdict เข้ากับ action ผ่านท่อที่กัน false positive รวมกับเซนเซอร์ดิบ และส่งเหตุการณ์ขึ้น MQTT

## เป้าหมายของโมดูล

เปลี่ยนคำตอบของโมเดลให้เป็นการกระทำที่เชื่อถือได้ และส่งออกไปนอกบอร์ดอย่างมีวินัย

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [6.1](l01-focused-apps/README.md) | หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว | 70 | [slides.md](l01-focused-apps/slides.md) |
| [6.2](l02-focused-app-lab/README.md) | ลงมือทำ: แอปโฟกัสของเราเอง | 75 | [slides.md](l02-focused-app-lab/slides.md) |
| [6.3](l03-action-pipeline/README.md) | ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result | 70 | [slides.md](l03-action-pipeline/slides.md) |
| [6.4](l04-action-pipeline-lab/README.md) | ลงมือทำ: action pipeline ที่กัน false positive | 75 | [slides.md](l04-action-pipeline-lab/slides.md) |
| [6.5](l05-sensor-fusion/README.md) | sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ | 70 | [slides.md](l05-sensor-fusion/slides.md) |
| [6.6](l06-fusion-iot-lab/README.md) | ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT | 75 | [slides.md](l06-fusion-iot-lab/slides.md) |

บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ** ที่มีไฟล์ฝึก เฉลย และแล็บ

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] แอปโฟกัสต่อโมเดลที่ UI สะอาด เล็งโมเดลด้วย `find_model()` โชว์ verdict แถบทุกคลาสและ latency และมีตัวนับที่ทำงานจริงเมื่อคลาสเป้าหมายข้าม `CONF_FLOOR` รีทาร์เก็ตได้อย่างน้อยสองโมเดล (บทเรียน 6.2)
- [ ] action pipeline แบบ debounce ที่คลาสเป้าหมายต่อเนื่องจุดชนวน action จริง ส่วนสัญญาณกระพริบสั้น ๆ ถูกกันไว้ (บทเรียน 6.4)
- [ ] การตัดสินใจแบบ fused (verdict AND ประตูดิบ) ถูก publish ขึ้น MQTT ได้จริง ครั้งเดียวต่อเหตุการณ์ ส่วนการขยับเบา ๆ ไม่ถูกส่ง (บทเรียน 6.6)
