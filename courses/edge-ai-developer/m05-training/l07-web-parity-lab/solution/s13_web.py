# s13_web.py - เอาโมเดลของเราลง Web แล้วทวนผลให้ตรงกับ PC
# วิธีรัน: 1) เปิดเทอร์มินัลใน shared/training/ (ที่มี dataset_tools.py กับ
#             model_int8.tflite) แล้ว  pip install ai-edge-litert numpy
#          2) python s13_web.py   -> ได้ verdict ฝั่ง PC ที่เป็น ground truth
#          3) รัน window เดียวกันในเบราว์เซอร์ (LiteRT.js) แล้วเทียบให้ตรงภายใน TOL
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละที่สมองจะจำได้ว่า
# ทำไม parity ถึงพังง่ายตรง front-end ไม่ใช่ตรงตัวโมเดล ทั้งไฟล์ยืนอยู่บนความจริง
# ข้อเดียว: โมเดล .tflite ไฟล์เดียว รันได้หลายเป้าหมาย แต่คำตอบจะตรงกันก็ต่อเมื่อ
# เราเดินขั้นตอนก่อน/หลังกราฟให้เหมือนกันทุกเป้าหมาย

import argparse

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter      # LiteRT รุ่นต่อจาก tflite-runtime
except ImportError:                                          # ชื่อสำรอง ถ้ายังไม่ได้ลง ai-edge-litert
    from tensorflow.lite import Interpreter

import dataset_tools as dt

# เบราว์เซอร์ (XNNPACK) กับ PC/บอร์ด (CMSIS-NN) ไม่การันตีว่าจะได้เลขเป๊ะเท่ากันทุกบิต
# เราจึงตั้งเกณฑ์ยอมรับไว้เล็กน้อย ผ่านเมื่อคะแนนต่างกันไม่เกินนี้
TOL = 0.02


def web_verdict(model_path, window, z):
    """จำลองสิ่งที่เบราว์เซอร์ต้องทำก่อน m.run() ให้ครบทุกขั้น แล้วคืน verdict เป็น dict
    เลขชุดที่คืนออกไปนี้แหละคือ ground truth ที่ LiteRT.js ต้องผลิตให้ตรงกันภายใน TOL
    window รูปร่าง [1, WIN, 6] (หนึ่ง window ของ IMU 6 แกน)"""

    # ขั้นที่ 1 — normalization: ต้องเป็น mean/std ชุดเดียวกับตอนเทรนเป๊ะ นี่คือจุดที่
    # parity พังบ่อยที่สุด เพราะกราฟโมเดลไฟล์เดียวกัน แต่ถ้า front-end normalize คนละแบบ
    # โมเดลก็เห็นข้อมูลคนละอย่าง verdict เลยเพี้ยน — เราจึงเซฟ mean/std ไว้ตอน train.py
    x = (window - z["mean"]) / z["std"]

    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]      # โมเดล MCU เป็น full-integer int8 in/out
    out_scale, out_zero = out["quantization"]

    # ขั้นที่ 2 — quantize float -> int8 ด้วย scale/zero ของ input tensor เอง (อ่านมาจาก
    # โมเดล ไม่ใช่เดา) เบราว์เซอร์ที่ใช้ไฟล์ int8 ก็ต้องทำสูตรเดียวกันนี้
    q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)

    # ขั้นที่ 3 — ป้อนเข้าโมเดลแล้วอนุมาน (ตรงนี้แทบไม่มีอะไรต่างข้ามเป้าหมาย ตัวกราฟทำงานเอง)
    it.set_tensor(inp["index"], q)
    it.invoke()
    o = it.get_tensor(out["index"])[0].astype(np.float32)

    # ขั้นที่ 4 — dequantize int8 -> float กลับมา โมเดลมี softmax head ผลจึงเป็นความน่าจะเป็น
    # ที่รวมกันได้ ~1.0 พร้อมนำไปเทียบกับเบราว์เซอร์
    o = (o - out_zero) * out_scale

    top = int(o.argmax())
    conf = float(o[top])         # คะแนนของคลาสที่ชนะ = ตัวเลขที่เราจะใช้วัด parity
    return {"label": dt.CLASSES[top], "top": top, "conf": conf, "scores": o.tolist()}


