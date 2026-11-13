from cordial import cordial_const as CordialConst


class CordialAngle:
    """An angle in Cordial units: grau, and the Cordial hours, minutes and seconds into which a grau divides.

    The circle is 364 grau (a quarter circle 91), not 360 degrees. One grau is the turn of the Earth in one Cordial day divided by 364:
    26 Cordial hours of 52 minutes of 52 seconds, so 1 grau = 70,304 Cordial seconds, and a Cordial hour of the Earth's turn is 14 grau.
    Its Gregorian counterpart is degrees, arcminutes and arcseconds (see CordialAngleAdapter); 1 grau = 360/364 degrees."""

    def __init__(self, cdegrees, chours=0, cminutes=0, cseconds=0):
        self.cdegrees = cdegrees
        self.chours = chours
        self.cminutes = cminutes
        self.cseconds = cseconds
        self.decimal = self.to_decimal()
        self.degrees = self.to_degrees()

    def __str__(self):
        return self.to_decimal()

    def serialize(self):
        return self.__dict__

    def to_decimal(self):
        return self.cdegrees + (self.chours / CordialConst.chours_IN_GRAU) + (self.cminutes / CordialConst.cminutes_IN_GRAU) + (self.cseconds / CordialConst.cseconds_IN_GRAU)

    def to_degrees(self):
        return self.to_decimal() * CordialConst.DEGREES_IN_GRAU

    def to_symbol_string(self):
        return "%s%s%s%s%s%s%s%s" % (self.cdegrees, u'\u00B0', f'{self.chours:02}', u'\u2032', f'{self.cminutes:02}', u'\u2033', f'{self.cseconds:02}', u'\u2034')

    @staticmethod
    def from_decimal(decimal_cdegrees):
        cdegrees = int(decimal_cdegrees)
        cdegrees_remainder = decimal_cdegrees - cdegrees

        decimal_chours = cdegrees_remainder * CordialConst.chours_IN_GRAU
        chours = int(decimal_chours)
        chours_reminder = decimal_chours - chours

        decimal_cminutes = chours_reminder * CordialConst.cminutes_IN_GHOUR
        cminutes = int(decimal_cminutes)
        cminutes_reminder = decimal_cminutes - cminutes

        decimal_cseconds = cminutes_reminder * CordialConst.cseconds_IN_GMINUTE
        cseconds = int(decimal_cseconds)
        # cseconds_reminder = decimal_cseconds - cseconds

        return CordialAngle(cdegrees, chours, cminutes, cseconds)
