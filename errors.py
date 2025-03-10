from pos import Position

class Error:
    def __init__(
            self,
            msg: str = "",
            pos_start: Position | None = None,
            pos_end: Position | None = None,
        ):
        self.pos_start: Position = pos_start.copy()
        self.pos_end: Position = pos_end.copy()
        self.msg: str = msg
    
    def __repr__(self):
        return (
            f"<ERR({self.msg!r}) from {self.pos_start} to {self.pos_end}>"
        )
    
    def display_err_simple(self):
        line = self.pos_start.line
        col = self.pos_start.col
        return (
            f"Line {line+1}, col {col+1}\n"
            f"{self.msg}"
        )
    
    def display_err(self, code):
        line = self.pos_start.line
        col = self.pos_start.col
        col_end = self.pos_end.col
        lines = code.split("\n")

        if self.pos_end.line != line:
            col_end = len(lines[line]) - 1
        err_length = col_end - col

        return (
            f"Line {line+1}, col {col+1}\n"
            f"{lines[line]}\n"
            f"{" " * col}{"^" * err_length}\n"
            f"{self.msg}"
        )