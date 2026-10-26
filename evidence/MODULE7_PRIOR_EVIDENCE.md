# Verified earlier Module 7.2 failure / recovery (provenance)

**Original run:** [GitHub Actions #39151149764](https://github.com/Barquito0/EGN-321-Module-7_2/actions/runs/39151149764)

**Original evidence directory:** https://github.com/Barquito0/EGN-321-Module-7_2/tree/main/evidence

These events come from **Module 7.2**, not a new capstone run. The controlled failure stopped classroom replay by creating `state/pause.flag`. The operator removed it without deleting or rebuilding the runtime SQLite database.

| Time (UTC, recorded Oct. 18, 2026) | Component | Event | Meaning |
|---|---|---|---|
| 17:47:24.807 | Operator | FAILURE_INJECTED | Deliberate source pause flag creation |
| 17:47:25.011 | Replay worker | SOURCE_PAUSED | First recorded source warning, cursor 30 |
| 17:47:27.814 | Health watchdog | STALE_INPUT | HEALTHY → DEGRADED; input no longer fresh |
| 17:47:33.430 | Health watchdog | INPUT_FAILED | DEGRADED → FAILED |
| 17:47:34.032 | Operator | RECOVERY_ACTION | Pause flag removed |
| 17:47:34.224 | Replay worker | SOURCE_RESUMED | Input resumed; interruption duration 9.212 s |
| 17:47:34.494 | Health watchdog | HEALTH_RECOVERED | FAILED → HEALTHY |

The original `evidence/verification.json` recorded `archive_before=8780` and `archive_after=8780` with `db_integrity_after=ok` and `verified=true`. The JSONL logs and original screenshots remain in that source repository. Link to them rather than presenting newly authored diagrams as real screenshots.
