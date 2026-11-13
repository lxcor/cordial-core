import datetime
from math import ceil

from cordial import cordial_const as CordialConst
from cordial.cordial_date import CordialDate
from cordial.cordial_julian import CordialJulian
from cordial.cordial_void_day import CordialVoidDay


class GregorianDate:
    """
        A class to represent and convert Gregorian dates and times to the cordial calendar system.

    """

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def from_date(date):
        return GregorianDate(date.year, date.month, date.day)

    def to_date(self):
        return datetime.date(self.year, self.month, self.day)

    def to_datetime(self):
        return datetime.datetime(self.year, self.month, self.day)

    def get_day_of_week(self):
        return self.to_date().weekday() + 1

    def get_day_of_year(self):
        return self.to_date().timetuple().tm_yday

    def get_week_of_month(self):
        first_day = self.to_date().replace(day=1)
        dom = self.to_date().day
        adjusted_dom = dom + first_day.weekday()
        return int(ceil(adjusted_dom / 7.0))

    def get_week_of_year(self):
        return self.to_date().isocalendar()[1]

    def get_name_of_month(self):
        return self.to_date().strftime("%B")

    def get_name_of_week(self):
        return self.to_date().strftime("%A")

    def to_cordial_day_of_year(self):
        """Day of the Cordial year (1-364, then 365 and 366 for the Void Days) of the Cordial day that begins at noon on this date."""
        return self.to_cordial_date().get_day_of_year()

    def to_cordial_year(self):
        """The (internal) Cordial year of the Cordial day that begins at noon on this date."""
        cordial_day = self.to_cordial_date()
        return cordial_day.cordial_year if isinstance(cordial_day, CordialVoidDay) else cordial_day.year

    def to_cordial_month(self):
        """Month 1-13 of the Cordial day that begins at noon on this date; 0 for a Void Day."""
        cordial_day = self.to_cordial_date()
        return 0 if isinstance(cordial_day, CordialVoidDay) else cordial_day.month

    def to_cordial_day(self):
        """Day of the month (1-28) of the Cordial day that begins at noon on this date; for a Void Day, its number (1 or 2)."""
        cordial_day = self.to_cordial_date()
        return cordial_day.void_day if isinstance(cordial_day, CordialVoidDay) else cordial_day.day

    def to_date_string(self):
        return self.to_date().strftime("%B %d, %Y")

    def to_julian_day_number(self):
        """The Julian Day Number of the day that begins at noon on this Gregorian date (Julian days and Cordial days both begin at noon)."""
        return self.to_date().toordinal() + CordialConst.JULIAN_DAY_NUMBER_OF_ORDINAL_ZERO

    def to_cordial_day_from_noon(self):
        """The Cordial day (a CordialDate or a CordialVoidDay) that BEGINS at noon on this Gregorian date, or None outside the equinox table.

        A Cordial day runs from Gregorian noon to the next noon, and the table of dates lists each Cordial day under the Gregorian
        date on which it begins. A Cordial day is a Julian day, so this is a lookup of the Julian Day Number of the date
        (CordialJulian), the exact inverse of CordialDate.to_gregorian_date and CordialVoidDay.to_gregorian_date.
        """
        try:
            kind = CordialJulian.jdn_to_cordial(self.to_julian_day_number())
        except ValueError:
            return None
        if kind[0] == "date":
            return CordialDate(*kind[1:])
        return CordialVoidDay(*kind[1:])

    def to_cordial_date(self):
        """The Cordial day (a CordialDate or a CordialVoidDay) that begins at noon on this Gregorian date, as the table of dates lists it.

        A Cordial day begins at Gregorian noon, so the Gregorian date a Cordial day is listed under is the date it begins on.
        Raises ValueError for a date outside the years the astronomy covers.
        """
        cordial_day = self.to_cordial_day_from_noon()
        if cordial_day is None:
            raise ValueError("%s is outside the years the Cordial calendar covers" % self.to_date_string())
        return cordial_day

    def __str__(self):
        return self.to_date_string()
