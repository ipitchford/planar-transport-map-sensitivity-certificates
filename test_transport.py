"""Exact internal tests; finite cases corroborate, but do not prove P1--P5."""
import json
import random
import time
import unittest
from fractions import Fraction as F
from itertools import combinations, product

from transport_cert import (CertificateError, area, cross, difference, evaluate,
    overlay, polygon, robust_bound, squared_distance, tilt_box_max, tilt_family,
    check_target_witness, merge_planes, baseline_bound, tightness_bound, refine_bound,
    loose_family, loose_error, q)

SQUARE = [(-1,-1),(1,-1),(1,1),(-1,1)]


def halfplanes(poly):
    # Positive oriented-edge cross product: (a_y-b_y)x+(b_x-a_x)y+...>=0.
    return [(a[1]-b[1], b[0]-a[0], a[0]*b[1]-a[1]*b[0])
            for a,b in zip(poly,poly[1:]+poly[:1])]


def vertex_area(lines):
    """Independent algorithm: pairwise line intersections then exact hull.

    Does not call the production polygon clipping implementation.
    """
    points = set()
    for a,b in combinations(lines,2):
        det = a[0]*b[1]-a[1]*b[0]
        if not det:
            continue
        x = (a[1]*b[2]-a[2]*b[1])/det
        y = (a[2]*b[0]-a[0]*b[2])/det
        p = (x,y)
        if all(evaluate(line,p)>=0 for line in lines):
            points.add(p)
    points = sorted(points)
    if len(points)<3:
        return F(0)
    lower, upper = [], []
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1]+upper[:-1]
    # Separate determinant sum, not production area().
    return abs(sum((u[0]*v[1]-u[1]*v[0]
                    for u,v in zip(hull,hull[1:]+hull[:1])),F(0)))/2


def independent_distance(domain, first, second):
    poly = polygon(domain)
    first = [tuple(map(F,row)) for row in first]
    second = [tuple(map(F,row)) for row in second]
    constraints = halfplanes(poly)
    total = vertex_area(constraints)
    answer = F(0)
    for i,f in enumerate(first):
        for j,g in enumerate(second):
            lines = constraints+[difference(f,h) for k,h in enumerate(first) if i!=k]
            lines += [difference(g,h) for k,h in enumerate(second) if j!=k]
            answer += vertex_area(lines)*squared_distance(f[:2],g[:2])/total
    return answer


