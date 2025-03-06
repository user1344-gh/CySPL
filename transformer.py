import t_node as tn
import node as n
from res import Result
from namespace import Namespace
from errors import Error
from types_ import Types as T

class Transformer:
    def __init__(self, ast: n.BlockNode, namespace: Namespace):
        self.ast = ast
        self.nodes = ast.nodes
        self.index = -1
        self.current_node = None
        self.namespace = namespace
        self.advance()

    def advance(self):
        self.index += 1
        if self.index >= len(self.nodes):
            self.current_node = None
            return
        self.current_node = self.nodes[self.index]
    
    def transform(self):
        nodes = []
        res = Result()
        main_func = tn.MainFunc([])
        nodes.append(main_func)
        while self.current_node:
            node = res.register(self.tf_node(self.current_node, self.namespace))
            if res.error:
                return res
            main_func.nodes.append(node)
            self.advance()
        
        return res.success(main_func)

    def tf_node(self, node, ns: Namespace):
        res = Result()
        if type(node) == n.IntNode:
            return res.success(tn.IntNode(node))
        elif type(node) == n.UnsignedIntNode:
            return res.success(tn.UnsignedIntNode(node))
        elif type(node) == n.LongIntNode:
            return res.success(tn.LongIntNode(node))
        elif type(node) == n.UnsignedLongIntNode:
            return res.success(tn.UnsignedLongIntNode(node))
        elif type(node) == n.FloatNode:
            return res.success(tn.FloatNode(node))
        elif type(node) == n.DoubleNode:
            return res.success(tn.DoubleNode(node))
        elif type(node) == n.StringNode:
            return res.success(tn.StringNode(node))
        elif type(node) == n.BinOpNode:
            node_l = res.register(self.tf_node(node.node_l, ns))
            if res.error: return res
            node_r = res.register(self.tf_node(node.node_r, ns))
            if res.error: return res
            tnode = tn.BinOpNode(
                node,
                node_l,
                node_r
            )
            res.register(tnode.typecheck())
            if res.error: return res
            return res.success(tnode)
        elif type(node) == n.UnaryOpNode:
            node_tf = res.register(self.tf_node(node.node, ns))
            if res.error: return res
            tnode = tn.UnaryOpNode(
                node,
                node_tf,
            )
            res.register(tnode.typecheck())
            if res.error: return res
            return res.success(tnode)
        elif type(node) == n.VarDeclareNode:
            if node.value:
                value = res.register(self.tf_node(node.value, ns))
                if res.error: return res
            else:
                value = None
            type_ = node.type.type
            if res.error: return res
            tnode = tn.VarDeclareNode(
                node,
                type_,
                value,
            )
            res.register(tnode.typecheck())
            if res.error: return res

            res.register(ns.declare(
                tnode, tnode.name, tnode.type
            ))
            if res.error: return res
            if value: ns.vars[tnode.name].is_defined = True
            return res.success(tnode)
        elif type(node) == n.VarAssignNode:
            value = res.register(self.tf_node(node.value, ns))
            if res.error: return res
            name = node.name
            if name not in ns.vars:
                return res.failure(Error(
                    "Assignment to undeclared variable",
                    node.pos_start, node.pos_end
                ))
            type_ = ns.vars[name].type
            tnode = tn.VarAssignNode(node, type_, value)
            res.register(tnode.typecheck())
            if res.error: return res
            ns.vars[name].is_defined = True
            return res.success(tnode)
        elif type(node) == n.VarGetNode:
            name = node.name
            get_result = res.register(ns.get(node, name))
            if res.error: return res
            type_ = get_result.type
            return res.success(tn.VarGetNode(node, type_))
        elif type(node) == n.ConstantNode:
            return res.success(tn.ConstantNode(node))
        elif type(node) == n.TypeNode:
            return res.success(tn.TypeNode(node))
        print(node, type(node))
