# Data Privix Free Edition — v2.3.6

Release date: 2026-04-03

## Summary

v2.3.6 is a patch release focused on Console UX correctness for exclude patterns.
The “Reset exclude” action now reliably restores patterns from the currently uploaded `.exclude` file, even after deleting patterns in the table.

## What changed

- Console: “Reset exclude” now mirrors “Reset rules”: it keeps the uploaded file selected and reloads its patterns into the exclude table.
- Console: fixes a stale table state issue where patterns could reappear in the Preview but not repopulate the table.

## What’s included

- Installable Python wheel (`data_privix-2.3.6-py3-none-any.whl`)
- Optional Nuitka bundle (`data-privix-2.3.6-nuitka-linux-x86_64.tar.gz`)
- Documentation PDFs:
  - `user_guide.pdf`
  - `admin_guide.pdf`
  - `changelog.pdf`

## Notes

- This repository is **distribution-only**. It does not include product source code.
- Pro/Enterprise editions are available under commercial terms from MagicByte Consulting.
