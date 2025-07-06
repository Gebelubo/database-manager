import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import tkinter as tk
from tkinter import messagebox

try:
    from interfaceAluno import iniciar_interface as iniciar_interface_aluno
    from interfaceCurso import iniciar_interface_curso
    from interfaceProfessor import iniciar_interface_professor
    from interfaceDisciplina import iniciar_interface_disciplina
    from interfaceMatricula import iniciar_interface_matricula
    from interfaceOfertaCurso import iniciar_interface_oferta
    from interfacePerfil import iniciar_interface as iniciar_interface_perfil
except ImportError as e:
    # Mensagem de erro amigável se algum módulo não for encontrado
    tk.Tk().withdraw()
    messagebox.showerror("Erro de Importação", f"Erro ao importar módulos:\n{e}")
    sys.exit(1)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500

class SistemaGestaoCursos:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Sistema de Gerenciamento de Cursos")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.center_window()

        # Menu superior
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        modulos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=modulos_menu)

        modulos_menu.add_command(label="Alunos", command=iniciar_interface_aluno)
        modulos_menu.add_command(label="Cursos", command=iniciar_interface_curso)
        modulos_menu.add_command(label="Professores", command=iniciar_interface_professor)
        modulos_menu.add_command(label="Disciplinas", command=iniciar_interface_disciplina)
        modulos_menu.add_command(label="Matrículas", command=iniciar_interface_matricula)
        modulos_menu.add_command(label="Ofertas de Curso", command=iniciar_interface_oferta)

        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Botões com cores
        modules = self.get_modules()
        for text, command, color in modules:
            btn = tk.Button(
                main_frame,
                text=f"Gerenciar {text}",
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10),
                relief=tk.RAISED,
                bd=2,
                activebackground=color,
                activeforeground="white"
            )
            btn.pack(fill=tk.X, pady=5, ipady=8)

        # Botão sair
        btn_sair = tk.Button(
            main_frame,
            text="Sair do Sistema",
            command=self.on_close,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=2,
            activebackground="#d32f2f",
            activeforeground="white"
        )
        btn_sair.pack(fill=tk.X, pady=(20, 0), ipady=8)

        # Evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        self.root.update_idletasks()
        width = WINDOW_WIDTH
        height = WINDOW_HEIGHT
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def get_modules(self):
        return [
            ("Alunos", iniciar_interface_aluno, "#4CAF50"),
            ("Cursos", iniciar_interface_curso, "#2196F3"),
            ("Professores", iniciar_interface_professor, "#FF9800"),
            ("Disciplinas", iniciar_interface_disciplina, "#9C27B0"),
            ("Matrículas", iniciar_interface_matricula, "#607D8B"),
            ("Ofertas de Curso", iniciar_interface_oferta, "#009688"),
            ("Perfis de Professor", iniciar_interface_perfil, "#795548")  # NOVO
        ]

    def on_close(self, event=None):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?", parent=self.root):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = SistemaGestaoCursos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
