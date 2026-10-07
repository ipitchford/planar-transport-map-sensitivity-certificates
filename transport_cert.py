"""Exact planar affine-max transport certificates. Original code: MIT.

Python standard library only. Arithmetic inputs are integers or rational strings;
binary floats are rejected. No optimizer's success flag is trusted.
"""
from fractions import Fraction as F
from itertools import product
import heapq


class CertificateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def q(value):
    require(isinstance(value, (str, int, F)) and not isinstance(value, bool),
            'use exact integers or rational strings, not floats')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CertificateError(f'malformed rational {value!r}: {error}') from None


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def area(poly):
    if len(poly) < 3:
        return F(0)
    return abs(sum((p[0]*r[1]-r[0]*p[1]
                    for p, r in zip(poly, poly[1:]+poly[:1])), F(0)))/2


def polygon(vertices):
    p = [tuple(map(q, v)) for v in vertices]
    require(len(p) >= 3 and all(len(v) == 2 for v in p), 'invalid polygon dimensions')
    require(len(set(p)) == len(p), 'repeated polygon vertices')
    require(area(p) > 0, 'zero polygon area')
    require(all(cross(a,b,c) >= 0 for a,b in zip(p,p[1:]+p[:1]) for c in p),
            'polygon must be convex and counterclockwise')
    return p


def planes(coefficients):
    result = [tuple(map(q, row)) for row in coefficients]
    require(bool(result), 'empty potential')
    require(all(len(row) == 3 for row in result), 'planes need x,y,intercept')
    require(len({row[:2] for row in result}) == len(result),
            'duplicate slopes: merge them, retaining the largest intercept')
    return result


def evaluate(line, x):
    return line[0]*x[0]+line[1]*x[1]+line[2]


def clip(poly, line):
    """Intersect an ordered convex polygon with line(x) >= 0."""
    if not poly:
        return []
    out = []
    for a,b in zip(poly, poly[1:]+poly[:1]):
        va, vb = evaluate(line,a), evaluate(line,b)
        if va >= 0:
            out.append(a)
        if (va < 0 < vb) or (vb < 0 < va):
            t = va/(va-vb)
            out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
    # A line through an existing vertex can create consecutive duplicates.
    clean = []
    for x in out:
        if not clean or x != clean[-1]:
            clean.append(x)
    if len(clean) > 1 and clean[-1] == clean[0]:
        clean.pop()
    return clean if area(clean) > 0 else []


def difference(a,b):
    return tuple(x-y for x,y in zip(a,b))


def cell(domain, potential, i):
    p = domain
    for j,g in enumerate(potential):
        if i != j:
            p = clip(p,difference(potential[i],g))
    return p


def squared_distance(x,y):
    return sum(((a-b)**2 for a,b in zip(x,y)), F(0))


def overlay(domain, first, second):
    """Return exact masses, overlap coupling, and squared map distance."""
    domain, first, second = polygon(domain), planes(first), planes(second)
    total = area(domain)
    a = [cell(domain, first, i) for i in range(len(first))]
    b = [cell(domain, second, j) for j in range(len(second))]
    m = [area(p)/total for p in a]
    n = [area(p)/total for p in b]
    require(sum(m) == sum(n) == 1, 'partition mass failure')
    coupling = []
    for p in a:
        coupling.append([area(cell(p,second,j))/total for j in range(len(second))])
    require(all(sum(row) == m[i] for i,row in enumerate(coupling)), 'row mass failure')
    require(all(sum(row[j] for row in coupling) == n[j] for j in range(len(n))),
            'column mass failure')
    distance = sum((coupling[i][j]*squared_distance(f[:2],g[:2])
                    for i,f in enumerate(first) for j,g in enumerate(second)), F(0))
    return dict(first_masses=m, second_masses=n, overlap=coupling, map_distance_squared=distance)


def check_target_witness(first_sites, second_sites, masses, other_masses,
                         coupling, alpha, beta):
    """Prove finite quadratic transport optimality by exact primal=dual."""
    x, y = [tuple(map(q,p)) for p in first_sites], [tuple(map(q,p)) for p in second_sites]
    m,n = list(map(q,masses)), list(map(q,other_masses))
    a,b = list(map(q,alpha)), list(map(q,beta))
    pi = [list(map(q,row)) for row in coupling]
    require(bool(x) and bool(y), 'empty target')
    require(all(len(p)==2 for p in x+y), 'sites must be planar')
    require(len(m)==len(a)==len(pi)==len(x), 'first dimension mismatch')
    require(len(n)==len(b)==len(y) and all(len(row)==len(y) for row in pi),
            'second dimension mismatch')
    require(all(z>=0 for z in m+n) and sum(m)==sum(n)==1, 'invalid masses')
    require(all(v>=0 for row in pi for v in row), 'negative coupling mass')
    require(all(sum(row)==m[i] for i,row in enumerate(pi)), 'wrong coupling row')
    require(all(sum(row[j] for row in pi)==n[j] for j in range(len(n))), 'wrong coupling column')
    cost = [[squared_distance(u,v) for v in y] for u in x]
    require(all(a[i]+b[j]<=cost[i][j] for i in range(len(x)) for j in range(len(y))),
            'infeasible transport dual')
    primal = sum((pi[i][j]*cost[i][j] for i in range(len(x)) for j in range(len(y))), F(0))
    dual = dot(m,a)+dot(n,b)
    require(primal==dual, 'nonzero optimality gap')
    return primal


