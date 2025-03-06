# CySPL language docs
## Version 0.3

## Keywords
### let
Used to declare a variable\
Syntax:\
`let var_name: var_type`\
`let var_name: var_type = value`
## Constants
### null
A null value.
## Types
### int
A 32 bit signed integer.
### u_int
A 32 bit unsigned integer\
Syntax: `NUMBERu`
### l_int
A 64 bit signed integer\
Syntax: `NUMBERl`
### lu_int
A 64 bit unsigned integer\
Syntax: `NUMBERul`
### float
A single-precision (32bit) floating point value\
Syntax: `NUMBERf` / any number with a decimal point
### double
A double-precision (64bit) floating point value\
Syntax: `NUMBERd`
### str
A string, which is just an array of characters.\
Syntax: `"TEXT"`
## Operators
### Binary +
Syntax: `VAL1 + VAL2`\
Used to add 2 values
### Binary -
Syntax: `VAL1 - VAL2`\
Used to subtract 2 values
### Binary *
Syntax: `VAL1 * VAL2`\
Used to multiply 2 values
### Binary /
Syntax: `VAL1 / VAL2`\
Used to divide 2 values
### =
Syntax: `VAR = VAL`\
Used to assign to a variable
### Unary +
Syntax: `+VAL`\
Raises an error if the value isnt numeric.
### Unary -
Syntax: `-VAL`\
Negates the value
