"""Tests of the core, pure Python: no Django, no ephemeris, no data files besides the packaged equinox table.

Run with:  python -m unittest discover -s tests   (with src on the path, or after ``pip install -e .``)

The Julian Day Number is the external witness: every Cordial day must have the Julian Day Number of the Gregorian date it is listed
under, a count that is computed here from ``date.toordinal()`` and belongs to no calendar of ours.
"""
import datetime
import unittest

from cordial import CordialConst, CordialDate, CordialDatetime, CordialEquinox, CordialJulian, CordialTime, CordialUtil, CordialVoidDay
from cordial import GregorianDate, GregorianDatetime, GregorianTime
from cordial import cordial_converter as converter
from cordial.cordial_converter import ConverterError

AA = CordialConst.AA_OFFSET   # the converters speak AA years; the model keeps the internal index (the Gregorian year of the closing equinox)
FIRST, LAST = converter.CORDIAL_YEARS


def value(rows, label):
    return dict(rows)[label]


def external_jdn(date):
    """Julian Day Number of the day that begins at noon on a Gregorian date, independent of the Cordial code."""
    return date.toordinal() + 1721425


def days_of(year):
    days = [CordialDate(year, month, day) for month in range(1, 14) for day in range(1, 29)]
    return days + [CordialVoidDay(year, number) for number in range(1, CordialVoidDay(year).n_void_days() + 1)]


class DateStrings(unittest.TestCase):
    def test_blue_is_lividus(self):
        self.assertEqual([c['latin'] for c in CordialConst.COLORS if c['name'] == 'Blue'], ['Lividus'])

    def test_no_space_before_the_comma(self):
        for text in (CordialDate(2027, 1, 1).to_custom_date(), CordialDate(2027, 1, 1).to_date_string(), CordialDate(2027, 13, 28).to_full_date()):
            self.assertNotIn(' ,', text)
        self.assertTrue(CordialDate(2027, 1, 1).to_custom_date().endswith('Taurus, %d' % CordialConst.to_aa(2027)))


class Equinox(unittest.TestCase):

    def test_the_table_ships_with_the_package_and_covers_2019_to_2052(self):
        self.assertEqual((CordialEquinox.first_year(), CordialEquinox.last_year()), (2019, 2052))
        self.assertEqual((FIRST, LAST), (2020, 2052))

    def test_known_equinoxes(self):
        self.assertEqual(CordialEquinox.to_date(2026), datetime.date(2026, 3, 20))
        self.assertEqual(CordialEquinox.to_date(2025), datetime.date(2025, 3, 20))
        self.assertEqual(CordialEquinox.to_date(2028), datetime.date(2028, 3, 20))
        self.assertEqual(CordialEquinox.to_datetime(2026).hour, 14)           # 14:46 UT
        with self.assertRaises(ValueError):
            CordialEquinox.julian_date(2053)


