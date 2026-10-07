# Status

This is an **unrefereed candidate**, version `0.2.0-candidate`, dated 2026-10-07. The creator is Anonymous.

**Claimed** (exact statements in [CLAIMS.json](CLAIMS.json), proofs in [PROOFS.md](PROOFS.md) and the manuscript).
- P1–P2: finite affine maxima define the unique quadratic optimal map to their own pushforward; the rational cell overlay computes $F(u,v)$ exactly and an exact primal–dual witness certifies $W_2^2$ (known constructions, reproduced with attribution).
- P3 (Theorem 2): the possible-winner envelope $B$ bounds $F(u,\tilde v)$ for every single realisation of an independent coefficient box, without fixed combinatorics or masses.
- P4–P5 (Theorem 7, Corollary 8): closed formulas for $F$, $W_2^2$ and their excess on the two-parameter three-atom family; corner maximum on admissible rectangles; symmetric envelope gap $\beta/2$.
- P6 (Proposition 3): an admissible family with envelope $4$ and sharp maximum $\varepsilon^2/4$, separating the two relaxations of the envelope (winner–slope incompatibility, unbounded factor $8/\varepsilon^2$; pointwise independence, factor exactly $2$).
- P7 (Theorems 4 and 6): $0\le B-F(u,v_{\mathrm{nominal}})\le\gamma(r)$ with an explicit rational constant linear in the largest radius; a convergent box-subdivision interval $[\mathrm{LB},\mathrm{UB}]\ni\sup F$ valid at every budget, with $\mathrm{LB}$ attained by a literal point of the box.

**Not claimed.**
- Any new general transport-stability exponent, or validation of the originating one-third theorem.
- A prescribed-mass solver, nonuniform sources, or a higher-dimensional implementation.
- A general sharp maximum in closed form; a polynomial-cost refinement (uniform subdivision is exponential in the box dimension $3n$).
- Formal verification; independent reproduction by an unaffiliated party; specialist or editorial peer review.
- Historical priority beyond the bounded search ([PRIOR_ART.md](PRIOR_ART.md)).

**Computations.** Every recorded number is an exact rational recomputed by the replay ([REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)). Wall times and memory in the benchmark are single-machine observations.

**Reviews.**
- Version 0.1.0 (local, never public): a same-model fresh-context internal review of P3–P5 found one validation defect (empty iterator), repaired ([INTERNAL_REVIEW.md](INTERNAL_REVIEW.md), [REVIEW_DISPOSITION.md](REVIEW_DISPOSITION.md)).
- Version 0.1.0: an external review supplied by the publisher on 7 October 2026 recommended major revisions; it found no counterexample to P1–P5, reproduced all documented commands, and reported an independent exact geometry oracle agreeing with the implementation on 13 box integrals and 8 overlays. All items were actioned in 0.2.0 ([REVIEW_RESPONSE.md](REVIEW_RESPONSE.md)). The reviewer's identity is not recorded; the report is not redistributed.
- Version 0.2.0: before freezing, P6, P7 and the new code were sent to a cross-vendor model (OpenAI `gpt-5.6-sol`, Codex CLI, prompted to refute, default REFUTED when unsure). Its verdicts and the dispositions:

| Finding | Verdict | Disposition |
|---|---|---|
| P6 formulas, supremum, envelope, edge cases $\varepsilon=0$, $b=\pm1$ | correct | none needed |
| P6 heading said both relaxations are separately unbounded; in this family pointwise independence costs exactly a factor 2 | refuted (heading) | heading and the sentence in §3.1/P6 corrected to "one unbounded, one a factor two" |
| Theorem 4 (tightness): decomposition, first bracket, strip width, strip-area bound, pair count | not refuted | none needed |
| Theorem 4: index bookkeeping after merging duplicate nominal slopes; norm conversions implicit; rationality claim overbroad for an arbitrary $D_K$ | gaps | a sentence fixes the winner's original index and the merged-slope case; the $\ell^2\le\ell^1$ step is stated; rationality is asserted for the $\ell^1$ vertex diameter |
| Theorem 6 / `refine_bound`: enclosure and pruning valid; termination claim false for tolerance $0$ (maximiser $b=19/20$ of the adverse family is not dyadic) | refuted (termination wording) | "for any tolerance" replaced by "for any positive tolerance", with the non-dyadic example recorded; tolerance $0$ documented as "exact or budget" |
| `attaining_realization` is the merged potential, not a literal point of the $n$-plane box | refuted (interface) | the routine now also returns `attaining_coefficients`, the literal box point; the test checks membership in the box and that it merges to the evaluated planes |
| `refine_bound` consumed one-shot iterators during validation | minor | inputs are materialised once; regression test added |

None of these is specialist or journal peer review.

**Provenance.** Version 0.1.0 was produced by an OpenAI Codex assistant; version 0.2.0 by an Anthropic Claude agent actioning the external review, with an OpenAI model as adversarial reviewer; published by Evidence Press. See [PROVENANCE.md](PROVENANCE.md).
