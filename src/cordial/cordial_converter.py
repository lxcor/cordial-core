import datetime

from cordial import cordial_const as CordialConst
from cordial.cordial_angle import CordialAngle
from cordial.cordial_date import CordialDate
from cordial.cordial_datetime import CordialDatetime
from cordial.cordial_equinox import CordialEquinox
from cordial.cordial_julian import CordialJulian
from cordial.cordial_place import CordialPlace
from cordial.cordial_sky import CordialSky
from cordial.cordial_time import CordialTime
from cordial.cordial_util import CordialUtil
from cordial.cordial_void_day import CordialVoidDay
from cordial.cordial_angle_adapter import CordialAngleAdapter
from cordial.gregorian_date import GregorianDate
from cordial.gregorian_datetime import GregorianDatetime
from cordial.gregorian_time import GregorianTime


class ConverterError(ValueError):
    """The input cannot be converted; the message is meant for the person using the form."""


def _month_name(month):
    """CordialConst.MONTHS holds dicts with a name and an abbreviation."""
    return month["name"] if isinstance(month, dict) else month


def _aa_year(value, low, high):
    """A Cordial year typed as an AA number; returns the internal year. low and high are internal."""
    return CordialConst.from_aa(_integer(value, "Year", CordialConst.to_aa(low), CordialConst.to_aa(high)))


def _integer(value, name, low, high):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ConverterError("%s must be a whole number." % name)
    if not low <= number <= high:
        raise ConverterError("%s must be between %d and %d." % (name, low, high))
    return number


def _decimal(value, name, low, high):
    try:
        number = float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        raise ConverterError("%s must be a number." % name)
    if not low <= number <= high:
        raise ConverterError("%s must be between %g and %g." % (name, low, high))
    return number


# Dates are computed from the equinox table: the Cordial years it completes (internal years, see CordialEquinox) can be converted.
CORDIAL_YEARS = (CordialJulian.first_year(), CordialJulian.last_year())


def gregorian_date_range():
    """First and last Gregorian date the converter can answer: from the start of the first Cordial year to the day before the equinox that closes the last."""
    first = CordialDate(CORDIAL_YEARS[0], 1, 1).to_gregorian_date()
    last = CordialEquinox.to_date(CORDIAL_YEARS[1]) - datetime.timedelta(days=1)
    return first, last


def _time_given(*parts):
    return any(str(part).strip() != "" for part in parts)


def _cordial_day_rows(cordial):
    if isinstance(cordial, CordialVoidDay):
        return [("Cordial year", "%d %s" % (CordialConst.to_aa(cordial.cordial_year), CordialConst.ERA_NAME)), ("Day of year", cordial.get_day_of_year()), ("Colour", cordial.get_color_of_day())]
    return [
        ("Year, month, day", "%d %s, %d (%s), %d" % (CordialConst.to_aa(cordial.year), CordialConst.ERA_NAME, cordial.month, _month_name(cordial.get_name_of_month()), cordial.day)),
        ("Weekday", cordial.get_day_of_week_name()),
        ("Day of year", cordial.get_day_of_year()),
        ("Week of year", cordial.get_week_of_year()),
        ("Season", cordial.get_season_of_year_name()),
    ]


