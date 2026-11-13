from cordial import cordial_const as CordialConst
from cordial.cordial_util import CordialUtil


class GregorianTime:
    """A Gregorian time of day (hour, minute, second) with its conversion to Cordial time.

    A Cordial day begins at noon and has 26 hours of 52 minutes of 52 seconds (70,304 Cordial seconds, 492,128 crons). The
    conversion counts the time elapsed since the previous Gregorian noon, in exact integer arithmetic."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def get_seconds(self):
        seconds_in_hours = self.hour * CordialConst.GREGORIAN_MINUTES_IN_HOUR * CordialConst.GREGORIAN_SECONDS_IN_MINUTE
        seconds_in_minutes = self.minute * CordialConst.GREGORIAN_SECONDS_IN_MINUTE
        return seconds_in_hours + seconds_in_minutes + self.second

    def to_cordial_seconds_of_day(self):
        """Cordial seconds since Gregorian midnight (to a tenth)."""
        return round(self.get_seconds() * CordialConst.CORDIAL_SECONDS_IN_GREGORIAN_SECOND, 1)

    def to_crons_of_day(self):
        """Crons since Gregorian midnight (to a tenth)."""
        return round(self.get_seconds() * CordialConst.CORDIAL_CRONS_IN_DAY / CordialConst.GREGORIAN_SECONDS_IN_DAY, 1)

    def to_string(self, value):
        """ it takes a parameter string and returns a string representing the CodialDatetime instance"""
        r = value
        r = r.replace('%H', str(self.hour).zfill(2))
        r = r.replace('%M', str(self.minute).zfill(2))
        r = r.replace('%S', str(self.second).zfill(2))
        r = r.replace('%I', str(CordialUtil.to_am_pm_hours(self.hour, "gregorian")).zfill(2))
        r = r.replace('%p', str(CordialUtil.get_am_or_pm(self.hour, "gregorian")))
        return r

    def to_time_string(self):
        return self.to_string("%H:%M:%S")

    def to_am_pm_string(self):
        return self.to_string("%I:%M:%S %p")

    def to_day_period(self):
        return CordialUtil.get_day_period(self.get_seconds(), "gregorian")

    def to_day_divider(self):
        return CordialUtil.get_day_divider(self.get_seconds(), "gregorian")

    def to_cordial_hours(self):
        seconds = self.to_adjusted_cordial_seconds()
        hours = seconds // CordialConst.CORDIAL_SECONDS_IN_HOUR
        return int(hours)

    def to_cordial_minutes(self):
        seconds = self.to_adjusted_cordial_seconds()
        seconds %= CordialConst.CORDIAL_SECONDS_IN_HOUR
        minutes = seconds // CordialConst.CORDIAL_MINUTES_IN_HOUR
        return int(minutes)

    def to_cordial_seconds(self):
        seconds = self.to_adjusted_cordial_seconds()
        seconds %= CordialConst.CORDIAL_SECONDS_IN_HOUR
        seconds %= CordialConst.CORDIAL_SECONDS_IN_MINUTE
        return round(seconds)

    def to_cordial_time(self):
        # Format as HH:MM:SS
        hours = self.to_cordial_hours()
        minutes = self.to_cordial_minutes()
        seconds = self.to_cordial_seconds()
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def to_cordial_am_pm_time(self):
        # Format the hours and minutes as HH:MM AM/PM
        hours = self.to_cordial_hours()
        minutes = self.to_cordial_minutes()
        seconds = self.to_cordial_seconds()
        am_pm_hours = CordialUtil.to_am_pm_hours(hours)
        period_of_day = CordialUtil.get_am_or_pm(hours)
        return f"{am_pm_hours:02}:{minutes:02}:{seconds:02} {period_of_day}"

    def to_cordial_day_period(self):
        return CordialUtil.get_day_period(self.to_adjusted_cordial_seconds())

    def to_cordial_day_divider(self):
        return CordialUtil.get_day_divider(self.to_adjusted_cordial_seconds())

    def to_adjusted_cordial_seconds(self):
        """ offset to handle Cordial Day starting at noon: Cordial seconds since the Cordial day began (to a tenth) """
        to_seconds = self.to_cordial_seconds_of_day()
        offset = CordialConst.CORDIAL_SECONDS_IN_DAY / 2
        seconds = to_seconds
        if to_seconds < offset:
            seconds = to_seconds + offset
        elif to_seconds >= offset:
            seconds = to_seconds - offset
        return seconds

    def get_adjusted_seconds(self):
        """Whole Gregorian seconds since the Cordial day began, at noon."""
        return (self.get_seconds() + CordialConst.GREGORIAN_SECONDS_IN_DAY // 2) % CordialConst.GREGORIAN_SECONDS_IN_DAY

    def to_adjusted_crons(self):
        """Whole crons since the Cordial day began at noon: exact integer arithmetic, 492,128 to the day."""
        return (self.get_adjusted_seconds() * CordialConst.CORDIAL_CRONS_IN_DAY) // CordialConst.GREGORIAN_SECONDS_IN_DAY

    def to_cordial_cron(self):
        """The cron within the Cordial second, 0 to 6."""
        return self.to_adjusted_crons() % CordialConst.CORDIAL_CRONS_IN_SECOND

    def to_cordial_time_with_crons(self):
        """HH:MM:SS.c, truncated (not rounded) to the cron; the digit after the point counts crons, 0 to 6."""
        crons = self.to_adjusted_crons()
        hours, rest = divmod(crons, CordialConst.CORDIAL_CRONS_IN_HOUR)
        minutes, rest = divmod(rest, CordialConst.CORDIAL_CRONS_IN_MINUTE)
        seconds, cron = divmod(rest, CordialConst.CORDIAL_CRONS_IN_SECOND)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{cron}"
