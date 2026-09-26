# s14_tflite_board.py - quantize -> Vela -> รันบน NPU แล้วเทียบสามเป้าหมาย
# วิธีรัน: 1) เปิดเทอร์มินัลใน shared/training/ (มี dataset_tools.py, model_int8.tflite,
#             quantize_vela.sh) แล้ว  pip install ai-edge-litert numpy
#          2) python s14_tflite_board.py         -> bench int8 บน PC + รัน Vela + ตารางเทียบ
#          3) wrap _vela.tflite เป็น AIM_* แล้ว flash ลงบอร์ด อ่าน edge_ai.latency() มาเติม
#             ช่อง MCU:  python s14_tflite_board.py --mcu-ms <ค่าที่อ่านได้>
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละสมองจะจำได้ว่า Vela เป็น
# แค่ "ขั้นคอมไพล์เพิ่ม" ไม่ใช่การเทรนใหม่ — มันย้ายงานคูณเมทริกซ์ไป NPU โดยไม่แตะคณิต
# ทั้งไฟล์ยืนอยู่บนความจริงข้อเดียว: โมเดล int8 ไฟล์เดียว รันได้ทั้งสามเป้าหมาย accuracy
# ตรงกัน (เพราะกราฟเดียวกัน) แต่ latency/power ต่างกันคนละโลก — นั่นคือสิ่งที่เราวัดวันนี้

import argparse
import os
import subprocess
import time

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter      # LiteRT รุ่นต่อจาก tflite-runtime
except ImportError:                                          # ชื่อสำรอง ถ้ายังไม่ได้ลง ai-edge-litert
    from tensorflow.lite import Interpreter

import dataset_tools as dt


def bench_int8(model_path, X, y, z):
    """รันไฟล์ int8 เต็มบน PC วัดทั้งความแม่น (accuracy) และเวลาเฉลี่ยต่อ window (ms).
    เลข accuracy ชุดนี้คือ ground truth ที่ NPU ต้องได้ตรงกัน — Vela ไม่แก้คณิตของโมเดล
    มันแค่ย้ายงานคูณเมทริกซ์จาก CPU ไป NPU ให้เร็ว/ประหยัดกว่า คำตอบยังเท่าเดิมทุกบิตเชิงคลาส.
    X รูปร่าง [N, WIN, 6] (ยังไม่ normalize — เรา normalize ข้างในให้ตรงกับตอนเทรน)"""
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]          # โมเดล MCU เป็น full-integer int8 in/out
    out_scale, out_zero = out["quantization"]

    correct = 0
    total_ms = 0.0
    for i in range(len(X)):
        # ขั้นที่ 1 — normalize ด้วย mean/std ชุดเดียวกับตอนเทรน (parity front-end). ถ้าเป้าหมาย
        # ใด normalize คนละแบบ โมเดลจะเห็นข้อมูลคนละอย่าง accuracy เพี้ยนทันที แม้กราฟเดียวกัน
        x = (X[i:i + 1] - z["mean"]) / z["std"]

        # ขั้นที่ 2 — quantize float -> int8 ด้วย scale/zero ของ input tensor เอง (อ่านจากโมเดล
        # ไม่ใช่เดา) NPU รับ int8 ล้วน ขั้นนี้จึงต้องเป๊ะเหมือนที่ feed บนบอร์ดทำ
        q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)

        it.set_tensor(inp["index"], q)
        # ขั้นที่ 3 — จับเวลาเฉพาะช่วง invoke() ("เวลาอนุมานล้วน") ไม่รวม normalize/quantize
        # เพื่อเทียบกับ NPU ให้ยุติธรรม เพราะ edge_ai.latency() บนบอร์ดก็วัดเฉพาะช่วงนี้เช่นกัน
        t0 = time.perf_counter()
        it.invoke()
        total_ms += (time.perf_counter() - t0) * 1000.0

        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale               # dequantize int8 -> float กลับมา

        # ขั้นที่ 4 — คลาสที่ชนะ (argmax) ตรงกับคลาสจริงไหม สะสมไว้คำนวณ accuracy ทีเดียวตอนจบ
        correct += int(o.argmax() == y[i])

    acc = correct / len(X)
    lat = total_ms / len(X)
    return acc, lat


