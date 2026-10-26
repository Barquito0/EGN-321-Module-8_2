"""Integrated course capstone Flask app: workbook calculator + inherited monitor.

The Module 7 monitor is fetched at a pinned commit using the explicit installer.
Live state remains in application/state/monitor.db, never overwritten by this app.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def create_app():
    appdir=ROOT/'application'
    if not (appdir/'app.py').is_file():
        raise RuntimeError('Monitoring app not prepared. Run: python scripts/prepare_application.py')
    if str(appdir) not in sys.path:
        sys.path.insert(0,str(appdir))
    import app as inherited
    from capstone.routes import bp
    if 'tank_capstone' not in inherited.app.blueprints:
        inherited.app.register_blueprint(bp)
    return inherited


def main():
    inherited=create_app()
    inherited.launch()
    inherited.app.run(host=os.environ.get('HOST','127.0.0.1'),
                      port=int(os.environ.get('PORT','5000')),
                      debug=False,use_reloader=False,threaded=True)

if __name__=='__main__':
    main()