def split(poly,line):
    values = [evaluate(line,x) for x in poly]
    if min(values)>=0 or max(values)<=0:
        return [poly]
    return [p for p in (clip(poly,line),clip(poly,tuple(-v for v in line))) if p]


def robust_bound(domain, reference, centers, radii, max_regions=100000):
    """Uniform bound over one global coefficient box (possibly conservative).

    On each orthant, U_j and L_j are affine envelopes. The arrangement of
    U_j-L_k identifies every pointwise-possible winner. A global parameter
    choice cannot exceed the resulting pointwise cost maximum.
    """
    domain, reference = polygon(domain), planes(reference)
    centers = [tuple(map(q,row)) for row in centers]
    radii = [tuple(map(q,row)) for row in radii]
    require(bool(centers) and len(centers)==len(radii), 'box dimensions')
    require(all(len(row)==3 for row in centers+radii), 'box planes need three coefficients')
    require(all(v>=0 for row in radii for v in row), 'negative radius')
    total, bound, regions = area(domain), F(0), 0
    for i,f in enumerate(reference):
        base = cell(domain,reference,i)
        costs = [sum(((abs(f[k]-g[k])+r[k])**2 for k in range(2)),F(0))
                 for g,r in zip(centers,radii)]
        for sx,sy in product((-1,1),repeat=2):
            p = clip(clip(base,(F(sx),F(0),F(0))),(F(0),F(sy),F(0)))
            if not p:
                continue
            e = [(sx*r[0],sy*r[1],r[2]) for r in radii]
            upper = [tuple(g[k]+z[k] for k in range(3)) for g,z in zip(centers,e)]
            lower = [difference(g,z) for g,z in zip(centers,e)]
            lines = [difference(u,l) for u in upper for l in lower]
            parts = [p]
            for line in lines:
                parts = [piece for part in parts for piece in split(part,line)]
                require(len(parts)+regions<=max_regions, 'region safety limit reached; no certificate returned')
            for part in parts:
                midpoint = tuple(sum((v[k] for v in part),F(0))/len(part) for k in range(2))
                possible = [j for j,u in enumerate(upper)
                            if all(evaluate(difference(u,l),midpoint)>=0 for l in lower)]
                require(bool(possible), 'no possible winner')
                bound += area(part)*max(costs[j] for j in possible)/total
            regions += len(parts)
    return dict(map_distance_squared_upper=bound, arrangement_regions=regions)


def tilt_family(a,s,b):
    a,s,b = q(a),q(s),q(b)
    require(0<a<1 and 0<a+s-abs(b) and a+s+abs(b)<1, 'tilted strip leaves the cube')
    h = abs(s) if abs(s)>=abs(b) else (s*s+b*b)/(2*abs(b))
    first = [(F(-1),F(0),F(0)), (F(0),F(0),a), (F(1),F(0),F(0))]
    second = [(F(-1),F(0),F(0)), (F(0),b,a+s), (F(1),F(0),F(0))]
    m = [(1-a)/2,a,(1-a)/2]
    n = [(1-a-s)/2,a+s,(1-a-s)/2]
    pi = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        pi[i][i] = min(m[i],n[i])
    if s>=0:
        pi[0][1] = pi[2][1] = s/2
        alpha, beta = [F(1),F(0),F(1)], [F(-1),b*b,F(-1)]
    else:
        pi[1][0] = pi[1][2] = -s/2
        alpha, beta = [F(-1),F(0),F(-1)], [F(1),b*b,F(1)]
    return dict(first=first,second=second,masses=m,other_masses=n,
                coupling=pi,alpha=alpha,beta=beta,
                map_squared=h+(a+s)*b*b,target_squared=abs(s)+(a+s)*b*b,
                excess=h-abs(s))


