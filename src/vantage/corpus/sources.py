"""Check that every raw source of the Corpus is present, and restore missing files.

The list of sources lives in data/sources.toml. A missing file is downloaded
from its `url`, or extracted as `member` from its source's `archive`.

    python -m vantage.corpus.sources           # check, then restore what is missing
    python -m vantage.corpus.sources --check   # check only; exit 1 if anything is missing
"""

import argparse
import sys
import tomllib
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

MANIFEST_PATH = Path("data/sources.toml")
RAW_DIR = Path("data/raw")


@dataclass(frozen=True)
class SourceFile:
    source_id: str
    path: Path  # under data/raw/<source_id>/
    url: str | None = None
    archive: Path | None = None
    member: str | None = None

    def is_present(self) -> bool:
        return self.path.is_file() and self.path.stat().st_size > 0


def load_manifest(manifest: Path = MANIFEST_PATH, raw_dir: Path = RAW_DIR) -> list[SourceFile]:
    data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    files = []
    for source in data["source"]:
        folder = raw_dir / source["id"]
        archive = folder / source["archive"] if "archive" in source else None
        for entry in source["files"]:
            if ("url" in entry) == ("member" in entry):
                raise ValueError(f"{source['id']}/{entry['path']}: give exactly one of url or member")
            if "member" in entry and archive is None:
                raise ValueError(f"{source['id']}/{entry['path']}: member without an archive")
            files.append(
                SourceFile(
                    source_id=source["id"],
                    path=folder / entry["path"],
                    url=entry.get("url"),
                    archive=archive,
                    member=entry.get("member"),
                )
            )
    return files


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def restore(file: SourceFile, fetch: Callable[[str], bytes] = download) -> None:
    """Write one missing file, from its URL or from its source's archive."""
    if file.url is not None:
        content = fetch(file.url)
    else:
        if not file.archive.is_file():
            raise FileNotFoundError(f"archive {file.archive} is missing; cannot extract {file.member}")
        with zipfile.ZipFile(file.archive) as archive:
            content = archive.read(file.member)
    if not content:
        raise ValueError(f"{file.path}: empty content")
    file.path.parent.mkdir(parents=True, exist_ok=True)
    file.path.write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="only report; do not download or extract")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    args = parser.parse_args(argv)

    failed = 0
    for file in load_manifest(args.manifest, args.raw_dir):
        if file.is_present():
            print(f"ok        {file.path}")
            continue
        if args.check:
            print(f"missing   {file.path}")
            failed += 1
            continue
        try:
            restore(file)
        except Exception as error:  # report every failure, then exit non-zero
            print(f"FAILED    {file.path}: {error}")
            failed += 1
        else:
            print(f"{'downloaded' if file.url else 'extracted':<9} {file.path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
