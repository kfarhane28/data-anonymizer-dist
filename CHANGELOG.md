# Changelog

All notable changes to Data Anonymizer (Free Edition) public distribution will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-03-29

### Added
- Anonymization preview: highlighted output to clearly show which segments were transformed.
- Optional build hardening during packaging: wheel obfuscation step (local variable renaming).
- Optional Nuitka binary bundle artifact for restricted environments.

## [1.0.0] - 2026-03-22

### Added
- Free edition workload limits with explicit, actionable error messages (10 MB single file; 50 MB archive compressed; 200 MB extracted total; 200 extracted files).
- Updated User/Admin documentation to describe limits, measurement, and exceed behavior.

### Removed
- The v1.0.0 wheel artifact was withdrawn from this distribution repository. Use v1.1.0+.

## [0.1.0] - 2026-03-21 (Withdrawn)

### Added
- Initial public distribution structure for the Free edition (wheel + PDF documentation + checksums).

### Withdrawn
- v0.1.0 was removed from the public distribution channel and is not supported.
