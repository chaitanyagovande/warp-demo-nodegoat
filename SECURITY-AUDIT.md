# Security Sentinel Audit Report

Automated audit by Oz Sentinel (fast local mode).

## Summary
- Total HIGH/CRITICAL findings: **49**
- Reachable vulnerable packages: **5**
- Remediation: skipped (`SENTINEL_SKIP_REMEDIATION=1`)

## Reachable packages (imported in source)
The following vulnerable packages are imported in `server.js`, `app/`, `config/`, `Gruntfile.js`, or `test/` and represent the highest-priority risk surface:

- `body-parser` — CVE-2024-45590 (HIGH). Installed `1.18.3`, fixed in `1.20.3`.
- `marked` — CVE-2017-16114, CVE-2022-21680, CVE-2022-21681 (HIGH). Installed `0.3.5`, fixed in `4.0.10`+.
- `mongodb` — GHSA-mh5c-679w-hh4r (HIGH). Installed `2.2.36`, fixed in `3.1.13`.
- `swig` — CVE-2023-25345 (HIGH). Installed `1.4.2`, no upstream fix available — consider replacement.
- `underscore` — CVE-2021-23358 (CRITICAL), CVE-2026-27601 (HIGH). Installed `1.9.1`, fixed in `1.12.1` / `1.13.8`.

## Triaged as unreachable
Packages flagged by `trivy` but not directly imported in the searched source paths (likely transitive only):
`braces`, `bson`, `debug`, `decode-uri-component`, `fsevents`, `i`, `ini`, `kind-of`, `minimatch`, `minimist`, `mixin-deep`, `nconf`, `path-to-regexp`, `qs`, `semver`, `set-value`, `tar`, `y18n`.

These should still be reviewed but are deprioritized because the application code does not call them directly.

## Recommended next steps
1. Bump direct dependencies for the reachable packages to the fixed versions above.
2. Re-run `trivy fs` and the test suite (`npm test`) after bumps.
3. Replace `swig` (unmaintained, no upstream fix) with a maintained templating engine such as `swig-templates` or `nunjucks`.

_Generated automatically by Oz Sentinel._
