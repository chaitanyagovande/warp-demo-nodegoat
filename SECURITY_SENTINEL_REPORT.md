# Security Sentinel Report
Mode: Local fast (`SENTINEL_LOCAL_FAST=1`, `SENTINEL_SKIP_REMEDIATION=1`)
Scanner: `trivy fs` (HIGH/CRITICAL only, skip-dirs: node_modules, dist, .git, coverage, vendor)
Reachability roots: `app` (from `SENTINEL_REACHABILITY_PATHS=src app lib services`; only `app` exists), plus `server.js` entrypoint.
## Summary
- Total HIGH/CRITICAL findings: 49 (41 unique pkg+CVE)
- Reachable findings (directly imported by source): 6 across 4 packages
- Remediation: skipped (`SENTINEL_SKIP_REMEDIATION=1`); no package upgrades or tests run.
## Reachable vulnerabilities
Direct `require(...)` of these packages was confirmed in `server.js` (and downstream `app/` modules):
### body-parser@1.18.3 — reachable
- CVE-2024-45590 (HIGH) — fix: 1.20.3
- Call site: `server.js:5,71-72` (`bodyParser.json()`, `bodyParser.urlencoded({ extended: ... })`)
### marked@0.3.5 — reachable
- CVE-2017-16114 (HIGH) — fix: 0.3.9
- CVE-2022-21680 (HIGH) — fix: 4.0.10
- CVE-2022-21681 (HIGH) — fix: 4.0.10
- Call site: `server.js:13,124-129` (`marked.setOptions(...)`, exposed via `app.locals.marked`)
### mongodb@2.2.36 — reachable
- GHSA-mh5c-679w-hh4r (HIGH) — fix: 3.1.13
- Call sites: `MongoClient` in `server.js`; `.find(...)` in `app/data/memos-dao.js`, `app/data/benefits-dao.js`, `app/data/allocations-dao.js`.
### swig@1.4.2 — reachable
- CVE-2023-25345 (HIGH) — fix: none published
- Call site: `server.js:9,116,135` (`consolidate.swig`, `swig.setDefaults(...)`)
## Triaged: Unreachable (transitive only — not directly imported by source)
braces, bson, debug, decode-uri-component, fsevents, i, ini, kind-of, minimatch, minimist, mixin-deep, nconf, path-to-regexp, qs, semver, set-value, tar, underscore, y18n.
## Recommended next steps
- Upgrade direct deps in `package.json`:
  - `body-parser` → `^1.20.3`
  - `marked` → `^4.0.10` (note: API changes since 0.3.x)
  - `mongodb` → modern major (note: driver API changes)
  - `swig` is unmaintained; migrate to a maintained template engine (e.g., `swig-templates` or `nunjucks`).
- Run `npm audit fix` followed by full test suite.
- Re-run sentinel without `SENTINEL_SKIP_REMEDIATION` once upgrade plan is approved.
