# Capstone delivery report — From workbook to working application

**Student:** Marco Ruiz  
**Course:** EGN 321  
**Submitted artifact:** Integrated Flask application (rectangular tank-fill calculator + inherited temperature monitor)

## 1. Original process

The inherited `TANK_FILL_rev4.xlsx` workbook listed 18 fill runs and computed rectangular-tank liquid volume in US gallons. Each run used length and width in feet and fill depth in inches. The formula was `L × W × (D/12) × 7.48052`. The `Field Notes` sheet contained measurements for verification, while the `Tank Fill` sheet contained the copied depths and calculated gallons. A fixed cell range computed the overall total.

## 2. Defects and why they matter

Run R-108's field depth was **2.5 ft** but was entered as **2.5 in** in the main sheet. Its wrong volume was **93.5065 gal** instead of **1122.078 gal**, a deficit of **1028.5715 gal**. The total formula `SUM(G6:G17)` also excluded six valid rows, while the correct coverage was `SUM(G6:G23)`. The Module 1 investigation documented a reported total of 8527.79 gal and a fully corrected total of 14175.59 gal. The defect was hard to spot because Excel returned numbers without formula errors.

## 3. Replacement calculation

`capstone/tank_fill.py` expresses the same formula in reusable functions with named units. `calculate_from_units()` explicitly accepts depth units `in` or `ft`; a unit must be supplied. `total_run_volumes()` sums all valid uniquely identified rows instead of a hard-coded range. The Flask form is at `/tank`; the JSON API is `/api/tank-volume` and `/api/tank-total`.

## 4. Proof against the original workbook

The original Module 1 tests and defect report supply the expected results for R-103, R-116 and corrected R-108. This capstone tests all three, plus refusal of negative depth, unsupported/missing units, missing fields and non-finite numbers. A student-created fixture verifies the total across 18 rows and rejection on duplicate or incomplete runs. The fixture is **not** falsely labeled as 18 measured original-workbook runs. `evidence/workbook_verification.json` is generated from the actual function and `evidence/verification_cases.csv` documents assumptions.

## 5. Normal operation and refusal

With length 10 ft, width 6 ft, fill depth 2.5 and unit **feet**, the calculator returns **1122.078 gal** and confirms it used **30 inches**. With depth −1 in, it refuses calculation and gives an error message. A refusal is better than a plausible but unsupported engineering value that might mislead inventory decisions.

## 6. Growth through modules

| Module | Evidence and skill applied |
|---|---|
| 1 | `TANK_FILL_rev4.xlsx`, `DEFECTS.md`, known-correct test rows |
| 2 | Dimensional units, input contracts, invalid input refusal (unit-conversion project) |
| 3 | Reusable functions and tests, including temperature/unit calculations in other course exercises |
| 4 | UI/project planning; note original Module 4 proposal targeted a different synthetic planning workbook |
| 5 | Virtual-sensor replay introduction (separate course strand) |
| 6 | SQLite original historical reading archive, timestamps and missing gaps |
| 7 | Flask dashboard, persistence/hysteresis, stale/failed health, JSONL events and controlled recovery |
| 8 | Independent operating documentation, calculator UI addition and final presentation |

**Scope honesty:** The tank-fill calculator and temperature monitor were separate coursework strands. Their source data do not represent one tank instrumentation circuit. The Module 4 financial-planning concept remained a proposal, not a shipped feature.

## 7. SQLite and monitoring evidence

The Module 6 data contain 1,756 source rows × five sensor types = 8,780 sensor-specific archived records. Original timestamps are retained. The Module 7 monitor separates replay arrivals from source timestamps, validates accepted/rejected readings, provides a history view and charts, and uses independent stale-data detection. It changes from HEALTHY to DEGRADED after stale input and FAILED on longer input interruption.

## 8. Verified failure and recovery

The Module 7.2 controlled replay pause produced event sequence `FAILURE_INJECTED → SOURCE_PAUSED → STALE_INPUT → INPUT_FAILED → RECOVERY_ACTION → SOURCE_RESUMED → HEALTH_RECOVERED`. A real CI run reported original archive rows **8780 before and after**, `PRAGMA quick_check = ok`, and the state returned to **HEALTHY**. Original artifacts and logs are linked from README. Re-running this capstone's integrated workflow provides a new smoke test after source checkout. This report distinguishes earlier *verified* Module 7 evidence from new tests not run yet.

## 9. Handoff and operational quality

Assignment 8.1 prepared an extensive README, preflight script, source pause/resume command, log viewer, and operator checklists. Those are genuine documented improvements. The stored Megan Kahn observation report is **a draft**, not authenticated real-classmate performance; claims requiring a completed partner test or two specific post-test changes must be supported separately.

## 10. Trust and limitations

Confidence comes from known-source workbook cases, deterministic test suite, refused invalid units, permanent SQLite timestamps/status, automatic restart configuration, logged failure diagnostics, and explicit boundaries. Limitations include rectangular-only tank volume, no maximum fluid-depth check, uncalibrated simulated temperature readings, a local-only Flask server, and an unverified independent handoff. The original workbook is provided byte-identically with the capstone; the running monitor still needs a first-run Git download of the pinned Module 7.2 code.

## 11. Live code defense

The student should practice changing a threshold or validation rule, locating its function, rerunning the relevant test, and explaining the output *without AI during the live challenge*. The presenter notes and independent code-defense checklist are included.
