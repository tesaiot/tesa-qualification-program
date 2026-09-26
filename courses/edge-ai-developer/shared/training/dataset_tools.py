"""Dataset tools for the IMU gesture classifier (Pillar 4 / Training).

A dataset is a CSV captured on the board (see m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py):
    label,ax,ay,az,gx,gy,gz
one row per IMU sample at ~50 Hz. We turn that stream of samples into fixed
windows the model can learn from — the SAME windowing the on-device feed does,
so the model you train sees the same shape the board will feed it.

    load_csv        -> (samples[N,6], labels[N])
    make_windows    -> (X[W, win, 6], y[W])   overlapping windows
    normalize       -> per-channel standardization (fit on train only)
    split           -> train / val / test, stratified
    synthesize      -> generate a fake dataset so the pipeline runs before you
                       have real board data (idle=still, circle=rotating,
                       shaking=high-variance)

Run standalone to create a synthetic CSV:
    python dataset_tools.py --synthesize --out data/gestures.csv
"""
import argparse
import csv
import math
import os

import numpy as np

CLASSES = ["idle", "circle", "shaking"]      # matches the board's Motion model
CHANNELS = ["ax", "ay", "az", "gx", "gy", "gz"]
WIN = 50          # 1 s at 50 Hz — the window the model classifies
HOP = 25          # 50% overlap between windows


def load_csv(path):
    """Read a board CSV into (samples[N,6] float32, labels[N] int)."""
    xs, ys = [], []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            ys.append(CLASSES.index(row["label"]))
            xs.append([float(row[c]) for c in CHANNELS])
    return np.asarray(xs, dtype=np.float32), np.asarray(ys, dtype=np.int64)


def make_windows(samples, labels, win=WIN, hop=HOP):
    """Slice the sample stream into overlapping windows. A window's label is the
    majority label of its samples (windows should sit inside one gesture)."""
    X, y = [], []
    for start in range(0, len(samples) - win + 1, hop):
        seg = samples[start:start + win]
        lab = labels[start:start + win]
        X.append(seg)
        y.append(np.bincount(lab, minlength=len(CLASSES)).argmax())
    return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=np.int64)


def normalize(X_train, *others):
    """Per-channel standardize. Fit mean/std on TRAIN ONLY, apply to all — a
    core rule: never let val/test statistics leak into training."""
    mean = X_train.reshape(-1, X_train.shape[-1]).mean(0)
    std = X_train.reshape(-1, X_train.shape[-1]).std(0) + 1e-6
    norm = lambda A: (A - mean) / std
    return (norm(X_train), *[norm(o) for o in others]), (mean, std)


def split(X, y, val=0.15, test=0.15, seed=0):
    """Stratified train/val/test split."""
    rng = np.random.default_rng(seed)
    idx = {c: rng.permutation(np.where(y == c)[0]) for c in np.unique(y)}
    tr, va, te = [], [], []
    for c, ii in idx.items():
        n = len(ii)
        nte, nva = int(n * test), int(n * val)
        te += list(ii[:nte]); va += list(ii[nte:nte + nva]); tr += list(ii[nte + nva:])
    rng.shuffle(tr); rng.shuffle(va); rng.shuffle(te)
    pick = lambda s: (X[s], y[s])
    return pick(np.array(tr)), pick(np.array(va)), pick(np.array(te))


def synthesize(path, per_class=1200, seed=0):
    """Fabricate a believable IMU stream so students can run the whole pipeline
    before they have captured real data on the board. Real capture replaces this."""
    rng = np.random.default_rng(seed)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["label"] + CHANNELS)
        for label in CLASSES:
            t = 0.0
            for _ in range(per_class):
                if label == "idle":                       # near gravity, tiny noise
                    ax, ay, az = rng.normal([0, 0, 9.81], 0.05)
                    gx, gy, gz = rng.normal(0, 0.5, 3)
                elif label == "circle":                   # smooth rotation
                    ax = 2.0 * math.sin(t); ay = 2.0 * math.cos(t); az = 9.81 + 0.3 * math.sin(2 * t)
                    gx, gy, gz = 40 * math.cos(t), 40 * math.sin(t), rng.normal(0, 2)
                else:                                       # shaking — high variance
                    ax, ay, az = rng.normal([0, 0, 9.81], 6.0)
                    gx, gy, gz = rng.normal(0, 150, 3)
                w.writerow([label] + [round(v, 4) for v in (ax, ay, az, gx, gy, gz)])
                t += 0.12
    print("wrote", path, "(%d samples/class)" % per_class)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthesize", action="store_true")
    ap.add_argument("--out", default="data/gestures.csv")
    a = ap.parse_args()
    if a.synthesize:
        synthesize(a.out)
    else:
        s, l = load_csv(a.out)
        X, y = make_windows(s, l)
        print("samples", s.shape, "windows", X.shape, "class counts", np.bincount(y))

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
