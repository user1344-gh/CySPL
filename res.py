class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        self.error = error
        return self
    
    def __repr__(self):
        return (
            f"<{type(self.__name__)} Ok{{{self.node}}} Err{{{self.error}}}>"
        )
    
    def __str__(self):
        if self.error:
            return f"[ERR {self.error}]"
        elif self.node:
            return f"[OK {self.node}]"
        return "[EMPTY]"
