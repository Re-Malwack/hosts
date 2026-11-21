"""Write and verify the SHA-256 manifest for the generated hosts and blocklists.

The manifest lives in the repository root (checksums.txt) and has one
"<path> <sha256>" line per file, sorted by path. Paths are relative to the
repository root and always use forward slashes.

Usage (from the repository root):
    python scripts/checksums.py            write checksums.txt
    python scripts/checksums.py --check    exit 1 if checksums.txt is out of date

The update scripts call write_checksums() when they finish, so the manifest
always matches the files they just produced.
"""
import hashlib
import os
import sys
import urllib.request

CHECKSUM_FILE = "checksums.txt"
CHECKSUM_DIRS = ("hosts", "blocklists")
SKIP_SUFFIXES = (".count",)
REMOTE_FILES = (
    "https://raw.githubusercontent.com/ZG089/Re-Malwack/main/whitelist.txt",
    "https://raw.githubusercontent.com/ZG089/Re-Malwack/main/social_whitelist.txt",
)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def list_files(root="."):
    paths = []
    for directory in CHECKSUM_DIRS:
        for dirpath, _, filenames in os.walk(os.path.join(root, directory)):
            for name in filenames:
                if name.endswith(SKIP_SUFFIXES):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, name), root)
                paths.append(rel.replace(os.sep, "/"))
    return sorted(paths)


def compute_checksums(root="."):
    checksums = {
        path: sha256_of(os.path.join(root, path)) for path in list_files(root)
    }
    for url in REMOTE_FILES:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Re-Malwack hosts updater)"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            checksums[url] = hashlib.sha256(response.read()).hexdigest()
    return dict(sorted(checksums.items()))


def write_checksums(root="."):
    checksums = compute_checksums(root)
    with open(os.path.join(root, CHECKSUM_FILE), "w", encoding="utf-8", newline="\n") as f:
        for path, digest in checksums.items():
            f.write(f"{path} {digest}\n")
    print(f"Wrote {len(checksums)} checksums to {CHECKSUM_FILE}")
    return checksums


def read_checksums(root="."):
    checksums = {}
    with open(os.path.join(root, CHECKSUM_FILE), "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line:
                path, digest = line.rsplit(" ", 1)
                checksums[path] = digest
    return checksums


def verify_checksums(root="."):
    """Return a list of problems; an empty list means the manifest is current."""
    try:
        recorded = read_checksums(root)
    except FileNotFoundError:
        return [f"{CHECKSUM_FILE} is missing"]

    actual = compute_checksums(root)
    problems = []
    for path in sorted(recorded.keys() | actual.keys()):
        if path not in actual:
            problems.append(f"{path}: listed but missing")
        elif path not in recorded:
            problems.append(f"{path}: present but not listed")
        elif recorded[path] != actual[path]:
            problems.append(f"{path}: checksum mismatch")
    return problems


def main(argv):
    if "--check" in argv:
        problems = verify_checksums()
        for problem in problems:
            print(problem)
        if problems:
            return 1
        print(f"{CHECKSUM_FILE} is up to date")
        return 0
    write_checksums()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
