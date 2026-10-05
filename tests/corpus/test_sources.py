import zipfile

import pytest

from vantage.corpus.sources import load_manifest, main, restore


def _manifest(tmp_path, body):
    path = tmp_path / "sources.toml"
    path.write_text(body, encoding="utf-8")
    return path


def test_every_source_of_the_repo_manifest_is_present():
    missing = [str(f.path) for f in load_manifest() if not f.is_present()]
    assert missing == []


def test_missing_file_is_downloaded_from_its_url(tmp_path):
    manifest = _manifest(
        tmp_path,
        '[[source]]\nid = "act"\nfiles = [{ path = "act.html", url = "https://example.test/act" }]\n',
    )
    [file] = load_manifest(manifest, tmp_path / "raw")
    restore(file, fetch=lambda url: f"<html>{url}</html>".encode())
    assert file.path.read_text() == "<html>https://example.test/act</html>"


def test_missing_file_is_extracted_from_its_archive(tmp_path):
    folder = tmp_path / "raw" / "fiction"
    folder.mkdir(parents=True)
    with zipfile.ZipFile(folder / "docs.zip", "w") as archive:
        archive.writestr("docs/corpus/note.md", "# Note interne")
    manifest = _manifest(
        tmp_path,
        '[[source]]\nid = "fiction"\narchive = "docs.zip"\n'
        'files = [{ path = "corpus/note.md", member = "docs/corpus/note.md" }]\n',
    )
    [file] = load_manifest(manifest, tmp_path / "raw")
    restore(file)
    assert (folder / "corpus" / "note.md").read_text() == "# Note interne"


def test_check_only_reports_missing_files_without_restoring(tmp_path, capsys):
    manifest = _manifest(
        tmp_path,
        '[[source]]\nid = "act"\nfiles = [{ path = "act.html", url = "https://example.test/act" }]\n',
    )
    assert main(["--check", "--manifest", str(manifest), "--raw-dir", str(tmp_path / "raw")]) == 1
    assert "missing" in capsys.readouterr().out
    assert not (tmp_path / "raw" / "act" / "act.html").exists()


def test_entry_needs_exactly_one_origin(tmp_path):
    manifest = _manifest(tmp_path, '[[source]]\nid = "act"\nfiles = [{ path = "act.html" }]\n')
    with pytest.raises(ValueError, match="exactly one of url or member"):
        load_manifest(manifest, tmp_path / "raw")
