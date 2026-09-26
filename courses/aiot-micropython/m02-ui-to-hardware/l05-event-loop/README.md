---
id: aiot-mpy.m02.l05
lang: th
title: {th: 'event loop: แตะจอแล้วไฟจริงติด', en: 'The event loop: touch the screen, light the real LED'}
summary: {th: เขียน event loop ที่หยิบเหตุการณ์จาก ui.poll() ทุกรอบ แยกให้ออกว่า widget ไหนส่งอะไร ทำตามกฎเหล็กห้าข้อของโมดูล ui และให้สถานะบนจอกับหลอดไฟจริงเปลี่ยนผ่านประตูเดียวจนตรงกันเสมอ, en: 'Write an event loop that takes events from ui.poll() every round, tell which widget sent what, follow the five iron rules of the ui module, and route every change through one gate so the screen and the real LEDs always agree.'}
level: L2
time_min: {concept: 20, practise: 25, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m02.l04]
objectives:
  - {th: 'เขียน event loop สี่จังหวะ (poll → dispatch → act → sleep) ที่เทียบ handle คู่กับ type ด้วย elif ให้ครบทุกชนิดที่รู้จัก และเหลือกิ่งสุดท้ายพิมพ์ ''unknown'' ลง Console แล้วทายชนิดเหตุการณ์กับความหมายของ value จาก Button, Switch, Checkbox, Slider, Dropdown และ Textarea ได้ถูก', en: 'Write a four-step event loop (poll, dispatch, act, sleep) that checks handle together with type in an elif chain covering every known type, with a last branch that prints ''unknown'' to the Console, and predict the event type and value meaning for Button, Switch, Checkbox, Slider, Dropdown and Textarea.'}
  - {th: อธิบายกฎเหล็กห้าข้อของโมดูล ui และคิวเหตุการณ์ (ใส่ได้จริง 15 ช่อง หยิบได้ครั้งละไม่เกิน 8 เต็มแล้วทิ้งเหตุการณ์ใหม่) แล้วบอกได้ว่าอาการจอว่าง การแตะหาย และ RuntimeError มาจากกฎข้อไหน, en: 'Explain the five iron rules of the ui module and the event queue (15 usable slots, at most 8 per poll, new events dropped when full), and trace a blank screen, lost taps and a RuntimeError back to the rule behind each.'}
  - {th: ให้ทุกคำสั่งที่เปลี่ยนไฟผ่านฟังก์ชันเดียวแบบ set_led() ที่จำสถานะในตัวแปรก่อน สั่งหลอดจริง ดึง widget บนจอให้ตรง แล้วรายงานจากตัวแปรนั้นอย่างเดียว จนจอกับหลอดตรงกันในทุกกรณีที่ทดสอบ รวมทั้งหลังปุ่ม ALL OFF, en: 'Route every LED change through one set_led()-style function that records the state in a variable first, drives the real LED, pulls the on-screen widget into line and reports only from that variable, so screen and LEDs agree in every tested case, including after ALL OFF.'}
  - {th: เติมช่องว่างใน practice/s04b_layout_widgets.py ด้วย .add_tab() .content() .add_tile() และ ui.poll() จนแท็บทั้งสามใบแสดงของอยู่ในแท็บของมันเอง และอธิบายได้ว่าทำไมต้องส่งค่าที่คืนมาเป็น parent= เสมอ, en: 'Fill the blanks in practice/s04b_layout_widgets.py with .add_tab(), .content(), .add_tile() and ui.poll() until all three tabs show their contents inside their own tab, and explain why the returned handle must always be passed back as parent=.'}
