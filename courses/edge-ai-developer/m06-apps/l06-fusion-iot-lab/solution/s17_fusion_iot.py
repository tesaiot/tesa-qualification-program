# s17_fusion_iot.py - รวม verdict ของโมเดลกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) บนบอร์ด: ใส่ WIFI_SSID / WIFI_PASS ของ WiFi ที่คุณใช้ก่อนรัน
#          3) กด Program to Device แล้วเขย่าบอร์ดจนเหตุการณ์ fused ถูกส่งขึ้น broker
#          4) เปิดอีกเครื่องรัน  mosquitto_sub -h test.mosquitto.org -t tesaiot/edge-ai/s17
#             จะเห็นข้อความ JSON โผล่มาทุกครั้งที่เขย่าจริง
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ - ตอนพิมพ์เองสมองถึงจะจำ pattern ได้
#
# หัวใจของชุดบทเรียนนี้อยู่สองบรรทัด: fused = model_hit and raw_ok (fusion)
# และ mqtt.publish(TOPIC, payload) (IoT) ที่เหลือคือของเดิมที่คุณทำเป็นแล้ว

import edge_ai
import sensors
import ui
ui.screen()
import lcd
import time

# ----- remix ได้ที่นี่ -----
# เปลี่ยนสามบรรทัดนี้ = เปลี่ยนทั้งแอปโดยไม่ต้องแตะ logic ข้างล่างเลย
MODEL_KEYWORD = "Motion"      # โมเดลไหน (ค้นจากชื่อ ไม่ใช่ index)
TARGET_CLASS  = "shaking"     # จับคลาสไหนของโมเดลนั้น (ต้องตรงกับ labels เป๊ะ)
MOTION_FLOOR  = 40.0          # ประตูฟิสิกส์: gyro รวม (deg/s) ต้องเกินค่านี้จริง

# ----- IoT config -----
WIFI_SSID = "<ชื่อ WiFi ของคุณ>"  # ใส่ชื่อ WiFi ของคุณเองก่อนรัน
WIFI_PASS = "<รหัส WiFi ของคุณ>"  # ใส่รหัสของคุณตอนรัน และอย่า commit รหัสจริงขึ้น repo
BROKER    = "test.mosquitto.org"
PORT      = 1883
TOPIC     = "tesaiot/edge-ai/s17"     # ช่องที่ปลายทาง subscribe ไว้
CLIENT_ID = "bento-s17"               # ตั้งให้ไม่ซ้ำใครบน broker สาธารณะ

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
RED    = 0xE85B5B
CARD   = 0x2A1712

# ถ้าเฟิร์มแวร์ไม่มีโมดูล wifi/mqtt - import ไม่ได้ก็ตั้งธง offline
# ไว้ แทนที่จะให้ทั้งแอปพังตั้งแต่บรรทัด import (นิสัย degrade อย่างสง่างาม)
try:
    import wifi
    import mqtt
    HAVE_NET = True
except ImportError:
    HAVE_NET = False

lcd.clear()
lcd.console('<h2> Edge AI - fusion + IoT</h2>')


