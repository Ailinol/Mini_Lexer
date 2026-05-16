import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys
import os
import webbrowser
import threading
import time

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return Path(base_path) / relative_path

if getattr(sys, 'frozen', False):
    GUI_DIR = get_resource_path('GUI')
    sys.path.insert(0, str(get_resource_path('')))
else:
    GUI_DIR = Path(__file__).parent / 'GUI'
    sys.path.insert(0, str(Path(__file__).parent))

from lexer.lexer import Lexer

class BackendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(GUI_DIR), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/tokenize':
            self.handle_tokenize()
        elif self.path == '/api/ask-ai':
            self.handle_ask_ai()
        else:
            self.send_error(404)

    def handle_tokenize(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            payload = json.loads(body)
            source = payload.get('source', '')
            lexer = Lexer(source)
            tokens, errors = lexer.tokenize()
            
            response = json.dumps({
                'tokens': [{'linha': t.line, 'coluna': t.column, 'lexema': t.lexeme, 'classe': t.type.value} for t in tokens],
                'errors': [{'msg': e.get('message',''), 'lexema': e.get('token',''), 'linha': e.get('line',0), 'coluna': e.get('column',0), 'sugestao': e.get('suggestion','')} for e in errors]
            }).encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response)
        except Exception as e:
            self.send_error(500, str(e))

    def handle_ask_ai(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            payload = json.loads(body)
            question = payload.get('question', '')
            context = payload.get('context', '')
            
            API_KEY = "AIzaSyB0yXizix_1m6Fli7oA8fHTZIgqqhf_UGQ"
            
            if not API_KEY or API_KEY == "COLOQUE_A_SUA_API_KEY_AQUI" or len(API_KEY) < 10:
                answer = "A API Key não está configurada! 🛑\n\nPor favor, abra o ficheiro `src/server.py` e coloque a sua chave do Google Gemini na variável `API_KEY`."
            else:
                prompt = f"{context}\n\nPergunta do utilizador:\n{question}"
                answer = self.call_gemini_api(prompt, API_KEY)
                
            response = json.dumps({'answer': answer}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response)
        except Exception as e:
            self.send_error(500, str(e))

    def call_gemini_api(self, prompt, api_key):
        import urllib.request
        import urllib.error
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {
                "parts": [{"text": "És um assistente pedagógico especializado em compiladores e análise léxica para o mini-Pascal da UEM. Responde sempre em Português.\nRegras rigorosas deste lexer mini-Pascal:\n1. Palavras-chave permitidas: PROGRAM, VAR, ARRAY, OF, BEGIN, END, IF, THEN, ELSE, WHILE, DO, READ, WRITE, TRUE, FALSE, CHAR, INTEGER, BOOLEAN, FUNCTION, PROCEDURE.\n2. Operadores-palavra: DIV, OR, AND, NOT.\n3. Símbolos Especiais: + - * = <> < > <= >= ( ) [ ] := . , ; : ..\n4. Identificadores: Letra seguida de letras, números ou underscore (_). Case-insensitive.\n5. Constantes Inteiras (INT_CONST): Apenas dígitos. Não suporta floats (vírgula flutuante).\n6. Constantes de Caracter/String (CHAR_CONST): Delimitadas por aspas simples (').\n7. Comentários: Usam chavetas { ... } e podem ter múltiplas linhas.\nUsa estas regras para explicar os tokens ou ajudar a corrigir erros reportados aos utilizadores."}]
            }
        }
        
        import time
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    return text if text else "O modelo não retornou nenhuma resposta."
            except urllib.error.HTTPError as e:
                if e.code == 503:
                    print(f"API Error 503 (Serviço indisponível). Tentativa {attempt+1}/3. A aguardar 2 segundos...")
                    time.sleep(2)
                    continue
                error_body = getattr(e, 'read', lambda: b'')().decode('utf-8', errors='ignore')
                print(f"API Error: {error_body}")
                return f"Erro na API ({e.code}). Detalhes: {error_body[:100]}"
            except Exception as e:
                print(f"Request Error: {e}")
                return "Ocorreu um erro de ligação ao tentar contactar a API do assistente."
        
        return "Erro na API (503). O serviço do Google Gemini está temporariamente indisponível devido a elevada carga. Tente novamente mais tarde."

if __name__ == '__main__':
    PORT = 8001
    url = f'http://127.0.0.1:{PORT}'
    server = ThreadingHTTPServer(('127.0.0.1', PORT), BackendHandler)
    print(f'Servidor mini-Pascal iniciado em {url}')
    
    # Abertura robusta do navegador (pular se estiver no Electron)
    def open_browser():
        if os.environ.get('ELECTRON_RUNNING') == 'true':
            print("Running inside Electron, skipping auto browser open.")
            return
        time.sleep(1.5)
        webbrowser.open(url)
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()
