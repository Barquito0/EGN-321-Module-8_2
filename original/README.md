# Original inherited workbook — traceable source

The real Module 1 artifact is **`TANK_FILL_rev4.xlsx`** from the student's original repository:

- [Original XLSX file](https://github.com/Barquito0/EGN-321-Module-1/blob/main/original/TANK_FILL_rev4.xlsx)
- [Original defect investigation](https://github.com/Barquito0/EGN-321-Module-1/blob/main/DEFECTS.md)
- [Original formula tests](https://github.com/Barquito0/EGN-321-Module-1/blob/main/tests/test_tank_fill.py)

**Git blob SHA of exact workbook:** `144c878d815abb234fa34d2f56d6670a23a9ba72`

The original workbook is included at `original/TANK_FILL_rev4.xlsx` in this capstone repository. Verify its exact SHA (and download it only if absent) with:

```bash
python scripts/fetch_original_workbook.py
```

The fetch script compares the workbook's Git object hash and refuses unexpected bytes. It never overwrites an existing file. The capstone copy is byte-identical to the original Module 1 artifact.

**Do not substitute the instructor's Module 8 demo workbook** or the synthetic SyntraTech planning workbook for this original. These are different engineering artifacts. The present capstone's original-workbook tests use recorded Module 1 values and comparisons, not fabricated observations.
