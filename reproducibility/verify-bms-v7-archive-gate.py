#!/usr/bin/env python3
import argparse, hashlib, pathlib, sys, tarfile, tempfile

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Fail-closed verification gate for NOVA BMS v7 archive.')
    ap.add_argument('--archive', required=True, type=pathlib.Path)
    ap.add_argument('--expected-sha256', required=True)
    args=ap.parse_args()
    if not args.archive.is_file():
        raise SystemExit('FAIL: archive_missing')
    got=sha256(args.archive)
    if got != args.expected_sha256:
        raise SystemExit(f'FAIL: archive_sha256_mismatch expected={args.expected_sha256} got={got}')
    with tempfile.TemporaryDirectory(prefix='nova-bms-gate-') as td:
        root=pathlib.Path(td)
        with tarfile.open(args.archive, 'r:gz') as tf:
            tf.extractall(root, filter='data')
        sums=list(root.rglob('SHA256SUMS'))
        if len(sums)!=1: raise SystemExit('FAIL: sha256sums_missing_or_ambiguous')
        bad=[]
        base=sums[0].parent
        for line in sums[0].read_text().splitlines():
            if not line.strip(): continue
            expected,name=line.split(None,1); p=base/name.lstrip('*')
            if not p.is_file() or sha256(p)!=expected: bad.append(name)
        if bad: raise SystemExit('FAIL: internal_sha256_mismatch '+','.join(bad))
    print('PASS: archive_and_internal_sha256_verified')

if __name__=='__main__': main()
