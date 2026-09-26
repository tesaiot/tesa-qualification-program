"""Run the exported int8 .tflite on the PC and report accuracy + confusion.

This is the SAME .tflite that will run on the board and in the browser — running
it here first is your ground truth. On a Cortex-A board (RPi/Jetson) this exact
script runs unchanged (ai-edge-litert installs there too), which is the whole
"train once, run everywhere" point.

    python eval_pc.py --model model_int8.tflite --data data/gestures.csv
"""
import argparse

import numpy as np

try:
    from ai_edge_litert.interpreter import Interpreter      # the LiteRT successor
except ImportError:                                          # fallback name
    from tensorflow.lite import Interpreter

import dataset_tools as dt


def quantize_input(x, scale, zero):
    return np.clip(np.round(x / scale + zero), -128, 127).astype(np.int8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="model_int8.tflite")
    ap.add_argument("--data", default="data/gestures.csv")
    a = ap.parse_args()

    samples, labels = dt.load_csv(a.data)
    X, y = dt.make_windows(samples, labels)
    (Xtr, _), _, (Xte, yte) = dt.split(X, y)
    # apply the SAME normalization the model trained with
    z = np.load(a.model + ".norm.npz")
    Xte = (Xte - z["mean"]) / z["std"]

    it = Interpreter(model_path=a.model)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]

    preds = []
    for i in range(len(Xte)):
        q = quantize_input(Xte[i:i + 1], in_scale, in_zero)
        it.set_tensor(inp["index"], q)
        it.invoke()
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale                       # dequantize
        preds.append(int(o.argmax()))
    preds = np.asarray(preds)

    acc = (preds == yte).mean()
    print("int8 test accuracy: %.3f" % acc)
    print("\nconfusion (rows=true, cols=pred):", dt.CLASSES)
    cm = np.zeros((len(dt.CLASSES), len(dt.CLASSES)), int)
    for t, p in zip(yte, preds):
        cm[t, p] += 1
    for i, row in enumerate(cm):
        print("  %-8s %s" % (dt.CLASSES[i], row))
    # A little false-positive/negative literacy (the S-analysis lessons pay off here).


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
