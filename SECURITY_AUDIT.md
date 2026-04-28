# Security Sentinel Audit Report

Generated: 2026-04-28T18:45Z
Mode: `SENTINEL_LOCAL_FAST=1` (remediation skipped via `SENTINEL_SKIP_REMEDIATION=1`)

## Summary

- Total HIGH/CRITICAL findings: **49**
- Reachable (imported in `app/` or `server.js`): **6**
- Unique reachable packages: **4** (`body-parser`, `marked`, `mongodb`, `swig`)
- Remediation: skipped (per env config)

## Reachable Findings (action recommended)

These vulnerabilities are tied to packages directly imported in application code (`server.js`) and represent the highest-priority risks.

### body-parser 1.18.3 — server.js
- CVE-2024-45590 (HIGH) — Denial of Service Vulnerability in body-parser. Fixed in 1.20.3.

### marked 0.3.5 — server.js
- CVE-2017-16114 (HIGH) — ReDoS in marked. Fixed in 0.3.9.
- CVE-2022-21680 (HIGH) — `block.def` ReDoS. Fixed in 4.0.10.
- CVE-2022-21681 (HIGH) — `inline.reflinkSearch` ReDoS. Fixed in 4.0.10.

### mongodb 2.2.36 — server.js
- GHSA-mh5c-679w-hh4r (HIGH) — Denial of Service in mongodb. Fixed in 3.1.13.

### swig 1.4.2 — server.js
- CVE-2023-25345 (HIGH) — Arbitrary local file read during template rendering. **No upstream fix available**; project is unmaintained. Recommendation: migrate to a maintained template engine (e.g. `nunjucks`, `eta`, or `swig-templates`).

## Triaged: Unreachable

These vulnerable packages were detected by Trivy but are NOT directly imported under `app/` or `server.js`. They are pulled in transitively and have no direct call sites in application code.

`braces`, `bson`, `debug`, `decode-uri-component`, `fsevents`, `i`, `ini`, `kind-of`, `minimatch`, `minimist`, `mixin-deep`, `nconf`, `path-to-regexp`, `qs`, `semver`, `set-value`, `tar`, `underscore`, `y18n`

These should still be addressed via dependency upgrades when convenient, but they do not represent a directly exercised code path.

## Reachability Methodology

For each package flagged HIGH/CRITICAL by `trivy fs`, we ran:

```bash
grep -rE "require\(['\"]<pkg>['\"]\)|from ['\"]<pkg>['\"]" app server.js
```

Packages with at least one match are classified as **reachable**; otherwise **Triaged: Unreachable**.

Search roots followed `SENTINEL_REACHABILITY_PATHS` plus `server.js` (the configured `src lib services` paths do not exist in this repo).

## Configuration Used

- `SENTINEL_LOCAL_FAST=1`
- `SENTINEL_TRIVY_TIMEOUT=90s`
- `SENTINEL_SKIP_DIRS=node_modules,dist,.git,coverage,vendor`
- `SENTINEL_MAX_TRIAGE=100`
- `SENTINEL_REACHABILITY_PATHS=src app lib services`
- `SENTINEL_SKIP_REMEDIATION=1`
- `SENTINEL_TEST_CMD=npm test`
