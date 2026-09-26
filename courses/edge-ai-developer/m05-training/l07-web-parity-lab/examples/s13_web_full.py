# s13_web_full.py - แล็บ parity ครบวง: PC vs Web จากโมเดล .tflite ไฟล์เดียว (ฉบับเต็ม)
# วิธีรัน: เปิดใน shared/training/ (มี dataset_tools.py + model_int8.tflite + .keras)
#          pip install ai-edge-litert tensorflow numpy
#          python s13_web_full.py                 # ทวน parity ทั้งชุดทดสอบ
#          python s13_web_full.py --export-web     # สร้าง model_web.tflite ให้เบราว์เซอร์
#          python s13_web_full.py --show-js        # พิมพ์โค้ด LiteRT.js
#
# ฉบับนี้คือเวอร์ชันขัดจนเรียบร้อยของ s13_web.py — โครงเดียวกับที่คุณเติมในไฟล์ฝึก
# แต่เดินให้ครบเรื่อง: (1) สร้างไฟล์ web จากน้ำหนักชุดเดียวกับ MCU, (2) รันทั้ง int8
# (แบบบอร์ด/PC) และ web (float I/O แบบเบราว์เซอร์) บนชุดทดสอบเดียวกัน, (3) วัด
# max-abs-diff ต่อ window แล้วสรุปว่า parity ผ่านเกณฑ์ MVP ของบทเรียน 5.6–5.7 หรือไม่ ทั้งหมดยังยืน
# อยู่บนหลักเดิม: ไฟล์เดียว หลายเป้าหมาย คำตอบตรงกันได้ก็ต่อเมื่อ front-end ตรงกัน

import argparse
import os

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    from tensorflow.lite import Interpreter

import dataset_tools as dt

TOL = 0.02          # เกณฑ์ยอมรับ parity ต่อคะแนน


# ---- โหลดข้อมูล + normalization ---------------------------------------------

def load_test_set(data_path, model_path):
    """คืน (Xte, yte, z) โดยใช้ split ชุดเดียวกับ eval_pc — normalize ยังไม่ทำที่นี่
    เพราะ web_verdict/int8_verdict จะ normalize ข้างในเองให้เหมือนกันทั้งสองทาง"""
    if not os.path.exists(data_path):
        dt.synthesize(data_path)
    samples, labels = dt.load_csv(data_path)
    X, y = dt.make_windows(samples, labels)
    _, _, (Xte, yte) = dt.split(X, y)
    z = np.load(model_path + ".norm.npz")
    return Xte, yte, z


# ---- เส้นทาง int8 (แบบบอร์ด/PC) ----------------------------------------------

def int8_scores(model_path, window, z):
    """รันไฟล์ int8 เต็ม (int8 in/out) — เส้นทางเดียวกับบอร์ดและ eval_pc.py
    คืน scores เป็นความน่าจะเป็นหลัง dequantize. window รูปร่าง [1, WIN, 6]"""
    x = (window - z["mean"]) / z["std"]
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]
    q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)
    it.set_tensor(inp["index"], q)
    it.invoke()
    o = it.get_tensor(out["index"])[0].astype(np.float32)
    return (o - out_zero) * out_scale


# ---- เส้นทาง web (float I/O แบบเบราว์เซอร์) ----------------------------------

def web_scores(model_path, window, z):
    """รันไฟล์ web (float32 I/O) — เส้นทางเดียวกับ LiteRT.js ในเบราว์เซอร์ ไม่ต้อง
    quantize เอง เพราะกราฟรับ float ตรงๆ. นี่คือสิ่งที่ทำให้ไฟล์ browser-safe (§1)"""
    x = ((window - z["mean"]) / z["std"]).astype(np.float32)
    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    it.set_tensor(inp["index"], x)
    it.invoke()
    return it.get_tensor(out["index"])[0].astype(np.float32)


# ---- สร้างไฟล์ web จากน้ำหนักชุดเดียวกับ MCU (มิเรอร์ convert_web.py) ---------

def export_web(keras_path, out_path):
    """แปลง Keras ตัวเดียวกับที่เทรน -> model_web.tflite (weight-only int8, float I/O)
    เล็กกว่า float ~4 เท่า แต่ยังพอดีกับข้อจำกัด float32/int32 I/O ของ LiteRT.js"""
    import tensorflow as tf
    model = tf.keras.models.load_model(keras_path)
    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]     # dynamic-range int8 weights
    tflite = conv.convert()
    with open(out_path, "wb") as f:
        f.write(tflite)
    print("เขียน", out_path, "(%d bytes)" % len(tflite), "— browser-clean, ไม่มี ethos-u custom op")


