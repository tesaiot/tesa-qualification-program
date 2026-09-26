"""Prepare the trained model for the browser (BENTO Edge AI Emulator / any web page).

The web runtime we standardize on is LiteRT.js (loads .tflite directly via
WASM/WebGPU). One nuance from our research: LiteRT.js bounds the model's I/O
tensors to float32/int32, so a *full-integer* int8 model (int8 in/out, built for
the MCU) may need a float-I/O variant for the browser. This script produces that
variant from the SAME Keras training, so the web model provably comes from the
same weights as the MCU model.

    python convert_web.py --keras model.keras  --out model_web.tflite
    # (or, if you only kept the int8 file, re-run train.py once keeping model.keras)

Deploy: drop model_web.tflite next to the emulator and load it with
    import {loadLiteRt, loadAndCompile} from '@litertjs/core'
    await loadLiteRt('.../wasm/'); const m = await loadAndCompile('model_web.tflite', {accelerator:'webgpu'});
Then reproduce the SAME feature front-end + normalization in JS before m.run()
(lessons 5.6-5.7). Validate the browser verdict against eval_pc.py
on a shared test set — parity is a lab, not an assumption.
"""
import argparse

import numpy as np
import tensorflow as tf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keras", default="model.keras",
                    help="the float Keras model saved by train.py (--save-keras)")
    ap.add_argument("--out", default="model_web.tflite")
    ap.add_argument("--dynamic-int8", action="store_true",
                    help="weight-only int8 (smaller download, float32 I/O — browser-safe)")
    a = ap.parse_args()

    model = tf.keras.models.load_model(a.keras)
    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    if a.dynamic_int8:
        # dynamic-range: int8 weights, float32 activations/IO — fits LiteRT.js's
        # float32/int32 I/O constraint while still ~4x smaller than pure float.
        conv.optimizations = [tf.lite.Optimize.DEFAULT]
    # else: plain float32 — largest but always works in every browser runtime.
    tflite = conv.convert()
    with open(a.out, "wb") as f:
        f.write(tflite)
    print("wrote", a.out, "(%d bytes)" % len(tflite))
    print("This file is browser-clean (no ethos-u custom op) and also runs on")
    print("Cortex-A. The MCU keeps the Vela-compiled int8 variant.")


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
