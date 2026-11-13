import datetime

from cordial.cordial_datetime import CordialDatetime
from cordial.cordial_time import CordialTime
from cordial.gregorian_date import GregorianDate
from cordial.gregorian_time import GregorianTime


class GregorianDatetime:
    """A Gregorian date and time of day, convertible to the Cordial date and time at that instant.

    A Cordial day begins at noon, so the Cordial date of an instant is the day that began at the last noon: 09:00 on 13 November
    is still in the Cordial day that began on 12 November, 15:00 on 13 November is in the one that began on 13 November.
    The Cordial time is the time since that noon.
    """

    def __init__(self, date, time):
        self.date = date  # GregorianDate
        self.time = time  # GregorianTime

    def __str__(self):
        return "%s %s" % (self.date, self.time)

    def to_datetime(self):
        return datetime.datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute, self.time.second)

    def to_cordial_datetime(self):
        """A CordialDatetime, or None when the Cordial day that contains this instant is outside the cached years."""
        begin = GregorianDate.from_date((self.to_datetime() - datetime.timedelta(hours=12)).date())
        cordial_date = begin.to_cordial_day_from_noon()
        if cordial_date is None:
            return None
        cordial_time = CordialTime(self.time.to_cordial_hours(), self.time.to_cordial_minutes(), self.time.to_cordial_seconds())
        return CordialDatetime(cordial_date, cordial_time)
