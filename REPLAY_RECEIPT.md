# Replay receipt

Version `0.2.0-candidate`, dated 2026-10-07. Interpreter: CPython 3.14.7 (`/opt/homebrew/opt/python@3.14/bin/python3.14`) on macOS 27.0, Apple M2, standard library only, with `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1`.

**What is replayed.** `replay_archive.sh` runs, in order:

| Command | Expected output |
|---|---|
| `test_transport.py` | 14 test methods pass: 45 tilt cases, 24 generic two-algorithm cases, 32 sampled realisations, 169 grid points, 408 adverse-family grid evaluations, 108 tightness cases |
| `-O test_transport.py` | the same suite in optimised mode (no reliance on removable assertions) |
| `transport_cli.py examples/tilt.json --check examples/tilt.result.json` | exact recomputation of $F=13/192$, $W_2^2=1/192$, overlap matrix and masses |
| `transport_cli.py examples/uncertainty.json --check examples/uncertainty.result.json` | envelope $25/192$, baseline, 16 regions |
| `transport_cli.py examples/refine.json --check examples/refine.result.json` | envelope 4, interval $[41943/16777216,\ 88641311/35316039680]$, attaining coefficients, 151 sub-boxes |
| `benchmark.py --check` | all 65 recorded exact fields (bounds, regions, boxes, refusal, stop reason) recomputed and equal; timing and memory not compared |
| `verify_manifest.py` | every shipped file matches `MANIFEST.sha256` |

**Two replays are recorded.**
1. *Producer replay of the frozen files*, performed on the staged tree immediately before the manifest and archive were written: [evidence/replay.json](evidence/replay.json) holds the exact commands, exit codes, outputs, durations and the SHA-256 of every input file.
2. *Fresh-extraction replay of the final archive*: the archive was extracted into a new directory and `replay_archive.sh` run there, followed by a negative control (an altered recorded result must be rejected). Its receipt binds the archive's own SHA-256 and therefore cannot live inside the archive; it is published as the release asset `planar-transport-map-sensitivity-certificates-v0.2.0-candidate.clean-replay.json` on GitHub and Zenodo and is quoted on the Evidence Press page.

**Scope.** Both are producer-side replays on one machine with the same implementation. They are not an independent rerun by an unaffiliated party, a reimplementation or a formal verification. Continuous integration (`.github/workflows/ci.yml`) repeats the first replay on CPython 3.12 and 3.13 on Linux for every push; its run is recorded on the Evidence Press page.

**Manuscript.** `paper/manuscript.pdf` (11 pages) was built by pdfTeX from the included source and the two generated table files, then inspected page by page ([evidence/PDF_QA.json](evidence/PDF_QA.json)); rebuilt PDF bytes may differ across TeX installations and are not compared by the replay.
