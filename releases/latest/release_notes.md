# Data Privix Free Edition — v2.3.2

Release date: 2026-04-02

## Summary

v2.3.2 is a patch release that improves the marketing website with a clear “How it works” workflow animation and fixes iOS/Safari SVG animation positioning for a cleaner, more consistent render.

## What changed

- Website: add a lightweight workflow animation (raw sources → DataPrivix Engine → cleaned output) and feature it prominently on the homepage.
- Website/SVG animation: improve iOS/Safari rendering so animated transforms do not override SVG positioning (prevents overlapping / misaligned blocks).
- CI/Release: fix the Nuitka smoke test to validate the correct binary name (`data-privix`).

## What’s included

- Installable Python wheel (`data_privix-2.3.2-py3-none-any.whl`)
- Optional Nuitka bundle (`data-privix-2.3.2-nuitka-linux-x86_64.tar.gz`)
- Documentation PDFs:
  - `user_guide.pdf`
  - `admin_guide.pdf`
  - `changelog.pdf`

## Notes

- This repository is **distribution-only**. It does not include product source code.
- Pro/Enterprise editions are available under commercial terms from MagicByte Consulting.
