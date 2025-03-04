from pos import Position
import errors as err
from token_ import Token, TokenType

class Lexer:
    def __init__(self, code):
        self.pos = Position(0, -1, -1)
        self.current_char: str = None
        self.chars = code + "\x1A"
        self.advance()

    def advance(self):
        self.pos.index += 1
        if self.pos.index < len(self.chars):
            self.current_char = self.chars[self.pos.index]
        else:
            self.current_char = None
        if self.current_char == '\n':
            self.pos.line += 1
            self.pos.col = 0
        else:
            self.pos.col += 1
        return self.current_char
    
    def next_pos(self):
        from copy import copy
        pos = copy(self.pos)
        pos.index+=1
        if self.chars[pos.index] == '\n':
            pos.line += 1
            pos.col = 0
        else:
            pos.col += 1
        
        return pos

    def generate_tokens(self) -> tuple[str, str]:
        tokens = []
        while self.current_char and self.current_char != "\x1a":
            if self.current_char in " \t\n":
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(
                    TokenType.PLUS, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(
                    TokenType.MINUS, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(
                    TokenType.ASTERISK, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(
                    TokenType.SLASH, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char in "1234567890.":
                res = self.gen_number()
                if res[1]: return res
                tokens.append(res[0])
            else:
                return (None, err.SyntaxError(
                    msg=f"Invalid character: '{self.current_char}'",
                    pos_start=self.pos,
                    pos_end=self.next_pos()
                ))
        tokens.append(Token(TokenType.EOF, None, self.pos, self.pos))
        return (tokens, None)
    
    def gen_number(self) -> tuple[str, str]:
        number_str = ""
        decimal_point = False
        pos_start = self.pos

        while 1:
            if not self.current_char in "1234567890.": break
            if self.current_char == ".":
                if decimal_point:
                    return (None, err.SyntaxError(
                        msg="Unexpected decimal point",
                        pos_start=self.pos,
                        pos_end=self.next_pos()
                    ))
                decimal_point = True
            number_str += self.current_char
            self.advance()
        token_type = TokenType.FLOAT if decimal_point else TokenType.INT
        val_type = float if decimal_point else int
        return (Token(token_type, val_type(number_str), pos_start, self.pos),None)
