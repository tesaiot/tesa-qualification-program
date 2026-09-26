# 06 - VU Meter: ไมค์ PDM -> RMS -> dBFS -> แถบระดับเสียง + peak hold
# *** ข้อจำกัดปัจจุบัน: ตัวอย่างนี้ใช้ได้บน PSoC Edge AI Kit ***
# บน TESAIoT Dev Kit (มี audio codec) การเปิด PDM จะชนกับ clock ของ
# ระบบเสียง CM55 - แก้ใน firmware phase ถัดไป (PDM clock guard)
# Bar อัปเดตค่าเดียวต่อรอบ = เร็วพอวิ่ง ~15 Hz ได้สบาย
import ui
ui.screen()
import lcd
from machine import PDM_PCM
import sensors
import array, math, time

lcd.clear()
lcd.console('<h2> Microphone VU Meter</h2>')

ui.Label("PDM Mic - Level (dBFS)", x=290, y=10, color=0xFFFFFF)
bar = ui.Bar(x=50, y=90, w=690, min=0, max=60, value=0)   # แกน 0..60 = -60..0 dBFS
seg = ui.Seg7("---", x=300, y=150, color=0x00FF88)
lab_peak = ui.Label("peak: --", x=330, y=230, color=0xFFAA44)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("พูด / ปรบมือ ใส่ไมค์บนบอร์ด", x=60, y=360, color=0x888888)

pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
buf = array.array("h", (0 for _ in range(1024)))

peak = -96.0
try:
    while True:
        pdm.readinto(buf)
        acc = 0
        for s in buf:
            acc += s * s
        rms = math.sqrt(acc / len(buf))
        db = 20 * math.log10(rms / 32768) if rms > 0 else -96.0
        peak = max(peak, db)
        bar.value(max(0, int(db + 60)))
        seg.text("%d" % int(db))
        lab_peak.text("peak: %.1f dBFS" % peak)
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(60)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบ: peak %.1f dBFS</span>' % peak)
finally:
    pdm.deinit()                                # คืน hardware เสมอ

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
