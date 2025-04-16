
from skyfield.api import load, wgs84
import numpy as np

def get_velocity_vectors(utc_datetime, lat, lon, elevation_m=0):
    ts = load.timescale()
    t = ts.utc(utc_datetime.year, utc_datetime.month, utc_datetime.day,
               utc_datetime.hour, utc_datetime.minute, utc_datetime.second)

    planets = load('de421.bsp')
    earth = planets['earth']
    observer = earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon, elevation_m=elevation_m)

    vel_bary = observer.at(t).velocity.km_per_s

    ra_cmb, dec_cmb = np.deg2rad(168), np.deg2rad(-7)
    cmb_vector = 370 * np.array([
        np.cos(dec_cmb) * np.cos(ra_cmb),
        np.cos(dec_cmb) * np.sin(ra_cmb),
        np.sin(dec_cmb)
    ])

    ra_gc, dec_gc = np.deg2rad(266.4), np.deg2rad(-29.0)
    galactic_vector = 220 * np.array([
        np.cos(dec_gc) * np.cos(ra_gc),
        np.cos(dec_gc) * np.sin(ra_gc),
        np.sin(dec_gc)
    ])

    return {
        "CMB": tuple(vel_bary + cmb_vector),
        "Galactic": tuple(vel_bary + galactic_vector)
    }
