# Phone / Termux — Pixel 10 (Full 04901 Toolkit)

Everything you need to run the **full 04901-sentinel** toolkit (and your other scripts) directly on your Google Pixel 10 using **Termux**.

This is how you "incorporate it all to my Pixel 10".

## What's Included for the Phone

- `pixel_shipper.py` — The core Pixel 10 GPS telemetry shipper. Sends high-accuracy location over TCP to your Linux daemon (this Debian box or any reachable host).
- `termux_setup.sh` — One-time (or refresh) bootstrap script that installs everything you need.
- `monitor.py` (at repo root) — Convenience wrapper so `python monitor.py --mock` etc. works exactly like on your desktop.
- Full `bounty/` hunter — Run real or mock NVD CVE monitoring and research dossier generation from your phone.
- The rest of the repo (src/, etc.) comes along for free via git.

Other desktop scripts (`rag_indexer.py`, `fbi_osint_scanner_v0.4.py`) are more NAS / workstation oriented and not auto-included, but you can pull individual files if you want them later.

## One-Time Setup on Your Pixel 10 (Recommended Path)

In Termux on the phone:

```bash
# 1. Install Termux + the API companion app first (from F-Droid is best)
#    Grant the Termux:API app Location (and any other) permissions.

# 2. Bootstrap the full toolkit
pkg update && pkg install git python termux-api

git clone https://github.com/keithdickey207/04901-sentinel.git
cd 04901-sentinel

# 3. Run the dedicated phone setup script (installs deps + shows usage)
chmod +x phone/termux_setup.sh
./phone/termux_setup.sh
```

The setup script will:
- Make sure git + python + termux-api are present
- Install `requests` (needed for the bounty hunter)
- Print ready-to-run examples for both the shipper and the hunter

## Daily / Update Flow ("update my phone with my github")

```bash
cd ~/04901-sentinel          # or wherever you cloned it
git pull

# Re-run the setup script any time you want a refresh
./phone/termux_setup.sh
```

That's it. All of "it" (the sentinel + phone components + bounty tools) stays in sync with your GitHub.

## Running the Pixel 10 Location Shipper

```bash
# Easiest (recommended)
export DAEMON_IP=10.64.40.230     # your Debian box IP (update when it changes)
python phone/pixel_shipper.py

# Or with explicit flags
python phone/pixel_shipper.py --ip 10.64.40.230 --port 9876 --interval 60
```

**Before long runs, lock the wake:**
```bash
termux-wake-lock
```

The script will keep shipping `{ "event_type": "location_update", "payload": {lat, lon, accuracy, timestamp} }` until you kill it (Ctrl-C).

**Tips for always-on / background:**
- `termux-wake-lock` + run in a tmux/screen session
- Look into `termux-services` package for proper service management
- For connectivity from anywhere: run a VPN (Tailscale, WireGuard, ZeroTier) on both the phone and the Debian box so the IP is stable and reachable.

Update the `DAEMON_IP` export in your `~/.bashrc` (or Termux equivalent) once you have a stable address.

## Running the Bug Bounty Hunter on Your Phone

```bash
# From the repo root (after cd 04901-sentinel)
python monitor.py --help
python monitor.py --mock
python monitor.py --days 1 --min-cvss 8

# Alternative module form (also works)
python -m bounty.monitor --mock
```

It will create `bounty/reports/` and use `bounty/storage/ledger.json` (the ledger is gitignored so your phone's tracking state stays local).

Great for on-the-go research or when you're away from your main machine.

## Full "Incorporate It All" Checklist

1. Clone or pull the repo on the phone (git pull = your update mechanism).
2. Run `./phone/termux_setup.sh` (or do the pkg + pip steps manually).
3. (Optional but nice) `termux-wake-lock`
4. Start the shipper with your current daemon IP.
5. Use `python monitor.py ...` whenever you want the bounty tools on the device.
6. `git pull` whenever you make changes on desktop or want the latest from GitHub.

## Adding More of "Your" Scripts Later

Your other root scripts live on the desktop:
- `fbi_osint_scanner_v0.4.py`
- `rag_indexer.py`

If you want any of them on the phone, just `git pull` won't bring them (they're not in the 04901-sentinel tree yet). You have a few options:
- Manually `cp` them into the repo (e.g. `phone/fbi_osint_scanner.py`) and commit/push, then `git pull` on phone.
- Use your existing `Sync/` (Syncthing) folder — drop files there on the desktop and they'll appear on the phone.
- `scp` / `rsync` / USB file transfer from the Debian box.

We deliberately kept the phone/ subtree focused on the location shipper + the full bounty toolkit.

## Current Known Daemon Address (update as needed)

As of last desktop session: `10.64.40.230` (the Debian box on your local network).

Change it in the `export DAEMON_IP=...` line or pass `--ip` every time.

## Troubleshooting

- `termux-location` command not found → Install + grant perms to the Termux:API app.
- No network delivery → Check firewall on the receiving side, confirm the IP is reachable from the phone (same LAN or VPN), and that something is listening on the port.
- GPS is old/stale → The script uses `-r last`; move outside or force a fresh fix if needed.
- Want to run in background forever → Combine wake-lock + tmux + a small wrapper script.

---

"04901 Sentinel standing by — now also on your Pixel 10."

See the main repo README for the bigger picture (satellite tracker, etc.).