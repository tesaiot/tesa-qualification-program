# s12_train_full.py - ฝึก + ทดสอบโมเดลท่ามือ แบบครบวงจร (ฉบับเต็ม)
#
# ต่อยอดจาก s12_train.py: เพิ่มของที่ทำให้ "รันจริง" ลื่นขึ้น
#   - ถ้าไม่มี data/gestures.csv ให้สร้างชุดสังเคราะห์ให้อัตโนมัติ (pipeline รันได้เลย)
#   - พิมพ์สรุปโมเดล + จำนวนพารามิเตอร์ (โมเดลเล็กแค่ไหนถึงลงบอร์ดได้)
#   - เทียบ float32 vs int8 ตรงๆ แล้วเตือนถ้า int8 แม่นตกเกินเกณฑ์
#   - เกต MVP ของบทเรียน 5.3–5.5: ผ่านเมื่อ int8 accuracy >= เกณฑ์ที่ตั้งไว้ (คืน exit code)
#
# วิธีรัน (Docker):
#   docker build -t edgeai-train .
#   docker run --rm -v "$PWD":/work edgeai-train python s12_train_full.py
#   (วางไฟล์นี้ไว้ใน shared/training/ ข้างๆ dataset_tools.py)
#
# แนวคิดหลักไม่เปลี่ยนจากฉบับฝึก: สร้าง -> ฝึก -> บีบ int8 -> ทดสอบบน PC
# ไฟล์ .tflite ที่ได้คือ "หนึ่งชิ้นงาน" ที่เอาไปได้ทั้ง MCU / Web / Cortex-A

import argparse
import os
import sys

import numpy as np
import tensorflow as tf

import dataset_tools as dt

# เส้นแบ่ง MVP: int8 บน PC ต้องแม่นอย่างน้อยเท่านี้ถึงถือว่าโมเดลพร้อมไปต่อ
MVP_MIN_ACC = 0.80
# ยอมให้ int8 แม่นตกจาก float32 ได้ไม่เกินเท่านี้ (เกินแปลว่า quantization มีปัญหา)
INT8_DROP_WARN = 0.05


def build_model(win, chans, n_classes):
    """1-D CNN เล็กๆ ที่ทุก op เป็นมิตรกับ Ethos-U55 — เล็กเพื่อให้ลงชิปได้ แต่ยัง
    พอจับรูปร่างของท่ามือในหน้าต่าง 1 วินาทีได้ครบสามคลาส"""
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
    """Full-integer int8 (int8 เข้า int8 ออก) — คอนฟิกที่ NPU บังคับ และเป้าหมาย
    อื่นรับได้หมด int8 คือตัวหารร่วมของทุกเป้าหมาย"""

    def representative():
        for i in range(min(200, len(X_repr))):
            yield [X_repr[i:i + 1].astype(np.float32)]

    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]
    conv.representative_dataset = representative        # calibrate ช่วงค่า
    conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    conv.inference_input_type = tf.int8                 # NPU อ่าน int8 เท่านั้น
    conv.inference_output_type = tf.int8
    tflite = conv.convert()
    with open(out_path, "wb") as f:
        f.write(tflite)
    print("wrote %s (%d bytes)" % (out_path, len(tflite)))
    return len(tflite)


def eval_int8(out_path, Xte, yte):
    """รัน .tflite บน PC ผ่าน ai-edge-litert คืน (accuracy, confusion matrix)"""
    try:
        from ai_edge_litert.interpreter import Interpreter
    except ImportError:
        from tensorflow.lite import Interpreter

    it = Interpreter(model_path=out_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]

    preds = []
    for i in range(len(Xte)):
        q = np.clip(np.round(Xte[i:i + 1] / in_scale + in_zero), -128, 127).astype(np.int8)
        it.set_tensor(inp["index"], q)
        it.invoke()
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale                  # dequantize
        preds.append(int(o.argmax()))
    preds = np.asarray(preds)

    acc = (preds == yte).mean()
    cm = np.zeros((len(dt.CLASSES), len(dt.CLASSES)), int)
    for t, p in zip(yte, preds):
        cm[t, p] += 1
    return acc, cm


def print_confusion(cm):
    print("\nconfusion (rows=true, cols=pred):", dt.CLASSES)
    for i, row in enumerate(cm):
        print("  %-8s %s" % (dt.CLASSES[i], row))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--out", default="model_int8.tflite")
    ap.add_argument("--epochs", type=int, default=25)
    a = ap.parse_args()

    # ถ้ายังไม่มี dataset (เช่นยังไม่ได้เก็บบนบอร์ดใน บทเรียน 5.1–5.2) สร้างชุดสังเคราะห์ให้
    # pipeline จะได้รันได้ตั้งแต่ต้น แล้วค่อยเอา CSV จริงมาแทนทีหลัง
    if not os.path.exists(a.data):
        print("no dataset at %s — synthesizing one so the pipeline runs" % a.data)
        dt.synthesize(a.data)

    samples, labels = dt.load_csv(a.data)
    X, y = dt.make_windows(samples, labels)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = dt.split(X, y)
    (Xtr, Xva, Xte), (mean, std) = dt.normalize(Xtr, Xva, Xte)
    print("train/val/test windows: %d / %d / %d" % (len(Xtr), len(Xva), len(Xte)))
    print("classes:", dt.CLASSES, "| window:", dt.WIN, "| channels:", len(dt.CHANNELS))

    model = build_model(dt.WIN, len(dt.CHANNELS), len(dt.CLASSES))
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    print("trainable params: %d (เล็กพอจะลง NPU ได้)" % model.count_params())

    model.fit(Xtr, ytr, validation_data=(Xva, yva),
              epochs=a.epochs, batch_size=32, verbose=2)

    _, f32_acc = model.evaluate(Xte, yte, verbose=0)
    print("\nfloat32 test accuracy: %.3f" % f32_acc)

    nbytes = to_int8_tflite(model, Xtr, a.out)
    np.savez(a.out + ".norm.npz", mean=mean, std=std)
    print("saved normalization to %s" % (a.out + ".norm.npz"))

    int8_acc, cm = eval_int8(a.out, Xte, yte)
    print("int8 test accuracy:    %.3f" % int8_acc)
    print_confusion(cm)

    # รายงานสรุป: เทียบ float32 vs int8 + เกต MVP
    drop = f32_acc - int8_acc
    print("\n--- summary ---")
    print("float32 -> int8 accuracy drop: %.3f" % drop)
    print("model size on disk: %.1f KB" % (nbytes / 1024.0))
    if drop > INT8_DROP_WARN:
        print("WARN: int8 แม่นตกเกิน %.2f — ลองเพิ่ม epoch หรือตรวจ representative set"
              % INT8_DROP_WARN)

    passed = int8_acc >= MVP_MIN_ACC
    print("MVP ของบทเรียน 5.3–5.5: %s (int8 accuracy %.3f, เกณฑ์ >= %.2f)"
          % ("PASS" if passed else "NOT YET", int8_acc, MVP_MIN_ACC))
    print("\nNext: convert_web.py (Web) · quantize_vela.sh (MCU)")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