def tilt_box_max(a,s_interval,b_interval):
    """Exact maximum by separate convexity; validity checked at all corners."""
    a = q(a)
    require(len(s_interval)==len(b_interval)==2, 'two endpoints required')
    ss,bb = tuple(map(q,s_interval)),tuple(map(q,b_interval))
    require(ss[0]<=ss[1] and bb[0]<=bb[1], 'reversed interval')
    values = [(tilt_family(a,s,b)['map_squared'],s,b) for s,b in product(ss,bb)]
    value,s,b = max(values)
    return dict(maximum_map_squared=value,attaining_s=s,attaining_b=b)


def merge_planes(coefficients):
    """Merge planes with identical slopes, retaining the largest intercept.

    Order of first occurrence is kept. The result is a valid `planes()` input.
    """
    rows = [tuple(map(q, row)) for row in coefficients]
    require(bool(rows) and all(len(row) == 3 for row in rows), 'planes need x,y,intercept')
    best, order = {}, []
    for row in rows:
        key = row[:2]
        if key not in best:
            order.append(key)
            best[key] = row[2]
        else:
            best[key] = max(best[key], row[2])
    return [(key[0], key[1], best[key]) for key in order]


def baseline_bound(domain, reference, centers, radii):
    """Elementary slope-diameter bound: sum_i rho(C_i) max_j M_ij (no winner screening)."""
    domain, reference = polygon(domain), planes(reference)
    centers = [tuple(map(q, row)) for row in centers]
    radii = [tuple(map(q, row)) for row in radii]
    require(bool(centers) and len(centers) == len(radii), 'box dimensions')
    require(all(len(row) == 3 for row in centers+radii), 'box planes need three coefficients')
    require(all(v >= 0 for row in radii for v in row), 'negative radius')
    total, bound = area(domain), F(0)
    for i, f in enumerate(reference):
        mass = area(cell(domain, reference, i))/total
        costs = [sum(((abs(f[k]-g[k])+r[k])**2 for k in range(2)), F(0))
                 for g, r in zip(centers, radii)]
        bound += mass*max(costs)
    return bound


def tightness_bound(domain, reference, centers, radii):
    """Explicit constant gamma(r) with  B(box) - F(u, v_centre) <= gamma  (Theorem: tightness).

    r is the largest radius; Lambda bounds the l1 slope distance between any reference
    slope and any realised comparison slope; R_K = max over K of |x1|+|x2|+1; D_K is the
    l1 diameter of K (an upper bound for its Euclidean diameter). All quantities are rational.
    """
    domain, reference = polygon(domain), planes(reference)
    centers = [tuple(map(q, row)) for row in centers]
    radii = [tuple(map(q, row)) for row in radii]
    require(bool(centers) and len(centers) == len(radii), 'box dimensions')
    require(all(len(row) == 3 for row in centers+radii), 'box planes need three coefficients')
    require(all(v >= 0 for row in radii for v in row), 'negative radius')
    r = max(v for row in radii for v in row)
    lam = max(sum((abs(f[k]-g[k])+rad[k] for k in range(2)), F(0))
              for f in reference for g, rad in zip(centers, radii))
    big_r = max(abs(v[0])+abs(v[1])+1 for v in domain)
    diam = max(abs(a[0]-b[0])+abs(a[1]-b[1]) for a in domain for b in domain)
    n = len(centers)
    gamma = 2*r*lam + 2*r*r + 4*r*big_r*diam*n*(n-1)*lam/area(domain)
    return dict(gamma=gamma, radius=r, lam=lam, R_K=big_r, D_K=diam, planes=n)


