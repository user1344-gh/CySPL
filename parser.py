from res import ParseResult
from token_ import Token, TokenType as TT
import node as n
import errors as e

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_token: Token = None
        self.advance()
    def advance(self):
        self.index += 1
        if self.index == len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]
        return self.current_token
    def parse(self):
        res = self.expr()
        if self.current_token.ttype != TT.EOF:
            return res.failure(e.SyntaxError(
                msg = "Unexpected token",
                pos_start=self.current_token.pos_start,
                pos_end=self.current_token.pos_end
           ))
        return res
    
    def expr(self):
        return self.bin_op((TT.PLUS, TT.MINUS), self.term)
    
    def term(self):
        return self.bin_op((TT.ASTERISK, TT.SLASH), self.factor)
    
    def factor(self):
        return self.unary_op((TT.PLUS, TT.MINUS), self.atom)
    
    def atom(self):
        res = ParseResult()
        token = self.current_token
        ttype = token.ttype
        
        if ttype == TT.INT:
            self.advance()
            return res.success(n.IntNode(token))
        elif ttype == TT.FLOAT:
            self.advance()
            return res.success(n.FloatNode(token))
        elif ttype == TT.EOF:
            return res
        
        return res.failure(e.SyntaxError(
            msg = "Unexpected token",
            pos_start=token.pos_start,
            pos_end=token.pos_end
        ))
    
    def bin_op(self, ops, func_l, func_r=None):
        if not func_r: func_r = func_l
        res = ParseResult()
        
        left = res.register(func_l())
        if res.error: return res

        while (
            self.current_token.ttype in ops or
            (self.current_token.ttype, self.current_token.value) in ops
        ):
            op_tok = self.current_token
            self.advance()
            right = res.register(func_r())
            if res.error: return res
            left = n.BinOpNode(left, right, op_tok)
        
        return res.success(left)
    
    def unary_op(self, ops, func):
        res = ParseResult()

        if (
            self.current_token.ttype in ops or
            (self.current_token.ttype, self.current_token.value) in ops
        ):
            op_tok = self.current_token
            self.advance()
            node = res.register(
                self.unary_op(ops, func)
            )
            if res.error: return res
            node = n.UnaryOpNode(node, op_tok)
            return res.success(node)
        
        return func()
    