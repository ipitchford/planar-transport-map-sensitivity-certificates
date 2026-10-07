# Response to the external review of version 0.1.0

An external review of version 0.1.0 (a local, unpublished bundle of 7 October 2026) was supplied by the publisher on 7 October 2026. Its author is not recorded. It recommended major revisions and gave a prospective REF-style assessment; the review's text and audit bundle are not redistributed. Every item below was actioned in version 0.2.0. The review does not establish specialist or journal peer review.

The review found no counterexample to the five stated claims (P1–P5) and reproduced all five documented commands; its independent exact geometry checks agreed with the implementation. Its concerns were about informativeness, positioning and evidence of practical use.

## Major comments

| Item | Review request | Disposition in 0.2.0 |
|---|---|---|
| M1 | Characterise the enclosure's potentially unbounded conservatism: two distinct relaxations; add the adverse example; state that there is no general relative-tightness guarantee. | Done. Proposition 3 (manuscript §3.1, `PROOFS.md` P6) rederives the reviewer's family: $F(u,v_b)$ piecewise, $\sup F=\varepsilon^2/4$ at the interior parameter $b=1-\varepsilon/2$, envelope $4$, compatibility-respecting pointwise integral $\varepsilon^2/2$, ratio $16/\varepsilon^2$, zero error at both endpoints, $\varepsilon=0$ case. Both relaxations are named in §3.1 and in P3. The absence of a general relative guarantee is stated. `loose_family`/`loose_error` and `test_loose_family_two_relaxations` (404 exact grid cases) ship with the code; `examples/refine.json` is this family. |
| M2 | Complete the contribution-specific literature comparison: Mérigot–Delalande–Chazal 2020 (supplementary Lemma 5.1), Delalande–Mérigot 2023, Divol–Niles-Weed–Pooladian 2025, Xie et al. 2013, Letrouit 2026, Rux–Quellmalz–Steidl 2026 (Huber identity); organise by what varies / what is controlled / degeneracies / quantity certified; describe P3 as a transport-specific integration of established envelope reasoning. | Done. §1 cites all six and the published Carlier–Delalande–Mérigot record; Table 1 is the requested comparison; the fixed-positive-mass square-root phenomenon is attributed to Lemma 5.1 of the 2020 supplement; the possible-winner construction is presented as the same screening principle as the UV-diagram applied to affine coefficients; $H$ is identified as a shifted Huber penalty. Every added record was checked against Crossref/PMLR and the relevant passages read (`CITATION_AUDIT.md`). |
| M3 | Establish where the method provides useful information at a practical cost: a controlled planar benchmark against $B_0=\sum_i\rho(C_i)\max_j M_{ij}$, with explicit realisations and exact robust maxima where available; vary atom count, radius, bit length, inactive/near-coincident planes, polygon geometry; report tightness, time, memory, regions, refusals. | Done. `benchmark.py` records 65 cases in `evidence/benchmark.json` (exact fields recomputed by `--check`); §5 and Tables 2–3 report $B/B_0$, $B/\sup F$, $\mathrm{LB}/B$, $\mathrm{UB}/B$, regions, wall time, peak memory and a region-cap refusal. Findings: screening reduces $B_0$ to 12–46 % at $n=6$; explicit realisations reach 95–100 % of $B$ at $r=1/64$; subdivision is decisive on one-parameter boxes and marginal at budget 32 on $3n$-dimensional boxes. |

## "Could improve the work" items

| Item | Review suggestion | Disposition in 0.2.0 |
|---|---|---|
| C1 | A proved refinement retaining winner–slope compatibility or subdividing the global parameter box, with explicit feasible realisations supplying lower bounds. | Done, by subdivision. Theorem 6 (`PROOFS.md` P7, Theorem C) proves that for any finite cover of the box by sub-boxes, $\mathrm{LB}\le\sup F\le\mathrm{UB}$ and $\mathrm{UB}-\mathrm{LB}\le\gamma_{\mathrm{box}}(r_*)$, linear in the largest sub-box radius. `refine_bound` implements best-first bisection with pruning, centre and endpoint probes as feasible realisations, and a tolerance/budget stop that always returns a valid interval. Both relaxations vanish in the limit. On the adverse family the interval closes to within 0.14 % of $\varepsilon^2/4$ with 256 sub-boxes (envelope was 4); on the tilt family the sharp corner maximum is bracketed exactly with three sub-boxes. |
| C2 | Conditions linking enclosure tightness to margins, slope separation or uncertainty size. | Done. Theorem 4 (`PROOFS.md` Theorem T): $0\le B-F(u,v)\le 2r\Lambda+2r^2+4rR_KD_Kn(n-1)\Lambda/\lvert K\rvert$, uniform in the slope separation; Remark 5 gives the margin form ($B-F\le 2r\Lambda+2r^2+\max M_{ij}\,\lvert\{\mu\le 2rR_K\}\rvert/\lvert K\rvert$) and the slope-separation form of the near-tie measure. `tightness_bound` computes the constant exactly; `test_tightness_theorem_on_random_boxes` checks the inequality on 108 random boxes. |
| C3 | Extend beyond uniform planar integration where a concrete research application justifies it. | Not done, deliberately. No concrete application was identified that would justify a weighted or higher-dimensional integration backend; the proofs of Theorems 2, 4 and 6 do not use the dimension (stated in §6 and `PROOFS.md` Limits), and the limitation remains OPEN in `RESEARCH_GATES.json` with that reason. |

