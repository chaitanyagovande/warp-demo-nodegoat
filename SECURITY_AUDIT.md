# Oz Security Sentinel — Audit Report

Automated audit produced by the `Security Sentinel` skill.

- Mode: `SENTINEL_LOCAL_FAST=1`
- Remediation skipped: `SENTINEL_SKIP_REMEDIATION=1`
- Scanner: `trivy fs` (severity HIGH,CRITICAL)
- Reachability roots searched: `app server.js Gruntfile.js config`

## Summary

- Total HIGH/CRITICAL findings: **49**
- Distinct affected packages: **23**
- Reachable findings (package directly `require`d in source): **8**
- Unreachable / transitive findings: **41**

## Reachable findings (require attention)

These packages are imported directly by the application code. The patches
below are recommended next steps; auto-remediation was skipped because
`SENTINEL_SKIP_REMEDIATION=1`.

- `body-parser` 1.18.3 → 1.20.3 — CVE-2024-45590 (HIGH): Denial of Service in body-parser
- `marked` 0.3.5 → 0.3.9 — CVE-2017-16114 (HIGH): ReDoS in marked
- `marked` 0.3.5 → 4.0.10 — CVE-2022-21680 (HIGH): ReDoS via `block.def`
- `marked` 0.3.5 → 4.0.10 — CVE-2022-21681 (HIGH): ReDoS via `inline.reflinkSearch`
- `mongodb` 2.2.36 → 3.1.13 — GHSA-mh5c-679w-hh4r (HIGH): DoS in mongodb driver
- `swig` 1.4.2 → (no fixed version published) — CVE-2023-25345 (HIGH): Arbitrary local file read during template rendering
- `underscore` 1.9.1 → 1.12.1 — CVE-2021-23358 (CRITICAL): Arbitrary code execution via `template`
- `underscore` 1.9.1 → 1.13.8 — CVE-2026-27601 (HIGH): DoS via recursive data structures in `flatten`/`isEqual`

## Triaged: Unreachable (transitive only)

The following 18 packages were flagged but are not directly `require`d by
the application source under the configured reachability roots, and so
are logged as `Triaged: Unreachable` per skill policy:

`braces`, `bson`, `debug`, `decode-uri-component`, `fsevents`, `i`,
`ini`, `kind-of`, `minimatch`, `minimist`, `mixin-deep`, `nconf`,
`path-to-regexp`, `qs`, `semver`, `set-value`, `tar`, `y18n`.

These should still be cleaned up over time (e.g. by bumping their direct
parents), but they are not currently exercised by application code paths.

## Notes

- `swig` has no upstream fix (project is unmaintained); migrating to
  another templating engine is the appropriate long-term action.
- `underscore` CRITICAL is reachable only if `_.template` is used with
  untrusted input; a minor bump to ≥1.12.1 closes the issue regardless.
- The trivy scan output is preserved at `report.json` in the repo.
