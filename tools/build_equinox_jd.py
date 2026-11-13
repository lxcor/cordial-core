"""Rebuild src/cordial/data/equinox_jd.json: the Julian Date (UT) of every March equinox, straight from the JPL ephemeris.

These are instants on the continuous Julian count, not calendar dates, so the Cordial <-> Julian Day conversion never has to pass
through another calendar. Not part of the installed package: it needs skyfield and the ephemeris file.

    pip install skyfield
    python tools/build_equinox_jd.py [first_year] [last_year] [ephemeris]      # defaults: 2019 2052 de421.bsp

DE421 stops in 2053; DE440 covers 1550-2650 (pass de440.bsp to extend the table; the package then covers more Cordial years).
"""
import json
import os
import sys

from skyfield import almanac
from skyfield.api import load


def main():
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 2019
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 2052
    ephemeris = load(sys.argv[3] if len(sys.argv) > 3 else "de421.bsp")
    timescale = load.timescale()
    result = {}
    for year in range(first, last + 1):
        times, events = almanac.find_discrete(timescale.utc(year, 2, 1), timescale.utc(year, 4, 1), almanac.seasons(ephemeris))
        instant = [t for t, event in zip(times, events) if int(event) == 0][0]
        result[str(year)] = round(float(instant.ut1), 6)
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "cordial", "data", "equinox_jd.json")
    with open(target, "w") as out:
        json.dump(result, out, indent=1)
    print("%d equinoxes written to %s" % (len(result), os.path.normpath(target)))


if __name__ == "__main__":
    main()
