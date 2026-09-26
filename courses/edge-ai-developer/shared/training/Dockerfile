# Reproducible TensorFlow training environment for the Edge AI course.
# Works the same on macOS / Windows / Linux — this is why we train in Docker
# instead of the vendor GUI (which does not run on macOS).
FROM python:3.11-slim

WORKDIR /work

# TensorFlow for training + conversion; ai-edge-litert for on-PC .tflite inference
# (the successor to tflite-runtime). We use the plain `tensorflow` package (not
# `tensorflow-cpu`) because it publishes wheels for linux/arm64 (Apple-Silicon
# Docker) as well as x86 — `tensorflow-cpu` has no arm64 wheel.
RUN pip install --no-cache-dir \
        "tensorflow" \
        "ai-edge-litert" \
        "numpy" "scikit-learn"

# ethos-u-vela (MCU compile step, quantize_vela.sh) in its own layer so a version
# conflict with TF never blocks training; it is a standalone CLI (no TF import).
RUN pip install --no-cache-dir "ethos-u-vela" || \
    echo "WARN: ethos-u-vela not installed here — run quantize_vela.sh where vela is available"

# Source is bind-mounted at run time: docker run -v "$PWD":/work ...
CMD ["python", "--version"]

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
