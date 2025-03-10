from pos import Position
from errors import Error
from token_ import Token, TokenType, KEYWORDS
from string import ascii_letters as letters
digits = "1234567890"
alphanumerics = letters + digits

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
        pos = self.pos.copy()
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
            elif self.current_char in (digits + "."):
                res = self.gen_number()
                if res[1]: return res
                tokens.append(res[0])
            elif self.current_char == '"':
                res = self.gen_string()
                if res[1]: return res
                tokens.append(res[0])
            elif self.current_char == ";":
                tokens.append(Token(
                    TokenType.SEMICOLON, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char == "=":
                tokens.append(Token(
                    TokenType.EQUALS, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(
                    TokenType.COLON, None, self.pos, self.next_pos()
                ))
                self.advance()
            elif self.current_char in letters + "_":
                tokens.append(self.gen_ident())
            else:
                return (None, Error(
                    msg=f"Invalid character: '{self.current_char}'",
                    pos_start=self.pos,
                    pos_end=self.next_pos()
                ))
        tokens.append(Token(TokenType.EOF, None, self.pos, self.pos))
        return (tokens, None)
    
    def gen_number(self) -> tuple[str, str]:
        number_str = ""
        decimal_point = False
        token_type = TokenType.INT
        pos_start = self.pos.copy()

        while 1:
            if not self.current_char in (digits + "."): break
            if self.current_char == ".":
                if decimal_point:
                    return (None, Error(
                        msg="Unexpected decimal point",
                        pos_start=self.pos,
                        pos_end=self.next_pos()
                    ))
                decimal_point = True
                token_type = TokenType.FLOAT
            number_str += self.current_char
            self.advance()
        if self.current_char == "u":
            if decimal_point:
                return (None, Error(
                    msg="Unsigned mofidifier added to float value.",
                    pos_start=self.pos,
                    pos_end=self.next_pos()
                ))
            token_type = TokenType.U_INT
            self.advance()
        elif self.current_char == "f":
            token_type = TokenType.FLOAT
            self.advance()
        elif self.current_char == "l":
            if decimal_point:
                return (None, Error(
                    msg="Long mofidifier added to float value.",
                    pos_start=self.pos,
                    pos_end=self.next_pos()
                ))
            self.advance()
            if self.current_char == "u":
                token_type = TokenType.LU_INT
            else:
                token_type = TokenType.L_INT
            self.advance()
        elif self.current_char == "d":
            token_type = TokenType.DOUBLE
            self.advance()
        
        return (Token(token_type, number_str, pos_start, self.pos),None)

    def gen_string(self):
        import codecs
        pos_start = self.pos.copy()
        escape_chars = {
            "n": "\\n",
            "t": "\\t",
        }
        self.advance()
        string = ""
        while self.current_char != "\"":
            if self.current_char == "\x1a":
                return None, Error(
                    "Expected '\"'", pos_start, self.pos
                )
            elif self.current_char == "\\":
                self.advance()
                if self.current_char == "\"":
                    string += '\\"'
                else:
                    string += "\\" + self.current_char
            else:
                string += self.current_char
            self.advance()
        self.advance()
        return (Token(TokenType.STR, string, pos_start, self.pos), None)

    def gen_ident(self):
        ident_str = ""
        token_type = TokenType.IDENTIFIER
        pos_start = self.pos.copy()

        while self.current_char in alphanumerics + "_":
            ident_str += self.current_char
            self.advance()
        if ident_str in KEYWORDS:
            token_type = TokenType.KEYWORD
        
        return Token(token_type, ident_str, pos_start, self.pos)