def load_one_window(data_path):
    """หยิบ window ทดสอบมาหนึ่งอัน ใช้ split ชุดเดียวกับ eval_pc เพื่อให้เทียบตรงกันได้
    ถ้ายังไม่มี data/gestures.csv จะสร้างชุดสังเคราะห์ให้ pipeline เดินได้ก่อนมีข้อมูลจริง"""
    import os
    if not os.path.exists(data_path):
        dt.synthesize(data_path)
    samples, labels = dt.load_csv(data_path)
    X, y = dt.make_windows(samples, labels)
    _, _, (Xte, yte) = dt.split(X, y)
    return Xte[0:1], int(yte[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="model_int8.tflite")
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--index", type=int, default=0, help="เลือก window ทดสอบตัวที่เท่าไร")
    ap.add_argument("--show-js", action="store_true", help="พิมพ์โค้ด LiteRT.js สำหรับเบราว์เซอร์")
    a = ap.parse_args()

    if a.show_js:
        print(JS_LITERT)
        return

    z = np.load(a.model + ".norm.npz")          # mean/std ที่โมเดลถูกเทรนมาด้วย
    window, true_label = load_one_window(a.data)

    r = web_verdict(a.model, window, z)
    print("verdict ฝั่ง PC (ground truth ที่เบราว์เซอร์ต้องได้ตรงกัน):")
    print("  label = %-8s conf = %.4f  (คลาสจริง = %s)"
          % (r["label"], r["conf"], dt.CLASSES[true_label]))
    print("  scores =", ["%.4f" % s for s in r["scores"]])
    print()
    print("ไฟล์ .tflite ตัวเดียวกันนี้ยังรันได้บน Cortex-A (RPi/Jetson): คัดลอกไฟล์ไป")
    print("แล้วรัน eval_pc.py บนบอร์ดนั้นได้เลย ai-edge-litert ลงได้ทั้งสองที่ นี่คือ")
    print("ความหมายจริงของ train once, run everywhere")
    print()
    print("เอา window ตัวที่ %d ไปรันใน LiteRT.js บนหน้าเว็บ แล้วเทียบ:" % a.index)
    print("  ผ่าน parity เมื่อ  max|score_pc - score_web| <= TOL (%.2f)" % TOL)


# ---------------------------------------------------------------------------
# ฝั่ง JS — โหลดไฟล์เดียวกันในเบราว์เซอร์ด้วย LiteRT.js (python s13_web.py --show-js)
# สังเกตว่าเป็น 4 ขั้นเดียวกับ web_verdict() เป๊ะ ต่างแค่ภาษา — parity เริ่มจากตรงนี้
# ---------------------------------------------------------------------------
JS_LITERT = r"""
import {loadLiteRt, loadAndCompile} from '@litertjs/core';

await loadLiteRt('https://unpkg.com/@litertjs/core/dist/wasm/');
const model = await loadAndCompile('model_web.tflite', {accelerator: 'webgpu'});

function webVerdict(window, mean, std) {          // window: Float32Array ยาว WIN*6
  const x = window.map((v, i) => (v - mean[i % 6]) / std[i % 6]);   // (1) normalize ให้เหมือน PC
  const out = model.run([x]);                                       // (2)(3) LiteRT.js รับ float32 I/O
  const scores = out[0];                                            // (4) softmax อยู่ในกราฟแล้ว
  let top = 0;
  for (let i = 1; i < scores.length; i++) if (scores[i] > scores[top]) top = i;
  return {top, conf: scores[top], scores};
}
// LiteRT.js บังคับ I/O เป็น float32/int32 จึงใช้ model_web.tflite ที่ convert_web.py
// สร้าง (weight-only int8, float I/O) ไม่ใช่ไฟล์ int8 เต็มของ MCU — ไฟล์นี้ browser-clean
// ไม่มี ethos-u custom op จึงโหลดในเบราว์เซอร์ได้
"""


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
