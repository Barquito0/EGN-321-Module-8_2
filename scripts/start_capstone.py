"""Single command to run both workbook calculator and temperature monitor.

Run from repository root: python scripts/start_capstone.py
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    if not (ROOT/'application'/'app.py').is_file():
        raise SystemExit('Monitoring application missing. Run python scripts/prepare_application.py first.')
    env=os.environ.copy()
    for key,val in {'HOST':'127.0.0.1','PORT':'5000','REPLAY_SECONDS':'2','CLASSROOM_DEMO':'0',
                    'STALE_DEGRADED_SECONDS':'8','STALE_FAILED_SECONDS':'18','PYTHONUNBUFFERED':'1'}.items():
        env.setdefault(key,val)
    print('Starting integrated capstone:')
    print(f'  Monitoring: http://127.0.0.1:{env["PORT"]}/')
    print(f'  Tank volume: http://127.0.0.1:{env["PORT"]}/tank')
    try:
        subprocess.run([sys.executable, '-u', str(ROOT/'capstone_supervisor.py')],cwd=ROOT,env=env,check=False)
    except KeyboardInterrupt:
        print('Capstone stopped; SQLite history has been preserved.')

if __name__=='__main__':main()
