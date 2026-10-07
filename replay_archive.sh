#!/bin/sh
# Replay every recorded check of this archive (MIT). Set PY to the interpreter (default: python3).
set -eu
cd "$(dirname "$0")"
PY="${PY:-python3}"
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
"$PY" test_transport.py
"$PY" -O test_transport.py
"$PY" transport_cli.py examples/tilt.json --check examples/tilt.result.json
"$PY" transport_cli.py examples/uncertainty.json --check examples/uncertainty.result.json
"$PY" transport_cli.py examples/refine.json --check examples/refine.result.json
"$PY" benchmark.py --check
"$PY" verify_manifest.py
echo "REPLAY OK"
