# Live demonstration checklist — 8.2

**Prep before presentation:** Python 3.11+ and Git, active `.venv`, `pip install -r requirements.txt`, run both first-run setup commands, and verify `python -m pytest -q`. The original workbook should open in Excel or another spreadsheet viewer if available. Keep screenshots in the links below as an emergency reference, **but do not pretend screenshots are the live program**.

1. **What I inherited:** Open `original/TANK_FILL_rev4.xlsx`; locate `Field Notes` for R-108 and `Tank Fill!G25` (SUM range defect). Show exact source repository if the local file is not available.
2. **Working interface:** Run `python scripts/start_capstone.py`; open `/tank` and `/`.
3. **Workbook known-correct:** On `/tank`, enter 10 ft × 6 ft × 12 in. Expected 448.8312 US gal. Show `evidence/workbook_verification.json`.
4. **Defect correction:** Enter 10 ft × 6 ft × **2.5 ft**. Expected 1122.078 US gal, converted to 30 in. Explain original wrong value 93.5065 gal.
5. **Refusal:** Enter −1 in depth. Expected visible `REFUSED` message; no volume shown.
6. **Evidence:** Open `/` status, history chart and `application/logs/monitor.jsonl`; explain 60-s original sample cadence vs 2-s replay arrivals, health and alerts.
7. **Failure and recovery:** Run `python scripts/source_control.py pause`; wait for DEGRADED then FAILED, inspect JSONL; run `python scripts/source_control.py resume`; confirm new accepted arrival and HEALTHY. Avoid deleting `application/state/monitor.db`.
8. **Limitations:** Geometry only, not safety certified; virtual sensor rather than tank level sensor; local Flask only; no authenticated handoff evidence if not completed.
9. **Code defense:** Practice changing logic without AI and running `python -m pytest -q`.

**Previous genuine evidence:** [Module 7.2 failure report](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/FAILURE_REPORT.md), [source/health timeline](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/timeline.csv), [screenshots](https://github.com/Barquito0/EGN-321-Module-7_2/tree/main/evidence).
