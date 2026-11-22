#!/usr/bin/env bash
# One-time setup of a fresh workspace for Swirlverse runs (about 1-2 minutes).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
pip install --break-system-packages -q kokoro-onnx soundfile pycairo numpy scipy pillow 2>&1 | grep -v -i warning || true
mkdir -p ~/.fonts && cp "$HERE"/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
mkdir -p ~/.swirl_models
[ -s ~/.swirl_models/kokoro-v1.0.int8.onnx ] || curl -sSL -o ~/.swirl_models/kokoro-v1.0.int8.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s ~/.swirl_models/voices-v1.0.bin ] || curl -sSL -o ~/.swirl_models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
which ffmpeg >/dev/null || (apt-get install -y -q ffmpeg >/dev/null 2>&1 || true)
python3 -c "import cairo, kokoro_onnx, soundfile, scipy, PIL; print('swirlverse setup OK')"
fc-list | grep -qi "Luckiest" && fc-list | grep -qi "Fredoka" && echo "fonts OK"
