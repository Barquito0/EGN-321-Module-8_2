# 8–10 minute oral presentation — speaker notes (practice, not script to read verbatim)

## Slide 1 — What I inherited (about 1 minute)
I started with `TANK_FILL_rev4.xlsx`, an Excel workbook for calculating rectangular-tank fill volumes. Each run takes feet for length and width, inches for depth, and returns US gallons. The original source remains available in my Module 1 repository. My final capstone adds a standalone tank calculation to the Flask interface of my monitoring project, but these were separate course activities.

## Slide 2 — What needed improvement (about 1 minute)
In R-108, the Field Notes entry was 2.5 **feet**, but the Tank Fill table treated that number as 2.5 **inches**. That resulted in 93.5065 gallons when the correct value was 1122.078. The sum formula also stopped before six valid rows. The defect matters because the spreadsheet calculated a number without an error message.

## Slide 3 — How the system grew (about 1 minute)
Module 1 was defect investigation; Modules 2 and 3 emphasized units, validation and reusable tests. Separately, Modules 5 to 7 produced a replayed temperature-monitoring application with SQLite history, health states, alerts, logs, and process recovery. Module 8 focused on operating documentation and exposing the original calculation as a second, clearly identified Flask view. The Module 4 financial-forecast workbook remained a proposal and isn't described as completed functionality.

## Slide 4 — Final architecture (about 1 minute)
The two paths are intentionally separate. The workbook path takes length, width, depth, and a declared unit, validates them, then computes gallons. The monitoring path replays existing sensor history, validates and stores readings in SQLite, and reports status with persisted alerts. Flask presents both, and the capstone supervisor restarts its process if it exits unexpectedly.

## Slide 5 — Live demonstration (1–1.5 minutes)
Open `/tank`. Enter 10, 6, 12 and inches, then calculate: 448.8312 gallons. Change depth to 2.5 and unit to feet: it converts to 30 inches and returns 1122.078. Enter -1 inches: it refuses the invalid request. Open `/` to show the temperature replay and history chart, then view `/api/status`.

## Slide 6 — Why trust the calculations? (about 1 minute)
Compare known workbook cases R-103 and R-116 directly with the original recorded expectations. The R-108 test catches the original wrong-unit problem. Invalid inputs cause a refusal; a student-created 18-run fixture tests that every supplied run contributes to the total. The fixture is not presented as a reproduction of the original workbook's 18 distinct measurements.

## Slide 7 — Failure, recovery, and evidence (about 1 minute)
Module 7.2 has genuine CI-captured evidence for a controlled source stop: SOURCE_PAUSED, STALE_INPUT, INPUT_FAILED, SOURCE_RESUMED, and HEALTH_RECOVERED. The SQLite archive remained 8,780 rows and passed integrity checks. Our capstone's new integrated HTTP smoke script must also pass in CI before claiming the integrated app was live-tested.

## Slide 8 — Limits, handoff, and defense (about 1 minute)
The calculator assumes a rectangular tank and does not know tank height or measure real fluid level. The monitor replays classroom data, not calibrated physical measurements, and the Flask server is local only. Module 8.1 prepared detailed handoff instructions; the draft operator report is not independently verified as a completed assigned-classmate test. During the instructor's code challenge, I will identify the correct function and run tests without AI assistance.

## Likely questions / independent code defense

**Q: Why require a depth unit?** Because the workbook R-108 defect came from treating 2.5 ft as 2.5 in.

**Q: How do you know the new calculator is right?** Recompute the module's known correct R-103/R-116 values and corrected R-108 using the documented formula and pytest.

**Q: What proves missing data isn't forged?** The Module 6 archive preserves original timestamps/status; source replay uses separate arrival times and SQLite indexes.

**Q: How do you change a threshold?** Locate the corresponding validation/alert constant, document the meaning, add or edit a test, rerun pytest. Do not make untested changes live.
