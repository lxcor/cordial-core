from cordial import cordial_const as CordialConst


class CordialAngleAdapter:
    """A Gregorian angle (degrees, arcminutes, arcseconds) that converts to its Cordial counterpart (CordialAngle) and back.

    360 degrees and 364 grau are the same full turn, so the factor is 364/360 each way."""

    def __init__(self, degrees, arcminutes=0, arcseconds=0):
        self.degrees = degrees
        self.arcminutes = arcminutes
        self.arcseconds = arcseconds
        self.decimal = self.to_decimal()
        self.cdegrees = self.to_cordial()

    def __str__(self):
        return self.to_decimal()

    def serialize(self):
        return self.__dict__

    def to_decimal(self):
        return self.degrees + (self.arcminutes / CordialConst.ARCMINUTES_IN_DEGREE) + (self.arcseconds / CordialConst.ARCSECONDS_IN_DEGREE)

    def to_cordial(self):
        return self.to_decimal() * CordialConst.cdegrees_IN_DEGREE

    @staticmethod
    def from_decimal(decimal_degree):
        degree = int(decimal_degree)
        degree_reminder = decimal_degree - degree

        decimal_arcminutes = degree_reminder * CordialConst.ARCMINUTES_IN_DEGREE
        arcminutes = int(decimal_arcminutes)
        arcminutes_reminder = decimal_arcminutes - arcminutes

        decimal_arcseconds = arcminutes_reminder * CordialConst.ARCSECONDS_IN_DEGREE
        arcseconds = int(decimal_arcseconds)
        # arcseconds_reminder = decimal_arcseconds - arcseconds

        return CordialAngleAdapter(degree, arcminutes, arcseconds)
