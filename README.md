# 04901-sentinel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/keithdickey207/04901-sentinel/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/keithdickey207/04901-sentinel?style=social)](https://github.com/keithdickey207/04901-sentinel)
[![GitHub](https://img.shields.io/badge/GitHub-keithdickey207/04901-sentinel-181717?logo=github)](https://github.com/keithdickey207/04901-sentinel)

**Real-time satellite visibility tracker and ground station daemon.**

Tracks NORAD 39634 ("Sentinel") and reports when it is above the local horizon from a fixed observer in Maine. Provides continuous telemetry + change-of-state alerts. Designed for always-on operation with minimal dependencies.

---

## Features

- **Live tracking** — Computes topocentric altitude using SGP4/SDP4 via `ephem`
- **Auto TLE refresh** — Pulls fresh elements from CelesTrak every 6 hours
- **Horizon alerts** — Prints `ALERT: ONLINE/OFFLINE` exactly when the satellite crosses the horizon
- **Resilient** — Graceful handling of network blips, keeps running for days
- **One-shot installer** — `install.sh` sets up venv + background daemon + system logs
- **Extensible vault** — `zero_vacuum.py` stub ready for encrypted logs + push notifications (ntfy)

## Observer Location

Hard-coded for development:

- Lat: 44.5520° N
- Lon: -69.6317° W
- Elev: 33 m

(Waterville / central Maine area — same reference location used in related chronosat work.)

## Quick Start (Interactive)

```bash
git clone https://github.com/keithdickey207/04901-sentinel.git
cd 04901-sentinel

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/sentinel_daemon.py
```

You should see:

```
04901 Sentinel started
Telemetry: -12.34° OFFLINE
...
ALERT: ONLINE at 3.21°
Telemetry: 3.21° ONLINE
```

## Daemon / "Production" Install

```bash
# As a user that can write /var/log (or edit script)
bash install.sh
```

This does:
- Creates `/var/log/04901-sentinel/`
- Builds local venv
- Installs requirements
- Starts the daemon in background via nohup
- Writes PID to `/tmp/04901-sentinel.pid`

Watch logs:

```bash
tail -f /var/log/04901-sentinel/daemon.log
```

Stop:

```bash
kill $(cat /tmp/04901-sentinel.pid)
```

## Configuration

All configuration lives at the top of `src/sentinel_daemon.py`:

```python
OBS_LAT = "44.5520"
OBS_LON = "-69.6317"
OBS_ELEV = 33
NORAD = "39634"
```

Change and restart. For production use a config file or env vars (future improvement).

## Project Layout

```
04901-sentinel/
├── src/
│   ├── sentinel_daemon.py   # Main tracker / alerting loop
│   └── zero_vacuum.py       # Secure logger + vault stub (ntfy integration point)
├── install.sh
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## How the Tracking Works

1. On startup (and every 6h) fetch current TLE for the NORAD ID from Celestrak.
2. Use `ephem` to set observer + load TLE as a satellite.
3. Every 60s compute current altitude.
4. If `alt > 0` → visible ("ONLINE"). Crossing the 0° line triggers an alert print.

This is a very lightweight "is it up?" visibility predictor. It does **not** account for:
- Terrain / buildings
- Sunlight / terminator (for optical)
- Precise AOS/LOS with refraction or minimum elevation mask

For serious pass prediction use something with Skyfield + proper TLEs + masks.

## Secure Logging & Notifications (Roadmap)

`zero_vacuum.py` currently provides a no-op `SecureLogger` and a `load_vault()` that returns the ntfy endpoint `https://ntfy.sh/keith_04901_vault`.

Planned:
- Encrypt sensitive alert payloads
- POST rise/set events to ntfy (phone push)
- Optional local encrypted log append

Contributions or pairing on the crypto side welcome.

## Requirements

- Python 3.9+
- `ephem==4.1.5`
- `requests==2.32.3`
- `cryptography==42.0.5` (currently unused, reserved for vault)

## Related Projects

- [chronosat](https://github.com/keithdickey207/chronosat) — Historical Landsat 1-3 / Skylab data tools (same observer coords)
- [dotfiles](https://github.com/keithdickey207/dotfiles) — Personal env including SDR / satellite tooling
- goodperson — Daily practice CLI

## License

MIT License

Copyright (c) 2026 Keith Dickey

See [LICENSE](LICENSE) for full text.

## Contributing

Issues and PRs welcome. Especially interested in:

- Better pass prediction / next-event table
- Systemd service file + packaging
- Real rotator / SDR integration hooks
- Config-driven observer + multiple NORADs

## Links

- **Repo**: https://github.com/keithdickey207/04901-sentinel
- **Issues**: https://github.com/keithdickey207/04901-sentinel/issues
- **Author**: https://github.com/keithdickey207

---

"04901 Sentinel standing by."