def refine_bound(domain, reference, centers, radii, max_boxes=64, tolerance=None,
                 max_regions=100000):
    """Convergent box subdivision: certified interval for sup over the box of F.

    `lower` is F at an explicit point of the coefficient box (a sub-box centre
    or an endpoint probe): `attaining_coefficients` is that literal n-plane
    coefficient tuple and `attaining_realization` its merged equivalent (the
    planes actually evaluated). `upper` is the largest envelope among the
    sub-boxes still able to exceed `lower`. Both inequalities hold at every
    budget. A sub-box is split along its widest coordinate; the enclosure
    converges linearly in the sub-box radius (Theorem: tightness), so every
    positive tolerance is reached in finitely many splits; tolerance 0 asks
    for exact convergence, which happens only when a probe meets a maximiser
    (otherwise the budget stops the loop). The routine never returns a partial
    sum as a bound, and exhausting `max_boxes` widens the interval instead of
    lying.
    """
    domain, reference = polygon(domain), planes(reference)
    cen = [tuple(map(q, row)) for row in centers]
    rad = [tuple(map(q, row)) for row in radii]
    require(bool(cen) and len(cen) == len(rad), 'box dimensions')
    require(all(len(row) == 3 for row in cen+rad), 'box planes need three coefficients')
    require(all(v >= 0 for row in rad for v in row), 'negative radius')
    require(isinstance(max_boxes, int) and not isinstance(max_boxes, bool) and max_boxes >= 1,
            'max_boxes must be a positive integer')
    tol = None if tolerance is None else q(tolerance)
    require(tol is None or tol >= 0, 'negative tolerance')
    regions = 0

    def shifted(c, j, k, delta):
        return [tuple(c[jj][kk]+(delta if (jj, kk) == (j, k) else 0) for kk in range(3))
                for jj in range(len(c))]

    def evaluate(c, r, probes):
        """Envelope of the sub-box, plus exact F at its centre and at the probe realisations."""
        nonlocal regions
        out = robust_bound(domain, reference, c, r, max_regions=max_regions)
        regions += out['arrangement_regions']
        best, best_point, best_real = None, None, None
        for point in [c]+probes:
            realised = merge_planes(point)
            value = overlay(domain, reference, realised)['map_distance_squared']
            if best is None or value > best:
                best, best_point, best_real = value, point, realised
        return out['map_distance_squared_upper'], best_point, best_real, best

    root_probes = [shifted(cen, j, k, sign*rad[j][k]) for j in range(len(rad)) for k in range(3)
                   if rad[j][k] > 0 for sign in (-1, 1)]
    upper0, attaining_point, attaining, lower = evaluate(cen, rad, root_probes)
    evaluated, counter = 1, 0
    heap = [(-upper0, counter, cen, rad)]
    reason = 'converged'
    while heap:
        top = -heap[0][0]
        if top <= lower:
            reason = 'converged'
            break
        if tol is not None and top-lower <= tol:
            reason = 'tolerance'
            break
        if evaluated+2 > max_boxes:
            reason = 'budget'
            break
        _, _, c, r = heapq.heappop(heap)
        j, k = max(((jj, kk) for jj in range(len(r)) for kk in range(3)), key=lambda t: r[t[0]][t[1]])
        if r[j][k] == 0:
            # A point box: its envelope equals the exact discrepancy, already in `lower`.
            continue
        half = r[j][k]/2
        for sign in (-1, 1):
            child_c = [tuple(c[jj][kk]+(sign*half if (jj, kk) == (j, k) else 0) for kk in range(3))
                       for jj in range(len(c))]
            child_r = [tuple(half if (jj, kk) == (j, k) else r[jj][kk] for kk in range(3))
                       for jj in range(len(r))]
            # Probe the child's outer endpoint along the split coordinate: a feasible realisation.
            ub, point, realised, lb = evaluate(child_c, child_r, [shifted(child_c, j, k, sign*half)])
            evaluated += 1
            if lb > lower:
                lower, attaining_point, attaining = lb, point, realised
            counter += 1
            heapq.heappush(heap, (-ub, counter, child_c, child_r))
    upper = max([lower]+[-h[0] for h in heap])
    gap = upper-lower
    converged = gap <= tol if tol is not None else gap == 0
    return dict(lower=lower, upper=upper, gap=gap, attaining_coefficients=attaining_point,
                attaining_realization=attaining, boxes_evaluated=evaluated,
                arrangement_regions=regions, converged=converged, stop_reason=reason)


def loose_family(epsilon):
    """Admissible box on K=[1,2]x[0,1] whose envelope is 4 while sup F = epsilon^2/4.

    u(x)=x1 and v_b(x)=max{x1, b*x1+epsilon} with one global b in [-1,1]. Both
    coefficient-box endpoints give F=0; the maximum is interior at b=1-epsilon/2.
    """
    e = q(epsilon)
    require(0 <= e <= 1, 'epsilon must lie in [0,1]')
    return dict(domain=[(F(1), F(0)), (F(2), F(0)), (F(2), F(1)), (F(1), F(1))],
                reference=[(F(1), F(0), F(0))],
                centers=[(F(1), F(0), F(0)), (F(0), F(0), e)],
                radii=[(F(0), F(0), F(0)), (F(1), F(0), F(0))],
                supremum=e*e/4, attaining_b=1-e/2, conditioned_integral=e*e/2,
                envelope=F(4))


def loose_error(epsilon, b):
    """Exact F(u, v_b) for the loose family, by the piecewise formula."""
    e, b = q(epsilon), q(b)
    require(0 <= e <= 1 and -1 <= b <= 1, 'parameters outside the loose family')
    d = 1-b
    if d <= e/2:
        return d*d
    if d <= e:
        return e*d-d*d
    return F(0)
