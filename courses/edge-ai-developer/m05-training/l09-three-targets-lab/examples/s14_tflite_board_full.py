# s14_tflite_board_full.py - แล็บเทียบเป้าหมายครบวง: PC vs Web vs MCU จากโมเดลไฟล์เดียว (ฉบับเต็ม)
# วิธีรัน: เปิดใน shared/training/ (มี dataset_tools.py + model_int8.tflite + quantize_vela.sh)
#          pip install ai-edge-litert numpy        # (tensorflow ถ้าจะสร้าง model_web.tflite เอง)
#          python s14_tflite_board_full.py                 # bench int8(PC) + web(ถ้ามี) + Vela + ตาราง
#          python s14_tflite_board_full.py --mcu-ms 3.9    # เติมช่อง MCU ด้วยค่าจาก edge_ai.latency()
#          python s14_tflite_board_full.py --show-mpy      # พิมพ์ MPY สั้นๆ สำหรับอ่าน latency บนบอร์ด
#
# ฉบับนี้คือเวอร์ชันขัดจนเรียบร้อยของ s14_tflite_board.py — โครงเดียวกับที่คุณเติมในไฟล์ฝึก
# แต่เดินให้ครบเรื่อง: (1) bench int8 บน PC เป็น ground truth ทั้ง accuracy และ latency,
# (2) ถ้ามี model_web.tflite ก็ bench เส้นทางเบราว์เซอร์ (float I/O) เทียบ accuracy ให้เห็น,
# (3) รัน Vela ได้ไฟล์ MCU-only, (4) รวมทุกอย่างเป็นตารางเดียว MCU/Web/PC พร้อมคอลัมน์ power.
# หลักเดิมไม่เปลี่ยน: ไฟล์ int8 กราฟเดียว accuracy ตรงกันทุกเป้าหมาย ต่างกันที่ latency/พลังงาน
# ซึ่งคือหัวใจของคำถามวิศวกร "โมเดลตัวนี้ควรอยู่ที่ไหน"

import argparse
import os
import subprocess
import time

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    from tensorflow.lite import Interpreter

import dataset_tools as dt


# ---- โหลดข้อมูล + normalization ---------------------------------------------

def load_test_set(data_path, model_path):
    """คืน (Xte, yte, z) โดยใช้ split ชุดเดียวกับ eval_pc — normalize ทำข้างใน bench_* เอง
    เพื่อให้ทั้งเส้นทาง int8 และ web เดิน front-end ชุดเดียวกันเป๊ะ (parity เริ่มที่ตรงนี้)"""
    if not os.path.exists(data_path):
        dt.synthesize(data_path)
    samples, labels = dt.load_csv(data_path)
    X, y = dt.make_windows(samples, labels)
    _, _, (Xte, yte) = dt.split(X, y)
    z = np.load(model_path + ".norm.npz")
    return Xte, yte, z


# ---- เส้นทาง int8 (แบบบอร์ด/PC) — ground truth ------------------------------

def bench_int8(model_path, X, y, z):
    """รันไฟล์ int8 เต็ม (int8 in/out) — เส้นทางเดียวกับที่ NPU จะรันหลัง Vela คอมไพล์.
    วัด accuracy (ground truth ที่ MCU ต้องได้เท่ากัน) + latency เฉลี่ยเฉพาะช่วง invoke()"""
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]

    correct, total_ms = 0, 0.0
    for i in range(len(X)):
        x = (X[i:i + 1] - z["mean"]) / z["std"]                       # (1) normalize
        q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)  # (2) quantize
        it.set_tensor(inp["index"], q)
        t0 = time.perf_counter()
        it.invoke()                                                  # (3) อนุมานล้วน
        total_ms += (time.perf_counter() - t0) * 1000.0
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale                               # (4) dequantize
        correct += int(o.argmax() == y[i])
    return correct / len(X), total_ms / len(X)


# ---- เส้นทาง web (float I/O แบบเบราว์เซอร์) ----------------------------------

