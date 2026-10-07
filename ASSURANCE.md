# Assurance boundary

| Dimension | State | Evidence and limits |
|---|---|---|
| Availability | checked at publication | The GitHub release and the Zenodo record, compared byte for byte with the release SHA-256 sums. The result is recorded on the Evidence Press page and its machine records, not in this frozen file |
| Internal replay | passed | Tests in normal and optimised Python, three CLI recomputations, the 65-case benchmark recomputation and the manifest, run on the frozen files ([evidence/replay.json](evidence/replay.json)) and again from a fresh extraction of the archive ([REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)) |
| Separately implemented checks (same producer) | partial | The overlay discrepancy is recomputed by a separately implemented vertex-enumeration and convex-hull geometry (`test_transport.py`, 24 generic pairs and 45 tilt cases); the envelope has no second implementation in this package. The external review of 0.1.0 reported an independent inclusion–exclusion oracle agreeing on 13 box integrals and 8 full overlays; that oracle is not redistributed |
| Environment reproducibility | partial | Standard library only; interpreter and platform recorded in [ENVIRONMENT.txt](ENVIRONMENT.txt) and the receipts; no container image |
| Independent rerun | not established | No unaffiliated party has replayed the archive |
| Independent reimplementation | not established | The separately implemented geometry in the tests comes from the same producer workflow |
| Formal verification | not established | No proof assistant is used |
| Specialist review | not established | A same-model internal review (0.1.0), an external review of unrecorded authorship supplied by the publisher (0.1.0) and a cross-vendor adversarial model review (0.2.0) are not specialist review |
| Editorial peer review | not established | No journal or venue has reviewed the work |

**Load-bearing trust (trusted base).**
1. The written arguments P1–P7 in [PROOFS.md](PROOFS.md) and the manuscript. P1, P2 and P4 are standard; P3, P5, P6 and P7 are short and elementary but new in this combination.
2. The correctness of `transport_cert.py` (exact clipping, areas, arrangement splitting, interior representatives, weak-duality checking, best-first subdivision) and of CPython's `fractions.Fraction`.
3. The cited literature is used for positioning only; no external theorem is a dependency of any claim. The originating OpenAI one-third theorem is not used.

**Known historical defects, all repaired before the replays reported here.**
- 0.1.0 internal review: an empty reference iterator bypassed the nonempty-potential check and returned a spurious zero envelope; repaired and regression-tested.
- 0.1.0 external review: a rational string with denominator zero raised an uncaught exception (safe failure, wrong diagnostic); the manifest verifier excluded every file named `MANIFEST.sha256` instead of only the root manifest. Both repaired in 0.2.0 and regression-tested.
- 0.2.0 cross-vendor review: see [STATUS.md](STATUS.md).

**What the benchmark does and does not establish.** [evidence/benchmark.json](evidence/benchmark.json) records exact bounds, region counts and single-machine wall time and memory for 65 cases; its exact fields are recomputed by `benchmark.py --check`. It supports the three observations in manuscript §5 for those inputs; it does not establish asymptotic scaling, worst-case behaviour or usefulness on any downstream problem.
