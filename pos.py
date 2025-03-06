class Position:
    def __init__(self, line: int, col: int, index: int):
        self.line = line
        self.col = col
        self.index = index
    def __repr__(self):
        return f"(line: {self.line}, col: {self.col}, index: {self.index})"
    def __str__(self):
        return f"({self.index}: {self.line}, {self.col})"
    def __add__(self, other: int):
        clone = self.copy()
        clone.index += other
        clone.col += other
        return clone
    def __sub__(self, other: int):
        return (self + -other)
    def copy(self):
        from copy import copy
        return copy(self)
