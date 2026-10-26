"""Download exact inherited workbook; refuse to overwrite an existing workbook.

Git blob SHA was verified from Barquito0/EGN-321-Module-1 on Oct 25 2026.
"""
from __future__ import annotations
import shutil
import subprocess
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://github.com/Barquito0/EGN-321-Module-1.git'
BLOB='144c878d815abb234fa34d2f56d6670a23a9ba72'
DEST=ROOT/'original'/'TANK_FILL_rev4.xlsx'

def main():
    if DEST.exists():
        sha=subprocess.check_output(['git','hash-object',str(DEST)],text=True).strip()
        if sha!=BLOB:raise SystemExit(f'Unexpected workbook bytes: blob {sha}; expected {BLOB}. Preserve for review.')
        print('Original workbook already present and verified.');return
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['git','clone','--depth','1',SOURCE,d+'/source'],check=True)
        original=Path(d)/'source'/'original'/'TANK_FILL_rev4.xlsx'
        sha=subprocess.check_output(['git','hash-object',str(original)],text=True).strip()
        if sha!=BLOB:raise SystemExit('Upstream original workbook changed! Refusing unverified bytes.')
        DEST.parent.mkdir(exist_ok=True)
        shutil.copy2(original,DEST)
    print('Original workbook downloaded and blob-verified:',DEST)

if __name__=='__main__':main()
