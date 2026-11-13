# Cordial (`lxcor-cordial`)

Cordial is a calendar and clock built on two numbers, **364** and **52**: a year of 364 days (13 months of 28 days, 52 weeks of 7),
a day of 26 hours of 52 minutes of 52 seconds, and a circle of 364 grau (a quarter circle is 91). A Cordial day **begins at noon**; the
year begins at noon on the date of the **March equinox**, and the days left after the 364th (one or two, as the sky dictates) are the
**Void Days**. Years are counted from Adam's birth (Anno Adami, AA): the year that began in March 2026 is **6030 AA**.

This package is the pure core: the date, time, angle, place and sky classes, the Julian Day link and the converters to the Gregorian
system. It needs **only the Python standard library** (3.9+) and ships its one data file, the table of March equinoxes.

```
pip install lxcor-cordial
```

```python
from cordial import GregorianDate, CordialDate, CordialJulian

GregorianDate(2026, 11, 13).to_cordial_date().to_date_string()   # 'Sagittarius 15, 6030'  (the day that begins at noon on that date)
CordialDate(2027, 9, 15).to_gregorian_date()                      # datetime.date(2026, 11, 13); the year argument is the internal index (AA 6030 - 4003)
CordialJulian.cordial_to_jdn(2027, 9, 15)                         # 2461358: a Cordial day is a Julian day
```

```python
from cordial import cordial_converter as converter
converter.gregorian_date_to_cordial(2026, 11, 13)                 # rows of (label, value), ready to show; raises ConverterError with a message
```

## Scope and honesty about the sky

- Dates are computed from the packaged equinox table (`src/cordial/data/equinox_jd.json`, JPL DE421): Cordial years 2020 to 2052, that is
  Gregorian March 20, 2019 to March 18, 2052. Outside it conversions raise an error (`ValueError` / `ConverterError`). The number of Void
  Days beyond the table is only a forecast by the Gregorian leap-year rule, which differs from the sky in Cordial 2044, 2045, 2048, 2049 and 2052.
- `tools/build_equinox_jd.py` regenerates the table (needs `skyfield`); extend it and release a new version to widen the range.
- Positions of the Sun, Moon and stars, maps and charts are not in this package: they need an ephemeris and plotting libraries and live in the
  Cordial web site (https://cordial.lxcor.com), which uses this core.
- Every Cordial day has a Julian Day Number, computed directly with no other calendar as a step, and the tests check each day from 2020
  to 2052 against the Julian Day Number of its Gregorian date (an external witness).

## Tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Licence

Apache License 2.0 (see `LICENSE`), with attribution: keep the `NOTICE` file with any redistribution. Commercial use is allowed.
Copyright 2015-2026 Light Cross Holdings Corporation. All Rights Reserved.
