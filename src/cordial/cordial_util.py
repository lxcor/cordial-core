import math

from cordial import cordial_const as CordialConst


class CordialUtil:
    """Rules and helpers shared by the Cordial classes: how many Void Days a year has, the Gregorian leap-year rule, hours and day periods.

    The number of Void Days is dictated by the sky (n_void_days, from the equinox table); the leap-year rule is kept only as the
    forecast beyond the table and for the Gregorian calendar itself."""

    @staticmethod
    def n_void_days(cordial_year):
        """How many Void Days follow the 364th day of a Cordial year. The sky dictates it: the year closes at the March equinox, and
        whatever days remain are the Void Days, one or two (CordialJulian.n_void_days_by_equinox). Where the ephemeris table does not
        reach, the leap-year rule is only a forecast of that count (n_void_days_by_rule)."""
        from cordial.cordial_julian import CordialJulian
        if CordialJulian.covers(cordial_year):
            return CordialJulian.n_void_days_by_equinox(cordial_year)
        return CordialUtil.n_void_days_by_rule(cordial_year)

    @staticmethod
    def n_void_days_by_rule(cordial_year):
        """The Gregorian leap-year rule used as a forecast of the Void Days: two in a leap year, otherwise one."""
        return 2 if CordialUtil.is_leap_year(cordial_year, "cordial") else 1

    # Static method to determine if a given year is a leap year (the Gregorian calendar's rule)
    @staticmethod
    def is_leap_year(year, calendar="cordial"):
        if calendar == "cordial":
            year = year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return True
        return False

    # Static method to get the Julian Day number
    @staticmethod
    def cordial_to_julian_day(year, month, day):
        """The Julian Day Number of a Cordial date (the Cordial day and the Julian day both begin at noon), computed directly,
        with no other calendar in between: see CordialJulian."""
        from cordial.cordial_julian import CordialJulian
        return CordialJulian.cordial_to_jdn(year, month, day)

    @staticmethod
    def get_hours_in_day(calendar="cordial"):
        hours = CordialConst.CORDIAL_HOURS_IN_DAY
        if calendar == "gregorian":
            hours = CordialConst.GREGORIAN_HOURS_IN_DAY
        return int(hours)

    @staticmethod
    def get_seconds_in_day(calendar="cordial"):
        seconds = CordialConst.CORDIAL_SECONDS_IN_DAY
        if calendar == "gregorian":
            seconds = CordialConst.GREGORIAN_SECONDS_IN_DAY
        return int(seconds)

    @staticmethod
    def to_am_pm_hours(hours, calendar="cordial"):
        hours_in_period = CordialUtil.get_hours_in_day(calendar) / 2
        if calendar == "cordial":
            if hours >= hours_in_period:
                hours -= hours_in_period
        if calendar == "gregorian":
            if hours > hours_in_period:
                hours -= hours_in_period
            elif hours == 0:
                hours = hours_in_period
            pass
        return math.floor(hours)

    @staticmethod
    def get_hours_in_half_period(calendar="cordial"):
        hours = CordialConst.CORDIAL_HOURS_IN_DAY / 2
        if calendar == "gregorian":
            hours = CordialConst.GREGORIAN_HOURS_IN_DAY / 2
        return int(hours)

    @staticmethod
    def get_am_or_pm(hours, calendar="cordial"):
        period = "PM"
        if hours >= CordialUtil.get_hours_in_day(calendar) / 2:
            period = "AM"
        if calendar == "gregorian":
            period = "AM"
            if hours >= CordialUtil.get_hours_in_day(calendar) / 2:
                period = "PM"
        return period

    @staticmethod
    def get_day_divider(second_of_day, calendar="cordial"):
        divider = ""
        seconds_in_day = CordialUtil.get_seconds_in_day(calendar)
        if second_of_day == 0:
            divider = "noon"
            if calendar == "gregorian":
                return "midnight"
        elif second_of_day == seconds_in_day * 1 / 4:
            divider = "dusk"
            if calendar == "gregorian":
                return "dawn"
        elif second_of_day == seconds_in_day * 1 / 2:
            divider = "midnight"
            if calendar == "gregorian":
                return "noon"
        elif second_of_day == seconds_in_day * 3 / 4:
            divider = "dawn"
            if calendar == "gregorian":
                return "dusk"
        return divider

    @staticmethod
    def get_day_period(second_of_day, calendar="cordial"):
        period = ""
        seconds_in_day = CordialUtil.get_seconds_in_day(calendar)
        if 0 <= second_of_day < seconds_in_day * 1 / 4:
            period = "afternoon"
            if calendar == "gregorian":
                period = "night"
        elif seconds_in_day * 1 / 4 <= second_of_day < seconds_in_day * 1 / 2:
            period = "evening"
            if calendar == "gregorian":
                period = "morning"
        elif seconds_in_day * 1 / 2 <= second_of_day < seconds_in_day * 3 / 4:
            period = "night"
            if calendar == "gregorian":
                period = "afternoon"
        elif seconds_in_day * 3 / 4 <= second_of_day < seconds_in_day:
            period = "morning"
            if calendar == "gregorian":
                period = "evening"
        return period

    @staticmethod
    def get_gregorian_days_in_year(year):
        days_in_year = 365
        if CordialUtil.is_leap_year(year, "gregorian"):
            days_in_year = 366
        return days_in_year

    @staticmethod
    def get_gregorian_days_in_month(month_of_year, year):
        days_in_month = None
        if month_of_year == 2:
            days_in_month = 28
            if CordialUtil.is_leap_year(year, "gregorian"):
                days_in_month = 29
        elif month_of_year in [1, 3, 5, 7, 8, 10, 12]:
            days_in_month = 31
        elif month_of_year in [4, 6, 9, 11]:
            days_in_month = 30
        return days_in_month

    @staticmethod
    def rgb_to_hex(red, green, blue):
        """
        Converts an RGB color to an HTML hex color code.

        Args:
            red (int): The red component of the color (0-255).
            green (int): The green component of the color (0-255).
            blue (int): The blue component of the color (0-255).

        Returns:
            str: The HTML hex color code in the format '#RRGGBB'.
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Each color component must be an integer between 0 and 255.")

        return f'#{red:02x}{green:02x}{blue:02x}'.upper()