class JulianDayAsWitness(unittest.TestCase):

    def test_the_external_formula_is_right(self):
        self.assertEqual(external_jdn(datetime.date(2000, 1, 1)), 2451545)

    def test_every_cordial_day_has_the_julian_day_number_of_its_gregorian_date(self):
        for year in range(FIRST, LAST + 1):
            for day in days_of(year):
                if isinstance(day, CordialVoidDay):
                    jdn = CordialJulian.void_to_jdn(year, day.void_day)
                else:
                    jdn = CordialJulian.cordial_to_jdn(year, day.month, day.day)
                self.assertEqual(jdn, external_jdn(day.to_gregorian_date()), (year, day.to_date_string()))

    def test_every_julian_day_converts_back_and_agrees_with_gregorian_to_cordial(self):
        first = CordialJulian.year_start(FIRST)
        last = CordialJulian.year_start(LAST + 1) - 1
        for jdn in range(first, last + 1):
            kind = CordialJulian.jdn_to_cordial(jdn)
            if kind[0] == 'date':
                self.assertEqual(CordialJulian.cordial_to_jdn(*kind[1:]), jdn)
                text = CordialDate(*kind[1:]).to_date_string()
            else:
                self.assertEqual(CordialJulian.void_to_jdn(*kind[1:]), jdn)
                text = CordialVoidDay(*kind[1:]).to_date_string()
            gregorian = datetime.date.fromordinal(jdn - 1721425)
            self.assertEqual(GregorianDate.from_date(gregorian).to_cordial_date().to_date_string(), text, jdn)

    def test_the_calendar_has_no_gap_and_no_repeat(self):
        """Walking the Gregorian days from the first Cordial day to the last, the Cordial day advances by exactly one."""
        date, last = converter.gregorian_date_range()
        for day in [day for year in range(FIRST, LAST + 1) for day in days_of(year)]:
            self.assertLessEqual(date, last)
            self.assertEqual(GregorianDate.from_date(date).to_cordial_date().to_date_string(), day.to_date_string(), date)
            self.assertEqual(day.to_gregorian_date(), date)
            date += datetime.timedelta(days=1)
        self.assertEqual(date, last + datetime.timedelta(days=1))

    def test_years_chain_and_void_days_follow_the_sky(self):
        for year in range(FIRST, LAST + 1):
            n_void = CordialJulian.n_void_days(year)
            self.assertEqual(CordialJulian.year_start(year + 1), CordialJulian.year_start(year) + 364 + n_void, year)
        forecast_wrong = [year for year in range(FIRST, LAST + 1) if CordialUtil.n_void_days_by_rule(year) != CordialJulian.n_void_days_by_equinox(year)]
        self.assertEqual(forecast_wrong, [2044, 2045, 2048, 2049, 2052])       # where the leap-year forecast and the sky differ
        self.assertEqual((CordialVoidDay(2044).n_void_days(), CordialVoidDay(2045).n_void_days()), (1, 2))
        self.assertFalse(CordialJulian.covers(LAST + 1))
        self.assertEqual(CordialUtil.n_void_days(2100), CordialUtil.n_void_days_by_rule(2100))   # beyond the table the forecast is all there is
        with self.assertRaises(ValueError):
            CordialJulian.void_to_jdn(2044, 2)


class GregorianToCordial(unittest.TestCase):

    def test_boundary_days(self):
        self.assertEqual(GregorianDate(2026, 11, 13).to_cordial_date().to_date_string(), 'Sagittarius 15, 6030')
        self.assertEqual(GregorianDate(2026, 11, 13).to_cordial_day(), 15)
        self.assertIsInstance(GregorianDate(2026, 3, 19).to_cordial_date(), CordialVoidDay)   # the Void Day is the day before the equinox date
        self.assertEqual(GregorianDate(2026, 3, 20).to_cordial_date().to_date_string(), 'Taurus 01, 6030')   # the equinox date opens the year
        self.assertEqual(GregorianDate(2028, 3, 18).to_cordial_date().void_day, 1)             # 2028: two Void Days
        self.assertEqual(GregorianDate(2028, 3, 19).to_cordial_date().void_day, 2)
        self.assertEqual(CordialVoidDay(2027).year, 2027)

    def test_outside_the_table_is_a_clear_error(self):
        with self.assertRaises(ValueError):
            GregorianDate(2053, 6, 1).to_cordial_date()
        self.assertIsNone(GregorianDate(2019, 3, 19).to_cordial_day_from_noon())


