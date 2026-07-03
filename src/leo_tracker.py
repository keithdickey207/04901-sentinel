from skyfield.api import wgs84, load

def track_leo_pass():
    print("[*] Initializing LEO Orbital Matrix...")
    
    # Load ephemeris time data
    ts = load.timescale()
    t = ts.now()
    
    # Local coordinates mapping
    waterville = wgs84.latlon(44.5520, -69.6317)
    
    # Fetch active weather satellite TLEs
    stations_url = 'http://celestrak.org/NORAD/elements/weather.txt'
    try:
        satellites = load.tle_file(stations_url)
    except Exception as e:
        print(f"[-] Failed to fetch TLE data. Ensure external outbound is permitted. {e}")
        return
    
    # Target a specific LEO satellite (NOAA 19 is a reliable VHF target)
    by_name = {sat.name: sat for sat in satellites}
    target_sat = None
    for name in by_name:
        if 'NOAA 19' in name:
            target_sat = by_name[name]
            break
            
    if not target_sat:
        target_sat = satellites[0] # Fallback
        
    print(f"[+] Lock acquired on {target_sat.name} (LEO)")
    
    # Compute the vector difference between Waterville and the Satellite
    difference = target_sat - waterville
    topocentric = difference.at(t)
    
    # Calculate geometric positioning
    alt, az, distance = topocentric.altaz()
    
    print(f"[*] Current Telemetry for {target_sat.name} over the lattice:")
    print(f"    Elevation: {alt.degrees:.2f}°")
    print(f"    Azimuth:   {az.degrees:.2f}°")
    print(f"    Distance:  {distance.km:.2f} km")
    
    if alt.degrees > 0:
        print("\n[!] SATELLITE IS ABOVE THE HORIZON - INITIATING RF HANDOFF TO RTL-SDR")
    else:
        print("\n[-] Satellite is currently below horizon. Awaiting orbital phase alignment.")

if __name__ == '__main__':
    track_leo_pass()
