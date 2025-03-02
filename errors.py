from pos import Position

class Error:
    def __init__(
            self,
            name: str | None = None,
            msg: str = "",
            pos_start: Position | None = None,
            pos_end: Position | None = None,
        ):
        self.pos_start: Position = pos_start
        self.pos_end: Position = pos_end
        self.msg: str = msg
        if name:
            self.name: str = name
        elif hasattr(type(self), "err_name"):
            self.name = type(self).err_name
        else:
            raise ValueError("Missing error name.")
    
    def __repr__(self):
        return (
            f"<{self.name!r} ({self.msg!r}) from {self.pos_start} to {self.pos_end}>"
        )
    
    def __str__(self):
        line = self.pos_start.line
        col = self.pos_start.col
        return (
            f"Line {line}, col {col}\n"
            f"{self.name!r}: {self.msg!r}"
        )

class SyntaxError(Error):
    err_name = "SyntaxError"
