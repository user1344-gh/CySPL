from res import Result
from token_ import Token, TokenType as TT, KW_DICT, TYPE_KEYWORDS
from operators import Operator as O
import node as n
from errors import Error

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_token: Token = None
        self.advance()
    def advance(self):
        if self.index != len(self.tokens) - 1:
            self.index += 1
        if self.index != len(self.tokens):
            self.current_token = self.tokens[self.index]
        return self.current_token
    def parse(self):
        res = self.statements()
        if self.current_token.ttype != TT.EOF and not res.error:
            return res.failure(Error(
                msg = "Unexpected token",
                pos_start=self.current_token.pos_start,
                pos_end=self.current_token.pos_end
           ))
        return res
    
    def statements(self):
        res = Result()
        statements = []
        
        while 1:
            statement = res.register(self.statement())
            if res.error: return res
            statements.append(statement)
            if self.current_token.ttype != TT.SEMICOLON:
                break
            
            self.advance()

            if self.current_token.ttype == TT.EOF:
                break
        
        return res.success(n.BlockNode(statements))

    def statement(self):
        if self.current_token.ttype in (TT.EOF, TT.SEMICOLON):
            return Result().success(n.ConstantNode.from_token(
                self.current_token, "null"
            ))
        res = self.expr()

        return res
    
    def expr(self):
        return self.bin_op((TT.PLUS, TT.MINUS), (O.ADD, O.SUB), self.term)
    
    def term(self):
        return self.bin_op((TT.ASTERISK, TT.SLASH), (O.MUL, O.DIV), self.factor)
    
    def factor(self):
        return self.unary_op((TT.PLUS, TT.MINUS), (O.POS, O.NEG), self.atom)
    
    def atom(self):
        res = Result()
        token = self.current_token
        ttype = token.ttype
        
        if ttype == TT.INT:
            self.advance()
            return res.success(n.IntNode(token))
        elif ttype == TT.FLOAT:
            self.advance()
            return res.success(n.FloatNode(token))
        elif ttype == TT.U_INT:
            self.advance()
            return res.success(n.UnsignedIntNode(token))
        elif ttype == TT.L_INT:
            self.advance()
            return res.success(n.LongIntNode(token))
        elif ttype == TT.LU_INT:
            self.advance()
            return res.success(n.UnsignedLongIntNode(token))
        elif ttype == TT.DOUBLE:
            self.advance()
            return res.success(n.DoubleNode(token))
        elif ttype == TT.STRING:
            self.advance()
            return res.success(n.StringNode(token))
        elif ttype == TT.EOF:
            return res.failure(Error(
                "Unexpected EOF", token.pos_start-1, token.pos_end
            ))
        elif token.matches(TT.KEYWORD, KW_DICT["declare_var"]):
            pos_start = self.current_token.pos_start.copy()
            self.advance()
            if self.current_token.ttype != TT.IDENTIFIER:
                return res.failure(Error(
                    "Expected identifier",
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                ))
            var_name = self.current_token.value
            self.advance()
            if self.current_token.ttype != TT.COLON:
                return res.failure(Error(
                    "Expected ':'",
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                ))
            self.advance()
            if not self.current_token.matches(TT.KEYWORD, TYPE_KEYWORDS):
                return res.failure(Error(
                    "Expected a type",
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                ))
            var_type = n.TypeNode(self.current_token)
            self.advance()
            if self.current_token.ttype != TT.EQUALS:
                return res.success(n.VarDeclareNode(
                    var_name, var_type, pos_start, var_type.pos_end,
                    None 
                ))
            self.advance()
            value = res.register(self.expr())
            if res.error: return res
            return res.success(n.VarDeclareNode(
                var_name, var_type, pos_start, value.pos_end,
                value 
            ))
        elif token.matches(TT.KEYWORD, KW_DICT["null"]):
            self.advance()
            return res.success(n.ConstantNode(token))
        elif token.matches(TT.KEYWORD, TYPE_KEYWORDS):
            self.advance()
            return res.success(n.TypeNode(token))
        elif token.ttype == TT.IDENTIFIER:
            name_tok = self.current_token
            self.advance()
            if self.current_token.ttype != TT.EQUALS:
                return res.success(n.VarGetNode(name_tok))
            self.advance()
            value = res.register(self.expr())
            if res.error: return res
            self.advance()
            return res.success(n.VarAssignNode(
                name_tok, value
            ))
        elif ttype == TT.SEMICOLON:
            return res.failure(Error(
                "Unexpected semicolon", token.pos_start, token.pos_end
            ))
    
    def bin_op(self, ops: list, crs_ops, func_l, func_r=None):
        if not func_r: func_r = func_l

        res = Result()
        
        left = res.register(func_l())
        if res.error: return res

        while (
            self.current_token.ttype in ops
        ):
            op_tok = self.current_token
            index = ops.index(op_tok.ttype)
            self.advance()
            right = res.register(func_r())
                        
            if res.error: return res
            left = n.BinOpNode(left, right, crs_ops[index])
        
        return res.success(left)
    
    def unary_op(self, ops, crs_ops, func):
        res = Result()

        if (
            self.current_token.ttype in ops or
            (self.current_token.ttype, self.current_token.value) in ops
        ):
            op_tok = self.current_token
            
            index = ops.index(op_tok.ttype)
            self.advance()
            node = res.register(
                self.unary_op(ops, crs_ops, func)
            )
            if res.error: return res
            node = n.UnaryOpNode(node, crs_ops[index], op_tok.pos_start)
            return res.success(node)
        
        return func()
    