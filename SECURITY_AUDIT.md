# Security Sentinel Audit Report

Automated security audit performed by the Security Sentinel skill running in `SENTINEL_LOCAL_FAST=1` mode.

## Summary
- **Scan tool:** Trivy (filesystem mode, severity HIGH,CRITICAL)
- **Total HIGH/CRITICAL vulnerability findings:** 49
- **Unique vulnerable packages:** 23
- **Reachable packages (after triage):** 4
- **Remediation:** Skipped (`SENTINEL_SKIP_REMEDIATION=1`)

## Triage results

### Reachable (4)
These packages are imported in application code (`app/`, `server.js`, `Gruntfile.js`) and require attention:

- `body-parser`
- `marked`
- `mongodb`
- `swig`

### Unreachable / Triaged (19)
These packages are flagged by Trivy but are not directly imported in the searched application paths and are considered unreachable for this run:

`braces`, `bson`, `debug`, `decode-uri-component`, `fsevents`, `i`, `ini`, `kind-of`, `minimatch`, `minimist`, `mixin-deep`, `nconf`, `path-to-regexp`, `qs`, `semver`, `set-value`, `tar`, `underscore`, `y18n`

## Configuration used
- `SENTINEL_LOCAL_FAST=1`
- `SENTINEL_TRIVY_TIMEOUT=90s`
- `SENTINEL_SKIP_DIRS=node_modules,dist,.git,coverage,vendor`
- `SENTINEL_MAX_TRIAGE=100`
- `SENTINEL_REACHABILITY_PATHS=src app lib services`
- `SENTINEL_SKIP_REMEDIATION=1`
- `SENTINEL_TEST_CMD=npm test`

## Notes
- Reachability was determined via `grep` for `require('pkg')` / `from 'pkg'` patterns within the configured reachability paths.
- Because `SENTINEL_SKIP_REMEDIATION=1`, no `npm install` upgrades or test runs were performed in this audit.
- A follow-up PR should upgrade the four reachable packages to their fixed versions and re-run the test suite.
