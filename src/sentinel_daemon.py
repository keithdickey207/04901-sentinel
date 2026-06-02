#!/usr/bin/env python3
import signal, sys, time, math, requests
from datetime import datetime, timedelta, timezone
import ephem

OBS_LAT = "44.5520"
OBS_LON = "-69.6317"
OBS_ELEV = 33
NORAD = "39634"
CELESTRAK = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={NORAD}&FORMAT=TLE"

class Tracker:
    def __init__(self):
        self.observer = ephem.Observer()
        self.observer.lat = OBS_LAT
        self.observer.lon = OBS_LON
        self.observer.elevation = OBS_ELEV
        self.last_status = None
        self.last_update = datetime.min.replace(tzinfo=timezone.utc)
        self._load_tle()
        signal.signal(signal.SIGTERM, lambda s,f: sys.exit(0))
        signal.signal(signal.SIGINT, lambda s,f: sys.exit(0))

    def _load_tle(self):
        try:
            r = requests.get(CELESTRAK, timeout=10)
            lines = r.text.strip().splitlines()
            if len(lines) >= 3:
                self.tle1 = lines[1].strip()
                self.tle2 = lines[2].strip()
        except:
            self.tle1 = "1 39634U 14016A   26150.12345678  .00001234  00000-0  12345-4 0  9999"
            self.tle2 = "2 39634  98.1800  15.1234 0001234  45.6789  12.3456 14.56789012345678"
        self.satellite = ephem.readtle("Sentinel", self.tle1, self.tle2)

    def get_alt(self):
        self.observer.date = ephem.now()
        self.satellite.compute(self.observer)
        return round(math.degrees(self.satellite.alt), 2)

    def run(self):
        print("04901 Sentinel started")
        while True:
            try:
                now = datetime.now(timezone.utc)
                if now - self.last_update > timedelta(hours=6):
                    self._load_tle()
                    self.last_update = now
                alt = self.get_alt()
                status = "ONLINE" if alt > 0 else "OFFLINE"
                if status != self.last_status:
                    print(f"ALERT: {status} at {alt}°")
                    self.last_status = status
                print(f"Telemetry: {alt}° {status}")
                time.sleep(60)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(120)

if __name__ == "__main__":
    Tracker().run()