def find_model(keyword):
    """ค้นโมเดลจากชื่อ คืน dict ทั้งก้อน (ได้ทั้ง index และ labels มาใช้ต่อ)"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]          # ไม่เจอชื่อ ใช้ตัวแรกกันแอปพัง


# ต่อ WiFi ก่อน แล้วค่อยต่อ MQTT (mqtt ต้องมีเน็ตก่อน) ทั้งก้อนอยู่ใน try
# เพราะทุกขั้นพลาดได้ - เน็ตไม่ติด/broker ล่ม เราก็ยังอยากให้แอปรันแบบ SIM ต่อได้
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

# สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูป = จอกระพริบ + กินหน่วยความจำ)
ui.Label("Edge AI fusion", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=360, h=200, color=CARD)
verdict = ui.Seg7("---", x=40, y=70, color=GREEN)       # verdict จากโมเดล
conf = ui.Label("conf: -- %", x=40, y=158, color=CYAN)  # โมเดลมั่นใจแค่ไหน
raw_lab = ui.Label("gyro: --", x=40, y=190, color=CYAN)  # เซนเซอร์ดิบยืนยันแรงเท่าไร
state = ui.Label("รอเหตุการณ์ ...", x=40, y=214, color=DIM)
tx_lab = ui.Label("TX: 0", x=420, y=70, color=GREEN)
net_lab = ui.Label("MQTT: online" if ONLINE else "MQTT: [SIM]", x=420, y=100,
                   color=GREEN if ONLINE else RED)

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s - คลาส: %s' % (model['name'], ", ".join(labels)))
lcd.console(' เป้าหมาย: จับ "%s" + gyro > %.0f แล้วส่งขึ้นคลาวด์'
            % (TARGET_CLASS, MOTION_FLOOR))

tx_count = 0


def publish_event(conf_val, gmag):
    """ที่ที่ fused decision กลายเป็นข้อความบนคลาวด์
    payload พก verdict (event, conf) + หลักฐานดิบ (gyro) ให้ปลายทางตรวจสอบย้อนหลังได้"""
    global tx_count
    payload = '{"event":"%s","conf":%.2f,"gyro":%.0f,"ts":%d}' % (
        TARGET_CLASS, conf_val, gmag, time.ticks_ms())
    state.text("! ส่งเหตุการณ์ !")
    state.color(GREEN)
    if HAVE_NET and ONLINE and mqtt.is_connected():
        try:
            # หัวใจ IoT: ส่งเหตุการณ์ที่ผ่าน fusion ขึ้น topic ที่ปลายทางฟังอยู่
            mqtt.publish(TOPIC, payload)
            lcd.console('<span class=ok> MQTT TX: ' + payload + '</span>')
        except OSError as e:
            # เน็ตหลุดกลางคัน - แอปต้องไม่ล้ม แค่รายงานแล้วไปต่อ
            lcd.console('<span class=error> ส่งไม่สำเร็จ: %s</span>' % e)
    else:
        # โหมด offline: กลไกครบ แค่โชว์ payload แทนการส่งจริง
        lcd.console('<span class=info> [SIM] ' + payload + '</span>')
    tx_count += 1
    tx_lab.text("TX: %d" % tx_count)


try:
    # เลือกโมเดลจากทะเบียนแล้วสั่ง CM55 ให้เริ่มรัน (confirm by observation)
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มอนุมาน %s</span>' % model['name'])
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1          # กันวาดจอ/อ่านเซนเซอร์ซ้ำ: ทำเฉพาะตอนมี verdict ใหม่
fired = False          # edge-trigger: ยิงเหตุการณ์ครั้งเดียวต่อการเจอ

try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # จังหวะ 2: อ่าน verdict ล่าสุด (pull, ไม่บล็อกรอ)
        r = edge_ai.result()

        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))

            # จังหวะ 3 (fuse ครึ่งแรก): อ่านเซนเซอร์ดิบมาประกบ - นี่คือ "เส้นทางที่สอง"
            # ของสัญญาณเดียวกัน (IMU) โมเดลเห็นผ่าน NPU เราอ่านค่าปัจจุบันดิบๆ บน CM33
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            gmag = abs(gx) + abs(gy) + abs(gz)      # พลังงานการหมุนรวม (deg/s)
            raw_lab.text("gyro: %.0f" % gmag)

            model_hit = (r['label'] == TARGET_CLASS
                         and r['conf'] >= edge_ai.CONF_FLOOR)   # ด่านที่ 1: โมเดล
            raw_ok = gmag > MOTION_FLOOR                          # ด่านที่ 2: เซนเซอร์ดิบ

            # จังหวะ 3 (fuse ครึ่งหลัง): AND สองด่าน - false positive ของโมเดลจะถูก
            # กรองออกถ้าเซนเซอร์ดิบไม่เห็นด้วย (และกลับกัน) นี่คือ sensor fusion
            fused = model_hit and raw_ok

            if fused and not fired:
                publish_event(r['conf'], gmag)     # ยิงเหตุการณ์เดียว ตอนขอบขาขึ้น
                fired = True
            elif not fused:
                fired = False                      # หลุดเงื่อนไขแล้ว รีเซ็ตธง
                state.text("รอเหตุการณ์ ...")
                state.color(DIM)

        time.sleep_ms(250)      # เว้นจังหวะ ไม่รัดจอ/ไม่ spam broker
except KeyboardInterrupt:
    pass
finally:
    # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น: หยุดโมเดล + ตัด broker
    edge_ai.stop()
    if HAVE_NET and ONLINE:
        try:
            mqtt.disconnect()
        except OSError:
            pass
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