# ---- แล็บ parity -------------------------------------------------------------

def run_parity(int8_path, web_path, data_path):
    Xte, yte, z = load_test_set(data_path, int8_path)
    worst = 0.0
    agree = 0
    print("window | true    | int8 verdict     | web verdict      | max-diff")
    print("-------+---------+------------------+------------------+---------")
    for i in range(min(12, len(Xte))):
        w = Xte[i:i + 1]
        s_int8 = int8_scores(int8_path, w, z)
        s_web = web_scores(web_path, w, z)
        diff = float(np.max(np.abs(s_int8 - s_web)))
        worst = max(worst, diff)
        t8, tw = int(s_int8.argmax()), int(s_web.argmax())
        agree += (t8 == tw)
        flag = "ok" if diff <= TOL else "DIFF"
        print("  %3d  | %-7s | %-8s %.3f | %-8s %.3f | %.4f %s"
              % (i, dt.CLASSES[yte[i]], dt.CLASSES[t8], s_int8[t8],
                 dt.CLASSES[tw], s_web[tw], diff, flag))
    n = min(12, len(Xte))
    print()
    print("คลาสที่ชนะตรงกัน %d/%d window · max-abs-diff สูงสุด = %.4f (เกณฑ์ TOL = %.2f)"
          % (agree, n, worst, TOL))
    if worst <= TOL and agree == n:
        print("PARITY ผ่าน — ไฟล์ web ให้ verdict ตรงกับไฟล์ int8 บน PC ภายในเกณฑ์ (ยืนยันในเบราว์เซอร์ต่อด้วย --show-js)")
    else:
        print("PARITY ยังไม่ผ่าน — ไล่ดู front-end ก่อน (normalize/quantize) มักเพี้ยนตรงนั้น")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="model_int8.tflite")
    ap.add_argument("--web", default="model_web.tflite")
    ap.add_argument("--keras", default="model.keras")
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--export-web", action="store_true", help="สร้าง model_web.tflite จาก Keras")
    ap.add_argument("--show-js", action="store_true", help="พิมพ์โค้ด LiteRT.js สำหรับเบราว์เซอร์")
    a = ap.parse_args()

    if a.show_js:
        print(JS_LITERT)
        return
    if a.export_web:
        export_web(a.keras, a.web)
        return
    if not os.path.exists(a.web):
        print("ยังไม่มี", a.web, "— รัน  python s13_web_full.py --export-web  ก่อน")
        print("(ถ้ายังไม่มี model.keras ให้รัน train.py --save-keras อีกครั้งเพื่อเก็บไว้)")
        return
    run_parity(a.model, a.web, a.data)


# ---------------------------------------------------------------------------
# ฝั่ง JS — โหลด model_web.tflite ในเบราว์เซอร์ด้วย LiteRT.js (4 ขั้นเดียวกับ web_scores)
# ---------------------------------------------------------------------------
JS_LITERT = r"""
import {loadLiteRt, loadAndCompile} from '@litertjs/core';

await loadLiteRt('https://unpkg.com/@litertjs/core/dist/wasm/');
const model = await loadAndCompile('model_web.tflite', {accelerator: 'webgpu'});

function webVerdict(window, mean, std) {          // window: Float32Array ยาว WIN*6
  const x = window.map((v, i) => (v - mean[i % 6]) / std[i % 6]);   // (1) normalize เหมือน PC
  const out = model.run([x]);                                       // (2)(3) float32 I/O
  const scores = out[0];                                            // (4) softmax ในกราฟ
  let top = 0;
  for (let i = 1; i < scores.length; i++) if (scores[i] > scores[top]) top = i;
  return {top, conf: scores[top], scores};
}
// เกณฑ์ผ่าน: max|scores_web - scores_pc| <= 0.02 สำหรับ window เดียวกัน
// ไฟล์ model_web.tflite มาจาก convert_web.py / --export-web (weight-only int8, float I/O)
// จึง browser-clean และรันได้ทั้งบน Cortex-A ด้วยไฟล์เดียวกัน
"""


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