## Must-fix framing items

- Both sources of looseness explained and the exact adverse example added (M1).
- Direct prior-art comparison completed; the transport-specific additions are identified as the complete coefficient-box map-error integral with its tightness and convergence statements, the $s\neq0$ excess identity and the coupling-optimality threshold (M2; `RESEARCH_GATES.json` verdicts updated).
- Bounded study supplied (M3); the submission is framed as a certificate note with proved tightness/convergence, not as evidence of broad practical reach.

## Should-fix items

| Item | Disposition |
|---|---|
| Rational-input diagnostic (`"1/0"` raised an uncaught `ZeroDivisionError`) | Fixed: `q()` converts `ValueError`/`ZeroDivisionError` into `CertificateError('malformed rational …')`; the CLI also lists `ZeroDivisionError` defensively; regression `test_malformed_rationals_are_refused`. |
| Root-manifest exclusion (`verify_manifest.py` excluded every basename `MANIFEST.sha256`) | Fixed: only the root-relative path `MANIFEST.sha256` is excluded. |
| Retain independent geometry checks (full overlap matrices, box integrals) | The reviewer's checks are not redistributed (they are part of the review bundle). The shipped suite retains its separately implemented vertex-enumeration/hull geometry for the overlay and adds the exact adverse-family grid and the tightness inequality as further falsification tests; the external review's independent oracle results are recorded in `STATUS.md` as a review finding, not as shipped evidence. |
| Report region counts, arithmetic sizes, runtime, memory and refusals | Done in `evidence/benchmark.json` and §5. |
| End-to-end example of obtaining a coefficient box and interpreting the result | Done: `README.md` "Worked example" walks through `examples/refine.json` (what the radii mean, what the induced target masses are, how to read envelope, baseline, interval and attaining realisation). |

## Minor comments

| # | Request | Disposition |
|---|---|---|
| 1 | Malformed rational diagnostics | Fixed (above). |
| 2 | Manifest exclusion | Fixed (above). |
| 3 | Bibliographic details for Carlier–Delalande–Mérigot | Added: *Found. Comput. Math.* 25 (2025), 1259–1286, DOI 10.1007/s10208-024-09669-4, alongside the arXiv record. |
| 4 | Complete the coupling description in Theorem 3 (now Theorem 7) | Done: the three diagonal entries and the two surplus-mass entries are written out for both signs of $s$, including the centre's move from $0$ to $be_2$. |
| 5 | Separate notation ($B$ for the enclosure and the tilt radius) | Done: the tilt radius is now $\beta$ throughout; $B$ is the envelope, $B_0$ the baseline. |
| 6 | State elementary consequences ($J(x)\neq\emptyset$, zero radii exact, vertex mean interior) | Done after Theorem 2 and in P3. |
| 7 | Consistent assurance wording about `--check` and "certificate" | Done: §6 and `README.md` say that `--check` is a recomputation with the same implementation, not an independent verification; "certificate" is used for exact enclosures, with the trust boundary stated. |
| 8 | Tidy records: `target.yaml` fingerprints pending; `RESEARCH_GATES.json` `sourcesReadInFull` heading; theorem/sentence page splits | `target.yaml` fingerprint status is now "replayed exactly by `test_tilt_grid_exact`"; the machine key `sourcesReadInFull` is required by the publisher's gate checker and is retained, with an explicit `sourcesReadInFullMeaning` field stating that entries record the exact sections read; page splits were inspected after rebuilding (an 11-page manuscript; no theorem statement is split). |

## Changes beyond the review

- Version 0.2.0; the 0.1.0 bundle was never public. Its internal review (`INTERNAL_REVIEW.md`, `REVIEW_DISPOSITION.md`) is preserved unchanged.
- The command-line tool reports the baseline $B_0$ with every envelope and accepts a `refine` block; `examples/*.result.json` were regenerated; `benchmark.py --check` is part of the replay.
- The new theorems (Proposition 3, Theorems 4 and 6) and the new code were sent for a cross-vendor adversarial review (OpenAI model, prompted to refute) before freezing; its findings and dispositions are recorded in `STATUS.md`.