def bench_web(model_path, X, y, z):
    """รันไฟล์ web (float32 I/O) — เส้นทางเดียวกับ LiteRT.js ในเบราว์เซอร์ ไม่ต้อง quantize เอง.
    accuracy อาจต่างจาก int8 นิดหน่อยเพราะ activation เป็น float (ไม่ถูกบีบเป็น int8) — ตรงนี้
    แหละที่เห็นว่า 'ไฟล์เดียวกันเชิงน้ำหนัก แต่คนละ I/O' ให้ตัวเลขใกล้กันแต่ไม่เป๊ะ 100%"""
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    correct, total_ms = 0, 0.0
    for i in range(len(X)):
        x = ((X[i:i + 1] - z["mean"]) / z["std"]).astype(np.float32)
        it.set_tensor(inp["index"], x)
        t0 = time.perf_counter()
        it.invoke()
        total_ms += (time.perf_counter() - t0) * 1000.0
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        correct += int(o.argmax() == y[i])
    return correct / len(X), total_ms / len(X)


# ---- ขั้นพิเศษของ MCU: Vela --------------------------------------------------

def run_vela(int8_path):
    """เรียก quantize_vela.sh ให้ Vela คอมไพล์ int8 -> _vela.tflite สำหรับ Ethos-U55.
    เป็นขั้นเดียวที่มีแค่ MCU ต้องทำ (Web/Cortex-A ใช้ไฟล์ int8 เดิม) เพราะ Vela ฝัง custom op
    'ethos-u' ที่รันได้เฉพาะบน NPU. คืน path ไฟล์ผลลัพธ์ หรือ None ถ้าเครื่องนี้ยังไม่มี vela"""
    try:
        subprocess.run(["./quantize_vela.sh", int8_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ยังไม่มี vela ในเครื่องนี้ (อยู่ใน Docker image ของ บทเรียน 5.3–5.5) — ข้ามขั้น Vela ไปก่อนได้")
        return None
    base = os.path.splitext(os.path.basename(int8_path))[0]
    out = os.path.join("output", base + "_vela.tflite")
    return out if os.path.exists(out) else None


# ---- ตารางเทียบเป้าหมาย ------------------------------------------------------

def print_table(pc_acc, pc_ms, web, mcu_ms):
    """สรุปทุกอย่างเป็นตารางเดียว. accuracy MCU = accuracy int8 บน PC (Vela ไม่แก้คณิต).
    คอลัมน์ power เป็นเชิงคุณภาพ: NPU เร่งเมทริกซ์ด้วยพลังงานต่อการอนุมานต่ำสุด รองมาคือ CPU
    ฝั่ง PC/Cortex-A ส่วนเบราว์เซอร์แล้วแต่เครื่องผู้ใช้ (วัดยากข้ามอุปกรณ์)"""
    web_acc = "%.3f" % web[0] if web else "  -  "
    web_ms = "%.2f ms" % web[1] if web else "  -  "
    mcu_lat = "%.2f ms" % mcu_ms if mcu_ms is not None else "อ่านจากบอร์ด"
    print()
    print("เป้าหมาย   | ไฟล์ที่ใช้             | accuracy | latency/win | power/อนุมาน | รันด้วย")
    print("-----------+-----------------------+----------+-------------+--------------+------------------")
    print("PC/Docker  | model_int8.tflite     |  %.3f   | %11.2f ms | กลาง         | ai-edge-litert"
          % (pc_acc, pc_ms))
    print("MCU + NPU  | model_int8_vela.tflite|  %.3f   | %11s | ต่ำสุด        | edge_ai (Ethos-U55)"
          % (pc_acc, mcu_lat))
    print("Web        | model_web.tflite      |  %5s   | %11s | แล้วแต่เครื่อง  | LiteRT.js (เบราว์เซอร์)"
          % (web_acc, web_ms))
    print("Cortex-A   | model_int8.tflite     |  %.3f   |  (บนบอร์ดนั้น)| กลาง         | ai-edge-litert"
          % pc_acc)
    print()
    print("อ่านตาราง:")
    print(" - accuracy ตรงกันทั้ง int8 ทุกเป้าหมาย (กราฟเดียวกัน) Web ต่างเล็กน้อยเพราะ activation เป็น float")
    print(" - มีแค่ MCU ที่ต้องขั้น Vela เพิ่ม (custom op ethos-u) ที่เหลือใช้ .tflite ตรงๆ")
    print(" - latency/power ต่างกันคนละโลก -> คำถามวิศวกร: งานนี้ต้องเร็ว/ประหยัดแค่ไหน ควรอยู่เป้าหมายไหน")


# ---------------------------------------------------------------------------
# ฝั่ง MicroPython — โมเดลที่ wrap เป็น AIM_* (ai_models/README.md ของ SDK) โผล่ใน edge_ai.models() เอง
# (ทะเบียนเป็น shape-driven ไม่ต้องแตะ MicroPython/IPC) อ่าน latency บน NPU ได้แบบโมเดลอื่น —
# นี่คือรอยต่อ Python (ฝึก/วัดบน PC) -> MPY (รันจริงบนบอร์ด) ที่ชุดบทเรียนนี้พาข้าม
# ---------------------------------------------------------------------------
MPY_BOARD = r"""
import edge_ai, time
for m in edge_ai.models():
    print(m['index'], m['name'])           # โมเดลของเราโผล่เป็นชื่อใหม่ หา index ของมัน
edge_ai.select(N)                          # N = index ที่เจอ
time.sleep_ms(500)                         # ให้ NPU อนุมานสัก 1-2 window ก่อนอ่านผล
r = edge_ai.result()
print("บน NPU: label =", r['label'], "conf =", r['conf'], "latency =", r['latency_ms'], "ms")
# เอา r['latency_ms'] ไปเติมช่อง MCU:  python s14_tflite_board_full.py --mcu-ms <ค่านั้น>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="model_int8.tflite")
    ap.add_argument("--web", default="model_web.tflite")
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--mcu-ms", type=float, default=None,
                    help="ค่า edge_ai.latency() ที่อ่านจากบอร์ด (มิลลิวินาที)")
    ap.add_argument("--no-vela", action="store_true", help="ข้ามขั้น Vela")
    ap.add_argument("--show-mpy", action="store_true", help="พิมพ์ MPY สำหรับอ่าน latency บนบอร์ด")
    a = ap.parse_args()

    if a.show_mpy:
        print(MPY_BOARD)
        return

    Xte, yte, z = load_test_set(a.data, a.model)

    pc_acc, pc_ms = bench_int8(a.model, Xte, yte, z)
    print("PC int8:  accuracy = %.3f   latency = %.2f ms/window  (บน %d window)"
          % (pc_acc, pc_ms, len(Xte)))

    web = None
    if os.path.exists(a.web):
        web = bench_web(a.web, Xte, yte, z)
        print("Web float: accuracy = %.3f   latency = %.2f ms/window  (เส้นทางเบราว์เซอร์)"
              % (web[0], web[1]))
    else:
        print("ยังไม่มี", a.web, "— ข้ามการ bench เส้นทาง Web (สร้างด้วย convert_web.py จาก บทเรียน 5.6–5.7 ได้)")

    if not a.no_vela:
        vela = run_vela(a.model)
        if vela:
            print("Vela เขียน:", vela, "— MCU-only (มี ethos-u custom op) พร้อม wrap เป็น AIM_*")

    print_table(pc_acc, pc_ms, web, a.mcu_ms)
    print()
    print("ขั้นต่อไป (สู่บอร์ดจริง — MVP ของบทเรียน 5.8–5.9):")
    print(" 1) wrap output/*_vela.tflite เป็น AIM_GESTURE_* ตาม ai_models/README.md ของ SDK (3 edits)")
    print(" 2) rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo แล้ว hard power-cycle")
    print(" 3) บนบอร์ดรัน MPY นี้ (--show-mpy) อ่าน edge_ai.latency() มาเติมช่อง MCU")
    print("    เมื่อโมเดลของเราโผล่ใน edge_ai.models() และให้ verdict บน NPU = MVP ของบทเรียน 5.8–5.9 สำเร็จ")


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