develops: [{skill: gui.embedded, to: 2}, {skill: gui.hmi, to: 1}, {skill: prog.design-patterns, to: 1}]
assesses: [{skill: gui.embedded, level: 1, evidence: practice/s04b_layout_widgets.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-04.html (slides 15–35), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 2.5 — event loop: แตะจอแล้วไฟจริงติด

> โมดูล 2 — จากจอสู่ฮาร์ดแวร์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เขียน event loop ที่หยิบเหตุการณ์จาก ui.poll() ทุกรอบ แยกให้ออกว่า widget ไหนส่งอะไร ทำตามกฎเหล็กห้าข้อของโมดูล ui และให้สถานะบนจอกับหลอดไฟจริงเปลี่ยนผ่านประตูเดียวจนตรงกันเสมอ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เขียน event loop สี่จังหวะ (poll → dispatch → act → sleep) ที่เทียบ handle คู่กับ type ด้วย elif ให้ครบทุกชนิดที่รู้จัก และเหลือกิ่งสุดท้ายพิมพ์ 'unknown' ลง Console แล้วทายชนิดเหตุการณ์กับความหมายของ value จาก Button, Switch, Checkbox, Slider, Dropdown และ Textarea ได้ถูก
2. อธิบายกฎเหล็กห้าข้อของโมดูล ui และคิวเหตุการณ์ (ใส่ได้จริง 15 ช่อง หยิบได้ครั้งละไม่เกิน 8 เต็มแล้วทิ้งเหตุการณ์ใหม่) แล้วบอกได้ว่าอาการจอว่าง การแตะหาย และ RuntimeError มาจากกฎข้อไหน
3. ให้ทุกคำสั่งที่เปลี่ยนไฟผ่านฟังก์ชันเดียวแบบ set_led() ที่จำสถานะในตัวแปรก่อน สั่งหลอดจริง ดึง widget บนจอให้ตรง แล้วรายงานจากตัวแปรนั้นอย่างเดียว จนจอกับหลอดตรงกันในทุกกรณีที่ทดสอบ รวมทั้งหลังปุ่ม ALL OFF
4. เติมช่องว่างใน practice/s04b_layout_widgets.py ด้วย .add_tab() .content() .add_tile() และ ui.poll() จนแท็บทั้งสามใบแสดงของอยู่ในแท็บของมันเอง และอธิบายได้ว่าทำไมต้องส่งค่าที่คืนมาเป็น parent= เสมอ

## ก่อนเริ่ม

ทบทวนห้าขั้นของ widget จากบทเรียน 2.4 โดยเฉพาะขั้นที่ 4 (เก็บ `.id()` ไว้เทียบ) และ `value=` ของ Label ที่เป็นขนาดฟอนต์
บนจอบอร์ดแตะการ์ด BENTO Playground ค้างไว้ widget ทุกตัวเกิดบนหน้านี้เท่านั้น ถ้าปัดออกไปเมนูอื่น widget ทั้งหมดจะถูกทำลาย
กลับมาแล้วจอว่าง ต้องส่งโค้ดใหม่ ซึ่งไม่ใช่ความผิดพลาด แต่เป็นวิธีที่บอร์ดคืนหน่วยความจำ

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 2.4 — จอสัมผัสและ widget ตัวแรก](../l04-touch-widgets/README.md)

## ดูของจริงก่อน

รัน `01_first_widgets.py` แล้วแตะปุ่มสองใบสลับกัน ตัวนับ "แตะไปกี่ครั้ง" เดินขึ้นทันที และชื่อปุ่มที่แตะล่าสุดเปลี่ยนตาม
ทุกการแตะเดินทางจาก CM55 ผ่านคิวมาถึงลูปของเราบน CM33 แล้วกลับไปเปลี่ยนจอในรอบเดียวกัน บทเรียนนี้เปิดดูวงกลมนั้นทีละขั้น

## แนวคิด

**โปรแกรม UI ไม่ใช่โค้ดที่ไหลจากบนลงล่าง แต่เป็นวงกลมที่หมุนไม่หยุด** ทุกรอบมีสี่จังหวะ: 1 poll `ui.poll()` ถามว่ามีอะไรใหม่
· 2 dispatch เทียบ `handle` กับ `type` ว่าใครส่งอะไรมา · 3 act สั่ง `gpio.led()` และอัปเดต Label · 4 sleep `time.sleep_ms(50)`
คืนเวลาให้ระบบไปวาดจอ วนราว 20 รอบต่อวินาที นี่คือความคิดเดียวกับ `addEventListener` ของ JavaScript และ `lv_obj_add_event_cb` ของ LVGL

**หน้าตาของเหตุการณ์** `ui.poll()` คืน list ของ dict (ว่างได้ ไม่ใช่ `None`) ทุก dict มีสามช่องเสมอ `handle` `type` `value`
Button ส่ง `'clicked'` · Switch กับ Checkbox ส่ง `'toggled'` (1 = เปิดหรือติ๊ก) · Slider, Arc และ Dropdown ส่ง `'value_changed'`
พร้อมค่าใหม่ (Dropdown ให้ลำดับตัวเลือกเริ่มที่ 0) · Textarea ส่ง `'value_changed'` ที่ `value` เป็น 0 เสมอ ต้องถาม `.text()` เอาข้อความเอง
· Label, Bar, Seg7, Panel และ Chart ไม่ส่งอะไรเลย และมีชนิดที่สี่คือ `'unknown'` ที่เฟิร์มแวร์แปลรหัสไม่ออก
โค้ดแบบ `if t == 'clicked': … else: …` จะกวาดมันเข้า `else` เงียบ ๆ จึงต้องเขียน `elif` ให้ครบแล้วเหลือกิ่งสุดท้ายพิมพ์ของแปลกลง Console
และเพราะสอง widget ที่หน้าตาต่างกันอาจส่งชนิดเดียวกัน ให้เช็ก `type` คู่กับ `handle` เสมอ
คิวฝั่ง CM55 เป็นวงแหวน 16 ช่อง ใส่ได้จริง 15 หยิบได้ครั้งละไม่เกิน 8 และถ้าเต็ม เฟิร์มแวร์ทิ้งเหตุการณ์ใหม่ที่เพิ่งเข้ามา
นิ้วที่แตะรัว ๆ ตอนลูปหลับยาวจึงหายไปเลยโดยไม่มี error ให้จับ บั๊กแบบนี้หาเจอด้วยการนับ ไม่ใช่ด้วย print

**กฎเหล็กห้าข้อของโมดูล ui** 1 เรียก `ui.poll()` ทุกรอบ เพราะ CM55 ซ่อนกล่องบรรจุทั้งใบไว้จน `ui.poll()` ครั้งแรกมาถึง
ถ้าไม่เรียก จอจะว่างราว 2 วินาทีจนกลไกกันเหนียวปลดเอง · 2 `time.sleep_ms(50)` เป็นอย่างต่ำสำหรับ UI เบา ๆ (แดชบอร์ดหนักในบทเรียน 3.7–3.9 ใช้ 200)
· 3 งบของคอร์ส 32 widget ต่อหน้า เพดานเฟิร์มแวร์ 64 เกินเมื่อไรได้ `RuntimeError: ui: max 64 widgets` ของที่ `.hide()` ไว้และของในแท็บที่ไม่ได้เปิด
ยังกินโควตา มีแค่ `.delete()` หรือ `ui.clear()` ที่คืนให้ · 4 `ui.*` ครั้งแรกหยุดงานอ่านเซนเซอร์อัตโนมัติ เพราะบัส I2C ต้องไม่ชนกัน
ตั้งแต่นั้นเราอ่านเซนเซอร์เองในลูป · 5 ลูปเร็วเกินไปเฟรมหายเงียบ ๆ ไม่มี exception มีแต่จอกระตุกและค่าที่อัปเดตไม่ครบ

**สถานะบนจอกับสถานะจริงไม่ใช่อันเดียวกัน** `gpio.led(n).value()` ตอบแค่ระดับขา ณ วินาทีที่ถาม ความจริงจึงต้องอยู่ในตัวแปรของเรา
และทุกการเปลี่ยนต้องผ่าน **ประตูเดียว** `set_led(i, on)`: จำใน `led_on[i]` → สั่ง `gpio.led(LED_IDX[i])` → ให้ไฟบนจอสะท้อน
→ รายงานผ่าน `show_status()` ที่อ่านจาก `led_on` อย่างเดียว ถ้ามีบรรทัดไหนเรียก `gpio.led().on()` ตรง ๆ ข้ามประตูนี้ ไฟจะยังติด
แต่จอจะโกหกโดยหาสาเหตุไม่เจอ ข้อความบน Label คือผลลัพธ์ของความจริง ไม่ใช่ตัวความจริง ในงานจริงเรียกว่า single source of truth
ปุ่ม "เปิด" เรียก `set_led(on_ids.index(h), True)` คือสั่งเปิด ไม่ใช่สั่งสลับ กดซ้ำสิบครั้งได้ผลเท่ากดครั้งเดียว

**widget ที่ใส่ของอื่นไว้ข้างใน** `Tabview.add_tab()` `Tileview.add_tile(col, row)` `Win.content()` และ `Menu.add_page()`
คืนแฮนเดิลของช่องข้างใน ซึ่งต้องส่งกลับเป็น `parent=` ตอนสร้างของที่จะวางลงไป ลืมเมื่อไร ของจะไปโผล่บนจอหลักโดยไม่มีอะไรฟ้อง
Tabview สูง 336 ไม่ใช่ 398 เพราะมุมขวาล่างจองไว้ให้ปุ่ม Console และแท็บช่วยเรื่องพื้นที่สายตา ไม่ได้ช่วยเรื่องโควตา
ส่วนเอาต์พุตทางหู `ui.sfx(ui.SFX_...)` กับ `ui.tone(note, wave, velocity, dur_ms)` เป็นแบบยิงแล้วลืม `note` คือเลขโน้ต MIDI 0–127
ไม่ใช่เฮิรตซ์ รับแบบตำแหน่งเท่านั้น ให้คร่อมด้วย `hasattr(ui, "tone")` และให้ตัวนับบนจอเป็นพยานแทนหู

## ตัวอย่างสมบูรณ์

ทายก่อนรันทุกไฟล์ แล้วจดผลลงบันทึกการเรียน

1. **`02_event_types.py`** ก่อนแตะ ให้เขียนคำทายว่า Button, Switch, Checkbox และ Slider จะส่ง `type` อะไร แล้วเดินทีละท่าตามที่จอบอก
   ท่าที่ 3 คือกับดักของไฟล์ ทำตารางสามคอลัมน์ widget · type · value ลงบันทึกการเรียน
2. **`03_switch_matches_led.py`** แตะสวิตช์ทีละตัวแล้วมองจอกับหลอดคู่กัน จากนั้นกด ALL OFF สวิตช์ต้องเด้งกลับพร้อมกับ Seg7 ลงเป็น 0
   ลองปิดบรรทัด `switches[i].value(...)` ใน `set_led()` ด้วยคอมเมนต์แล้วรันใหม่ ดูว่าจอเริ่มโกหกตอนไหน แล้วคืนบรรทัดนั้น
3. **`04_seg7_takes_text.py`** Seg7 ไต่ทีละ 0.5 และเปลี่ยนเป็นแดงเมื่อเกิน 60 สังเกตว่า `.value(n)` แสดงได้แค่จำนวนเต็ม
   ทศนิยมต้องตัดสินใจเองแล้วส่งเป็น `.text()`
4. **`05_sound_feedback.py`** แตะปุ่มสามใบ ตัวนับบนจอเดินทุกครั้งที่สั่งเสียง ถ้าตัวนับเดินแต่เงียบ ปัญหาอยู่ที่ลำโพงหรือชิปเสียง
   ถ้าตัวนับไม่เดิน ปัญหาอยู่ที่โค้ด
5. **`06_layout_budget.py`** ดูแถบงบที่ใช้ไปจาก 32 และผลการลองสร้างตัวที่ 33 แล้วหาว่าทำไมปุ่มที่วางเลย x=690 และ y=340 พร้อมกันจึงแตะไม่ได้

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/01_first_widgets.py](examples/01_first_widgets.py) | widget ตัวแรก และเหตุผลที่ต้องใส่ x กับ y ทุกครั้ง |
| [examples/02_event_types.py](examples/02_event_types.py) | เหตุการณ์หน้าตาเป็นอย่างไร และใครส่งอะไร |
| [examples/03_switch_matches_led.py](examples/03_switch_matches_led.py) | จอกับไฟจริงต้องพูดตรงกันเสมอ |
| [examples/04_seg7_takes_text.py](examples/04_seg7_takes_text.py) | Seg7 รับได้ทั้งสองทาง แต่ให้ผลไม่เท่ากัน |
| [examples/05_sound_feedback.py](examples/05_sound_feedback.py) | เสียงตอบรับตอนแตะปุ่ม |
| [examples/06_layout_budget.py](examples/06_layout_budget.py) | พื้นที่ 792x398 กับงบ widget: งบของคอร์ส 32 ตัว (เพดานเฟิร์มแวร์ 64) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m02-ui-to-hardware/l06-touch-panel-lab/practice/s04_touch_panel.py](../l06-touch-panel-lab/practice/s04_touch_panel.py) — แผงควบคุม LED บนจอสัมผัส (ฉบับฝึกเติมโค้ด)

