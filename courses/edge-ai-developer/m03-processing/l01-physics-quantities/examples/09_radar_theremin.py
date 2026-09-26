# 09 - Radar Theremin: ระยะมือ = โน้ตดนตรี (ลำโพง J8) + เกจ pitch บนจอ
# ui.tone รับ MIDI note (60 = โด กลาง) - เล่น sine ผ่าน SFX mixer ฝั่ง CM55
import ui
ui.screen()
import lcd
import sensors
import time

NOTE_LOW, NOTE_HIGH = 45, 93          # A2 .. A6
MAX_M = 2.0

lcd.clear()
lcd.console('<h2> Radar Theremin</h2>')
sensors.radar_config(8.0)

ui.Label("Radar Theremin - ใกล้ = สูง, ไกล = ต่ำ", x=230, y=10, color=0xFFFFFF)
arc = ui.Arc(x=320, y=50, min=NOTE_LOW, max=NOTE_HIGH, value=NOTE_LOW)
seg = ui.Seg7("--", x=350, y=230, color=0x00FF88)
ui.Label("MIDI note", x=355, y=295, color=0x888888)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("เลื่อนมือหน้าบอร์ด 0.3 - 2.0 เมตร", x=60, y=360, color=0x888888)

has_sound = hasattr(ui, "tone")
if not has_sound:
    lcd.console('<span class=warn> firmware นี้ไม่มีเสียง - โชว์เกจอย่างเดียว</span>')

last_note = -1
try:
    while True:
        r = sensors.radar_range()
        if r["target"] and r["distance_m"] <= MAX_M:
            note = int(NOTE_HIGH - (r["distance_m"] / MAX_M)
                       * (NOTE_HIGH - NOTE_LOW))
            if has_sound:
                ui.tone(note, ui.WAVE_SINE, 100, 160)
            if note != last_note:
                arc.value(note)
                seg.text("%d" % note)
                last_note = note
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(180)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
