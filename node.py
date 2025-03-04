from token_ import TokenType, Token

class IntNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[INT {self.token.value}]"
        )

class FloatNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[FLOAT {self.token.value}]"
        )

class BinOpNode:
    "Binary infix operations"
    def __init__(self, node_l, node_r, op_tok: Token):
        self.node_l = node_l
        self.node_r = node_r
        self.op_tok = op_tok
        self.pos_start = node_l.pos_start
        self.pos_end = node_r.pos_end

    def __repr__(self):
        return f"[{self.node_l} {self.op_tok.ttype.name} {self.node_r}]"

class UnaryOpNode:
    "Unary prefix operations"
    def __init__(self, node, op_tok: Token):
        self.node = node
        self.op_tok = op_tok
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"[{self.op_tok.ttype.name} {self.node}]"
