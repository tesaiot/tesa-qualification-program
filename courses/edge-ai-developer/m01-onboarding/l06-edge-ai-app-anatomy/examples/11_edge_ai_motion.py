# 11 - Edge AI: โมเดล AI จำแนกการเคลื่อนไหว (รันบนบอร์ด ไม่ต้องต่อเน็ต)
#
# โมเดล DEEPCRAFT ทำงานบน CM55 (TFLite-Micro + Ethos-U55 NPU) อ่าน IMU
# แล้วส่งผลกลับมาที่ MicroPython ผ่าน deepcraft model link
#
# ลองทำท่าเหล่านี้: ถือบอร์ดวาดวงกลมในอากาศ / เขย่าบอร์ด / วางนิ่ง
import ui
ui.screen()
import lcd
import deepcraft
import time

CLASSES = ("idle", "circle", "shaking")

lcd.clear()
lcd.console('<h2> Edge AI - Motion Classifier</h2>')
lcd.console(' links: %s' % str(deepcraft.links()))

ui.Label("Edge AI - Motion", x=300, y=10, color=0xBB86FC)
verdict = ui.Seg7("---", x=280, y=60, color=0x50D890)
conf = ui.Bar(x=60, y=170, w=670, min=0, max=100, value=0)
lab_conf = ui.Label("confidence: --", x=60, y=140, color=0xAAAAAA)
lab_hint = ui.Label("วาดวงกลมในอากาศ / เขย่าบอร์ด", x=60, y=210, color=0x888888)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()

# deferred pattern: the model fires events fast — the callback ONLY stashes the
# latest value (cheap). The main loop draws the UI at a fixed cadence. Doing 4 IPC
# writes + a console log per event floods the IPC pipe and freezes the display.
_state = {"cls": -1, "pct": 0, "status": None}

def on_event(event, value):
    if event == deepcraft.EVENT_READY:
        _state["status"] = "ready"
    elif event == deepcraft.EVENT_STOPPED:
        _state["status"] = "stopped"
    elif event == deepcraft.EVENT_ERROR:
        _state["status"] = "error"
    else:
        # INTENT: value = (เปอร์เซ็นต์ << 8) | หมายเลขคลาส
        _state["cls"] = value & 0xFF
        _state["pct"] = (value >> 8) & 0xFF

m = deepcraft.DeepcraftModel()
m.set_event_cb(on_event)
m.start()

_STATUS_MSG = {"ready": '<span class=ok> โมเดลพร้อมแล้ว</span>',
               "stopped": ' โมเดลหยุดทำงาน',
               "error": '<span class=error> โมเดลผิดพลาด</span>'}
last_status = None
last_cls = -1
try:
    while True:
        # status changes: log once
        st = _state["status"]
        if st != last_status:
            lcd.console(_STATUS_MSG.get(st, ''))
            last_status = st
        # inference: redraw at loop cadence (not per-event); console only on change
        cls = _state["cls"]
        if cls >= 0:
            pct = _state["pct"]
            name = CLASSES[cls] if cls < len(CLASSES) else "?"
            conf.value(pct)
            lab_conf.text("confidence: %d%%" % pct)
            if cls != last_cls:
                verdict.text(name)
                lcd.console(' %s (%d%%)' % (name, pct))
                last_cls = cls
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    m.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
