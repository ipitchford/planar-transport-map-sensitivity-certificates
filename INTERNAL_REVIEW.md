# Bounded internal mathematical review

Date: 2026-10-07. This is a fresh-context, same-model internal review, not external independence, formal verification, or a prior-art clearance. No further agents were used. The requested scope was P3–P5 in `PROOFS.md` and their correspondence to `transport_cert.py`; P1–P2 were inspected as dependencies. Main files were not changed by this reviewer.

Reviewed snapshots (SHA-256):

- `PROOFS.md`: `504b9db6c977609692ccfc6c21ab4d4fb060a0e186cf85e0eba5066393c4d504`
- `transport_cert.py`: `aba55fc438026f095496667f190a1e6b35656545b68fdc72d6b83e432aaf7e09`

Line references below refer to these snapshots. The existing contract and prior-art record were read for scope; their source-comparison claims were not independently re-audited. This was a correctness challenge of supplied candidate arguments, not a new research or literature-search campaign. First retained review timestamp: 05:33:56Z; exact-check runs through 05:35:58Z plus the subsequent empty-iterator reproduction. Initial reading preceded that timestamp. No pre-work numerical effort estimate was recorded; remaining report milestone was estimated at 2–4 minutes. Report readback completed at 05:38:41Z, 4 minutes 45 seconds after the first retained timestamp; this excludes initial reading and is not a full-task elapsed-time measure. Token usage was not measured.

## Disposition

**The P3–P5 mathematical claims are accepted within their stated hypotheses, with the reconstructions below.** No mathematical counterexample or load-bearing unsupported inference was found. This is a bounded review judgment, not a theorem certificate supplied by a separate proof assistant.

**The reviewed implementation is not ready for unconditional fail-closed checker sign-off.** An empty reference iterator bypasses potential validation and returns a spurious zero bound. This is a concrete input-validation defect, not a refutation of P3 for admissible nonempty potentials. A fix and regression test are required. There is also one nonblocking a.e./boundary wording clarification in P3.

## Accepted mathematical reconstruction

### P3: uniform coefficient-box envelope

Use tildes for a realized plane: `g_tilde_j(x) = g_j(x) + delta_j dot (x1,x2,1)`, with each coefficient deviation bounded by its stated radius. The triangle inequality gives `L_j(x) <= g_tilde_j(x) <= U_j(x)` for every x and every realization. If j is an actual maximizing index, then for every k,

`U_j(x) >= g_tilde_j(x) >= g_tilde_k(x) >= L_k(x)`.

Thus j belongs to J. Also, coordinatewise,

`|a_il - b_tilde_jl| <= |a_il - b_jl| + r_jl`.

Squaring and summing proves the displayed pointwise cost bound wherever the reference map has value a_i. Integrating it proves the claimed bound for **each globally fixed coefficient realization**, hence uniformly for all such realizations. No interchange of maximization and integration as an equality is used. Independence of box coordinates is sufficient; the enclosure would also remain valid for correlated subsets of that box, though it may be looser.

J is nonempty: choose a nominal maximizing plane j; then `U_j >= g_j >= g_k >= L_k` for every k. On an orthant, each comparison is affine. Splitting by all its nontrivial zero lines makes its sign constant on every full-dimensional region's interior. An identically zero comparison is everywhere satisfied. The resulting integrand is constant almost everywhere on each region, so rational areas and rational costs give an exact value for this enclosure.

In the implementation, the arithmetic mean of the vertices of a positive-area convex polygon lies strictly inside it: for any supporting edge, all vertices are on its nonnegative side and at least one is strictly on the positive side. Therefore the mean used at lines 184–186 is a legitimate sign representative, including when redundant collinear vertices occur. Dropping zero-area pieces does not change an integral. Orthant overlaps are on coordinate axes and have zero area.

For any fixed realization, unequal affine slopes tie only on lines; identical affine functions have identical slopes. Possible collisions, disappearance of cells, and zero masses therefore do not invalidate the map or bound. The exceptional null set may depend on the realization: the proof does not need one common null set for all parameters. The arrangement-limit exception at line 182 does not return a partial sum.

### P4: map discrepancy and exact target cost

