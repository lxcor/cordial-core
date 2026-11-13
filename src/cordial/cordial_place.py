import math


class CordialPlace:
    """Places on the Earth in Cordial units: longitude and latitude in grau, and the 26 Cordial time zones.

    The circle is 364 grau (a quarter circle 91), so one Cordial hour of the Earth's turn is 364 / 26 = 14 grau. Cordial longitude
    is unsigned, like right ascension: 0 to 364 eastward from Greenwich. Cordial time zones are numbered 1 to 26 in the
    direction of the sun (the grau fall): zone n starts at 364 - 14 (n - 1) grau and ends 14 grau lower, so zone 1 is 350 to 364,
    just west of Greenwich, and zone 26 is 0 to 14. The Gregorian zones are 24 bands of 15 degrees, zone 0 centred on Greenwich.
    The anchor of the Cordial zones is provisional.
    """

    GRAU_IN_CIRCLE = 364
    ZONE_GRAU = 14
    ZONES_CORDIAL = 26
    ZONE_DEGREES = 15

    @staticmethod
    def to_cordial_lon(lon):
        """Longitude in degrees (-180..180, east positive) to Cordial longitude: unsigned grau, 0..364 eastward from Greenwich."""
        return (lon % 360) * 364 / 360

    @staticmethod
    def to_cordial_lat(lat):
        """Latitude in degrees (-90..90, equator at 0) to Cordial latitude (-91..91): a quarter circle is 91 grau, not 90 degrees."""
        return lat * 91 / 90

    @staticmethod
    def zone_number(calendar, lon):
        """The zone number of a longitude in degrees: 1..26 for the Cordial calendar, -12..12 (the UTC offset) for the Gregorian."""
        if calendar == "cordial":
            clon = CordialPlace.to_cordial_lon(lon)
            if clon == 0:
                clon = 364.0  # Greenwich is both 0 and 364: the sun enters zone 1 there
            return int(math.floor((364.0 - clon) / CordialPlace.ZONE_GRAU)) + 1
        return int(min(max(math.floor((lon + 7.5) / 15), -12), 12))

    @staticmethod
    def zone_bands(calendar):
        """[(zone number, west edge, east edge), ...] clipped to the canvas, in degrees (gregorian) or grau (cordial)."""
        if calendar == "cordial":
            width = CordialPlace.ZONE_GRAU
            # zone n starts at 364 - 14(n-1) and ends 14 grau lower: the numbers rise in the direction of the sun (the grau fall)
            return [(n, (CordialPlace.ZONES_CORDIAL - n) * width, (CordialPlace.ZONES_CORDIAL - n + 1) * width) for n in range(1, CordialPlace.ZONES_CORDIAL + 1)]
        return [(k, max(15 * k - 7.5, -180), min(15 * k + 7.5, 180)) for k in range(-12, 13)]
