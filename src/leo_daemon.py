from skyfield.api import wgs84, load
import time
import os

def run_leo_daemon():
    print("[*] LEO Orbital Daemon Initialized (Waterville Lattice)")
    ts = load.timescale()
    waterville = wgs84.latlon(44.5520, -69.6317)
    
    # Pre-load TLEs to memory to avoid constant external requests
    try:
        satellites = load.tle_file('http://celestrak.org/NORAD/elements/weather.txt')
    except Exception as e:
        print(f"[-] TLE Load Failure: {e}")
        return

    # Targeting the DMSP 5D-3 F16 or NOAA 19
    target_sat = next((sat for sat in satellites if 'DMSP' in sat.name or 'NOAA 19' in sat.name), satellites[0])
    print(f"[+] Tracking locked on {target_sat.name}")

    is_recording = False

    while True:
        t = ts.now()
        difference = target_sat - waterville
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()

        sys_status = f"EL: {alt.degrees:06.2f}° | AZ: {az.degrees:06.2f}°"
        
        if alt.degrees > 0.0 and not is_recording:
            print(f"\n[!] AOS (Acquisition of Signal) at {sys_status}")
            print("[+] Executing RF Handoff to RTL-SDR...")
            
            # TRIGGER THE SDR (VHF/UHF intercept)
            intercept = os.path.expanduser("~/projects/sovereign/intercept.wav")
            os.system(f"rtl_fm -f 137.9125M -s 60k -g 45 -p 55 -E wav -E deemp -F 9 - | sox -t raw -e signed -c 1 -b 16 -r 60000 - {intercept} &")
            is_recording = True

        elif alt.degrees < 0.0 and is_recording:
            print(f"\n[-] LOS (Loss of Signal) at {sys_status}")
            print("[*] Halting SDR intercept and saving to disk.")
            os.system("killall rtl_fm")
            is_recording = False
            
        time.sleep(10) # Recalculate every 10 seconds

if __name__ == '__main__':
    run_leo_daemon()
