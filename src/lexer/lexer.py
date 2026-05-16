try:
    from .tokens import Token, TokenType
    from .error_recovery import ErrorRecovery
except ImportError:
    from tokens import Token, TokenType
    from error_recovery import ErrorRecovery


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current_char = self.source[0] if self.length > 0 else None

        self.recovery = ErrorRecovery()

        self.keywords = {
            'program': TokenType.PROGRAM,
            'var': TokenType.VAR,
            'array': TokenType.ARRAY,
            'of': TokenType.OF,
            'begin': TokenType.BEGIN,
            'end': TokenType.END,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'read': TokenType.READ,
            'write': TokenType.WRITE,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'char': TokenType.CHAR,
            'integer': TokenType.INTEGER,
            'boolean': TokenType.BOOLEAN,
            'function': TokenType.FUNCTION,
            'procedure': TokenType.PROCEDURE,
            'div': TokenType.DIV,
            'or': TokenType.OR,
            'and': TokenType.AND,
            'not': TokenType.NOT,
        }

        self.tokens = []
        self.errors = []

    def advance(self):
        if self.pos < self.length - 1:
            self.pos += 1
            self.col += 1
            self.current_char = self.source[self.pos]
        else:
            self.pos = self.length
            self.current_char = None

    def peek(self):
        if self.pos + 1 < self.length:
            return self.source[self.pos + 1]
        return None

    def skip_whitespace_and_comments(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Comentário { ... }
            if self.current_char == '{':
                self.advance()
                while self.current_char and self.current_char != '}':
                    if self.current_char == '\n':
                        self.line += 1
                        self.col = 0
                    self.advance()
                
                if self.current_char == '}':
                    self.advance()
                else:
                    self.add_error("Unterminated comment '{'", self.line, self.col)
                continue
            break

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.col = 0
            self.advance()

    def read_identifier_or_keyword(self):
        start_col = self.col
        start_line = self.line
        result = ''

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == '_'
        ):
            result += self.current_char
            self.advance()

        word = result.lower()

        if word in self.keywords:
            return Token(self.keywords[word], result, start_line, start_col)

        # Mecanismo de Recuperação / Sugestão de Typo
        suggestion = self.recovery.suggest(result)
        if suggestion and "Did you mean" in suggestion:
            self.add_error(f"Possible keyword typo: '{result}'", start_line, start_col, result)
            return Token(TokenType.ERROR, result, start_line, start_col)

        return Token(TokenType.IDENTIFIER, result, start_line, start_col)

    def read_number(self):
        start_col = self.col
        start_line = self.line
        result = ''

        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char and (self.current_char.isalpha() or self.current_char == '_'):
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                result += self.current_char
                self.advance()
            self.add_error(f"Malformed number: '{result}'", start_line, start_col, result)
            return Token(TokenType.ERROR, result, start_line, start_col)

        return Token(TokenType.INT_CONST, result, start_line, start_col)

    def read_char_constant(self):
        start_col = self.col
        start_line = self.line
        self.advance() # '
        result = ''

        while self.current_char and self.current_char != "'":
            result += self.current_char
            self.advance()

        if self.current_char == "'":
            self.advance()
        else:
            self.add_error("Unterminated character constant", start_line, start_col, result)

        return Token(TokenType.CHAR_CONST, result, start_line, start_col)

    def read_special_symbol(self):
        start_col = self.col
        start_line = self.line
        char = self.current_char
        next_char = self.peek()

        # Operadores Duplos
        if char == ':' and next_char == '=':
            self.advance(); self.advance()
            return Token(TokenType.ASSIGN, ':=', start_line, start_col)
        if char == '<' and next_char == '>':
            self.advance(); self.advance()
            return Token(TokenType.NOT_EQUAL, '<>', start_line, start_col)
        if char == '<' and next_char == '=':
            self.advance(); self.advance()
            return Token(TokenType.LESS_EQUAL, '<=', start_line, start_col)
        if char == '>' and next_char == '=':
            self.advance(); self.advance()
            return Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col)
        if char == '.' and next_char == '.':
            self.advance(); self.advance()
            return Token(TokenType.DOTDOT, '..', start_line, start_col)

        symbols = {
            '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MULTIPLY,
            '=': TokenType.EQUAL, '<': TokenType.LESS, '>': TokenType.GREATER,
            '(': TokenType.LPAREN, ')': TokenType.RPAREN, '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET, '.': TokenType.DOT, ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON, ':': TokenType.COLON,
        }

        if char in symbols:
            self.advance()
            return Token(symbols[char], char, start_line, start_col)

        self.add_error(f"Invalid character: '{char}'", start_line, start_col, char)
        self.advance()
        return Token(TokenType.ERROR, char, start_line, start_col)

    def add_error(self, message, line, col, invalid_token=None):
        suggestion = self.recovery.suggest(invalid_token) if invalid_token else None
        self.errors.append({
            'message': message, 'line': line, 'column': col,
            'token': invalid_token, 'suggestion': suggestion
        })

    def get_next_token(self):
        self.skip_whitespace_and_comments()
        if not self.current_char:
            return Token(TokenType.EOF, '', self.line, self.col)
        if self.current_char.isalpha() or self.current_char == '_':
            return self.read_identifier_or_keyword()
        if self.current_char.isdigit():
            return self.read_number()
        if self.current_char == "'":
            return self.read_char_constant()
        return self.read_special_symbol()

    def tokenize(self):
        self.tokens = []
        self.errors = []
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return self.tokens, self.errors
