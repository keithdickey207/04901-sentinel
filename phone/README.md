# Phone / Termux (Pixel)

Scripts intended to run on an Android device (Google Pixel recommended) using **Termux**.

## pixel_shipper.py

Lightweight GPS telemetry shipper.

- Uses `termux-location` (high-accuracy GPS via Android hardware).
- Sends periodic JSON location updates over a plain TCP socket to a listening daemon/orchestrator (typically your Linux box on the same network or via port forward).
- Designed for always-on background use in Termux.

### One-time Termux setup on phone

```bash
pkg update && pkg install python termux-api
# Install the companion "Termux:API" app from F-Droid or GitHub and grant it location permission.
```

### Get / update the code from GitHub (this is how you "update your phone with my github")

```bash
# First time
git clone https://github.com/keithdickey207/04901-sentinel.git
cd 04901-sentinel

# Later updates (run this on the phone to pull the latest from GitHub)
git pull
```

### Run the shipper

```bash
# Point --ip at the machine running your daemon (this Debian box when on LAN, or its public IP)
python phone/pixel_shipper.py --ip 10.64.40.230 --port 9876 --interval 60
```

Flags:
- `--ip` (required): target daemon IP
- `--port`: default 9876
- `--interval`: seconds between pings (default 60)

The script will keep running and shipping lat/lon + accuracy + timestamp.

### Updating in the future

Just `git pull` inside the cloned repo on your phone, then restart the shipper process. That's the entire "update my phone with my github" flow.

### Notes
- Keep Termux running (or use a wake lock / termux-wake-lock if available).
- For production you may want to wrap it in a simple loop or use termux-services / crond.
- The receiving side just needs to listen on the TCP port and parse the JSON `{"event_type": "location_update", "payload": {...}}`.

Part of the 04901-sentinel toolkit.
