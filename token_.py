import pos
from enum import Enum

class TokenType(Enum):
    INT      = 1
    FLOAT    = 2
    PLUS     = 3
    MINUS    = 4
    ASTERISK = 5
    SLASH    = 6

class Token:
    def __init__(self, ttype, value, pos_start, pos_end):
        self.ttype: TokenType = ttype
        self.pos_start: pos.Position = pos_start 
        self.pos_end: pos.Position = pos_end
        self.value = value
    def __repr__(self):
        if self.value is None:
            return f"[{self.ttype.name}]"
        return f"[{self.ttype.name}:{self.value}]"
