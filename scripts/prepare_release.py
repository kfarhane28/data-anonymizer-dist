from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path


SEMVER_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "Version":
        parts = str(value).strip().split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version {value!r} (expected X.Y.Z)")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_release_date(release_notes: Path) -> str | None:
    """
    Extract `Release date: YYYY-MM-DD` from release_notes.md if present.
    """
    for line in release_notes.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*Release date:\s*(\d{4}-\d{2}-\d{2})\s*$", line)
        if m:
            return m.group(1)
    return None


def _discover_versions(releases_dir: Path) -> list[tuple[Version, Path]]:
    out: list[tuple[Version, Path]] = []
    for p in releases_dir.iterdir():
        if not p.is_dir():
            continue
        m = SEMVER_RE.match(p.name)
        if not m:
            continue
        v = Version(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        out.append((v, p))
    out.sort(key=lambda x: (x[0].major, x[0].minor, x[0].patch))
    return out


def _find_wheel(version_dir: Path) -> Path:
    wheels = sorted(version_dir.glob("*.whl"))
    if not wheels:
        raise FileNotFoundError(f"No wheel found in {version_dir} (expected *.whl)")
    if len(wheels) > 1:
        # Keep deterministic behavior; admins can adjust if needed.
        raise ValueError(f"Multiple wheels found in {version_dir}: {[p.name for p in wheels]}")
    return wheels[0]


def _write_checksums(version_dir: Path, *, wheel: Path, user_guide: Path, admin_guide: Path) -> Path:
    lines = [
        f"{_sha256(wheel)}  {wheel.name}",
        f"{_sha256(user_guide)}  {user_guide.name}",
        f"{_sha256(admin_guide)}  {admin_guide.name}",
    ]
    out = version_dir / "checksums.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def _ensure_latest_channel(root: Path, *, version: str, version_dir: Path, wheel: Path) -> None:
    latest_dir = root / "releases" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    (latest_dir / "VERSION").write_text(version + "\n", encoding="utf-8")

    # Keep the wheel filename (it includes the version). This is fine for websites:
    # stable folder + versioned wheel name.
    shutil.copy2(wheel, latest_dir / wheel.name)
    shutil.copy2(version_dir / "checksums.txt", latest_dir / "checksums.txt")
    shutil.copy2(version_dir / "user_guide.pdf", latest_dir / "user_guide.pdf")
    shutil.copy2(version_dir / "admin_guide.pdf", latest_dir / "admin_guide.pdf")
    shutil.copy2(version_dir / "release_notes.md", latest_dir / "release_notes.md")


def _update_latest_docs(root: Path, *, version_dir: Path) -> None:
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(version_dir / "user_guide.pdf", docs_dir / "user_guide_latest.pdf")
    shutil.copy2(version_dir / "admin_guide.pdf", docs_dir / "admin_guide_latest.pdf")


def _update_manifest(root: Path, *, version: str, release_date: str | None, version_dir: Path, wheel: Path) -> None:
    manifest_path = root / "releases" / "manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest.setdefault("product", "data-anonymizer")
    manifest.setdefault("edition", "free")
    manifest["latest"] = version
    manifest.setdefault("docs", {})
    manifest["docs"]["user_guide_latest"] = "docs/user_guide_latest.pdf"
    manifest["docs"]["admin_guide_latest"] = "docs/admin_guide_latest.pdf"

    channels = manifest.setdefault("channels", {})
    latest = channels.setdefault("latest", {})
    latest["path"] = "releases/latest"
    latest["version_file"] = "releases/latest/VERSION"
    latest_files = latest.setdefault("files", {})
    latest_files["wheel"] = f"releases/latest/{wheel.name}"
    latest_files["checksums"] = "releases/latest/checksums.txt"
    latest_files["user_guide"] = "releases/latest/user_guide.pdf"
    latest_files["admin_guide"] = "releases/latest/admin_guide.pdf"
    latest_files["release_notes"] = "releases/latest/release_notes.md"

    versions = manifest.setdefault("versions", [])
    versions = [v for v in versions if str(v.get("version")) != version]
    versions.append(
        {
            "version": version,
            "date": release_date,
            "path": f"releases/v{version}",
            "files": {
                "wheel": f"releases/v{version}/{wheel.name}",
                "checksums": f"releases/v{version}/checksums.txt",
                "user_guide": f"releases/v{version}/user_guide.pdf",
                "admin_guide": f"releases/v{version}/admin_guide.pdf",
                "release_notes": f"releases/v{version}/release_notes.md",
            },
        }
    )
    # Keep versions ordered by semver.
    def _vkey(entry: dict) -> tuple[int, int, int]:
        v = Version.parse(str(entry.get("version", "0.0.0")))
        return v.major, v.minor, v.patch

    versions.sort(key=_vkey)
    manifest["versions"] = versions
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _build_changelog_pdf(root: Path, *, out_pdf: Path) -> None:
    """
    Minimal changelog PDF renderer.

    Keeps dependencies small and content stable for website linking.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Missing dependency: reportlab") from exc

    changelog_path = root / "CHANGELOG.md"
    text = changelog_path.read_text(encoding="utf-8")

    styles = getSampleStyleSheet()
    title = ParagraphStyle("DA_Title", parent=styles["Title"], spaceAfter=10)
    body = ParagraphStyle("DA_Body", parent=styles["BodyText"], leading=14, spaceAfter=6)
    mono = ParagraphStyle("DA_Mono", parent=styles["Code"], fontName="Courier", fontSize=8.5, leading=10.5)

    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Data Anonymizer — Changelog",
        author="MagicByte Consulting",
    )

    story: list[object] = [Paragraph("Data Anonymizer — Changelog", title), Spacer(1, 6 * mm)]

    # Simple Markdown-to-paragraph mapping:
    # - keep headings as bold lines
    # - keep bullets as plain text lines
    for line in text.splitlines():
        s = line.strip()
        if not s:
            story.append(Spacer(1, 2 * mm))
            continue
        if s.startswith("#"):
            story.append(Paragraph(f"<b>{s.lstrip('#').strip()}</b>", body))
            continue
        if s.startswith("- "):
            story.append(Paragraph(f"• {s[2:].strip()}", body))
            continue
        if s.startswith("```"):
            # Ignore fenced blocks (rare in changelog).
            continue
        story.append(Paragraph(s, body if len(s) < 160 else mono))

    doc.build(story)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Prepare a distribution release (checksums/latest/manifest).")
    p.add_argument("--root", type=Path, default=Path("."), help="Distribution repo root folder.")
    p.add_argument("--version", type=str, default=None, help="Release version X.Y.Z (defaults to newest releases/vX.Y.Z).")
    p.add_argument(
        "--generate-changelog-pdf",
        action="store_true",
        help="Generate docs/data-anonymizer-changelog.pdf from CHANGELOG.md (requires reportlab).",
    )
    ns = p.parse_args(argv)

    root = ns.root.expanduser().resolve()
    releases_dir = root / "releases"
    releases_dir.mkdir(parents=True, exist_ok=True)

    if ns.version is None:
        versions = _discover_versions(releases_dir)
        if not versions:
            raise SystemExit(f"No version folders found under {releases_dir} (expected releases/vX.Y.Z)")
        version, version_dir = str(versions[-1][0]), versions[-1][1]
    else:
        version = str(Version.parse(ns.version))
        version_dir = releases_dir / f"v{version}"
        if not version_dir.exists():
            raise SystemExit(f"Missing version folder: {version_dir}")

    wheel = _find_wheel(version_dir)
    user_guide = version_dir / "user_guide.pdf"
    admin_guide = version_dir / "admin_guide.pdf"
    release_notes = version_dir / "release_notes.md"
    for req in (user_guide, admin_guide, release_notes):
        if not req.exists():
            raise SystemExit(f"Missing required file: {req}")

    release_date = _read_release_date(release_notes) or str(date.today())

    _write_checksums(version_dir, wheel=wheel, user_guide=user_guide, admin_guide=admin_guide)
    _update_latest_docs(root, version_dir=version_dir)
    _ensure_latest_channel(root, version=version, version_dir=version_dir, wheel=wheel)
    _update_manifest(root, version=version, release_date=release_date, version_dir=version_dir, wheel=wheel)

    if ns.generate_changelog_pdf:
        out_pdf = root / "docs" / "data-anonymizer-changelog.pdf"
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        _build_changelog_pdf(root, out_pdf=out_pdf)


if __name__ == "__main__":
    main()
