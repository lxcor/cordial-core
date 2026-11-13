import datetime

from cordial.gregorian_date import GregorianDate
from cordial.gregorian_time import GregorianTime


class CordialDatetime:
    """A Cordial date (or void day) and time of day, convertible to the Gregorian date and time at that instant.

    The Cordial day begins at Gregorian noon on the date the table of dates lists for it; the Cordial time counts from that noon.
    """

    def __init__(self, date, time):
        self.date = date  # CordialDate or CordialVoidDay
        self.time = time  # CordialTime

    def __str__(self):
        return "%s %s" % (self.date, self.time)

    def to_string(self):
        return "%s %s" % (self.date, self.time)

    def to_datetime(self):
        """The Gregorian datetime: noon on the date the Cordial day begins, plus the Cordial time (cut to whole seconds)."""
        begin = self.date.to_gregorian_date()
        noon = datetime.datetime(begin.year, begin.month, begin.day, 12, 0, 0)
        return noon + datetime.timedelta(seconds=int(self.time.to_seconds()))

    def to_gregorian_datetime(self):
        """A GregorianDatetime."""
        from cordial.gregorian_datetime import GregorianDatetime  # imported here: GregorianDatetime imports this module
        moment = self.to_datetime()
        return GregorianDatetime(GregorianDate(moment.year, moment.month, moment.day), GregorianTime(moment.hour, moment.minute, moment.second))
