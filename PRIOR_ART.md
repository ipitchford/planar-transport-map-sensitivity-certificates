# Prior-art gate, 7 October 2026

## Frozen target and contribution units

Exact certificates for planar affine-max transport-map sensitivity, with a coefficient-box uncertainty envelope and sharp calibration. General optimal-map stability, power diagrams, and overlay couplings are not claimed new. The originating three-atom construction will be reproduced with attribution.

## Searches performed before extension work

Web search, primary repositories and full texts:

- `Brenier map sharp stability discrete target computable conditioning power diagram sensitivity atom mass one third`
- `Bansil Kitagawa quantitative stability geometry semi discrete optimal transport pdf theorem`
- `"optimal transport" "certificate" "power diagram" perturbation sensitivity`
- `"Brenier" "three atoms" stability`
- `"semi-discrete" "stability" "moving" "support" optimal transport`
- `"optimal transport" "power diagram" "interval" "certified"`
- `"optimal transport" "exact rational" "stability"`
- `"semi-discrete" "optimal transport" "a posteriori" error`
- `"Brenier" "b/2" stability`
- `optimal transport power diagram exact arithmetic overlap cells map distance certification`
- `"optimal transport" "robust" "Laguerre cells" certificate`
- `"Approximate Discrete Optimal Transport Plan" power diagrams overlap`
- `"optimal transport" "margin" "perturbation" Laguerre`
- Google Scholar domain search for Bansil–Kitagawa title: no usable independent Scholar record returned; bibliographic identity instead checked at arXiv/publisher. No Scholar scraping.

## Inspected primary sources and comparisons

1. OpenAI, *Sharp One-Third Stability of Brenier Maps*, 25 September 2026, repository commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. `build/source/sections/sharpness.tex` read in full; introduction read. Three-affine-max optimality and tilt calculations are existing source claims. We will rederive rather than treat these as newly discovered. The general upper-bound proof is not a dependency.
   https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026

2. Mohit Bansil and Jun Kitagawa, *Quantitative stability in the geometry of semi-discrete optimal transport*, arXiv:2002.02022; published IMRN 2022(10), 7354–7389, DOI 10.1093/imrn/rnaa355. Read definitions and Theorem 1.3 (PDF page 3), plus surrounding scope and inverse-map discussion. It bounds summed symmetric cell differences by 4N times L1 target-mass change for a fixed finite site set. Thus cell stability and quantitative bounds are established; the planned variable-slope box checker is a different computational specification, not a replacement theorem.
   https://arxiv.org/pdf/2002.02022

3. Guillaume Carlier, Alex Delalande and Quentin Mérigot, *Quantitative Stability of the Pushforward Operation by an Optimal Transport Map*, arXiv:2401.01088v2. Introduction, problem statement, and LOT discussion inspected. Fixed-potential/varying-source stability differs from fixed-source/varying-potential sensitivity. The LOT distance is explicitly the L2 distance of Brenier maps: naming that distance is not novel.
   https://arxiv.org/html/2401.01088v2

4. Dongsheng An, Na Lei and Xianfeng Gu, *Approximate Discrete Optimal Transport Plan with Auxiliary Measure Method*, ECCV 2022. Primary PDF search-extracted method passage and university bibliographic record inspected; complete PDF remains to be read for final comparison. It already constructs the coupling from intersections of two source-cell decompositions. Outcome: COLLISION for claiming overlay couplings as a new construction. Our remaining contribution is exact checking and uncertainty certification, subject to further search.
   https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136830602.pdf
   https://researchconnect.stonybrook.edu/en/publications/approximate-discrete-optimal-transport-plan-withauxiliary-measure/

5. Elise Bonnet-Weill and Luca Nenna, *A reduced-order model for parametrized Optimal Transport problems*, arXiv:2604.09325v1. Metadata and abstract inspected; full HTML located. Its reduced-order potentials and optimal-value error estimators are relevant context, not evidence that exact map-error box certificates are new. Full theorem comparison remains before final novelty wording.
   https://arxiv.org/html/2604.09325v1

## Access and coverage limits

NSF PDF wrapper returned 502 for two sources; arXiv and ECVA primary alternatives located. No paywall bypass. English-language bounded web/full-text search, not exhaustive history or citation-graph coverage; no author enquiry. Most proposed formula-level fingerprints cannot exist until the precise uncertainty statement is derived. Recheck that statement and any simplified formula before concluding the research.

## Decision

