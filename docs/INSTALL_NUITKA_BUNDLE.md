# Install the Nuitka bundle (binary artifact)

This repository may ship an optional OS-specific **Nuitka bundle**:

`data-anonymizer-<version>-nuitka-<os>-<arch>.tar.gz`

It contains a self-contained `data-anonymizer` executable that is **harder to inspect than a wheel** and can be
convenient for restricted environments where installing Python dependencies is undesirable.

## What you get

The archive extracts to a versioned folder:

```
data-anonymizer-<version>/
  data-anonymizer
  LICENSE
  EULA.md
  LEGAL.md
  README.md
```

Notes:
- The bundle is **OS/architecture specific** (example: `linux-x86_64`).
- The current bundle is intended for the **CLI**. For the Streamlit UI, use the wheel or Docker image.

## Download

Pick a specific version folder under `releases/` (example `releases/v1.1.0/`) and download:
- `data-anonymizer-<version>-nuitka-<os>-<arch>.tar.gz`

## Verify integrity (recommended)

If your version folder includes `checksums.txt`, verify the SHA-256 before running any binary.

macOS / Linux:

```bash
cd releases/v1.1.0
sha256sum data-anonymizer-1.1.0-nuitka-linux-x86_64.tar.gz
```

Compare the output hash with the corresponding entry in `checksums.txt`.

If `checksums.txt` does not list the Nuitka bundle yet, treat the artifact as unverified (or verify via a trusted
out-of-band channel).

## Install (extract)

```bash
tar -xzf data-anonymizer-1.1.0-nuitka-linux-x86_64.tar.gz
```

This creates `data-anonymizer-1.1.0/`.

## Run

```bash
./data-anonymizer-1.1.0/data-anonymizer --version
./data-anonymizer-1.1.0/data-anonymizer --help
```

Example anonymization run:

```bash
./data-anonymizer-1.1.0/data-anonymizer --input /path/to/in --output /path/to/out
```

## Troubleshooting

- **“Permission denied”**: `chmod +x ./data-anonymizer-1.1.0/data-anonymizer`
- **Wrong platform**: ensure you downloaded the correct `<os>-<arch>` build for your host.
- **Dynamic linking errors** (Linux): the bundle may require a compatible `glibc` and system libraries for the
  target distribution.

