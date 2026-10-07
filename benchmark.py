"""Bounded synthetic benchmark of the coefficient-box certificates (MIT).

Compares, on exact rational inputs: the elementary slope-diameter baseline
B0 = sum_i rho(C_i) max_j M_ij, the possible-winner envelope of Theorem 2, the
certified refinement interval [lower, upper] of the box-subdivision routine
at a fixed box budget, and, where available, the exact robust maximum.
Records arrangement regions, wall time, process peak memory and refusals.

    python3 benchmark.py                  # writes evidence/benchmark.json
    python3 benchmark.py --check          # recomputes every exact field and compares
    python3 benchmark.py --table          # writes paper/benchmark_*.tex from the JSON

Wall times and memory are observations on one machine, not performance claims.
"""
import argparse
import json
import platform
import random
import resource
import sys
import time
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from transport_cert import (CertificateError, baseline_bound, loose_family, overlay,
                            refine_bound, robust_bound, tilt_box_max, tilt_family)

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'evidence'/'benchmark.json'
TABLES = (ROOT/'paper'/'benchmark_exact.tex', ROOT/'paper'/'benchmark_generic.tex')
SQUARE = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
TRIANGLE = [(0, 0), (3, 0), (0, 2)]
PENTAGON = [(0, 0), (3, 0), (4, 2), (2, 3), (-1, 2)]
POLYGONS = {'square': SQUARE, 'triangle': TRIANGLE, 'pentagon': PENTAGON}
EXACT_FIELDS = ('envelope', 'baseline', 'lower', 'upper', 'exact', 'regions', 'refine_regions',
                'boxes', 'refusal', 'stop_reason')


