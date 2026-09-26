# s12_train.py - ฝึกโมเดลของเราเองด้วย TensorFlow แล้วทดสอบบน PC
# วิธีรัน (บน PC ผ่าน Docker):
#   1) วางไฟล์นี้ไว้ในโฟลเดอร์ shared/training/ (ข้างๆ dataset_tools.py, Dockerfile)
#   2) docker build -t edgeai-train .
#   3) docker run --rm -v "$PWD":/work edgeai-train python s12_train.py
#   4) ดู float32 accuracy -> int8 accuracy -> confusion matrix บนหน้าจอ
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละสมองจะจำ 4 จังหวะ
# ของการฝึกได้: สร้างโมเดล (build) -> ฝึก (fit) -> บีบ int8 (convert) -> ทดสอบ (eval)
#
# จุดที่คนพลาดกันบ่อยไม่ใช่ตอนฝึก แต่เป็นตอนบีบ int8 กับตอนทดสอบ — สองจังหวะนั้น
# แหละคือของจริงของ Edge AI เพราะโมเดลที่ฝึกมาสวยแต่ int8 แล้วแม่นตกฮวบ ก็เอาลง
# บอร์ดไม่ได้ ส่วนที่ยุ่งเรื่อง CSV / หน้าต่าง / แบ่งชุด เรายืม dataset_tools ของ บทเรียน 5.1–5.2

import argparse

import numpy as np
import tensorflow as tf

import dataset_tools as dt      # ของ บทเรียน 5.1–5.2: load_csv / make_windows / normalize / split


def build_model(win, chans, n_classes):
    """โมเดล 1-D CNN ขนาดเล็ก — ตั้งใจให้เล็กพอจะรันบน NPU ของไมโครคอนโทรลเลอร์
    Conv1D กวาดไปตามแกนเวลา จับ "รูปร่างของการเคลื่อนไหว" ในหน้าต่าง 1 วินาที
    GlobalAveragePooling ยุบเวลาให้เหลือเวกเตอร์เดียว แล้ว dense head ตัดสินคลาส
    ทุก layer ที่เลือกไว้เป็น op ที่ Ethos-U55 เร่งได้ (นี่คือเหตุผลที่โมเดลต้องเล็ก)"""
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
    """บีบโมเดลเป็น int8 แบบ full-integer (int8 เข้า int8 ออก) นี่คือคอนฟิกที่
    Ethos-U55 บังคับ และเป้าหมายอื่น (Web / Cortex-A) ก็รับได้หมด int8 จึงเป็น
    'ตัวหารร่วม' ของทุกเป้าหมาย — บีบครั้งเดียว เอาไปได้ทั่วสเปกตรัม"""

    def representative():
        # หัวใจของ int8: converter ต้องรู้ว่า activation จริงๆ มีค่าอยู่ในช่วงไหน
        # ถึงจะเลือกสเกลได้เหมาะ เราจึง "ป้อนตัวอย่างจริง" จากชุดฝึกให้มันดู 200 อัน
        # เรียกจังหวะนี้ว่า calibration — ถ้าไม่ผูก convert() จะหยุดด้วย ValueError ถ้าป้อนตัวอย่างไม่เหมือนจริง สเกลจะเพี้ยน ความแม่นตก
        for i in range(min(200, len(X_repr))):
            yield [X_repr[i:i + 1].astype(np.float32)]

    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]
    # จังหวะที่สอง: ผูก representative dataset เข้ากับ converter
    conv.representative_dataset = representative
    conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    # จังหวะที่สาม: บังคับ int8 ทั้งขาเข้าและขาออก NPU อ่าน float ไม่ได้เลย
    # ต้องเป็น int8 ล้วน — ตรงนี้แหละที่แยก "โมเดลรันบนชิปได้จริง" ออกจากโมเดล PC
    conv.inference_input_type = tf.int8
    conv.inference_output_type = tf.int8
    tflite = conv.convert()
    with open(out_path, "wb") as f:
        f.write(tflite)
    print("wrote", out_path, "(%d bytes)" % len(tflite))


