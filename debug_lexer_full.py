from src.lexer.lexer import Lexer
import sys

source = 'writln("hola mundo");'
lexer = Lexer(source)
tokens, errors = lexer.tokenize()

print(f"Fonte: {source}")
print(f"Número de tokens: {len(tokens)}")

for i, t in enumerate(tokens):
    print(f"{i}: {t.type.name} -> '{t.lexeme}'")

print("\nErros:")
for e in errors:
    print(e)