Proceed with a attributed reproduction plus clearly scoped certificate extension. Known statement/overlay constructions: COLLISION. Certificate contribution and robust envelope: BOUNDED UNCERTAINTY. Permitted wording: exact certificate implementation and proved scoped estimates. Forbidden: first stability result, new optimal-transport representation, or proven historical priority.

## Follow-up after formula derivation

Searches on 7 October: `"optimal transport" "tilted" "strip" sensitivity`, `"Brenier" "mass" "tilt" stability`, `"transport" "squared" "b/2" "three"`, and `"linearized optimal transport" "distortion" "three" atoms`. No exact match to the two-parameter excess formula was located; several broad searches returned irrelevant material. This is weak negative evidence, not priority clearance. The new formula is an elementary extension of the credited source construction.

ECVA full PDF became accessible: pages 2–3, method and discussion following the overlay definition, explicitly state that the induced coupling need not be optimal. That observation is also known and must be credited. Section 4 of Bonnet-Weill–Nenna HTML inspected: its estimators compare reduced and full optimal values; this differs from the pointwise winner-envelope bound for map distance in P3. No upstream PDF is redistributed in our bundle.

Final fingerprint refresh on 7 October: `"optimal transport" "coefficient uncertainty" "map"`, `"optimal transport" "s^2+b^2" tilt`, and `"Brenier" "three-atom" "uncertainty"`. No exact match was located. Returned material was predominantly unrelated or much broader; absence in these search results is not a novelty proof. No priority language was added.

## Revision 0.2.0 (7 October 2026): sources located by the external review, verified here

The external review of version 0.1.0 identified direct antecedents that the bounded search above had missed. Each was checked against Crossref (or PMLR) and the relevant passage read before citation; the comparison is in manuscript Table 1 and the entries are in `RESEARCH_GATES.json`.

1. Mérigot, Delalande and Chazal, PMLR 108 (2020), with supplementary material. Definition 1.1 defines the Monge embedding (the $L^2$ map distance from a fixed source). Supplementary Lemma 5.1 (read in full) obtains $\lVert T_{\mu_\theta}-T_{\mu_0}\rVert\ge C\,W_2^{1/2}$ with two equal-mass atoms rotating on the unit circle and a uniform disc source. Outcome: the fixed-positive-mass square-root phenomenon is **known**; our calibration's version is an exact formula in a different family and is no longer presented as an observation of the phenomenon.
2. Delalande and Mérigot, Duke Math. J. 172(17) (2023). Theorem 4.2 (compact case) read: fixed source density bounded above and below on a compact convex set, varying target, exponent 1/6. Outcome: closest direct stability context; different problem (no coefficient box).
3. Divol, Niles-Weed and Pooladian, IMRN 2025(7). Abstract and Section 4 opening read: semi-discrete unregularised map stability of order $W_2^{1/3}$ for discrete targets with possibly different supports under mass/separation assumptions. Outcome: moving supports alone are not new; our tolerance of disappearing cells and direct coefficient boxes is a different specification.
4. Letrouit, C. R. Math. 364 (2026). Theorem 2, Conjecture 3 and Section 3.1 read: exponent obstruction for a uniform source on a special bounded open set; conjectured 1/2 for convex sources. Outcome: historical context for the source's construction; not a dependency.
5. Xie, Cheng, Yiu, Sun and Chen, VLDB J. 22 (2013). Abstract read (UV-partitions carry the set of objects that can be nearest neighbours); the Section 4.1 envelope construction reported by the review could not be read in full here (paywalled). Outcome: cross-domain antecedent of possible-winner screening; the transport integral is not there.
6. Rux, Quellmalz and Steidl, Adv. Comput. Math. 52 (2026). The identity $H(s,b)=h_{|b|}(s)/|b|+|b|/2$ (Huber penalty) was verified by direct calculation. Outcome: $H$ is classical as a scalar function; novelty, if any, attaches to its transport role.
7. Carlier, Delalande and Mérigot: published record *Found. Comput. Math.* 25 (2025) 1259–1286 added.

Fingerprint queries rerun on 7 October 2026 for the new results: `"optimal transport" "branch and bound" "Laguerre" robust map error`; `"semi-discrete" "optimal transport" "interval" "subdivision" certified maximum`; `"possible winner" envelope "optimal transport" conservatism`. No exact match for the linear-in-radius tightness bound of the possible-winner envelope or for the coefficient-box map-error interval was located. Subdivision over interval boxes is standard global-optimisation practice and is not claimed as new. This remains weak negative evidence, not priority clearance.