## ฝึกเติม

ไฟล์ฝึกมีช่องว่าง `____` เจ็ดจุดในสี่ท่า เติมทีละท่าแล้วส่งขึ้นบอร์ดดูผลทุกครั้ง

- ท่าที่ 1: สร้างแท็บสามใบด้วย `tabs.add_tab("ชื่อแท็บ")` แล้วเก็บค่าที่คืนมาไว้ใน `tab_win` `tab_dots` `tab_tile`
- ท่าที่ 2: `body = win.content()` พื้นที่ใต้แถบหัวของ Win (ไม่ใช่ `.add_tab()`)
- ท่าที่ 3: ไทล์สองใบคอลัมน์เดียวกันคนละแถวด้วย `tiles.add_tile(col, row)` จึงปัดขึ้นลงได้
- ท่าที่ 4: `for _ev in ui.poll():` ในลูปเหตุการณ์ ตามกฎข้อ 1

ทำงานถูกเมื่อแท็บสามใบด้านบนแตะสลับได้ แท็บแรกมีหน้าต่างที่มีป้ายสามบรรทัดอยู่ข้างใน (ไม่ได้โผล่บนจอหลัก)
แท็บสองมีจอจุดที่ไฟวิ่งกับวงกลมหมุน แท็บสามปัดขึ้นไปดูไทล์ที่สองได้ ไฟล์รันจบเองใน 30 วินาที แล้วพิมพ์จำนวนครั้งที่แตะลง Console

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s04b_layout_widgets.py](practice/s04b_layout_widgets.py) | widget ที่ "ใส่ของอื่นไว้ข้างใน" ได้ (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ แล้วอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s04b_layout_widgets.py](solution/s04b_layout_widgets.py) | [practice/s04b_layout_widgets.py](practice/s04b_layout_widgets.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดถูกต้องเกี่ยวกับเหตุการณ์ที่ ui.poll() คืนมา เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) Checkbox ส่ง 'toggled' ไม่ใช่ 'clicked' ทั้งที่หน้าตาเหมือนของกด
   - ข) Switch ส่ง 'toggled' และ value เป็น 1 เมื่อเปิด 0 เมื่อปิด
   - ค) Textarea ส่ง 'value_changed' พร้อมข้อความที่พิมพ์อยู่ในช่อง value
   - ง) ui.poll() คืน None เมื่อไม่มีเหตุการณ์ จึงต้องเช็กก่อนวนลูป
   - จ) Label ส่ง 'clicked' เมื่อถูกแตะ

   <details><summary>เฉลย</summary>

   **ก, ข** — Checkbox กับ Switch ส่ง toggled ถ้าไปรอ clicked จาก Checkbox จะรอทั้งวัน ส่วน Textarea ให้ value เป็น 0 เสมอ ต้องถาม .text() เอง ui.poll() คืน list ว่างได้ ไม่ใช่ None และ Label เป็นตัวแสดงผลที่ไม่ส่งอะไรเลย

   </details>

