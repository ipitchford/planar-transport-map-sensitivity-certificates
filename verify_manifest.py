"""Verify all shipped bytes against the root manifest (MIT)."""
import hashlib
from pathlib import Path, PurePosixPath


def main():
    root = Path(__file__).resolve().parent
    expected = {}
    for line in (root/'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split('  ',1)
        path = PurePosixPath(name)
        if (path.is_absolute() or '..' in path.parts or name in expected
                or len(digest) != 64 or name == 'MANIFEST.sha256'):
            raise ValueError('unsafe or duplicate manifest entry')
        expected[name] = digest
    if not expected:
        raise ValueError('empty manifest')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.relative_to(root).as_posix() != 'MANIFEST.sha256'}
    if actual != set(expected):
        raise ValueError(f'file-set mismatch: missing={set(expected)-actual}, extra={actual-set(expected)}')
    for name,digest in expected.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'hash mismatch: {name}')
    print(f'PASS: {len(expected)} manifested files; manifest itself excluded by definition')


if __name__ == '__main__':
    main()
