from enum import Enum

class TokenType(Enum):
    # Palavras Reservadas (Keywords)
    PROGRAM = 'PROGRAM'
    VAR = 'VAR'
    ARRAY = 'ARRAY'
    OF = 'OF'
    BEGIN = 'BEGIN'
    END = 'END'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    DO = 'DO'
    READ = 'READ'
    WRITE = 'WRITE'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    CHAR = 'CHAR'
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    FUNCTION = 'FUNCTION'
    PROCEDURE = 'PROCEDURE'
    
    # Operadores que são palavras (também Keywords)
    DIV = 'DIV'
    OR = 'OR'
    AND = 'AND'
    NOT = 'NOT'

    # Identificadores e Constantes
    IDENTIFIER = 'IDENTIFIER'
    INT_CONST = 'INTEGER_CONSTANT'
    CHAR_CONST = 'CHARACTER_CONSTANT'

    # Símbolos Especiais
    PLUS = 'PLUS'           # +
    MINUS = 'MINUS'         # -
    MULTIPLY = 'MULTIPLY'   # *
    EQUAL = 'EQUAL'         # =
    NOT_EQUAL = 'NOT_EQUAL' # <>
    LESS = 'LESS'           # <
    GREATER = 'GREATER'     # >
    LESS_EQUAL = 'LESS_EQUAL' # <=
    GREATER_EQUAL = 'GREATER_EQUAL' # >=
    LPAREN = 'LPAREN'       # (
    RPAREN = 'RPAREN'       # )
    LBRACKET = 'LBRACKET'   # [
    RBRACKET = 'RBRACKET'   # ]
    ASSIGN = 'ASSIGN'       # :=
    DOT = 'DOT'             # .
    COMMA = 'COMMA'         # ,
    SEMICOLON = 'SEMICOLON' # ;
    COLON = 'COLON'         # :
    DOTDOT = 'DOTDOT'       # ..

    # Diversos
    EOF = 'EOF'
    ERROR = 'ERROR'

class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int, column: int):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', line={self.line}, col={self.column})"