def run_vela(int8_path):
    """เรียก quantize_vela.sh ให้ Vela คอมไพล์ int8 -> _vela.tflite สำหรับ Ethos-U55.
    Vela แทน subgraph ที่ NPU ทำได้ด้วย custom op "ethos-u" — ไฟล์ผลลัพธ์รันได้เฉพาะ MCU
    (เบราว์เซอร์/Cortex-A รันไม่ได้ ต้องใช้ไฟล์ int8 ธรรมดาแทน) คืน path ของ _vela.tflite
    หรือ None ถ้าเครื่องนี้ยังไม่มี vela (มันอยู่ใน Docker image ของบทเรียน 5.3–5.5)"""
    try:
        # นี่คือ "ขั้นพิเศษ" ขั้นเดียวที่มีแค่ MCU ต้องทำ Web กับ Cortex-A ใช้ไฟล์ int8 เดิมได้เลย
        # check=True เพื่อให้ error ของ vela เด้งขึ้นมา ไม่กลืนเงียบ
        subprocess.run(["./quantize_vela.sh", int8_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ยังไม่มี vela ในเครื่องนี้ (อยู่ใน Docker image ของ บทเรียน 5.3–5.5) — ข้ามขั้น Vela ไปก่อนได้")
        return None

    base = os.path.splitext(os.path.basename(int8_path))[0]
    out = os.path.join("output", base + "_vela.tflite")
    return out if os.path.exists(out) else None


def load_test_set(data_path, model_path):
    """หยิบชุดทดสอบ (Xte, yte) ด้วย split ชุดเดียวกับ eval_pc + โหลด mean/std (z). ยังไม่
    normalize ที่นี่ เพราะ bench_int8 จะ normalize ข้างในเองให้ตรงกับตอนเทรน (ที่เดียว จุดเดียว)"""
    if not os.path.exists(data_path):
        dt.synthesize(data_path)
    samples, labels = dt.load_csv(data_path)
    X, y = dt.make_windows(samples, labels)
    _, _, (Xte, yte) = dt.split(X, y)
    z = np.load(model_path + ".norm.npz")
    return Xte, yte, z


def print_table(pc_acc, pc_ms, mcu_ms):
    """เทียบสามเป้าหมายด้วยเลขจริง. accuracy ของ MCU = accuracy int8 บน PC เป๊ะ เพราะ Vela
    ไม่แก้คณิต. latency คนละเรื่อง: NPU ออกแบบมาคูณเมทริกซ์โดยเฉพาะ มักเร็วกว่า CPU หลายเท่า
    ที่พลังงานต่อการอนุมานต่ำกว่ามาก. ช่อง MCU เติมได้เมื่อรันบนบอร์ดแล้วอ่าน edge_ai.latency()"""
    mcu_lat = "%.2f" % mcu_ms if mcu_ms is not None else "อ่านจากบอร์ด"
    print()
    print("เป้าหมาย   | ไฟล์ที่ใช้             | accuracy | latency/win | หมายเหตุ")
    print("-----------+-----------------------+----------+-------------+---------------------------")
    print("PC/Docker  | model_int8.tflite     |  %.3f   |  %8.2f ms | ground truth (int8, CPU)"
          % (pc_acc, pc_ms))
    print("MCU + NPU  | model_int8_vela.tflite|  %.3f   |  %8s ms | Vela + Ethos-U55 (edge_ai)"
          % (pc_acc, mcu_lat))
    print("Web        | model_web.tflite      |  ~%.3f  |   (เบราว์เซอร์)| float I/O, ไม่มี ethos-u op"
          % pc_acc)
    print()
    print("อ่าน: accuracy ตรงกันทั้งสามเพราะเป็น int8 กราฟเดียวกัน (Web ต่างเล็กน้อยที่ front-end)")
    print("      latency ต่างกันคนละโลก — นั่นคือเหตุผลที่เราเลือกเป้าหมายตามงาน ไม่ใช่ตามความเท่")


# ---------------------------------------------------------------------------
# ฝั่ง MicroPython — โมเดลที่ wrap แล้ว (ผ่าน AIM_* contract, ai_models/README.md ของ SDK) จะโผล่ใน
# edge_ai.models() เองโดยไม่ต้องแตะ MicroPython หรือ IPC เลย เพราะทะเบียนโมเดลเป็น shape-driven
# จากนั้นอ่าน latency บน NPU ได้แบบเดียวกับโมเดลอื่น — นี่คือรอยต่อ Python (ฝึกบน PC) -> MPY
# (รันจริงบนบอร์ด) ที่ชุดบทเรียนนี้พาข้าม: เลข latency ในตารางฝั่ง MCU มาจาก r['latency_ms'] ตรงนี้
# ---------------------------------------------------------------------------
MPY_BOARD = r"""
import edge_ai, time
for m in edge_ai.models():
    print(m['index'], m['name'])           # โมเดลของเราโผล่เป็นชื่อใหม่ หา index ของมัน
edge_ai.select(N)                          # N = index ที่เจอด้านบน
time.sleep_ms(500)                         # ให้ NPU อนุมานสัก 1-2 window ก่อนอ่านผล
r = edge_ai.result()
print("บน NPU: label =", r['label'], "latency =", r['latency_ms'], "ms")
# เอา r['latency_ms'] ไปเติมช่อง MCU:  python s14_tflite_board.py --mcu-ms <ค่านั้น>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="model_int8.tflite")
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--mcu-ms", type=float, default=None,
                    help="ค่า edge_ai.latency() ที่อ่านมาจากบอร์ด (มิลลิวินาที)")
    ap.add_argument("--no-vela", action="store_true", help="ข้ามขั้น Vela (แค่ bench + เทียบ)")
    a = ap.parse_args()

    Xte, yte, z = load_test_set(a.data, a.model)
    pc_acc, pc_ms = bench_int8(a.model, Xte, yte, z)
    print("PC int8:  accuracy = %.3f   latency = %.2f ms/window  (บน %d window)"
          % (pc_acc, pc_ms, len(Xte)))

    if not a.no_vela:
        vela = run_vela(a.model)
        if vela:
            print("Vela เขียน:", vela, "— MCU-only (มี ethos-u custom op) พร้อม wrap เป็น AIM_*")

    print_table(pc_acc, pc_ms, a.mcu_ms)
    print()
    print("ขั้นต่อไป: wrap _vela.tflite เป็น AIM_GESTURE_* (ai_models/README.md ของ SDK) แล้ว flash")
    print("จากนั้นบนบอร์ดรัน MPY สั้นๆ นี้เพื่ออ่าน latency จริงบน NPU:")
    print(MPY_BOARD)


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
