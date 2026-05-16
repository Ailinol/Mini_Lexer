from tkinter import filedialog

class FileManager:

    def __init__(self):
        self.current_file = None

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Pascal Files", "*.pas"), ("Text Files", "*.txt")]
        )

        if not path:
            return None

        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        self.current_file = path
        return content

    def save_file(self, content):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            return self.save_as(content)

    def save_as(self, content):
        path = filedialog.asksaveasfilename(
            defaultextension=".pas",
            filetypes=[("Pascal Files", "*.pas")]
        )

        if not path:
            return

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

        self.current_file = path