Write `w(t)=a+s+bt`. Strict admissibility guarantees `0<w(t)<1` for all t in [-1,1]. The central intervals are [-a,a] and [-w(t),w(t)]; their normalized symmetric-difference length is `|w(t)-a|=|s+bt|`. No point switches directly between the left and right outer cells. Thus the horizontal squared map discrepancy averages to H(s,b).

Only the new central map has nonzero second coordinate. Its mass is `E w(U)=a+s`, so its vertical contribution is `(a+s)b^2`. This proves F. Splitting the one-dimensional integral at `-s/b` when that point lies in (-1,1) gives the two stated H branches. They agree at `|s|=|b|`, and the first branch handles b=0 without division by zero. Unused coordinates integrate out under product-uniform cube measure.

With atoms ordered left, center, right, the cost matrix is

```
C = [[0, 1+b^2, 4],
     [1, b^2,   1],
     [4, 1+b^2, 0]].
```

Subtracting the proposed dual sums gives nonnegative slack matrices:

```
s >= 0:                 s < 0:
[[0, 0, 4],             [[0, 2, 4],
 [2, 0, 2],              [0, 0, 0],
 [4, 0, 0]]              [4, 2, 0]].
```

For s>=0 the diagonal masses are `((1-a-s)/2, a, (1-a-s)/2)`, with s/2 moved from each outer source to the new center. For s<0 they are `((1-a)/2, a+s, (1-a)/2)`, with -s/2 moved from the old center to each outer target. All entries are nonnegative under admissibility, have the claimed marginals, and use only zero-slack pairs. The dual objective is respectively `s+(a+s)b^2` or `-s+(a+s)b^2`. Weak duality therefore proves the exact W2-squared identity; a numerical optimizer or strong-duality theorem is unnecessary.

Subtracting the two exact costs gives the claimed excess, including equality at `|s|=|b|`. The source specialization `s=0, b=a/2` is within the stated strict domain only for `a<2/3`; this is an inherited hypothesis, not an assertion valid for every a in (0,1).

### P5: rectangle maximum and symmetric-envelope comparison

For fixed b, H is convex in s because it is an average of absolute values of affine functions; the remaining term is affine in s. For fixed s, H is convex in b by the same argument and `(a+s)b^2` is convex since `a+s>0`. Applying the endpoint bound for a convex function first in s and then in b bounds every rectangle value by the largest corner value. Since those corners are included, that bound is attained. This also covers degenerate intervals. Joint convexity is not needed.

Admissibility at all four corners suffices: both `a+s-|b|` and `1-a-s-|b|` are concave functions on the rectangle, so their values at any convex combination of corners are at least the corresponding combination of positive corner values. Equivalently, their minima use an extreme s and the endpoint with largest absolute b.

For the last comparison, take `0<=B<min(a,1-a)` and t=x2, `tau=|t|`. The only uncertain coefficient is the central slope b in [-B,B]. At a fixed slice, normalized widths and P3 costs are:

- reference-central core `|x1|<a-B*tau`: mass `a-B*tau`, cost `B^2`;
- reference-central boundary band: mass `B*tau`, cost 1;
- reference-outer boundary band: mass `B*tau`, cost `1+B^2`;
- remaining outer region: cost 0.

Here B<1/2, so 1 dominates `B^2` in the inner band. The slice enclosure is consequently `a*B^2+2*B*tau`. Since `E|U|=1/2`, the exact P3 enclosure is `B+a*B^2`. The exact globally fixed tilt maximum is `B/2+a*B^2`; their gap is B/2. This supplies the otherwise compressed justification of `PROOFS.md:70`.

## Concrete objections and requested dispositions

### R1 — Empty iterators bypass the nonempty-potential precondition

Location: `transport_cert.py:50–56`, propagating to `153–190`.

`planes()` checks `bool(coefficients)` before converting it to a list. An empty iterator is truthy. Its conversion then yields an empty list, and all subsequent universal/cardinality checks pass vacuously. `robust_bound()` iterates over no reference planes and returns zero with zero arrangement regions. The reference potential is undefined, so that output is not a valid certificate.

Exact reproduction under Python 3.14.7:

```python
from transport_cert import planes, robust_bound
square = [(-1,-1), (1,-1), (1,1), (-1,1)]
print(planes(iter(())))
# []
print(robust_bound(square, iter(()), [(0,0,0)], [(0,0,0)]))
# {'map_distance_squared_upper': Fraction(0, 1), 'arrangement_regions': 0}
```

