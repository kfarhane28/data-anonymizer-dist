# Release process (distribution repository)

This repository is **distribution-only** for the Data Anonymizer **Free edition**.
Releases are created by adding a new version folder under `releases/`, updating `CHANGELOG.md`,
and refreshing the “latest” documentation copies under `docs/`.

## Preconditions

- You have the release artifacts available:
  - Python wheel: `data_anonymizer-X.Y.Z-py3-none-any.whl`
  - `user_guide.pdf` and `admin_guide.pdf` for the same version
- You know the release version `X.Y.Z` and release date (YYYY-MM-DD).

## Step-by-step: create a new release folder

1. Pick the new version (example: `0.1.1`).
2. Create the folder:

```bash
mkdir -p releases/v0.1.1
```

3. Copy the artifacts into the folder (filenames are suggestions; keep them consistent):

```bash
cp /path/to/data_anonymizer-0.1.1-py3-none-any.whl releases/v0.1.1/
cp /path/to/user_guide.pdf releases/v0.1.1/user_guide.pdf
cp /path/to/admin_guide.pdf releases/v0.1.1/admin_guide.pdf
```

4. Add `release_notes.md`:

```bash
cat > releases/v0.1.1/release_notes.md <<'EOF'
# Data Anonymizer Free Edition — v0.1.1

Release date: YYYY-MM-DD

## Summary

- <Add 3–6 concise bullets describing the changes relevant to Free edition users>

## Notes

- This repository is distribution-only and does not include product source code.
EOF
```

## Generate checksums (SHA-256)

Create `releases/vX.Y.Z/checksums.txt` with SHA-256 hashes for the artifacts.

Note: in this repository, the GitHub Action can generate `checksums.txt` automatically after you commit the new
release folder content.

macOS / Linux:

```bash
cd releases/v0.1.1
shasum -a 256 data_anonymizer-0.1.1-py3-none-any.whl user_guide.pdf admin_guide.pdf > checksums.txt
```

Linux alternative:

```bash
sha256sum data_anonymizer-0.1.1-py3-none-any.whl user_guide.pdf admin_guide.pdf > checksums.txt
```

Windows PowerShell (create lines manually):

```powershell
Get-FileHash .\data_anonymizer-0.1.1-py3-none-any.whl -Algorithm SHA256
Get-FileHash .\user_guide.pdf -Algorithm SHA256
Get-FileHash .\admin_guide.pdf -Algorithm SHA256
```

Ensure the file uses the format:

```
<sha256>  <filename>
```

## Update CHANGELOG.md

1. Add a new version section to `CHANGELOG.md`:

```md
## [0.1.1] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

2. Keep the tone factual and avoid internal-only details.

## Update “latest” documentation

Replace the latest copies under `docs/`:

```bash
cp releases/v0.1.1/user_guide.pdf docs/user_guide_latest.pdf
cp releases/v0.1.1/admin_guide.pdf docs/admin_guide_latest.pdf
```

Note: the GitHub Action can update `docs/*_latest.pdf` automatically.

## Update the “latest” download channel

To keep website URLs stable, update `releases/latest/` to point to the newest release.

```bash
LATEST=0.1.1

mkdir -p releases/latest
printf "%s\n" "$LATEST" > releases/latest/VERSION

cp "releases/v${LATEST}/data_anonymizer-${LATEST}-py3-none-any.whl" releases/latest/
cp "releases/v${LATEST}/checksums.txt" releases/latest/checksums.txt
cp "releases/v${LATEST}/user_guide.pdf" releases/latest/user_guide.pdf
cp "releases/v${LATEST}/admin_guide.pdf" releases/latest/admin_guide.pdf
cp "releases/v${LATEST}/release_notes.md" releases/latest/release_notes.md
```

Note: the GitHub Action can update `releases/latest/` automatically.

## Update the release manifest (optional but recommended)

If you use `releases/manifest.json` for website integration, update:
- `latest`
- the `channels.latest.files.*` wheel filename/path
- append the new version entry to `versions[]`

Note: the GitHub Action can update `releases/manifest.json` automatically.

## Release checklist

Before merging/publishing:

- [ ] Create `releases/vX.Y.Z/`
- [ ] Add wheel: `data_anonymizer-X.Y.Z-py3-none-any.whl`
- [ ] Add `user_guide.pdf` and `admin_guide.pdf`
- [ ] Add `release_notes.md` (3–6 user-facing bullets)
- [ ] Generate `checksums.txt` (SHA-256) and verify it matches the files
- [ ] Update `CHANGELOG.md` with `X.Y.Z` and release date
- [ ] Update `docs/user_guide_latest.pdf` and `docs/admin_guide_latest.pdf`
- [ ] Update `releases/latest/` (VERSION + artifacts) for stable website URLs
- [ ] Update `releases/manifest.json` (if used by the website)
- [ ] (Optional) Generate/refresh `docs/data-anonymizer-changelog.pdf`
- [ ] Verify README examples still point to a real release folder (or keep them version-agnostic)
- [ ] Commit changes with a clear message (e.g., `docs: release vX.Y.Z`)

## Automation (GitHub Actions)

This repository includes a workflow that can automate:
- `checksums.txt` generation
- `docs/*_latest.pdf` updates
- `releases/latest/` channel update
- `releases/manifest.json` update
- `docs/data-anonymizer-changelog.pdf` generation from `CHANGELOG.md`

Recommended operator workflow:
1) Add the new release folder and artifacts under `releases/vX.Y.Z/` (wheel + PDFs + release notes).
2) Update `CHANGELOG.md`.
3) Commit and push to `main`.

The GitHub Action will prepare the remaining metadata and push the result commit to `main`.
