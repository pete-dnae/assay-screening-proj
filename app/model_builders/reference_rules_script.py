xxxx = """V ver-1
P Plate1
A Titanium-Taq              1-12  A-H 0.02 M/uL
A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x
A (Eco)-ATCC-BAA-9999       2     C,D 1.16 x
# This is a comment
P Plate42
T Plate1 1 B                1-12  A-H   20 dilution
"""

REFERENCE_SCRIPT = xxxx

"""
Constructed this wierd way so that there are exactly 10 characters in the 
source code before the first character of the script. Makes it easier to
correlate the information from a ParseError(s) about which character position
within the script the problem lies at.
"""
