# Exact planar sensitivity certificates: working proof

Status: written candidate arguments. Version 0.1.0 (local, unpublished) received a fresh-context internal challenge (INTERNAL_REVIEW.md, REVIEW_DISPOSITION.md) and an external review supplied by the publisher (REVIEW_RESPONSE.md). Version 0.2.0 adds P6 (an adverse family exposing two distinct relaxations in P3) and P7 (an explicit tightness bound and a convergent box-subdivision refinement with feasible lower bounds). Package QA is recorded separately. No external peer review or formal verification is claimed. Original source is OpenAI family 374, pinned in RESEARCH_CONTRACT.md; its three-plane example is credited, not claimed as our discovery. Power-diagram and common-source overlap constructions are established prior art.

## P1. Affine maxima define optimal maps

Let K be a convex polygon of positive area and rho its uniform probability measure. Let f_i(x)=a_i dot x+c_i with distinct slopes, and T(x)=a_i on its maximizing cell C_i. Distinct ties lie on lines and have zero area. Let mu=T#rho. For any coupling pi of rho and mu,

integral x dot y dpi <= integral max_i f_i(x) drho - sum_i c_i mu({a_i}).

The graph coupling of T attains equality. Because both marginal second moments are fixed, this maximizes the cross term in squared Euclidean cost and minimizes that cost. Equality forces a maximizing slope almost everywhere, establishing uniqueness. This is the standard finite-affine-max optimality argument, reproduced here to make the checker independent of the source's general stability theorem.

## P2. Exact overlay certificate

For a second potential g_j(x)=b_j dot x+d_j with cells D_j, define Q_ij=area(C_i intersect D_j)/area(K). These are rational for rational inputs. They form a coupling of the pushforward masses and

F = integral |T_f-T_g|^2 drho = sum_ij Q_ij |a_i-b_j|^2.

This follows by integrating the constant integrand on each overlay cell. In general F is only an upper bound on W2(mu,nu)^2, not equality. Separate finite vectors alpha_i,beta_j and a coupling P certify target optimality if their marginal sums match, P>=0, alpha_i+beta_j<=|a_i-b_j|^2, and primal cost equals sum_i mu_i alpha_i + sum_j nu_j beta_j. Weak duality alone proves the certificate. No floating-point optimization result is trusted.

## P3. A uniform coefficient-box envelope

Fix f and let every coefficient of g_j vary independently about a nominal coefficient with nonnegative radii (r_j1,r_j2,r_j0). For each x define

e_j(x)=r_j1 |x1|+r_j2 |x2|+r_j0,
U_j(x)=g_j(x)+e_j(x), L_j(x)=g_j(x)-e_j(x),
J(x)={j: U_j(x)>=L_k(x) for every k}.

For every admissible global coefficient choice, any actual maximizing index belongs to J(x). Indeed its actual value is at most U_j and every competing actual value is at least L_k. Thus on reference cell C_i,

|T_f(x)-T_g(x)|^2 <= max_(j in J(x)) sum_(l=1,2) (|a_il-b_jl|+r_jl)^2.

Integrating gives a valid uniform bound. On each coordinate orthant, all U_j-L_k are affine. Partitioning C_i by their zero lines makes J constant on the interior of each positive-area region, so the integral is exactly computable using rational clipping and polygon areas. An identically zero comparison is allowed. Ties with unequal slopes occupy null lines for any fixed realization; coincident affine functions have identical slopes and therefore do not affect the map. Lower-dimensional arrangement boundaries are null. The proof does not require preservation of combinatorics, positive mass of each cell, or preservation of target masses.

The enclosure can be conservative for two distinct reasons. First, the cost M_ij maximises the slope discrepancy of plane j over the whole box without requiring that the same coefficient choice makes j win at x (winner–slope incompatibility). Second, the pointwise maximum lets different source points use different global parameters (pointwise independence). P6 gives an admissible family in which the first relaxation alone costs an unbounded factor and the second a further factor two. The enclosure is an upper bound, not an assertion that all pointwise maxima can be attained simultaneously; there is no general relative-tightness guarantee. P7 shows that the gap is nevertheless linear in the largest radius, with an explicit constant, which is what makes box subdivision converge. A declared complexity limit may stop computation, but may never return a partial integral as a valid bound.

Elementary consequences used by the implementation: J(x) is nonempty (a nominal maximiser j satisfies U_j >= g_j >= g_k >= L_k); with all radii zero the envelope equals the exact discrepancy almost everywhere; the arithmetic mean of the vertices of a positive-area convex polygon lies in its interior, so it is a valid sign representative for each arrangement region.

