from cordial import cordial_const as CordialConst
from cordial.cordial_util import CordialUtil


class CordialTime:
    """
    CordialTime class
    """

    def __init__(self, hour=0, minute=0, second=0, cron=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.cron = cron  # 0 to 6: a seventh of a Cordial second, one division of the clock's dial

    def get_cordial_seconds(self):
        """Whole Cordial seconds since the start of the Cordial day (the table of minutes calls them 'Cordial second of the day')."""
        seconds_in_hours = self.hour * CordialConst.CORDIAL_MINUTES_IN_HOUR * CordialConst.CORDIAL_SECONDS_IN_MINUTE
        seconds_in_minutes = self.minute * CordialConst.CORDIAL_SECONDS_IN_MINUTE
        return seconds_in_hours + seconds_in_minutes + self.second

    def get_crons(self):
        """Crons since the start of the Cordial day: seven to a Cordial second, 492,128 to the day."""
        return self.get_cordial_seconds() * CordialConst.CORDIAL_CRONS_IN_SECOND + self.cron

    def to_seconds(self):
        """Real (Gregorian) seconds since the start of the Cordial day, at today's calibration of the cron."""
        return round(self.get_crons() * CordialConst.GREGORIAN_SECONDS_IN_CRON, 1)

    def to_string(self, value):
        """ it takes a parameter string and returns a string representing the CodialDatetime instance"""
        r = value
        r = r.replace('%H', str(self.hour).zfill(2))
        r = r.replace('%M', str(self.minute).zfill(2))
        r = r.replace('%S', str(self.second).zfill(2))
        r = r.replace('%I', str(CordialUtil.to_am_pm_hours(self.hour)).zfill(2))
        r = r.replace('%p', str(CordialUtil.get_am_or_pm(self.hour)))
        return r

    def to_time(self):
        return self.to_string("%H:%M:%S")

    def to_time_with_crons(self):
        """HH:MM:SS.c where the digit after the point counts crons, 0 to 6."""
        return "%s.%d" % (self.to_string("%H:%M:%S"), self.cron)

    def to_am_pm_time(self):
        return self.to_string("%I:%M:%S %p")

    def to_day_period(self):
        return CordialUtil.get_day_period(self.get_cordial_seconds())

    def to_day_divider(self):
        return CordialUtil.get_day_divider(self.get_cordial_seconds())

    def to_adjusted_seconds(self):
        """ offset to handle Cordial Day starting at noon """
        to_seconds = self.to_seconds()
        offset = CordialConst.GREGORIAN_SECONDS_IN_DAY / 2
        seconds = to_seconds
        if to_seconds < offset:
            seconds = to_seconds + offset
        elif to_seconds >= offset:
            seconds = to_seconds - offset
        return seconds

    def to_gregorian_hours(self):
        seconds = self.to_adjusted_seconds()
        hours = seconds // CordialConst.GREGORIAN_SECONDS_IN_HOUR
        return int(hours)

    def to_gregorian_minutes(self):
        seconds = self.to_adjusted_seconds()
        seconds %= CordialConst.GREGORIAN_SECONDS_IN_HOUR
        minutes = seconds // CordialConst.GREGORIAN_MINUTES_IN_HOUR
        return int(minutes)

    def to_gregorian_seconds(self):
        seconds = self.to_adjusted_seconds()
        seconds %= CordialConst.GREGORIAN_SECONDS_IN_HOUR
        seconds %= CordialConst.GREGORIAN_SECONDS_IN_MINUTE
        return int(seconds)

    def to_gregorian_time(self):
        # Format as HH:MM:SS
        hours = self.to_gregorian_hours()
        minutes = self.to_gregorian_minutes()
        seconds = self.to_gregorian_seconds()
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def to_gregorian_am_pm_time(self):
        # Format the hours and minutes as HH:MM AM/PM
        hours = self.to_gregorian_hours()
        minutes = self.to_gregorian_minutes()
        seconds = self.to_gregorian_seconds()
        am_pm_hours = CordialUtil.to_am_pm_hours(hours, "gregorian")
        period_of_day = CordialUtil.get_am_or_pm(hours, "gregorian")
        return f"{am_pm_hours:02}:{minutes:02}:{seconds:02} {period_of_day}"

    def to_gregorian_day_period(self):
        return CordialUtil.get_day_period(self.to_adjusted_seconds(), "gregorian")

    def to_gregorian_day_divider(self):
        return CordialUtil.get_day_divider(self.to_adjusted_seconds(), "gregorian")

    def __str__(self):
        return self.to_time()
