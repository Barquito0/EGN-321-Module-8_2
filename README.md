# EGN 321 — Final Capstone (Assignment 8.2)

## From an inherited workbook to a tested engineering application

**Student:** Marco Ruiz  
**Inherited artifact:** [`TANK_FILL_rev4.xlsx` (original workbook)](https://github.com/Barquito0/EGN-321-Module-1/blob/main/original/TANK_FILL_rev4.xlsx)  
**Original defect investigation:** [`DEFECTS.md`](https://github.com/Barquito0/EGN-321-Module-1/blob/main/DEFECTS.md)  
**Monitored system:** [`EGN-321-Module-7_2`](https://github.com/Barquito0/EGN-321-Module-7_2) (reused at pinned revision)  
**Handoff operating documentation:** [`EGN-321-Module-8_1`](https://github.com/Barquito0/EGN-321-Module-8_1)  
**Instructor's assignment example:** [Module 8.2](https://github.com/ivansuarez-AU/EGN321_Module8_Assignment8_2)

This capstone is a **two-part engineering application**: a validated rectangular-tank-fill calculator connected to the Module 1 workbook cases, plus an **existing, separately developed** temperature-sensor monitoring and failure/recovery system from Modules 5–7. The application serves both at one local Flask address. The two functions are not misleadingly described as one physical system or one continuous calculation pipeline.

> **Original-file note:** The exact, unmodified Module 1 workbook `original/TANK_FILL_rev4.xlsx` is committed in this capstone repository; its Git blob SHA `144c878d815abb234fa34d2f56d6670a23a9ba72` was checked against the original Module 1 repository. `python -m scripts.fetch_original_workbook` verifies the bundled file and retrieves it only if missing.

## Quick start — Windows PowerShell

Install Python 3.11+, Git, and ensure Internet access for the **first** download:

```powershell
# From the folder containing this README (after cloning/extracting):
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.fetch_original_workbook
python -m scripts.prepare_application
python -m pytest -q
python -m scripts.verify_capstone
python scripts/start_capstone.py
```

Open both interfaces in your browser:

- **http://127.0.0.1:5000/tank** — workbook-derived fill-volume calculator.
- **http://127.0.0.1:5000/** — temperature history/alert/health dashboard.

If PowerShell blocks environment activation, run `.venv\Scripts\python.exe` instead of `python` for each command. Keep the terminal open; press **Ctrl+C** to stop. This does **not** delete the SQLite database.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m scripts.fetch_original_workbook
python -m scripts.prepare_application
python -m pytest -q
python -m scripts.verify_capstone
python scripts/start_capstone.py
```

**Offline limitation:** The original workbook is bundled and checked locally. First setup still uses Git to fetch a pinned revision of the public Module 7.2 application (see `scripts/prepare_application.py`). The app cannot initialize from a fresh checkout without Internet/Git. Once prepared it can replay the bundled sensor CSV locally without Internet.

## What I inherited (Module 1)

`TANK_FILL_rev4.xlsx` recorded **18 tank-fill runs** in the `Tank Fill` sheet and their source measurements in `Field Notes`. It calculated US gallons for rectangular tanks from **length (ft), width (ft), depth (in)**:

```text
volume_gal = length_ft * width_ft * (depth_in / 12) * 7.48052
```

Two verifiable problems appeared in the inherited artifact:

1. Run **R-108**: the original Field Notes depth was **2.5 ft** but the spreadsheet's inches column used **2.5**, instead of the correct **30 in**. The erroneous output was **93.5065 US gal** instead of **1122.078 US gal**. The source case understated that run by **1028.5715 gal**.
2. Cell **G25** had `SUM(G6:G17)` and omitted the last six recorded runs (`G18:G23`). The Module 1 defect report gives a reported total of **8527.79 gal** versus a fully corrected total of **14175.59 gal**. Those original aggregate figures are *documented historical investigation results*, not claimed as freshly recomputed from the original 18-row workbook in this package.

See `original/README.md` and the original repository's `DEFECTS.md` for source evidence.

## What I built

| Component | Purpose | Code |
|---|---|---|
| Workbook calculator | Calculate rectangular-tank fill volume; explicitly select depth units | `capstone/tank_fill.py` |
| Form & JSON API | Web input, visible units, refusal messages, full-run total endpoint | `capstone/routes.py` |
| Integrated Flask startup | Adds calculator routes to inherited live monitor | `capstone_launcher.py` |
| Automatic app restart | Restarts integrated Flask process after crash; does not reset SQLite | `capstone_supervisor.py` |
| Temperature monitor | Preserves source timestamps, accepted/rejected rows, alert state, health | Prepared `application/` checkout from Module 7.2 |
| Log/recovery evidence | Actual Module 7.2 failure timeline, browser captures and SQLite checks | [Module 7.2 evidence](https://github.com/Barquito0/EGN-321-Module-7_2/tree/main/evidence) |
| Automated tests | Original known-correct, known-defect, invalid, student-created, and HTTP cases | `tests/` |
| Setup & deployment | Verified workbook retrieval, monitor download, supervised launch | `scripts/` |

**The Module 4.2 capstone *proposal* discussed a separate synthetic SyntraTech financial-planning workbook.** That financial-planning product was not developed into the Module 7 temperature monitor and is not presented as implemented here. This final delivery traces the Module 1 tank-fill calculation to an actual implemented calculator and separately documents the sensor-monitoring strand.

## Calculator: inputs, units and refusal behavior

`POST /api/tank-volume` accepts a JSON object:

```json
{"length_ft": 10, "width_ft": 6, "fill_depth": 2.5, "depth_unit": "ft"}
```

Successful result:

```json
{"volume_gallons": 1122.078, "depth_inches_used": 30.0,
 "depth_unit_supplied": "ft", "method": "rectangular tank volume"}
```

**Required:** `length_ft` and `width_ft` in feet (>0), `fill_depth` as finite numeric (≥0), and `depth_unit` **explicitly** chosen from `in` or `ft`. Results are in **US gallons**. The calculator does not guess a missing unit. It refuses negative or zero length/width, negative depth, strings, NaN, infinity, boolean values, missing input and unsupported depth units with HTTP `400/422` and a clear error. Do not enter irregular tanks or use this as a certified fluid-flow/safety controller. Physical tank height is not supplied, so the tool cannot detect overfill.

`POST /api/tank-total` requires a nonempty `runs` list with a unique `run_id` for each row plus the fields above. It sums **every provided row** instead of a fixed spreadsheet range; one missing/invalid run refuses the whole total. The web form is for **one tank**; batch totals use the documented JSON endpoint, not a separate upload form.

## Exact workbook tests and expected numbers

| Test | Source/inputs | Expected result | New logic |
|---|---|---:|---|
| Known-correct 1 | R-103, 10 ft × 6 ft × 12 in | 448.8312 gal | Should match |
| Known-correct 2 | R-116, 12 ft × 5 ft × 22 in | 822.8572 gal | Should match |
| Workbook defect | R-108, 2.5 **ft**, 10 ft × 6 ft | 1122.078 gal | Explicit conversion to 30 in |
| Invalid | 10 ft × 6 ft × **−1 in** | **Refused** | No misleading output |
| Student-created | 18 uniquely identified 10 × 6 × 12-in runs | 8078.9616 gal | Includes all 18 rows |

The final student-created set is deliberately a **synthetic uniform-depth fixture**, **not** the actual original workbook's 18 different measurements. This distinction matters for traceability.

Run `python -m pytest -q` and `python -m scripts.verify_capstone`. The latter writes `evidence/workbook_verification.json` using the actual Python calculations. The GitHub Actions workflow additionally installs the pinned monitor, runs its inherited tests, and performs real HTTP smoke checks of `/tank`, `/api/status`, and SQLite-backed archive history. CI smoke evidence is generated when the workflow runs, not preclaimed.

## Temperature sensor: inputs, status and alerts

The original Module 6 archive contains **1,756 time-stamped rows, each with 5 sensor fields = 8,780 individual SQLite readings**. Archived source timestamps are not disguised as current readings. Temperature monitoring uses replay *arrival* timestamps and separates original archive rows from newly replayed data. Its classroom feed samples approximately **every 2 seconds**; source archive nominal samples were **every 60 seconds**. The original archive has **45 genuinely absent timestamp slots** across two gaps, distinct from explicitly rejected readings.

**Temperature validation** accepts numeric finite values 0–50 °C with source status `OK`. Other readings are kept as rejected and do not masquerade as accepted. A sustained temperature alert activates after **3 consecutive accepted readings at or above 30.0 °C** and clears after **2 consecutive readings at or below 28.5 °C**, providing persistence and hysteresis.

| Health | Meaning |
|---|---|
| `RECOVERING` | Starting or awaiting first replay arrival |
| `HEALTHY` | Fresh accepted replay data and no threshold alert |
| `DEGRADED` | Rejected/missing input, active high-temperature alert, or input older than 8 s |
| `FAILED` | No replay input for more than 18 s; `/healthz` can return HTTP 503 |

Set `REPLAY_SECONDS`, `STALE_DEGRADED_SECONDS`, `STALE_FAILED_SECONDS`, `PORT`, and `CLASSROOM_DEMO` in the environment as documented in Module 7.2. The student-created tank API is **not a physical tank-level sensor** and does not use the temperature to compute tank volume.

## Logs, failure, recovery

- **SQLite:** `application/state/monitor.db` (runtime file; never delete to make a failure disappear).
- **JSONL:** `application/logs/monitor.jsonl` (process and sensor events).
- **Dashboard:** http://127.0.0.1:5000/ and `/api/status`, `/api/history?mode=archive`.
- **Evidence:** [actual Module 7.2 controlled failure report](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/FAILURE_REPORT.md), [logs](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/application_logs.jsonl), [failure timeline](https://github.com/Barquito0/EGN-321-Module-7_2/blob/main/evidence/timeline.csv), [screenshots](https://github.com/Barquito0/EGN-321-Module-7_2/tree/main/evidence).

**Recovery procedure (controlled source pause)**

1. Start the integrated app with `python scripts/start_capstone.py`.
2. To pause source replay (classroom failure only): `python scripts/source_control.py pause` after the app is prepared. Watch `/` move to DEGRADED, then FAILED. Capture logs and health outputs. Do not delete history.
3. Restore input using `python scripts/source_control.py resume`.
4. Wait for a new accepted reading, confirm health becomes HEALTHY at `/api/status`, verify SQLite remains accessible and inspect `application/logs/monitor.jsonl` for `SOURCE_PAUSED`, `STALE_INPUT`, `INPUT_FAILED`, `SOURCE_RESUMED`, `HEALTH_RECOVERED`.
5. If Flask crashes, supervisor will try restarting it. If the whole computer or disk fails, someone must restore the host/storage. Do not claim this program cures hardware faults.

**Troubleshooting:** `No module named flask` → install requirements in active venv. `Application folder not found` → run `python -m scripts.prepare_application`. `Port already in use` → set `PORT` to free local port. `FAILED` with no new data → check pause flag and source CSV; resume without wiping DB. Database error → preserve file and inspect permissions and SQLite logs rather than silently regenerate existing records.

## Assumptions and limitations

- Rectangular geometry; stated feet/inches units; US gallons conversion factor 7.48052.
- No physical tank height, wall thickness or measurement uncertainty model. No irregular geometry.
- Course temperature replay from an *instructor-provided simulator*; not calibrated physical sensor hardware.
- Flask development server on loopback only; not publicly hardened or production-ready.
- Inherited temperature monitor and tank calculation are separate subsystems, not a unified hardware control circuit.
- Module 8.1 contains a **draft Megan Kahn handoff report**; a real assigned-classmate silent test and actual post-test improvements must be documented before claiming those as observed evidence.
- The exact original workbook is bundled and hash-verified. First installation still needs Git and Internet to retrieve the pinned historical temperature-monitor application and Python dependencies.

## Presentation and technical defense

**Narrated video:** [Watch or download the narrated final presentation (MP4)](presentation/EGN321_Final_Capstone_Narrated.mp4) — 1080p, approximately 9 minutes 48 seconds. The editable slide deck remains at [`presentation/EGN321_Final_Capstone.pptx`](presentation/EGN321_Final_Capstone.pptx).



See `presentation/EGN321_Final_Capstone.pptx`, `docs/PRESENTATION_SCRIPT.md`, and `docs/LIVE_DEMO_CHECKLIST.md`. During the defense **do not use AI**. Practice the four source locations: `capstone/tank_fill.py` (formula and validation), `capstone/routes.py` (form/API), `application/src/alerting.py` (persistence/hysteresis), and `application/src/health.py` (timeouts).

## AI assistance

See `AI_LOG.md` for AI involvement, accepted corrections, verification method, and known limits. AI-generated output is not evidence of independent lab testing unless the actual test ran and the logs show it.