def gregorian_date_to_cordial(year, month, day, hour="", minute="", second=""):
    """Without a time: the Cordial day that begins at noon on that Gregorian date (the date the table of dates lists).
    With a time: the Cordial date and time at that instant (before noon it is still the day that began the previous noon)."""
    year = _integer(year, "Year", 1, 9999)
    month = _integer(month, "Month", 1, 12)
    day = _integer(day, "Day", 1, 31)
    try:
        date = datetime.date(year, month, day)
    except ValueError:
        raise ConverterError("That is not a valid Gregorian date.")

    first, last = gregorian_date_range()
    out_of_range = ConverterError("Dates from %s to %s can be converted." % (first.strftime("%B %d, %Y"), last.strftime("%B %d, %Y")))

    if not _time_given(hour, minute, second):
        cordial = GregorianDate.from_date(date).to_cordial_day_from_noon() if first <= date <= last else None
        if cordial is None:
            raise out_of_range
        return [("Cordial date", cordial.to_date_string()), ("The Cordial day begins", "%s 12:00 (noon)" % date.strftime("%B %d, %Y"))] + _cordial_day_rows(cordial)

    hour = _integer(hour or 0, "Hour", 0, 23)
    minute = _integer(minute or 0, "Minute", 0, 59)
    second = _integer(second or 0, "Second", 0, 59)
    moment = GregorianDatetime(GregorianDate.from_date(date), GregorianTime(hour, minute, second))
    cordial = moment.to_cordial_datetime() if first <= (moment.to_datetime() - datetime.timedelta(hours=12)).date() <= last else None
    if cordial is None:
        raise out_of_range
    began = (moment.to_datetime() - datetime.timedelta(hours=12)).date()
    return [
        ("Cordial date", cordial.date.to_date_string()),
        ("Cordial time", cordial.time.to_time()),
        ("Cordial 12-hour", cordial.time.to_am_pm_time()),
        ("Cordial time, truncated to the cron", GregorianTime(hour, minute, second).to_cordial_time_with_crons()),
        ("That Cordial day began", "%s 12:00 (noon)" % began.strftime("%B %d, %Y")),
    ] + _cordial_day_rows(cordial.date)


def cordial_date_to_gregorian(year, month, day, void_day=1, hour="", minute="", second="", cron=""):
    """month 1..13 with day 1..28, or month 0 for a void day (``void_day`` 1, or 2 in a leap year).
    Without a time: the Gregorian date on which that Cordial day begins (at noon). With a time: the Gregorian date and time at that instant."""
    year = _aa_year(year, *CORDIAL_YEARS)
    month = _integer(month, "Month", 0, CordialConst.CORDIAL_MONTHS_IN_YEAR)

    if month == 0:
        void_day = _integer(void_day or 1, "Void day", 1, 2)
        cordial = CordialVoidDay(year, void_day)
        if void_day > cordial.n_void_days():
            raise ConverterError("Cordial year %d has only one Void Day." % CordialConst.to_aa(year))
    else:
        day = _integer(day, "Day", 1, CordialConst.CORDIAL_DAYS_IN_MONTH)
        cordial = CordialDate(year, month, day)

    begins = cordial.to_gregorian_date()

    if not _time_given(hour, minute, second, cron):
        return [
            ("Gregorian date", begins.strftime("%B %d, %Y")),
            ("The Cordial day begins", "%s 12:00 (noon)" % begins.strftime("%B %d, %Y")),
            ("Weekday", begins.strftime("%A")),
            ("Cordial date", cordial.to_date_string()),
        ]

    hour = _integer(hour or 0, "Hour", 0, CordialConst.CORDIAL_HOURS_IN_DAY - 1)
    minute = _integer(minute or 0, "Minute", 0, CordialConst.CORDIAL_MINUTES_IN_HOUR - 1)
    second = _integer(second or 0, "Second", 0, CordialConst.CORDIAL_SECONDS_IN_MINUTE - 1)
    cron = _integer(cron or 0, "Cron", 0, CordialConst.CORDIAL_CRONS_IN_SECOND - 1)
    moment = CordialDatetime(cordial, CordialTime(hour, minute, second, cron)).to_gregorian_datetime()
    return [
        ("Gregorian date", moment.date.to_date_string()),
        ("Gregorian time", moment.time.to_time_string()),
        ("Gregorian 12-hour", moment.time.to_am_pm_string()),
        ("Weekday", moment.date.to_date().strftime("%A")),
        ("The Cordial day begins", "%s 12:00 (noon)" % begins.strftime("%B %d, %Y")),
        ("Cordial date and time", "%s %s" % (cordial.to_date_string(), CordialTime(hour, minute, second, cron).to_time_with_crons())),
    ]


def gregorian_time_to_cordial(hour, minute, second):
    hour = _integer(hour, "Hour", 0, 23)
    minute = _integer(minute, "Minute", 0, 59)
    second = _integer(second, "Second", 0, 59)
    time = GregorianTime(hour, minute, second)
    return [
        ("Cordial time", time.to_cordial_time()),
        ("Cordial 12-hour", time.to_cordial_am_pm_time()),
        ("Cordial time, truncated to the cron (HH:MM:SS.c, c = 0 to 6)", time.to_cordial_time_with_crons()),
        ("Cordial seconds since the Cordial day began (noon)", round(time.to_adjusted_cordial_seconds(), 1)),
        ("Crons since the Cordial day began (noon), seven to a Cordial second", time.to_adjusted_crons()),
    ]


