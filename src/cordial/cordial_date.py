import datetime
import math

from cordial import cordial_const as CordialConst
from cordial.cordial_equinox import CordialEquinox
from cordial.cordial_util import CordialUtil


class CordialDate:
    """
    A class to represent and manipulate dates and times in the cordial calendar system.

      Attributes:
      -----------
      year : int
          The year in the cordial calendar.
      month : int
          The month in the cordial calendar, ranging from 1 to 13.
      day : int
          The day of the month in the cordial calendar, ranging from 1 to 28.
    """

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __eq__(self, other):
        if not isinstance(other, CordialDate):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.year == other.year and self.month == other.month and self.day == other.day

    def get_day_of_year(self):
        """ returns an integer from 1 to 364 representing the cordial Day of Year """
        return int((self.month - 1) * 28 + self.day)

    def get_day_of_month(self):
        """ returns an integer from 1 to 13 representing the month of the year """
        return (self.get_day_of_year() - 1) % 28 + 1

    def get_day_of_week(self):
        """ returns an integer from 1 to 7 representing the day of the week """
        return (self.get_day_of_year() - 1) % 7 + 1

    def get_week_of_year(self):
        """ returns an integer from 1 to 52 representing the week of the year """
        return (self.get_day_of_year() - 1) // 7 + 1

    def get_week_of_month(self):
        """ returns an integer from 1 to 4 representing the week of the month """
        return (self.get_day_of_month() - 1) // 7 + 1

    def get_week_of_season(self):
        """ returns an integer from 1 to 13 representing the week of the season """
        return ((self.get_week_of_year() - 1) % 13) + 1

    def get_name_of_month(self):
        """ returns a string representing the cordial Month Name """
        return CordialConst.MONTHS[self.month - 1]

    def get_day_of_week_name(self):
        """ returns a string representing the cordial Weekday Name """
        # return CordialConst.WEEKDAYS[self.get_day_of_week() - 1]
        return CordialConst.COLORS[self.get_day_of_week() - 1]['latin']

    def get_day_of_week_color_name(self):
        """ returns a string representing the cordial Weekday Name """
        # return CordialConst.WEEKDAYS[self.get_day_of_week() - 1]
        return CordialConst.COLORS[self.get_day_of_week() - 1]['name']

    def get_day_of_week_color_code(self):
        """ returns a string representing the cordial Weekday Name """
        # return CordialConst.WEEKDAYS[self.get_day_of_week() - 1]
        return CordialConst.COLORS[self.get_day_of_week() - 1]['html']

    def get_day_of_week_abbrev(self):
        """ returns a string representing the cordial Weekday Name """
        # return CordialConst.WEEKDAYS[self.get_day_of_week() - 1]
        return CordialConst.COLORS[self.get_day_of_week() - 1]['code']

    def get_season_of_year(self):
        """ returns an integer from 1 to 4 representing the season of the year 1-Winter, 2-Spring, 3-Summer, 4-Autumn"""
        return int((self.get_day_of_year() - 1) // (CordialConst.CORDIAL_DAYS_IN_YEAR / 4)) + 1

    def get_season_of_year_name(self):
        """ returns an string representing the season of the year 1-Winter, 2-Spring, 3-Summer, 4-Autumn"""
        return CordialConst.SEASONS[self.get_season_of_year() - 1]["name"]

    def to_gregorian_datetime(self):
        """ the Gregorian datetime at which this Cordial day begins: noon on the date it is listed under """
        return datetime.datetime.combine(self.to_gregorian_date(), datetime.time(12))

    def to_gregorian_date(self):
        """ the Gregorian date on which this Cordial day begins (at noon): the date of the March equinox that opens the year, plus the days elapsed """
        return CordialEquinox.to_date(self.year - 1) + datetime.timedelta(days=self.get_day_of_year() - 1)

    def to_gregorian_date_string(self):
        return self.to_gregorian_date().strftime("%B %d, %Y")

    def to_gregorian_day_of_week_name(self):
        return self.to_gregorian_date().strftime("%A")

    def to_gregorian_day_of_year(self):
        return self.to_gregorian_date().timetuple().tm_yday

    def get_day_polarity(self):
        if self.get_day_of_year() % 2 == 0:  # even -> negative
            return CordialConst.CORDIAL_DAY_POLARITY_NEGATIVE
        return CordialConst.CORDIAL_DAY_POLARITY_POSITIVE  # odd -> positive

    def get_day_polarity_color(self):
        if self.get_day_polarity() == CordialConst.CORDIAL_DAY_POLARITY_NEGATIVE:
            return "Green"
        return "Red"

    def get_color_of_day(self):

        season = self.get_season_of_year() - 1
        week = self.get_week_of_season() - 1
        day_of_week = self.get_day_of_week() - 1

        normalized_season = season / 4.0
        normalized_week = week / 13.0
        normalized_day = day_of_week / 7.0

        total_normalized = normalized_season + (normalized_week / 4.0) + (normalized_day / 52.0)

        red = round(math.sin(2 * math.pi * total_normalized) * 127 + 128)
        green = round(math.sin(2 * math.pi * total_normalized + (2 * math.pi / 3)) * 127 + 128)
        blue = round(math.sin(2 * math.pi * total_normalized + (4 * math.pi / 3)) * 127 + 128)

        hex_color = CordialUtil.rgb_to_hex(red, green, blue)

        return hex_color

    def to_string(self, value):
        """ it takes a parameter string and returns a string representing the CodialDatetime instance"""
        r = value
        r = r.replace('%Y', str(CordialConst.to_aa(self.year)))
        r = r.replace('%y', str(CordialConst.to_aa(self.year))[2:])
        r = r.replace('%m', str(self.month).zfill(2))
        r = r.replace('%d', str(self.day).zfill(2))
        r = r.replace('%B', CordialConst.MONTHS[self.month - 1]["name"])
        r = r.replace('%b', CordialConst.MONTHS[self.month - 1]['abbrev'])
        r = r.replace('%A', CordialConst.COLORS[self.get_day_of_week() - 1]["latin"])
        r = r.replace('%a', CordialConst.COLORS[self.get_day_of_week() - 1]["code"])
        r = r.replace('%WoMo', CordialConst.WEEKS[self.get_week_of_month() - 1]["name"])
        r = r.replace('%WoMc', CordialConst.WEEKS[self.get_week_of_month() - 1]["code"])
        r = r.replace('%DoWc', CordialConst.COLORS[self.get_day_of_week() - 1]["name"])
        return r

    def to_date_string(self):
        return self.to_string("%B %d, %Y")

    def to_full_date(self):
        return self.to_string("%A, %B %d, %Y")

    def to_abbrev_date(self):
        return self.to_string("%a, %b %d")

    def to_custom_date(self):
        return self.to_string("%WoMc-%DoWc day of %B , %Y")

    def to_mm_dd_yyyy(self):
        return self.to_string("%m/%d/%Y")

    def to_dd_mm_yyyy(self):
        return self.to_string("%d/%m/%Y")

    def to_dd_mon_yy(self):
        return self.to_string("%d-%b-%y")

    def __str__(self):
        return self.to_date_string()