2. ลูปของทีมหลับทีละ 500 ms ผู้ใช้แตะปุ่มรัว ๆ ยี่สิบครั้งในช่วงที่ลูปหลับ จะเกิดอะไรขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ทั้งยี่สิบครั้งมาถึงครบ แค่ช้าไปครึ่งวินาที
   - ข) คิวเต็มที่ 15 ช่อง แล้วเฟิร์มแวร์ทิ้งเหตุการณ์ใหม่ที่เพิ่งเข้ามา การแตะส่วนเกินหายไปเลยโดยไม่มี error
   - ค) คิวเต็มแล้วเฟิร์มแวร์ทิ้งเหตุการณ์เก่าที่สุด เก็บของใหม่ไว้แทน
   - ง) โปรแกรมหยุดด้วย RuntimeError เพราะคิวล้น

   <details><summary>เฉลย</summary>

   **ข** — คิวเป็นวงแหวน 16 ช่องที่ใส่ได้จริง 15 และถ้าเต็ม เฟิร์มแวร์ทิ้งเหตุการณ์ใหม่ ไม่ได้ทิ้งของเก่าและไม่ได้ให้รอ นิ้วที่แตะตอนลูปหลับยาวจึงหายไปเงียบ ๆ นี่คือเหตุผลที่กฎข้อ 2 บอกให้หลับ 50 ms ไม่ใช่ 500

   </details>

