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

def transform(ast, namespace):
    from transformer import Transformer

    transformer = Transformer(ast, namespace)
    res = transformer.transform()
    return res.node, res.error

def compile(code, level=1, namespace=None):
    value, error = lex(code)
    if level == 1 or error:
        return value, error
    
    value, error = parse(value)
    if level == 2 or error:
        return value, error
    
    if not namespace:
        raise ValueError("Expected namespaces")
    value, error = transform(value, namespace)
    if level == 3 or error:
        return value, error
    
    raise ValueError(f"Invalid level: {level}")