## P4. Two-parameter three-atom calibration

Let d>=2, rho uniform on [-1,1]^d, 0<a<1, and 0<a+s-|b|<=a+s+|b|<1, with the first inequality strict. Put

u=max(-x1,x1,a), v=max(-x1,x1,a+s+b*x2).

The central source intervals on slice x2=t have half-widths a and a+s+bt. Their masses are a and a+s; each pair of outer masses is respectively (1-a)/2 and (1-a-s)/2. The slopes are (-e1,0,e1) and (-e1,b*e2,e1).

Define H(s,b)=E|s+bU| for U uniform on [-1,1]. Elementary integration gives

H(s,b)=|s| if |s|>=|b| (including b=0), and H(s,b)=(s^2+b^2)/(2|b|) otherwise.

The first-coordinate squared map discrepancy is precisely the indicator of the central intervals' symmetric difference. The second-coordinate squared discrepancy is b^2 on the new central cell. These orthogonal contributions give the exact identity

F(a,s,b)=H(s,b)+(a+s)b^2.

Every target coupling incurs vertical cost (a+s)b^2. For s>=0, fix all common atom mass and move s/2 from each outer atom to the new center. For s<0, move -s/2 from the old center to each outer atom. The horizontal cost is |s|. Exact duals certify optimality: for s>=0 use alpha=(1,0,1), beta=(-1,b^2,-1); for s<0 use alpha=(-1,0,-1), beta=(1,b^2,1). Their inequalities can be checked in a 3x3 cost matrix. Consequently

W2(mu,nu)^2=|s|+(a+s)b^2.

The common-source coupling excess is therefore

F-W2^2 = 0 when |s|>=|b|;
F-W2^2 = (|b|-|s|)^2/(2|b|) when |s|<|b|.

This gives an exact criterion for when the overlay coupling is target-optimal. Setting s=0 and b=a/2 with 0<a<1/2 recovers the source example. No new claim to its one-third obstruction is made.

## P5. Exact worst-case interval certificate

Fix a, and let s and b range over a closed rectangle entirely inside the admissible region. For fixed b, H(s,b) is convex in s, and (a+s)b^2 is affine in s. For fixed s, H(s,b)=E|s+bU| is convex in b, and (a+s)b^2 is convex because a+s>0. Hence F is separately convex. First maximize in s at an endpoint, then in b at an endpoint. The exact maximum is attained at one of the rectangle's four corners. Joint convexity is neither needed nor asserted.

Admissibility can also be checked at the four corners: the positive functions a+s-|b| and 1-a-s-|b| have their minimum over the rectangle at a corner.

For the symmetric tilt interval s=0, b in [-B,B], the sharp global maximum is B/2+aB^2. The pointwise-box envelope of P3 is B+aB^2 (provided B<min(a,1-a)); its excess B/2 quantifies the loss from relaxing one global slope choice to pointwise independent choices. Thus the general checker can be safe without being sharp, while the specialized interval certificate retains the correlation exactly.

## P6. An adverse family: the two relaxations separated, one unbounded

Let K=[1,2]x[0,1] with uniform rho (|K|=1), u(x)=x1, and the comparison box with the fixed plane g_1(x)=x1 (all radii zero) and the uncertain plane g_2(x)=b x1+epsilon with nominal b=0, slope radius r_21=1 and the other radii zero, for a rational 0<=epsilon<=1. A realisation is v_b(x)=max{x1, b x1+epsilon} with one global b in [-1,1]. This family was supplied by the external review of version 0.1.0; the statements below are rederived here.

(i) Exact error. Put d=1-b in [0,2]. Plane 2 wins where d x1<epsilon. For d>0 its cell is {1<=x1<min(2,epsilon/d)}x[0,1], of mass (min(2,epsilon/d)-1)_+, and the squared slope discrepancy on it is (1-b)^2=d^2. Hence

F(u,v_b) = d^2 if 0<=d<=epsilon/2;  epsilon d-d^2 if epsilon/2<=d<=epsilon;  0 if d>=epsilon.

At d=0 (b=1) plane 2 has the reference slope, so T_v=T_u almost everywhere after merging and F=0, in agreement with the formula.

(ii) Sharp maximum. d^2 increases on [0,epsilon/2] and epsilon d-d^2 decreases on [epsilon/2,epsilon] (its derivative is epsilon-2d<=0), so sup_b F(u,v_b)=epsilon^2/4, attained only at the interior parameter b=1-epsilon/2 when epsilon>0, while both box endpoints b=-1 and b=1 give F=0. Consequently the corner reduction of P5 does not extend to general coefficient boxes: it used the separate convexity of the calibration family, which this family lacks.

