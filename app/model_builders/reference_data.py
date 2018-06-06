xxxx = """V ver-1
P Plate1
A Titanium-Taq              1-12  A-H 0.02 M/uL
A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x
A (Eco)-ATCC-BAA-9999       2     C,D 1.16 x
C 10@95,12@60,15@65                   5    x
C 7@60,10@65,10@95                    5    x
# This is a comment
P Plate42
T Plate1 1 B                1-12  A-H   20 dilution
A Pool_1                    1-3   A-H    1 x
A Ec_uidA_6.x_Eco63_Eco60   4-9   A-H  0.4 uM
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
            ('Titanium-Taq', 'Buffer Ingredient',None),
            ('(Eco)-ATCC-BAA-2355', 'Strain',None),
            ('(Eco)-ATCC-BAA-9999', 'Strain',None),
            ('Ec_uidA_6.x_Eco63_Eco60', 'Primer',None),
            ('Efs_cpn60_1.x_Efs04_Efs01', 'Primer',None),
            ('Efs_vanB_1.x_van10_van06', 'Primer',None),
)

REFERENCE_GROUP = {
    'name': 'Pool_1',
    'members': (
        ('Efs_cpn60_1.x_Efs04_Efs01', 0.4, 'uM'),
        ('Efs_vanB_1.x_van10_van06', 0.4, 'uM'),
    )
}

REFERENCE_REAGENT_NAMES = [name for name, category,opaque_payload in
                           REFERENCE_REAGENTS_DATA]
REFERENCE_GROUP_NAMES = [REFERENCE_GROUP['name']]
REFERENCE_ALLOWED_NAMES = REFERENCE_REAGENT_NAMES + REFERENCE_GROUP_NAMES

REFERENCE_UNITS = ('M/uL', 'x', 'uM', 'dilution')
