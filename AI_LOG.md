# AI assistance record — Module 8.2 capstone

AI was used as a development assistant to organize the integration, produce unit-aware tank calculations, Flask form/API routes, supervisor wrapper, automated tests, documentation and presentation materials. The exact original formula/cases were retrieved from the student's published Module 1 `src/tank_fill.py`, `tests/test_tank_fill.py`, and `DEFECTS.md`; the Module 6/7 evidence came from the student's prior GitHub projects. AI did **not** invent new workbook measurements or partner screenshots.

## Tasks and decisions

- **Prompt/task:** Merge the verifiable Module 1 tank-fill calculation with the existing independently developed Module 7.2 Flask sensor monitoring application for the final course capstone. **Accepted:** a two-panel local interface, explicit units, reusable calculator, baseline monitor fetched at pinned revision. **Rejected:** pretending temperature sensors measure liquid height or that the Module 4 synthetic financial-planning proposal had been delivered.
- **Prompt/task:** Design known-workbook comparison cases and invalid/edge tests. **Accepted:** R-103 = 448.8312, R-116 = 822.8572, R-108 corrected = 1122.078; invalid-depth refusal; student-created complete 18-run fixture. **Verification:** local pytest for calculation logic, actual generated JSON report; Flask HTTP tests additionally require Flask to be installed. Original workbook's full 18-row aggregate has only been sourced from the Module 1 defect report, not independently recomputed in this package.
- **Prompt/task:** Document safe source replay failure and recovery. **Accepted:** link to original Module 7.2 JSONL, SQLite and screenshots; do not fabricate a new event timeline.
- **Prompt/task:** Develop presenter materials and technical-defense practice. **Accepted:** editable slides, demo instructions and code challenge examples. **Restriction:** no AI during actual live instructor defense.

## Verification and limitations

At initial artifact preparation the local environment lacked Flask and network package installation, so the non-Flask calculation tests were executed locally; Flask-specific tests were written but skipped locally, and full integrated run was delegated to the included GitHub Actions workflow once the project is published and CI can install Flask and fetch the existing GitHub repositories. Any claim of an integrated end-to-end test passing requires inspecting the actual CI result. The original workbook downloader checks the exact Git blob SHA and refuses unverified changes. The Megan Kahn handoff report in Module 8.1 remains a **draft** pending evidence of a real permitted operator test.