def enc(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: enc(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [enc(v) for v in value]
    return value


def rss_mb():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(peak/(2**20 if sys.platform == 'darwin' else 2**10), 1)


def timed(function, *args, **kwargs):
    start = time.perf_counter()
    value = function(*args, **kwargs)
    return value, round(time.perf_counter()-start, 4)


def measure(label, domain, reference, centers, radii, budget, exact=None, max_regions=100000):
    record = dict(case=label, planes=len(centers), exact=exact, refusal=None)
    try:
        env, t_env = timed(robust_bound, domain, reference, centers, radii, max_regions=max_regions)
    except CertificateError as error:
        record.update(refusal=str(error), envelope=None, baseline=baseline_bound(domain, reference, centers, radii),
                      lower=None, upper=None, regions=None, refine_regions=None, boxes=None, stop_reason=None,
                      seconds_envelope=None, seconds_refine=None, peak_rss_mb=rss_mb())
        return record
    base = baseline_bound(domain, reference, centers, radii)
    if budget:
        ref, t_ref = timed(refine_bound, domain, reference, centers, radii, max_boxes=budget, max_regions=max_regions)
        lower, upper, rr, boxes, stop = (ref['lower'], ref['upper'], ref['arrangement_regions'],
                                         ref['boxes_evaluated'], ref['stop_reason'])
    else:
        lower = overlay(domain, reference, centers)['map_distance_squared']
        upper, rr, boxes, stop, t_ref = env['map_distance_squared_upper'], None, 0, 'not-run', None
    record.update(envelope=env['map_distance_squared_upper'], baseline=base, lower=lower, upper=upper,
                  regions=env['arrangement_regions'], refine_regions=rr, boxes=boxes, stop_reason=stop,
                  seconds_envelope=t_env, seconds_refine=t_ref, peak_rss_mb=rss_mb())
    return record


def dyadic(rng, bits):
    return F(rng.randint(-(2**bits), 2**bits), 2**bits) if bits else F(0)


def generic_case(rng, n, bits):
    slopes = rng.sample(list(product(range(-3, 4), repeat=2)), 2*n)
    rows = [(F(a)+dyadic(rng, bits), F(b)+dyadic(rng, bits), F(rng.randint(-3, 3))+dyadic(rng, bits))
            for a, b in slopes]
    return rows[:n], rows[n:]


def run():
    cases = []
    for a, B in product((F(1, 4), F(1, 3), F(1, 2)), (F(1, 32), F(1, 16), F(1, 8))):
        g = tilt_family(a, 0, 0)
        exact = tilt_box_max(a, (0, 0), (-B, B))['maximum_map_squared']
        cases.append(measure(f'tilt a={a} B={B}', SQUARE, g['first'], g['first'],
                             [(0, 0, 0), (0, B, 0), (0, 0, 0)], 32, exact=exact))
    for eps in (F(1, 2), F(1, 10), F(1, 100)):
        f = loose_family(eps)
        for budget in (64, 256):
            cases.append(measure(f'loose eps={eps} budget={budget}', f['domain'], f['reference'],
                                 f['centers'], f['radii'], budget, exact=f['supremum']))
    rng = random.Random(374)
    for name, domain in POLYGONS.items():
        for n in (2, 3, 4, 6, 8):
            ref, cen = generic_case(rng, n, 0)
            for r in (F(1, 64), F(1, 16), F(1, 4)):
                budget = 32 if n <= 6 else 8
                cases.append(measure(f'generic {name} n={n} r={r}', domain, ref, cen, [(r, r, r)]*n, budget))
    for bits in (8, 20):
        ref, cen = generic_case(rng, 4, bits)
        cases.append(measure(f'generic square n=4 r=1/16 bits={bits}', SQUARE, ref, cen, [(F(1, 16),)*3]*4, 32))
    ref, cen = generic_case(rng, 4, 0)
    inactive = cen+[(F(0), F(0), F(-100))]
    cases.append(measure('generic square n=4+inactive r=1/16', SQUARE, ref, inactive, [(F(1, 16),)*3]*5, 32))
    near = cen+[(cen[0][0]+F(1, 2**20), cen[0][1], cen[0][2])]
    cases.append(measure('generic square n=4+near-coincident r=1/16', SQUARE, ref, near, [(F(1, 16),)*3]*5, 32))
    ref, cen = generic_case(rng, 8, 0)
    cases.append(measure('refusal pentagon n=8 r=1/4 cap=100', PENTAGON, ref, cen, [(F(1, 4),)*3]*8, 0,
                         max_regions=100))
    return dict(schemaVersion='1.0', python=sys.version.split()[0], platform=platform.platform(),
                boundary='Single-machine observations on exact rational inputs; wall time and process '
                         'peak memory are not performance claims. Region counts and bounds are exact.',
                cases=cases)


def table(data):
    """Aggregate the recorded cases into the two manuscript tables (booktabs rows)."""
    def fr(values, digits=2):
        values = [float(v) for v in values if v is not None]
        if not values:
            return '--'
        lo, hi = min(values), max(values)
        fmt = lambda v: f'{v:.{digits}f}' if v < 1000 else f'{v:.0f}'
        return fmt(lo) if fmt(lo) == fmt(hi) else f'{fmt(lo)}--{fmt(hi)}'
    exact_rows, generic_rows = [], []
    groups = {}
    for c in data['cases']:
        name = c['case']
        if name.startswith('tilt'):
            key = ('exact', 'tilt family, nine $(a,\\beta)$ pairs')
        elif name.startswith('loose'):
            eps = name.split('eps=')[1].split(' ')[0]; budget = name.split('budget=')[1]
            key = ('exact', f'adverse family, $\\varepsilon={eps}$, budget {budget}')
        elif name.startswith('generic') and 'bits' not in name and '+' not in name:
            n = name.split('n=')[1].split(' ')[0]; r = name.split('r=')[1]
            key = ('generic', f'$n={n}$, $r={r}$, three polygons')
        elif 'bits' in name:
            key = ('generic', f"$n=4$, $r=1/16$, denominators $2^{{{name.split('bits=')[1]}}}$")
        elif 'inactive' in name:
            key = ('generic', '$n=4$ plus an inactive plane, $r=1/16$')
        elif 'near-coincident' in name:
            key = ('generic', '$n=4$ plus a near-coincident plane, $r=1/16$')
        else:
            key = ('refusal', '$n=8$, $r=1/4$, region cap 100')
        groups.setdefault(key, []).append(c)
    for (kind, label), cs in groups.items():
        if kind == 'refusal':
            generic_rows.append(f'{label} & -- & -- & -- & refused & -- \\\\')
            continue
        env_base = [F(c['envelope'])/F(c['baseline']) for c in cs]
        secs = max((c['seconds_refine'] or 0)+c['seconds_envelope'] for c in cs)
        if kind == 'exact':
            env_ex = [F(c['envelope'])/F(c['exact']) for c in cs]
            lo_ex = [F(c['lower'])/F(c['exact']) for c in cs]
            up_ex = [F(c['upper'])/F(c['exact']) for c in cs]
            boxes = max(c['boxes'] for c in cs)
            exact_rows.append(f'{label} & {fr(env_base)} & {fr(env_ex)} & {fr(lo_ex, 4)} & {fr(up_ex, 4)} & {boxes} & {secs:.2f} \\\\')
        else:
            lo_env = [F(c['lower'])/F(c['envelope']) for c in cs]
            up_env = [F(c['upper'])/F(c['envelope']) for c in cs]
            regions = max(c['regions'] for c in cs)
            generic_rows.append(f'{label} & {fr(env_base)} & {fr(lo_env)} & {fr(up_env)} & {regions} & {secs:.2f} \\\\')
    wrap = lambda name, rows: '\\providecommand{\\%s}{%%\n%s}\n' % (name, '\n'.join(rows)+'\n')
    return wrap('benchmarkExactRows', exact_rows), wrap('benchmarkGenericRows', generic_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--table', action='store_true')
    args = parser.parse_args()
    if args.table:
        for path, text in zip(TABLES, table(json.loads(OUT.read_text()))):
            path.write_text(text)
            print(f'wrote {path}')
        return
    data = enc(run())
    if args.check:
        recorded = json.loads(OUT.read_text())
        mismatch = [(a['case'], k, a.get(k), b.get(k)) for a, b in zip(data['cases'], recorded['cases'])
                    for k in EXACT_FIELDS if a.get(k) != b.get(k)]
        if len(data['cases']) != len(recorded['cases']) or mismatch:
            print(json.dumps(dict(status='failed', mismatch=mismatch[:10]), indent=2))
            raise SystemExit(1)
        print(json.dumps(dict(status='passed', cases=len(data['cases']),
                              note='exact fields match; timing and memory are not compared')))
        return
    OUT.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(dict(wrote=str(OUT), cases=len(data['cases']), peak_rss_mb=rss_mb())))


if __name__ == '__main__':
    main()
