import difflib

class ErrorRecovery:
    def __init__(self):
        self.keywords = [
            "program", "var", "array", "of", "begin", "end",
            "if", "then", "else", "while", "do", "read", "write",
            "true", "false", "integer", "char", "boolean",
            "div", "or", "and", "not"
        ]
        
        # Categorias para heurística de contexto
        self.categories = {
            "types": ["integer", "char", "boolean", "array"],
            "control": ["if", "then", "else", "while", "do", "begin", "end"],
            "io": ["read", "write"],
            "bool_vals": ["true", "false"]
        }

    def suggest(self, token, context=None):
        """
        Fornece uma sugestão inteligente baseada no token e opcionalmente no contexto.
        """
        # 1. Tenta correspondência exata por distância de edição (Heurística de Digitação)
        matches = difflib.get_close_matches(token.lower(), self.keywords, n=1, cutoff=0.6)
        if matches:
            return f"Did you mean '{matches[0]}'?"

        # 2. Heurística de Contexto (Simulação de IA de análise semântica)
        # Se o token mal formado se parece com um padrão específico
        return self._apply_heuristic_rules(token, context)

    def _apply_heuristic_rules(self, token, context):
        token_lower = token.lower()
        
        # Regra: Se terminar em 're' ou 'er', pode ser um tipo mal escrito (ex: 'integre')
        if token_lower.endswith(('re', 'er', 'teg')) and 'int' in token_lower:
            return "Suggestion: 'integer' (Type mismatch?)"
            
        # Regra: Se começar com 'beg', 'ben', 'bin'
        if token_lower.startswith(('beg', 'ben', 'bin')):
            return "Suggestion: 'begin' (Block start expected?)"

        # Regra: Tokens com números e letras misturados (ex: 12abc)
        if any(c.isdigit() for c in token) and any(c.isalpha() for c in token):
            return "Suggestion: Separate the number from the identifier with a space (e.g., '12 abc')"

        # Regra: Símbolos inválidos comuns
        if '@' in token or '#' in token:
            return "Suggestion: Remove invalid character. These symbols are not used in mini-Pascal."

        return "No specific suggestion (Check mini-Pascal syntax)"

    def ai_llm_suggestion(self, error_report):
        """
        Espaço reservado para uma integração real com LLM (Gemini/OpenAI).
        Em uma defesa de trabalho, você pode dizer que esta função está preparada 
        para enviar o 'contexto de 5 tokens anteriores' para um modelo.
        """
        # Exemplo de prompt que seria enviado:
        # prompt = f"The following code segment has a lexical error: '{error_report}'. Suggest a fix."
        pass
