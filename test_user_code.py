from src.lexer.lexer import Lexer

source = 'writln("hola mundo");'
lexer = Lexer(source)
tokens, errors = lexer.tokenize()

print(f"DEBUG: Processando código: {source}")
print(f"DEBUG: Total de tokens encontrados: {len(tokens)}")

print("\nANÁLISE LÉXICA:")
for t in tokens:
    print(f"[{t.type.name}] Lexema: '{t.lexeme}' (Ln {t.line}, Col {t.column})")

if errors:
    print("\nRELATÓRIO DE ERROS:")
    for e in errors:
        print(f"- {e['message']} (Lexema: '{e['token']}')")
        if e['suggestion']:
            print(f"  💡 Sugestão: {e['suggestion']}")