The empty-list variant correctly raises `CertificateError('empty potential')`. Thus the earliest failing implementation inference is that truthiness of the **unmaterialized input** proves existence of a plane. Request: check that the materialized result is nonempty, or explicitly restrict and validate the input container type; regression-test both empty lists and empty iterators. This is a medium-severity fail-closed API issue. It does not alter the accepted mathematical result on the stated nonempty domain.

### R2 — Qualify arrangement constancy by interiors/almost everywhere

Location: `PROOFS.md:33`.

J need not be constant on a *closed* clipped polygon including its boundary. For example, at zero uncertainty with planes x1 and -x1, J is a singleton on either open half-plane but contains both indices on x1=0. Standard arrangement terminology can already mean open cells, so this is an exposition clarification, not a mathematical failure. Request: write “J is constant on each region's interior, hence almost everywhere on that region.” The implementation's interior representative and null-boundary argument are correct.

## Exact finite corroboration performed

Commands used `PYTHONDONTWRITEBYTECODE=1 python3` and imported the reviewed module. No main-file edits or broad computations were performed.

- 23 admissible cases from `a in {1/4,1/2,3/4}`, `s,b in {-1/8,0,1/8}`: formula F equalled exact polygon overlay; exact primal/dual checking equalled the W2 formula; masses agreed; the zero-radius robust enclosure equalled the overlay. H was also evaluated separately by integrating `sign*(s+b*t)` on intervals split at its zero.
- Symmetric tilt cases `(a,B)=(1/4,1/8),(1/2,1/4),(3/4,1/8),(1/2,0)`: P3 bounds were respectively `33/256, 9/32, 35/256, 0`; sharp maxima were `17/256, 5/32, 19/256, 0`.
- Coincident nominal uncertain planes with zero radii returned zero correctly; an inactive reference plane with zero cell mass did not change the zero bound.
- Strict-boundary inputs `(a,s,b)=(1/2,0,1/2),(1/2,-1/2,0),(1/2,1/2,0)` were rejected. A zero region limit raised the specified no-certificate exception.
- A 153-point rational grid inside `s in [-1/8,1/8], b in [-1/4,1/4]`, a=1/2, did not exceed the exact corner maximum `25/128`.
- A mixed slope/intercept box on triangle `(-2,-1),(2,-1),(0,2)` used reference planes `(-1,0,0),(1,0,0),(0,1,-1)`, centers `(-1/2,0,1/8),(1/2,0,-1/8)`, and radii `(1/2,1/4,1/8)` for both planes. All 64 endpoint realizations obeyed the bound `317/80` (six regions); eight realizations required merging duplicate slopes. The largest tested exact map discrepancy was `601/480`.
- The nonoptimal overlap coupling for `(a,s,b)=(1/2,0,1/4)`, supplied alongside the genuine optimal dual, was rejected with `nonzero optimality gap`.
- R1's empty-iterator failure was reproduced exactly as above.

These checks corroborate implementation behavior on finite inputs. They do not prove a uniform box bound, corner reduction, or correctness on every polygon. The analytic arguments above supply the universal reasoning. In particular, the 64 box corners are **not** asserted to control a general coefficient box: that separate-convexity property was proved only for the specialized (s,b) family.

## Unexamined and residual assurance boundaries

- No historical novelty, source attribution accuracy, or general one-third stability theorem was independently reviewed. The prior-art record itself retains source-comparison limitations.
- No formal verification, independent replacement geometry engine, exhaustive malformed-input fuzzing, resource-scaling study, package/document QA, clean distribution replay, or downstream release review was performed.
- The inspected clipping and midpoint logic supports the specification, but sharing the production geometry code across several checks limits computational independence. The direct H integral and symbolic dual reconstruction are independent of that clipping logic.
- No assertion extends to nonuniform sources, prescribed target-mass inversion, general-dimensional implementations, or preservation of perturbed masses/combinatorics.
- The reviewed code's strict tilt domain excludes equality at strip contact with cube boundaries. Some formulas may extend continuously there, but such an extension was not needed or certified here.
- Any changes to the hashed proof or implementation require checking the affected claims and updating review status; this review does not automatically approve later bytes.
