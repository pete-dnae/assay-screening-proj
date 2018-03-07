# Script Language Specification


## Minimum Complete Example Fragment

V 1

P 1

A Titanium-Taq            1-12  A-H 0.02 x
A (Eco)-ATCC-BAA-2355     1,5,9 A-H 2.00E+04 copies/ul
A HgDna                   1-8   G-H 50 ng/foo
A Ec_uidA_6.x_Eco63_Eco60 5-8   A-H 0.4 uM/bar

# I am a comment

P 2

T P 1                     1,5,9 A-H 0.02 dilution
A Ec_uidA_x.2_Eco64_Eco66 1,5,9 A-H 2.00E+04 copies/ul

P 3

A Titanium-Taq            1-12  A-H 0.02 x
etc...

## Parsing Specification

Each parser implementation is obliged to implement this particular sequence of
evaluation. We use this to define the script language.

The input text will split into lines delimitted by either Windows and Linux line
end characters.

Lines will be processed in the order they appear in the input.

Lines comprising only whitespace, or which start with a hash '#' are ignored.

The following parsing process applies to lines that get this far.

Fields are extracted by splitting the line on whitespace.

It is an error if the first extracted field is not one of 
'A', 'T', 'P', or 'V'. In which case the remainder of the fields/line is 
ignored.

Now we have distinct parsing specifications for the fields that remain
depending on what the first field was, as follows:

## *A* - i.e. Allocation Rule

Example

    A Titanium-Taq            1-12  A-H 0.02 x

It is an error if field 1 does not match exactly one of the *name* strings 
provided to the parser at construction time.

The implementation can split this into two mutually exclusive errors if it
wishes.  (Note1)

1. Not recognized as the start of a known name.
2. Recognized as the start of a known name - with <n> completion possibilities.

It is an error if field[2] is not in one of these 3 forms:
- 3
- 3-12
- 1,2,3

It is an error if field[3] is not in one of these 3 forms:
- A
- C-F
- A,B,C

It is an error if field 4 does not conform to one of the following forms.
1. 3
2. 3.16
3. 3.16e-12

It is likely not sufficient to use native numeric value parsing because most 
implementations will tolerate ignored trailing input (e.g. '3.16a' will often
parse as a number - having ignored the trailing 'a'.

It is an error if field[5] does not match exactly one of the *units* 
strings provided to the parser at construction time.
(The implementation can choose to split this into two sub-errors as per Note1).

It is an error if there are more than 6 fields.
Note that this is evaluated last (by design) to provide useful feedback about
the earlier part of the lines.

## *T* - i.e. Transfer Rule

Example

    T P1                     1,5,9 A-H 0.02 dilution

It is an error if field[1] is not the letter 'P' concatenated with an integer.



The parsing of the remaining fields is identical to that for 'A' rules - and
the code should be resused to ensure consistency.

## *'P'* - i.e. Plate statements

E.g.
    P 1

It is an error if field[1] is not an integer.

It is an error if additional fields are present.

## *'V'* - i.e. Version statements

E.g.
    V 1

It is an error if field[1] cannot be parsed as a number.

It is an error if the extracted number does not match the hard-coded version
of the parser's source code.

## Stateful Parsing

Note that none of the previous parsing dependend on the parser holding any
state. Some state-dependent checking is however necessary as follows.
It is left to the implementation to decide how to organise this stateful
checking.

It is an error if the first (non-blank / non-comment) line is not a version 
line.

### Version
It is an error if more than one version line is encountered.

### Plates

It is an error if a plate statement cites a plate number that is the
 most recently encountered plate number.

It is an error if a plate statement cites a plate number that does not
match one of the previously
encountered plate numbers. (See parsing rules for 'P').

It is an error if a plate line introduces a plate number that has been used by
a previous plate line.

It is an error for an *A* or *T* rule to be encountered before any plate line
has been encountered..