(iii) Envelope. For every x in K, U_2(x)=epsilon+|x1|=x1+epsilon>=x1=L_1(x) and trivially U_2>=L_2, so 2 in J(x) everywhere. The cost M_12=(|1-0|+1)^2=4 and M_11=0, so the P3 integrand is 4 everywhere and B=4 for every epsilon in [0,1]; the slope-diameter baseline sum_i rho(C_i) max_j M_ij is also 4.

(iv) The two relaxations separated. At a point with x1 in (1,2), plane 2 wins for exactly those b with d x1<epsilon, that is b>1-epsilon/x1, and the supremum of its cost (1-b)^2 over these b is (epsilon/x1)^2 (approached as b decreases to the tie, which is excluded). The pointwise supremum that respects winner–slope compatibility but still lets b depend on x therefore integrates to epsilon^2 * integral_1^2 x1^{-2} dx1 = epsilon^2/2. Thus

epsilon^2/4 = sup_b F(u,v_b) <= epsilon^2/2 (pointwise, compatibility respected) <= 4 = B (pointwise, compatibility ignored).

The first inequality is the price of letting the parameter vary with x, a factor exactly 2 in this family; the second is the price of the unconditional slope maximum, a factor 8/epsilon^2. Only the second is unbounded here. The envelope-to-maximum ratio 16/epsilon^2 is unbounded as epsilon decreases with the slope radius fixed at one, and at epsilon=0 every realisation has F=0 while B=4. One arrangement region suffices, so the loss is unrelated to computational scale. This is a limitation of informativeness, not a counterexample to P3.

## P7. Tightness at small radius and a convergent refinement

Notation. Reference planes (a_i,c_i), i<=m, with distinct slopes; nominal comparison planes (b_j,d_j), j<=n (slopes may coincide), radii (r_j1,r_j2,r_j0)>=0, and r the largest radius entry. v denotes the nominal realisation (duplicate slopes merged, largest intercept kept); for the proof, the nominal winner k(x) at a point is an original index with the winning slope and the largest intercept among planes of that slope, so that J, M_ij and the pair count use original indices throughout; two original planes with equal slopes contribute nothing to the second bracket below because the cost difference vanishes. Let R_K=max_{x in K}(|x1|+|x2|+1), attained at a vertex; let D_K be any upper bound for the Euclidean diameter of K (the implementation uses the l1 vertex diameter); and let Lambda=max_{i,j} sum_{l=1,2}(|a_il-b_jl|+r_jl), an l1 bound for the distance between any reference slope and any realised comparison slope. Norms |.| on slopes are Euclidean.

**Theorem T (tightness).** 0 <= B - F(u,v) <= gamma(r) := 2 r Lambda + 2 r^2 + 4 r R_K D_K n(n-1) Lambda / |K|.

Proof. The lower inequality is P3 applied to the nominal realisation. For the upper one fix x in the interior of some C_i, off every nominal tie line (a full-measure set), and let k=k(x) be the nominal winner. The P3 integrand at x is max_{j in J(x)} M_ij and the realised integrand is |a_i-b_k|^2. For j in J(x) write

M_ij - |a_i-b_k|^2 = (M_ij - |a_i-b_j|^2) + (|a_i-b_j|^2 - |a_i-b_k|^2).

The first bracket equals sum_l (2 r_jl |a_il-b_jl| + r_jl^2) <= 2 r Lambda + 2 r^2. The second bracket vanishes for j=k. For j in J(x) with j != k, the membership U_j(x) >= L_k(x) gives g_k(x)-g_j(x) <= e_j(x)+e_k(x) <= 2 r R_K, and g_k(x) >= g_j(x) because k wins; so x lies in T_jk := {y in K : 0 <= g_k(y)-g_j(y) <= 2 r R_K}. Moreover |a_i-b_j|^2-|a_i-b_k|^2 = (b_k-b_j).(2a_i-b_j-b_k) <= |b_k-b_j| (|a_i-b_j|+|a_i-b_k|) <= 2 Lambda |b_k-b_j|, using Euclidean norms on the right and the fact that a Euclidean norm is at most the l1 norm bounded by Lambda. Hence the excess of the integrand at x is at most 2 r Lambda + 2 r^2 + sum_{j != k(x)} 1_{T_jk}(x) 2 Lambda |b_k-b_j|. Integrating over K (the C_i partition K up to null sets) gives

|K| (B - F(u,v)) <= (2 r Lambda + 2 r^2)|K| + sum over ordered pairs j != k of |T_jk| 2 Lambda |b_k-b_j|.

