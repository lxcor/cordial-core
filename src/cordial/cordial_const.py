JULIAN_EPOCH = 1721425.5  # Julian Date of the Gregorian epoch (1 Jan 1 CE, at midnight)
JULIAN_DAY_NUMBER_OF_ORDINAL_ZERO = 1721425  # date.toordinal() + this = the Julian Day Number of the day that begins at noon on that date

CORDIAL_HOURS_IN_DAY = 26  # 28
CORDIAL_MINUTES_IN_HOUR = 52  # 56
CORDIAL_SECONDS_IN_MINUTE = 52  # 56

GREGORIAN_HOURS_IN_DAY = 24
GREGORIAN_MINUTES_IN_HOUR = 60
GREGORIAN_SECONDS_IN_MINUTE = 60

CORDIAL_SECONDS_IN_DAY = 70304  # 75712  # 87808
GREGORIAN_SECONDS_IN_DAY = 86400

CORDIAL_SECONDS_IN_HOUR = 2704  # 3136
GREGORIAN_SECONDS_IN_HOUR = 3600

# The cron is one division of the Cordial clock's dial: a seventh of a Cordial second, 364 to a Cordial minute (a full lap of the
# second hand). The system fixes the NUMBER of crons in a day, not the length of one: a cron is a fixed fraction of the sun's mean
# day and its length is calibrated against the sun. The conversions to today's seconds below are a snapshot of that calibration.
CORDIAL_CRONS_IN_SECOND = 7
CORDIAL_CRONS_IN_MINUTE = CORDIAL_SECONDS_IN_MINUTE * CORDIAL_CRONS_IN_SECOND  # 364
CORDIAL_CRONS_IN_HOUR = CORDIAL_MINUTES_IN_HOUR * CORDIAL_CRONS_IN_MINUTE  # 18928
CORDIAL_CRONS_IN_DAY = CORDIAL_HOURS_IN_DAY * CORDIAL_CRONS_IN_HOUR  # 492128

GREGORIAN_SECONDS_IN_CORDIAL_SECOND = GREGORIAN_SECONDS_IN_DAY / CORDIAL_SECONDS_IN_DAY  # 1.2289...
CORDIAL_SECONDS_IN_GREGORIAN_SECOND = CORDIAL_SECONDS_IN_DAY / GREGORIAN_SECONDS_IN_DAY  # 0.8137...
GREGORIAN_SECONDS_IN_CRON = GREGORIAN_SECONDS_IN_DAY / CORDIAL_CRONS_IN_DAY  # 0.1755...

CORDIAL_DAYS_IN_YEAR = 364
CORDIAL_MONTHS_IN_YEAR = 13
CORDIAL_DAYS_IN_MONTH = 28
CORDIAL_WEEKS_IN_MONTH = 4
CORDIAL_DAYS_IN_WEEK = 7

GREGORIAN_MONTHS_IN_YEAR = 12
GREGORIAN_DAYS_IN_MONTH = 4

GREGORIAN_DAYS_IN_NON_LEAP_YEAR = 365
GREGORIAN_DAYS_IN_LEAP_YEAR = 366

# VIBGYOR = ["Violet", "Indigo", "Blue", "Green", "Yellow", "Orange", "Red"]
# RYOGBIV = ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Magenta"]
# RYOGBIV = ["Lime", "Cyan", "Blue", "Magenta", "Yellow", "Orange", "Red"]
# WEEKDAYS = RYOGBIV


spring = {
    'index': 0,
    'name': 'Spring'}

summer = {
    'index': 1,
    'name': 'Summer'}

autumn = {
    'index': 2,
    'name': 'Autumn'}

winter = {
    'index': 3,
    'name': 'Winter'}

SEASONS = [spring, summer, autumn, winter]

TAURUS = {'name': 'Taurus',
          'abbrev': 'Tau'}

ORION = {'name': 'Orion',
         'abbrev': 'Ori'}

GEMINI = {'name': 'Gemini',
          'abbrev': 'Gem'}

CANCER = {'name': 'Cancer',
          'abbrev': 'Cnc'}

LEO = {'name': 'Leo',
       'abbrev': 'Leo'}

VIRGO = {'name': 'Virgo',
         'abbrev': 'Vir'}

