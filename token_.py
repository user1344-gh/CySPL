import pos
from enum import Enum

class TokenType(Enum):
    EOF        = 0
    INT        = 1
    U_INT      = 2
    FLOAT      = 3
    PLUS       = 4
    MINUS      = 5
    ASTERISK   = 6
    SLASH      = 7
    STRING     = 8
    L_INT      = 9
    LU_INT     = 10
    DOUBLE     = 11
    SEMICOLON  = 12
    KEYWORD    = 13
    IDENTIFIER = 14
    EQUALS     = 15
    COLON      = 16

KW_DICT = {
    "null": "null",
    "declare_var": "let",
    "int_type": "int",
    "u_int_type": "u_int",
    "l_int_type": "l_int",
    "lu_int_type": "lu_int",
    "float_type": "float",
    "string_type": "str",
    "double_type": "double",
}
KEYWORDS = [*(KW_DICT.values())]
TYPE_KEYWORDS = [
    KW_DICT["int_type"], KW_DICT["u_int_type"], KW_DICT["l_int_type"], 
    KW_DICT["lu_int_type"], KW_DICT["float_type"], KW_DICT["string_type"], 
    KW_DICT["double_type"], 
]

class Token:
    def __init__(self, ttype, value, pos_start, pos_end):
        self.ttype: TokenType = ttype
        self.pos_start: pos.Position = pos_start.copy()
        self.pos_end: pos.Position = pos_end.copy()
        self.value = value
    def __repr__(self):
        if self.value is None:
            return f"[{self.ttype.name}]"
        return f"[{self.ttype.name}:{self.value!r}]"
    def matches(self, ttype, value):
        if type(value) in (list, tuple):
            return self.ttype == ttype and self.value in value
        return self.ttype == ttype and self.value == value