If b_j=b_k the pair contributes nothing. Otherwise T_jk is contained in the intersection of K with a closed strip of width 2 r R_K/|b_k-b_j| perpendicular to b_k-b_j, and a strip of width w meets a convex set of diameter at most D_K in area at most w D_K (integrate the chord lengths across the strip). So each pair contributes at most 4 r R_K D_K Lambda, there are at most n(n-1) ordered pairs, and dividing by |K| gives gamma(r). QED

Remarks. (a) Margins. Let mu(x) be the nominal margin: the winning value minus the largest competing value among planes with a different slope. Where mu(x) > 2 r R_K the set J(x) contains only planes with the winner's slope, and the excess is at most 2 r Lambda + 2 r^2; elsewhere it is at most max_{i,j} M_ij. So B - F(u,v) <= 2 r Lambda + 2 r^2 + (max_{i,j} M_ij) |{mu <= 2 r R_K}|/|K|. (b) Slope separation. The strip bound gives |{mu <= t}| <= D_K t sum over distinct-slope pairs 1/|b_k-b_j| <= n(n-1) D_K t/sigma, where sigma is the smallest distance between distinct comparison slopes; the uniform constant in Theorem T avoids sigma because the strip width and the cost difference are reciprocal in |b_k-b_j|. (c) With the l1 vertex diameter as D_K all quantities in gamma are rational for rational data (the exact Euclidean diameter of a rational polygon can be irrational); `tightness_bound` computes it and the test suite checks B - F(u,v) <= gamma on 108 random boxes.

**Theorem C (convergent box subdivision).** Let the box be covered by finitely many sub-boxes P (coordinate boxes of the same form, radii r_P), and let r_* = max_P max radius of P. Put UB = max_P B(P) and let LB be the largest value of F(u,.) over any finite set of realisations in the box that contains every sub-box centre. Then

LB <= sup over realisations in the box of F(u,.) <= UB,  and  UB - LB <= max_P [B(P) - F(u, v_{c(P)})] <= gamma_box(r_*),

where gamma_box(r) = 2 r Lambda_box + 2 r^2 + 4 r R_K D_K n(n-1) Lambda_box/|K| and Lambda_box is Lambda computed for the full box.

Proof. Every realisation lies in some P, so P3 for that sub-box gives F <= B(P) <= UB; LB is a maximum of feasible values. For the gap, UB - LB <= B(P*) - F(u, v_{c(P*)}) for a sub-box P* attaining UB, and Theorem T applies to P* with its own constant Lambda(P*) <= Lambda_box, because for a sub-interval [b'-r', b'+r'] of [b-r, b+r] one has |a-b'|+r' <= |a-b|+|b-b'|+r' <= |a-b|+r. QED

Algorithm. `refine_bound` keeps a best-first heap of sub-boxes ordered by their envelopes, splits the sub-box with the largest envelope along its widest coordinate, evaluates the exact F at each child centre and at the child's outer endpoint along the split coordinate (feasible realisations, which supply LB and the attaining realisation), and never splits a sub-box whose envelope is at most LB (pruning preserves the inequalities because such sub-boxes cannot exceed LB). It stops when the largest remaining envelope is at most LB, when UB - LB is within a requested tolerance, or when the box budget is exhausted; in every case it returns the valid interval [LB, UB], the number of sub-boxes evaluated and the stop reason. Termination within a positive tolerance tau: splitting the widest coordinate halves the largest radius of a lineage at least once every 3n splits, so every sub-box with gamma_box(radius) > tau lies at bounded depth and there are finitely many of them. Tolerance 0 requests exact convergence, which occurs only when a probe meets a maximiser (as in the tilt family, where the endpoint probes do); on the adverse family with epsilon=1/10 the maximiser b=19/20 is not dyadic, so no finite bisection from [-1,1] probes it and the loop ends by budget with a positive gap. The returned `attaining_coefficients` is a literal point of the n-plane box; `attaining_realization` is its merged equivalent. Uniform refinement needs a number of sub-boxes exponential in the box dimension 3n; the benchmark records this.

## Limits

The planar checker does not solve for potentials realizing arbitrary prescribed masses, does not certify nonuniform source density integrals, and does not claim scalable high-dimensional performance. The cube calibration extends in dimension by integrating out unused coordinates, not by a general-dimensional computational implementation. Historical novelty of the two-parameter formula and uncertainty certificate remains bounded by the documented search. The general-dimensional extension of P3 and P7 is immediate at the level of the proofs (the pointwise envelope reasoning does not use the dimension, and the strip bound has a slab analogue) but is not implemented; no concrete application justified a weighted or higher-dimensional integration backend in this version.
