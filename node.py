from token_ import TokenType, Token
from types_ import Types as T

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

class UnsignedIntNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[U_INT {self.token.value}]"
        )
class LongIntNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[L_INT {self.token.value}]"
        )

class UnsignedLongIntNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[LU_INT {self.token.value}]"
        )

class DoubleNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[DOUBLE {self.token.value}]"
        )


class BinOpNode:
    "Binary infix operations"
    def __init__(self, node_l, node_r, operator):
        self.node_l = node_l
        self.node_r = node_r
        self.operator = operator
        self.pos_start = node_l.pos_start
        self.pos_end = node_r.pos_end

    def __repr__(self):
        return f"[{self.node_l} {self.operator.name} {self.node_r}]"

class UnaryOpNode:
    "Unary prefix operations"
    def __init__(self, node, operator, pos_start):
        self.node = node
        self.operator = operator
        self.pos_start = pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"[{self.operator.name} {self.node}]"

class StringNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return (
            f"[STRING {self.token.value}]"
        )

class BlockNode:
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.pos_start = nodes[0].pos_start
        self.pos_end = nodes[-1].pos_end
    
    def __repr__(self):
        return (
            f"{{{";".join([str(i) for i in self.nodes])}}}"
        )

class ConstantNode:
    def __init__(self, token: Token):
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
        self.value = token.value
    
    def __repr__(self):
        return f"[{self.value}]"
    
    @classmethod
    def from_token(cls, token: Token, value):
        instance = object.__new__(cls)
        instance.pos_start = token.pos_start
        instance.pos_end = token.pos_end
        instance.value = value
        return instance

class VarDeclareNode:
    def __init__(self, name, type_, pos_start, pos_end, value=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return (
            f"[DECLARE {self.name}: {self.type.value}" +
            (f" = {self.value}]" if self.value else "]")
        )

class VarAssignNode:
    def __init__(self, name_tok, value):
        self.pos_start = name_tok.pos_start
        self.pos_end = value.pos_end
        self.name = name_tok.value
        self.value = value
    
    def __repr__(self):
        return (
            f"[SET {self.name} {self.value}]"
        )

class VarGetNode:
    def __init__(self, name_tok):
        self.pos_start = name_tok.pos_start
        self.pos_end = name_tok.pos_end
        self.name = name_tok.value
    
    def __repr__(self):
        return (
            f"[GET {self.name}]"
        )

class TypeNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
        match token.value:
            case "int":
                self.type = T.INT
            case "u_int":
                self.type = T.U_INT
            case "l_int":
                self.type = T.L_INT
            case "lu_int":
                self.type = T.LU_INT
            case "float":
                self.type = T.FLOAT
            case "double":
                self.type = T.DOUBLE
            case "str":
                self.type = T.STR
    
    def __repr__(self):
        return (
            f"[TYPE {self.type.name}]"
        )
