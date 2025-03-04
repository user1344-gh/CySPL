def lex(code):
    from lexer import Lexer

    lexer = Lexer(code)
    res = lexer.generate_tokens()
    return res

def parse(tokens):
    from parser import Parser

    parser = Parser(tokens)
    res = parser.parse()
    return res.node, res.error

def run(code, level=1):
    value, error = lex(code)
    if level == 1 or error:
        return value, error
    
    value, error = parse(value)
    if level == 2 or error:
        return value, error
    
    raise ValueError(f"Invalid level: {level}")
