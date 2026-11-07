"""Standard-library-only checked input primitives for the notice CLI.

The four functions retain the frozen static-distribution reader's behavior;
importing them must not load its optional schema-validation dependency.
The historical checker and its source identity remain unchanged.
"""
import hashlib
import json
import os
from pathlib import Path
import stat

LIMIT = 512 * 1024 * 1024


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON field: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('non-finite JSON value: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def transfer(path, destination=None, retain=False):
    """Stream a bounded no-follow regular file, checking descriptor stability."""
    path = Path(path)
    require(path.is_absolute() and '..' not in path.parts, 'absolute physical file path required')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = child
        child = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        writer = None
        try:
            before = os.fstat(child)
            limit = 32 * 1024 * 1024 if retain else LIMIT
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size <= limit,
                    'unsupported linked/special file or explicit size bound exceeded')
            if destination is not None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                writer = destination.open('wb')
            digest, chunks, size = hashlib.sha256(), [], 0
            while True:
                chunk = os.read(child, 1024 * 1024)
                if not chunk: break
                size += len(chunk)
                require(size <= limit, 'explicit file byte limit exceeded')
                digest.update(chunk)
                if writer: writer.write(chunk)
                if retain: chunks.append(chunk)
            after = os.fstat(child)
            stamp = lambda v: (v.st_dev, v.st_ino, v.st_mode, v.st_size, v.st_mtime_ns, v.st_ctime_ns)
            require(stamp(before) == stamp(after), 'input changed during read')
            return (b''.join(chunks) if retain else None), digest.hexdigest(), size
        finally:
            if writer: writer.close()
            os.close(child)
    finally:
        os.close(fd)
