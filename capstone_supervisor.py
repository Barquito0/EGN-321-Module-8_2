"""Restart integrated Flask capstone after an application process crash.

The inherited Module 7 event supervisor is in the original source. This light
supervisor launches the integrated /tank + monitoring app, not the old-only app.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    if not (ROOT/'application'/'app.py').exists():
        raise SystemExit('Run python scripts/prepare_application.py before startup.')
    tries=0
    while True:
        print(f'CAPSTONE_SUPERVISOR starting child (restart={tries})',flush=True)
        start=time.monotonic()
        child=subprocess.Popen([sys.executable,'-u',str(ROOT/'capstone_launcher.py')],cwd=ROOT,
                                env={**os.environ,'PYTHONUNBUFFERED':'1'})
        try:
            code=child.wait()
        except KeyboardInterrupt:
            print('Stopping child gracefully',flush=True)
            child.terminate()
            try:child.wait(timeout=7)
            except subprocess.TimeoutExpired:child.kill()
            return
        tries+=1
        print(f'CAPSTONE_SUPERVISOR child exited code={code}; scheduling restart',flush=True)
        time.sleep(3 if time.monotonic()-start<1 else 1)

if __name__=='__main__':main()
