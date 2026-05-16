import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
import sys
import os

# Ajusta o path para importar o lexer da pasta src/lexer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer.lexer import Lexer
from lexer.syntax_highlighter import SyntaxHighlighter

class MiniPascalGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mini-Pascal Lexical Analyzer")
        self.geometry("1100x700")
        
        # Configuração de grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Mini-Pascal Lexer IDE", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left", padx=20)

        self.open_btn = ctk.CTkButton(self.header_frame, text="Abrir Arquivo", command=self.open_file, width=100)
        self.open_btn.pack(side="left", padx=5)

        self.run_btn = ctk.CTkButton(self.header_frame, text="Analisar Código", command=self.run_lexer, width=100, fg_color="#28a745", hover_color="#218838")
        self.run_btn.pack(side="left", padx=5)

        # --- MAIN CONTENT ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=2) # Editor
        self.main_frame.grid_columnconfigure(1, weight=1) # Tabela
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Editor de Código
        self.editor_frame = ctk.CTkFrame(self.main_frame)
        self.editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.editor_label = ctk.CTkLabel(self.editor_frame, text="Código Fonte", font=ctk.CTkFont(weight="bold"))
        self.editor_label.pack(pady=5)
        
        self.code_editor = ctk.CTkTextbox(self.editor_frame, font=("Consolas", 14), undo=True)
        self.code_editor.pack(fill="both", expand=True, padx=10, pady=10)
        self.code_editor.insert("0.0", "program Exemplo;\nvar\n  x : integer;\nbegin\n  x := 10;\nend.")

        # Inicializa o Syntax Highlighter
        self.highlighter = SyntaxHighlighter(self.code_editor)

        # Tabela de Tokens
        self.table_frame = ctk.CTkFrame(self.main_frame)
        self.table_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.table_label = ctk.CTkLabel(self.table_frame, text="Tabela de Tokens", font=ctk.CTkFont(weight="bold"))
        self.table_label.pack(pady=5)

        # Estilo para Treeview (Tkinter padrão dentro do CustomTkinter)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=25)
        style.map("Treeview", background=[('selected', '#3a3a3a')])

        self.tree = ttk.Treeview(self.table_frame, columns=("Classe", "Lexema", "Linha"), show='headings')
        self.tree.heading("Classe", text="Classe / Categoria")
        self.tree.heading("Lexema", text="Lexema")
        self.tree.heading("Linha", text="Linha")
        self.tree.column("Classe", width=120)
        self.tree.column("Lexema", width=100)
        self.tree.column("Linha", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- FOOTER (ERROS E IA) ---
        self.error_frame = ctk.CTkFrame(self, height=150)
        self.error_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.error_label = ctk.CTkLabel(self.error_frame, text="Relatório de Erros & Sugestões IA", font=ctk.CTkFont(weight="bold"), text_color="#ff4444")
        self.error_label.pack(pady=5)

        self.error_log = ctk.CTkTextbox(self.error_frame, height=100, font=("Consolas", 12), text_color="#ffbaba", fg_color="#2b1a1a")
        self.error_log.pack(fill="both", expand=True, padx=10, pady=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pascal files", "*.pas *.p"), ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.code_editor.delete("0.0", "end")
                self.code_editor.insert("0.0", content)

    def run_lexer(self):
        # Limpar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.error_log.delete("0.0", "end")

        code = self.code_editor.get("0.0", "end")
        lexer = Lexer(code)
        tokens, errors = lexer.tokenize()

        # Atualiza o Realce de Sintaxe
        self.highlighter.highlight(tokens, errors)

        # Preencher Tabela
        for token in tokens:
            if token.type.value != "EOF":
                self.tree.insert("", "end", values=(token.type.value, token.lexeme, token.line))

        # Preencher Erros
        if not errors:
            self.error_log.insert("end", "Nenhum erro léxico detectado. Código limpo!")
        else:
            for err in errors:
                msg = f"[ERRO] Linha {err['line']}, Col {err['column']}: {err['message']}\n"
                if err['suggestion'] and err['suggestion'] != "No suggestion":
                    msg += f"       -> {err['suggestion']}\n"
                self.error_log.insert("end", msg + "-"*50 + "\n")

if __name__ == "__main__":
    app = MiniPascalGUI()
    app.mainloop()
