# Security Sentinel Report

Automated security audit by Oz Security Sentinel (fast/local mode).

- Scanner: `trivy fs` (HIGH, CRITICAL only)
- Mode: `SENTINEL_LOCAL_FAST=1`
- Remediation: skipped (`SENTINEL_SKIP_REMEDIATION=1`)
- Skipped dirs: `node_modules,dist,.git,coverage,vendor`
- Reachability roots: `app`, `server.js`, `config` (only `app` of the configured roots existed)

## Summary

- Total HIGH/CRITICAL findings: **49**
- Unique vulnerable packages: **23**
- Reachable packages (directly imported in code): **5**
- Reachable findings: **8**

## Reachable vulnerabilities

These packages are imported from the application code paths (`server.js` / `config/config.js`) and the corresponding CVEs are exploitable in this codebase.

### body-parser (1 finding)
- Imported from `server.js:5` — `const bodyParser = require("body-parser");`
- HIGH `CVE-2024-45590` — installed `1.18.3`, fixed in `1.20.3` — Denial of Service in body-parser.

### marked (3 findings)
- Imported from `server.js:13` — `const marked = require("marked");`
- HIGH `CVE-2017-16114` — installed `0.3.5`, fixed in `0.3.9` — ReDoS in marked.
- HIGH `CVE-2022-21680` — installed `0.3.5`, fixed in `4.0.10` — ReDoS via `block.def`.
- HIGH `CVE-2022-21681` — installed `0.3.5`, fixed in `4.0.10` — ReDoS via `inline.reflinkSearch`.

### mongodb (1 finding)
- Imported from `server.js:11` — `const MongoClient = require("mongodb").MongoClient;`
- HIGH `GHSA-mh5c-679w-hh4r` — installed `2.2.36`, fixed in `3.1.13` — Denial of Service in mongodb.

### swig (1 finding)
- Imported from `server.js:9` — `const swig = require("swig");`
- HIGH `CVE-2023-25345` — installed `1.4.2`, no fix available — Arbitrary local file read during template rendering.

### underscore (2 findings)
- Imported from `config/config.js:1` — `const _ = require("underscore");`
- CRITICAL `CVE-2021-23358` — installed `1.9.1`, fixed in `1.12.1` — Arbitrary code execution via the template function.
- HIGH `CVE-2026-27601` — installed `1.9.1`, fixed in `1.13.8` — DoS via recursive structures in `flatten`/`isEqual`.

## Triaged: Unreachable

The following packages had HIGH/CRITICAL findings but are not directly imported from the configured reachability roots; they were marked **Triaged: Unreachable** for this run:

`tar`, `minimatch`, `minimist`, `set-value`, `path-to-regexp`, `nconf`, `semver`, `braces`, `bson`, `debug`, `decode-uri-component`, `fsevents`, `i`, `ini`, `kind-of`, `mixin-deep`, `qs`, `y18n`.

These are transitive dev/build dependencies and may still warrant follow-up patching, but no reachable call site was identified in `app/`, `server.js`, or `config/`.

## Recommended remediation

Remediation was skipped per environment config. To apply patches manually:

```bash
npm install body-parser@latest marked@latest mongodb@latest underscore@latest
# swig has no fixed version available; consider migrating to a maintained
# templating engine (e.g. swig-templates, nunjucks, or pug).
```

After updating, run the project test suite (`npm test`) and re-run the sentinel scan to verify resolution.
