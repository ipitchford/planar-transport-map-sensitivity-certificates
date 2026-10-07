"""CI check: every file tracked in Git (except the manifest itself) matches MANIFEST.sha256 (MIT)."""
import hashlib
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tracked = set(subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True, text=True, check=True).stdout.split('\n'))
tracked.discard('')
expected = {}
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    expected[name] = digest
tracked.discard('MANIFEST.sha256')
missing = sorted(set(expected)-tracked)
extra = sorted(tracked-set(expected))
bad = [n for n, d in expected.items() if n in tracked and hashlib.sha256((root/n).read_bytes()).hexdigest() != d]
if missing or extra or bad:
    print({'missing_from_git': missing, 'not_in_manifest': extra, 'hash_mismatch': bad})
    sys.exit(1)
print(f'PASS: {len(expected)} manifested files match Git')
