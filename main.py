import info
import lexer

print("CySPL (Cy's simplified programming language)")
print(f"Version {info.VER_STRING}")

x = lexer.Lexer("345-3.4")

print(
    x.generate_tokens()
)