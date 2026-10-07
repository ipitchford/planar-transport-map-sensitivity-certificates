"""Produce/recheck exact JSON results. See README for the trust boundary."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from transport_cert import (CertificateError, overlay, robust_bound, refine_bound,
                            baseline_bound, check_target_witness)


def encoded(value):
    if isinstance(value,Fraction):
        return str(value)
    if isinstance(value,dict):
        return {k:encoded(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [encoded(v) for v in value]
    return value


def run(path):
    raw=Path(path).read_bytes()
    data=json.loads(raw)
    result=overlay(data['domain'],data['reference'],data['comparison'])
    if 'radii' in data:
        result['coefficient_box']=robust_bound(data['domain'],data['reference'],data['comparison'],data['radii'])
        result['coefficient_box']['baseline_slope_diameter']=baseline_bound(
            data['domain'],data['reference'],data['comparison'],data['radii'])
        if 'refine' in data:
            options=data['refine']
            if not isinstance(options,dict):
                raise CertificateError('refine must be an object with max_boxes and optional tolerance')
            result['refined_box']=refine_bound(data['domain'],data['reference'],data['comparison'],
                data['radii'],max_boxes=options.get('max_boxes',64),tolerance=options.get('tolerance'))
    if 'target_witness' in data:
        w=data['target_witness']
        result['optimal_target_cost_squared']=check_target_witness(
            [p[:2] for p in data['reference']],[p[:2] for p in data['comparison']],
            result['first_masses'],result['second_masses'],w['coupling'],w['alpha'],w['beta'])
    result['input_sha256']=hashlib.sha256(raw).hexdigest()
    result['assurance']='Exact arithmetic implementation; not formal verification, independent peer review, or a general prescribed-mass solver.'
    return encoded(result)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--check',help='recompute and compare every field of a previously produced JSON result')
    args=parser.parse_args()
    try:
        result=run(args.input)
        if args.check and result!=json.loads(Path(args.check).read_text()):
            raise CertificateError('recorded result differs from exact recomputation')
        print(json.dumps(result,indent=2,sort_keys=True))
    except (CertificateError,ValueError,KeyError,OSError,TypeError,ZeroDivisionError) as error:
        parser.exit(1,f'REFUSING: {error}\n')