class Datetimes(unittest.TestCase):
    """A Cordial day begins at Gregorian noon; the Cordial time counts from that noon."""

    def cordial_of(self, year, month, day, hour, minute, second):
        moment = GregorianDatetime(GregorianDate(year, month, day), GregorianTime(hour, minute, second)).to_cordial_datetime()
        return moment.date.to_date_string(), moment.time.to_time()

    def test_the_noon_boundary(self):
        self.assertEqual(value(converter.cordial_date_to_gregorian(2027 + AA, 9, 15), 'Gregorian date'), 'November 13, 2026')
        self.assertEqual(self.cordial_of(2026, 11, 13, 12, 0, 0), ('Sagittarius 15, 6030', '00:00:00'))
        self.assertEqual(self.cordial_of(2026, 11, 13, 11, 59, 59), ('Sagittarius 14, 6030', '25:51:51'))
        self.assertEqual(self.cordial_of(2026, 11, 13, 0, 0, 0)[0], 'Sagittarius 14, 6030')
        self.assertEqual(self.cordial_of(2026, 11, 13, 23, 59, 59)[0], 'Sagittarius 15, 6030')

    def test_year_boundary_and_void_days(self):
        self.assertEqual(self.cordial_of(2026, 3, 20, 12, 0, 0), ('Taurus 01, 6030', '00:00:00'))
        self.assertEqual(self.cordial_of(2026, 3, 20, 11, 59, 59)[0], 'Void Day (non leap)')
        self.assertEqual(self.cordial_of(2026, 3, 19, 12, 0, 0)[0], 'Void Day (non leap)')
        self.assertEqual(self.cordial_of(2026, 3, 19, 11, 59, 59)[0], 'Aries 28, 6029')

    def test_every_cordial_day_round_trips_through_a_datetime(self):
        for year in range(FIRST, LAST + 1):
            for cordial in days_of(year)[:364]:
                for time in (CordialTime(0, 0, 0), CordialTime(13, 26, 0), CordialTime(25, 51, 51)):
                    back = CordialDatetime(cordial, time).to_gregorian_datetime().to_cordial_datetime()
                    self.assertEqual(back.date.to_date_string(), cordial.to_date_string(), (cordial, time))
                    # a Cordial second is 1.23 Gregorian seconds and the Gregorian time is cut to whole seconds: at most one Cordial second apart
                    self.assertLessEqual(abs(back.time.get_cordial_seconds() - time.get_cordial_seconds()), 1, (cordial, time))

    def test_the_converter_with_a_time(self):
        rows = converter.gregorian_date_to_cordial(2026, 11, 13, 15, 0, 0)
        self.assertEqual((value(rows, 'Cordial date'), value(rows, 'Cordial time')), ('Sagittarius 15, 6030', '03:13:00'))
        self.assertEqual(value(converter.gregorian_date_to_cordial(2026, 11, 13, 9, 0, 0), 'Cordial date'), 'Sagittarius 14, 6030')
        rows = converter.cordial_date_to_gregorian(2027 + AA, 9, 15, 1, 3, 13, 0)
        self.assertEqual((value(rows, 'Gregorian date'), value(rows, 'Gregorian time')), ('November 13, 2026', '15:00:00'))

    def test_outside_the_table_gives_a_message(self):
        for call in (lambda: converter.gregorian_date_to_cordial(2019, 3, 20, 11, 0, 0), lambda: converter.gregorian_date_to_cordial(2053, 1, 1, 12, 0, 0),
                     lambda: converter.gregorian_date_to_cordial(1999, 1, 1), lambda: converter.gregorian_date_to_cordial(2052, 3, 19)):
            with self.assertRaises(ConverterError):
                call()
        self.assertEqual(value(converter.gregorian_date_to_cordial(2052, 3, 18), 'Cordial date'), 'Void Day (non leap)')   # the last day of the table


class ConverterFunctions(unittest.TestCase):

    def test_places_and_zones(self):
        rows = converter.place_to_cordial(0, 0)
        self.assertTrue(value(rows, 'Cordial time zone').startswith('1 of 26 (starts at 364'))
        self.assertTrue(value(rows, 'Cordial longitude').startswith('0.0000'))
        rows = converter.place_to_cordial(48.4284, -123.3656)        # Victoria BC: zone 9, conventional -8
        self.assertTrue(value(rows, 'Cordial time zone').startswith('9 of 26'))
        self.assertTrue(value(rows, 'Conventional time zone').startswith('-8'))
        back = converter.cordial_to_place(float(value(rows, 'Cordial longitude').split()[0]), float(value(rows, 'Cordial latitude').split()[0]))
        self.assertTrue(value(back, 'Longitude').startswith('-123.3656'))
        self.assertTrue(value(back, 'Latitude').startswith('48.4284'))

    def test_sky_round_trip(self):
        rows = converter.sky_to_cordial(6, 23.44)
        self.assertTrue(value(rows, 'Cordial right ascension').startswith('91.0000'))
        back = converter.cordial_to_sky(91, float(value(rows, 'Cordial declination').split()[0]))
        self.assertTrue(value(back, 'Right ascension').startswith('6.0000'))
        self.assertTrue(value(back, 'Declination').startswith('23.4400'))

    def test_bad_input_gives_a_message_not_an_error(self):
        for call in (lambda: converter.gregorian_date_to_cordial(2026, 2, 30),
                     lambda: converter.cordial_time_to_gregorian(26, 0, 0),
                     lambda: converter.cordial_date_to_gregorian(2027 + AA, 14, 1),
                     lambda: converter.cordial_date_to_gregorian(2027 + AA, 0, 1, 2),   # 2027 has one Void Day
                     lambda: converter.place_to_cordial(91, 0),
                     lambda: converter.degrees_to_grau('abc'),
                     lambda: converter.cordial_date_to_julian(1999 + AA, 1, 1),
                     lambda: converter.julian_to_cordial_date(1),
                     lambda: converter.julian_to_cordial_date('abc')):
            with self.assertRaises(ConverterError):
                call()

    def test_cordial_date_to_julian_and_back(self):
        rows = converter.cordial_date_to_julian(2027 + AA, 9, 15)
        self.assertEqual(value(rows, 'Julian Day Number'), 2461358)
        self.assertIn('November 13, 2026', value(rows, 'The Julian day (and the Cordial day) begins at noon on'))
        self.assertEqual(value(converter.julian_to_cordial_date(2461358), 'Cordial date'), 'Sagittarius 15, 6030')
        void = converter.cordial_date_to_julian(2028 + AA, 0, 1, 2)
        self.assertEqual(converter.julian_to_cordial_date(value(void, 'Julian Day Number'))[0][1], value(void, 'Cordial date'))


