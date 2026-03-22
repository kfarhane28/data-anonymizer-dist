from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


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
        raise SystemExit("Missing dependency: reportlab") from exc

    changelog_path = root / "CHANGELOG.md"
    text = changelog_path.read_text(encoding="utf-8")

    styles = getSampleStyleSheet()
    title = ParagraphStyle("DA_Title", parent=styles["Title"], spaceAfter=10)
    body = ParagraphStyle("DA_Body", parent=styles["BodyText"], leading=14, spaceAfter=6)
    mono = ParagraphStyle("DA_Mono", parent=styles["Code"], fontName="Courier", fontSize=8.5, leading=10.5)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
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
    in_code = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if not s:
            story.append(Spacer(1, 2 * mm))
            continue
        if s.startswith("#"):
            story.append(Paragraph(f"<b>{s.lstrip('#').strip()}</b>", body))
            continue
        if s.startswith("- "):
            story.append(Paragraph(f"• {s[2:].strip()}", body))
            continue
        story.append(Paragraph(s, body if len(s) < 160 else mono))

    doc.build(story)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Render CHANGELOG.md to a PDF (requires reportlab).")
    p.add_argument("--root", type=Path, default=Path("."), help="Distribution repo root folder.")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("docs/data-anonymizer-changelog.pdf"),
        help="Output PDF path (relative to --root if not absolute).",
    )
    p.add_argument(
        "--copy-to-release",
        type=str,
        default=None,
        help="Optional version X.Y.Z to also copy the PDF to releases/vX.Y.Z/changelog.pdf.",
    )
    ns = p.parse_args(argv)

    root = ns.root.expanduser().resolve()
    out_pdf = ns.out.expanduser()
    if not out_pdf.is_absolute():
        out_pdf = (root / out_pdf).resolve()

    _build_changelog_pdf(root, out_pdf=out_pdf)
    print(str(out_pdf))

    if ns.copy_to_release:
        version = str(ns.copy_to_release).strip()
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            raise SystemExit(f"Invalid --copy-to-release version {version!r} (expected X.Y.Z)")
        version_dir = root / "releases" / f"v{version}"
        version_dir.mkdir(parents=True, exist_ok=True)
        dest = version_dir / "changelog.pdf"
        shutil.copy2(out_pdf, dest)
        print(str(dest))


if __name__ == "__main__":
    main()

