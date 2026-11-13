import datetime
import json
from importlib import resources


class CordialEquinox:
    """The March equinoxes that open and close every Cordial year.

    The Cordial year begins at noon on the date of the March equinox and closes at the next one; whatever days remain after the
    364th are the Void Days. The sky therefore dictates both where a Cordial year starts and how many Void Days it has.

    The equinox instants ship with the package as Julian Dates (UT), in ``data/equinox_jd.json``: one entry per Gregorian year,
    computed from the JPL DE421 ephemeris (see ``tools/build_equinox_jd.py``). They are plain numbers on the continuous Julian
    count, so no calendar is a step between them and the Cordial dates built on them. The table runs from 2019 to 2052, which
    makes the Cordial years 2020 to 2052 complete; ``CordialUtil.n_void_days`` forecasts beyond it.

    Years here are Gregorian years of the equinox, the internal label of a Cordial year (it closes at the equinox of the Gregorian year
    of that number); ``CordialConst.to_aa`` turns it into the Anno Adami year shown to people.
    """

    JULIAN_DATE_OF_UNIX_EPOCH = 2440587.5  # JD of 1970-01-01 00:00 UT
    _table = None

    @staticmethod
    def table():
        """{Gregorian year: Julian Date (UT) of its March equinox}."""
        if CordialEquinox._table is None:
            with resources.files("cordial").joinpath("data", "equinox_jd.json").open("r", encoding="utf-8") as source:
                CordialEquinox._table = {int(year): jd for year, jd in json.load(source).items()}
        return CordialEquinox._table

    @staticmethod
    def first_year():
        return min(CordialEquinox.table())

    @staticmethod
    def last_year():
        return max(CordialEquinox.table())

    @staticmethod
    def covers(year):
        return year in CordialEquinox.table()

    @staticmethod
    def julian_date(year):
        """The Julian Date (UT) of the March equinox of a Gregorian year."""
        try:
            return CordialEquinox.table()[year]
        except KeyError:
            raise ValueError("The equinox table covers %d to %d, not %s." % (CordialEquinox.first_year(), CordialEquinox.last_year(), year))

    @staticmethod
    def to_datetime(year):
        """The instant of the March equinox as a naive UTC datetime."""
        days = CordialEquinox.julian_date(year) - CordialEquinox.JULIAN_DATE_OF_UNIX_EPOCH
        return datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days)

    @staticmethod
    def to_date(year):
        """The Gregorian date (UTC) of the March equinox: the date a Cordial year begins on, at noon."""
        instant = CordialEquinox.to_datetime(year)
        return datetime.date(instant.year, instant.month, instant.day)
