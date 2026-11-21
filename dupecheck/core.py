"""Duplicate detection: group by size first, hash only the candidates.

Files are duplicates when their content is identical (sha256), whatever
their names are. dupecheck never deletes anything; it reports groups and
the space that extra copies waste, and can print a keep plan.
"""
import hashlib
import os
from collections import defaultdict

CHUNK = 1024 * 1024


def hash_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def find_duplicates(roots, min_size=1):
    by_size = defaultdict(list)
    scanned = 0
    for root in roots:
        for dirpath, _dirnames, filenames in os.walk(root):
            for name in filenames:
                path = os.path.join(dirpath, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                scanned += 1
                if size >= min_size:
                    by_size[size].append(path)
    groups = []
    for size, paths in by_size.items():
        if len(paths) < 2 or size == 0:
            continue
        by_hash = defaultdict(list)
        for path in paths:
            try:
                by_hash[hash_file(path)].append(path)
            except OSError:
                continue
        for digest, same in by_hash.items():
            if len(same) > 1:
                groups.append({
                    "sha256": digest,
                    "size": size,
                    "files": sorted(same),
                    "wasted": size * (len(same) - 1),
                })
    groups.sort(key=lambda g: g["wasted"], reverse=True)
    return {"scanned": scanned, "groups": groups,
            "total_wasted": sum(g["wasted"] for g in groups)}


def human(nbytes):
    value = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