3. ข้อใดตรงกับกฎเหล็กของโมดูล ui เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 2)*
   - ก) ถ้าไม่เรียก ui.poll() เลย จอจะว่างอยู่ราว 2 วินาที เพราะ CM55 ซ่อน widget ไว้จนกว่า poll ครั้งแรกจะมาถึง
   - ข) สร้าง widget เกิน 64 ตัวต่อหน้าได้ RuntimeError ทันที
   - ค) widget ที่ .hide() ไว้ยังกินโควตาอยู่ มีแค่ .delete() ที่คืนให้
   - ง) widget ในแท็บที่ไม่ได้เปิดอยู่ไม่นับโควตา
   - จ) ยิ่งลูปเร็วยิ่งดี หลับ 5 ms จอจะลื่นที่สุด

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — ของในแท็บที่ไม่ได้เปิดยังกินโควตาเท่าเดิม แท็บช่วยแค่พื้นที่สายตา และลูปที่เร็วเกินไปทำให้เฟรมหายเงียบ ๆ ไม่มี exception UI เบา ๆ จึงหลับอย่างต่ำ 50 ms

   </details>

4. ทีมหนึ่งเขียนปุ่ม ALL OFF ให้วน `gpio.led(i).off()` ตรง ๆ แทนการเรียก `set_led(i, False)` กดแล้วจะเห็นอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ทุกอย่างถูกต้อง เพราะหลอดดับจริงแล้ว
   - ข) หลอดดับจริง แต่สวิตช์บนจอกับตัวเลขที่นับจาก led_on ยังบอกว่าติดอยู่ จอโกหกทันที
   - ค) หลอดไม่ดับ เพราะ gpio.led() ใช้ไม่ได้หลังมีจอ
   - ง) โปรแกรมหยุดด้วย error เพราะเรียก gpio นอก set_led()

   <details><summary>เฉลย</summary>

   **ข** — set_led() คือประตูเดียวที่จำสถานะ สั่งหลอด ดึง widget บนจอ และรายงาน การเรียก gpio.led() ตรง ๆ ข้ามประตูนี้ ไฟยังเปลี่ยนตามสั่ง แต่ led_on และจอไม่รู้เรื่อง ผู้ใช้เชื่อจอ ไม่ได้เชื่อหลอดไฟ

   </details>

