# AI index

Agent-readable map of this archive. Read [STATUS.md](STATUS.md) and [ASSURANCE.md](ASSURANCE.md) before reusing any claim.

## Identity
- Title: *Exact sensitivity certificates for planar transport maps: coefficient uncertainty, a convergent box refinement and a sharp three-atom calibration*.
- Version `0.2.0-candidate`, dated 2026-10-07, DOI 10.5281/zenodo.23205731.
- Creator: Anonymous. Publisher: Evidence Press.
- Status: unrefereed candidate. Written scoped proofs plus an exact rational implementation.
- Not formally verified, not independently reproduced, not peer reviewed; historical priority not claimed.

## The claims
- [CLAIMS.json](CLAIMS.json): P1–P7 with contribution status, proof locator, evidence class and qualifications.
- [PROOFS.md](PROOFS.md): accessible proofs. [paper/manuscript.pdf](paper/manuscript.pdf) (source [paper/manuscript.tex](paper/manuscript.tex)) is the typeset paper.

| Claim | Statement | Written argument | Code | Test |
|---|---|---|---|---|
| P1 | affine maxima define the unique optimal map to their own pushforward | manuscript Prop. 1; PROOFS P1 | `overlay` | `test_tilt_grid_exact` |
| P2 | exact overlay discrepancy; exact primal–dual target witness | Prop. 1, eq. (2); PROOFS P2 | `overlay`, `check_target_witness` | `test_generic_overlay_two_algorithms`, `test_negative_controls` |
| P3 | possible-winner envelope $B\ge F$ for every realisation of the box | Thm. 2; PROOFS P3 | `robust_bound`, `baseline_bound` | `test_zero_box_is_exact`, `test_general_box_samples`, `test_global_versus_pointwise_uncertainty` |
| P4 | tilt family: $F=H+(a+s)b^2$, $W_2^2=\lvert s\rvert+(a+s)b^2$, excess | Thm. 7; PROOFS P4 | `tilt_family` | `test_tilt_grid_exact` |
| P5 | corner maximum on admissible rectangles; symmetric envelope gap $\beta/2$ | Cor. 8; PROOFS P5 | `tilt_box_max` | `test_corner_maximum_grid` |
| P6 | adverse family: envelope 4, sharp maximum $\varepsilon^2/4$, two relaxations separated | Prop. 3; PROOFS P6 | `loose_family`, `loose_error` | `test_loose_family_two_relaxations` |
| P7 | tightness $B-F\le\gamma(r)$; convergent subdivision interval | Thms. 4, 6, Remark 5; PROOFS P7 | `tightness_bound`, `refine_bound`, `merge_planes` | `test_tightness_theorem_on_random_boxes`, `test_refinement_is_certified_and_converges` |

## Replay
- Entry point: [replay_archive.sh](replay_archive.sh) (tests in normal and optimised Python, three CLI recomputations, the benchmark recomputation, the manifest).
- Inputs and recorded results: [examples/tilt.json](examples/tilt.json) → [examples/tilt.result.json](examples/tilt.result.json); [examples/uncertainty.json](examples/uncertainty.json) → [examples/uncertainty.result.json](examples/uncertainty.result.json); [examples/refine.json](examples/refine.json) → [examples/refine.result.json](examples/refine.result.json).
- Benchmark: [benchmark.py](benchmark.py) → [evidence/benchmark.json](evidence/benchmark.json) (65 cases; exact fields recomputed by `--check`; timing and memory are observations only).
- Receipts: [evidence/replay.json](evidence/replay.json) (producer replay of the frozen files), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md) (fresh-extraction replay of the archive), [evidence/PDF_QA.json](evidence/PDF_QA.json) (page inspection).
- Integrity: [MANIFEST.sha256](MANIFEST.sha256), [verify_manifest.py](verify_manifest.py); environment: [ENVIRONMENT.txt](ENVIRONMENT.txt).

## Review and provenance
- Internal fresh-context review of 0.1.0 (P3–P5): [INTERNAL_REVIEW.md](INTERNAL_REVIEW.md), [REVIEW_DISPOSITION.md](REVIEW_DISPOSITION.md).
- External review of 0.1.0 supplied by the publisher, authorship not recorded, major revisions, all items actioned: [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md).
- Cross-vendor adversarial review of the 0.2.0 results: [STATUS.md](STATUS.md).
- Prior art and gates: [PRIOR_ART.md](PRIOR_ART.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [target.yaml](target.yaml), [RESEARCH_CONTRACT.md](RESEARCH_CONTRACT.md).
- Citations: [CITATION_AUDIT.md](CITATION_AUDIT.md), [SOURCES.md](SOURCES.md). Provenance: [PROVENANCE.md](PROVENANCE.md). Licences: [LICENSES.md](LICENSES.md).

## Reuse guidance for agents
- `map_distance_squared_upper` is a uniform upper bound over the box, not an attainable maximum; `refined_box.lower` is attained by `attaining_realization`; `refined_box.upper` is valid at every budget.
- `optimal_target_cost_squared` requires an exact primal–dual witness; map discrepancy $F$ and target cost $W_2^2$ are different quantities.
- Targets are the pushforwards of the supplied potentials; this is not a prescribed-mass solver; the implementation is planar with a uniform source.
- The originating OpenAI manuscript's general one-third upper bound is neither a dependency nor a claim checked here.
