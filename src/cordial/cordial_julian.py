import math

from cordial import cordial_const as CordialConst
from cordial.cordial_equinox import CordialEquinox


class CordialJulian:
    """Cordial dates and the Julian Day Number, directly: no other calendar is a step in either direction.

    Two facts make it plain addition.
      - A Julian day begins at noon, and so does a Cordial day. A Cordial day IS a Julian day.
      - The Cordial year begins at noon on the equinox date, which is the Julian day number nearest the equinox instant:
        start(Y) = floor(JD of the March equinox of Gregorian year Y-1, + 0.5), the year number being only a label.
    After that: day D of month M of year Y is  start(Y) + 28 (M - 1) + (D - 1),  and the Void Days follow the 364th day, as many as the next equinox leaves.

    The equinox instants come from the ephemeris as Julian Dates (``data/equinox_jd.json``, built by ``tools/build_equinox_jd.py``),
    so the result can be checked against any external Julian Day source: that is what makes it an independent verification
    of the tables. Cordial years 2020 to 2052 are available.
    """

    @staticmethod
    def _equinoxes():
        return CordialEquinox.table()

    @staticmethod
    def first_year():
        return min(CordialJulian._equinoxes()) + 1

    @staticmethod
    def last_year():
        return max(CordialJulian._equinoxes())  # the year after it needs the next equinox to know where it ends

    @staticmethod
    def year_start(cordial_year):
        """The Julian Day Number of the first day of a Cordial year: the Julian day nearest the March equinox that begins it."""
        equinoxes = CordialJulian._equinoxes()
        if (cordial_year - 1) not in equinoxes:
            raise ValueError("Cordial year %s is outside %s-%s" % (cordial_year, CordialJulian.first_year(), CordialJulian.last_year() + 1))
        return math.floor(equinoxes[cordial_year - 1] + 0.5)

    @staticmethod
    def covers(cordial_year):
        """True when the equinox table holds both equinoxes that bound this Cordial year."""
        equinoxes = CordialJulian._equinoxes()
        return (cordial_year - 1) in equinoxes and cordial_year in equinoxes

    @staticmethod
    def n_void_days(cordial_year):
        """The Void Days of a Cordial year: dictated by the equinox where the table reaches, the leap-year rule beyond it."""
        from cordial.cordial_util import CordialUtil
        return CordialUtil.n_void_days(cordial_year)

    @staticmethod
    def n_void_days_by_rule(cordial_year):
        """The Gregorian leap-year rule as a forecast, for comparison with the sky."""
        from cordial.cordial_util import CordialUtil
        return CordialUtil.n_void_days_by_rule(cordial_year)

    @staticmethod
    def n_void_days_by_equinox(cordial_year):
        """What the sky says: the days between this year's start and the next, less the 364. Used to check the rule."""
        return CordialJulian.year_start(cordial_year + 1) - CordialJulian.year_start(cordial_year) - CordialConst.CORDIAL_DAYS_IN_YEAR

    @staticmethod
    def cordial_to_jdn(year, month, day):
        if not (1 <= month <= CordialConst.CORDIAL_MONTHS_IN_YEAR and 1 <= day <= CordialConst.CORDIAL_DAYS_IN_MONTH):
            raise ValueError("month 1-13 and day 1-28 expected")
        return CordialJulian.year_start(year) + (month - 1) * CordialConst.CORDIAL_DAYS_IN_MONTH + (day - 1)

    @staticmethod
    def void_to_jdn(year, void_day=1):
        if not 1 <= void_day <= CordialJulian.n_void_days(year):
            raise ValueError("Cordial year %s has %d Void Day(s)" % (year, CordialJulian.n_void_days(year)))
        return CordialJulian.year_start(year) + CordialConst.CORDIAL_DAYS_IN_YEAR - 1 + void_day

    @staticmethod
    def jdn_to_cordial(jdn):
        """('date', year, month, day) or ('void', year, void_day) for a Julian Day Number."""
        for year in range(CordialJulian.first_year(), CordialJulian.last_year() + 1):
            start = CordialJulian.year_start(year)
            if start <= jdn < CordialJulian.year_start(year + 1):
                offset = jdn - start
                if offset < CordialConst.CORDIAL_DAYS_IN_YEAR:
                    return ("date", year, offset // CordialConst.CORDIAL_DAYS_IN_MONTH + 1, offset % CordialConst.CORDIAL_DAYS_IN_MONTH + 1)
                return ("void", year, offset - CordialConst.CORDIAL_DAYS_IN_YEAR + 1)
        raise ValueError("Julian Day Number %s is outside the years %s-%s" % (jdn, CordialJulian.first_year(), CordialJulian.last_year()))
