# 04 - Radar: ป้ายสถานะใหญ่เปลี่ยนสีเมื่อพบคน (event-driven)
# บทเรียนสำคัญ: อัปเดตจอ "เฉพาะตอนสถานะเปลี่ยน" - จอนิ่ง สายตาไม่ล้า และ IPC ไม่รก
import ui
ui.screen()
import lcd
import sensors
import time

lcd.clear()
lcd.console('<h2> Radar Presence Monitor</h2>')

panel = ui.Panel(x=100, y=50, w=590, h=220, color=0x115511)
state = ui.Label("CLEAR", x=330, y=140, color=0xFFFFFF)
lab_e = ui.Label("energy: --", x=100, y=290, color=0xAAAAAA)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("นั่งนิ่งๆ หน้าบอร์ด vs ออกนอกระยะ", x=60, y=360, color=0x888888)

was = None
try:
    while True:
        r = sensors.radar()
        now = bool(r["presence"])
        if now != was:                          # เปลี่ยนสถานะเท่านั้นถึงวาดใหม่
            if now:
                panel.color(0x881111)
                state.text("PRESENCE")
                if hasattr(ui, "sfx"):
                    ui.sfx(ui.SFX_UI_DENY)
                lcd.console('<span class=warn> พบการเคลื่อนไหว!</span>')
            else:
                panel.color(0x115511)
                state.text("CLEAR")
                lcd.console('<span class=ok> พื้นที่ว่าง</span>')
            was = now
        lab_e.text("energy: %.0f" % r["energy"])
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(300)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