class TransportTests(unittest.TestCase):
    def test_tilt_grid_exact(self):
        for a,s,b in product((F(1,4),F(1,3),F(1,2)),
                              (F(-1,16),F(0),F(1,16)),
                              (F(-1,8),F(-1,16),F(0),F(1,16),F(1,8))):
            f = tilt_family(a,s,b)
            result = overlay(SQUARE,f['first'],f['second'])
            self.assertEqual(result['first_masses'],f['masses'])
            self.assertEqual(result['second_masses'],f['other_masses'])
            self.assertEqual(result['map_distance_squared'],f['map_squared'])
            self.assertEqual(independent_distance(SQUARE,f['first'],f['second']),f['map_squared'])
            target = check_target_witness([p[:2] for p in f['first']], [p[:2] for p in f['second']],
                result['first_masses'],result['second_masses'],f['coupling'],f['alpha'],f['beta'])
            self.assertEqual(target,f['target_squared'])
            expected_gap = F(0) if abs(s)>=abs(b) else (abs(b)-abs(s))**2/(2*abs(b))
            self.assertEqual(f['map_squared']-target,expected_gap)

    def test_generic_overlay_two_algorithms(self):
        rng = random.Random(374)
        domains = [SQUARE,[(0,0),(3,0),(0,2)],[(0,0),(3,0),(4,2),(2,3),(-1,2)]]
        for domain in domains:
            for _ in range(8):
                slopes = rng.sample(list(product(range(-3,4),repeat=2)),8)
                ps = [tuple(map(F,(*p,rng.randint(-3,3)))) for p in slopes]
                result = overlay(domain,ps[:4],ps[4:])
                self.assertEqual(result['map_distance_squared'],independent_distance(domain,ps[:4],ps[4:]))
                self.assertEqual(overlay(domain,ps[4:],ps[:4])['map_distance_squared'],result['map_distance_squared'])

    def test_shift_and_relabel(self):
        f = tilt_family(F(1,3),F(1,16),F(1,8))
        base = overlay(SQUARE,f['first'],f['second'])['map_distance_squared']
        moved = [[(p[0]+7,p[1]-9,p[2]+c) for p in f[key]]
                 for key,c in [('first',13),('second',-21)]]
        self.assertEqual(overlay(SQUARE,moved[0][::-1],moved[1])['map_distance_squared'],base)

    def test_zero_box_is_exact(self):
        first = [(-1,0,0),(0,0,'1/3'),(1,0,0)]
        second = [(-1,0,0),(0,'1/8','5/16'),(1,0,0),(0,-1,-2)]
        result = robust_bound(SQUARE,first,second,[(0,0,0)]*4)
        self.assertEqual(result['map_distance_squared_upper'],overlay(SQUARE,first,second)['map_distance_squared'])
        self.assertEqual(robust_bound(SQUARE,first,first,[(0,0,0)]*3)['map_distance_squared_upper'],0)

    def test_degenerate_cells_and_coincident_uncertain_planes(self):
        reference = [(0,0,0),(1,0,-2)]  # second reference cell is empty
        coincident = [(0,0,0),(0,0,0)]
        result = robust_bound(SQUARE,reference,coincident,[(0,0,0)]*2)
        self.assertEqual(result['map_distance_squared_upper'],0)
        # The public overlay routine requires explicit duplicate-slope merging.
        self.assertEqual(overlay(SQUARE,reference,[(0,0,0)])['first_masses'],[1,0])

    def test_global_versus_pointwise_uncertainty(self):
        a,B = F(1,3),F(1,8)
        f = tilt_family(a,0,0)
        result = robust_bound(SQUARE,f['first'],f['first'],[(0,0,0),(0,B,0),(0,0,0)])
        exact = tilt_box_max(a,(0,0),(-B,B))['maximum_map_squared']
        self.assertEqual(exact,B/2+a*B*B)
        self.assertEqual(result['map_distance_squared_upper'],B+a*B*B)
        self.assertEqual(result['map_distance_squared_upper']-exact,B/2)

    def test_general_box_samples(self):
        first = [(-1,0,0),(1,0,0),(0,1,'1/3')]
        centers = [(-1,0,0),(1,0,0),(0,1,'1/4')]
        radii = [(F(1,32),F(1,32),F(1,16))]*3
        bound = robust_bound(SQUARE,first,centers,radii)['map_distance_squared_upper']
        rng = random.Random(276)
        for _ in range(32):
            realization = [tuple(F(c)+r*F(rng.randint(-4,4),4) for c,r in zip(p,rad))
                           for p,rad in zip(centers,radii)]
            self.assertLessEqual(overlay(SQUARE,first,realization)['map_distance_squared'],bound)
        self.assertGreater(bound,0)

    def test_corner_maximum_grid(self):
        a = F(1,3)
        ss,bb = (F(-1,16),F(1,8)),(F(-1,8),F(1,16))
        exact = tilt_box_max(a,ss,bb)
        values = [tilt_family(a,ss[0]+i*(ss[1]-ss[0])/12,bb[0]+j*(bb[1]-bb[0])/12)['map_squared']
                  for i,j in product(range(13),repeat=2)]
        self.assertEqual(max(values),exact['maximum_map_squared'])


    def test_malformed_rationals_are_refused(self):
        for bad in ('1/0', '0/0', 'abc', '1/2/3'):
            with self.assertRaisesRegex(CertificateError, 'malformed rational'):
                q(bad)
            with self.assertRaises(CertificateError):
                overlay(SQUARE, [(bad, 0, 0)], [(0, 0, 0)])
        for bad in (0.5, True, None):
            with self.assertRaises(CertificateError):
                q(bad)

    def test_merge_planes(self):
        merged = merge_planes([(1, 0, '1/3'), (0, 1, 2), (1, 0, 1), (0, 1, -5), (2, 2, 0)])
        self.assertEqual(merged, [(1, 0, 1), (0, 1, 2), (2, 2, 0)])
        self.assertEqual(overlay(SQUARE, [(0, 0, 0)], merged)['second_masses'],
                         overlay(SQUARE, [(0, 0, 0)], [(1, 0, 1), (0, 1, 2), (2, 2, 0)])['second_masses'])
        with self.assertRaises(CertificateError):
            merge_planes([])

    def test_loose_family_two_relaxations(self):
        # Theorem (adverse family): envelope 4 for every epsilon, sharp maximum epsilon^2/4
        # at the interior parameter b=1-epsilon/2, zero error at both box endpoints.
        for eps in (F(1, 2), F(1, 10), F(1, 100), F(0)):
            f = loose_family(eps)
            env = robust_bound(f['domain'], f['reference'], f['centers'], f['radii'])
            self.assertEqual(env['map_distance_squared_upper'], 4)
            self.assertEqual(baseline_bound(f['domain'], f['reference'], f['centers'], f['radii']), 4)
            for b in [F(i, 50) for i in range(-50, 51)]+[f['attaining_b']]:
                realised = merge_planes([(1, 0, 0), (b, 0, eps)])
                exact = overlay(f['domain'], f['reference'], realised)['map_distance_squared']
                self.assertEqual(exact, loose_error(eps, b))
                self.assertLessEqual(exact, f['supremum'])
            self.assertEqual(loose_error(eps, f['attaining_b']), f['supremum'])
            self.assertEqual(loose_error(eps, -1), 0)
            self.assertEqual(loose_error(eps, 1), 0)

    def test_refinement_is_certified_and_converges(self):
        f = loose_family(F(1, 10))
        previous = None
        for budget in (8, 64, 512):
            out = refine_bound(f['domain'], f['reference'], f['centers'], f['radii'], max_boxes=budget)
            self.assertLessEqual(out['lower'], f['supremum'])
            self.assertLessEqual(f['supremum'], out['upper'])
            # The lower bound is attained by the returned explicit realisation.
            self.assertEqual(overlay(f['domain'], f['reference'], out['attaining_realization'])['map_distance_squared'],
                             out['lower'])
            # The literal coefficient tuple lies in the box and merges to the evaluated planes.
            point = out['attaining_coefficients']
            self.assertEqual(len(point), len(f['centers']))
            for row, c, r in zip(point, f['centers'], f['radii']):
                self.assertTrue(all(abs(row[k]-c[k]) <= r[k] for k in range(3)))
            self.assertEqual(merge_planes(point), out['attaining_realization'])
            self.assertLessEqual(out['boxes_evaluated'], budget)
            if previous is not None:
                self.assertLessEqual(out['upper'], previous['upper'])
                self.assertGreaterEqual(out['lower'], previous['lower'])
            previous = out
        self.assertLess(previous['upper'], F(1, 400)+F(1, 100000))
        self.assertGreater(previous['lower'], F(1, 400)-F(1, 100000))
        # Tolerance stop: a certified interval at least as narrow as requested.
        out = refine_bound(f['domain'], f['reference'], f['centers'], f['radii'],
                           max_boxes=4096, tolerance=F(1, 10000))
        self.assertTrue(out['converged'])
        self.assertLessEqual(out['gap'], F(1, 10000))
        # Tilt family: the sharp corner maximum is bracketed and the envelope gap B/2 is closed.
        a, B = F(1, 3), F(1, 8)
        g = tilt_family(a, 0, 0)
        exact = tilt_box_max(a, (0, 0), (-B, B))['maximum_map_squared']
        out = refine_bound(SQUARE, g['first'], g['first'], [(0, 0, 0), (0, B, 0), (0, 0, 0)], max_boxes=64)
        self.assertEqual(out['lower'], exact)
        self.assertEqual(out['upper'], exact)
        self.assertTrue(out['converged'])
        # One-shot iterators are materialised once (reviewer finding), and tolerance 0 is accepted.
        out = refine_bound(iter(SQUARE), iter(g['first']), g['first'], [(0, 0, 0), (0, B, 0), (0, 0, 0)],
                           max_boxes=8, tolerance=0)
        self.assertEqual((out['lower'], out['upper']), (exact, exact))
        with self.assertRaises(CertificateError):
            refine_bound(SQUARE, g['first'], g['first'], [(0, 0, 0)]*3, max_boxes=0)
        with self.assertRaises(CertificateError):
            refine_bound(SQUARE, g['first'], g['first'], [(0, 0, 0)]*3, tolerance='-1')

    def test_tightness_theorem_on_random_boxes(self):
        # B(box) - F(u, v_centre) <= gamma(r): a falsification test of the stated constant.
        rng = random.Random(149)
        domains = [SQUARE, [(0, 0), (3, 0), (0, 2)], [(0, 0), (3, 0), (4, 2), (2, 3), (-1, 2)]]
        checked = 0
        for domain in domains:
            for n in (2, 3, 4):
                for _ in range(4):
                    slopes = rng.sample(list(product(range(-3, 4), repeat=2)), 2*n)
                    ref = [(F(a), F(b), F(rng.randint(-3, 3))) for a, b in slopes[:n]]
                    cen = [(F(a), F(b), F(rng.randint(-3, 3))) for a, b in slopes[n:]]
                    for r in (F(1, 64), F(1, 8), F(1, 2)):
                        rad = [tuple(r*F(rng.randint(0, 4), 4) for _ in range(3)) for _ in range(n)]
                        env = robust_bound(domain, ref, cen, rad)['map_distance_squared_upper']
                        exact = overlay(domain, ref, merge_planes(cen))['map_distance_squared']
                        gamma = tightness_bound(domain, ref, cen, rad)['gamma']
                        self.assertLessEqual(exact, env)
                        self.assertLessEqual(env-exact, gamma)
                        self.assertLessEqual(env, baseline_bound(domain, ref, cen, rad))
                        checked += 1
        self.assertEqual(checked, 108)

    def test_negative_controls(self):
        f = tilt_family(F(1,3),0,F(1,8))
        result = overlay(SQUARE,f['first'],f['second'])
        args = [[p[:2] for p in f['first']],[p[:2] for p in f['second']],f['masses'],f['other_masses']]
        # Feasible but nonoptimal common-source coupling must not pass as target optimum.
        with self.assertRaisesRegex(CertificateError,'optimality gap'):
            check_target_witness(*args,result['overlap'],f['alpha'],f['beta'])
        corrupted = [row[:] for row in f['coupling']]
        corrupted[0][0] += F(1,1000)
        with self.assertRaises(CertificateError):
            check_target_witness(*args,corrupted,f['alpha'],f['beta'])
        with self.assertRaisesRegex(CertificateError,'dual'):
            check_target_witness(*args,f['coupling'],[99,0,1],f['beta'])
        with self.assertRaises(CertificateError):
            overlay(SQUARE,[(0.1,0,0)],[(0,0,0)])
        with self.assertRaises(CertificateError):
            overlay(SQUARE,[(0,0,0),(0,0,1)],[(0,0,0)])
        with self.assertRaisesRegex(CertificateError,'empty potential'):
            robust_bound(SQUARE,iter(()),[(0,0,0)],[(0,0,0)])
        with self.assertRaisesRegex(CertificateError,'empty potential'):
            robust_bound(SQUARE,[],[(0,0,0)],[(0,0,0)])
        with self.assertRaises(CertificateError):
            overlay(SQUARE[::-1],[(0,0,0)],[(1,0,0)])
        with self.assertRaises(CertificateError):
            tilt_family(F(1,3),0,F(1,2))
        with self.assertRaises(CertificateError):
            robust_bound(SQUARE,f['first'],f['second'],[(0,-1,0)]*3)
        with self.assertRaisesRegex(CertificateError,'limit'):
            robust_bound(SQUARE,f['first'],f['second'],[(1,1,1)]*3,max_regions=1)


if __name__=='__main__':
    start=time.monotonic()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TransportTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps(dict(passed=result.wasSuccessful(),tests=result.testsRun,
        seconds=round(time.monotonic()-start,4),tilt_cases=45,generic_two_algorithm_cases=24,
        uncertainty_sample_cases=32,corner_grid_cases=169,loose_grid_cases=4*102,tightness_cases=108,
        caveat='Finite tests plus written proofs; not formal verification or external review.')))
    raise SystemExit(0 if result.wasSuccessful() else 1)
