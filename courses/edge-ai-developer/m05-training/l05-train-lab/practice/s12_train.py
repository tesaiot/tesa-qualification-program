# s12_train.py - ฝึกโมเดลของเราเองด้วย TensorFlow แล้วทดสอบบน PC (ฉบับฝึกเติมโค้ด)
# วิธีรัน (บน PC ผ่าน Docker — ไม่ต้องลง TensorFlow ลงเครื่องเอง):
#   1) วางไฟล์นี้ไว้ในโฟลเดอร์ shared/training/ (ข้างๆ dataset_tools.py, Dockerfile)
#   2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#   3) build อิมเมจครั้งเดียว:  docker build -t edgeai-train .
#   4) รัน:  docker run --rm -v "$PWD":/work edgeai-train python s12_train.py
#   5) อ่านผล: float32 accuracy -> int8 accuracy -> confusion matrix บนหน้าจอ
#
# ชุดบทเรียนนี้เราเลิก "ยืมโมเดลสำเร็จรูป" แล้วมาฝึกของเราเอง โจทย์คือท่ามือ 3 คลาส
# (idle / circle / shaking) ตัวเดียวกับที่โมเดล Motion บนบอร์ดทำ dataset มาจาก
# gestures.csv ที่เราเก็บบนบอร์ดตั้งแต่ บทเรียน 5.1–5.2 งานของเราชุดบทเรียนนี้คือเติม 4 จังหวะหลัก
# ของการฝึก: สร้างโมเดล -> ฝึก -> บีบเป็น int8 -> ทดสอบบน PC
#
# ส่วนที่ยุ่งเรื่องอ่าน CSV / ตัดหน้าต่าง / แบ่ง train-val-test เราให้ dataset_tools
# (ของ บทเรียน 5.1–5.2) จัดการให้แล้ว เหมือนที่บทเรียน 1.1–1.3 เราให้ edge_ai.models() มาฟรีๆ

import argparse

import numpy as np
import tensorflow as tf

import dataset_tools as dt      # ของ บทเรียน 5.1–5.2: load_csv / make_windows / normalize / split


def build_model(win, chans, n_classes):
    """โมเดล 1-D CNN ขนาดเล็ก — รูปทรงที่พอดีกับ NPU บนไมโครคอนโทรลเลอร์
    Conv1D ไล่ตามแกนเวลา -> pooling -> dense head ทุก op เป็นมิตรกับ Ethos-U55"""
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
    """บีบโมเดลเป็น int8 แบบ full-integer (int8 เข้า int8 ออก) — คอนฟิกที่ NPU
    Ethos-U55 บังคับ ส่วนเป้าหมายอื่น (Web / Cortex-A) ก็รับ int8 ได้เหมือนกัน"""

    def representative():
        # ป้อนตัวอย่างจริงจากชุดฝึกให้ converter ดู "ช่วงค่า" ของ activation
        # แล้วเลือกสเกล int8 ที่เหมาะ — เรียกว่า calibration
        for i in range(min(200, len(X_repr))):
            yield [X_repr[i:i + 1].astype(np.float32)]

    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]

    # ----- เติมช่องที่ 2 -----
    # เติม: ป้อน representative dataset ให้ converter ใช้ calibrate ช่วงค่า
    #       -> conv.representative_dataset = representative
    pass

    conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

    # ----- เติมช่องที่ 3 -----
    # เติม: บังคับให้ทั้ง input และ output เป็น int8 (สัญญาที่ NPU ต้องการ)
    #       -> conv.inference_input_type = tf.int8
    #          conv.inference_output_type = tf.int8
    pass

    tflite = conv.convert()
    with open(out_path, "wb") as f:
        f.write(tflite)
    print("wrote", out_path, "(%d bytes)" % len(tflite))


def eval_int8(out_path, Xte, yte):
    """รันไฟล์ .tflite บน PC ผ่าน ai-edge-litert แล้ววัดความแม่น + confusion matrix
    นี่คือ ground truth: ไฟล์เดียวกันนี้จะไปรันบนบอร์ดและในเบราว์เซอร์ต่อ"""
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
        # แปลง float -> int8 ด้วยสเกล/zero-point ของ input (quantize)
        q = np.clip(np.round(Xte[i:i + 1] / in_scale + in_zero), -128, 127).astype(np.int8)
        it.set_tensor(inp["index"], q)
        it.invoke()
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale                  # int8 -> float (dequantize)
        preds.append(int(o.argmax()))
    preds = np.asarray(preds)

    # ----- เติมช่องที่ 4 -----
    # เติม: คำนวณความแม่นบนชุดทดสอบ (สัดส่วนที่ทายถูก)
    #       -> acc = (preds == yte).mean()
    acc = 0.0
    pass
    print("int8 test accuracy: %.3f" % acc)

    print("\nconfusion (rows=true, cols=pred):", dt.CLASSES)
    cm = np.zeros((len(dt.CLASSES), len(dt.CLASSES)), int)
    for t, p in zip(yte, preds):
        cm[t, p] += 1
    for i, row in enumerate(cm):
        print("  %-8s %s" % (dt.CLASSES[i], row))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/gestures.csv")
    ap.add_argument("--out", default="model_int8.tflite")
    ap.add_argument("--epochs", type=int, default=25)
    a = ap.parse_args()

    # dataset_tools ของ บทเรียน 5.1–5.2 อ่าน CSV -> ตัดหน้าต่าง -> แบ่ง train/val/test ให้เรา
    samples, labels = dt.load_csv(a.data)
    X, y = dt.make_windows(samples, labels)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = dt.split(X, y)
    # normalize: หา mean/std จาก "ชุดฝึกเท่านั้น" แล้วเอาไปใช้กับทุกชุด
    (Xtr, Xva, Xte), (mean, std) = dt.normalize(Xtr, Xva, Xte)
    print("train/val/test windows:", len(Xtr), len(Xva), len(Xte))

    model = build_model(dt.WIN, len(dt.CHANNELS), len(dt.CLASSES))
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # ----- เติมช่องที่ 1 -----
    # เติม: ฝึกโมเดลด้วยชุดฝึก และตรวจกับชุด val ทุก epoch
    #       -> model.fit(Xtr, ytr, validation_data=(Xva, yva),
    #                    epochs=a.epochs, batch_size=32, verbose=2)
    pass

    _, acc = model.evaluate(Xte, yte, verbose=0)
    print("float32 test accuracy: %.3f" % acc)

    # บีบเป็น int8 โดย calibrate จากหน้าต่างชุดฝึกจริง
    to_int8_tflite(model, Xtr, a.out)
    # เก็บ mean/std ไว้ ให้ฝั่งบอร์ด/เบราว์เซอร์ normalize ด้วยค่าเดียวกับตอนฝึก
    # (ถ้าลืม จะเป็นจุดพังเงียบๆ ที่หายากมาก)
    np.savez(a.out + ".norm.npz", mean=mean, std=std)
    print("saved normalization to", a.out + ".norm.npz")

    # ทดสอบไฟล์ int8 บน PC — ต้องได้ความแม่นใกล้ float32
    eval_int8(a.out, Xte, yte)
    print("\nNext: convert_web.py (Web) · quantize_vela.sh (MCU)")


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