LIBRA = {'name': 'Libra',
         'abbrev': 'Lib'}

SCORPIO = {'name': 'Scorpio',
           'abbrev': 'Sco'}

SAGITTARIUS = {'name': 'Sagittarius',
               'abbrev': 'Sgr'}

CAPRICORN = {'name': 'Capricorn',
             'abbrev': 'Cap'}

AQUARIUS = {'name': 'Aquarius',
            'abbrev': 'Aqr'}

PISCES = {'name': 'Pisces',
          'abbrev': 'Psc'}

ARIES = {'name': 'Aries',
         'abbrev': 'Ari'}

MONTHS = [TAURUS, ORION, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES, ARIES]
# "Taurus", "Orion", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces", "Aries"]

VERNAL_EQUINOX = 0
SUMMER_SOLSTICE = 1
AUTUMNAL_EQUINOX = 2
WINTER_SOLSTICE = 3

CORDIAL_DAY_POLARITY_POSITIVE = "+"
CORDIAL_DAY_POLARITY_NEGATIVE = "-"

# Fixit
DEGREES_IN_GRAU = 0.989010989010989
cdegrees_IN_DEGREE = 1.01111111111111

DEGREES_IN_CIRCLE = 360
ARCMINUTES_IN_DEGREE = 60
ARCSECONDS_IN_DEGREE = 3600
ARCSECONDS_IN_ARCMINUTE = 60

cdegrees_IN_CIRCLE = 364
chours_IN_GRAU = 26
cminutes_IN_GRAU = 1352  # 1568
cseconds_IN_GRAU = 70304  # 87808
cminutes_IN_GHOUR = 52
cseconds_IN_GMINUTE = 52

# Red: Ruber (Rb)
# Orange: Aurantium (Au)
# Yellow: Flavus (Fl)
# Green: Viridis (Vi)
# Cyan: Caeruleus (Cy)
# Blue: Livens (Li)
# Magenta: Ostrum (Ot)

red = {
    "name": "Red",
    "latin": "Ruber",
    "code": "Ru",
    "html": "red"
}

orange = {
    "name": "Orange",
    "latin": "Aurantium",
    "code": "Au",
    "html": "orange"
}

yellow = {
    "name": "Yellow",
    "latin": "Flavus",
    "code": "Fl",
    "html": "yellow"
}

green = {
    "name": "Green",
    "latin": "Viridis",
    "code": "Vi",
    "html": "green"
}

cyan = {
    "name": "Aqua",
    "latin": "Caeruleus",
    "code": "Cy",
    "html": "cyan"
}

blue = {
    "name": "Blue",
    "latin": "Lividus",
    "code": "Li",
    "html": "blue"
}

magenta = {
    "name": "Purple",
    "latin": "Ostrum",
    "code": "Os",
    "html": "magenta"
}

# hyacinth

black = {
    "name": "Black",
    "latin": "Perniger",
    "code": "Ng",
    "html": "black"
}

COLORS = [blue, cyan, green, yellow, orange, red, magenta]
# COLORS = [blue, cyan, green, yellow, red ,magenta, black]

first = {
    "name": "First",
    "code": "1st"
}

second = {
    "name": "Second",
    "code": "2nd"
}

third = {
    "name": "Third",
    "code": "3rd"
}

fourth = {
    "name": "Fourth",
    "code": "4th"
}

WEEKS = [first, second, third, fourth]

# Era of the Cordial year count: Anno Adami (AA). Year 1 begins at noon on the spring equinox of the year of Adam's birth,
# taken as 4004 BC (the author's reading of Ussher's chronology). Internally a Cordial year is still labelled by the Gregorian
# year of its closing equinox (astronomy caches, equinox tables, Julian module); the AA number exists only at the edges
# (URLs, forms, displayed dates) through to_aa / from_aa. 4004 BC is the Gregorian year -4003 (no year 0 in BC counting),
# so internal -4002 (closing equinox of Year 1) -> AA 1.
ERA_NAME = "AA"
ADAM_BIRTH_YEAR_BC = 4004
AA_OFFSET = ADAM_BIRTH_YEAR_BC - 1


def to_aa(internal_year):
    return internal_year + AA_OFFSET


def from_aa(aa_year):
    return aa_year - AA_OFFSET
