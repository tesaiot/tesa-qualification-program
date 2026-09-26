# 10 - ระบบกันขโมย 3 เซนเซอร์ + สวิตช์ arm/disarm บนจอ
# *** ข้อจำกัดปัจจุบัน: ตัวอย่างนี้ใช้ได้บน PSoC Edge AI Kit ***
# บน TESAIoT Dev Kit (มี audio codec) การเปิด PDM จะชนกับ clock ของ
# ระบบเสียง CM55 - แก้ใน firmware phase ถัดไป (PDM clock guard)
# state machine: DISARMED -> ARMED -> TRIGGERED (โหวต 2 ใน 3)
# จออัปเดตเฉพาะตอน "สถานะเปลี่ยน" - pattern เดียวกับระบบ embedded จริง
import ui
ui.screen()
import lcd
from machine import PDM_PCM
import sensors
import array, math, time

lcd.clear()
lcd.console('<h2> Motion Alarm (radar + IMU + mic)</h2>')

ui.Label("Security Monitor", x=310, y=8, color=0xFFFFFF)
panel = ui.Panel(x=60, y=45, w=670, h=200, color=0x333333)
state_lab = ui.Label("DISARMED", x=320, y=125, color=0xAAAAAA)
ui.Label("Arm ระบบ:", x=60, y=280, color=0xAAAAAA)
sw = ui.Switch(x=180, y=272)
sw_id = sw.id()
votes_lab = ui.Label("", x=320, y=280, color=0xFFAA44)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()

pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
mic = array.array("h", (0 for _ in range(512)))

def mic_db():
    pdm.readinto(mic)
    acc = 0
    for s in mic:
        acc += s * s
    rms = math.sqrt(acc / len(mic))
    return 20 * math.log10(rms / 32768) if rms > 0 else -96.0

# จำ baseline gyro ตอนสงบ
base = 0.0
for _ in range(10):
    ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
    base += abs(gx) + abs(gy) + abs(gz)
    time.sleep_ms(50)
base /= 10

armed = False
triggered = False
try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
            if ev.get('handle') == sw_id and ev.get('type') == 'toggled':
                armed = bool(ev.get('value'))
                triggered = False
                if armed:
                    panel.color(0x114411); state_lab.text("ARMED")
                    state_lab.color(0x44FF88); votes_lab.text("")
                    lcd.console('<span class=info> ระบบพร้อมเฝ้าระวัง</span>')
                else:
                    panel.color(0x333333); state_lab.text("DISARMED")
                    state_lab.color(0xAAAAAA); votes_lab.text("")
                    lcd.console(' ปิดระบบ')

        if armed and not triggered:
            votes = []
            if sensors.radar()["presence"]:
                votes.append("radar")
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            if (abs(gx) + abs(gy) + abs(gz)) > base + 30:
                votes.append("imu")
            if mic_db() > -25:
                votes.append("mic")

            if len(votes) >= 2:                     # โหวต 2 ใน 3 = บุกรุกจริง
                triggered = True
                panel.color(0xAA1111)
                state_lab.text("!! INTRUDER !!")
                state_lab.color(0xFFFFFF)
                votes_lab.text("+".join(votes))
                if hasattr(ui, "sfx"):
                    ui.sfx(ui.SFX_GAME_OVER)
                lcd.console('<span class=error> ALERT: %s</span>'
                            % "+".join(votes))
        time.sleep_ms(300)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')
finally:
    pdm.deinit()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
