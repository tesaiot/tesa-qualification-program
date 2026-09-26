# s13_web.py - เอาโมเดลของเราลง Web แล้วทวนผลให้ตรงกับ PC (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดเทอร์มินัลใน shared/training/ (ที่มี dataset_tools.py กับ
#             model_int8.tflite อยู่) — สคริปต์นี้พึ่งสองไฟล์นั้น
#          2) ติดตั้ง runtime:  pip install ai-edge-litert numpy   (หรือรันใน Docker
#             image เดียวกับบทเรียน 5.3–5.5 ก็ได้ ไลบรารีครบอยู่แล้ว)
#          3) เติมช่องว่างทั้ง 5 จุดตามคำใบ้ `# เติม:` ให้ครบ
#          4) รัน  python s13_web.py  แล้วดู "verdict ฝั่ง PC" ที่พิมพ์ออกมา
#          5) เอา window เดียวกันไปรันในเบราว์เซอร์ (หน้าเว็บที่โหลด LiteRT.js)
#             แล้วเทียบว่า conf/label ตรงกันภายในเกณฑ์ TOL หรือไม่ — นั่นคือ MVP ของบทเรียน 5.6–5.7
#
# เรื่องของชุดบทเรียนนี้: โมเดล .tflite ตัวเดียวที่เราเทรนใน บทเรียน 5.3–5.5 ไม่ได้รันแค่บนบอร์ด มัน
# รันได้ทั้งในเบราว์เซอร์ (ผ่าน LiteRT.js) และบน Cortex-A Linux (RPi/Jetson ผ่าน
# ai-edge-litert) ด้วยไฟล์เดียวกัน แต่ "รันได้" กับ "ได้คำตอบตรงกัน" เป็นคนละเรื่อง
# หัวใจของงานวันนี้จึงเป็น parity: ทำ verdict ฝั่ง PC ให้เป็น ground truth ก่อน แล้ว
# ค่อยพิสูจน์ว่าเบราว์เซอร์ได้ตรงกัน. parity คือการทดลองในแล็บ ไม่ใช่ข้อสมมติ

import argparse

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter      # LiteRT รุ่นต่อจาก tflite-runtime
except ImportError:                                          # ชื่อสำรอง ถ้ายังไม่ได้ลง ai-edge-litert
    from tensorflow.lite import Interpreter

import dataset_tools as dt

# เกณฑ์ยอมรับ parity: เบราว์เซอร์ (XNNPACK) กับ PC ไม่จำเป็นต้อง bit-exact กัน — เรายอม
# ให้ conf ต่างกันได้เล็กน้อย ผ่านเมื่อ max-abs-diff <= TOL
TOL = 0.02


def web_verdict(model_path, window, z):
    """ทำหน้าที่เดียวกับที่เบราว์เซอร์ต้องทำก่อน m.run(): front-end + quantize + อนุมาน
    + dequantize คืน verdict เป็น dict {label, top, conf, scores} — เลขชุดนี้คือสิ่งที่
    LiteRT.js ในเบราว์เซอร์ต้องผลิตให้ตรงกันภายใน TOL. window รูปร่าง [1, WIN, 6]."""

    # เติม 1: ทำ normalization ชุดเดียวกับตอนเทรน (mean/std จากไฟล์ .norm.npz) — นี่คือ
    #         หัวใจของ parity: ถ้า front-end ฝั่ง PC กับเบราว์เซอร์ normalize ไม่เหมือนกัน
    #         verdict จะเพี้ยนทันที แม้จะเป็นโมเดลไฟล์เดียวกัน
    #         แทนบรรทัดนี้ด้วย:  x = (window - z["mean"]) / z["std"]
    x = window

    it = Interpreter(model_path=model_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]

    # เติม 2: quantize float -> int8 ด้วย scale/zero ของ input tensor (โมเดล MCU เป็น
    #         full-integer int8 in/out) — เบราว์เซอร์ที่ใช้ไฟล์ int8 ก็ต้องทำขั้นนี้เป๊ะ
    #         แทนด้วย:  q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)
    q = np.zeros(inp["shape"], dtype=np.int8)

    # เติม 3: ป้อน q เข้าโมเดลแล้วสั่งอนุมาน
    #         แทน pass ด้วยสองบรรทัด:  it.set_tensor(inp["index"], q)  แล้ว  it.invoke()
    pass
    o = it.get_tensor(out["index"])[0].astype(np.float32)

    # เติม 4: dequantize output int8 -> float — โมเดลมี softmax head ผลจึงเป็นความน่าจะเป็น
    #         แทนด้วย:  o = (o - out_zero) * out_scale
    o = o

    top = int(o.argmax())
    # เติม 5: conf = คะแนนของคลาสที่ชนะ (เลขตัวนี้แหละที่เบราว์เซอร์ต้องได้ตรงกันภายใน TOL)
    #         แทนด้วย:  conf = float(o[top])
    conf = 0.0

    return {"label": dt.CLASSES[top], "top": top, "conf": conf, "scores": o.tolist()}


