try:
    from .tokens import TokenType
except ImportError:
    from tokens import TokenType

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget

        # Cores modernas para Dark Mode
        self.colors = {
            "keyword": "#569cd6",    # Azul
            "identifier": "#9cdcfe", # Azul claro
            "number": "#b5cea8",    # Verde claro
            "string": "#ce9178",    # Laranja/Marrom
            "comment": "#6a9955",   # Verde comentário
            "symbol": "#d4d4d4",    # Cinza claro
            "error": "#f44747",      # Vermelho
        }

        for tag, color in self.colors.items():
            self.text_widget.tag_config(tag, foreground=color)

    def highlight(self, tokens, errors):
        # Limpa cores antigas
        for tag in self.colors:
            self.text_widget.tag_remove(tag, "1.0", "end")

        # Colorir Tokens
        for token in tokens:
            if token.type == TokenType.EOF: continue
            
            # Cálculo de posição para o Tkinter (linha.coluna)
            # O Tkinter usa colunas baseadas em 0
            start = f"{token.line}.{token.column - 1}"
            end = f"{token.line}.{token.column - 1 + len(token.lexeme)}"

            tag = self._get_tag(token.type)
            if tag:
                self.text_widget.tag_add(tag, start, end)

    def _get_tag(self, token_type):
        name = token_type.name
        if name in [
            "PROGRAM", "VAR", "ARRAY", "OF", "BEGIN", "END",
            "IF", "THEN", "ELSE", "WHILE", "DO", "READ", "WRITE",
            "TRUE", "FALSE", "INTEGER", "CHAR", "BOOLEAN", "DIV", "OR", "AND", "NOT"
        ]:
            return "keyword"
        if token_type == TokenType.IDENTIFIER:
            return "identifier"
        if token_type == TokenType.INT_CONST:
            return "number"
        if token_type == TokenType.CHAR_CONST:
            return "string"
        if token_type == TokenType.ERROR:
            return "error"
        return "symbol"
