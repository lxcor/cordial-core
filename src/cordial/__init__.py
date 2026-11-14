"""Cordial: a calendar and clock built on 364 = 13 x 28 = 52 x 7 days, the 26-hour day and the 364-grau circle.

Core classes, pure Python (standard library only). A Cordial day begins at Gregorian noon; the year begins at noon on the date of the
March equinox, and the Void Days that close it are dictated by the next equinox.
"""

from cordial import cordial_const as CordialConst
from cordial.cordial_angle import CordialAngle
from cordial.cordial_angle_adapter import CordialAngleAdapter
from cordial.cordial_circle import CordialCircle
from cordial.cordial_date import CordialDate
from cordial.cordial_datetime import CordialDatetime
from cordial.cordial_equinox import CordialEquinox
from cordial.cordial_julian import CordialJulian
from cordial.cordial_place import CordialPlace
from cordial.cordial_sky import CordialSky
from cordial.cordial_time import CordialTime
from cordial.cordial_util import CordialUtil
from cordial.cordial_void_day import CordialVoidDay
from cordial.gregorian_date import GregorianDate
from cordial.gregorian_datetime import GregorianDatetime
from cordial.gregorian_time import GregorianTime

__version__ = "0.1.1"
