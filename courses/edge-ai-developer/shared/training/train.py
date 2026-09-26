"""Train a tiny IMU gesture classifier and export it as int8 TFLite.

This is the heart of Pillar 4: your OWN model, trained on YOUR data, exported to
the one artifact (model_int8.tflite) that then deploys to the MCU, the browser,
and a Cortex-A board. Small on purpose — a Conv1D that fits an Ethos-U55.

    python train.py --data data/gestures.csv --out model_int8.tflite

Why int8 full-integer quantization: the Ethos-U55 NPU only accelerates quantized
ops, and int8 also works fine in the browser and on Cortex-A. So int8 is the
common denominator across every target. We supply a representative dataset so the
converter can calibrate the activation ranges.
"""
import argparse

import numpy as np
import tensorflow as tf

import dataset_tools as dt


def build_model(win, chans, n_classes):
    """A small 1-D CNN — the kind of shape that fits a microcontroller NPU.
    Conv1D over time, global pooling, one dense head. All ops are Ethos-U friendly."""
    return tf.keras.Sequential([
        tf.keras.layers.Input(shape=(win, chans)),
        tf.keras.layers.Conv1D(16, 5, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling1D(2),
        tf.keras.layers.Conv1D(32, 3, padding="same", activation="relu"),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(n_classes, activation="softmax"),
    ])


def to_int8_tflite(model, X_repr, out_path):
    """Full-integer post-training quantization. int8 in, int8 out — the config
    the MCU/Ethos-U55 requires (and the others accept)."""
    def representative():
        for i in range(min(200, len(X_repr))):
            yield [X_repr[i:i + 1].astype(np.float32)]

    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]
    conv.representative_dataset = representative
    conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    conv.inference_input_type = tf.int8
    conv.inference_output_type = tf.int8
    tflite = conv.convert()
    with open(out_path, "wb") as f:
        f.write(tflite)
    print("wrote", out_path, "(%d bytes)" % len(tflite))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--out", default="model_int8.tflite")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--save-keras", action="store_true",
                    help="also save the float Keras model as model.keras (convert_web.py reads it)")
    a = ap.parse_args()

    samples, labels = dt.load_csv(a.data)
    X, y = dt.make_windows(samples, labels)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = dt.split(X, y)
    (Xtr, Xva, Xte), (mean, std) = dt.normalize(Xtr, Xva, Xte)
    print("train/val/test windows:", len(Xtr), len(Xva), len(Xte))

    model = build_model(dt.WIN, len(dt.CHANNELS), len(dt.CLASSES))
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(Xtr, ytr, validation_data=(Xva, yva),
              epochs=a.epochs, batch_size=32, verbose=2)

    _, acc = model.evaluate(Xte, yte, verbose=0)
    print("float32 test accuracy: %.3f" % acc)

    # Export int8 — calibrate on real training windows.
    to_int8_tflite(model, Xtr, a.out)
    # Save the normalization so the board/browser front-end applies the SAME
    # mean/std the model was trained with (a common silent-failure point).
    np.savez(a.out + ".norm.npz", mean=mean, std=std)
    print("saved normalization to", a.out + ".norm.npz")
    if a.save_keras:
        model.save("model.keras")
        print("saved the float Keras model to model.keras")
    print("\nNext: eval_pc.py (PC) · quantize_vela.sh (MCU) · convert_web.py (Web)")


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
