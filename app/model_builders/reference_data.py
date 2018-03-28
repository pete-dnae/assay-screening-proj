xxxx = """V ver-1
P Plate1
A Titanium-Taq              1-12  A-H 0.02 M/uL
A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x
A (Eco)-ATCC-BAA-9999       2     C,D 1.16 x
# This is a comment
P Plate42
T Plate1 1 B                1-12  A-H   20 dilution
"""

"""
The data in this module forms our *reference* experiment, and is intended to
provide a conveniently centralised data set to support unit tests, and
initialising a virgin database.
"""

"""
The assignmento REFERENCE_SCRIPT is constructed this wierd way so that there
are exactly 10 characters in the source code before the first character of the
script. Makes it easier to correlate the information from a ParseError(s) about
which character position within the script the problem lies at.
"""
REFERENCE_SCRIPT = xxxx

REFERENCE_REAGENTS_DATA = (
            ('Titanium-Taq', 'Buffer Ingredient'),
            ('(Eco)-ATCC-BAA-2355', 'Strain'),
            ('(Eco)-ATCC-BAA-9999', 'Strain'),
            ('Ec_uidA_6.x_Eco63_Eco60', 'Primer'),
            ('Efs_cpn60_1.x_Efs04_Efs01', 'Primer'),
            ('Efs_vanB_1.x_van10_van06', 'Primer'),
)

REFERENCE_GROUP = {
    'name': 'Pool_1',
    'members': (
        ('Efs_cpn60_1.x_Efs04_Efs01', 0.4, 'uM'),
        ('Efs_vanB_1.x_van10_van06', 0.4, 'uM'),
    )
}

REFERENCE_REAGENT_NAMES = [name for name, category in REFERENCE_REAGENTS_DATA]

REFERENCE_UNITS = ('M/uL', 'x', 'uM', 'dilution')