def eval_int8(out_path, Xte, yte):
    """รันไฟล์ .tflite บน PC ผ่าน ai-edge-litert แล้ววัดความแม่น + confusion matrix
    ไฟล์เดียวกันนี้จะไปรันบนบอร์ด (หลัง Vela) และในเบราว์เซอร์ต่อ — รันบน PC ก่อน
    คือ ground truth ที่เราเชื่อได้ ถ้า int8 บน PC แม่น บนบอร์ดก็ควรแม่นตาม"""
    try:
        from ai_edge_litert.interpreter import Interpreter      # LiteRT ตัวใหม่
    except ImportError:
        from tensorflow.lite import Interpreter                 # ชื่อเดิม (สำรอง)

    it = Interpreter(model_path=out_path)
    it.allocate_tensors()
    inp, out = it.get_input_details()[0], it.get_output_details()[0]
    in_scale, in_zero = inp["quantization"]
    out_scale, out_zero = out["quantization"]

    preds = []
    for i in range(len(Xte)):
        # โมเดลรับ int8 เราจึงต้องแปลง float -> int8 ด้วยสเกล/zero-point ของ input
        q = np.clip(np.round(Xte[i:i + 1] / in_scale + in_zero), -128, 127).astype(np.int8)
        it.set_tensor(inp["index"], q)
        it.invoke()
        o = it.get_tensor(out["index"])[0].astype(np.float32)
        o = (o - out_zero) * out_scale                  # int8 -> float (dequantize)
        preds.append(int(o.argmax()))
    preds = np.asarray(preds)

    # ความแม่น = สัดส่วนหน้าต่างที่ทายถูกในชุดทดสอบ (ชุดที่โมเดลไม่เคยเห็นตอนฝึก)
    acc = (preds == yte).mean()
    print("int8 test accuracy: %.3f" % acc)

    # confusion matrix: แถว = คลาสจริง คอลัมน์ = คลาสที่โมเดลทาย เลขนอกแนวทแยง
    # คือความผิดพลาด บอกเราว่าโมเดลสับสนคู่ไหนกับคู่ไหน (บทเรียน false pos/neg)
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

    # dataset_tools ของ บทเรียน 5.1–5.2 ทำงานหนักเรื่องข้อมูลให้เรา: อ่าน CSV -> ตัดหน้าต่าง
    # ทับเหลื่อม -> แบ่ง train/val/test แบบ stratified (แต่ละคลาสกระจายครบทุกชุด)
    samples, labels = dt.load_csv(a.data)
    X, y = dt.make_windows(samples, labels)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = dt.split(X, y)
    # normalize: หา mean/std จาก "ชุดฝึกเท่านั้น" แล้วเอาไปใช้กับ val/test ด้วย
    # ห้ามให้สถิติของ val/test รั่วเข้ามาตอนฝึก ไม่งั้นตัวเลขจะสวยเกินจริง
    (Xtr, Xva, Xte), (mean, std) = dt.normalize(Xtr, Xva, Xte)
    print("train/val/test windows:", len(Xtr), len(Xva), len(Xte))

    model = build_model(dt.WIN, len(dt.CHANNELS), len(dt.CLASSES))
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    # จังหวะแรก: ฝึก ดู accuracy ของ train เทียบกับ val ทุก epoch ถ้า train พุ่ง
    # แต่ val ไม่ตาม แปลว่าเริ่ม overfit (จำข้อสอบ ไม่ได้เข้าใจ)
    model.fit(Xtr, ytr, validation_data=(Xva, yva),
              epochs=a.epochs, batch_size=32, verbose=2)

    _, acc = model.evaluate(Xte, yte, verbose=0)
    print("float32 test accuracy: %.3f" % acc)

    # บีบเป็น int8 โดย calibrate จากหน้าต่างชุดฝึกจริง แล้วเซฟไฟล์ .tflite
    to_int8_tflite(model, Xtr, a.out)
    # เก็บ mean/std ไว้คู่กับโมเดล ฝั่งบอร์ด/เบราว์เซอร์ต้อง normalize ด้วยค่าเดียวกัน
    # นี่คือจุดพังเงียบที่พบบ่อยสุด: โมเดลถูก แต่ front-end ใช้ mean/std คนละชุด
    np.savez(a.out + ".norm.npz", mean=mean, std=std)
    print("saved normalization to", a.out + ".norm.npz")

    # ทดสอบไฟล์ int8 บน PC เทียบกับ float32 ควรใกล้กัน ถ้าตกเยอะแปลว่า calibration
    # ยังไม่ดีพอ หรือโมเดลไวต่อ quantization
    eval_int8(a.out, Xte, yte)
    print("\nNext: convert_web.py (Web) · quantize_vela.sh (MCU)")


if __name__ == "__main__":
    main()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
