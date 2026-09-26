# s17_fusion_iot.py - รวม verdict ของโมเดลกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์ (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 5 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) บนบอร์ด: ใส่ WIFI_SSID / WIFI_PASS ของ WiFi ที่คุณใช้ก่อนรัน
#             บน Emulator: WiFi จำลองต่อติดเอง ถ้าเน็ตไม่ติดจะเข้าโหมด [SIM] (ไม่พัง)
#          4) กด Program to Device แล้วเขย่าบอร์ดจริงจนเหตุการณ์ fused ถูกส่ง
#
# ชุดบทเรียนนี้ต่อยอดจาก "verdict -> action" (บทเรียน 1.6–1.7 / 6.3–6.4) อีกสองชั้น:
#   fusion  - action ยิงเมื่อ verdict ของโมเดล "และ" เซนเซอร์ดิบ เห็นตรงกัน (กัน false positive)
#   IoT     - เหตุการณ์ที่ผ่าน fusion ถูก publish ขึ้น MQTT broker (ออกไปนอกบอร์ด)
# อ้างอิงแอปโหวต 3 เซนเซอร์: m06-apps/l05-sensor-fusion/examples/10_motion_alarm.py

import edge_ai
import sensors
import ui
ui.screen()
import lcd
import time

# ----- remix ได้ที่นี่ (สองสามบรรทัดนี้คือปุ่มปรับทั้งแอป) -----
MODEL_KEYWORD = "Motion"      # -> "Baby Cry" / "Cough" / "Siren" / "Push"
TARGET_CLASS  = "shaking"     # -> คลาสของโมเดลใหม่ (ดูจาก labels ในคอนโซล)
MOTION_FLOOR  = 40.0          # ประตูเซนเซอร์ดิบ: gyro รวม (deg/s) ต้องเกินค่านี้

# ----- IoT config -----
WIFI_SSID = "<ชื่อ WiFi ของคุณ>"  # ใส่ชื่อ WiFi ของคุณเองก่อนรัน
WIFI_PASS = "<รหัส WiFi ของคุณ>"  # ใส่รหัสของคุณตอนรัน และอย่า commit รหัสจริงขึ้น repo
BROKER    = "test.mosquitto.org"       # broker สาธารณะ (ฟรี ไม่ต้องล็อกอิน)
PORT      = 1883
TOPIC     = "tesaiot/edge-ai/s17"
CLIENT_ID = "bento-s17"

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
RED    = 0xE85B5B
CARD   = 0x2A1712

# โค้ดชุดเดียวต้องรันได้ทั้งบอร์ด Emulator และที่ที่ไม่มีเน็ต
# ถ้าไม่มีโมดูล wifi/mqtt ก็ตั้งธง offline แทนที่จะ crash ตอน import
try:
    import wifi
    import mqtt
    HAVE_NET = True
except ImportError:
    HAVE_NET = False

lcd.clear()
lcd.console('<h2> Edge AI - fusion + IoT</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อ (ไม่ hard-code index) - ยืมมาจากบทเรียน 1.6–1.7"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


# ต่อ WiFi + MQTT (ให้ไว้แล้ว - ห่อ try/except เผื่อ Emulator/เน็ตไม่ติด)
ONLINE = False
if HAVE_NET:
    try:
        if not wifi.is_connected():
            lcd.console(' กำลังต่อ WiFi: %s' % WIFI_SSID)
            wifi.connect(WIFI_SSID, WIFI_PASS)
        if wifi.is_connected():
            lcd.console('<span class=ok> WiFi ok: %s</span>' % wifi.ip())
            mqtt.connect(BROKER, PORT, client_id=CLIENT_ID)
            ONLINE = mqtt.is_connected()
    except OSError as e:
        lcd.console('<span class=error> เน็ตไม่ติด (จะไปโหมด SIM): %s</span>' % e)
        ONLINE = False

if ONLINE:
    lcd.console('<span class=ok> MQTT ok -> %s/%s</span>' % (BROKER, TOPIC))
else:
    lcd.console('<span class=info> โหมด offline [SIM] - จะโชว์ payload แทนการส่งจริง</span>')

# สร้าง widget ครั้งเดียวก่อนเข้าลูป
ui.Label("Edge AI fusion", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=360, h=200, color=CARD)
verdict = ui.Seg7("---", x=40, y=70, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=158, color=CYAN)
raw_lab = ui.Label("gyro: --", x=40, y=190, color=CYAN)
state = ui.Label("รอเหตุการณ์ ...", x=40, y=214, color=DIM)
tx_lab = ui.Label("TX: 0", x=420, y=70, color=GREEN)
net_lab = ui.Label("MQTT: online" if ONLINE else "MQTT: [SIM]", x=420, y=100,
                   color=GREEN if ONLINE else RED)

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()

model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s - คลาส: %s' % (model['name'], ", ".join(labels)))
lcd.console(' เป้าหมาย: จับ "%s" + gyro > %.0f แล้วส่งขึ้นคลาวด์'
            % (TARGET_CLASS, MOTION_FLOOR))

tx_count = 0


def publish_event(conf_val, gmag):
    """fused decision กลายเป็นข้อความบนคลาวด์ (หรือ [SIM] บน console ถ้า offline)"""
    global tx_count
    payload = '{"event":"%s","conf":%.2f,"gyro":%.0f,"ts":%d}' % (
        TARGET_CLASS, conf_val, gmag, time.ticks_ms())
    state.text("! ส่งเหตุการณ์ !")
    state.color(GREEN)
    if HAVE_NET and ONLINE and mqtt.is_connected():
        try:
            # เติม: ส่ง payload ขึ้น broker ด้วย mqtt.publish(TOPIC, payload)
            pass
            lcd.console('<span class=ok> MQTT TX: ' + payload + '</span>')
        except OSError as e:
            lcd.console('<span class=error> ส่งไม่สำเร็จ: %s</span>' % e)
    else:
        lcd.console('<span class=info> [SIM] ' + payload + '</span>')
    tx_count += 1
    tx_lab.text("TX: %d" % tx_count)


try:
    # เติม: สั่งให้ CM55 รันโมเดลนี้ ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มอนุมาน %s</span>' % model['name'])
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1
fired = False

try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
        r = None
        pass

        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))

            # เติม: อ่านเซนเซอร์ดิบมายืนยัน verdict
            #       -> ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            gx = gy = gz = 0.0
            pass
            gmag = abs(gx) + abs(gy) + abs(gz)
            raw_lab.text("gyro: %.0f" % gmag)

            model_hit = (r['label'] == TARGET_CLASS
                         and r['conf'] >= edge_ai.CONF_FLOOR)   # โมเดลผ่าน
            raw_ok = gmag > MOTION_FLOOR                          # เซนเซอร์ดิบผ่าน

            # เติม: รวมสองสัญญาณด้วย AND  ->  fused = model_hit and raw_ok
            fused = False
            pass

            if fused and not fired:
                publish_event(r['conf'], gmag)     # สองสัญญาณเห็นตรงกัน -> ส่ง
                fired = True
            elif not fused:
                fired = False
                state.text("รอเหตุการณ์ ...")
                state.color(DIM)

        time.sleep_ms(250)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()                     # หยุดเครื่องยนต์อนุมานเสมอ
    if HAVE_NET and ONLINE:
        try:
            mqtt.disconnect()          # ตัดการเชื่อมต่อ broker ให้เรียบร้อย
        except OSError:
            pass
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
