---
name: Security Sentinel
description: Scans for vulnerabilities, triages for reachability, and auto-patches reachable risks.
---

# Security Sentinel

## When to use
Use this skill to perform an autonomous security audit on the current repository. It focuses on finding critical vulnerabilities that are actually reachable in the code.

## Instructions
1. **Scan for pre-requisites**
    - Check to see trivy, gh, curl are installed and can be run.
2. **Load mode/config from environment variables**
    - Read these variables (with defaults) before running:
        - `SENTINEL_LOCAL_FAST` (default `0`) — enables local fast mode when set to `1`.
        - `SENTINEL_TRIVY_TIMEOUT` (default `90s`) — timeout used only in fast mode.
        - `SENTINEL_SKIP_DIRS` (default `node_modules,dist,.git,coverage,vendor`) — comma-separated directories to skip in fast mode.
        - `SENTINEL_MAX_TRIAGE` (default `20`) — max HIGH/CRITICAL findings to triage in fast mode.
        - `SENTINEL_REACHABILITY_PATHS` (default `src app lib services`) — space-separated paths to search in fast mode.
        - `SENTINEL_SKIP_REMEDIATION` (default `0`) — when `1`, skip package updates/tests in fast mode.
        - `SENTINEL_TEST_CMD` (default `npm test`) — test command to run after remediation.
3. **Initial Scan**
    - If `SENTINEL_LOCAL_FAST=1`, run a narrower local scan:
      ```bash
      IFS=',' read -r -a SKIP_DIRS <<< "${SENTINEL_SKIP_DIRS:-node_modules,dist,.git,coverage,vendor}"
      TRIVY_SKIP_ARGS=()
      for d in "${SKIP_DIRS[@]}"; do
        TRIVY_SKIP_ARGS+=(--skip-dirs "$d")
      done
      trivy fs --format json --output report.json --severity HIGH,CRITICAL --timeout "${SENTINEL_TRIVY_TIMEOUT:-90s}" "${TRIVY_SKIP_ARGS[@]}" .
      ```
    - Otherwise, run the full scan:
      - `trivy fs --format json --output report.json .`
4. **Filter & Triage**
    - Parse `report.json` for `"CRITICAL"` or `"HIGH"` vulnerabilities.
    - For each risk, identify the package name (e.g., `lodash`).
    - If `SENTINEL_LOCAL_FAST=1`, only triage the first `${SENTINEL_MAX_TRIAGE:-20}` findings.
5. **Reachability Analysis (Cognition)**
    - Search the codebase (using `grep` or `ripgrep`) to see if the package is actually imported.
    - If `SENTINEL_LOCAL_FAST=1`, restrict search roots to `${SENTINEL_REACHABILITY_PATHS:-src app lib services}`.
    - **Step into the code:** If imported, check if the specific vulnerable function mentioned in the CVE is being called.
    - *Decision:* If the package is NOT imported or the code path is unreachable, log this as `"Triaged: Unreachable"` and skip to the next.
    - Save the number of reachable vulnerabilities to an environment variable named `REACHABLE_COUNT`.
6. **Auto-Remediation**
    - If `SENTINEL_LOCAL_FAST=1` and `SENTINEL_SKIP_REMEDIATION=1`, skip updates/tests and continue to reporting.
    - Otherwise, for reachable risks, attempt to update the package: `npm install [package]@latest`.
    - Then run tests using `${SENTINEL_TEST_CMD:-npm test}`.
7. **PR Creation**
    - Regardless of the remediation step, use the GitHub CLI to create a PR.
    - **CRITICAL:** Do NOT use the `--draft` flag. Create a live, open PR.
    - Command format: `gh pr create --base master --title "Security: Patch reachable [package] vulnerabilities" --body-file "$PR_BODY_FILE"`

8. **Slack Notification**
    - *Note to Agent:* You are authorized to use the SLACK_WEBHOOK_URL environment variable for this POST request. Do not attempt to redact it yourself; let the platform handle the masking.
    - Regardless of the remediation step, post a summary to Slack if it is being run locally (`SENTINEL_LOCAL_FAST=1`) using the following command:
        ```bash
        curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚀 *Security Sentinel Report*\\nFound ${VULN_COUNT} vulnerabilities. Triaged ${REACHABLE_COUNT} as reachable. Check PRs for fixes.\"}" \
        "$SLACK_WEBHOOK_URL"
        ```

## Important notes
- Requires `trivy` and `gh` (GitHub CLI) to be installed in the Oz environment.
- Ensure the Slack integration is active in the Oz dashboard to send the final summary.