#!/data/data/com.termux/files/usr/bin/env python
"""
Pixel 10 / Termux GPS Telemetry Shipper

Part of 04901-sentinel phone toolkit.

Runs on your Google Pixel (via Termux + Termux:API) and ships high-accuracy
location updates to a listening daemon (usually your Linux box) over plain TCP JSON.

Update "it all" on your phone with:
    git pull   (from inside the cloned 04901-sentinel repo)

Env var support for easy use:
    export DAEMON_IP=10.64.40.230
    python phone/pixel_shipper.py
"""

import subprocess
import json
import socket
import time
import argparse
import os
from datetime import datetime


def get_device_location():
    """Queries Android hardware for high-accuracy GPS coordinates via Termux."""
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'gps', '-r', 'last'],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"[!] Hardware GPS query failed: {e}")
        return None


def ship_telemetry(ip, port, interval):
    print(f"[*] Initializing Pixel 10 Spatiotemporal Link -> {ip}:{port}")

    while True:
        loc_data = get_device_location()
        if loc_data and "latitude" in loc_data:
            payload = {
                "event_type": "location_update",
                "payload": {
                    "lat": loc_data["latitude"],
                    "lon": loc_data["longitude"],
                    "accuracy": loc_data.get("accuracy", 0),
                    "timestamp": datetime.now().isoformat()
                }
            }

            try:
                # Open a brief, raw TCP socket to the orchestrator, drop the payload, and close it
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5.0)
                    s.connect((ip, port))
                    s.sendall(json.dumps(payload).encode('utf-8'))
                print(f"[✓] {datetime.now().strftime('%H:%M:%S')} - Shipped: {payload['payload']['lat']}, {payload['payload']['lon']}")
            except Exception as e:
                print(f"[!] Network delivery failed. Daemon offline? ({e})")

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pixel 10 Local Telemetry Shipper (Termux)")
    parser.add_argument("--ip", help="Target Linux Daemon IP (or set DAEMON_IP env var)")
    parser.add_argument("--port", type=int, default=9876, help="Target TCP Port")
    parser.add_argument("--interval", type=int, default=60, help="Seconds between GPS pings")
    args = parser.parse_args()

    target_ip = args.ip or os.environ.get("DAEMON_IP")
    if not target_ip:
        parser.error("--ip is required (or export DAEMON_IP=...)")

    ship_telemetry(target_ip, args.port, args.interval)