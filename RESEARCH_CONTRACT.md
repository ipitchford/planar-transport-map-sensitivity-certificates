# Transport sensitivity investigation

## Target

Original opportunity: sharp or certified, computable conditioning bounds for discrete-target optimal transport, including degenerating masses and cells. Deliver an Evidence Press research bundle, not a website publication.

Current concrete target: for rational planar affine-max potentials on a rational convex polygon, certify exact map L2 displacement; separately certify target transport cost using a primal/dual witness; derive a computable envelope valid for every independent coefficient perturbation in a stated box. Seek sharp special-case calibration and identify when map instability is caused by cell reassignment. Do not treat a generic polygon intersection routine as a new theorem.

## Hypotheses and conventions

Uniform probability measure on a bounded convex polygon of positive area. Potentials are maxima of finitely many affine functions. Distinct slopes within each potential, or explicit deduplication retaining the largest intercept. Quadratic transport cost is squared Euclidean distance without a factor 1/2. Rational arithmetic for computational certificates. Targets are the pushforward laws of the supplied potentials; solving for prescribed target masses is a separate problem.

## Known evidence

OpenAI family 374, commit adc7f1241b42e322a6451854ab7e4b4c146bf78a, section `sharpness.tex`: affine-max optimality proof and three-atom tilt example read in full. Its claimed general one-third upper bound is not a dependency of the planned checker and has not been re-proved or formally replayed here.

## Prior-art gate

Prospective search 2026-10-07, before substantive extension work. See PRIOR_ART.md and target.yaml. Power-diagram representation and overlap couplings are known. Their reproduction and extension as certificate infrastructure are authorized by the original shortlist; no priority claim on either construction is permitted. Exact uncertainty envelope and specialized calibration proceed under bounded uncertainty, not proven novelty.

## Success and scope

Full result for this chosen computational target means a proved certificate specification, usable implementation on arbitrary admissible planar inputs, worked sharp calibration, and adversarial tests. It does not mean a new general transport exponent, a general efficient prescribed-mass solver, or empirical validation of a downstream ML system.

## Forecast

At 2026-10-07T05:25:55Z: initial prior-art and exact-computation milestone estimated 1–2 active hours, measured against retained execution timestamps. This is not a stopping cap. Token use is not inferred from elapsed time.

## Routes

R1: direct exact overlay geometry plus finite transport dual witnesses. Cheap falsification: recover the source tilt formula and ensure a deliberately nonoptimal overlap coupling is rejected as an optimal target coupling.

R2: coefficient-box winner enclosures. Hard step: bound all possible winners without assuming the uncertain diagram preserves combinatorics or masses. Cheap test: zero uncertainty must reproduce the exact map distance; samples may falsify but cannot prove a bound.

R3: derive new uniform exponents from the source theorem. Deferred: duplicates the originating manuscript and would require broad source-proof validation without improving the current bounded applied target.

## Obligations

- O1 addressed: P1–P2 written proofs; rational clipping versus separate line-intersection/hull tests.
- O2 addressed: exact weak-duality witness checker; feasible nonoptimal coupling and corrupted witnesses rejected.
- O3 addressed: P3 proof, degenerate-cell tests, coincident uncertain planes, fail-closed region cap. No claim that sampling proves the bound.
- O4 addressed: P4–P5 proofs, 45 exact calibration cases, separate geometric calculation and internal fresh-context challenge.
- O5 addressed to bounded-search standard: initial and final formula/method queries and explicit existing-work attribution in PRIOR_ART.md. Historical priority remains unestablished.
- O6 research review addressed: INTERNAL_REVIEW.md and REVIEW_DISPOSITION.md. Distribution integrity is separately established by evidence/replay.json and the exact-ZIP clean-extraction receipt delivered alongside the archive.

## Experiments

Before code execution: test general rational polygon overlays, the three-atom tilt family, pointwise uncertainty enclosures, translation/intercept invariances, and malformed/altered certificates. Predict that cell-switching dominates target displacement at small tilt. Do not use float agreement as exact evidence.

## Revision 0.2.0 (7 October 2026)

The publisher supplied an external review of the 0.1.0 bundle and authorised actioning it in full and publishing the result. New obligations and their closure: O7 adverse family (P6) proved and tested; O8 tightness bound (P7, Theorem T) proved with an explicit rational constant and checked on 108 random boxes; O9 convergent subdivision (P7, Theorem C) proved and implemented with feasible lower bounds; O10 bounded benchmark against the slope-diameter baseline recorded with exact recomputation; O11 literature comparison completed with verified records; O12 software repairs (rational diagnostics, root-manifest exclusion). Scope unchanged otherwise: uniform planar source, own pushforward targets, no prescribed-mass solver.

## Handoff

Research disposition: concluded for the frozen direct-certificate target at the unrefereed-candidate assurance level, version 0.2.0. No unresolved fatal objection was identified in the bounded internal review (0.1.0) or in the external review (0.1.0, all items actioned in REVIEW_RESPONSE.md). Source theory, written proofs, finite tests, internal review, and novelty limits remain separate. Packaging is not authorized to relabel this as external peer review or a general prescribed-mass solver.

The operational programme tracker and external clean-extraction receipt determine whether the ZIP itself is ready; this source document cannot certify its own future archive. Public publication of version 0.2.0 was authorised by the publisher on 7 October 2026 and is recorded by the publisher's workflow, not by this document. More general inverse, nonuniform, high-dimensional and empirical applications remain outside the frozen target, as recorded in RESEARCH_GATES.json.