def load_one_window(data_path):
    """หยิบ window ทดสอบมาหนึ่งอัน (ใช้ split ชุดเดิมกับ eval_pc เพื่อให้เทียบกันได้)
    ถ้ายังไม่มี data/gestures.csv จะสร้างชุดสังเคราะห์ให้ pipeline เดินได้ก่อน"""
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
    a = ap.parse_args()

    z = np.load(a.model + ".norm.npz")          # mean/std ที่โมเดลถูกเทรนมาด้วย
    window, true_label = load_one_window(a.data)

    r = web_verdict(a.model, window, z)
    print("verdict ฝั่ง PC (ground truth ที่เบราว์เซอร์ต้องได้ตรงกัน):")
    print("  label = %-8s conf = %.4f  (คลาสจริง = %s)"
          % (r["label"], r["conf"], dt.CLASSES[true_label]))
    print("  scores =", ["%.4f" % s for s in r["scores"]])
    print()
    print("เอา window ตัวที่ %d นี้ไปรันใน LiteRT.js บนหน้าเว็บ แล้วเทียบ:" % a.index)
    print("  ผ่าน parity เมื่อ  max|score_pc - score_web| <= TOL (%.2f)" % TOL)


# ---------------------------------------------------------------------------
# ฝั่ง JS — โค้ดที่โหลดไฟล์เดียวกันนี้ในเบราว์เซอร์ด้วย LiteRT.js
# (ก๊อปไปวางในหน้าเว็บของคุณ ฉบับเฉลยและฉบับเต็มพิมพ์ออกมาให้ด้วย --show-js)
# ---------------------------------------------------------------------------
JS_LITERT = r"""
// เบราว์เซอร์ทำ 4 ขั้นเดียวกับ web_verdict() ข้างบนเป๊ะ ต่างแค่ภาษา
import {loadLiteRt, loadAndCompile} from '@litertjs/core';

await loadLiteRt('https://unpkg.com/@litertjs/core/dist/wasm/');
const model = await loadAndCompile('model_web.tflite', {accelerator: 'webgpu'});

function webVerdict(window, mean, std) {          // window: Float32Array [WIN*6]
  const x = window.map((v, i) => (v - mean[i % 6]) / std[i % 6]);   // (1) normalize เหมือนกัน
  const out = model.run([x]);                                       // (2)(3) LiteRT.js รับ float32 I/O
  const scores = out[0];                                            // (4) softmax แล้วในกราฟ
  let top = 0;
  for (let i = 1; i < scores.length; i++) if (scores[i] > scores[top]) top = i;
  return {top, conf: scores[top], scores};
}
// หมายเหตุ: LiteRT.js บังคับ I/O เป็น float32/int32 จึงใช้ไฟล์ model_web.tflite ที่
// convert_web.py สร้าง (weight-only int8, float I/O) ไม่ใช่ไฟล์ int8 เต็มของ MCU
// ไฟล์นี้ browser-clean (ไม่มี ethos-u custom op)
"""


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