def cordial_time_to_gregorian(hour, minute, second, cron=""):
    hour = _integer(hour, "Hour", 0, CordialConst.CORDIAL_HOURS_IN_DAY - 1)
    minute = _integer(minute, "Minute", 0, CordialConst.CORDIAL_MINUTES_IN_HOUR - 1)
    second = _integer(second, "Second", 0, CordialConst.CORDIAL_SECONDS_IN_MINUTE - 1)
    cron = _integer(cron or 0, "Cron", 0, CordialConst.CORDIAL_CRONS_IN_SECOND - 1)
    time = CordialTime(hour, minute, second, cron)
    return [
        ("Gregorian time", time.to_gregorian_time()),
        ("Gregorian 12-hour", time.to_gregorian_am_pm_time()),
        ("Seconds since the Cordial day began (noon)", time.to_adjusted_seconds()),
        ("Crons since the Cordial day began (noon)", time.get_crons()),
    ]


def degrees_to_grau(degrees, arcminutes=0, arcseconds=0):
    degrees = _integer(degrees, "Degrees", 0, 360)
    arcminutes = _integer(arcminutes or 0, "Arcminutes", 0, 59)
    arcseconds = _decimal(arcseconds or 0, "Arcseconds", 0, 59.999)
    angle = CordialAngleAdapter(degrees, arcminutes, arcseconds)
    if angle.decimal > 360:
        raise ConverterError("An angle cannot be larger than a full circle (360 degrees).")
    cordial = CordialAngle.from_decimal(round(angle.cdegrees, 9))  # rounded: 90 degrees is 90.99999... in floating point, not 91
    return [
        ("Grau", "%.6f" % round(angle.cdegrees, 9)),
        ("Grau, hours, minutes, seconds", cordial.to_symbol_string()),
        ("Decimal degrees", "%.6f" % angle.decimal),
    ]


def grau_to_degrees(cdegrees, chours=0, cminutes=0, cseconds=0):
    cdegrees = _integer(cdegrees, "Grau", 0, CordialConst.cdegrees_IN_CIRCLE)
    chours = _integer(chours or 0, "Grau hours", 0, CordialConst.chours_IN_GRAU - 1)
    cminutes = _integer(cminutes or 0, "Grau minutes", 0, CordialConst.cminutes_IN_GHOUR - 1)
    cseconds = _integer(cseconds or 0, "Grau seconds", 0, CordialConst.cseconds_IN_GMINUTE - 1)
    angle = CordialAngle(cdegrees, chours, cminutes, cseconds)
    if angle.decimal > CordialConst.cdegrees_IN_CIRCLE:
        raise ConverterError("An angle cannot be larger than a full circle (364 grau).")
    gregorian = CordialAngleAdapter.from_decimal(round(angle.degrees, 9))
    return [
        ("Decimal degrees", "%.6f" % angle.degrees),
        ("Degrees, arcminutes, arcseconds", "%d° %02d′ %02d″" % (gregorian.degrees, gregorian.arcminutes, gregorian.arcseconds)),
        ("Decimal grau", "%.6f" % angle.decimal),
    ]


def place_to_cordial(latitude, longitude):
    latitude = _decimal(latitude, "Latitude", -90, 90)
    longitude = _decimal(longitude, "Longitude", -180, 360)
    longitude = ((longitude + 180) % 360) - 180 if longitude > 180 else longitude  # 0..360 east is accepted too
    clon = float(CordialPlace.to_cordial_lon(longitude))
    clat = float(CordialPlace.to_cordial_lat(latitude))
    zone = CordialPlace.zone_number("cordial", longitude)
    conventional = CordialPlace.zone_number("gregorian", longitude)
    start = CordialConst.cdegrees_IN_CIRCLE - CordialPlace.ZONE_GRAU * (zone - 1)
    return [
        ("Cordial longitude", "%.4f grau (0 to 364, eastward from Greenwich)" % clon),
        ("Cordial latitude", "%.4f grau (-91 to 91)" % clat),
        ("Cordial time zone", "%d of 26 (starts at %d grau, ends at %d)" % (zone, start, start - CordialPlace.ZONE_GRAU)),
        ("Conventional time zone", "%+d (UTC)" % conventional),
    ]


