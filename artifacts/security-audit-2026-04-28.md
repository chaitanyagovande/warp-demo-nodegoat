# Security Sentinel Audit Report
**Date:** 2026-04-28  
**Mode:** Local Fast (`SENTINEL_LOCAL_FAST=1`)  
**Scan Tool:** Trivy v0.70.0  
**Total HIGH/CRITICAL Findings:** 49  
**Reachable Findings:** 6 (across 4 packages)  
**Remediation:** Skipped (`SENTINEL_SKIP_REMEDIATION=1`)

---

## Reachable Vulnerabilities

### 1. `body-parser` (imported in `server.js`)
| CVE | Severity | Installed | Fixed | Description |
|-----|----------|-----------|-------|-------------|
| CVE-2024-45590 | HIGH | 1.18.3 | 1.20.3 | Denial of Service Vulnerability in body-parser |

**Reachability:** `bodyParser.json()` and `bodyParser.urlencoded()` are actively called in `server.js:71-72`.

---

### 2. `swig` (imported in `server.js`)
| CVE | Severity | Installed | Fixed | Description |
|-----|----------|-----------|-------|-------------|
| CVE-2023-25345 | HIGH | 1.4.2 | None | Arbitrary local file read vulnerability during template rendering |

**Reachability:** Used as Express view engine via `consolidate.swig` in `server.js:116`. `swig.setDefaults(...)` called at `server.js:135`. No upstream fix available.

---

### 3. `mongodb` (imported in `server.js`)
| CVE | Severity | Installed | Fixed | Description |
|-----|----------|-----------|-------|-------------|
| GHSA-mh5c-679w-hh4r | HIGH | 2.2.36 | 3.1.13 | Denial of Service in mongodb |

**Reachability:** `MongoClient.connect(db, ...)` called at `server.js:30`.

---

### 4. `marked` (imported in `server.js`)
| CVE | Severity | Installed | Fixed | Description |
|-----|----------|-----------|-------|-------------|
| CVE-2017-16114 | HIGH | 0.3.5 | 0.3.9 | Regular expression denial of service |
| CVE-2022-21680 | HIGH | 0.3.5 | 4.0.10 | ReDoS via block.def regex |
| CVE-2022-21681 | HIGH | 0.3.5 | 4.0.10 | ReDoS via inline.reflinkSearch regex |

**Reachability:** `marked.setOptions(...)` and `app.locals.marked = marked` set at `server.js:126-129`. Markdown rendering is exposed to user-controlled content.

---

## Triaged: Unreachable (Transitive Dependencies Only)

The following packages were found vulnerable but are **not directly imported** by application code (`app/`, `server.js`). They exist only as transitive dependencies and are not reachable through application logic:

| Package | Severity | CVEs |
|---------|----------|------|
| braces | HIGH | CVE-2024-4068 |
| bson | CRITICAL | CVE-2020-7610 |
| debug | HIGH | CVE-2017-20165 |
| decode-uri-component | HIGH | CVE-2022-38900 |
| fsevents | CRITICAL | CVE-2023-45311 |
| i | HIGH | CVE-2021-3820 |
| ini | HIGH | CVE-2020-7788 |
| kind-of | HIGH | CVE-2019-20149 |
| minimatch | HIGH | CVE-2022-3517, CVE-2026-26996, CVE-2026-27903, CVE-2026-27904 |
| minimist | CRITICAL | CVE-2021-44906 (×4) |
| mixin-deep | CRITICAL | CVE-2019-10746 |
| nconf | HIGH | CVE-2022-21803 (×2) |
| path-to-regexp | HIGH | CVE-2024-45296, CVE-2024-52798, CVE-2026-4867 |
| qs | HIGH | CVE-2022-24999 |
| semver | HIGH | CVE-2022-25883 (×2) |
| set-value | CRITICAL/HIGH | CVE-2019-10747, CVE-2021-23440 (×4) |
| tar | HIGH | CVE-2021-32803/04, CVE-2021-37701/12/13, CVE-2026-23745/23950/24842/26960/29786/31802 |
| underscore | CRITICAL/HIGH | CVE-2021-23358, CVE-2026-27601 |
| y18n | HIGH | CVE-2020-7774 |

---

## Recommended Actions

1. **`body-parser`** → Upgrade to `>=1.20.3` (`npm install body-parser@latest`)
2. **`mongodb`** → Upgrade to `>=3.1.13` (`npm install mongodb@latest`) — note: this is a major version bump; validate API compatibility
3. **`marked`** → Upgrade to `>=4.0.10` (`npm install marked@latest`) — note: major version breaking changes expected
4. **`swig`** → **No upstream fix available.** Consider migrating to a maintained template engine (e.g., `nunjucks`, `ejs`, `pug`)
