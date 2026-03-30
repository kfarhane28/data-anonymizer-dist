# Data Anonymizer Free Edition — v1.2.0

Release date: 2026-03-30

## Summary

v1.2.0 improves the Streamlit preview UX and makes profiling suggestions more actionable by aligning suggested rules with the masking examples shown in the profiling report.

## What changed

- Streamlit UI: show the tool version in the sidebar footer.
- Anonymization preview (highlighted): render one log line per row (no concatenation), with better wrapping for long lines.
- Sensitive-data profiling: suggested rules are now emitted as **rules v2** (action-based) and aligned with the masked examples:
  - Email: keep only the first character of the local part (`keepFirst=1`) and mask with `***`.
  - IPv4: keep the first and last octets and mask the middle as `***.***`.
- Rules engine: new v2 action `mask_fixed` for fixed-length masking (useful for consistent masked examples like `c***@domain`).

## What’s included

- Installable Python wheel (`data_anonymizer-1.2.0-py3-none-any.whl`)
- Optional Nuitka bundle (`data-anonymizer-1.2.0-nuitka-linux-x86_64.tar.gz`)
- Documentation PDFs:
  - `user_guide.pdf`
  - `admin_guide.pdf`
  - `changelog.pdf`

## Notes

- This repository is **distribution-only**. It does not include product source code.
- Pro/Enterprise editions are available under commercial terms from MagicByte Consulting.
