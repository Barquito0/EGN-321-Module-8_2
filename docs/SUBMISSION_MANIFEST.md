# Final capstone submission manifest — status verified at packaging

| Rubric deliverable | Artifact/status |
|---|---|
| GitHub repository link | [Barquito0/EGN-321-Module-8_2](https://github.com/Barquito0/EGN-321-Module-8_2) |
| Working tank calculation | `capstone/tank_fill.py`, `capstone/routes.py`, `capstone_launcher.py` — unit-tested |
| Prior sensor monitoring application | `scripts/prepare_application.py` pins public user's [Module 7.2 repo](https://github.com/Barquito0/EGN-321-Module-7_2); requires first-run checkout |
| Original artifact | Bundled exact `original/TANK_FILL_rev4.xlsx` from [Module 1](https://github.com/Barquito0/EGN-321-Module-1/blob/main/original/TANK_FILL_rev4.xlsx); SHA `144c878d815abb234fa34d2f56d6670a23a9ba72`; fetch+hash-check via `scripts/fetch_original_workbook.py` |
| Known-workbook comparisons | `tests/test_tank_fill.py`, `evidence/workbook_verification.json`, `evidence/verification_cases.csv` |
| Validation/refusal | `capstone/tank_fill.py` (explicit ft/in, rejects invalid), API tests in `tests/test_flask_routes.py` |
| SQLite/history evidence | Prior Module 7.2 GitHub evidence and readme; pinned checkout preserves SQLite/replay statuses |
| Monitoring/logging | Prior Module 7.2 JSONL, health and screenshots linked from README |
| Failure/recovery | Prior [verified failure report](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/FAILURE_REPORT.md) |
| Final operating guide | `README.md`, quick start for Windows, Mac/Linux, `docs/LIVE_DEMO_CHECKLIST.md` |
| Handoff improvements | `scripts/preflight.py`, `scripts/source_control.py`, `docs/PRE_HANDOFF_CHANGES.md`; **actual classmate outcomes unverified** |
| AI disclosure | `AI_LOG.md` |
| Final presentation | `presentation/EGN321_Final_Capstone.pptx`, 8 slides and `docs/PRESENTATION_SCRIPT.md` |
| Live code challenge | `docs/CODE_DEFENSE_PRACTICE.md`; instructor assessment still requires in-person execution without AI |
| Local unit tests | 14 passed, 1 Flask test module skipped: Flask unavailable in this offline sandbox |
| CI/integrated tests | `.github/workflows/tests.yml` authored; **not claimed passed** until published and run on GitHub Actions |

The capstone GitHub repository includes the byte-identical original workbook; the pinned prior application checkout is retrieved on first setup. Use a real classmate handoff before presenting 8.1 draft observations as historical fact.
