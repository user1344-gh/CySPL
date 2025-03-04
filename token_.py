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
