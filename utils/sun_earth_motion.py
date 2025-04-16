
from skyfield.api import load

def get_solar_info(utc_datetime):
    ts = load.timescale()
    t = ts.utc(utc_datetime.year, utc_datetime.month, utc_datetime.day,
               utc_datetime.hour, utc_datetime.minute, utc_datetime.second)

    planets = load('de421.bsp')
    earth, sun = planets['earth'], planets['sun']
    astrometric = earth.at(t).observe(sun)

    return {
        "distance_au": astrometric.distance().au,
        "velocity_km_s": tuple(astrometric.velocity.km_per_s)
    }
