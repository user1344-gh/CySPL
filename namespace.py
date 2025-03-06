from res import Result
from errors import Error
import t_node as tn

class Variable:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        self.is_defined = False
    
    def __eq__(self, other):
        if type(other) == Variable:
            return self.name == other.name
        elif type(other) == str:
            return self.name == other
        return NotImplemented
    
    def __hash__(self):
        return hash(f"USERVAR_{self.name}")

class Namespace:
    def __init__(self):
        self.vars: dict[Variable] = {}
    
    def declare(self, expr, name, type_):
        res = Result()
        if name in self.vars:
            return res.failure(Error(
                f"Redeclaration of variable {name}",
                expr.pos_start, expr.pos_end
            ))
        self.vars[name] = Variable(name, type_)
        return res
    
    def get(self, expr, name):
        res = Result()
        if name not in self.vars:
            return res.failure(Error(
                f"Invalid variable {name}",
                expr.pos_start, expr.pos_end
            ))
        elif not self.vars[name].is_defined:
            return res.failure(Error(
                f"Use of undefined variable {name}",
                expr.pos_start, expr.pos_end
            ))
        return res.success(self.vars[name])
    
