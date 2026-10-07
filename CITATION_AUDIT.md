# Citation audit

Checked on 7 October 2026 against Crossref (DOI records), PMLR (page and supplement URLs) and the publisher or arXiv full texts named below. Every DOI resolves to a record whose authors, title, container and volume match.

## Load-bearing sources and the relationship checked

| Source | Used for | Checked |
|---|---|---|
| OpenAI (2026), *Sharp One-Third Stability of Brenier Maps*, repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, section "Sharpness on a fixed cube" | the three-atom construction and its $s=0$ identities; attribution | section read in full (0.1.0); the $s=0$ specialisations of Theorem 7 agree with its reported values ($a=1/4$: $W_2^2\in\{0,1/1024,1/256\}$, $F\in\{0,33/1024,17/256\}$, replayed by `test_tilt_grid_exact`) |
| Mérigot, Delalande and Chazal (2020), PMLR 108, 3186–3196, with supplement | Monge embedding (Definition 1.1); fixed-positive-mass square-root sensitivity (supplementary Lemma 5.1) | main paper Definition 1.1 and Proposition 2.1 read; supplementary Lemma 5.1 and proof read (two equal-mass atoms rotating on the unit circle, uniform disc) |
| An, Lei and Gu (2022), ECCV, LNCS, 619–635, doi:10.1007/978-3-031-20050-2_36 | common-source overlay coupling and its possible non-optimality | method pages 2–3 read (0.1.0); Crossref record |

## Context sources

| Source | Used for | Checked |
|---|---|---|
| Delalande and Mérigot (2023), *Duke Math. J.* 172(17), 3321–3357, doi:10.1215/00127094-2022-0106 | fixed-source/varying-target stability, exponent 1/6 | Crossref record (pages from the journal listing); Theorem 4.2 read in arXiv:2103.05934v2 |
| Divol, Niles-Weed and Pooladian (2025), *IMRN* 2025(7), rnaf078 | semi-discrete $W_2^{1/3}$ stability with varying supports | Crossref record; abstract, introduction and Section 4 opening read in arXiv:2404.02855v1 |
| Letrouit (2026), *C. R. Math.* 364, 333–344, doi:10.5802/crmath.834 | instability context for the source construction | publisher PDF: Theorem 2, Conjecture 3, Sections 1.3 and 3.1 read |
| Bansil and Kitagawa (2022), *IMRN* 2022(10), 7354–7389, doi:10.1093/imrn/rnaa355 | fixed-site cell stability without mass lower bounds | definitions and Theorem 1.3 read (0.1.0); Crossref record |
| Carlier, Delalande and Mérigot (2025), *Found. Comput. Math.* 25, 1259–1286, doi:10.1007/s10208-024-09669-4 | fixed-map/varying-source problem; LOT distance | introduction and problem statement read in arXiv:2401.01088v2 (0.1.0); Crossref record for the published version |
| Bonnet-Weill and Nenna (2026), arXiv:2604.09325v1 | reduced-order optimal-value estimators | abstract and Section 4 inspected (0.1.0) |
| Xie, Cheng, Yiu, Sun and Chen (2013), *VLDB J.* 22, 319–344, doi:10.1007/s00778-012-0290-x | possible-nearest-neighbour regions as an antecedent of possible-winner screening | Crossref and Semantic Scholar records; abstract read (UV-partitions associated with the set of possible nearest neighbours). The Section 4.1 envelope construction is reported by the external review and could not be read here (paywalled); the manuscript's sentence is phrased at the level the abstract supports |
| Rux, Quellmalz and Steidl (2026), *Adv. Comput. Math.* 52, article 24, doi:10.1007/s10444-026-10289-5 | $H$ is a shifted Huber penalty (uniform smoothing of the absolute value) | Crossref record; the identity $H(s,b)=h_{\lvert b\rvert}(s)/\lvert b\rvert+\lvert b\rvert/2$ verified by direct calculation; the source's Appendix 2 location is as reported by the external review |

## Not fully verified (recorded, not load-bearing)
- The Duke page range 3321–3357 (Crossref lacks pages; taken from the journal listing).
- The exact appendix and equation numbers inside Rux et al. and the Section 4.1 equations of Xie et al.; the manuscript cites both works without equation numbers.

## Corrections made during the audit
- Carlier–Delalande–Mérigot: the published journal record was added; the arXiv version is retained.
- An, Lei and Gu: the LNCS record and DOI were added.
