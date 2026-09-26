# s14_tflite_board.py - quantize -> Vela -> รันบน NPU แล้วเทียบสามเป้าหมาย (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดเทอร์มินัลใน shared/training/ (ที่มี dataset_tools.py,
#             model_int8.tflite และ quantize_vela.sh อยู่) — สคริปต์นี้พึ่งสามไฟล์นั้น
#          2) ติดตั้ง runtime:  pip install ai-edge-litert numpy   (หรือรันใน Docker
#             image เดียวกับบทเรียน 5.3–5.5 ก็ได้ ไลบรารีครบ + มี vela ให้อยู่แล้ว)
#          3) เติมช่องว่างทั้ง 5 จุดตามคำใบ้ `# เติม:` ให้ครบ
#          4) รัน  python s14_tflite_board.py  แล้วดูตารางเทียบ MCU / Web / PC
#          5) รัน Vela + wrap + flash ลงบอร์ด แล้วอ่าน edge_ai.latency() มาเติมช่อง MCU
#             ในตาราง — นั่นคือ MVP ของบทเรียน 5.8–5.9: โมเดลของเรารันบน NPU จริง เทียบสามเป้าหมายได้
#
# เรื่องของชุดบทเรียนนี้: โมเดล int8 .tflite ไฟล์เดียวที่เราเทรน (บทเรียน 5.3–5.5) และทวน parity บน Web (บทเรียน 5.6–5.7)
# เหลืออีกหนึ่งเป้าหมายที่ต้อง "ขั้นพิเศษ" — MCU + Ethos-U55 NPU. ทั้งเบราว์เซอร์และ
# Cortex-A ใช้ไฟล์ .tflite ตรงๆ ได้ แต่ NPU อ่านกราฟธรรมดาไม่ออก ต้องให้ Vela คอมไพล์
# แทน subgraph ที่ NPU ทำได้ด้วย custom op "ethos-u" ก่อน. งานวันนี้จึงมีสองส่วน:
# (1) quantize->Vela ให้ได้ไฟล์ที่บอร์ดรันได้, (2) เทียบสามเป้าหมายด้วยเลขจริง —
# accuracy ต้องตรง (int8 คือคณิตเดียวกัน) แต่ latency/power ต่างกันคนละโลก

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
    เลข accuracy ชุดนี้คือ ground truth ที่ NPU ต้องได้ตรงกัน เพราะ Vela ไม่แก้คณิต
    ของโมเดล มันแค่ย้ายงานคูณเมทริกซ์จาก CPU ไป NPU — คำตอบเท่าเดิม แต่เร็ว/ประหยัดกว่า.
    X รูปร่าง [N, WIN, 6] (ยังไม่ normalize — เรา normalize ข้างในให้ตรงกับตอนเทรน)"""
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]          # โมเดล MCU เป็น full-integer int8 in/out
    out_scale, out_zero = out["quantization"]

    correct = 0
    total_ms = 0.0
    for i in range(len(X)):
        # เติม 1: normalize window ด้วย mean/std ชุดเดียวกับตอนเทรน (parity front-end) — ถ้า
        #         normalize คนละแบบ โมเดลเห็นข้อมูลคนละอย่าง accuracy จะเพี้ยนทันที
        #         แทนบรรทัดนี้ด้วย:  x = (X[i:i + 1] - z["mean"]) / z["std"]
        x = X[i:i + 1]

        # เติม 2: quantize float -> int8 ด้วย scale/zero ของ input tensor เอง (อ่านมาจากโมเดล
        #         ไม่ใช่เดา) — NPU รับ int8 ล้วน ขั้นนี้จึงต้องเป๊ะเหมือนบนบอร์ด
        #         แทนด้วย:  q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)
        q = np.zeros(inp["shape"], dtype=np.int8)

        it.set_tensor(inp["index"], q)
        # เติม 3: จับเวลาเฉพาะช่วง invoke() แล้วบวกสะสมลงใน total_ms (หน่วยมิลลิวินาที) — เรา
        #         วัด "เวลาอนุมานล้วน" ไม่รวม normalize/quantize เพื่อเทียบกับ NPU ให้ยุติธรรม
        #         แทน pass ด้วยสามบรรทัด:
        #             t0 = time.perf_counter()
        #             it.invoke()
        #             total_ms += (time.perf_counter() - t0) * 1000.0
        pass
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale               # dequantize int8 -> float กลับมา

        # เติม 4: นับว่าคลาสที่ชนะ (argmax) ตรงกับคลาสจริง y[i] ไหม สะสมใน correct
        #         แทน pass ด้วย:  correct += int(o.argmax() == y[i])
        pass

    acc = correct / len(X)
    lat = total_ms / len(X)
    return acc, lat


def run_vela(int8_path):
    """เรียก quantize_vela.sh ให้ Vela คอมไพล์ int8 -> _vela.tflite สำหรับ Ethos-U55.
    Vela แทน subgraph ที่ NPU ทำได้ด้วย custom op "ethos-u" — ไฟล์ผลลัพธ์รันได้เฉพาะ MCU
    (เบราว์เซอร์/Cortex-A รันไม่ได้ ต้องใช้ไฟล์ int8 ธรรมดาแทน) คืน path ของไฟล์ _vela.tflite
    หรือ None ถ้าเครื่องนี้ยังไม่มี vela (มันอยู่ใน Docker image ของบทเรียน 5.3–5.5)"""
    try:
        # เติม 5: เรียกสคริปต์ ./quantize_vela.sh <int8_path> ด้วย subprocess (check=True เพื่อ
        #         โยน error ถ้า vela ล้มเหลว) — นี่คือ "ขั้นพิเศษ" ขั้นเดียวที่ MCU ต้องมี
        #         แทน pass ด้วย:  subprocess.run(["./quantize_vela.sh", int8_path], check=True)
        pass
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ยังไม่มี vela ในเครื่องนี้ (อยู่ใน Docker image ของ บทเรียน 5.3–5.5) — ข้ามขั้น Vela ไปก่อนได้")
        return None

    base = os.path.splitext(os.path.basename(int8_path))[0]
    out = os.path.join("output", base + "_vela.tflite")
    return out if os.path.exists(out) else None


def load_test_set(data_path, model_path):
    """หยิบชุดทดสอบ (Xte, yte) ด้วย split ชุดเดียวกับ eval_pc + โหลด mean/std (z) — ยังไม่
    normalize ที่นี่ เพราะ bench_int8 จะ normalize ข้างในเองให้ตรงกับตอนเทรน"""
    if not os.path.exists(data_path):
        dt.synthesize(data_path)
    samples, labels = dt.load_csv(data_path)
    X, y = dt.make_windows(samples, labels)
    _, _, (Xte, yte) = dt.split(X, y)
    z = np.load(model_path + ".norm.npz")
    return Xte, yte, z


def print_table(pc_acc, pc_ms, mcu_ms):
    """เทียบสามเป้าหมายด้วยเลขจริง. accuracy ของ MCU = accuracy int8 บน PC เป๊ะ (Vela ไม่
    แก้คณิต) latency คนละเรื่อง: NPU ออกแบบมาคูณเมทริกซ์โดยเฉพาะ มักเร็วกว่า CPU หลายเท่า
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
# edge_ai.models() เอง จากนั้นอ่าน latency บน NPU ได้แบบเดียวกับโมเดลอื่น นี่คือรอยต่อ
# Python (ฝึกบน PC) -> MPY (รันจริงบนบอร์ด) ที่ชุดบทเรียนนี้พาข้าม
# ---------------------------------------------------------------------------
MPY_BOARD = r"""
import edge_ai, time
# โมเดลของเราถูก wrap เป็น AIM_GESTURE_* แล้ว appear เป็นชื่อใหม่ใน models()
for m in edge_ai.models():
    print(m['index'], m['name'])           # หา index ของโมเดลเรา
edge_ai.select(N)                          # N = index ที่เจอด้านบน
time.sleep_ms(500)
r = edge_ai.result()
print("บน NPU: label =", r['label'], "latency =", r['latency_ms'], "ms")
# เอา r['latency_ms'] นี้ไปเติมช่อง MCU ในตารางเทียบเป้าหมาย
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
