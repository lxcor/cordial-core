import datetime

from cordial.cordial_date import CordialDate
from cordial.cordial_equinox import CordialEquinox
from cordial.cordial_util import CordialUtil


class CordialVoidDay:
    """The Void Day (or the two of them) that closes a Cordial year: days outside the 13 months of 28 days, outside the week and with no month.

    The year closes at the March equinox and the days left after the 364th are the Void Days, one or two as the sky dictates. A
    Void Day is listed under the Gregorian date it begins on (at noon), just before the equinox date. Gregorian counterpart: the
    leap day, which the Cordial system does not need because these days absorb it."""

    def __init__(self, cordial_year, void_day=1):
        self.cordial_year = cordial_year
        self.void_day = void_day

    @property
    def year(self):
        """The Cordial year, under the same name CordialDate uses."""
        return self.cordial_year

    def n_void_days(self):
        """One or two, as the equinox dictates (CordialUtil.n_void_days)."""
        return CordialUtil.n_void_days(self.cordial_year)

    def get_day_of_year(self):
        day_of_year = 365
        if self.void_day == 2:
            day_of_year = 366
        return day_of_year

    def get_color_of_day(self):

        void_day_color = "Black"

        if self.n_void_days() == 2:

            if self.void_day == 2:
                void_day_color = "White"
            elif self.void_day == 1:
                void_day_color = "Black"

        return void_day_color

    def to_gregorian_datetime(self):
        """ the Gregorian datetime at which this Void Day begins: noon on the date it is listed under """
        return datetime.datetime.combine(self.to_gregorian_date(), datetime.time(12))

    def to_gregorian_date(self):
        """ the Void Days sit just before the equinox that closes the year: the last one on the day before it, the first one a day earlier when there are two """
        days_before_equinox = self.n_void_days() - self.void_day + 1
        return CordialEquinox.to_date(self.cordial_year) - datetime.timedelta(days=days_before_equinox)

    def to_gregorian_date_string(self):
        return self.to_gregorian_datetime().strftime("%B %d, %Y")

    def to_date_string(self):

        if self.n_void_days() == 1:
            return "Void Day (non leap)"
        else:  # leap year
            if self.void_day == 1:
                return "Void Day (leap) - VD"
            elif self.void_day == 2:
                return "Other Void (leap) - V2"

    def get_day_of_week(self):
        return 0

    def get_day_of_week_name(self):
        return "-"

    def get_day_polarity(self):
        return "-"

    def get_day_polarity_color(self):
        return "-"