class Crons(unittest.TestCase):
    """A cron is one division of the clock's dial: a seventh of a Cordial second, 364 to a Cordial minute, 492,128 to the day."""

    def test_the_counts(self):
        self.assertEqual((CordialConst.CORDIAL_CRONS_IN_SECOND, CordialConst.CORDIAL_CRONS_IN_MINUTE, CordialConst.CORDIAL_CRONS_IN_HOUR, CordialConst.CORDIAL_CRONS_IN_DAY),
                         (7, 364, 18928, 492128))
        self.assertEqual(CordialConst.CORDIAL_CRONS_IN_DAY, 32 * 13 ** 3 * 7)
        self.assertAlmostEqual(CordialConst.GREGORIAN_SECONDS_IN_CORDIAL_SECOND, 1.22894856622667, places=12)
        self.assertAlmostEqual(CordialConst.GREGORIAN_SECONDS_IN_CRON, 0.17556408, places=7)

    def test_cordial_time_counts_crons(self):
        self.assertEqual(CordialTime(0, 0, 0, 3).get_crons(), 3)
        self.assertEqual(CordialTime(0, 1, 0).get_crons(), 364)
        self.assertEqual(CordialTime(25, 51, 51, 6).get_crons(), 492128 - 1)
        self.assertEqual(CordialTime(4, 25, 48, 5).to_time_with_crons(), '04:25:48.5')

    def test_gregorian_time_to_the_cron(self):
        self.assertEqual(GregorianTime(12, 0, 0).to_cordial_time_with_crons(), '00:00:00.0')
        self.assertEqual(GregorianTime(11, 59, 59).to_cordial_time_with_crons(), '25:51:51.1')
        self.assertEqual(GregorianTime(15, 0, 0).to_cordial_time_with_crons(), '03:13:00.0')
        self.assertEqual(GregorianTime(16, 9, 9).to_cordial_time_with_crons(), '04:25:48.0')
        for second in range(0, 86400, 997):
            self.assertTrue(0 <= GregorianTime(second // 3600, (second // 60) % 60, second % 60).to_adjusted_crons() < 492128)

    def test_the_converter_knows_crons(self):
        with self.assertRaises(ConverterError):
            converter.cordial_time_to_gregorian(4, 25, 48, 7)
        rows = converter.cordial_date_to_gregorian(2027 + AA, 9, 15, 1, 3, 13, 0, 4)
        self.assertTrue(value(rows, 'Cordial date and time').endswith('03:13:00.4'))


class AnnoAdami(unittest.TestCase):

    def test_the_offset(self):
        self.assertEqual(CordialConst.AA_OFFSET, 4003)
        self.assertEqual(CordialConst.to_aa(2027), 6030)
        self.assertEqual(CordialConst.from_aa(6030), 2027)
        self.assertEqual(CordialConst.to_aa(-4002), 1)

    def test_cordial_dates_show_the_aa_year(self):
        self.assertIn('6030 AA', value(converter.gregorian_date_to_cordial(2026, 11, 13), 'Year, month, day'))


class NothingHeavyIsImported(unittest.TestCase):

    def test_the_core_needs_only_the_standard_library(self):
        import sys
        for name in ('django', 'numpy', 'pandas', 'skyfield', 'matplotlib'):
            self.assertNotIn(name, sys.modules, name)


if __name__ == '__main__':
    unittest.main()