5. ในไฟล์ฝึก s04b ถ้าลืมใส่ `parent=body` ตอนสร้างป้ายที่ควรอยู่ในหน้าต่างของแท็บแรก จะเกิดอะไรขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) โปรแกรมหยุดด้วย ValueError ทันที
   - ข) ป้ายไปโผล่บนจอหลัก ไม่ได้อยู่ในหน้าต่าง และไม่มีอะไรฟ้อง
   - ค) ป้ายไม่ถูกสร้าง แต่ก็ไม่กินโควตา
   - ง) ป้ายเข้าไปอยู่ในแท็บที่เปิดอยู่ตอนนั้นเอง

   <details><summary>เฉลย</summary>

   **ข** — .add_tab() .content() .add_tile() และ .add_page() คืนแฮนเดิลของช่องข้างใน ต้องส่งกลับเป็น parent= เสมอ ลืมแล้วของไปอยู่ผิดที่โดยไม่มี exception หรือคำเตือน

   </details>

## แล็บ

**เช็กก่อนไปบทเรียน 2.6** จดผลลงบันทึกการเรียน

- [ ] ตาราง widget · type · value จาก `02_event_types.py` ครบสี่ widget และคำทายของ Checkbox ถูกหรือผิดพร้อมเหตุผล
- [ ] `03_switch_matches_led.py` ในทุกกรณีที่ทดสอบ รวมทั้งหลัง ALL OFF สวิตช์บนจอ ตัวเลขบน Seg7 และหลอดจริงตรงกัน
- [ ] ไฟล์ฝึก `s04b_layout_widgets.py` ครบสี่ท่า ของทุกชิ้นอยู่ในแท็บของตัวเอง และ Console พิมพ์จำนวนครั้งที่แตะตอนจบ
- [ ] เขียนหนึ่งประโยคต่อกฎหนึ่งข้อ ว่าถ้าฝ่ากฎเหล็กข้อนั้นจะเห็นอาการอะไรบนจอ

## ไปต่อ

บทเรียน 2.6 เอาทุกอย่างนี้มาประกอบเป็นแผงควบคุม LED สามสีของทีมใน `s04_touch_panel.py` ที่แกะในสไลด์บทเรียนนี้
คือแถวละไฟสถานะ ปุ่มเปิด และปุ่มปิด ผ่าน `set_led()` ประตูเดียว พร้อมกล่องยืนยันก่อน "ปิดทั้งหมด"

บทเรียนถัดไป: [บทเรียน 2.6 — ลงมือทำ: แผงควบคุมสัมผัสของเรา และ widget ขั้นต่อไป](../l06-touch-panel-lab/README.md)

## สะท้อนคิด

- ถ้าจอของแผงควบคุมในโรงงานบอกว่าเครื่องหยุดแล้วแต่เครื่องยังหมุน บรรทัดไหนในโค้ดของคุณที่กันไม่ให้เรื่องนี้เกิด
- ลูปของคุณหลับ 50 ms ถ้าวันหนึ่งต้องเปลี่ยนเป็น 200 ms เพื่อแดชบอร์ดที่หนักขึ้น คุณแลกอะไรกับอะไร และจะรู้ได้อย่างไรว่ามีการแตะหาย
