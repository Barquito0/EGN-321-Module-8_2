"""Actual local HTTP smoke test of the integrated inherited monitor + tank app.

This runs only after application/ has been bootstrapped from GitHub.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import URLError

ROOT=Path(__file__).resolve().parents[1]
PORT='54329'
BASE=f'http://127.0.0.1:{PORT}'

def request_json(path, body=None):
    headers={}
    payload=None
    if body is not None:
        headers['Content-Type']='application/json'
        payload=json.dumps(body).encode()
    req=Request(BASE+path,data=payload,headers=headers)
    with urlopen(req,timeout=2) as res:
        return res.status,res.read().decode('utf-8')


def main():
    env={**os.environ,'PORT':PORT,'HOST':'127.0.0.1','CLASSROOM_DEMO':'0','REPLAY_SECONDS':'.4'}
    process=subprocess.Popen([sys.executable,'-u',str(ROOT/'capstone_launcher.py')],cwd=ROOT,
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env=env)
    try:
        reached=False
        for _ in range(100):
            if process.poll() is not None:
                raise AssertionError(f'Integrated Flask exited early with code {process.returncode}')
            try:
                status,html=request_json('/tank')
                if status==200 and 'Tank Fill Calculator' in html:
                    reached=True;break
            except (URLError,OSError):time.sleep(.2)
        assert reached,'Tank UI not reachable'
        status,result=request_json('/api/tank-volume',
                          {'length_ft':10,'width_ft':6,'fill_depth':2.5,'depth_unit':'ft'})
        assert status==200 and abs(json.loads(result)['volume_gallons']-1122.078)<1e-8
        status,status_data=request_json('/api/status')
        assert status==200 and 'health' in json.loads(status_data)
        status,history=request_json('/api/history?mode=archive&limit=15')
        assert status==200 and len(json.loads(history)['rows'])==15
        print('PASS: running integrated app, tank volume, sensor status, original SQLite archive')
        (ROOT/'evidence'/'integration_smoke.json').write_text(json.dumps({
            'status':'PASS','tank_gallons':1122.078,'sensor_http_status':status,
            'archive_rows_returned':15,'evidence_origin':'actual local HTTP test'},indent=2)+'\n')
    finally:
        process.terminate()
        try:process.wait(timeout=8)
        except subprocess.TimeoutExpired:process.kill();process.wait()

if __name__=='__main__':main()
