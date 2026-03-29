# Data Anonymizer (Free Edition) — Public Distribution

This repository is the **public distribution channel** for the **Data Anonymizer – Free edition**.
It provides **downloadable artifacts**, **documentation**, and **release history**.

## Product summary

Data Anonymizer is a Python-based tool to **anonymize sensitive data in logs, text files, and support bundles**
before sharing them with vendors or other teams. It is designed for operational workflows where files and archives
must be sanitized **without sending data to external services**.

## Important notice

- **Proprietary software** owned by **MagicByte Consulting**.
- **Source code is not included** in this repository.
- **Pro / Enterprise** editions are available under commercial terms.

## Security note (offline-first)

Data Anonymizer is designed to run **locally or on-prem**. Under normal operation, **no data needs to leave your
environment** to anonymize inputs. You remain responsible for validating anonymized outputs before sharing them,
and for applying rules/excludes appropriate for your data.

## Editions (Free vs Pro)

The Free edition is intended for basic anonymization workflows and evaluation.
Pro unlocks additional capabilities for large-scale and enterprise workflows.

Typical differences:
- **Free**: basic anonymization, user rules limited to **replace-only** rules, **sequential** processing.
- **Pro**: advanced rule actions, **parallel** processing, UI preview mode, sensitive-data profiling, and improved
  cancellation behavior for long runs.

## Current public version

The current supported public release in this distribution repository is **v1.1.0**.

## Free edition workload limits

Free is designed for evaluation and light workloads:
- Single file: up to **10 MB**
- Archives: up to **50 MB** (compressed)
- Extracted archive content: up to **200 MB** total
- Extracted files: up to **200 files**

Pro supports larger operational datasets and support bundles (limits removed).

## Repository layout

- `releases/` — versioned folders (e.g. `releases/v1.0.0/`) containing:
  - wheel (`.whl`)
  - `checksums.txt` (SHA-256)
  - `user_guide.pdf`, `admin_guide.pdf`
  - `release_notes.md`
- `docs/` — latest documentation copies:
  - `user_guide_latest.pdf`
  - `admin_guide_latest.pdf`
- `assets/` — branding assets (logo placeholder).

## Versioning

Releases follow Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`.
Each release is published under `releases/vX.Y.Z/` and includes the artifacts and release notes for that version.
For details, see `CHANGELOG.md`.

## Download and verify

1. Choose a version folder under `releases/` (example: `releases/v1.0.0/`).
2. Download the wheel and the PDF guides.
3. Verify integrity using the SHA-256 checksum in `checksums.txt`.

Example (macOS / Linux):

```bash
cd releases/v1.0.0
shasum -a 256 data_anonymizer-1.0.0-py3-none-any.whl
```

Example (Linux alternative):

```bash
sha256sum data_anonymizer-1.0.0-py3-none-any.whl
```

Example (Windows PowerShell):

```powershell
Get-FileHash .\data_anonymizer-1.0.0-py3-none-any.whl -Algorithm SHA256
```

Compare the computed hash with the corresponding line in `checksums.txt`.

## Clean, predictable links (for websites)

To keep URLs stable, a “latest” channel is provided:
- Latest release folder: `releases/latest/`
- Latest version string: `releases/latest/VERSION`

For websites that need to fetch structured metadata, use:
- Release manifest (JSON): `releases/manifest.json`

Version-specific URLs remain stable and predictable:
- `releases/vX.Y.Z/` (example: `releases/v1.0.0/`)

## Install (wheel)

```bash
python3 -m venv .venv
source .venv/bin/activate

# Prefer the "latest" channel for stable URLs.
VERSION="$(cat ./releases/latest/VERSION)"
pip install "./releases/latest/data_anonymizer-${VERSION}-py3-none-any.whl"

data-anonymizer --help
```

## Optional: Nuitka bundle (binary)

Some releases also ship an OS-specific Nuitka bundle (`data-anonymizer-<version>-nuitka-<os>-<arch>.tar.gz`).

Install instructions: `docs/INSTALL_NUITKA_BUNDLE.md`.

## Documentation

Local copies:
- User Guide (latest): `docs/user_guide_latest.pdf`
- Admin Guide (latest): `docs/admin_guide_latest.pdf`

Link placeholders (replace with your official documentation URLs):
- User Guide: `https://docs.example.com/data-anonymizer/user-guide`
- Admin Guide: `https://docs.example.com/data-anonymizer/admin-guide`
- Security & licensing: `https://docs.example.com/data-anonymizer/security-licensing`

## Licensing and procurement

The Free edition is distributed under proprietary terms. See `LICENSE.txt`.

For Pro/Enterprise licensing and procurement, contact **MagicByte Consulting** (placeholder):
- Sales: `sales@magicbyteconsulting.example`
- Support: `support@magicbyteconsulting.example`

## Maintaining releases

For a repeatable release checklist (version folder, checksums, changelog, latest docs), see `RELEASE_PROCESS.md`.
