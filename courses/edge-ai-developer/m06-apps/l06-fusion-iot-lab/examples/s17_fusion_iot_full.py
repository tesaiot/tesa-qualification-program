# s17_fusion_iot_full.py - fusion + IoT ฉบับขัดเรียบร้อย
# ต่อยอดจาก solution: เพิ่มของที่ทำให้ "ใช้งานได้จริง" ขึ้นอีกขั้น
#   - multi-modal gate: เลือก gate ได้ 2 แบบ  "imu" (gyro ดิบ) หรือ "radar" (มีคนไหม)
#     -> "radar" คือ fusion แบบ multi-modal จริง (โมเดลใช้ IMU, gate ใช้เรดาร์ คนละเซนเซอร์)
#   - นับจำนวนเหตุการณ์ + เวลาเหตุการณ์ล่าสุด
#   - reconnect broker อัตโนมัติถ้าหลุดกลางทาง
#   - โชว์ WiFi RSSI (ความแรงสัญญาณ) ให้เห็นสุขภาพการเชื่อมต่อ
# รันได้ทั้งบอร์ดและ Emulator ด้วยโค้ดชุดเดียว ถ้าเน็ตไม่ติดจะเข้าโหมด [SIM]
#
# แนวคิดปิดกล่อง โมดูล 6 (Apps): verdict (บทเรียน 1.6–1.7 / 6.3–6.4) + raw gate (บทเรียน 3.3–3.4) + IoT = ระบบ Edge AI
# ที่ตัดสินใจเชื่อถือได้แล้วสตรีมข้อสรุปขึ้นคลาวด์ - ต่างจาก Cloud AI ตรงที่เราส่งแค่
# "เหตุการณ์ที่ผ่านการยืนยัน" ไม่ใช่ข้อมูลดิบทั้งสตรีม (privacy + bandwidth)

import edge_ai
import sensors
import ui
ui.screen()
import lcd
import time

# ----- remix -----
MODEL_KEYWORD = "Motion"
TARGET_CLASS  = "shaking"
GATE_MODE     = "imu"       # "imu" = gyro ดิบ (corroboration) | "radar" = มีคน (multi-modal)
MOTION_FLOOR  = 40.0        # เกณฑ์ gyro รวม (deg/s) เมื่อ GATE_MODE = "imu"

# ----- IoT -----
WIFI_SSID = "<ชื่อ WiFi ของคุณ>"  # ใส่ชื่อ WiFi ของคุณเองก่อนรัน
WIFI_PASS = "<รหัส WiFi ของคุณ>"  # ใส่รหัสของคุณตอนรัน และอย่า commit รหัสจริงขึ้น repo
BROKER    = "test.mosquitto.org"
PORT      = 1883
TOPIC     = "tesaiot/edge-ai/s17"
CLIENT_ID = "bento-s17-full"

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
RED    = 0xE85B5B
AMBER  = 0xFFB454
CARD   = 0x2A1712

try:
    import wifi
    import mqtt
    HAVE_NET = True
except ImportError:
    HAVE_NET = False

lcd.clear()
lcd.console('<h2> Edge AI - fusion + IoT (full)</h2>')


def find_model(keyword):
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


def net_up():
    """ต่อ WiFi + MQTT ให้พร้อม คืน True ถ้า online จริง (เรียกซ้ำเพื่อ reconnect ได้)"""
    if not HAVE_NET:
        return False
    try:
        if not wifi.is_connected():
            wifi.connect(WIFI_SSID, WIFI_PASS)
        if not wifi.is_connected():
            return False
        if not mqtt.is_connected():
            mqtt.connect(BROKER, PORT, client_id=CLIENT_ID)
        return mqtt.is_connected()
    except OSError:
        return False


ONLINE = net_up()
if ONLINE:
    lcd.console('<span class=ok> WiFi %s · MQTT %s/%s</span>' % (wifi.ip(), BROKER, TOPIC))
else:
    lcd.console('<span class=info> โหมด offline [SIM] - โชว์ payload แทนการส่งจริง</span>')

