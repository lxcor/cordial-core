import math


class CordialSky:
    """Celestial coordinates in Cordial units: the circle of the sky is 364 grau, not 360 degrees, and a quarter circle is 91.

    Right ascension runs 0-24 hours in the Gregorian system and 0-364 grau in the Cordial one (the Cordial day has 26 hours, so
    a Cordial hour is 14 grau); declination and latitude run -90..90 degrees against -91..91 grau. Longitude is unsigned.
    Only the arithmetic lives here: positions of the Sun, Moon and stars come from an ephemeris and are not part of this package.
    """

    @staticmethod
    def ra_to_degrees(hours, minutes, seconds):
        """
        Convert right ascension (RA) from hours, minutes, and seconds to degrees.

        Parameters:
        hours (int): Hours part of RA - from 0 to 24
        minutes (int): Minutes part of RA - from 0 to 59
        seconds (float): Seconds part of RA - from 0 to 59.99

        Returns:
        float: RA in degrees
        """
        # There are 15 degrees per hour of RA (since 360 degrees / 24 hours = 15 degrees/hour)
        degrees = hours * 15.0
        # There are 0.25 degrees per minute of RA (since 15 degrees / 60 minutes = 0.25 degrees/minute)
        degrees += minutes * 0.25
        # There are 0.00416667 degrees per second of RA (since 0.25 degrees / 60 seconds = 0.00416667 degrees/second)
        degrees += seconds * (15.0 / 3600.0)
        return degrees

    @staticmethod
    def dec_to_degrees(degrees, minutes, seconds, is_negative=False):
        """
        Convert declination (Dec) from degrees, minutes, and seconds to decimal degrees.

        Parameters:
        degrees (int): Degrees part of Dec - from -90 to 90
        minutes (int): Minutes part of Dec - from 0 to 59
        seconds (float): Seconds part of Dec - from 0 to 59.99
        is_negative (bool): Whether the declination is negative

        Returns:
        float: Dec in decimal degrees
        """
        # Convert everything to positive degrees
        decimal_degrees = abs(degrees) + minutes / 60.0 + seconds / 3600.0
        # Apply negative sign if necessary
        if is_negative or degrees < 0:
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    @staticmethod
    def is_valid_declination(degrees, minutes, seconds):
        """
        Check if the given degrees, minutes, and seconds form a valid declination.

        Parameters:
        degrees (int): Degrees part of Dec
        minutes (int): Minutes part of Dec
        seconds (float): Seconds part of Dec

        Returns:
        bool: True if the declination is valid, False otherwise
        """
        if not (-90 <= degrees <= 90):
            return False
        if not (0 <= minutes < 60):
            return False
        if not (0 <= seconds < 60):
            return False
        return True

    @staticmethod
    def is_valid_right_ascension(hours, minutes, seconds):
        """
        Check if the given hours, minutes, and seconds form a valid right ascension.

        Parameters:
        hours (int): Hours part of RA
        minutes (int): Minutes part of RA
        seconds (float): Seconds part of RA

        Returns:
        bool: True if the right ascension is valid, False otherwise
        """
        if not (0 <= hours < 24):
            return False
        if not (0 <= minutes < 60):
            return False
        if not (0 <= seconds < 60):
            return False
        return True

    @staticmethod
    def ra_to_radians(ra_degrees):
        """
        Convert Right Ascension from degrees to radians.

        Parameters:
        ra_degrees (float): Right Ascension in degrees.

        Returns:
        float: Right Ascension in radians.
        """
        return ra_degrees * (math.pi / 180)

    @staticmethod
    def dec_to_radians(dec_degrees):
        """
        Convert Declination from degrees to radians.

        Parameters:
        dec_degrees (float): Declination in degrees.

        Returns:
        float: Declination in radians.
        """
        return dec_degrees * (math.pi / 180)

    @staticmethod
    def degrees_to_radians(degrees):
        return degrees * (math.pi / 180)

    @staticmethod
    def radians_to_degrees(radians):
        return radians * (180 / math.pi)

    @staticmethod
    def angular_distance(ra1, dec1, ra2, dec2):
        # Convert degrees to radians
        ra1_rad = CordialSky.ra_to_radians(ra1)
        dec1_rad = CordialSky.dec_to_radians(dec1)
        ra2_rad = CordialSky.ra_to_radians(ra2)
        dec2_rad = CordialSky.dec_to_radians(dec2)

        # Apply the haversine formula for angular distance
        delta_ra = ra2_rad - ra1_rad
        central_angle = math.acos(math.sin(dec1_rad) * math.sin(dec2_rad) + math.cos(dec1_rad) * math.cos(dec2_rad) * math.cos(delta_ra))

        # Convert radians to degrees for the result
        return central_angle * (180 / math.pi)

    @staticmethod
    def ra_degrees_to_hms(degrees):

        if not math.isnan(degrees):
            # Convert degrees to total hours
            total_hours = degrees / 15.0

            # Extract the hours
            hours = int(total_hours)

            # Extract the minutes
            minutes = int((total_hours - hours) * 60)

            # Extract the seconds
            seconds = ((total_hours - hours) * 60 - minutes) * 60

            # print(f"RA: {hours}h {minutes}m {seconds:.2f}s")

            return hours, minutes, seconds

    @staticmethod
    def to_cra(ra):

        if ra < 0 or ra > 24:
            raise ValueError("value_a must be in the range 0-24")

        # Calculate the conversion factor
        conversion_factor = 364 / 24

        # Convert value_a to value_b
        cra = ra * conversion_factor

        return cra

    @staticmethod
    def to_cdec(dec):

        if not -90 <= dec <= 90:
            raise ValueError("Dec must be in the range -90 to 90.")

        # Normalize value_A to a range of 0 to 1
        normalized_dec = (dec + 90) / 180

        # Scale normalized value to the range of -91 to 91
        cdec = normalized_dec * 182 - 91

        return cdec

    @staticmethod
    def to_clon(lon):

        if lon < 0:
            lon = 360+lon

        if lon > 360:
            lon = lon-360

        # Ensure the input is within the 0-360 range
        if not (0 <= lon <= 360):
            raise ValueError("Input value must be between 0 and 360")

        # Convert the value from 0-360 to 0-364
        converted_value = (lon / 360) * 364

        return round(converted_value)

    @staticmethod
    def to_clat(lat):

        # Ensure the input is within the -90 to 90 range
        if not (-90 <= lat <= 90):
            raise ValueError("Input value must be between -90 and 90")

        # Convert the value from -90 to 90 to -91 to 91
        converted_value = (lat / 90) * 91

        return round(converted_value)
