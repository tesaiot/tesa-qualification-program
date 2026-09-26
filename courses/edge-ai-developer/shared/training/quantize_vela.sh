#!/usr/bin/env bash
# Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.
# This is the ONE target that needs an extra step beyond the plain .tflite —
# Vela replaces NPU-eligible subgraphs with an "ethos-u" custom op (the browser
# and Cortex-A cannot run that op, which is why they use the plain file instead).
#
#   ./quantize_vela.sh model_int8.tflite   ->  ./output/model_int8_vela.tflite
set -euo pipefail

MODEL="${1:-model_int8.tflite}"
[ -f "$MODEL" ] || { echo "no such file: $MODEL (run train.py first)"; exit 1; }

# ethos-u-vela is installed in the training Docker image.
vela --accelerator-config ethos-u55-128 --optimise Performance "$MODEL"

echo
echo "Vela output in ./output/ :"
ls -1 output/ 2>/dev/null || true
echo
echo "Next: wrap output/*_vela.tflite in the AIM_* contract and add it as a model"
echo "      (see proj_cm55/modules/ai_models/README.md in tesaiot/tesaiot-pse84-devkit-sdk)."
echo "Note: this _vela.tflite is MCU-only. Keep the plain model_int8.tflite for"
echo "      the browser (convert_web.py) and Cortex-A (eval_pc.py)."

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
