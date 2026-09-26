# Training — train once, run everywhere (module 5)

This is where the course stops *consuming* models and starts *making* them. You
collect a dataset on the board, train a model on your PC in Docker, and deploy
the **same** model to four targets: the MCU (Cortex-M55 + Ethos-U55), the PC, the
web browser, and a Cortex-A Linux board.

## The one artifact, four targets

```
                    train.py  (Keras, in Docker)
                        │
                        ▼
              model_int8.tflite   ← the "train once" artifact
                        │
        ┌───────────────┼───────────────┬────────────────┐
        ▼               ▼               ▼                ▼
  quantize_vela.sh   eval_pc.py    convert_web.py   (same file)
  → *_vela.tflite    ai-edge-litert  → browser        ai-edge-litert
  MCU / Ethos-U55    PC / Docker      LiteRT.js/ORT    Cortex-A (RPi/Jetson)
```

Only the MCU needs the extra **Vela** compile; the browser and Cortex-A reuse the
plain `model_int8.tflite`. int8 is the common denominator (the NPU requires it;
the others accept it). Lessons 5.3 and 5.8 walk through the full matrix.

## Files

| File | What it does | Where it runs |
|---|---|---|
| `Dockerfile` | reproducible TensorFlow env (works on macOS/Win/Linux) | PC |
| `dataset_tools.py` | load / window / normalize / split an IMU CSV dataset | PC |
| `train.py` | train a small Conv1D gesture classifier, export **int8** `.tflite` | PC (Docker) |
| `eval_pc.py` | run the `.tflite` on PC via `ai-edge-litert`, print accuracy + confusion | PC |
| `quantize_vela.sh` | compile `model_int8.tflite` → `_vela.tflite` for the Ethos-U55 | PC → MCU |
| `convert_web.py` | make a browser-friendly variant + notes for LiteRT.js/ORT-Web | PC → Web |

The dataset is IMU 6-axis windows labelled `idle / circle / shaking` — the same
problem the board's built-in **Motion** model solves, so you can compare *your*
model against the shipped one.

## Quick start (Docker)

```bash
# 1. build the training image (once)
docker build -t edgeai-train .

# 2. train (expects data/gestures.csv captured on the board in lesson 5.2)
docker run --rm -v "$PWD":/work edgeai-train python train.py \
    --data data/gestures.csv --out model_int8.tflite

# 3. check it on the PC
docker run --rm -v "$PWD":/work edgeai-train python eval_pc.py \
    --model model_int8.tflite --data data/gestures.csv

# 4a. MCU:   ./quantize_vela.sh model_int8.tflite       -> model_int8_vela.tflite
# 4b. Web:   docker run ... python convert_web.py model_int8.tflite
# 4c. Cortex-A: copy model_int8.tflite to the Pi/Jetson and run eval_pc.py there
```

`data/gestures.csv` is produced on the board by `s04_daq_logger.py` (lesson 2.2) or
`s11_dataset.py` (lesson 5.2). A tiny synthetic generator is included in
`dataset_tools.py` (`--synthesize`) so the pipeline runs before you have real data.

<!--
SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
SPDX-License-Identifier: MIT
-->
