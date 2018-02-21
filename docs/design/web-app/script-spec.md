# Script Language Specification


## Example Fragment

    Language Version 1

    P1

      A Titanium-Taq            1-12  A-H 0.02 x
      A (Eco)-ATCC-BAA-2355     1,5,9 A-H 2.00E+04 copies/ul
      A HgDna                   1-8   G-H 50 ng/foo
      A Ec_uidA_6.x_Eco63_Eco60 5-8   A-H 0.4 uM/bar

    # I am a comment
    P2

      T P1                      1,5,9 A-H 0.02 dilution
      A Ec_uidA_x.2_Eco64_Eco66 1,5,9 A-H 2.00E+04 copies/ul

    P3

      A Titanium-Taq            1-12  A-H 0.02 x
      etc...

## Approach
We will define this language in terms of how programs **WILL** parse it.
That will imply the language specification, but serve also to support the
parser implementation(s).

## Parsing

The input text will split into lines delimitted by either Windows and Linux line
end characters.

Lines will be processed in the order they appear in the input.

Lines comprising only whitespace are ignored.

Lines in which the first non-whitespace character is '#' are ignored.

The following parsing process applies to lines that get this far.

Leading and trailing whitespace is removed.

The parser holds a state <version_known>, initialised to False.

It is an error if the version is unknown, and the line does not look like 
this: 

    Language Version N

It is an error if the extraction version number is not the same as the version
for which the parser implementation has been coded.

The extracted version number is used to set the <version_known> state.

The parser holds a <current plate number> state. This is initialised to
undefined.

When a line is encountered that matches this regex '^P\d+$', it shall be
interpreted as a mandate to update the current plate number to the extracted
integer. (A plate field). It is an error if the plate number has been 
encountered before.

All remaining lines will be interpreted as follows.

It is an error if <current plate number> is undefined.

Fields are extracted by splitting the line on whitespace.

The processing that follows attempts to harvest 6 fields in sequence.

Each of the fields have different parsing criteria as follows.

Field[0] must be 'A' or 'T'.

Field[1] (when field[0] is 'A'), must match exactly one of the *name* strings 
provided to the parser at construction time.

Field[1] (when field[0] is 'T'), must match exactly one of the previously
encountered plate fields.

Field[2] must be of the form of one of the following examples:
- 3
- 3-12
- 1,2,3

Field[3] must be of the form of one of the following examples:
- A
- C-F
- A,B,C

Field[4] (if it contains one 'e'), must parse (in its entirety) as a 
positive scientific notation float.

Field[4] (otherwise) must parse (in its entirety) as a positive floating point 
number or integer).

Field[5] must match exactly one of the *units* strings provided to the
parser at construction time.

It is an error if there are more than 6 fields.
