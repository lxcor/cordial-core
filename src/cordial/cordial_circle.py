from cordial import cordial_const as CordialConst


class CordialCircle:
    """Marks an angle that falls exactly on a division of the full circle: a half, third, quarter, sixth, seventh or eighth.

    ``system`` is "cordial" (a circle of 364 grau, which divides by 7 and 13 as well as by 2) or "degree" / "gregorian" (360 degrees,
    which does not divide by 7). Each ``is_*`` attribute holds its name ("Half", "Quarter", ...) when the angle is on that division
    and an empty string when it is not; the table of angles shows them.
    """

    def __init__(self, angle, system="cordial"):
        self.angle = angle
        self.system = system
        self.is_half = self.get_half_label()
        self.is_third = self.get_third_label()
        self.is_quarter = self.get_quarter_label()
        self.is_sixth = self.get_sixth_label()
        self.is_seventh = self.get_seventh_label()
        self.is_eighth = self.get_eighth_label()

    def serialize(self):
        return self.__dict__

    def get_angles_in_circle(self):
        if self.system in ("degree", "gregorian"):
            return CordialConst.DEGREES_IN_CIRCLE
        return CordialConst.cdegrees_IN_CIRCLE

    def get_half_of_circle(self):
        return self.get_angles_in_circle() / 2

    def get_quarter_of_circle(self):
        return self.get_angles_in_circle() / 4

    def get_sixth_of_circle(self):
        return self.get_angles_in_circle() / 6

    def get_eighth_of_circle(self):
        return self.get_angles_in_circle() / 8

    def get_third_of_circle(self):
        return self.get_angles_in_circle() / 3

    def get_seventh_of_circle(self):
        return self.get_angles_in_circle() / 7

    def get_half_label(self):
        if self.angle % self.get_half_of_circle() == 0:
            return "Half"
        return ""

    def get_third_label(self):
        if round(self.angle, 5) % round(self.get_third_of_circle(), 5) == 0:
            return "Third"
        return ""

    def get_quarter_label(self):
        if self.angle % self.get_quarter_of_circle() == 0:
            return "Quarter"
        return ""

    def get_sixth_label(self):
        if round(self.angle, 5) % round(self.get_sixth_of_circle(), 5) == 0:
            return "Sixth"
        return ""

    def get_seventh_label(self):
        if self.angle % self.get_seventh_of_circle() == 0:
            return "Seventh"
        return ""

    def get_eighth_label(self):
        if self.angle % self.get_eighth_of_circle() == 0:
            return "Eighth"
        return ""