def cordial_to_place(clongitude, clatitude):
    clongitude = _decimal(clongitude, "Cordial longitude", 0, CordialConst.cdegrees_IN_CIRCLE)
    clatitude = _decimal(clatitude, "Cordial latitude", -91, 91)
    longitude = clongitude * 360 / 364
    longitude = longitude - 360 if longitude > 180 else longitude
    return [
        ("Longitude", "%.4f° (-180 to 180, east positive)" % longitude),
        ("Latitude", "%.4f° (-90 to 90)" % (clatitude * 90 / 91)),
    ]


def sky_to_cordial(right_ascension, declination):
    right_ascension = _decimal(right_ascension, "Right ascension", 0, 24)
    declination = _decimal(declination, "Declination", -90, 90)
    return [
        ("Cordial right ascension", "%.4f grau (0 to 364)" % CordialSky.to_cra(right_ascension)),
        ("Cordial right ascension in Cordial hours", "%.4f (0 to 26)" % (right_ascension * CordialConst.CORDIAL_HOURS_IN_DAY / 24)),
        ("Cordial declination", "%.4f grau (-91 to 91)" % CordialSky.to_cdec(declination)),
    ]


def cordial_to_sky(cra, cdec):
    cra = _decimal(cra, "Cordial right ascension", 0, CordialConst.cdegrees_IN_CIRCLE)
    cdec = _decimal(cdec, "Cordial declination", -91, 91)
    return [
        ("Right ascension", "%.4f hours (0 to 24)" % (cra * 24 / 364)),
        ("Declination", "%.4f° (-90 to 90)" % (cdec * 90 / 91)),
    ]


def _julian_range():
    return CordialJulian, CordialJulian.first_year(), CordialJulian.last_year()


def _gregorian_check(jdn):
    """The Gregorian date of a Julian Day Number by the standard formula: shown only so the result can be checked against any other source."""
    return datetime.date.fromordinal(jdn - 1721425).strftime("%B %d, %Y")


def cordial_date_to_julian(year, month, day, void_day=1):
    """Cordial date (month 0 for a Void Day) to the Julian Day Number, directly: no other calendar is a step in it."""
    julian, first, last = _julian_range()
    year = _aa_year(year, first, last)
    month = _integer(month, "Month", 0, CordialConst.CORDIAL_MONTHS_IN_YEAR)
    if month == 0:
        void_day = _integer(void_day or 1, "Void day", 1, 2)
        if void_day > julian.n_void_days(year):
            raise ConverterError("Cordial year %d has only %d Void Day(s)." % (CordialConst.to_aa(year), julian.n_void_days(year)))
        jdn = julian.void_to_jdn(year, void_day)
        cordial_text = CordialVoidDay(year, void_day).to_date_string()
    else:
        day = _integer(day, "Day", 1, CordialConst.CORDIAL_DAYS_IN_MONTH)
        jdn = julian.cordial_to_jdn(year, month, day)
        cordial_text = CordialDate(year, month, day).to_date_string()
    return [
        ("Julian Day Number", jdn),
        ("Cordial date", cordial_text),
        ("The Julian day (and the Cordial day) begins at noon on", _gregorian_check(jdn) + " (the standard formula, shown for checking)"),
    ]


def julian_to_cordial_date(jdn):
    julian, first, last = _julian_range()
    low, high = julian.year_start(first), julian.year_start(last + 1) - 1
    jdn = _integer(jdn, "Julian Day Number", low, high)
    kind = julian.jdn_to_cordial(jdn)
    if kind[0] == "date":
        cordial = CordialDate(*kind[1:])
        text = cordial.to_date_string()
        extra = [("Year, month, day", "%d %s, %d (%s), %d" % (CordialConst.to_aa(cordial.year), CordialConst.ERA_NAME, cordial.month, _month_name(cordial.get_name_of_month()), cordial.day))]
    else:
        text = CordialVoidDay(*kind[1:]).to_date_string()
        extra = [("Cordial year", "%d %s" % (CordialConst.to_aa(kind[1]), CordialConst.ERA_NAME))]
    return [("Cordial date", text)] + extra + [("The Julian day (and the Cordial day) begins at noon on", _gregorian_check(jdn) + " (the standard formula, shown for checking)")]
