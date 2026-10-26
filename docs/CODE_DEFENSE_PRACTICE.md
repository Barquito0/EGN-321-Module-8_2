# Live code challenge rehearsal (practice in advance, no AI in live defense)

| Instructor request | Where to edit | What to verify |
|---|---|---|
| Change accepted depth to refuse zero instead of allow empty | `capstone/tank_fill.py`, `calculate_tank_volume` | Adjust `if depth < 0`, add boundary test, run pytest. Explain design tradeoff. |
| Support a separate 'cm' input depth | `capstone/tank_fill.py`, `calculate_from_units` | Add explicit conversion `cm / 2.54` to inches; require a new test; do not silently assume units. |
| Change temperature alert threshold from 30.0 to 29.5 °C | `application/src/alerting.py` after running setup | Update threshold and test 3-read persistence; consider recorded policy/docs. |
| Modify stale threshold from 8 to 10 seconds | `STALE_DEGRADED_SECONDS` runtime setting, `application/src/health.py` | Explain DEGRADED/FAILED changes and verify event log. |
| Change calculator form label | `capstone/routes.py` | Find `PAGE` and reload `/tank`; confirm units still explicit. |
| Add new log context field | `application/src/eventlog.py` | New JSON key in structured events; test not solely visual inspection. |

Answer defense questions from understanding: why feet-to-inches matters; why one noisy sensor reading does not trigger an alert; why old timestamps are not current; how SQLite preserves rejected readings; why a refusal is safer than a made-up value. **The assignment explicitly prohibits AI during the live code challenge.**
