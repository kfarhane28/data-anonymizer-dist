# Data Anonymizer Free Edition — v2.3.0

Release date: 2026-04-01

## Summary

v2.3.0 improves rule control and evaluation order with per-rule priority, and refreshes the Streamlit rules editor UX to support it.

## What changed

- Rules: add optional `priority: <int>` to control rule precedence (higher priority evaluated first; ties keep file order).
- Streamlit UI: rules editor supports `priority` and keeps the column at the end of the table.
- Streamlit UI: PDF mode button layout fix (avoid clipping “Run PDF redaction”).
- Website: update plan comparison / features messaging for per-rule enable/disable and rule priority.

## What’s included

- Installable Python wheel (`data_anonymizer-2.3.0-py3-none-any.whl`)
- Optional Nuitka bundle (`data-anonymizer-2.3.0-nuitka-linux-x86_64.tar.gz`)
- Documentation PDFs:
  - `user_guide.pdf`
  - `admin_guide.pdf`
  - `changelog.pdf`

## Notes

- This repository is **distribution-only**. It does not include product source code.
- Pro/Enterprise editions are available under commercial terms from MagicByte Consulting.

