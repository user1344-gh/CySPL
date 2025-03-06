import node as n
from types_ import Types as T
from res import Result
from errors import Error

class IntNode:
    def __init__(self, node: n.IntNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}i32)"
        )
    
    def return_type(self):
        return T.INT
    
    def typecheck(self):
        return Result()

class FloatNode:
    def __init__(self, node: n.FloatNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}f32)"
        )
    
    def return_type(self):
        return T.FLOAT
    
    def typecheck(self):
        return Result()

class UnsignedIntNode:
    def __init__(self, node: n.UnsignedIntNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}u32)"
        )    
    
    def return_type(self):
        return T.U_INT
    
    def typecheck(self):
        return Result()

class LongIntNode:
    def __init__(self, node: n.LongIntNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}i64)"
        )
    
    def return_type(self):
        return T.L_INT
    
    def typecheck(self):
        return Result()

class UnsignedLongIntNode:
    def __init__(self, node: n.UnsignedLongIntNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}u64)"
        )
    
    def return_type(self):
        return T.LU_INT
    
    def typecheck(self):
        return Result()

class DoubleNode:
    def __init__(self, node: n.DoubleNode):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"({self.value}f64)"
        )
        
    def return_type(self):
        return T.DOUBLE
    
    def typecheck(self):
        return Result()


class BinOpNode:
    "Binary infix operations"
    def __init__(self, node: n.BinOpNode, node_l, node_r):
        self.node_l = node_l
        self.node_r = node_r
        self.op = node.operator
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.node_l} {self.op.name} {self.node_r})"
    
    def return_type(self):
        return self.node_l.return_type()
    
    def typecheck(self):
        res = Result()
        if self.node_l.return_type() != self.node_r.return_type():
            return res.failure(Error(
                f"Type mismatch ({self.node_l.return_type().name} "
                f"and {self.node_r.return_type().name})",
                self.pos_start, self.pos_end
            ))
        elif self.node_l.return_type() in (
            T.DOUBLE, T.FLOAT, T.INT, T.L_INT, T.LU_INT, T.U_INT
        ):
            return res
        return res.failure(Error(
                f"Operation not supported for type "
                f"({self.node_l.return_type().name})",
                self.pos_start, self.pos_end
            ))

class UnaryOpNode:
    "Unary prefix operations"
    def __init__(self, node: n.UnaryOpNode, operand):
        self.node = node.node
        self.operand = operand
        self.op = node.operator
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.op.name} {self.operand})"
    
    def return_type(self):
        return self.operand.return_type()
    
    def typecheck(self):
        res = Result()
        if self.operand.return_type() in (
            T.DOUBLE, T.FLOAT, T.INT, T.L_INT, T.LU_INT, T.U_INT
        ):
            return res
        return res.failure(Error(
                f"Operation not supported for type "
                f"({self.operand.return_type().name})",
                self.pos_start, self.pos_end
            ))

class StringNode:
    def __init__(self, node):
        self.value = node.token.value
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return (
            f"(\"{self.value}\")"
        )
    
    def return_type(self):
        return T.STR
    
    def typecheck(self):
        return Result()

class MainFunc:
    def __init__(self, nodes):
        self.nodes = nodes
        self.update_pos()
    
    def __repr__(self):
        return (
            f"[FUNC_MAIN {{{";".join([str(i) for i in self.nodes])}}}]"
        )
    
    def update_pos(self):
        if self.nodes:
            self.pos_start = self.nodes[0].pos_start
            self.pos_end = self.nodes[-1].pos_end
        else:
            from pos import Position
            self.pos_start = Position(0, 0, 0)
            self.pos_end = Position(0, 0, 0)
    
    def return_type(self):
        return T.NULL
    
    def typecheck(self):
        return Result()

class ConstantNode:
    def __init__(self, node: n.ConstantNode):
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

        match node.value:
            case "null":
                self.value = "null"
    
    def __repr__(self):
        return f"({self.value})"
    
    def return_type(self):
        match self.value:
            case "null":
                return T.NULL

    
    def typecheck(self):
        return Result()
    
class VarDeclareNode:
    def __init__(self, node: n.VarDeclareNode, type_, value=None):
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
        self.name = node.name
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return (
            f"(let {self.name}: {self.type.name}" +
            (f" = {self.value})" if self.value else ")")
        )
    
    def return_type(self):
        return T.NULL
    
    def typecheck(self):
        res = Result()
        if self.value is None: return res

        if self.value.return_type() != self.type:
            return res.failure(Error(
                f"Expected {self.type.name}, got {self.value.return_type().name}",
                self.value.pos_start, self.value.pos_end
            ))
        
        return res

class VarAssignNode:
    def __init__(self, node: n.VarAssignNode, type_, value):
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
        self.name = node.name
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return (
            f"({self.name} = {self.value})"
        )
    
    def return_type(self):
        return self.type
    
    def typecheck(self):
        res = Result()

        if self.value.return_type() != self.type:
            return res.failure(Error(
                f"Expected {self.type.name}, got {self.value.return_type().name}",
                self.value.pos_start, self.value.pos_end
            ))
        
        return res

class VarGetNode:
    def __init__(self, node: n.VarGetNode, type_):
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
        self.name = node.name
        self.type = type_
    
    def __repr__(self):
        return (
            f"({self.name})"
        )
    
    def return_type(self):
        return self.type
    
    def typecheck(self):
        return Result()

class TypeNode:
    def __init__(self, node):
        self.pos_start = node.pos_start
        self.pos_end = node.pos_end
        self.type = node.type
    
    def __repr__(self):
        return (
            f"({self.type.name})"
        )
    
    def return_type(self):
        return T.TYPE

    
    def typecheck(self):
        return Result()

