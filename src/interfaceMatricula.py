import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_matriculas,
    inserir_matricula,
    buscar_matricula,
    atualizar_matricula,
    remover_matricula,
    listar_alunos,
    listar_disciplinas
)

def iniciar_interface_matricula():
    janela = tk.Toplevel()
    janela.title("Gestão de Matrículas")
    janela.geometry("700x520")

    # Frame principal
    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    # Campos de entrada
    entry_id_aluno = tk.Entry(main_frame)
    entry_id_disc = tk.Entry(main_frame)
    entry_semestre = tk.Entry(main_frame)
    entry_nota = tk.Entry(main_frame)

    # Layout dos campos
    tk.Label(main_frame, text="ID Aluno").grid(row=0, column=0, sticky="e")  # obrigatório
    entry_id_aluno.grid(row=0, column=1)

    tk.Label(main_frame, text="ID Disciplina").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_id_disc.grid(row=1, column=1)

    tk.Label(main_frame, text="Semestre").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_semestre.grid(row=2, column=1)

    tk.Label(main_frame, text="Nota (opcional)").grid(row=3, column=0, sticky="e")
    entry_nota.grid(row=3, column=1)

    tk.Label(main_frame, text="Status (opcional)").grid(row=4, column=0, sticky="e")
    # Listbox para mostrar matrículas
    lista = tk.Listbox(janela, width=90, height=15)
    lista.pack(pady=10)

    # Funções de operação
    def mostrar_matriculas():
        lista.delete(0, tk.END)
        for mat in listar_matriculas():
            nota = mat[3] if mat[3] is not None else "N/A"
            lista.insert(tk.END, f"Aluno: {mat[0]} | Disciplina: {mat[1]} | Semestre: {mat[2]} | Nota: {nota}")

    def adicionar_matricula():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            semestre = entry_semestre.get().strip()
            if not semestre:
                messagebox.showwarning("Atenção", "Semestre é obrigatório.")
                return
            nota_str = entry_nota.get().strip()
            nota = float(nota_str) if nota_str else None

            inserir_matricula(id_aluno, id_disc, semestre, nota)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula adicionada com sucesso!")

            # Limpa os campos após adição
            entry_id_aluno.delete(0, tk.END)
            entry_id_disc.delete(0, tk.END)
            entry_semestre.delete(0, tk.END)
            entry_nota.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros e nota deve ser número decimal válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_matricula_gui():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            semestre = entry_semestre.get().strip() or None
            nota_str = entry_nota.get().strip()
            nota = float(nota_str) if nota_str else None

            if semestre is None and nota is None:
                messagebox.showwarning("Atenção", "Informe ao menos semestre ou nota para atualizar.")
                return

            atualizar_matricula(id_aluno, id_disc, semestre=semestre, nota=nota)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula atualizada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros e nota deve ser um número decimal.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_matricula_gui():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            remover_matricula(id_aluno, id_disc)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula removida com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_matricula_gui():
        try:
            id_aluno_str = entry_id_aluno.get().strip()
            id_disc_str = entry_id_disc.get().strip()

            if not id_aluno_str or not id_disc_str:
                messagebox.showwarning("Atenção", "Digite ambos IDs (Aluno e Disciplina) para buscar.")
                return

            id_aluno = int(id_aluno_str)
            id_disc = int(id_disc_str)

            mat = buscar_matricula(id_aluno, id_disc)
            lista.delete(0, tk.END)
            if mat:
                nota = mat[3] if mat[3] is not None else "N/A"
                lista.insert(tk.END, f"Aluno: {mat[0]} | Disciplina: {mat[1]} | Semestre: {mat[2]} | Nota: {nota}")
            else:
                messagebox.showinfo("Resultado", "Matrícula não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # Frame de botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botões de ação
    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_ids(), adicionar_matricula()])
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_ids(), atualizar_matricula_gui()])
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_ids(), remover_matricula_gui()])
    btn_remover.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="Buscar", width=12, command=lambda: [mostrar_ids(), buscar_matricula_gui()])
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_matriculas)
    btn_listar.grid(row=1, column=1, padx=5, pady=5)

    # Mostra as matrículas ao iniciar
    mostrar_matriculas()

if __name__ == "__main__":
    iniciar_interface_matricula()
    tk.mainloop()