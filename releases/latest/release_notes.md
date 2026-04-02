# Data Privix Free Edition — v2.3.3

Release date: 2026-04-02

## Summary

v2.3.3 is a patch release that tightens PDF handling and improves demo materials.
PDF redaction is now explicitly gated to Pro licenses, and Free-mode runs will omit PDFs found inside archives to avoid accidental leakage of unredacted documents.

## What changed

- PDF redaction: requires a Pro license.
- Free mode: PDFs inside `.zip`/`.tar.gz` inputs are omitted from outputs (not copied through).
- Website: add a new PDF redaction demo transcript.

## What’s included

- Installable Python wheel (`data_privix-2.3.3-py3-none-any.whl`)
- Optional Nuitka bundle (`data-privix-2.3.3-nuitka-linux-x86_64.tar.gz`)
- Documentation PDFs:
  - `user_guide.pdf`
  - `admin_guide.pdf`
  - `changelog.pdf`

## Notes

- This repository is **distribution-only**. It does not include product source code.
- Pro/Enterprise editions are available under commercial terms from MagicByte Consulting.

