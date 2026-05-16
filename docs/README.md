# mini-pascal-lexer

Este projecto é um analisador léxico (lexer) para uma versão reduzida de Pascal, com suporte adicional para sugestões de correção usando IA.

## O que o projeto faz

- Analisa código-fonte escrito em uma sintaxe simplificada de Pascal.
- Converte o texto em uma sequência de tokens léxicos.
- Identifica palavras reservadas, identificadores, constantes inteiras e constantes de caractere.
- Reconhece operadores aritméticos, relacionais e lógicos.
- Reconhece delimitadores e símbolos especiais como `:=`, `;`, `:`, `,`, `(`, `)`, `[`, `]`, `..`, `.`
- Trata espaços em branco e novas linhas, mantendo a numeração de linha e coluna para erros.
- Coleta erros léxicos com mensagem, linha e coluna para facilitar depuração.
- Integra sugestões de correção de tokens usando um modelo de IA (via OpenAI) em `src/lexer/ai_suggestions.py`.

## Tokens suportados

O lexer suporta os seguintes tipos de tokens:

- Palavras reservadas: `program`, `var`, `array`, `of`, `begin`, `end`, `if`, `then`, `else`, `while`, `do`, `read`, `write`, `true`, `false`, `integer`, `char`, `boolean`, `div`, `or`, `and`, `not`
- Identificadores e nomes de variáveis
- Constantes inteiras
- Constantes de caractere
- Operadores aritméticos: `+`, `-`, `*`, `div`
- Operadores relacionais: `=`, `<>`, `<`, `<=`, `>`, `>=`
- Operadores lógicos: `or`, `and`, `not`
- Atribuição: `:=`
- Delimitadores: `;`, `:`, `,`, `(`, `)`, `[`, `]`, `.`, `..`

## Estrutura do projeto

- `src/lexer/lexer.py` - implementação do lexer e análise léxica.
- `src/lexer/tokens.py` - definições de tokens e tipos de token.
- `src/lexer/ai_suggestions.py` - suporte a sugestões de correção com IA.
- `src/lexer/tests.py` - arquivo de testes / exemplos de uso.

## Como usar

1. Coloque o código Pascal em uma string.
2. Instancie `Lexer` com o código fonte.
3. Chame `tokenize()` para obter a lista de tokens e erros.

Exemplo básico:

```python
from lexer.lexer import Lexer

source = "program exemplo; begin x := 10; end."
lexer = Lexer(source)
tokens, errors = lexer.tokenize()

for token in tokens:
    print(token)

if errors:
    print("Erros léxicos:")
    for err in errors:
        print(err)
```

## Usar a GUI com backend Python

1. Inicie o servidor Python:
   ```bash
   python3 src/server.py
   ```
2. Abra a aplicação no navegador em `http://127.0.0.1:8000`.

## Observações

- O projeto é focado apenas na análise léxica, não na análise sintática ou semântica completa.
- Existe integração inicial com IA para sugestões de token inválido, mas a implementação pode exigir configuração de credenciais OpenAI.
- Ainda é um projeto de base e pode ser ampliado para um compilador mini-Pascal completo.