# UI
ui.Label("Edge AI fusion + IoT", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=380, h=210, color=CARD)
verdict = ui.Seg7("---", x=40, y=70, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=158, color=CYAN)
raw_lab = ui.Label("gate: --", x=40, y=188, color=CYAN)
state = ui.Label("รอเหตุการณ์ ...", x=40, y=216, color=DIM)

tx_lab = ui.Label("events: 0", x=430, y=70, color=GREEN)
last_lab = ui.Label("last: -", x=430, y=104, color=CYAN)
net_lab = ui.Label("net: [SIM]", x=430, y=138, color=RED)
rssi_lab = ui.Label("rssi: -", x=430, y=172, color=DIM)

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()


def refresh_net_ui():
    if ONLINE:
        net_lab.text("net: online")
        net_lab.color(GREEN)
        try:
            rssi_lab.text("rssi: %d dBm" % wifi.status()["rssi"])
        except (OSError, AttributeError):
            rssi_lab.text("rssi: -")
    else:
        net_lab.text("net: [SIM]")
        net_lab.color(AMBER if HAVE_NET else RED)
        rssi_lab.text("rssi: -")


refresh_net_ui()

model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s · คลาส: %s · gate: %s'
            % (model['name'], ", ".join(labels), GATE_MODE))

tx_count = 0


def read_gate():
    """คืน (ผ่านประตูไหม, ค่าที่จะโชว์) ตาม GATE_MODE
    imu   = gyro ดิบเกินเกณฑ์ (corroboration - เซนเซอร์เดียวกับโมเดล มองคนละมุม)
    radar = มีคนอยู่จริงไหม   (multi-modal  - คนละเซนเซอร์กับโมเดลเลย)"""
    if GATE_MODE == "radar":
        try:
            present = sensors.radar()["presence"]
        except OSError:
            present = False
        return bool(present), ("radar: %s" % ("yes" if present else "no"))
    ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
    gmag = abs(gx) + abs(gy) + abs(gz)
    return gmag > MOTION_FLOOR, ("gyro: %.0f" % gmag)


def publish_event(conf_val, gate_str):
    global tx_count, ONLINE
    payload = '{"event":"%s","conf":%.2f,"gate":"%s","ts":%d}' % (
        TARGET_CLASS, conf_val, gate_str.replace(" ", ""), time.ticks_ms())
    state.text("! ส่งเหตุการณ์ !")
    state.color(GREEN)
    sent = False
    if HAVE_NET and ONLINE:
        try:
            if not mqtt.is_connected():      # หลุดกลางทาง -> ลองต่อใหม่
                ONLINE = net_up()
                refresh_net_ui()
            if mqtt.is_connected():
                mqtt.publish(TOPIC, payload)
                sent = True
        except OSError as e:
            lcd.console('<span class=error> ส่งไม่สำเร็จ: %s</span>' % e)
            ONLINE = False
            refresh_net_ui()
    if sent:
        lcd.console('<span class=ok> MQTT TX: ' + payload + '</span>')
    else:
        lcd.console('<span class=info> [SIM] ' + payload + '</span>')
    tx_count += 1
    tx_lab.text("events: %d" % tx_count)
    last_lab.text("last: %s" % gate_str)


try:
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มอนุมาน %s</span>' % model['name'])
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1
fired = False
ticks = 0

try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        r = edge_ai.result()
        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))

            gate_ok, gate_str = read_gate()
            raw_lab.text(gate_str)

            model_hit = (r['label'] == TARGET_CLASS
                         and r['conf'] >= edge_ai.CONF_FLOOR)
            fused = model_hit and gate_ok      # verdict AND gate = fused decision

            if fused and not fired:
                publish_event(r['conf'], gate_str)
                fired = True
            elif not fused:
                fired = False
                state.text("รอเหตุการณ์ ...")
                state.color(DIM)

        ticks += 1
        if ticks % 40 == 0:                    # ~10 วินาที: รีเฟรช rssi + สุขภาพเน็ต
            refresh_net_ui()

        time.sleep_ms(250)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    if HAVE_NET and ONLINE:
        try:
            mqtt.disconnect()
        except OSError:
            pass
    lcd.console('<span class=ok> จบการทำงาน · ส่งไป %d เหตุการณ์</span>' % tx_count)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
